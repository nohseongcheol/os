#!/usr/bin/env python3
"""jkoros 전용 VirtualBox പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ. 기존 VM/디스크/സ്_റ്റോർ_മൂല്യം 상태는 삭제하지 않는다."""
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


def നടപ്പാക്കുക_ഷെല്_കമാന്_ഡ്(인수):
    환경 = dict(os.environ, LC_ALL='C')
    അളവ് = subprocess.run([str(മൂല്യം) for മൂല്യം in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    ഉള്ളടക്കം_മൂല്യം = അളവ്.stdout.decode('utf-8', 'replace')
    if അളവ്.returncode:
        raise 실행오류('ആജ്ഞ പരാജയം_മൂല്യം: ' + ' '.join(str(മൂല്യം) for മൂല്യം in 인수) + '\n' + ഉള്ളടക്കം_മൂല്യം[-10000:])
    return ഉള്ളടക്കം_മൂല്യം


def ആട്രിബ്യൂട്ട്_മൂല്യം(ഉള്ളടക്കം_മൂല്യം):
    അളവ് = {}
    for ലൈൻ in ഉള്ളടക്കം_മൂല്യം.splitlines():
        if '=' not in ലൈൻ:
            continue
        പേരു്, മൂല്യം = ലൈൻ.split('=', 1)
        if പേരു്.startswith('"'):
            പേരു് = json.loads(പേരു്)
        if മൂല്യം.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(മൂല്യം)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(മൂല്യം): മൂല്യം = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox ആട്രിബ്യൂട്ട്_മൂല്യം ఫార్మాట్_മൂല്യം പിശക്: ' + ലൈൻ)
        അളവ്[പേരു്] = മൂല്യം
    return അളവ്


def 등록목록(ഉള്ളടക്കം_മൂല്യം):
    അളവ് = {}
    for ലൈൻ in ഉള്ളടക്കം_മൂല്യം.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', ലൈൻ)
        if 일치: അളവ്[일치.group(2).lower()] = 일치.group(1)
    return അളവ്


def 검사합(വഴി):
    മൂല്യം = hashlib.sha256()
    with വഴി.open('rb') as ഫയല്:
        for ഡാറ്റാ in iter(lambda: ഫയല്.read(1024 * 1024), b''): മൂല്യം.update(ഡാറ്റാ)
    return മൂല്യം.hexdigest()


class പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ:
    def __init__(self, വർഗ്ഗമൂലം_മൂല്യം, പേരു്, విధానం_മോഡ്='gui', ആജ്ഞ=നടപ്പാക്കുക_ഷെല്_കമാന്_ഡ്):
        self.വർഗ്ഗമൂലം_മൂല്യം = Path(വർഗ്ഗമൂലം_മൂല്യം).resolve()
        self.പേരു്, self.విధానం_മോഡ്, self.ആജ്ഞ = പേരു്, విధానం_മോഡ്, ആജ്ഞ
        self.보관 = self.വർഗ്ഗമൂലം_മൂല്യം / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', പേരു്) or പേരു് in ('.', '..'):
            raise 실행오류('VM 이름은 문자·അക്കം_മൂല്യം·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if విధానం_മോഡ് not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def വഴി(self, പീര്_മൂല്യം):
        if Path(പീര്_മൂല്യം).is_absolute() or '..' in Path(പീര്_മൂല്യം).parts:
            raise 실행오류('잘못된 관리 വഴി: ' + str(പീര്_മൂല്യം))
        അളവ് = self.보관
        for 부분 in ['.vbox'] + list(Path(പീര്_മൂല്യം).parts):
            if 부분 == '.vbox': അളവ് = self.보관
            else: അളവ് = അളവ് / 부분
            if അളവ്.is_symlink(): raise 실행오류('കണക്ടു്_ചെയ്യുക 경로는 사용하지 않습니다: ' + str(അളവ്))
        return അളവ്

    def വായന(self):
        വഴി = self.വഴി('state.json')
        if not വഴി.exists(): return None
        അവസ്ഥ_മൂല്യം = json.loads(വഴി.read_text(encoding='utf-8'))
        if അവസ്ഥ_മൂല്യം.get('version') != 1 or അവസ്ഥ_മൂല്യം.get('name') != self.പേരു്:
            raise 실행오류('관리 상태의 VM പേരു്/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for പേരു് in ('uuid', 'owner'):
            if str(uuid.UUID(അവസ്ഥ_മൂല്യം[പേരു്])) != അവസ്ഥ_മൂല്യം[പേരു്]: raise 실행오류('잘못된 VM ఐడెంటిఫయర్_മൂല്യം')
        return അവസ്ഥ_മൂല്യം

    def സ്_റ്റോർ_മൂല്യം(self, അവസ്ഥ_മൂല്യം):
        ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം = self.വഴി('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as ഫയല്:
            json.dump(അവസ്ഥ_മൂല്യം, ഫയല്, ensure_ascii=False, indent=2)
            ഫയല്.write('\n')
            임시 = ഫയല്.name
        os.replace(임시, str(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം))

    def സിസ്റ്റം_വിവരങ്ങള്(self, അവസ്ഥ_മൂല്യം, 등록됨, വീണ്ടെടുക്കുക_അവസ്ഥ=False):
        if അവസ്ഥ_മൂല്യം['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        സിസ്റ്റം_വിവരങ്ങള് = ആട്രിബ്യൂട്ട്_മൂല്യം(self.ആജ്ഞ(['VBoxManage', 'showvminfo', അവസ്ഥ_മൂല്യം['uuid'], '--machinereadable']))
        സ്ഥാനം = Path(സിസ്റ്റം_വിവരങ്ങള്.get('CfgFile', '')).resolve()
        if self.വഴി('machines').resolve() not in സ്ഥാനം.parents or സിസ്റ്റം_വിവരങ്ങള്.get('UUID') != അവസ്ഥ_മൂല്യം['uuid']:
            raise 실행오류('이 프로젝트의 VM സജ്ജീകരണം വഴി/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.ആജ്ഞ(['VBoxManage', 'getextradata', അവസ്ഥ_മൂല്യം['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + അവസ്ഥ_മൂല്യം['owner']:
            if വീണ്ടെടുക്കുക_അവസ്ഥ and അവസ്ഥ_മൂല്യം.get('pending') and 표식 == 'No value set!':
                self.ആജ്ഞ(['VBoxManage', 'setextradata', അവസ്ഥ_മൂല്യം['uuid'], 'JKOROS/Owner', അവസ്ഥ_മൂല്യം['owner']])
            else:
                raise 실행오류('VM ഉടമ_മൂല്യം 표식이 일치하지 않아 변경하지 않습니다.')
        return സിസ്റ്റം_വിവരങ്ങള്

    def 매체검사(self, അവസ്ഥ_മൂല്യം, സിസ്റ്റം_വിവരങ്ങള്):
        제어기들 = [മൂല്യം for പേരു്, മൂല്യം in സിസ്റ്റം_വിവരങ്ങള്.items() if re.fullmatch(r'storagecontrollername\d+', പേരു്)]
        അനുവദിക്കുക_മൂല്യം = [str(self.വഴി(മൂല്യം)) for മൂല്യം in അവസ്ഥ_മൂല്യം.get('media', [])]
        for പേരു്, മൂല്യം in സിസ്റ്റം_വിവരങ്ങള്.items():
            if any(re.fullmatch(re.escape(കൺട്രോളർ) + r'-\d+-\d+', പേരു്) for കൺട്രോളർ in 제어기들):
                if മൂല്യം not in ('none', 'emptydrive') and മൂല്യം not in അനുവദിക്കുക_മൂല്യം:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + മൂല്യം)

    def പ്രദർശനം_അവസ്ഥ(self):
        അവസ്ഥ_മൂല്യം = self.വായന()
        if അവസ്ഥ_മൂല്യം is None: return {'name': self.പേരു്, 'state': 'not-created'}
        സിസ്റ്റം_വിവരങ്ങള് = self.സിസ്റ്റം_വിവരങ്ങള്(അവസ്ഥ_മൂല്യം, 등록목록(self.ആജ്ഞ(['VBoxManage', 'list', 'vms'])))
        return {'name': സിസ്റ്റം_വിവരങ്ങള്.get('name', അവസ്ഥ_മൂല്യം['name']), 'uuid': അവസ്ഥ_മൂല്യം['uuid'], 'state': സിസ്റ്റം_വിവരങ്ങള്.get('VMState'),
                'iso': str(self.വഴി(അവസ്ഥ_മൂല്യം['iso'])) if അവസ്ഥ_മൂല്യം.get('iso') else None,
                'serial_log': str(self.വഴി(അവസ്ഥ_മൂല്യം['serial_log'])) if അവസ്ഥ_മൂല്യം.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def നടപ്പാക്കുക_കമാന്_ഡ്(self):
        അവസ്ഥ_മൂല്യം = self.വായന()
        등록됨 = 등록목록(self.ആജ്ഞ(['VBoxManage', 'list', 'vms']))
        സിസ്റ്റം_വിവരങ്ങള് = None
        if അവസ്ഥ_മൂല്യം is not None and അവസ്ഥ_മൂല്യം['uuid'] in 등록됨:
            സിസ്റ്റം_വിവരങ്ങള് = self.സിസ്റ്റം_വിവരങ്ങള്(അവസ്ഥ_മൂല്യം, 등록됨, വീണ്ടെടുക്കുക_അവസ്ഥ=True)
            현재 = സിസ്റ്റം_വിവരങ്ങള്.get('VMState')
            if 현재 == 'running':
                print('이미 നടപ്പാക്കുക_കമാന്_ഡ് 중입니다. 재빌드·재시작하지 않습니다.')
                return self.പ്രദർശനം_അവസ്ഥ()
            self.매체검사(അവസ്ഥ_മൂല്യം, സിസ്റ്റം_വിവരങ്ങള്)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 സ്_റ്റോർ_മൂല്യം 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.ആജ്ഞ(['VBoxManage', 'controlvm', അവസ്ഥ_മൂല്യം['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 തുറക്കുക 전에 기존 기록도 보관한다.
                    if അവസ്ഥ_മൂല്യം.get('serial_log'):
                        원본 = self.വഴി(അവസ്ഥ_മൂല്യം['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.വഴി('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.ആജ്ഞ(['VBoxManage', 'startvm', അവസ്ഥ_മൂല്യം['uuid'], '--type', self.విధానం_മോഡ്])
                return self.പ്രദർശനം_അവസ്ഥ()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 സ്വിച്ച്_മോഡ് 중입니다 ({}). 작업이 끝난 പിന്നിലേക്ക്_മൂല്യം 다시 실행하세요.'.format(현재))
        elif അവസ്ഥ_മൂല്യം is not None and not അവസ്ഥ_മൂല്യം.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.പേരു് in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # സ്_റ്റോർ_മൂല്യം/നടപ്പാക്കുക_കമാന്_ഡ് 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.ആജ്ഞ(['make', '-C', str(self.വർഗ്ഗമൂലം_മൂല്യം / 'os'), 'iso']), end='')
        원본 = self.വർഗ്ഗമൂലം_മൂല്യം / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം = self.വഴി(매체)
        ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം.parent.mkdir(exist_ok=True)
        if ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം.exists():
            if 검사합(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം))
        else:
            with tempfile.NamedTemporaryFile(dir=str(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം.parent)) as ഫയല്:
                shutil.copyfile(str(원본), ഫയല്.name)
                os.link(ഫയല്.name, str(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം))

        if അവസ്ഥ_മൂല്യം is None:
            അവസ്ഥ_മൂല്യം = {'version': 1, 'name': self.പേരു്, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.സ്_റ്റോർ_മൂല്യം(അവസ്ഥ_മൂല്യം)
        if സിസ്റ്റം_വിവരങ്ങള് is None:
            self.ആജ്ഞ(['VBoxManage', 'createvm', '--name', അവസ്ഥ_മൂല്യം['name'], '--uuid', അവസ്ഥ_മൂല്യം['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.വഴി('machines')), '--register'])
            self.ആജ്ഞ(['VBoxManage', 'setextradata', അവസ്ഥ_മൂല്യം['uuid'], 'JKOROS/Owner', അവസ്ഥ_മൂല്യം['owner']])
        # ബിൽഡ്_సిస్టమ్ 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        സിസ്റ്റം_വിവരങ്ങള് = self.സിസ്റ്റം_വിവരങ്ങള്(അവസ്ഥ_മൂല്യം, 등록목록(self.ആജ്ഞ(['VBoxManage', 'list', 'vms'])))
        if സിസ്റ്റം_വിവരങ്ങള്.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('ബിൽഡ്_సిస్టమ్ 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(അവസ്ഥ_മൂല്യം, സിസ്റ്റം_വിവരങ്ങള്)
        അവസ്ഥ_മൂല്യം['iso'] = 매체
        if 매체 not in അവസ്ഥ_മൂല്യം['media']: അവസ്ഥ_മൂല്യം['media'].append(매체)
        അവസ്ഥ_മൂല്യം['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        ലോഗ്_മൂല്യം = self.വഴി(അവസ്ഥ_മൂല്യം['serial_log'])
        ലോഗ്_മൂല്യം.parent.mkdir(exist_ok=True)
        self.സ്_റ്റോർ_മൂല്യം(അവസ്ഥ_മൂല്യം)
        self.ആജ്ഞ(['VBoxManage', 'modifyvm', അവസ്ഥ_മൂല്യം['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(ലോഗ്_മൂല്യം)])
        제어기들 = [മൂല്യം for പേരു്, മൂല്യം in സിസ്റ്റം_വിവരങ്ങള്.items() if re.fullmatch(r'storagecontrollername\d+', പേരു്)]
        if 'JKOROS IDE' not in 제어기들:
            self.ആജ്ഞ(['VBoxManage', 'storagectl', അവസ്ഥ_മൂല്യം['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.ആജ്ഞ(['VBoxManage', 'storageattach', അവസ്ഥ_മൂല്യം['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം)])
        അവസ്ഥ_മൂല്യം['pending'] = False
        self.സ്_റ്റോർ_മൂല്യം(അവസ്ഥ_മൂല്യം)
        self.ആജ്ഞ(['VBoxManage', 'startvm', അവസ്ഥ_മൂല്യം['uuid'], '--type', self.విధానం_മോഡ്])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.പ്രദർശനം_അവസ്ഥ()


def നടപ്പിലാക്കുക():
    പാര്_സ്_ചെയ്യുക_മൂല്യം = argparse.ArgumentParser(description='jkoros 전용 VirtualBox നടപ്പാക്കുക_കമാന്_ഡ് 및 അവസ്ഥ_മൂല്യം ചോദ്യം_മൂല്യം')
    പാര്_സ്_ചെയ്യുക_മൂല്യം.add_argument('action', choices=['run', 'status'])
    പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ് = പാര്_സ്_ചെയ്യുക_മൂല്യം.parse_args()
    നടപ്പാക്കുക_കമാന്_ഡ് = പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.action == 'status':
        print(json.dumps(നടപ്പാക്കുക_കമാന്_ഡ്.പ്രദർശനം_അവസ്ഥ(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. ഹോസ്റ്റ് 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/അനുമതി_മൂല്യം 변경은 하지 않습니다.')
    os.umask(0o077)
    നടപ്പാക്കുക_കമാന്_ഡ്.വഴി('lock').parent.mkdir(parents=True, exist_ok=True)
    with നടപ്പാക്കുക_കമാന്_ഡ്.വഴി('lock').open('a') as ലോക്ക്_മൂല്യം:
        try: fcntl.flock(ലോക്ക്_മൂല്യം, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox നടപ്പാക്കുക_കമാന്_ഡ് 작업이 진행 중입니다.')
        print(json.dumps(നടപ്പാക്കുക_കമാന്_ഡ്.നടപ്പാക്കുക_കമാന്_ഡ്(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: നടപ്പിലാക്കുക()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as പിശക്:
        print('VBOX പിശക്: ' + str(പിശക്), file=sys.stderr)
        sys.exit(1)
