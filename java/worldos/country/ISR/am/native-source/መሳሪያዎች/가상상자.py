#!/usr/bin/env python3
"""jkoros 전용 VirtualBox ፕሮግራም_የመተግበሪያ_መሳቢያ. 기존 VM/디스크/ማከማቻ_እሴት 상태는 삭제하지 않는다."""
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


def ፈጽም_ሼል_ትእዛዝ(인수):
    환경 = dict(os.environ, LC_ALL='C')
    ልኬት = subprocess.run([str(እሴት) for እሴት in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    ይዘት_እሴት = ልኬት.stdout.decode('utf-8', 'replace')
    if ልኬት.returncode:
        raise 실행오류('ትእዛዝ ተስኖት_እሴት: ' + ' '.join(str(እሴት) for እሴት in 인수) + '\n' + ይዘት_እሴት[-10000:])
    return ይዘት_እሴት


def ዓይነታ_እሴት(ይዘት_እሴት):
    ልኬት = {}
    for መስመር in ይዘት_እሴት.splitlines():
        if '=' not in መስመር:
            continue
        ስም, እሴት = መስመር.split('=', 1)
        if ስም.startswith('"'):
            ስም = json.loads(ስም)
        if እሴት.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(እሴት)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(እሴት): እሴት = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox ዓይነታ_እሴት ቅርጸት_እሴት ስህተት: ' + መስመር)
        ልኬት[ስም] = እሴት
    return ልኬት


def 등록목록(ይዘት_እሴት):
    ልኬት = {}
    for መስመር in ይዘት_እሴት.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', መስመር)
        if 일치: ልኬት[일치.group(2).lower()] = 일치.group(1)
    return ልኬት


def ድምር_ፍተሻ(መተላለፊያ):
    እሴት = hashlib.sha256()
    with መተላለፊያ.open('rb') as ፋይል:
        for ውሂብ in iter(lambda: ፋይል.read(1024 * 1024), b''): እሴት.update(ውሂብ)
    return እሴት.hexdigest()


class ፕሮግራም_የመተግበሪያ_መሳቢያ:
    def __init__(self, ስር_እሴት, ስም, ስልት_ሁነታ='gui', ትእዛዝ=ፈጽም_ሼል_ትእዛዝ):
        self.ስር_እሴት = Path(ስር_እሴት).resolve()
        self.ስም, self.ስልት_ሁነታ, self.ትእዛዝ = ስም, ስልት_ሁነታ, ትእዛዝ
        self.보관 = self.ስር_እሴት / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', ስም) or ስም in ('.', '..'):
            raise 실행오류('VM 이름은 문자·숫자·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if ስልት_ሁነታ not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def መተላለፊያ(self, አቻ_እሴት):
        if Path(አቻ_እሴት).is_absolute() or '..' in Path(አቻ_እሴት).parts:
            raise 실행오류('잘못된 관리 መተላለፊያ: ' + str(አቻ_እሴት))
        ልኬት = self.보관
        for 부분 in ['.vbox'] + list(Path(አቻ_እሴት).parts):
            if 부분 == '.vbox': ልኬት = self.보관
            else: ልኬት = ልኬት / 부분
            if ልኬት.is_symlink(): raise 실행오류('መገናኛ 경로는 사용하지 않습니다: ' + str(ልኬት))
        return ልኬት

    def ማንበቢያ(self):
        መተላለፊያ = self.መተላለፊያ('state.json')
        if not መተላለፊያ.exists(): return None
        ዞን_እሴት = json.loads(መተላለፊያ.read_text(encoding='utf-8'))
        if ዞን_እሴት.get('version') != 1 or ዞን_እሴት.get('name') != self.ስም:
            raise 실행오류('관리 상태의 VM ስም/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for ስም in ('uuid', 'owner'):
            if str(uuid.UUID(ዞን_እሴት[ስም])) != ዞን_እሴት[ስም]: raise 실행오류('잘못된 VM መለያ_እሴት_5b7b8b77')
        return ዞን_እሴት

    def ማከማቻ_እሴት(self, ዞን_እሴት):
        መድረሻ_እሴት = self.መተላለፊያ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as ፋይል:
            json.dump(ዞን_እሴት, ፋይል, ensure_ascii=False, indent=2)
            ፋይል.write('\n')
            임시 = ፋይል.name
        os.replace(임시, str(መድረሻ_እሴት))

    def የስርዓት_መረጃ(self, ዞን_እሴት, 등록됨, ወደ_ነበረበት_መልስ_ዞን=False):
        if ዞን_እሴት['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        የስርዓት_መረጃ = ዓይነታ_እሴት(self.ትእዛዝ(['VBoxManage', 'showvminfo', ዞን_እሴት['uuid'], '--machinereadable']))
        አካባቢ = Path(የስርዓት_መረጃ.get('CfgFile', '')).resolve()
        if self.መተላለፊያ('machines').resolve() not in አካባቢ.parents or የስርዓት_መረጃ.get('UUID') != ዞን_እሴት['uuid']:
            raise 실행오류('이 프로젝트의 VM ማሰናጃዎች መተላለፊያ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.ትእዛዝ(['VBoxManage', 'getextradata', ዞን_እሴት['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + ዞን_እሴት['owner']:
            if ወደ_ነበረበት_መልስ_ዞን and ዞን_እሴት.get('pending') and 표식 == 'No value set!':
                self.ትእዛዝ(['VBoxManage', 'setextradata', ዞን_እሴት['uuid'], 'JKOROS/Owner', ዞን_እሴት['owner']])
            else:
                raise 실행오류('VM ባለቤት_እሴት 표식이 일치하지 않아 변경하지 않습니다.')
        return የስርዓት_መረጃ

    def 매체검사(self, ዞን_እሴት, የስርዓት_መረጃ):
        제어기들 = [እሴት for ስም, እሴት in የስርዓት_መረጃ.items() if re.fullmatch(r'storagecontrollername\d+', ስም)]
        ፍቀድ_እሴት = [str(self.መተላለፊያ(እሴት)) for እሴት in ዞን_እሴት.get('media', [])]
        for ስም, እሴት in የስርዓት_መረጃ.items():
            if any(re.fullmatch(re.escape(ተቆጣጣሪ) + r'-\d+-\d+', ስም) for ተቆጣጣሪ in 제어기들):
                if እሴት not in ('none', 'emptydrive') and እሴት not in ፍቀድ_እሴት:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + እሴት)

    def አሳይ_ዞን(self):
        ዞን_እሴት = self.ማንበቢያ()
        if ዞን_እሴት is None: return {'name': self.ስም, 'state': 'not-created'}
        የስርዓት_መረጃ = self.የስርዓት_መረጃ(ዞን_እሴት, 등록목록(self.ትእዛዝ(['VBoxManage', 'list', 'vms'])))
        return {'name': የስርዓት_መረጃ.get('name', ዞን_እሴት['name']), 'uuid': ዞን_እሴት['uuid'], 'state': የስርዓት_መረጃ.get('VMState'),
                'iso': str(self.መተላለፊያ(ዞን_እሴት['iso'])) if ዞን_እሴት.get('iso') else None,
                'serial_log': str(self.መተላለፊያ(ዞን_እሴት['serial_log'])) if ዞን_እሴት.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def ፈጽም_ትእዛዝ(self):
        ዞን_እሴት = self.ማንበቢያ()
        등록됨 = 등록목록(self.ትእዛዝ(['VBoxManage', 'list', 'vms']))
        የስርዓት_መረጃ = None
        if ዞን_እሴት is not None and ዞን_እሴት['uuid'] in 등록됨:
            የስርዓት_መረጃ = self.የስርዓት_መረጃ(ዞን_እሴት, 등록됨, ወደ_ነበረበት_መልስ_ዞን=True)
            현재 = የስርዓት_መረጃ.get('VMState')
            if 현재 == 'running':
                print('이미 ፈጽም_ትእዛዝ 중입니다. 재빌드·재시작하지 않습니다.')
                return self.አሳይ_ዞን()
            self.매체검사(ዞን_እሴት, የስርዓት_መረጃ)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 ማከማቻ_እሴት 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.ትእዛዝ(['VBoxManage', 'controlvm', ዞን_እሴት['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 መክፈቻ 전에 기존 기록도 보관한다.
                    if ዞን_እሴት.get('serial_log'):
                        원본 = self.መተላለፊያ(ዞን_እሴት['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.መተላለፊያ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.ትእዛዝ(['VBoxManage', 'startvm', ዞን_እሴት['uuid'], '--type', self.ስልት_ሁነታ])
                return self.አሳይ_ዞን()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 ቀይር_ሁነታ 중입니다 ({}). 작업이 끝난 ተመለስ_እሴት 다시 실행하세요.'.format(현재))
        elif ዞን_እሴት is not None and not ዞን_እሴት.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.ስም in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # ማከማቻ_እሴት/ፈጽም_ትእዛዝ 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.ትእዛዝ(['make', '-C', str(self.ስር_እሴት / 'os'), 'iso']), end='')
        원본 = self.ስር_እሴት / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + ድምር_ፍተሻ(원본) + '.iso'
        መድረሻ_እሴት = self.መተላለፊያ(매체)
        መድረሻ_እሴት.parent.mkdir(exist_ok=True)
        if መድረሻ_እሴት.exists():
            if ድምር_ፍተሻ(መድረሻ_እሴት) != ድምር_ፍተሻ(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(መድረሻ_እሴት))
        else:
            with tempfile.NamedTemporaryFile(dir=str(መድረሻ_እሴት.parent)) as ፋይል:
                shutil.copyfile(str(원본), ፋይል.name)
                os.link(ፋይል.name, str(መድረሻ_እሴት))

        if ዞን_እሴት is None:
            ዞን_እሴት = {'version': 1, 'name': self.ስም, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.ማከማቻ_እሴት(ዞን_እሴት)
        if የስርዓት_መረጃ is None:
            self.ትእዛዝ(['VBoxManage', 'createvm', '--name', ዞን_እሴት['name'], '--uuid', ዞን_እሴት['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.መተላለፊያ('machines')), '--register'])
            self.ትእዛዝ(['VBoxManage', 'setextradata', ዞን_እሴት['uuid'], 'JKOROS/Owner', ዞን_እሴት['owner']])
        # ግንብ_ስርዓት 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        የስርዓት_መረጃ = self.የስርዓት_መረጃ(ዞን_እሴት, 등록목록(self.ትእዛዝ(['VBoxManage', 'list', 'vms'])))
        if የስርዓት_መረጃ.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('ግንብ_ስርዓት 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(ዞን_እሴት, የስርዓት_መረጃ)
        ዞን_እሴት['iso'] = 매체
        if 매체 not in ዞን_እሴት['media']: ዞን_እሴት['media'].append(매체)
        ዞን_እሴት['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        መዝግብ_እሴት_e0918eb0 = self.መተላለፊያ(ዞን_እሴት['serial_log'])
        መዝግብ_እሴት_e0918eb0.parent.mkdir(exist_ok=True)
        self.ማከማቻ_እሴት(ዞን_እሴት)
        self.ትእዛዝ(['VBoxManage', 'modifyvm', ዞን_እሴት['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(መዝግብ_እሴት_e0918eb0)])
        제어기들 = [እሴት for ስም, እሴት in የስርዓት_መረጃ.items() if re.fullmatch(r'storagecontrollername\d+', ስም)]
        if 'JKOROS IDE' not in 제어기들:
            self.ትእዛዝ(['VBoxManage', 'storagectl', ዞን_እሴት['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.ትእዛዝ(['VBoxManage', 'storageattach', ዞን_እሴት['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(መድረሻ_እሴት)])
        ዞን_እሴት['pending'] = False
        self.ማከማቻ_እሴት(ዞን_እሴት)
        self.ትእዛዝ(['VBoxManage', 'startvm', ዞን_እሴት['uuid'], '--type', self.ስልት_ሁነታ])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.አሳይ_ዞን()


def ማስኬጃ():
    ተንትን_እሴት = argparse.ArgumentParser(description='jkoros 전용 VirtualBox ፈጽም_ትእዛዝ 및 ዞን_እሴት መጠይቅ_እሴት')
    ተንትን_እሴት.add_argument('action', choices=['run', 'status'])
    ግቤት_ነጋሪ_እሴት = ተንትን_እሴት.parse_args()
    ፈጽም_ትእዛዝ = ፕሮግራም_የመተግበሪያ_መሳቢያ(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if ግቤት_ነጋሪ_እሴት.action == 'status':
        print(json.dumps(ፈጽም_ትእዛዝ.አሳይ_ዞን(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. አዘጋጅ_b78e430d 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/ፈቃድ_እሴት 변경은 하지 않습니다.')
    os.umask(0o077)
    ፈጽም_ትእዛዝ.መተላለፊያ('lock').parent.mkdir(parents=True, exist_ok=True)
    with ፈጽም_ትእዛዝ.መተላለፊያ('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox ፈጽም_ትእዛዝ 작업이 진행 중입니다.')
        print(json.dumps(ፈጽም_ትእዛዝ.ፈጽም_ትእዛዝ(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: ማስኬጃ()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ስህተት:
        print('VBOX ስህተት: ' + str(ስህተት), file=sys.stderr)
        sys.exit(1)
