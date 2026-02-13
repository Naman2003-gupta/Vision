const { app, BrowserWindow, session } = require('electron');
const path = require('path');

let mainWindow;
const MEDIA_PERMISSIONS = new Set(['media', 'microphone', 'camera']);

function configureMediaPermissions() {
  const defaultSession = session.defaultSession;
  if (!defaultSession) {
    return;
  }

  defaultSession.setPermissionRequestHandler((_, permission, callback) => {
    callback(MEDIA_PERMISSIONS.has(permission));
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 700,
    minWidth: 800,
    minHeight: 600,
    backgroundColor: '#1a1a1a',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
    frame: true,
    show: false,
  });

  const devUrl = process.env.VITE_DEV_SERVER_URL;
  const isDev = process.env.NODE_ENV === 'development' || Boolean(devUrl);

  if (isDev) {
    mainWindow.loadURL(devUrl || 'http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, 'dist', 'index.html'));
  }

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  configureMediaPermissions();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

require('./ipcHandlers');
