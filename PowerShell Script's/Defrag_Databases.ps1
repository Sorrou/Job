#Ночная дефрагментация баз exchange, с отправкой статуса в телеграм
#База #1
$diskE = 'E:'
$baseE = 'E:\Mail_DB\BASE.edb'
#База #2
$diskF = 'F:'
$baseF = 'F:\Mail_DB\BASE2.edb'
#База #3
$diskH = 'H:'
$baseH = 'H:\Mamsy_Archive\BASE3.edb'

Function Defragmentation($Disk, $Base) {
    #Переменные
    $start_defrag= -join("Start defragmentation ", $Base)
    $stop_defrag = -join($Base, ' defragmentation is over, released ', $spaceDiff, ' GB')

    #Отправка в телегу
    Function CurlPost {
        C:\Defrag\curl.exe -s --socks5-hostname proxy.lalala.ru:80 -U User:Pass -X POST `
        "https://api.telegram.org/bot(bottoken)/sendMessage?chat_id=(chat-it)&text=$args"
        }
    
    #сколько свободного место До:
    $space = Get-WmiObject Win32_LogicalDisk -Filter "DriveType=2" -Computer localhost  | `
    Select DeviceID,@{Name="size(GB)";Expression={"{0:N1}" -f($_.size/1gb)}},@{Name="freespace(GB)";Expression={"{0:N1}" -f($_.freespace/1gb)}} 
    $spaceE_before = foreach($line in $space) {if ($line.DeviceID -eq $Disk) {$spaceE_before = $line.'freespace(GB)'}}
    
    #Начало дефрагментации
    CurlPost $start_defrag
    
    #Вырубаем сервис
    $serviceOff = net stop msexchangeis 2>&1
    $numline = 0
    foreach($line in $serviceOff) {CurlPost $line}
    
    #Запускаем дефрагментацию
    $ese = eseutil.exe /d $Base 2>&1
    foreach($line in $ese) {
        if ($numline -lt 4) {
            $numline += 1}
        else {CurlPost $line}}
    
    #Включаем сервис
    $serviceOn = net start msexchangeis 2>&1
    foreach($line in $serviceOn) {CurlPost $line}
    
    #Сколько места мы освободили
    $spaceE_after = foreach($line in $space) {if ($line.DeviceID -eq "E:") {$spaceE_after = $line.'freespace(GB)'}}
    $spaceDiff = $spaceE_after - $spaceE_before
    CurlPost $stop_defrag
}

Defragmentation $diskE $baseE
