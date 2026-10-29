#!/usr/bin/env python3
"""jkoros 전용 VirtualBox ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍. 기존 VM/디스크/ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ 상태는 삭제하지 않는다."""
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


def ନିର୍ବାହ_କରିବା_ଖୋଳ_ନିର୍ଦ୍ଦେଶ(인수):
    환경 = dict(os.environ, LC_ALL='C')
    ମାପ = subprocess.run([str(ମୂଲ୍ୟ) for ମୂଲ୍ୟ in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    ବିଷୟ_ମୂଲ୍ୟ = ମାପ.stdout.decode('utf-8', 'replace')
    if ମାପ.returncode:
        raise 실행오류('ନିର୍ଦ୍ଦେଶ ବିଫଳତା_ମୂଲ୍ୟ: ' + ' '.join(str(ମୂଲ୍ୟ) for ମୂଲ୍ୟ in 인수) + '\n' + ବିଷୟ_ମୂଲ୍ୟ[-10000:])
    return ବିଷୟ_ମୂଲ୍ୟ


def ଗୁଣ_ମୂଲ୍ୟ(ବିଷୟ_ମୂଲ୍ୟ):
    ମାପ = {}
    for ରେଖା in ବିଷୟ_ମୂଲ୍ୟ.splitlines():
        if '=' not in ରେଖା:
            continue
        ନାମ, ମୂଲ୍ୟ = ରେଖା.split('=', 1)
        if ନାମ.startswith('"'):
            ନାମ = json.loads(ନାମ)
        if ମୂଲ୍ୟ.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(ମୂଲ୍ୟ)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(ମୂଲ୍ୟ): ମୂଲ୍ୟ = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox ଗୁଣ_ମୂଲ୍ୟ ଫର୍ମାଟ୍_ମୂଲ୍ୟ ତ୍ରୁଟି: ' + ରେଖା)
        ମାପ[ନାମ] = ମୂଲ୍ୟ
    return ମାପ


def 등록목록(ବିଷୟ_ମୂଲ୍ୟ):
    ମାପ = {}
    for ରେଖା in ବିଷୟ_ମୂଲ୍ୟ.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', ରେଖା)
        if 일치: ମାପ[일치.group(2).lower()] = 일치.group(1)
    return ମାପ


def ଚେକସୁମ୍(ପଥ):
    ମୂଲ୍ୟ = hashlib.sha256()
    with ପଥ.open('rb') as ଫାଇଲ:
        for ଡାଟା in iter(lambda: ଫାଇଲ.read(1024 * 1024), b''): ମୂଲ୍ୟ.update(ଡାଟା)
    return ମୂଲ୍ୟ.hexdigest()


class ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍:
    def __init__(self, ରୁଟ୍_ମୂଲ୍ୟ, ନାମ, ପଦ୍ଧତି_ମୋଡ୍='gui', ନିର୍ଦ୍ଦେଶ=ନିର୍ବାହ_କରିବା_ଖୋଳ_ନିର୍ଦ୍ଦେଶ):
        self.ରୁଟ୍_ମୂଲ୍ୟ = Path(ରୁଟ୍_ମୂଲ୍ୟ).resolve()
        self.ନାମ, self.ପଦ୍ଧତି_ମୋଡ୍, self.ନିର୍ଦ୍ଦେଶ = ନାମ, ପଦ୍ଧତି_ମୋଡ୍, ନିର୍ଦ୍ଦେଶ
        self.보관 = self.ରୁଟ୍_ମୂଲ୍ୟ / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', ନାମ) or ନାମ in ('.', '..'):
            raise 실행오류('VM 이름은 문자·ଅଙ୍କ_ମୂଲ୍ୟ·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if ପଦ୍ଧତି_ମୋଡ୍ not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ପଥ(self, ସମକକ୍ଷ_ମୂଲ୍ୟ):
        if Path(ସମକକ୍ଷ_ମୂଲ୍ୟ).is_absolute() or '..' in Path(ସମକକ୍ଷ_ମୂଲ୍ୟ).parts:
            raise 실행오류('잘못된 관리 ପଥ: ' + str(ସମକକ୍ଷ_ମୂଲ୍ୟ))
        ମାପ = self.보관
        for 부분 in ['.vbox'] + list(Path(ସମକକ୍ଷ_ମୂଲ୍ୟ).parts):
            if 부분 == '.vbox': ମାପ = self.보관
            else: ମାପ = ମାପ / 부분
            if ମାପ.is_symlink(): raise 실행오류('ସଂଯୋଗ_କରନ୍ତୁ 경로는 사용하지 않습니다: ' + str(ମାପ))
        return ମାପ

    def ପଢନ୍ତୁ(self):
        ପଥ = self.ପଥ('state.json')
        if not ପଥ.exists(): return None
        ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 = json.loads(ପଥ.read_text(encoding='utf-8'))
        if ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.get('version') != 1 or ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.get('name') != self.ନାମ:
            raise 실행오류('관리 상태의 VM ନାମ/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for ନାମ in ('uuid', 'owner'):
            if str(uuid.UUID(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1[ନାମ])) != ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1[ନାମ]: raise 실행오류('잘못된 VM ପରିଚାୟକ_ମୂଲ୍ୟ')
        return ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1

    def ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ(self, ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1):
        ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ = self.ପଥ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as ଫାଇଲ:
            json.dump(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1, ଫାଇଲ, ensure_ascii=False, indent=2)
            ଫାଇଲ.write('\n')
            임시 = ଫାଇଲ.name
        os.replace(임시, str(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ))

    def ସିଷ୍ଟମ୍_ସୂଚନା(self, ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1, 등록됨, ପୁନଃଉଦ୍ଧାର_କରିବା_ସ୍ଥିତି=False):
        if ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        ସିଷ୍ଟମ୍_ସୂଚନା = ଗୁଣ_ମୂଲ୍ୟ(self.ନିର୍ଦ୍ଦେଶ(['VBoxManage', 'showvminfo', ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['uuid'], '--machinereadable']))
        ଅବସ୍ଥାନ = Path(ସିଷ୍ଟମ୍_ସୂଚନା.get('CfgFile', '')).resolve()
        if self.ପଥ('machines').resolve() not in ଅବସ୍ଥାନ.parents or ସିଷ୍ଟମ୍_ସୂଚନା.get('UUID') != ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['uuid']:
            raise 실행오류('이 프로젝트의 VM ବିନ୍ଯାସ ପଥ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.ନିର୍ଦ୍ଦେଶ(['VBoxManage', 'getextradata', ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['owner']:
            if ପୁନଃଉଦ୍ଧାର_କରିବା_ସ୍ଥିତି and ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.get('pending') and 표식 == 'No value set!':
                self.ନିର୍ଦ୍ଦେଶ(['VBoxManage', 'setextradata', ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['uuid'], 'JKOROS/Owner', ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['owner']])
            else:
                raise 실행오류('VM ମାଲିକ_ମୂଲ୍ୟ 표식이 일치하지 않아 변경하지 않습니다.')
        return ସିଷ୍ଟମ୍_ସୂଚନା

    def 매체검사(self, ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1, ସିଷ୍ଟମ୍_ସୂଚନା):
        제어기들 = [ମୂଲ୍ୟ for ନାମ, ମୂଲ୍ୟ in ସିଷ୍ଟମ୍_ସୂଚନା.items() if re.fullmatch(r'storagecontrollername\d+', ନାମ)]
        ମଞ୍ଜୁର_ମୂଲ୍ୟ = [str(self.ପଥ(ମୂଲ୍ୟ)) for ମୂଲ୍ୟ in ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.get('media', [])]
        for ନାମ, ମୂଲ୍ୟ in ସିଷ୍ଟମ୍_ସୂଚନା.items():
            if any(re.fullmatch(re.escape(ନିୟନ୍ତ୍ରକ) + r'-\d+-\d+', ନାମ) for ନିୟନ୍ତ୍ରକ in 제어기들):
                if ମୂଲ୍ୟ not in ('none', 'emptydrive') and ମୂଲ୍ୟ not in ମଞ୍ଜୁର_ମୂଲ୍ୟ:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + ମୂଲ୍ୟ)

    def ପ୍ରଦର୍ଶନ_କରିବା_ସ୍ଥିତି(self):
        ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 = self.ପଢନ୍ତୁ()
        if ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 is None: return {'name': self.ନାମ, 'state': 'not-created'}
        ସିଷ୍ଟମ୍_ସୂଚନା = self.ସିଷ୍ଟମ୍_ସୂଚନା(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1, 등록목록(self.ନିର୍ଦ୍ଦେଶ(['VBoxManage', 'list', 'vms'])))
        return {'name': ସିଷ୍ଟମ୍_ସୂଚନା.get('name', ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['name']), 'uuid': ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['uuid'], 'state': ସିଷ୍ଟମ୍_ସୂଚନା.get('VMState'),
                'iso': str(self.ପଥ(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['iso'])) if ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.get('iso') else None,
                'serial_log': str(self.ପଥ(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['serial_log'])) if ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(self):
        ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 = self.ପଢନ୍ତୁ()
        등록됨 = 등록목록(self.ନିର୍ଦ୍ଦେଶ(['VBoxManage', 'list', 'vms']))
        ସିଷ୍ଟମ୍_ସୂଚନା = None
        if ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 is not None and ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['uuid'] in 등록됨:
            ସିଷ୍ଟମ୍_ସୂଚନା = self.ସିଷ୍ଟମ୍_ସୂଚନା(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1, 등록됨, ପୁନଃଉଦ୍ଧାର_କରିବା_ସ୍ଥିତି=True)
            현재 = ସିଷ୍ଟମ୍_ସୂଚନା.get('VMState')
            if 현재 == 'running':
                print('이미 ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ 중입니다. 재빌드·재시작하지 않습니다.')
                return self.ପ୍ରଦର୍ଶନ_କରିବା_ସ୍ଥିତି()
            self.매체검사(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1, ସିଷ୍ଟମ୍_ସୂଚନା)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.ନିର୍ଦ୍ଦେଶ(['VBoxManage', 'controlvm', ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 ଖୋଲନ୍ତୁ 전에 기존 기록도 보관한다.
                    if ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.get('serial_log'):
                        원본 = self.ପଥ(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ପଥ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.ନିର୍ଦ୍ଦେଶ(['VBoxManage', 'startvm', ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['uuid'], '--type', self.ପଦ୍ଧତି_ମୋଡ୍])
                return self.ପ୍ରଦର୍ଶନ_କରିବା_ସ୍ଥିତି()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 ସୁଇଚ୍_ମୋଡ୍ 중입니다 ({}). 작업이 끝난 ପଛ_ମୂଲ୍ୟ 다시 실행하세요.'.format(현재))
        elif ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 is not None and not ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.ନାମ in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ/ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.ନିର୍ଦ୍ଦେଶ(['make', '-C', str(self.ରୁଟ୍_ମୂଲ୍ୟ / 'os'), 'iso']), end='')
        원본 = self.ରୁଟ୍_ମୂଲ୍ୟ / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + ଚେକସୁମ୍(원본) + '.iso'
        ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ = self.ପଥ(매체)
        ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ.parent.mkdir(exist_ok=True)
        if ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ.exists():
            if ଚେକସୁମ୍(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ) != ଚେକସୁମ୍(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ))
        else:
            with tempfile.NamedTemporaryFile(dir=str(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ.parent)) as ଫାଇଲ:
                shutil.copyfile(str(원본), ଫାଇଲ.name)
                os.link(ଫାଇଲ.name, str(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ))

        if ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 is None:
            ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 = {'version': 1, 'name': self.ନାମ, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1)
        if ସିଷ୍ଟମ୍_ସୂଚନା is None:
            self.ନିର୍ଦ୍ଦେଶ(['VBoxManage', 'createvm', '--name', ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['name'], '--uuid', ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ପଥ('machines')), '--register'])
            self.ନିର୍ଦ୍ଦେଶ(['VBoxManage', 'setextradata', ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['uuid'], 'JKOROS/Owner', ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['owner']])
        # ବିଲ୍ଡ୍_ସିଷ୍ଟମ 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        ସିଷ୍ଟମ୍_ସୂଚନା = self.ସିଷ୍ଟମ୍_ସୂଚନା(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1, 등록목록(self.ନିର୍ଦ୍ଦେଶ(['VBoxManage', 'list', 'vms'])))
        if ସିଷ୍ଟମ୍_ସୂଚନା.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('ବିଲ୍ଡ୍_ସିଷ୍ଟମ 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1, ସିଷ୍ଟମ୍_ସୂଚନା)
        ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['iso'] = 매체
        if 매체 not in ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['media']: ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['media'].append(매체)
        ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        ଲଗ୍_ମୂଲ୍ୟ = self.ପଥ(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['serial_log'])
        ଲଗ୍_ମୂଲ୍ୟ.parent.mkdir(exist_ok=True)
        self.ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1)
        self.ନିର୍ଦ୍ଦେଶ(['VBoxManage', 'modifyvm', ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(ଲଗ୍_ମୂଲ୍ୟ)])
        제어기들 = [ମୂଲ୍ୟ for ନାମ, ମୂଲ୍ୟ in ସିଷ୍ଟମ୍_ସୂଚନା.items() if re.fullmatch(r'storagecontrollername\d+', ନାମ)]
        if 'JKOROS IDE' not in 제어기들:
            self.ନିର୍ଦ୍ଦେଶ(['VBoxManage', 'storagectl', ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.ନିର୍ଦ୍ଦେଶ(['VBoxManage', 'storageattach', ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ)])
        ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['pending'] = False
        self.ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1)
        self.ନିର୍ଦ୍ଦେଶ(['VBoxManage', 'startvm', ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1['uuid'], '--type', self.ପଦ୍ଧତି_ମୋଡ୍])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.ପ୍ରଦର୍ଶନ_କରିବା_ସ୍ଥିତି()


def ଚଳାନ୍ତୁ():
    ପାର୍ସ_ମୂଲ୍ୟ = argparse.ArgumentParser(description='jkoros 전용 VirtualBox ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ 및 ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 ଜିଜ୍ଞାସା_ମୂଲ୍ୟ')
    ପାର୍ସ_ମୂଲ୍ୟ.add_argument('action', choices=['run', 'status'])
    ପାରାମିଟର୍_ଯୁକ୍ତି = ପାର୍ସ_ମୂଲ୍ୟ.parse_args()
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ = ଅନୁପ୍ରୟୋଗ_ଆପ୍ଲିକେସନ୍_ଡ୍ରୟର୍(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if ପାରାମିଟର୍_ଯୁକ୍ତି.action == 'status':
        print(json.dumps(ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ପ୍ରଦର୍ଶନ_କରିବା_ସ୍ଥିତି(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. ଆୟୋଜକ 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/ଅନୁମତି_ମୂଲ୍ୟ 변경은 하지 않습니다.')
    os.umask(0o077)
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ପଥ('lock').parent.mkdir(parents=True, exist_ok=True)
    with ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ପଥ('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ 작업이 진행 중입니다.')
        print(json.dumps(ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: ଚଳାନ୍ତୁ()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ତ୍ରୁଟି:
        print('VBOX ତ୍ରୁଟି: ' + str(ତ୍ରୁଟି), file=sys.stderr)
        sys.exit(1)
