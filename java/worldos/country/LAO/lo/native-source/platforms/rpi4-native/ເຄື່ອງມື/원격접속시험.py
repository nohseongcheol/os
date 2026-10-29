#!/usr/bin/env python3
"""ຕົວ_ຈິງ_ຂໍ້ມູນ OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ, ຄໍາສັ່ງ_1f12b8e2
from ເຄືອຂ່າຍ_ຕົວເຊື່ອມ import ເຄືອຂ່າຍ_ຕົວເຊື່ອມ


def ແລ່ນ():
    ຕົວແຍກວິເຄາະ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--kernel', type=Path, default=ໂຄງ_ການ_ເລກຮາກ / 'build/kernel8.img')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--access', type=Path, default=ໂຄງ_ການ_ເລກຮາກ / 'build/remote/access.json')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--output', type=Path, default=ໂຄງ_ການ_ເລກຮາກ / 'build/verification/native-remote')
    인수 = ຕົວແຍກວິເຄາະ_48ee4b1b.parse_args()
    출력 = 인수.output
    출력.mkdir(parents=True, exist_ok=True)
    ການຕັ້ງຄ່າ = json.loads(인수.access.read_text())
    ລາຍງານ_ຄ່າ = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(인수.kernel.read_bytes()).hexdigest(), 'checks': []}
    def ຫວ່າງ_ເປົ່າ_ຜອດ():
        with socket.socket() as ເຊື່ອມຕໍ່:
            ເຊື່ອມຕໍ່.bind(('127.0.0.5', 0))
            return ເຊື່ອມຕໍ່.getsockname()[1]
    ເຊລ_ຜອດ, 화면포트, ຟາຍ_ຜອດ = ຫວ່າງ_ເປົ່າ_ຜອດ(), ຫວ່າງ_ເປົ່າ_ຜອດ(), ຫວ່າງ_ເປົ່າ_ຜອດ()
    ບັນທຶກ_ແຖວ = bytearray()
    ຂະ_ບວນ_ການ_ຄ່າ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, ເຄືອຂ່າຍ_ຕົວເຊື່ອມ(ຟາຍ_ຜອດ,
                ['tcp:{}:22'.format(ເຊລ_ຜອດ), 'tcp:{}:5900'.format(화면포트)], ໂຮສ_ອີເມວ='127.0.0.5') as ຕົວເຊື່ອມ_ຄ່າ:
            실행인수 = ຄໍາສັ່ງ_1f12b8e2()
            실행인수[실행인수.index('-kernel') + 1] = str(인수.kernel.resolve())
            ຂະ_ບວນ_ການ_ຄ່າ = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + ຕົວເຊື່ອມ_ຄ່າ.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    ຂໍ້ມູນ = ຂະ_ບວນ_ການ_ຄ່າ.stdout.read(4096)
                    if not ຂໍ້ມູນ: break
                    ບັນທຶກ_ແຖວ.extend(ຂໍ້ມູນ)
            ສອດຕໍ່_ຄ່າ = threading.Thread(target=수집, daemon=True)
            ສອດຕໍ່_ຄ່າ.start()
            def ລໍຖ້າ_ສະຖານະ(ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ not in ບັນທຶກ_ແຖວ[처음:]:
                    if time.monotonic()>끝 or ຂະ_ບວນ_ການ_ຄ່າ.poll() is not None:
                        raise AssertionError('Missing '+repr(ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ)+'\n'+ບັນທຶກ_ແຖວ[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            ລໍຖ້າ_ສະຖານະ(b'jkoros-native> ')
            도우미 = Path(임시)/'askpass'
            도우미.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            도우미.chmod(0o700)
            환경 = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(도우미), SSH_ASKPASS_REQUIRE='force')
            def ຮັກສາຄວາມປອດໄພ_ເຊລ(ລະຫັດຜ່ານ_ຄ່າ, ຄໍາແນະນໍາ_ຄ່າ, 추가=()):
                환경['JKOROS_TEST_PASSWORD']=ລະຫັດຜ່ານ_ຄ່າ
                인수=['ssh','-v']+list(추가)+['-p',str(ເຊລ_ຜອດ),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',ຄໍາແນະນໍາ_ຄ່າ]
                ມາດຕະການ=subprocess.run(인수,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=환경,start_new_session=True,timeout=50)
                return ມາດຕະການ
            ມາດຕະການ=ຮັກສາຄວາມປອດໄພ_ເຊລ('!' + ການຕັ້ງຄ່າ['ssh_password'], 'echo SHOULD_NOT_RUN')
            (출력/'ssh-rejected.log').write_bytes(ມາດຕະການ.stderr)
            assert ມາດຕະການ.returncode!=0 and b'Permission denied' in ມາດຕະການ.stderr and b'SHOULD_NOT_RUN' not in ບັນທຶກ_ແຖວ, ມາດຕະການ.stderr
            ລາຍງານ_ຄ່າ['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            ມາດຕະການ=ຮັກສາຄວາມປອດໄພ_ເຊລ(ການຕັ້ງຄ່າ['ssh_password'], 'echo SSH_NATIVE_PASS')
            (출력/'ssh.log').write_bytes(ມາດຕະການ.stderr)
            (출력/'ssh-output.txt').write_bytes(ມາດຕະການ.stdout)
            assert ມາດຕະການ.returncode==0 and b'SSH_NATIVE_PASS' in ມາດຕະການ.stdout, (ມາດຕະການ.returncode,ມາດຕະການ.stdout,ມາດຕະການ.stderr)
            ລາຍງານ_ຄ່າ['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in ມາດຕະການ.stderr, ມາດຕະການ.stderr
            ລາຍງານ_ຄ່າ['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            ມາດຕະການ=ຮັກສາຄວາມປອດໄພ_ເຊລ(ການຕັ້ງຄ່າ['ssh_password'], 'cd /example/java; java 출력예제; cd /')
            assert ມາດຕະການ.returncode==0 and 'JAVA 출력: 안녕하세요 😀'.encode() in ມາດຕະການ.stdout,ມາດຕະການ.stdout
            ລາຍງານ_ຄ່າ['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            ມາດຕະການ=ຮັກສາຄວາມປອດໄພ_ເຊລ(ການຕັ້ງຄ່າ['ssh_password'], 'missing_remote_command')
            assert ມາດຕະການ.returncode==127,ມາດຕະການ.returncode
            ລາຍງານ_ຄ່າ['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            ມາດຕະການ=ຮັກສາຄວາມປອດໄພ_ເຊລ(ການຕັ້ງຄ່າ['ssh_password'], 'cat /example/java/창예제.java', ('-o', 'RekeyLimit=1K'))
            (출력/'ssh-rekey.log').write_bytes(ມາດຕະການ.stderr)
            assert ມາດຕະການ.returncode==0 and 'class 창예제'.encode() in ມາດຕະການ.stdout, (ມາດຕະການ.returncode,ມາດຕະການ.stdout,ມາດຕະການ.stderr)
            assert ມາດຕະການ.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, ມາດຕະການ.stderr
            ລາຍງານ_ຄ່າ['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(ເຊລ_ຜອດ),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            ແບບໂຕ້ຕອບ_ສະໄຫມ=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=환경,start_new_session=True,bufsize=0)
            대화기록=bytearray();ການ_ເລືອກ_ຄ່າ=selectors.DefaultSelector();ການ_ເລືອກ_ຄ່າ.register(ແບບໂຕ້ຕອບ_ສະໄຫມ.stdout,selectors.EVENT_READ)
            def 대화읽기(ລາຍການ_ຄ່າ):
                마감=time.monotonic()+30
                while ລາຍການ_ຄ່າ not in 대화기록:
                    if time.monotonic()>마감 or ແບບໂຕ້ຕອບ_ສະໄຫມ.poll() is not None:raise AssertionError('SSH interactive missing '+repr(ລາຍການ_ຄ່າ)+' '+repr(bytes(대화기록)))
                    for ເຂົ້າໃນ_ຄ່າ,_ in ການ_ເລືອກ_ຄ່າ.select(.1):
                        조각=ເຂົ້າໃນ_ຄ່າ.fileobj.read(4096)
                        if 조각:대화기록.extend(조각)
            try:
                대화읽기(b'shared native console')
                ແບບໂຕ້ຕອບ_ສະໄຫມ.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');ແບບໂຕ້ຕອບ_ສະໄຫມ.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                ແບບໂຕ້ຕອບ_ສະໄຫມ.stdin.write(b'\x04');ແບບໂຕ້ຕອບ_ສະໄຫມ.stdin.flush();나머지,ຂໍ້ຜິດພາດ=ແບບໂຕ້ຕອບ_ສະໄຫມ.communicate(timeout=15)
                assert ແບບໂຕ້ຕອບ_ສະໄຫມ.returncode==0 and b'PTY allocation request failed' not in ຂໍ້ຜິດພາດ,(ແບບໂຕ້ຕອບ_ສະໄຫມ.returncode,ຂໍ້ຜິດພາດ)
                (출력/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                ການ_ເລືອກ_ຄ່າ.close()
                if ແບບໂຕ້ຕອບ_ສະໄຫມ.poll() is None:ແບບໂຕ້ຕອບ_ສະໄຫມ.kill();ແບບໂຕ້ຕອບ_ສະໄຫມ.wait()
            ລາຍງານ_ຄ່າ['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(ເຊື່ອມຕໍ່, 수):
                ຂໍ້ມູນ=bytearray()
                while len(ຂໍ້ມູນ)<수:
                    덩이=ເຊື່ອມຕໍ່.recv(수-len(ຂໍ້ມູນ))
                    if not 덩이: raise AssertionError('RFB EOF')
                    ຂໍ້ມູນ.extend(덩이)
                return bytes(ຂໍ້ມູນ)
            def 화면인증(ລະຫັດຜ່ານ_ຄ່າ):
                ເຊື່ອມຕໍ່=socket.create_connection(('127.0.0.5',화면포트),10);ເຊື່ອມຕໍ່.settimeout(30)
                assert 정확히(ເຊື່ອມຕໍ່,12)==b'RFB 003.008\n'
                ເຊື່ອມຕໍ່.sendall(b'RFB 003.008\n');assert 정확히(ເຊື່ອມຕໍ່,2)==b'\x01\x02'
                ເຊື່ອມຕໍ່.sendall(b'\x02');ການທ້າທາຍ_ຄ່າ=정확히(ເຊື່ອມຕໍ່,16)
                입력암호=ລະຫັດຜ່ານ_ຄ່າ.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in 입력암호)
                ເຊື່ອມຕໍ່.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(ການທ້າທາຍ_ຄ່າ))
                ສະຖານະ_ຄ່າ=struct.unpack('!I',정확히(ເຊື່ອມຕໍ່,4))[0]
                return ເຊື່ອມຕໍ່,ສະຖານະ_ຄ່າ
            ໃຊ້ບໍ່ໄດ້_ລະຫັດຜ່ານ='!' if not ການຕັ້ງຄ່າ['vnc_password'].startswith('!') else '?'
            ເຊື່ອມຕໍ່,ສະຖານະ_ຄ່າ=화면인증(ໃຊ້ບໍ່ໄດ້_ລະຫັດຜ່ານ);assert ສະຖານະ_ຄ່າ==1;ເຊື່ອມຕໍ່.close();time.sleep(.6)
            ລາຍງານ_ຄ່າ['checks'].append('VNC incorrect password rejected')
            ເຊື່ອມຕໍ່,ສະຖານະ_ຄ່າ=화면인증(ການຕັ້ງຄ່າ['vnc_password']);assert ສະຖານະ_ຄ່າ==0
            with ເຊື່ອມຕໍ່:
                ເຊື່ອມຕໍ່.sendall(b'\x01');초기=정확히(ເຊື່ອມຕໍ່,24);너비,높이=struct.unpack('!HH',초기[:4]);ຊື່=정확히(ເຊື່ອມຕໍ່,struct.unpack('!I',초기[20:24])[0])
                assert (너비,높이)==(640,480) and b'jkoros native'==ຊື່
                def 화면(증분=0):
                    ເຊື່ອມຕໍ່.sendall(struct.pack('!BBHHHH',3,증분,0,0,너비,높이));머리=정확히(ເຊື່ອມຕໍ່,4);수=struct.unpack('!H',머리[2:])[0];합계=0
                    ການ_ແຕ້ມ_ຄ່າ=bytearray(너비*높이*4)
                    for _ in range(수):
                        ຈຸດ_ພິ_ກັດ_x,ປຸ່ມ_Y_ຈຸດປະສານ,영역너비,영역높이,ວິ_ທີ_ໂຫມດ=struct.unpack('!HHHHi',정확히(ເຊື່ອມຕໍ່,12));assert ວິ_ທີ_ໂຫມດ==0 and ຈຸດ_ພິ_ກັດ_x+영역너비<=너비 and ປຸ່ມ_Y_ຈຸດປະສານ+영역높이<=높이
                        ເປ_ລ=정확히(ເຊື່ອມຕໍ່,영역너비*영역높이*4);합계+=len(ເປ_ລ)
                        for ສາຍ in range(영역높이):ການ_ແຕ້ມ_ຄ່າ[((ປຸ່ມ_Y_ຈຸດປະສານ+ສາຍ)*너비+ຈຸດ_ພິ_ກັດ_x)*4:((ປຸ່ມ_Y_ຈຸດປະສານ+ສາຍ)*너비+ຈຸດ_ພິ_ກັດ_x+영역너비)*4]=ເປ_ລ[ສາຍ*영역너비*4:(ສາຍ+1)*영역너비*4]
                    if not 증분:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,높이),bytes(ການ_ແຕ້ມ_ຄ່າ),'raw','BGRX').save(str(출력/'native-vnc.png'))
                    return 수,합계
                수,합계=화면();assert 수>0 and 합계==너비*높이*4
                ລາຍງານ_ຄ່າ['checks'].append('Native framebuffer RFB full update {} bytes'.format(합계))
                수,합계=화면(1);assert 합계<너비*높이*4
                ລາຍງານ_ຄ່າ['checks'].append('RFB incremental update')
                처음=len(ບັນທຶກ_ແຖວ)
                for ຕົວອັກສອນ_ຄ່າ in 'echo VNC_NATIVE_PASS\r':
                    ສັນຍາລັກ=0xff0d if ຕົວອັກສອນ_ຄ່າ=='\r' else ord(ຕົວອັກສອນ_ຄ່າ)
                    ເຊື່ອມຕໍ່.sendall(struct.pack('!BBHI',4,1,0,ສັນຍາລັກ));ເຊື່ອມຕໍ່.sendall(struct.pack('!BBHI',4,0,0,ສັນຍາລັກ))
                ລໍຖ້າ_ສະຖານະ(b'VNC_NATIVE_PASS',처음)
                ລາຍງານ_ຄ່າ['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(ສັນຍາລັກ,누름=1):ເຊື່ອມຕໍ່.sendall(struct.pack('!BBHI',4,누름,0,ສັນຍາລັກ))
                처음=len(ບັນທຶກ_ແຖວ)
                for ຕົວອັກສອນ_ຄ່າ in 'echo ':글쇠(ord(ຕົວອັກສອນ_ຄ່າ))
                글쇠(0xffc6)
                for ຕົວອັກສອນ_ຄ່າ in 'gksrmf':글쇠(ord(ຕົວອັກສອນ_ຄ່າ))
                글쇠(0xffc6);글쇠(0xff0d)
                ລໍຖ້າ_ສະຖານະ('\r\n한글\r\n'.encode(),처음)
                ລາຍງານ_ຄ່າ['checks'].append('Native VNC F9 two-set Hangul composition')
                ເຊື່ອມຕໍ່.sendall(struct.pack('!BBHH',5,0,120,100))
                ລາຍງານ_ຄ່າ['checks'].append('VNC pointer input accepted')
            ຂະ_ບວນ_ການ_ຄ່າ.stdin.write(b'poweroff\n');ຂະ_ບວນ_ການ_ຄ່າ.stdin.flush();ຂະ_ບວນ_ການ_ຄ່າ.wait(timeout=15);assert ຂະ_ບວນ_ການ_ຄ່າ.returncode==0
            ລາຍງານ_ຄ່າ['passed']=True
    finally:
        if ຂະ_ບວນ_ການ_ຄ່າ and ຂະ_ບວນ_ການ_ຄ່າ.poll() is None:
            ຂະ_ບວນ_ການ_ຄ່າ.terminate()
            try: ຂະ_ບວນ_ການ_ຄ່າ.wait(timeout=5)
            except subprocess.TimeoutExpired: ຂະ_ບວນ_ການ_ຄ່າ.kill();ຂະ_ບວນ_ການ_ຄ່າ.wait()
        (출력/'serial.log').write_bytes(ບັນທຶກ_ແຖວ)
        (출력/'report.json').write_text(json.dumps(ລາຍງານ_ຄ່າ,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(ລາຍງານ_ຄ່າ,ensure_ascii=False,indent=2))


if __name__=='__main__': ແລ່ນ()
