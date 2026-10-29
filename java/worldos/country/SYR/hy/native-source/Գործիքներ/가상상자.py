#!/usr/bin/env python3
"""jkoros 전용 VirtualBox ծրագիր_թողարկիչ. 기존 VM/디스크/պահեստավորել_արժեք 상태는 삭제하지 않는다."""
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


def կատարել_խեցի_հրաման(인수):
    환경 = dict(os.environ, LC_ALL='C')
    չափ = subprocess.run([str(արժեք) for արժեք in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Բովանդակություն_արժեք = չափ.stdout.decode('utf-8', 'replace')
    if չափ.returncode:
        raise 실행오류('Հրահանգ ձախողում_արժեք: ' + ' '.join(str(արժեք) for արժեք in 인수) + '\n' + Բովանդակություն_արժեք[-10000:])
    return Բովանդակություն_արժեք


def հատկանիշ_արժեք(Բովանդակություն_արժեք):
    չափ = {}
    for կապ in Բովանդակություն_արժեք.splitlines():
        if '=' not in կապ:
            continue
        Անուն, արժեք = կապ.split('=', 1)
        if Անուն.startswith('"'):
            Անուն = json.loads(Անուն)
        if արժեք.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(արժեք)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(արժեք): արժեք = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox հատկանիշ_արժեք ձեւաչափ_արժեք Սխալ: ' + կապ)
        չափ[Անուն] = արժեք
    return չափ


def 등록목록(Բովանդակություն_արժեք):
    չափ = {}
    for կապ in Բովանդակություն_արժեք.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', կապ)
        if 일치: չափ[일치.group(2).lower()] = 일치.group(1)
    return չափ


def 검사합(Ճանապարհ):
    արժեք = hashlib.sha256()
    with Ճանապարհ.open('rb') as Ֆայլ:
        for տվյալ in iter(lambda: Ֆայլ.read(1024 * 1024), b''): արժեք.update(տվյալ)
    return արժեք.hexdigest()


class ծրագիր_թողարկիչ:
    def __init__(self, արմատ_արժեք, Անուն, եղանակ_կերպ='gui', Հրահանգ=կատարել_խեցի_հրաման):
        self.արմատ_արժեք = Path(արմատ_արժեք).resolve()
        self.Անուն, self.եղանակ_կերպ, self.Հրահանգ = Անուն, եղանակ_կերպ, Հրահանգ
        self.보관 = self.արմատ_արժեք / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Անուն) or Անուն in ('.', '..'):
            raise 실행오류('VM 이름은 문자·թվանշան_արժեք·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if եղանակ_կերպ not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Ճանապարհ(self, հավասարազոր_սարք_արժեք):
        if Path(հավասարազոր_սարք_արժեք).is_absolute() or '..' in Path(հավասարազոր_սարք_արժեք).parts:
            raise 실행오류('잘못된 관리 Ճանապարհ: ' + str(հավասարազոր_սարք_արժեք))
        չափ = self.보관
        for 부분 in ['.vbox'] + list(Path(հավասարազոր_սարք_արժեք).parts):
            if 부분 == '.vbox': չափ = self.보관
            else: չափ = չափ / 부분
            if չափ.is_symlink(): raise 실행오류('Միացնել 경로는 사용하지 않습니다: ' + str(չափ))
        return չափ

    def Ընթերցում(self):
        Ճանապարհ = self.Ճանապարհ('state.json')
        if not Ճանապարհ.exists(): return None
        վիճակ_արժեք = json.loads(Ճանապարհ.read_text(encoding='utf-8'))
        if վիճակ_արժեք.get('version') != 1 or վիճակ_արժեք.get('name') != self.Անուն:
            raise 실행오류('관리 상태의 VM Անուն/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Անուն in ('uuid', 'owner'):
            if str(uuid.UUID(վիճակ_արժեք[Անուն])) != վիճակ_արժեք[Անուն]: raise 실행오류('잘못된 VM նույնացուցիչ_արժեք')
        return վիճակ_արժեք

    def պահեստավորել_արժեք(self, վիճակ_արժեք):
        նպատակակետ_արժեք = self.Ճանապարհ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Ֆայլ:
            json.dump(վիճակ_արժեք, Ֆայլ, ensure_ascii=False, indent=2)
            Ֆայլ.write('\n')
            임시 = Ֆայլ.name
        os.replace(임시, str(նպատակակետ_արժեք))

    def Համակարգի_տեղեկություն(self, վիճակ_արժեք, 등록됨, վերականգնել_վիճակ=False):
        if վիճակ_արժեք['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        Համակարգի_տեղեկություն = հատկանիշ_արժեք(self.Հրահանգ(['VBoxManage', 'showvminfo', վիճակ_արժեք['uuid'], '--machinereadable']))
        Դիրք = Path(Համակարգի_տեղեկություն.get('CfgFile', '')).resolve()
        if self.Ճանապարհ('machines').resolve() not in Դիրք.parents or Համակարգի_տեղեկություն.get('UUID') != վիճակ_արժեք['uuid']:
            raise 실행오류('이 프로젝트의 VM Նախընտրանքներ Ճանապարհ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Հրահանգ(['VBoxManage', 'getextradata', վիճակ_արժեք['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + վիճակ_արժեք['owner']:
            if վերականգնել_վիճակ and վիճակ_արժեք.get('pending') and 표식 == 'No value set!':
                self.Հրահանգ(['VBoxManage', 'setextradata', վիճակ_արժեք['uuid'], 'JKOROS/Owner', վիճակ_արժեք['owner']])
            else:
                raise 실행오류('VM տնօրինող_արժեք 표식이 일치하지 않아 변경하지 않습니다.')
        return Համակարգի_տեղեկություն

    def 매체검사(self, վիճակ_արժեք, Համակարգի_տեղեկություն):
        제어기들 = [արժեք for Անուն, արժեք in Համակարգի_տեղեկություն.items() if re.fullmatch(r'storagecontrollername\d+', Անուն)]
        Թույլատրել_արժեք = [str(self.Ճանապարհ(արժեք)) for արժեք in վիճակ_արժեք.get('media', [])]
        for Անուն, արժեք in Համակարգի_տեղեկություն.items():
            if any(re.fullmatch(re.escape(հսկիչ) + r'-\d+-\d+', Անուն) for հսկիչ in 제어기들):
                if արժեք not in ('none', 'emptydrive') and արժեք not in Թույլատրել_արժեք:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + արժեք)

    def ցուցադրել_վիճակ(self):
        վիճակ_արժեք = self.Ընթերցում()
        if վիճակ_արժեք is None: return {'name': self.Անուն, 'state': 'not-created'}
        Համակարգի_տեղեկություն = self.Համակարգի_տեղեկություն(վիճակ_արժեք, 등록목록(self.Հրահանգ(['VBoxManage', 'list', 'vms'])))
        return {'name': Համակարգի_տեղեկություն.get('name', վիճակ_արժեք['name']), 'uuid': վիճակ_արժեք['uuid'], 'state': Համակարգի_տեղեկություն.get('VMState'),
                'iso': str(self.Ճանապարհ(վիճակ_արժեք['iso'])) if վիճակ_արժեք.get('iso') else None,
                'serial_log': str(self.Ճանապարհ(վիճակ_արժեք['serial_log'])) if վիճակ_արժեք.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def կատարել_հրաման(self):
        վիճակ_արժեք = self.Ընթերցում()
        등록됨 = 등록목록(self.Հրահանգ(['VBoxManage', 'list', 'vms']))
        Համակարգի_տեղեկություն = None
        if վիճակ_արժեք is not None and վիճակ_արժեք['uuid'] in 등록됨:
            Համակարգի_տեղեկություն = self.Համակարգի_տեղեկություն(վիճակ_արժեք, 등록됨, վերականգնել_վիճակ=True)
            현재 = Համակարգի_տեղեկություն.get('VMState')
            if 현재 == 'running':
                print('이미 կատարել_հրաման 중입니다. 재빌드·재시작하지 않습니다.')
                return self.ցուցադրել_վիճակ()
            self.매체검사(վիճակ_արժեք, Համակարգի_տեղեկություն)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 պահեստավորել_արժեք 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Հրահանգ(['VBoxManage', 'controlvm', վիճակ_արժեք['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Բաց 전에 기존 기록도 보관한다.
                    if վիճակ_արժեք.get('serial_log'):
                        원본 = self.Ճանապարհ(վիճակ_արժեք['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Ճանապարհ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Հրահանգ(['VBoxManage', 'startvm', վիճակ_արժեք['uuid'], '--type', self.եղանակ_կերպ])
                return self.ցուցադրել_վիճակ()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 փոխարկել_կերպ 중입니다 ({}). 작업이 끝난 Հետ_արժեք 다시 실행하세요.'.format(현재))
        elif վիճակ_արժեք is not None and not վիճակ_արժեք.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Անուն in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # պահեստավորել_արժեք/կատարել_հրաման 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Հրահանգ(['make', '-C', str(self.արմատ_արժեք / 'os'), 'iso']), end='')
        원본 = self.արմատ_արժեք / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        նպատակակետ_արժեք = self.Ճանապարհ(매체)
        նպատակակետ_արժեք.parent.mkdir(exist_ok=True)
        if նպատակակետ_արժեք.exists():
            if 검사합(նպատակակետ_արժեք) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(նպատակակետ_արժեք))
        else:
            with tempfile.NamedTemporaryFile(dir=str(նպատակակետ_արժեք.parent)) as Ֆայլ:
                shutil.copyfile(str(원본), Ֆայլ.name)
                os.link(Ֆայլ.name, str(նպատակակետ_արժեք))

        if վիճակ_արժեք is None:
            վիճակ_արժեք = {'version': 1, 'name': self.Անուն, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.պահեստավորել_արժեք(վիճակ_արժեք)
        if Համակարգի_տեղեկություն is None:
            self.Հրահանգ(['VBoxManage', 'createvm', '--name', վիճակ_արժեք['name'], '--uuid', վիճակ_արժեք['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Ճանապարհ('machines')), '--register'])
            self.Հրահանգ(['VBoxManage', 'setextradata', վիճակ_արժեք['uuid'], 'JKOROS/Owner', վիճակ_արժեք['owner']])
        # կառուցել_համակարգ 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        Համակարգի_տեղեկություն = self.Համակարգի_տեղեկություն(վիճակ_արժեք, 등록목록(self.Հրահանգ(['VBoxManage', 'list', 'vms'])))
        if Համակարգի_տեղեկություն.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('կառուցել_համակարգ 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(վիճակ_արժեք, Համակարգի_տեղեկություն)
        վիճակ_արժեք['iso'] = 매체
        if 매체 not in վիճակ_արժեք['media']: վիճակ_արժեք['media'].append(매체)
        վիճակ_արժեք['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        մատյան_արժեք = self.Ճանապարհ(վիճակ_արժեք['serial_log'])
        մատյան_արժեք.parent.mkdir(exist_ok=True)
        self.պահեստավորել_արժեք(վիճակ_արժեք)
        self.Հրահանգ(['VBoxManage', 'modifyvm', վիճակ_արժեք['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(մատյան_արժեք)])
        제어기들 = [արժեք for Անուն, արժեք in Համակարգի_տեղեկություն.items() if re.fullmatch(r'storagecontrollername\d+', Անուն)]
        if 'JKOROS IDE' not in 제어기들:
            self.Հրահանգ(['VBoxManage', 'storagectl', վիճակ_արժեք['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Հրահանգ(['VBoxManage', 'storageattach', վիճակ_արժեք['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(նպատակակետ_արժեք)])
        վիճակ_արժեք['pending'] = False
        self.պահեստավորել_արժեք(վիճակ_արժեք)
        self.Հրահանգ(['VBoxManage', 'startvm', վիճակ_արժեք['uuid'], '--type', self.եղանակ_կերպ])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.ցուցադրել_վիճակ()


def Գործարկել():
    վերլուծել_արժեք = argparse.ArgumentParser(description='jkoros 전용 VirtualBox կատարել_հրաման 및 վիճակ_արժեք հարցում_արժեք')
    վերլուծել_արժեք.add_argument('action', choices=['run', 'status'])
    인자 = վերլուծել_արժեք.parse_args()
    կատարել_հրաման = ծրագիր_թողարկիչ(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(կատարել_հրաման.ցուցադրել_վիճակ(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. հոստ 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/թույլտվություն_արժեք 변경은 하지 않습니다.')
    os.umask(0o077)
    կատարել_հրաման.Ճանապարհ('lock').parent.mkdir(parents=True, exist_ok=True)
    with կատարել_հրաման.Ճանապարհ('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox կատարել_հրաման 작업이 진행 중입니다.')
        print(json.dumps(կատարել_հրաման.կատարել_հրաման(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Գործարկել()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Սխալ:
        print('VBOX Սխալ: ' + str(Սխալ), file=sys.stderr)
        sys.exit(1)
