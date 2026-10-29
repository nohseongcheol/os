#!/usr/bin/env python3
"""jkoros 전용 VirtualBox ایپ_ایپ_دراز. 기존 VM/디스크/ذخیرہ_کریں_قدر 상태는 삭제하지 않는다."""
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


def نفاذ_کریں_شیل_حکم(دلائل):
    환경 = dict(os.environ, LC_ALL='C')
    پیمائش = subprocess.run([str(قدر) for قدر in دلائل], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    مشمول_قدر = پیمائش.stdout.decode('utf-8', 'replace')
    if پیمائش.returncode:
        raise 실행오류('حکم ناکامی_قدر: ' + ' '.join(str(قدر) for قدر in دلائل) + '\n' + مشمول_قدر[-10000:])
    return مشمول_قدر


def وصف_قدر(مشمول_قدر):
    پیمائش = {}
    for اندراج_کی_سطر in مشمول_قدر.splitlines():
        if '=' not in اندراج_کی_سطر:
            continue
        نام, قدر = اندراج_کی_سطر.split('=', 1)
        if نام.startswith('"'):
            نام = json.loads(نام)
        if قدر.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(قدر)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(قدر): قدر = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox وصف_قدر وضع_قدر غلطی: ' + اندراج_کی_سطر)
        پیمائش[نام] = قدر
    return پیمائش


def 등록목록(مشمول_قدر):
    پیمائش = {}
    for اندراج_کی_سطر in مشمول_قدر.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', اندراج_کی_سطر)
        if 일치: پیمائش[일치.group(2).lower()] = 일치.group(1)
    return پیمائش


def میزان_کی_جانچ_کرنا(راستہ_2):
    قدر = hashlib.sha256()
    with راستہ_2.open('rb') as فائل_کا_نام:
        for کوائف in iter(lambda: فائل_کا_نام.read(1024 * 1024), b''): قدر.update(کوائف)
    return قدر.hexdigest()


class ایپ_ایپ_دراز:
    def __init__(self, روٹ_قدر, نام, طریقہ_موڈ='gui', حکم=نفاذ_کریں_شیل_حکم):
        self.روٹ_قدر = Path(روٹ_قدر).resolve()
        self.نام, self.طریقہ_موڈ, self.حکم = نام, طریقہ_موڈ, حکم
        self.보관 = self.روٹ_قدر / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', نام) or نام in ('.', '..'):
            raise 실행오류('VM 이름은 문자·عدد_قدر·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if طریقہ_موڈ not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def راستہ_2(self, ساتھی_قدر):
        if Path(ساتھی_قدر).is_absolute() or '..' in Path(ساتھی_قدر).parts:
            raise 실행오류('잘못된 관리 راستہ_2: ' + str(ساتھی_قدر))
        پیمائش = self.보관
        for 부분 in ['.vbox'] + list(Path(ساتھی_قدر).parts):
            if 부분 == '.vbox': پیمائش = self.보관
            else: پیمائش = پیمائش / 부분
            if پیمائش.is_symlink(): raise 실행오류('متصل_ہوں 경로는 사용하지 않습니다: ' + str(پیمائش))
        return پیمائش

    def پڑھیں(self):
        راستہ_2 = self.راستہ_2('state.json')
        if not راستہ_2.exists(): return None
        حالت_قدر = json.loads(راستہ_2.read_text(encoding='utf-8'))
        if حالت_قدر.get('version') != 1 or حالت_قدر.get('name') != self.نام:
            raise 실행오류('관리 상태의 VM نام/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for نام in ('uuid', 'owner'):
            if str(uuid.UUID(حالت_قدر[نام])) != حالت_قدر[نام]: raise 실행오류('잘못된 VM شناخت_کنندہ_قدر')
        return حالت_قدر

    def ذخیرہ_کریں_قدر(self, حالت_قدر):
        منزل_مقصود_قدر = self.راستہ_2('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as فائل_کا_نام:
            json.dump(حالت_قدر, فائل_کا_نام, ensure_ascii=False, indent=2)
            فائل_کا_نام.write('\n')
            임시 = فائل_کا_نام.name
        os.replace(임시, str(منزل_مقصود_قدر))

    def نظام_کی_معلومات(self, حالت_قدر, 등록됨, بحال_کریں_حالت=False):
        if حالت_قدر['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        نظام_کی_معلومات = وصف_قدر(self.حکم(['VBoxManage', 'showvminfo', حالت_قدر['uuid'], '--machinereadable']))
        مقام = Path(نظام_کی_معلومات.get('CfgFile', '')).resolve()
        if self.راستہ_2('machines').resolve() not in مقام.parents or نظام_کی_معلومات.get('UUID') != حالت_قدر['uuid']:
            raise 실행오류('이 프로젝트의 VM ترتیبات راستہ_2/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.حکم(['VBoxManage', 'getextradata', حالت_قدر['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + حالت_قدر['owner']:
            if بحال_کریں_حالت and حالت_قدر.get('pending') and 표식 == 'No value set!':
                self.حکم(['VBoxManage', 'setextradata', حالت_قدر['uuid'], 'JKOROS/Owner', حالت_قدر['owner']])
            else:
                raise 실행오류('VM مالک_قدر 표식이 일치하지 않아 변경하지 않습니다.')
        return نظام_کی_معلومات

    def پڑتال_کریں_میڈیا(self, حالت_قدر, نظام_کی_معلومات):
        제어기들 = [قدر for نام, قدر in نظام_کی_معلومات.items() if re.fullmatch(r'storagecontrollername\d+', نام)]
        اجازت_قدر_688200c4 = [str(self.راستہ_2(قدر)) for قدر in حالت_قدر.get('media', [])]
        for نام, قدر in نظام_کی_معلومات.items():
            if any(re.fullmatch(re.escape(کنٹرولر) + r'-\d+-\d+', نام) for کنٹرولر in 제어기들):
                if قدر not in ('none', 'emptydrive') and قدر not in اجازت_قدر_688200c4:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + قدر)

    def دکھانا_حالت(self):
        حالت_قدر = self.پڑھیں()
        if حالت_قدر is None: return {'name': self.نام, 'state': 'not-created'}
        نظام_کی_معلومات = self.نظام_کی_معلومات(حالت_قدر, 등록목록(self.حکم(['VBoxManage', 'list', 'vms'])))
        return {'name': نظام_کی_معلومات.get('name', حالت_قدر['name']), 'uuid': حالت_قدر['uuid'], 'state': نظام_کی_معلومات.get('VMState'),
                'iso': str(self.راستہ_2(حالت_قدر['iso'])) if حالت_قدر.get('iso') else None,
                'serial_log': str(self.راستہ_2(حالت_قدر['serial_log'])) if حالت_قدر.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def نفاذ_کریں_حکم(self):
        حالت_قدر = self.پڑھیں()
        등록됨 = 등록목록(self.حکم(['VBoxManage', 'list', 'vms']))
        نظام_کی_معلومات = None
        if حالت_قدر is not None and حالت_قدر['uuid'] in 등록됨:
            نظام_کی_معلومات = self.نظام_کی_معلومات(حالت_قدر, 등록됨, بحال_کریں_حالت=True)
            현재 = نظام_کی_معلومات.get('VMState')
            if 현재 == 'running':
                print('이미 نفاذ_کریں_حکم 중입니다. 재빌드·재시작하지 않습니다.')
                return self.دکھانا_حالت()
            self.پڑتال_کریں_میڈیا(حالت_قدر, نظام_کی_معلومات)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 ذخیرہ_کریں_قدر 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.حکم(['VBoxManage', 'controlvm', حالت_قدر['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 کھولیں 전에 기존 기록도 보관한다.
                    if حالت_قدر.get('serial_log'):
                        원본 = self.راستہ_2(حالت_قدر['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.راستہ_2('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.حکم(['VBoxManage', 'startvm', حالت_قدر['uuid'], '--type', self.طریقہ_موڈ])
                return self.دکھانا_حالت()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 سوئچ_موڈ 중입니다 ({}). 작업이 끝난 واپس_قدر 다시 실행하세요.'.format(현재))
        elif حالت_قدر is not None and not حالت_قدر.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.نام in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # ذخیرہ_کریں_قدر/نفاذ_کریں_حکم 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.حکم(['make', '-C', str(self.روٹ_قدر / 'os'), 'iso']), end='')
        원본 = self.روٹ_قدر / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        میڈیا_قدر = 'media/kernel-' + میزان_کی_جانچ_کرنا(원본) + '.iso'
        منزل_مقصود_قدر = self.راستہ_2(میڈیا_قدر)
        منزل_مقصود_قدر.parent.mkdir(exist_ok=True)
        if منزل_مقصود_قدر.exists():
            if میزان_کی_جانچ_کرنا(منزل_مقصود_قدر) != میزان_کی_جانچ_کرنا(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(منزل_مقصود_قدر))
        else:
            with tempfile.NamedTemporaryFile(dir=str(منزل_مقصود_قدر.parent)) as فائل_کا_نام:
                shutil.copyfile(str(원본), فائل_کا_نام.name)
                os.link(فائل_کا_نام.name, str(منزل_مقصود_قدر))

        if حالت_قدر is None:
            حالت_قدر = {'version': 1, 'name': self.نام, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.ذخیرہ_کریں_قدر(حالت_قدر)
        if نظام_کی_معلومات is None:
            self.حکم(['VBoxManage', 'createvm', '--name', حالت_قدر['name'], '--uuid', حالت_قدر['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.راستہ_2('machines')), '--register'])
            self.حکم(['VBoxManage', 'setextradata', حالت_قدر['uuid'], 'JKOROS/Owner', حالت_قدر['owner']])
        # بلڈ_نظام 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        نظام_کی_معلومات = self.نظام_کی_معلومات(حالت_قدر, 등록목록(self.حکم(['VBoxManage', 'list', 'vms'])))
        if نظام_کی_معلومات.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('بلڈ_نظام 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.پڑتال_کریں_میڈیا(حالت_قدر, نظام_کی_معلومات)
        حالت_قدر['iso'] = میڈیا_قدر
        if میڈیا_قدر not in حالت_قدر['media']: حالت_قدر['media'].append(میڈیا_قدر)
        حالت_قدر['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        لاگ_قدر = self.راستہ_2(حالت_قدر['serial_log'])
        لاگ_قدر.parent.mkdir(exist_ok=True)
        self.ذخیرہ_کریں_قدر(حالت_قدر)
        self.حکم(['VBoxManage', 'modifyvm', حالت_قدر['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(لاگ_قدر)])
        제어기들 = [قدر for نام, قدر in نظام_کی_معلومات.items() if re.fullmatch(r'storagecontrollername\d+', نام)]
        if 'JKOROS IDE' not in 제어기들:
            self.حکم(['VBoxManage', 'storagectl', حالت_قدر['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.حکم(['VBoxManage', 'storageattach', حالت_قدر['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(منزل_مقصود_قدر)])
        حالت_قدر['pending'] = False
        self.ذخیرہ_کریں_قدر(حالت_قدر)
        self.حکم(['VBoxManage', 'startvm', حالت_قدر['uuid'], '--type', self.طریقہ_موڈ])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.دکھانا_حالت()


def چلائیں():
    پارس_قدر = argparse.ArgumentParser(description='jkoros 전용 VirtualBox نفاذ_کریں_حکم 및 حالت_قدر طلب_قدر')
    پارس_قدر.add_argument('action', choices=['run', 'status'])
    پیرا_میٹر_دلائل = پارس_قدر.parse_args()
    نفاذ_کریں_حکم = ایپ_ایپ_دراز(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if پیرا_میٹر_دلائل.action == 'status':
        print(json.dumps(نفاذ_کریں_حکم.دکھانا_حالت(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. میزبان 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/اجازت_قدر 변경은 하지 않습니다.')
    os.umask(0o077)
    نفاذ_کریں_حکم.راستہ_2('lock').parent.mkdir(parents=True, exist_ok=True)
    with نفاذ_کریں_حکم.راستہ_2('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox نفاذ_کریں_حکم 작업이 진행 중입니다.')
        print(json.dumps(نفاذ_کریں_حکم.نفاذ_کریں_حکم(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: چلائیں()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as غلطی:
        print('VBOX غلطی: ' + str(غلطی), file=sys.stderr)
        sys.exit(1)
