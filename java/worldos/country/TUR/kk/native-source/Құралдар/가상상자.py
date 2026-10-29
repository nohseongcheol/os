#!/usr/bin/env python3
"""jkoros 전용 VirtualBox бағдарлама_іске_қосу_құралы. 기존 VM/디스크/сақтау_мән 상태는 삭제하지 않는다."""
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


def орындау_қоршам_пәрмен(Аргументтер):
    환경 = dict(os.environ, LC_ALL='C')
    НӘТИЖЕ = subprocess.run([str(мән) for мән in Аргументтер], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    мазмұн_мән = НӘТИЖЕ.stdout.decode('utf-8', 'replace')
    if НӘТИЖЕ.returncode:
        raise 실행오류('Команда қате_мән: ' + ' '.join(str(мән) for мән in Аргументтер) + '\n' + мазмұн_мән[-10000:])
    return мазмұн_мән


def атрибут_мән(мазмұн_мән):
    НӘТИЖЕ = {}
    for Жол in мазмұн_мән.splitlines():
        if '=' not in Жол:
            continue
        Аты, мән = Жол.split('=', 1)
        if Аты.startswith('"'):
            Аты = json.loads(Аты)
        if мән.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(мән)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(мән): мән = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox атрибут_мән пішім_мән Қате: ' + Жол)
        НӘТИЖЕ[Аты] = мән
    return НӘТИЖЕ


def 등록목록(мазмұн_мән):
    НӘТИЖЕ = {}
    for Жол in мазмұн_мән.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Жол)
        if 일치: НӘТИЖЕ[일치.group(2).lower()] = 일치.group(1)
    return НӘТИЖЕ


def тексеру_қорытындысы(Жол_2):
    мән = hashlib.sha256()
    with Жол_2.open('rb') as Файл:
        for деректер in iter(lambda: Файл.read(1024 * 1024), b''): мән.update(деректер)
    return мән.hexdigest()


