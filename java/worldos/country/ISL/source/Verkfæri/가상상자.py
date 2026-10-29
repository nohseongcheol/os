#!/usr/bin/env python3
"""jkoros 전용 VirtualBox forrit_ræsir. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def keyra_skel_skipun(Viðföng):
    환경 = dict(os.environ, LC_ALL='C')
    NIÐURSTAÐA = subprocess.run([str(VALUE) for VALUE in Viðföng], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Efni_VALUE = NIÐURSTAÐA.stdout.decode('utf-8', 'replace')
    if NIÐURSTAÐA.returncode:
        raise 실행오류('Skipun bilun_VALUE: ' + ' '.join(str(VALUE) for VALUE in Viðföng) + '\n' + Efni_VALUE[-10000:])
    return Efni_VALUE


def eigind_VALUE(Efni_VALUE):
    NIÐURSTAÐA = {}
    for Lína in Efni_VALUE.splitlines():
        if '=' not in Lína:
            continue
        Heiti, VALUE = Lína.split('=', 1)
        if Heiti.startswith('"'):
            Heiti = json.loads(Heiti)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox eigind_VALUE snið_VALUE Villa: ' + Lína)
        NIÐURSTAÐA[Heiti] = VALUE
    return NIÐURSTAÐA


def 등록목록(Efni_VALUE):
    NIÐURSTAÐA = {}
    for Lína in Efni_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Lína)
        if 일치: NIÐURSTAÐA[일치.group(2).lower()] = 일치.group(1)
    return NIÐURSTAÐA


def prófsumma(SLÓÐ):
    VALUE = hashlib.sha256()
    with SLÓÐ.open('rb') as Skrá:
        for gögn in iter(lambda: Skrá.read(1024 * 1024), b''): VALUE.update(gögn)
    return VALUE.hexdigest()


class forrit_ræsir:
    def __init__(self, rót_VALUE, Heiti, aðferð_MODE='gui', Skipun=keyra_skel_skipun):
        self.rót_VALUE = Path(rót_VALUE).resolve()
        self.Heiti, self.aðferð_MODE, self.Skipun = Heiti, aðferð_MODE, Skipun
        self.보관 = self.rót_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Heiti) or Heiti in ('.', '..'):
            raise 실행오류('VM 이름은 문자·tölustafur_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 númer 있습니다.')
        if aðferð_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def SLÓÐ(self, jafningi_VALUE):
        if Path(jafningi_VALUE).is_absolute() or '..' in Path(jafningi_VALUE).parts:
            raise 실행오류('잘못된 관리 SLÓÐ: ' + str(jafningi_VALUE))
        NIÐURSTAÐA = self.보관
        for 부분 in ['.vbox'] + list(Path(jafningi_VALUE).parts):
            if 부분 == '.vbox': NIÐURSTAÐA = self.보관
            else: NIÐURSTAÐA = NIÐURSTAÐA / 부분
            if NIÐURSTAÐA.is_symlink(): raise 실행오류('Tengjast 경로는 사용하지 않습니다: ' + str(NIÐURSTAÐA))
        return NIÐURSTAÐA

    def Lestur(self):
        SLÓÐ = self.SLÓÐ('state.json')
        if not SLÓÐ.exists(): return None
        staða_VALUE_e10195a1 = json.loads(SLÓÐ.read_text(encoding='utf-8'))
        if staða_VALUE_e10195a1.get('version') != 1 or staða_VALUE_e10195a1.get('name') != self.Heiti:
            raise 실행오류('관리 상태의 VM Heiti/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Heiti in ('uuid', 'owner'):
            if str(uuid.UUID(staða_VALUE_e10195a1[Heiti])) != staða_VALUE_e10195a1[Heiti]: raise 실행오류('잘못된 VM auðkenni_VALUE')
        return staða_VALUE_e10195a1

    def Store_VALUE(self, staða_VALUE_e10195a1):
        endastaður_VALUE = self.SLÓÐ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Skrá:
            json.dump(staða_VALUE_e10195a1, Skrá, ensure_ascii=False, indent=2)
            Skrá.write('\n')
            임시 = Skrá.name
        os.replace(임시, str(endastaður_VALUE))

    def msinfo32_exe(self, staða_VALUE_e10195a1, 등록됨, endurheimta_staða=False):
        if staða_VALUE_e10195a1['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = eigind_VALUE(self.Skipun(['VBoxManage', 'showvminfo', staða_VALUE_e10195a1['uuid'], '--machinereadable']))
        Staðsetning = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.SLÓÐ('machines').resolve() not in Staðsetning.parents or msinfo32_exe.get('UUID') != staða_VALUE_e10195a1['uuid']:
            raise 실행오류('이 프로젝트의 VM Stillingar SLÓÐ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Skipun(['VBoxManage', 'getextradata', staða_VALUE_e10195a1['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + staða_VALUE_e10195a1['owner']:
            if endurheimta_staða and staða_VALUE_e10195a1.get('pending') and 표식 == 'No value set!':
                self.Skipun(['VBoxManage', 'setextradata', staða_VALUE_e10195a1['uuid'], 'JKOROS/Owner', staða_VALUE_e10195a1['owner']])
            else:
                raise 실행오류('VM eigandi_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, staða_VALUE_e10195a1, msinfo32_exe):
        제어기들 = [VALUE for Heiti, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Heiti)]
        leyfa_VALUE = [str(self.SLÓÐ(VALUE)) for VALUE in staða_VALUE_e10195a1.get('media', [])]
        for Heiti, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(stjórntæki) + r'-\d+-\d+', Heiti) for stjórntæki in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in leyfa_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def sýna_staða(self):
        staða_VALUE_e10195a1 = self.Lestur()
        if staða_VALUE_e10195a1 is None: return {'name': self.Heiti, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(staða_VALUE_e10195a1, 등록목록(self.Skipun(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', staða_VALUE_e10195a1['name']), 'uuid': staða_VALUE_e10195a1['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.SLÓÐ(staða_VALUE_e10195a1['iso'])) if staða_VALUE_e10195a1.get('iso') else None,
                'serial_log': str(self.SLÓÐ(staða_VALUE_e10195a1['serial_log'])) if staða_VALUE_e10195a1.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def keyra_skipun(self):
        staða_VALUE_e10195a1 = self.Lestur()
        등록됨 = 등록목록(self.Skipun(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if staða_VALUE_e10195a1 is not None and staða_VALUE_e10195a1['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(staða_VALUE_e10195a1, 등록됨, endurheimta_staða=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 keyra_skipun 중입니다. 재빌드·재시작하지 않습니다.')
                return self.sýna_staða()
            self.매체검사(staða_VALUE_e10195a1, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Skipun(['VBoxManage', 'controlvm', staða_VALUE_e10195a1['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Opna 전에 기존 기록도 보관한다.
                    if staða_VALUE_e10195a1.get('serial_log'):
                        원본 = self.SLÓÐ(staða_VALUE_e10195a1['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.SLÓÐ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Skipun(['VBoxManage', 'startvm', staða_VALUE_e10195a1['uuid'], '--type', self.aðferð_MODE])
                return self.sýna_staða()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 TIL_BAKA_VALUE 다시 실행하세요.'.format(현재))
        elif staða_VALUE_e10195a1 is not None and not staða_VALUE_e10195a1.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Heiti in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/keyra_skipun 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Skipun(['make', '-C', str(self.rót_VALUE / 'os'), 'iso']), end='')
        원본 = self.rót_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + prófsumma(원본) + '.iso'
        endastaður_VALUE = self.SLÓÐ(매체)
        endastaður_VALUE.parent.mkdir(exist_ok=True)
        if endastaður_VALUE.exists():
            if prófsumma(endastaður_VALUE) != prófsumma(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(endastaður_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(endastaður_VALUE.parent)) as Skrá:
                shutil.copyfile(str(원본), Skrá.name)
                os.link(Skrá.name, str(endastaður_VALUE))

        if staða_VALUE_e10195a1 is None:
            staða_VALUE_e10195a1 = {'version': 1, 'name': self.Heiti, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(staða_VALUE_e10195a1)
        if msinfo32_exe is None:
            self.Skipun(['VBoxManage', 'createvm', '--name', staða_VALUE_e10195a1['name'], '--uuid', staða_VALUE_e10195a1['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.SLÓÐ('machines')), '--register'])
            self.Skipun(['VBoxManage', 'setextradata', staða_VALUE_e10195a1['uuid'], 'JKOROS/Owner', staða_VALUE_e10195a1['owner']])
        # smíð_kerfi 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(staða_VALUE_e10195a1, 등록목록(self.Skipun(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('smíð_kerfi 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(staða_VALUE_e10195a1, msinfo32_exe)
        staða_VALUE_e10195a1['iso'] = 매체
        if 매체 not in staða_VALUE_e10195a1['media']: staða_VALUE_e10195a1['media'].append(매체)
        staða_VALUE_e10195a1['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.SLÓÐ(staða_VALUE_e10195a1['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(staða_VALUE_e10195a1)
        self.Skipun(['VBoxManage', 'modifyvm', staða_VALUE_e10195a1['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Heiti, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Heiti)]
        if 'JKOROS IDE' not in 제어기들:
            self.Skipun(['VBoxManage', 'storagectl', staða_VALUE_e10195a1['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Skipun(['VBoxManage', 'storageattach', staða_VALUE_e10195a1['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(endastaður_VALUE)])
        staða_VALUE_e10195a1['pending'] = False
        self.Store_VALUE(staða_VALUE_e10195a1)
        self.Skipun(['VBoxManage', 'startvm', staða_VALUE_e10195a1['uuid'], '--type', self.aðferð_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.sýna_staða()


def Keyra_2():
    þátta_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox keyra_skipun 및 staða_VALUE_e10195a1 fyrirspurn_VALUE')
    þátta_VALUE.add_argument('action', choices=['run', 'status'])
    færibreyta_frumbreyta = þátta_VALUE.parse_args()
    keyra_skipun = forrit_ræsir(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if færibreyta_frumbreyta.action == 'status':
        print(json.dumps(keyra_skipun.sýna_staða(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 númer 없습니다. hýsa 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/leyfi_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    keyra_skipun.SLÓÐ('lock').parent.mkdir(parents=True, exist_ok=True)
    with keyra_skipun.SLÓÐ('lock').open('a') as Loka_VALUE:
        try: fcntl.flock(Loka_VALUE, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox keyra_skipun 작업이 진행 중입니다.')
        print(json.dumps(keyra_skipun.keyra_skipun(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Keyra_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Villa:
        print('VBOX Villa: ' + str(Villa), file=sys.stderr)
        sys.exit(1)
