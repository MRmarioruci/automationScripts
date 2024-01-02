import paramiko
import subprocess

# SSH connection parameters
hostname = '52.211.143.31'
port = 22
username = 'ubuntu'
private_key_path = '/home/mario/.ssh/id_rsa'

# Create an SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

local_folder_path = '../interviewerAI'
excluded_local_folder_path = '../interviewerAI/node_modules'
remote_folder = '~/interviewerAI'
remote_folder_path = f'{username}@{hostname}:~/'
excluded_items = ['server/node_modules/', 'client/node_modules/', '.git/', 'server/core/database.js']
rsync_args = ['-av', '-e', f'ssh -i {private_key_path}']

try:
    private_key = paramiko.RSAKey.from_private_key_file(private_key_path, 'smilemalaka0343')
    # Connect to the SSH server
    ssh.connect(hostname, port, username, pkey=private_key)

    # Install Docker
    stdin, stdout, stderr = ssh.exec_command('sudo apt update')
    print(stdout.read().decode())
    stdin, stdout, stderr = ssh.exec_command('sudo apt install docker.io -y')
    print(stdout.read().decode())
    stdin, stdout, stderr = ssh.exec_command('sudo systemctl start docker')
    print(stdout.read().decode()) 
    stdin, stdout, stderr = ssh.exec_command('sudo systemctl enable docker')
    print(stdout.read().decode()) 

    # Install Docker Compose
    stdin, stdout, stderr = ssh.exec_command('sudo apt install curl -y')
    print(stdout.read().decode())
    stdin, stdout, stderr = ssh.exec_command('sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose')
    print(stdout.read().decode())
    stdin, stdout, stderr = ssh.exec_command('sudo chmod +x /usr/local/bin/docker-compose')
    print(stdout.read().decode())

    # Verify Docker and Docker Compose installations
    stdin, stdout, stderr = ssh.exec_command('docker --version')
    print(stdout.read().decode())
    stdin, stdout, stderr = ssh.exec_command('docker-compose --version')
    print(stdout.read().decode())

    # Upload files
    for item in excluded_items:
        rsync_args.extend(['--exclude', item])

    rsync_args.extend([local_folder_path, remote_folder_path])
    subprocess.run(['rsync'] + rsync_args)

    # Start the containers ~ This will take a bit
    stdin, stdout, stderr = ssh.exec_command(f'cd ./interviewerAI && sudo docker-compose up --build -d')
    print(stdout.read().decode())

finally:
    ssh.close()