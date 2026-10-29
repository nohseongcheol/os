#!/usr/bin/env python3
"""dữLiệuThựcTế OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from thựcThiLệnh import gốcCâyDựÁn, lệnh
from cầuNốiMạng import cầuNốiMạng


def chạy():
    BộPhânTích = argparse.ArgumentParser(description=__doc__)
    BộPhânTích.add_argument('--kernel', type=Path, default=gốcCâyDựÁn / 'build/kernel8.img')
    BộPhânTích.add_argument('--access', type=Path, default=gốcCâyDựÁn / 'build/remote/access.json')
    BộPhânTích.add_argument('--output', type=Path, default=gốcCâyDựÁn / 'build/verification/native-remote')
    cácĐốiSố = BộPhânTích.parse_args()
    ĐầuRa = cácĐốiSố.output
    ĐầuRa.mkdir(parents=True, exist_ok=True)
    cácThiếtLập = json.loads(cácĐốiSố.access.read_text())
    giáTrịBáoCáo = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(cácĐốiSố.kernel.read_bytes()).hexdigest(), 'checks': []}
    def cổngRỗng():
        with socket.socket() as nốiKết:
            nốiKết.bind(('127.0.0.5', 0))
            return nốiKết.getsockname()[1]
    cổngVỏLệnh, cổngMànHình, cổngTệp = cổngRỗng(), cổngRỗng(), cổngRỗng()
    bảnGhiNhậtKý = bytearray()
    giáTrịTiếnTrình = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as giáTrịTạm, cầuNốiMạng(cổngTệp,
                ['tcp:{}:22'.format(cổngVỏLệnh), 'tcp:{}:5900'.format(cổngMànHình)], địaChỉChủ='127.0.0.5') as giáTrịCầuNối:
            CácĐốiSố = lệnh()
            CácĐốiSố[CácĐốiSố.index('-kernel') + 1] = str(cácĐốiSố.kernel.resolve())
            giáTrịTiếnTrình = subprocess.Popen(CácĐốiSố + ['-display','none','-monitor','none','-serial','stdio'] + giáTrịCầuNối.đốiSốĐãChuyểnTiếp(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def gomCácGiáTrị():
                while True:
                    DữLiệu = giáTrịTiếnTrình.stdout.read(4096)
                    if not DữLiệu: break
                    bảnGhiNhậtKý.extend(DữLiệu)
            giáTrịLuồngChạy = threading.Thread(target=gomCácGiáTrị, daemon=True)
            giáTrịLuồngChạy.start()
            def chờTrạngThái(vănBảnTừ, phầnMụcBanĐầu=0, giáTrịGiớiHạn=60):
                phầnKết = time.monotonic() + giáTrịGiớiHạn
                while vănBảnTừ not in bảnGhiNhậtKý[phầnMụcBanĐầu:]:
                    if time.monotonic()>phầnKết or giáTrịTiếnTrình.poll() is not None:
                        raise AssertionError('Missing '+repr(vănBảnTừ)+'\n'+bảnGhiNhậtKý[phầnMụcBanĐầu:].decode('utf-8','replace'))
                    time.sleep(.02)
            chờTrạngThái(b'jkoros-native> ')
            giáTrịPhụGiúp = Path(giáTrịTạm)/'askpass'
            giáTrịPhụGiúp.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            giáTrịPhụGiúp.chmod(0o700)
            môiTrường = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(giáTrịPhụGiúp), SSH_ASKPASS_REQUIRE='force')
            def vỏLệnhAnToàn(giáTrịMậtKhẩu, giáTrịChỉLệnh, thêmCuốiMục=()):
                môiTrường['JKOROS_TEST_PASSWORD']=giáTrịMậtKhẩu
                cácĐốiSố=['ssh','-v']+list(thêmCuốiMục)+['-p',str(cổngVỏLệnh),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(giáTrịTạm)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',giáTrịChỉLệnh]
                kếtQuả=subprocess.run(cácĐốiSố,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=môiTrường,start_new_session=True,timeout=50)
                return kếtQuả
            kếtQuả=vỏLệnhAnToàn('!' + cácThiếtLập['ssh_password'], 'echo SHOULD_NOT_RUN')
            (ĐầuRa/'ssh-rejected.log').write_bytes(kếtQuả.stderr)
            assert kếtQuả.returncode!=0 and b'Permission denied' in kếtQuả.stderr and b'SHOULD_NOT_RUN' not in bảnGhiNhậtKý, kếtQuả.stderr
            giáTrịBáoCáo['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            kếtQuả=vỏLệnhAnToàn(cácThiếtLập['ssh_password'], 'echo SSH_NATIVE_PASS')
            (ĐầuRa/'ssh.log').write_bytes(kếtQuả.stderr)
            (ĐầuRa/'ssh-output.txt').write_bytes(kếtQuả.stdout)
            assert kếtQuả.returncode==0 and b'SSH_NATIVE_PASS' in kếtQuả.stdout, (kếtQuả.returncode,kếtQuả.stdout,kếtQuả.stderr)
            giáTrịBáoCáo['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in kếtQuả.stderr, kếtQuả.stderr
            giáTrịBáoCáo['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            kếtQuả=vỏLệnhAnToàn(cácThiếtLập['ssh_password'], 'cd /example/java; java VíDụIn; cd /')
            assert kếtQuả.returncode==0 and 'JAVA ĐầuRa: 안녕하세요 😀'.encode() in kếtQuả.stdout,kếtQuả.stdout
            giáTrịBáoCáo['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            kếtQuả=vỏLệnhAnToàn(cácThiếtLập['ssh_password'], 'missing_remote_command')
            assert kếtQuả.returncode==127,kếtQuả.returncode
            giáTrịBáoCáo['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            kếtQuả=vỏLệnhAnToàn(cácThiếtLập['ssh_password'], 'cat /example/java/VíDụCửaSổ.java', ('-o', 'RekeyLimit=1K'))
            (ĐầuRa/'ssh-rekey.log').write_bytes(kếtQuả.stderr)
            assert kếtQuả.returncode==0 and 'class VíDụCửaSổ'.encode() in kếtQuả.stdout, (kếtQuả.returncode,kếtQuả.stdout,kếtQuả.stderr)
            assert kếtQuả.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, kếtQuả.stderr
            giáTrịBáoCáo['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            cácĐốiSốTươngTác=['ssh','-tt','-p',str(cổngVỏLệnh),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(giáTrịTạm)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            phiênTươngTác=subprocess.Popen(cácĐốiSốTươngTác,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=môiTrường,start_new_session=True,bufsize=0)
            bảnGhiDiễnTiến=bytearray();giáTrịViệcChọn=selectors.DefaultSelector();giáTrịViệcChọn.register(phiênTươngTác.stdout,selectors.EVENT_READ)
            def đọcTươngTác(hiệnGiáTrị):
                giáTrịHạnChót=time.monotonic()+30
                while hiệnGiáTrị not in bảnGhiDiễnTiến:
                    if time.monotonic()>giáTrịHạnChót or phiênTươngTác.poll() is not None:raise AssertionError('SSH interactive missing '+repr(hiệnGiáTrị)+' '+repr(bytes(bảnGhiDiễnTiến)))
                    for giáTrịMục,_ in giáTrịViệcChọn.select(.1):
                        giáTrịĐoạn=giáTrịMục.fileobj.read(4096)
                        if giáTrịĐoạn:bảnGhiDiễnTiến.extend(giáTrịĐoạn)
            try:
                đọcTươngTác(b'shared native console')
                phiênTươngTác.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');phiênTươngTác.stdin.flush();đọcTươngTác(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                phiênTươngTác.stdin.write(b'\x04');phiênTươngTác.stdin.flush();giáTrịSốDư,lỗi=phiênTươngTác.communicate(timeout=15)
                assert phiênTươngTác.returncode==0 and b'PTY allocation request failed' not in lỗi,(phiênTươngTác.returncode,lỗi)
                (ĐầuRa/'ssh-interactive.txt').write_bytes(bảnGhiDiễnTiến+giáTrịSốDư)
            finally:
                giáTrịViệcChọn.close()
                if phiênTươngTác.poll() is None:phiênTươngTác.kill();phiênTươngTác.wait()
            giáTrịBáoCáo['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def giáTrịĐúngBằng(nốiKết, trịSố):
                DữLiệu=bytearray()
                while len(DữLiệu)<trịSố:
                    giáTrịMảnh=nốiKết.recv(trịSố-len(DữLiệu))
                    if not giáTrịMảnh: raise AssertionError('RFB EOF')
                    DữLiệu.extend(giáTrịMảnh)
                return bytes(DữLiệu)
            def xácThựcMànHình(giáTrịMậtKhẩu):
                nốiKết=socket.create_connection(('127.0.0.5',cổngMànHình),10);nốiKết.settimeout(30)
                assert giáTrịĐúngBằng(nốiKết,12)==b'RFB 003.008\n'
                nốiKết.sendall(b'RFB 003.008\n');assert giáTrịĐúngBằng(nốiKết,2)==b'\x01\x02'
                nốiKết.sendall(b'\x02');giáTrịTháchThức=giáTrịĐúngBằng(nốiKết,16)
                mậtKhẩuĐầuVào=giáTrịMậtKhẩu.encode('ascii')[:8].ljust(8, b'\0')
                vậtLiệuPhím=bytes(int('{:08b}'.format(trịSố)[::-1],2) for trịSố in mậtKhẩuĐầuVào)
                nốiKết.sendall(DES.new(vậtLiệuPhím,DES.MODE_ECB).encrypt(giáTrịTháchThức))
                giáTrịTrạngThái=struct.unpack('!I',giáTrịĐúngBằng(nốiKết,4))[0]
                return nốiKết,giáTrịTrạngThái
            mậtKhẩuKhôngHợpLệ='!' if not cácThiếtLập['vnc_password'].startswith('!') else '?'
            nốiKết,giáTrịTrạngThái=xácThựcMànHình(mậtKhẩuKhôngHợpLệ);assert giáTrịTrạngThái==1;nốiKết.close();time.sleep(.6)
            giáTrịBáoCáo['checks'].append('VNC incorrect password rejected')
            nốiKết,giáTrịTrạngThái=xácThựcMànHình(cácThiếtLập['vnc_password']);assert giáTrịTrạngThái==0
            with nốiKết:
                nốiKết.sendall(b'\x01');trạngTháiBanĐầu=giáTrịĐúngBằng(nốiKết,24);giáTrịRộng,giáTrịCao=struct.unpack('!HH',trạngTháiBanĐầu[:4]);tên=giáTrịĐúngBằng(nốiKết,struct.unpack('!I',trạngTháiBanĐầu[20:24])[0])
                assert (giáTrịRộng,giáTrịCao)==(640,480) and b'jkoros native'==tên
                def MànHình(bướcBướcTăng=0):
                    nốiKết.sendall(struct.pack('!BBHHHH',3,bướcBướcTăng,0,0,giáTrịRộng,giáTrịCao));giáTrịĐầu=giáTrịĐúngBằng(nốiKết,4);trịSố=struct.unpack('!H',giáTrịĐầu[2:])[0];giáTrịTổngCộng=0
                    HìnhVẽ=bytearray(giáTrịRộng*giáTrịCao*4)
                    for _ in range(trịSố):
                        tọaĐộX,tọaĐộY,rộngMiền,caoMiền,chếĐộPhươngThức=struct.unpack('!HHHHi',giáTrịĐúngBằng(nốiKết,12));assert chếĐộPhươngThức==0 and tọaĐộX+rộngMiền<=giáTrịRộng and tọaĐộY+caoMiền<=giáTrịCao
                        điểmẢnh=giáTrịĐúngBằng(nốiKết,rộngMiền*caoMiền*4);giáTrịTổngCộng+=len(điểmẢnh)
                        for dòng in range(caoMiền):HìnhVẽ[((tọaĐộY+dòng)*giáTrịRộng+tọaĐộX)*4:((tọaĐộY+dòng)*giáTrịRộng+tọaĐộX+rộngMiền)*4]=điểmẢnh[dòng*rộngMiền*4:(dòng+1)*rộngMiền*4]
                    if not bướcBướcTăng:
                        from PIL import Image
                        Image.frombytes('RGB',(giáTrịRộng,giáTrịCao),bytes(HìnhVẽ),'raw','BGRX').save(str(ĐầuRa/'native-vnc.png'))
                    return trịSố,giáTrịTổngCộng
                trịSố,giáTrịTổngCộng=MànHình();assert trịSố>0 and giáTrịTổngCộng==giáTrịRộng*giáTrịCao*4
                giáTrịBáoCáo['checks'].append('Native framebuffer RFB full update {} bytes'.format(giáTrịTổngCộng))
                trịSố,giáTrịTổngCộng=MànHình(1);assert giáTrịTổngCộng<giáTrịRộng*giáTrịCao*4
                giáTrịBáoCáo['checks'].append('RFB incremental update')
                phầnMụcBanĐầu=len(bảnGhiNhậtKý)
                for giáTrịKýTự in 'echo VNC_NATIVE_PASS\r':
                    kýHiệu=0xff0d if giáTrịKýTự=='\r' else ord(giáTrịKýTự)
                    nốiKết.sendall(struct.pack('!BBHI',4,1,0,kýHiệu));nốiKết.sendall(struct.pack('!BBHI',4,0,0,kýHiệu))
                chờTrạngThái(b'VNC_NATIVE_PASS',phầnMụcBanĐầu)
                giáTrịBáoCáo['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def nétPhím(kýHiệu,giáTrịNhấn=1):nốiKết.sendall(struct.pack('!BBHI',4,giáTrịNhấn,0,kýHiệu))
                phầnMụcBanĐầu=len(bảnGhiNhậtKý)
                for giáTrịKýTự in 'echo ':nétPhím(ord(giáTrịKýTự))
                nétPhím(0xffc6)
                for giáTrịKýTự in 'gksrmf':nétPhím(ord(giáTrịKýTự))
                nétPhím(0xffc6);nétPhím(0xff0d)
                chờTrạngThái('\r\n한글\r\n'.encode(),phầnMụcBanĐầu)
                giáTrịBáoCáo['checks'].append('Native VNC F9 two-set Hangul composition')
                nốiKết.sendall(struct.pack('!BBHH',5,0,120,100))
                giáTrịBáoCáo['checks'].append('VNC pointer input accepted')
            giáTrịTiếnTrình.stdin.write(b'poweroff\n');giáTrịTiếnTrình.stdin.flush();giáTrịTiếnTrình.wait(timeout=15);assert giáTrịTiếnTrình.returncode==0
            giáTrịBáoCáo['passed']=True
    finally:
        if giáTrịTiếnTrình and giáTrịTiếnTrình.poll() is None:
            giáTrịTiếnTrình.terminate()
            try: giáTrịTiếnTrình.wait(timeout=5)
            except subprocess.TimeoutExpired: giáTrịTiếnTrình.kill();giáTrịTiếnTrình.wait()
        (ĐầuRa/'serial.log').write_bytes(bảnGhiNhậtKý)
        (ĐầuRa/'report.json').write_text(json.dumps(giáTrịBáoCáo,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(giáTrịBáoCáo,ensure_ascii=False,indent=2))


if __name__=='__main__': chạy()
