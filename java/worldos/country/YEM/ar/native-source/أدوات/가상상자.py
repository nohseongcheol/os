#!/usr/bin/env python3
"""jkoros 전용 VirtualBox تطبيق_مشغّل. 기존 VM/디스크/مخزن_قيمة 상태는 삭제하지 않는다."""
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


def 명령실행(وسائط):
    بيئة_التشغيل = dict(os.environ, LC_ALL='C')
    نتيجة = subprocess.run([str(قيمة) for قيمة in وسائط], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=بيئة_التشغيل, timeout=180)
    محتوى_قيمة = نتيجة.stdout.decode('utf-8', 'replace')
    if نتيجة.returncode:
        raise 실행오류('أمر فشل_قيمة: ' + ' '.join(str(قيمة) for قيمة in وسائط) + '\n' + محتوى_قيمة[-10000:])
    return محتوى_قيمة


def قيمة_السمة(محتوى_قيمة):
    نتيجة = {}
    for سطر in محتوى_قيمة.splitlines():
        if '=' not in سطر:
            continue
        اسم, قيمة = سطر.split('=', 1)
        if اسم.startswith('"'):
            اسم = json.loads(اسم)
        if قيمة.startswith('"'):
            try:
                يقرأ_قيمة, 끝 = json.JSONDecoder().raw_decode(قيمة)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(قيمة): قيمة = يقرأ_قيمة
            except ValueError:
                raise 실행오류('VirtualBox قيمة_السمة ينسق_قيمة خطأ: ' + سطر)
        نتيجة[اسم] = قيمة
    return نتيجة


def 등록목록(محتوى_قيمة):
    نتيجة = {}
    for سطر in محتوى_قيمة.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', سطر)
        if 일치: نتيجة[일치.group(2).lower()] = 일치.group(1)
    return نتيجة


def مجموع_اختباري(مسار):
    قيمة = hashlib.sha256()
    with مسار.open('rb') as ملف:
        for بيانات in iter(lambda: ملف.read(1024 * 1024), b''): قيمة.update(بيانات)
    return قيمة.hexdigest()


