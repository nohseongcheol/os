#!/usr/bin/env python3
"""jkoros 전용 VirtualBox መተግበሪ_ተመዛዚ_መተግበሪ. 기존 VM/디스크/ከዝን_ዋጋ 상태는 삭제하지 않는다."""
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


def ተግብር_ሽፋን_ትእዛዝ(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(ዋጋ) for ዋጋ in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    ትሕዝቶ_ዋጋ = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('ትእዛዝ ፍሽለት_ዋጋ: ' + ' '.join(str(ዋጋ) for ዋጋ in 인수) + '\n' + ትሕዝቶ_ዋጋ[-10000:])
    return ትሕዝቶ_ዋጋ


def ባህሪ_ዋጋ(ትሕዝቶ_ዋጋ):
    결과 = {}
    for መስመር in ትሕዝቶ_ዋጋ.splitlines():
        if '=' not in መስመር:
            continue
        ሽም, ዋጋ = መስመር.split('=', 1)
        if ሽም.startswith('"'):
            ሽም = json.loads(ሽም)
        if ዋጋ.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(ዋጋ)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(ዋጋ): ዋጋ = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox ባህሪ_ዋጋ ቅረጽ_ዋጋ ጌጋ: ' + መስመር)
        결과[ሽም] = ዋጋ
    return 결과


def 등록목록(ትሕዝቶ_ዋጋ):
    결과 = {}
    for መስመር in ትሕዝቶ_ዋጋ.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', መስመር)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(መገዲ):
    ዋጋ = hashlib.sha256()
    with መገዲ.open('rb') as ፋይል:
        for ሓበሬታ in iter(lambda: ፋይል.read(1024 * 1024), b''): ዋጋ.update(ሓበሬታ)
    return ዋጋ.hexdigest()


class መተግበሪ_ተመዛዚ_መተግበሪ:
    def __init__(self, 뿌리, ሽም, ሜላ_ኹነት='gui', ትእዛዝ=ተግብር_ሽፋን_ትእዛዝ):
        self.뿌리 = Path(뿌리).resolve()
        self.ሽም, self.ሜላ_ኹነት, self.ትእዛዝ = ሽም, ሜላ_ኹነት, ትእዛዝ
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', ሽም) or ሽም in ('.', '..'):
            raise 실행오류('VM 이름은 문자·ኣሃዝ_ዋጋ·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if ሜላ_ኹነት not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def መገዲ(self, መዘና_ዋጋ):
        if Path(መዘና_ዋጋ).is_absolute() or '..' in Path(መዘና_ዋጋ).parts:
            raise 실행오류('잘못된 관리 መገዲ: ' + str(መዘና_ዋጋ))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(መዘና_ዋጋ).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('ኣላግብ 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def 읽기(self):
        መገዲ = self.መገዲ('state.json')
        if not መገዲ.exists(): return None
        ደረጃ_ዋጋ = json.loads(መገዲ.read_text(encoding='utf-8'))
        if ደረጃ_ዋጋ.get('version') != 1 or ደረጃ_ዋጋ.get('name') != self.ሽም:
            raise 실행오류('관리 상태의 VM ሽም/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for ሽም in ('uuid', 'owner'):
            if str(uuid.UUID(ደረጃ_ዋጋ[ሽም])) != ደረጃ_ዋጋ[ሽም]: raise 실행오류('잘못된 VM ፈላዪ_ዋጋ_5b7b8b77')
        return ደረጃ_ዋጋ

    def ከዝን_ዋጋ(self, ደረጃ_ዋጋ):
        መዓልቦ_ዋጋ = self.መገዲ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as ፋይል:
            json.dump(ደረጃ_ዋጋ, ፋይል, ensure_ascii=False, indent=2)
            ፋይል.write('\n')
            임시 = ፋይል.name
        os.replace(임시, str(መዓልቦ_ዋጋ))

    def ናይ_ስርዓት_ሓበሬታ(self, ደረጃ_ዋጋ, 등록됨, መሊስካ_ርከብ_ደረጃ=False):
        if ደረጃ_ዋጋ['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        ናይ_ስርዓት_ሓበሬታ = ባህሪ_ዋጋ(self.ትእዛዝ(['VBoxManage', 'showvminfo', ደረጃ_ዋጋ['uuid'], '--machinereadable']))
        위치 = Path(ናይ_ስርዓት_ሓበሬታ.get('CfgFile', '')).resolve()
        if self.መገዲ('machines').resolve() not in 위치.parents or ናይ_ስርዓት_ሓበሬታ.get('UUID') != ደረጃ_ዋጋ['uuid']:
            raise 실행오류('이 프로젝트의 VM ኣቀማምጣታት መገዲ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.ትእዛዝ(['VBoxManage', 'getextradata', ደረጃ_ዋጋ['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + ደረጃ_ዋጋ['owner']:
            if መሊስካ_ርከብ_ደረጃ and ደረጃ_ዋጋ.get('pending') and 표식 == 'No value set!':
                self.ትእዛዝ(['VBoxManage', 'setextradata', ደረጃ_ዋጋ['uuid'], 'JKOROS/Owner', ደረጃ_ዋጋ['owner']])
            else:
                raise 실행오류('VM ወናኒ_ዋጋ 표식이 일치하지 않아 변경하지 않습니다.')
        return ናይ_ስርዓት_ሓበሬታ

    def ፈትሽ_መራኸቢ_ብዙሃን(self, ደረጃ_ዋጋ, ናይ_ስርዓት_ሓበሬታ):
        제어기들 = [ዋጋ for ሽም, ዋጋ in ናይ_ስርዓት_ሓበሬታ.items() if re.fullmatch(r'storagecontrollername\d+', ሽም)]
        ፍቐድ_ዋጋ = [str(self.መገዲ(ዋጋ)) for ዋጋ in ደረጃ_ዋጋ.get('media', [])]
        for ሽም, ዋጋ in ናይ_ስርዓት_ሓበሬታ.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', ሽም) for 제어기 in 제어기들):
                if ዋጋ not in ('none', 'emptydrive') and ዋጋ not in ፍቐድ_ዋጋ:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + ዋጋ)

    def ኣርእይ_ደረጃ(self):
        ደረጃ_ዋጋ = self.읽기()
        if ደረጃ_ዋጋ is None: return {'name': self.ሽም, 'state': 'not-created'}
        ናይ_ስርዓት_ሓበሬታ = self.ናይ_ስርዓት_ሓበሬታ(ደረጃ_ዋጋ, 등록목록(self.ትእዛዝ(['VBoxManage', 'list', 'vms'])))
        return {'name': ናይ_ስርዓት_ሓበሬታ.get('name', ደረጃ_ዋጋ['name']), 'uuid': ደረጃ_ዋጋ['uuid'], 'state': ናይ_ስርዓት_ሓበሬታ.get('VMState'),
                'iso': str(self.መገዲ(ደረጃ_ዋጋ['iso'])) if ደረጃ_ዋጋ.get('iso') else None,
                'serial_log': str(self.መገዲ(ደረጃ_ዋጋ['serial_log'])) if ደረጃ_ዋጋ.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def ተግብር_ትእዛዝ(self):
        ደረጃ_ዋጋ = self.읽기()
        등록됨 = 등록목록(self.ትእዛዝ(['VBoxManage', 'list', 'vms']))
        ናይ_ስርዓት_ሓበሬታ = None
        if ደረጃ_ዋጋ is not None and ደረጃ_ዋጋ['uuid'] in 등록됨:
            ናይ_ስርዓት_ሓበሬታ = self.ናይ_ስርዓት_ሓበሬታ(ደረጃ_ዋጋ, 등록됨, መሊስካ_ርከብ_ደረጃ=True)
            현재 = ናይ_ስርዓት_ሓበሬታ.get('VMState')
            if 현재 == 'running':
                print('이미 ተግብር_ትእዛዝ 중입니다. 재빌드·재시작하지 않습니다.')
                return self.ኣርእይ_ደረጃ()
            self.ፈትሽ_መራኸቢ_ብዙሃን(ደረጃ_ዋጋ, ናይ_ስርዓት_ሓበሬታ)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 ከዝን_ዋጋ 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.ትእዛዝ(['VBoxManage', 'controlvm', ደረጃ_ዋጋ['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 ክፈት 전에 기존 기록도 보관한다.
                    if ደረጃ_ዋጋ.get('serial_log'):
                        원본 = self.መገዲ(ደረጃ_ዋጋ['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.መገዲ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.ትእዛዝ(['VBoxManage', 'startvm', ደረጃ_ዋጋ['uuid'], '--type', self.ሜላ_ኹነት])
                return self.ኣርእይ_ደረጃ()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 ቀይር_ኹነት 중입니다 ({}). 작업이 끝난 ድሕሪት_ዋጋ 다시 실행하세요.'.format(현재))
        elif ደረጃ_ዋጋ is not None and not ደረጃ_ዋጋ.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.ሽም in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # ከዝን_ዋጋ/ተግብር_ትእዛዝ 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.ትእዛዝ(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        መራኸቢ_ብዙሃን_ዋጋ = 'media/kernel-' + 검사합(원본) + '.iso'
        መዓልቦ_ዋጋ = self.መገዲ(መራኸቢ_ብዙሃን_ዋጋ)
        መዓልቦ_ዋጋ.parent.mkdir(exist_ok=True)
        if መዓልቦ_ዋጋ.exists():
            if 검사합(መዓልቦ_ዋጋ) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(መዓልቦ_ዋጋ))
        else:
            with tempfile.NamedTemporaryFile(dir=str(መዓልቦ_ዋጋ.parent)) as ፋይል:
                shutil.copyfile(str(원본), ፋይል.name)
                os.link(ፋይል.name, str(መዓልቦ_ዋጋ))

        if ደረጃ_ዋጋ is None:
            ደረጃ_ዋጋ = {'version': 1, 'name': self.ሽም, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.ከዝን_ዋጋ(ደረጃ_ዋጋ)
        if ናይ_ስርዓት_ሓበሬታ is None:
            self.ትእዛዝ(['VBoxManage', 'createvm', '--name', ደረጃ_ዋጋ['name'], '--uuid', ደረጃ_ዋጋ['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.መገዲ('machines')), '--register'])
            self.ትእዛዝ(['VBoxManage', 'setextradata', ደረጃ_ዋጋ['uuid'], 'JKOROS/Owner', ደረጃ_ዋጋ['owner']])
        # ህነጽ_ስርዓት 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        ናይ_ስርዓት_ሓበሬታ = self.ናይ_ስርዓት_ሓበሬታ(ደረጃ_ዋጋ, 등록목록(self.ትእዛዝ(['VBoxManage', 'list', 'vms'])))
        if ናይ_ስርዓት_ሓበሬታ.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('ህነጽ_ስርዓት 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.ፈትሽ_መራኸቢ_ብዙሃን(ደረጃ_ዋጋ, ናይ_ስርዓት_ሓበሬታ)
        ደረጃ_ዋጋ['iso'] = መራኸቢ_ብዙሃን_ዋጋ
        if መራኸቢ_ብዙሃን_ዋጋ not in ደረጃ_ዋጋ['media']: ደረጃ_ዋጋ['media'].append(መራኸቢ_ብዙሃን_ዋጋ)
        ደረጃ_ዋጋ['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        ምዝጉብ_ዋጋ = self.መገዲ(ደረጃ_ዋጋ['serial_log'])
        ምዝጉብ_ዋጋ.parent.mkdir(exist_ok=True)
        self.ከዝን_ዋጋ(ደረጃ_ዋጋ)
        self.ትእዛዝ(['VBoxManage', 'modifyvm', ደረጃ_ዋጋ['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(ምዝጉብ_ዋጋ)])
        제어기들 = [ዋጋ for ሽም, ዋጋ in ናይ_ስርዓት_ሓበሬታ.items() if re.fullmatch(r'storagecontrollername\d+', ሽም)]
        if 'JKOROS IDE' not in 제어기들:
            self.ትእዛዝ(['VBoxManage', 'storagectl', ደረጃ_ዋጋ['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.ትእዛዝ(['VBoxManage', 'storageattach', ደረጃ_ዋጋ['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(መዓልቦ_ዋጋ)])
        ደረጃ_ዋጋ['pending'] = False
        self.ከዝን_ዋጋ(ደረጃ_ዋጋ)
        self.ትእዛዝ(['VBoxManage', 'startvm', ደረጃ_ዋጋ['uuid'], '--type', self.ሜላ_ኹነት])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.ኣርእይ_ደረጃ()


def ኣኺድ():
    해석 = argparse.ArgumentParser(description='jkoros 전용 VirtualBox ተግብር_ትእዛዝ 및 ደረጃ_ዋጋ ሕቶ_ዋጋ')
    해석.add_argument('action', choices=['run', 'status'])
    인자 = 해석.parse_args()
    ተግብር_ትእዛዝ = መተግበሪ_ተመዛዚ_መተግበሪ(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(ተግብር_ትእዛዝ.ኣርእይ_ደረጃ(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. አዐንግድ 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/ፍቓድ_ዋጋ 변경은 하지 않습니다.')
    os.umask(0o077)
    ተግብር_ትእዛዝ.መገዲ('lock').parent.mkdir(parents=True, exist_ok=True)
    with ተግብር_ትእዛዝ.መገዲ('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox ተግብር_ትእዛዝ 작업이 진행 중입니다.')
        print(json.dumps(ተግብር_ትእዛዝ.ተግብር_ትእዛዝ(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: ኣኺድ()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ጌጋ:
        print('VBOX ጌጋ: ' + str(ጌጋ), file=sys.stderr)
        sys.exit(1)
