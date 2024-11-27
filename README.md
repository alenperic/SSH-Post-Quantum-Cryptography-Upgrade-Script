# Automated Post-Quantum SSH Migration Tool

This project helps securely upgrade SSH keys and configurations to **post-quantum cryptography (PQC)** algorithms for both servers and clients. It ensures your SSH connections are resistant to future quantum computing attacks.

---

## Why Post-Quantum Cryptography?

Quantum computers, once fully realized, will be capable of breaking many widely-used encryption methods, including RSA and ECC. This poses a significant threat to the security of:
- Sensitive data
- Encrypted communications
- Identity verification systems

**Post-Quantum Cryptography (PQC)** uses algorithms designed to resist quantum attacks, ensuring long-term data security.

---

## Why Upgrade SSH?

SSH (Secure Shell) is a fundamental protocol for securely accessing remote servers. Most current SSH keys use RSA, ECDSA, or Ed25519, which quantum computers could eventually crack. Upgrading to PQC algorithms like **ECDSA-p256+Kyber512** helps future-proof your SSH connections.

---

## What Does This Script Do?

This script:
1. **Checks Prerequisites**: Ensures both client and server support PQC algorithms.
2. **Backs Up Current Keys**: Safely stores your existing SSH keys and configurations.
3. **Updates Client SSH**: Installs PQC-capable OpenSSH and generates new PQC keys on the client machine.
4. **Upgrades Server SSH**: Replaces the server's SSH keys with PQC keys and updates its configuration.
5. **Tests Connections**: Verifies that new keys work for both client-to-server and server-to-client connections.
6. **Rolls Back if Needed**: Restores old keys and configurations if any issues are detected.

---

## How to Use This Script

### Prerequisites
1. **Install Python 3**: Make sure Python 3 is installed on your machine.
2. **Install Dependencies**:
   ```bash
   pip install paramiko
   ```
3. **Ensure OQS-Enabled OpenSSH**:
   - Your server and client must use [Open Quantum Safe OpenSSH](https://github.com/open-quantum-safe/openssh).
   - Follow the installation guide on their repository to set it up.

### Step-by-Step Instructions
1. **Download the Script**:
   Clone this repository or download the script file.
   ```bash
   git clone https://github.com/yourusername/post-quantum-ssh
   cd post-quantum-ssh
   ```

2. **Run the Script**:
   Execute the script to upgrade your SSH setup:
   ```bash
   python3 update_pqc_ssh.py
   ```

3. **Provide Information**:
   - Enter the **client IP**, **username**, and **password** when prompted.

4. **Watch the Process**:
   - The script will:
     - Test the connection to the client.
     - Update SSH on the client.
     - Backup and replace keys on the server.
     - Test the new PQC setup.

5. **Verify the Results**:
   If the script reports success, your SSH setup is now post-quantum ready. If there are issues, the script will restore your original configurations.

---

## Resources

- **Learn About Post-Quantum Cryptography**:  
  [NIST Post-Quantum Cryptography Project](https://csrc.nist.gov/projects/post-quantum-cryptography)

- **Open Quantum Safe**:  
  [Open Quantum Safe Organization](https://openquantumsafe.org/)

- **Why Quantum Computers Threaten Encryption**:  
  [IBM Quantum Computing Explained](https://www.ibm.com/quantum/learn/quantum-computing)

---

## Contributing

If you’d like to contribute to this project, feel free to submit pull requests or issues. Let’s work together to make encryption quantum-safe!

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