class تطبيق_مشغّل:
    def __init__(self, جذر_قيمة, اسم, أسلوب_الوضع='gui', أمر=명령실행):
        self.جذر_قيمة = Path(جذر_قيمة).resolve()
        self.اسم, self.أسلوب_الوضع, self.أمر = اسم, أسلوب_الوضع, أمر
        self.보관 = self.جذر_قيمة / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', اسم) or اسم in ('.', '..'):
            raise 실행오류('VM 이름은 문자·رقم_قيمة·공백·밑줄·괄호·마침표·하이픈만 사용할 رقم 있습니다.')
        if أسلوب_الوضع not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def مسار(self, نظير_قيمة):
        if Path(نظير_قيمة).is_absolute() or '..' in Path(نظير_قيمة).parts:
            raise 실행오류('잘못된 관리 مسار: ' + str(نظير_قيمة))
        نتيجة = self.보관
        for 부분 in ['.vbox'] + list(Path(نظير_قيمة).parts):
            if 부분 == '.vbox': نتيجة = self.보관
            else: نتيجة = نتيجة / 부분
            if نتيجة.is_symlink(): raise 실행오류('اتصال 경로는 사용하지 않습니다: ' + str(نتيجة))
        return نتيجة

    def قراءة(self):
        مسار = self.مسار('state.json')
        if not مسار.exists(): return None
        حالة_قيمة = json.loads(مسار.read_text(encoding='utf-8'))
        if حالة_قيمة.get('version') != 1 or حالة_قيمة.get('name') != self.اسم:
            raise 실행오류('관리 상태의 VM اسم/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for اسم in ('uuid', 'owner'):
            if str(uuid.UUID(حالة_قيمة[اسم])) != حالة_قيمة[اسم]: raise 실행오류('잘못된 VM معرف_قيمة')
        return حالة_قيمة

    def مخزن_قيمة(self, حالة_قيمة):
        وجهة_قيمة = self.مسار('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as ملف:
            json.dump(حالة_قيمة, ملف, ensure_ascii=False, indent=2)
            ملف.write('\n')
            임시 = ملف.name
        os.replace(임시, str(وجهة_قيمة))

    def معلومات_النظام(self, حالة_قيمة, 등록됨, يسترد_حالة=False):
        if حالة_قيمة['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        معلومات_النظام = قيمة_السمة(self.أمر(['VBoxManage', 'showvminfo', حالة_قيمة['uuid'], '--machinereadable']))
        موضع = Path(معلومات_النظام.get('CfgFile', '')).resolve()
        if self.مسار('machines').resolve() not in موضع.parents or معلومات_النظام.get('UUID') != حالة_قيمة['uuid']:
            raise 실행오류('이 프로젝트의 VM إعدادات مسار/UUID와 일치하지 않아 변경하지 않습니다.')
        علامة_قيمة_7e8f90bd = self.أمر(['VBoxManage', 'getextradata', حالة_قيمة['uuid'], 'JKOROS/Owner']).strip()
        if علامة_قيمة_7e8f90bd != 'Value: ' + حالة_قيمة['owner']:
            if يسترد_حالة and حالة_قيمة.get('pending') and علامة_قيمة_7e8f90bd == 'No value set!':
                self.أمر(['VBoxManage', 'setextradata', حالة_قيمة['uuid'], 'JKOROS/Owner', حالة_قيمة['owner']])
            else:
                raise 실행오류('VM مالك_قيمة 표식이 일치하지 않아 변경하지 않습니다.')
        return معلومات_النظام

    def شيك_وسائط(self, حالة_قيمة, معلومات_النظام):
        제어기들 = [قيمة for اسم, قيمة in معلومات_النظام.items() if re.fullmatch(r'storagecontrollername\d+', اسم)]
        يسمح_قيمة = [str(self.مسار(قيمة)) for قيمة in حالة_قيمة.get('media', [])]
        for اسم, قيمة in معلومات_النظام.items():
            if any(re.fullmatch(re.escape(متحكم) + r'-\d+-\d+', اسم) for متحكم in 제어기들):
                if قيمة not in ('none', 'emptydrive') and قيمة not in يسمح_قيمة:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + قيمة)

    def عرض_حالة(self):
        حالة_قيمة = self.قراءة()
        if حالة_قيمة is None: return {'name': self.اسم, 'state': 'not-created'}
        معلومات_النظام = self.معلومات_النظام(حالة_قيمة, 등록목록(self.أمر(['VBoxManage', 'list', 'vms'])))
        return {'name': معلومات_النظام.get('name', حالة_قيمة['name']), 'uuid': حالة_قيمة['uuid'], 'state': معلومات_النظام.get('VMState'),
                'iso': str(self.مسار(حالة_قيمة['iso'])) if حالة_قيمة.get('iso') else None,
                'serial_log': str(self.مسار(حالة_قيمة['serial_log'])) if حالة_قيمة.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def ينفذ_أمر(self):
        حالة_قيمة = self.قراءة()
        등록됨 = 등록목록(self.أمر(['VBoxManage', 'list', 'vms']))
        معلومات_النظام = None
        if حالة_قيمة is not None and حالة_قيمة['uuid'] in 등록됨:
            معلومات_النظام = self.معلومات_النظام(حالة_قيمة, 등록됨, يسترد_حالة=True)
            حديث_عنصر = معلومات_النظام.get('VMState')
            if حديث_عنصر == 'running':
                print('이미 ينفذ_أمر 중입니다. 재빌드·재시작하지 않습니다.')
                return self.عرض_حالة()
            self.شيك_وسائط(حالة_قيمة, معلومات_النظام)
            if حديث_عنصر in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 مخزن_قيمة 상태를 버리지 않습니다.'.format(حديث_عنصر))
                if حديث_عنصر == 'paused':
                    self.أمر(['VBoxManage', 'controlvm', حالة_قيمة['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 إعادة_محاولة_قيمة فتح 전에 기존 기록도 보관한다.
                    if حالة_قيمة.get('serial_log'):
                        원본 = self.مسار(حالة_قيمة['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.مسار('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.أمر(['VBoxManage', 'startvm', حالة_قيمة['uuid'], '--type', self.أسلوب_الوضع])
                return self.عرض_حالة()
            if حديث_عنصر not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 تبديل_الوضع 중입니다 ({}). 작업이 끝난 عودة_قيمة إعادة_محاولة_قيمة 실행하세요.'.format(حديث_عنصر))
        elif حالة_قيمة is not None and not حالة_قيمة.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 إعادة_محاولة_قيمة 등록하세요.')
        elif self.اسم in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # مخزن_قيمة/ينفذ_أمر 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.أمر(['make', '-C', str(self.جذر_قيمة / 'os'), 'iso']), end='')
        원본 = self.جذر_قيمة / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('إقلاع_الآلة ISO가 생성되지 않았습니다.')
        وسائط_قيمة = 'media/kernel-' + مجموع_اختباري(원본) + '.iso'
        وجهة_قيمة = self.مسار(وسائط_قيمة)
        وجهة_قيمة.parent.mkdir(exist_ok=True)
        if وجهة_قيمة.exists():
            if مجموع_اختباري(وجهة_قيمة) != مجموع_اختباري(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(وجهة_قيمة))
        else:
            with tempfile.NamedTemporaryFile(dir=str(وجهة_قيمة.parent)) as ملف:
                shutil.copyfile(str(원본), ملف.name)
                os.link(ملف.name, str(وجهة_قيمة))

        if حالة_قيمة is None:
            حالة_قيمة = {'version': 1, 'name': self.اسم, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.مخزن_قيمة(حالة_قيمة)
        if معلومات_النظام is None:
            self.أمر(['VBoxManage', 'createvm', '--name', حالة_قيمة['name'], '--uuid', حالة_قيمة['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.مسار('machines')), '--register'])
            self.أمر(['VBoxManage', 'setextradata', حالة_قيمة['uuid'], 'JKOROS/Owner', حالة_قيمة['owner']])
        # بنية_نظام 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        معلومات_النظام = self.معلومات_النظام(حالة_قيمة, 등록목록(self.أمر(['VBoxManage', 'list', 'vms'])))
        if معلومات_النظام.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('بنية_نظام 중 VM 상태가 바뀌었습니다. إعادة_محاولة_قيمة make vbox를 실행하세요.')
        self.شيك_وسائط(حالة_قيمة, معلومات_النظام)
        حالة_قيمة['iso'] = وسائط_قيمة
        if وسائط_قيمة not in حالة_قيمة['media']: حالة_قيمة['media'].append(وسائط_قيمة)
        حالة_قيمة['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        سجل_قيمة = self.مسار(حالة_قيمة['serial_log'])
        سجل_قيمة.parent.mkdir(exist_ok=True)
        self.مخزن_قيمة(حالة_قيمة)
        self.أمر(['VBoxManage', 'modifyvm', حالة_قيمة['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(سجل_قيمة)])
        제어기들 = [قيمة for اسم, قيمة in معلومات_النظام.items() if re.fullmatch(r'storagecontrollername\d+', اسم)]
        if 'JKOROS IDE' not in 제어기들:
            self.أمر(['VBoxManage', 'storagectl', حالة_قيمة['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.أمر(['VBoxManage', 'storageattach', حالة_قيمة['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(وجهة_قيمة)])
        حالة_قيمة['pending'] = False
        self.مخزن_قيمة(حالة_قيمة)
        self.أمر(['VBoxManage', 'startvm', حالة_قيمة['uuid'], '--type', self.أسلوب_الوضع])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.عرض_حالة()


def تشغيل():
    يوزّع_قيمة = argparse.ArgumentParser(description='jkoros 전용 VirtualBox ينفذ_أمر 및 حالة_قيمة يستعلم_قيمة')
    يوزّع_قيمة.add_argument('action', choices=['run', 'status'])
    معلمة_وسيطة = يوزّع_قيمة.parse_args()
    ينفذ_أمر = تطبيق_مشغّل(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if معلمة_وسيطة.action == 'status':
        print(json.dumps(ينفذ_أمر.عرض_حالة(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 رقم 없습니다. مضيف 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/إذن_قيمة 변경은 하지 않습니다.')
    os.umask(0o077)
    ينفذ_أمر.مسار('lock').parent.mkdir(parents=True, exist_ok=True)
    with ينفذ_أمر.مسار('lock').open('a') as قفل_قيمة:
        try: fcntl.flock(قفل_قيمة, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox ينفذ_أمر 작업이 진행 중입니다.')
        print(json.dumps(ينفذ_أمر.ينفذ_أمر(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: تشغيل()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as خطأ:
        print('VBOX خطأ: ' + str(خطأ), file=sys.stderr)
        sys.exit(1)
