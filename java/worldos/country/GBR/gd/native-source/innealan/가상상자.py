#!/usr/bin/env python3
"""jkoros 전용 VirtualBox ap_drathair_nan_aplacaid. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def gnìomhaich_slige_àithne(인수):
    환경 = dict(os.environ, LC_ALL='C')
    tomhas = subprocess.run([str(VALUE) for VALUE in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    susbaint_VALUE = tomhas.stdout.decode('utf-8', 'replace')
    if tomhas.returncode:
        raise 실행오류('àithne fàilligeadh_VALUE: ' + ' '.join(str(VALUE) for VALUE in 인수) + '\n' + susbaint_VALUE[-10000:])
    return susbaint_VALUE


def buadh_VALUE(susbaint_VALUE):
    tomhas = {}
    for loidhne in susbaint_VALUE.splitlines():
        if '=' not in loidhne:
            continue
        Ainm, VALUE = loidhne.split('=', 1)
        if Ainm.startswith('"'):
            Ainm = json.loads(Ainm)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox buadh_VALUE fòrmat_VALUE Mearachd: ' + loidhne)
        tomhas[Ainm] = VALUE
    return tomhas


def 등록목록(susbaint_VALUE):
    tomhas = {}
    for loidhne in susbaint_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', loidhne)
        if 일치: tomhas[일치.group(2).lower()] = 일치.group(1)
    return tomhas


def 검사합(Slighe):
    VALUE = hashlib.sha256()
    with Slighe.open('rb') as faidhle:
        for dàta in iter(lambda: faidhle.read(1024 * 1024), b''): VALUE.update(dàta)
    return VALUE.hexdigest()


class ap_drathair_nan_aplacaid:
    def __init__(self, freumh_VALUE, Ainm, dòigh_MODE='gui', àithne=gnìomhaich_slige_àithne):
        self.freumh_VALUE = Path(freumh_VALUE).resolve()
        self.Ainm, self.dòigh_MODE, self.àithne = Ainm, dòigh_MODE, àithne
        self.보관 = self.freumh_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Ainm) or Ainm in ('.', '..'):
            raise 실행오류('VM 이름은 문자·figear_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if dòigh_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Slighe(self, seise_VALUE):
        if Path(seise_VALUE).is_absolute() or '..' in Path(seise_VALUE).parts:
            raise 실행오류('잘못된 관리 Slighe: ' + str(seise_VALUE))
        tomhas = self.보관
        for 부분 in ['.vbox'] + list(Path(seise_VALUE).parts):
            if 부분 == '.vbox': tomhas = self.보관
            else: tomhas = tomhas / 부분
            if tomhas.is_symlink(): raise 실행오류('CONNECT 경로는 사용하지 않습니다: ' + str(tomhas))
        return tomhas

    def 읽기(self):
        Slighe = self.Slighe('state.json')
        if not Slighe.exists(): return None
        cor_VALUE = json.loads(Slighe.read_text(encoding='utf-8'))
        if cor_VALUE.get('version') != 1 or cor_VALUE.get('name') != self.Ainm:
            raise 실행오류('관리 상태의 VM Ainm/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Ainm in ('uuid', 'owner'):
            if str(uuid.UUID(cor_VALUE[Ainm])) != cor_VALUE[Ainm]: raise 실행오류('잘못된 VM aithnichear_VALUE')
        return cor_VALUE

    def Store_VALUE(self, cor_VALUE):
        ceann_uidhe_VALUE = self.Slighe('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as faidhle:
            json.dump(cor_VALUE, faidhle, ensure_ascii=False, indent=2)
            faidhle.write('\n')
            임시 = faidhle.name
        os.replace(임시, str(ceann_uidhe_VALUE))

    def msinfo32_exe(self, cor_VALUE, 등록됨, aisig_cor=False):
        if cor_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = buadh_VALUE(self.àithne(['VBoxManage', 'showvminfo', cor_VALUE['uuid'], '--machinereadable']))
        suidhich = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.Slighe('machines').resolve() not in suidhich.parents or msinfo32_exe.get('UUID') != cor_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM roghainnean Slighe/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.àithne(['VBoxManage', 'getextradata', cor_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + cor_VALUE['owner']:
            if aisig_cor and cor_VALUE.get('pending') and 표식 == 'No value set!':
                self.àithne(['VBoxManage', 'setextradata', cor_VALUE['uuid'], 'JKOROS/Owner', cor_VALUE['owner']])
            else:
                raise 실행오류('VM sealbhadair_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def seic_meadhanan(self, cor_VALUE, msinfo32_exe):
        제어기들 = [VALUE for Ainm, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Ainm)]
        Ceadaich_VALUE = [str(self.Slighe(VALUE)) for VALUE in cor_VALUE.get('media', [])]
        for Ainm, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(smachdair) + r'-\d+-\d+', Ainm) for smachdair in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Ceadaich_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def show_cor(self):
        cor_VALUE = self.읽기()
        if cor_VALUE is None: return {'name': self.Ainm, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(cor_VALUE, 등록목록(self.àithne(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', cor_VALUE['name']), 'uuid': cor_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.Slighe(cor_VALUE['iso'])) if cor_VALUE.get('iso') else None,
                'serial_log': str(self.Slighe(cor_VALUE['serial_log'])) if cor_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def gnìomhaich_àithne(self):
        cor_VALUE = self.읽기()
        등록됨 = 등록목록(self.àithne(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if cor_VALUE is not None and cor_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(cor_VALUE, 등록됨, aisig_cor=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 gnìomhaich_àithne 중입니다. 재빌드·재시작하지 않습니다.')
                return self.show_cor()
            self.seic_meadhanan(cor_VALUE, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.àithne(['VBoxManage', 'controlvm', cor_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 fosgail 전에 기존 기록도 보관한다.
                    if cor_VALUE.get('serial_log'):
                        원본 = self.Slighe(cor_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Slighe('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.àithne(['VBoxManage', 'startvm', cor_VALUE['uuid'], '--type', self.dòigh_MODE])
                return self.show_cor()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 Air_ais_VALUE 다시 실행하세요.'.format(현재))
        elif cor_VALUE is not None and not cor_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Ainm in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/gnìomhaich_àithne 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.àithne(['make', '-C', str(self.freumh_VALUE / 'os'), 'iso']), end='')
        원본 = self.freumh_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        meadhanan_VALUE = 'media/kernel-' + 검사합(원본) + '.iso'
        ceann_uidhe_VALUE = self.Slighe(meadhanan_VALUE)
        ceann_uidhe_VALUE.parent.mkdir(exist_ok=True)
        if ceann_uidhe_VALUE.exists():
            if 검사합(ceann_uidhe_VALUE) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(ceann_uidhe_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(ceann_uidhe_VALUE.parent)) as faidhle:
                shutil.copyfile(str(원본), faidhle.name)
                os.link(faidhle.name, str(ceann_uidhe_VALUE))

        if cor_VALUE is None:
            cor_VALUE = {'version': 1, 'name': self.Ainm, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(cor_VALUE)
        if msinfo32_exe is None:
            self.àithne(['VBoxManage', 'createvm', '--name', cor_VALUE['name'], '--uuid', cor_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Slighe('machines')), '--register'])
            self.àithne(['VBoxManage', 'setextradata', cor_VALUE['uuid'], 'JKOROS/Owner', cor_VALUE['owner']])
        # tog_siostam 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(cor_VALUE, 등록목록(self.àithne(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('tog_siostam 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.seic_meadhanan(cor_VALUE, msinfo32_exe)
        cor_VALUE['iso'] = meadhanan_VALUE
        if meadhanan_VALUE not in cor_VALUE['media']: cor_VALUE['media'].append(meadhanan_VALUE)
        cor_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.Slighe(cor_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(cor_VALUE)
        self.àithne(['VBoxManage', 'modifyvm', cor_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Ainm, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Ainm)]
        if 'JKOROS IDE' not in 제어기들:
            self.àithne(['VBoxManage', 'storagectl', cor_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.àithne(['VBoxManage', 'storageattach', cor_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(ceann_uidhe_VALUE)])
        cor_VALUE['pending'] = False
        self.Store_VALUE(cor_VALUE)
        self.àithne(['VBoxManage', 'startvm', cor_VALUE['uuid'], '--type', self.dòigh_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.show_cor()


def ruith():
    해석 = argparse.ArgumentParser(description='jkoros 전용 VirtualBox gnìomhaich_àithne 및 cor_VALUE ceist_VALUE')
    해석.add_argument('action', choices=['run', 'status'])
    인자 = 해석.parse_args()
    gnìomhaich_àithne = ap_drathair_nan_aplacaid(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(gnìomhaich_àithne.show_cor(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. òstair 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/cead_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    gnìomhaich_àithne.Slighe('lock').parent.mkdir(parents=True, exist_ok=True)
    with gnìomhaich_àithne.Slighe('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox gnìomhaich_àithne 작업이 진행 중입니다.')
        print(json.dumps(gnìomhaich_àithne.gnìomhaich_àithne(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: ruith()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Mearachd:
        print('VBOX Mearachd: ' + str(Mearachd), file=sys.stderr)
        sys.exit(1)
