#!/usr/bin/env python3
"""jkoros 전용 VirtualBox កម្មវិធី_ថត_កម្មវិធី. 기존 VM/디스크/ផ្ទុក_តំលៃ 상태는 삭제하지 않는다."""
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


def 명령실행(អាគុយម៉ង់):
    환경 = dict(os.environ, LC_ALL='C')
    ការវាស់វែង = subprocess.run([str(តំលៃ) for តំលៃ in អាគុយម៉ង់], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    មាតិកា_តំលៃ = ការវាស់វែង.stdout.decode('utf-8', 'replace')
    if ការវាស់វែង.returncode:
        raise 실행오류('ពាក្យ_បញ្ជា បរាជ័យ_តំលៃ: ' + ' '.join(str(តំលៃ) for តំលៃ in អាគុយម៉ង់) + '\n' + មាតិកា_តំលៃ[-10000:])
    return មាតិកា_តំលៃ


def លក្ខណះ_តំលៃ(មាតិកា_តំលៃ):
    ការវាស់វែង = {}
    for បន្ទាត់ in មាតិកា_តំលៃ.splitlines():
        if '=' not in បន្ទាត់:
            continue
        ឈ្មោះ, តំលៃ = បន្ទាត់.split('=', 1)
        if ឈ្មោះ.startswith('"'):
            ឈ្មោះ = json.loads(ឈ្មោះ)
        if តំលៃ.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(តំលៃ)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(តំលៃ): តំលៃ = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox លក្ខណះ_តំលៃ ទំរង់_តំលៃ កំហុស: ' + បន្ទាត់)
        ការវាស់វែង[ឈ្មោះ] = តំលៃ
    return ការវាស់វែង


def 등록목록(មាតិកា_តំលៃ):
    ការវាស់វែង = {}
    for បន្ទាត់ in មាតិកា_តំលៃ.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', បន្ទាត់)
        if 일치: ការវាស់វែង[일치.group(2).lower()] = 일치.group(1)
    return ការវាស់វែង


def លេខសរុបដើម្បីពិនិត្យមើលទិន្នន័យត្រឹមត្រូវ(ផ្លូវ):
    តំលៃ = hashlib.sha256()
    with ផ្លូវ.open('rb') as ឯកសារ:
        for ទិន្នន័យ in iter(lambda: ឯកសារ.read(1024 * 1024), b''): តំលៃ.update(ទិន្នន័យ)
    return តំលៃ.hexdigest()


class កម្មវិធី_ថត_កម្មវិធី:
    def __init__(self, ឬស_តំលៃ, ឈ្មោះ, វិធីសាស្រ្ត_ម៉ូដ='gui', ពាក្យ_បញ្ជា=명령실행):
        self.ឬស_តំលៃ = Path(ឬស_តំលៃ).resolve()
        self.ឈ្មោះ, self.វិធីសាស្រ្ត_ម៉ូដ, self.ពាក្យ_បញ្ជា = ឈ្មោះ, វិធីសាស្រ្ត_ម៉ូដ, ពាក្យ_បញ្ជា
        self.보관 = self.ឬស_តំលៃ / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', ឈ្មោះ) or ឈ្មោះ in ('.', '..'):
            raise 실행오류('VM 이름은 문자·숫자·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if វិធីសាស្រ្ត_ម៉ូដ not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ផ្លូវ(self, សិទ្ធស្មើ_តំលៃ):
        if Path(សិទ្ធស្មើ_តំលៃ).is_absolute() or '..' in Path(សិទ្ធស្មើ_តំលៃ).parts:
            raise 실행오류('잘못된 관리 ផ្លូវ: ' + str(សិទ្ធស្មើ_តំលៃ))
        ការវាស់វែង = self.보관
        for 부분 in ['.vbox'] + list(Path(សិទ្ធស្មើ_តំលៃ).parts):
            if 부분 == '.vbox': ការវាស់វែង = self.보관
            else: ការវាស់វែង = ការវាស់វែង / 부분
            if ការវាស់វែង.is_symlink(): raise 실행오류('ភ្ជាប់ 경로는 사용하지 않습니다: ' + str(ការវាស់វែង))
        return ការវាស់វែង

    def អាន(self):
        ផ្លូវ = self.ផ្លូវ('state.json')
        if not ផ្លូវ.exists(): return None
        ភាព_តំលៃ = json.loads(ផ្លូវ.read_text(encoding='utf-8'))
        if ភាព_តំលៃ.get('version') != 1 or ភាព_តំលៃ.get('name') != self.ឈ្មោះ:
            raise 실행오류('관리 상태의 VM ឈ្មោះ/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for ឈ្មោះ in ('uuid', 'owner'):
            if str(uuid.UUID(ភាព_តំលៃ[ឈ្មោះ])) != ភាព_តំលៃ[ឈ្មោះ]: raise 실행오류('잘못된 VM អង្គសម្គាល់_តំលៃ')
        return ភាព_តំលៃ

    def ផ្ទុក_តំលៃ(self, ភាព_តំលៃ):
        ទិសដៅ_តំលៃ = self.ផ្លូវ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as ឯកសារ:
            json.dump(ភាព_តំលៃ, ឯកសារ, ensure_ascii=False, indent=2)
            ឯកសារ.write('\n')
            임시 = ឯកសារ.name
        os.replace(임시, str(ទិសដៅ_តំលៃ))

    def ប្រព័ន្ធព័ត៌មាន(self, ភាព_តំលៃ, 등록됨, សង្គ្រោះឯកសារ_ភាព=False):
        if ភាព_តំលៃ['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        ប្រព័ន្ធព័ត៌មាន = លក្ខណះ_តំលៃ(self.ពាក្យ_បញ្ជា(['VBoxManage', 'showvminfo', ភាព_តំលៃ['uuid'], '--machinereadable']))
        កំណត់ទីតាំង = Path(ប្រព័ន្ធព័ត៌មាន.get('CfgFile', '')).resolve()
        if self.ផ្លូវ('machines').resolve() not in កំណត់ទីតាំង.parents or ប្រព័ន្ធព័ត៌មាន.get('UUID') != ភាព_តំលៃ['uuid']:
            raise 실행오류('이 프로젝트의 VM ការកំណត់ ផ្លូវ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.ពាក្យ_បញ្ជា(['VBoxManage', 'getextradata', ភាព_តំលៃ['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + ភាព_តំលៃ['owner']:
            if សង្គ្រោះឯកសារ_ភាព and ភាព_តំលៃ.get('pending') and 표식 == 'No value set!':
                self.ពាក្យ_បញ្ជា(['VBoxManage', 'setextradata', ភាព_តំលៃ['uuid'], 'JKOROS/Owner', ភាព_តំលៃ['owner']])
            else:
                raise 실행오류('VM ម្ចាស់_តំលៃ 표식이 일치하지 않아 변경하지 않습니다.')
        return ប្រព័ន្ធព័ត៌មាន

    def 매체검사(self, ភាព_តំលៃ, ប្រព័ន្ធព័ត៌មាន):
        제어기들 = [តំលៃ for ឈ្មោះ, តំលៃ in ប្រព័ន្ធព័ត៌មាន.items() if re.fullmatch(r'storagecontrollername\d+', ឈ្មោះ)]
        អនុញ្ញាត_តំលៃ = [str(self.ផ្លូវ(តំលៃ)) for តំលៃ in ភាព_តំលៃ.get('media', [])]
        for ឈ្មោះ, តំលៃ in ប្រព័ន្ធព័ត៌មាន.items():
            if any(re.fullmatch(re.escape(ឧបករណ៍_បញ្ជា) + r'-\d+-\d+', ឈ្មោះ) for ឧបករណ៍_បញ្ជា in 제어기들):
                if តំលៃ not in ('none', 'emptydrive') and តំលៃ not in អនុញ្ញាត_តំលៃ:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + តំលៃ)

    def បង្ហាញ_ភាព(self):
        ភាព_តំលៃ = self.អាន()
        if ភាព_តំលៃ is None: return {'name': self.ឈ្មោះ, 'state': 'not-created'}
        ប្រព័ន្ធព័ត៌មាន = self.ប្រព័ន្ធព័ត៌មាន(ភាព_តំលៃ, 등록목록(self.ពាក្យ_បញ្ជា(['VBoxManage', 'list', 'vms'])))
        return {'name': ប្រព័ន្ធព័ត៌មាន.get('name', ភាព_តំលៃ['name']), 'uuid': ភាព_តំលៃ['uuid'], 'state': ប្រព័ន្ធព័ត៌មាន.get('VMState'),
                'iso': str(self.ផ្លូវ(ភាព_តំលៃ['iso'])) if ភាព_តំលៃ.get('iso') else None,
                'serial_log': str(self.ផ្លូវ(ភាព_តំលៃ['serial_log'])) if ភាព_តំលៃ.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def អនុវត្ត_ពាក្យបញ្ជា(self):
        ភាព_តំលៃ = self.អាន()
        등록됨 = 등록목록(self.ពាក្យ_បញ្ជា(['VBoxManage', 'list', 'vms']))
        ប្រព័ន្ធព័ត៌មាន = None
        if ភាព_តំលៃ is not None and ភាព_តំលៃ['uuid'] in 등록됨:
            ប្រព័ន្ធព័ត៌មាន = self.ប្រព័ន្ធព័ត៌មាន(ភាព_តំលៃ, 등록됨, សង្គ្រោះឯកសារ_ភាព=True)
            현재 = ប្រព័ន្ធព័ត៌មាន.get('VMState')
            if 현재 == 'running':
                print('이미 អនុវត្ត_ពាក្យបញ្ជា 중입니다. 재빌드·재시작하지 않습니다.')
                return self.បង្ហាញ_ភាព()
            self.매체검사(ភាព_តំលៃ, ប្រព័ន្ធព័ត៌មាន)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 ផ្ទុក_តំលៃ 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.ពាក្យ_បញ្ជា(['VBoxManage', 'controlvm', ភាព_តំលៃ['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 បើក 전에 기존 기록도 보관한다.
                    if ភាព_តំលៃ.get('serial_log'):
                        원본 = self.ផ្លូវ(ភាព_តំលៃ['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ផ្លូវ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.ពាក្យ_បញ្ជា(['VBoxManage', 'startvm', ភាព_តំលៃ['uuid'], '--type', self.វិធីសាស្រ្ត_ម៉ូដ])
                return self.បង្ហាញ_ភាព()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 ប្ដូរ_ម៉ូដ 중입니다 ({}). 작업이 끝난 ការថយ_តំលៃ 다시 실행하세요.'.format(현재))
        elif ភាព_តំលៃ is not None and not ភាព_តំលៃ.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.ឈ្មោះ in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # ផ្ទុក_តំលៃ/អនុវត្ត_ពាក្យបញ្ជា 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.ពាក្យ_បញ្ជា(['make', '-C', str(self.ឬស_តំលៃ / 'os'), 'iso']), end='')
        원본 = self.ឬស_តំលៃ / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + លេខសរុបដើម្បីពិនិត្យមើលទិន្នន័យត្រឹមត្រូវ(원본) + '.iso'
        ទិសដៅ_តំលៃ = self.ផ្លូវ(매체)
        ទិសដៅ_តំលៃ.parent.mkdir(exist_ok=True)
        if ទិសដៅ_តំលៃ.exists():
            if លេខសរុបដើម្បីពិនិត្យមើលទិន្នន័យត្រឹមត្រូវ(ទិសដៅ_តំលៃ) != លេខសរុបដើម្បីពិនិត្យមើលទិន្នន័យត្រឹមត្រូវ(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(ទិសដៅ_តំលៃ))
        else:
            with tempfile.NamedTemporaryFile(dir=str(ទិសដៅ_តំលៃ.parent)) as ឯកសារ:
                shutil.copyfile(str(원본), ឯកសារ.name)
                os.link(ឯកសារ.name, str(ទិសដៅ_តំលៃ))

        if ភាព_តំលៃ is None:
            ភាព_តំលៃ = {'version': 1, 'name': self.ឈ្មោះ, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.ផ្ទុក_តំលៃ(ភាព_តំលៃ)
        if ប្រព័ន្ធព័ត៌មាន is None:
            self.ពាក្យ_បញ្ជា(['VBoxManage', 'createvm', '--name', ភាព_តំលៃ['name'], '--uuid', ភាព_តំលៃ['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ផ្លូវ('machines')), '--register'])
            self.ពាក្យ_បញ្ជា(['VBoxManage', 'setextradata', ភាព_តំលៃ['uuid'], 'JKOROS/Owner', ភាព_តំលៃ['owner']])
        # ចងក្រង_ប្រព័ន្ធ 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        ប្រព័ន្ធព័ត៌មាន = self.ប្រព័ន្ធព័ត៌មាន(ភាព_តំលៃ, 등록목록(self.ពាក្យ_បញ្ជា(['VBoxManage', 'list', 'vms'])))
        if ប្រព័ន្ធព័ត៌មាន.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('ចងក្រង_ប្រព័ន្ធ 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(ភាព_តំលៃ, ប្រព័ន្ធព័ត៌មាន)
        ភាព_តំលៃ['iso'] = 매체
        if 매체 not in ភាព_តំលៃ['media']: ភាព_តំលៃ['media'].append(매체)
        ភាព_តំលៃ['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        កំណត់_ហេតុ_តំលៃ = self.ផ្លូវ(ភាព_តំលៃ['serial_log'])
        កំណត់_ហេតុ_តំលៃ.parent.mkdir(exist_ok=True)
        self.ផ្ទុក_តំលៃ(ភាព_តំលៃ)
        self.ពាក្យ_បញ្ជា(['VBoxManage', 'modifyvm', ភាព_តំលៃ['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(កំណត់_ហេតុ_តំលៃ)])
        제어기들 = [តំលៃ for ឈ្មោះ, តំលៃ in ប្រព័ន្ធព័ត៌មាន.items() if re.fullmatch(r'storagecontrollername\d+', ឈ្មោះ)]
        if 'JKOROS IDE' not in 제어기들:
            self.ពាក្យ_បញ្ជា(['VBoxManage', 'storagectl', ភាព_តំលៃ['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.ពាក្យ_បញ្ជា(['VBoxManage', 'storageattach', ភាព_តំលៃ['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(ទិសដៅ_តំលៃ)])
        ភាព_តំលៃ['pending'] = False
        self.ផ្ទុក_តំលៃ(ភាព_តំលៃ)
        self.ពាក្យ_បញ្ជា(['VBoxManage', 'startvm', ភាព_តំលៃ['uuid'], '--type', self.វិធីសាស្រ្ត_ម៉ូដ])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.បង្ហាញ_ភាព()


def រត់():
    ញែក_តំលៃ = argparse.ArgumentParser(description='jkoros 전용 VirtualBox អនុវត្ត_ពាក្យបញ្ជា 및 ភាព_តំលៃ សំណើ_តំលៃ')
    ញែក_តំលៃ.add_argument('action', choices=['run', 'status'])
    ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់ = ញែក_តំលៃ.parse_args()
    អនុវត្ត_ពាក្យបញ្ជា = កម្មវិធី_ថត_កម្មវិធី(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.action == 'status':
        print(json.dumps(អនុវត្ត_ពាក្យបញ្ជា.បង្ហាញ_ភាព(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. ហូស 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/ការអនុញ្ញាត_តំលៃ 변경은 하지 않습니다.')
    os.umask(0o077)
    អនុវត្ត_ពាក្យបញ្ជា.ផ្លូវ('lock').parent.mkdir(parents=True, exist_ok=True)
    with អនុវត្ត_ពាក្យបញ្ជា.ផ្លូវ('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox អនុវត្ត_ពាក្យបញ្ជា 작업이 진행 중입니다.')
        print(json.dumps(អនុវត្ត_ពាក្យបញ្ជា.អនុវត្ត_ពាក្យបញ្ជា(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: រត់()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as កំហុស:
        print('VBOX កំហុស: ' + str(កំហុស), file=sys.stderr)
        sys.exit(1)
