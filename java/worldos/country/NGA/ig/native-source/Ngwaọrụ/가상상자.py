#!/usr/bin/env python3
"""jkoros 전용 VirtualBox app_ihengosi_ndi_app. 기존 VM/디스크/Store_valuu 상태는 삭제하지 않는다."""
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


def mee_nkọwannyemiwu_nnyemiwu(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(valuu) for valuu in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    ndịnà_valuu = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('Ntiiwu ọdịdà_valuu: ' + ' '.join(str(valuu) for valuu in 인수) + '\n' + ndịnà_valuu[-10000:])
    return ndịnà_valuu


def njìama_valuu(ndịnà_valuu):
    결과 = {}
    for ahịrī in ndịnà_valuu.splitlines():
        if '=' not in ahịrī:
            continue
        Aha, valuu = ahịrī.split('=', 1)
        if Aha.startswith('"'):
            Aha = json.loads(Aha)
        if valuu.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(valuu)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(valuu): valuu = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox njìama_valuu hàzie_valuu mmejọ: ' + ahịrī)
        결과[Aha] = valuu
    return 결과


def 등록목록(ndịnà_valuu):
    결과 = {}
    for ahịrī in ndịnà_valuu.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', ahịrī)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(ụzọ_ozi):
    valuu = hashlib.sha256()
    with ụzọ_ozi.open('rb') as Faịlụ:
        for datà in iter(lambda: Faịlụ.read(1024 * 1024), b''): valuu.update(datà)
    return valuu.hexdigest()


class app_ihengosi_ndi_app:
    def __init__(self, 뿌리, Aha, usoro_moòdù='gui', Ntiiwu=mee_nkọwannyemiwu_nnyemiwu):
        self.뿌리 = Path(뿌리).resolve()
        self.Aha, self.usoro_moòdù, self.Ntiiwu = Aha, usoro_moòdù, Ntiiwu
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Aha) or Aha in ('.', '..'):
            raise 실행오류('VM 이름은 문자·ọbula_valuu·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if usoro_moòdù not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ụzọ_ozi(self, ibè_valuu):
        if Path(ibè_valuu).is_absolute() or '..' in Path(ibè_valuu).parts:
            raise 실행오류('잘못된 관리 ụzọ_ozi: ' + str(ibè_valuu))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(ibè_valuu).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('Banye 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def Wepụta_ọzi(self):
        ụzọ_ozi = self.ụzọ_ozi('state.json')
        if not ụzọ_ozi.exists(): return None
        ọnọdụ_valuu = json.loads(ụzọ_ozi.read_text(encoding='utf-8'))
        if ọnọdụ_valuu.get('version') != 1 or ọnọdụ_valuu.get('name') != self.Aha:
            raise 실행오류('관리 상태의 VM Aha/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Aha in ('uuid', 'owner'):
            if str(uuid.UUID(ọnọdụ_valuu[Aha])) != ọnọdụ_valuu[Aha]: raise 실행오류('잘못된 VM ihe_nkọwapụta_valuu')
        return ọnọdụ_valuu

    def Store_valuu(self, ọnọdụ_valuu):
        ebemwèga_valuu = self.ụzọ_ozi('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Faịlụ:
            json.dump(ọnọdụ_valuu, Faịlụ, ensure_ascii=False, indent=2)
            Faịlụ.write('\n')
            임시 = Faịlụ.name
        os.replace(임시, str(ebemwèga_valuu))

    def Ozi_Sistèm(self, ọnọdụ_valuu, 등록됨, nnweghàchi_ọnọdụ=False):
        if ọnọdụ_valuu['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        Ozi_Sistèm = njìama_valuu(self.Ntiiwu(['VBoxManage', 'showvminfo', ọnọdụ_valuu['uuid'], '--machinereadable']))
        위치 = Path(Ozi_Sistèm.get('CfgFile', '')).resolve()
        if self.ụzọ_ozi('machines').resolve() not in 위치.parents or Ozi_Sistèm.get('UUID') != ọnọdụ_valuu['uuid']:
            raise 실행오류('이 프로젝트의 VM Mwube ụzọ_ozi/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Ntiiwu(['VBoxManage', 'getextradata', ọnọdụ_valuu['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + ọnọdụ_valuu['owner']:
            if nnweghàchi_ọnọdụ and ọnọdụ_valuu.get('pending') and 표식 == 'No value set!':
                self.Ntiiwu(['VBoxManage', 'setextradata', ọnọdụ_valuu['uuid'], 'JKOROS/Owner', ọnọdụ_valuu['owner']])
            else:
                raise 실행오류('VM nwe_valuu 표식이 일치하지 않아 변경하지 않습니다.')
        return Ozi_Sistèm

    def cheèk_midịà(self, ọnọdụ_valuu, Ozi_Sistèm):
        제어기들 = [valuu for Aha, valuu in Ozi_Sistèm.items() if re.fullmatch(r'storagecontrollername\d+', Aha)]
        Kwère_valuu = [str(self.ụzọ_ozi(valuu)) for valuu in ọnọdụ_valuu.get('media', [])]
        for Aha, valuu in Ozi_Sistèm.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', Aha) for 제어기 in 제어기들):
                if valuu not in ('none', 'emptydrive') and valuu not in Kwère_valuu:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + valuu)

    def gòsi_ọnọdụ(self):
        ọnọdụ_valuu = self.Wepụta_ọzi()
        if ọnọdụ_valuu is None: return {'name': self.Aha, 'state': 'not-created'}
        Ozi_Sistèm = self.Ozi_Sistèm(ọnọdụ_valuu, 등록목록(self.Ntiiwu(['VBoxManage', 'list', 'vms'])))
        return {'name': Ozi_Sistèm.get('name', ọnọdụ_valuu['name']), 'uuid': ọnọdụ_valuu['uuid'], 'state': Ozi_Sistèm.get('VMState'),
                'iso': str(self.ụzọ_ozi(ọnọdụ_valuu['iso'])) if ọnọdụ_valuu.get('iso') else None,
                'serial_log': str(self.ụzọ_ozi(ọnọdụ_valuu['serial_log'])) if ọnọdụ_valuu.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def mee_nnyemiwu(self):
        ọnọdụ_valuu = self.Wepụta_ọzi()
        등록됨 = 등록목록(self.Ntiiwu(['VBoxManage', 'list', 'vms']))
        Ozi_Sistèm = None
        if ọnọdụ_valuu is not None and ọnọdụ_valuu['uuid'] in 등록됨:
            Ozi_Sistèm = self.Ozi_Sistèm(ọnọdụ_valuu, 등록됨, nnweghàchi_ọnọdụ=True)
            현재 = Ozi_Sistèm.get('VMState')
            if 현재 == 'running':
                print('이미 mee_nnyemiwu 중입니다. 재빌드·재시작하지 않습니다.')
                return self.gòsi_ọnọdụ()
            self.cheèk_midịà(ọnọdụ_valuu, Ozi_Sistèm)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_valuu 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Ntiiwu(['VBoxManage', 'controlvm', ọnọdụ_valuu['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Mepee 전에 기존 기록도 보관한다.
                    if ọnọdụ_valuu.get('serial_log'):
                        원본 = self.ụzọ_ozi(ọnọdụ_valuu['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ụzọ_ozi('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Ntiiwu(['VBoxManage', 'startvm', ọnọdụ_valuu['uuid'], '--type', self.usoro_moòdù])
                return self.gòsi_ọnọdụ()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 ngbanwụ_moòdù 중입니다 ({}). 작업이 끝난 Àzụ_valuu 다시 실행하세요.'.format(현재))
        elif ọnọdụ_valuu is not None and not ọnọdụ_valuu.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Aha in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_valuu/mee_nnyemiwu 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Ntiiwu(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        midịà_valuu = 'media/kernel-' + 검사합(원본) + '.iso'
        ebemwèga_valuu = self.ụzọ_ozi(midịà_valuu)
        ebemwèga_valuu.parent.mkdir(exist_ok=True)
        if ebemwèga_valuu.exists():
            if 검사합(ebemwèga_valuu) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(ebemwèga_valuu))
        else:
            with tempfile.NamedTemporaryFile(dir=str(ebemwèga_valuu.parent)) as Faịlụ:
                shutil.copyfile(str(원본), Faịlụ.name)
                os.link(Faịlụ.name, str(ebemwèga_valuu))

        if ọnọdụ_valuu is None:
            ọnọdụ_valuu = {'version': 1, 'name': self.Aha, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_valuu(ọnọdụ_valuu)
        if Ozi_Sistèm is None:
            self.Ntiiwu(['VBoxManage', 'createvm', '--name', ọnọdụ_valuu['name'], '--uuid', ọnọdụ_valuu['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ụzọ_ozi('machines')), '--register'])
            self.Ntiiwu(['VBoxManage', 'setextradata', ọnọdụ_valuu['uuid'], 'JKOROS/Owner', ọnọdụ_valuu['owner']])
        # wue_sistèm 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        Ozi_Sistèm = self.Ozi_Sistèm(ọnọdụ_valuu, 등록목록(self.Ntiiwu(['VBoxManage', 'list', 'vms'])))
        if Ozi_Sistèm.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('wue_sistèm 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.cheèk_midịà(ọnọdụ_valuu, Ozi_Sistèm)
        ọnọdụ_valuu['iso'] = midịà_valuu
        if midịà_valuu not in ọnọdụ_valuu['media']: ọnọdụ_valuu['media'].append(midịà_valuu)
        ọnọdụ_valuu['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        ndekọ_valuu = self.ụzọ_ozi(ọnọdụ_valuu['serial_log'])
        ndekọ_valuu.parent.mkdir(exist_ok=True)
        self.Store_valuu(ọnọdụ_valuu)
        self.Ntiiwu(['VBoxManage', 'modifyvm', ọnọdụ_valuu['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(ndekọ_valuu)])
        제어기들 = [valuu for Aha, valuu in Ozi_Sistèm.items() if re.fullmatch(r'storagecontrollername\d+', Aha)]
        if 'JKOROS IDE' not in 제어기들:
            self.Ntiiwu(['VBoxManage', 'storagectl', ọnọdụ_valuu['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Ntiiwu(['VBoxManage', 'storageattach', ọnọdụ_valuu['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(ebemwèga_valuu)])
        ọnọdụ_valuu['pending'] = False
        self.Store_valuu(ọnọdụ_valuu)
        self.Ntiiwu(['VBoxManage', 'startvm', ọnọdụ_valuu['uuid'], '--type', self.usoro_moòdù])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.gòsi_ọnọdụ()


def Bido():
    kerìsịa_valuu = argparse.ArgumentParser(description='jkoros 전용 VirtualBox mee_nnyemiwu 및 ọnọdụ_valuu mgbaajụjụ_valuu')
    kerìsịa_valuu.add_argument('action', choices=['run', 'status'])
    인자 = kerìsịa_valuu.parse_args()
    mee_nnyemiwu = app_ihengosi_ndi_app(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(mee_nnyemiwu.gòsi_ọnọdụ(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. usu 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/ikikere_valuu 변경은 하지 않습니다.')
    os.umask(0o077)
    mee_nnyemiwu.ụzọ_ozi('lock').parent.mkdir(parents=True, exist_ok=True)
    with mee_nnyemiwu.ụzọ_ozi('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox mee_nnyemiwu 작업이 진행 중입니다.')
        print(json.dumps(mee_nnyemiwu.mee_nnyemiwu(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Bido()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as mmejọ:
        print('VBOX mmejọ: ' + str(mmejọ), file=sys.stderr)
        sys.exit(1)
