#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 자체 커널을 다시 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ప్రొజెక్ట్_మూలం = Path(__file__).resolve().parent


def అమలు_చేయి_ఆదేశం(పదం_పాఠం):
    subprocess.check_call([str(ప్రవేశం_మూల్యం) for ప్రవేశం_మూల్యం in పదం_పాఠం], cwd=str(ప్రొజెక్ట్_మూలం))


def నడుపుము():
    పార్సర్_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    పార్సర్_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 సరిచూడు')
    పార్సర్_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    పార్సర్_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    పార్సర్_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = పార్సర్_48ee4b1b.parse_args()
    명세 = json.loads((ప్రొజెక్ట్_మూలం / 'relink.json').read_text())
    బిల్డ్_సిస్టం = ప్రొజెక్ట్_మూలం / 'build'
    새묶음 = బిల్డ్_సిస్టం / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    అనుసంధకం = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ఆర్కైవ్_ఉపకరణం = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    రిమోట్_సెట్టింగ్_లు = json.loads((బిల్డ్_సిస్టం / 'remote/libassh-build.json').read_text())
    అమరికలు = రిమోట్_సెట్టింగ్_లు['flags']
    if 인수.libassh_archive:
        భద్రత_బండిల్ = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', ప్రొజెక్ట్_మూలం / 'రిమోట్_మూల్యం', '-I', ప్రొజెక్ట్_మూలం / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for పేరు in రిమోట్_సెట్టింగ్_లు['sources']:
            గమ్యం_మూల్యం = 새묶음 / (Path(పేరు).stem + '.o')
            అమలు_చేయి_ఆదేశం([번역기] + అమరికలు + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', ప్రొజెక్ట్_మూలం / పేరు, '-o', గమ్యం_మూల్యం])
            목적들.append(గమ్యం_మూల్యం)
        భద్రత_బండిల్ = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            అమలు_చేయి_ఆదేశం([ఆర్కైవ్_ఉపకరణం, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(భద్రత_బండిల్)
    if 인수.tinycc:
        if not 인수.sdk:
            పార్సర్_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            పార్సర్_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [ఎంపిక_మూల్యం for ఎంపిక_మూల్యం in అమరికలు if ఎంపిక_మూల్యం != '-mgeneral-regs-only']
        గమ్యం_మూల్యం = 새묶음 / '번역기.o'
        అమలు_చేయి_ఆదేశం([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', ప్రొజెక్ట్_మూలం / '시언어번역기', '-I', ప్రొజెక్ట్_మూలం / 'vendor/tinycc', '-I', ప్రొజెక్ట్_మూలం / 'వినియోగదారు',
             '-I', బిల్డ్_సిస్టం / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', ప్రొజెక్ట్_మూలం / '시언어번역기/번역기.c', '-o', గమ్యం_మూల్యం])
        అమలు_చేయి_ఆదేశం([అనుసంధకం, '--gc-sections', '-T', ప్రొజెక్ట్_మూలం / 'వినియోగదారు/బంధం_లేవుట్.ld', '-z', 'max-page-size=4096',
             '-o', బిల్డ్_సిస్టం / 'user/cc.elf', బిల్డ్_సిస్టం / 'user/start.o', బిల్డ్_సిస్టం / 'user/runtime.o', గమ్యం_మూల్యం] +
             [బిల్డ్_సిస్టం / 'ccompiler' / (పేరు + '.o') for పేరు in ('సాధారణ_భాష_అమలు_సమయం_మద్దతు', 'నడుపుము', '미리번역', '되돌림')] +
             [బిల్డ్_సిస్టం / 'user' / (పేరు + '.o') for పేరు in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = బిల్డ్_సిస్టం / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((బిల్డ్_సిస్టం / 'user/cc.elf').stat().st_size), 머리.read_text()))
        అమలు_చేయి_ఆదేశం([번역기] + అమరికలు + ['-c', బిల్డ్_సిస్టం / 'programs.S', '-o', ప్రొజెక్ట్_మూలం / 'objects/programs.o'])
        అమలు_చేయి_ఆదేశం([번역기] + అమరికలు + ['-std=c11', '-I', ప్రొజెక్ట్_మూలం / 'posix-kor/arm64-native/포함', '-I', బిల్డ్_సిస్టం,
             '-c', ప్రొజెక్ట్_మూలం / 'యంత్రం/వినియోగదారు.c', '-o', ప్రొజెక్ట్_మూలం / 'objects/user.o'])
    అమలు_చేయి_ఆదేశం([అనుసంధకం, '--gc-sections', '-T', ప్రొజెక్ట్_మూలం / '부팅/బంధం_లేవుట్.ld', '-o', 새묶음 / 'kernel.elf'] +
         [ప్రొజెక్ట్_మూలం / పాత్ for పాత్ in 명세['objects']] + ['--start-group'] +
         [భద్రత_బండిల్ if పాత్ == 'objects/libassh.a' else ప్రొజెక్ట్_మూలం / పాత్ for పాత్ in 명세['libraries']] + ['--end-group'])
    అమలు_చేయి_ఆదేశం([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    హాష్_ఫైలు = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and హాష్_ఫైలు != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + హాష్_ఫైలు)
    print('RELINK PASS', హాష్_ఫైలు, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    నడుపుము()
