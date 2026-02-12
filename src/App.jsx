import { useEffect, useMemo, useRef, useState } from "react";

const QUICK_COMMANDS = [
  "what time is it",
  "system info",
  "open app calculator",
  "ask what is artificial intelligence"
];

const MODE_TEXT = {
  idle: "Standby",
  listening: "Listening",
  speaking: "Speaking"
};

function getRecognitionCtor() {
  return window.SpeechRecognition || window.webkitSpeechRecognition || null;
}

function parseCommand(input) {
  const text = input.toLowerCase().trim();
  if (text.startsWith("run ")) {
    return { kind: "run", value: input.slice(4).trim() };
  }
  if (text.startsWith("open app ")) {
    return { kind: "openApp", value: input.slice(9).trim() };
  }
  if (text.startsWith("open file ")) {
    return { kind: "openFile", value: input.slice(10).trim() };
  }
  if (text.startsWith("ask ")) {
    return { kind: "askAI", value: input.slice(4).trim() };
  }
  if (text.includes("system info") || text.includes("system status")) {
    return { kind: "sysInfo", value: "" };
  }
  if (text.includes("time")) {
    return { kind: "localTime", value: "" };
  }
  if (text.includes("date")) {
    return { kind: "localDate", value: "" };
  }
  return { kind: "fallback", value: input };
}

