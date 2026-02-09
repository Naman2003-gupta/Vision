import os

def handle_system(command):
    if "open chrome" in command:
        os.system("start chrome")
        return "Opening Chrome"

    if "open notepad" in command:
        os.system("notepad")
        return "Opening Notepad"
    
    if "open whatsapp" in command:
        os.system("start shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App")
        return "Opening WhatsApp"
    
    if "open firefox" in command:
        os.system("start firefox")
        return "Opening Firefox"


    if "open vscode" in command or "open vs code" in command:
        os.system("code")
        return "Opening Visual Studio Code"

    return None
  