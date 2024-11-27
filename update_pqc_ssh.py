import os
import subprocess
from pathlib import Path
from getpass import getpass
import paramiko

# Paths and settings
OQS_ALGORITHM = "ecdsa-p256+kyber512"
SSH_DIR = Path.home() / ".ssh"
NEW_KEY_FILE = SSH_DIR / "id_oqs"
BACKUP_DIR = SSH_DIR / "backup_keys"

# Function to check if OQS-enabled OpenSSH is installed
def check_oqs_ssh_installed():
    try:
        result = subprocess.run(["ssh", "-Q", "key"], stdout=subprocess.PIPE, text=True)
        if OQS_ALGORITHM in result.stdout:
            print("[INFO] OQS-enabled OpenSSH is installed.")
            return True
        else:
            print("[INFO] OQS-enabled OpenSSH is not installed.")
            return False
    except FileNotFoundError:
        print("[ERROR] SSH is not installed on this system.")
        return False

# Function to install OQS-enabled OpenSSH
def install_oqs_ssh():
    try:
        print("[INFO] Installing OQS-enabled OpenSSH...")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "build-essential", "libssl-dev", "zlib1g-dev", "git"], check=True)
        
        # Clone the OQS-OpenSSH repository
        if not Path("openssh").exists():
            subprocess.run(["git", "clone", "https://github.com/open-quantum-safe/openssh.git"], check=True)
        
        # Build and install
        os.chdir("openssh")
        subprocess.run(["./configure", "--with-ssl-dir=/usr/local/ssl"], check=True)
        subprocess.run(["make"], check=True)
        subprocess.run(["sudo", "make", "install"], check=True)
        os.chdir("..")

        print("[INFO] OQS-enabled OpenSSH installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to install OQS-enabled OpenSSH: {e}")
        return False

# Function to ensure OQS-enabled OpenSSH is installed
def ensure_oqs_ssh_installed():
    if not check_oqs_ssh_installed():
        print("[INFO] OQS-enabled OpenSSH is not found. Installing...")
        if not install_oqs_ssh():
            print("[ERROR] Failed to install OQS-enabled OpenSSH. Exiting.")
            exit(1)

# Function to generate PQC SSH keys
def generate_pqc_ssh_key():
    try:
        if not SSH_DIR.exists():
            SSH_DIR.mkdir(parents=True, mode=0o700)
            print(f"[INFO] Created SSH directory: {SSH_DIR}")

        print(f"[INFO] Generating new SSH key with algorithm {OQS_ALGORITHM}...")
        subprocess.run(
            ["ssh-keygen", "-t", OQS_ALGORITHM, "-f", str(NEW_KEY_FILE), "-N", ""],
            check=True
        )
        print(f"[INFO] New SSH key generated: {NEW_KEY_FILE}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to generate SSH key: {e}")
        exit(1)

# Function to update authorized_keys file
def update_authorized_keys():
    try:
        authorized_keys = SSH_DIR / "authorized_keys"
        new_key_file_pub = NEW_KEY_FILE.with_suffix(".pub")

        if not new_key_file_pub.exists():
            print(f"[ERROR] Public key file not found: {new_key_file_pub}")
            return False

        with open(new_key_file_pub, "r") as pub_key_file:
            new_key = pub_key_file.read()

        with open(authorized_keys, "a") as auth_keys_file:
            auth_keys_file.write(new_key)

        print(f"[INFO] Added new key to {authorized_keys}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to update authorized_keys: {e}")
        return False

# Function to backup old SSH keys and configuration
def backup_ssh():
    try:
        if not BACKUP_DIR.exists():
            BACKUP_DIR.mkdir(parents=True, mode=0o700)
            print(f"[INFO] Created backup directory: {BACKUP_DIR}")

        print("[INFO] Backing up old SSH keys...")
        for key_file in SSH_DIR.glob("id_*"):
            shutil.move(str(key_file), BACKUP_DIR / key_file.name)
            print(f"[INFO] Backed up {key_file} to {BACKUP_DIR}")

        sshd_config = Path("/etc/ssh/sshd_config")
        if sshd_config.exists():
            shutil.copy(sshd_config, BACKUP_DIR / "sshd_config.backup")
            print(f"[INFO] Backed up SSHD configuration: {sshd_config}")
    except Exception as e:
        print(f"[ERROR] Failed to back up SSH keys/configuration: {e}")

# Function to connect to a remote system
def remote_ssh_execute(host, user, password, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=user, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        ssh.close()
        if error:
            print(f"[ERROR] Command failed on {host}: {error}")
            return None
        return output
    except Exception as e:
        print(f"[ERROR] Failed to connect to {host}: {e}")
        return None

# Function to test SSH connection
def test_ssh_connection(host, user, key_file=None, password=None):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key_file:
            ssh.connect(hostname=host, username=user, key_filename=key_file)
        elif password:
            ssh.connect(hostname=host, username=user, password=password)
        ssh.close()
        print(f"[INFO] Successfully connected to {host} as {user}.")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to connect to {host}: {e}")
        return False

# Function to update client-side SSH
def update_client_ssh(client_ip, client_user, client_password):
    print(f"[INFO] Updating SSH on client machine {client_ip}...")
    commands = [
        "sudo apt update",
        "sudo apt install -y oqs-openssh-client",
        f"ssh-keygen -t {OQS_ALGORITHM} -f ~/.ssh/id_oqs -N ''"
    ]
    for command in commands:
        result = remote_ssh_execute(client_ip, client_user, client_password, command)
        if result is None:
            print(f"[ERROR] Command failed on client {client_ip}: {command}")
            return False
    print("[INFO] SSH updated successfully on the client.")
    return True

# Main function to orchestrate the upgrade
def main():
    # Ensure OQS-enabled OpenSSH is installed on the server
    ensure_oqs_ssh_installed()

    # Collect client details
    client_ip = input("Enter the client machine's IP address: ").strip()
    client_user = input("Enter the client machine's username: ").strip()
    client_password = getpass("Enter the client machine's password: ")

    # Test client connection
    if not test_ssh_connection(client_ip, client_user, password=client_password):
        print("[ERROR] Client connection test failed. Exiting.")
        return

    # Update client-side SSH
    if not update_client_ssh(client_ip, client_user, client_password):
        print("[ERROR] Client SSH update failed. Exiting.")
        return

    # Generate and install PQC key on the server
    backup_ssh()
    generate_pqc_ssh_key()
    if not update_authorized_keys():
        print("[ERROR] Failed to update authorized_keys on the server.")
        return

    # Test connection with new key
    if test_ssh_connection(client_ip, client_user, key_file=str(NEW_KEY_FILE)):
        print("[INFO] New SSH key works. Migration successful.")
    else:
        print("[ERROR] New SSH key test failed. Reverting...")
        revert_ssh_config()
        print("[INFO] Reverted to old SSH configuration and keys.")

if __name__ == "__main__":
    main()
