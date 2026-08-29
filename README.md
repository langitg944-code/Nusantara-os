<div align="center">

```
 _  _ _  _ ____ ____ _  _ ___ ____ ____ ____
 |\ | |  | [__  |__| |\ |  |  |__| |__/ |__|
 | \| |__| ___] |  | | \|  |  |  | |  \ |  |
```

# Nusantara OS

**Satu file Python. Lima puluh shortcut. Nol dependensi.**

![version](https://img.shields.io/badge/version-V4.1--QUIET-black?style=flat-square)
![python](https://img.shields.io/badge/python-3.7%2B-blue?style=flat-square)
![platform](https://img.shields.io/badge/platform-Termux%20%7C%20Linux-green?style=flat-square)
![license](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)

*Dikembangkan oleh Langit — built for speed, security & aesthetics*

</div>

---

> Terminal di layar 6 inci itu ruang sempit.
> Nusantara OS memampatkan command panjang jadi satu-dua huruf,
> lalu menahan output yang tidak perlu supaya layar tetap bersih.

Nusantara OS adalah **wrapper terminal berbasis Python** untuk **Termux** dan Linux. Ia berdiri di antara kamu dan shell: menerima command pendek, mengembangkannya menjadi command penuh, lalu menjalankannya secara aman tanpa `shell=True`.

---

## ▸ Sorotan Fitur

| Fitur | Keterangan |
|---|---|
| **Single-File Architecture** | Satu file `nusantara.py`. Tanpa `requirements.txt`, tanpa `pip install`. |
| **50 Command Shortcuts** | Paket, Python, Git, file, jaringan, dan Termux API — semua dipangkas. |
| **Quiet Mode** | Command paket berjalan di balik satu baris spinner. Layar tidak dibanjiri log. |
| **Ghost Vault** | Master key di-hash SHA-256. Salah 3 kali → self-destruct. |
| **Ghost Shield** | Karakter kontrol shell ditolak di pintu masuk. |
| **Safe Command Runner** | Semua eksekusi lewat `subprocess` dengan `shell=False`. |
| **Hyper-Aesthetic UI** | Banner neon, prompt ala Powerline, indikator path live. |

---

## ▸ Quiet Mode

Biasanya `pkg update` memuntahkan puluhan baris `Get:1 ... Hit:2 ...` sampai layar penuh. Di Nusantara OS, output itu ditahan dan diganti **satu baris hidup** yang berputar di tempat:

```
⠹  Memperbarui daftar paket · 4s
```

Selesai, baris itu diganti ringkasan:

```
✔  Memperbarui daftar paket · 6.2s
```

Kalau gagal, hanya 5 baris error terakhir yang ditampilkan:

```
✘  Gagal · exit 100
   E: Unable to locate package xyz
   Ketik 'log' untuk output lengkap.
```

**Cara kerjanya:**

- Spinner memakai frame braille `⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏`, berputar tiap 0,08 detik di baris yang sama — tidak pernah menggeser layar ke bawah.
- Aktif untuk shortcut bertanda `●` di menu `h`: **`u` `ug` `up` `i` `un` `pi`**.
- `up` berjalan dua fase berurutan: *Memperbarui daftar paket* → *Meng-upgrade paket*.
- Output penuh tetap disimpan. Ketik **`log`** kapan saja untuk membacanya.
- Tekan **Ctrl+C** untuk membatalkan — proses dihentikan rapi, ditandai `○ Dibatalkan`.
- Kalau output di-pipe atau bukan terminal interaktif, spinner otomatis mati dan command berjalan normal. Aman dipakai di dalam script.

Shortcut lain — `gcl`, `w`, `run`, `gp` — sengaja **tidak** di-quiet, karena progress bawaannya justru berguna untuk dilihat.

---

## ▸ Instalasi

Satu baris, langsung jalan:

```bash
curl -fsSL https://raw.githubusercontent.com/langitg944-code/Nusantara-os/main/nusantara.py -o nusantara.py && chmod +x nusantara.py && python3 nusantara.py
```

Untuk shortcut Termux API, pasang dulu:

```bash
pkg install termux-api
```

lalu install aplikasi **Termux:API** dari F-Droid.

---

## ▸ Alur Login

```
[1] Run pertama    → GHOST INITIALIZATION → buat Master Key
[2] Run berikutnya  → ENTER KEY
[3] Salah 3x        → PURGE: vault + script dihapus permanen
```

Setelah masuk, ketik `h` untuk memanggil daftar lengkap 50 shortcut langsung dari dalam aplikasi.

---

## ▸ Kamus Shortcut

> Tanda `●` = berjalan dalam Quiet Mode.

### Paket & Sistem

| Shortcut | Menjadi | Contoh |
|---|---|---|
| `u` ● | `pkg update` | `u` |
| `ug` ● | `pkg upgrade -y` | `ug` |
| `up` ● | `pkg update` + `pkg upgrade` | `up` |
| `i` ● | `pkg install -y` | `i git` |
| `un` ● | `pkg uninstall` | `un git` |
| `s` | `pkg search` | `s python` |
| `li` | `pkg list-installed` | `li` |
| `py` | `python` | `py --version` |
| `pi` ● | `pip install` | `pi requests` |
| `run` | `python` | `run bot.py` |
| `c` | `clear` | `c` |
| `h` | `help` | `h` |
| `q` | `exit` | `q` |
| `si` | `sys-info` | `si` |
| `la` | `ls -lah` | `la` |

### Git

| Shortcut | Menjadi | Contoh |
|---|---|---|
| `g` | `git` | `g remote -v` |
| `gs` | `git status -sb` | `gs` |
| `ga` | `git add` | `ga .` |
| `gc` | `git commit -m` | `gc "fix login bug"` |
| `gp` | `git push` | `gp origin main` |
| `gl` | `git log --oneline -10` | `gl` |
| `gd` | `git diff` | `gd nusantara.py` |
| `gcl` | `git clone` | `gcl https://github.com/user/repo` |

### File & Folder

| Shortcut | Menjadi | Contoh |
|---|---|---|
| `e` | `nano` | `e config.txt` |
| `ct` | `cat` | `ct notes.md` |
| `mk` | `mkdir -p` | `mk project/src` |
| `del` | `rm -i` | `del sampah.log` |
| `cpy` | `cp -r` | `cpy src backup` |
| `mvf` | `mv` | `mvf lama.py baru.py` |
| `f` | `find . -name` | `f "*.py"` |
| `gr` | `grep -rn` | `gr TODO .` |
| `z` | `unzip` | `z arsip.zip` |
| `tz` | `tar -xzvf` | `tz data.tar.gz` |

### Disk & Jaringan

| Shortcut | Menjadi | Contoh |
|---|---|---|
| `d` | `df -h` | `d` |
| `w` | `wget` | `w https://example.com/file.zip` |
| `cu` | `curl -L` | `cu https://example.com` |
| `myip` | `curl -s https://ifconfig.me` | `myip` |

### Termux API & Perangkat

| Shortcut | Menjadi | Contoh |
|---|---|---|
| `o` | `termux-open` | `o foto.jpg` |
| `url` | `termux-open-url` | `url https://example.com` |
| `sh` | `termux-share` | `sh file.zip` |
| `clip` | `termux-clipboard-set` | `clip "Halo Nusantara"` |
| `paste` | `termux-clipboard-get` | `paste` |
| `n` | `termux-notification` | `n "Backup selesai"` |
| `v` | `termux-vibrate` | `v` |
| `cam` | `termux-camera-photo` | `cam foto.jpg` |
| `loc` | `termux-location` | `loc` |
| `wifi` | `termux-wifi-connectioninfo` | `wifi` |
| `bat` | `termux-battery-status` | `bat` |
| `tts` | `termux-tts-speak` | `tts "selamat pagi"` |
| `stor` | `termux-setup-storage` | `stor` |

> Shortcut pada bagian **Termux API & Perangkat** membutuhkan package `termux-api` dan aplikasi **Termux:API**.

---

## ▸ Command Tambahan

| Command | Fungsi |
|---|---|
| `log` | Tampilkan output lengkap command Quiet Mode terakhir |
| `cd` | Pindah direktori |
| `sys-info` | Info sistem dan versi |
| `help` | Sama dengan `h` |
| `exit` | Keluar |

---

## ▸ Catatan Keamanan

- **Tanpa shell.** Command dieksekusi dengan `shell=False`, jadi injeksi lewat karakter kontrol tidak punya jalan masuk.
- **Filter karakter.** Input yang mengandung karakter kontrol shell langsung ditolak `GHOST-SHIELD`.
- **Redirection terbatas.** Hanya satu `>` atau `>>` di akhir baris yang diizinkan.
- **Self-destruct itu nyata.** Tiga kali salah key akan menghapus `.nusa_vault` **dan** file script itu sendiri. Simpan cadangan jika perlu.

---

## ▸ Command di Luar Kamus

Shortcut bukan penjara. Command apa pun yang tidak terdaftar tetap diteruskan ke sistem seperti biasa — `cd`, `ls`, `ping`, `nano`, semuanya jalan. Nusantara OS hanya memotong yang sering kamu ketik.

---

## ▸ Kontribusi

Pull request dan issue terbuka.

- Shortcut baru → tambahkan di dict `SHORTCUTS`.
- Argumen harus digabung jadi satu kalimat → daftarkan di `JOINED_ARG_SHORTCUTS`.
- Ingin command berjalan senyap dengan spinner → daftarkan di `QUIET_SHORTCUTS`.

---

## ▸ Lisensi

MIT — lihat [LICENSE](LICENSE).

<div align="center">

**Nusantara OS** · *Sistem Termux yang dibuat mudah* 💛

</div>
