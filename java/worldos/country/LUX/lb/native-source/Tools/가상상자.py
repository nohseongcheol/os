#!/usr/bin/env python3
"""jkoros 전용 VirtualBox App_App_Beräich. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def ausféieren_Shell_Befeel(인수):
    환경 = dict(os.environ, LC_ALL='C')
    Mooss = subprocess.run([str(VALUE) for VALUE in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Inhalt_VALUE = Mooss.stdout.decode('utf-8', 'replace')
    if Mooss.returncode:
        raise 실행오류('Befeel Feeler_VALUE: ' + ' '.join(str(VALUE) for VALUE in 인수) + '\n' + Inhalt_VALUE[-10000:])
    return Inhalt_VALUE


def Attribut_VALUE(Inhalt_VALUE):
    Mooss = {}
    for Zeil in Inhalt_VALUE.splitlines():
        if '=' not in Zeil:
            continue
        Numm, VALUE = Zeil.split('=', 1)
        if Numm.startswith('"'):
            Numm = json.loads(Numm)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox Attribut_VALUE Format_VALUE Feeler: ' + Zeil)
        Mooss[Numm] = VALUE
    return Mooss


def 등록목록(Inhalt_VALUE):
    Mooss = {}
    for Zeil in Inhalt_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Zeil)
        if 일치: Mooss[일치.group(2).lower()] = 일치.group(1)
    return Mooss


def 검사합(Wee):
    VALUE = hashlib.sha256()
    with Wee.open('rb') as Fichier:
        for Daten in iter(lambda: Fichier.read(1024 * 1024), b''): VALUE.update(Daten)
    return VALUE.hexdigest()


class App_App_Beräich:
    def __init__(self, Racinn_VALUE, Numm, Method_MODE='gui', Befeel=ausféieren_Shell_Befeel):
        self.Racinn_VALUE = Path(Racinn_VALUE).resolve()
        self.Numm, self.Method_MODE, self.Befeel = Numm, Method_MODE, Befeel
        self.보관 = self.Racinn_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Numm) or Numm in ('.', '..'):
            raise 실행오류('VM 이름은 문자·Ziffer_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if Method_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Wee(self, Peer_VALUE):
        if Path(Peer_VALUE).is_absolute() or '..' in Path(Peer_VALUE).parts:
            raise 실행오류('잘못된 관리 Wee: ' + str(Peer_VALUE))
        Mooss = self.보관
        for 부분 in ['.vbox'] + list(Path(Peer_VALUE).parts):
            if 부분 == '.vbox': Mooss = self.보관
            else: Mooss = Mooss / 부분
            if Mooss.is_symlink(): raise 실행오류('Verbannen 경로는 사용하지 않습니다: ' + str(Mooss))
        return Mooss

    def 읽기(self):
        Wee = self.Wee('state.json')
        if not Wee.exists(): return None
        Status_VALUE = json.loads(Wee.read_text(encoding='utf-8'))
        if Status_VALUE.get('version') != 1 or Status_VALUE.get('name') != self.Numm:
            raise 실행오류('관리 상태의 VM Numm/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Numm in ('uuid', 'owner'):
            if str(uuid.UUID(Status_VALUE[Numm])) != Status_VALUE[Numm]: raise 실행오류('잘못된 VM Identifikateur_VALUE')
        return Status_VALUE

    def Store_VALUE(self, Status_VALUE):
        Zil_VALUE = self.Wee('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Fichier:
            json.dump(Status_VALUE, Fichier, ensure_ascii=False, indent=2)
            Fichier.write('\n')
            임시 = Fichier.name
        os.replace(임시, str(Zil_VALUE))

    def msinfo32_exe(self, Status_VALUE, 등록됨, restauréieren_Status=False):
        if Status_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = Attribut_VALUE(self.Befeel(['VBoxManage', 'showvminfo', Status_VALUE['uuid'], '--machinereadable']))
        positionéieren = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.Wee('machines').resolve() not in positionéieren.parents or msinfo32_exe.get('UUID') != Status_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Astellungen Wee/UUID와 일치하지 않아 변경하지 않습니다.')
        Markéierung_VALUE = self.Befeel(['VBoxManage', 'getextradata', Status_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if Markéierung_VALUE != 'Value: ' + Status_VALUE['owner']:
            if restauréieren_Status and Status_VALUE.get('pending') and Markéierung_VALUE == 'No value set!':
                self.Befeel(['VBoxManage', 'setextradata', Status_VALUE['uuid'], 'JKOROS/Owner', Status_VALUE['owner']])
            else:
                raise 실행오류('VM Besëtzer_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, Status_VALUE, msinfo32_exe):
        제어기들 = [VALUE for Numm, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Numm)]
        Erlaben_VALUE = [str(self.Wee(VALUE)) for VALUE in Status_VALUE.get('media', [])]
        for Numm, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(Controller) + r'-\d+-\d+', Numm) for Controller in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Erlaben_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def Show_Status(self):
        Status_VALUE = self.읽기()
        if Status_VALUE is None: return {'name': self.Numm, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Status_VALUE, 등록목록(self.Befeel(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Status_VALUE['name']), 'uuid': Status_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.Wee(Status_VALUE['iso'])) if Status_VALUE.get('iso') else None,
                'serial_log': str(self.Wee(Status_VALUE['serial_log'])) if Status_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def ausféieren_Befeel(self):
        Status_VALUE = self.읽기()
        등록됨 = 등록목록(self.Befeel(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Status_VALUE is not None and Status_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Status_VALUE, 등록됨, restauréieren_Status=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 ausféieren_Befeel 중입니다. 재빌드·재시작하지 않습니다.')
                return self.Show_Status()
            self.매체검사(Status_VALUE, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Befeel(['VBoxManage', 'controlvm', Status_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 ariichten 전에 기존 기록도 보관한다.
                    if Status_VALUE.get('serial_log'):
                        원본 = self.Wee(Status_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Wee('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Befeel(['VBoxManage', 'startvm', Status_VALUE['uuid'], '--type', self.Method_MODE])
                return self.Show_Status()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 Zeréck_VALUE 다시 실행하세요.'.format(현재))
        elif Status_VALUE is not None and not Status_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Numm in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/ausféieren_Befeel 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Befeel(['make', '-C', str(self.Racinn_VALUE / 'os'), 'iso']), end='')
        원본 = self.Racinn_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        Zil_VALUE = self.Wee(매체)
        Zil_VALUE.parent.mkdir(exist_ok=True)
        if Zil_VALUE.exists():
            if 검사합(Zil_VALUE) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(Zil_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(Zil_VALUE.parent)) as Fichier:
                shutil.copyfile(str(원본), Fichier.name)
                os.link(Fichier.name, str(Zil_VALUE))

        if Status_VALUE is None:
            Status_VALUE = {'version': 1, 'name': self.Numm, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(Status_VALUE)
        if msinfo32_exe is None:
            self.Befeel(['VBoxManage', 'createvm', '--name', Status_VALUE['name'], '--uuid', Status_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Wee('machines')), '--register'])
            self.Befeel(['VBoxManage', 'setextradata', Status_VALUE['uuid'], 'JKOROS/Owner', Status_VALUE['owner']])
        # Build_System 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Status_VALUE, 등록목록(self.Befeel(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('Build_System 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(Status_VALUE, msinfo32_exe)
        Status_VALUE['iso'] = 매체
        if 매체 not in Status_VALUE['media']: Status_VALUE['media'].append(매체)
        Status_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.Wee(Status_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(Status_VALUE)
        self.Befeel(['VBoxManage', 'modifyvm', Status_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Numm, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Numm)]
        if 'JKOROS IDE' not in 제어기들:
            self.Befeel(['VBoxManage', 'storagectl', Status_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Befeel(['VBoxManage', 'storageattach', Status_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(Zil_VALUE)])
        Status_VALUE['pending'] = False
        self.Store_VALUE(Status_VALUE)
        self.Befeel(['VBoxManage', 'startvm', Status_VALUE['uuid'], '--type', self.Method_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.Show_Status()


def Laf():
    analyséieren_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox ausféieren_Befeel 및 Status_VALUE Requête_VALUE')
    analyséieren_VALUE.add_argument('action', choices=['run', 'status'])
    인자 = analyséieren_VALUE.parse_args()
    ausféieren_Befeel = App_App_Beräich(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(ausféieren_Befeel.Show_Status(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. Host 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/Geneemegung_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    ausféieren_Befeel.Wee('lock').parent.mkdir(parents=True, exist_ok=True)
    with ausféieren_Befeel.Wee('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox ausféieren_Befeel 작업이 진행 중입니다.')
        print(json.dumps(ausféieren_Befeel.ausféieren_Befeel(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Laf()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Feeler:
        print('VBOX Feeler: ' + str(Feeler), file=sys.stderr)
        sys.exit(1)
