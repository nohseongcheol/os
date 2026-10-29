#!/usr/bin/env python3
"""jkoros 전용 VirtualBox ແອັບ_ຕົວເປີດໃຊ້. 기존 VM/디스크/ຮ້ານຄ້າ_ຄ່າ 상태는 삭제하지 않는다."""
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


def ປະ_ຕິ_ບັດ_ເຊລ_ຄໍາສັ່ງ(인수):
    환경 = dict(os.environ, LC_ALL='C')
    ມາດຕະການ = subprocess.run([str(ຄ່າ) for ຄ່າ in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    ເນື້ອໃນ_ຄ່າ_cb0f2404 = ມາດຕະການ.stdout.decode('utf-8', 'replace')
    if ມາດຕະການ.returncode:
        raise 실행오류('ຄໍາສັ່ງ_1f12b8e2 ຫຼົ້ມເຫຼວ_ຄ່າ: ' + ' '.join(str(ຄ່າ) for ຄ່າ in 인수) + '\n' + ເນື້ອໃນ_ຄ່າ_cb0f2404[-10000:])
    return ເນື້ອໃນ_ຄ່າ_cb0f2404


def ຄຸນສົມບັດ_ຄ່າ(ເນື້ອໃນ_ຄ່າ_cb0f2404):
    ມາດຕະການ = {}
    for ສາຍ in ເນື້ອໃນ_ຄ່າ_cb0f2404.splitlines():
        if '=' not in ສາຍ:
            continue
        ຊື່, ຄ່າ = ສາຍ.split('=', 1)
        if ຊື່.startswith('"'):
            ຊື່ = json.loads(ຊື່)
        if ຄ່າ.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(ຄ່າ)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(ຄ່າ): ຄ່າ = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox ຄຸນສົມບັດ_ຄ່າ ຮູບແບບ_ຄ່າ_d1a42ea5 ຂໍ້ຜິດພາດ: ' + ສາຍ)
        ມາດຕະການ[ຊື່] = ຄ່າ
    return ມາດຕະການ


def 등록목록(ເນື້ອໃນ_ຄ່າ_cb0f2404):
    ມາດຕະການ = {}
    for ສາຍ in ເນື້ອໃນ_ຄ່າ_cb0f2404.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', ສາຍ)
        if 일치: ມາດຕະການ[일치.group(2).lower()] = 일치.group(1)
    return ມາດຕະການ


def 검사합(ທາງໂຄຈອນ):
    ຄ່າ = hashlib.sha256()
    with ທາງໂຄຈອນ.open('rb') as ຟາຍ:
        for ຂໍ້ມູນ in iter(lambda: ຟາຍ.read(1024 * 1024), b''): ຄ່າ.update(ຂໍ້ມູນ)
    return ຄ່າ.hexdigest()


class ແອັບ_ຕົວເປີດໃຊ້:
    def __init__(self, ເລກຮາກ_ຄ່າ, ຊື່, ວິ_ທີ_ໂຫມດ='gui', ຄໍາສັ່ງ_1f12b8e2=ປະ_ຕິ_ບັດ_ເຊລ_ຄໍາສັ່ງ):
        self.ເລກຮາກ_ຄ່າ = Path(ເລກຮາກ_ຄ່າ).resolve()
        self.ຊື່, self.ວິ_ທີ_ໂຫມດ, self.ຄໍາສັ່ງ_1f12b8e2 = ຊື່, ວິ_ທີ_ໂຫມດ, ຄໍາສັ່ງ_1f12b8e2
        self.보관 = self.ເລກຮາກ_ຄ່າ / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', ຊື່) or ຊື່ in ('.', '..'):
            raise 실행오류('VM 이름은 문자·ຕົວເລກ_ຄ່າ·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if ວິ_ທີ_ໂຫມດ not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ທາງໂຄຈອນ(self, ລຸ້ນດຽວກັນ_ຄ່າ):
        if Path(ລຸ້ນດຽວກັນ_ຄ່າ).is_absolute() or '..' in Path(ລຸ້ນດຽວກັນ_ຄ່າ).parts:
            raise 실행오류('잘못된 관리 ທາງໂຄຈອນ: ' + str(ລຸ້ນດຽວກັນ_ຄ່າ))
        ມາດຕະການ = self.보관
        for 부분 in ['.vbox'] + list(Path(ລຸ້ນດຽວກັນ_ຄ່າ).parts):
            if 부분 == '.vbox': ມາດຕະການ = self.보관
            else: ມາດຕະການ = ມາດຕະການ / 부분
            if ມາດຕະການ.is_symlink(): raise 실행오류('ເຊື່ອມຕໍ່ 경로는 사용하지 않습니다: ' + str(ມາດຕະການ))
        return ມາດຕະການ

    def 읽기(self):
        ທາງໂຄຈອນ = self.ທາງໂຄຈອນ('state.json')
        if not ທາງໂຄຈອນ.exists(): return None
        ສະຖານະ_ຄ່າ = json.loads(ທາງໂຄຈອນ.read_text(encoding='utf-8'))
        if ສະຖານະ_ຄ່າ.get('version') != 1 or ສະຖານະ_ຄ່າ.get('name') != self.ຊື່:
            raise 실행오류('관리 상태의 VM ຊື່/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for ຊື່ in ('uuid', 'owner'):
            if str(uuid.UUID(ສະຖານະ_ຄ່າ[ຊື່])) != ສະຖານະ_ຄ່າ[ຊື່]: raise 실행오류('잘못된 VM ຕົວ_ກໍາ_ນົດ_ຄ່າ')
        return ສະຖານະ_ຄ່າ

    def ຮ້ານຄ້າ_ຄ່າ(self, ສະຖານະ_ຄ່າ):
        ປາຍທາງ_ຄ່າ = self.ທາງໂຄຈອນ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as ຟາຍ:
            json.dump(ສະຖານະ_ຄ່າ, ຟາຍ, ensure_ascii=False, indent=2)
            ຟາຍ.write('\n')
            임시 = ຟາຍ.name
        os.replace(임시, str(ປາຍທາງ_ຄ່າ))

    def ລະບົບ_ຂໍ້_ມູນ(self, ສະຖານະ_ຄ່າ, 등록됨, 복구=False):
        if ສະຖານະ_ຄ່າ['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        ລະບົບ_ຂໍ້_ມູນ = ຄຸນສົມບັດ_ຄ່າ(self.ຄໍາສັ່ງ_1f12b8e2(['VBoxManage', 'showvminfo', ສະຖານະ_ຄ່າ['uuid'], '--machinereadable']))
        ຈັດຕໍາແຫນ່ງ = Path(ລະບົບ_ຂໍ້_ມູນ.get('CfgFile', '')).resolve()
        if self.ທາງໂຄຈອນ('machines').resolve() not in ຈັດຕໍາແຫນ່ງ.parents or ລະບົບ_ຂໍ້_ມູນ.get('UUID') != ສະຖານະ_ຄ່າ['uuid']:
            raise 실행오류('이 프로젝트의 VM ການຕັ້ງຄ່າ ທາງໂຄຈອນ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.ຄໍາສັ່ງ_1f12b8e2(['VBoxManage', 'getextradata', ສະຖານະ_ຄ່າ['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + ສະຖານະ_ຄ່າ['owner']:
            if 복구 and ສະຖານະ_ຄ່າ.get('pending') and 표식 == 'No value set!':
                self.ຄໍາສັ່ງ_1f12b8e2(['VBoxManage', 'setextradata', ສະຖານະ_ຄ່າ['uuid'], 'JKOROS/Owner', ສະຖານະ_ຄ່າ['owner']])
            else:
                raise 실행오류('VM ເຈົ້າຂອງ_ຄ່າ 표식이 일치하지 않아 변경하지 않습니다.')
        return ລະບົບ_ຂໍ້_ມູນ

    def ເຊັກເງິນ_ມີເດຍ(self, ສະຖານະ_ຄ່າ, ລະບົບ_ຂໍ້_ມູນ):
        제어기들 = [ຄ່າ for ຊື່, ຄ່າ in ລະບົບ_ຂໍ້_ມູນ.items() if re.fullmatch(r'storagecontrollername\d+', ຊື່)]
        ອະນຸຍາດ_ຄ່າ = [str(self.ທາງໂຄຈອນ(ຄ່າ)) for ຄ່າ in ສະຖານະ_ຄ່າ.get('media', [])]
        for ຊື່, ຄ່າ in ລະບົບ_ຂໍ້_ມູນ.items():
            if any(re.fullmatch(re.escape(ຄອນໂທຣເລີ) + r'-\d+-\d+', ຊື່) for ຄອນໂທຣເລີ in 제어기들):
                if ຄ່າ not in ('none', 'emptydrive') and ຄ່າ not in ອະນຸຍາດ_ຄ່າ:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + ຄ່າ)

    def ລາຍການ_ສະຖານະ(self):
        ສະຖານະ_ຄ່າ = self.읽기()
        if ສະຖານະ_ຄ່າ is None: return {'name': self.ຊື່, 'state': 'not-created'}
        ລະບົບ_ຂໍ້_ມູນ = self.ລະບົບ_ຂໍ້_ມູນ(ສະຖານະ_ຄ່າ, 등록목록(self.ຄໍາສັ່ງ_1f12b8e2(['VBoxManage', 'list', 'vms'])))
        return {'name': ລະບົບ_ຂໍ້_ມູນ.get('name', ສະຖານະ_ຄ່າ['name']), 'uuid': ສະຖານະ_ຄ່າ['uuid'], 'state': ລະບົບ_ຂໍ້_ມູນ.get('VMState'),
                'iso': str(self.ທາງໂຄຈອນ(ສະຖານະ_ຄ່າ['iso'])) if ສະຖານະ_ຄ່າ.get('iso') else None,
                'serial_log': str(self.ທາງໂຄຈອນ(ສະຖານະ_ຄ່າ['serial_log'])) if ສະຖານະ_ຄ່າ.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(self):
        ສະຖານະ_ຄ່າ = self.읽기()
        등록됨 = 등록목록(self.ຄໍາສັ່ງ_1f12b8e2(['VBoxManage', 'list', 'vms']))
        ລະບົບ_ຂໍ້_ມູນ = None
        if ສະຖານະ_ຄ່າ is not None and ສະຖານະ_ຄ່າ['uuid'] in 등록됨:
            ລະບົບ_ຂໍ້_ມູນ = self.ລະບົບ_ຂໍ້_ມູນ(ສະຖານະ_ຄ່າ, 등록됨, 복구=True)
            현재 = ລະບົບ_ຂໍ້_ມູນ.get('VMState')
            if 현재 == 'running':
                print('이미 ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ 중입니다. 재빌드·재시작하지 않습니다.')
                return self.ລາຍການ_ສະຖານະ()
            self.ເຊັກເງິນ_ມີເດຍ(ສະຖານະ_ຄ່າ, ລະບົບ_ຂໍ້_ມູນ)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 ຮ້ານຄ້າ_ຄ່າ 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.ຄໍາສັ່ງ_1f12b8e2(['VBoxManage', 'controlvm', ສະຖານະ_ຄ່າ['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 ສ້າງ 전에 기존 기록도 보관한다.
                    if ສະຖານະ_ຄ່າ.get('serial_log'):
                        원본 = self.ທາງໂຄຈອນ(ສະຖານະ_ຄ່າ['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ທາງໂຄຈອນ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.ຄໍາສັ່ງ_1f12b8e2(['VBoxManage', 'startvm', ສະຖານະ_ຄ່າ['uuid'], '--type', self.ວິ_ທີ_ໂຫມດ])
                return self.ລາຍການ_ສະຖານະ()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 ສະວິດ_ໂຫມດ 중입니다 ({}). 작업이 끝난 ກັບ_ຄືນ_ຄ່າ 다시 실행하세요.'.format(현재))
        elif ສະຖານະ_ຄ່າ is not None and not ສະຖານະ_ຄ່າ.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.ຊື່ in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # ຮ້ານຄ້າ_ຄ່າ/ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.ຄໍາສັ່ງ_1f12b8e2(['make', '-C', str(self.ເລກຮາກ_ຄ່າ / 'os'), 'iso']), end='')
        원본 = self.ເລກຮາກ_ຄ່າ / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        ມີເດຍ_ຄ່າ = 'media/kernel-' + 검사합(원본) + '.iso'
        ປາຍທາງ_ຄ່າ = self.ທາງໂຄຈອນ(ມີເດຍ_ຄ່າ)
        ປາຍທາງ_ຄ່າ.parent.mkdir(exist_ok=True)
        if ປາຍທາງ_ຄ່າ.exists():
            if 검사합(ປາຍທາງ_ຄ່າ) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(ປາຍທາງ_ຄ່າ))
        else:
            with tempfile.NamedTemporaryFile(dir=str(ປາຍທາງ_ຄ່າ.parent)) as ຟາຍ:
                shutil.copyfile(str(원본), ຟາຍ.name)
                os.link(ຟາຍ.name, str(ປາຍທາງ_ຄ່າ))

        if ສະຖານະ_ຄ່າ is None:
            ສະຖານະ_ຄ່າ = {'version': 1, 'name': self.ຊື່, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.ຮ້ານຄ້າ_ຄ່າ(ສະຖານະ_ຄ່າ)
        if ລະບົບ_ຂໍ້_ມູນ is None:
            self.ຄໍາສັ່ງ_1f12b8e2(['VBoxManage', 'createvm', '--name', ສະຖານະ_ຄ່າ['name'], '--uuid', ສະຖານະ_ຄ່າ['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ທາງໂຄຈອນ('machines')), '--register'])
            self.ຄໍາສັ່ງ_1f12b8e2(['VBoxManage', 'setextradata', ສະຖານະ_ຄ່າ['uuid'], 'JKOROS/Owner', ສະຖານະ_ຄ່າ['owner']])
        # ສ້າງ_ລະບົບ 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        ລະບົບ_ຂໍ້_ມູນ = self.ລະບົບ_ຂໍ້_ມູນ(ສະຖານະ_ຄ່າ, 등록목록(self.ຄໍາສັ່ງ_1f12b8e2(['VBoxManage', 'list', 'vms'])))
        if ລະບົບ_ຂໍ້_ມູນ.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('ສ້າງ_ລະບົບ 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.ເຊັກເງິນ_ມີເດຍ(ສະຖານະ_ຄ່າ, ລະບົບ_ຂໍ້_ມູນ)
        ສະຖານະ_ຄ່າ['iso'] = ມີເດຍ_ຄ່າ
        if ມີເດຍ_ຄ່າ not in ສະຖານະ_ຄ່າ['media']: ສະຖານະ_ຄ່າ['media'].append(ມີເດຍ_ຄ່າ)
        ສະຖານະ_ຄ່າ['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        ບັນທຶກ_ຄ່າ = self.ທາງໂຄຈອນ(ສະຖານະ_ຄ່າ['serial_log'])
        ບັນທຶກ_ຄ່າ.parent.mkdir(exist_ok=True)
        self.ຮ້ານຄ້າ_ຄ່າ(ສະຖານະ_ຄ່າ)
        self.ຄໍາສັ່ງ_1f12b8e2(['VBoxManage', 'modifyvm', ສະຖານະ_ຄ່າ['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(ບັນທຶກ_ຄ່າ)])
        제어기들 = [ຄ່າ for ຊື່, ຄ່າ in ລະບົບ_ຂໍ້_ມູນ.items() if re.fullmatch(r'storagecontrollername\d+', ຊື່)]
        if 'JKOROS IDE' not in 제어기들:
            self.ຄໍາສັ່ງ_1f12b8e2(['VBoxManage', 'storagectl', ສະຖານະ_ຄ່າ['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.ຄໍາສັ່ງ_1f12b8e2(['VBoxManage', 'storageattach', ສະຖານະ_ຄ່າ['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(ປາຍທາງ_ຄ່າ)])
        ສະຖານະ_ຄ່າ['pending'] = False
        self.ຮ້ານຄ້າ_ຄ່າ(ສະຖານະ_ຄ່າ)
        self.ຄໍາສັ່ງ_1f12b8e2(['VBoxManage', 'startvm', ສະຖານະ_ຄ່າ['uuid'], '--type', self.ວິ_ທີ_ໂຫມດ])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.ລາຍການ_ສະຖານະ()


def ແລ່ນ():
    ການແຈກຄໍາສັບ_ຄ່າ = argparse.ArgumentParser(description='jkoros 전용 VirtualBox ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ 및 ສະຖານະ_ຄ່າ ຄິວຣີ_ຄ່າ')
    ການແຈກຄໍາສັບ_ຄ່າ.add_argument('action', choices=['run', 'status'])
    ພາຣາມິເຕີ_ຂໍ້ພິສູດ = ການແຈກຄໍາສັບ_ຄ່າ.parse_args()
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ = ແອັບ_ຕົວເປີດໃຊ້(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if ພາຣາມິເຕີ_ຂໍ້ພິສູດ.action == 'status':
        print(json.dumps(ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ລາຍການ_ສະຖານະ(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. ໂຮສ 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/ການອະນຸຍາດ_ຄ່າ 변경은 하지 않습니다.')
    os.umask(0o077)
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ທາງໂຄຈອນ('lock').parent.mkdir(parents=True, exist_ok=True)
    with ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ທາງໂຄຈອນ('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ 작업이 진행 중입니다.')
        print(json.dumps(ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: ແລ່ນ()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ຂໍ້ຜິດພາດ:
        print('VBOX ຂໍ້ຜິດພາດ: ' + str(ຂໍ້ຜິດພາດ), file=sys.stderr)
        sys.exit(1)
