Set WshShell = CreateObject("WScript.Shell")
' Get the directory where this VBS script is located
ScriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
' Launch Python script with visible command window (1 = normal window)
WshShell.Run "python """ & ScriptDir & "\pdf_editor_complete.py""", 1, False