export default function App() {
  const [mode, setMode] = useState("idle");
  const [transcript, setTranscript] = useState("No command captured yet.");
  const [reply, setReply] = useState("Jarvis core online. Awaiting input.");
  const [lastResult, setLastResult] = useState("No IPC result yet.");
  const [speechSupport, setSpeechSupport] = useState(true);
  const recognitionRef = useRef(null);
  const bars = useMemo(() => Array.from({ length: 18 }, (_, i) => i), []);

  const speak = (text) => {
    if (!("speechSynthesis" in window)) {
      setMode("idle");
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1.05;
    utterance.onstart = () => setMode("speaking");
    utterance.onend = () => setMode("idle");
    utterance.onerror = () => setMode("idle");
    window.speechSynthesis.speak(utterance);
  };

  const handleParsedCommand = async (parsed) => {
    if (!window.jarvis) {
      const msg = "IPC bridge not available.";
      setReply(msg);
      speak(msg);
      return;
    }

    if (parsed.kind === "run" && parsed.value) {
      setReply(`Running command: ${parsed.value}`);
      window.jarvis.runCommand(parsed.value);
      return;
    }

    if (parsed.kind === "openApp" && parsed.value) {
      setReply(`Opening app: ${parsed.value}`);
      window.jarvis.openApp(parsed.value);
      return;
    }

    if (parsed.kind === "openFile" && parsed.value) {
      setReply(`Opening file: ${parsed.value}`);
      window.jarvis.openFile(parsed.value);
      return;
    }

    if (parsed.kind === "sysInfo") {
      const info = await window.jarvis.getSystemInfo();
      const text = `System ${info.platform}, ${info.cpus} CPU cores, ${info.totalMemory} total memory.`;
      setReply(text);
      setLastResult(JSON.stringify(info, null, 2));
      speak(text);
      return;
    }

    if (parsed.kind === "askAI" && parsed.value) {
      const response = await window.jarvis.sendToAI(parsed.value);
      const text = response?.response || "No AI response.";
      setReply(text);
      setLastResult(JSON.stringify(response, null, 2));
      speak(text);
      return;
    }

    if (parsed.kind === "localTime") {
      const timeText = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
      });
      const text = `The time is ${timeText}.`;
      setReply(text);
      speak(text);
      return;
    }

    if (parsed.kind === "localDate") {
      const dateText = new Date().toLocaleDateString(undefined, {
        weekday: "long",
        month: "long",
        day: "numeric",
        year: "numeric"
      });
      const text = `Today is ${dateText}.`;
      setReply(text);
      speak(text);
      return;
    }

    const fallback = "Command recognized. Say: run, open app, open file, ask, or system info.";
    setReply(fallback);
    speak(fallback);
  };

  const runCommandText = async (text) => {
    const cleaned = text.trim();
    if (!cleaned) {
      const msg = "I did not catch that command.";
      setReply(msg);
      speak(msg);
      return;
    }
    setTranscript(cleaned);
    await handleParsedCommand(parseCommand(cleaned));
  };

  const startListening = () => {
    const Recognition = getRecognitionCtor();
    if (!Recognition) {
      setSpeechSupport(false);
      setReply("Speech recognition is unavailable in this runtime.");
      return;
    }

    setSpeechSupport(true);
    if (!recognitionRef.current) {
      const recognition = new Recognition();
      recognition.lang = "en-US";
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onresult = (event) => {
        const text = event.results?.[0]?.[0]?.transcript || "";
        runCommandText(text);
      };

      recognition.onend = () => {
        setMode((current) => (current === "listening" ? "idle" : current));
      };

      recognition.onerror = (event) => {
        setReply(`Voice recognition error: ${event.error || "unknown"}`);
        setMode("idle");
      };

      recognitionRef.current = recognition;
    }

    setMode("listening");
    recognitionRef.current.start();
  };

  const stopAll = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
    setMode("idle");
  };

  useEffect(() => {
    if (!window.jarvis) {
      return undefined;
    }

    const commandResultHandler = (data) => {
      if (data.success) {
        const output = data.output || data.error || "Action completed.";
        setLastResult(output.trim() || "Action completed.");
        const spoken = "Action completed.";
        setReply(spoken);
        speak(spoken);
      } else {
        const err = data.error || "Unknown error.";
        setLastResult(err);
        const spoken = `Operation failed. ${err}`;
        setReply(spoken);
        speak(spoken);
      }
    };

    window.jarvis.onCommandResult(commandResultHandler);

    return () => {
      if (window.jarvis?.removeAllListeners) {
        window.jarvis.removeAllListeners("command-result");
      }
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  return (
    <div className={`app mode-${mode}`}>
      <div className="bg-grid" />
      <div className="bg-glow bg-glow-a" />
      <div className="bg-glow bg-glow-b" />

      <header className="topbar">
        <div>
          <p className="eyebrow">Vision Assistant</p>
          <h1>Jarvis Interface</h1>
        </div>
        <div className="mode-pill">{MODE_TEXT[mode]}</div>
      </header>

      <main className="layout">
        <section className="orbital-panel">
          <div className="core">
            <div className="ring ring-1" />
            <div className="ring ring-2" />
            <div className="ring ring-3" />
            <div className="nucleus" />
          </div>
          <div className="wave">
            {bars.map((bar) => (
              <span key={bar} className="bar" style={{ "--i": bar }} />
            ))}
          </div>
        </section>

        <section className="status-panel">
          <div className="card">
            <h2>Captured Command</h2>
            <p>{transcript}</p>
          </div>

          <div className="card">
            <h2>Jarvis Reply</h2>
            <p>{reply}</p>
          </div>

          <div className="card">
            <h2>IPC Result</h2>
            <pre>{lastResult}</pre>
          </div>

          <div className="actions">
            <button onClick={startListening} className="btn btn-primary">
              Start Listening
            </button>
            <button onClick={stopAll} className="btn btn-secondary">
              Stop
            </button>
            <button onClick={() => runCommandText("system info")} className="btn btn-secondary">
              System Info
            </button>
          </div>

          <div className="quick">
            {QUICK_COMMANDS.map((command) => (
              <button key={command} onClick={() => runCommandText(command)} className="chip">
                {command}
              </button>
            ))}
          </div>

          {!speechSupport && <p className="warning">Speech recognition unavailable in this runtime.</p>}
        </section>
      </main>
    </div>
  );
}

