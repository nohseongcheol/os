#!/usr/bin/env python3
"""Run all examples in the real combined VNC + SLIP/FTP native VM."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from အလုပ်မျက်နှာပြင်ရှုမြင်ရာ import 정확한값
from ပြန်ပို့စက်ဥပမာ import 되돌림서버
from စက်မောင်း import စီမံကိန်းအမြစ်


def ဘာသာစကားစမ်းသပ်(ဘာသာစကား,ပြန်ပို့ဝန်ဆောင်စက်အချက်,ရလဒ်ဒေတာ):
    with socket.socket() as ယာယီ:
        ယာယီ.bind(('127.0.0.1',0));ဖိုင်လွှဲပြောင်းဆက်သွယ်ပေါက်ကိန်း=ယာယီ.getsockname()[1]
    실행과정=subprocess.Popen(['python3',str(စီမံကိန်းအမြစ်/'ကိရိယာစု/စက်မောင်း.py'),'--desktop','--network','--port','0','--ftp-port',str(ဖိုင်လွှဲပြောင်းဆက်သွယ်ပေါက်ကိန်း)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비선택기=selectors.DefaultSelector();준비선택기.register(실행과정.stdout,selectors.EVENT_READ)
    대화기록=bytearray();လက်ခံစက်=None;ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု=None
    def စာပို့ချက်လက်ခံရယူ(확인표시,လုပ်ဆောင်=0):
        အဆုံးအရွေ့=time.monotonic()+60
        while 확인표시 not in 대화기록[လုပ်ဆောင်:]:
            if time.monotonic()>အဆုံးအရွေ့ or 실행과정.poll() is not None:raise AssertionError(대화기록[လုပ်ဆောင်:].decode('utf-8','replace'))
            for 누름값,_ in 준비선택기.select(.1):
                ဒေတာ=누름값.fileobj.read(65536)
                if ဒေတာ:대화기록.extend(ဒေတာ)
        return 대화기록[လုပ်ဆောင်:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(သင်္ကေတတန်ဖိုး,누르는중=True):လက်ခံစက်.sendall(struct.pack('>BBHI',4,int(누르는중),0,သင်္ကေတတန်ဖိုး))
    def အရွေ့စတင်(စာကြောင်း):
        လုပ်ဆောင်=len(대화기록)
        for အက္ခရာကုဒ် in စာကြောင်း+'\n':
            သင်္ကေတတန်ဖိုး=0xff0d if အက္ခရာကုဒ်=='\n' else ord(အက္ခရာကုဒ်) if ord(အက္ခရာကုဒ်)<256 else 0x1000000|ord(အက္ခရာကုဒ်)
            누름값(သင်္ကေတတန်ဖိုး);누름값(သင်္ကေတတန်ဖိုး,False)
        return လုပ်ဆောင်
    def အမိန့်ဝင်း(စာကြောင်း):return စာပို့ချက်လက်ခံရယူ(b'jkoros-native> ',အရွေ့စတင်(စာကြောင်း))
    def စက်မောင်း(စာကြောင်း,예상결과):
        စာသား=အမိန့်ဝင်း(စာကြောင်း);assert 예상결과 in စာသား and 'exit 0' in စာသား,(စာကြောင်း,စာသား)
        return စာသား
    def 화소들():
        လက်ခံစက်.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            분류=정확한값(လက်ခံစက်,1)[0]
            if 분류==2:continue
            if 분류==3:
                အရေအတွက်=struct.unpack('>I',정확한값(လက်ခံစက်,7)[3:])[0];정확한값(လက်ခံစက်,အရေအတွက်);continue
            assert 분류==0,분류
            အချက်အရေအတွက်=struct.unpack('>H',정확한값(လက်ခံစက်,3)[1:])[0]
            for _ in range(အချက်အရေအတွက်):
                xတည်နေရာအမှတ်,yတည်နေရာအမှတ်,너비값,높이값,အက္ခရာကုဒ်စနစ်=struct.unpack('>HHHHi',정확한값(လက်ခံစက်,12));assert အက္ခရာကုဒ်စနစ်==0,အက္ခရာကုဒ်စနစ်
                ဒေတာ=정확한값(လက်ခံစက်,너비값*높이값*4)
                for အတန်းလိုက်နေရာ in range(높이값):
                    for ကော်လံနေရာ in range(너비값):
                        မူရင်းဒေတာ=(အတန်းလိုက်နေရာ*너비값+ကော်လံနေရာ)*4;ဦးတည်ချက်တန်ဖိုး=((yတည်နေရာအမှတ်+အတန်းလိုက်နေရာ)*640+xတည်နေရာအမှတ်+ကော်လံနေရာ)*3
                        빛삼원색[ဦးတည်ချက်တန်ဖိုး:ဦးတည်ချက်တန်ဖိုး+3]=bytes((ဒေတာ[မူရင်းဒေတာ+2],ဒေတာ[မူရင်းဒေတာ+1],ဒေတာ[မူရင်းဒေတာ]))
            if အချက်အရေအတွက်:return 빛삼원색
    try:
        စာပို့ချက်လက်ခံရယူ(b'TERMINAL READY');စာပို့ချက်လက်ခံရယူ(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        ဆက်သွယ်ပေါက်ကိန်း=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        လက်ခံစက်=socket.create_connection(('127.0.0.1',ဆက်သွယ်ပေါက်ကိန်း),timeout=10)
        assert 정확한값(လက်ခံစက်,12)==b'RFB 003.008\n';လက်ခံစက်.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(လက်ခံစက်,정확한값(လက်ခံစက်,1)[0]);လက်ခံစက်.sendall(b'\x01');assert 정확한값(လက်ခံစက်,4)==b'\0'*4
        လက်ခံစက်.sendall(b'\x01');အစဦးတန်ဖိုး=정확한값(လက်ခံစက်,24);정확한값(လက်ခံစက်,struct.unpack('>I',အစဦးတန်ဖိုး[20:])[0])
        လက်ခံစက်.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        လက်ခံစက်.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in အမိန့်ဝင်း('ftpd start')
        ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု=ftplib.FTP();ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.encoding='utf-8';ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.connect('127.0.0.1',ဖိုင်လွှဲပြောင်းဆက်သွယ်ပေါက်ကိန်း,timeout=20);ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.login()
        내용자료=('GUI와 FTP 동시 သုံးစွဲမှု '+ဘာသာစကား+' 😀\n').encode()
        ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR 함께.txt',io.BytesIO(내용자료))
        assert 내용자료.decode().strip() in အမိန့်ဝင်း('cat /함께.txt')
        ရရှိအရေအတွက်=bytearray();ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.retrbinary('RETR 함께.txt',ရရှိအရေအတွက်.extend);assert ရရှိအရေအတွက်==내용자료;ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        စာရင်းပို့=အမိန့်ဝင်း('ls /example')
        assert all(အမည် in စာရင်းပို့ for အမည် in ('java/','c/','python/','README.md')),စာရင်းပို့
        if ဘာသာစကား=='java':
            꾸러미명세=json.loads((စီမံကိန်းအမြစ်/'build/examples/manifest.json').read_text())
            for လမ်း,အချက်အမှတ်တစ်ခု in 꾸러미명세.items():
                အမိန့်ဝင်း('cp '+လမ်း+' /example-check.bin')
                အကြောင်းအရာတန်ဖိုး=bytearray();ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.retrbinary('RETR example-check.bin',အကြောင်းအရာတန်ဖိုး.extend)
                assert len(အကြောင်းအရာတန်ဖိုး)==အချက်အမှတ်တစ်ခု['bytes'] and hashlib.sha256(အကြောင်းအရာတန်ဖိုး).hexdigest()==အချက်အမှတ်တစ်ခု['sha256'],လမ်း
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ဒွိစနစ်=bytes(range(256))*64
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR boundary.bin',io.BytesIO(ဒွိစနစ်))
            အကြောင်းအရာတန်ဖိုး=bytearray();ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.retrbinary('RETR boundary.bin',အကြောင်းအရာတန်ဖိုး.extend)
            assert အကြောင်းအရာတန်ဖိုး==ဒွိစနစ် and 'boundary.bin' in ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.nlst()
            အမိန့်ဝင်း('cp /boundary.bin /boundary-copy.bin')
            အကြောင်းအရာတန်ဖိုး=bytearray();ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.retrbinary('RETR boundary-copy.bin',အကြောင်းအရာတန်ဖိုး.extend)
            assert အကြောင်းအရာတန်ဖိုး==ဒွိစနစ်
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.delete('boundary.bin');ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.delete('boundary-copy.bin')
        assert 'ထုတ်ဥပမာ' in အမိန့်ဝင်း('ls /example/'+ဘာသာစကား)
        အမိန့်ဝင်း('cd /example/'+ဘာသာစကား)
        အမည်ဇယား={'java':'JAVA','c':'C','python':'PYTHON'}[ဘာသာစကား]
        예상파일=အမည်ဇယား+' ဖိုင်: 한글 ဒေတာ 😀\n'
        if ဘာသာစကား=='java':
            စက်မောင်း('javac ထုတ်ဥပမာ.java','Compiled:');စက်မောင်း('java ထုတ်ဥပမာ','JAVA အထွက်: 안녕하세요 😀')
            စက်မောင်း('javac ဖိုင်ဥပမာ.java','Compiled:');စက်မောင်း('java ဖိုင်ဥပမာ',예상파일)
            စက်မောင်း('java ကွန်ရက်ဥပမာ {} {}'.format(ပြန်ပို့ဝန်ဆောင်စက်အချက်.TCPဆက်သွယ်ပေါက်,ပြန်ပို့ဝန်ဆောင်စက်အချက်.UDPဆက်သွယ်ပေါက်),'JAVA ကွန်ရက်ဆက် အတည်ပြု: TCP UDP 한글')
            ရုပ်ပုံအမိန့်='java ပုံဆွဲဥပမာ'
        elif ဘာသာစကား=='c':
            for အမည်,전달값,예상결과 in [('အထွက်','', 'C အထွက်: 안녕하세요 😀'),('ဖိုင်','',예상파일),
                    ('ကွန်ရက်ဆက်',' '+str(ပြန်ပို့ဝန်ဆောင်စက်အချက်.UDPဆက်သွယ်ပေါက်),'C ကွန်ရက်ဆက် အတည်ပြု: UDP 한글')]:
                စက်မောင်း('cc '+အမည်+'ဥပမာ.c -o စက်မောင်း','Compiled native ARM64 ELF:')
                စက်မောင်း('./စက်မောင်း'+전달값,예상결과)
            စက်မောင်း('cc ပုံဆွဲဥပမာ.c -o စက်မောင်း','Compiled native ARM64 ELF:');ရုပ်ပုံအမိန့်='./စက်မောင်း'
        else:
            for အမည်,전달값,예상결과 in [('အထွက်','','PYTHON အထွက်: 안녕하세요 😀'),('ဖိုင်','',예상파일),
                    ('ကွန်ရက်ဆက်',' '+str(ပြန်ပို့ဝန်ဆောင်စက်အချက်.UDPဆက်သွယ်ပေါက်),'PYTHON ကွန်ရက်ဆက် အတည်ပြု: UDP 한글')]:
                စက်မောင်း('python '+အမည်+'ဥပမာ.py'+전달값,예상결과)
            ရုပ်ပုံအမိန့်='python ပုံဆွဲဥပမာ.py'
        ပုံရေးဆွဲမှုစတင်=အရွေ့စတင်(ရုပ်ပုံအမိန့်)
        စာသား=စာပို့ချက်လက်ခံရယူ('그림을 확인한 နောက်တန်ဖိုး Enter를 누르세요.\r\n'.encode(),ပုံရေးဆွဲမှုစတင်)
        assert အမည်ဇယား+' 그래픽: 빨강 초록 파랑' in စာသား and 'exit 0' not in စာသား,စာသား
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        ရရှိအရေအတွက်=bytearray();ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.retrbinary('RETR 도중.txt',ရရှိအရေအတွက်.extend);assert ရရှိအရေအတွက်==b'FTP DURING GRAPHICS';ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.delete('도중.txt')
        빛삼원색=화소들()
        for yတည်နေရာအမှတ်,ပုံမှတ်အရောင် in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            အရွေ့တန်ဖိုး=(yတည်နေရာအမှတ်*640+610)*3;assert tuple(빛삼원색[အရွေ့တန်ဖိုး:အရွေ့တန်ဖိုး+3])==ပုံမှတ်အရောင်,(ဘာသာစကား,yတည်နေရာအမှတ်,tuple(빛삼원색[အရွေ့တန်ဖိုး:အရွေ့တန်ဖိုး+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(ရလဒ်ဒေတာ/(ဘာသာစကား+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in စာပို့ချက်လက်ခံရယူ(b'jkoros-native> ',ပုံရေးဆွဲမှုစတင်)
        if ဘာသာစကား=='java':
            ဝင်းစတင်=အရွေ့စတင်('java ဝင်းဥပမာ')
            စာပို့ချက်လက်ခံရယူ('GUI ဥပမာ ပြင်ဆင်: ဝင်းဥပမာ'.encode(),ဝင်းစတင်)
            def 클릭(အလျားတည်နေရာ,ဒေါင်လိုက်တည်နေရာ):
                for ခလုတ် in (1,0):လက်ခံစက်.sendall(struct.pack('>BBHH',5,ခလုတ်,အလျားတည်နေရာ,ဒေါင်လိုက်တည်နေရာ))
            time.sleep(.3)
            ယခင်စက်ပုံရိပ်=Image.frombytes('RGB',(640,480),bytes(화소들()))
            클릭(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for အက္ခရာတန်ဖိုး in '한글':누름값(0x1000000|ord(အက္ခရာတန်ဖိုး));누름값(0x1000000|ord(အက္ခရာတန်ဖိုး),False)
            for အကြိမ်အရေအတွက် in (1,2):
                လုပ်ဆောင်=len(대화기록);클릭(180,242)
                စာပို့ချက်လက်ခံရယူ(('GUI နှုတ်ဆက်: 안녕하세요, 한글님! ('+str(အကြိမ်အရေအတွက်)+')').encode(),လုပ်ဆောင်)
            time.sleep(.3)
            ဝင်းပုံရေးဆွဲမှု=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert ယခင်စက်ပုံရိပ်.crop((110,272,530,300)).tobytes()!=ဝင်းပုံရေးဆွဲမှု.crop((110,272,530,300)).tobytes()
            ဝင်းပုံရေးဆွဲမှု.save(str(ရလဒ်ဒေတာ/'java-swing.png'))
            လုပ်ဆောင်=len(대화기록);클릭(535,105)
            assert 'exit 0' in စာပို့ချက်လက်ခံရယူ(b'jkoros-native> ',လုပ်ဆောင်)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ဖိုင်အချက်အမည်={'java':'java.txt','c':'c.txt','python':'python.txt'}[ဘာသာစကား]
        အမိန့်ဝင်း('cp '+ဖိုင်အချက်အမည်+' /မှန်ကန်ကြောင်းစစ်.txt')
        ရရှိအရေအတွက်=bytearray();ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.retrbinary('RETR မှန်ကန်ကြောင်းစစ်.txt',ရရှိအရေအတွက်.extend);assert ရရှိအရေအတွက်==예상파일.encode()
        အမိန့်ဝင်း('echo preserved > ထုတ်ဥပမာ.'+('py' if ဘာသာစကား=='python' else ဘာသာစကား))
        assert 'EXAMPLES READY' in အမိန့်ဝင်း('example '+ဘာသာစကား)
        assert '\npreserved\n' in အမိန့်ဝင်း('cat ထုတ်ဥပမာ.'+('py' if ဘာသာစကား=='python' else ဘာသာစကား))
        assert '한/သုညတွက်ချက်ခံ သော့တန်ဖိုး, Shift+Space 또는 F9' in အမိန့်ဝင်း('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in အမိန့်ဝင်း('echo GUI NETWORK TOGETHER')
        ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.quit();ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု=None;assert 'FTP stopped' in အမိန့်ဝင်း('ftpd stop')
        print('PASS '+ဘာသာစကား+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု:
            try:ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.close()
            except OSError:pass
        if လက်ခံစက်:လက်ခံစက်.close()
        실행과정.terminate()
        try:실행과정.wait(timeout=8)
        except subprocess.TimeoutExpired:실행과정.kill();실행과정.wait()
        준비선택기.close();실행과정.stdout.close();(ရလဒ်ဒေတာ/(ဘာသာစကား+'-serial.log')).write_bytes(대화기록)


def လုပ်ဆောင်():
    ရလဒ်ဒေတာ=စီမံကိန်းအမြစ်/'build/verification/examples';ရလဒ်ဒေတာ.mkdir(parents=True,exist_ok=True)
    검증기록={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((စီမံကိန်းအမြစ်/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as ပြန်ပို့ဝန်ဆောင်စက်အချက်:
            for ဘာသာစကား in ('java','c','python'):
                ဘာသာစကားစမ်းသပ်(ဘာသာစကား,ပြန်ပို့ဝန်ဆောင်စက်အချက်,ရလဒ်ဒေတာ);검증기록['languages'].append(ဘာသာစကား)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert ပြန်ပို့ဝန်ဆောင်စက်အချက်.수신됨==[(분류,ဒေတာ.encode()) for 분류,ဒေတာ in 예상결과],ပြန်ပို့ဝန်ဆောင်စက်အချက်.수신됨
            검증기록['host_network_payloads']=[{'protocol':분류,'text':ဒေတာ.decode()} for 분류,ဒေတာ in ပြန်ပို့ဝန်ဆောင်စက်အချက်.수신됨]
        검증기록.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(ရလဒ်ဒေတာ/'report.json').write_text(json.dumps(검증기록,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':လုပ်ဆောင်()
