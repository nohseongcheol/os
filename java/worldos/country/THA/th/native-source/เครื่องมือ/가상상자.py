#!/usr/bin/env python3
"""jkoros 전용 VirtualBox แอป_ลิ้นชักแอป. 기존 VM/디스크/เก็บ_ค่า 상태는 삭제하지 않는다."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import uuid


class 실행오류(RuntimeError):
    pass


def ดําเนินการ_เชลล์_คําสั่ง(อาร์กิวเมนต์):
    สภาพแวดล้อม = dict(os.environ, LC_ALL='C')
    ผลลัพธ์ = subprocess.run([str(ค่า) for ค่า in อาร์กิวเมนต์], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=สภาพแวดล้อม, timeout=180)
    เนื้อหา_ค่า = ผลลัพธ์.stdout.decode('utf-8', 'replace')
    if ผลลัพธ์.returncode:
        raise 실행오류('คําสั่ง ความล้มเหลว_ค่า: ' + ' '.join(str(ค่า) for ค่า in อาร์กิวเมนต์) + '\n' + เนื้อหา_ค่า[-10000:])
    return เนื้อหา_ค่า


def แอตทริบิวต์_ค่า(เนื้อหา_ค่า):
    ผลลัพธ์ = {}
    for บรรทัด in เนื้อหา_ค่า.splitlines():
        if '=' not in บรรทัด:
            continue
        ชื่อ, ค่า = บรรทัด.split('=', 1)
        if ชื่อ.startswith('"'):
            ชื่อ = json.loads(ชื่อ)
        if ค่า.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(ค่า)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(ค่า): ค่า = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox แอตทริบิวต์_ค่า รูปแบบ_ค่า_d1a42ea5 ข้อผิดพลาด: ' + บรรทัด)
        ผลลัพธ์[ชื่อ] = ค่า
    return ผลลัพธ์


def 등록목록(เนื้อหา_ค่า):
    ผลลัพธ์ = {}
    for บรรทัด in เนื้อหา_ค่า.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', บรรทัด)
        if 일치: ผลลัพธ์[일치.group(2).lower()] = 일치.group(1)
    return ผลลัพธ์


def 검사합(เส้นทาง):
    ค่า = hashlib.sha256()
    with เส้นทาง.open('rb') as แฟ้ม:
        for ข้อมูล in iter(lambda: แฟ้ม.read(1024 * 1024), b''): ค่า.update(ข้อมูล)
    return ค่า.hexdigest()


class แอป_ลิ้นชักแอป:
    def __init__(self, ราก_ค่า, ชื่อ, เมธอด_โหมด='gui', คําสั่ง=ดําเนินการ_เชลล์_คําสั่ง):
        self.ราก_ค่า = Path(ราก_ค่า).resolve()
        self.ชื่อ, self.เมธอด_โหมด, self.คําสั่ง = ชื่อ, เมธอด_โหมด, คําสั่ง
        self.보관 = self.ราก_ค่า / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', ชื่อ) or ชื่อ in ('.', '..'):
            raise 실행오류('VM 이름은 문자·ตัวเลข_ค่า·공백·밑줄·괄호·마침표·하이픈만 사용할 หมายเลข 있습니다.')
        if เมธอด_โหมด not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def เส้นทาง(self, ชั้น_ค่า):
        if Path(ชั้น_ค่า).is_absolute() or '..' in Path(ชั้น_ค่า).parts:
            raise 실행오류('잘못된 관리 เส้นทาง: ' + str(ชั้น_ค่า))
        ผลลัพธ์ = self.보관
        for 부분 in ['.vbox'] + list(Path(ชั้น_ค่า).parts):
            if 부분 == '.vbox': ผลลัพธ์ = self.보관
            else: ผลลัพธ์ = ผลลัพธ์ / 부분
            if ผลลัพธ์.is_symlink(): raise 실행오류('เชื่อมต่อ 경로는 사용하지 않습니다: ' + str(ผลลัพธ์))
        return ผลลัพธ์

    def อ่าน(self):
        เส้นทาง = self.เส้นทาง('state.json')
        if not เส้นทาง.exists(): return None
        สถานะ_ค่า = json.loads(เส้นทาง.read_text(encoding='utf-8'))
        if สถานะ_ค่า.get('version') != 1 or สถานะ_ค่า.get('name') != self.ชื่อ:
            raise 실행오류('관리 상태의 VM ชื่อ/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for ชื่อ in ('uuid', 'owner'):
            if str(uuid.UUID(สถานะ_ค่า[ชื่อ])) != สถานะ_ค่า[ชื่อ]: raise 실행오류('잘못된 VM ตัวระบุ_ค่า')
        return สถานะ_ค่า

    def เก็บ_ค่า(self, สถานะ_ค่า):
        ปลายทาง_ค่า_a0fbc067 = self.เส้นทาง('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as แฟ้ม:
            json.dump(สถานะ_ค่า, แฟ้ม, ensure_ascii=False, indent=2)
            แฟ้ม.write('\n')
            임시 = แฟ้ม.name
        os.replace(임시, str(ปลายทาง_ค่า_a0fbc067))

    def ข้อมูลระบบ(self, สถานะ_ค่า, 등록됨, กู้คืน_สถานะ=False):
        if สถานะ_ค่า['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        ข้อมูลระบบ = แอตทริบิวต์_ค่า(self.คําสั่ง(['VBoxManage', 'showvminfo', สถานะ_ค่า['uuid'], '--machinereadable']))
        ตําแหน่ง = Path(ข้อมูลระบบ.get('CfgFile', '')).resolve()
        if self.เส้นทาง('machines').resolve() not in ตําแหน่ง.parents or ข้อมูลระบบ.get('UUID') != สถานะ_ค่า['uuid']:
            raise 실행오류('이 프로젝트의 VM ตั้งค่า เส้นทาง/UUID와 일치하지 않아 변경하지 않습니다.')
        มาร์กเกอร์_ค่า = self.คําสั่ง(['VBoxManage', 'getextradata', สถานะ_ค่า['uuid'], 'JKOROS/Owner']).strip()
        if มาร์กเกอร์_ค่า != 'Value: ' + สถานะ_ค่า['owner']:
            if กู้คืน_สถานะ and สถานะ_ค่า.get('pending') and มาร์กเกอร์_ค่า == 'No value set!':
                self.คําสั่ง(['VBoxManage', 'setextradata', สถานะ_ค่า['uuid'], 'JKOROS/Owner', สถานะ_ค่า['owner']])
            else:
                raise 실행오류('VM เจ้าของ_ค่า 표식이 일치하지 않아 변경하지 않습니다.')
        return ข้อมูลระบบ

    def เช็ค_สื่อข้อมูล(self, สถานะ_ค่า, ข้อมูลระบบ):
        제어기들 = [ค่า for ชื่อ, ค่า in ข้อมูลระบบ.items() if re.fullmatch(r'storagecontrollername\d+', ชื่อ)]
        อนุญาต_ค่า = [str(self.เส้นทาง(ค่า)) for ค่า in สถานะ_ค่า.get('media', [])]
        for ชื่อ, ค่า in ข้อมูลระบบ.items():
            if any(re.fullmatch(re.escape(ตัวควบคุม) + r'-\d+-\d+', ชื่อ) for ตัวควบคุม in 제어기들):
                if ค่า not in ('none', 'emptydrive') and ค่า not in อนุญาต_ค่า:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + ค่า)

    def แสดง_สถานะ(self):
        สถานะ_ค่า = self.อ่าน()
        if สถานะ_ค่า is None: return {'name': self.ชื่อ, 'state': 'not-created'}
        ข้อมูลระบบ = self.ข้อมูลระบบ(สถานะ_ค่า, 등록목록(self.คําสั่ง(['VBoxManage', 'list', 'vms'])))
        return {'name': ข้อมูลระบบ.get('name', สถานะ_ค่า['name']), 'uuid': สถานะ_ค่า['uuid'], 'state': ข้อมูลระบบ.get('VMState'),
                'iso': str(self.เส้นทาง(สถานะ_ค่า['iso'])) if สถานะ_ค่า.get('iso') else None,
                'serial_log': str(self.เส้นทาง(สถานะ_ค่า['serial_log'])) if สถานะ_ค่า.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def ดําเนินการ_คําสั่ง(self):
        สถานะ_ค่า = self.อ่าน()
        등록됨 = 등록목록(self.คําสั่ง(['VBoxManage', 'list', 'vms']))
        ข้อมูลระบบ = None
        if สถานะ_ค่า is not None and สถานะ_ค่า['uuid'] in 등록됨:
            ข้อมูลระบบ = self.ข้อมูลระบบ(สถานะ_ค่า, 등록됨, กู้คืน_สถานะ=True)
            ปัจจุบัน_รายการ = ข้อมูลระบบ.get('VMState')
            if ปัจจุบัน_รายการ == 'running':
                print('이미 ดําเนินการ_คําสั่ง 중입니다. 재빌드·재시작하지 않습니다.')
                return self.แสดง_สถานะ()
            self.เช็ค_สื่อข้อมูล(สถานะ_ค่า, ข้อมูลระบบ)
            if ปัจจุบัน_รายการ in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 เก็บ_ค่า 상태를 버리지 않습니다.'.format(ปัจจุบัน_รายการ))
                if ปัจจุบัน_รายการ == 'paused':
                    self.คําสั่ง(['VBoxManage', 'controlvm', สถานะ_ค่า['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 ลองอีกครั้ง_ค่า เปิด 전에 기존 기록도 보관한다.
                    if สถานะ_ค่า.get('serial_log'):
                        원본 = self.เส้นทาง(สถานะ_ค่า['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.เส้นทาง('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.คําสั่ง(['VBoxManage', 'startvm', สถานะ_ค่า['uuid'], '--type', self.เมธอด_โหมด])
                return self.แสดง_สถานะ()
            if ปัจจุบัน_รายการ not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 สลับ_โหมด 중입니다 ({}). 작업이 끝난 ย้อนกลับ_ค่า ลองอีกครั้ง_ค่า 실행하세요.'.format(ปัจจุบัน_รายการ))
        elif สถานะ_ค่า is not None and not สถานะ_ค่า.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 ลองอีกครั้ง_ค่า 등록하세요.')
        elif self.ชื่อ in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # เก็บ_ค่า/ดําเนินการ_คําสั่ง 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.คําสั่ง(['make', '-C', str(self.ราก_ค่า / 'os'), 'iso']), end='')
        원본 = self.ราก_ค่า / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        สื่อข้อมูล_ค่า = 'media/kernel-' + 검사합(원본) + '.iso'
        ปลายทาง_ค่า_a0fbc067 = self.เส้นทาง(สื่อข้อมูล_ค่า)
        ปลายทาง_ค่า_a0fbc067.parent.mkdir(exist_ok=True)
        if ปลายทาง_ค่า_a0fbc067.exists():
            if 검사합(ปลายทาง_ค่า_a0fbc067) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(ปลายทาง_ค่า_a0fbc067))
        else:
            with tempfile.NamedTemporaryFile(dir=str(ปลายทาง_ค่า_a0fbc067.parent)) as แฟ้ม:
                shutil.copyfile(str(원본), แฟ้ม.name)
                os.link(แฟ้ม.name, str(ปลายทาง_ค่า_a0fbc067))

        if สถานะ_ค่า is None:
            สถานะ_ค่า = {'version': 1, 'name': self.ชื่อ, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.เก็บ_ค่า(สถานะ_ค่า)
        if ข้อมูลระบบ is None:
            self.คําสั่ง(['VBoxManage', 'createvm', '--name', สถานะ_ค่า['name'], '--uuid', สถานะ_ค่า['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.เส้นทาง('machines')), '--register'])
            self.คําสั่ง(['VBoxManage', 'setextradata', สถานะ_ค่า['uuid'], 'JKOROS/Owner', สถานะ_ค่า['owner']])
        # สร้าง 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        ข้อมูลระบบ = self.ข้อมูลระบบ(สถานะ_ค่า, 등록목록(self.คําสั่ง(['VBoxManage', 'list', 'vms'])))
        if ข้อมูลระบบ.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('สร้าง 중 VM 상태가 바뀌었습니다. ลองอีกครั้ง_ค่า make vbox를 실행하세요.')
        self.เช็ค_สื่อข้อมูล(สถานะ_ค่า, ข้อมูลระบบ)
        สถานะ_ค่า['iso'] = สื่อข้อมูล_ค่า
        if สื่อข้อมูล_ค่า not in สถานะ_ค่า['media']: สถานะ_ค่า['media'].append(สื่อข้อมูล_ค่า)
        สถานะ_ค่า['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        บันทึก_ค่า = self.เส้นทาง(สถานะ_ค่า['serial_log'])
        บันทึก_ค่า.parent.mkdir(exist_ok=True)
        self.เก็บ_ค่า(สถานะ_ค่า)
        self.คําสั่ง(['VBoxManage', 'modifyvm', สถานะ_ค่า['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(บันทึก_ค่า)])
        제어기들 = [ค่า for ชื่อ, ค่า in ข้อมูลระบบ.items() if re.fullmatch(r'storagecontrollername\d+', ชื่อ)]
        if 'JKOROS IDE' not in 제어기들:
            self.คําสั่ง(['VBoxManage', 'storagectl', สถานะ_ค่า['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.คําสั่ง(['VBoxManage', 'storageattach', สถานะ_ค่า['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(ปลายทาง_ค่า_a0fbc067)])
        สถานะ_ค่า['pending'] = False
        self.เก็บ_ค่า(สถานะ_ค่า)
        self.คําสั่ง(['VBoxManage', 'startvm', สถานะ_ค่า['uuid'], '--type', self.เมธอด_โหมด])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.แสดง_สถานะ()


def เรียกใช้งาน():
    แยกวิเคราะห์_ค่า = argparse.ArgumentParser(description='jkoros 전용 VirtualBox ดําเนินการ_คําสั่ง 및 สถานะ_ค่า คิวรี_ค่า')
    แยกวิเคราะห์_ค่า.add_argument('action', choices=['run', 'status'])
    พารามิเตอร์_อาร์กิวเมนต์ = แยกวิเคราะห์_ค่า.parse_args()
    ดําเนินการ_คําสั่ง = แอป_ลิ้นชักแอป(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if พารามิเตอร์_อาร์กิวเมนต์.action == 'status':
        print(json.dumps(ดําเนินการ_คําสั่ง.แสดง_สถานะ(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 หมายเลข 없습니다. โฮสต์ 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/สิทธิ์_ค่า 변경은 하지 않습니다.')
    os.umask(0o077)
    ดําเนินการ_คําสั่ง.เส้นทาง('lock').parent.mkdir(parents=True, exist_ok=True)
    with ดําเนินการ_คําสั่ง.เส้นทาง('lock').open('a') as ล็อก_ค่า:
        try: fcntl.flock(ล็อก_ค่า, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox ดําเนินการ_คําสั่ง 작업이 진행 중입니다.')
        print(json.dumps(ดําเนินการ_คําสั่ง.ดําเนินการ_คําสั่ง(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: เรียกใช้งาน()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ข้อผิดพลาด:
        print('VBOX ข้อผิดพลาด: ' + str(ข้อผิดพลาด), file=sys.stderr)
        sys.exit(1)
