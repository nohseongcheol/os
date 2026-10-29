#!/usr/bin/env python3
"""jkoros 전용 VirtualBox এপ্প্_এপ্প্_ড্ৰৱাৰ. 기존 VM/디스크/জমা_কৰক_মান 상태는 삭제하지 않는다."""
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


def নিষ্পাদন_শ্বেল_আদেশ(인수):
    환경 = dict(os.environ, LC_ALL='C')
    পৰিমাপ = subprocess.run([str(মান) for মান in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    সামগ্ৰী_মান = পৰিমাপ.stdout.decode('utf-8', 'replace')
    if পৰিমাপ.returncode:
        raise 실행오류('কমান্ড বিফলতা_মান: ' + ' '.join(str(মান) for মান in 인수) + '\n' + সামগ্ৰী_মান[-10000:])
    return সামগ্ৰী_মান


def গুণাগুণ_মান(সামগ্ৰী_মান):
    পৰিমাপ = {}
    for লাইন in সামগ্ৰী_মান.splitlines():
        if '=' not in লাইন:
            continue
        নাম, মান = লাইন.split('=', 1)
        if নাম.startswith('"'):
            নাম = json.loads(নাম)
        if মান.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(মান)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(মান): মান = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox গুণাগুণ_মান সজ্জা_মান ত্ৰুটি: ' + লাইন)
        পৰিমাপ[নাম] = মান
    return পৰিমাপ


def 등록목록(সামগ্ৰী_মান):
    পৰিমাপ = {}
    for লাইন in সামগ্ৰী_মান.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', লাইন)
        if 일치: পৰিমাপ[일치.group(2).lower()] = 일치.group(1)
    return পৰিমাপ


def 검사합(পথ):
    মান = hashlib.sha256()
    with পথ.open('rb') as নথিপত্ৰ:
        for ডাটা in iter(lambda: নথিপত্ৰ.read(1024 * 1024), b''): মান.update(ডাটা)
    return মান.hexdigest()


class এপ্প্_এপ্প্_ড্ৰৱাৰ:
    def __init__(self, ৰুট_মান, নাম, পদ্ধতি_মোড='gui', কমান্ড=নিষ্পাদন_শ্বেল_আদেশ):
        self.ৰুট_মান = Path(ৰুট_মান).resolve()
        self.নাম, self.পদ্ধতি_মোড, self.কমান্ড = নাম, পদ্ধতি_মোড, কমান্ড
        self.보관 = self.ৰুট_মান / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', নাম) or নাম in ('.', '..'):
            raise 실행오류('VM 이름은 문자·অংক_মান·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if পদ্ধতি_মোড not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def পথ(self, পীয়েৰ_মান):
        if Path(পীয়েৰ_মান).is_absolute() or '..' in Path(পীয়েৰ_মান).parts:
            raise 실행오류('잘못된 관리 পথ: ' + str(পীয়েৰ_মান))
        পৰিমাপ = self.보관
        for 부분 in ['.vbox'] + list(Path(পীয়েৰ_মান).parts):
            if 부분 == '.vbox': পৰিমাপ = self.보관
            else: পৰিমাপ = পৰিমাপ / 부분
            if পৰিমাপ.is_symlink(): raise 실행오류('সংযোগ_স্থাপনা 경로는 사용하지 않습니다: ' + str(পৰিমাপ))
        return পৰিমাপ

    def পড়া(self):
        পথ = self.পথ('state.json')
        if not পথ.exists(): return None
        অৱস্থা_মান = json.loads(পথ.read_text(encoding='utf-8'))
        if অৱস্থা_মান.get('version') != 1 or অৱস্থা_মান.get('name') != self.নাম:
            raise 실행오류('관리 상태의 VM নাম/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for নাম in ('uuid', 'owner'):
            if str(uuid.UUID(অৱস্থা_মান[নাম])) != অৱস্থা_মান[নাম]: raise 실행오류('잘못된 VM চিনাক্তকাৰী_মান')
        return অৱস্থা_মান

    def জমা_কৰক_মান(self, অৱস্থা_মান):
        গন্তব্য_স্থান_মান = self.পথ('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as নথিপত্ৰ:
            json.dump(অৱস্থা_মান, নথিপত্ৰ, ensure_ascii=False, indent=2)
            নথিপত্ৰ.write('\n')
            임시 = নথিপত্ৰ.name
        os.replace(임시, str(গন্তব্য_স্থান_মান))

    def ছিষ্টেম_তথ্য(self, অৱস্থা_মান, 등록됨, পুনৰুদ্ধাৰ_কৰক_অৱস্থা=False):
        if অৱস্থা_মান['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        ছিষ্টেম_তথ্য = গুণাগুণ_মান(self.কমান্ড(['VBoxManage', 'showvminfo', অৱস্থা_মান['uuid'], '--machinereadable']))
        অৱস্থান = Path(ছিষ্টেম_তথ্য.get('CfgFile', '')).resolve()
        if self.পথ('machines').resolve() not in অৱস্থান.parents or ছিষ্টেম_তথ্য.get('UUID') != অৱস্থা_মান['uuid']:
            raise 실행오류('이 프로젝트의 VM বৈশিষ্ট্য পথ/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.কমান্ড(['VBoxManage', 'getextradata', অৱস্থা_মান['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + অৱস্থা_মান['owner']:
            if পুনৰুদ্ধাৰ_কৰক_অৱস্থা and অৱস্থা_মান.get('pending') and 표식 == 'No value set!':
                self.কমান্ড(['VBoxManage', 'setextradata', অৱস্থা_মান['uuid'], 'JKOROS/Owner', অৱস্থা_মান['owner']])
            else:
                raise 실행오류('VM গৰাকী_মান 표식이 일치하지 않아 변경하지 않습니다.')
        return ছিষ্টেম_তথ্য

    def 매체검사(self, অৱস্থা_মান, ছিষ্টেম_তথ্য):
        제어기들 = [মান for নাম, মান in ছিষ্টেম_তথ্য.items() if re.fullmatch(r'storagecontrollername\d+', নাম)]
        অনুমতি_দিয়ক_মান = [str(self.পথ(মান)) for মান in অৱস্থা_মান.get('media', [])]
        for নাম, মান in ছিষ্টেম_তথ্য.items():
            if any(re.fullmatch(re.escape(নিয়ন্ত্ৰক) + r'-\d+-\d+', নাম) for নিয়ন্ত্ৰক in 제어기들):
                if মান not in ('none', 'emptydrive') and মান not in অনুমতি_দিয়ক_মান:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + মান)

    def শ্ব_অৱস্থা(self):
        অৱস্থা_মান = self.পড়া()
        if অৱস্থা_মান is None: return {'name': self.নাম, 'state': 'not-created'}
        ছিষ্টেম_তথ্য = self.ছিষ্টেম_তথ্য(অৱস্থা_মান, 등록목록(self.কমান্ড(['VBoxManage', 'list', 'vms'])))
        return {'name': ছিষ্টেম_তথ্য.get('name', অৱস্থা_মান['name']), 'uuid': অৱস্থা_মান['uuid'], 'state': ছিষ্টেম_তথ্য.get('VMState'),
                'iso': str(self.পথ(অৱস্থা_মান['iso'])) if অৱস্থা_মান.get('iso') else None,
                'serial_log': str(self.পথ(অৱস্থা_মান['serial_log'])) if অৱস্থা_মান.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def নিষ্পাদন_আদেশ(self):
        অৱস্থা_মান = self.পড়া()
        등록됨 = 등록목록(self.কমান্ড(['VBoxManage', 'list', 'vms']))
        ছিষ্টেম_তথ্য = None
        if অৱস্থা_মান is not None and অৱস্থা_মান['uuid'] in 등록됨:
            ছিষ্টেম_তথ্য = self.ছিষ্টেম_তথ্য(অৱস্থা_মান, 등록됨, পুনৰুদ্ধাৰ_কৰক_অৱস্থা=True)
            현재 = ছিষ্টেম_তথ্য.get('VMState')
            if 현재 == 'running':
                print('이미 নিষ্পাদন_আদেশ 중입니다. 재빌드·재시작하지 않습니다.')
                return self.শ্ব_অৱস্থা()
            self.매체검사(অৱস্থা_মান, ছিষ্টেম_তথ্য)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 জমা_কৰক_মান 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.কমান্ড(['VBoxManage', 'controlvm', অৱস্থা_মান['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 খোলো 전에 기존 기록도 보관한다.
                    if অৱস্থা_মান.get('serial_log'):
                        원본 = self.পথ(অৱস্থা_মান['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.পথ('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.কমান্ড(['VBoxManage', 'startvm', অৱস্থা_মান['uuid'], '--type', self.পদ্ধতি_মোড])
                return self.শ্ব_অৱস্থা()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 সাল_সলনি_মোড 중입니다 ({}). 작업이 끝난 পাছলৈ_মান 다시 실행하세요.'.format(현재))
        elif অৱস্থা_মান is not None and not অৱস্থা_মান.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.নাম in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # জমা_কৰক_মান/নিষ্পাদন_আদেশ 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.কমান্ড(['make', '-C', str(self.ৰুট_মান / 'os'), 'iso']), end='')
        원본 = self.ৰুট_মান / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + 검사합(원본) + '.iso'
        গন্তব্য_স্থান_মান = self.পথ(매체)
        গন্তব্য_স্থান_মান.parent.mkdir(exist_ok=True)
        if গন্তব্য_স্থান_মান.exists():
            if 검사합(গন্তব্য_স্থান_মান) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(গন্তব্য_স্থান_মান))
        else:
            with tempfile.NamedTemporaryFile(dir=str(গন্তব্য_স্থান_মান.parent)) as নথিপত্ৰ:
                shutil.copyfile(str(원본), নথিপত্ৰ.name)
                os.link(নথিপত্ৰ.name, str(গন্তব্য_স্থান_মান))

        if অৱস্থা_মান is None:
            অৱস্থা_মান = {'version': 1, 'name': self.নাম, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.জমা_কৰক_মান(অৱস্থা_মান)
        if ছিষ্টেম_তথ্য is None:
            self.কমান্ড(['VBoxManage', 'createvm', '--name', অৱস্থা_মান['name'], '--uuid', অৱস্থা_মান['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.পথ('machines')), '--register'])
            self.কমান্ড(['VBoxManage', 'setextradata', অৱস্থা_মান['uuid'], 'JKOROS/Owner', অৱস্থা_মান['owner']])
        # বিল্ড_ছিষ্টেম 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        ছিষ্টেম_তথ্য = self.ছিষ্টেম_তথ্য(অৱস্থা_মান, 등록목록(self.কমান্ড(['VBoxManage', 'list', 'vms'])))
        if ছিষ্টেম_তথ্য.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('বিল্ড_ছিষ্টেম 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(অৱস্থা_মান, ছিষ্টেম_তথ্য)
        অৱস্থা_মান['iso'] = 매체
        if 매체 not in অৱস্থা_মান['media']: অৱস্থা_মান['media'].append(매체)
        অৱস্থা_মান['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        লগ_মান = self.পথ(অৱস্থা_মান['serial_log'])
        লগ_মান.parent.mkdir(exist_ok=True)
        self.জমা_কৰক_মান(অৱস্থা_মান)
        self.কমান্ড(['VBoxManage', 'modifyvm', অৱস্থা_মান['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(লগ_মান)])
        제어기들 = [মান for নাম, মান in ছিষ্টেম_তথ্য.items() if re.fullmatch(r'storagecontrollername\d+', নাম)]
        if 'JKOROS IDE' not in 제어기들:
            self.কমান্ড(['VBoxManage', 'storagectl', অৱস্থা_মান['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.কমান্ড(['VBoxManage', 'storageattach', অৱস্থা_মান['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(গন্তব্য_স্থান_মান)])
        অৱস্থা_মান['pending'] = False
        self.জমা_কৰক_মান(অৱস্থা_মান)
        self.কমান্ড(['VBoxManage', 'startvm', অৱস্থা_মান['uuid'], '--type', self.পদ্ধতি_মোড])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.শ্ব_অৱস্থা()


def সঞ্চালন():
    পাৰ্ছ_কৰক_মান = argparse.ArgumentParser(description='jkoros 전용 VirtualBox নিষ্পাদন_আদেশ 및 অৱস্থা_মান কুৱেৰী_মান')
    পাৰ্ছ_কৰক_মান.add_argument('action', choices=['run', 'status'])
    인자 = পাৰ্ছ_কৰক_মান.parse_args()
    নিষ্পাদন_আদেশ = এপ্প্_এপ্প্_ড্ৰৱাৰ(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(নিষ্পাদন_আদেশ.শ্ব_অৱস্থা(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. হ_ষ্ট 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/অনুমতি_মান 변경은 하지 않습니다.')
    os.umask(0o077)
    নিষ্পাদন_আদেশ.পথ('lock').parent.mkdir(parents=True, exist_ok=True)
    with নিষ্পাদন_আদেশ.পথ('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox নিষ্পাদন_আদেশ 작업이 진행 중입니다.')
        print(json.dumps(নিষ্পাদন_আদেশ.নিষ্পাদন_আদেশ(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: সঞ্চালন()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ত্ৰুটি:
        print('VBOX ত্ৰুটি: ' + str(ত্ৰুটি), file=sys.stderr)
        sys.exit(1)
