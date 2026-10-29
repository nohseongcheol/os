#!/usr/bin/env python3
"""jkoros 전용 VirtualBox ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ. 기존 VM/디스크/ਸੰਭਾਲੋ_ਕੀਮਤ 상태는 삭제하지 않는다."""
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


def ਅਮਲ_ਕਰੋ_ਸ਼ੈਲ_ਆਦੇਸ਼(ਆਰਗੂਮੈਂਟ):
    환경 = dict(os.environ, LC_ALL='C')
    ਮਾਪ = subprocess.run([str(ਕੀਮਤ) for ਕੀਮਤ in ਆਰਗੂਮੈਂਟ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    ਤਤਕਰਾ_ਕੀਮਤ = ਮਾਪ.stdout.decode('utf-8', 'replace')
    if ਮਾਪ.returncode:
        raise 실행오류('ਕਮਾਂਡ ਅਸਫਲ_ਕੀਮਤ: ' + ' '.join(str(ਕੀਮਤ) for ਕੀਮਤ in ਆਰਗੂਮੈਂਟ) + '\n' + ਤਤਕਰਾ_ਕੀਮਤ[-10000:])
    return ਤਤਕਰਾ_ਕੀਮਤ


def ਯੋਗ_ਕੀਮਤ(ਤਤਕਰਾ_ਕੀਮਤ):
    ਮਾਪ = {}
    for ਲਾਈਨ in ਤਤਕਰਾ_ਕੀਮਤ.splitlines():
        if '=' not in ਲਾਈਨ:
            continue
        ਨਾਂ, ਕੀਮਤ = ਲਾਈਨ.split('=', 1)
        if ਨਾਂ.startswith('"'):
            ਨਾਂ = json.loads(ਨਾਂ)
        if ਕੀਮਤ.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(ਕੀਮਤ)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(ਕੀਮਤ): ਕੀਮਤ = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox ਯੋਗ_ਕੀਮਤ ਸਰੂਪ_ਕੀਮਤ ਗਲਤੀ: ' + ਲਾਈਨ)
        ਮਾਪ[ਨਾਂ] = ਕੀਮਤ
    return ਮਾਪ


def 등록목록(ਤਤਕਰਾ_ਕੀਮਤ):
    ਮਾਪ = {}
    for ਲਾਈਨ in ਤਤਕਰਾ_ਕੀਮਤ.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', ਲਾਈਨ)
        if 일치: ਮਾਪ[일치.group(2).lower()] = 일치.group(1)
    return ਮਾਪ


def 검사합(ਮਾਰਗ):
    ਕੀਮਤ = hashlib.sha256()
    with ਮਾਰਗ.open('rb') as ਫਾਇਲ:
        for ਸਮੱਗਰੀ in iter(lambda: ਫਾਇਲ.read(1024 * 1024), b''): ਕੀਮਤ.update(ਸਮੱਗਰੀ)
    return ਕੀਮਤ.hexdigest()


class ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ:
    def __init__(self, ਰੂਟ_ਕੀਮਤ, ਨਾਂ, ਮੈਥਡ_ਮੋਡ='gui', ਕਮਾਂਡ=ਅਮਲ_ਕਰੋ_ਸ਼ੈਲ_ਆਦੇਸ਼):
        self.ਰੂਟ_ਕੀਮਤ = Path(ਰੂਟ_ਕੀਮਤ).resolve()
        self.ਨਾਂ, self.ਮੈਥਡ_ਮੋਡ, self.ਕਮਾਂਡ = ਨਾਂ, ਮੈਥਡ_ਮੋਡ, ਕਮਾਂਡ
        self.보관 = self.ਰੂਟ_ਕੀਮਤ / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', ਨਾਂ) or ਨਾਂ in ('.', '..'):
            raise 실행오류('VM 이름은 문자·ਅੰਕ_ਕੀਮਤ·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if ਮੈਥਡ_ਮੋਡ not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ਮਾਰਗ(self, ਪਿਅਰ_ਕੀਮਤ):
        if Path(ਪਿਅਰ_ਕੀਮਤ).is_absolute() or '..' in Path(ਪਿਅਰ_ਕੀਮਤ).parts:
            raise 실행오류('잘못된 관리 ਮਾਰਗ: ' + str(ਪਿਅਰ_ਕੀਮਤ))
        ਮਾਪ = self.보관
        for 부분 in ['.vbox'] + list(Path(ਪਿਅਰ_ਕੀਮਤ).parts):
            if 부분 == '.vbox': ਮਾਪ = self.보관
            else: ਮਾਪ = ਮਾਪ / 부분
            if ਮਾਪ.is_symlink(): raise 실행오류('ਕੁਨੈਕਸ਼ਨ_ਕਰੋ 경로는 사용하지 않습니다: ' + str(ਮਾਪ))
        return ਮਾਪ

    def ਪੜ੍ਹਨ(self):
        ਮਾਰਗ = self.ਮਾਰਗ('state.json')
        if not ਮਾਰਗ.exists(): return None
        ਸਥਿਤੀ_ਕੀਮਤ = json.loads(ਮਾਰਗ.read_text(encoding='utf-8'))
        if ਸਥਿਤੀ_ਕੀਮਤ.get('version') != 1 or ਸਥਿਤੀ_ਕੀਮਤ.get('name') != self.ਨਾਂ:
            raise 실행오류('관리 상태의 VM ਨਾਂ/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for ਨਾਂ in ('uuid', 'owner'):
            if str(uuid.UUID(ਸਥਿਤੀ_ਕੀਮਤ[ਨਾਂ])) != ਸਥਿਤੀ_ਕੀਮਤ[ਨਾਂ]: raise 실행오류('잘못된 VM ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ_ਕੀਮਤ')
        return ਸਥਿਤੀ_ਕੀਮਤ

    def ਸੰਭਾਲੋ_ਕੀਮਤ(self, ਸਥਿਤੀ_ਕੀਮਤ):
        ਮੰਜਿਲ_ਕੀਮਤ = self.ਮਾਰਗ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as ਫਾਇਲ:
            json.dump(ਸਥਿਤੀ_ਕੀਮਤ, ਫਾਇਲ, ensure_ascii=False, indent=2)
            ਫਾਇਲ.write('\n')
            임시 = ਫਾਇਲ.name
        os.replace(임시, str(ਮੰਜਿਲ_ਕੀਮਤ))

    def ਸਿਸਟਮ_ਜਾਣਕਾਰੀ(self, ਸਥਿਤੀ_ਕੀਮਤ, 등록됨, ਮੁੜ_ਪ੍ਰਾਪਤ_ਕਰਨਾ_ਸਥਿਤੀ=False):
        if ਸਥਿਤੀ_ਕੀਮਤ['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        ਸਿਸਟਮ_ਜਾਣਕਾਰੀ = ਯੋਗ_ਕੀਮਤ(self.ਕਮਾਂਡ(['VBoxManage', 'showvminfo', ਸਥਿਤੀ_ਕੀਮਤ['uuid'], '--machinereadable']))
        ਸਥਿਤੀ = Path(ਸਿਸਟਮ_ਜਾਣਕਾਰੀ.get('CfgFile', '')).resolve()
        if self.ਮਾਰਗ('machines').resolve() not in ਸਥਿਤੀ.parents or ਸਿਸਟਮ_ਜਾਣਕਾਰੀ.get('UUID') != ਸਥਿਤੀ_ਕੀਮਤ['uuid']:
            raise 실행오류('이 프로젝트의 VM ਸੈਟਿੰਗ ਮਾਰਗ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.ਕਮਾਂਡ(['VBoxManage', 'getextradata', ਸਥਿਤੀ_ਕੀਮਤ['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + ਸਥਿਤੀ_ਕੀਮਤ['owner']:
            if ਮੁੜ_ਪ੍ਰਾਪਤ_ਕਰਨਾ_ਸਥਿਤੀ and ਸਥਿਤੀ_ਕੀਮਤ.get('pending') and 표식 == 'No value set!':
                self.ਕਮਾਂਡ(['VBoxManage', 'setextradata', ਸਥਿਤੀ_ਕੀਮਤ['uuid'], 'JKOROS/Owner', ਸਥਿਤੀ_ਕੀਮਤ['owner']])
            else:
                raise 실행오류('VM ਮਾਲਕ_ਕੀਮਤ 표식이 일치하지 않아 변경하지 않습니다.')
        return ਸਿਸਟਮ_ਜਾਣਕਾਰੀ

    def 매체검사(self, ਸਥਿਤੀ_ਕੀਮਤ, ਸਿਸਟਮ_ਜਾਣਕਾਰੀ):
        제어기들 = [ਕੀਮਤ for ਨਾਂ, ਕੀਮਤ in ਸਿਸਟਮ_ਜਾਣਕਾਰੀ.items() if re.fullmatch(r'storagecontrollername\d+', ਨਾਂ)]
        ਇਜਾਜ਼ਤ_ਦਿਉ_ਕੀਮਤ = [str(self.ਮਾਰਗ(ਕੀਮਤ)) for ਕੀਮਤ in ਸਥਿਤੀ_ਕੀਮਤ.get('media', [])]
        for ਨਾਂ, ਕੀਮਤ in ਸਿਸਟਮ_ਜਾਣਕਾਰੀ.items():
            if any(re.fullmatch(re.escape(ਕੰਟਰੋਲਰ) + r'-\d+-\d+', ਨਾਂ) for ਕੰਟਰੋਲਰ in 제어기들):
                if ਕੀਮਤ not in ('none', 'emptydrive') and ਕੀਮਤ not in ਇਜਾਜ਼ਤ_ਦਿਉ_ਕੀਮਤ:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + ਕੀਮਤ)

    def ਸ਼ੋਅ_ਸਥਿਤੀ(self):
        ਸਥਿਤੀ_ਕੀਮਤ = self.ਪੜ੍ਹਨ()
        if ਸਥਿਤੀ_ਕੀਮਤ is None: return {'name': self.ਨਾਂ, 'state': 'not-created'}
        ਸਿਸਟਮ_ਜਾਣਕਾਰੀ = self.ਸਿਸਟਮ_ਜਾਣਕਾਰੀ(ਸਥਿਤੀ_ਕੀਮਤ, 등록목록(self.ਕਮਾਂਡ(['VBoxManage', 'list', 'vms'])))
        return {'name': ਸਿਸਟਮ_ਜਾਣਕਾਰੀ.get('name', ਸਥਿਤੀ_ਕੀਮਤ['name']), 'uuid': ਸਥਿਤੀ_ਕੀਮਤ['uuid'], 'state': ਸਿਸਟਮ_ਜਾਣਕਾਰੀ.get('VMState'),
                'iso': str(self.ਮਾਰਗ(ਸਥਿਤੀ_ਕੀਮਤ['iso'])) if ਸਥਿਤੀ_ਕੀਮਤ.get('iso') else None,
                'serial_log': str(self.ਮਾਰਗ(ਸਥਿਤੀ_ਕੀਮਤ['serial_log'])) if ਸਥਿਤੀ_ਕੀਮਤ.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(self):
        ਸਥਿਤੀ_ਕੀਮਤ = self.ਪੜ੍ਹਨ()
        등록됨 = 등록목록(self.ਕਮਾਂਡ(['VBoxManage', 'list', 'vms']))
        ਸਿਸਟਮ_ਜਾਣਕਾਰੀ = None
        if ਸਥਿਤੀ_ਕੀਮਤ is not None and ਸਥਿਤੀ_ਕੀਮਤ['uuid'] in 등록됨:
            ਸਿਸਟਮ_ਜਾਣਕਾਰੀ = self.ਸਿਸਟਮ_ਜਾਣਕਾਰੀ(ਸਥਿਤੀ_ਕੀਮਤ, 등록됨, ਮੁੜ_ਪ੍ਰਾਪਤ_ਕਰਨਾ_ਸਥਿਤੀ=True)
            현재 = ਸਿਸਟਮ_ਜਾਣਕਾਰੀ.get('VMState')
            if 현재 == 'running':
                print('이미 ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ 중입니다. 재빌드·재시작하지 않습니다.')
                return self.ਸ਼ੋਅ_ਸਥਿਤੀ()
            self.매체검사(ਸਥਿਤੀ_ਕੀਮਤ, ਸਿਸਟਮ_ਜਾਣਕਾਰੀ)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 ਸੰਭਾਲੋ_ਕੀਮਤ 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.ਕਮਾਂਡ(['VBoxManage', 'controlvm', ਸਥਿਤੀ_ਕੀਮਤ['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 ਖੋਲ੍ਹੋ 전에 기존 기록도 보관한다.
                    if ਸਥਿਤੀ_ਕੀਮਤ.get('serial_log'):
                        원본 = self.ਮਾਰਗ(ਸਥਿਤੀ_ਕੀਮਤ['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ਮਾਰਗ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.ਕਮਾਂਡ(['VBoxManage', 'startvm', ਸਥਿਤੀ_ਕੀਮਤ['uuid'], '--type', self.ਮੈਥਡ_ਮੋਡ])
                return self.ਸ਼ੋਅ_ਸਥਿਤੀ()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 ਸਵਿੱਚ_ਮੋਡ 중입니다 ({}). 작업이 끝난 ਪਿਛਲਾ_ਕੀਮਤ 다시 실행하세요.'.format(현재))
        elif ਸਥਿਤੀ_ਕੀਮਤ is not None and not ਸਥਿਤੀ_ਕੀਮਤ.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.ਨਾਂ in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # ਸੰਭਾਲੋ_ਕੀਮਤ/ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.ਕਮਾਂਡ(['make', '-C', str(self.ਰੂਟ_ਕੀਮਤ / 'os'), 'iso']), end='')
        원본 = self.ਰੂਟ_ਕੀਮਤ / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        ਮੰਜਿਲ_ਕੀਮਤ = self.ਮਾਰਗ(매체)
        ਮੰਜਿਲ_ਕੀਮਤ.parent.mkdir(exist_ok=True)
        if ਮੰਜਿਲ_ਕੀਮਤ.exists():
            if 검사합(ਮੰਜਿਲ_ਕੀਮਤ) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(ਮੰਜਿਲ_ਕੀਮਤ))
        else:
            with tempfile.NamedTemporaryFile(dir=str(ਮੰਜਿਲ_ਕੀਮਤ.parent)) as ਫਾਇਲ:
                shutil.copyfile(str(원본), ਫਾਇਲ.name)
                os.link(ਫਾਇਲ.name, str(ਮੰਜਿਲ_ਕੀਮਤ))

        if ਸਥਿਤੀ_ਕੀਮਤ is None:
            ਸਥਿਤੀ_ਕੀਮਤ = {'version': 1, 'name': self.ਨਾਂ, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.ਸੰਭਾਲੋ_ਕੀਮਤ(ਸਥਿਤੀ_ਕੀਮਤ)
        if ਸਿਸਟਮ_ਜਾਣਕਾਰੀ is None:
            self.ਕਮਾਂਡ(['VBoxManage', 'createvm', '--name', ਸਥਿਤੀ_ਕੀਮਤ['name'], '--uuid', ਸਥਿਤੀ_ਕੀਮਤ['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ਮਾਰਗ('machines')), '--register'])
            self.ਕਮਾਂਡ(['VBoxManage', 'setextradata', ਸਥਿਤੀ_ਕੀਮਤ['uuid'], 'JKOROS/Owner', ਸਥਿਤੀ_ਕੀਮਤ['owner']])
        # ਬਿਲਡ_ਪਰਬੰਧ 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        ਸਿਸਟਮ_ਜਾਣਕਾਰੀ = self.ਸਿਸਟਮ_ਜਾਣਕਾਰੀ(ਸਥਿਤੀ_ਕੀਮਤ, 등록목록(self.ਕਮਾਂਡ(['VBoxManage', 'list', 'vms'])))
        if ਸਿਸਟਮ_ਜਾਣਕਾਰੀ.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('ਬਿਲਡ_ਪਰਬੰਧ 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(ਸਥਿਤੀ_ਕੀਮਤ, ਸਿਸਟਮ_ਜਾਣਕਾਰੀ)
        ਸਥਿਤੀ_ਕੀਮਤ['iso'] = 매체
        if 매체 not in ਸਥਿਤੀ_ਕੀਮਤ['media']: ਸਥਿਤੀ_ਕੀਮਤ['media'].append(매체)
        ਸਥਿਤੀ_ਕੀਮਤ['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        ਲੌਗ_ਕੀਮਤ = self.ਮਾਰਗ(ਸਥਿਤੀ_ਕੀਮਤ['serial_log'])
        ਲੌਗ_ਕੀਮਤ.parent.mkdir(exist_ok=True)
        self.ਸੰਭਾਲੋ_ਕੀਮਤ(ਸਥਿਤੀ_ਕੀਮਤ)
        self.ਕਮਾਂਡ(['VBoxManage', 'modifyvm', ਸਥਿਤੀ_ਕੀਮਤ['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(ਲੌਗ_ਕੀਮਤ)])
        제어기들 = [ਕੀਮਤ for ਨਾਂ, ਕੀਮਤ in ਸਿਸਟਮ_ਜਾਣਕਾਰੀ.items() if re.fullmatch(r'storagecontrollername\d+', ਨਾਂ)]
        if 'JKOROS IDE' not in 제어기들:
            self.ਕਮਾਂਡ(['VBoxManage', 'storagectl', ਸਥਿਤੀ_ਕੀਮਤ['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.ਕਮਾਂਡ(['VBoxManage', 'storageattach', ਸਥਿਤੀ_ਕੀਮਤ['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(ਮੰਜਿਲ_ਕੀਮਤ)])
        ਸਥਿਤੀ_ਕੀਮਤ['pending'] = False
        self.ਸੰਭਾਲੋ_ਕੀਮਤ(ਸਥਿਤੀ_ਕੀਮਤ)
        self.ਕਮਾਂਡ(['VBoxManage', 'startvm', ਸਥਿਤੀ_ਕੀਮਤ['uuid'], '--type', self.ਮੈਥਡ_ਮੋਡ])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.ਸ਼ੋਅ_ਸਥਿਤੀ()


def ਚਲਾਓ_2():
    ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ = argparse.ArgumentParser(description='jkoros 전용 VirtualBox ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ 및 ਸਥਿਤੀ_ਕੀਮਤ ਪੜਤਾਲ_ਕੀਮਤ')
    ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.add_argument('action', choices=['run', 'status'])
    인자 = ਪਦ_ਵਿਆਖਿਆ_ਕਰੋ_ਕੀਮਤ.parse_args()
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ = ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਸ਼ੋਅ_ਸਥਿਤੀ(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. ਹੋਸਟ 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/ਆਗਿਆ_ਕੀਮਤ 변경은 하지 않습니다.')
    os.umask(0o077)
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਮਾਰਗ('lock').parent.mkdir(parents=True, exist_ok=True)
    with ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਮਾਰਗ('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ 작업이 진행 중입니다.')
        print(json.dumps(ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: ਚਲਾਓ_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ਗਲਤੀ:
        print('VBOX ਗਲਤੀ: ' + str(ਗਲਤੀ), file=sys.stderr)
        sys.exit(1)
