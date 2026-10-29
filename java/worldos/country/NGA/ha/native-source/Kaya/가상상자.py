#!/usr/bin/env python3
"""jkoros 전용 VirtualBox Shiri_Mai_Fara_Ka_ida. 기존 VM/디스크/Ajiye_Daraja 상태는 삭제하지 않는다."""
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


def gudanar_Mai_fayyace_umani_Umarni(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(Daraja) for Daraja in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    kunshiya_Daraja = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('Umarni Kasa_aiki_Daraja: ' + ' '.join(str(Daraja) for Daraja in 인수) + '\n' + kunshiya_Daraja[-10000:])
    return kunshiya_Daraja


def siffofi_Daraja(kunshiya_Daraja):
    결과 = {}
    for Layi in kunshiya_Daraja.splitlines():
        if '=' not in Layi:
            continue
        Suna, Daraja = Layi.split('=', 1)
        if Suna.startswith('"'):
            Suna = json.loads(Suna)
        if Daraja.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(Daraja)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(Daraja): Daraja = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox siffofi_Daraja zubi_Daraja Kuskure: ' + Layi)
        결과[Suna] = Daraja
    return 결과


def 등록목록(kunshiya_Daraja):
    결과 = {}
    for Layi in kunshiya_Daraja.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Layi)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def checksum(Hanyar_shiga):
    Daraja = hashlib.sha256()
    with Hanyar_shiga.open('rb') as Fayil:
        for Tarin_bayani in iter(lambda: Fayil.read(1024 * 1024), b''): Daraja.update(Tarin_bayani)
    return Daraja.hexdigest()


