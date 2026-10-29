#!/usr/bin/env python3
"""वास्तविक_डेटा QEMU/VNC에서 आदेशपटल 모서리 खींचे_मान·सूचक·동적 कैरेक्टर_मान 칸·संपादन_मान सामग्री_मान 보존를 검사한다."""
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
from PIL import Image
from डेस्कटॉप_दृश्य import 정확한값
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल


def 창크기시험(너비, 높이, परिणाम_पथ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); पोर्ट_संख्या = 임시.getsockname()[1]
    आकार_पाठ = '{}x{}'.format(너비, 높이)
    प्रक्रिया_मान = subprocess.Popen(['python3', str(प्रोजेक्ट_करें_मूल/'उपकरण/निष्पादित_करें_आदेश.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(पोर्ट_संख्या), '--resolution', आकार_पाठ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    सिलेक्टर_a916db4e = selectors.DefaultSelector(); सिलेक्टर_a916db4e.register(प्रक्रिया_मान.stdout, selectors.EVENT_READ)
    लॉग_रिकॉर्ड = bytearray(); दूरस्थ_मान = None; हस्तांतरण_मान = None; सूचक_छुपा_हुआ=[False]

    def 기다리기(शो_मान, चलाएँ=0):
        अंति_म_समय_सीमा_मान = time.monotonic() + 60
        while शो_मान not in लॉग_रिकॉर्ड[चलाएँ:]:
            if time.monotonic() > अंति_म_समय_सीमा_मान or प्रक्रिया_मान.poll() is not None or b'HALTED' in लॉग_रिकॉर्ड or b'PANIC:' in लॉग_रिकॉर्ड:
                raise AssertionError(लॉग_रिकॉर्ड[चलाएँ:].decode('utf-8', 'replace'))
            for घटना, _ in सिलेक्टर_a916db4e.select(.1):
                आँकड़े = घटना.fileobj.read(65536)
                if आँकड़े: लॉग_रिकॉर्ड.extend(आँकड़े)
        return लॉग_रिकॉर्ड[चलाएँ:].decode('utf-8', 'replace')

    def क्लिक_करना_बटन(प्रतीक, 눌림=True): दूरस्थ_मान.sendall(struct.pack('>BBHI', 4, int(눌림), 0, प्रतीक))

    def SMS_भेजें(पाठ):
        चलाएँ = len(लॉग_रिकॉर्ड)
        for कैरेक्टर_मान in पाठ:
            प्रतीक = 0xff0d if कैरेक्टर_मान == '\n' else ord(कैरेक्टर_मान) if ord(कैरेक्टर_मान) < 256 else 0x1000000 | ord(कैरेक्टर_मान)
            क्लिक_करना_बटन(प्रतीक); क्लिक_करना_बटन(प्रतीक, False)
        return चलाएँ

    def शेल(पाठ): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_भेजें(पाठ+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, अनुलंब_पद, 눌림): दूरस्थ_मान.sendall(struct.pack('>BBHH', 5, 눌림, 가로, अनुलंब_पद))

    def क्लिक_करना_मान(가로, अनुलंब_पद): 가리키기(가로, अनुलंब_पद, 1); 가리키기(가로, अनुलंब_पद, 0)

    def बिटमैप_छवि():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 वास्तविक_डेटा 너비를 쓴다.
        दूरस्थ_मान.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ड्रॉइंग_मान = Image.new('RGB', (너비, 높이)); क्षेत्र_मान_9285603e = 0
        while True:
            종류 = 정확한값(दूरस्थ_मान, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', 정확한값(दूरस्थ_मान, 7)[3:])[0]; 정확한값(दूरस्थ_मान, 길이); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(दूरस्थ_मान, 3)[1:])[0]
            for _ in range(개수):
                가로, अनुलंब_पद, 폭, 길이, एन्कोडिंग_मान = struct.unpack('>HHHHi', 정확한값(दूरस्थ_मान, 12))
                if एन्कोडिंग_मान == -239:
                    assert 폭==0 and 길이==0, 'remote cursor must be hidden'
                    सूचक_छुपा_हुआ[0]=True
                    continue
                assert एन्कोडिंग_मान == 0 and 가로+폭 <= 너비 and अनुलंब_पद+길이 <= 높이
                ड्रॉइंग_मान.paste(Image.frombytes('RGB', (폭, 길이), 정확한값(दूरस्थ_मान, 폭*길이*4), 'raw', 'BGRX'), (가로, अनुलंब_पद))
                क्षेत्र_मान_9285603e += 폭*길이
            if क्षेत्र_मान_9285603e:
                assert क्षेत्र_मान_9285603e == 너비*높이, क्षेत्र_मान_9285603e
                return ड्रॉइंग_मान

    def जाँचें_पिक्सेल(좌표, 색):
        अंति_म_समय_सीमा_मान = time.monotonic()+10
        while True:
            ड्रॉइंग_मान = बिटमैप_छवि()
            if ड्रॉइंग_मान.getpixel(좌표) == 색: return ड्रॉइंग_मान
            if time.monotonic() > अंति_म_समय_सीमा_मान: raise AssertionError((좌표, ड्रॉइंग_मान.getpixel(좌표), 색))

    def अपलोड_फ़ाइलें(नाम, आँकड़े): हस्तांतरण_मान.storbinary('STOR '+नाम, io.BytesIO(आँकड़े))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+आकार_पाठ+' RGB32').encode() in लॉग_रिकॉर्ड
        print('BOOT:', आकार_पाठ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', लॉग_रिकॉर्ड).group(1))
        दूरस्थ_मान = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(दूरस्थ_मान, 12) == b'RFB 003.008\n'; दूरस्थ_मान.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(दूरस्थ_मान, 정확한값(दूरस्थ_मान, 1)[0]); दूरस्थ_मान.sendall(b'\x01')
        assert 정확한값(दूरस्थ_मान, 4) == b'\0'*4; दूरस्थ_मान.sendall(b'\x01')
        प्रारंभिक_स्थिति = 정확한값(दूरस्थ_मान, 24); assert struct.unpack('>HH', प्रारंभिक_स्थिति[:4]) == (너비, 높이)
        정확한값(दूरस्थ_मान, struct.unpack('>I', प्रारंभिक_स्थिति[20:])[0])
        दूरस्थ_मान.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        दूरस्थ_मान.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        जाँचें_पिक्सेल((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for घटना,_ in सिलेक्टर_a916db4e.select(.02):
                    आँकड़े=घटना.fileobj.read(65536)
                    if आँकड़े:लॉग_रिकॉर्ड.extend(आँकड़े)
        खिड़की=[12,48,568,360]
        def सत्यापित_करें_आकार():
            कालम_मान,पंक्ति_मान=(खिड़की[2]-24)//8,(खिड़की[3]-56)//16
            पाठ=शेल('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(कालम_मान,पंक्ति_मान) in पाठ,पाठ
            # वास्तविक_डेटा खिड़की 테두리: 단지 आकार क्वेरी_मान 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            जाँचें_पिक्सेल((खिड़की[0],खिड़की[1]),(32,80,144))
            ड्रॉइंग_मान=जाँचें_पिक्सेल((खिड़की[0]+खिड़की[2]-1,खिड़की[1]+खिड़की[3]-1),(39,49,64))
            return ड्रॉइंग_मान
        def 모서리(방향):
            return (खिड़की[0]+(3 if 방향 in (1,3) else खिड़की[2]-4),खिड़की[1]+(3 if 방향<=2 else खिड़की[3]-4))
        def आकार_बदलें_खींचे(방향,차이,बटन=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            जाँचें_पिक्सेल(흰점,(255,255,255))
            가리키기(가,세,बटन)
            끝가=max(0,min(너비-1,가+차이[0]));समाप्त_करें_अनुलंब=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,समाप्त_करें_अनुलंब,बटन);가리키기(끝가,समाप्त_करें_अनुलंब,0);숨고르기()
            if बटन==1:
                왼,위,폭,길이=खिड़की;오른,아래=왼+폭,위+길이
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+समाप्त_करें_अनुलंब-세))
                else:아래=max(위+216,min(높이,아래+समाप्त_करें_अनुलंब-세))
                खिड़की[:]=[왼,위,오른-왼,아래-위]
        सत्यापित_करें_आकार();assert सूचक_छुपा_हुआ[0]
        आकार_बदलें_खींचे(4,(-100,-60),4);सत्यापित_करें_आकार() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            आकार_बदलें_खींचे(방향,차이);सत्यापित_करें_आकार()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_भेजें("echo '"+긴글+"'");숨고르기()
        आकार_बदलें_खींचे(4,(-1000,-1000));assert खिड़की[2:]==[360,216]
        आकार_बदलें_खींचे(4,(너비,높이))
        चलाएँ=SMS_भेजें('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),चलाएँ);सत्यापित_करें_आकार()
        # vi가 संपादन_मान 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        शेल('ftpd start')
        हस्तांतरण_मान=ftplib.FTP();हस्तांतरण_मान.encoding='utf-8';हस्तांतरण_मान.connect('127.0.0.1',पोर्ट_संख्या,timeout=20);हस्तांतरण_मान.login()
        기다리기(b'NORMAL',SMS_भेजें('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_भेजें('i미저장 한글 आँकड़े\n'));숨고르기()
        आकार_बदलें_खींचे(4,(-너비,-높이))
        # ANSI पंक्ति_मान 이동에 새 पंक्ति_मान 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((खिड़की[3]-56)//16)).encode() in लॉग_रिकॉर्ड[-4096:]
        SMS_भेजें('작은 창에서도 이어 लिखें\n');숨고르기()
        आकार_बदलें_खींचे(4,(너비,높이))
        SMS_भेजें('큰 창에서도 이어 लिखें\n');숨고르기()
        क्लिक_करना_बटन(0xff1b);क्लिक_करना_बटन(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_भेजें(':wq\n'))
        सामग्री_मान=bytearray();हस्तांतरण_मान.retrbinary('RETR 크기자료.txt',सामग्री_मान.extend)
        assert सामग्री_मान=='미저장 한글 आँकड़े\n작은 창에서도 이어 लिखें\n큰 창에서도 이어 लिखें\n'.encode(),सामग्री_मान
        सत्यापित_करें_आकार().save(str(परिणाम_पथ/(आकार_पाठ+'-large.png')))
        # 두 번째 창은 डिफ़ॉल्ट_मान आकार, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        चलाएँ=len(लॉग_रिकॉर्ड);क्लिक_करना_मान(70,16);기다리기(b'TERMINAL FOCUS 2',चलाएँ)
        assert 'TERMINAL SIZE 68x19' in शेल('terminal size')
        चलाएँ=len(लॉग_रिकॉर्ड);क्लिक_करना_मान(180,16);기다리기(b'TERMINAL FOCUS 1',चलाएँ);सत्यापित_करें_आकार()
        आकार_बदलें_खींचे(4,(-너비,-높이));सत्यापित_करें_आकार().save(str(परिणाम_पथ/(आकार_पाठ+'-small.png')))
        # आकार परिवर्तित_करें_मान वापस_मान X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        चलाएँ=len(लॉग_रिकॉर्ड);क्लिक_करना_मान(खिड़की[0]+खिड़की[2]-20,खिड़की[1]+15);기다리기(b'TERMINAL FOCUS 2',चलाएँ)
        assert 'RESIZE CLOSED' in शेल('echo RESIZE CLOSED')
        print('PASS:',आकार_पाठ,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if हस्तांतरण_मान:हस्तांतरण_मान.close()
        if दूरस्थ_मान:दूरस्थ_मान.close()
        if प्रक्रिया_मान.poll() is None:
            प्रक्रिया_मान.terminate()
            try:प्रक्रिया_मान.wait(timeout=8)
            except subprocess.TimeoutExpired:प्रक्रिया_मान.kill();प्रक्रिया_मान.wait()
        सिलेक्टर_a916db4e.close();प्रक्रिया_मान.stdout.close();(परिणाम_पथ/(आकार_पाठ+'.log')).write_bytes(लॉग_रिकॉर्ड)


def चलाएँ():
    परिणाम_पथ=प्रोजेक्ट_करें_मूल/'build/verification/resize';परिणाम_पथ.mkdir(parents=True,exist_ok=True)
    लॉग_रिकॉर्ड={'passed':False,'kernel_sha256':hashlib.sha256((प्रोजेक्ट_करें_मूल/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,परिणाम_पथ);लॉग_रिकॉर्ड['resolutions'].append([너비,높이])
        लॉग_रिकॉर्ड.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(परिणाम_पथ/'report.json').write_text(json.dumps(लॉग_रिकॉर्ड,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':चलाएँ()
