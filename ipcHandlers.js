const { ipcMain } = require('electron');
const { exec, spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

ipcMain.on('run-command', (event, command) => {
  console.log(`[IPC] Running command: ${command}`);
  
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`[IPC] Error: ${error.message}`);
      event.reply('command-result', { 
        success: false, 
        error: error.message 
      });
      return;
    }
    
    event.reply('command-result', { 
      success: true, 
      output: stdout,
      error: stderr 
    });
  });
});


ipcMain.on('open-file', (event, filePath) => {
  console.log(`[IPC] Opening file: ${filePath}`);
  
  const normalizedPath = path.normalize(filePath);
  
  if (!fs.existsSync(normalizedPath)) {
    event.reply('command-result', { 
      success: false, 
      error: 'File not found' 
    });
    return;
  }
  
  const command = process.platform === 'win32' 
    ? `start "" "${normalizedPath}"`
    : process.platform === 'darwin'
    ? `open "${normalizedPath}"`
    : `xdg-open "${normalizedPath}"`;
  
  exec(command, (error) => {
    event.reply('command-result', { 
      success: !error,
      error: error?.message 
    });
  });
});


ipcMain.on('open-app', (event, appName) => {
  console.log(`[IPC] Opening app: ${appName}`);
  
  const appCommands = {
    win32: {
      chrome: 'start chrome',
      vscode: 'code',
      notepad: 'notepad',
      explorer: 'explorer',
      calculator: 'calc',
    },
    darwin: {
      chrome: 'open -a "Google Chrome"',
      vscode: 'open -a "Visual Studio Code"',
      safari: 'open -a "Safari"',
      finder: 'open -a "Finder"',
      calculator: 'open -a "Calculator"',
    },
    linux: {
      chrome: 'google-chrome',
      vscode: 'code',
      firefox: 'firefox',
      nautilus: 'nautilus',
      calculator: 'gnome-calculator',
    },
  };
  
  const platform = process.platform;
  const command = appCommands[platform]?.[appName.toLowerCase()];
  
  if (!command) {
    event.reply('command-result', { 
      success: false, 
      error: `App "${appName}" not configured for ${platform}` 
    });
    return;
  }
  
  exec(command, (error) => {
    event.reply('command-result', { 
      success: !error,
      error: error?.message 
    });
  });
});


ipcMain.handle('get-system-info', async () => {
  return {
    platform: process.platform,
    arch: process.arch,
    hostname: os.hostname(),
    userInfo: os.userInfo().username,
    totalMemory: (os.totalmem() / 1024 / 1024 / 1024).toFixed(2) + ' GB',
    freeMemory: (os.freemem() / 1024 / 1024 / 1024).toFixed(2) + ' GB',
    cpus: os.cpus().length,
    uptime: (os.uptime() / 60 / 60).toFixed(2) + ' hours',
  };
});


ipcMain.handle('send-to-ai', async (event, message) => {
  console.log(`[IPC] AI Request: ${message}`);
  
  
  
  return {
    response: "AI integration pending - connect your API in ai-engine/",
    intent: "chat",
    confidence: 0.8,
  };
});

console.log('[IPC] All handlers registered successfully');
