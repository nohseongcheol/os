#!/usr/bin/env python3
"""jkoros 전용 VirtualBox kaupapa_pūwhiri_taupānga. 기존 VM/디스크/Store_uara 상태는 삭제하지 않는다."""
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


def kawe_anga_tono(인수):
    환경 = dict(os.environ, LC_ALL='C')
    mēhua = subprocess.run([str(uara) for uara in 인수], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=환경, timeout=180)
    Ihirangi_uara = mēhua.stdout.decode('utf-8', 'replace')
    if mēhua.returncode:
        raise 실행오류('tono rahunga_uara: ' + ' '.join(str(uara) for uara in 인수) + '\n' + Ihirangi_uara[-10000:])
    return Ihirangi_uara


def huanga_uara(Ihirangi_uara):
    mēhua = {}
    for hononga in Ihirangi_uara.splitlines():
        if '=' not in hononga:
            continue
        Ingoa, uara = hononga.split('=', 1)
        if Ingoa.startswith('"'):
            Ingoa = json.loads(Ingoa)
        if uara.startswith('"'):
            try:
                읽은값, 끝 = json.JSONDecoder().raw_decode(uara)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if 끝 == len(uara): uara = 읽은값
            except ValueError:
                raise 실행오류('VirtualBox huanga_uara hōputu_uara Pōhēhē: ' + hononga)
        mēhua[Ingoa] = uara
    return mēhua


def 등록목록(Ihirangi_uara):
    mēhua = {}
    for hononga in Ihirangi_uara.splitlines():
        일치 = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', hononga)
        if 일치: mēhua[일치.group(2).lower()] = 일치.group(1)
    return mēhua


def 검사합(ara):
    uara = hashlib.sha256()
    with ara.open('rb') as Kōnae:
        for raraunga in iter(lambda: Kōnae.read(1024 * 1024), b''): uara.update(raraunga)
    return uara.hexdigest()


