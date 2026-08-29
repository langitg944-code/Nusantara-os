import getpass
import hashlib
import os
import re
import shlex
import subprocess
import sys
import threading
import time

# --- SYSTEM METADATA ---
VERSION = "V4.1-QUIET"
ENGINE = "SKY-SHIELD-ULTRA"


class NusantaraOS:
    """A small terminal wrapper with Termux-friendly shortcuts."""

    # Exactly 50 shortcuts. The first word of a shortcut is intentionally
    # short, while its expansion can be a longer Termux command.
    SHORTCUTS = {
        # --- Paket & sistem ---
        "u": (("pkg", "update"), "Update daftar paket Termux"),
        "ug": (("pkg", "upgrade", "-y"), "Upgrade semua paket Termux"),
        "up": (None, "Update lalu upgrade paket Termux"),
        "i": (("pkg", "install", "-y"), "Install paket: i <nama-paket>"),
        "un": (("pkg", "uninstall"), "Hapus paket: un <nama-paket>"),
        "s": (("pkg", "search"), "Cari paket: s <kata-kunci>"),
        "li": (("pkg", "list-installed"), "Tampilkan paket yang terpasang"),
        "py": (("python",), "Jalankan Python: py <argumen>"),
        "pi": (("pip", "install"), "Install library Python: pi <nama-library>"),
        "run": (("python",), "Jalankan file Python: run <file.py>"),
        "c": (("clear",), "Bersihkan layar"),
        "h": (None, "Tampilkan bantuan dan 50 shortcut"),
        "q": (None, "Keluar dari Nusantara OS"),
        "si": (None, "Tampilkan informasi sistem"),
        "la": (("ls", "-lah"), "Tampilkan semua file secara detail"),
        # --- Termux API ---
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
        # --- Git ---
        "g": (("git",), "Jalankan git: g <argumen>"),
        "gs": (("git", "status", "-sb"), "Status repo secara ringkas"),
        "ga": (("git", "add"), "Tambahkan file ke stage: ga <file>"),
        "gc": (("git", "commit", "-m"), "Commit perubahan: gc <pesan>"),
        "gp": (("git", "push"), "Push ke remote"),
        "gl": (("git", "log", "--oneline", "-10"), "10 commit terakhir"),
        "gd": (("git", "diff"), "Lihat perubahan: gd <file>"),
        "gcl": (("git", "clone"), "Clone repo: gcl <url>"),
        # --- File & folder ---
        "e": (("nano",), "Edit file: e <file>"),
        "ct": (("cat",), "Tampilkan isi file: ct <file>"),
        "mk": (("mkdir", "-p"), "Buat folder: mk <nama-folder>"),
        "del": (("rm", "-i"), "Hapus file dengan konfirmasi: del <file>"),
        "cpy": (("cp", "-r"), "Salin file/folder: cpy <asal> <tujuan>"),
        "mvf": (("mv",), "Pindah atau rename: mvf <asal> <tujuan>"),
        "f": (("find", ".", "-name"), "Cari file: f <pola>"),
        "gr": (("grep", "-rn"), "Cari teks di file: gr <kata> <lokasi>"),
        "z": (("unzip",), "Ekstrak arsip zip: z <file.zip>"),
        "tz": (("tar", "-xzvf"), "Ekstrak arsip tar.gz: tz <file.tar.gz>"),
        # --- Disk & jaringan ---
        "d": (("df", "-h"), "Tampilkan sisa ruang penyimpanan"),
        "w": (("wget",), "Unduh file: w <url>"),
        "cu": (("curl", "-L"), "Ambil data dari URL: cu <url>"),
        "myip": (("curl", "-s", "https://ifconfig.me"), "Tampilkan IP publik"),
        # --- Perangkat ---
        "bat": (("termux-battery-status",), "Tampilkan status baterai"),
        "tts": (("termux-tts-speak",), "Ucapkan teks: tts <kalimat>"),
        "stor": (("termux-setup-storage",), "Aktifkan akses storage Termux"),
    }
    SHORTCUT_COUNT = 50

    # Shortcut yang argumennya digabung menjadi satu nilai.
    JOINED_ARG_SHORTCUTS = {"clip", "n", "gc", "tts"}

    # Shortcut yang dijalankan dalam Quiet Mode: output ditahan, hanya
    # satu baris spinner yang tampil di layar.
    QUIET_SHORTCUTS = {"u", "ug", "up", "i", "un", "pi"}

    # Frame spinner braille. Halus, kecil, dan tidak menggeser baris.
    SPINNER_FRAMES = "\u280b\u2819\u2839\u2838\u283c\u2834\u2826\u2827\u2807\u280f"
    SPINNER_INTERVAL = 0.08

    def __init__(self):
        self.config_file = ".nusa_vault"
        self.is_authenticated = False
        self.last_output = []
        self.last_label = ""
        # Shell control characters are rejected. Commands are executed with
        # shell=False, so normal arguments and quoted text remain usable.
        self.blocked_chars = re.compile(r"[;&|`$()<\n\r]")

    def clear(self):
        os.system("clear" if os.name != "nt" else "cls")

    def ui_banner(self):
        self.clear()
        print("\033[1;35m    _  _ _  _ ____ ____ _  _ ___ ____ ____ ____ \033[0m")
        print("\033[1;36m    |\\ | |  | [__  |__| |\\ |  |  |__| |__/ |__| \033[0m")
        print("\033[1;34m    | \\| |__| ___] |  | | \\|  |  |  | |  \\ |  | \033[0m \033[1;31m[GHOST-V4]\033[0m")
        print("\033[1;30m    \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\033[0m")
        print("    \033[1;31mMODE: GHOST\033[0m | \033[1;32mENCRYPTION: SHA-256\033[0m | \033[1;36mQUIET: ON\033[0m\n")

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
        print(f"Ketik shortcut lalu argumennya. Total shortcut: {self.SHORTCUT_COUNT}\n")
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
            marker = " \u25cf" if shortcut in self.QUIET_SHORTCUTS else ""
            print(f"{shortcut:<8}{target:<36}{description}{marker}")
        print("\n\u25cf = Quiet Mode: output disembunyikan, diganti satu baris spinner.")
        print("   Ketik 'log' untuk membaca output lengkap command terakhir.")
        print("Command lain tetap bisa dijalankan seperti biasa.")
        print("Termux API (o, url, sh, clip, paste, n, v, cam, loc, wifi, bat, tts, stor)")
        print("membutuhkan Termux:API.")

    def show_system_info(self):
        print(f"OS: Nusantara Ghost\nVersion: {VERSION}\nIntegrity: Verified")

    def show_last_log(self):
        if not self.last_output:
            print("\033[1;30mBelum ada output yang tersimpan.\033[0m")
            return
        print(f"\n\033[1;30m--- output: {self.last_label} ---\033[0m")
        for line in self.last_output:
            print(line)
        print(f"\033[1;30m--- {len(self.last_output)} baris ---\033[0m")

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
            "ga": "Pemakaian: ga <file>",
            "gc": "Pemakaian: gc <pesan-commit>",
            "gcl": "Pemakaian: gcl <url-repo>",
            "e": "Pemakaian: e <file>",
            "ct": "Pemakaian: ct <file>",
            "mk": "Pemakaian: mk <nama-folder>",
            "del": "Pemakaian: del <file>",
            "cpy": "Pemakaian: cpy <asal> <tujuan>",
            "mvf": "Pemakaian: mvf <asal> <tujuan>",
            "f": "Pemakaian: f <pola-nama-file>",
            "gr": "Pemakaian: gr <kata> <lokasi>",
            "z": "Pemakaian: z <file.zip>",
            "tz": "Pemakaian: tz <file.tar.gz>",
            "w": "Pemakaian: w <url>",
            "cu": "Pemakaian: cu <url>",
            "tts": "Pemakaian: tts <kalimat>",
        }
        return usages.get(shortcut)

    @staticmethod
    def _quiet_label(shortcut, extra_args):
        target = " ".join(extra_args)
        labels = {
            "u": "Memperbarui daftar paket",
            "ug": "Meng-upgrade paket",
            "i": f"Memasang {target}",
            "un": f"Menghapus {target}",
            "pi": f"Memasang library {target}",
        }
        return labels.get(shortcut, shortcut)

    @staticmethod
    def _drain(stream, sink):
        """Baca output command ke dalam buffer, bukan ke layar."""
        try:
            for line in stream:
                sink.append(line.rstrip("\n"))
        except (ValueError, OSError):
            pass

    def run_quiet(self, command, label):
        """Jalankan command dengan satu baris spinner, tanpa membanjiri layar."""
        # Di luar terminal interaktif, animasi dimatikan agar aman untuk pipe.
        if not sys.stdout.isatty():
            return self.run_external(command)

        try:
            process = subprocess.Popen(
                command,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                text=True,
                errors="replace",
                bufsize=1,
            )
        except FileNotFoundError:
            print(f"\033[1;31m\u2718  Command tidak ditemukan: {command[0]}\033[0m")
            return 1
        except OSError as error:
            print(f"\033[1;31m\u2718  Gagal menjalankan command: {error}\033[0m")
            return 1

        buffer = []
        reader = threading.Thread(
            target=self._drain, args=(process.stdout, buffer), daemon=True
        )
        reader.start()

        start = time.time()
        index = 0
        interrupted = False
        try:
            while process.poll() is None:
                frame = self.SPINNER_FRAMES[index % len(self.SPINNER_FRAMES)]
                elapsed = int(time.time() - start)
                sys.stdout.write(
                    f"\r\033[2K\033[1;36m{frame}\033[0m  {label} "
                    f"\033[1;30m\u00b7 {elapsed}s\033[0m"
                )
                sys.stdout.flush()
                index += 1
                time.sleep(self.SPINNER_INTERVAL)
        except KeyboardInterrupt:
            interrupted = True
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

        reader.join(timeout=2)
        duration = time.time() - start
        sys.stdout.write("\r\033[2K")
        sys.stdout.flush()

        self.last_output = buffer
        self.last_label = label

        if interrupted:
            print(f"\033[1;33m\u25cb  Dibatalkan\033[0m \033[1;30m\u00b7 {label}\033[0m")
            return 130

        code = process.returncode
        if code == 0:
            print(
                f"\033[1;32m\u2714\033[0m  {label} "
                f"\033[1;30m\u00b7 {duration:.1f}s\033[0m"
            )
        else:
            print(f"\033[1;31m\u2718  Gagal\033[0m \033[1;30m\u00b7 exit {code}\033[0m")
            for line in [entry for entry in buffer if entry.strip()][-5:]:
                print(f"   \033[1;30m{line}\033[0m")
            print("   \033[1;30mKetik 'log' untuk output lengkap.\033[0m")
        return code

    def execute_shortcut(self, shortcut, extra_args):
        """Expand and execute one of the built-in shortcuts."""
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
            status = self.run_quiet(["pkg", "update"], "Memperbarui daftar paket")
            if status == 0:
                self.run_quiet(["pkg", "upgrade", "-y"], "Meng-upgrade paket")
            return

        command = list(self.SHORTCUTS[shortcut][0])
        if shortcut in self.JOINED_ARG_SHORTCUTS:
            # These commands expect the message as one single value.
            command.append(" ".join(extra_args))
            if shortcut == "n":
                command[1:1] = ["--content"]
        else:
            command.extend(extra_args)

        if shortcut in self.QUIET_SHORTCUTS:
            self.run_quiet(command, self._quiet_label(shortcut, extra_args))
            return
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
        print(f"Ketik 'h' untuk melihat {self.SHORTCUT_COUNT} shortcut Nusantara OS.\n")
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
                if command_name == "log":
                    self.show_last_log()
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
