#!/usr/bin/env python3
"""jkoros 전용 VirtualBox TrìnhKhởiChạyChươngTrình. 기존 VM/디스크/giáTrịCất 상태는 삭제하지 않는다."""
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


class lỗiViệcThựcThi(RuntimeError):
    pass


def thựcThiLệnhVỏLệnh(cácĐốiSố):
    môiTrường = dict(os.environ, LC_ALL='C')
    kếtQuả = subprocess.run([str(giáTrị) for giáTrị in cácĐốiSố], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=môiTrường, timeout=180)
    giáTrịNộiDung = kếtQuả.stdout.decode('utf-8', 'replace')
    if kếtQuả.returncode:
        raise lỗiViệcThựcThi('lệnh giáTrịSựThấtBại: ' + ' '.join(str(giáTrị) for giáTrị in cácĐốiSố) + '\n' + giáTrịNộiDung[-10000:])
    return giáTrịNộiDung


def giáTrịThuộcTính(giáTrịNộiDung):
    kếtQuả = {}
    for dòng in giáTrịNộiDung.splitlines():
        if '=' not in dòng:
            continue
        tên, giáTrị = dòng.split('=', 1)
        if tên.startswith('"'):
            tên = json.loads(tên)
        if giáTrị.startswith('"'):
            try:
                đọcGiáTrị, phầnKết = json.JSONDecoder().raw_decode(giáTrị)
                # VirtualBox 5.2의 VideoMode="..."@0,0 같은 복합 값은 그대로 둔다.
                if phầnKết == len(giáTrị): giáTrị = đọcGiáTrị
            except ValueError:
                raise lỗiViệcThựcThi('VirtualBox giáTrịThuộcTính giáTrịĐịnhDạng lỗi: ' + dòng)
        kếtQuả[tên] = giáTrị
    return kếtQuả


def cácMụcĐãĐăngKý(giáTrịNộiDung):
    kếtQuả = {}
    for dòng in giáTrịNộiDung.splitlines():
        làBằng = re.fullmatch(r'"(.*)" \{([0-9a-fA-F-]{36})\}', dòng)
        if làBằng: kếtQuả[làBằng.group(2).lower()] = làBằng.group(1)
    return kếtQuả


def tổngKiểm(đườngDẫn):
    giáTrị = hashlib.sha256()
    with đườngDẫn.open('rb') as Tệp:
        for DữLiệu in iter(lambda: Tệp.read(1024 * 1024), b''): giáTrị.update(DữLiệu)
    return giáTrị.hexdigest()


