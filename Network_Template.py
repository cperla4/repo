__author__ = "Christian.Perla"
if __name__ == "__main__":

    from getpass import getpass
    
    ios_connect = {
        'device_type' : 'cisco_ios',
        'host' : 'ip',
        'username' : 'username',
        'password' : 'password',
        'port' : '22',
    }
    user_id = input('Username: ')
    pass_id = getpass('Password: ')
    host_id = input('IP: ')
    
    ios_connect['username'] = user_id
    ios_connect['password'] = pass_id
    ios_connect['host'] = host_id
    
    ssh_connect = ConnectHandler(**ios_connect)    #Runs IOS Parameters against Netmiko Terminal
    ssh_output = ssh_connect.send_command('cli show commands')    #Runs show commands in terminal
    ssh_connect.disconnect()

    print(ssh_output)    #Print results in terminal
    
    
