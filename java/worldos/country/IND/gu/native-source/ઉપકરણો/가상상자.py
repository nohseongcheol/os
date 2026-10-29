#!/usr/bin/env python3
"""jkoros 전용 VirtualBox એપ્લિકેશન_લૉન્ચર. 기존 VM/디스크/સંગ્રહ_કરવો_મૂલ્ય 상태는 삭제하지 않는다."""
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


def અમલ_કરો_શેલ_આદેશ(દલીલો):
    환경 = dict(os.environ, LC_ALL='C')
    પરિમાણ = subprocess.run([str(મૂલ્ય) for મૂલ્ય in દલીલો], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    સામગ્રી_મૂલ્ય = પરિમાણ.stdout.decode('utf-8', 'replace')
    if પરિમાણ.returncode:
        raise 실행오류('આદેશ નિષ્ફળતા_મૂલ્ય: ' + ' '.join(str(મૂલ્ય) for મૂલ્ય in દલીલો) + '\n' + સામગ્રી_મૂલ્ય[-10000:])
    return સામગ્રી_મૂલ્ય


def વિશેષતા_મૂલ્ય(સામગ્રી_મૂલ્ય):
    પરિમાણ = {}
    for લાઇન in સામગ્રી_મૂલ્ય.splitlines():
        if '=' not in લાઇન:
            continue
        નામ, મૂલ્ય = લાઇન.split('=', 1)
        if નામ.startswith('"'):
            નામ = json.loads(નામ)
        if મૂલ્ય.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(મૂલ્ય)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(મૂલ્ય): મૂલ્ય = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox વિશેષતા_મૂલ્ય સ્વરૂપ_મૂલ્ય ભૂલ: ' + લાઇન)
        પરિમાણ[નામ] = મૂલ્ય
    return પરિમાણ


def 등록목록(સામગ્રી_મૂલ્ય):
    પરિમાણ = {}
    for લાઇન in સામગ્રી_મૂલ્ય.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', લાઇન)
        if 일치: પરિમાણ[일치.group(2).lower()] = 일치.group(1)
    return પરિમાણ


def ચેકસમ(પથ):
    મૂલ્ય = hashlib.sha256()
    with પથ.open('rb') as ફાઈલ:
        for ડેટા in iter(lambda: ફાઈલ.read(1024 * 1024), b''): મૂલ્ય.update(ડેટા)
    return મૂલ્ય.hexdigest()


class એપ્લિકેશન_લૉન્ચર:
    def __init__(self, રૂટ_મૂલ્ય, નામ, પદ્ધતિ_મોડ='gui', આદેશ=અમલ_કરો_શેલ_આદેશ):
        self.રૂટ_મૂલ્ય = Path(રૂટ_મૂલ્ય).resolve()
        self.નામ, self.પદ્ધતિ_મોડ, self.આદેશ = નામ, પદ્ધતિ_મોડ, આદેશ
        self.보관 = self.રૂટ_મૂલ્ય / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', નામ) or નામ in ('.', '..'):
            raise 실행오류('VM 이름은 문자·અંક_મૂલ્ય·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if પદ્ધતિ_મોડ not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def પથ(self, પીઅર_મૂલ્ય):
        if Path(પીઅર_મૂલ્ય).is_absolute() or '..' in Path(પીઅર_મૂલ્ય).parts:
            raise 실행오류('잘못된 관리 પથ: ' + str(પીઅર_મૂલ્ય))
        પરિમાણ = self.보관
        for 부분 in ['.vbox'] + list(Path(પીઅર_મૂલ્ય).parts):
            if 부분 == '.vbox': પરિમાણ = self.보관
            else: પરિમાણ = પરિમાણ / 부분
            if પરિમાણ.is_symlink(): raise 실행오류('સંપર્ક_કરો 경로는 사용하지 않습니다: ' + str(પરિમાણ))
        return પરિમાણ

    def વાંચો(self):
        પથ = self.પથ('state.json')
        if not પથ.exists(): return None
        સ્થિતિ_મૂલ્ય_e10195a1 = json.loads(પથ.read_text(encoding='utf-8'))
        if સ્થિતિ_મૂલ્ય_e10195a1.get('version') != 1 or સ્થિતિ_મૂલ્ય_e10195a1.get('name') != self.નામ:
            raise 실행오류('관리 상태의 VM નામ/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for નામ in ('uuid', 'owner'):
            if str(uuid.UUID(સ્થિતિ_મૂલ્ય_e10195a1[નામ])) != સ્થિતિ_મૂલ્ય_e10195a1[નામ]: raise 실행오류('잘못된 VM ઓળખકર્તા_મૂલ્ય')
        return સ્થિતિ_મૂલ્ય_e10195a1

    def સંગ્રહ_કરવો_મૂલ્ય(self, સ્થિતિ_મૂલ્ય_e10195a1):
        ગંતવ્ય_મૂલ્ય = self.પથ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as ફાઈલ:
            json.dump(સ્થિતિ_મૂલ્ય_e10195a1, ફાઈલ, ensure_ascii=False, indent=2)
            ફાઈલ.write('\n')
            임시 = ફાઈલ.name
        os.replace(임시, str(ગંતવ્ય_મૂલ્ય))

    def સિસ્ટમ_માહિતી(self, સ્થિતિ_મૂલ્ય_e10195a1, 등록됨, પુનઃપ્રાપ્ત_કરો_સ્થિતિ=False):
        if સ્થિતિ_મૂલ્ય_e10195a1['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        સિસ્ટમ_માહિતી = વિશેષતા_મૂલ્ય(self.આદેશ(['VBoxManage', 'showvminfo', સ્થિતિ_મૂલ્ય_e10195a1['uuid'], '--machinereadable']))
        સ્થાન = Path(સિસ્ટમ_માહિતી.get('CfgFile', '')).resolve()
        if self.પથ('machines').resolve() not in સ્થાન.parents or સિસ્ટમ_માહિતી.get('UUID') != સ્થિતિ_મૂલ્ય_e10195a1['uuid']:
            raise 실행오류('이 프로젝트의 VM સુયોજના પથ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.આદેશ(['VBoxManage', 'getextradata', સ્થિતિ_મૂલ્ય_e10195a1['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + સ્થિતિ_મૂલ્ય_e10195a1['owner']:
            if પુનઃપ્રાપ્ત_કરો_સ્થિતિ and સ્થિતિ_મૂલ્ય_e10195a1.get('pending') and 표식 == 'No value set!':
                self.આદેશ(['VBoxManage', 'setextradata', સ્થિતિ_મૂલ્ય_e10195a1['uuid'], 'JKOROS/Owner', સ્થિતિ_મૂલ્ય_e10195a1['owner']])
            else:
                raise 실행오류('VM સ્વામી_મૂલ્ય 표식이 일치하지 않아 변경하지 않습니다.')
        return સિસ્ટમ_માહિતી

    def 매체검사(self, સ્થિતિ_મૂલ્ય_e10195a1, સિસ્ટમ_માહિતી):
        제어기들 = [મૂલ્ય for નામ, મૂલ્ય in સિસ્ટમ_માહિતી.items() if re.fullmatch(r'storagecontrollername\d+', નામ)]
        પરવાનગી_આપો_મૂલ્ય = [str(self.પથ(મૂલ્ય)) for મૂલ્ય in સ્થિતિ_મૂલ્ય_e10195a1.get('media', [])]
        for નામ, મૂલ્ય in સિસ્ટમ_માહિતી.items():
            if any(re.fullmatch(re.escape(કંટ્રોલર) + r'-\d+-\d+', નામ) for કંટ્રોલર in 제어기들):
                if મૂલ્ય not in ('none', 'emptydrive') and મૂલ્ય not in પરવાનગી_આપો_મૂલ્ય:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + મૂલ્ય)

    def શૉ_સ્થિતિ(self):
        સ્થિતિ_મૂલ્ય_e10195a1 = self.વાંચો()
        if સ્થિતિ_મૂલ્ય_e10195a1 is None: return {'name': self.નામ, 'state': 'not-created'}
        સિસ્ટમ_માહિતી = self.સિસ્ટમ_માહિતી(સ્થિતિ_મૂલ્ય_e10195a1, 등록목록(self.આદેશ(['VBoxManage', 'list', 'vms'])))
        return {'name': સિસ્ટમ_માહિતી.get('name', સ્થિતિ_મૂલ્ય_e10195a1['name']), 'uuid': સ્થિતિ_મૂલ્ય_e10195a1['uuid'], 'state': સિસ્ટમ_માહિતી.get('VMState'),
                'iso': str(self.પથ(સ્થિતિ_મૂલ્ય_e10195a1['iso'])) if સ્થિતિ_મૂલ્ય_e10195a1.get('iso') else None,
                'serial_log': str(self.પથ(સ્થિતિ_મૂલ્ય_e10195a1['serial_log'])) if સ્થિતિ_મૂલ્ય_e10195a1.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def અમલ_કરો_આદેશ(self):
        સ્થિતિ_મૂલ્ય_e10195a1 = self.વાંચો()
        등록됨 = 등록목록(self.આદેશ(['VBoxManage', 'list', 'vms']))
        સિસ્ટમ_માહિતી = None
        if સ્થિતિ_મૂલ્ય_e10195a1 is not None and સ્થિતિ_મૂલ્ય_e10195a1['uuid'] in 등록됨:
            સિસ્ટમ_માહિતી = self.સિસ્ટમ_માહિતી(સ્થિતિ_મૂલ્ય_e10195a1, 등록됨, પુનઃપ્રાપ્ત_કરો_સ્થિતિ=True)
            현재 = સિસ્ટમ_માહિતી.get('VMState')
            if 현재 == 'running':
                print('이미 અમલ_કરો_આદેશ 중입니다. 재빌드·재시작하지 않습니다.')
                return self.શૉ_સ્થિતિ()
            self.매체검사(સ્થિતિ_મૂલ્ય_e10195a1, સિસ્ટમ_માહિતી)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 સંગ્રહ_કરવો_મૂલ્ય 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.આદેશ(['VBoxManage', 'controlvm', સ્થિતિ_મૂલ્ય_e10195a1['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 ખોલો 전에 기존 기록도 보관한다.
                    if સ્થિતિ_મૂલ્ય_e10195a1.get('serial_log'):
                        원본 = self.પથ(સ્થિતિ_મૂલ્ય_e10195a1['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.પથ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.આદેશ(['VBoxManage', 'startvm', સ્થિતિ_મૂલ્ય_e10195a1['uuid'], '--type', self.પદ્ધતિ_મોડ])
                return self.શૉ_સ્થિતિ()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 સ્વિચ_મોડ 중입니다 ({}). 작업이 끝난 બેક_મૂલ્ય 다시 실행하세요.'.format(현재))
        elif સ્થિતિ_મૂલ્ય_e10195a1 is not None and not સ્થિતિ_મૂલ્ય_e10195a1.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.નામ in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # સંગ્રહ_કરવો_મૂલ્ય/અમલ_કરો_આદેશ 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.આદેશ(['make', '-C', str(self.રૂટ_મૂલ્ય / 'os'), 'iso']), end='')
        원본 = self.રૂટ_મૂલ્ય / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + ચેકસમ(원본) + '.iso'
        ગંતવ્ય_મૂલ્ય = self.પથ(매체)
        ગંતવ્ય_મૂલ્ય.parent.mkdir(exist_ok=True)
        if ગંતવ્ય_મૂલ્ય.exists():
            if ચેકસમ(ગંતવ્ય_મૂલ્ય) != ચેકસમ(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(ગંતવ્ય_મૂલ્ય))
        else:
            with tempfile.NamedTemporaryFile(dir=str(ગંતવ્ય_મૂલ્ય.parent)) as ફાઈલ:
                shutil.copyfile(str(원본), ફાઈલ.name)
                os.link(ફાઈલ.name, str(ગંતવ્ય_મૂલ્ય))

        if સ્થિતિ_મૂલ્ય_e10195a1 is None:
            સ્થિતિ_મૂલ્ય_e10195a1 = {'version': 1, 'name': self.નામ, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.સંગ્રહ_કરવો_મૂલ્ય(સ્થિતિ_મૂલ્ય_e10195a1)
        if સિસ્ટમ_માહિતી is None:
            self.આદેશ(['VBoxManage', 'createvm', '--name', સ્થિતિ_મૂલ્ય_e10195a1['name'], '--uuid', સ્થિતિ_મૂલ્ય_e10195a1['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.પથ('machines')), '--register'])
            self.આદેશ(['VBoxManage', 'setextradata', સ્થિતિ_મૂલ્ય_e10195a1['uuid'], 'JKOROS/Owner', સ્થિતિ_મૂલ્ય_e10195a1['owner']])
        # બિલ્ડ_સિસ્ટમ 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        સિસ્ટમ_માહિતી = self.સિસ્ટમ_માહિતી(સ્થિતિ_મૂલ્ય_e10195a1, 등록목록(self.આદેશ(['VBoxManage', 'list', 'vms'])))
        if સિસ્ટમ_માહિતી.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('બિલ્ડ_સિસ્ટમ 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(સ્થિતિ_મૂલ્ય_e10195a1, સિસ્ટમ_માહિતી)
        સ્થિતિ_મૂલ્ય_e10195a1['iso'] = 매체
        if 매체 not in સ્થિતિ_મૂલ્ય_e10195a1['media']: સ્થિતિ_મૂલ્ય_e10195a1['media'].append(매체)
        સ્થિતિ_મૂલ્ય_e10195a1['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        લૉગ_મૂલ્ય = self.પથ(સ્થિતિ_મૂલ્ય_e10195a1['serial_log'])
        લૉગ_મૂલ્ય.parent.mkdir(exist_ok=True)
        self.સંગ્રહ_કરવો_મૂલ્ય(સ્થિતિ_મૂલ્ય_e10195a1)
        self.આદેશ(['VBoxManage', 'modifyvm', સ્થિતિ_મૂલ્ય_e10195a1['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(લૉગ_મૂલ્ય)])
        제어기들 = [મૂલ્ય for નામ, મૂલ્ય in સિસ્ટમ_માહિતી.items() if re.fullmatch(r'storagecontrollername\d+', નામ)]
        if 'JKOROS IDE' not in 제어기들:
            self.આદેશ(['VBoxManage', 'storagectl', સ્થિતિ_મૂલ્ય_e10195a1['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.આદેશ(['VBoxManage', 'storageattach', સ્થિતિ_મૂલ્ય_e10195a1['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(ગંતવ્ય_મૂલ્ય)])
        સ્થિતિ_મૂલ્ય_e10195a1['pending'] = False
        self.સંગ્રહ_કરવો_મૂલ્ય(સ્થિતિ_મૂલ્ય_e10195a1)
        self.આદેશ(['VBoxManage', 'startvm', સ્થિતિ_મૂલ્ય_e10195a1['uuid'], '--type', self.પદ્ધતિ_મોડ])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.શૉ_સ્થિતિ()


def ચલાવો_2():
    પાર્સ_કરો_મૂલ્ય = argparse.ArgumentParser(description='jkoros 전용 VirtualBox અમલ_કરો_આદેશ 및 સ્થિતિ_મૂલ્ય_e10195a1 ક્વેરી_મૂલ્ય')
    પાર્સ_કરો_મૂલ્ય.add_argument('action', choices=['run', 'status'])
    પેરામીટર_દલીલ = પાર્સ_કરો_મૂલ્ય.parse_args()
    અમલ_કરો_આદેશ = એપ્લિકેશન_લૉન્ચર(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if પેરામીટર_દલીલ.action == 'status':
        print(json.dumps(અમલ_કરો_આદેશ.શૉ_સ્થિતિ(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. હોસ્ટ 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/અનુમતિ_મૂલ્ય 변경은 하지 않습니다.')
    os.umask(0o077)
    અમલ_કરો_આદેશ.પથ('lock').parent.mkdir(parents=True, exist_ok=True)
    with અમલ_કરો_આદેશ.પથ('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox અમલ_કરો_આદેશ 작업이 진행 중입니다.')
        print(json.dumps(અમલ_કરો_આદેશ.અમલ_કરો_આદેશ(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: ચલાવો_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ભૂલ:
        print('VBOX ભૂલ: ' + str(ભૂલ), file=sys.stderr)
        sys.exit(1)
