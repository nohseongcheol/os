#!/usr/bin/env python3
"""Exercise an exported edition's normal GUI, serial compiler and poweroff path."""
import argparse
import base64
import json
import os
from pathlib import Path
import shlex
import signal
import socket
import subprocess
import time
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--timeout', type=int, default=360)
    args = parser.parse_args()
    edition = Path(args.root).resolve()
    output = ROOT / 'build/verification' / ('normal-' + time.strftime('%Y%m%d-%H%M%S'))
    output.mkdir(parents=True)
    disk = output / 'data.ext4'
    serial = output / 'serial.log'
    qmp_path = output / 'qmp.sock'
    report = {'edition': json.loads((edition / 'edition.json').read_text())['main'],
              'standalone_root': str(edition), 'passed': False}
    source = ('public class जाँच { public static void main(String[] args) throws Exception { '
              'java.nio.file.Files.writeString(java.nio.file.Path.of("normal.txt"), "नमस्ते"); '
              'System.out.println("PASS normal-guest-javac-file-io"); } }')
    encoded = base64.b64encode(source.encode('utf-8')).decode('ascii')
    font_source = base64.b64encode((ROOT / 'tests/FontFeatures.java').read_bytes()).decode('ascii')
    command = ("printf '%s' " + shlex.quote(encoded) + ' | base64 -d > जाँच.java\n'
               "printf '%s' " + shlex.quote(font_source) + ' | base64 -d > FontFeatures.java\n'
               'javac -encoding UTF-8 जाँच.java FontFeatures.java && java -cp . FontFeatures && java -cp . जाँच\n')
    with serial.open('wb') as log:
        process = subprocess.Popen(['python3', str(edition / 'edition.py'), 'run',
                                    '--headless', '--disk', str(disk), '--qmp', str(qmp_path),
                                    '--timeout', str(args.timeout)], stdin=subprocess.PIPE,
                                   stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        deadline = time.monotonic() + args.timeout

        def wait_for(predicate):
            while not predicate():
                text = serial.read_text(errors='replace')
                if process.poll() is not None or time.monotonic() > deadline or 'applet not found' in text or 'java.lang.AssertionError' in text:
                    raise RuntimeError('Normal session failed; see ' + str(serial))
                time.sleep(1)

        try:
            wait_for(lambda: 'Type poweroff to stop.' in serial.read_text(errors='replace'))
            process.stdin.write(command.encode('utf-8'))
            process.stdin.flush()
            wait_for(lambda: 'PASS normal-guest-javac-file-io' in serial.read_text(errors='replace'))
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
                connection.settimeout(10)
                connection.connect(str(qmp_path))
                stream = connection.makefile('rb')
                json.loads(stream.readline().decode())

                def qmp(request):
                    connection.sendall((json.dumps(request) + '\n').encode())
                    while True:
                        reply = json.loads(stream.readline().decode())
                        if 'error' in reply:
                            raise RuntimeError(str(reply))
                        if 'return' in reply:
                            return reply['return']

                qmp({'execute': 'qmp_capabilities'})

                def screenshot_ready():
                    qmp({'execute': 'screendump', 'arguments': {'filename': str(output / 'desktop.ppm')}})
                    with Image.open(str(output / 'desktop.ppm')) as screen:
                        pixels = list(screen.convert('RGB').resize((128, 96)).getdata())
                        # The normal desktop's two editor panes occupy most of the screen.
                        ready = sum(min(pixel) > 235 for pixel in pixels) > len(pixels) * 0.25
                        if ready:
                            screen.save(str(output / 'desktop.png'))
                        return ready

                wait_for(screenshot_ready)
                time.sleep(3)
                screenshot_ready()
            process.stdin.write(b'poweroff\n')
            process.stdin.flush()
            process.wait(timeout=60)
            text = serial.read_text(errors='replace')
            with (output / 'filesystem.log').open('wb') as diagnostics:
                check = subprocess.run(['e2fsck', '-fn', str(disk)], stdout=diagnostics, stderr=subprocess.STDOUT)
            diagnostics = (output / 'filesystem.log').read_text(errors='replace')
            clean = check.returncode == 0 and 'skipping journal recovery' not in diagnostics and 'Fix? no' not in diagnostics
            subprocess.run(['debugfs', '-R', 'dump /root/home/user/workspace/normal.txt ' + str(output / 'normal.txt'), str(disk)], check=True)
            persisted = (output / 'normal.txt').read_text() == 'नमस्ते'
            report.update({'filesystem_clean': clean, 'saved_unicode_file': persisted,
                           'font_samples': 27 if 'PASS logical-fonts-27-script-samples' in text else 0,
                           'serial_poweroff': 'WORLDOS_SHUTDOWN_CLEAN' in text,
                           'passed': process.returncode == 0 and clean and persisted and 'WORLDOS_SHUTDOWN_CLEAN' in text})
            if not report['passed']:
                raise RuntimeError('Normal session validation failed')
        finally:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
            (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
            print('Normal session artifacts: ' + str(output), flush=True)


if __name__ == '__main__':
    main()
