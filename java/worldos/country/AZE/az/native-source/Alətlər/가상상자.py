#!/usr/bin/env python3
"""jkoros 전용 VirtualBox proqram_işəsalma. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def icra_etmək_örtük_əmr(인수):
    환경 = dict(os.environ, LC_ALL='C')
    ölçü = subprocess.run([str(VALUE) for VALUE in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Məzmun_VALUE = ölçü.stdout.decode('utf-8', 'replace')
    if ölçü.returncode:
        raise 실행오류('Əmr xəta_VALUE: ' + ' '.join(str(VALUE) for VALUE in 인수) + '\n' + Məzmun_VALUE[-10000:])
    return Məzmun_VALUE


def atribut_VALUE(Məzmun_VALUE):
    ölçü = {}
    for Giriş in Məzmun_VALUE.splitlines():
        if '=' not in Giriş:
            continue
        Ad, VALUE = Giriş.split('=', 1)
        if Ad.startswith('"'):
            Ad = json.loads(Ad)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox atribut_VALUE format_VALUE XƏTA: ' + Giriş)
        ölçü[Ad] = VALUE
    return ölçü


def 등록목록(Məzmun_VALUE):
    ölçü = {}
    for Giriş in Məzmun_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', Giriş)
        if 일치: ölçü[일치.group(2).lower()] = 일치.group(1)
    return ölçü


def 검사합(Cığır):
    VALUE = hashlib.sha256()
    with Cığır.open('rb') as FAYL:
        for verilənlər in iter(lambda: FAYL.read(1024 * 1024), b''): VALUE.update(verilənlər)
    return VALUE.hexdigest()


class proqram_işəsalma:
    def __init__(self, kök_VALUE, Ad, metod_MODE='gui', Əmr=icra_etmək_örtük_əmr):
        self.kök_VALUE = Path(kök_VALUE).resolve()
        self.Ad, self.metod_MODE, self.Əmr = Ad, metod_MODE, Əmr
        self.보관 = self.kök_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Ad) or Ad in ('.', '..'):
            raise 실행오류('VM 이름은 문자·rəqəm_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if metod_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Cığır(self, eynisəviyyəli_VALUE):
        if Path(eynisəviyyəli_VALUE).is_absolute() or '..' in Path(eynisəviyyəli_VALUE).parts:
            raise 실행오류('잘못된 관리 Cığır: ' + str(eynisəviyyəli_VALUE))
        ölçü = self.보관
        for 부분 in ['.vbox'] + list(Path(eynisəviyyəli_VALUE).parts):
            if 부분 == '.vbox': ölçü = self.보관
            else: ölçü = ölçü / 부분
            if ölçü.is_symlink(): raise 실행오류('Bağlan 경로는 사용하지 않습니다: ' + str(ölçü))
        return ölçü

    def Oxuma(self):
        Cığır = self.Cığır('state.json')
        if not Cığır.exists(): return None
        vəziyyət_VALUE = json.loads(Cığır.read_text(encoding='utf-8'))
        if vəziyyət_VALUE.get('version') != 1 or vəziyyət_VALUE.get('name') != self.Ad:
            raise 실행오류('관리 상태의 VM Ad/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Ad in ('uuid', 'owner'):
            if str(uuid.UUID(vəziyyət_VALUE[Ad])) != vəziyyət_VALUE[Ad]: raise 실행오류('잘못된 VM identifikator_VALUE')
        return vəziyyət_VALUE

    def Store_VALUE(self, vəziyyət_VALUE):
        təyinat_VALUE_a0fbc067 = self.Cığır('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as FAYL:
            json.dump(vəziyyət_VALUE, FAYL, ensure_ascii=False, indent=2)
            FAYL.write('\n')
            임시 = FAYL.name
        os.replace(임시, str(təyinat_VALUE_a0fbc067))

    def msinfo32_exe(self, vəziyyət_VALUE, 등록됨, bərpa_etmək_vəziyyət=False):
        if vəziyyət_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = atribut_VALUE(self.Əmr(['VBoxManage', 'showvminfo', vəziyyət_VALUE['uuid'], '--machinereadable']))
        yerinə_qoymaq = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.Cığır('machines').resolve() not in yerinə_qoymaq.parents or msinfo32_exe.get('UUID') != vəziyyət_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Sazlama Cığır/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Əmr(['VBoxManage', 'getextradata', vəziyyət_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + vəziyyət_VALUE['owner']:
            if bərpa_etmək_vəziyyət and vəziyyət_VALUE.get('pending') and 표식 == 'No value set!':
                self.Əmr(['VBoxManage', 'setextradata', vəziyyət_VALUE['uuid'], 'JKOROS/Owner', vəziyyət_VALUE['owner']])
            else:
                raise 실행오류('VM sahib_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, vəziyyət_VALUE, msinfo32_exe):
        제어기들 = [VALUE for Ad, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Ad)]
        İcazə_ver_VALUE = [str(self.Cığır(VALUE)) for VALUE in vəziyyət_VALUE.get('media', [])]
        for Ad, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(idarəedici) + r'-\d+-\d+', Ad) for idarəedici in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in İcazə_ver_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def göstərmək_vəziyyət(self):
        vəziyyət_VALUE = self.Oxuma()
        if vəziyyət_VALUE is None: return {'name': self.Ad, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(vəziyyət_VALUE, 등록목록(self.Əmr(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', vəziyyət_VALUE['name']), 'uuid': vəziyyət_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.Cığır(vəziyyət_VALUE['iso'])) if vəziyyət_VALUE.get('iso') else None,
                'serial_log': str(self.Cığır(vəziyyət_VALUE['serial_log'])) if vəziyyət_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def icra_etmək_əmr(self):
        vəziyyət_VALUE = self.Oxuma()
        등록됨 = 등록목록(self.Əmr(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if vəziyyət_VALUE is not None and vəziyyət_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(vəziyyət_VALUE, 등록됨, bərpa_etmək_vəziyyət=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 icra_etmək_əmr 중입니다. 재빌드·재시작하지 않습니다.')
                return self.göstərmək_vəziyyət()
            self.매체검사(vəziyyət_VALUE, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Əmr(['VBoxManage', 'controlvm', vəziyyət_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Aç 전에 기존 기록도 보관한다.
                    if vəziyyət_VALUE.get('serial_log'):
                        원본 = self.Cığır(vəziyyət_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Cığır('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Əmr(['VBoxManage', 'startvm', vəziyyət_VALUE['uuid'], '--type', self.metod_MODE])
                return self.göstərmək_vəziyyət()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 GERİ_VALUE 다시 실행하세요.'.format(현재))
        elif vəziyyət_VALUE is not None and not vəziyyət_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Ad in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/icra_etmək_əmr 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Əmr(['make', '-C', str(self.kök_VALUE / 'os'), 'iso']), end='')
        원본 = self.kök_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        təyinat_VALUE_a0fbc067 = self.Cığır(매체)
        təyinat_VALUE_a0fbc067.parent.mkdir(exist_ok=True)
        if təyinat_VALUE_a0fbc067.exists():
            if 검사합(təyinat_VALUE_a0fbc067) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(təyinat_VALUE_a0fbc067))
        else:
            with tempfile.NamedTemporaryFile(dir=str(təyinat_VALUE_a0fbc067.parent)) as FAYL:
                shutil.copyfile(str(원본), FAYL.name)
                os.link(FAYL.name, str(təyinat_VALUE_a0fbc067))

        if vəziyyət_VALUE is None:
            vəziyyət_VALUE = {'version': 1, 'name': self.Ad, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(vəziyyət_VALUE)
        if msinfo32_exe is None:
            self.Əmr(['VBoxManage', 'createvm', '--name', vəziyyət_VALUE['name'], '--uuid', vəziyyət_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Cığır('machines')), '--register'])
            self.Əmr(['VBoxManage', 'setextradata', vəziyyət_VALUE['uuid'], 'JKOROS/Owner', vəziyyət_VALUE['owner']])
        # qurmaq_sistem 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(vəziyyət_VALUE, 등록목록(self.Əmr(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('qurmaq_sistem 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(vəziyyət_VALUE, msinfo32_exe)
        vəziyyət_VALUE['iso'] = 매체
        if 매체 not in vəziyyət_VALUE['media']: vəziyyət_VALUE['media'].append(매체)
        vəziyyət_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.Cığır(vəziyyət_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(vəziyyət_VALUE)
        self.Əmr(['VBoxManage', 'modifyvm', vəziyyət_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Ad, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Ad)]
        if 'JKOROS IDE' not in 제어기들:
            self.Əmr(['VBoxManage', 'storagectl', vəziyyət_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Əmr(['VBoxManage', 'storageattach', vəziyyət_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(təyinat_VALUE_a0fbc067)])
        vəziyyət_VALUE['pending'] = False
        self.Store_VALUE(vəziyyət_VALUE)
        self.Əmr(['VBoxManage', 'startvm', vəziyyət_VALUE['uuid'], '--type', self.metod_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.göstərmək_vəziyyət()


def İcra_Et():
    parselləmək_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox icra_etmək_əmr 및 vəziyyət_VALUE sorğu_VALUE')
    parselləmək_VALUE.add_argument('action', choices=['run', 'status'])
    인자 = parselləmək_VALUE.parse_args()
    icra_etmək_əmr = proqram_işəsalma(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(icra_etmək_əmr.göstərmək_vəziyyət(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. host 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/icazə_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    icra_etmək_əmr.Cığır('lock').parent.mkdir(parents=True, exist_ok=True)
    with icra_etmək_əmr.Cığır('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox icra_etmək_əmr 작업이 진행 중입니다.')
        print(json.dumps(icra_etmək_əmr.icra_etmək_əmr(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: İcra_Et()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as XƏTA:
        print('VBOX XƏTA: ' + str(XƏTA), file=sys.stderr)
        sys.exit(1)
