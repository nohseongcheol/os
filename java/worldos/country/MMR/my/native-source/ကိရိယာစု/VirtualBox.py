#!/usr/bin/env python3
"""jkoros 전용 VirtualBox ပရိုဂရမ်စက်နှိုးကိရိယာ. 기존 VM/디스크/သိုလှောင်တန်ဖိုး 상태는 삭제하지 않는다."""
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


class လုပ်ဆောင်မှုအမှား(RuntimeError):
    pass


def အမိန့်ဝင်းအမိန့်လုပ်ဆောင်(အချက်များ):
    ဝန်းကျင် = dict(os.environ, LC_ALL='C')
    ရလဒ် = subprocess.run([str(တန်ဖိုး) for တန်ဖိုး in အချက်များ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=ဝန်းကျင်, timeout=180)
    အကြောင်းအရာတန်ဖိုး = ရလဒ်.stdout.decode('utf-8', 'replace')
    if ရလဒ်.returncode:
        raise လုပ်ဆောင်မှုအမှား('အမိန့် မအောင်မြင်မှု: ' + ' '.join(str(တန်ဖိုး) for တန်ဖိုး in အချက်များ) + '\n' + အကြောင်းအရာတန်ဖိုး[-10000:])
    return အကြောင်းအရာတန်ဖိုး


def ဂုဏ်သတ္တိတန်ဖိုး(အကြောင်းအရာတန်ဖိုး):
    ရလဒ် = {}
    for စာကြောင်း in အကြောင်းအရာတန်ဖိုး.splitlines():
        if '=' not in စာကြောင်း:
            continue
        အမည်, တန်ဖိုး = စာကြောင်း.split('=', 1)
        if အမည်.startswith('"'):
            အမည် = json.loads(အမည်)
        if တန်ဖိုး.startswith('"'):
            try:
                တန်ဖိုးဖတ်, အဆုံး = json.JSONDecoder().raw_decode(တန်ဖိုး)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if အဆုံး == len(တန်ဖိုး): တန်ဖိုး = တန်ဖိုးဖတ်
            except ValueError:
                raise လုပ်ဆောင်မှုအမှား('VirtualBox ဂုဏ်သတ္တိတန်ဖိုး ပုံစံတန်ဖိုး အမှား: ' + စာကြောင်း)
        ရလဒ်[အမည်] = တန်ဖိုး
    return ရလဒ်


def 등록목록(အကြောင်းအရာတန်ဖိုး):
    ရလဒ် = {}
    for စာကြောင်း in အကြောင်းအရာတန်ဖိုး.splitlines():
        ဖြစ်သောညီ = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', စာကြောင်း)
        if ဖြစ်သောညီ: ရလဒ်[ဖြစ်သောညီ.group(2).lower()] = ဖြစ်သောညီ.group(1)
    return ရလဒ်


def စစ်ဆေးပေါင်းလဒ်(လမ်း):
    တန်ဖိုး = hashlib.sha256()
    with လမ်း.open('rb') as ဖိုင်:
        for ဒေတာ in iter(lambda: ဖိုင်.read(1024 * 1024), b''): တန်ဖိုး.update(ဒေတာ)
    return တန်ဖိုး.hexdigest()


class ပရိုဂရမ်စက်နှိုးကိရိယာ:
    def __init__(self, အမြစ်တန်ဖိုး, အမည်, နည်းလမ်းနည်းစနစ်='gui', အမိန့်=အမိန့်ဝင်းအမိန့်လုပ်ဆောင်):
        self.အမြစ်တန်ဖိုး = Path(အမြစ်တန်ဖိုး).resolve()
        self.အမည်, self.နည်းလမ်းနည်းစနစ်, self.အမိန့် = အမည်, နည်းလမ်းနည်းစနစ်, အမိန့်
        self.တန်ဖိုးထိန်းသိမ်း = self.အမြစ်တန်ဖိုး / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', အမည်) or အမည် in ('.', '..'):
            raise လုပ်ဆောင်မှုအမှား('VM 이름은 အက္ခရာ·ဂဏန်းတန်ဖိုး·공백·밑줄·괄호·마침표·하이픈만 사용할 ကိန်းတန်ဖိုး 있습니다.')
        if နည်းလမ်းနည်းစနစ် not in ('gui', 'headless'): raise လုပ်ဆောင်မှုအမှား('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def လမ်း(self, တစ်ဖက်တန်ဖိုး):
        if Path(တစ်ဖက်တန်ဖိုး).is_absolute() or '..' in Path(တစ်ဖက်တန်ဖိုး).parts:
            raise လုပ်ဆောင်မှုအမှား('잘못된 관리 လမ်း: ' + str(တစ်ဖက်တန်ဖိုး))
        ရလဒ် = self.တန်ဖိုးထိန်းသိမ်း
        for အစိတ်အပိုင်းတန်ဖိုး in ['.vbox'] + list(Path(တစ်ဖက်တန်ဖိုး).parts):
            if အစိတ်အပိုင်းတန်ဖိုး == '.vbox': ရလဒ် = self.တန်ဖိုးထိန်းသိမ်း
            else: ရလဒ် = ရလဒ် / အစိတ်အပိုင်းတန်ဖိုး
            if ရလဒ်.is_symlink(): raise လုပ်ဆောင်မှုအမှား('ချိတ်ဆက် 경로는 사용하지 않습니다: ' + str(ရလဒ်))
        return ရလဒ်

    def ဖတ်(self):
        လမ်း = self.လမ်း('state.json')
        if not လမ်း.exists(): return None
        အခြေအနေတန်ဖိုး = json.loads(လမ်း.read_text(encoding='utf-8'))
        if အခြေအနေတန်ဖိုး.get('version') != 1 or အခြေအနေတန်ဖိုး.get('name') != self.အမည်:
            raise လုပ်ဆောင်မှုအမှား('관리 상태의 VM အမည်/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for အမည် in ('uuid', 'owner'):
            if str(uuid.UUID(အခြေအနေတန်ဖိုး[အမည်])) != အခြေအနေတန်ဖိုး[အမည်]: raise လုပ်ဆောင်မှုအမှား('잘못된 VM သတ်မှတ်နံပါတ်တန်ဖိုး')
        return အခြေအနေတန်ဖိုး

    def သိုလှောင်တန်ဖိုး(self, အခြေအနေတန်ဖိုး):
        ဦးတည်ရာတန်ဖိုး = self.လမ်း('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.တန်ဖိုးထိန်းသိမ်း), delete=False) as ဖိုင်:
            json.dump(အခြေအနေတန်ဖိုး, ဖိုင်, ensure_ascii=False, indent=2)
            ဖိုင်.write('\n')
            ယာယီတန်ဖိုး = ဖိုင်.name
        os.replace(ယာယီတန်ဖိုး, str(ဦးတည်ရာတန်ဖိုး))

    def စနစ်သတင်းအချက်အလက်(self, အခြေအနေတန်ဖိုး, 등록됨, အခြေအနေပြန်လည်ရယူ=False):
        if အခြေအနေတန်ဖိုး['uuid'] not in 등록됨:
            raise လုပ်ဆောင်မှုအမှား('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        စနစ်သတင်းအချက်အလက် = ဂုဏ်သတ္တိတန်ဖိုး(self.အမိန့်(['VBoxManage', 'showvminfo', အခြေအနေတန်ဖိုး['uuid'], '--machinereadable']))
        နေရာ = Path(စနစ်သတင်းအချက်အလက်.get('CfgFile', '')).resolve()
        if self.လမ်း('machines').resolve() not in နေရာ.parents or စနစ်သတင်းအချက်အလက်.get('UUID') != အခြေအနေတန်ဖိုး['uuid']:
            raise လုပ်ဆောင်မှုအမှား('이 프로젝트의 VM သတ်မှတ်ချက် လမ်း/UUID와 일치하지 않아 변경하지 않습니다.')
        အမှတ်အသား = self.အမိန့်(['VBoxManage', 'getextradata', အခြေအနေတန်ဖိုး['uuid'], 'JKOROS/Owner']).strip()
        if အမှတ်အသား != 'Value: ' + အခြေအနေတန်ဖိုး['owner']:
            if အခြေအနေပြန်လည်ရယူ and အခြေအနေတန်ဖိုး.get('pending') and အမှတ်အသား == 'No value set!':
                self.အမိန့်(['VBoxManage', 'setextradata', အခြေအနေတန်ဖိုး['uuid'], 'JKOROS/Owner', အခြေအနေတန်ဖိုး['owner']])
            else:
                raise လုပ်ဆောင်မှုအမှား('VM ပိုင်ရှင်တန်ဖိုး 표식이 일치하지 않아 변경하지 않습니다.')
        return စနစ်သတင်းအချက်အလက်

    def 매체검사(self, အခြေအနေတန်ဖိုး, စနစ်သတင်းအချက်အလက်):
        제어기들 = [တန်ဖိုး for အမည်, တန်ဖိုး in စနစ်သတင်းအချက်အလက်.items() if re.fullmatch(r'storagecontrollername\d+', အမည်)]
        တန်ဖိုးခွင့်ပြု = [str(self.လမ်း(တန်ဖိုး)) for တန်ဖိုး in အခြေအနေတန်ဖိုး.get('media', [])]
        for အမည်, တန်ဖိုး in စနစ်သတင်းအချက်အလက်.items():
            if any(re.fullmatch(re.escape(ထိန်းချုပ်သူ) + r'-\d+-\d+', အမည်) for ထိန်းချုပ်သူ in 제어기들):
                if တန်ဖိုး not in ('none', 'emptydrive') and တန်ဖိုး not in တန်ဖိုးခွင့်ပြု:
                    raise လုပ်ဆောင်မှုအမှား('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + တန်ဖိုး)

    def အခြေအနေပြသ(self):
        အခြေအနေတန်ဖိုး = self.ဖတ်()
        if အခြေအနေတန်ဖိုး is None: return {'name': self.အမည်, 'state': 'not-created'}
        စနစ်သတင်းအချက်အလက် = self.စနစ်သတင်းအချက်အလက်(အခြေအနေတန်ဖိုး, 등록목록(self.အမိန့်(['VBoxManage', 'list', 'vms'])))
        return {'name': စနစ်သတင်းအချက်အလက်.get('name', အခြေအနေတန်ဖိုး['name']), 'uuid': အခြေအနေတန်ဖိုး['uuid'], 'state': စနစ်သတင်းအချက်အလက်.get('VMState'),
                'iso': str(self.လမ်း(အခြေအနေတန်ဖိုး['iso'])) if အခြေအနေတန်ဖိုး.get('iso') else None,
                'serial_log': str(self.လမ်း(အခြေအနေတန်ဖိုး['serial_log'])) if အခြေအနေတန်ဖိုး.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def စက်မောင်း(self):
        အခြေအနေတန်ဖိုး = self.ဖတ်()
        등록됨 = 등록목록(self.အမိန့်(['VBoxManage', 'list', 'vms']))
        စနစ်သတင်းအချက်အလက် = None
        if အခြေအနေတန်ဖိုး is not None and အခြေအနေတန်ဖိုး['uuid'] in 등록됨:
            စနစ်သတင်းအချက်အလက် = self.စနစ်သတင်းအချက်အလက်(အခြေအနေတန်ဖိုး, 등록됨, အခြေအနေပြန်လည်ရယူ=True)
            လက်ရှိအချက်အလက်တစ်ခု = စနစ်သတင်းအချက်အလက်.get('VMState')
            if လက်ရှိအချက်အလက်တစ်ခု == 'running':
                print('이미 စက်မောင်း 중입니다. 재빌드·재시작하지 않습니다.')
                return self.အခြေအနေပြသ()
            self.매체검사(အခြေအနေတန်ဖိုး, စနစ်သတင်းအချက်အလက်)
            if လက်ရှိအချက်အလက်တစ်ခု in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 သိုလှောင်တန်ဖိုး 상태를 버리지 않습니다.'.format(လက်ရှိအချက်အလက်တစ်ခု))
                if လက်ရှိအချက်အလက်တစ်ခု == 'paused':
                    self.အမိန့်(['VBoxManage', 'controlvm', အခြေအနေတန်ဖိုး['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 ပြန်ကြိုးစား ဖွင့် 전에 기존 기록도 보관한다.
                    if အခြေအနေတန်ဖိုး.get('serial_log'):
                        မူရင်း = self.လမ်း(အခြေအနေတန်ဖိုး['serial_log'])
                        if မူရင်း.is_file():
                            shutil.copyfile(str(မူရင်း), str(self.လမ်း('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.အမိန့်(['VBoxManage', 'startvm', အခြေအနေတန်ဖိုး['uuid'], '--type', self.နည်းလမ်းနည်းစနစ်])
                return self.အခြေအနေပြသ()
            if လက်ရှိအချက်အလက်တစ်ခု not in ('poweroff', 'aborted'):
                raise လုပ်ဆောင်မှုအမှား('VM이 အလှည့်ပြောင်းနည်းစနစ် 중입니다 ({}). 작업이 끝난 နောက်တန်ဖိုး ပြန်ကြိုးစား 실행하세요.'.format(လက်ရှိအချက်အလက်တစ်ခု))
        elif အခြေအနေတန်ဖိုး is not None and not အခြေအနေတန်ဖိုး.get('pending'):
            raise လုပ်ဆောင်မှုအမှား('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 ပြန်ကြိုးစား 등록하세요.')
        elif self.အမည် in 등록됨.values():
            raise လုပ်ဆောင်မှုအမှား('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # သိုလှောင်တန်ဖိုး/စက်မောင်း 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.အမိန့်(['make', '-C', str(self.အမြစ်တန်ဖိုး / 'os'), 'iso']), end='')
        မူရင်း = self.အမြစ်တန်ဖိုး / 'os/build/kernel.iso'
        if not မူရင်း.is_file() or မူရင်း.stat().st_size == 0: raise လုပ်ဆောင်မှုအမှား('စက်တင် ISO가 생성되지 않았습니다.')
        매체 = 'media/kernel-' + စစ်ဆေးပေါင်းလဒ်(မူရင်း) + '.iso'
        ဦးတည်ရာတန်ဖိုး = self.လမ်း(매체)
        ဦးတည်ရာတန်ဖိုး.parent.mkdir(exist_ok=True)
        if ဦးတည်ရာတန်ဖိုး.exists():
            if စစ်ဆေးပေါင်းလဒ်(ဦးတည်ရာတန်ဖိုး) != စစ်ဆေးပေါင်းလဒ်(မူရင်း): raise လုပ်ဆောင်မှုအမှား('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(ဦးတည်ရာတန်ဖိုး))
        else:
            with tempfile.NamedTemporaryFile(dir=str(ဦးတည်ရာတန်ဖိုး.parent)) as ဖိုင်:
                shutil.copyfile(str(မူရင်း), ဖိုင်.name)
                os.link(ဖိုင်.name, str(ဦးတည်ရာတန်ဖိုး))

        if အခြေအနေတန်ဖိုး is None:
            အခြေအနေတန်ဖိုး = {'version': 1, 'name': self.အမည်, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.သိုလှောင်တန်ဖိုး(အခြေအနေတန်ဖိုး)
        if စနစ်သတင်းအချက်အလက် is None:
            self.အမိန့်(['VBoxManage', 'createvm', '--name', အခြေအနေတန်ဖိုး['name'], '--uuid', အခြေအနေတန်ဖိုး['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.လမ်း('machines')), '--register'])
            self.အမိန့်(['VBoxManage', 'setextradata', အခြေအနေတန်ဖိုး['uuid'], 'JKOROS/Owner', အခြေအနေတန်ဖိုး['owner']])
        # တည်ဆောက် 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        စနစ်သတင်းအချက်အလက် = self.စနစ်သတင်းအချက်အလက်(အခြေအနေတန်ဖိုး, 등록목록(self.အမိန့်(['VBoxManage', 'list', 'vms'])))
        if စနစ်သတင်းအချက်အလက်.get('VMState') not in ('poweroff', 'aborted'):
            raise လုပ်ဆောင်မှုအမှား('တည်ဆောက် 중 VM 상태가 바뀌었습니다. ပြန်ကြိုးစား make vbox를 실행하세요.')
        self.매체검사(အခြေအနေတန်ဖိုး, စနစ်သတင်းအချက်အလက်)
        အခြေအနေတန်ဖိုး['iso'] = 매체
        if 매체 not in အခြေအနေတန်ဖိုး['media']: အခြေအနေတန်ဖိုး['media'].append(매체)
        အခြေအနေတန်ဖိုး['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        မှတ်တမ်းတန်ဖိုး = self.လမ်း(အခြေအနေတန်ဖိုး['serial_log'])
        မှတ်တမ်းတန်ဖိုး.parent.mkdir(exist_ok=True)
        self.သိုလှောင်တန်ဖိုး(အခြေအနေတန်ဖိုး)
        self.အမိန့်(['VBoxManage', 'modifyvm', အခြေအနေတန်ဖိုး['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(မှတ်တမ်းတန်ဖိုး)])
        제어기들 = [တန်ဖိုး for အမည်, တန်ဖိုး in စနစ်သတင်းအချက်အလက်.items() if re.fullmatch(r'storagecontrollername\d+', အမည်)]
        if 'JKOROS IDE' not in 제어기들:
            self.အမိန့်(['VBoxManage', 'storagectl', အခြေအနေတန်ဖိုး['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.အမိန့်(['VBoxManage', 'storageattach', အခြေအနေတန်ဖိုး['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(ဦးတည်ရာတန်ဖိုး)])
        အခြေအနေတန်ဖိုး['pending'] = False
        self.သိုလှောင်တန်ဖိုး(အခြေအနေတန်ဖိုး)
        self.အမိန့်(['VBoxManage', 'startvm', အခြေအနေတန်ဖိုး['uuid'], '--type', self.နည်းလမ်းနည်းစနစ်])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.အခြေအနေပြသ()


def လုပ်ဆောင်():
    တန်ဖိုးသဒ္ဒါခွဲခြမ်း = argparse.ArgumentParser(description='jkoros 전용 VirtualBox စက်မောင်း 및 အခြေအနေတန်ဖိုး 조회')
    တန်ဖိုးသဒ္ဒါခွဲခြမ်း.add_argument('action', choices=['run', 'status'])
    သတ်မှတ်အချက်ပေးအချက် = တန်ဖိုးသဒ္ဒါခွဲခြမ်း.parse_args()
    စက်မောင်း = ပရိုဂရမ်စက်နှိုးကိရိယာ(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if သတ်မှတ်အချက်ပေးအချက်.action == 'status':
        print(json.dumps(စက်မောင်း.အခြေအနေပြသ(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise လုပ်ဆောင်မှုအမှား('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise လုပ်ဆောင်မှုအမှား('/dev/vboxdrv에 접근할 ကိန်းတန်ဖိုး 없습니다. အိမ်ရှင် 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/ခွင့်ပြုချက်တန်ဖိုး 변경은 하지 않습니다.')
    os.umask(0o077)
    စက်မောင်း.လမ်း('lock').parent.mkdir(parents=True, exist_ok=True)
    with စက်မောင်း.လမ်း('lock').open('a') as သော့ခတ်တန်ဖိုး:
        try: fcntl.flock(သော့ခတ်တန်ဖိုး, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise လုပ်ဆောင်မှုအမှား('다른 jkoros VirtualBox စက်မောင်း 작업이 진행 중입니다.')
        print(json.dumps(စက်မောင်း.စက်မောင်း(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: လုပ်ဆောင်()
    except (လုပ်ဆောင်မှုအမှား, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as အမှား:
        print('VBOX အမှား: ' + str(အမှား), file=sys.stderr)
        sys.exit(1)
