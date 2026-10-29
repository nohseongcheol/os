#!/usr/bin/env python3
"""တကယ့်ဒေတာ OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
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
from စက်မောင်း import စီမံကိန်းအမြစ်, အမိန့်
from ကွန်ရက်တံတား import ကွန်ရက်တံတား


def လုပ်ဆောင်():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--kernel', type=Path, default=စီမံကိန်းအမြစ် / 'build/kernel8.img')
    해석기.add_argument('--access', type=Path, default=စီမံကိန်းအမြစ် / 'build/remote/access.json')
    해석기.add_argument('--output', type=Path, default=စီမံကိန်းအမြစ် / 'build/verification/native-remote')
    အချက်များ = 해석기.parse_args()
    အထွက် = အချက်များ.output
    အထွက်.mkdir(parents=True, exist_ok=True)
    သတ်မှတ်ချက် = json.loads(အချက်များ.access.read_text())
    အစီရင်ခံစာတန်ဖိုး = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(အချက်များ.kernel.read_bytes()).hexdigest(), 'checks': []}
    def အလွတ်ဆက်သွယ်ပေါက်():
        with socket.socket() as ချိတ်ဆက်:
            ချိတ်ဆက်.bind(('127.0.0.5', 0))
            return ချိတ်ဆက်.getsockname()[1]
    အမိန့်ဝင်းဆက်သွယ်ပေါက်, မျက်နှာပြင်ဆက်သွယ်ပေါက်, ဖိုင်ဆက်သွယ်ပေါက် = အလွတ်ဆက်သွယ်ပေါက်(), အလွတ်ဆက်သွယ်ပေါက်(), အလွတ်ဆက်သွယ်ပေါက်()
    မှတ်တမ်းမှတ်တမ်းတစ်ခု = bytearray()
    လုပ်ငန်းစဉ် = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as ယာယီတန်ဖိုး, ကွန်ရက်တံတား(ဖိုင်ဆက်သွယ်ပေါက်,
                ['tcp:{}:22'.format(အမိန့်ဝင်းဆက်သွယ်ပေါက်), 'tcp:{}:5900'.format(မျက်နှာပြင်ဆက်သွယ်ပေါက်)], အိမ်ရှင်လိပ်စာ='127.0.0.5') as တံတားတန်ဖိုး:
            လုပ်ဆောင်အချက်များ = အမိန့်()
            လုပ်ဆောင်အချက်များ[လုပ်ဆောင်အချက်များ.index('-kernel') + 1] = str(အချက်များ.kernel.resolve())
            လုပ်ငန်းစဉ် = subprocess.Popen(လုပ်ဆောင်အချက်များ + ['-display','none','-monitor','none','-serial','stdio'] + တံတားတန်ဖိုး.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    ဒေတာ = လုပ်ငန်းစဉ်.stdout.read(4096)
                    if not ဒေတာ: break
                    မှတ်တမ်းမှတ်တမ်းတစ်ခု.extend(ဒေတာ)
            အလုပ်ကြိုးတန်ဖိုး = threading.Thread(target=수집, daemon=True)
            အလုပ်ကြိုးတန်ဖိုး.start()
            def အခြေအနေစောင့်(စကားလုံးစာသား, အစဦးအချက်အလက်တစ်ခု=0, ကန့်သတ်ချက်တန်ဖိုး=60):
                အဆုံး = time.monotonic() + ကန့်သတ်ချက်တန်ဖိုး
                while စကားလုံးစာသား not in မှတ်တမ်းမှတ်တမ်းတစ်ခု[အစဦးအချက်အလက်တစ်ခု:]:
                    if time.monotonic()>အဆုံး or လုပ်ငန်းစဉ်.poll() is not None:
                        raise AssertionError('Missing '+repr(စကားလုံးစာသား)+'\n'+မှတ်တမ်းမှတ်တမ်းတစ်ခု[အစဦးအချက်အလက်တစ်ခု:].decode('utf-8','replace'))
                    time.sleep(.02)
            အခြေအနေစောင့်(b'jkoros-native> ')
            အကူတန်ဖိုး = Path(ယာယီတန်ဖိုး)/'askpass'
            အကူတန်ဖိုး.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            အကူတန်ဖိုး.chmod(0o700)
            ဝန်းကျင် = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(အကူတန်ဖိုး), SSH_ASKPASS_REQUIRE='force')
            def 보안셸(စကားဝှက်တန်ဖိုး, စက်ညွှန်ကြားချက်တန်ဖိုး, အချက်နောက်တွဲ=()):
                ဝန်းကျင်['JKOROS_TEST_PASSWORD']=စကားဝှက်တန်ဖိုး
                အချက်များ=['ssh','-v']+list(အချက်နောက်တွဲ)+['-p',str(အမိန့်ဝင်းဆက်သွယ်ပေါက်),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(ယာယီတန်ဖိုး)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',စက်ညွှန်ကြားချက်တန်ဖိုး]
                ရလဒ်=subprocess.run(အချက်များ,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=ဝန်းကျင်,start_new_session=True,timeout=50)
                return ရလဒ်
            ရလဒ်=보안셸('!' + သတ်မှတ်ချက်['ssh_password'], 'echo SHOULD_NOT_RUN')
            (အထွက်/'ssh-rejected.log').write_bytes(ရလဒ်.stderr)
            assert ရလဒ်.returncode!=0 and b'Permission denied' in ရလဒ်.stderr and b'SHOULD_NOT_RUN' not in မှတ်တမ်းမှတ်တမ်းတစ်ခု, ရလဒ်.stderr
            အစီရင်ခံစာတန်ဖိုး['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            ရလဒ်=보안셸(သတ်မှတ်ချက်['ssh_password'], 'echo SSH_NATIVE_PASS')
            (အထွက်/'ssh.log').write_bytes(ရလဒ်.stderr)
            (အထွက်/'ssh-output.txt').write_bytes(ရလဒ်.stdout)
            assert ရလဒ်.returncode==0 and b'SSH_NATIVE_PASS' in ရလဒ်.stdout, (ရလဒ်.returncode,ရလဒ်.stdout,ရလဒ်.stderr)
            အစီရင်ခံစာတန်ဖိုး['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in ရလဒ်.stderr, ရလဒ်.stderr
            အစီရင်ခံစာတန်ဖိုး['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            ရလဒ်=보안셸(သတ်မှတ်ချက်['ssh_password'], 'cd /example/java; java ထုတ်ဥပမာ; cd /')
            assert ရလဒ်.returncode==0 and 'JAVA အထွက်: 안녕하세요 😀'.encode() in ရလဒ်.stdout,ရလဒ်.stdout
            အစီရင်ခံစာတန်ဖိုး['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            ရလဒ်=보안셸(သတ်မှတ်ချက်['ssh_password'], 'missing_remote_command')
            assert ရလဒ်.returncode==127,ရလဒ်.returncode
            အစီရင်ခံစာတန်ဖိုး['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            ရလဒ်=보안셸(သတ်မှတ်ချက်['ssh_password'], 'cat /example/java/ဝင်းဥပမာ.java', ('-o', 'RekeyLimit=1K'))
            (အထွက်/'ssh-rekey.log').write_bytes(ရလဒ်.stderr)
            assert ရလဒ်.returncode==0 and 'class ဝင်းဥပမာ'.encode() in ရလဒ်.stdout, (ရလဒ်.returncode,ရလဒ်.stdout,ရလဒ်.stderr)
            assert ရလဒ်.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, ရလဒ်.stderr
            အစီရင်ခံစာတန်ဖိုး['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            အပြန်အလှန်ပေးအချက်များ=['ssh','-tt','-p',str(အမိန့်ဝင်းဆက်သွယ်ပေါက်),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(ယာယီတန်ဖိုး)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            အပြန်အလှန်အသုံးပြုချိန်ပိုင်း=subprocess.Popen(အပြန်အလှန်ပေးအချက်များ,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=ဝန်းကျင်,start_new_session=True,bufsize=0)
            대화기록=bytearray();ရွေးချယ်မှုတန်ဖိုး=selectors.DefaultSelector();ရွေးချယ်မှုတန်ဖိုး.register(အပြန်အလှန်အသုံးပြုချိန်ပိုင်း.stdout,selectors.EVENT_READ)
            def အပြန်အလှန်ဖတ်(တန်ဖိုးပြသ):
                마감=time.monotonic()+30
                while တန်ဖိုးပြသ not in 대화기록:
                    if time.monotonic()>마감 or အပြန်အလှန်အသုံးပြုချိန်ပိုင်း.poll() is not None:raise AssertionError('SSH interactive missing '+repr(တန်ဖိုးပြသ)+' '+repr(bytes(대화기록)))
                    for အချက်တန်ဖိုး,_ in ရွေးချယ်မှုတန်ဖိုး.select(.1):
                        အစိတ်အပိုင်း=အချက်တန်ဖိုး.fileobj.read(4096)
                        if အစိတ်အပိုင်း:대화기록.extend(အစိတ်အပိုင်း)
            try:
                အပြန်အလှန်ဖတ်(b'shared native console')
                အပြန်အလှန်အသုံးပြုချိန်ပိုင်း.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');အပြန်အလှန်အသုံးပြုချိန်ပိုင်း.stdin.flush();အပြန်အလှန်ဖတ်(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                အပြန်အလှန်အသုံးပြုချိန်ပိုင်း.stdin.write(b'\x04');အပြန်အလှန်အသုံးပြုချိန်ပိုင်း.stdin.flush();나머지,အမှား=အပြန်အလှန်အသုံးပြုချိန်ပိုင်း.communicate(timeout=15)
                assert အပြန်အလှန်အသုံးပြုချိန်ပိုင်း.returncode==0 and b'PTY allocation request failed' not in အမှား,(အပြန်အလှန်အသုံးပြုချိန်ပိုင်း.returncode,အမှား)
                (အထွက်/'ssh-interactive.txt').write_bytes(대화기록+나머지)
            finally:
                ရွေးချယ်မှုတန်ဖိုး.close()
                if အပြန်အလှန်အသုံးပြုချိန်ပိုင်း.poll() is None:အပြန်အလှန်အသုံးပြုချိန်ပိုင်း.kill();အပြန်အလှန်အသုံးပြုချိန်ပိုင်း.wait()
            အစီရင်ခံစာတန်ဖိုး['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(ချိတ်ဆက်, ကိန်းတန်ဖိုး):
                ဒေတာ=bytearray()
                while len(ဒေတာ)<ကိန်းတန်ဖိုး:
                    ဒေတာတုံး=ချိတ်ဆက်.recv(ကိန်းတန်ဖိုး-len(ဒေတာ))
                    if not ဒေတာတုံး: raise AssertionError('RFB EOF')
                    ဒေတာ.extend(ဒေတာတုံး)
                return bytes(ဒေတာ)
            def 화면인증(စကားဝှက်တန်ဖိုး):
                ချိတ်ဆက်=socket.create_connection(('127.0.0.5',မျက်နှာပြင်ဆက်သွယ်ပေါက်),10);ချိတ်ဆက်.settimeout(30)
                assert 정확히(ချိတ်ဆက်,12)==b'RFB 003.008\n'
                ချိတ်ဆက်.sendall(b'RFB 003.008\n');assert 정확히(ချိတ်ဆက်,2)==b'\x01\x02'
                ချိတ်ဆက်.sendall(b'\x02');도전=정확히(ချိတ်ဆက်,16)
                အဝင်စကားဝှက်=စကားဝှက်တန်ဖိုး.encode('ascii')[:8].ljust(8, b'\0')
                အဓိကသော့=bytes(int('{:08b}'.format(ကိန်းတန်ဖိုး)[::-1],2) for ကိန်းတန်ဖိုး in အဝင်စကားဝှက်)
                ချိတ်ဆက်.sendall(DES.new(အဓိကသော့,DES.MODE_ECB).encrypt(도전))
                အခြေအနေတန်ဖိုး=struct.unpack('!I',정확히(ချိတ်ဆက်,4))[0]
                return ချိတ်ဆက်,အခြေအနေတန်ဖိုး
            မမှန်ကန်စကားဝှက်='!' if not သတ်မှတ်ချက်['vnc_password'].startswith('!') else '?'
            ချိတ်ဆက်,အခြေအနေတန်ဖိုး=화면인증(မမှန်ကန်စကားဝှက်);assert အခြေအနေတန်ဖိုး==1;ချိတ်ဆက်.close();time.sleep(.6)
            အစီရင်ခံစာတန်ဖိုး['checks'].append('VNC incorrect password rejected')
            ချိတ်ဆက်,အခြေအနေတန်ဖိုး=화면인증(သတ်မှတ်ချက်['vnc_password']);assert အခြေအနေတန်ဖိုး==0
            with ချိတ်ဆက်:
                ချိတ်ဆက်.sendall(b'\x01');အစဦးအခြေအနေ=정확히(ချိတ်ဆက်,24);အနံတန်ဖိုး,အမြင့်တန်ဖိုး=struct.unpack('!HH',အစဦးအခြေအနေ[:4]);အမည်=정확히(ချိတ်ဆက်,struct.unpack('!I',အစဦးအခြေအနေ[20:24])[0])
                assert (အနံတန်ဖိုး,အမြင့်တန်ဖိုး)==(640,480) and b'jkoros native'==အမည်
                def မျက်နှာပြင်(တိုးဆင့်=0):
                    ချိတ်ဆက်.sendall(struct.pack('!BBHHHH',3,တိုးဆင့်,0,0,အနံတန်ဖိုး,အမြင့်တန်ဖိုး));ဦးခေါင်းတန်ဖိုး=정확히(ချိတ်ဆက်,4);ကိန်းတန်ဖိုး=struct.unpack('!H',ဦးခေါင်းတန်ဖိုး[2:])[0];အကုန်စုစုပေါင်းတန်ဖိုး=0
                    ပုံဆွဲမှု=bytearray(အနံတန်ဖိုး*အမြင့်တန်ဖိုး*4)
                    for _ in range(ကိန်းတန်ဖိုး):
                        xတည်နေရာအမှတ်,yတည်နေရာအမှတ်,နယ်ပယ်အနံ,နယ်ပယ်အမြင့်,နည်းလမ်းနည်းစနစ်=struct.unpack('!HHHHi',정확히(ချိတ်ဆက်,12));assert နည်းလမ်းနည်းစနစ်==0 and xတည်နေရာအမှတ်+နယ်ပယ်အနံ<=အနံတန်ဖိုး and yတည်နေရာအမှတ်+နယ်ပယ်အမြင့်<=အမြင့်တန်ဖိုး
                        ပုံမှတ်=정확히(ချိတ်ဆက်,နယ်ပယ်အနံ*နယ်ပယ်အမြင့်*4);အကုန်စုစုပေါင်းတန်ဖိုး+=len(ပုံမှတ်)
                        for စာကြောင်း in range(နယ်ပယ်အမြင့်):ပုံဆွဲမှု[((yတည်နေရာအမှတ်+စာကြောင်း)*အနံတန်ဖိုး+xတည်နေရာအမှတ်)*4:((yတည်နေရာအမှတ်+စာကြောင်း)*အနံတန်ဖိုး+xတည်နေရာအမှတ်+နယ်ပယ်အနံ)*4]=ပုံမှတ်[စာကြောင်း*နယ်ပယ်အနံ*4:(စာကြောင်း+1)*နယ်ပယ်အနံ*4]
                    if not တိုးဆင့်:
                        from PIL import Image
                        Image.frombytes('RGB',(အနံတန်ဖိုး,အမြင့်တန်ဖိုး),bytes(ပုံဆွဲမှု),'raw','BGRX').save(str(အထွက်/'native-vnc.png'))
                    return ကိန်းတန်ဖိုး,အကုန်စုစုပေါင်းတန်ဖိုး
                ကိန်းတန်ဖိုး,အကုန်စုစုပေါင်းတန်ဖိုး=မျက်နှာပြင်();assert ကိန်းတန်ဖိုး>0 and အကုန်စုစုပေါင်းတန်ဖိုး==အနံတန်ဖိုး*အမြင့်တန်ဖိုး*4
                အစီရင်ခံစာတန်ဖိုး['checks'].append('Native framebuffer RFB full update {} bytes'.format(အကုန်စုစုပေါင်းတန်ဖိုး))
                ကိန်းတန်ဖိုး,အကုန်စုစုပေါင်းတန်ဖိုး=မျက်နှာပြင်(1);assert အကုန်စုစုပေါင်းတန်ဖိုး<အနံတန်ဖိုး*အမြင့်တန်ဖိုး*4
                အစီရင်ခံစာတန်ဖိုး['checks'].append('RFB incremental update')
                အစဦးအချက်အလက်တစ်ခု=len(မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                for အက္ခရာတန်ဖိုး in 'echo VNC_NATIVE_PASS\r':
                    သင်္ကေတ=0xff0d if အက္ခရာတန်ဖိုး=='\r' else ord(အက္ခရာတန်ဖိုး)
                    ချိတ်ဆက်.sendall(struct.pack('!BBHI',4,1,0,သင်္ကေတ));ချိတ်ဆက်.sendall(struct.pack('!BBHI',4,0,0,သင်္ကေတ))
                အခြေအနေစောင့်(b'VNC_NATIVE_PASS',အစဦးအချက်အလက်တစ်ခု)
                အစီရင်ခံစာတန်ဖိုး['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def 글쇠(သင်္ကေတ,နှိပ်ထားမှု=1):ချိတ်ဆက်.sendall(struct.pack('!BBHI',4,နှိပ်ထားမှု,0,သင်္ကေတ))
                အစဦးအချက်အလက်တစ်ခု=len(မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                for အက္ခရာတန်ဖိုး in 'echo ':글쇠(ord(အက္ခရာတန်ဖိုး))
                글쇠(0xffc6)
                for အက္ခရာတန်ဖိုး in 'gksrmf':글쇠(ord(အက္ခရာတန်ဖိုး))
                글쇠(0xffc6);글쇠(0xff0d)
                အခြေအနေစောင့်('\r\n한글\r\n'.encode(),အစဦးအချက်အလက်တစ်ခု)
                အစီရင်ခံစာတန်ဖိုး['checks'].append('Native VNC F9 two-set Hangul composition')
                ချိတ်ဆက်.sendall(struct.pack('!BBHH',5,0,120,100))
                အစီရင်ခံစာတန်ဖိုး['checks'].append('VNC pointer input accepted')
            လုပ်ငန်းစဉ်.stdin.write(b'poweroff\n');လုပ်ငန်းစဉ်.stdin.flush();လုပ်ငန်းစဉ်.wait(timeout=15);assert လုပ်ငန်းစဉ်.returncode==0
            အစီရင်ခံစာတန်ဖိုး['passed']=True
    finally:
        if လုပ်ငန်းစဉ် and လုပ်ငန်းစဉ်.poll() is None:
            လုပ်ငန်းစဉ်.terminate()
            try: လုပ်ငန်းစဉ်.wait(timeout=5)
            except subprocess.TimeoutExpired: လုပ်ငန်းစဉ်.kill();လုပ်ငန်းစဉ်.wait()
        (အထွက်/'serial.log').write_bytes(မှတ်တမ်းမှတ်တမ်းတစ်ခု)
        (အထွက်/'report.json').write_text(json.dumps(အစီရင်ခံစာတန်ဖိုး,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(အစီရင်ခံစာတန်ဖိုး,ensure_ascii=False,indent=2))


if __name__=='__main__': လုပ်ဆောင်()