class TrìnhKhởiChạyChươngTrình:
    def __init__(self, giáTrịGốcCây, tên, chếĐộPhươngThức='gui', lệnh=thựcThiLệnhVỏLệnh):
        self.giáTrịGốcCây = Path(giáTrịGốcCây).resolve()
        self.tên, self.chếĐộPhươngThức, self.lệnh = tên, chếĐộPhươngThức, lệnh
        self.giữNguyênGiáTrị = self.giáTrịGốcCây / '.vbox'
        if not re.fullmatch(r'[\w .()-]{1,80}', tên) or tên in ('.', '..'):
            raise lỗiViệcThựcThi('VM 이름은 KýTự·giáTrịChữSố·공백·밑줄·괄호·마침표·하이픈만 사용할 trịSố 있습니다.')
        if chếĐộPhươngThức not in ('gui', 'headless'): raise lỗiViệcThựcThi('VBOX_TYPE은 gui 또는 headless여야 합니다.')

    def đườngDẫn(self, giáTrịĐốiTác):
        if Path(giáTrịĐốiTác).is_absolute() or '..' in Path(giáTrịĐốiTác).parts:
            raise lỗiViệcThựcThi('잘못된 관리 đườngDẫn: ' + str(giáTrịĐốiTác))
        kếtQuả = self.giữNguyênGiáTrị
        for giáTrịPhầnCon in ['.vbox'] + list(Path(giáTrịĐốiTác).parts):
            if giáTrịPhầnCon == '.vbox': kếtQuả = self.giữNguyênGiáTrị
            else: kếtQuả = kếtQuả / giáTrịPhầnCon
            if kếtQuả.is_symlink(): raise lỗiViệcThựcThi('nốiKết 경로는 사용하지 않습니다: ' + str(kếtQuả))
        return kếtQuả

    def đọc(self):
        đườngDẫn = self.đườngDẫn('state.json')
        if not đườngDẫn.exists(): return None
        giáTrịTrạngThái = json.loads(đườngDẫn.read_text(encoding='utf-8'))
        if giáTrịTrạngThái.get('version') != 1 or giáTrịTrạngThái.get('name') != self.tên:
            raise lỗiViệcThựcThi('관리 상태의 VM tên/버전이 다릅니다. 기존 .vbox 자료를 보존하고 원래 VBOX_NAME을 사용하세요.')
        for tên in ('uuid', 'owner'):
            if str(uuid.UUID(giáTrịTrạngThái[tên])) != giáTrịTrạngThái[tên]: raise lỗiViệcThựcThi('잘못된 VM giáTrịĐịnhDanh')
        return giáTrịTrạngThái

    def giáTrịCất(self, giáTrịTrạngThái):
        giáTrịĐích = self.đườngDẫn('state.json')
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=str(self.giữNguyênGiáTrị), delete=False) as Tệp:
            json.dump(giáTrịTrạngThái, Tệp, ensure_ascii=False, indent=2)
            Tệp.write('\n')
            giáTrịTạm = Tệp.name
        os.replace(giáTrịTạm, str(giáTrịĐích))

    def thôngTinHệThống(self, giáTrịTrạngThái, giáTrịĐãĐăngKý, khôiPhụcTrạngThái=False):
        if giáTrịTrạngThái['uuid'] not in giáTrịĐãĐăngKý:
            raise lỗiViệcThựcThi('관리 VM이 등록되어 있지 않습니다. 기존 .vbox/machines 안의 VM 등록을 복구하세요. 새 VM으로 덮어쓰지 않습니다.')
        thôngTinHệThống = giáTrịThuộcTính(self.lệnh(['VBoxManage', 'showvminfo', giáTrịTrạngThái['uuid'], '--machinereadable']))
        vịTrí = Path(thôngTinHệThống.get('CfgFile', '')).resolve()
        if self.đườngDẫn('machines').resolve() not in vịTrí.parents or thôngTinHệThống.get('UUID') != giáTrịTrạngThái['uuid']:
            raise lỗiViệcThựcThi('이 프로젝트의 VM cácThiếtLập đườngDẫn/UUID와 일치하지 않아 변경하지 않습니다.')
        giáTrịDấuMốc = self.lệnh(['VBoxManage', 'getextradata', giáTrịTrạngThái['uuid'], 'JKOROS/Owner']).strip()
        if giáTrịDấuMốc != 'Value: ' + giáTrịTrạngThái['owner']:
            if khôiPhụcTrạngThái and giáTrịTrạngThái.get('pending') and giáTrịDấuMốc == 'No value set!':
                self.lệnh(['VBoxManage', 'setextradata', giáTrịTrạngThái['uuid'], 'JKOROS/Owner', giáTrịTrạngThái['owner']])
            else:
                raise lỗiViệcThựcThi('VM giáTrịChủSởHữu 표식이 일치하지 않아 변경하지 않습니다.')
        return thôngTinHệThống

    def kiểmTraPhươngTiện(self, giáTrịTrạngThái, thôngTinHệThống):
        danhSáchCácBộĐiềuKhiển = [giáTrị for tên, giáTrị in thôngTinHệThống.items() if re.fullmatch(r'storagecontrollername\d+', tên)]
        choPhépGiáTrị = [str(self.đườngDẫn(giáTrị)) for giáTrị in giáTrịTrạngThái.get('media', [])]
        for tên, giáTrị in thôngTinHệThống.items():
            if any(re.fullmatch(re.escape(BộĐiềuKhiển) + r'-\d+-\d+', tên) for BộĐiềuKhiển in danhSáchCácBộĐiềuKhiển):
                if giáTrị not in ('none', 'emptydrive') and giáTrị not in choPhépGiáTrị:
                    raise lỗiViệcThựcThi('사용자가 연결한 다른 매체를 보존합니다. 자동 교체하지 않습니다: ' + giáTrị)

    def hiệnTrạngThái(self):
        giáTrịTrạngThái = self.đọc()
        if giáTrịTrạngThái is None: return {'name': self.tên, 'state': 'not-created'}
        thôngTinHệThống = self.thôngTinHệThống(giáTrịTrạngThái, cácMụcĐãĐăngKý(self.lệnh(['VBoxManage', 'list', 'vms'])))
        return {'name': thôngTinHệThống.get('name', giáTrịTrạngThái['name']), 'uuid': giáTrịTrạngThái['uuid'], 'state': thôngTinHệThống.get('VMState'),
                'iso': str(self.đườngDẫn(giáTrịTrạngThái['iso'])) if giáTrịTrạngThái.get('iso') else None,
                'serial_log': str(self.đườngDẫn(giáTrịTrạngThái['serial_log'])) if giáTrịTrạngThái.get('serial_log') else None,
                'network': 'disabled (RTL8139 is not available in VirtualBox)'}

    def thựcThiLệnh(self):
        giáTrịTrạngThái = self.đọc()
        giáTrịĐãĐăngKý = cácMụcĐãĐăngKý(self.lệnh(['VBoxManage', 'list', 'vms']))
        thôngTinHệThống = None
        if giáTrịTrạngThái is not None and giáTrịTrạngThái['uuid'] in giáTrịĐãĐăngKý:
            thôngTinHệThống = self.thôngTinHệThống(giáTrịTrạngThái, giáTrịĐãĐăngKý, khôiPhụcTrạngThái=True)
            phầnMụcHiệnTại = thôngTinHệThống.get('VMState')
            if phầnMụcHiệnTại == 'running':
                print('이미 thựcThiLệnh 중입니다. 재빌드·재시작하지 않습니다.')
                return self.hiệnTrạngThái()
            self.kiểmTraPhươngTiện(giáTrịTrạngThái, thôngTinHệThống)
            if phầnMụcHiệnTại in ('saved', 'paused'):
                print('기존 {} 상태를 재개합니다. ISO를 재빌드하거나 giáTrịCất 상태를 버리지 않습니다.'.format(phầnMụcHiệnTại))
                if phầnMụcHiệnTại == 'paused':
                    self.lệnh(['VBoxManage', 'controlvm', giáTrịTrạngThái['uuid'], 'resume'])
                else:
                    # VirtualBox가 원래 UART 파일을 giáTrịThửLại mở 전에 기존 기록도 보관한다.
                    if giáTrịTrạngThái.get('serial_log'):
                        nguyênBản = self.đườngDẫn(giáTrịTrạngThái['serial_log'])
                        if nguyênBản.is_file():
                            shutil.copyfile(str(nguyênBản), str(self.đườngDẫn('logs/before-resume-' + str(uuid.uuid4()) + '.log')))
                    self.lệnh(['VBoxManage', 'startvm', giáTrịTrạngThái['uuid'], '--type', self.chếĐộPhươngThức])
                return self.hiệnTrạngThái()
            if phầnMụcHiệnTại not in ('poweroff', 'aborted'):
                raise lỗiViệcThựcThi('VM이 chếĐộChuyển 중입니다 ({}). 작업이 끝난 giáTrịLùi giáTrịThửLại 실행하세요.'.format(phầnMụcHiệnTại))
        elif giáTrịTrạngThái is not None and not giáTrịTrạngThái.get('pending'):
            raise lỗiViệcThựcThi('등록이 해제된 관리 VM을 자동 대체하지 않습니다. .vbox/machines의 VM을 giáTrịThửLại 등록하세요.')
        elif self.tên in giáTrịĐãĐăngKý.values():
            raise lỗiViệcThựcThi('같은 이름의 다른 VM이 있습니다. 변경하지 않습니다. 다른 VBOX_NAME을 지정하세요.')

        # giáTrịCất/thựcThiLệnh 중인 VM에 대해 make iso를 선행하지 않는다.
        print(self.lệnh(['make', '-C', str(self.giáTrịGốcCây / 'os'), 'iso']), end='')
        nguyênBản = self.giáTrịGốcCây / 'os/build/kernel.iso'
        if not nguyênBản.is_file() or nguyênBản.stat().st_size == 0: raise lỗiViệcThựcThi('KhởiĐộng ISO가 생성되지 않았습니다.')
        giáTrịPhươngTiện = 'media/kernel-' + tổngKiểm(nguyênBản) + '.iso'
        giáTrịĐích = self.đườngDẫn(giáTrịPhươngTiện)
        giáTrịĐích.parent.mkdir(exist_ok=True)
        if giáTrịĐích.exists():
            if tổngKiểm(giáTrịĐích) != tổngKiểm(nguyênBản): raise lỗiViệcThựcThi('보존된 ISO가 변경되어 사용하지 않습니다: ' + str(giáTrịĐích))
        else:
            with tempfile.NamedTemporaryFile(dir=str(giáTrịĐích.parent)) as Tệp:
                shutil.copyfile(str(nguyênBản), Tệp.name)
                os.link(Tệp.name, str(giáTrịĐích))

        if giáTrịTrạngThái is None:
            giáTrịTrạngThái = {'version': 1, 'name': self.tên, 'uuid': str(uuid.uuid4()), 'owner': str(uuid.uuid4()), 'pending': True, 'media': []}
            self.giáTrịCất(giáTrịTrạngThái)
        if thôngTinHệThống is None:
            self.lệnh(['VBoxManage', 'createvm', '--name', giáTrịTrạngThái['name'], '--uuid', giáTrịTrạngThái['uuid'],
                      '--ostype', 'Other', '--basefolder', str(self.đườngDẫn('machines')), '--register'])
            self.lệnh(['VBoxManage', 'setextradata', giáTrịTrạngThái['uuid'], 'JKOROS/Owner', giáTrịTrạngThái['owner']])
        # xâyDựngHệThống 도중 GUI에서 VM을 켰다면 하드웨어를 수정하지 않는다.
        thôngTinHệThống = self.thôngTinHệThống(giáTrịTrạngThái, cácMụcĐãĐăngKý(self.lệnh(['VBoxManage', 'list', 'vms'])))
        if thôngTinHệThống.get('VMState') not in ('poweroff', 'aborted'):
            raise lỗiViệcThựcThi('xâyDựngHệThống 중 VM 상태가 바뀌었습니다. giáTrịThửLại make vbox를 실행하세요.')
        self.kiểmTraPhươngTiện(giáTrịTrạngThái, thôngTinHệThống)
        giáTrịTrạngThái['iso'] = giáTrịPhươngTiện
        if giáTrịPhươngTiện not in giáTrịTrạngThái['media']: giáTrịTrạngThái['media'].append(giáTrịPhươngTiện)
        giáTrịTrạngThái['serial_log'] = 'logs/serial-' + str(uuid.uuid4()) + '.log'
        giáTrịNhậtKý = self.đườngDẫn(giáTrịTrạngThái['serial_log'])
        giáTrịNhậtKý.parent.mkdir(exist_ok=True)
        self.giáTrịCất(giáTrịTrạngThái)
        self.lệnh(['VBoxManage', 'modifyvm', giáTrịTrạngThái['uuid'], '--memory', '64', '--cpus', '1', '--vram', '16',
                  '--firmware', 'bios', '--chipset', 'piix3', '--ioapic', 'off',
                  '--boot1', 'dvd', '--boot2', 'none', '--boot3', 'none', '--boot4', 'none', '--nic1', 'none',
                  '--uart1', '0x3F8', '4', '--uartmode1', 'file', str(giáTrịNhậtKý)])
        danhSáchCácBộĐiềuKhiển = [giáTrị for tên, giáTrị in thôngTinHệThống.items() if re.fullmatch(r'storagecontrollername\d+', tên)]
        if 'JKOROS IDE' not in danhSáchCácBộĐiềuKhiển:
            self.lệnh(['VBoxManage', 'storagectl', giáTrịTrạngThái['uuid'], '--name', 'JKOROS IDE', '--add', 'ide', '--controller', 'PIIX4'])
        self.lệnh(['VBoxManage', 'storageattach', giáTrịTrạngThái['uuid'], '--storagectl', 'JKOROS IDE', '--port', '0',
                  '--device', '0', '--type', 'dvddrive', '--medium', str(giáTrịĐích)])
        giáTrịTrạngThái['pending'] = False
        self.giáTrịCất(giáTrịTrạngThái)
        self.lệnh(['VBoxManage', 'startvm', giáTrịTrạngThái['uuid'], '--type', self.chếĐộPhươngThức])
        print('전용 VM을 실행했습니다. 가상 하드디스크는 생성하지 않았습니다.')
        return self.hiệnTrạngThái()


