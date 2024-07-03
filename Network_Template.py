__author__ = "Christian.Perla"
if __name__ == "__main__":

    ios_connect = {
        'device_type' : 'cisco_ios',
        'host' : 'ip',
        'username' : 'username',
        'password' : 'password',
        'port' : '22',
    }
    
    ssh_connect = ConnectHandler(**ios_connect)    #Runs IOS Parameters against Netmiko Terminal
    ssh_output = ssh_connect.send_command('cli show commands')    #Runs show commands in terminal

    print(ssh_output)    #Print results in terminal
    
    
