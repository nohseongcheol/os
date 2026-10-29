#!/usr/bin/env python3
"""jkoros 전용 VirtualBox барнома_панели_барномаҳо. 기존 VM/디스크/ҳифз_кардан_қимат 상태는 삭제하지 않는다."""
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


def иҷро_кардан_восит_фармон(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(қимат) for қимат in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Мӯҳтаво_қимат = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('фармон нокомӣ_қимат: ' + ' '.join(str(қимат) for қимат in 인수) + '\n' + Мӯҳтаво_қимат[-10000:])
    return Мӯҳтаво_қимат


def сифат_қимат(Мӯҳтаво_қимат):
    결과 = {}
    for хат in Мӯҳтаво_қимат.splitlines():
        if '=' not in хат:
            continue
        Ном, қимат = хат.split('=', 1)
        if Ном.startswith('"'):
            Ном = json.loads(Ном)
        if қимат.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(қимат)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(қимат): қимат = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox сифат_қимат формат_қимат Хато: ' + хат)
        결과[Ном] = қимат
    return 결과


def 등록목록(Мӯҳтаво_қимат):
    결과 = {}
    for хат in Мӯҳтаво_қимат.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', хат)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(масир):
    қимат = hashlib.sha256()
    with масир.open('rb') as Файл:
        for иттилоот in iter(lambda: Файл.read(1024 * 1024), b''): қимат.update(иттилоот)
    return қимат.hexdigest()


class барнома_панели_барномаҳо:
    def __init__(self, 뿌리, Ном, сабк_ҳолат='gui', фармон=иҷро_кардан_восит_фармон):
        self.뿌리 = Path(뿌리).resolve()
        self.Ном, self.сабк_ҳолат, self.фармон = Ном, сабк_ҳолат, фармон
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Ном) or Ном in ('.', '..'):
            raise 실행오류('VM 이름은 문자·рақам_қимат·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if сабк_ҳолат not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def масир(self, ҳамсон_қимат):
        if Path(ҳамсон_қимат).is_absolute() or '..' in Path(ҳамсон_қимат).parts:
            raise 실행오류('잘못된 관리 масир: ' + str(ҳамсон_қимат))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(ҳамсон_қимат).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('ПАЙВАСТ 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def Хондан(self):
        масир = self.масир('state.json')
        if not масир.exists(): return None
        вазъият_қимат = json.loads(масир.read_text(encoding='utf-8'))
        if вазъият_қимат.get('version') != 1 or вазъият_қимат.get('name') != self.Ном:
            raise 실행오류('관리 상태의 VM Ном/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Ном in ('uuid', 'owner'):
            if str(uuid.UUID(вазъият_қимат[Ном])) != вазъият_қимат[Ном]: raise 실행오류('잘못된 VM идентификатор_қимат')
        return вазъият_қимат

    def ҳифз_кардан_қимат(self, вазъият_қимат):
        ҷои_таъинот_қимат = self.масир('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Файл:
            json.dump(вазъият_қимат, Файл, ensure_ascii=False, indent=2)
            Файл.write('\n')
            임시 = Файл.name
        os.replace(임시, str(ҷои_таъинот_қимат))

    def Маълумоти_система(self, вазъият_қимат, 등록됨, барқарор_кардан_вазъият=False):
        if вазъият_қимат['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        Маълумоти_система = сифат_қимат(self.фармон(['VBoxManage', 'showvminfo', вазъият_қимат['uuid'], '--machinereadable']))
        위치 = Path(Маълумоти_система.get('CfgFile', '')).resolve()
        if self.масир('machines').resolve() not in 위치.parents or Маълумоти_система.get('UUID') != вазъият_қимат['uuid']:
            raise 실행오류('이 프로젝트의 VM Танзимот масир/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.фармон(['VBoxManage', 'getextradata', вазъият_қимат['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + вазъият_қимат['owner']:
            if барқарор_кардан_вазъият and вазъият_қимат.get('pending') and 표식 == 'No value set!':
                self.фармон(['VBoxManage', 'setextradata', вазъият_қимат['uuid'], 'JKOROS/Owner', вазъият_қимат['owner']])
            else:
                raise 실행오류('VM молик_қимат 표식이 일치하지 않아 변경하지 않습니다.')
        return Маълумоти_система

    def санҷиш_медиа(self, вазъият_қимат, Маълумоти_система):
        제어기들 = [қимат for Ном, қимат in Маълумоти_система.items() if re.fullmatch(r'storagecontrollername\d+', Ном)]
        Иҷозат_қимат = [str(self.масир(қимат)) for қимат in вазъият_қимат.get('media', [])]
        for Ном, қимат in Маълумоти_система.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', Ном) for 제어기 in 제어기들):
                if қимат not in ('none', 'emptydrive') and қимат not in Иҷозат_қимат:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + қимат)

    def намоиш_додан_вазъият(self):
        вазъият_қимат = self.Хондан()
        if вазъият_қимат is None: return {'name': self.Ном, 'state': 'not-created'}
        Маълумоти_система = self.Маълумоти_система(вазъият_қимат, 등록목록(self.фармон(['VBoxManage', 'list', 'vms'])))
        return {'name': Маълумоти_система.get('name', вазъият_қимат['name']), 'uuid': вазъият_қимат['uuid'], 'state': Маълумоти_система.get('VMState'),
                'iso': str(self.масир(вазъият_қимат['iso'])) if вазъият_қимат.get('iso') else None,
                'serial_log': str(self.масир(вазъият_қимат['serial_log'])) if вазъият_қимат.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def иҷро_кардан_фармон(self):
        вазъият_қимат = self.Хондан()
        등록됨 = 등록목록(self.фармон(['VBoxManage', 'list', 'vms']))
        Маълумоти_система = None
        if вазъият_қимат is not None and вазъият_қимат['uuid'] in 등록됨:
            Маълумоти_система = self.Маълумоти_система(вазъият_қимат, 등록됨, барқарор_кардан_вазъият=True)
            현재 = Маълумоти_система.get('VMState')
            if 현재 == 'running':
                print('이미 иҷро_кардан_фармон 중입니다. 재빌드·재시작하지 않습니다.')
                return self.намоиш_додан_вазъият()
            self.санҷиш_медиа(вазъият_қимат, Маълумоти_система)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 ҳифз_кардан_қимат 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.фармон(['VBoxManage', 'controlvm', вазъият_қимат['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 кушодан 전에 기존 기록도 보관한다.
                    if вазъият_қимат.get('serial_log'):
                        원본 = self.масир(вазъият_қимат['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.масир('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.фармон(['VBoxManage', 'startvm', вазъият_қимат['uuid'], '--type', self.сабк_ҳолат])
                return self.намоиш_додан_вазъият()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 қатъу_васл_кардан_ҳолат 중입니다 ({}). 작업이 끝난 Бозгашт_қимат 다시 실행하세요.'.format(현재))
        elif вазъият_қимат is not None and not вазъият_қимат.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Ном in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # ҳифз_кардан_қимат/иҷро_кардан_фармон 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.фармон(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        медиа_қимат = 'media/kernel-' + 검사합(원본) + '.iso'
        ҷои_таъинот_қимат = self.масир(медиа_қимат)
        ҷои_таъинот_қимат.parent.mkdir(exist_ok=True)
        if ҷои_таъинот_қимат.exists():
            if 검사합(ҷои_таъинот_қимат) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(ҷои_таъинот_қимат))
        else:
            with tempfile.NamedTemporaryFile(dir=str(ҷои_таъинот_қимат.parent)) as Файл:
                shutil.copyfile(str(원본), Файл.name)
                os.link(Файл.name, str(ҷои_таъинот_қимат))

        if вазъият_қимат is None:
            вазъият_қимат = {'version': 1, 'name': self.Ном, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.ҳифз_кардан_қимат(вазъият_қимат)
        if Маълумоти_система is None:
            self.фармон(['VBoxManage', 'createvm', '--name', вазъият_қимат['name'], '--uuid', вазъият_қимат['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.масир('machines')), '--register'])
            self.фармон(['VBoxManage', 'setextradata', вазъият_қимат['uuid'], 'JKOROS/Owner', вазъият_қимат['owner']])
        # сохт_система 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        Маълумоти_система = self.Маълумоти_система(вазъият_қимат, 등록목록(self.фармон(['VBoxManage', 'list', 'vms'])))
        if Маълумоти_система.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('сохт_система 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.санҷиш_медиа(вазъият_қимат, Маълумоти_система)
        вазъият_қимат['iso'] = медиа_қимат
        if медиа_қимат not in вазъият_қимат['media']: вазъият_қимат['media'].append(медиа_қимат)
        вазъият_қимат['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        сабт_кардан_қимат = self.масир(вазъият_қимат['serial_log'])
        сабт_кардан_қимат.parent.mkdir(exist_ok=True)
        self.ҳифз_кардан_қимат(вазъият_қимат)
        self.фармон(['VBoxManage', 'modifyvm', вазъият_қимат['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(сабт_кардан_қимат)])
        제어기들 = [қимат for Ном, қимат in Маълумоти_система.items() if re.fullmatch(r'storagecontrollername\d+', Ном)]
        if 'JKOROS IDE' not in 제어기들:
            self.фармон(['VBoxManage', 'storagectl', вазъият_қимат['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.фармон(['VBoxManage', 'storageattach', вазъият_қимат['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(ҷои_таъинот_қимат)])
        вазъият_қимат['pending'] = False
        self.ҳифз_кардан_қимат(вазъият_қимат)
        self.фармон(['VBoxManage', 'startvm', вазъият_қимат['uuid'], '--type', self.сабк_ҳолат])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.намоиш_додан_вазъият()


def порча():
    해석 = argparse.ArgumentParser(description='jkoros 전용 VirtualBox иҷро_кардан_фармон 및 вазъият_қимат ковиш_қимат')
    해석.add_argument('action', choices=['run', 'status'])
    인자 = 해석.parse_args()
    иҷро_кардан_фармон = барнома_панели_барномаҳо(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(иҷро_кардан_фармон.намоиш_додан_вазъият(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. мизбон 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/иҷозат_қимат 변경은 하지 않습니다.')
    os.umask(0o077)
    иҷро_кардан_фармон.масир('lock').parent.mkdir(parents=True, exist_ok=True)
    with иҷро_кардан_фармон.масир('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox иҷро_кардан_фармон 작업이 진행 중입니다.')
        print(json.dumps(иҷро_кардан_фармон.иҷро_кардан_фармон(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: порча()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Хато:
        print('VBOX Хато: ' + str(Хато), file=sys.stderr)
        sys.exit(1)
