#!/usr/bin/env python3
"""Verify the real QEMU VNC display and USB input with Swing, without Xvfb."""
import argparse
import base64
import json
from pathlib import Path
import re
import socket
import struct
import subprocess
import time

from PIL import Image
from build import data_image
from prepare import ROOT, digest
from run_qemu import command


class VNC:
    def __init__(self, port):
        self.sock = socket.create_connection(('127.0.0.1', port), timeout=30)
        assert self.read(12).startswith(b'RFB 003.')
        self.sock.sendall(b'RFB 003.008\n')
        choices = self.read(self.read(1)[0])
        assert 1 in choices, 'Local QEMU VNC must offer None authentication'
        self.sock.sendall(b'\x01')
        assert self.read(4) == b'\0' * 4
        self.sock.sendall(b'\x01')
        header = self.read(24)
        self.width, self.height = struct.unpack('!HH', header[:4])
        self.read(struct.unpack('!I', header[20:])[0])
        pixel_format = struct.pack('!BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0)
        self.sock.sendall(b'\0' * 4 + pixel_format)
        self.sock.sendall(struct.pack('!BBHi', 2, 0, 1, 0))

    def read(self, length):
        result = bytearray()
        while len(result) < length:
            block = self.sock.recv(length - len(result))
            if not block:
                raise RuntimeError('VNC disconnected')
            result.extend(block)
        return bytes(result)

    def screenshot(self, destination):
        self.sock.sendall(struct.pack('!BBHHHH', 3, 0, 0, 0, self.width, self.height))
        picture = Image.new('RGB', (self.width, self.height))
        while True:
            kind = self.read(1)[0]
            if kind == 0:
                count = struct.unpack('!xH', self.read(3))[0]
                for _ in range(count):
                    x, y, w, h, encoding = struct.unpack('!HHHHi', self.read(12))
                    assert encoding == 0, encoding
                    tile = Image.frombytes('RGB', (w, h), self.read(w * h * 4), 'raw', 'BGRX')
                    picture.paste(tile, (x, y))
                picture.save(str(destination))
                return
            if kind == 2:
                continue
            if kind == 3:
                self.read(struct.unpack('!3xI', self.read(7))[0])
            else:
                raise RuntimeError('Unexpected VNC message: ' + str(kind))

    def click_and_type(self, x, y):
        for mask in [0, 1, 0]:
            self.sock.sendall(struct.pack('!BBHH', 5, mask, x, y))
            time.sleep(.15)
        for down in [1, 0]:
            self.sock.sendall(struct.pack('!BBHI', 4, down, 0, ord('k')))
            time.sleep(.15)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=5912)
    parser.add_argument('--data', type=Path, help='reuse a disposable test data image')
    args = parser.parse_args()
    report_dir = ROOT / 'build/verification'
    disk = args.data.resolve() if args.data else report_dir / ('desktop-user-' + str(int(time.time())) + '.img')
    if not disk.exists():
        data_image(disk, 2048)
    log = report_dir / 'desktop.log'
    with log.open('wb') as output:
        process = subprocess.Popen(command(disk, vnc_port=args.port), stdin=subprocess.PIPE,
                                   stdout=output, stderr=subprocess.STDOUT)
        def send(text):
            raw = text.encode('utf-8') + b'\n'
            for offset in range(0, len(raw), 64):
                process.stdin.write(raw[offset:offset + 64])
                process.stdin.flush()
                time.sleep(.05)
        def wait(pattern, timeout=900):
            end = time.monotonic() + timeout
            while time.monotonic() < end:
                contents = log.read_text(errors='replace')
                found = re.search(pattern, contents)
                if found:
                    return found
                if process.poll() is not None:
                    raise RuntimeError('QEMU exited; see ' + str(log))
                time.sleep(1)
            raise RuntimeError('Timed out waiting for ' + pattern + '; see ' + str(log))
        client = None
        try:
            wait(r'jkoros:~\$')
            send('stty cols 120 rows 40')
            time.sleep(1)
            send("export TERM=dumb; set +o emacs; set +o vi; stty -echo; printf 'SERIAL_%s\\n' READY")
            wait(r'\nSERIAL_READY\r?\n')
            # Use the same X server and authentication as the graphical terminal.
            send('export DISPLAY=:0 XAUTHORITY=/run/user/1000/Xauthority; cd ~/workspace')
            code = base64.b64encode((ROOT / 'tests/图形输入测试.java').read_bytes()).decode()
            send("base64 -d > /tmp/图形输入测试.java <<'JKOROS_SOURCE'")
            for offset in range(0, len(code), 64):
                send(code[offset:offset + 64])
            send('JKOROS_SOURCE')
            send("javac -encoding UTF-8 -cp /opt/jkoros/lib/中文Java.jar -d /tmp /tmp/图形输入测试.java 问候例.java")
            send("java -cp /tmp:/opt/jkoros/lib/中文Java.jar 图形输入测试 &")
            ready = wait(r'JKOROS_GUI_READY (\d+) (\d+)')
            client = VNC(args.port)
            client.screenshot(report_dir / 'desktop-input.png')
            deadline = time.monotonic() + 180
            while 'JKOROS_VNC_INPUT_PASS' not in log.read_text(errors='replace'):
                if time.monotonic() > deadline:
                    raise RuntimeError('VNC keyboard/mouse input was not received')
                client.click_and_type(int(ready[1]), int(ready[2]))
                time.sleep(3)
            wait(r'JKOROS_GREETING_VISIBLE')
            time.sleep(2)
            client.screenshot(report_dir / 'desktop-greeting.png')
            send('sudo poweroff')
            assert process.wait(timeout=60) == 0
            contents = log.read_text(errors='replace')
            assert 'JKOROS_OVERLAY_READONLY' in contents and 'JKOROS_DATA_READONLY' in contents
            report = {'base_id': json.loads((ROOT / 'dist/manifest.json').read_text())['base_id'],
                      'display': 'Xorg + bochs DRM + QEMU VNC', 'xvfb': False,
                      'swing_window': 'pass', 'vnc_mouse_and_keyboard': 'pass',
                      'greeting': 'pass', 'clean_shutdown': 'pass',
                      'data_image': str(disk), 'log_sha256': digest(log)}
            (report_dir / 'desktop.json').write_text(json.dumps(report, indent=2) + '\n')
            print(json.dumps(report, indent=2))
        finally:
            if client:
                client.sock.close()
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill(); process.wait()


if __name__ == '__main__':
    main()
