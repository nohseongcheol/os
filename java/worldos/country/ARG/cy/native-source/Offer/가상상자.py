#!/usr/bin/env python3
"""jkoros 전용 VirtualBox Rhaglen_lansiwr. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def Gweithredu_cragen_gorchymyn(인수):
    환경 = dict(os.environ, LC_ALL='C')
    mesur = subprocess.run([str(VALUE) for VALUE in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Cynnwys_VALUE = mesur.stdout.decode('utf-8', 'replace')
    if mesur.returncode:
        raise 실행오류('Gorchymyn methiant_VALUE: ' + ' '.join(str(VALUE) for VALUE in 인수) + '\n' + Cynnwys_VALUE[-10000:])
    return Cynnwys_VALUE


def priodoledd_VALUE(Cynnwys_VALUE):
    mesur = {}
    for llinell in Cynnwys_VALUE.splitlines():
        if '=' not in llinell:
            continue
        Enw, VALUE = llinell.split('=', 1)
        if Enw.startswith('"'):
            Enw = json.loads(Enw)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox priodoledd_VALUE fformat_VALUE Gwall: ' + llinell)
        mesur[Enw] = VALUE
    return mesur


def 등록목록(Cynnwys_VALUE):
    mesur = {}
    for llinell in Cynnwys_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', llinell)
        if 일치: mesur[일치.group(2).lower()] = 일치.group(1)
    return mesur


def prawfswm(LLWYBR):
    VALUE = hashlib.sha256()
    with LLWYBR.open('rb') as Ffeil:
        for data in iter(lambda: Ffeil.read(1024 * 1024), b''): VALUE.update(data)
    return VALUE.hexdigest()


class Rhaglen_lansiwr:
    def __init__(self, gwraidd_VALUE, Enw, dull_MODE='gui', Gorchymyn=Gweithredu_cragen_gorchymyn):
        self.gwraidd_VALUE = Path(gwraidd_VALUE).resolve()
        self.Enw, self.dull_MODE, self.Gorchymyn = Enw, dull_MODE, Gorchymyn
        self.보관 = self.gwraidd_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Enw) or Enw in ('.', '..'):
            raise 실행오류('VM 이름은 문자·digid_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if dull_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def LLWYBR(self, cymar_VALUE):
        if Path(cymar_VALUE).is_absolute() or '..' in Path(cymar_VALUE).parts:
            raise 실행오류('잘못된 관리 LLWYBR: ' + str(cymar_VALUE))
        mesur = self.보관
        for 부분 in ['.vbox'] + list(Path(cymar_VALUE).parts):
            if 부분 == '.vbox': mesur = self.보관
            else: mesur = mesur / 부분
            if mesur.is_symlink(): raise 실행오류('Cysylltu 경로는 사용하지 않습니다: ' + str(mesur))
        return mesur

    def Darllen(self):
        LLWYBR = self.LLWYBR('state.json')
        if not LLWYBR.exists(): return None
        cyflwr_VALUE = json.loads(LLWYBR.read_text(encoding='utf-8'))
        if cyflwr_VALUE.get('version') != 1 or cyflwr_VALUE.get('name') != self.Enw:
            raise 실행오류('관리 상태의 VM Enw/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Enw in ('uuid', 'owner'):
            if str(uuid.UUID(cyflwr_VALUE[Enw])) != cyflwr_VALUE[Enw]: raise 실행오류('잘못된 VM dynodwr_VALUE')
        return cyflwr_VALUE

    def Store_VALUE(self, cyflwr_VALUE):
        cyrchfan_VALUE = self.LLWYBR('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Ffeil:
            json.dump(cyflwr_VALUE, Ffeil, ensure_ascii=False, indent=2)
            Ffeil.write('\n')
            임시 = Ffeil.name
        os.replace(임시, str(cyrchfan_VALUE))

    def msinfo32_exe(self, cyflwr_VALUE, 등록됨, adfer_cyflwr=False):
        if cyflwr_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = priodoledd_VALUE(self.Gorchymyn(['VBoxManage', 'showvminfo', cyflwr_VALUE['uuid'], '--machinereadable']))
        safle = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.LLWYBR('machines').resolve() not in safle.parents or msinfo32_exe.get('UUID') != cyflwr_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Gosodiadau LLWYBR/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.Gorchymyn(['VBoxManage', 'getextradata', cyflwr_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + cyflwr_VALUE['owner']:
            if adfer_cyflwr and cyflwr_VALUE.get('pending') and 표식 == 'No value set!':
                self.Gorchymyn(['VBoxManage', 'setextradata', cyflwr_VALUE['uuid'], 'JKOROS/Owner', cyflwr_VALUE['owner']])
            else:
                raise 실행오류('VM perchennog_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, cyflwr_VALUE, msinfo32_exe):
        제어기들 = [VALUE for Enw, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Enw)]
        Caniatáu_VALUE = [str(self.LLWYBR(VALUE)) for VALUE in cyflwr_VALUE.get('media', [])]
        for Enw, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(rheolydd) + r'-\d+-\d+', Enw) for rheolydd in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in Caniatáu_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def sioe_cyflwr(self):
        cyflwr_VALUE = self.Darllen()
        if cyflwr_VALUE is None: return {'name': self.Enw, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(cyflwr_VALUE, 등록목록(self.Gorchymyn(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', cyflwr_VALUE['name']), 'uuid': cyflwr_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.LLWYBR(cyflwr_VALUE['iso'])) if cyflwr_VALUE.get('iso') else None,
                'serial_log': str(self.LLWYBR(cyflwr_VALUE['serial_log'])) if cyflwr_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def Gweithredu_gorchymyn(self):
        cyflwr_VALUE = self.Darllen()
        등록됨 = 등록목록(self.Gorchymyn(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if cyflwr_VALUE is not None and cyflwr_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(cyflwr_VALUE, 등록됨, adfer_cyflwr=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 Gweithredu_gorchymyn 중입니다. 재빌드·재시작하지 않습니다.')
                return self.sioe_cyflwr()
            self.매체검사(cyflwr_VALUE, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.Gorchymyn(['VBoxManage', 'controlvm', cyflwr_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Agor 전에 기존 기록도 보관한다.
                    if cyflwr_VALUE.get('serial_log'):
                        원본 = self.LLWYBR(cyflwr_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.LLWYBR('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.Gorchymyn(['VBoxManage', 'startvm', cyflwr_VALUE['uuid'], '--type', self.dull_MODE])
                return self.sioe_cyflwr()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 newid_MODE 중입니다 ({}). 작업이 끝난 BACK_VALUE 다시 실행하세요.'.format(현재))
        elif cyflwr_VALUE is not None and not cyflwr_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Enw in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/Gweithredu_gorchymyn 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.Gorchymyn(['make', '-C', str(self.gwraidd_VALUE / 'os'), 'iso']), end='')
        원본 = self.gwraidd_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + prawfswm(원본) + '.iso'
        cyrchfan_VALUE = self.LLWYBR(매체)
        cyrchfan_VALUE.parent.mkdir(exist_ok=True)
        if cyrchfan_VALUE.exists():
            if prawfswm(cyrchfan_VALUE) != prawfswm(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(cyrchfan_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(cyrchfan_VALUE.parent)) as Ffeil:
                shutil.copyfile(str(원본), Ffeil.name)
                os.link(Ffeil.name, str(cyrchfan_VALUE))

        if cyflwr_VALUE is None:
            cyflwr_VALUE = {'version': 1, 'name': self.Enw, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(cyflwr_VALUE)
        if msinfo32_exe is None:
            self.Gorchymyn(['VBoxManage', 'createvm', '--name', cyflwr_VALUE['name'], '--uuid', cyflwr_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.LLWYBR('machines')), '--register'])
            self.Gorchymyn(['VBoxManage', 'setextradata', cyflwr_VALUE['uuid'], 'JKOROS/Owner', cyflwr_VALUE['owner']])
        # llunio_system 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(cyflwr_VALUE, 등록목록(self.Gorchymyn(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('llunio_system 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(cyflwr_VALUE, msinfo32_exe)
        cyflwr_VALUE['iso'] = 매체
        if 매체 not in cyflwr_VALUE['media']: cyflwr_VALUE['media'].append(매체)
        cyflwr_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.LLWYBR(cyflwr_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(cyflwr_VALUE)
        self.Gorchymyn(['VBoxManage', 'modifyvm', cyflwr_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for Enw, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Enw)]
        if 'JKOROS IDE' not in 제어기들:
            self.Gorchymyn(['VBoxManage', 'storagectl', cyflwr_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.Gorchymyn(['VBoxManage', 'storageattach', cyflwr_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(cyrchfan_VALUE)])
        cyflwr_VALUE['pending'] = False
        self.Store_VALUE(cyflwr_VALUE)
        self.Gorchymyn(['VBoxManage', 'startvm', cyflwr_VALUE['uuid'], '--type', self.dull_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.sioe_cyflwr()


def Gweithredu_2():
    dosrannu_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox Gweithredu_gorchymyn 및 cyflwr_VALUE ymholiad_VALUE')
    dosrannu_VALUE.add_argument('action', choices=['run', 'status'])
    paramedr_arg = dosrannu_VALUE.parse_args()
    Gweithredu_gorchymyn = Rhaglen_lansiwr(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if paramedr_arg.action == 'status':
        print(json.dumps(Gweithredu_gorchymyn.sioe_cyflwr(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. lletya 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/hawl_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    Gweithredu_gorchymyn.LLWYBR('lock').parent.mkdir(parents=True, exist_ok=True)
    with Gweithredu_gorchymyn.LLWYBR('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox Gweithredu_gorchymyn 작업이 진행 중입니다.')
        print(json.dumps(Gweithredu_gorchymyn.Gweithredu_gorchymyn(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: Gweithredu_2()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Gwall:
        print('VBOX Gwall: ' + str(Gwall), file=sys.stderr)
        sys.exit(1)
