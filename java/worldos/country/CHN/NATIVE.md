# CHN — Chinese

按 F9 或 Shift+Space 可切换到中文拼音输入。

```sh
make build
make desktop ARGS=--network
make run
make image
```

Source: `源代码`; examples: `example/`.
Guest: `help input`, `example java`, `cd /example/java`, `vi 输出例.java`.
Build: Python 3, JDK javac (--release 8), Clang/Clang++, aarch64-linux-gnu binutils, libnewlib-dev.
Bundled QEMU: x86_64 Linux. Other hosts: set QEMU_AARCH64 to a raspi4b-capable QEMU.
No build-time dependency on another country, /home/user/jkoros, or golang/worldos.
Country archives: independent regular native-vendor.tar.gz and qemu-host.tar.gz; language subfolders use the parent country archives. Copy the entire country for offline independence.
The country folder can be copied and built without the WorldOS shared resources.
To export only the generated native sources, use make native-export COUNTRY=CHN OUTPUT=/path/to/new-directory.
Existing Linux editions under language-code folders are preserved. Their Makefiles add native-* targets; make -f native.mk x86-iso builds the copied x86 kernel.
Names: native-names.tsv; incomplete translations: native-pending.tsv. Native-speaker and historical-etymology review remains pending.
Rendering: BMP glyphs + emoji; complex-script shaping and full bidirectional layout remain incomplete.
Input: candidates; Syllable candidates: Space cycles, F9 commits. No predictive phrase model.

Network / system: `help system` (standard and local command names both accepted).
IP configuration: edit project `ip.conf`; default `192.168.0.100/24`, gateway `192.168.0.1`. An `ip.conf` beside `native.json` overrides the shared file. Standalone copies use `源代码/ip.conf`. Rebuild/restart after changes; regenerate board images too.
IPv4: `ipconfig`, `ipconfig set 192.168.0.120 255.255.255.0 192.168.0.1`, `ip addr show`, `ping -c 4 192.168.0.1`.
Status: `route`, `netstat` / `ss`, `ps`, `top` (q quits), `free`, `df`, `uptime`; shutdown: `poweroff`.
Settings last until reboot. df measures RAM files, not SD. ps measures native tasks, not Linux processes.
Inbound NAT after changing IP: `make desktop ARGS="--network --guest-ip 192.168.0.120"`, then configure that IP in the guest.
Independent concurrent VM network: add `--network-host 127.0.0.2 --port 5903`.

| Standard | Local command |
|---|---|
| `ipconfig` | `网络设置` |
| `ip` | `网络地址` |
| `ping` | `回声测试` |
| `route` | `路由表` |
| `netstat` | `网络状态` |
| `ps` | `进程列表` |
| `top` | `运行概况` |
| `free` | `内存状态` |
| `df` | `存储容量` |
| `uptime` | `运行时间` |
| `poweroff` | `关机` |
| `help` | `帮助` |

Command translations still pending: none.
Command names are functional proposals; native-speaker terminology review remains pending.
The native kernel retains its existing JVM/Python/C/network limits. No full Java SE, SD filesystem, physical Pi input/network driver claim.
