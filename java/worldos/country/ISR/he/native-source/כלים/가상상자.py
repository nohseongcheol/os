#!/usr/bin/env python3
"""jkoros 전용 VirtualBox תוכנית_מפעיל. 기존 VM/디스크/מאגר_ערך 상태는 삭제하지 않는다."""
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


def לבצע_מעטפת_פקודה(ארגומנטים):
    סביבה = dict(os.environ, LC_ALL='C')
    תוצאה = subprocess.run([str(ערך) for ערך in ארגומנטים], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=סביבה, timeout=180)
    תוכן_ערך = תוצאה.stdout.decode('utf-8', 'replace')
    if תוצאה.returncode:
        raise 실행오류('פקודה כשל_ערך: ' + ' '.join(str(ערך) for ערך in ארגומנטים) + '\n' + תוכן_ערך[-10000:])
    return תוכן_ערך


def ערך_תכונה(תוכן_ערך):
    תוצאה = {}
    for שורה in תוכן_ערך.splitlines():
        if '=' not in שורה:
            continue
        שם, ערך = שורה.split('=', 1)
        if שם.startswith('"'):
            שם = json.loads(שם)
        if ערך.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(ערך)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(ערך): ערך = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox ערך_תכונה לעצב_ערך שגיאה: ' + שורה)
        תוצאה[שם] = ערך
    return תוצאה


def 등록목록(תוכן_ערך):
    תוצאה = {}
    for שורה in תוכן_ערך.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', שורה)
        if 일치: תוצאה[일치.group(2).lower()] = 일치.group(1)
    return תוצאה


def בדיקת_סיכום(נתיב):
    ערך = hashlib.sha256()
    with נתיב.open('rb') as קובץ:
        for נתונים in iter(lambda: קובץ.read(1024 * 1024), b''): ערך.update(נתונים)
    return ערך.hexdigest()


