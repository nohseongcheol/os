#!/usr/bin/env python3
"""jkoros 전용 VirtualBox అనువర్తనం_లాంచర్. 기존 VM/디스크/నిల్వ_మూల్యం 상태는 삭제하지 않는다."""
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


def అమలు_చేయి_షెల్_ఆదేశం(인수):
    환경 = dict(os.environ, LC_ALL='C')
    ప్రమాణం = subprocess.run([str(మూల్యం) for మూల్యం in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    విషయం_మూల్యం = ప్రమాణం.stdout.decode('utf-8', 'replace')
    if ప్రమాణం.returncode:
        raise 실행오류('ఆదేశము వైఫల్యం_మూల్యం: ' + ' '.join(str(మూల్యం) for మూల్యం in 인수) + '\n' + విషయం_మూల్యం[-10000:])
    return విషయం_మూల్యం


def లక్షణం_మూల్యం(విషయం_మూల్యం):
    ప్రమాణం = {}
    for పంక్తి in విషయం_మూల్యం.splitlines():
        if '=' not in పంక్తి:
            continue
        పేరు, మూల్యం = పంక్తి.split('=', 1)
        if పేరు.startswith('"'):
            పేరు = json.loads(పేరు)
        if మూల్యం.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(మూల్యం)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(మూల్యం): మూల్యం = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox లక్షణం_మూల్యం ఆకృతి_మూల్యం దోషం: ' + పంక్తి)
        ప్రమాణం[పేరు] = మూల్యం
    return ప్రమాణం


def 등록목록(విషయం_మూల్యం):
    ప్రమాణం = {}
    for పంక్తి in విషయం_మూల్యం.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', పంక్తి)
        if 일치: ప్రమాణం[일치.group(2).lower()] = 일치.group(1)
    return ప్రమాణం


def 검사합(పాత్):
    మూల్యం = hashlib.sha256()
    with పాత్.open('rb') as దస్త్రం:
        for డేటా in iter(lambda: దస్త్రం.read(1024 * 1024), b''): మూల్యం.update(డేటా)
    return మూల్యం.hexdigest()


class అనువర్తనం_లాంచర్:
    def __init__(self, మూలం_మూల్యం, పేరు, విధానం_మోడ్_3f5e5497='gui', ఆదేశము=అమలు_చేయి_షెల్_ఆదేశం):
        self.మూలం_మూల్యం = Path(మూలం_మూల్యం).resolve()
        self.పేరు, self.విధానం_మోడ్_3f5e5497, self.ఆదేశము = పేరు, విధానం_మోడ్_3f5e5497, ఆదేశము
        self.보관 = self.మూలం_మూల్యం / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', పేరు) or పేరు in ('.', '..'):
            raise 실행오류('VM 이름은 문자·అంకె_మూల్యం·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if విధానం_మోడ్_3f5e5497 not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def పాత్(self, పియర్_మూల్యం):
        if Path(పియర్_మూల్యం).is_absolute() or '..' in Path(పియర్_మూల్యం).parts:
            raise 실행오류('잘못된 관리 పాత్: ' + str(పియర్_మూల్యం))
        ప్రమాణం = self.보관
        for 부분 in ['.vbox'] + list(Path(పియర్_మూల్యం).parts):
            if 부분 == '.vbox': ప్రమాణం = self.보관
            else: ప్రమాణం = ప్రమాణం / 부분
            if ప్రమాణం.is_symlink(): raise 실행오류('కనెక్టుచేయి 경로는 사용하지 않습니다: ' + str(ప్రమాణం))
        return ప్రమాణం

    def చదువు(self):
        పాత్ = self.పాత్('state.json')
        if not పాత్.exists(): return None
        స్థితి_మూల్యం = json.loads(పాత్.read_text(encoding='utf-8'))
        if స్థితి_మూల్యం.get('version') != 1 or స్థితి_మూల్యం.get('name') != self.పేరు:
            raise 실행오류('관리 상태의 VM పేరు/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for పేరు in ('uuid', 'owner'):
            if str(uuid.UUID(స్థితి_మూల్యం[పేరు])) != స్థితి_మూల్యం[పేరు]: raise 실행오류('잘못된 VM ఐడెంటిఫయర్_మూల్యం')
        return స్థితి_మూల్యం

    def నిల్వ_మూల్యం(self, స్థితి_మూల్యం):
        గమ్యం_మూల్యం = self.పాత్('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as దస్త్రం:
            json.dump(స్థితి_మూల్యం, దస్త్రం, ensure_ascii=False, indent=2)
            దస్త్రం.write('\n')
            임시 = దస్త్రం.name
        os.replace(임시, str(గమ్యం_మూల్యం))

    def సిస్టమ్_సమాచారం(self, స్థితి_మూల్యం, 등록됨, పునరుద్ధరణ_స్థితి=False):
        if స్థితి_మూల్యం['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        సిస్టమ్_సమాచారం = లక్షణం_మూల్యం(self.ఆదేశము(['VBoxManage', 'showvminfo', స్థితి_మూల్యం['uuid'], '--machinereadable']))
        స్థానము = Path(సిస్టమ్_సమాచారం.get('CfgFile', '')).resolve()
        if self.పాత్('machines').resolve() not in స్థానము.parents or సిస్టమ్_సమాచారం.get('UUID') != స్థితి_మూల్యం['uuid']:
            raise 실행오류('이 프로젝트의 VM అమరికలు పాత్/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.ఆదేశము(['VBoxManage', 'getextradata', స్థితి_మూల్యం['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + స్థితి_మూల్యం['owner']:
            if పునరుద్ధరణ_స్థితి and స్థితి_మూల్యం.get('pending') and 표식 == 'No value set!':
                self.ఆదేశము(['VBoxManage', 'setextradata', స్థితి_మూల్యం['uuid'], 'JKOROS/Owner', స్థితి_మూల్యం['owner']])
            else:
                raise 실행오류('VM యజమాని_మూల్యం 표식이 일치하지 않아 변경하지 않습니다.')
        return సిస్టమ్_సమాచారం

    def 매체검사(self, స్థితి_మూల్యం, సిస్టమ్_సమాచారం):
        제어기들 = [మూల్యం for పేరు, మూల్యం in సిస్టమ్_సమాచారం.items() if re.fullmatch(r'storagecontrollername\d+', పేరు)]
        అనుమతించు_మూల్యం = [str(self.పాత్(మూల్యం)) for మూల్యం in స్థితి_మూల్యం.get('media', [])]
        for పేరు, మూల్యం in సిస్టమ్_సమాచారం.items():
            if any(re.fullmatch(re.escape(కంట్రోలర్) + r'-\d+-\d+', పేరు) for కంట్రోలర్ in 제어기들):
                if మూల్యం not in ('none', 'emptydrive') and మూల్యం not in అనుమతించు_మూల్యం:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + మూల్యం)

    def చూపించు_స్థితి(self):
        స్థితి_మూల్యం = self.చదువు()
        if స్థితి_మూల్యం is None: return {'name': self.పేరు, 'state': 'not-created'}
        సిస్టమ్_సమాచారం = self.సిస్టమ్_సమాచారం(స్థితి_మూల్యం, 등록목록(self.ఆదేశము(['VBoxManage', 'list', 'vms'])))
        return {'name': సిస్టమ్_సమాచారం.get('name', స్థితి_మూల్యం['name']), 'uuid': స్థితి_మూల్యం['uuid'], 'state': సిస్టమ్_సమాచారం.get('VMState'),
                'iso': str(self.పాత్(స్థితి_మూల్యం['iso'])) if స్థితి_మూల్యం.get('iso') else None,
                'serial_log': str(self.పాత్(స్థితి_మూల్యం['serial_log'])) if స్థితి_మూల్యం.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def అమలు_చేయి_ఆదేశం(self):
        స్థితి_మూల్యం = self.చదువు()
        등록됨 = 등록목록(self.ఆదేశము(['VBoxManage', 'list', 'vms']))
        సిస్టమ్_సమాచారం = None
        if స్థితి_మూల్యం is not None and స్థితి_మూల్యం['uuid'] in 등록됨:
            సిస్టమ్_సమాచారం = self.సిస్టమ్_సమాచారం(స్థితి_మూల్యం, 등록됨, పునరుద్ధరణ_స్థితి=True)
            현재 = సిస్టమ్_సమాచారం.get('VMState')
            if 현재 == 'running':
                print('이미 అమలు_చేయి_ఆదేశం 중입니다. 재빌드·재시작하지 않습니다.')
                return self.చూపించు_స్థితి()
            self.매체검사(స్థితి_మూల్యం, సిస్టమ్_సమాచారం)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 నిల్వ_మూల్యం 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.ఆదేశము(['VBoxManage', 'controlvm', స్థితి_మూల్యం['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 తెరువు 전에 기존 기록도 보관한다.
                    if స్థితి_మూల్యం.get('serial_log'):
                        원본 = self.పాత్(స్థితి_మూల్యం['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.పాత్('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.ఆదేశము(['VBoxManage', 'startvm', స్థితి_మూల్యం['uuid'], '--type', self.విధానం_మోడ్_3f5e5497])
                return self.చూపించు_స్థితి()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 మారు_మోడ్ 중입니다 ({}). 작업이 끝난 వెనుకకు_మూల్యం 다시 실행하세요.'.format(현재))
        elif స్థితి_మూల్యం is not None and not స్థితి_మూల్యం.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.పేరు in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # నిల్వ_మూల్యం/అమలు_చేయి_ఆదేశం 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.ఆదేశము(['make', '-C', str(self.మూలం_మూల్యం / 'os'), 'iso']), end='')
        원본 = self.మూలం_మూల్యం / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        గమ్యం_మూల్యం = self.పాత్(매체)
        గమ్యం_మూల్యం.parent.mkdir(exist_ok=True)
        if గమ్యం_మూల్యం.exists():
            if 검사합(గమ్యం_మూల్యం) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(గమ్యం_మూల్యం))
        else:
            with tempfile.NamedTemporaryFile(dir=str(గమ్యం_మూల్యం.parent)) as దస్త్రం:
                shutil.copyfile(str(원본), దస్త్రం.name)
                os.link(దస్త్రం.name, str(గమ్యం_మూల్యం))

        if స్థితి_మూల్యం is None:
            స్థితి_మూల్యం = {'version': 1, 'name': self.పేరు, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.నిల్వ_మూల్యం(స్థితి_మూల్యం)
        if సిస్టమ్_సమాచారం is None:
            self.ఆదేశము(['VBoxManage', 'createvm', '--name', స్థితి_మూల్యం['name'], '--uuid', స్థితి_మూల్యం['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.పాత్('machines')), '--register'])
            self.ఆదేశము(['VBoxManage', 'setextradata', స్థితి_మూల్యం['uuid'], 'JKOROS/Owner', స్థితి_మూల్యం['owner']])
        # బిల్డ్_సిస్టం 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        సిస్టమ్_సమాచారం = self.సిస్టమ్_సమాచారం(స్థితి_మూల్యం, 등록목록(self.ఆదేశము(['VBoxManage', 'list', 'vms'])))
        if సిస్టమ్_సమాచారం.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('బిల్డ్_సిస్టం 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(స్థితి_మూల్యం, సిస్టమ్_సమాచారం)
        స్థితి_మూల్యం['iso'] = 매체
        if 매체 not in స్థితి_మూల్యం['media']: స్థితి_మూల్యం['media'].append(매체)
        స్థితి_మూల్యం['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        లాగ్_మూల్యం = self.పాత్(స్థితి_మూల్యం['serial_log'])
        లాగ్_మూల్యం.parent.mkdir(exist_ok=True)
        self.నిల్వ_మూల్యం(స్థితి_మూల్యం)
        self.ఆదేశము(['VBoxManage', 'modifyvm', స్థితి_మూల్యం['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(లాగ్_మూల్యం)])
        제어기들 = [మూల్యం for పేరు, మూల్యం in సిస్టమ్_సమాచారం.items() if re.fullmatch(r'storagecontrollername\d+', పేరు)]
        if 'JKOROS IDE' not in 제어기들:
            self.ఆదేశము(['VBoxManage', 'storagectl', స్థితి_మూల్యం['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.ఆదేశము(['VBoxManage', 'storageattach', స్థితి_మూల్యం['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(గమ్యం_మూల్యం)])
        స్థితి_మూల్యం['pending'] = False
        self.నిల్వ_మూల్యం(స్థితి_మూల్యం)
        self.ఆదేశము(['VBoxManage', 'startvm', స్థితి_మూల్యం['uuid'], '--type', self.విధానం_మోడ్_3f5e5497])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.చూపించు_స్థితి()


def నడుపుము():
    పార్స్_మూల్యం = argparse.ArgumentParser(description='jkoros 전용 VirtualBox అమలు_చేయి_ఆదేశం 및 స్థితి_మూల్యం ప్రశ్న_మూల్యం')
    పార్స్_మూల్యం.add_argument('action', choices=['run', 'status'])
    పారామీటర్_కారకం = పార్స్_మూల్యం.parse_args()
    అమలు_చేయి_ఆదేశం = అనువర్తనం_లాంచర్(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if పారామీటర్_కారకం.action == 'status':
        print(json.dumps(అమలు_చేయి_ఆదేశం.చూపించు_స్థితి(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. హోస్ట్ 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/అనుమతి_మూల్యం 변경은 하지 않습니다.')
    os.umask(0o077)
    అమలు_చేయి_ఆదేశం.పాత్('lock').parent.mkdir(parents=True, exist_ok=True)
    with అమలు_చేయి_ఆదేశం.పాత్('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox అమలు_చేయి_ఆదేశం 작업이 진행 중입니다.')
        print(json.dumps(అమలు_చేయి_ఆదేశం.అమలు_చేయి_ఆదేశం(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: నడుపుము()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as దోషం:
        print('VBOX దోషం: ' + str(దోషం), file=sys.stderr)
        sys.exit(1)
