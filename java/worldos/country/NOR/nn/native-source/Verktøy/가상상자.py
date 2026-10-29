#!/usr/bin/env python3
"""jkoros 전용 VirtualBox app_appskuff. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def Utfør_grensesnitt_kommando(Argument):
    환경 = dict(os.environ, LC_ALL='C')
    forretningsmål = subprocess.run([str(VALUE) for VALUE in Argument], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Innhald_VALUE = forretningsmål.stdout.decode('utf-8', 'replace')
    if forretningsmål.returncode:
        raise 실행오류('Kommando feil_VALUE: ' + ' '.join(str(VALUE) for VALUE in Argument) + '\n' + Innhald_VALUE[-10000:])
    return Innhald_VALUE


def attributt_VALUE(Innhald_VALUE):
    forretningsmål = {}
    for linje in Innhald_VALUE.splitlines():
        if '=' not in linje:
            continue
        Namn, VALUE = linje.split('=', 1)
        if Namn.startswith('"'):
            Namn = json.loads(Namn)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox attributt_VALUE format_VALUE FEIL: ' + linje)
        forretningsmål[Namn] = VALUE
    return forretningsmål


def 등록목록(Innhald_VALUE):
    forretningsmål = {}
    for linje in Innhald_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', linje)
        if 일치: forretningsmål[일치.group(2).lower()] = 일치.group(1)
    return forretningsmål


def kontrollsum(STIGE):
    VALUE = hashlib.sha256()
    with STIGE.open('rb') as Fil:
        for data in iter(lambda: Fil.read(1024 * 1024), b''): VALUE.update(data)
    return VALUE.hexdigest()


class app_appskuff:
    def __init__(self, rot_VALUE, Namn, metode_MODE='gui', Kommando=Utfør_grensesnitt_kommando):
        self.rot_VALUE = Path(rot_VALUE).resolve()
        self.Namn, self.metode_MODE, self.Kommando = Namn, metode_MODE, Kommando
        self.보관 = self.rot_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Namn) or Namn in ('.', '..'):
            raise 실행오류('VM 이름은 문자·siffer_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if metode_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def STIGE(self, node_VALUE_6a3b6fa7):
        if Path(node_VALUE_6a3b6fa7).is_absolute() or '..' in Path(node_VALUE_6a3b6fa7).parts:
            raise 실행오류('잘못된 관리 STIGE: ' + str(node_VALUE_6a3b6fa7))
        forretningsmål = self.보관
        for 부분 in ['.vbox'] + list(Path(node_VALUE_6a3b6fa7).parts):
            if 부분 == '.vbox': forretningsmål = self.보관
            else: forretningsmål = forretningsmål / 부분
            if forretningsmål.is_symlink(): raise 실행오류('Kopla_til 경로는 사용하지 않습니다: ' + str(forretningsmål))
        return forretningsmål

    def Les(self):
        STIGE = self.STIGE('state.json')
        if not STIGE.exists(): return None
        status_VALUE = json.loads(STIGE.read_text(encoding='utf-8'))
        if status_VALUE.get('version') != 1 or status_VALUE.get('name') != self.Namn:
            raise 실행오류('관리 상태의 VM Namn/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Namn in ('uuid', 'owner'):
            if str(uuid.UUID(status_VALUE[Namn])) != status_VALUE[Namn]: raise 실행오류('잘못된 VM identifikator_VALUE')
        return status_VALUE

    def Store_VALUE(self, status_VALUE):
        mål_VALUE = self.STIGE('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Fil:
            json.dump(status_VALUE, Fil, ensure_ascii=False, indent=2)
            Fil.write('\n')
            임시 = Fil.name
        os.replace(임시, str(mål_VALUE))

    def msinfo32_exe(self, status_VALUE, 등록됨, gjenopprette_status=False):
        if status_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = attributt_VALUE(self.Kommando(['VBoxManage', 'showvminfo', status_VALUE['uuid'], '--machinereadable']))
        Posisjon = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.STIGE('machines').resolve() not in Posisjon.parents or msinfo32_exe.get('UUID') != status_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Innstillingar STIGE/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Kommando(['VBoxManage', 'getextradata', status_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + status_VALUE['owner']:
            if gjenopprette_status and status_VALUE.get('pending') and 표식 == 'No value set!':
                self.Kommando(['VBoxManage', 'setextradata', status_VALUE['uuid'], 'JKOROS/Owner', status_VALUE['owner']])
            else:
                raise 실행오류('VM eigar_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, status_VALUE, msinfo32_exe):
        제어기들 = [VALUE for Namn, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Namn)]
        Tillat_VALUE = [str(self.STIGE(VALUE)) for VALUE in status_VALUE.get('media', [])]
        for Namn, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(kontrollar) + r'-\d+-\d+', Namn) for kontrollar in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Tillat_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def vise_status(self):
        status_VALUE = self.Les()
        if status_VALUE is None: return {'name': self.Namn, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(status_VALUE, 등록목록(self.Kommando(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', status_VALUE['name']), 'uuid': status_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.STIGE(status_VALUE['iso'])) if status_VALUE.get('iso') else None,
                'serial_log': str(self.STIGE(status_VALUE['serial_log'])) if status_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Utfør_kommando(self):
        status_VALUE = self.Les()
        등록됨 = 등록목록(self.Kommando(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if status_VALUE is not None and status_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(status_VALUE, 등록됨, gjenopprette_status=True)
            betalt_vare = msinfo32_exe.get('VMState')
            if betalt_vare == 'running':
                print('이미 Utfør_kommando 중입니다. 재빌드·재시작하지 않습니다.')
                return self.vise_status()
            self.매체검사(status_VALUE, msinfo32_exe)
            if betalt_vare in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(betalt_vare))
                if betalt_vare == 'paused':
                    self.Kommando(['VBoxManage', 'controlvm', status_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Opna 전에 기존 기록도 보관한다.
                    if status_VALUE.get('serial_log'):
                        원본 = self.STIGE(status_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.STIGE('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Kommando(['VBoxManage', 'startvm', status_VALUE['uuid'], '--type', self.metode_MODE])
                return self.vise_status()
            if betalt_vare not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 byte_MODE 중입니다 ({}). 작업이 끝난 TILBAKE_VALUE 다시 실행하세요.'.format(betalt_vare))
        elif status_VALUE is not None and not status_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Namn in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/Utfør_kommando 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Kommando(['make', '-C', str(self.rot_VALUE / 'os'), 'iso']), end='')
        원본 = self.rot_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + kontrollsum(원본) + '.iso'
        mål_VALUE = self.STIGE(매체)
        mål_VALUE.parent.mkdir(exist_ok=True)
        if mål_VALUE.exists():
            if kontrollsum(mål_VALUE) != kontrollsum(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(mål_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(mål_VALUE.parent)) as Fil:
                shutil.copyfile(str(원본), Fil.name)
                os.link(Fil.name, str(mål_VALUE))

        if status_VALUE is None:
            status_VALUE = {'version': 1, 'name': self.Namn, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(status_VALUE)
        if msinfo32_exe is None:
            self.Kommando(['VBoxManage', 'createvm', '--name', status_VALUE['name'], '--uuid', status_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.STIGE('machines')), '--register'])
            self.Kommando(['VBoxManage', 'setextradata', status_VALUE['uuid'], 'JKOROS/Owner', status_VALUE['owner']])
        # bygg_system 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(status_VALUE, 등록목록(self.Kommando(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('bygg_system 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(status_VALUE, msinfo32_exe)
        status_VALUE['iso'] = 매체
        if 매체 not in status_VALUE['media']: status_VALUE['media'].append(매체)
        status_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.STIGE(status_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(status_VALUE)
        self.Kommando(['VBoxManage', 'modifyvm', status_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Namn, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Namn)]
        if 'JKOROS IDE' not in 제어기들:
            self.Kommando(['VBoxManage', 'storagectl', status_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Kommando(['VBoxManage', 'storageattach', status_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(mål_VALUE)])
        status_VALUE['pending'] = False
        self.Store_VALUE(status_VALUE)
        self.Kommando(['VBoxManage', 'startvm', status_VALUE['uuid'], '--type', self.metode_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.vise_status()


def Køyr_2():
    dele_opp_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Utfør_kommando 및 status_VALUE spørjing_VALUE')
    dele_opp_VALUE.add_argument('action', choices=['run', 'status'])
    parameter_argument = dele_opp_VALUE.parse_args()
    Utfør_kommando = app_appskuff(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parameter_argument.action == 'status':
        print(json.dumps(Utfør_kommando.vise_status(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. vert 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/løyve_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    Utfør_kommando.STIGE('lock').parent.mkdir(parents=True, exist_ok=True)
    with Utfør_kommando.STIGE('lock').open('a') as blokkere_VALUE:
        try: fcntl.flock(blokkere_VALUE, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Utfør_kommando 작업이 진행 중입니다.')
        print(json.dumps(Utfør_kommando.Utfør_kommando(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Køyr_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as FEIL:
        print('VBOX FEIL: ' + str(FEIL), file=sys.stderr)
        sys.exit(1)
