#!/usr/bin/env python3
"""jkoros 전용 VirtualBox jëfekaay_armuwaaru_jëfekaay. 기존 VM/디스크/Store_xëyma 상태는 삭제하지 않는다."""
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


def def_Wëreef_ndigel(인수):
    환경 = dict(os.environ, LC_ALL='C')
    결과 = subprocess.run([str(xëyma) for xëyma in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Këmb_xëyma = 결과.stdout.decode('utf-8', 'replace')
    if 결과.returncode:
        raise 실행오류('ndigel foo_xëyma: ' + ' '.join(str(xëyma) for xëyma in 인수) + '\n' + Këmb_xëyma[-10000:])
    return Këmb_xëyma


def jagle_xëyma(Këmb_xëyma):
    결과 = {}
    for buum in Këmb_xëyma.splitlines():
        if '=' not in buum:
            continue
        tur_253d1510, xëyma = buum.split('=', 1)
        if tur_253d1510.startswith('"'):
            tur_253d1510 = json.loads(tur_253d1510)
        if xëyma.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(xëyma)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(xëyma): xëyma = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox jagle_xëyma dayo_xëyma njumte: ' + buum)
        결과[tur_253d1510] = xëyma
    return 결과


def 등록목록(Këmb_xëyma):
    결과 = {}
    for buum in Këmb_xëyma.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', buum)
        if 일치: 결과[일치.group(2).lower()] = 일치.group(1)
    return 결과


def 검사합(Yoonu_jëmale):
    xëyma = hashlib.sha256()
    with Yoonu_jëmale.open('rb') as bara_denc:
        for mbir in iter(lambda: bara_denc.read(1024 * 1024), b''): xëyma.update(mbir)
    return xëyma.hexdigest()


class jëfekaay_armuwaaru_jëfekaay:
    def __init__(self, 뿌리, tur_253d1510, doxalin_anam='gui', ndigel=def_Wëreef_ndigel):
        self.뿌리 = Path(뿌리).resolve()
        self.tur_253d1510, self.doxalin_anam, self.ndigel = tur_253d1510, doxalin_anam, ndigel
        self.보관 = self.뿌리 / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', tur_253d1510) or tur_253d1510 in ('.', '..'):
            raise 실행오류('VM 이름은 문자·siifar_xëyma·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if doxalin_anam not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def Yoonu_jëmale(self, Nàttangoo_xëyma):
        if Path(Nàttangoo_xëyma).is_absolute() or '..' in Path(Nàttangoo_xëyma).parts:
            raise 실행오류('잘못된 관리 Yoonu_jëmale: ' + str(Nàttangoo_xëyma))
        결과 = self.보관
        for 부분 in ['.vbox'] + list(Path(Nàttangoo_xëyma).parts):
            if 부분 == '.vbox': 결과 = self.보관
            else: 결과 = 결과 / 부분
            if 결과.is_symlink(): raise 실행오류('JOKKOO 경로는 사용하지 않습니다: ' + str(결과))
        return 결과

    def 읽기(self):
        Yoonu_jëmale = self.Yoonu_jëmale('state.json')
        if not Yoonu_jëmale.exists(): return None
        nekkin_xëyma = json.loads(Yoonu_jëmale.read_text(encoding='utf-8'))
        if nekkin_xëyma.get('version') != 1 or nekkin_xëyma.get('name') != self.tur_253d1510:
            raise 실행오류('관리 상태의 VM tur_253d1510/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for tur_253d1510 in ('uuid', 'owner'):
            if str(uuid.UUID(nekkin_xëyma[tur_253d1510])) != nekkin_xëyma[tur_253d1510]: raise 실행오류('잘못된 VM raññeekaay_xëyma')
        return nekkin_xëyma

    def Store_xëyma(self, nekkin_xëyma):
        jëmmukaay_xëyma = self.Yoonu_jëmale('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as bara_denc:
            json.dump(nekkin_xëyma, bara_denc, ensure_ascii=False, indent=2)
            bara_denc.write('\n')
            임시 = bara_denc.name
        os.replace(임시, str(jëmmukaay_xëyma))

    def msinfo32_exe(self, nekkin_xëyma, 등록됨, defaru_nekkin=False):
        if nekkin_xëyma['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = jagle_xëyma(self.ndigel(['VBoxManage', 'showvminfo', nekkin_xëyma['uuid'], '--machinereadable']))
        위치 = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.Yoonu_jëmale('machines').resolve() not in 위치.parents or msinfo32_exe.get('UUID') != nekkin_xëyma['uuid']:
            raise 실행오류('이 프로젝트의 VM Jekkal_yi Yoonu_jëmale/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.ndigel(['VBoxManage', 'getextradata', nekkin_xëyma['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + nekkin_xëyma['owner']:
            if defaru_nekkin and nekkin_xëyma.get('pending') and 표식 == 'No value set!':
                self.ndigel(['VBoxManage', 'setextradata', nekkin_xëyma['uuid'], 'JKOROS/Owner', nekkin_xëyma['owner']])
            else:
                raise 실행오류('VM boroom_xëyma 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def sek_yebuwaay(self, nekkin_xëyma, msinfo32_exe):
        제어기들 = [xëyma for tur_253d1510, xëyma in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', tur_253d1510)]
        Maye_xëyma = [str(self.Yoonu_jëmale(xëyma)) for xëyma in nekkin_xëyma.get('media', [])]
        for tur_253d1510, xëyma in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(제어기) + r'-\d+-\d+', tur_253d1510) for 제어기 in 제어기들):
                if xëyma not in ('none', 'emptydrive') and xëyma not in Maye_xëyma:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + xëyma)

    def féeñal_nekkin(self):
        nekkin_xëyma = self.읽기()
        if nekkin_xëyma is None: return {'name': self.tur_253d1510, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(nekkin_xëyma, 등록목록(self.ndigel(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', nekkin_xëyma['name']), 'uuid': nekkin_xëyma['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.Yoonu_jëmale(nekkin_xëyma['iso'])) if nekkin_xëyma.get('iso') else None,
                'serial_log': str(self.Yoonu_jëmale(nekkin_xëyma['serial_log'])) if nekkin_xëyma.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def def_ndigel(self):
        nekkin_xëyma = self.읽기()
        등록됨 = 등록목록(self.ndigel(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if nekkin_xëyma is not None and nekkin_xëyma['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(nekkin_xëyma, 등록됨, defaru_nekkin=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 def_ndigel 중입니다. 재빌드·재시작하지 않습니다.')
                return self.féeñal_nekkin()
            self.sek_yebuwaay(nekkin_xëyma, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_xëyma 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.ndigel(['VBoxManage', 'controlvm', nekkin_xëyma['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 sos 전에 기존 기록도 보관한다.
                    if nekkin_xëyma.get('serial_log'):
                        원본 = self.Yoonu_jëmale(nekkin_xëyma['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.Yoonu_jëmale('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.ndigel(['VBoxManage', 'startvm', nekkin_xëyma['uuid'], '--type', self.doxalin_anam])
                return self.féeñal_nekkin()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 jalantu_anam 중입니다 ({}). 작업이 끝난 woñeeku_xëyma 다시 실행하세요.'.format(현재))
        elif nekkin_xëyma is not None and not nekkin_xëyma.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.tur_253d1510 in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_xëyma/def_ndigel 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.ndigel(['make', '-C', str(self.뿌리 / 'os'), 'iso']), end='')
        원본 = self.뿌리 / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        yebuwaay_xëyma = 'media/kernel-' + 검사합(원본) + '.iso'
        jëmmukaay_xëyma = self.Yoonu_jëmale(yebuwaay_xëyma)
        jëmmukaay_xëyma.parent.mkdir(exist_ok=True)
        if jëmmukaay_xëyma.exists():
            if 검사합(jëmmukaay_xëyma) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(jëmmukaay_xëyma))
        else:
            with tempfile.NamedTemporaryFile(dir=str(jëmmukaay_xëyma.parent)) as bara_denc:
                shutil.copyfile(str(원본), bara_denc.name)
                os.link(bara_denc.name, str(jëmmukaay_xëyma))

        if nekkin_xëyma is None:
            nekkin_xëyma = {'version': 1, 'name': self.tur_253d1510, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_xëyma(nekkin_xëyma)
        if msinfo32_exe is None:
            self.ndigel(['VBoxManage', 'createvm', '--name', nekkin_xëyma['name'], '--uuid', nekkin_xëyma['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.Yoonu_jëmale('machines')), '--register'])
            self.ndigel(['VBoxManage', 'setextradata', nekkin_xëyma['uuid'], 'JKOROS/Owner', nekkin_xëyma['owner']])
        # tabax_kureel 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(nekkin_xëyma, 등록목록(self.ndigel(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('tabax_kureel 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.sek_yebuwaay(nekkin_xëyma, msinfo32_exe)
        nekkin_xëyma['iso'] = yebuwaay_xëyma
        if yebuwaay_xëyma not in nekkin_xëyma['media']: nekkin_xëyma['media'].append(yebuwaay_xëyma)
        nekkin_xëyma['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        làq_xëyma = self.Yoonu_jëmale(nekkin_xëyma['serial_log'])
        làq_xëyma.parent.mkdir(exist_ok=True)
        self.Store_xëyma(nekkin_xëyma)
        self.ndigel(['VBoxManage', 'modifyvm', nekkin_xëyma['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(làq_xëyma)])
        제어기들 = [xëyma for tur_253d1510, xëyma in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', tur_253d1510)]
        if 'JKOROS IDE' not in 제어기들:
            self.ndigel(['VBoxManage', 'storagectl', nekkin_xëyma['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.ndigel(['VBoxManage', 'storageattach', nekkin_xëyma['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(jëmmukaay_xëyma)])
        nekkin_xëyma['pending'] = False
        self.Store_xëyma(nekkin_xëyma)
        self.ndigel(['VBoxManage', 'startvm', nekkin_xëyma['uuid'], '--type', self.doxalin_anam])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.féeñal_nekkin()


def daw():
    Segg_xëyma = argparse.ArgumentParser(description='jkoros 전용 VirtualBox def_ndigel 및 nekkin_xëyma laaj_xëyma')
    Segg_xëyma.add_argument('action', choices=['run', 'status'])
    인자 = Segg_xëyma.parse_args()
    def_ndigel = jëfekaay_armuwaaru_jëfekaay(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(def_ndigel.féeñal_nekkin(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. dalal 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/sañ_sañ_xëyma 변경은 하지 않습니다.')
    os.umask(0o077)
    def_ndigel.Yoonu_jëmale('lock').parent.mkdir(parents=True, exist_ok=True)
    with def_ndigel.Yoonu_jëmale('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox def_ndigel 작업이 진행 중입니다.')
        print(json.dumps(def_ndigel.def_ndigel(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: daw()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as njumte:
        print('VBOX njumte: ' + str(njumte), file=sys.stderr)
        sys.exit(1)
