![PythOS banner](PythOS.png)
# PythOS

A lightweight Linux distro written *almost* completely with Python!

---

## Architecture Overview

The system is organized into a modular directory structure mimicking a traditional Unix layout:

* **`bin/`**: Contains core user utilities.
* **`sbin/`**: Reserved for system administration binaries and low-level power management infrastructure.
* **`etc/`**: Stores system-wide configuration data, including operating system details

---

## Core Components

### 1. System Logon Menu (`init.py`)
The bootstrapping layer for PythOS built on top of the `curses` library. It handles system startup and presents an interactive logon interface.
* **Features**: Includes options for system logon, machine reboots, halts, and power-offs.

### 2. PythOS Shell (`pysh.py`)
The central interactive command-line interpreter executing the user loop. 
* **Path Resolution**: Traverses environment lookups prioritizing local script overrides.
* **Execution Handler**: Parses file shebang headers natively and isolates execution permissions to prevent shell environment crashes.

### 3. Utility Suite
Handcrafted Python implementations of traditional system utilities optimized with standard `argparse` execution schemas.

---
