#!/usr/bin/env python3
"""jkoros 전용 VirtualBox programma_programma_paneli. 기존 VM/디스크/Store_baha 상태는 삭제하지 않는다."""
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


def ýerine_ýetir_gabyjak_buýruk(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(baha) for baha in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Mazmun_baha = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('buýruk näsazlyk_baha: ' + ' '.join(str(baha) for baha in 인수) + '\n' + Mazmun_baha[-10000:])
    return Mazmun_baha


def alamat_baha(Mazmun_baha):
    결과 = {}
    for setir in Mazmun_baha.splitlines():
        if '=' not in setir:
            continue
        Ad, baha = setir.split('=', 1)
        if Ad.startswith('"'):
            Ad = json.loads(Ad)
        if baha.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(baha)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(baha): baha = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox alamat_baha format_baha Hata: ' + setir)
        결과[Ad] = baha
    return 결과


def 등록목록(Mazmun_baha):
    결과 = {}
    for setir in Mazmun_baha.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', setir)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(Ýol):
    baha = hashlib.sha256()
    with Ýol.open('rb') as Faýl:
        for maglumat in iter(lambda: Faýl.read(1024 * 1024), b''): baha.update(maglumat)
    return baha.hexdigest()


class programma_programma_paneli:
    def __init__(self, 뿌리, Ad, usul_reje='gui', buýruk=ýerine_ýetir_gabyjak_buýruk):
        self.뿌리 = Path(뿌리).resolve()
        self.Ad, self.usul_reje, self.buýruk = Ad, usul_reje, buýruk
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Ad) or Ad in ('.', '..'):
            raise 실행오류('VM 이름은 문자·san_baha·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if usul_reje not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Ýol(self, deň_derejeli_düwün_baha):
        if Path(deň_derejeli_düwün_baha).is_absolute() or '..' in Path(deň_derejeli_düwün_baha).parts:
            raise 실행오류('잘못된 관리 Ýol: ' + str(deň_derejeli_düwün_baha))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(deň_derejeli_düwün_baha).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('Birikme 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def Oka(self):
        Ýol = self.Ýol('state.json')
        if not Ýol.exists(): return None
        ýagdaý_baha = json.loads(Ýol.read_text(encoding='utf-8'))
        if ýagdaý_baha.get('version') != 1 or ýagdaý_baha.get('name') != self.Ad:
            raise 실행오류('관리 상태의 VM Ad/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Ad in ('uuid', 'owner'):
            if str(uuid.UUID(ýagdaý_baha[Ad])) != ýagdaý_baha[Ad]: raise 실행오류('잘못된 VM tanaýjy_baha')
        return ýagdaý_baha

    def Store_baha(self, ýagdaý_baha):
        barylmaly_ýer_baha = self.Ýol('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Faýl:
            json.dump(ýagdaý_baha, Faýl, ensure_ascii=False, indent=2)
            Faýl.write('\n')
            임시 = Faýl.name
        os.replace(임시, str(barylmaly_ýer_baha))

    def msinfo32_exe(self, ýagdaý_baha, 등록됨, dikelt_ýagdaý=False):
        if ýagdaý_baha['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = alamat_baha(self.buýruk(['VBoxManage', 'showvminfo', ýagdaý_baha['uuid'], '--machinereadable']))
        위치 = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.Ýol('machines').resolve() not in 위치.parents or msinfo32_exe.get('UUID') != ýagdaý_baha['uuid']:
            raise 실행오류('이 프로젝트의 VM Düzümler Ýol/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.buýruk(['VBoxManage', 'getextradata', ýagdaý_baha['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + ýagdaý_baha['owner']:
            if dikelt_ýagdaý and ýagdaý_baha.get('pending') and 표식 == 'No value set!':
                self.buýruk(['VBoxManage', 'setextradata', ýagdaý_baha['uuid'], 'JKOROS/Owner', ýagdaý_baha['owner']])
            else:
                raise 실행오류('VM eýe_baha 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, ýagdaý_baha, msinfo32_exe):
        제어기들 = [baha for Ad, baha in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Ad)]
        Rugsat_ber_baha = [str(self.Ýol(baha)) for baha in ýagdaý_baha.get('media', [])]
        for Ad, baha in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', Ad) for 제어기 in 제어기들):
                if baha not in ('none', 'emptydrive') and baha not in Rugsat_ber_baha:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + baha)

    def görkez_ýagdaý(self):
        ýagdaý_baha = self.Oka()
        if ýagdaý_baha is None: return {'name': self.Ad, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(ýagdaý_baha, 등록목록(self.buýruk(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', ýagdaý_baha['name']), 'uuid': ýagdaý_baha['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.Ýol(ýagdaý_baha['iso'])) if ýagdaý_baha.get('iso') else None,
                'serial_log': str(self.Ýol(ýagdaý_baha['serial_log'])) if ýagdaý_baha.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def ýerine_ýetir_buýruk(self):
        ýagdaý_baha = self.Oka()
        등록됨 = 등록목록(self.buýruk(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if ýagdaý_baha is not None and ýagdaý_baha['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(ýagdaý_baha, 등록됨, dikelt_ýagdaý=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 ýerine_ýetir_buýruk 중입니다. 재빌드·재시작하지 않습니다.')
                return self.görkez_ýagdaý()
            self.매체검사(ýagdaý_baha, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_baha 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.buýruk(['VBoxManage', 'controlvm', ýagdaý_baha['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Aç 전에 기존 기록도 보관한다.
                    if ýagdaý_baha.get('serial_log'):
                        원본 = self.Ýol(ýagdaý_baha['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Ýol('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.buýruk(['VBoxManage', 'startvm', ýagdaý_baha['uuid'], '--type', self.usul_reje])
                return self.görkez_ýagdaý()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 calşyr_reje 중입니다 ({}). 작업이 끝난 Yza_baha 다시 실행하세요.'.format(현재))
        elif ýagdaý_baha is not None and not ýagdaý_baha.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Ad in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_baha/ýerine_ýetir_buýruk 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.buýruk(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        barylmaly_ýer_baha = self.Ýol(매체)
        barylmaly_ýer_baha.parent.mkdir(exist_ok=True)
        if barylmaly_ýer_baha.exists():
            if 검사합(barylmaly_ýer_baha) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(barylmaly_ýer_baha))
        else:
            with tempfile.NamedTemporaryFile(dir=str(barylmaly_ýer_baha.parent)) as Faýl:
                shutil.copyfile(str(원본), Faýl.name)
                os.link(Faýl.name, str(barylmaly_ýer_baha))

        if ýagdaý_baha is None:
            ýagdaý_baha = {'version': 1, 'name': self.Ad, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_baha(ýagdaý_baha)
        if msinfo32_exe is None:
            self.buýruk(['VBoxManage', 'createvm', '--name', ýagdaý_baha['name'], '--uuid', ýagdaý_baha['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Ýol('machines')), '--register'])
            self.buýruk(['VBoxManage', 'setextradata', ýagdaý_baha['uuid'], 'JKOROS/Owner', ýagdaý_baha['owner']])
        # düz_ulgam 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(ýagdaý_baha, 등록목록(self.buýruk(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('düz_ulgam 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(ýagdaý_baha, msinfo32_exe)
        ýagdaý_baha['iso'] = 매체
        if 매체 not in ýagdaý_baha['media']: ýagdaý_baha['media'].append(매체)
        ýagdaý_baha['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        hasaba_alyş_baha = self.Ýol(ýagdaý_baha['serial_log'])
        hasaba_alyş_baha.parent.mkdir(exist_ok=True)
        self.Store_baha(ýagdaý_baha)
        self.buýruk(['VBoxManage', 'modifyvm', ýagdaý_baha['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(hasaba_alyş_baha)])
        제어기들 = [baha for Ad, baha in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Ad)]
        if 'JKOROS IDE' not in 제어기들:
            self.buýruk(['VBoxManage', 'storagectl', ýagdaý_baha['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.buýruk(['VBoxManage', 'storageattach', ýagdaý_baha['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(barylmaly_ýer_baha)])
        ýagdaý_baha['pending'] = False
        self.Store_baha(ýagdaý_baha)
        self.buýruk(['VBoxManage', 'startvm', ýagdaý_baha['uuid'], '--type', self.usul_reje])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.görkez_ýagdaý()


def Bitir():
    seljer_baha = argparse.ArgumentParser(description='jkoros 전용 VirtualBox ýerine_ýetir_buýruk 및 ýagdaý_baha talap_baha')
    seljer_baha.add_argument('action', choices=['run', 'status'])
    인자 = seljer_baha.parse_args()
    ýerine_ýetir_buýruk = programma_programma_paneli(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(ýerine_ýetir_buýruk.görkez_ýagdaý(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. esasy 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/rugsat_baha 변경은 하지 않습니다.')
    os.umask(0o077)
    ýerine_ýetir_buýruk.Ýol('lock').parent.mkdir(parents=True, exist_ok=True)
    with ýerine_ýetir_buýruk.Ýol('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox ýerine_ýetir_buýruk 작업이 진행 중입니다.')
        print(json.dumps(ýerine_ýetir_buýruk.ýerine_ýetir_buýruk(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Bitir()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Hata:
        print('VBOX Hata: ' + str(Hata), file=sys.stderr)
        sys.exit(1)
