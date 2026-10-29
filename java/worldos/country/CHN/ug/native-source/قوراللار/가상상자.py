#!/usr/bin/env python3
"""jkoros 전용 VirtualBox ئەپ_خادىم. 기존 VM/디스크/ساقلىماق_قىممىتى 상태는 삭제하지 않는다."""
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


def ئىجرا_قىلىش_قاپ_بۇيرۇق(ئۆزگەرگۈچىلەر):
    환경 = dict(os.environ, LC_ALL='C')
    ئۆلچەم = subprocess.run([str(قىممىتى) for قىممىتى in ئۆزگەرگۈچىلەر], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    مەزمۇن_قىممىتى = ئۆلچەم.stdout.decode('utf-8', 'replace')
    if ئۆلچەم.returncode:
        raise 실행오류('بۇيرۇق مەغلۇپ_بولۇش_قىممىتى: ' + ' '.join(str(قىممىتى) for قىممىتى in ئۆزگەرگۈچىلەر) + '\n' + مەزمۇن_قىممىتى[-10000:])
    return مەزمۇن_قىممىتى


def خاسلىق_قىممىتى(مەزمۇن_قىممىتى):
    ئۆلچەم = {}
    for قۇر in مەزمۇن_قىممىتى.splitlines():
        if '=' not in قۇر:
            continue
        ئاتى, قىممىتى = قۇر.split('=', 1)
        if ئاتى.startswith('"'):
            ئاتى = json.loads(ئاتى)
        if قىممىتى.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(قىممىتى)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(قىممىتى): قىممىتى = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox خاسلىق_قىممىتى فورمات_قىممىتى خاتالىق: ' + قۇر)
        ئۆلچەم[ئاتى] = قىممىتى
    return ئۆلچەم


def 등록목록(مەزمۇن_قىممىتى):
    ئۆلچەم = {}
    for قۇر in مەزمۇن_قىممىتى.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', قۇر)
        if 일치: ئۆلچەم[일치.group(2).lower()] = 일치.group(1)
    return ئۆلچەم


def 검사합(يول):
    قىممىتى = hashlib.sha256()
    with يول.open('rb') as ھۆججەت:
        for مەلۇمات in iter(lambda: ھۆججەت.read(1024 * 1024), b''): قىممىتى.update(مەلۇمات)
    return قىممىتى.hexdigest()


class ئەپ_خادىم:
    def __init__(self, يىلتىز_قىممىتى, ئاتى, ئۇسۇل_ھالەت='gui', بۇيرۇق=ئىجرا_قىلىش_قاپ_بۇيرۇق):
        self.يىلتىز_قىممىتى = Path(يىلتىز_قىممىتى).resolve()
        self.ئاتى, self.ئۇسۇل_ھالەت, self.بۇيرۇق = ئاتى, ئۇسۇل_ھالەت, بۇيرۇق
        self.보관 = self.يىلتىز_قىممىتى / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', ئاتى) or ئاتى in ('.', '..'):
            raise 실행오류('VM 이름은 문자·خانا_قىممىتى·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if ئۇسۇل_ھالەت not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def يول(self, باراۋەرلىك_قىممىتى):
        if Path(باراۋەرلىك_قىممىتى).is_absolute() or '..' in Path(باراۋەرلىك_قىممىتى).parts:
            raise 실행오류('잘못된 관리 يول: ' + str(باراۋەرلىك_قىممىتى))
        ئۆلچەم = self.보관
        for 부분 in ['.vbox'] + list(Path(باراۋەرلىك_قىممىتى).parts):
            if 부분 == '.vbox': ئۆلچەم = self.보관
            else: ئۆلچەم = ئۆلچەم / 부분
            if ئۆلچەم.is_symlink(): raise 실행오류('ئۇلا 경로는 사용하지 않습니다: ' + str(ئۆلچەم))
        return ئۆلچەم

    def ئوقۇ(self):
        يول = self.يول('state.json')
        if not يول.exists(): return None
        ھالەت_قىممىتى = json.loads(يول.read_text(encoding='utf-8'))
        if ھالەت_قىممىتى.get('version') != 1 or ھالەت_قىممىتى.get('name') != self.ئاتى:
            raise 실행오류('관리 상태의 VM ئاتى/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for ئاتى in ('uuid', 'owner'):
            if str(uuid.UUID(ھالەت_قىممىتى[ئاتى])) != ھالەت_قىممىتى[ئاتى]: raise 실행오류('잘못된 VM پەرقلەندۈرگۈچ_قىممىتى')
        return ھالەت_قىممىتى

    def ساقلىماق_قىممىتى(self, ھالەت_قىممىتى):
        نىشان_قىممىتى = self.يول('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as ھۆججەت:
            json.dump(ھالەت_قىممىتى, ھۆججەت, ensure_ascii=False, indent=2)
            ھۆججەت.write('\n')
            임시 = ھۆججەت.name
        os.replace(임시, str(نىشان_قىممىتى))

    def سىستېما_ئۇچۇرى(self, ھالەت_قىممىتى, 등록됨, ئەسلىگە_قايتۇرماق_ھالەت=False):
        if ھالەت_قىممىتى['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        سىستېما_ئۇچۇرى = خاسلىق_قىممىتى(self.بۇيرۇق(['VBoxManage', 'showvminfo', ھالەت_قىممىتى['uuid'], '--machinereadable']))
        ئورۇن = Path(سىستېما_ئۇچۇرى.get('CfgFile', '')).resolve()
        if self.يول('machines').resolve() not in ئورۇن.parents or سىستېما_ئۇچۇرى.get('UUID') != ھالەت_قىممىتى['uuid']:
            raise 실행오류('이 프로젝트의 VM تەڭشەكلەر يول/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.بۇيرۇق(['VBoxManage', 'getextradata', ھالەت_قىممىتى['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + ھالەت_قىممىتى['owner']:
            if ئەسلىگە_قايتۇرماق_ھالەت and ھالەت_قىممىتى.get('pending') and 표식 == 'No value set!':
                self.بۇيرۇق(['VBoxManage', 'setextradata', ھالەت_قىممىتى['uuid'], 'JKOROS/Owner', ھالەت_قىممىتى['owner']])
            else:
                raise 실행오류('VM ئىگە_قىممىتى 표식이 일치하지 않아 변경하지 않습니다.')
        return سىستېما_ئۇچۇرى

    def تەكشۈرۈش_مېدىيا(self, ھالەت_قىممىتى, سىستېما_ئۇچۇرى):
        제어기들 = [قىممىتى for ئاتى, قىممىتى in سىستېما_ئۇچۇرى.items() if re.fullmatch(r'storagecontrollername\d+', ئاتى)]
        رۇخسەتنامە_قىممىتى = [str(self.يول(قىممىتى)) for قىممىتى in ھالەت_قىممىتى.get('media', [])]
        for ئاتى, قىممىتى in سىستېما_ئۇچۇرى.items():
            if any(re.fullmatch(re.escape(كونتىرول_قىلغۇچى) + r'-\d+-\d+', ئاتى) for كونتىرول_قىلغۇچى in 제어기들):
                if قىممىتى not in ('none', 'emptydrive') and قىممىتى not in رۇخسەتنامە_قىممىتى:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + قىممىتى)

    def كۆرسەتمەك_ھالەت(self):
        ھالەت_قىممىتى = self.ئوقۇ()
        if ھالەت_قىممىتى is None: return {'name': self.ئاتى, 'state': 'not-created'}
        سىستېما_ئۇچۇرى = self.سىستېما_ئۇچۇرى(ھالەت_قىممىتى, 등록목록(self.بۇيرۇق(['VBoxManage', 'list', 'vms'])))
        return {'name': سىستېما_ئۇچۇرى.get('name', ھالەت_قىممىتى['name']), 'uuid': ھالەت_قىممىتى['uuid'], 'state': سىستېما_ئۇچۇرى.get('VMState'),
                'iso': str(self.يول(ھالەت_قىممىتى['iso'])) if ھالەت_قىممىتى.get('iso') else None,
                'serial_log': str(self.يول(ھالەت_قىممىتى['serial_log'])) if ھالەت_قىممىتى.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def ئىجرا_قىلىش_بۇيرۇق(self):
        ھالەت_قىممىتى = self.ئوقۇ()
        등록됨 = 등록목록(self.بۇيرۇق(['VBoxManage', 'list', 'vms']))
        سىستېما_ئۇچۇرى = None
        if ھالەت_قىممىتى is not None and ھالەت_قىممىتى['uuid'] in 등록됨:
            سىستېما_ئۇچۇرى = self.سىستېما_ئۇچۇرى(ھالەت_قىممىتى, 등록됨, ئەسلىگە_قايتۇرماق_ھالەت=True)
            현재 = سىستېما_ئۇچۇرى.get('VMState')
            if 현재 == 'running':
                print('이미 ئىجرا_قىلىش_بۇيرۇق 중입니다. 재빌드·재시작하지 않습니다.')
                return self.كۆرسەتمەك_ھالەت()
            self.تەكشۈرۈش_مېدىيا(ھالەت_قىممىتى, سىستېما_ئۇچۇرى)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 ساقلىماق_قىممىتى 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.بۇيرۇق(['VBoxManage', 'controlvm', ھالەت_قىممىتى['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 ئاچ 전에 기존 기록도 보관한다.
                    if ھالەت_قىممىتى.get('serial_log'):
                        원본 = self.يول(ھالەت_قىممىتى['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.يول('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.بۇيرۇق(['VBoxManage', 'startvm', ھالەت_قىممىتى['uuid'], '--type', self.ئۇسۇل_ھالەت])
                return self.كۆرسەتمەك_ھالەت()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 ئۆزگەرتمەك_ھالەت 중입니다 ({}). 작업이 끝난 ئارقىغا_قىممىتى 다시 실행하세요.'.format(현재))
        elif ھالەت_قىممىتى is not None and not ھالەت_قىممىتى.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.ئاتى in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # ساقلىماق_قىممىتى/ئىجرا_قىلىش_بۇيرۇق 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.بۇيرۇق(['make', '-C', str(self.يىلتىز_قىممىتى / 'os'), 'iso']), end='')
        원본 = self.يىلتىز_قىممىتى / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        مېدىيا_قىممىتى = 'media/kernel-' + 검사합(원본) + '.iso'
        نىشان_قىممىتى = self.يول(مېدىيا_قىممىتى)
        نىشان_قىممىتى.parent.mkdir(exist_ok=True)
        if نىشان_قىممىتى.exists():
            if 검사합(نىشان_قىممىتى) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(نىشان_قىممىتى))
        else:
            with tempfile.NamedTemporaryFile(dir=str(نىشان_قىممىتى.parent)) as ھۆججەت:
                shutil.copyfile(str(원본), ھۆججەت.name)
                os.link(ھۆججەت.name, str(نىشان_قىممىتى))

        if ھالەت_قىممىتى is None:
            ھالەت_قىممىتى = {'version': 1, 'name': self.ئاتى, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.ساقلىماق_قىممىتى(ھالەت_قىممىتى)
        if سىستېما_ئۇچۇرى is None:
            self.بۇيرۇق(['VBoxManage', 'createvm', '--name', ھالەت_قىممىتى['name'], '--uuid', ھالەت_قىممىتى['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.يول('machines')), '--register'])
            self.بۇيرۇق(['VBoxManage', 'setextradata', ھالەت_قىممىتى['uuid'], 'JKOROS/Owner', ھالەت_قىممىتى['owner']])
        # نۇسخا_سىستېما 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        سىستېما_ئۇچۇرى = self.سىستېما_ئۇچۇرى(ھالەت_قىممىتى, 등록목록(self.بۇيرۇق(['VBoxManage', 'list', 'vms'])))
        if سىستېما_ئۇچۇرى.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('نۇسخا_سىستېما 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.تەكشۈرۈش_مېدىيا(ھالەت_قىممىتى, سىستېما_ئۇچۇرى)
        ھالەت_قىممىتى['iso'] = مېدىيا_قىممىتى
        if مېدىيا_قىممىتى not in ھالەت_قىممىتى['media']: ھالەت_قىممىتى['media'].append(مېدىيا_قىممىتى)
        ھالەت_قىممىتى['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        خاتىرە_قىممىتى = self.يول(ھالەت_قىممىتى['serial_log'])
        خاتىرە_قىممىتى.parent.mkdir(exist_ok=True)
        self.ساقلىماق_قىممىتى(ھالەت_قىممىتى)
        self.بۇيرۇق(['VBoxManage', 'modifyvm', ھالەت_قىممىتى['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(خاتىرە_قىممىتى)])
        제어기들 = [قىممىتى for ئاتى, قىممىتى in سىستېما_ئۇچۇرى.items() if re.fullmatch(r'storagecontrollername\d+', ئاتى)]
        if 'JKOROS IDE' not in 제어기들:
            self.بۇيرۇق(['VBoxManage', 'storagectl', ھالەت_قىممىتى['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.بۇيرۇق(['VBoxManage', 'storageattach', ھالەت_قىممىتى['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(نىشان_قىممىتى)])
        ھالەت_قىممىتى['pending'] = False
        self.ساقلىماق_قىممىتى(ھالەت_قىممىتى)
        self.بۇيرۇق(['VBoxManage', 'startvm', ھالەت_قىممىتى['uuid'], '--type', self.ئۇسۇل_ھالەت])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.كۆرسەتمەك_ھالەت()


def ئىجرا_قىل_2():
    해석 = argparse.ArgumentParser(description='jkoros 전용 VirtualBox ئىجرا_قىلىش_بۇيرۇق 및 ھالەت_قىممىتى تەكشۈرۈش_قىممىتى')
    해석.add_argument('action', choices=['run', 'status'])
    인자 = 해석.parse_args()
    ئىجرا_قىلىش_بۇيرۇق = ئەپ_خادىم(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(ئىجرا_قىلىش_بۇيرۇق.كۆرسەتمەك_ھالەت(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. باقار 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/ئىجازەت_قىممىتى 변경은 하지 않습니다.')
    os.umask(0o077)
    ئىجرا_قىلىش_بۇيرۇق.يول('lock').parent.mkdir(parents=True, exist_ok=True)
    with ئىجرا_قىلىش_بۇيرۇق.يول('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox ئىجرا_قىلىش_بۇيرۇق 작업이 진행 중입니다.')
        print(json.dumps(ئىجرا_قىلىش_بۇيرۇق.ئىجرا_قىلىش_بۇيرۇق(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: ئىجرا_قىل_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as خاتالىق:
        print('VBOX خاتالىق: ' + str(خاتالىق), file=sys.stderr)
        sys.exit(1)
