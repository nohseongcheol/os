#!/usr/bin/env python3
"""jkoros 전용 VirtualBox programu_droo_ya_programu. 기존 VM/디스크/Store_thamani 상태는 삭제하지 않는다."""
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


def tekeleza_sheli_amri(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(thamani) for thamani in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    maudhui_thamani = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('amri kushindwa_thamani: ' + ' '.join(str(thamani) for thamani in 인수) + '\n' + maudhui_thamani[-10000:])
    return maudhui_thamani


def sifa_thamani(maudhui_thamani):
    결과 = {}
    for laini in maudhui_thamani.splitlines():
        if '=' not in laini:
            continue
        Jina, thamani = laini.split('=', 1)
        if Jina.startswith('"'):
            Jina = json.loads(Jina)
        if thamani.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(thamani)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(thamani): thamani = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox sifa_thamani umbiza_thamani kosa: ' + laini)
        결과[Jina] = thamani
    return 결과


def 등록목록(maudhui_thamani):
    결과 = {}
    for laini in maudhui_thamani.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', laini)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def jumla(njia):
    thamani = hashlib.sha256()
    with njia.open('rb') as faili:
        for data in iter(lambda: faili.read(1024 * 1024), b''): thamani.update(data)
    return thamani.hexdigest()


class programu_droo_ya_programu:
    def __init__(self, 뿌리, Jina, mbinu_hali_tumizi='gui', amri=tekeleza_sheli_amri):
        self.뿌리 = Path(뿌리).resolve()
        self.Jina, self.mbinu_hali_tumizi, self.amri = Jina, mbinu_hali_tumizi, amri
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Jina) or Jina in ('.', '..'):
            raise 실행오류('VM 이름은 문자·dijiti_thamani·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if mbinu_hali_tumizi not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def njia(self, kompyuta_rika_thamani):
        if Path(kompyuta_rika_thamani).is_absolute() or '..' in Path(kompyuta_rika_thamani).parts:
            raise 실행오류('잘못된 관리 njia: ' + str(kompyuta_rika_thamani))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(kompyuta_rika_thamani).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('UNGANISHA 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def 읽기(self):
        njia = self.njia('state.json')
        if not njia.exists(): return None
        hali_thamani = json.loads(njia.read_text(encoding='utf-8'))
        if hali_thamani.get('version') != 1 or hali_thamani.get('name') != self.Jina:
            raise 실행오류('관리 상태의 VM Jina/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Jina in ('uuid', 'owner'):
            if str(uuid.UUID(hali_thamani[Jina])) != hali_thamani[Jina]: raise 실행오류('잘못된 VM kitambulishi_thamani')
        return hali_thamani

    def Store_thamani(self, hali_thamani):
        fikio_thamani = self.njia('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as faili:
            json.dump(hali_thamani, faili, ensure_ascii=False, indent=2)
            faili.write('\n')
            임시 = faili.name
        os.replace(임시, str(fikio_thamani))

    def msinfo32_exe(self, hali_thamani, 등록됨, rejesha_hali=False):
        if hali_thamani['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = sifa_thamani(self.amri(['VBoxManage', 'showvminfo', hali_thamani['uuid'], '--machinereadable']))
        위치 = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.njia('machines').resolve() not in 위치.parents or msinfo32_exe.get('UUID') != hali_thamani['uuid']:
            raise 실행오류('이 프로젝트의 VM Mipangilio njia/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.amri(['VBoxManage', 'getextradata', hali_thamani['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + hali_thamani['owner']:
            if rejesha_hali and hali_thamani.get('pending') and 표식 == 'No value set!':
                self.amri(['VBoxManage', 'setextradata', hali_thamani['uuid'], 'JKOROS/Owner', hali_thamani['owner']])
            else:
                raise 실행오류('VM mmiliki_thamani 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, hali_thamani, msinfo32_exe):
        제어기들 = [thamani for Jina, thamani in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Jina)]
        Ruhusu_thamani = [str(self.njia(thamani)) for thamani in hali_thamani.get('media', [])]
        for Jina, thamani in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(mdhibiti) + r'-\d+-\d+', Jina) for mdhibiti in 제어기들):
                if thamani not in ('none', 'emptydrive') and thamani not in Ruhusu_thamani:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + thamani)

    def onyesha_hali(self):
        hali_thamani = self.읽기()
        if hali_thamani is None: return {'name': self.Jina, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(hali_thamani, 등록목록(self.amri(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', hali_thamani['name']), 'uuid': hali_thamani['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.njia(hali_thamani['iso'])) if hali_thamani.get('iso') else None,
                'serial_log': str(self.njia(hali_thamani['serial_log'])) if hali_thamani.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def tekeleza_amri(self):
        hali_thamani = self.읽기()
        등록됨 = 등록목록(self.amri(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if hali_thamani is not None and hali_thamani['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(hali_thamani, 등록됨, rejesha_hali=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 tekeleza_amri 중입니다. 재빌드·재시작하지 않습니다.')
                return self.onyesha_hali()
            self.매체검사(hali_thamani, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_thamani 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.amri(['VBoxManage', 'controlvm', hali_thamani['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 unda 전에 기존 기록도 보관한다.
                    if hali_thamani.get('serial_log'):
                        원본 = self.njia(hali_thamani['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.njia('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.amri(['VBoxManage', 'startvm', hali_thamani['uuid'], '--type', self.mbinu_hali_tumizi])
                return self.onyesha_hali()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 badili_hali_tumizi 중입니다 ({}). 작업이 끝난 Nyuma_thamani 다시 실행하세요.'.format(현재))
        elif hali_thamani is not None and not hali_thamani.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Jina in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_thamani/tekeleza_amri 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.amri(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + jumla(원본) + '.iso'
        fikio_thamani = self.njia(매체)
        fikio_thamani.parent.mkdir(exist_ok=True)
        if fikio_thamani.exists():
            if jumla(fikio_thamani) != jumla(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(fikio_thamani))
        else:
            with tempfile.NamedTemporaryFile(dir=str(fikio_thamani.parent)) as faili:
                shutil.copyfile(str(원본), faili.name)
                os.link(faili.name, str(fikio_thamani))

        if hali_thamani is None:
            hali_thamani = {'version': 1, 'name': self.Jina, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_thamani(hali_thamani)
        if msinfo32_exe is None:
            self.amri(['VBoxManage', 'createvm', '--name', hali_thamani['name'], '--uuid', hali_thamani['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.njia('machines')), '--register'])
            self.amri(['VBoxManage', 'setextradata', hali_thamani['uuid'], 'JKOROS/Owner', hali_thamani['owner']])
        # jenga_mfumo 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(hali_thamani, 등록목록(self.amri(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('jenga_mfumo 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(hali_thamani, msinfo32_exe)
        hali_thamani['iso'] = 매체
        if 매체 not in hali_thamani['media']: hali_thamani['media'].append(매체)
        hali_thamani['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        batli_thamani = self.njia(hali_thamani['serial_log'])
        batli_thamani.parent.mkdir(exist_ok=True)
        self.Store_thamani(hali_thamani)
        self.amri(['VBoxManage', 'modifyvm', hali_thamani['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(batli_thamani)])
        제어기들 = [thamani for Jina, thamani in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Jina)]
        if 'JKOROS IDE' not in 제어기들:
            self.amri(['VBoxManage', 'storagectl', hali_thamani['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.amri(['VBoxManage', 'storageattach', hali_thamani['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(fikio_thamani)])
        hali_thamani['pending'] = False
        self.Store_thamani(hali_thamani)
        self.amri(['VBoxManage', 'startvm', hali_thamani['uuid'], '--type', self.mbinu_hali_tumizi])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.onyesha_hali()


def endesha():
    changanua_thamani = argparse.ArgumentParser(description='jkoros 전용 VirtualBox tekeleza_amri 및 hali_thamani uliza_thamani')
    changanua_thamani.add_argument('action', choices=['run', 'status'])
    parameta_hoja = changanua_thamani.parse_args()
    tekeleza_amri = programu_droo_ya_programu(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if parameta_hoja.action == 'status':
        print(json.dumps(tekeleza_amri.onyesha_hali(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. mwenyeji 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/kibali_thamani 변경은 하지 않습니다.')
    os.umask(0o077)
    tekeleza_amri.njia('lock').parent.mkdir(parents=True, exist_ok=True)
    with tekeleza_amri.njia('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox tekeleza_amri 작업이 진행 중입니다.')
        print(json.dumps(tekeleza_amri.tekeleza_amri(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: endesha()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as kosa:
        print('VBOX kosa: ' + str(kosa), file=sys.stderr)
        sys.exit(1)
