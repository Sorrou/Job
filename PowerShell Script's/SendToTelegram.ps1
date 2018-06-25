#Переходим в папку, куда будут падать скриншоты, папка должна сужествовать, сам он её не создаст
cd D:\Screenshot

#Делаем переменную, которая будет делать сам скриншот, именется следующим образом: Название компьютера + дата создания
$screen={
$dir="D:\Screenshot"
Add-Type -AssemblyName System.Windows.Forms
$screenBounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$image = New-Object System.Drawing.Bitmap($screenBounds.Width, $screenBounds.Height)
$g = [System.Drawing.Graphics]::FromImage($image)
$p = New-Object System.Drawing.Point(0, 0)
$g.CopyFromScreen($p, $p, $image.Size);
$cursorBounds = New-Object System.Drawing.Rectangle([System.Windows.Forms.Cursor]::Position, [System.Windows.Forms.Cursor]::Current.Size)
[System.Windows.Forms.Cursors]::Default.Draw($g, $cursorBounds)
$image.Save("$dir\$(($(Get-WmiObject Win32_Computersystem).name) + " " + (get-date).tostring('yyyy.MM.dd-HH.mm.ss')).jpg",[System.Drawing.Imaging.ImageFormat]::png)
}

#Делаем скриншот, без всплывающих окон PS
powershell -executionpolicy RemoteSigned -WindowStyle Hidden $screen

#Сортируем файлы, выбираем последний, подключаем курл, и отправляем скриншот ботом в телеграм
#Определяем ID магазина
$comp = ((Get-WmiObject Win32_Computersystem).name).substring(3,2)
#Судя по ID определяем в какой чат слать скриншот
$content = (Get-Content -path D:\Screenshot\ID.txt)[$comp]
ls -File | sort LastAccessTime | select -Last 1 | ForEach-Object {.\curl --socks5-hostname IP:PORT -s -X POST "https://api.telegram.org/bot$content" -F document="@D:\Screenshot\$_"}
