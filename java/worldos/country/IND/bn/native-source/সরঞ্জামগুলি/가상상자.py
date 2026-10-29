#!/usr/bin/env python3
"""jkoros 전용 VirtualBox অ্যাপ_অ্যাপ_লঞ্চার. 기존 VM/디스크/ভাণ্ডার_মান 상태는 삭제하지 않는다."""
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


def কার্যকর_করুন_শেল_আদেশ(আর্গুমেন্ট_তালিকা):
    환경 = dict(os.environ, LC_ALL='C')
    পরিমাপ = subprocess.run([str(মান) for মান in আর্গুমেন্ট_তালিকা], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    সামগ্রি_মান = পরিমাপ.stdout.decode('utf-8', 'replace')
    if পরিমাপ.returncode:
        raise 실행오류('আদেশ বিফলতা_মান: ' + ' '.join(str(মান) for মান in আর্গুমেন্ট_তালিকা) + '\n' + সামগ্রি_মান[-10000:])
    return সামগ্রি_মান


def গুণ_মান(সামগ্রি_মান):
    পরিমাপ = {}
    for নিবেশের_পঙ্_ক্তি in সামগ্রি_মান.splitlines():
        if '=' not in নিবেশের_পঙ্_ক্তি:
            continue
        নাম, মান = নিবেশের_পঙ্_ক্তি.split('=', 1)
        if নাম.startswith('"'):
            নাম = json.loads(নাম)
        if মান.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(মান)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(মান): মান = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox গুণ_মান বিন্যাস_মান ত্রুটি: ' + নিবেশের_পঙ্_ক্তি)
        পরিমাপ[নাম] = মান
    return পরিমাপ


def 등록목록(সামগ্রি_মান):
    পরিমাপ = {}
    for নিবেশের_পঙ্_ক্তি in সামগ্রি_মান.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', নিবেশের_পঙ্_ক্তি)
        if 일치: পরিমাপ[일치.group(2).lower()] = 일치.group(1)
    return পরিমাপ


def চেকসাম(পথ_2):
    মান = hashlib.sha256()
    with পথ_2.open('rb') as নথির_নাম:
        for ডাটা in iter(lambda: নথির_নাম.read(1024 * 1024), b''): মান.update(ডাটা)
    return মান.hexdigest()


class অ্যাপ_অ্যাপ_লঞ্চার:
    def __init__(self, মূল_মান, নাম, পদ্ধতি_মোড='gui', আদেশ=কার্যকর_করুন_শেল_আদেশ):
        self.মূল_মান = Path(মূল_মান).resolve()
        self.নাম, self.পদ্ধতি_মোড, self.আদেশ = নাম, পদ্ধতি_মোড, আদেশ
        self.보관 = self.মূল_মান / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', নাম) or নাম in ('.', '..'):
            raise 실행오류('VM 이름은 문자·সংখ্যা_মান·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if পদ্ধতি_মোড not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def পথ_2(self, পিয়ার_মান):
        if Path(পিয়ার_মান).is_absolute() or '..' in Path(পিয়ার_মান).parts:
            raise 실행오류('잘못된 관리 পথ_2: ' + str(পিয়ার_মান))
        পরিমাপ = self.보관
        for 부분 in ['.vbox'] + list(Path(পিয়ার_মান).parts):
            if 부분 == '.vbox': পরিমাপ = self.보관
            else: পরিমাপ = পরিমাপ / 부분
            if পরিমাপ.is_symlink(): raise 실행오류('সংযোগ_স্থাপনা 경로는 사용하지 않습니다: ' + str(পরিমাপ))
        return পরিমাপ

    def পড়া(self):
        পথ_2 = self.পথ_2('state.json')
        if not পথ_2.exists(): return None
        অবস্হা_মান = json.loads(পথ_2.read_text(encoding='utf-8'))
        if অবস্হা_মান.get('version') != 1 or অবস্হা_মান.get('name') != self.নাম:
            raise 실행오류('관리 상태의 VM নাম/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for নাম in ('uuid', 'owner'):
            if str(uuid.UUID(অবস্হা_মান[নাম])) != অবস্হা_মান[নাম]: raise 실행오류('잘못된 VM সনাক্তকারী_মান')
        return অবস্হা_মান

    def ভাণ্ডার_মান(self, অবস্হা_মান):
        গন্তব্য_মান = self.পথ_2('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as নথির_নাম:
            json.dump(অবস্হা_মান, নথির_নাম, ensure_ascii=False, indent=2)
            নথির_নাম.write('\n')
            임시 = নথির_নাম.name
        os.replace(임시, str(গন্তব্য_মান))

    def সিসটেম_তথ্য(self, অবস্হা_মান, 등록됨, পুনরুদ্ধার_অবস্হা=False):
        if অবস্হা_মান['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        সিসটেম_তথ্য = গুণ_মান(self.আদেশ(['VBoxManage', 'showvminfo', অবস্হা_মান['uuid'], '--machinereadable']))
        অবস্থান = Path(সিসটেম_তথ্য.get('CfgFile', '')).resolve()
        if self.পথ_2('machines').resolve() not in অবস্থান.parents or সিসটেম_তথ্য.get('UUID') != অবস্হা_মান['uuid']:
            raise 실행오류('이 프로젝트의 VM সেটিংস পথ_2/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.আদেশ(['VBoxManage', 'getextradata', অবস্হা_মান['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + অবস্হা_মান['owner']:
            if পুনরুদ্ধার_অবস্হা and অবস্হা_মান.get('pending') and 표식 == 'No value set!':
                self.আদেশ(['VBoxManage', 'setextradata', অবস্হা_মান['uuid'], 'JKOROS/Owner', অবস্হা_মান['owner']])
            else:
                raise 실행오류('VM মালিক_মান 표식이 일치하지 않아 변경하지 않습니다.')
        return সিসটেম_তথ্য

    def 매체검사(self, অবস্হা_মান, সিসটেম_তথ্য):
        제어기들 = [মান for নাম, মান in সিসটেম_তথ্য.items() if re.fullmatch(r'storagecontrollername\d+', নাম)]
        সম্মতি_মান = [str(self.পথ_2(মান)) for মান in অবস্হা_মান.get('media', [])]
        for নাম, মান in সিসটেম_তথ্য.items():
            if any(re.fullmatch(re.escape(কন্ট্রোলার) + r'-\d+-\d+', নাম) for কন্ট্রোলার in 제어기들):
                if মান not in ('none', 'emptydrive') and মান not in সম্মতি_মান:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + মান)

    def শো_অবস্হা(self):
        অবস্হা_মান = self.পড়া()
        if অবস্হা_মান is None: return {'name': self.নাম, 'state': 'not-created'}
        সিসটেম_তথ্য = self.সিসটেম_তথ্য(অবস্হা_মান, 등록목록(self.আদেশ(['VBoxManage', 'list', 'vms'])))
        return {'name': সিসটেম_তথ্য.get('name', অবস্হা_মান['name']), 'uuid': অবস্হা_মান['uuid'], 'state': সিসটেম_তথ্য.get('VMState'),
                'iso': str(self.পথ_2(অবস্হা_মান['iso'])) if অবস্হা_মান.get('iso') else None,
                'serial_log': str(self.পথ_2(অবস্হা_মান['serial_log'])) if অবস্হা_মান.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def কার্যকর_করুন_আদেশ(self):
        অবস্হা_মান = self.পড়া()
        등록됨 = 등록목록(self.আদেশ(['VBoxManage', 'list', 'vms']))
        সিসটেম_তথ্য = None
        if অবস্হা_মান is not None and অবস্হা_মান['uuid'] in 등록됨:
            সিসটেম_তথ্য = self.সিসটেম_তথ্য(অবস্হা_মান, 등록됨, পুনরুদ্ধার_অবস্হা=True)
            현재 = সিসটেম_তথ্য.get('VMState')
            if 현재 == 'running':
                print('이미 কার্যকর_করুন_আদেশ 중입니다. 재빌드·재시작하지 않습니다.')
                return self.শো_অবস্হা()
            self.매체검사(অবস্হা_মান, সিসটেম_তথ্য)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 ভাণ্ডার_মান 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.আদেশ(['VBoxManage', 'controlvm', অবস্হা_মান['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 খুলুন 전에 기존 기록도 보관한다.
                    if অবস্হা_মান.get('serial_log'):
                        원본 = self.পথ_2(অবস্হা_মান['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.পথ_2('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.আদেশ(['VBoxManage', 'startvm', অবস্হা_মান['uuid'], '--type', self.পদ্ধতি_মোড])
                return self.শো_অবস্হা()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 সুইচ_মোড 중입니다 ({}). 작업이 끝난 ফিরে_যান_মান 다시 실행하세요.'.format(현재))
        elif অবস্হা_মান is not None and not অবস্হা_মান.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.নাম in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # ভাণ্ডার_মান/কার্যকর_করুন_আদেশ 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.আদেশ(['make', '-C', str(self.মূল_মান / 'os'), 'iso']), end='')
        원본 = self.মূল_মান / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + চেকসাম(원본) + '.iso'
        গন্তব্য_মান = self.পথ_2(매체)
        গন্তব্য_মান.parent.mkdir(exist_ok=True)
        if গন্তব্য_মান.exists():
            if চেকসাম(গন্তব্য_মান) != চেকসাম(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(গন্তব্য_মান))
        else:
            with tempfile.NamedTemporaryFile(dir=str(গন্তব্য_মান.parent)) as নথির_নাম:
                shutil.copyfile(str(원본), নথির_নাম.name)
                os.link(নথির_নাম.name, str(গন্তব্য_মান))

        if অবস্হা_মান is None:
            অবস্হা_মান = {'version': 1, 'name': self.নাম, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.ভাণ্ডার_মান(অবস্হা_মান)
        if সিসটেম_তথ্য is None:
            self.আদেশ(['VBoxManage', 'createvm', '--name', অবস্হা_মান['name'], '--uuid', অবস্হা_মান['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.পথ_2('machines')), '--register'])
            self.আদেশ(['VBoxManage', 'setextradata', অবস্হা_মান['uuid'], 'JKOROS/Owner', অবস্হা_মান['owner']])
        # গঠন_সিস্টেম 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        সিসটেম_তথ্য = self.সিসটেম_তথ্য(অবস্হা_মান, 등록목록(self.আদেশ(['VBoxManage', 'list', 'vms'])))
        if সিসটেম_তথ্য.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('গঠন_সিস্টেম 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.매체검사(অবস্হা_মান, সিসটেম_তথ্য)
        অবস্হা_মান['iso'] = 매체
        if 매체 not in অবস্হা_মান['media']: অবস্হা_মান['media'].append(매체)
        অবস্হা_মান['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        লগ_মান = self.পথ_2(অবস্হা_মান['serial_log'])
        লগ_মান.parent.mkdir(exist_ok=True)
        self.ভাণ্ডার_মান(অবস্হা_মান)
        self.আদেশ(['VBoxManage', 'modifyvm', অবস্হা_মান['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(লগ_মান)])
        제어기들 = [মান for নাম, মান in সিসটেম_তথ্য.items() if re.fullmatch(r'storagecontrollername\d+', নাম)]
        if 'JKOROS IDE' not in 제어기들:
            self.আদেশ(['VBoxManage', 'storagectl', অবস্হা_মান['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.আদেশ(['VBoxManage', 'storageattach', অবস্হা_মান['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(গন্তব্য_মান)])
        অবস্হা_মান['pending'] = False
        self.ভাণ্ডার_মান(অবস্হা_মান)
        self.আদেশ(['VBoxManage', 'startvm', অবস্হা_মান['uuid'], '--type', self.পদ্ধতি_মোড])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.শো_অবস্হা()


def চালনা():
    বিভাজন_করা_মান = argparse.ArgumentParser(description='jkoros 전용 VirtualBox কার্যকর_করুন_আদেশ 및 অবস্হা_মান জিজ্ঞাসা_মান')
    বিভাজন_করা_মান.add_argument('action', choices=['run', 'status'])
    প্যারামিটার_যুক্তি = বিভাজন_করা_মান.parse_args()
    কার্যকর_করুন_আদেশ = অ্যাপ_অ্যাপ_লঞ্চার(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if প্যারামিটার_যুক্তি.action == 'status':
        print(json.dumps(কার্যকর_করুন_আদেশ.শো_অবস্হা(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. হোস্ট 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/অনুমতি_মান 변경은 하지 않습니다.')
    os.umask(0o077)
    কার্যকর_করুন_আদেশ.পথ_2('lock').parent.mkdir(parents=True, exist_ok=True)
    with কার্যকর_করুন_আদেশ.পথ_2('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox কার্যকর_করুন_আদেশ 작업이 진행 중입니다.')
        print(json.dumps(কার্যকর_করুন_আদেশ.কার্যকর_করুন_আদেশ(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: চালনা()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as ত্রুটি:
        print('VBOX ত্রুটি: ' + str(ত্রুটি), file=sys.stderr)
        sys.exit(1)
