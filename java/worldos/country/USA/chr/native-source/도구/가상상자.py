#!/usr/bin/env python3
"""jkoros 전용 VirtualBox 실행기. 기존 VM/디스크/Store_ᏧᎬᏩᎶᏗᏯ 상태는 삭제하지 않는다."""
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


def ᎠᎴᏅᏗᏱ_ᎤᏯᏍᎦ_ᎤᏁᏤᎸᎩ(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(ᏧᎬᏩᎶᏗᏯ) for ᏧᎬᏩᎶᏗᏯ in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('ᎤᏁᏤᎸᎩ ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ: ' + ' '.join(str(ᏧᎬᏩᎶᏗᏯ) for ᏧᎬᏩᎶᏗᏯ in 인수) + '\n' + ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ[-10000:])
    return ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ


def ᏄᏍᏛ_ᎠᎦᏅᏛᎢ_ᏧᎬᏩᎶᏗᏯ(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ):
    결과 = {}
    for ᏚᏓᏅᏅᎢ in ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.splitlines():
        if '=' not in ᏚᏓᏅᏅᎢ:
            continue
        ᏚᏙᎥᎢ, ᏧᎬᏩᎶᏗᏯ = ᏚᏓᏅᏅᎢ.split('=', 1)
        if ᏚᏙᎥᎢ.startswith('"'):
            ᏚᏙᎥᎢ = json.loads(ᏚᏙᎥᎢ)
        if ᏧᎬᏩᎶᏗᏯ.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(ᏧᎬᏩᎶᏗᏯ)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(ᏧᎬᏩᎶᏗᏯ): ᏧᎬᏩᎶᏗᏯ = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox ᏄᏍᏛ_ᎠᎦᏅᏛᎢ_ᏧᎬᏩᎶᏗᏯ ᏱᎬᏁᎸᎯ_ᏧᎬᏩᎶᏗᏯ ᎦᎵᏓᏍᏔᏅ: ' + ᏚᏓᏅᏅᎢ)
        결과[ᏚᏙᎥᎢ] = ᏧᎬᏩᎶᏗᏯ
    return 결과


def 등록목록(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ):
    결과 = {}
    for ᏚᏓᏅᏅᎢ in ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', ᏚᏓᏅᏅᎢ)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(ᎠᏍᏓᏩᏛᏍᏗ):
    ᏧᎬᏩᎶᏗᏯ = hashlib.sha256()
    with ᎠᏍᏓᏩᏛᏍᏗ.open('rb') as ᎠᏍᏆᏂᎪᏙᏗ:
        for ᎦᏟᏌᏅᎯ in iter(lambda: ᎠᏍᏆᏂᎪᏙᏗ.read(1024 * 1024), b''): ᏧᎬᏩᎶᏗᏯ.update(ᎦᏟᏌᏅᎯ)
    return ᏧᎬᏩᎶᏗᏯ.hexdigest()


class 실행기:
    def __init__(self, 뿌리, ᏚᏙᎥᎢ, method_ᎬᏙᏗ='gui', ᎤᏁᏤᎸᎩ=ᎠᎴᏅᏗᏱ_ᎤᏯᏍᎦ_ᎤᏁᏤᎸᎩ):
        self.뿌리 = Path(뿌리).resolve()
        self.ᏚᏙᎥᎢ, self.method_ᎬᏙᏗ, self.ᎤᏁᏤᎸᎩ = ᏚᏙᎥᎢ, method_ᎬᏙᏗ, ᎤᏁᏤᎸᎩ
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', ᏚᏙᎥᎢ) or ᏚᏙᎥᎢ in ('.', '..'):
            raise 실행오류('VM 이름은 문자·숫자·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if method_ᎬᏙᏗ not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ᎠᏍᏓᏩᏛᏍᏗ(self, ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ):
        if Path(ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ).is_absolute() or '..' in Path(ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ).parts:
            raise 실행오류('잘못된 관리 ᎠᏍᏓᏩᏛᏍᏗ: ' + str(ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('ᎫᏓᎳ 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def 읽기(self):
        ᎠᏍᏓᏩᏛᏍᏗ = self.ᎠᏍᏓᏩᏛᏍᏗ('state.json')
        if not ᎠᏍᏓᏩᏛᏍᏗ.exists(): return None
        ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ = json.loads(ᎠᏍᏓᏩᏛᏍᏗ.read_text(encoding='utf-8'))
        if ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.get('version') != 1 or ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.get('name') != self.ᏚᏙᎥᎢ:
            raise 실행오류('관리 상태의 VM ᏚᏙᎥᎢ/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for ᏚᏙᎥᎢ in ('uuid', 'owner'):
            if str(uuid.UUID(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ[ᏚᏙᎥᎢ])) != ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ[ᏚᏙᎥᎢ]: raise 실행오류('잘못된 VM ᎠᏓᏙᎵᎩ_ᏧᎬᏩᎶᏗᏯ')
        return ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ

    def Store_ᏧᎬᏩᎶᏗᏯ(self, ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ):
        ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ = self.ᎠᏍᏓᏩᏛᏍᏗ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as ᎠᏍᏆᏂᎪᏙᏗ:
            json.dump(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ, ᎠᏍᏆᏂᎪᏙᏗ, ensure_ascii=False, indent=2)
            ᎠᏍᏆᏂᎪᏙᏗ.write('\n')
            임시 = ᎠᏍᏆᏂᎪᏙᏗ.name
        os.replace(임시, str(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ))

    def msinfo32_exe(self, ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ, 등록됨, ᎠᏩᏛᏗ_ᏄᏍᏗᏓᏅ=False):
        if ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = ᏄᏍᏛ_ᎠᎦᏅᏛᎢ_ᏧᎬᏩᎶᏗᏯ(self.ᎤᏁᏤᎸᎩ(['VBoxManage', 'showvminfo', ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['uuid'], '--machinereadable']))
        위치 = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.ᎠᏍᏓᏩᏛᏍᏗ('machines').resolve() not in 위치.parents or msinfo32_exe.get('UUID') != ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['uuid']:
            raise 실행오류('이 프로젝트의 VM ᏕᎦᎧᎲᎢ ᎠᏍᏓᏩᏛᏍᏗ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.ᎤᏁᏤᎸᎩ(['VBoxManage', 'getextradata', ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['owner']:
            if ᎠᏩᏛᏗ_ᏄᏍᏗᏓᏅ and ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.get('pending') and 표식 == 'No value set!':
                self.ᎤᏁᏤᎸᎩ(['VBoxManage', 'setextradata', ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['uuid'], 'JKOROS/Owner', ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['owner']])
            else:
                raise 실행오류('VM ᎣᏤᎵᎢ_ᏧᎬᏩᎶᏗᏯ 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def ᎪᎯᏳᏔᏅ_ᎦᎶᏙᏗ(self, ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ, msinfo32_exe):
        제어기들 = [ᏧᎬᏩᎶᏗᏯ for ᏚᏙᎥᎢ, ᏧᎬᏩᎶᏗᏯ in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', ᏚᏙᎥᎢ)]
        ᏗᎵᏍᎪᏟᏙᏗᎢ_ᏧᎬᏩᎶᏗᏯ = [str(self.ᎠᏍᏓᏩᏛᏍᏗ(ᏧᎬᏩᎶᏗᏯ)) for ᏧᎬᏩᎶᏗᏯ in ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.get('media', [])]
        for ᏚᏙᎥᎢ, ᏧᎬᏩᎶᏗᏯ in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', ᏚᏙᎥᎢ) for 제어기 in 제어기들):
                if ᏧᎬᏩᎶᏗᏯ not in ('none', 'emptydrive') and ᏧᎬᏩᎶᏗᏯ not in ᏗᎵᏍᎪᏟᏙᏗᎢ_ᏧᎬᏩᎶᏗᏯ:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + ᏧᎬᏩᎶᏗᏯ)

    def ᏍᎩᎪᏩᏛᏓ_ᏄᏍᏗᏓᏅ(self):
        ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ = self.읽기()
        if ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ is None: return {'name': self.ᏚᏙᎥᎢ, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ, 등록목록(self.ᎤᏁᏤᎸᎩ(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['name']), 'uuid': ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.ᎠᏍᏓᏩᏛᏍᏗ(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['iso'])) if ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.get('iso') else None,
                'serial_log': str(self.ᎠᏍᏓᏩᏛᏍᏗ(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['serial_log'])) if ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(self):
        ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ = self.읽기()
        등록됨 = 등록목록(self.ᎤᏁᏤᎸᎩ(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ is not None and ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ, 등록됨, ᎠᏩᏛᏗ_ᏄᏍᏗᏓᏅ=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 중입니다. 재빌드·재시작하지 않습니다.')
                return self.ᏍᎩᎪᏩᏛᏓ_ᏄᏍᏗᏓᏅ()
            self.ᎪᎯᏳᏔᏅ_ᎦᎶᏙᏗ(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_ᏧᎬᏩᎶᏗᏯ 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.ᎤᏁᏤᎸᎩ(['VBoxManage', 'controlvm', ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 ᎯᏍᏚᎢ 전에 기존 기록도 보관한다.
                    if ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.get('serial_log'):
                        원본 = self.ᎠᏍᏓᏩᏛᏍᏗ(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ᎠᏍᏓᏩᏛᏍᏗ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.ᎤᏁᏤᎸᎩ(['VBoxManage', 'startvm', ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['uuid'], '--type', self.method_ᎬᏙᏗ])
                return self.ᏍᎩᎪᏩᏛᏓ_ᏄᏍᏗᏓᏅ()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 ᎦᏁᏟᏴᏍᏗ_ᎬᏙᏗ 중입니다 ({}). 작업이 끝난 ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ 다시 실행하세요.'.format(현재))
        elif ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ is not None and not ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.ᏚᏙᎥᎢ in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_ᏧᎬᏩᎶᏗᏯ/ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.ᎤᏁᏤᎸᎩ(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        ᎦᎶᏙᏗ_ᏧᎬᏩᎶᏗᏯ = 'media/kernel-' + 검사합(원본) + '.iso'
        ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ = self.ᎠᏍᏓᏩᏛᏍᏗ(ᎦᎶᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
        ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ.parent.mkdir(exist_ok=True)
        if ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ.exists():
            if 검사합(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ))
        else:
            with tempfile.NamedTemporaryFile(dir=str(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ.parent)) as ᎠᏍᏆᏂᎪᏙᏗ:
                shutil.copyfile(str(원본), ᎠᏍᏆᏂᎪᏙᏗ.name)
                os.link(ᎠᏍᏆᏂᎪᏙᏗ.name, str(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ))

        if ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ is None:
            ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ = {'version': 1, 'name': self.ᏚᏙᎥᎢ, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_ᏧᎬᏩᎶᏗᏯ(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ)
        if msinfo32_exe is None:
            self.ᎤᏁᏤᎸᎩ(['VBoxManage', 'createvm', '--name', ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['name'], '--uuid', ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ᎠᏍᏓᏩᏛᏍᏗ('machines')), '--register'])
            self.ᎤᏁᏤᎸᎩ(['VBoxManage', 'setextradata', ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['uuid'], 'JKOROS/Owner', ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['owner']])
        # ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ, 등록목록(self.ᎤᏁᏤᎸᎩ(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.ᎪᎯᏳᏔᏅ_ᎦᎶᏙᏗ(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ, msinfo32_exe)
        ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['iso'] = ᎦᎶᏙᏗ_ᏧᎬᏩᎶᏗᏯ
        if ᎦᎶᏙᏗ_ᏧᎬᏩᎶᏗᏯ not in ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['media']: ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['media'].append(ᎦᎶᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
        ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᏧᎬᏩᎶᏗᏯ = self.ᎠᏍᏓᏩᏛᏍᏗ(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['serial_log'])
        ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᏧᎬᏩᎶᏗᏯ.parent.mkdir(exist_ok=True)
        self.Store_ᏧᎬᏩᎶᏗᏯ(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ)
        self.ᎤᏁᏤᎸᎩ(['VBoxManage', 'modifyvm', ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᏧᎬᏩᎶᏗᏯ)])
        제어기들 = [ᏧᎬᏩᎶᏗᏯ for ᏚᏙᎥᎢ, ᏧᎬᏩᎶᏗᏯ in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', ᏚᏙᎥᎢ)]
        if 'JKOROS IDE' not in 제어기들:
            self.ᎤᏁᏤᎸᎩ(['VBoxManage', 'storagectl', ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.ᎤᏁᏤᎸᎩ(['VBoxManage', 'storageattach', ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ)])
        ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['pending'] = False
        self.Store_ᏧᎬᏩᎶᏗᏯ(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ)
        self.ᎤᏁᏤᎸᎩ(['VBoxManage', 'startvm', ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ['uuid'], '--type', self.method_ᎬᏙᏗ])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.ᏍᎩᎪᏩᏛᏓ_ᏄᏍᏗᏓᏅ()


def ᎠᎢᏎᏍᏗ():
    해석 = argparse.ArgumentParser(description='jkoros 전용 VirtualBox ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 및 ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ ᎠᏛᏛᎲᏍᎩ_ᏧᎬᏩᎶᏗᏯ')
    해석.add_argument('action', choices=['run', 'status'])
    인자 = 해석.parse_args()
    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ = 실행기(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᏍᎩᎪᏩᏛᏓ_ᏄᏍᏗᏓᏅ(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. ᎠᏁᏢᏍᎩ 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/권한 변경은 하지 않습니다.')
    os.umask(0o077)
    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᏍᏓᏩᏛᏍᏗ('lock').parent.mkdir(parents=True, exist_ok=True)
    with ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᏍᏓᏩᏛᏍᏗ('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 작업이 진행 중입니다.')
        print(json.dumps(ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: ᎠᎢᏎᏍᏗ()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ᎦᎵᏓᏍᏔᏅ:
        print('VBOX ᎦᎵᏓᏍᏔᏅ: ' + str(ᎦᎵᏓᏍᏔᏅ), file=sys.stderr)
        sys.exit(1)
