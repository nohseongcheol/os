#!/usr/bin/env python3
"""Type Korean through real VNC/XIM into Swing and xterm, then verify UTF-8."""
import argparse
import base64
import json
from pathlib import Path
import re
import struct
import subprocess
import time

from build import data_image
from prepare import ROOT, digest
from run_qemu import command
from test_desktop import VNC


def key(client, code, down):
    client.sock.sendall(struct.pack('!BBHI', 4, int(down), 0, code))
    time.sleep(.07)


def press(client, code):
    key(client, code, True); key(client, code, False)


def toggle(client):
    key(client, 0xffe3, True)  # Control_L
    press(client, ord(' '))
    key(client, 0xffe3, False)
    time.sleep(.4)


def type_hangul(client, x, y):
    for mask in [0, 1, 0]:
        client.sock.sendall(struct.pack('!BBHH', 5, mask, x, y))
        time.sleep(.2)
    toggle(client)
    for char in 'gksrmf dlqfur ':  # Korean Dubeolsik: 한글 입력
        press(client, ord(char))
    toggle(client)
    press(client, 0xff0d)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=5930)
    parser.add_argument('--data', type=Path, help='reuse a disposable test image')
    args = parser.parse_args()
    report = ROOT / 'build/verification'
    report.mkdir(parents=True, exist_ok=True)
    disk = args.data.resolve() if args.data else report / ('korean-user-' + str(int(time.time())) + '.img')
    if not disk.exists():
        prior = report / 'korean.json'
        if not prior.exists(): prior = report / 'desktop.json'
        if prior.exists():
            seed = json.loads(prior.read_text())['data_image']
            subprocess.run(['cp', '--reflink=auto', '--sparse=always', seed, str(disk)], check=True)
        else:
            data_image(disk, 2048)
    log = report / 'korean.log'
    client = None
    with log.open('wb') as output:
        process = subprocess.Popen(command(disk, vnc_port=args.port), stdin=subprocess.PIPE,
                                   stdout=output, stderr=subprocess.STDOUT)
        def send(text):
            raw = text.encode('utf-8') + b'\n'
            for offset in range(0, len(raw), 64):
                process.stdin.write(raw[offset:offset + 64]); process.stdin.flush(); time.sleep(.05)
        def wait(pattern, timeout=900):
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                found = re.search(pattern, log.read_text(errors='replace'))
                if found: return found
                if process.poll() is not None: raise RuntimeError('QEMU exited; see ' + str(log))
                time.sleep(1)
            raise RuntimeError('Timeout: ' + pattern)
        try:
            wait(r'jkoros:~\$')
            send('stty cols 120 rows 40'); time.sleep(1)
            send("export TERM=dumb; set +o emacs; set +o vi; stty -echo; printf 'SERIAL_%s\\n' READY")
            wait(r'\nSERIAL_READY\r?\n')
            send("while [ ! -f /run/user/1000/jkoros-input-ready ]; do sleep 10; tail -n 8 /var/log/desktop.log; done; printf 'INPUT_%s\\n' READY")
            wait(r'INPUT_READY\r?\n', 180)
            send('rm -f ~/한글입력검증.txt ~/터미널입력검증.txt')
            send('export DISPLAY=:0 XAUTHORITY=/run/user/1000/Xauthority; . /etc/profile.d/jkoros.sh')
            send("export DBUS_SESSION_BUS_ADDRESS=$(tr '\\0' '\\n' < /proc/$(pgrep -u 1000 -f '^/usr/bin/fcitx5$')/environ | sed -n 's/^DBUS_SESSION_BUS_ADDRESS=//p')")
            send("fcitx5-remote -c; fcitx5-remote -q; printf 'LOCALE %s %s; XIM %s\\n' \"$LANG\" \"$LC_CTYPE\" \"$XMODIFIERS\"; fc-match monospace; fc-match sans-serif")
            code = base64.b64encode((ROOT / 'tests/한글입력시험.java').read_bytes()).decode()
            send("base64 -d > /tmp/한글입력시험.java <<'JKOROS_SOURCE'")
            for offset in range(0, len(code), 64): send(code[offset:offset + 64])
            send('JKOROS_SOURCE')
            send('javac -encoding UTF-8 -d /tmp /tmp/한글입력시험.java')
            send('java -cp /tmp 한글입력시험 &')
            ready = wait(r'JKOROS_HANGUL_READY (\d+) (\d+)')
            client = VNC(args.port)
            time.sleep(3)
            type_hangul(client, int(ready[1]), int(ready[2]))
            result = wait(r'JKOROS_HANGUL_RESULT ([A-Za-z0-9+/=]+)', 90)
            swing = base64.b64decode(result[1]).decode('utf-8')
            client.screenshot(report / 'korean-swing.png')
            send('fcitx5-remote -c')
            script = "import pathlib; value=input('Ctrl+Space: '); pathlib.Path('/home/user/터미널입력검증.txt').write_text(value.strip(),encoding='utf-8'); print('입력 결과:',value); input('Enter to close: ')"
            encoded = base64.b64encode(script.encode()).decode()
            send("printf '%s' '" + encoded + "' | base64 -d > /tmp/terminal-input.py")
            send('jkoros-terminal -report-fonts -geometry 88x8+120+420 -title "한글 Termînal" -e python3 /tmp/terminal-input.py >/tmp/xterm-fonts.log 2>&1 &')
            time.sleep(10)
            type_hangul(client, 250, 480)
            send('for n in $(seq 1 60); do [ -f ~/터미널입력검증.txt ] && break; sleep 1; done')
            send("printf 'XTERM_%s ' RESULT; base64 -w0 ~/터미널입력검증.txt; printf '\\n'")
            result = wait(r'XTERM_RESULT ([A-Za-z0-9+/=]+)', 90)
            terminal = base64.b64decode(result[1]).decode('utf-8')
            client.screenshot(report / 'korean-desktop.png')
            send('cat /tmp/xterm-fonts.log; xrdb -query')
            send('cat /var/log/desktop.log | tail -n 15')
            send('sudo poweroff')
            assert process.wait(timeout=60) == 0
            assert swing == '한글 입력', repr(swing)
            assert terminal == '한글 입력', repr(terminal)
            content = log.read_text(errors='replace')
            assert 'JKOROS_OVERLAY_READONLY' in content and 'JKOROS_DATA_READONLY' in content
            wide = content.split('Loaded XftFonts(Noto Sans Mono CJK KR[wide])', 1)[1]
            wide = wide.split('Loaded XftFonts(', 1)[0]
            assert 'file=/usr/share/fonts/noto/NotoSansCJK-Regular.ttc' in wide, 'CJK font was substituted'
            result = {'base_id': json.loads((ROOT / 'dist/manifest.json').read_text())['base_id'],
                      'swing_korean': swing, 'xterm_korean': terminal,
                      'xterm_wide_font': 'Noto Sans Mono CJK KR (NotoSansCJK-Regular.ttc)',
                      'input': 'VNC USB keyboard, Ctrl+Space, Dubeolsik composition',
                      'data_image': str(disk), 'clean_shutdown': True, 'log_sha256': digest(log)}
            (report / 'korean.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
            print(json.dumps(result, ensure_ascii=False, indent=2))
        finally:
            if client: client.sock.close()
            if process.poll() is None:
                process.stdin.write(b'\x03'); process.stdin.flush()
                time.sleep(1)
                send('cat /var/log/desktop.log; ps -ef; sudo poweroff')
                try: process.wait(timeout=45)
                except subprocess.TimeoutExpired:
                    process.terminate()
                    try: process.wait(timeout=10)
                    except subprocess.TimeoutExpired: process.kill(); process.wait()


if __name__ == '__main__':
    main()
