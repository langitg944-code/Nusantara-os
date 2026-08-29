# ☁️ Nusantara OS V3
**The Next-Gen Single-File Terminal Environment**

*Dikembangkan oleh Langit — Built for Security & Aesthetics*

Nusantara OS adalah wrapper terminal berbasis Python untuk **Termux** dan Linux. Dengan Nusantara OS, command Termux yang panjang bisa dipanggil menggunakan shortcut yang lebih singkat.

## 🚀 Fitur Unggulan
- **Single-File Architecture:** hanya satu file Python, tanpa dependensi eksternal.
- **25 Command Shortcuts:** command paket, Python, file, dan Termux API dibuat lebih singkat.
- **Paranoid Security:** autentikasi SHA-256 dan proteksi karakter shell berbahaya.
- **Hyper-Aesthetic UI:** desain neon dengan prompt ala Powerline.
- **Safe Command Runner:** command dijalankan tanpa `shell=True`.

## ⚡ 25 Shortcut Nusantara OS

Ketik `h` atau `help` setelah login untuk melihat daftar ini langsung dari aplikasi.

| Shortcut | Command panjang | Contoh |
|---|---|---|
| `u` | `pkg update` | `u` |
| `ug` | `pkg upgrade` | `ug` |
| `up` | `pkg update` lalu `pkg upgrade` | `up` |
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

Shortcut `o`, `url`, `sh`, `clip`, `paste`, `n`, `v`, `cam`, `loc`, dan `wifi` membutuhkan package/aplikasi **Termux:API** di perangkat Android.

## 📦 Instalasi

Jalankan di Termux atau Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/langitg944-code/Nusantara-OS/main/nusantara.py -o nusantara.py && chmod +x nusantara.py && python3 nusantara.py
```

Setelah login, ketik `h` untuk melihat semua shortcut.
