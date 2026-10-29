#!/usr/bin/env python3
"""jkoros 전용 VirtualBox app_launcher. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def Mag_execute_shell_utos(인수):
    환경 = dict(os.environ, LC_ALL='C')
    sukat = subprocess.run([str(VALUE) for VALUE in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Nilalaman_VALUE = sukat.stdout.decode('utf-8', 'replace')
    if sukat.returncode:
        raise 실행오류('utos pagpalya_VALUE: ' + ' '.join(str(VALUE) for VALUE in 인수) + '\n' + Nilalaman_VALUE[-10000:])
    return Nilalaman_VALUE


def katangian_VALUE(Nilalaman_VALUE):
    sukat = {}
    for linya in Nilalaman_VALUE.splitlines():
        if '=' not in linya:
            continue
        pangalan, VALUE = linya.split('=', 1)
        if pangalan.startswith('"'):
            pangalan = json.loads(pangalan)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox katangian_VALUE format_VALUE error: ' + linya)
        sukat[pangalan] = VALUE
    return sukat


def 등록목록(Nilalaman_VALUE):
    sukat = {}
    for linya in Nilalaman_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', linya)
        if 일치: sukat[일치.group(2).lower()] = 일치.group(1)
    return sukat


def checksum(path):
    VALUE = hashlib.sha256()
    with path.open('rb') as file:
        for data in iter(lambda: file.read(1024 * 1024), b''): VALUE.update(data)
    return VALUE.hexdigest()


class app_launcher:
    def __init__(self, root_VALUE, pangalan, pamamaraan_MODE='gui', utos=Mag_execute_shell_utos):
        self.root_VALUE = Path(root_VALUE).resolve()
        self.pangalan, self.pamamaraan_MODE, self.utos = pangalan, pamamaraan_MODE, utos
        self.보관 = self.root_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', pangalan) or pangalan in ('.', '..'):
            raise 실행오류('VM 이름은 문자·digit_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if pamamaraan_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def path(self, peer_VALUE):
        if Path(peer_VALUE).is_absolute() or '..' in Path(peer_VALUE).parts:
            raise 실행오류('잘못된 관리 path: ' + str(peer_VALUE))
        sukat = self.보관
        for 부분 in ['.vbox'] + list(Path(peer_VALUE).parts):
            if 부분 == '.vbox': sukat = self.보관
            else: sukat = sukat / 부분
            if sukat.is_symlink(): raise 실행오류('CONNECT 경로는 사용하지 않습니다: ' + str(sukat))
        return sukat

    def 읽기(self):
        path = self.path('state.json')
        if not path.exists(): return None
        katayuan_VALUE = json.loads(path.read_text(encoding='utf-8'))
        if katayuan_VALUE.get('version') != 1 or katayuan_VALUE.get('name') != self.pangalan:
            raise 실행오류('관리 상태의 VM pangalan/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for pangalan in ('uuid', 'owner'):
            if str(uuid.UUID(katayuan_VALUE[pangalan])) != katayuan_VALUE[pangalan]: raise 실행오류('잘못된 VM tagakilala_VALUE')
        return katayuan_VALUE

    def Store_VALUE(self, katayuan_VALUE):
        patutunguhan_VALUE = self.path('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as file:
            json.dump(katayuan_VALUE, file, ensure_ascii=False, indent=2)
            file.write('\n')
            임시 = file.name
        os.replace(임시, str(patutunguhan_VALUE))

    def msinfo32_exe(self, katayuan_VALUE, 등록됨, bawiin_katayuan=False):
        if katayuan_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = katangian_VALUE(self.utos(['VBoxManage', 'showvminfo', katayuan_VALUE['uuid'], '--machinereadable']))
        posisyon = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.path('machines').resolve() not in posisyon.parents or msinfo32_exe.get('UUID') != katayuan_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Mga_Setting path/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.utos(['VBoxManage', 'getextradata', katayuan_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + katayuan_VALUE['owner']:
            if bawiin_katayuan and katayuan_VALUE.get('pending') and 표식 == 'No value set!':
                self.utos(['VBoxManage', 'setextradata', katayuan_VALUE['uuid'], 'JKOROS/Owner', katayuan_VALUE['owner']])
            else:
                raise 실행오류('VM may_ari_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, katayuan_VALUE, msinfo32_exe):
        제어기들 = [VALUE for pangalan, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', pangalan)]
        payagan_VALUE = [str(self.path(VALUE)) for VALUE in katayuan_VALUE.get('media', [])]
        for pangalan, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(controller) + r'-\d+-\d+', pangalan) for controller in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in payagan_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def ipakita_katayuan(self):
        katayuan_VALUE = self.읽기()
        if katayuan_VALUE is None: return {'name': self.pangalan, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(katayuan_VALUE, 등록목록(self.utos(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', katayuan_VALUE['name']), 'uuid': katayuan_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.path(katayuan_VALUE['iso'])) if katayuan_VALUE.get('iso') else None,
                'serial_log': str(self.path(katayuan_VALUE['serial_log'])) if katayuan_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Mag_execute_utos(self):
        katayuan_VALUE = self.읽기()
        등록됨 = 등록목록(self.utos(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if katayuan_VALUE is not None and katayuan_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(katayuan_VALUE, 등록됨, bawiin_katayuan=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 Mag_execute_utos 중입니다. 재빌드·재시작하지 않습니다.')
                return self.ipakita_katayuan()
            self.매체검사(katayuan_VALUE, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.utos(['VBoxManage', 'controlvm', katayuan_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 buksan 전에 기존 기록도 보관한다.
                    if katayuan_VALUE.get('serial_log'):
                        원본 = self.path(katayuan_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.path('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.utos(['VBoxManage', 'startvm', katayuan_VALUE['uuid'], '--type', self.pamamaraan_MODE])
                return self.ipakita_katayuan()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 Bumalik_VALUE 다시 실행하세요.'.format(현재))
        elif katayuan_VALUE is not None and not katayuan_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.pangalan in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/Mag_execute_utos 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.utos(['make', '-C', str(self.root_VALUE / 'os'), 'iso']), end='')
        원본 = self.root_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + checksum(원본) + '.iso'
        patutunguhan_VALUE = self.path(매체)
        patutunguhan_VALUE.parent.mkdir(exist_ok=True)
        if patutunguhan_VALUE.exists():
            if checksum(patutunguhan_VALUE) != checksum(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(patutunguhan_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(patutunguhan_VALUE.parent)) as file:
                shutil.copyfile(str(원본), file.name)
                os.link(file.name, str(patutunguhan_VALUE))

        if katayuan_VALUE is None:
            katayuan_VALUE = {'version': 1, 'name': self.pangalan, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(katayuan_VALUE)
        if msinfo32_exe is None:
            self.utos(['VBoxManage', 'createvm', '--name', katayuan_VALUE['name'], '--uuid', katayuan_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.path('machines')), '--register'])
            self.utos(['VBoxManage', 'setextradata', katayuan_VALUE['uuid'], 'JKOROS/Owner', katayuan_VALUE['owner']])
        # build_system 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(katayuan_VALUE, 등록목록(self.utos(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('build_system 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(katayuan_VALUE, msinfo32_exe)
        katayuan_VALUE['iso'] = 매체
        if 매체 not in katayuan_VALUE['media']: katayuan_VALUE['media'].append(매체)
        katayuan_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.path(katayuan_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(katayuan_VALUE)
        self.utos(['VBoxManage', 'modifyvm', katayuan_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for pangalan, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', pangalan)]
        if 'JKOROS IDE' not in 제어기들:
            self.utos(['VBoxManage', 'storagectl', katayuan_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.utos(['VBoxManage', 'storageattach', katayuan_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(patutunguhan_VALUE)])
        katayuan_VALUE['pending'] = False
        self.Store_VALUE(katayuan_VALUE)
        self.utos(['VBoxManage', 'startvm', katayuan_VALUE['uuid'], '--type', self.pamamaraan_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.ipakita_katayuan()


def run():
    mag_parse_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Mag_execute_utos 및 katayuan_VALUE query_VALUE')
    mag_parse_VALUE.add_argument('action', choices=['run', 'status'])
    parameter_argumento = mag_parse_VALUE.parse_args()
    Mag_execute_utos = app_launcher(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parameter_argumento.action == 'status':
        print(json.dumps(Mag_execute_utos.ipakita_katayuan(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. host 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/pahintulot_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    Mag_execute_utos.path('lock').parent.mkdir(parents=True, exist_ok=True)
    with Mag_execute_utos.path('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Mag_execute_utos 작업이 진행 중입니다.')
        print(json.dumps(Mag_execute_utos.Mag_execute_utos(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: run()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        print('VBOX error: ' + str(error), file=sys.stderr)
        sys.exit(1)
