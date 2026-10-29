#!/usr/bin/env python3
"""개인 kếtNối 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from cácThiếtLậpTừXa import chuẩnBị
from BảnPhânPhốiCOSL import tênĐích, thưViện

gốcCâyDựÁn = Path(__file__).resolve().parents[1]


def chạy():
    ĐầuRa = gốcCâyDựÁn / 'build/verification/password-length'
    ĐầuRa.mkdir(parents=True, exist_ok=True)
    cácThiếtLậpCáNhân = gốcCâyDựÁn / 'build/remote/access.json'
    cácThiếtLậpNguyênBản = cácThiếtLậpCáNhân.read_bytes()
    giáTrịBáoCáo = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as giáTrịTạm:
            thửKhôngGianLàmViệc = Path(giáTrịTạm)
            đườngDẫnCácThiếtLập = thửKhôngGianLàmViệc / 'build/remote'
            đườngDẫnCácThiếtLập.mkdir(parents=True)
            tệpCácThiếtLập = đườngDẫnCácThiếtLập / 'access.json'
            def ghiCácThiếtLập(DữLiệu):
                tệpCácThiếtLập.write_text(json.dumps(DữLiệu, ensure_ascii=False) + '\n')
                tệpCácThiếtLập.chmod(0o600)
            def xácMinhCácThiếtLập(vỏLệnh, MànHình):
                ghiCácThiếtLập({'user': 'user', 'ssh_password': vỏLệnh, 'vnc_password': MànHình})
                nguyênBản = tệpCácThiếtLập.read_bytes()
                chuẩnBị(thửKhôngGianLàmViệc)
                assert tệpCácThiếtLập.read_bytes() == nguyênBản, 'Settings were rewritten'
                giáTrịĐầu = (đườngDẫnCácThiếtLập / 'hồSơ.h').read_text()
                làBằng = re.search(r'mậtKhẩuMànHình\[\] = \{([^}]+)\}', giáTrịĐầu)
                assert làBằng and len(làBằng.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (đườngDẫnCácThiếtLập / 'hồSơ.h').stat().st_mode & 0o777 == 0o600
            for vỏLệnh, MànHình in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                xácMinhCácThiếtLập(vỏLệnh, MànHình)
            giáTrịBáoCáo['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for đổiGiáTrị, giáTrịMục in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                DữLiệu = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                DữLiệu.update(đổiGiáTrị)
                ghiCácThiếtLập(DữLiệu)
                try:
                    chuẩnBị(thửKhôngGianLàmViệc)
                except SystemExit as lỗi:
                    assert giáTrịMục in str(lỗi), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + giáTrịMục)
            giáTrịBáoCáo['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            cácThiếtLập = json.loads((gốcCâyDựÁn / 'build/remote/libassh-build.json').read_text())['flags']
            côngCụTrìnhBiênDịch = os.environ.get('ARM64_CC', 'clang')
            đầuNối = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            côngCụKhoLưuTrữ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def thựcThiLệnh(cácĐốiSố, bảnGhiNhậtKý):
                subprocess.run(list(map(str, cácĐốiSố)), cwd=str(gốcCâyDựÁn), stdout=bảnGhiNhậtKý,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for tên, vỏLệnh, MànHình in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + tên, flush=True)
                xácMinhCácThiếtLập(vỏLệnh, MànHình)
                kếtQuả = ĐầuRa / tên
                kếtQuả.mkdir(exist_ok=True)
                with (kếtQuả / 'build.log').open('wb') as bảnGhiNhậtKý:
                    cácĐích = []
                    for nguyênBản in sorted((gốcCâyDựÁn / 'giáTrịTừXa').glob('*.c')):
                        giáTrịĐích = thửKhôngGianLàmViệc / (nguyênBản.stem + '.o')
                        thựcThiLệnh([côngCụTrìnhBiênDịch] + cácThiếtLập + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', đườngDẫnCácThiếtLập, '-I', gốcCâyDựÁn / 'giáTrịTừXa', '-I', gốcCâyDựÁn / 'vendor/libassh/src',
                             '-I', gốcCâyDựÁn / 'vendor/bearssl/inc', '-I', gốcCâyDựÁn / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', nguyênBản, '-o', giáTrịĐích], bảnGhiNhậtKý)
                        cácĐích.append(giáTrịĐích)
                    góiGộpTừXa = thửKhôngGianLàmViệc / 'libremote.a'
                    thựcThiLệnh([côngCụKhoLưuTrữ, 'rcs', góiGộpTừXa] + cácĐích, bảnGhiNhậtKý)
                    thựcThiLệnh([đầuNối, '--gc-sections', '-T', gốcCâyDựÁn / 'KhởiĐộng/BốTríLiênKết.ld', '-o', thửKhôngGianLàmViệc / 'kernel.elf'] +
                         [gốcCâyDựÁn / 'build' / (tên + '.o') for tên in tênĐích] + ['--start-group'] +
                         [góiGộpTừXa if đườngDẫn == 'remote/libremote.a' else gốcCâyDựÁn / 'build' / đườngDẫn for đườngDẫn in thưViện] + ['--end-group'], bảnGhiNhậtKý)
                    thựcThiLệnh([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         thửKhôngGianLàmViệc / 'kernel.elf', thửKhôngGianLàmViệc / 'kernel8.img'], bảnGhiNhậtKý)
                with (kếtQuả / 'remote-test.log').open('wb') as bảnGhiNhậtKý:
                    thựcThiLệnh(['python3', gốcCâyDựÁn / 'CôngCụ/ThửKếtNốiTừXa.py', '--kernel', thửKhôngGianLàmViệc / 'kernel8.img',
                         '--access', tệpCácThiếtLập, '--output', kếtQuả], bảnGhiNhậtKý)
                thẩmĐịnh = json.loads((kếtQuả / 'report.json').read_text())
                assert thẩmĐịnh['passed']
                giáTrịBáoCáo['checks'].append(tên + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        giáTrịBáoCáo['passed'] = True
    finally:
        giáTrịBáoCáo['personal_settings_unchanged'] = cácThiếtLậpCáNhân.read_bytes() == cácThiếtLậpNguyênBản
        if not giáTrịBáoCáo['personal_settings_unchanged']:
            giáTrịBáoCáo['passed'] = False
        giáTrịBáoCáo['kernel_sha256'] = hashlib.sha256((gốcCâyDựÁn / 'build/kernel8.img').read_bytes()).hexdigest()
        (ĐầuRa / 'report.json').write_text(json.dumps(giáTrịBáoCáo, ensure_ascii=False, indent=2) + '\n')
    assert giáTrịBáoCáo['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(giáTrịBáoCáo, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    chạy()
