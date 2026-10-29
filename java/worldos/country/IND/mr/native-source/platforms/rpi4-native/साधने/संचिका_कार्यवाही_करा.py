#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. होस्ट 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from आज्ञा_कार्यवाही_करा import आदेश


def सुरू_करा():
    व्याकरणविश्लेषक = argparse.ArgumentParser(description=__doc__)
    व्याकरणविश्लेषक.add_argument('file', type=Path)
    व्याकरणविश्लेषक.add_argument('arguments', nargs='*')
    व्याकरणविश्लेषक.add_argument('--class-name', help='패키지가 있는 .class의 전체 नाव(예: प्रमाणित.बंडल_चाचणी)')
    व्याकरणविश्लेषक.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 आवाहन ABI वापर_मूल्य')
    व्याकरणविश्लेषक.add_argument('--vnc', help='예: 127.0.0.1:2')
    व्याकरणविश्लेषक.add_argument('--include', action='append', type=Path, default=[], help='शेवटीजोडा_प्रविष्टी class फाइल 또는 class 디렉터리(패키지 नाव राखा_मूल्य)')
    वितर्क_ऍरे = व्याकरणविश्लेषक.parse_args()
    डेटा = वितर्क_ऍरे.file.read_bytes()
    if वितर्क_ऍरे.class_name and वितर्क_ऍरे.file.suffix != '.class': व्याकरणविश्लेषक.error('--class-name은 .class 입력에서 사용합니다.')
    नाव = वितर्क_ऍरे.class_name + '.class' if वितर्क_ऍरे.class_name else वितर्क_ऍरे.file.name
    if len(डेटा) > 16384 or not 1 <= len(नाव.encode('utf-8')) <= 63 or '\n' in नाव or '\r' in नाव:
        व्याकरणविश्लेषक.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    वर्गवारी_मूल्य = '.elf' if डेटा[:4] == b'\x7fELF' else वितर्क_ऍरे.file.suffix
    if वितर्क_ऍरे.linux and वर्गवारी_मूल्य != '.elf': व्याकरणविश्लेषक.error('--linux는 ELF 바이너리에만 사용합니다.')
    if वर्गवारी_मूल्य not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        व्याकरणविश्लेषक.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(वितर्क_ऍरे.arguments) > 7 or any(len(स्ट्रींग_डेटा.encode('utf-8')) > 255 or '\n' in स्ट्रींग_डेटा or '\r' in स्ट्रींग_डेटा for स्ट्रींग_डेटा in वितर्क_ऍरे.arguments):
        व्याकरणविश्लेषक.error('인수는 कमाल_मूल्य 7개, 각각 UTF-8 255바이트 이하입니다.')
    पर्याय_7f769d16 = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if वितर्क_ऍरे.vnc: पर्याय_7f769d16 += ['-vnc', वितर्क_ऍरे.vnc]
    प्रक्रिया = subprocess.Popen(आदेश() + पर्याय_7f769d16, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    निवडक = selectors.DefaultSelector(); निवडक.register(प्रक्रिया.stdout, selectors.EVENT_READ)
    def संदेश_स्वीकारा(खूण, निष्पादन_प्रतीक्षामर्यादा=45):
        प्रदान = bytearray(); शेवट_करा_ऑफसेट = time.monotonic() + निष्पादन_प्रतीक्षामर्यादा
        while खूण not in प्रदान:
            if time.monotonic() > शेवट_करा_ऑफसेट: raise RuntimeError('UART timeout: ' + प्रदान.decode('utf-8', 'replace'))
            for दाबलेले_मूल्य, _ in निवडक.select(0.1):
                तुकडा_मूल्य = दाबलेले_मूल्य.fileobj.read(4096)
                if तुकडा_मूल्य: प्रदान.extend(तुकडा_मूल्य)
            if b'PANIC:' in प्रदान or b'FAIL ' in प्रदान: raise RuntimeError(प्रदान.decode('utf-8', 'replace'))
            if प्रक्रिया.poll() is not None: raise RuntimeError('QEMU exited: ' + प्रदान.decode('utf-8', 'replace'))
        return bytes(प्रदान)
    def पाठवा(ओळ, खूण=b'jkoros-native> '):
        प्रक्रिया.stdin.write(ओळ.encode('utf-8') + b'\n'); प्रक्रिया.stdin.flush()
        return संदेश_स्वीकारा(खूण)
    def आज्ञा_कार्यवाही_करा(ओळ):
        प्रदान = पाठवा(ओळ); sys.stdout.buffer.write(प्रदान); sys.stdout.buffer.flush()
        आहे_समान = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', प्रदान)
        if not आहे_समान: raise RuntimeError('guest did not report exit status')
        return int(आहे_समान.group(1))
    try:
        संदेश_स्वीकारा(b'jkoros-native> ')
        संचिका_यादी = []
        for समाविष्टकरा in वितर्क_ऍरे.include:
            if समाविष्टकरा.is_dir():
                संचिका_यादी += [(str(डेटा_स्थान.relative_to(समाविष्टकरा).with_suffix('')).replace('/', '.') + '.class', डेटा_स्थान.read_bytes()) for डेटा_स्थान in sorted(समाविष्टकरा.rglob('*.class'))]
            else:
                संचिका_यादी.append((समाविष्टकरा.name, समाविष्टकरा.read_bytes()))
        संचिका_यादी = [(आयटम_संख्या, गंतव्यस्थान_डेटा) for आयटम_संख्या, गंतव्यस्थान_डेटा in संचिका_यादी if आयटम_संख्या != नाव] + [(नाव, डेटा)]
        for अपलोड_करा_नाव, अपलोड_करा_डेटा in संचिका_यादी:
            if len(अपलोड_करा_डेटा) > 16384 or len(अपलोड_करा_नाव.encode('utf-8')) > 63 or '\n' in अपलोड_करा_नाव or '\r' in अपलोड_करा_नाव:
                raise ValueError('शेवटीजोडा_प्रविष्टी 파일의 नाव/आकार मर्यादा_मूल्य 초과: ' + अपलोड_करा_नाव)
            पाठवा('load ' + shlex.quote(अपलोड_करा_नाव), b'hex> ')
            for क्रमांक_अनुक्रमणिका in range(0, len(अपलोड_करा_डेटा), 64): पाठवा(अपलोड_करा_डेटा[क्रमांक_अनुक्रमणिका:क्रमांक_अनुक्रमणिका+64].hex(), b'hex> ')
            if b'LOADED' not in पाठवा('.'): raise RuntimeError('upload failed: ' + अपलोड_करा_नाव)
            स्मृतिप्रतिलेखित = पाठवा('hex ' + shlex.quote(अपलोड_करा_नाव))
            आहे_समान = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', स्मृतिप्रतिलेखित, re.S)
            if not आहे_समान or bytes.fromhex(''.join(आहे_समान.group(2).decode().split())) != अपलोड_करा_डेटा: raise RuntimeError('upload verification failed')
        if वर्गवारी_मूल्य == '.java' and आज्ञा_कार्यवाही_करा('javac ' + shlex.quote(नाव)) != 0: return 1
        निष्पादनीय_चित्र = वितर्क_ऍरे.file.stem + '.elf'
        if वर्गवारी_मूल्य == '.c' and आज्ञा_कार्यवाही_करा('cc ' + shlex.quote(नाव) + ' -o ' + shlex.quote(निष्पादनीय_चित्र)) != 0: return 1
        अनुप्रयोग = 'java ' + shlex.quote(वितर्क_ऍरे.class_name or वितर्क_ऍरे.file.stem) if वर्गवारी_मूल्य in ('.java', '.class') else ('python ' if वर्गवारी_मूल्य == '.py' else 'run ') + shlex.quote(नाव)
        if वर्गवारी_मूल्य == '.jar': अनुप्रयोग = 'java -jar ' + shlex.quote(नाव)
        if वर्गवारी_मूल्य == '.c': अनुप्रयोग = 'run ' + shlex.quote(निष्पादनीय_चित्र)
        if वितर्क_ऍरे.linux: अनुप्रयोग = 'run --linux ' + shlex.quote(नाव)
        if वितर्क_ऍरे.arguments: अनुप्रयोग += ' ' + ' '.join(shlex.quote(स्ट्रींग_डेटा) for स्ट्रींग_डेटा in वितर्क_ऍरे.arguments)
        return 0 if आज्ञा_कार्यवाही_करा(अनुप्रयोग) == 0 else 1
    finally:
        if प्रक्रिया.poll() is None:
            प्रक्रिया.terminate()
            try: प्रक्रिया.wait(timeout=5)
            except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait(timeout=5)
        निवडक.close(); प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close()


if __name__ == '__main__':
    raise SystemExit(सुरू_करा())
