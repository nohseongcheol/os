#!/usr/bin/env python3
"""jkoros 전용 VirtualBox programm_käiviti. 기존 VM/디스크/salv_VALUE 상태는 삭제하지 않는다."""
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


def Täida_kest_käsk(Argumendid):
    환경 = dict(os.environ, LC_ALL='C')
    TULEMUS = subprocess.run([str(VALUE) for VALUE in Argumendid], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Sisu_VALUE = TULEMUS.stdout.decode('utf-8', 'replace')
    if TULEMUS.returncode:
        raise 실행오류('Käsk tõrge_VALUE: ' + ' '.join(str(VALUE) for VALUE in Argumendid) + '\n' + Sisu_VALUE[-10000:])
    return Sisu_VALUE


def atribuut_VALUE(Sisu_VALUE):
    TULEMUS = {}
    for Joon in Sisu_VALUE.splitlines():
        if '=' not in Joon:
            continue
        Nimi_2, VALUE = Joon.split('=', 1)
        if Nimi_2.startswith('"'):
            Nimi_2 = json.loads(Nimi_2)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox atribuut_VALUE vorming_VALUE VIGA: ' + Joon)
        TULEMUS[Nimi_2] = VALUE
    return TULEMUS


def 등록목록(Sisu_VALUE):
    TULEMUS = {}
    for Joon in Sisu_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Joon)
        if 일치: TULEMUS[일치.group(2).lower()] = 일치.group(1)
    return TULEMUS


def kontrollsumma(RADA):
    VALUE = hashlib.sha256()
    with RADA.open('rb') as Fail:
        for andmed in iter(lambda: Fail.read(1024 * 1024), b''): VALUE.update(andmed)
    return VALUE.hexdigest()


