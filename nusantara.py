import os, subprocess, sys, hashlib, getpass, time, socket, re
from datetime import datetime

# --- SYSTEM METADATA ---
VERSION = "V2.0-FORTRESS"
ENGINE = "SKY-SHIELD-V2"

class NusantaraOS:
    def __init__(self):
        self.config_file = ".nusa_vault"
        self.is_authenticated = False
        self.blocked_chars = re.compile(r'[;&|`$]') # Anti-Injection Shield

    def clear(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def ui_banner(self):
        self.clear()
        print(f"\033[1;35m    _  _ _  _ ____ ____ _  _ ___ ____ ____ ____ \033[0m")
        print(f"\033[1;36m    |\ | |  | [__  |__| |\ |  |  |__| |__/ |__| \033[0m")
        print(f"\033[1;34m    | \| |__| ___] |  | | \|  |  |  | |  \ |  | \033[0m \033[1;31m[V2.0]\033[0m")
        print(f"\033[1;30m    ────────────────────────────────────────────\033[0m")
        print(f"    \033[1;32mSTATUS: SECURED\033[0m | \033[1;33mENGINE: {ENGINE}\033[0m\n")

    def setup_system(self):
        """Meminta user membuat password baru saat pertama kali run"""
        if not os.path.exists(self.config_file):
            print("\033[1;33m[!] First Time Setup: Create your Master Key\033[0m")
            new_key = getpass.getpass("Set New Master Key: ")
            confirm_key = getpass.getpass("Confirm Master Key: ")
            if new_key == confirm_key:
                hashed = hashlib.sha256(new_key.encode()).hexdigest()
                with open(self.config_file, "w") as f:
                    f.write(hashed)
                print("\033[1;32m[+] Vault Created Successfully!\033[0m")
                time.sleep(1)
            else:
                print("\033[1;31m[-] Passwords do not match. System Exit.\033[0m")
                sys.exit()

    def secure_login(self):
        self.setup_system()
        self.ui_banner()
        with open(self.config_file, "r") as f:
            saved_hash = f.read().strip()
            
        attempts = 0
        while attempts < 3:
            key = getpass.getpass("\033[1;31m[!] ENTER MASTER KEY:\033[0m ")
            if hashlib.sha256(key.encode()).hexdigest() == saved_hash:
                return True
            attempts += 1
            print(f"\033[1;31m[-] Access Denied. ({attempts}/3)\033[0m")
        
        print("\033[1;41m [!] INTRUSION DETECTED: WIPING SESSION LOGS... \033[0m")
        sys.exit()

    def sanitize_input(self, cmd):
        """Mencegah Command Injection (Balasan buat DeepSeek!)"""
        if self.blocked_chars.search(cmd):
            return False
        return True

    def run_scanner(self, target):
        print(f"\033[1;34m[*] Probing {target} on Secure Ports...\033[0m")
        for port in [21, 22, 80, 443, 3306, 8080]:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.7)
                res = s.connect_ex((target, port))
                status = "\033[1;32mOPEN\033[0m" if res == 0 else "\033[1;31mCLOSED\033[0m"
                print(f"  > Port {port:4} : {status}")

    def shell(self):
        self.ui_banner()
        while True:
            try:
                current_dir = os.getcwd().replace(os.path.expanduser("~"), "~")
                prompt = input(f"\033[1;36mNusantara\033[1;37m@\033[1;35mSky \033[1;30m[{current_dir}]\033[0m\n\033[1;32m$ \033[0m").strip()
                
                if not prompt: continue
                if prompt.lower() in ["exit", "shutdown"]: break

                # Security Filter
                if not self.sanitize_input(prompt):
                    print("\033[1;31m[SHIELD] Execution Blocked: Dangerous characters detected.\033[0m")
                    continue

                args = prompt.split()
                if args[0] == "scan" and len(args) > 1:
                    self.run_scanner(args[1])
                elif args[0] == "help":
                    print("\033[1;37mNative: scan, help, exit, clear, sys-info\033[0m")
                elif args[0] == "sys-info":
                    print(f"Build: {VERSION}\nEngine: {ENGINE}\nSecurity: Shield-Active")
                elif args[0] == "cd":
                    try: os.chdir(args[1] if len(args) > 1 else os.path.expanduser("~"))
                    except: print("Path not found.")
                else:
                    # Menjalankan command sistem asli dengan aman
                    subprocess.run(args) # Pakai list args (shell=False) biar aman dari injection!

            except KeyboardInterrupt:
                print("\n\033[1;33m[!] Use 'exit' to logout.\033[0m")

if __name__ == "__main__":
    os_sys = NusantaraOS()
    if os_sys.secure_login():
        os_sys.shell()
        
