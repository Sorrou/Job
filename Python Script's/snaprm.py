import subprocess
from datetime import date
from datetime import timedelta
import time

command = "yc compute snapshot list --folder-name="
delete_command = "yc compute snapshot delete "

info = []

ids= ["renault-mdm-test", "common-prod", "renault-dsp-test", "renault-ftp", "renault-1c-prod", "renault-dsp-prod", "default", "renault-mdm-prod", "regru", "renault-shared", "renault-shared-database", "renault-sdb-prod" ]

disk_list = []
delta = date.today() - timedelta(days=1)
count = 0

for folder in ids:
    with subprocess.Popen(command+str(folder)+ " --format=yaml", stdout=subprocess.PIPE, stderr=None, shell=True) as  process:
        output = process.communicate()[0]
        for s in output.split():
            info.append(s) 
    
    i = 0

    for d in info:
        i += 1
        if d == "name:":
            disk_list.append(info[i])

    for disk in disk_list:
        if str(delta) in disk:
            count += 1
            print(count)
            print(str(delete_command + disk + " --folder-name=" + folder))
            subprocess.Popen([delete_command + disk + " --folder-name=" + folder], shell=True)
            if count % 15 == 0:
                time.sleep(90)

    disk_list = []
    info = []