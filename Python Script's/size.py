import subprocess
from datetime import datetime
import time

# command = "yc compute instance get --id="
command = "yc compute disk list --folder-name="
create_snapshot = "yc compute snapshot create " 

#ids= ["renault-mdm-test", "common-prod"]
ids= ["renault-mdm-test", "common-prod", "renault-dsp-test", "renault-ftp", "renault-1c-prod", "renault-dsp-prod", "default", "renault-mdm-prod", "regru", "renault-shared", "renault-shared-database", "renault-sdb-prod" ]
# ids2 = ["renault-dsp-test", "renault-ftp"]
# ids3 = ["renault-1c-prod", "renault-dsp-prod"]
# ids4 = ["default", "renault-mdm-prod"]
# ids5 = ["regru", "renault-shared"]
# ids6 = ["renault-shared-database", "renault-sdb-prod"]

info = []
disk_list = []
count = 0

for folder in ids:
    with subprocess.Popen(command+str(folder)+ " --format=yaml", stdout=subprocess.PIPE, stderr=None, shell=True) as  process:
        output = process.communicate()[0].decode("utf-8")
        for s in output.split():
            info.append(s) 

    i = 0

    for d in info:
        i += 1
        # if d == "disk_id:":
        if d == "name:":
            disk_list.append(info[i])
    
    for disk in disk_list:
        count += 1
        print(count)
        print(str(create_snapshot + disk + "-" + str(datetime.today().strftime("%Y-%m-%d-%H-%M")) + " --disk-name=" + disk + " --folder-name=" + folder))
        subprocess.Popen([create_snapshot + disk + "-" + str(datetime.today().strftime("%Y-%m-%d-%H-%M")) + " --disk-name=" + disk + " --folder-name=" + folder], shell=True)
        if count % 15 == 0:
            time.sleep(300)
    
    disk_list = []
    info = []

    # for disk in disk_list:
    #     with subprocess.Popen([create_snapshot + disk + "-" + str(datetime.today().strftime("%Y-%m-%d-%H-%M")) + " --disk-id=" + disk], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True) as snap:
    #         task = snap.communicate()

    # for disk in disk_list:
    #     with subprocess.Popen([create_snapshot + disk + "-" + str(datetime.today().strftime("%Y-%m-%d-%H-%M")) + " --disk-id=" + disk + " --folder-id=" + folder], shell=True) as Timuh:
    #         task = Timuh.communicate()