class Shiri_Mai_Fara_Ka_ida:
    def __init__(self, 뿌리, Suna, tsari_yanayin_aiki='gui', Umarni=gudanar_Mai_fayyace_umani_Umarni):
        self.뿌리 = Path(뿌리).resolve()
        self.Suna, self.tsari_yanayin_aiki, self.Umarni = Suna, tsari_yanayin_aiki, Umarni
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Suna) or Suna in ('.', '..'):
            raise 실행오류('VM 이름은 문자·lamba_Daraja·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if tsari_yanayin_aiki not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Hanyar_shiga(self, Fiya_Daraja):
        if Path(Fiya_Daraja).is_absolute() or '..' in Path(Fiya_Daraja).parts:
            raise 실행오류('잘못된 관리 Hanyar_shiga: ' + str(Fiya_Daraja))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(Fiya_Daraja).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('Haɗi 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def Yi_Karatu(self):
        Hanyar_shiga = self.Hanyar_shiga('state.json')
        if not Hanyar_shiga.exists(): return None
        Matsayi_Daraja = json.loads(Hanyar_shiga.read_text(encoding='utf-8'))
        if Matsayi_Daraja.get('version') != 1 or Matsayi_Daraja.get('name') != self.Suna:
            raise 실행오류('관리 상태의 VM Suna/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Suna in ('uuid', 'owner'):
            if str(uuid.UUID(Matsayi_Daraja[Suna])) != Matsayi_Daraja[Suna]: raise 실행오류('잘못된 VM mai_ganewa_Daraja')
        return Matsayi_Daraja

    def Ajiye_Daraja(self, Matsayi_Daraja):
        Zangon_ƙarshe_Daraja = self.Hanyar_shiga('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Fayil:
            json.dump(Matsayi_Daraja, Fayil, ensure_ascii=False, indent=2)
            Fayil.write('\n')
            임시 = Fayil.name
        os.replace(임시, str(Zangon_ƙarshe_Daraja))

    def msinfo32_exe(self, Matsayi_Daraja, 등록됨, dawo_da_martaba_Matsayi=False):
        if Matsayi_Daraja['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = siffofi_Daraja(self.Umarni(['VBoxManage', 'showvminfo', Matsayi_Daraja['uuid'], '--machinereadable']))
        위치 = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.Hanyar_shiga('machines').resolve() not in 위치.parents or msinfo32_exe.get('UUID') != Matsayi_Daraja['uuid']:
            raise 실행오류('이 프로젝트의 VM Saituna Hanyar_shiga/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Umarni(['VBoxManage', 'getextradata', Matsayi_Daraja['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + Matsayi_Daraja['owner']:
            if dawo_da_martaba_Matsayi and Matsayi_Daraja.get('pending') and 표식 == 'No value set!':
                self.Umarni(['VBoxManage', 'setextradata', Matsayi_Daraja['uuid'], 'JKOROS/Owner', Matsayi_Daraja['owner']])
            else:
                raise 실행오류('VM mamallaki_Daraja 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def Bincika_Midiya(self, Matsayi_Daraja, msinfo32_exe):
        제어기들 = [Daraja for Suna, Daraja in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Suna)]
        Bada_izini_Daraja = [str(self.Hanyar_shiga(Daraja)) for Daraja in Matsayi_Daraja.get('media', [])]
        for Suna, Daraja in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(mai_kulawa) + r'-\d+-\d+', Suna) for mai_kulawa in 제어기들):
                if Daraja not in ('none', 'emptydrive') and Daraja not in Bada_izini_Daraja:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + Daraja)

    def Nuna_Matsayi(self):
        Matsayi_Daraja = self.Yi_Karatu()
        if Matsayi_Daraja is None: return {'name': self.Suna, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(Matsayi_Daraja, 등록목록(self.Umarni(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', Matsayi_Daraja['name']), 'uuid': Matsayi_Daraja['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.Hanyar_shiga(Matsayi_Daraja['iso'])) if Matsayi_Daraja.get('iso') else None,
                'serial_log': str(self.Hanyar_shiga(Matsayi_Daraja['serial_log'])) if Matsayi_Daraja.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def gudanar_Umarni(self):
        Matsayi_Daraja = self.Yi_Karatu()
        등록됨 = 등록목록(self.Umarni(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if Matsayi_Daraja is not None and Matsayi_Daraja['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(Matsayi_Daraja, 등록됨, dawo_da_martaba_Matsayi=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 gudanar_Umarni 중입니다. 재빌드·재시작하지 않습니다.')
                return self.Nuna_Matsayi()
            self.Bincika_Midiya(Matsayi_Daraja, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Ajiye_Daraja 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Umarni(['VBoxManage', 'controlvm', Matsayi_Daraja['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Buɗe 전에 기존 기록도 보관한다.
                    if Matsayi_Daraja.get('serial_log'):
                        원본 = self.Hanyar_shiga(Matsayi_Daraja['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Hanyar_shiga('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Umarni(['VBoxManage', 'startvm', Matsayi_Daraja['uuid'], '--type', self.tsari_yanayin_aiki])
                return self.Nuna_Matsayi()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 Sauya_yanayin_aiki 중입니다 ({}). 작업이 끝난 Baya_Daraja 다시 실행하세요.'.format(현재))
        elif Matsayi_Daraja is not None and not Matsayi_Daraja.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Suna in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Ajiye_Daraja/gudanar_Umarni 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Umarni(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        Midiya_Daraja = 'media/kernel-' + checksum(원본) + '.iso'
        Zangon_ƙarshe_Daraja = self.Hanyar_shiga(Midiya_Daraja)
        Zangon_ƙarshe_Daraja.parent.mkdir(exist_ok=True)
        if Zangon_ƙarshe_Daraja.exists():
            if checksum(Zangon_ƙarshe_Daraja) != checksum(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(Zangon_ƙarshe_Daraja))
        else:
            with tempfile.NamedTemporaryFile(dir=str(Zangon_ƙarshe_Daraja.parent)) as Fayil:
                shutil.copyfile(str(원본), Fayil.name)
                os.link(Fayil.name, str(Zangon_ƙarshe_Daraja))

        if Matsayi_Daraja is None:
            Matsayi_Daraja = {'version': 1, 'name': self.Suna, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Ajiye_Daraja(Matsayi_Daraja)
        if msinfo32_exe is None:
            self.Umarni(['VBoxManage', 'createvm', '--name', Matsayi_Daraja['name'], '--uuid', Matsayi_Daraja['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Hanyar_shiga('machines')), '--register'])
            self.Umarni(['VBoxManage', 'setextradata', Matsayi_Daraja['uuid'], 'JKOROS/Owner', Matsayi_Daraja['owner']])
        # Gina_na_ura 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(Matsayi_Daraja, 등록목록(self.Umarni(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('Gina_na_ura 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.Bincika_Midiya(Matsayi_Daraja, msinfo32_exe)
        Matsayi_Daraja['iso'] = Midiya_Daraja
        if Midiya_Daraja not in Matsayi_Daraja['media']: Matsayi_Daraja['media'].append(Midiya_Daraja)
        Matsayi_Daraja['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        logu_Daraja = self.Hanyar_shiga(Matsayi_Daraja['serial_log'])
        logu_Daraja.parent.mkdir(exist_ok=True)
        self.Ajiye_Daraja(Matsayi_Daraja)
        self.Umarni(['VBoxManage', 'modifyvm', Matsayi_Daraja['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(logu_Daraja)])
        제어기들 = [Daraja for Suna, Daraja in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Suna)]
        if 'JKOROS IDE' not in 제어기들:
            self.Umarni(['VBoxManage', 'storagectl', Matsayi_Daraja['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Umarni(['VBoxManage', 'storageattach', Matsayi_Daraja['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(Zangon_ƙarshe_Daraja)])
        Matsayi_Daraja['pending'] = False
        self.Ajiye_Daraja(Matsayi_Daraja)
        self.Umarni(['VBoxManage', 'startvm', Matsayi_Daraja['uuid'], '--type', self.tsari_yanayin_aiki])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.Nuna_Matsayi()


def Tafiyar_da():
    Daddatse_Daraja = argparse.ArgumentParser(description='jkoros 전용 VirtualBox gudanar_Umarni 및 Matsayi_Daraja Matantanci_Daraja')
    Daddatse_Daraja.add_argument('action', choices=['run', 'status'])
    maaunin_Tubalin_aiki = Daddatse_Daraja.parse_args()
    gudanar_Umarni = Shiri_Mai_Fara_Ka_ida(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if maaunin_Tubalin_aiki.action == 'status':
        print(json.dumps(gudanar_Umarni.Nuna_Matsayi(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. sauka 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/izini_Daraja 변경은 하지 않습니다.')
    os.umask(0o077)
    gudanar_Umarni.Hanyar_shiga('lock').parent.mkdir(parents=True, exist_ok=True)
    with gudanar_Umarni.Hanyar_shiga('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox gudanar_Umarni 작업이 진행 중입니다.')
        print(json.dumps(gudanar_Umarni.gudanar_Umarni(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Tafiyar_da()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Kuskure:
        print('VBOX Kuskure: ' + str(Kuskure), file=sys.stderr)
        sys.exit(1)
