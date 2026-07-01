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

### How to dualboot
**(for Windows users. Skip if you know how to dualboot Linux, but please do not ignore step 6 when flashing):**
*Prerequisites:*
- Rufus (download from [here](https://rufus.ie))
- PythOS ISO (download from below)
- A USB (at least 200MB)

*Steps:*
1. Plug in your USB and run Rufus you have just downloaded
2. Select your USB device in the "Device" dropdown menu
3. In the "Boot selection" dropdown, select "Disk or ISO image (Please select)"
4. Select PythOS ISO file
5. Click START
6. Select DD mode as the flash mode instead of ISO mode (ISO mode will NOT work) and click OK
7. Wait for it to flash
8. Reboot your computer after flashing and enter UEFI boot menu
9. Select the USB flash drive 
10. Select PythOS Phoenix
11. ENJOY!

---

### How the OS works:
1. Boots grub bootloader
2. Boots Linux kernel
3. Loads init script
4. Loads init.py from sbin/
5. Tries to load pysh.py from bin/
-> If fails or user exits pyshell, it falls back to init.py as a logon menu (written with ncurses)
- This is a protection mechanism that prevents kernel panic (which needs us to force reboot the PC)