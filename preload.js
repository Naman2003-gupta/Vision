const { contextBridge, ipcRenderer } = require('electron');


contextBridge.exposeInMainWorld('jarvis', {
  
  runCommand: (command) => ipcRenderer.send('run-command', command),
  
 
  openFile: (filePath) => ipcRenderer.send('open-file', filePath),
  
  
  openApp: (appName) => ipcRenderer.send('open-app', appName),
  
  
  getSystemInfo: () => ipcRenderer.invoke('get-system-info'),
  
  
  sendToAI: (message) => ipcRenderer.invoke('send-to-ai', message),
  
  
  onCommandResult: (callback) => 
    ipcRenderer.on('command-result', (_, data) => callback(data)),
  
  onAIResponse: (callback) => 
    ipcRenderer.on('ai-response', (_, data) => callback(data)),
  
  
  removeAllListeners: (channel) => 
    ipcRenderer.removeAllListeners(channel),
});


contextBridge.exposeInMainWorld('electronAPI', {
  platform: process.platform,
  version: process.versions.electron,
});
