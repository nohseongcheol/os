#!/usr/bin/env python3
"""jkoros 전용 VirtualBox 실행기. 기존 VM/디스크/resde_njaru 상태는 삭제하지 않는다."""
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


def 명령실행(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(njaru) for njaru in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    loowdi_njaru = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('ginol ella_njaru: ' + ' '.join(str(njaru) for njaru in 인수) + '\n' + loowdi_njaru[-10000:])
    return loowdi_njaru


def mbaadi_njaru(loowdi_njaru):
    결과 = {}
    for diidol in loowdi_njaru.splitlines():
        if '=' not in diidol:
            continue
        innde, njaru = diidol.split('=', 1)
        if innde.startswith('"'):
            innde = json.loads(innde)
        if njaru.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(njaru)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(njaru): njaru = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox mbaadi_njaru formaa_njaru juumre: ' + diidol)
        결과[innde] = njaru
    return 결과


def 등록목록(loowdi_njaru):
    결과 = {}
    for diidol in loowdi_njaru.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', diidol)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(laawol):
    njaru = hashlib.sha256()
    with laawol.open('rb') as fiilde:
        for keɓe in iter(lambda: fiilde.read(1024 * 1024), b''): njaru.update(keɓe)
    return njaru.hexdigest()


class 실행기:
    def __init__(self, 뿌리, innde, 방식='gui', ginol=명령실행):
        self.뿌리 = Path(뿌리).resolve()
        self.innde, self.방식, self.ginol = innde, 방식, ginol
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', innde) or innde in ('.', '..'):
            raise 실행오류('VM 이름은 문자·숫자·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if 방식 not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def laawol(self, giƴiraaɗo_njaru):
        if Path(giƴiraaɗo_njaru).is_absolute() or '..' in Path(giƴiraaɗo_njaru).parts:
            raise 실행오류('잘못된 관리 laawol: ' + str(giƴiraaɗo_njaru))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(giƴiraaɗo_njaru).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('seŋaade 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def 읽기(self):
        laawol = self.laawol('state.json')
        if not laawol.exists(): return None
        ngonka_njaru = json.loads(laawol.read_text(encoding='utf-8'))
        if ngonka_njaru.get('version') != 1 or ngonka_njaru.get('name') != self.innde:
            raise 실행오류('관리 상태의 VM innde/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for innde in ('uuid', 'owner'):
            if str(uuid.UUID(ngonka_njaru[innde])) != ngonka_njaru[innde]: raise 실행오류('잘못된 VM 식별자')
        return ngonka_njaru

    def resde_njaru(self, ngonka_njaru):
        tiindaare_njaru = self.laawol('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as fiilde:
            json.dump(ngonka_njaru, fiilde, ensure_ascii=False, indent=2)
            fiilde.write('\n')
            임시 = fiilde.name
        os.replace(임시, str(tiindaare_njaru))

    def msinfo32_exe(self, ngonka_njaru, 등록됨, 복구=False):
        if ngonka_njaru['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = mbaadi_njaru(self.ginol(['VBoxManage', 'showvminfo', ngonka_njaru['uuid'], '--machinereadable']))
        위치 = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.laawol('machines').resolve() not in 위치.parents or msinfo32_exe.get('UUID') != ngonka_njaru['uuid']:
            raise 실행오류('이 프로젝트의 VM 설정 laawol/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.ginol(['VBoxManage', 'getextradata', ngonka_njaru['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + ngonka_njaru['owner']:
            if 복구 and ngonka_njaru.get('pending') and 표식 == 'No value set!':
                self.ginol(['VBoxManage', 'setextradata', ngonka_njaru['uuid'], 'JKOROS/Owner', ngonka_njaru['owner']])
            else:
                raise 실행오류('VM 소유 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def sek_mejaare(self, ngonka_njaru, msinfo32_exe):
        제어기들 = [njaru for innde, njaru in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', innde)]
        Wellit_njaru = [str(self.laawol(njaru)) for njaru in ngonka_njaru.get('media', [])]
        for innde, njaru in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', innde) for 제어기 in 제어기들):
                if njaru not in ('none', 'emptydrive') and njaru not in Wellit_njaru:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + njaru)

    def hollirde_ngonka(self):
        ngonka_njaru = self.읽기()
        if ngonka_njaru is None: return {'name': self.innde, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(ngonka_njaru, 등록목록(self.ginol(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', ngonka_njaru['name']), 'uuid': ngonka_njaru['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.laawol(ngonka_njaru['iso'])) if ngonka_njaru.get('iso') else None,
                'serial_log': str(self.laawol(ngonka_njaru['serial_log'])) if ngonka_njaru.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def 실행(self):
        ngonka_njaru = self.읽기()
        등록됨 = 등록목록(self.ginol(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if ngonka_njaru is not None and ngonka_njaru['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(ngonka_njaru, 등록됨, 복구=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 실행 중입니다. 재빌드·재시작하지 않습니다.')
                return self.hollirde_ngonka()
            self.sek_mejaare(ngonka_njaru, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 resde_njaru 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.ginol(['VBoxManage', 'controlvm', ngonka_njaru['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 udditde 전에 기존 기록도 보관한다.
                    if ngonka_njaru.get('serial_log'):
                        원본 = self.laawol(ngonka_njaru['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.laawol('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.ginol(['VBoxManage', 'startvm', ngonka_njaru['uuid'], '--type', self.방식])
                return self.hollirde_ngonka()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 waylude_modd 중입니다 ({}). 작업이 끝난 Caggal_njaru 다시 실행하세요.'.format(현재))
        elif ngonka_njaru is not None and not ngonka_njaru.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.innde in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # resde_njaru/실행 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.ginol(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        mejaare_njaru = 'media/kernel-' + 검사합(원본) + '.iso'
        tiindaare_njaru = self.laawol(mejaare_njaru)
        tiindaare_njaru.parent.mkdir(exist_ok=True)
        if tiindaare_njaru.exists():
            if 검사합(tiindaare_njaru) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(tiindaare_njaru))
        else:
            with tempfile.NamedTemporaryFile(dir=str(tiindaare_njaru.parent)) as fiilde:
                shutil.copyfile(str(원본), fiilde.name)
                os.link(fiilde.name, str(tiindaare_njaru))

        if ngonka_njaru is None:
            ngonka_njaru = {'version': 1, 'name': self.innde, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.resde_njaru(ngonka_njaru)
        if msinfo32_exe is None:
            self.ginol(['VBoxManage', 'createvm', '--name', ngonka_njaru['name'], '--uuid', ngonka_njaru['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.laawol('machines')), '--register'])
            self.ginol(['VBoxManage', 'setextradata', ngonka_njaru['uuid'], 'JKOROS/Owner', ngonka_njaru['owner']])
        # tafde_yuɓɓo 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(ngonka_njaru, 등록목록(self.ginol(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('tafde_yuɓɓo 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.sek_mejaare(ngonka_njaru, msinfo32_exe)
        ngonka_njaru['iso'] = mejaare_njaru
        if mejaare_njaru not in ngonka_njaru['media']: ngonka_njaru['media'].append(mejaare_njaru)
        ngonka_njaru['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        suurnal_njaru = self.laawol(ngonka_njaru['serial_log'])
        suurnal_njaru.parent.mkdir(exist_ok=True)
        self.resde_njaru(ngonka_njaru)
        self.ginol(['VBoxManage', 'modifyvm', ngonka_njaru['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(suurnal_njaru)])
        제어기들 = [njaru for innde, njaru in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', innde)]
        if 'JKOROS IDE' not in 제어기들:
            self.ginol(['VBoxManage', 'storagectl', ngonka_njaru['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.ginol(['VBoxManage', 'storageattach', ngonka_njaru['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(tiindaare_njaru)])
        ngonka_njaru['pending'] = False
        self.resde_njaru(ngonka_njaru)
        self.ginol(['VBoxManage', 'startvm', ngonka_njaru['uuid'], '--type', self.방식])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.hollirde_ngonka()


def huutoraade():
    해석 = argparse.ArgumentParser(description='jkoros 전용 VirtualBox 실행 및 ngonka_njaru ɗaɓɓal_njaru')
    해석.add_argument('action', choices=['run', 'status'])
    인자 = 해석.parse_args()
    실행 = 실행기(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(실행.hollirde_ngonka(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. njaatigi 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/권한 변경은 하지 않습니다.')
    os.umask(0o077)
    실행.laawol('lock').parent.mkdir(parents=True, exist_ok=True)
    with 실행.laawol('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox 실행 작업이 진행 중입니다.')
        print(json.dumps(실행.실행(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: huutoraade()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as juumre:
        print('VBOX juumre: ' + str(juumre), file=sys.stderr)
        sys.exit(1)
