#!/usr/bin/env python3
"""SD용 MBR/FAT32 이미지만 생성한다. 물리 디스크는 열지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tarfile
import tempfile
from စက်မောင်း import စီမံကိန်းအမြစ်
from COSL배포 import စက်ဖိုင်ထုပ်ပိုး


def 해시계산(လမ်း):
    တန်ဖိုး = hashlib.sha256()
    with လမ်း.open('rb') as ဖိုင်အချက်:
        for ဒေတာအတုံး in iter(lambda: ဖိုင်အချက်.read(1024 * 1024), b''): တန်ဖိုး.update(ဒေတာအတုံး)
    return တန်ဖိုး.hexdigest()


def လုပ်ဆောင်():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD စက်တင် HDMI/프레임버퍼 အရွယ်')
    ကြည်လင်ပြတ်သားမှုတန်ဖိုး = 해석기.parse_args().resolution
    အနံတန်ဖိုး, အမြင့်တန်ဖိုး = map(int, ကြည်လင်ပြတ်သားမှုတန်ဖိုး.split('x'))
    မျက်နှာပြင်အုပ်စု, မျက်နှာပြင်နည်းစနစ် = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[ကြည်လင်ပြတ်သားမှုတန်ဖိုး]
    기초제어프로그램 = စီမံကိန်းအမြစ် / 'vendor/pi4-firmware.tar.gz'
    예상결과 = 기초제어프로그램.with_name(기초제어프로그램.name + '.sha256')
    이용허락파일 = စီမံကိန်းအမြစ် / 'vendor/LICENCE.broadcom'
    if not 기초제어프로그램.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi စက်တင် 펌웨어 အုပ်စုတန်ဖိုး 필요: ' + str(기초제어프로그램))
    if 해시계산(기초제어프로그램) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 အုပ်စုတန်ဖိုး SHA256 불일치')
    if not 이용허락파일.is_file():
        raise SystemExit('စက်တင် 펌웨어 라이선스 ဖိုင် 없음: ' + str(이용허락파일))
    ဖြန့်ချိမှုလမ်းကြောင်း = စီမံကိန်းအမြစ် / 'dist'
    ဖြန့်ချိမှုလမ်းကြောင်း.mkdir(exist_ok=True)
    재연결꾸러미 = စက်ဖိုင်ထုပ်ပိုး()
    စုစုပေါင်းဆံ့ပမာဏ, လုပ်ဆောင် = 128 * 1024 * 1024, 2048
    စက်ကွက်အရေအတွက် = စုစုပေါင်းဆံ့ပမာဏ // 512 - လုပ်ဆောင်
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(စီမံကိန်းအမြစ် / 'build')) as လုပ်ဆောင်လမ်း:
        အဆင့်ကာလတန်ဖိုး = Path(လုပ်ဆောင်လမ်း)
        စက်တင်လမ်းကြောင်း = အဆင့်ကာလတန်ဖိုး / 'boot'
        (စက်တင်လမ်းကြောင်း / 'overlays').mkdir(parents=True)
        ဖိုင်စာရင်း = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(기초제어프로그램)) as မော်ကွန်း:
            for အမည် in ဖိုင်စာရင်း:
                အဖွဲ့ဝင် = မော်ကွန်း.getmember('./' + အမည်)
                if not အဖွဲ့ဝင်.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + အမည်)
                with မော်ကွန်း.extractfile(အဖွဲ့ဝင်) as မူရင်းလိပ်စာ, (စက်တင်လမ်းကြောင်း / အမည်).open('wb') as ဦးတည်ရာတန်ဖိုးနေရာ:
                    shutil.copyfileobj(မူရင်းလိပ်စာ, ဦးတည်ရာတန်ဖိုးနေရာ)
        shutil.copyfile(str(စီမံကိန်းအမြစ် / 'build/kernel8.img'), str(စက်တင်လမ်းကြောင်း / 'kernel8.img'))
        သတ်မှတ်ချက် = (စီမံကိန်းအမြစ် / 'စက်တင်/config.txt').read_text()
        သတ်မှတ်ချက် = သတ်မှတ်ချက်.replace('hdmi_group=2', 'hdmi_group=' + str(မျက်နှာပြင်အုပ်စု)).replace('hdmi_mode=4', 'hdmi_mode=' + str(မျက်နှာပြင်နည်းစနစ်))
        သတ်မှတ်ချက် = သတ်မှတ်ချက်.replace('framebuffer_width=640', 'framebuffer_width=' + str(အနံတန်ဖိုး)).replace('framebuffer_height=480', 'framebuffer_height=' + str(အမြင့်တန်ဖိုး))
        (စက်တင်လမ်းကြောင်း / 'config.txt').write_text(သတ်မှတ်ချက်)
        shutil.copyfile(str(이용허락파일), str(စက်တင်လမ်းကြောင်း / 'LICENCE.broadcom'))
        shutil.copyfile(str(စီမံကိန်းအမြစ် / 'vendor/LICENSE.micropython'), str(စက်တင်လမ်းကြောင်း / 'LICENSE.micropython'))
        for အမည် in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(စီမံကိန်းအမြစ်.parents[1] / အမည်), str(စက်တင်လမ်းကြောင်း / အမည်))
        shutil.copyfile(str(재연결꾸러미), str(စက်တင်လမ်းကြောင်း / 재연결꾸러미.name))
        for မူရင်းဒေတာ, အမည် in ((စီမံကိန်းအမြစ်/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (စီမံကိန်းအမြစ်/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (စီမံကိန်းအမြစ်/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (စီမံကိန်းအမြစ်/'vendor/LICENSE.genet','LICENSE.genet'),
                             (စီမံကိန်းအမြစ်/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (စီမံကိန်းအမြစ်/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (စီမံကိန်းအမြစ်/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (စီမံကိန်းအမြစ်/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(မူရင်းဒေတာ), str(စက်တင်လမ်းကြောင်း/အမည်))
        for အမည် in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(စီမံကိန်းအမြစ် / 'vendor' / အမည်), str(စက်တင်လမ်းကြောင်း / အမည်))
        (စက်တင်လမ်းကြောင်း / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 ကိရိယာစု/စက်မောင်း.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 ကိရိယာစု/စက်မောင်း.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/လမ်းညွှန်.md.\n')
        အပိုင်းခြားမှုဖိုင် = အဆင့်ကာလတန်ဖိုး / 'boot.fat'
        with အပိုင်းခြားမှုဖိုင်.open('wb') as ဖိုင်အချက်: ဖိုင်အချက်.truncate(စက်ကွက်အရေအတွက် * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(လုပ်ဆောင်), '-n', 'JKJAVA', str(အပိုင်းခြားမှုဖိုင်)])
        subprocess.check_call(['mcopy', '-i', str(အပိုင်းခြားမှုဖိုင်), '-s'] + [str(ဒေတာနေရာ) for ဒေတာနေရာ in sorted(စက်တင်လမ်းကြောင်း.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 တည်ဆောက် 결과와 ညီ 확인한다.
        추출자료 = အဆင့်ကာလတန်ဖိုး / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(အပိုင်းခြားမှုဖိုင်), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(စီမံကိန်းအမြစ် / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 အူတိုင်တန်ဖိုး SHA256 불일치')
        စက်ကုဒ်ပုံရိပ် = အဆင့်ကာလတန်ဖိုး / 'jkoros-native-rpi4.img'
        주부트기록 = bytearray(512)
        주부트기록[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', လုပ်ဆောင်, စက်ကွက်အရေအတွက်)
        주부트기록[510:512] = b'\x55\xaa'
        with စက်ကုဒ်ပုံရိပ်.open('wb') as ရလဒ်ဒေတာ:
            ရလဒ်ဒေတာ.truncate(စုစုပေါင်းဆံ့ပမာဏ); ရလဒ်ဒေတာ.write(주부트기록); ရလဒ်ဒေတာ.seek(လုပ်ဆောင် * 512)
            with အပိုင်းခြားမှုဖိုင်.open('rb') as မူရင်းလိပ်စာ: shutil.copyfileobj(မူရင်းလိပ်စာ, ရလဒ်ဒေတာ)
        꾸러미명세 = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
                    'license': 'COSL with third-party/LGPL carve-outs',
                    'relink_archive': 재연결꾸러미.name, 'relink_sha256': 해시계산(재연결꾸러미),
                    'user_abi': 1, 'elf_extension_required': False, 'linux_static_elf_subset': True,
                    'full_linux_binary_compatibility': False,
                    'openjdk': False, 'guest_java': 'jkoros JVM 0.4 subset/JAR with Korean library and native Swing subset',
                    'guest_c_compiler': 'TinyCC ARM64, own ABI', 'guest_aot': 'static Java int/reference subset to native ARM64 ELF',
                    'all_class_or_jar_compatible': False,
                    'python': 'MicroPython 1.24.1 integer build', 'cpython': False,
                    'network': 'lwIP IPv4 TCP/UDP/ARP/ICMP; GENET v5 DHCP or QEMU UART1 SLIP', 'ftp': 'guest anonymous passive RAM service',
                    'genet_ethernet': True, 'physical_network_tested': False,
                    'ssh': 'native libassh server :22, shared console', 'vnc': 'native authenticated RFB 3.8 :5900', 'rdp': False,
                    'gui': 'four resizable terminal windows and native Swing subset peers',
                    'terminal_resize': 'hover corner; hold left mouse button and drag; live shell/vi grid',
                    'java_gui_example': '/example/java/ဝင်းဥပမာ.java; run: java ဝင်းဥပမာ',
                    'framebuffer_resolution': [အနံတန်ဖိုး, အမြင့်တန်ဖိုး], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': 기초제어프로그램.name, 'source_sha256': 해시계산(기초제어프로그램),
                    'image_sha256': 해시계산(စက်ကုဒ်ပုံရိပ်), 'boot_files': {}}
        for ဒေတာနေရာ in sorted(စက်တင်လမ်းကြောင်း.rglob('*')):
            if ဒေတာနေရာ.is_file(): 꾸러미명세['boot_files'][str(ဒေတာနေရာ.relative_to(စက်တင်လမ်းကြောင်း))] = 해시계산(ဒေတာနေရာ)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux စက်ပုံရိပ်တည်ဆောက်/သုံးစွဲသူ 디스크는 건드리지 않는다.
        os.replace(str(စက်ကုဒ်ပုံရိပ်), str(ဖြန့်ချိမှုလမ်းကြောင်း / စက်ကုဒ်ပုံရိပ်.name))
        မော်ကွန်းအခြေ = အဆင့်ကာလတန်ဖိုး / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(မော်ကွန်းအခြေ), 'zip', str(စက်တင်လမ်းကြောင်း))
        os.replace(str(မော်ကွန်းအခြေ) + '.zip', str(ဖြန့်ချိမှုလမ်းကြောင်း / 'jkoros-native-rpi4-boot.zip'))
        (ဖြန့်ချိမှုလမ်းကြောင်း / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('ထုတ်လုပ်:', ဖြန့်ချိမှုလမ်းကြောင်း / 'jkoros-native-rpi4.img')
    print('တကယ့်ဒေတာ Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    လုပ်ဆောင်()
