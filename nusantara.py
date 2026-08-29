import getpass
import hashlib
import os
import re
import shlex
import subprocess
import sys
import time

# --- SYSTEM METADATA ---
VERSION = "V3.1-SHORTCUTS"
ENGINE = "SKY-SHIELD-ULTRA"


class NusantaraOS:
    """A small terminal wrapper with Termux-friendly shortcuts."""

    # Exactly 25 shortcuts. The first word of a shortcut is intentionally
    # short, while its expansion can be a longer Termux command.
    SHORTCUTS = {
        "u": (("pkg", "update"), "Update daftar paket Termux"),
        "ug": (("pkg", "upgrade"), "Upgrade semua paket Termux"),
        "up": (None, "Update lalu upgrade paket Termux"),
        "i": (("pkg", "install"), "Install paket: i <nama-paket>"),
        "un": (("pkg", "uninstall"), "Hapus paket: un <nama-paket>"),
        "s": (("pkg", "search"), "Cari paket: s <kata-kunci>"),
        "li": (("pkg", "list-installed"), "Tampilkan paket yang terpasang"),
        "py": (("python",), "Jalankan Python: py <argumen>"),
        "pi": (("pip", "install"), "Install library Python: pi <nama-library>"),
        "run": (("python",), "Jalankan file Python: run <file.py>"),
        "c": (("clear",), "Bersihkan layar"),
        "h": (None, "Tampilkan bantuan dan 25 shortcut"),
        "q": (None, "Keluar dari Nusantara OS"),
        "si": (None, "Tampilkan informasi sistem"),
        "la": (("ls", "-lah"), "Tampilkan semua file secara detail"),
        "o": (("termux-open",), "Buka file: o <file>"),
        "url": (("termux-open-url",), "Buka URL: url <alamat>"),
        "sh": (("termux-share",), "Bagikan file: sh <file>"),
        "clip": (("termux-clipboard-set",), "Salin teks: clip <teks>"),
        "paste": (("termux-clipboard-get",), "Ambil isi clipboard"),
        "n": (("termux-notification",), "Kirim notifikasi: n <pesan>"),
        "v": (("termux-vibrate",), "Getarkan perangkat"),
        "cam": (("termux-camera-photo",), "Ambil foto: cam <output.jpg>"),
        "loc": (("termux-location",), "Ambil lokasi perangkat"),
        "wifi": (("termux-wifi-connectioninfo",), "Tampilkan info koneksi Wi-Fi"),
    }
    SHORTCUT_COUNT = 25

    def __init__(self):
        self.config_file = ".nusa_vault"
        self.is_authenticated = False
        # Shell control characters are rejected. Commands are executed with
        # shell=False, so normal arguments and quoted text remain usable.
        self.blocked_chars = re.compile(r"[;&|`$()<\n\r]")

    def clear(self):
        os.system("clear" if os.name != "nt" else "cls")

    def ui_banner(self):
        self.clear()
        print("\033[1;35m    _  _ _  _ ____ ____ _  _ ___ ____ ____ ____ \033[0m")
        print("\033[1;36m    |\\ | |  | [__  |__| |\\ |  |  |__| |__/ |__| \033[0m")
        print("\033[1;34m    | \\| |__| ___] |  | | \\|  |  |  | |  \\ |  | \033[0m \033[1;31m[GHOST-V3]\033[0m")
        print("\033[1;30m    ────────────────────────────────────────────\033[0m")
        print("    \033[1;31mMODE: GHOST\033[0m | \033[1;32mENCRYPTION: SHA-256\033[0m\n")

    def self_destruct(self):
        """MENGHAPUS SEMUA JEJAK SISTEM"""
        print("\033[1;41m [!!!] PURGING ALL DATA... GOODBYE. \033[0m")
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            os.remove(__file__)  # MENGHAPUS SCRIPT INI SENDIRI
        except OSError:
            pass
        sys.exit()

    def setup_system(self):
        if not os.path.exists(self.config_file):
            print("\033[1;33m[!] GHOST INITIALIZATION: Create Master Key\033[0m")
            new_key = getpass.getpass("Set Key: ")
            confirm = getpass.getpass("Confirm: ")
            if new_key == confirm:
                hashed = hashlib.sha256(new_key.encode()).hexdigest()
                with open(self.config_file, "w", encoding="utf-8") as vault:
                    vault.write(hashed)
                print("\033[1;32m[+] Ghost Vault Activated.\033[0m")
                time.sleep(1)
            else:
                sys.exit()

    def secure_login(self):
        self.setup_system()
        self.ui_banner()
        with open(self.config_file, "r", encoding="utf-8") as vault:
            saved_hash = vault.read().strip()
        attempts = 0
        while attempts < 3:
            key = getpass.getpass("\033[1;31m[!] ENTER KEY:\033[0m ")
            if hashlib.sha256(key.encode()).hexdigest() == saved_hash:
                return True
            attempts += 1
            print(f"\033[1;31m[-] DENIED ({attempts}/3)\033[0m")

        self.self_destruct()  # JALANKAN SELF-DESTRUCT JIKA SALAH 3X
        return False

    def show_help(self):
        print("\nNusantara OS - command shortcuts")
        print("Ketik shortcut lalu argumennya. Total shortcut: 25\n")
        print(f"{'CMD':<8}{'MENJADI':<36}KETERANGAN")
        print("-" * 80)
        for shortcut, (command, description) in self.SHORTCUTS.items():
            if shortcut == "up":
                target = "pkg update + pkg upgrade"
            elif shortcut in {"h", "q", "si"}:
                target = {
                    "h": "help",
                    "q": "exit",
                    "si": "sys-info",
                }[shortcut]
            else:
                target = " ".join(command)
            print(f"{shortcut:<8}{target:<36}{description}")
        print("\nCommand lain tetap bisa dijalankan seperti biasa.")
        print("Termux API (o, url, sh, clip, paste, n, v, cam, loc, wifi) membutuhkan Termux:API.")

    def show_system_info(self):
        print(f"OS: Nusantara Ghost\nVersion: {VERSION}\nIntegrity: Verified")

    @staticmethod
    def _usage_for(shortcut):
        usages = {
            "i": "Pemakaian: i <nama-paket>",
            "un": "Pemakaian: un <nama-paket>",
            "s": "Pemakaian: s <kata-kunci>",
            "pi": "Pemakaian: pi <nama-library>",
            "run": "Pemakaian: run <file.py>",
            "o": "Pemakaian: o <file>",
            "url": "Pemakaian: url <alamat>",
            "sh": "Pemakaian: sh <file>",
            "clip": "Pemakaian: clip <teks>",
            "n": "Pemakaian: n <pesan>",
            "cam": "Pemakaian: cam <output.jpg>",
        }
        return usages.get(shortcut)

    def execute_shortcut(self, shortcut, extra_args):
        """Expand and execute one of the 25 built-in shortcuts."""
        usage = self._usage_for(shortcut)
        if usage and not extra_args:
            print(usage)
            return

        if shortcut == "h":
            self.show_help()
            return
        if shortcut == "q":
            return
        if shortcut == "si":
            self.show_system_info()
            return
        if shortcut == "c":
            self.clear()
            return
        if shortcut == "up":
            update_status = self.run_external(["pkg", "update"])
            if update_status == 0:
                self.run_external(["pkg", "upgrade"])
            return

        command = list(self.SHORTCUTS[shortcut][0])
        if shortcut in {"clip", "n"}:
            # These Termux API commands expect the message as one value.
            command.append(" ".join(extra_args))
            if shortcut == "n":
                command[1:1] = ["--content"]
        else:
            command.extend(extra_args)
        self.run_external(command)

    def _split_redirection(self, args):
        """Allow only a simple safe `>` or `>>` redirection."""
        redirect_indexes = [
            (index, token) for index, token in enumerate(args) if token in {">", ">>"}
        ]
        if not redirect_indexes:
            return args, None, False

        if len(redirect_indexes) != 1:
            raise ValueError("Hanya satu redirection yang diizinkan.")

        index, operator = redirect_indexes[0]
        if index != len(args) - 2:
            raise ValueError("Redirection harus diakhiri nama file output.")

        command = args[:index]
        output_path = args[index + 1]
        if not command or not output_path:
            raise ValueError("Format redirection tidak valid.")
        return command, output_path, operator == ">>"

    def run_external(self, args):
        """Run a command without invoking a shell."""
        try:
            command, output_path, append = self._split_redirection(args)
        except ValueError as error:
            print(f"\033[1;31m[GHOST-SHIELD] {error}\033[0m")
            return 2

        try:
            if output_path:
                mode = "a" if append else "w"
                with open(output_path, mode, encoding="utf-8") as output:
                    result = subprocess.run(command, shell=False, stdout=output)
            else:
                result = subprocess.run(command, shell=False)
            return result.returncode
        except FileNotFoundError:
            print(f"\033[1;31m[!] Command tidak ditemukan: {command[0]}\033[0m")
        except PermissionError:
            print(f"\033[1;31m[!] Tidak punya izin menjalankan: {command[0]}\033[0m")
        except OSError as error:
            print(f"\033[1;31m[!] Gagal menjalankan command: {error}\033[0m")
        return 1

    def shell(self):
        self.ui_banner()
        print("Ketik 'h' untuk melihat 25 shortcut Nusantara OS.\n")
        while True:
            try:
                path = os.getcwd().replace(os.path.expanduser("~"), "~")
                prompt = input(
                    f"\033[1;36mNusantara\033[1;31m@\033[1;37mGhost "
                    f"\033[1;30m[{path}]\033[0m\n\033[1;31m# \033[0m"
                ).strip()

                if not prompt:
                    continue

                if self.blocked_chars.search(prompt):
                    print("\033[1;31m[GHOST-SHIELD] Access Denied: Dangerous Character.\033[0m")
                    continue

                try:
                    args = shlex.split(prompt)
                except ValueError as error:
                    print(f"\033[1;31m[!] Format command tidak valid: {error}\033[0m")
                    continue

                if not args:
                    continue

                command_name = args[0].lower()
                extra_args = args[1:]

                if command_name in {"exit", "shutdown", "q"}:
                    break
                if command_name in {"help", "shortcuts"}:
                    self.show_help()
                    continue
                if command_name == "cd":
                    target = os.path.expanduser(extra_args[0]) if extra_args else os.path.expanduser("~")
                    try:
                        os.chdir(target)
                    except OSError:
                        print("Invalid Path.")
                    continue
                if command_name == "sys-info":
                    self.show_system_info()
                    continue
                if command_name == "scan" and extra_args:
                    print(f"[*] Scanning {extra_args[0]}...")
                    continue
                if command_name in self.SHORTCUTS:
                    self.execute_shortcut(command_name, extra_args)
                    continue

                # Unknown commands still work, but are executed safely without
                # shell expansion. Simple `>` and `>>` redirection is supported.
                self.run_external(args)

            except KeyboardInterrupt:
                print("\n\033[1;31m[!] Use 'exit' to logout.\033[0m")
            except EOFError:
                print()
                break


if __name__ == "__main__":
    os_sys = NusantaraOS()
    if os_sys.secure_login():
        os_sys.shell()
