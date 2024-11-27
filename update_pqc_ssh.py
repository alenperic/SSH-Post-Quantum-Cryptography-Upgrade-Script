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
