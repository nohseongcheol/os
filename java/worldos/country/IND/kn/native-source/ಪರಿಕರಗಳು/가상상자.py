#!/usr/bin/env python3
"""jkoros 전용 VirtualBox ಅಪ್ಲಿ_ಲಾಂಚರ್. 기존 VM/디스크/ಸ್ಟೋರ್_ಮೌಲ್ಯ 상태는 삭제하지 않는다."""
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


def ಪೂರೈಸು_ಶೆಲ್_ಆದೇಶ(인수):
    환경 = dict(os.environ, LC_ALL='C')
    ಮಾಪನ = subprocess.run([str(ಮೌಲ್ಯ) for ಮೌಲ್ಯ in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    ವಿಷಯ_ಮೌಲ್ಯ = ಮಾಪನ.stdout.decode('utf-8', 'replace')
    if ಮಾಪನ.returncode:
        raise 실행오류('ಆಜ್ಞೆ ವೈಫಲ್ಯ_ಮೌಲ್ಯ: ' + ' '.join(str(ಮೌಲ್ಯ) for ಮೌಲ್ಯ in 인수) + '\n' + ವಿಷಯ_ಮೌಲ್ಯ[-10000:])
    return ವಿಷಯ_ಮೌಲ್ಯ


def ವಿಶೇಷಣ_ಮೌಲ್ಯ(ವಿಷಯ_ಮೌಲ್ಯ):
    ಮಾಪನ = {}
    for ಸಾಲು in ವಿಷಯ_ಮೌಲ್ಯ.splitlines():
        if '=' not in ಸಾಲು:
            continue
        ಹೆಸರು, ಮೌಲ್ಯ = ಸಾಲು.split('=', 1)
        if ಹೆಸರು.startswith('"'):
            ಹೆಸರು = json.loads(ಹೆಸರು)
        if ಮೌಲ್ಯ.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(ಮೌಲ್ಯ)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(ಮೌಲ್ಯ): ಮೌಲ್ಯ = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox ವಿಶೇಷಣ_ಮೌಲ್ಯ ಸ್ವರೂಪ_ಮೌಲ್ಯ ದೋಷ: ' + ಸಾಲು)
        ಮಾಪನ[ಹೆಸರು] = ಮೌಲ್ಯ
    return ಮಾಪನ


def 등록목록(ವಿಷಯ_ಮೌಲ್ಯ):
    ಮಾಪನ = {}
    for ಸಾಲು in ವಿಷಯ_ಮೌಲ್ಯ.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', ಸಾಲು)
        if 일치: ಮಾಪನ[일치.group(2).lower()] = 일치.group(1)
    return ಮಾಪನ


def 검사합(ಮಾರ್ಗ):
    ಮೌಲ್ಯ = hashlib.sha256()
    with ಮಾರ್ಗ.open('rb') as ಕಡತ:
        for ಡೇಟಾ in iter(lambda: ಕಡತ.read(1024 * 1024), b''): ಮೌಲ್ಯ.update(ಡೇಟಾ)
    return ಮೌಲ್ಯ.hexdigest()


class ಅಪ್ಲಿ_ಲಾಂಚರ್:
    def __init__(self, ಮೂಲ_ಮೌಲ್ಯ, ಹೆಸರು, ವಿಧಾನ_ಮೋಡ್='gui', ಆಜ್ಞೆ=ಪೂರೈಸು_ಶೆಲ್_ಆದೇಶ):
        self.ಮೂಲ_ಮೌಲ್ಯ = Path(ಮೂಲ_ಮೌಲ್ಯ).resolve()
        self.ಹೆಸರು, self.ವಿಧಾನ_ಮೋಡ್, self.ಆಜ್ಞೆ = ಹೆಸರು, ವಿಧಾನ_ಮೋಡ್, ಆಜ್ಞೆ
        self.보관 = self.ಮೂಲ_ಮೌಲ್ಯ / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', ಹೆಸರು) or ಹೆಸರು in ('.', '..'):
            raise 실행오류('VM 이름은 문자·ಅಂಕೆ_ಮೌಲ್ಯ·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if ವಿಧಾನ_ಮೋಡ್ not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ಮಾರ್ಗ(self, ಪೀರ್_ಮೌಲ್ಯ):
        if Path(ಪೀರ್_ಮೌಲ್ಯ).is_absolute() or '..' in Path(ಪೀರ್_ಮೌಲ್ಯ).parts:
            raise 실행오류('잘못된 관리 ಮಾರ್ಗ: ' + str(ಪೀರ್_ಮೌಲ್ಯ))
        ಮಾಪನ = self.보관
        for 부분 in ['.vbox'] + list(Path(ಪೀರ್_ಮೌಲ್ಯ).parts):
            if 부분 == '.vbox': ಮಾಪನ = self.보관
            else: ಮಾಪನ = ಮಾಪನ / 부분
            if ಮಾಪನ.is_symlink(): raise 실행오류('ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು 경로는 사용하지 않습니다: ' + str(ಮಾಪನ))
        return ಮಾಪನ

    def ಓದು(self):
        ಮಾರ್ಗ = self.ಮಾರ್ಗ('state.json')
        if not ಮಾರ್ಗ.exists(): return None
        ಸ್ಥಿತಿ_ಮೌಲ್ಯ = json.loads(ಮಾರ್ಗ.read_text(encoding='utf-8'))
        if ಸ್ಥಿತಿ_ಮೌಲ್ಯ.get('version') != 1 or ಸ್ಥಿತಿ_ಮೌಲ್ಯ.get('name') != self.ಹೆಸರು:
            raise 실행오류('관리 상태의 VM ಹೆಸರು/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for ಹೆಸರು in ('uuid', 'owner'):
            if str(uuid.UUID(ಸ್ಥಿತಿ_ಮೌಲ್ಯ[ಹೆಸರು])) != ಸ್ಥಿತಿ_ಮೌಲ್ಯ[ಹೆಸರು]: raise 실행오류('잘못된 VM ಗುರುತಿಸುವಿಕೆ_ಮೌಲ್ಯ')
        return ಸ್ಥಿತಿ_ಮೌಲ್ಯ

    def ಸ್ಟೋರ್_ಮೌಲ್ಯ(self, ಸ್ಥಿತಿ_ಮೌಲ್ಯ):
        ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ = self.ಮಾರ್ಗ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as ಕಡತ:
            json.dump(ಸ್ಥಿತಿ_ಮೌಲ್ಯ, ಕಡತ, ensure_ascii=False, indent=2)
            ಕಡತ.write('\n')
            임시 = ಕಡತ.name
        os.replace(임시, str(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ))

    def ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ(self, ಸ್ಥಿತಿ_ಮೌಲ್ಯ, 등록됨, ಮರಳಿಪಡೆ_ಸ್ಥಿತಿ=False):
        if ಸ್ಥಿತಿ_ಮೌಲ್ಯ['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ = ವಿಶೇಷಣ_ಮೌಲ್ಯ(self.ಆಜ್ಞೆ(['VBoxManage', 'showvminfo', ಸ್ಥಿತಿ_ಮೌಲ್ಯ['uuid'], '--machinereadable']))
        ಸ್ಥಾನ = Path(ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ.get('CfgFile', '')).resolve()
        if self.ಮಾರ್ಗ('machines').resolve() not in ಸ್ಥಾನ.parents or ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ.get('UUID') != ಸ್ಥಿತಿ_ಮೌಲ್ಯ['uuid']:
            raise 실행오류('이 프로젝트의 VM ಸಿದ್ಧತೆಗಳು ಮಾರ್ಗ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.ಆಜ್ಞೆ(['VBoxManage', 'getextradata', ಸ್ಥಿತಿ_ಮೌಲ್ಯ['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + ಸ್ಥಿತಿ_ಮೌಲ್ಯ['owner']:
            if ಮರಳಿಪಡೆ_ಸ್ಥಿತಿ and ಸ್ಥಿತಿ_ಮೌಲ್ಯ.get('pending') and 표식 == 'No value set!':
                self.ಆಜ್ಞೆ(['VBoxManage', 'setextradata', ಸ್ಥಿತಿ_ಮೌಲ್ಯ['uuid'], 'JKOROS/Owner', ಸ್ಥಿತಿ_ಮೌಲ್ಯ['owner']])
            else:
                raise 실행오류('VM ಮಾಲೀಕ_ಮೌಲ್ಯ 표식이 일치하지 않아 변경하지 않습니다.')
        return ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ

    def 매체검사(self, ಸ್ಥಿತಿ_ಮೌಲ್ಯ, ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ):
        제어기들 = [ಮೌಲ್ಯ for ಹೆಸರು, ಮೌಲ್ಯ in ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ.items() if re.fullmatch(r'storagecontrollername\d+', ಹೆಸರು)]
        ಅನುಮತಿಸು_ಮೌಲ್ಯ = [str(self.ಮಾರ್ಗ(ಮೌಲ್ಯ)) for ಮೌಲ್ಯ in ಸ್ಥಿತಿ_ಮೌಲ್ಯ.get('media', [])]
        for ಹೆಸರು, ಮೌಲ್ಯ in ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ.items():
            if any(re.fullmatch(re.escape(ನಿಯಂತ್ರಕ) + r'-\d+-\d+', ಹೆಸರು) for ನಿಯಂತ್ರಕ in 제어기들):
                if ಮೌಲ್ಯ not in ('none', 'emptydrive') and ಮೌಲ್ಯ not in ಅನುಮತಿಸು_ಮೌಲ್ಯ:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + ಮೌಲ್ಯ)

    def ಶೋ_ಸ್ಥಿತಿ(self):
        ಸ್ಥಿತಿ_ಮೌಲ್ಯ = self.ಓದು()
        if ಸ್ಥಿತಿ_ಮೌಲ್ಯ is None: return {'name': self.ಹೆಸರು, 'state': 'not-created'}
        ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ = self.ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ(ಸ್ಥಿತಿ_ಮೌಲ್ಯ, 등록목록(self.ಆಜ್ಞೆ(['VBoxManage', 'list', 'vms'])))
        return {'name': ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ.get('name', ಸ್ಥಿತಿ_ಮೌಲ್ಯ['name']), 'uuid': ಸ್ಥಿತಿ_ಮೌಲ್ಯ['uuid'], 'state': ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ.get('VMState'),
                'iso': str(self.ಮಾರ್ಗ(ಸ್ಥಿತಿ_ಮೌಲ್ಯ['iso'])) if ಸ್ಥಿತಿ_ಮೌಲ್ಯ.get('iso') else None,
                'serial_log': str(self.ಮಾರ್ಗ(ಸ್ಥಿತಿ_ಮೌಲ್ಯ['serial_log'])) if ಸ್ಥಿತಿ_ಮೌಲ್ಯ.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def ಪೂರೈಸು_ಆದೇಶ(self):
        ಸ್ಥಿತಿ_ಮೌಲ್ಯ = self.ಓದು()
        등록됨 = 등록목록(self.ಆಜ್ಞೆ(['VBoxManage', 'list', 'vms']))
        ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ = None
        if ಸ್ಥಿತಿ_ಮೌಲ್ಯ is not None and ಸ್ಥಿತಿ_ಮೌಲ್ಯ['uuid'] in 등록됨:
            ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ = self.ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ(ಸ್ಥಿತಿ_ಮೌಲ್ಯ, 등록됨, ಮರಳಿಪಡೆ_ಸ್ಥಿತಿ=True)
            현재 = ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ.get('VMState')
            if 현재 == 'running':
                print('이미 ಪೂರೈಸು_ಆದೇಶ 중입니다. 재빌드·재시작하지 않습니다.')
                return self.ಶೋ_ಸ್ಥಿತಿ()
            self.매체검사(ಸ್ಥಿತಿ_ಮೌಲ್ಯ, ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 ಸ್ಟೋರ್_ಮೌಲ್ಯ 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.ಆಜ್ಞೆ(['VBoxManage', 'controlvm', ಸ್ಥಿತಿ_ಮೌಲ್ಯ['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 ತೆರೆ 전에 기존 기록도 보관한다.
                    if ಸ್ಥಿತಿ_ಮೌಲ್ಯ.get('serial_log'):
                        원본 = self.ಮಾರ್ಗ(ಸ್ಥಿತಿ_ಮೌಲ್ಯ['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ಮಾರ್ಗ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.ಆಜ್ಞೆ(['VBoxManage', 'startvm', ಸ್ಥಿತಿ_ಮೌಲ್ಯ['uuid'], '--type', self.ವಿಧಾನ_ಮೋಡ್])
                return self.ಶೋ_ಸ್ಥಿತಿ()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 ಸ್ವಿಚ್_ಮಾಡಿ_ಮೋಡ್ 중입니다 ({}). 작업이 끝난 ಹಿಂದೆ_ಮೌಲ್ಯ 다시 실행하세요.'.format(현재))
        elif ಸ್ಥಿತಿ_ಮೌಲ್ಯ is not None and not ಸ್ಥಿತಿ_ಮೌಲ್ಯ.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.ಹೆಸರು in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # ಸ್ಟೋರ್_ಮೌಲ್ಯ/ಪೂರೈಸು_ಆದೇಶ 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.ಆಜ್ಞೆ(['make', '-C', str(self.ಮೂಲ_ಮೌಲ್ಯ / 'os'), 'iso']), end='')
        원본 = self.ಮೂಲ_ಮೌಲ್ಯ / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ = self.ಮಾರ್ಗ(매체)
        ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ.parent.mkdir(exist_ok=True)
        if ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ.exists():
            if 검사합(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ))
        else:
            with tempfile.NamedTemporaryFile(dir=str(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ.parent)) as ಕಡತ:
                shutil.copyfile(str(원본), ಕಡತ.name)
                os.link(ಕಡತ.name, str(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ))

        if ಸ್ಥಿತಿ_ಮೌಲ್ಯ is None:
            ಸ್ಥಿತಿ_ಮೌಲ್ಯ = {'version': 1, 'name': self.ಹೆಸರು, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.ಸ್ಟೋರ್_ಮೌಲ್ಯ(ಸ್ಥಿತಿ_ಮೌಲ್ಯ)
        if ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ is None:
            self.ಆಜ್ಞೆ(['VBoxManage', 'createvm', '--name', ಸ್ಥಿತಿ_ಮೌಲ್ಯ['name'], '--uuid', ಸ್ಥಿತಿ_ಮೌಲ್ಯ['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ಮಾರ್ಗ('machines')), '--register'])
            self.ಆಜ್ಞೆ(['VBoxManage', 'setextradata', ಸ್ಥಿತಿ_ಮೌಲ್ಯ['uuid'], 'JKOROS/Owner', ಸ್ಥಿತಿ_ಮೌಲ್ಯ['owner']])
        # ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ = self.ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ(ಸ್ಥಿತಿ_ಮೌಲ್ಯ, 등록목록(self.ಆಜ್ಞೆ(['VBoxManage', 'list', 'vms'])))
        if ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(ಸ್ಥಿತಿ_ಮೌಲ್ಯ, ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ)
        ಸ್ಥಿತಿ_ಮೌಲ್ಯ['iso'] = 매체
        if 매체 not in ಸ್ಥಿತಿ_ಮೌಲ್ಯ['media']: ಸ್ಥಿತಿ_ಮೌಲ್ಯ['media'].append(매체)
        ಸ್ಥಿತಿ_ಮೌಲ್ಯ['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        ಲಾಗ್_ಮೌಲ್ಯ = self.ಮಾರ್ಗ(ಸ್ಥಿತಿ_ಮೌಲ್ಯ['serial_log'])
        ಲಾಗ್_ಮೌಲ್ಯ.parent.mkdir(exist_ok=True)
        self.ಸ್ಟೋರ್_ಮೌಲ್ಯ(ಸ್ಥಿತಿ_ಮೌಲ್ಯ)
        self.ಆಜ್ಞೆ(['VBoxManage', 'modifyvm', ಸ್ಥಿತಿ_ಮೌಲ್ಯ['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(ಲಾಗ್_ಮೌಲ್ಯ)])
        제어기들 = [ಮೌಲ್ಯ for ಹೆಸರು, ಮೌಲ್ಯ in ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ.items() if re.fullmatch(r'storagecontrollername\d+', ಹೆಸರು)]
        if 'JKOROS IDE' not in 제어기들:
            self.ಆಜ್ಞೆ(['VBoxManage', 'storagectl', ಸ್ಥಿತಿ_ಮೌಲ್ಯ['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.ಆಜ್ಞೆ(['VBoxManage', 'storageattach', ಸ್ಥಿತಿ_ಮೌಲ್ಯ['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ)])
        ಸ್ಥಿತಿ_ಮೌಲ್ಯ['pending'] = False
        self.ಸ್ಟೋರ್_ಮೌಲ್ಯ(ಸ್ಥಿತಿ_ಮೌಲ್ಯ)
        self.ಆಜ್ಞೆ(['VBoxManage', 'startvm', ಸ್ಥಿತಿ_ಮೌಲ್ಯ['uuid'], '--type', self.ವಿಧಾನ_ಮೋಡ್])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.ಶೋ_ಸ್ಥಿತಿ()


def ಚಲಾಯಿಸು_2():
    ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ = argparse.ArgumentParser(description='jkoros 전용 VirtualBox ಪೂರೈಸು_ಆದೇಶ 및 ಸ್ಥಿತಿ_ಮೌಲ್ಯ ಪ್ರಶ್ನಾವಳಿ_ಮೌಲ್ಯ')
    ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.add_argument('action', choices=['run', 'status'])
    ಪ್ಯಾರಾಮೀಟರ್_ವಾದ = ಪಾರ್ಸ್_ಮಾಡಿ_ಮೌಲ್ಯ.parse_args()
    ಪೂರೈಸು_ಆದೇಶ = ಅಪ್ಲಿ_ಲಾಂಚರ್(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.action == 'status':
        print(json.dumps(ಪೂರೈಸು_ಆದೇಶ.ಶೋ_ಸ್ಥಿತಿ(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. ಹೋಸ್ಟ್ 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/ಅನುಮತಿ_ಮೌಲ್ಯ 변경은 하지 않습니다.')
    os.umask(0o077)
    ಪೂರೈಸು_ಆದೇಶ.ಮಾರ್ಗ('lock').parent.mkdir(parents=True, exist_ok=True)
    with ಪೂರೈಸು_ಆದೇಶ.ಮಾರ್ಗ('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox ಪೂರೈಸು_ಆದೇಶ 작업이 진행 중입니다.')
        print(json.dumps(ಪೂರೈಸು_ಆದೇಶ.ಪೂರೈಸು_ಆದೇಶ(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: ಚಲಾಯಿಸು_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ದೋಷ:
        print('VBOX ದೋಷ: ' + str(ದೋಷ), file=sys.stderr)
        sys.exit(1)
