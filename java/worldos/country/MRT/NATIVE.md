# MRT — العربية

اضغط F9 أو Shift+Space للتبديل إلى الكتابة بالعربية.

```sh
make build
make desktop ARGS=--network
make run
make image
```

Source: `النص-المصدري`; examples: `example/`.
Guest: `help input`, `example java`, `cd /example/java`, `vi مثالطباعة.java`.
Build: Python 3, JDK javac (--release 8), Clang/Clang++, aarch64-linux-gnu binutils, libnewlib-dev.
Bundled QEMU: x86_64 Linux. Other hosts: set QEMU_AARCH64 to a raspi4b-capable QEMU.
No build-time dependency on another country, /home/user/jkoros, or golang/worldos.
Country archives: independent regular native-vendor.tar.gz and qemu-host.tar.gz; language subfolders use the parent country archives. Copy the entire country for offline independence.
The country folder can be copied and built without the WorldOS shared resources.
To export only the generated native sources, use make native-export COUNTRY=MRT OUTPUT=/path/to/new-directory.
Existing Linux editions under language-code folders are preserved. Their Makefiles add native-* targets; make -f native.mk x86-iso builds the copied x86 kernel.
Names: native-names.tsv; incomplete translations: native-pending.tsv. Native-speaker and historical-etymology review remains pending.
Rendering: BMP glyphs + emoji; complex-script shaping and full bidirectional layout remain incomplete.
Input: keyboard; US host positions; AltGr for additional symbols.

Network / system: `help system` (standard and local command names both accepted).
IP configuration: edit project `ip.conf`; default `192.168.0.100/24`, gateway `192.168.0.1`. An `ip.conf` beside `native.json` overrides the shared file. Standalone copies use `النص-المصدري/ip.conf`. Rebuild/restart after changes; regenerate board images too.
IPv4: `ipconfig`, `ipconfig set 192.168.0.120 255.255.255.0 192.168.0.1`, `ip addr show`, `ping -c 4 192.168.0.1`.
Status: `route`, `netstat` / `ss`, `ps`, `top` (q quits), `free`, `df`, `uptime`; shutdown: `poweroff`.
Settings last until reboot. df measures RAM files, not SD. ps measures native tasks, not Linux processes.
Inbound NAT after changing IP: `make desktop ARGS="--network --guest-ip 192.168.0.120"`, then configure that IP in the guest.
Independent concurrent VM network: add `--network-host 127.0.0.2 --port 5903`.

| Standard | Local command |
|---|---|
| `ipconfig` | `إعداد-الشبكة` |
| `ip` | `عنوان-الشبكة` |
| `ping` | `اختبار-الصدى` |
| `route` | `المسارات` |
| `netstat` | `الاتصالات` |
| `ps` | `العمليات` |
| `top` | `مراقبة-النشاط` |
| `free` | `الذاكرة` |
| `df` | `التخزين` |
| `uptime` | `مدة-التشغيل` |
| `poweroff` | `إيقاف-التشغيل` |
| `help` | `مساعدة` |

Command translations still pending: none.
Command names are functional proposals; native-speaker terminology review remains pending.
The native kernel retains its existing JVM/Python/C/network limits. No full Java SE, SD filesystem, physical Pi input/network driver claim.
