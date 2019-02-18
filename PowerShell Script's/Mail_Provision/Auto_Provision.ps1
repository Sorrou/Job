cd E:\Provision\
#Делаем файлик с ящиками, которые уже есть
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -noexit -command ". 'C:\Program Files\Microsoft\Exchange Server\V15\bin\RemoteExchange.ps1'; Connect-ExchangeServer -auto; Get-Mailbox | select -expand Alias | Out-File E:\Provision\Current_Mailbox.txt -Encoding UTF8; exit" 
Start-Sleep -s 20

#смотрим учетные записи в AD, выбираем те, для которых еще нет созданых почтовых ящиков.
.\Mail_prov.py
Start-Sleep -s 30

$users = Get-Content -Path E:\Provision\New_Mailbox.txt

#Создаем почтовые ящики
foreach($line in $users) {
    C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -noexit -command ". 'C:\Program Files\Microsoft\Exchange Server\V15\bin\RemoteExchange.ps1'; Connect-ExchangeServer -auto; Enable-Mailbox -Identity $line -Database MAMSY2; exit" 
    }
Start-Sleep -s 30
Remove-Item E:\Provision\Current_Mailbox.txt
Remove-Item E:\Provision\New_Mailbox.txt
