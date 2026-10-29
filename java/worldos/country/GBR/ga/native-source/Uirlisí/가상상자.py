#!/usr/bin/env python3
"""jkoros 전용 VirtualBox clár_tarraiceán_feidhmchlár. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def Rith_blaosc_ordú(Argóintí):
    환경 = dict(os.environ, LC_ALL='C')
    tomhas = subprocess.run([str(VALUE) for VALUE in Argóintí], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Inneachar_VALUE = tomhas.stdout.decode('utf-8', 'replace')
    if tomhas.returncode:
        raise 실행오류('Ordú teip_VALUE: ' + ' '.join(str(VALUE) for VALUE in Argóintí) + '\n' + Inneachar_VALUE[-10000:])
    return Inneachar_VALUE


def tréith_VALUE(Inneachar_VALUE):
    tomhas = {}
    for Líne in Inneachar_VALUE.splitlines():
        if '=' not in Líne:
            continue
        Ainm, VALUE = Líne.split('=', 1)
        if Ainm.startswith('"'):
            Ainm = json.loads(Ainm)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox tréith_VALUE formáid_VALUE ERREÁID: ' + Líne)
        tomhas[Ainm] = VALUE
    return tomhas


def 등록목록(Inneachar_VALUE):
    tomhas = {}
    for Líne in Inneachar_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Líne)
        if 일치: tomhas[일치.group(2).lower()] = 일치.group(1)
    return tomhas


def suim_seiceála(CONAIR):
    VALUE = hashlib.sha256()
    with CONAIR.open('rb') as Comhad:
        for sonraí in iter(lambda: Comhad.read(1024 * 1024), b''): VALUE.update(sonraí)
    return VALUE.hexdigest()


class clár_tarraiceán_feidhmchlár:
    def __init__(self, fréamh_VALUE, Ainm, modh_mód='gui', Ordú=Rith_blaosc_ordú):
        self.fréamh_VALUE = Path(fréamh_VALUE).resolve()
        self.Ainm, self.modh_mód, self.Ordú = Ainm, modh_mód, Ordú
        self.보관 = self.fréamh_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Ainm) or Ainm in ('.', '..'):
            raise 실행오류('VM 이름은 문자·digit_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if modh_mód not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def CONAIR(self, piara_VALUE):
        if Path(piara_VALUE).is_absolute() or '..' in Path(piara_VALUE).parts:
            raise 실행오류('잘못된 관리 CONAIR: ' + str(piara_VALUE))
        tomhas = self.보관
        for 부분 in ['.vbox'] + list(Path(piara_VALUE).parts):
            if 부분 == '.vbox': tomhas = self.보관
            else: tomhas = tomhas / 부분
            if tomhas.is_symlink(): raise 실행오류('Nasc 경로는 사용하지 않습니다: ' + str(tomhas))
        return tomhas

    def Léigh(self):
        CONAIR = self.CONAIR('state.json')
        if not CONAIR.exists(): return None
        staid_VALUE = json.loads(CONAIR.read_text(encoding='utf-8'))
        if staid_VALUE.get('version') != 1 or staid_VALUE.get('name') != self.Ainm:
            raise 실행오류('관리 상태의 VM Ainm/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Ainm in ('uuid', 'owner'):
            if str(uuid.UUID(staid_VALUE[Ainm])) != staid_VALUE[Ainm]: raise 실행오류('잘못된 VM aitheantóir_VALUE')
        return staid_VALUE

    def Store_VALUE(self, staid_VALUE):
        sprioc_VALUE = self.CONAIR('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Comhad:
            json.dump(staid_VALUE, Comhad, ensure_ascii=False, indent=2)
            Comhad.write('\n')
            임시 = Comhad.name
        os.replace(임시, str(sprioc_VALUE))

    def msinfo32_exe(self, staid_VALUE, 등록됨, athshlánaigh_staid=False):
        if staid_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = tréith_VALUE(self.Ordú(['VBoxManage', 'showvminfo', staid_VALUE['uuid'], '--machinereadable']))
        suíomh = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.CONAIR('machines').resolve() not in suíomh.parents or msinfo32_exe.get('UUID') != staid_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Socruithe CONAIR/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Ordú(['VBoxManage', 'getextradata', staid_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + staid_VALUE['owner']:
            if athshlánaigh_staid and staid_VALUE.get('pending') and 표식 == 'No value set!':
                self.Ordú(['VBoxManage', 'setextradata', staid_VALUE['uuid'], 'JKOROS/Owner', staid_VALUE['owner']])
            else:
                raise 실행오류('VM úinéir_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, staid_VALUE, msinfo32_exe):
        제어기들 = [VALUE for Ainm, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Ainm)]
        Ceadaigh_VALUE = [str(self.CONAIR(VALUE)) for VALUE in staid_VALUE.get('media', [])]
        for Ainm, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(rialaitheoir) + r'-\d+-\d+', Ainm) for rialaitheoir in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Ceadaigh_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def seó_staid(self):
        staid_VALUE = self.Léigh()
        if staid_VALUE is None: return {'name': self.Ainm, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(staid_VALUE, 등록목록(self.Ordú(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', staid_VALUE['name']), 'uuid': staid_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.CONAIR(staid_VALUE['iso'])) if staid_VALUE.get('iso') else None,
                'serial_log': str(self.CONAIR(staid_VALUE['serial_log'])) if staid_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Rith_ordú(self):
        staid_VALUE = self.Léigh()
        등록됨 = 등록목록(self.Ordú(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if staid_VALUE is not None and staid_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(staid_VALUE, 등록됨, athshlánaigh_staid=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 Rith_ordú 중입니다. 재빌드·재시작하지 않습니다.')
                return self.seó_staid()
            self.매체검사(staid_VALUE, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Ordú(['VBoxManage', 'controlvm', staid_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Oscail 전에 기존 기록도 보관한다.
                    if staid_VALUE.get('serial_log'):
                        원본 = self.CONAIR(staid_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.CONAIR('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Ordú(['VBoxManage', 'startvm', staid_VALUE['uuid'], '--type', self.modh_mód])
                return self.seó_staid()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_mód 중입니다 ({}). 작업이 끝난 Siar_VALUE 다시 실행하세요.'.format(현재))
        elif staid_VALUE is not None and not staid_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Ainm in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/Rith_ordú 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Ordú(['make', '-C', str(self.fréamh_VALUE / 'os'), 'iso']), end='')
        원본 = self.fréamh_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + suim_seiceála(원본) + '.iso'
        sprioc_VALUE = self.CONAIR(매체)
        sprioc_VALUE.parent.mkdir(exist_ok=True)
        if sprioc_VALUE.exists():
            if suim_seiceála(sprioc_VALUE) != suim_seiceála(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(sprioc_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(sprioc_VALUE.parent)) as Comhad:
                shutil.copyfile(str(원본), Comhad.name)
                os.link(Comhad.name, str(sprioc_VALUE))

        if staid_VALUE is None:
            staid_VALUE = {'version': 1, 'name': self.Ainm, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(staid_VALUE)
        if msinfo32_exe is None:
            self.Ordú(['VBoxManage', 'createvm', '--name', staid_VALUE['name'], '--uuid', staid_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.CONAIR('machines')), '--register'])
            self.Ordú(['VBoxManage', 'setextradata', staid_VALUE['uuid'], 'JKOROS/Owner', staid_VALUE['owner']])
        # tóg_córas 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(staid_VALUE, 등록목록(self.Ordú(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('tóg_córas 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(staid_VALUE, msinfo32_exe)
        staid_VALUE['iso'] = 매체
        if 매체 not in staid_VALUE['media']: staid_VALUE['media'].append(매체)
        staid_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.CONAIR(staid_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(staid_VALUE)
        self.Ordú(['VBoxManage', 'modifyvm', staid_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Ainm, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Ainm)]
        if 'JKOROS IDE' not in 제어기들:
            self.Ordú(['VBoxManage', 'storagectl', staid_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Ordú(['VBoxManage', 'storageattach', staid_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(sprioc_VALUE)])
        staid_VALUE['pending'] = False
        self.Store_VALUE(staid_VALUE)
        self.Ordú(['VBoxManage', 'startvm', staid_VALUE['uuid'], '--type', self.modh_mód])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.seó_staid()


def Rith_2():
    parsáil_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Rith_ordú 및 staid_VALUE iarratas_VALUE')
    parsáil_VALUE.add_argument('action', choices=['run', 'status'])
    paraiméadar_argóint = parsáil_VALUE.parse_args()
    Rith_ordú = clár_tarraiceán_feidhmchlár(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if paraiméadar_argóint.action == 'status':
        print(json.dumps(Rith_ordú.seó_staid(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. óstach 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/cead_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    Rith_ordú.CONAIR('lock').parent.mkdir(parents=True, exist_ok=True)
    with Rith_ordú.CONAIR('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Rith_ordú 작업이 진행 중입니다.')
        print(json.dumps(Rith_ordú.Rith_ordú(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Rith_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ERREÁID:
        print('VBOX ERREÁID: ' + str(ERREÁID), file=sys.stderr)
        sys.exit(1)