class kaupapa_pūwhiri_taupānga:
    def __init__(self, pūtake_uara, Ingoa, aratuka_MODE='gui', tono=kawe_anga_tono):
        self.pūtake_uara = Path(pūtake_uara).resolve()
        self.Ingoa, self.aratuka_MODE, self.tono = Ingoa, aratuka_MODE, tono
        self.보관 = self.pūtake_uara / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', Ingoa) or Ingoa in ('.', '..'):
            raise 실행오류('VM 이름은 문자·mati_uara·공백·밑줄·괄호·마침표·하이픈만 사용할 수 있습니다.')
        if aratuka_MODE not in ('gui', 'headless'): raise 실행오류('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def ara(self, hoa_uara):
        if Path(hoa_uara).is_absolute() or '..' in Path(hoa_uara).parts:
            raise 실행오류('잘못된 관리 ara: ' + str(hoa_uara))
        mēhua = self.보관
        for 부분 in ['.vbox'] + list(Path(hoa_uara).parts):
            if 부분 == '.vbox': mēhua = self.보관
            else: mēhua = mēhua / 부분
            if mēhua.is_symlink(): raise 실행오류('TŪHONO 경로는 사용하지 않습니다: ' + str(mēhua))
        return mēhua

    def Pānuitia(self):
        ara = self.ara('state.json')
        if not ara.exists(): return None
        tūnga_uara = json.loads(ara.read_text(encoding='utf-8'))
        if tūnga_uara.get('version') != 1 or tūnga_uara.get('name') != self.Ingoa:
            raise 실행오류('관리 상태의 VM Ingoa/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for Ingoa in ('uuid', 'owner'):
            if str(uuid.UUID(tūnga_uara[Ingoa])) != tūnga_uara[Ingoa]: raise 실행오류('잘못된 VM pūtāutu_uara')
        return tūnga_uara

    def Store_uara(self, tūnga_uara):
        ūnga_uara = self.ara('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.보관), delete=False) as Kōnae:
            json.dump(tūnga_uara, Kōnae, ensure_ascii=False, indent=2)
            Kōnae.write('\n')
            임시 = Kōnae.name
        os.replace(임시, str(ūnga_uara))

    def msinfo32_exe(self, tūnga_uara, 등록됨, whakaora_tūnga=False):
        if tūnga_uara['uuid'] not in 등록됨:
            raise 실행오류('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        msinfo32_exe = huanga_uara(self.tono(['VBoxManage', 'showvminfo', tūnga_uara['uuid'], '--machinereadable']))
        tūranga = Path(msinfo32_exe.get('CfgFile', '')).resolve()
        if self.ara('machines').resolve() not in tūranga.parents or msinfo32_exe.get('UUID') != tūnga_uara['uuid']:
            raise 실행오류('이 프로젝트의 VM Ngā_Tautuhinga ara/UUID와 일치하지 않아 변경하지 않습니다.')
        표식 = self.tono(['VBoxManage', 'getextradata', tūnga_uara['uuid'], 'JKOROS/Owner']).strip()
        if 표식 != 'Value: ' + tūnga_uara['owner']:
            if whakaora_tūnga and tūnga_uara.get('pending') and 표식 == 'No value set!':
                self.tono(['VBoxManage', 'setextradata', tūnga_uara['uuid'], 'JKOROS/Owner', tūnga_uara['owner']])
            else:
                raise 실행오류('VM kaipupuri_uara 표식이 일치하지 않아 변경하지 않습니다.')
        return msinfo32_exe

    def taki_pāpāhotanga(self, tūnga_uara, msinfo32_exe):
        제어기들 = [uara for Ingoa, uara in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Ingoa)]
        Tuku_uara = [str(self.ara(uara)) for uara in tūnga_uara.get('media', [])]
        for Ingoa, uara in msinfo32_exe.items():
            if any(re.fullmatch(re.escape(pūmana) + r'-\d+-\d+', Ingoa) for pūmana in 제어기들):
                if uara not in ('none', 'emptydrive') and uara not in Tuku_uara:
                    raise 실행오류('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + uara)

    def whakaatu_tūnga(self):
        tūnga_uara = self.Pānuitia()
        if tūnga_uara is None: return {'name': self.Ingoa, 'state': 'not-created'}
        msinfo32_exe = self.msinfo32_exe(tūnga_uara, 등록목록(self.tono(['VBoxManage', 'list', 'vms'])))
        return {'name': msinfo32_exe.get('name', tūnga_uara['name']), 'uuid': tūnga_uara['uuid'], 'state': msinfo32_exe.get('VMState'),
                'iso': str(self.ara(tūnga_uara['iso'])) if tūnga_uara.get('iso') else None,
                'serial_log': str(self.ara(tūnga_uara['serial_log'])) if tūnga_uara.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def kawe_tono(self):
        tūnga_uara = self.Pānuitia()
        등록됨 = 등록목록(self.tono(['VBoxManage', 'list', 'vms']))
        msinfo32_exe = None
        if tūnga_uara is not None and tūnga_uara['uuid'] in 등록됨:
            msinfo32_exe = self.msinfo32_exe(tūnga_uara, 등록됨, whakaora_tūnga=True)
            현재 = msinfo32_exe.get('VMState')
            if 현재 == 'running':
                print('이미 kawe_tono 중입니다. 재빌드·재시작하지 않습니다.')
                return self.whakaatu_tūnga()
            self.taki_pāpāhotanga(tūnga_uara, msinfo32_exe)
            if 현재 in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 Store_uara 상태를 버리지 않습니다.'.format(현재))
                if 현재 == 'paused':
                    self.tono(['VBoxManage', 'controlvm', tūnga_uara['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 다시 Huaki 전에 기존 기록도 보관한다.
                    if tūnga_uara.get('serial_log'):
                        원본 = self.ara(tūnga_uara['serial_log'])
                        if 원본.is_file():
                            shutil.copyfile(str(원본), str(self.ara('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.tono(['VBoxManage', 'startvm', tūnga_uara['uuid'], '--type', self.aratuka_MODE])
                return self.whakaatu_tūnga()
            if 현재 not in ('poweroff', 'aborted'):
                raise 실행오류('VM이 SWITCH_MODE 중입니다 ({}). 작업이 끝난 Hoki_uara 다시 실행하세요.'.format(현재))
        elif tūnga_uara is not None and not tūnga_uara.get('pending'):
            raise 실행오류('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 다시 등록하세요.')
        elif self.Ingoa in 등록됨.values():
            raise 실행오류('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # Store_uara/kawe_tono 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.tono(['make', '-C', str(self.pūtake_uara / 'os'), 'iso']), end='')
        원본 = self.pūtake_uara / 'os/build/kernel.iso'
        if not 원본.is_file() or 원본.stat().st_size == 0: raise 실행오류('부팅 ISO가 생성되지 않았습니다.')
        pāpāhotanga_uara = 'media/kernel-' + 검사합(원본) + '.iso'
        ūnga_uara = self.ara(pāpāhotanga_uara)
        ūnga_uara.parent.mkdir(exist_ok=True)
        if ūnga_uara.exists():
            if 검사합(ūnga_uara) != 검사합(원본): raise 실행오류('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(ūnga_uara))
        else:
            with tempfile.NamedTemporaryFile(dir=str(ūnga_uara.parent)) as Kōnae:
                shutil.copyfile(str(원본), Kōnae.name)
                os.link(Kōnae.name, str(ūnga_uara))

        if tūnga_uara is None:
            tūnga_uara = {'version': 1, 'name': self.Ingoa, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.Store_uara(tūnga_uara)
        if msinfo32_exe is None:
            self.tono(['VBoxManage', 'createvm', '--name', tūnga_uara['name'], '--uuid', tūnga_uara['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.ara('machines')), '--register'])
            self.tono(['VBoxManage', 'setextradata', tūnga_uara['uuid'], 'JKOROS/Owner', tūnga_uara['owner']])
        # hanga_pūnaha 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        msinfo32_exe = self.msinfo32_exe(tūnga_uara, 등록목록(self.tono(['VBoxManage', 'list', 'vms'])))
        if msinfo32_exe.get('VMState') not in ('poweroff', 'aborted'):
            raise 실행오류('hanga_pūnaha 중 VM 상태가 바뀌었습니다. 다시 make vbox를 실행하세요.')
        self.taki_pāpāhotanga(tūnga_uara, msinfo32_exe)
        tūnga_uara['iso'] = pāpāhotanga_uara
        if pāpāhotanga_uara not in tūnga_uara['media']: tūnga_uara['media'].append(pāpāhotanga_uara)
        tūnga_uara['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        LOG_uara = self.ara(tūnga_uara['serial_log'])
        LOG_uara.parent.mkdir(exist_ok=True)
        self.Store_uara(tūnga_uara)
        self.tono(['VBoxManage', 'modifyvm', tūnga_uara['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(LOG_uara)])
        제어기들 = [uara for Ingoa, uara in msinfo32_exe.items() if re.fullmatch(r'storagecontrollername\d+', Ingoa)]
        if 'JKOROS IDE' not in 제어기들:
            self.tono(['VBoxManage', 'storagectl', tūnga_uara['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.tono(['VBoxManage', 'storageattach', tūnga_uara['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(ūnga_uara)])
        tūnga_uara['pending'] = False
        self.Store_uara(tūnga_uara)
        self.tono(['VBoxManage', 'startvm', tūnga_uara['uuid'], '--type', self.aratuka_MODE])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.whakaatu_tūnga()


def whakahaere():
    poroporo_uara = argparse.ArgumentParser(description='jkoros 전용 VirtualBox kawe_tono 및 tūnga_uara uiui_uara')
    poroporo_uara.add_argument('action', choices=['run', 'status'])
    인자 = poroporo_uara.parse_args()
    kawe_tono = kaupapa_pūwhiri_taupānga(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if 인자.action == 'status':
        print(json.dumps(kawe_tono.whakaatu_tūnga(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise 실행오류('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise 실행오류('/dev/vboxdrv에 접근할 수 없습니다. taurima 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/mana_uru_uara 변경은 하지 않습니다.')
    os.umask(0o077)
    kawe_tono.ara('lock').parent.mkdir(parents=True, exist_ok=True)
    with kawe_tono.ara('lock').open('a') as 잠금:
        try: fcntl.flock(잠금, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise 실행오류('다른 jkoros VirtualBox kawe_tono 작업이 진행 중입니다.')
        print(json.dumps(kawe_tono.kawe_tono(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: whakahaere()
    except (실행오류, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as Pōhēhē:
        print('VBOX Pōhēhē: ' + str(Pōhēhē), file=sys.stderr)
        sys.exit(1)
