# SSH Post-Quantum Cryptography Upgrade Script

This project provides a secure, automated script to upgrade SSH keys and configurations to **post-quantum cryptography (PQC)** algorithms for both servers and clients. The tool ensures your SSH connections are resistant to future quantum computing attacks.

---

## Why Post-Quantum Cryptography Matters

Quantum computers, once fully realized, will have the power to break many of the encryption methods used today, including RSA and ECC. This could compromise:
- Sensitive data
- Encrypted communications
- Authentication systems

**Post-Quantum Cryptography (PQC)** uses algorithms designed to resist attacks from quantum computers, ensuring your data remains secure for years to come.

---

## Why Upgrade SSH?

SSH (Secure Shell) is one of the most widely used protocols for secure remote access. Most SSH configurations rely on traditional encryption algorithms, such as RSA and ECDSA, which will eventually become vulnerable to quantum attacks. Upgrading to PQC algorithms, like **ECDSA-p256+Kyber512**, protects your SSH connections from future threats.

---

## What Does This Script Do?

This script:
1. **Checks Compatibility**: Ensures both server and client systems support PQC-capable OpenSSH.
2. **Backs Up Current Keys**: Creates a secure backup of existing SSH keys and configurations.
3. **Updates the Client**: Installs PQC-capable OpenSSH and generates PQC keys on the client.
4. **Upgrades the Server**: Replaces the server’s SSH keys with PQC-compatible keys and updates its configuration.
5. **Tests Connections**: Verifies that the new keys work for both client-to-server and server-to-client communication.
6. **Rolls Back if Necessary**: Automatically restores old keys and configurations if an issue is detected during the process.

---

## How to Use This Script

### Prerequisites

1. **Install Python 3**: Ensure Python 3 is installed on your system.
2. **Install Dependencies**:
   ```bash
   pip install paramiko
   ```
3. **Install OQS-Enabled OpenSSH**:
   - Both the server and client must support PQC algorithms. Install [Open Quantum Safe OpenSSH](https://github.com/open-quantum-safe/openssh) on both systems.
   - Follow the installation instructions in the repository.

### Step-by-Step Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/alenperic/SSH-Post-Quantum-Cryptography-Upgrade-Script.git
   cd SSH-Post-Quantum-Cryptography-Upgrade-Script
   ```

2. **Run the Script**:
   Execute the script to start the SSH upgrade process:
   ```bash
   python3 update_pqc_ssh.py
   ```

3. **Enter Details**:
   - When prompted, provide the **IP address**, **username**, and **password** for the client machine.

4. **Observe the Process**:
   - The script will:
     - Test the connection to the client.
     - Update the client’s SSH setup to support PQC.
     - Backup and replace the server's SSH keys with PQC keys.
     - Test connections using the new setup.

5. **Verify the Results**:
   - If the script completes successfully, your SSH connections are now post-quantum ready.
   - If any issues occur, the script will restore your original SSH keys and configurations.

---

## Example Output

Here’s what you can expect to see when running the script:
```
[INFO] Successfully connected to client 192.168.1.100.
[INFO] Updating SSH on client machine...
[INFO] Backing up old SSH keys and configurations.
[INFO] Generating new post-quantum SSH keys.
[INFO] Adding new keys to authorized_keys.
[INFO] Testing new key connection to client.
[INFO] Successfully migrated to post-quantum cryptography!
```

---

## Additional Resources

- [NIST Post-Quantum Cryptography Project](https://csrc.nist.gov/projects/post-quantum-cryptography)  
  Learn about NIST's ongoing efforts to standardize post-quantum cryptographic algorithms.

- [Open Quantum Safe](https://openquantumsafe.org/)  
  Explore tools and libraries for post-quantum cryptography.

- [Why Quantum Computers Threaten Encryption](https://www.ibm.com/quantum/learn/quantum-computing)  
  Understand the implications of quantum computing on current cryptographic methods.

---

## Contributing

We welcome contributions to improve the script or enhance its functionality. Feel free to submit issues or pull requests on GitHub.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
