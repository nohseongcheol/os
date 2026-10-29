#!/usr/bin/env python3
"""jkoros 전용 VirtualBox ilova_ilovalar_paneli. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def bajarmoq_qobiq_buyruq(인수):
    환경 = dict(os.environ, LC_ALL='C')
    o_lchov = subprocess.run([str(VALUE) for VALUE in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    tarkib_VALUE = o_lchov.stdout.decode('utf-8', 'replace')
    if o_lchov.returncode:
        raise 실행오류('Buyruq to_xtab_qolish_VALUE: ' + ' '.join(str(VALUE) for VALUE in 인수) + '\n' + tarkib_VALUE[-10000:])
    return tarkib_VALUE


def xususiyat_VALUE(tarkib_VALUE):
    o_lchov = {}
    for satr in tarkib_VALUE.splitlines():
        if '=' not in satr:
            continue
        Nomi, VALUE = satr.split('=', 1)
        if Nomi.startswith('"'):
            Nomi = json.loads(Nomi)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox xususiyat_VALUE format_VALUE Xato: ' + satr)
        o_lchov[Nomi] = VALUE
    return o_lchov


def 등록목록(tarkib_VALUE):
    o_lchov = {}
    for satr in tarkib_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', satr)
        if 일치: o_lchov[일치.group(2).lower()] = 일치.group(1)
    return o_lchov


def 검사합(yo_l):
    VALUE = hashlib.sha256()
    with yo_l.open('rb') as Fayl:
        for ma_lumotlar in iter(lambda: Fayl.read(1024 * 1024), b''): VALUE.update(ma_lumotlar)
    return VALUE.hexdigest()


class ilova_ilovalar_paneli:
    def __init__(self, ildiz_VALUE, Nomi, uslub_MODE='gui', Buyruq=bajarmoq_qobiq_buyruq):
        self.ildiz_VALUE = Path(ildiz_VALUE).resolve()
        self.Nomi, self.uslub_MODE, self.Buyruq = Nomi, uslub_MODE, Buyruq
        self.보관 = self.ildiz_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Nomi) or Nomi in ('.', '..'):
            raise 실행오류('VM 이름은 문자·raqam_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if uslub_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def yo_l(self, bir_rangli_VALUE):
        if Path(bir_rangli_VALUE).is_absolute() or '..' in Path(bir_rangli_VALUE).parts:
            raise 실행오류('잘못된 관리 yo_l: ' + str(bir_rangli_VALUE))
        o_lchov = self.보관
        for 부분 in ['.vbox'] + list(Path(bir_rangli_VALUE).parts):
            if 부분 == '.vbox': o_lchov = self.보관
            else: o_lchov = o_lchov / 부분
            if o_lchov.is_symlink(): raise 실행오류('Ulanish 경로는 사용하지 않습니다: ' + str(o_lchov))
        return o_lchov

    def Oʻqish(self):
        yo_l = self.yo_l('state.json')
        if not yo_l.exists(): return None
        holat_VALUE_e10195a1 = json.loads(yo_l.read_text(encoding='utf-8'))
        if holat_VALUE_e10195a1.get('version') != 1 or holat_VALUE_e10195a1.get('name') != self.Nomi:
            raise 실행오류('관리 상태의 VM Nomi/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Nomi in ('uuid', 'owner'):
            if str(uuid.UUID(holat_VALUE_e10195a1[Nomi])) != holat_VALUE_e10195a1[Nomi]: raise 실행오류('잘못된 VM identifikator_VALUE')
        return holat_VALUE_e10195a1

    def Store_VALUE(self, holat_VALUE_e10195a1):
        ko_chirish_joyi_VALUE = self.yo_l('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Fayl:
            json.dump(holat_VALUE_e10195a1, Fayl, ensure_ascii=False, indent=2)
            Fayl.write('\n')
            임시 = Fayl.name
        os.replace(임시, str(ko_chirish_joyi_VALUE))

    def msinfo32_exe(self, holat_VALUE_e10195a1, 등록됨, tiklamoq_holat=False):
        if holat_VALUE_e10195a1['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = xususiyat_VALUE(self.Buyruq(['VBoxManage', 'showvminfo', holat_VALUE_e10195a1['uuid'], '--machinereadable']))
        Holati = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.yo_l('machines').resolve() not in Holati.parents or msinfo32_exe.get('UUID') != holat_VALUE_e10195a1['uuid']:
            raise 실행오류('이 프로젝트의 VM Moslamalar yo_l/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Buyruq(['VBoxManage', 'getextradata', holat_VALUE_e10195a1['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + holat_VALUE_e10195a1['owner']:
            if tiklamoq_holat and holat_VALUE_e10195a1.get('pending') and 표식 == 'No value set!':
                self.Buyruq(['VBoxManage', 'setextradata', holat_VALUE_e10195a1['uuid'], 'JKOROS/Owner', holat_VALUE_e10195a1['owner']])
            else:
                raise 실행오류('VM egasi_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, holat_VALUE_e10195a1, msinfo32_exe):
        제어기들 = [VALUE for Nomi, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nomi)]
        Ruxsatnoma_VALUE = [str(self.yo_l(VALUE)) for VALUE in holat_VALUE_e10195a1.get('media', [])]
        for Nomi, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(boshqaruv_pulti) + r'-\d+-\d+', Nomi) for boshqaruv_pulti in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Ruxsatnoma_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def ko_rsatmoq_holat(self):
        holat_VALUE_e10195a1 = self.Oʻqish()
        if holat_VALUE_e10195a1 is None: return {'name': self.Nomi, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(holat_VALUE_e10195a1, 등록목록(self.Buyruq(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', holat_VALUE_e10195a1['name']), 'uuid': holat_VALUE_e10195a1['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.yo_l(holat_VALUE_e10195a1['iso'])) if holat_VALUE_e10195a1.get('iso') else None,
                'serial_log': str(self.yo_l(holat_VALUE_e10195a1['serial_log'])) if holat_VALUE_e10195a1.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def bajarmoq_buyruq(self):
        holat_VALUE_e10195a1 = self.Oʻqish()
        등록됨 = 등록목록(self.Buyruq(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if holat_VALUE_e10195a1 is not None and holat_VALUE_e10195a1['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(holat_VALUE_e10195a1, 등록됨, tiklamoq_holat=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 bajarmoq_buyruq 중입니다. 재빌드·재시작하지 않습니다.')
                return self.ko_rsatmoq_holat()
            self.매체검사(holat_VALUE_e10195a1, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Buyruq(['VBoxManage', 'controlvm', holat_VALUE_e10195a1['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Ochish 전에 기존 기록도 보관한다.
                    if holat_VALUE_e10195a1.get('serial_log'):
                        원본 = self.yo_l(holat_VALUE_e10195a1['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.yo_l('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Buyruq(['VBoxManage', 'startvm', holat_VALUE_e10195a1['uuid'], '--type', self.uslub_MODE])
                return self.ko_rsatmoq_holat()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 Orqaga_VALUE 다시 실행하세요.'.format(현재))
        elif holat_VALUE_e10195a1 is not None and not holat_VALUE_e10195a1.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Nomi in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/bajarmoq_buyruq 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Buyruq(['make', '-C', str(self.ildiz_VALUE / 'os'), 'iso']), end='')
        원본 = self.ildiz_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        ko_chirish_joyi_VALUE = self.yo_l(매체)
        ko_chirish_joyi_VALUE.parent.mkdir(exist_ok=True)
        if ko_chirish_joyi_VALUE.exists():
            if 검사합(ko_chirish_joyi_VALUE) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(ko_chirish_joyi_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(ko_chirish_joyi_VALUE.parent)) as Fayl:
                shutil.copyfile(str(원본), Fayl.name)
                os.link(Fayl.name, str(ko_chirish_joyi_VALUE))

        if holat_VALUE_e10195a1 is None:
            holat_VALUE_e10195a1 = {'version': 1, 'name': self.Nomi, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(holat_VALUE_e10195a1)
        if msinfo32_exe is None:
            self.Buyruq(['VBoxManage', 'createvm', '--name', holat_VALUE_e10195a1['name'], '--uuid', holat_VALUE_e10195a1['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.yo_l('machines')), '--register'])
            self.Buyruq(['VBoxManage', 'setextradata', holat_VALUE_e10195a1['uuid'], 'JKOROS/Owner', holat_VALUE_e10195a1['owner']])
        # nashr_tizim 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(holat_VALUE_e10195a1, 등록목록(self.Buyruq(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('nashr_tizim 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(holat_VALUE_e10195a1, msinfo32_exe)
        holat_VALUE_e10195a1['iso'] = 매체
        if 매체 not in holat_VALUE_e10195a1['media']: holat_VALUE_e10195a1['media'].append(매체)
        holat_VALUE_e10195a1['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.yo_l(holat_VALUE_e10195a1['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(holat_VALUE_e10195a1)
        self.Buyruq(['VBoxManage', 'modifyvm', holat_VALUE_e10195a1['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Nomi, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nomi)]
        if 'JKOROS IDE' not in 제어기들:
            self.Buyruq(['VBoxManage', 'storagectl', holat_VALUE_e10195a1['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Buyruq(['VBoxManage', 'storageattach', holat_VALUE_e10195a1['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(ko_chirish_joyi_VALUE)])
        holat_VALUE_e10195a1['pending'] = False
        self.Store_VALUE(holat_VALUE_e10195a1)
        self.Buyruq(['VBoxManage', 'startvm', holat_VALUE_e10195a1['uuid'], '--type', self.uslub_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.ko_rsatmoq_holat()


def Bajarish():
    tahlil_qilmoq_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox bajarmoq_buyruq 및 holat_VALUE_e10195a1 so_rov_VALUE')
    tahlil_qilmoq_VALUE.add_argument('action', choices=['run', 'status'])
    인자 = tahlil_qilmoq_VALUE.parse_args()
    bajarmoq_buyruq = ilova_ilovalar_paneli(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(bajarmoq_buyruq.ko_rsatmoq_holat(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. tashkilotchi 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/ruxsat_VALUE_a9fa0dfa 변경은 하지 않습니다.')
    os.umask(0o077)
    bajarmoq_buyruq.yo_l('lock').parent.mkdir(parents=True, exist_ok=True)
    with bajarmoq_buyruq.yo_l('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox bajarmoq_buyruq 작업이 진행 중입니다.')
        print(json.dumps(bajarmoq_buyruq.bajarmoq_buyruq(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Bajarish()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Xato:
        print('VBOX Xato: ' + str(Xato), file=sys.stderr)
        sys.exit(1)
