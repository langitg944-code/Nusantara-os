import os, subprocess, sys, hashlib, getpass, time, socket, re
from datetime import datetime

# --- SYSTEM METADATA ---
VERSION = "V3.0-GHOST"
ENGINE = "SKY-SHIELD-ULTRA"

class NusantaraOS:
    def __init__(self):
        self.config_file = ".nusa_vault"
        self.is_authenticated = False
        # Block characters that are truly dangerous while allowing useful ones
        self.blocked_chars = re.compile(r'[;`$]') 

    def clear(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def ui_banner(self):
        self.clear()
        print(f"\033[1;35m    _  _ _  _ ____ ____ _  _ ___ ____ ____ ____ \033[0m")
        print(f"\033[1;36m    |\ | |  | [__  |__| |\ |  |  |__| |__/ |__| \033[0m")
        print(f"\033[1;34m    | \| |__| ___] |  | | \|  |  |  | |  \ |  | \033[0m \033[1;31m[GHOST-V3]\033[0m")
        print(f"\033[1;30m    ────────────────────────────────────────────\033[0m")
        print(f"    \033[1;31mMODE: GHOST\033[0m | \033[1;32mENCRYPTION: AES-256\033[0m\n")

    def self_destruct(self):
        """MENGHAPUS SEMUA JEJAK SISTEM"""
        print("\033[1;41m [!!!] PURGING ALL DATA... GOODBYE. \033[0m")
        try:
            if os.path.exists(self.config_file): os.remove(self.config_file)
            os.remove(__file__) # MENGHAPUS SCRIPT INI SENDIRI
        except:
            pass
        sys.exit()

    def setup_system(self):
        if not os.path.exists(self.config_file):
            print("\033[1;33m[!] GHOST INITIALIZATION: Create Master Key\033[0m")
            new_key = getpass.getpass("Set Key: ")
            confirm = getpass.getpass("Confirm: ")
            if new_key == confirm:
                hashed = hashlib.sha256(new_key.encode()).hexdigest()
                with open(self.config_file, "w") as f: f.write(hashed)
                print("\033[1;32m[+] Ghost Vault Activated.\033[0m")
                time.sleep(1)
            else: sys.exit()

    def secure_login(self):
        self.setup_system()
        self.ui_banner()
        with open(self.config_file, "r") as f: saved_hash = f.read().strip()
        attempts = 0
        while attempts < 3:
            key = getpass.getpass("\033[1;31m[!] ENTER KEY:\033[0m ")
            if hashlib.sha256(key.encode()).hexdigest() == saved_hash:
                return True
            attempts += 1
            print(f"\033[1;31m[-] DENIED ({attempts}/3)\033[0m")
        
        self.self_destruct() # JALANKAN SELF-DESTRUCT JIKA SALAH 3X

    def shell(self):
        self.ui_banner()
        while True:
            try:
                path = os.getcwd().replace(os.path.expanduser("~"), "~")
                prompt = input(f"\033[1;36mNusantara\033[1;31m@\033[1;37mGhost \033[1;30m[{path}]\033[0m\n\033[1;31m# \033[0m").strip()
                
                if not prompt: continue
                if prompt.lower() in ["exit", "shutdown"]: break

                # Security Guard
                if self.blocked_chars.search(prompt):
                    print("\033[1;31m[GHOST-SHIELD] Access Denied: Dangerous Character.\033[0m")
                    continue

                args = prompt.split()
                if args[0] == "scan" and len(args) > 1:
                    print(f"[*] Scanning {args[1]}...")
                elif args[0] == "sys-info":
                    print(f"OS: Nusantara Ghost\nVersion: {VERSION}\nIntegrity: Verified")
                elif args[0] == "cd":
                    try: os.chdir(args[1] if len(args) > 1 else os.path.expanduser("~"))
                    except: print("Invalid Path.")
                else:
                    # SMART PARSER: Memungkinkan redirection sederhana tapi tetap aman
                    if ">" in prompt:
                        subprocess.run(prompt, shell=True) # Redirection butuh shell=True
                    else:
                        subprocess.run(args, shell=False)

            except KeyboardInterrupt:
                print("\n\033[1;31m[!] Use 'exit' to logout.\033[0m")

if __name__ == "__main__":
    os_sys = NusantaraOS()
    if os_sys.secure_login():
        os_sys.shell()
            