def chạy():
    phânTíchCúPhápGiáTrị = argparse.ArgumentParser(description='jkoros 전용 VirtualBox thựcThiLệnh 및 giáTrịTrạngThái giáTrịTruyVấn')
    phânTíchCúPhápGiáTrị.add_argument('action', choices=['run', 'status'])
    đốiSốThamSố = phânTíchCúPhápGiáTrị.parse_args()
    thựcThiLệnh = TrìnhKhởiChạyChươngTrình(Path(__file__).resolve().parents[1], os.environ.get('VBOX_NAME', 'jkoros operating system'),
                 os.environ.get('VBOX_TYPE', 'gui'))
    if đốiSốThamSố.action == 'status':
        print(json.dumps(thựcThiLệnh.hiệnTrạngThái(), ensure_ascii=False, indent=2))
        return
    if shutil.which('VBoxManage') is None: raise lỗiViệcThựcThi('VBoxManage가 없습니다. VirtualBox 설치를 확인하세요.')
    if sys.platform.startswith('linux') and not Path('/dev/vboxdrv').exists():
        raise lỗiViệcThựcThi('/dev/vboxdrv에 접근할 trịSố 없습니다. Chủ 드라이버 또는 샌드박스 권한을 확인하세요. 자동 재설치/giáTrịQuyền 변경은 하지 않습니다.')
    os.umask(0o077)
    thựcThiLệnh.đườngDẫn('lock').parent.mkdir(parents=True, exist_ok=True)
    with thựcThiLệnh.đườngDẫn('lock').open('a') as giáTrịKhóa:
        try: fcntl.flock(giáTrịKhóa, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise lỗiViệcThựcThi('다른 jkoros VirtualBox thựcThiLệnh 작업이 진행 중입니다.')
        print(json.dumps(thựcThiLệnh.thựcThiLệnh(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try: chạy()
    except (lỗiViệcThựcThi, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as lỗi:
        print('VBOX lỗi: ' + str(lỗi), file=sys.stderr)
        sys.exit(1)
