import os, subprocess, sys, hashlib, getpass, time, socket
from datetime import datetime

# --- CONFIGURATION & SECURITY CORE ---
VERSION = "V1.0-FINAL"
CODENAME = "SKY-ARCH"
# Default Key: admin (Ganti hash ini untuk custom password)
MASTER_KEY = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

class NusantaraOS:
    def __init__(self):
        self.is_authenticated = False
        self.session_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def neon_banner(self):
        self.clear()
        colors = ["\033[1;36m", "\033[1;35m", "\033[0m"]
        print(f"""
    {colors[0]}╔╗╔╦ ╦╔═╗╔═╗╔╗╔╔╦╗╔═╗╦═╗╔═╗  ╔═╗╔═╗  {colors[1]}██╗   ██╗ ██╗
    {colors[0]}║║║║ ║╚═╗╠═╣║║║ ║ ╠═╣╠╦╝╠═╣  ║ ║╚═╗  {colors[1]}██║   ██║███║
    {colors[0]}╝╚╝╚═╝╚═╝╩ ╩╝╚╝ ╩ ╩ ╩╩╚═╩ ╩  ╚═╝╚═╝  {colors[1]}╚██╗ ██╔╝╚██║
                                         {colors[1]} ╚████╔╝  ██║
    {colors[2]}─── \033[1;32mSECURE TERMINAL ENVIRONMENT\033[0m ───  {colors[1]}  ╚═══╝   ╚═╝\033[0m
        """)
        print(f"\033[1;30m[ BUILD: {VERSION} ] [ ENGINE: SKY-AI ] [ SESSION: {self.session_start} ]\033[0m\n")

    def secure_boot(self):
        self.neon_banner()
        attempts = 0
        while attempts < 3:
            key = getpass.getpass("\033[1;31m[!] ENTER SYSTEM KEY:\033[0m ")
            if hashlib.sha256(key.encode()).hexdigest() == MASTER_KEY:
                print("\033[1;32m[+] Authentication Bypass... Granted.\033[0m")
                time.sleep(1)
                self.is_authenticated = True
                return True
            attempts += 1
            print(f"\033[1;31m[-] Access Denied. ({attempts}/3)\033[0m")
        
        print("\033[1;41m[!!!] SECURITY BREACH: SELF-DESTRUCT INITIATED \033[0m")
        # os.remove(__file__) # Aktifkan ini untuk benar-benar menghapus file jika salah pass
        sys.exit()

    def vdp_scan(self, target):
        """Simulasi Smart Scan untuk Bug Bounty / VDP"""
        print(f"\033[1;34m[*] Initiating Nusantara-Scan on: {target}\033[0m")
        common_ports = [21, 22, 80, 443, 8080]
        for port in common_ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(0.5)
            result = s.connect_ex((target, port))
            status = "\033[1;32mOPEN\033[0m" if result == 0 else "\033[1;31mCLOSED\033[0m"
            print(f"    - Port {port}: {status}")
            s.close()

    def main_loop(self):
        self.neon_banner()
        while True:
            try:
                current_time = datetime.now().strftime("%H:%M")
                path = os.getcwd().replace(os.path.expanduser("~"), "~")
                
                # Terminal Prompt Aesthetic
                cmd = input(f"\033[1;35m{current_time} \033[1;36m\033[7;36m\033[1;30m Nusantara \033[0;36m \033[1;37m{path} \033[1;30m\n$ \033[0m").strip()

                if cmd.lower() in ["exit", "shutdown"]:
                    print("\033[1;33m[!] Locking Vault... Goodbye.\033[0m")
                    break
                
                if not cmd: continue

                # Custom Command Logic
                parts = cmd.split()
                if parts[0] == "scan" and len(parts) > 1:
                    self.vdp_scan(parts[1])
                elif parts[0] == "help":
                    print("\033[1;37mCommands: \033[1;36mscan [target]\033[0m, \033[1;36msys-info\033[0m, \033[1;36mclear\033[0m, \033[1;36mexit\033[0m")
                elif parts[0] == "sys-info":
                    print(f"\033[1;35mOS:\033[0m Nusantara OS {VERSION}")
                    print(f"\033[1;35mKERNEL:\033[0m {CODENAME}")
                    print(f"\033[1;35mSHELL:\033[0m Python-Nusantara-Shell")
                else:
                    # Jalankan perintah system (ls, cd, git, dll)
                    if parts[0] == "cd" and len(parts) > 1:
                        try: os.chdir(parts[1])
                        except: print("Directory not found.")
                    else:
                        subprocess.run(cmd, shell=True)

            except KeyboardInterrupt:
                print("\n\033[1;33m[!] Locked. Use 'exit' to quit.\033[0m")

if __name__ == "__main__":
    os_sys = NusantaraOS()
    if os_sys.secure_boot():
        os_sys.main_loop()
        