class programm_käiviti:
    def __init__(self, juur_VALUE, Nimi_2, meetod_MODE='gui', Käsk=Täida_kest_käsk):
        self.juur_VALUE = Path(juur_VALUE).resolve()
        self.Nimi_2, self.meetod_MODE, self.Käsk = Nimi_2, meetod_MODE, Käsk
        self.보관 = self.juur_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Nimi_2) or Nimi_2 in ('.', '..'):
            raise 실행오류('VM 이름은 문자·number_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 number 있습니다.')
        if meetod_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def RADA(self, partner_VALUE):
        if Path(partner_VALUE).is_absolute() or '..' in Path(partner_VALUE).parts:
            raise 실행오류('잘못된 관리 RADA: ' + str(partner_VALUE))
        TULEMUS = self.보관
        for 부분 in ['.vbox'] + list(Path(partner_VALUE).parts):
            if 부분 == '.vbox': TULEMUS = self.보관
            else: TULEMUS = TULEMUS / 부분
            if TULEMUS.is_symlink(): raise 실행오류('Ühendu 경로는 사용하지 않습니다: ' + str(TULEMUS))
        return TULEMUS

    def Lugemine(self):
        RADA = self.RADA('state.json')
        if not RADA.exists(): return None
        Olek_VALUE = json.loads(RADA.read_text(encoding='utf-8'))
        if Olek_VALUE.get('version') != 1 or Olek_VALUE.get('name') != self.Nimi_2:
            raise 실행오류('관리 상태의 VM Nimi_2/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Nimi_2 in ('uuid', 'owner'):
            if str(uuid.UUID(Olek_VALUE[Nimi_2])) != Olek_VALUE[Nimi_2]: raise 실행오류('잘못된 VM identifikaator_VALUE')
        return Olek_VALUE

    def salv_VALUE(self, Olek_VALUE):
        sihtkoht_VALUE = self.RADA('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Fail:
            json.dump(Olek_VALUE, Fail, ensure_ascii=False, indent=2)
            Fail.write('\n')
            임시 = Fail.name
        os.replace(임시, str(sihtkoht_VALUE))

    def msinfo32_exe(self, Olek_VALUE, 등록됨, taastama_Olek=False):
        if Olek_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = atribuut_VALUE(self.Käsk(['VBoxManage', 'showvminfo', Olek_VALUE['uuid'], '--machinereadable']))
        Asukoht = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.RADA('machines').resolve() not in Asukoht.parents or msinfo32_exe.get('UUID') != Olek_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Seaded RADA/UUID와 일치하지 않아 변경하지 않습니다.')
        marker_VALUE = self.Käsk(['VBoxManage', 'getextradata', Olek_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if marker_VALUE != 'Value: ' + Olek_VALUE['owner']:
            if taastama_Olek and Olek_VALUE.get('pending') and marker_VALUE == 'No value set!':
                self.Käsk(['VBoxManage', 'setextradata', Olek_VALUE['uuid'], 'JKOROS/Owner', Olek_VALUE['owner']])
            else:
                raise 실행오류('VM omanik_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, Olek_VALUE, msinfo32_exe):
        제어기들 = [VALUE for Nimi_2, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nimi_2)]
        Luba_VALUE = [str(self.RADA(VALUE)) for VALUE in Olek_VALUE.get('media', [])]
        for Nimi_2, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(kontroller) + r'-\d+-\d+', Nimi_2) for kontroller in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Luba_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def saade_Olek(self):
        Olek_VALUE = self.Lugemine()
        if Olek_VALUE is None: return {'name': self.Nimi_2, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Olek_VALUE, 등록목록(self.Käsk(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Olek_VALUE['name']), 'uuid': Olek_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.RADA(Olek_VALUE['iso'])) if Olek_VALUE.get('iso') else None,
                'serial_log': str(self.RADA(Olek_VALUE['serial_log'])) if Olek_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Täida_käsk(self):
        Olek_VALUE = self.Lugemine()
        등록됨 = 등록목록(self.Käsk(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Olek_VALUE is not None and Olek_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Olek_VALUE, 등록됨, taastama_Olek=True)
            tähtaja_piires_kaup = msinfo32_exe.get('VMState')
            if tähtaja_piires_kaup == 'running':
                print('이미 Täida_käsk 중입니다. 재빌드·재시작하지 않습니다.')
                return self.saade_Olek()
            self.매체검사(Olek_VALUE, msinfo32_exe)
            if tähtaja_piires_kaup in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 salv_VALUE 상태를 버리지 않습니다.'.format(tähtaja_piires_kaup))
                if tähtaja_piires_kaup == 'paused':
                    self.Käsk(['VBoxManage', 'controlvm', Olek_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 uuesti_proovima_VALUE Ava 전에 기존 기록도 보관한다.
                    if Olek_VALUE.get('serial_log'):
                        원본 = self.RADA(Olek_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.RADA('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Käsk(['VBoxManage', 'startvm', Olek_VALUE['uuid'], '--type', self.meetod_MODE])
                return self.saade_Olek()
            if tähtaja_piires_kaup not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 Tagasi_VALUE uuesti_proovima_VALUE 실행하세요.'.format(tähtaja_piires_kaup))
        elif Olek_VALUE is not None and not Olek_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 uuesti_proovima_VALUE 등록하세요.')
        elif self.Nimi_2 in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # salv_VALUE/Täida_käsk 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Käsk(['make', '-C', str(self.juur_VALUE / 'os'), 'iso']), end='')
        원본 = self.juur_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + kontrollsumma(원본) + '.iso'
        sihtkoht_VALUE = self.RADA(매체)
        sihtkoht_VALUE.parent.mkdir(exist_ok=True)
        if sihtkoht_VALUE.exists():
            if kontrollsumma(sihtkoht_VALUE) != kontrollsumma(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(sihtkoht_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(sihtkoht_VALUE.parent)) as Fail:
                shutil.copyfile(str(원본), Fail.name)
                os.link(Fail.name, str(sihtkoht_VALUE))

        if Olek_VALUE is None:
            Olek_VALUE = {'version': 1, 'name': self.Nimi_2, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.salv_VALUE(Olek_VALUE)
        if msinfo32_exe is None:
            self.Käsk(['VBoxManage', 'createvm', '--name', Olek_VALUE['name'], '--uuid', Olek_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.RADA('machines')), '--register'])
            self.Käsk(['VBoxManage', 'setextradata', Olek_VALUE['uuid'], 'JKOROS/Owner', Olek_VALUE['owner']])
        # järk_süsteem 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Olek_VALUE, 등록목록(self.Käsk(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('järk_süsteem 중 VM 상태가 바뀌었습니다. uuesti_proovima_VALUE make vbox를 실행하세요.')
        self.매체검사(Olek_VALUE, msinfo32_exe)
        Olek_VALUE['iso'] = 매체
        if 매체 not in Olek_VALUE['media']: Olek_VALUE['media'].append(매체)
        Olek_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.RADA(Olek_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.salv_VALUE(Olek_VALUE)
        self.Käsk(['VBoxManage', 'modifyvm', Olek_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Nimi_2, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nimi_2)]
        if 'JKOROS IDE' not in 제어기들:
            self.Käsk(['VBoxManage', 'storagectl', Olek_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Käsk(['VBoxManage', 'storageattach', Olek_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(sihtkoht_VALUE)])
        Olek_VALUE['pending'] = False
        self.salv_VALUE(Olek_VALUE)
        self.Käsk(['VBoxManage', 'startvm', Olek_VALUE['uuid'], '--type', self.meetod_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.saade_Olek()


def Käivita_2():
    sõeluma_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Täida_käsk 및 Olek_VALUE päring_VALUE')
    sõeluma_VALUE.add_argument('action', choices=['run', 'status'])
    parameeter_argument = sõeluma_VALUE.parse_args()
    Täida_käsk = programm_käiviti(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parameeter_argument.action == 'status':
        print(json.dumps(Täida_käsk.saade_Olek(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 number 없습니다. host 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/luba_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    Täida_käsk.RADA('lock').parent.mkdir(parents=True, exist_ok=True)
    with Täida_käsk.RADA('lock').open('a') as lukk_VALUE:
        try: fcntl.flock(lukk_VALUE, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Täida_käsk 작업이 진행 중입니다.')
        print(json.dumps(Täida_käsk.Täida_käsk(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Käivita_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as VIGA:
        print('VBOX VIGA: ' + str(VIGA), file=sys.stderr)
        sys.exit(1)
