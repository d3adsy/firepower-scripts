#%%
from netmiko import ConnectHandler
from datetime import datetime
from getpass import getpass
import csv
#
user =input ("Firepower Username: ")
user_password =getpass("Password: ")
type = "generic_termserver"
#
#lists
Non_Compliant = []
hosts = []
#lists
#
#opening csv file
with open ('test.csv', mode='r', encoding='utf-8-sig') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    for row in readCSV:
        hosts.append (row[0])
        
for hosts in hosts:
    try:
        device = ConnectHandler(device_type=type, ip=hosts, username=user, password=user_password)
        device.send_command_timing("scope system")
        device.send_command_timing("scope services")
        show_tls = device.send_command_timing("show")
        #print(show_tls)
        show_tls_response = show_tls.splitlines()
        #print(show_tls_response)
        tls_1 = "Tls Ver: V1 1"
        for line in show_tls_response:
            if tls_1 in line:
                print(f"Tls 1.1 was found enabled on " + hosts + ". Adding device to non-compliant list.")
                Non_Compliant.append(hosts)
    except Exception as e:
        print(e)
#
if Non_Compliant == []:
    exit ("All devices seem to be using tls v1.2, script will now exit.")
else:
    print ("The following devices were not compliant")
    print (Non_Compliant)

    if input("Do you want to update non-compliant devices to TLS version 1.2? (y/n)") != "y":
        exit("You input something other than 'y', I assume this is intentional and you do not wish to continue. Goodbye!")
#
for Non_Compliant in Non_Compliant:
    try:
        device = ConnectHandler(device_type=type, ip=Non_Compliant, username=user, password=user_password)
        device.send_command_timing("scope system")
        device.send_command_timing("set services tls-ver v1_2")
        device.send_command_timing("commit-buffer")
        device.send_command_timing("scope services")
        show_tls = device.send_command_timing("show")
        #print(show_tls)
        show_tls_response = show_tls.splitlines()
        #print(show_tls_response)
        tls_1 = "Tls Ver: V1 2"
        for line in show_tls_response:
            if tls_1 in line:
                print(f"TLS succesfully updated to v1.2 on " + Non_Compliant + ".")
    except Exception as e:
        print(e)
print ("Finished")
#
#%%