class תוכנית_מפעיל:
    def __init__(self, בסיס_ערך, שם, פעולת_שירות_מצב='gui', פקודה=לבצע_מעטפת_פקודה):
        self.בסיס_ערך = Path(בסיס_ערך).resolve()
        self.שם, self.פעולת_שירות_מצב, self.פקודה = שם, פעולת_שירות_מצב, פקודה
        self.보관 = self.בסיס_ערך / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', שם) or שם in ('.', '..'):
            raise 실행오류('VM 이름은 문자·ספרה_ערך·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if פעולת_שירות_מצב not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def נתיב(self, עמית_ערך):
        if Path(עמית_ערך).is_absolute() or '..' in Path(עמית_ערך).parts:
            raise 실행오류('잘못된 관리 נתיב: ' + str(עמית_ערך))
        תוצאה = self.보관
        for 부분 in ['.vbox'] + list(Path(עמית_ערך).parts):
            if 부분 == '.vbox': תוצאה = self.보관
            else: תוצאה = תוצאה / 부분
            if תוצאה.is_symlink(): raise 실행오류('חיבור 경로는 사용하지 않습니다: ' + str(תוצאה))
        return תוצאה

    def קרא(self):
        נתיב = self.נתיב('state.json')
        if not נתיב.exists(): return None
        מצב_ערך = json.loads(נתיב.read_text(encoding='utf-8'))
        if מצב_ערך.get('version') != 1 or מצב_ערך.get('name') != self.שם:
            raise 실행오류('관리 상태의 VM שם/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for שם in ('uuid', 'owner'):
            if str(uuid.UUID(מצב_ערך[שם])) != מצב_ערך[שם]: raise 실행오류('잘못된 VM מזהה_ערך')
        return מצב_ערך

    def מאגר_ערך(self, מצב_ערך):
        יעד_ערך = self.נתיב('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as קובץ:
            json.dump(מצב_ערך, קובץ, ensure_ascii=False, indent=2)
            קובץ.write('\n')
            임시 = קובץ.name
        os.replace(임시, str(יעד_ערך))

    def מידע_מערכת(self, מצב_ערך, 등록됨, לשחזר_מצב=False):
        if מצב_ערך['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        מידע_מערכת = ערך_תכונה(self.פקודה(['VBoxManage', 'showvminfo', מצב_ערך['uuid'], '--machinereadable']))
        מיקום = Path(מידע_מערכת.get('CfgFile', '')).resolve()
        if self.נתיב('machines').resolve() not in מיקום.parents or מידע_מערכת.get('UUID') != מצב_ערך['uuid']:
            raise 실행오류('이 프로젝트의 VM הגדרות נתיב/UUID와 일치하지 않아 변경하지 않습니다.')
        סמן_ערך = self.פקודה(['VBoxManage', 'getextradata', מצב_ערך['uuid'], 'JKOROS/Owner']).strip()
        if סמן_ערך != 'Value: ' + מצב_ערך['owner']:
            if לשחזר_מצב and מצב_ערך.get('pending') and סמן_ערך == 'No value set!':
                self.פקודה(['VBoxManage', 'setextradata', מצב_ערך['uuid'], 'JKOROS/Owner', מצב_ערך['owner']])
            else:
                raise 실행오류('VM בעלים_ערך 표식이 일치하지 않아 변경하지 않습니다.')
        return מידע_מערכת

    def שיק_מדיה(self, מצב_ערך, מידע_מערכת):
        제어기들 = [ערך for שם, ערך in מידע_מערכת.items() if re.fullmatch(r'storagecontrollername\d+', שם)]
        אפשר_ערך = [str(self.נתיב(ערך)) for ערך in מצב_ערך.get('media', [])]
        for שם, ערך in מידע_מערכת.items():
            if any(re.fullmatch(re.escape(בקר) + r'-\d+-\d+', שם) for בקר in 제어기들):
                if ערך not in ('none', 'emptydrive') and ערך not in אפשר_ערך:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + ערך)

    def הופעה_מצב(self):
        מצב_ערך = self.קרא()
        if מצב_ערך is None: return {'name': self.שם, 'state': 'not-created'}
        מידע_מערכת = self.מידע_מערכת(מצב_ערך, 등록목록(self.פקודה(['VBoxManage', 'list', 'vms'])))
        return {'name': מידע_מערכת.get('name', מצב_ערך['name']), 'uuid': מצב_ערך['uuid'], 'state': מידע_מערכת.get('VMState'),
                'iso': str(self.נתיב(מצב_ערך['iso'])) if מצב_ערך.get('iso') else None,
                'serial_log': str(self.נתיב(מצב_ערך['serial_log'])) if מצב_ערך.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def לבצע_פקודה(self):
        מצב_ערך = self.קרא()
        등록됨 = 등록목록(self.פקודה(['VBoxManage', 'list', 'vms']))
        מידע_מערכת = None
        if מצב_ערך is not None and מצב_ערך['uuid'] in 등록됨:
            מידע_מערכת = self.מידע_מערכת(מצב_ערך, 등록됨, לשחזר_מצב=True)
            נוכחי_פריט = מידע_מערכת.get('VMState')
            if נוכחי_פריט == 'running':
                print('이미 לבצע_פקודה 중입니다. 재빌드·재시작하지 않습니다.')
                return self.הופעה_מצב()
            self.שיק_מדיה(מצב_ערך, מידע_מערכת)
            if נוכחי_פריט in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 מאגר_ערך 상태를 버리지 않습니다.'.format(נוכחי_פריט))
                if נוכחי_פריט == 'paused':
                    self.פקודה(['VBoxManage', 'controlvm', מצב_ערך['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 נסה_שנית_ערך פתח 전에 기존 기록도 보관한다.
                    if מצב_ערך.get('serial_log'):
                        원본 = self.נתיב(מצב_ערך['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.נתיב('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.פקודה(['VBoxManage', 'startvm', מצב_ערך['uuid'], '--type', self.פעולת_שירות_מצב])
                return self.הופעה_מצב()
            if נוכחי_פריט not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 מתג_מצב 중입니다 ({}). 작업이 끝난 הקודם_ערך נסה_שנית_ערך 실행하세요.'.format(נוכחי_פריט))
        elif מצב_ערך is not None and not מצב_ערך.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 נסה_שנית_ערך 등록하세요.')
        elif self.שם in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # מאגר_ערך/לבצע_פקודה 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.פקודה(['make', '-C', str(self.בסיס_ערך / 'os'), 'iso']), end='')
        원본 = self.בסיס_ערך / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        מדיה_ערך = 'media/kernel-' + בדיקת_סיכום(원본) + '.iso'
        יעד_ערך = self.נתיב(מדיה_ערך)
        יעד_ערך.parent.mkdir(exist_ok=True)
        if יעד_ערך.exists():
            if בדיקת_סיכום(יעד_ערך) != בדיקת_סיכום(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(יעד_ערך))
        else:
            with tempfile.NamedTemporaryFile(dir=str(יעד_ערך.parent)) as קובץ:
                shutil.copyfile(str(원본), קובץ.name)
                os.link(קובץ.name, str(יעד_ערך))

        if מצב_ערך is None:
            מצב_ערך = {'version': 1, 'name': self.שם, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.מאגר_ערך(מצב_ערך)
        if מידע_מערכת is None:
            self.פקודה(['VBoxManage', 'createvm', '--name', מצב_ערך['name'], '--uuid', מצב_ערך['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.נתיב('machines')), '--register'])
            self.פקודה(['VBoxManage', 'setextradata', מצב_ערך['uuid'], 'JKOROS/Owner', מצב_ערך['owner']])
        # בנייה 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        מידע_מערכת = self.מידע_מערכת(מצב_ערך, 등록목록(self.פקודה(['VBoxManage', 'list', 'vms'])))
        if מידע_מערכת.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('בנייה 중 VM 상태가 바뀌었습니다. נסה_שנית_ערך make vbox를 실행하세요.')
        self.שיק_מדיה(מצב_ערך, מידע_מערכת)
        מצב_ערך['iso'] = מדיה_ערך
        if מדיה_ערך not in מצב_ערך['media']: מצב_ערך['media'].append(מדיה_ערך)
        מצב_ערך['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        לרשום_ערך = self.נתיב(מצב_ערך['serial_log'])
        לרשום_ערך.parent.mkdir(exist_ok=True)
        self.מאגר_ערך(מצב_ערך)
        self.פקודה(['VBoxManage', 'modifyvm', מצב_ערך['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(לרשום_ערך)])
        제어기들 = [ערך for שם, ערך in מידע_מערכת.items() if re.fullmatch(r'storagecontrollername\d+', שם)]
        if 'JKOROS IDE' not in 제어기들:
            self.פקודה(['VBoxManage', 'storagectl', מצב_ערך['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.פקודה(['VBoxManage', 'storageattach', מצב_ערך['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(יעד_ערך)])
        מצב_ערך['pending'] = False
        self.מאגר_ערך(מצב_ערך)
        self.פקודה(['VBoxManage', 'startvm', מצב_ערך['uuid'], '--type', self.פעולת_שירות_מצב])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.הופעה_מצב()


def הפעלה():
    ניתוח_מבנה_טקסט_ערך = argparse.ArgumentParser(description='jkoros 전용 VirtualBox לבצע_פקודה 및 מצב_ערך שאילתה_ערך')
    ניתוח_מבנה_טקסט_ערך.add_argument('action', choices=['run', 'status'])
    פרמטר_ארגומנט = ניתוח_מבנה_טקסט_ערך.parse_args()
    לבצע_פקודה = תוכנית_מפעיל(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if פרמטר_ארגומנט.action == 'status':
        print(json.dumps(לבצע_פקודה.הופעה_מצב(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. ארח 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/הרשאה_ערך 변경은 하지 않습니다.')
    os.umask(0o077)
    לבצע_פקודה.נתיב('lock').parent.mkdir(parents=True, exist_ok=True)
    with לבצע_פקודה.נתיב('lock').open('a') as נעל_ערך:
        try: fcntl.flock(נעל_ערך, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox לבצע_פקודה 작업이 진행 중입니다.')
        print(json.dumps(לבצע_פקודה.לבצע_פקודה(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: הפעלה()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as שגיאה:
        print('VBOX שגיאה: ' + str(שגיאה), file=sys.stderr)
        sys.exit(1)