class бағдарлама_іске_қосу_құралы:
    def __init__(self, түбір_мән, Аты, әдіс_режим='gui', Команда=орындау_қоршам_пәрмен):
        self.түбір_мән = Path(түбір_мән).resolve()
        self.Аты, self.әдіс_режим, self.Команда = Аты, әдіс_режим, Команда
        self.보관 = self.түбір_мән / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Аты) or Аты in ('.', '..'):
            raise 실행오류('VM 이름은 문자·сан_мән·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if әдіс_режим not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Жол_2(self, бір_рангілі_мән):
        if Path(бір_рангілі_мән).is_absolute() or '..' in Path(бір_рангілі_мән).parts:
            raise 실행오류('잘못된 관리 Жол_2: ' + str(бір_рангілі_мән))
        НӘТИЖЕ = self.보관
        for 부분 in ['.vbox'] + list(Path(бір_рангілі_мән).parts):
            if 부분 == '.vbox': НӘТИЖЕ = self.보관
            else: НӘТИЖЕ = НӘТИЖЕ / 부분
            if НӘТИЖЕ.is_symlink(): raise 실행오류('Байланысу 경로는 사용하지 않습니다: ' + str(НӘТИЖЕ))
        return НӘТИЖЕ

    def Оқу(self):
        Жол_2 = self.Жол_2('state.json')
        if not Жол_2.exists(): return None
        күй_мән = json.loads(Жол_2.read_text(encoding='utf-8'))
        if күй_мән.get('version') != 1 or күй_мән.get('name') != self.Аты:
            raise 실행오류('관리 상태의 VM Аты/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Аты in ('uuid', 'owner'):
            if str(uuid.UUID(күй_мән[Аты])) != күй_мән[Аты]: raise 실행오류('잘못된 VM идентификатор_мән')
        return күй_мән

    def сақтау_мән(self, күй_мән):
        тағайындау_мән = self.Жол_2('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Файл:
            json.dump(күй_мән, Файл, ensure_ascii=False, indent=2)
            Файл.write('\n')
            임시 = Файл.name
        os.replace(임시, str(тағайындау_мән))

    def Жүйелік_ақпарат(self, күй_мән, 등록됨, қалпына_келу_күй=False):
        if күй_мән['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        Жүйелік_ақпарат = атрибут_мән(self.Команда(['VBoxManage', 'showvminfo', күй_мән['uuid'], '--machinereadable']))
        Орны = Path(Жүйелік_ақпарат.get('CfgFile', '')).resolve()
        if self.Жол_2('machines').resolve() not in Орны.parents or Жүйелік_ақпарат.get('UUID') != күй_мән['uuid']:
            raise 실행오류('이 프로젝트의 VM Баптаулар Жол_2/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Команда(['VBoxManage', 'getextradata', күй_мән['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + күй_мән['owner']:
            if қалпына_келу_күй and күй_мән.get('pending') and 표식 == 'No value set!':
                self.Команда(['VBoxManage', 'setextradata', күй_мән['uuid'], 'JKOROS/Owner', күй_мән['owner']])
            else:
                raise 실행오류('VM ие_мән 표식이 일치하지 않아 변경하지 않습니다.')
        return Жүйелік_ақпарат

    def 매체검사(self, күй_мән, Жүйелік_ақпарат):
        제어기들 = [мән for Аты, мән in Жүйелік_ақпарат.items() if re.fullmatch(r'storagecontrollername\d+', Аты)]
        рұқсат_ету_мән = [str(self.Жол_2(мән)) for мән in күй_мән.get('media', [])]
        for Аты, мән in Жүйелік_ақпарат.items():
            if any(re.fullmatch(re.escape(контроллер) + r'-\d+-\d+', Аты) for контроллер in 제어기들):
                if мән not in ('none', 'emptydrive') and мән not in рұқсат_ету_мән:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + мән)

    def көрсету_күй(self):
        күй_мән = self.Оқу()
        if күй_мән is None: return {'name': self.Аты, 'state': 'not-created'}
        Жүйелік_ақпарат = self.Жүйелік_ақпарат(күй_мән, 등록목록(self.Команда(['VBoxManage', 'list', 'vms'])))
        return {'name': Жүйелік_ақпарат.get('name', күй_мән['name']), 'uuid': күй_мән['uuid'], 'state': Жүйелік_ақпарат.get('VMState'),
                'iso': str(self.Жол_2(күй_мән['iso'])) if күй_мән.get('iso') else None,
                'serial_log': str(self.Жол_2(күй_мән['serial_log'])) if күй_мән.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def орындау_пәрмен(self):
        күй_мән = self.Оқу()
        등록됨 = 등록목록(self.Команда(['VBoxManage', 'list', 'vms']))
        Жүйелік_ақпарат = None
        if күй_мән is not None and күй_мән['uuid'] in 등록됨:
            Жүйелік_ақпарат = self.Жүйелік_ақпарат(күй_мән, 등록됨, қалпына_келу_күй=True)
            ток_элемент = Жүйелік_ақпарат.get('VMState')
            if ток_элемент == 'running':
                print('이미 орындау_пәрмен 중입니다. 재빌드·재시작하지 않습니다.')
                return self.көрсету_күй()
            self.매체검사(күй_мән, Жүйелік_ақпарат)
            if ток_элемент in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 сақтау_мән 상태를 버리지 않습니다.'.format(ток_элемент))
                if ток_элемент == 'paused':
                    self.Команда(['VBoxManage', 'controlvm', күй_мән['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Ашу 전에 기존 기록도 보관한다.
                    if күй_мән.get('serial_log'):
                        원본 = self.Жол_2(күй_мән['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Жол_2('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Команда(['VBoxManage', 'startvm', күй_мән['uuid'], '--type', self.әдіс_режим])
                return self.көрсету_күй()
            if ток_элемент not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 ауысу_режим 중입니다 ({}). 작업이 끝난 АРТҚА_мән 다시 실행하세요.'.format(ток_элемент))
        elif күй_мән is not None and not күй_мән.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Аты in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # сақтау_мән/орындау_пәрмен 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Команда(['make', '-C', str(self.түбір_мән / 'os'), 'iso']), end='')
        원본 = self.түбір_мән / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + тексеру_қорытындысы(원본) + '.iso'
        тағайындау_мән = self.Жол_2(매체)
        тағайындау_мән.parent.mkdir(exist_ok=True)
        if тағайындау_мән.exists():
            if тексеру_қорытындысы(тағайындау_мән) != тексеру_қорытындысы(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(тағайындау_мән))
        else:
            with tempfile.NamedTemporaryFile(dir=str(тағайындау_мән.parent)) as Файл:
                shutil.copyfile(str(원본), Файл.name)
                os.link(Файл.name, str(тағайындау_мән))

        if күй_мән is None:
            күй_мән = {'version': 1, 'name': self.Аты, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.сақтау_мән(күй_мән)
        if Жүйелік_ақпарат is None:
            self.Команда(['VBoxManage', 'createvm', '--name', күй_мән['name'], '--uuid', күй_мән['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Жол_2('machines')), '--register'])
            self.Команда(['VBoxManage', 'setextradata', күй_мән['uuid'], 'JKOROS/Owner', күй_мән['owner']])
        # құрастыру_жүйе 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        Жүйелік_ақпарат = self.Жүйелік_ақпарат(күй_мән, 등록목록(self.Команда(['VBoxManage', 'list', 'vms'])))
        if Жүйелік_ақпарат.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('құрастыру_жүйе 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(күй_мән, Жүйелік_ақпарат)
        күй_мән['iso'] = 매체
        if 매체 not in күй_мән['media']: күй_мән['media'].append(매체)
        күй_мән['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        журнал_мән = self.Жол_2(күй_мән['serial_log'])
        журнал_мән.parent.mkdir(exist_ok=True)
        self.сақтау_мән(күй_мән)
        self.Команда(['VBoxManage', 'modifyvm', күй_мән['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(журнал_мән)])
        제어기들 = [мән for Аты, мән in Жүйелік_ақпарат.items() if re.fullmatch(r'storagecontrollername\d+', Аты)]
        if 'JKOROS IDE' not in 제어기들:
            self.Команда(['VBoxManage', 'storagectl', күй_мән['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Команда(['VBoxManage', 'storageattach', күй_мән['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(тағайындау_мән)])
        күй_мән['pending'] = False
        self.сақтау_мән(күй_мән)
        self.Команда(['VBoxManage', 'startvm', күй_мән['uuid'], '--type', self.әдіс_режим])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.көрсету_күй()


def Орындау_2():
    талдау_мән = argparse.ArgumentParser(description='jkoros 전용 VirtualBox орындау_пәрмен 및 күй_мән сұрау_мән')
    талдау_мән.add_argument('action', choices=['run', 'status'])
    параметр_аргумент = талдау_мән.parse_args()
    орындау_пәрмен = бағдарлама_іске_қосу_құралы(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if параметр_аргумент.action == 'status':
        print(json.dumps(орындау_пәрмен.көрсету_күй(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. орналастыру 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/рұқсат_мән 변경은 하지 않습니다.')
    os.umask(0o077)
    орындау_пәрмен.Жол_2('lock').parent.mkdir(parents=True, exist_ok=True)
    with орындау_пәрмен.Жол_2('lock').open('a') as блоктау_мән:
        try: fcntl.flock(блоктау_мән, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox орындау_пәрмен 작업이 진행 중입니다.')
        print(json.dumps(орындау_пәрмен.орындау_пәрмен(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Орындау_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Қате:
        print('VBOX Қате: ' + str(Қате), file=sys.stderr)
        sys.exit(1)
