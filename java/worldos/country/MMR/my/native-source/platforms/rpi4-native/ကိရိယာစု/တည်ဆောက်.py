#!/usr/bin/env python3
"""အိမ်ရှင် javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from သုံးစွဲသူနေရာလပ်တည်ဆောက် import သုံးစွဲသူနေရာလပ်ဖန်တီး
from ကွန်ရက်တည်ဆောက် import ကွန်ရက်ဖန်တီး
from ဥပမာတည်ဆောက် import ဥပမာများဖန်တီး
from အဝေးတည်ဆောက် import အဝေးဖန်တီး

စီမံကိန်းအမြစ် = Path(__file__).resolve().parents[1]
저장소 = စီမံကိန်းအမြစ်.parents[1]
လမ်းကြောင်းတည်ဆောက် = စီမံကိန်းအမြစ် / 'build'


def စက်မောင်း(ပေးအချက်အခင်းအကျင်း):
    subprocess.check_call([str(ပထမတန်ဖိုး) for ပထမတန်ဖိုး in ပေးအချက်အခင်းအကျင်း], cwd=str(စီမံကိန်းအမြစ်))


def လုပ်ဆောင်():
    လမ်းကြောင်းတည်ဆောက်.mkdir(exist_ok=True)
    Cဘာသာပြန်စက် = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    ချိတ်ဆက်စက်ကိရိယာတစ်ခု = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    목적파일변환기 = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    မော်ကွန်းကိရိယာတစ်ခု = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for ကိရိယာစု in ('javac', Cဘာသာပြန်စက်, 시플플번역기, ချိတ်ဆက်စက်ကိရိယာတစ်ခု, 목적파일변환기, မော်ကွန်းကိရိယာတစ်ခု):
        if not shutil.which(ကိရိယာစု):
            raise SystemExit('필요한 တည်ဆောက် ကိရိယာစု 없음: ' + ကိရိယာစု)
    စာလုံးပုံစံအချက်အလက် = json.loads((စီမံကိန်းအမြစ် / 'vendor/terminal-font.json').read_text())
    စာလုံးပုံစံဒေတာ = (စီမံကိန်းအမြစ် / 'vendor/terminal-font.bin').read_bytes()
    if len(စာလုံးပုံစံဒေတာ) != 65616 * 32 or hashlib.sha256(စာလုံးပုံစံဒေတာ).hexdigest() != စာလုံးပုံစံအချက်အလက်['sha256']:
        raise SystemExit('အဆုံးသုံးမျက်နှာပြင် စာလုံးပုံစံတန်ဖိုး အရွယ်/SHA256 불일치')
    တင်ပို့ဇယား = {'jshell_interactive': 'အမိန့်ဝင်းဝင်ထွက်.ဖြစ်သောအပြန်အလှန်', 'jshell_output': 'အမိန့်ဝင်းဝင်ထွက်.အထွက်', 'jshell_input': 'အမိန့်ဝင်းဝင်ထွက်.ဝင်ဒေတာ', 'java_task': 'အူတိုင်.အလုပ်', 'jfs_path_start': 'မှတ်ဉာဏ်ဖိုင်.လမ်းကြောင်းစတင်',
               'jfs_path_byte': 'မှတ်ဉာဏ်ဖိုင်.လမ်းကြောင်းဘိုက်', 'jfs_open': 'မှတ်ဉာဏ်ဖိုင်.ဖွင့်',
               'jfs_read': 'မှတ်ဉာဏ်ဖိုင်.ဖတ်', 'jfs_write': 'မှတ်ဉာဏ်ဖိုင်.ရေး',
               'jfs_seek': 'မှတ်ဉာဏ်ဖိုင်.နေရာနေရာရှာရွှေ့', 'jfs_close': 'မှတ်ဉာဏ်ဖိုင်.ပိတ်',
               'jfs_size': 'မှတ်ဉာဏ်ဖိုင်.အရွယ်', 'jfs_unlink': 'မှတ်ဉာဏ်ဖိုင်.အချက်ဖျက်',
               'jfs_truncate': 'မှတ်ဉာဏ်ဖိုင်.အလျားသတ်မှတ်'}
    တင်ပို့ဇယား.update({'jfs_entry_count': 'မှတ်ဉာဏ်ဖိုင်.ဖိုင်ကန့်သတ်ချက်', 'jfs_entry_length': 'မှတ်ဉာဏ်ဖိုင်.ထုတ်ပေးအမည်အရှည်', 'jfs_entry_byte': 'မှတ်ဉာဏ်ဖိုင်.ထုတ်ပေးအမည်ဘိုက်', 'jfs_entry_size': 'မှတ်ဉာဏ်ဖိုင်.ထုတ်ပေးဖိုင်အရွယ်'})
    တင်ပို့ဇယား.update({'jdraw_prepare': 'မျက်နှာပြင်ပေါင်းစပ်.ပြင်ဆင်', 'jdraw_width': 'မျက်နှာပြင်ပေါင်းစပ်.အနံယူ',
        'jdraw_height': 'မျက်နှာပြင်ပေါင်းစပ်.အမြင့်ယူ', 'jdraw_count_low': 'မျက်နှာပြင်ပေါင်းစပ်.ရေတွက်သူနိမ့်ယူ',
        'jdraw_count_high': 'မျက်နှာပြင်ပေါင်းစပ်.ရေတွက်သူမြင့်ယူ', 'jdraw_clip': 'မျက်နှာပြင်ပေါင်းစပ်.ဖြတ်နယ်ပယ်',
        'jdraw_clip_value': 'မျက်နှာပြင်ပေါင်းစပ်.ဖြတ်နယ်ပယ်တန်ဖိုး', 'jdraw_begin': 'မျက်နှာပြင်ပေါင်းစပ်.လုပ်ဆောင်',
        'jdraw_end': 'မျက်နှာပြင်ပေါင်းစပ်.ပြီးဆုံး', 'jdraw_pixel': 'မျက်နှာပြင်ပေါင်းစပ်.ပုံမှတ်',
        'jdraw_rectangle': 'မျက်နှာပြင်ပေါင်းစပ်.စတုဂံဖြည့်', 'jdraw_pointer': 'မျက်နှာပြင်ပေါင်းစပ်.ညွှန်တံ'})
    တင်ပို့ဇယား.update({'jfs_mkdir': 'မှတ်ဉာဏ်ဖိုင်.ဖိုင်တွဲဖန်တီး', 'jfs_rmdir': 'မှတ်ဉာဏ်ဖိုင်.ဖိုင်တွဲဖယ်ရှား', 'jfs_kind': 'မှတ်ဉာဏ်ဖိုင်.အချက်အမျိုးအစား'})
    တင်ပို့ဇယား.update({'jnet_socket': 'ပြန်လှည့်ကွန်ရက်.အချက်ဖန်တီး', 'jnet_bind': 'ပြန်လှည့်ကွန်ရက်.စက်ဖိုင်ထုပ်ပိုး',
        'jnet_put': 'ပြန်လှည့်ကွန်ရက်.ဒေတာထား', 'jnet_get': 'ပြန်လှည့်ကွန်ရက်.ဒေတာဖတ်', 'jnet_send': 'ပြန်လှည့်ကွန်ရက်.ပို့',
        'jnet_recv': 'ပြန်လှည့်ကွန်ရက်.လက်ခံ', 'jnet_port': 'ပြန်လှည့်ကွန်ရက်.အဆုံးမှတ်ဆက်သွယ်ပေါက်ဖတ်', 'jnet_address': 'ပြန်လှည့်ကွန်ရက်.လိပ်စာဖတ်',
        'jnet_peer': 'ပြန်လှည့်ကွန်ရက်.ပို့သူအဆုံးမှတ်', 'jnet_close': 'ပြန်လှည့်ကွန်ရက်.ပိတ်'})
    တင်ပို့ဇယား.update({'jstream_create': 'စီးကြောင်းဆက်သွယ်မှု.အချက်ဖန်တီး', 'jstream_bind': 'စီးကြောင်းဆက်သွယ်မှု.စက်ဖိုင်ထုပ်ပိုး', 'jstream_listen': 'စီးကြောင်းဆက်သွယ်မှု.အဆုံးမှတ်နားထောင်', 'jstream_connect': 'စီးကြောင်းဆက်သွယ်မှု.ချိတ်ဆက်', 'jstream_accept': 'စီးကြောင်းဆက်သွယ်မှု.ချိတ်ဆက်မှုလက်ခံ', 'jstream_read': 'စီးကြောင်းဆက်သွယ်မှု.ဖတ်', 'jstream_write': 'စီးကြောင်းဆက်သွယ်မှု.ရေး', 'jstream_port': 'စီးကြောင်းဆက်သွယ်မှု.အဆုံးမှတ်ဆက်သွယ်ပေါက်ဖတ်', 'jstream_peer': 'စီးကြောင်းဆက်သွယ်မှု.တစ်ဖက်ပေါက်ဖတ်', 'jstream_close': 'စီးကြောင်းဆက်သွယ်မှု.ပိတ်'})
    for သင်္ကေတတန်ဖိုး in list(တင်ပို့ဇယား):
        if သင်္ကေတတန်ဖိုး.startswith('jstream_') or သင်္ကေတတန်ဖိုး.startswith('jnet_') and သင်္ကေတတန်ဖိုး not in ('jnet_put', 'jnet_get'):
            တင်ပို့ဇယား[သင်္ကေတတန်ဖိုး.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = တင်ပို့ဇယား.pop(သင်္ကေတတန်ဖိုး)
    예제들 = ['public final class အထုပ် { public static void ပြင်ဆင်() {']
    for လမ်း in sorted((စီမံကိန်းအမြစ် / 'ဥပမာ').iterdir()):
        if လမ်း.is_file():
            예제들.append('အမိန့်အဓိပ္ပာယ်ဖော်.တည်ငြိမ်ဖိုင်(%s, %s);' %
                (json.dumps(လမ်း.name), json.dumps(လမ်း.read_text(encoding='utf-8'), ensure_ascii=True)))
    (လမ်းကြောင်းတည်ဆောက် / 'အထုပ်.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    ဥပမာများဖန်တီး(စီမံကိန်းအမြစ်, 저장소, စက်မောင်း)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(လမ်းကြောင်းတည်ဆောက်)) as လုပ်ဆောင်လမ်း:
        အတန်းလမ်းကြောင်း = Path(လုပ်ဆောင်လမ်း)
        စက်မောင်း(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', အတန်းလမ်းကြောင်း, '-sourcepath', အတန်းလမ်းကြောင်း, '-d', အတန်းလမ်းကြောင်း] + sorted((စီမံကိန်းအမြစ် / 'မူရင်းကုဒ်').glob('*.java')) + [လမ်းကြောင်းတည်ဆောက် / 'အထုပ်.java', လမ်းကြောင်းတည်ဆောက် / 'ဥပမာအထုပ်.java'])
        # ဖိုင်·အမိန့်ဝင်း·ဝင်း 세션·통신과 Java မျက်နှာပြင် 합성 배열을 အားလုံးတည်ဆောက် 수용한다.
        ပေးအချက်အခင်းအကျင်း = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'အူတိုင်.လုပ်ဆောင်', '--heap-words', '1048576', '-o', လမ်းကြောင်းတည်ဆောက် / 'kernel-java.c']
        for သင်္ကေတတန်ဖိုး, နည်းလမ်းအချက် in sorted(တင်ပို့ဇယား.items()):
            ပေးအချက်အခင်းအကျင်း += ['--export', သင်္ကေတတန်ဖိုး + '=' + နည်းလမ်းအချက်]
        စက်မောင်း(ပေးအချက်အခင်းအကျင်း + sorted(အတန်းလမ်းကြောင်း.glob('*.class')))
    (လမ်းကြောင်းတည်ဆောက် / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    ပြင်ဆင်မှုဘစ်များ = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    POSIX = 저장소 / 'posix-kor/arm64-native'
    သုံးစွဲသူနေရာလပ်ဖန်တီး(စီမံကိန်းအမြစ်, 저장소, Cဘာသာပြန်စက်, 시플플번역기, ချိတ်ဆက်စက်ကိရိယာတစ်ခု, မော်ကွန်းကိရိယာတစ်ခု, ပြင်ဆင်မှုဘစ်များ, စက်မောင်း)
    ကွန်ရက်သုံးမှု = ကွန်ရက်ဖန်တီး(စီမံကိန်းအမြစ်, Cဘာသာပြန်စက်, မော်ကွန်းကိရိယာတစ်ခု, ပြင်ဆင်မှုဘစ်များ, စက်မောင်း)
    အဝေးသုံး = အဝေးဖန်တီး(စီမံကိန်းအမြစ်, Cဘာသာပြန်စက်, မော်ကွန်းကိရိယာတစ်ခု, ပြင်ဆင်မှုဘစ်များ, စက်မောင်း)
    포함인수 = ['-I', POSIX / 'ခေါင်းစီးဖိုင်', '-I', လမ်းကြောင်းတည်ဆောက်]
    빌드작업 = [(Cဘာသာပြန်စက်, [], လမ်းကြောင်းတည်ဆောက် / 'terminal-font.S', 'font.o'),
            (Cဘာသာပြန်စက်, ['-std=c11', '-Wall', '-Wextra', '-Werror'], စီမံကိန်းအမြစ် / 'စက်/အဆုံးသုံးမျက်နှာပြင်.c', 'terminal.o'),
            (Cဘာသာပြန်စက်, ['-std=c11', '-Wall', '-Wextra', '-Werror'], စီမံကိန်းအမြစ် / 'စက်/မြင်ကွင်းအစိတ်အပိုင်း.c', 'widgets.o'),
            (Cဘာသာပြန်စက်, ['-std=c11'], လမ်းကြောင်းတည်ဆောက် / 'kernel-java.c', 'java.o'),
            (Cဘာသာပြန်စက်, ['-std=c11', '-Wall', '-Wextra', '-Werror'], စီမံကိန်းအမြစ် / 'စက်/ဆားကစ်ပြား.c', 'board.o'),
            (Cဘာသာပြန်စက်, ['-std=c11', '-Wall', '-Wextra', '-Werror'], စီမံကိန်းအမြစ် / 'စက်/မျက်နှာပြင်ပုံရေးဆွဲမှု.c', 'drawing.o'),
            (Cဘာသာပြန်စက်, ['-std=c11', '-Wall', '-Wextra', '-Werror'], စီမံကိန်းအမြစ် / 'စက်/သုံးစွဲသူ.c', 'user.o'),
            (Cဘာသာပြန်စက်, [], စီမံကိန်းအမြစ် / 'စက်တင်/အချက်အမှတ်တစ်ခုတန်ဖိုး.S', 'entry.o'),
            (Cဘာသာပြန်စက်, ['-std=c11', '-Wall', '-Wextra', '-Werror'], POSIX / 'ချိတ်ဆက်.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], စီမံကိန်းအမြစ် / 'စမ်းသပ်မှု/파일호출.cpp', 'cpp.o')]
    for ဘာသာပြန်စက်ကိရိယာတစ်ခု, 추가영역, မူရင်းဒေတာ, 출력결과 in 빌드작업:
        မူရင်းပြင်ဆင်မှု = [ဖိုင်အချက် for ဖိုင်အချက် in ပြင်ဆင်မှုဘစ်များ if ဖိုင်အချက် != '-mgeneral-regs-only'] if မူရင်းဒေတာ.suffix == '.S' else ပြင်ဆင်မှုဘစ်များ
        စက်မောင်း([ဘာသာပြန်စက်ကိရိယာတစ်ခု] + မူရင်းပြင်ဆင်မှု + 추가영역 + 포함인수 + ['-c', မူရင်းဒေတာ, '-o', လမ်းကြောင်းတည်ဆောက် / 출력결과])
    စက်မောင်း([မော်ကွန်းကိရိယာတစ်ခု, 'rcs', လမ်းကြောင်းတည်ဆောက် / 'libposix-kor-arm64.a', လမ်းကြောင်းတည်ဆောက် / 'posix.o'])
    စက်မောင်း([ချိတ်ဆက်စက်ကိရိယာတစ်ခု, '--gc-sections', '-T', စီမံကိန်းအမြစ် / 'စက်တင်/နေရာချထားပုံ.ld', '-Map', လမ်းကြောင်းတည်ဆောက် / 'kernel.map', '-o', လမ်းကြောင်းတည်ဆောက် / 'kernel.elf'] +
        [လမ်းကြောင်းတည်ဆောက် / အမည် for အမည် in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', လမ်းကြောင်းတည်ဆောက် / 'libposix-kor-arm64.a', ကွန်ရက်သုံးမှု, အဝေးသုံး, လမ်းကြောင်းတည်ဆောက် / 'remote/libassh.a', လမ်းကြောင်းတည်ဆောက် / 'remote/libbearssl.a', '--end-group'])
    စက်မောင်း([목적파일변환기, '-O', 'binary', လမ်းကြောင်းတည်ဆောက် / 'kernel.elf', လမ်းကြောင်းတည်ဆောက် / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'မြန်မာ.ကိုယ်ပိုင်', 'korean_exceptions': 20,
                                 'full_awt_swing': False, 'swing_subset': ['JFrame','JPanel','JLabel','JButton','JTextField','ActionListener','SwingUtilities.invokeLater'], 'java_se_certified': False},
                'python': 'MicroPython 1.24.1 integer build', 'cpython': False,
                'pip': {'kind': 'source installer with host PyPI HTTPS relay', 'commands': ['install','list','uninstall'], 'cpython_pip': False, 'dependencies': False, 'persistent': False},
                'korean_c_api': 'independent structs, enum constants and real function symbols',
                'framebuffer': {'format': 'RGB32', 'default': [640,480], 'maximum': [1920,1080], 'boot_configurable': True, 'size_syscall': 22},
                'shell': 'UTF-8 editor/history, directories, variables, scripts, sequential pipes, redirects, ELF execution',
                'system_commands': ['ipconfig','ip','ifconfig','ping','route','netstat','ss','ps','top','free','df','uptime','poweroff'],
                'system_status': 'real lwIP interface/endpoints, native task/session PIDs, AOT heap pools, RAM filesystem slots',
                'ip_configuration': 'GENET DHCP on real Pi4; static IPv4/netmask/gateway; volatile; close active sockets before address changes',
                'ping': 'real ICMPv4 echo, numeric addresses, count/timeout/RTT; no DNS resolver',
                'poweroff': 'BCM2835 PM firmware-halt watchdog; QEMU guest shutdown; physical Pi untested',
                'pipe_capacity_bytes': 16384, 'posix_shell_complete': False,
                'ram_files': {'count': 64, 'bytes_each': 16384, 'directories': 16, 'persistent': False},
                'user_abi': 1, 'user_elf64': True, 'elf_extension_required': False,
                'linux_static_elf_subset': True, 'full_linux_binary_compatibility': False,
                'mmu': True, 'user_timeout_seconds': 2, 'cooperative_user_sessions': 4,
                'interactive_wait_renews_deadline': True, 'vi': 'native EL0 UTF-8 vi subset',
                'network': 'lwIP 2.2.0 IPv4 TCP/UDP/ARP/ICMP; GENET v5 Ethernet or UART1 SLIP', 'external_network': True,
                'external_network_transport': 'Pi4 GENET (hardware untested); QEMU auxiliary UART SLIP bridge',
                'ftp': 'guest service, passive binary transfers, anonymous root RAM workspace',
                'genet_ethernet': True, 'genet_driver_status': 'implemented; MMIO/MDIO model tests only', 'physical_network_tested': False,
                'ssh': {'implementation': 'guest libassh 1.1 / LGPL-2.1-or-later', 'port': 22, 'password_auth': True, 'console': 'shared kernel shell', 'independent_sessions': False, 'sftp': False, 'port_forwarding': False},
                'vnc': {'implementation': 'guest RFB 3.8 / VNC authentication / raw incremental tiles', 'port': 5900, 'encrypted_pixels': False, 'clients': 1, 'korean_input': 'native two-set F9/Shift+Space'},
                'rdp': False,
                'gui': 'four native terminal windows and Swing subset peers; guest VNC server with native input; optional QEMU VNC bridge',
                'native_usb_input': False, 'full_swing': False, 'swing_subset': True, 'sha256': {}}
    for အမည် in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][အမည်] = hashlib.sha256((လမ်းကြောင်းတည်ဆောက် / အမည်).read_bytes()).hexdigest()
    (လမ်းကြောင်းတည်ဆောက် / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('ဖြစ်သောအပြည့်အစုံ:', လမ်းကြောင်းတည်ဆောက် / 'kernel8.img')


if __name__ == '__main__':
    လုပ်ဆောင်()
