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
from executeCommand import projectRoot
from CoslDistribution import bindEndpoint


def calculateHash(path):
    value = hashlib.sha256()
    with path.open('rb') as fileEntry:
        for dataBlock in iter(lambda: fileEntry.read(1024 * 1024), b''): value.update(dataBlock)
    return value.hexdigest()


def run():
    Parser = argparse.ArgumentParser(description=__doc__)
    Parser.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD machine_boot HDMI/프레임버퍼 size')
    resolutionValue = Parser.parse_args().resolution
    widthValue, heightValue = map(int, resolutionValue.split('x'))
    screenGroup, screenMode = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[resolutionValue]
    firmwareValue = projectRoot / 'vendor/pi4-firmware.tar.gz'
    expected = firmwareValue.with_name(firmwareValue.name + '.sha256')
    license_ = projectRoot / 'vendor/LICENCE.broadcom'
    if not firmwareValue.is_file() or not expected.is_file():
        raise SystemExit('공식 Pi machine_boot 펌웨어 groupValue neededValue: ' + str(firmwareValue))
    if calculateHash(firmwareValue) != expected.read_text().split()[0]:
        raise SystemExit('펌웨어 groupValue SHA256 불일치')
    if not license_.is_file():
        raise SystemExit('machine_boot 펌웨어 라이선스 file missingMethod: ' + str(license_))
    distributionPath = projectRoot / 'dist'
    distributionPath.mkdir(exist_ok=True)
    relinkBundle = bindEndpoint()
    totalCapacity, run = 128 * 1024 * 1024, 2048
    sectorCount = totalCapacity // 512 - run
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(projectRoot / 'build')) as workingPath:
        stageValue = Path(workingPath)
        bootPath = stageValue / 'boot'
        (bootPath / 'overlays').mkdir(parents=True)
        fileList = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(firmwareValue)) as archive:
            for name in fileList:
                member = archive.getmember('./' + name)
                if not member.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + name)
                with archive.extractfile(member) as originalAddress, (bootPath / name).open('wb') as destinationValuePosition:
                    shutil.copyfileobj(originalAddress, destinationValuePosition)
        shutil.copyfile(str(projectRoot / 'build/kernel8.img'), str(bootPath / 'kernel8.img'))
        settings = (projectRoot / 'machine_boot/config.txt').read_text()
        settings = settings.replace('hdmi_group=2', 'hdmi_group=' + str(screenGroup)).replace('hdmi_mode=4', 'hdmi_mode=' + str(screenMode))
        settings = settings.replace('framebuffer_width=640', 'framebuffer_width=' + str(widthValue)).replace('framebuffer_height=480', 'framebuffer_height=' + str(heightValue))
        (bootPath / 'config.txt').write_text(settings)
        shutil.copyfile(str(license_), str(bootPath / 'LICENCE.broadcom'))
        shutil.copyfile(str(projectRoot / 'vendor/LICENSE.micropython'), str(bootPath / 'LICENSE.micropython'))
        for name in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(projectRoot.parents[1] / name), str(bootPath / name))
        shutil.copyfile(str(relinkBundle), str(bootPath / relinkBundle.name))
        for originalData, name in ((projectRoot/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (projectRoot/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (projectRoot/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (projectRoot/'vendor/LICENSE.genet','LICENSE.genet'),
                             (projectRoot/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (projectRoot/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (projectRoot/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (projectRoot/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(originalData), str(bootPath/name))
        for name in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(projectRoot / 'vendor' / name), str(bootPath / name))
        (bootPath / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 tools/executeCommand.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 tools/executeCommand.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/README.md.\n')
        partitionFile = stageValue / 'boot.fat'
        with partitionFile.open('wb') as fileEntry: fileEntry.truncate(sectorCount * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(run), '-n', 'JKJAVA', str(partitionFile)])
        subprocess.check_call(['mcopy', '-i', str(partitionFile), '-s'] + [str(dataPosition) for dataPosition in sorted(bootPath.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 buildSystem 결과와 equal 확인한다.
        extracted = stageValue / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(partitionFile), '::/kernel8.img', str(extracted)])
        if calculateHash(extracted) != calculateHash(projectRoot / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 kernelValue SHA256 불일치')
        image = stageValue / 'jkoros-native-rpi4.img'
        MasterBootRecord = bytearray(512)
        MasterBootRecord[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', run, sectorCount)
        MasterBootRecord[510:512] = b'\x55\xaa'
        with image.open('wb') as resultData:
            resultData.truncate(totalCapacity); resultData.write(MasterBootRecord); resultData.seek(run * 512)
            with partitionFile.open('rb') as originalAddress: shutil.copyfileobj(originalAddress, resultData)
        bundleManifest = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
                    'license': 'COSL with third-party/LGPL carve-outs',
                    'relink_archive': relinkBundle.name, 'relink_sha256': calculateHash(relinkBundle),
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
                    'java_gui_example': '/example/java/WindowExample.java; run: java WindowExample',
                    'framebuffer_resolution': [widthValue, heightValue], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': firmwareValue.name, 'source_sha256': calculateHash(firmwareValue),
                    'image_sha256': calculateHash(image), 'boot_files': {}}
        for dataPosition in sorted(bootPath.rglob('*')):
            if dataPosition.is_file(): bundleManifest['boot_files'][str(dataPosition.relative_to(bootPath))] = calculateHash(dataPosition)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux buildImage/User 디스크는 건드리지 않는다.
        os.replace(str(image), str(distributionPath / image.name))
        archiveBase = stageValue / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(archiveBase), 'zip', str(bootPath))
        os.replace(str(archiveBase) + '.zip', str(distributionPath / 'jkoros-native-rpi4-boot.zip'))
        (distributionPath / 'manifest.json').write_text(json.dumps(bundleManifest, indent=2) + '\n')
    print('generate:', distributionPath / 'jkoros-native-rpi4.img')
    print('actualData Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    run()
