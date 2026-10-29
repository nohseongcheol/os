#!/usr/bin/env python3
"""jkoros 전용 VirtualBox programm_ġabra_ta_apps. 기존 VM/디스크/Store_VALUE 상태는 삭제하지 않는다."""
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


def eżegwixxa_shell_kmand(인수):
    환경 = dict(os.environ, LC_ALL='C')
    miżura = subprocess.run([str(VALUE) for VALUE in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Kontenut_VALUE = miżura.stdout.decode('utf-8', 'replace')
    if miżura.returncode:
        raise 실행오류('kmand żball_VALUE: ' + ' '.join(str(VALUE) for VALUE in 인수) + '\n' + Kontenut_VALUE[-10000:])
    return Kontenut_VALUE


def attribut_VALUE(Kontenut_VALUE):
    miżura = {}
    for linja in Kontenut_VALUE.splitlines():
        if '=' not in linja:
            continue
        isem, VALUE = linja.split('=', 1)
        if isem.startswith('"'):
            isem = json.loads(isem)
        if VALUE.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(VALUE)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(VALUE): VALUE = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox attribut_VALUE format_VALUE żball: ' + linja)
        miżura[isem] = VALUE
    return miżura


def 등록목록(Kontenut_VALUE):
    miżura = {}
    for linja in Kontenut_VALUE.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', linja)
        if 일치: miżura[일치.group(2).lower()] = 일치.group(1)
    return miżura


def 검사합(mogħdija):
    VALUE = hashlib.sha256()
    with mogħdija.open('rb') as fajl:
        for data in iter(lambda: fajl.read(1024 * 1024), b''): VALUE.update(data)
    return VALUE.hexdigest()


class programm_ġabra_ta_apps:
    def __init__(self, għerq_VALUE, isem, metodu_MODE='gui', kmand=eżegwixxa_shell_kmand):
        self.għerq_VALUE = Path(għerq_VALUE).resolve()
        self.isem, self.metodu_MODE, self.kmand = isem, metodu_MODE, kmand
        self.보관 = self.għerq_VALUE / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', isem) or isem in ('.', '..'):
            raise 실행오류('VM 이름은 문자·ċifra_VALUE·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if metodu_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def mogħdija(self, peer_VALUE):
        if Path(peer_VALUE).is_absolute() or '..' in Path(peer_VALUE).parts:
            raise 실행오류('잘못된 관리 mogħdija: ' + str(peer_VALUE))
        miżura = self.보관
        for 부분 in ['.vbox'] + list(Path(peer_VALUE).parts):
            if 부분 == '.vbox': miżura = self.보관
            else: miżura = miżura / 부분
            if miżura.is_symlink(): raise 실행오류('AQBAD 경로는 사용하지 않습니다: ' + str(miżura))
        return miżura

    def 읽기(self):
        mogħdija = self.mogħdija('state.json')
        if not mogħdija.exists(): return None
        stat_VALUE = json.loads(mogħdija.read_text(encoding='utf-8'))
        if stat_VALUE.get('version') != 1 or stat_VALUE.get('name') != self.isem:
            raise 실행오류('관리 상태의 VM isem/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for isem in ('uuid', 'owner'):
            if str(uuid.UUID(stat_VALUE[isem])) != stat_VALUE[isem]: raise 실행오류('잘못된 VM identifikatur_VALUE')
        return stat_VALUE

    def Store_VALUE(self, stat_VALUE):
        destinazzjoni_VALUE = self.mogħdija('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as fajl:
            json.dump(stat_VALUE, fajl, ensure_ascii=False, indent=2)
            fajl.write('\n')
            임시 = fajl.name
        os.replace(임시, str(destinazzjoni_VALUE))

    def msinfo32_exe(self, stat_VALUE, 등록됨, rkupra_stat=False):
        if stat_VALUE['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = attribut_VALUE(self.kmand(['VBoxManage', 'showvminfo', stat_VALUE['uuid'], '--machinereadable']))
        pożizzjoni = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.mogħdija('machines').resolve() not in pożizzjoni.parents or msinfo32_exe.get('UUID') != stat_VALUE['uuid']:
            raise 실행오류('이 프로젝트의 VM Settings mogħdija/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.kmand(['VBoxManage', 'getextradata', stat_VALUE['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + stat_VALUE['owner']:
            if rkupra_stat and stat_VALUE.get('pending') and 표식 == 'No value set!':
                self.kmand(['VBoxManage', 'setextradata', stat_VALUE['uuid'], 'JKOROS/Owner', stat_VALUE['owner']])
            else:
                raise 실행오류('VM propjetarju_VALUE 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def 매체검사(self, stat_VALUE, msinfo32_exe):
        제어기들 = [VALUE for isem, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', isem)]
        ppermetti_VALUE = [str(self.mogħdija(VALUE)) for VALUE in stat_VALUE.get('media', [])]
        for isem, VALUE in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(kontrollur) + r'-\d+-\d+', isem) for kontrollur in 제어기들):
                if VALUE not in ('none', 'emptydrive') and VALUE not in ppermetti_VALUE:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + VALUE)

    def wera_stat(self):
        stat_VALUE = self.읽기()
        if stat_VALUE is None: return {'name': self.isem, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(stat_VALUE, 등록목록(self.kmand(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', stat_VALUE['name']), 'uuid': stat_VALUE['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.mogħdija(stat_VALUE['iso'])) if stat_VALUE.get('iso') else None,
                'serial_log': str(self.mogħdija(stat_VALUE['serial_log'])) if stat_VALUE.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def eżegwixxa_kmand(self):
        stat_VALUE = self.읽기()
        등록됨 = 등록목록(self.kmand(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if stat_VALUE is not None and stat_VALUE['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(stat_VALUE, 등록됨, rkupra_stat=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 eżegwixxa_kmand 중입니다. 재빌드·재시작하지 않습니다.')
                return self.wera_stat()
            self.매체검사(stat_VALUE, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_VALUE 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.kmand(['VBoxManage', 'controlvm', stat_VALUE['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 fetaħ 전에 기존 기록도 보관한다.
                    if stat_VALUE.get('serial_log'):
                        원본 = self.mogħdija(stat_VALUE['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.mogħdija('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.kmand(['VBoxManage', 'startvm', stat_VALUE['uuid'], '--type', self.metodu_MODE])
                return self.wera_stat()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 qaleb_MODE 중입니다 ({}). 작업이 끝난 Lura_VALUE 다시 실행하세요.'.format(현재))
        elif stat_VALUE is not None and not stat_VALUE.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.isem in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_VALUE/eżegwixxa_kmand 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.kmand(['make', '-C', str(self.għerq_VALUE / 'os'), 'iso']), end='')
        원본 = self.għerq_VALUE / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        destinazzjoni_VALUE = self.mogħdija(매체)
        destinazzjoni_VALUE.parent.mkdir(exist_ok=True)
        if destinazzjoni_VALUE.exists():
            if 검사합(destinazzjoni_VALUE) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(destinazzjoni_VALUE))
        else:
            with tempfile.NamedTemporaryFile(dir=str(destinazzjoni_VALUE.parent)) as fajl:
                shutil.copyfile(str(원본), fajl.name)
                os.link(fajl.name, str(destinazzjoni_VALUE))

        if stat_VALUE is None:
            stat_VALUE = {'version': 1, 'name': self.isem, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_VALUE(stat_VALUE)
        if msinfo32_exe is None:
            self.kmand(['VBoxManage', 'createvm', '--name', stat_VALUE['name'], '--uuid', stat_VALUE['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.mogħdija('machines')), '--register'])
            self.kmand(['VBoxManage', 'setextradata', stat_VALUE['uuid'], 'JKOROS/Owner', stat_VALUE['owner']])
        # bena_sistema 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(stat_VALUE, 등록목록(self.kmand(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('bena_sistema 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(stat_VALUE, msinfo32_exe)
        stat_VALUE['iso'] = 매체
        if 매체 not in stat_VALUE['media']: stat_VALUE['media'].append(매체)
        stat_VALUE['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_VALUE = self.mogħdija(stat_VALUE['serial_log'])
        LOG_VALUE.parent.mkdir(exist_ok=True)
        self.Store_VALUE(stat_VALUE)
        self.kmand(['VBoxManage', 'modifyvm', stat_VALUE['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_VALUE)])
        제어기들 = [VALUE for isem, VALUE in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', isem)]
        if 'JKOROS IDE' not in 제어기들:
            self.kmand(['VBoxManage', 'storagectl', stat_VALUE['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.kmand(['VBoxManage', 'storageattach', stat_VALUE['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(destinazzjoni_VALUE)])
        stat_VALUE['pending'] = False
        self.Store_VALUE(stat_VALUE)
        self.kmand(['VBoxManage', 'startvm', stat_VALUE['uuid'], '--type', self.metodu_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.wera_stat()


def serje():
    analizza_VALUE = argparse.ArgumentParser(description='jkoros 전용 VirtualBox eżegwixxa_kmand 및 stat_VALUE query_VALUE')
    analizza_VALUE.add_argument('action', choices=['run', 'status'])
    인자 = analizza_VALUE.parse_args()
    eżegwixxa_kmand = programm_ġabra_ta_apps(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(eżegwixxa_kmand.wera_stat(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. host 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/permess_VALUE 변경은 하지 않습니다.')
    os.umask(0o077)
    eżegwixxa_kmand.mogħdija('lock').parent.mkdir(parents=True, exist_ok=True)
    with eżegwixxa_kmand.mogħdija('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox eżegwixxa_kmand 작업이 진행 중입니다.')
        print(json.dumps(eżegwixxa_kmand.eżegwixxa_kmand(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: serje()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as żball:
        print('VBOX żball: ' + str(żball), file=sys.stderr)
        sys.exit(1)
