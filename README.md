<div align="center">

```
 _  _ _  _ ____ ____ _  _ ___ ____ ____ ____
 |\ | |  | [__  |__| |\ |  |  |__| |__/ |__|
 | \| |__| ___] |  | | \|  |  |  | |  \ |  |
```

# Nusantara OS

**Satu file Python. Lima puluh shortcut. Nol dependensi.**

![version](https://img.shields.io/badge/version-V4.0--SHORTCUTS-black?style=flat-square)
![python](https://img.shields.io/badge/python-3.7%2B-blue?style=flat-square)
![platform](https://img.shields.io/badge/platform-Termux%20%7C%20Linux-green?style=flat-square)
![license](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)

*Dikembangkan oleh Langit \u2014 built for speed, security & aesthetics*

</div>

---

> Terminal di layar 6 inci itu ruang sempit.
> Nusantara OS memampatkan command panjang jadi satu-dua huruf,
> tanpa mengorbankan keamanan dan tanpa menambah satu pun dependensi.

Nusantara OS adalah **wrapper terminal berbasis Python** untuk **Termux** dan Linux. Ia berdiri di antara kamu dan shell: menerima command pendek, mengembangkannya menjadi command penuh, lalu menjalankannya secara aman tanpa `shell=True`.

---

## \u25b8 Sorotan Fitur

| | |
|---|---|
| **Single-File Architecture** | Satu file `nusantara.py`. Tanpa `requirements.txt`, tanpa `pip install`. |
| **50 Command Shortcuts** | Paket, Python, Git, file, jaringan, dan Termux API \u2014 semua dipangkas. |
| **Ghost Vault** | Master key di-hash SHA-256. Salah 3 kali \u2192 self-destruct. |
| **Ghost Shield** | Karakter shell berbahaya (`;` `&` <code>&#124;</code> `` ` `` `$` `(` `)` `<`) ditolak di pintu masuk. |
| **Safe Command Runner** | Semua eksekusi lewat `subprocess` dengan `shell=False`. |
| **Hyper-Aesthetic UI** | Banner neon, prompt ala Powerline, indikator path live. |

---

## \u25b8 Instalasi

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

## \u25b8 Alur Login

```
[1] Run pertama   \u2192 GHOST INITIALIZATION \u2192 buat Master Key
[2] Run berikutnya \u2192 ENTER KEY
[3] Salah 3x       \u2192 PURGE: vault + script dihapus permanen
```

Setelah masuk, ketik `h` untuk memanggil daftar lengkap 50 shortcut langsung dari dalam aplikasi.

---

## \u25b8 Kamus Shortcut

### Paket & Sistem

| Shortcut | Menjadi | Contoh |
|---|---|---|
| `u` | `pkg update` | `u` |
| `ug` | `pkg upgrade` | `ug` |
| `up` | `pkg update` + `pkg upgrade` | `up` |
| `i` | `pkg install` | `i git` |
| `un` | `pkg uninstall` | `un git` |
| `s` | `pkg search` | `s python` |
| `li` | `pkg list-installed` | `li` |
| `py` | `python` | `py --version` |
| `pi` | `pip install` | `pi requests` |
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

## \u25b8 Catatan Keamanan

- **Tanpa shell.** Command dieksekusi dengan `shell=False`, jadi injeksi lewat `;` atau `&&` tidak punya jalan masuk.
- **Filter karakter.** Input yang mengandung karakter kontrol shell langsung ditolak `GHOST-SHIELD`.
- **Redirection terbatas.** Hanya satu `>` atau `>>` di akhir baris yang diizinkan.
- **Self-destruct itu nyata.** Tiga kali salah key akan menghapus `.nusa_vault` **dan** file script itu sendiri. Simpan cadangan jika perlu.

---

## \u25b8 Command di Luar Kamus

Shortcut bukan penjara. Command apa pun yang tidak terdaftar tetap diteruskan ke sistem seperti biasa \u2014 `cd`, `ls`, `ping`, `nano`, semuanya jalan. Nusantara OS hanya memotong yang sering kamu ketik.

---

## \u25b8 Kontribusi

Pull request dan issue terbuka. Tambahkan shortcut baru di dict `SHORTCUTS`, dan jika argumennya harus digabung jadi satu kalimat, daftarkan namanya di `JOINED_ARG_SHORTCUTS`.

---

## \u25b8 Lisensi

MIT \u2014 lihat [LICENSE](LICENSE).

<div align="center">

**Nusantara OS** \u00b7 *Sistem Termux yang dibuat mudah* \U0001f49b

</div>
