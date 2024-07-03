__author__ = "Christian.Perla"
if __name__ == "__main__":

    def cli_cmd():

    ios_connect = {
        'device_type' : 'cisco_ios',
        'host' : 'ip',
        'username' : 'username',
        'password' : 'password',
        'port' : '22',
    }
    
    ssh_connect = ConnectHandler(**ios_connect)
    ssh_output = ssh_connect.send_command(ent_cmd.get())
