#!/usr/bin/env python3
"""ค่าจริง_ข้อมูล OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import tempfile
import threading
import time
import selectors
from Crypto.Cipher import DES
from ดําเนินการ_คําสั่ง import แสดง_ราก, คําสั่ง
from บริดจ์_3de4fe3a import บริดจ์_3de4fe3a


def เรียกใช้งาน():
    ตัวแยกวิเคราะห์_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--kernel', type=Path, default=แสดง_ราก / 'build/kernel8.img')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--access', type=Path, default=แสดง_ราก / 'build/remote/access.json')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--output', type=Path, default=แสดง_ราก / 'build/verification/native-remote')
    อาร์กิวเมนต์ = ตัวแยกวิเคราะห์_48ee4b1b.parse_args()
    ข้อความออก = อาร์กิวเมนต์.output
    ข้อความออก.mkdir(parents=True, exist_ok=True)
    ตั้งค่า = json.loads(อาร์กิวเมนต์.access.read_text())
    รายงาน_ค่า = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(อาร์กิวเมนต์.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as เชื่อมต่อ:
            เชื่อมต่อ.bind(('127.0.0.5', 0))
            return เชื่อมต่อ.getsockname()[1]
    เชลล์_แปลง, 화면포트, แฟ้ม_แปลง = 빈포트(), 빈포트(), 빈포트()
    บันทึก_สถิติ = bytearray()
    กระบวนการ_ค่า = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, บริดจ์_3de4fe3a(แฟ้ม_แปลง,
                ['tcp:{}:22'.format(เชลล์_แปลง), 'tcp:{}:5900'.format(화면포트)], โฮสต์_อีเมล='127.0.0.5') as บริดจ์_ค่า:
            실행인수 = คําสั่ง()
            실행인수[실행인수.index('-kernel') + 1] = str(อาร์กิวเมนต์.kernel.resolve())
            กระบวนการ_ค่า = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + บริดจ์_ค่า.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    ข้อมูล = กระบวนการ_ค่า.stdout.read(4096)
                    if not ข้อมูล: break
                    บันทึก_สถิติ.extend(ข้อมูล)
            เธรด_ค่า = threading.Thread(target=수집, daemon=True)
            เธรด_ค่า.start()
            def ภาวะรอ(คํา_ข้อความ, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while คํา_ข้อความ not in บันทึก_สถิติ[처음:]:
                    if time.monotonic()>끝 or กระบวนการ_ค่า.poll() is not None:
                        raise AssertionError('Missing '+repr(คํา_ข้อความ)+'\n'+บันทึก_สถิติ[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            ภาวะรอ(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            สภาพแวดล้อม = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def ปลอดภัย_เชลล์(รหัสผ่าน_ค่า, 명령어, ผนวก_รายการ=()):
                สภาพแวดล้อม['JKOROS_TEST_PASSWORD']=รหัสผ่าน_ค่า
                อาร์กิวเมนต์=['ssh','-v']+list(ผนวก_รายการ)+['-p',str(เชลล์_แปลง),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                ผลลัพธ์=subprocess.run(อาร์กิวเมนต์,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=สภาพแวดล้อม,start_new_session=True,timeout=50)
                return ผลลัพธ์
            ผลลัพธ์=ปลอดภัย_เชลล์('!' + ตั้งค่า['ssh_password'], 'echo SHOULD_NOT_RUN')
            (ข้อความออก/'ssh-rejected.log').write_bytes(ผลลัพธ์.stderr)
            assert ผลลัพธ์.returncode!=0 and b'Permission denied' in ผลลัพธ์.stderr and b'SHOULD_NOT_RUN' not in บันทึก_สถิติ, ผลลัพธ์.stderr
            รายงาน_ค่า['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            ผลลัพธ์=ปลอดภัย_เชลล์(ตั้งค่า['ssh_password'], 'echo SSH_NATIVE_PASS')
            (ข้อความออก/'ssh.log').write_bytes(ผลลัพธ์.stderr)
            (ข้อความออก/'ssh-output.txt').write_bytes(ผลลัพธ์.stdout)
            assert ผลลัพธ์.returncode==0 and b'SSH_NATIVE_PASS' in ผลลัพธ์.stdout, (ผลลัพธ์.returncode,ผลลัพธ์.stdout,ผลลัพธ์.stderr)
            รายงาน_ค่า['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in ผลลัพธ์.stderr, ผลลัพธ์.stderr
            รายงาน_ค่า['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            ผลลัพธ์=ปลอดภัย_เชลล์(ตั้งค่า['ssh_password'], 'cd /example/java; java พิมพ์; cd /')
            assert ผลลัพธ์.returncode==0 and 'JAVA ข้อความออก: 안녕하세요 😀'.encode() in ผลลัพธ์.stdout,ผลลัพธ์.stdout
            รายงาน_ค่า['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            ผลลัพธ์=ปลอดภัย_เชลล์(ตั้งค่า['ssh_password'], 'missing_remote_command')
            assert ผลลัพธ์.returncode==127,ผลลัพธ์.returncode
            รายงาน_ค่า['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            ผลลัพธ์=ปลอดภัย_เชลล์(ตั้งค่า['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (ข้อความออก/'ssh-rekey.log').write_bytes(ผลลัพธ์.stderr)
            assert ผลลัพธ์.returncode==0 and 'class 창예제'.encode() in ผลลัพธ์.stdout, (ผลลัพธ์.returncode,ผลลัพธ์.stdout,ผลลัพธ์.stderr)
            assert ผลลัพธ์.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, ผลลัพธ์.stderr
            รายงาน_ค่า['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(เชลล์_แปลง),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            대화=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=สภาพแวดล้อม,start_new_session=True,bufsize=0)
            การถอดความ=bytearray();การเลือก_ค่า=selectors.DefaultSelector();การเลือก_ค่า.register(대화.stdout,selectors.EVENT_READ)
            def 대화읽기(แสดง_ค่า):
                วันครบกําหนด_ค่า=time.monotonic()+30
                while แสดง_ค่า not in การถอดความ:
                    if time.monotonic()>วันครบกําหนด_ค่า or 대화.poll() is not None:raise AssertionError('SSH interactive missing '+repr(แสดง_ค่า)+' '+repr(bytes(การถอดความ)))
                    for รายการ_ค่า,_ in การเลือก_ค่า.select(.1):
                        조각=รายการ_ค่า.fileobj.read(4096)
                        if 조각:การถอดความ.extend(조각)
            try:
                대화읽기(b'shared native console')
                대화.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');대화.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                대화.stdin.write(b'\x04');대화.stdin.flush();나머지,ข้อผิดพลาด=대화.communicate(timeout=15)
                assert 대화.returncode==0 and b'PTY allocation request failed' not in ข้อผิดพลาด,(대화.returncode,ข้อผิดพลาด)
                (ข้อความออก/'ssh-interactive.txt').write_bytes(การถอดความ+나머지)
            finally:
                การเลือก_ค่า.close()
                if 대화.poll() is None:대화.kill();대화.wait()
            รายงาน_ค่า['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(เชื่อมต่อ, หมายเลข):
                ข้อมูล=bytearray()
                while len(ข้อมูล)<หมายเลข:
                    덩이=เชื่อมต่อ.recv(หมายเลข-len(ข้อมูล))
                    if not 덩이: raise AssertionError('RFB EOF')
                    ข้อมูล.extend(덩이)
                return bytes(ข้อมูล)
            def 화면인증(รหัสผ่าน_ค่า):
                เชื่อมต่อ=socket.create_connection(('127.0.0.5',화면포트),10);เชื่อมต่อ.settimeout(30)
                assert 정확히(เชื่อมต่อ,12)==b'RFB 003.008\n'
                เชื่อมต่อ.sendall(b'RFB 003.008\n');assert 정확히(เชื่อมต่อ,2)==b'\x01\x02'
                เชื่อมต่อ.sendall(b'\x02');การทดสอบ_ค่า=정확히(เชื่อมต่อ,16)
                입력암호=รหัสผ่าน_ค่า.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(หมายเลข)[::-1],2) for หมายเลข in 입력암호)
                เชื่อมต่อ.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(การทดสอบ_ค่า))
                สถานะ_ค่า=struct.unpack('!I',정확히(เชื่อมต่อ,4))[0]
                return เชื่อมต่อ,สถานะ_ค่า
            ไม่ถูกต้อง_รหัสผ่าน='!' if not ตั้งค่า['vnc_password'].startswith('!') else '?'
            เชื่อมต่อ,สถานะ_ค่า=화면인증(ไม่ถูกต้อง_รหัสผ่าน);assert สถานะ_ค่า==1;เชื่อมต่อ.close();time.sleep(.6)
            รายงาน_ค่า['checks'].append('VNC incorrect password rejected')
            เชื่อมต่อ,สถานะ_ค่า=화면인증(ตั้งค่า['vnc_password']);assert สถานะ_ค่า==0
            with เชื่อมต่อ:
                เชื่อมต่อ.sendall(b'\x01');สภาวะเริ่มต้น=정확히(เชื่อมต่อ,24);너비,높이=struct.unpack('!HH',สภาวะเริ่มต้น[:4]);ชื่อ=정확히(เชื่อมต่อ,struct.unpack('!I',สภาวะเริ่มต้น[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==ชื่อ
                def 화면(증분=0):
                    เชื่อมต่อ.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(เชื่อมต่อ,4);หมายเลข=struct.unpack('!H',머리[2:])[0];รวม_ค่า=0
                    รูปวาด_ค่า=bytearray(너비*높이*4)
                    for _ in range(หมายเลข):
                        พิกัดแกน_x,세로좌표,영역너비,영역높이,เมธอด_โหมด=struct.unpack('!HHHHi',정확히(เชื่อมต่อ,12));assert เมธอด_โหมด==0 and พิกัดแกน_x+영역너비<=너비 and 세로좌표+영역높이<=높이
                        พิกเซล=정확히(เชื่อมต่อ,영역너비*영역높이*4);รวม_ค่า+=len(พิกเซล)
                        for บรรทัด in range(영역높이):รูปวาด_ค่า[((세로좌표+บรรทัด)*너비+พิกัดแกน_x)*4:((세로좌표+บรรทัด)*너비+พิกัดแกน_x+영역너비)*4]=พิกเซล[บรรทัด*영역너비*4:(บรรทัด+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(รูปวาด_ค่า),'raw','BGRX').save(str(ข้อความออก/'native-vnc.png'))
                    return หมายเลข,รวม_ค่า
                หมายเลข,รวม_ค่า=화면();assert หมายเลข>0 and รวม_ค่า==너비*높이*4
                รายงาน_ค่า['checks'].append('Native framebuffer RFB full update {} bytes'.format(รวม_ค่า))
                หมายเลข,รวม_ค่า=화면(1);assert รวม_ค่า<너비*높이*4
                รายงาน_ค่า['checks'].append('RFB incremental update')
                처음=len(บันทึก_สถิติ)
                for อักขระ_ค่า in 'echo VNC_NATIVE_PASS\r':
                    สัญลักษณ์=0xff0d if อักขระ_ค่า=='\r' else ord(อักขระ_ค่า)
                    เชื่อมต่อ.sendall(struct.pack('!BBHI',4,1,0,สัญลักษณ์));เชื่อมต่อ.sendall(struct.pack('!BBHI',4,0,0,สัญลักษณ์))
                ภาวะรอ(b'VNC_NATIVE_PASS',처음)
                รายงาน_ค่า['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def คีย์_เส้นหมึก(สัญลักษณ์,กด_ค่า=1):เชื่อมต่อ.sendall(struct.pack('!BBHI',4,กด_ค่า,0,สัญลักษณ์))
                처음=len(บันทึก_สถิติ)
                for อักขระ_ค่า in 'echo ':คีย์_เส้นหมึก(ord(อักขระ_ค่า))
                คีย์_เส้นหมึก(0xffc6)
                for อักขระ_ค่า in 'gksrmf':คีย์_เส้นหมึก(ord(อักขระ_ค่า))
                คีย์_เส้นหมึก(0xffc6);คีย์_เส้นหมึก(0xff0d)
                ภาวะรอ('\r\n한글\r\n'.encode(),처음)
                รายงาน_ค่า['checks'].append('Native VNC F9 two-set Hangul composition')
                เชื่อมต่อ.sendall(struct.pack('!BBHH',5,0,120,100))
                รายงาน_ค่า['checks'].append('VNC pointer input accepted')
            กระบวนการ_ค่า.stdin.write(b'poweroff\n');กระบวนการ_ค่า.stdin.flush();กระบวนการ_ค่า.wait(timeout=15);assert กระบวนการ_ค่า.returncode==0
            รายงาน_ค่า['passed']=True
    finally:
        if กระบวนการ_ค่า and กระบวนการ_ค่า.poll() is None:
            กระบวนการ_ค่า.terminate()
            try: กระบวนการ_ค่า.wait(timeout=5)
            except subprocess.TimeoutExpired: กระบวนการ_ค่า.kill();กระบวนการ_ค่า.wait()
        (ข้อความออก/'serial.log').write_bytes(บันทึก_สถิติ)
        (ข้อความออก/'report.json').write_text(json.dumps(รายงาน_ค่า,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(รายงาน_ค่า,ensure_ascii=False,indent=2))


if __name__=='__main__': เรียกใช้งาน()
