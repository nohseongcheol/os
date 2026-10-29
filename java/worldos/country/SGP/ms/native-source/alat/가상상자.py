#!/usr/bin/env python3
"""jkoros 전용 VirtualBox aplikasi_pelancar. 기존 VM/디스크/stor_VALUE 상태는 삭제하지 않는다."""
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


def laksanakan_cangkerang_perintah(인수):
    persekitaran = dict(os.environ, LC_ALL='C')
    ukuran = subprocess.run([str(VALUE) for VALUE in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=persekitaran, timeout=180)
    Kandungan_VALUE = ukuran.stdout.decode('utf-8', 'replace')
    if ukuran.returncode:
        raise 실행오류('Perintah kegagalan_VALUE: ' + ' '.join(str(VALUE) for VALUE in 인수) + '\n' + Kandungan_VALUE[-10000:])
    return Kandungan_VALUE


def atribut_VALUE(Kandungan_VALUE):
    ukuran = {}
    for baris in Kandungan_VALUE.splitlines():
        if '=' not in baris:
            continue
        Nama, VALUE = baris.split('=', 1)
        if Nama.startswith('"'):
            Nama = json.loads(Nama)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox atribut_VALUE format_VALUE RALAT: ' + baris)
        ukuran[Nama] = VALUE
    return ukuran


def 등록목록(Kandungan_VALUE):
    ukuran = {}
    for baris in Kandungan_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', baris)
        if 일치: ukuran[일치.group(2).lower()] = 일치.group(1)
    return ukuran


def hasil_tambah_semak(LALUAN):
    VALUE = hashlib.sha256()
    with LALUAN.open('rb') as Fail:
        for data in iter(lambda: Fail.read(1024 * 1024), b''): VALUE.update(data)
    return VALUE.hexdigest()


class aplikasi_pelancar:
    def __init__(self, akar_VALUE, Nama, kaedah_mod='gui', Perintah=laksanakan_cangkerang_perintah):
        self.akar_VALUE = Path(akar_VALUE).resolve()
        self.Nama, self.kaedah_mod, self.Perintah = Nama, kaedah_mod, Perintah
        self.보관 = self.akar_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Nama) or Nama in ('.', '..'):
            raise 실행오류('VM 이름은 문자·digit_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if kaedah_mod not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def LALUAN(self, rakan_VALUE):
        if Path(rakan_VALUE).is_absolute() or '..' in Path(rakan_VALUE).parts:
            raise 실행오류('잘못된 관리 LALUAN: ' + str(rakan_VALUE))
        ukuran = self.보관
        for 부분 in ['.vbox'] + list(Path(rakan_VALUE).parts):
            if 부분 == '.vbox': ukuran = self.보관
            else: ukuran = ukuran / 부분
            if ukuran.is_symlink(): raise 실행오류('Sambung 경로는 사용하지 않습니다: ' + str(ukuran))
        return ukuran

    def Baca(self):
        LALUAN = self.LALUAN('state.json')
        if not LALUAN.exists(): return None
        status_VALUE = json.loads(LALUAN.read_text(encoding='utf-8'))
        if status_VALUE.get('version') != 1 or status_VALUE.get('name') != self.Nama:
            raise 실행오류('관리 상태의 VM Nama/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Nama in ('uuid', 'owner'):
            if str(uuid.UUID(status_VALUE[Nama])) != status_VALUE[Nama]: raise 실행오류('잘못된 VM 식별자')
        return status_VALUE

    def stor_VALUE(self, status_VALUE):
        destinasi_VALUE = self.LALUAN('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Fail:
            json.dump(status_VALUE, Fail, ensure_ascii=False, indent=2)
            Fail.write('\n')
            임시 = Fail.name
        os.replace(임시, str(destinasi_VALUE))

    def msinfo32_exe(self, status_VALUE, 등록됨, pulih_status=False):
        if status_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = atribut_VALUE(self.Perintah(['VBoxManage', 'showvminfo', status_VALUE['uuid'], '--machinereadable']))
        Kedudukan = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.LALUAN('machines').resolve() not in Kedudukan.parents or msinfo32_exe.get('UUID') != status_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Tetapan LALUAN/UUID와 일치하지 않아 변경하지 않습니다.')
        penanda_VALUE = self.Perintah(['VBoxManage', 'getextradata', status_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if penanda_VALUE != 'Value: ' + status_VALUE['owner']:
            if pulih_status and status_VALUE.get('pending') and penanda_VALUE == 'No value set!':
                self.Perintah(['VBoxManage', 'setextradata', status_VALUE['uuid'], 'JKOROS/Owner', status_VALUE['owner']])
            else:
                raise 실행오류('VM pemilik_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, status_VALUE, msinfo32_exe):
        제어기들 = [VALUE for Nama, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nama)]
        Izin_VALUE = [str(self.LALUAN(VALUE)) for VALUE in status_VALUE.get('media', [])]
        for Nama, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(pengawal) + r'-\d+-\d+', Nama) for pengawal in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Izin_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def tayang_status(self):
        status_VALUE = self.Baca()
        if status_VALUE is None: return {'name': self.Nama, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(status_VALUE, 등록목록(self.Perintah(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', status_VALUE['name']), 'uuid': status_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.LALUAN(status_VALUE['iso'])) if status_VALUE.get('iso') else None,
                'serial_log': str(self.LALUAN(status_VALUE['serial_log'])) if status_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def laksanakan_perintah(self):
        status_VALUE = self.Baca()
        등록됨 = 등록목록(self.Perintah(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if status_VALUE is not None and status_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(status_VALUE, 등록됨, pulih_status=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 laksanakan_perintah 중입니다. 재빌드·재시작하지 않습니다.')
                return self.tayang_status()
            self.매체검사(status_VALUE, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 stor_VALUE 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Perintah(['VBoxManage', 'controlvm', status_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Buka 전에 기존 기록도 보관한다.
                    if status_VALUE.get('serial_log'):
                        원본 = self.LALUAN(status_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.LALUAN('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Perintah(['VBoxManage', 'startvm', status_VALUE['uuid'], '--type', self.kaedah_mod])
                return self.tayang_status()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 tukar_mod 중입니다 ({}). 작업이 끝난 BACK_VALUE 다시 실행하세요.'.format(현재))
        elif status_VALUE is not None and not status_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Nama in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # stor_VALUE/laksanakan_perintah 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Perintah(['make', '-C', str(self.akar_VALUE / 'os'), 'iso']), end='')
        원본 = self.akar_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('permulaan_mesin ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + hasil_tambah_semak(원본) + '.iso'
        destinasi_VALUE = self.LALUAN(매체)
        destinasi_VALUE.parent.mkdir(exist_ok=True)
        if destinasi_VALUE.exists():
            if hasil_tambah_semak(destinasi_VALUE) != hasil_tambah_semak(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(destinasi_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(destinasi_VALUE.parent)) as Fail:
                shutil.copyfile(str(원본), Fail.name)
                os.link(Fail.name, str(destinasi_VALUE))

        if status_VALUE is None:
            status_VALUE = {'version': 1, 'name': self.Nama, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.stor_VALUE(status_VALUE)
        if msinfo32_exe is None:
            self.Perintah(['VBoxManage', 'createvm', '--name', status_VALUE['name'], '--uuid', status_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.LALUAN('machines')), '--register'])
            self.Perintah(['VBoxManage', 'setextradata', status_VALUE['uuid'], 'JKOROS/Owner', status_VALUE['owner']])
        # bina_sistem 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(status_VALUE, 등록목록(self.Perintah(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('bina_sistem 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(status_VALUE, msinfo32_exe)
        status_VALUE['iso'] = 매체
        if 매체 not in status_VALUE['media']: status_VALUE['media'].append(매체)
        status_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.LALUAN(status_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.stor_VALUE(status_VALUE)
        self.Perintah(['VBoxManage', 'modifyvm', status_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Nama, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Nama)]
        if 'JKOROS IDE' not in 제어기들:
            self.Perintah(['VBoxManage', 'storagectl', status_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Perintah(['VBoxManage', 'storageattach', status_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(destinasi_VALUE)])
        status_VALUE['pending'] = False
        self.stor_VALUE(status_VALUE)
        self.Perintah(['VBoxManage', 'startvm', status_VALUE['uuid'], '--type', self.kaedah_mod])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.tayang_status()


def Jalan():
    hurai_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox laksanakan_perintah 및 status_VALUE pertanyaan_VALUE')
    hurai_VALUE.add_argument('action', choices=['run', 'status'])
    parameter_argumen = hurai_VALUE.parse_args()
    laksanakan_perintah = aplikasi_pelancar(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parameter_argumen.action == 'status':
        print(json.dumps(laksanakan_perintah.tayang_status(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. hos 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/keizinan_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    laksanakan_perintah.LALUAN('lock').parent.mkdir(parents=True, exist_ok=True)
    with laksanakan_perintah.LALUAN('lock').open('a') as kunci_VALUE:
        try: fcntl.flock(kunci_VALUE, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox laksanakan_perintah 작업이 진행 중입니다.')
        print(json.dumps(laksanakan_perintah.laksanakan_perintah(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Jalan()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as RALAT:
        print('VBOX RALAT: ' + str(RALAT), file=sys.stderr)
        sys.exit(1)
