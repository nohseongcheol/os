#!/usr/bin/env python3
"""वास्तविक_लगत QEMU/VNC에서 टर्मिनल 모서리 तान्नुहोस्_मान·पोइन्टर·동적 वर्ण_मान स्लट_प्रविष्टि·सम्पादन_गर्नुहोस्_मान सामग्री_मान 보존를 검사한다."""
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
from डेस्कटप_दृश्य import 정확한값
from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट


def 창크기시험(너비, 높이, मापन_बाटो):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    साइज_पाठ = '{}x{}'.format(너비, 높이)
    प्रक्रिया_मान = subprocess.Popen(['python3', str(परियोजना_रूट/'उपकरणहरू/कार्यान्वयन_गर्नुहोस्_आदेश.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', साइज_पाठ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    चयनकर्ता_a916db4e = selectors.DefaultSelector(); चयनकर्ता_a916db4e.register(प्रक्रिया_मान.stdout, selectors.EVENT_READ)
    लग_रेकर्ड = bytearray(); दूर_मान = None; ट्रान्सफर_मान = None; पोइन्टर_लुकाएको=[False]

    def 기다리기(शो_मान, चलाउनुहोस्=0):
        마감 = time.monotonic() + 60
        while शो_मान not in लग_रेकर्ड[चलाउनुहोस्:]:
            if time.monotonic() > 마감 or प्रक्रिया_मान.poll() is not None or b'HALTED' in लग_रेकर्ड or b'PANIC:' in लग_रेकर्ड:
                raise AssertionError(लग_रेकर्ड[चलाउनुहोस्:].decode('utf-8', 'replace'))
            for घटना, _ in चयनकर्ता_a916db4e.select(.1):
                लगत = घटना.fileobj.read(65536)
                if लगत: लग_रेकर्ड.extend(लगत)
        return लग_रेकर्ड[चलाउनुहोस्:].decode('utf-8', 'replace')

    def क्लिक_गर्नुहोस्_बटन(चिन्ह, 눌림=True): दूर_मान.sendall(struct.pack('>BBHI', 4, int(눌림), 0, चिन्ह))

    def SMS_पठाउनुहोस्(पाठ):
        चलाउनुहोस् = len(लग_रेकर्ड)
        for वर्ण_मान in पाठ:
            चिन्ह = 0xff0d if वर्ण_मान == '\n' else ord(वर्ण_मान) if ord(वर्ण_मान) < 256 else 0x1000000 | ord(वर्ण_मान)
            क्लिक_गर्नुहोस्_बटन(चिन्ह); क्लिक_गर्नुहोस्_बटन(चिन्ह, False)
        return चलाउनुहोस्

    def शेल(पाठ): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_पठाउनुहोस्(पाठ+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, ठाडो_राख्नुहोस्, 눌림): दूर_मान.sendall(struct.pack('>BBHH', 5, 눌림, 가로, ठाडो_राख्नुहोस्))

    def क्लिक_गर्नुहोस्_मान(가로, ठाडो_राख्नुहोस्): 가리키기(가로, ठाडो_राख्नुहोस्, 1); 가리키기(가로, ठाडो_राख्नुहोस्, 0)

    def बिटम्याप_छवि():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 वास्तविक_लगत 너비를 쓴다.
        दूर_मान.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        चित्रकारी_मान = Image.new('RGB', (너비, 높이)); कोटी_मान = 0
        while True:
            종류 = 정확한값(दूर_मान, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                लम्बाइ_मान = struct.unpack('>I', 정확한값(दूर_मान, 7)[3:])[0]; 정확한값(दूर_मान, लम्बाइ_मान); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(दूर_मान, 3)[1:])[0]
            for _ in range(개수):
                가로, ठाडो_राख्नुहोस्, 폭, लम्बाइ_मान, एनकोडिङ_मान = struct.unpack('>HHHHi', 정확한값(दूर_मान, 12))
                if एनकोडिङ_मान == -239:
                    assert 폭==0 and लम्बाइ_मान==0, 'remote cursor must be hidden'
                    पोइन्टर_लुकाएको[0]=True
                    continue
                assert एनकोडिङ_मान == 0 and 가로+폭 <= 너비 and ठाडो_राख्नुहोस्+लम्बाइ_मान <= 높이
                चित्रकारी_मान.paste(Image.frombytes('RGB', (폭, लम्बाइ_मान), 정확한값(दूर_मान, 폭*लम्बाइ_मान*4), 'raw', 'BGRX'), (가로, ठाडो_राख्नुहोस्))
                कोटी_मान += 폭*लम्बाइ_मान
            if कोटी_मान:
                assert कोटी_मान == 너비*높이, कोटी_मान
                return चित्रकारी_मान

    def चेक_पेल(समन्वित_मान, 색):
        마감 = time.monotonic()+10
        while True:
            चित्रकारी_मान = बिटम्याप_छवि()
            if चित्रकारी_मान.getpixel(समन्वित_मान) == 색: return चित्रकारी_मान
            if time.monotonic() > 마감: raise AssertionError((समन्वित_मान, चित्रकारी_मान.getpixel(समन्वित_मान), 색))

    def अपलोड_गर्नुहोस्_फाइलहरू(नाम, लगत): ट्रान्सफर_मान.storbinary('STOR '+नाम, io.BytesIO(लगत))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+साइज_पाठ+' RGB32').encode() in लग_रेकर्ड
        print('BOOT:', साइज_पाठ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', लग_रेकर्ड).group(1))
        दूर_मान = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(दूर_मान, 12) == b'RFB 003.008\n'; दूर_मान.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(दूर_मान, 정확한값(दूर_मान, 1)[0]); दूर_मान.sendall(b'\x01')
        assert 정확한값(दूर_मान, 4) == b'\0'*4; दूर_मान.sendall(b'\x01')
        초기 = 정확한값(दूर_मान, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(दूर_मान, struct.unpack('>I', 초기[20:])[0])
        दूर_मान.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        दूर_मान.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        चेक_पेल((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for घटना,_ in चयनकर्ता_a916db4e.select(.02):
                    लगत=घटना.fileobj.read(65536)
                    if लगत:लग_रेकर्ड.extend(लगत)
        सन्झ्याल=[12,48,568,360]
        def रुजू_गर्नुहोस्_साइज():
            स्तम्भ_मान,रेकर्ड_मान=(सन्झ्याल[2]-24)//8,(सन्झ्याल[3]-56)//16
            पाठ=शेल('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(स्तम्भ_मान,रेकर्ड_मान) in पाठ,पाठ
            # वास्तविक_लगत सन्झ्याल 테두리: 단지 आकार क्वेरी_मान 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            चेक_पेल((सन्झ्याल[0],सन्झ्याल[1]),(32,80,144))
            चित्रकारी_मान=चेक_पेल((सन्झ्याल[0]+सन्झ्याल[2]-1,सन्झ्याल[1]+सन्झ्याल[3]-1),(39,49,64))
            return चित्रकारी_मान
        def 모서리(방향):
            return (सन्झ्याल[0]+(3 if 방향 in (1,3) else सन्झ्याल[2]-4),सन्झ्याल[1]+(3 if 방향<=2 else सन्झ्याल[3]-4))
        def रिसाइज_गर्नुहोस्_तान्नुहोस्(방향,차이,बटन=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            चेक_पेल(흰점,(255,255,255))
            가리키기(가,세,बटन)
            끝가=max(0,min(너비-1,가+차이[0]));समाप्त_गर्नुहोस्_ठाडो=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,समाप्त_गर्नुहोस्_ठाडो,बटन);가리키기(끝가,समाप्त_गर्नुहोस्_ठाडो,0);숨고르기()
            if बटन==1:
                왼,위,폭,लम्बाइ_मान=सन्झ्याल;오른,아래=왼+폭,위+लम्बाइ_मान
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+समाप्त_गर्नुहोस्_ठाडो-세))
                else:아래=max(위+216,min(높이,아래+समाप्त_गर्नुहोस्_ठाडो-세))
                सन्झ्याल[:]=[왼,위,오른-왼,아래-위]
        रुजू_गर्नुहोस्_साइज();assert पोइन्टर_लुकाएको[0]
        रिसाइज_गर्नुहोस्_तान्नुहोस्(4,(-100,-60),4);रुजू_गर्नुहोस्_साइज() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            रिसाइज_गर्नुहोस्_तान्नुहोस्(방향,차이);रुजू_गर्नुहोस्_साइज()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_पठाउनुहोस्("echo '"+긴글+"'");숨고르기()
        रिसाइज_गर्नुहोस्_तान्नुहोस्(4,(-1000,-1000));assert सन्झ्याल[2:]==[360,216]
        रिसाइज_गर्नुहोस्_तान्नुहोस्(4,(너비,높이))
        चलाउनुहोस्=SMS_पठाउनुहोस्('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),चलाउनुहोस्);रुजू_गर्नुहोस्_साइज()
        # vi가 सम्पादन_गर्नुहोस्_मान 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        शेल('ftpd start')
        ट्रान्सफर_मान=ftplib.FTP();ट्रान्सफर_मान.encoding='utf-8';ट्रान्सफर_मान.connect('127.0.0.1',접속번호,timeout=20);ट्रान्सफर_मान.login()
        기다리기(b'NORMAL',SMS_पठाउनुहोस्('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_पठाउनुहोस्('i미저장 한글 लगत\n'));숨고르기()
        रिसाइज_गर्नुहोस्_तान्नुहोस्(4,(-너비,-높이))
        # ANSI रेकर्ड_मान 이동에 새 रेकर्ड_मान 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((सन्झ्याल[3]-56)//16)).encode() in लग_रेकर्ड[-4096:]
        SMS_पठाउनुहोस्('작은 창에서도 이어 लेख्नुहोस्\n');숨고르기()
        रिसाइज_गर्नुहोस्_तान्नुहोस्(4,(너비,높이))
        SMS_पठाउनुहोस्('큰 창에서도 이어 लेख्नुहोस्\n');숨고르기()
        क्लिक_गर्नुहोस्_बटन(0xff1b);क्लिक_गर्नुहोस्_बटन(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_पठाउनुहोस्(':wq\n'))
        सामग्री_मान=bytearray();ट्रान्सफर_मान.retrbinary('RETR 크기자료.txt',सामग्री_मान.extend)
        assert सामग्री_मान=='미저장 한글 लगत\n작은 창에서도 이어 लेख्नुहोस्\n큰 창에서도 이어 लेख्नुहोस्\n'.encode(),सामग्री_मान
        रुजू_गर्नुहोस्_साइज().save(str(मापन_बाटो/(साइज_पाठ+'-large.png')))
        # 두 번째 창은 पूर्वनिर्धारित_मान आकार, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        चलाउनुहोस्=len(लग_रेकर्ड);क्लिक_गर्नुहोस्_मान(70,16);기다리기(b'TERMINAL FOCUS 2',चलाउनुहोस्)
        assert 'TERMINAL SIZE 68x19' in शेल('terminal size')
        चलाउनुहोस्=len(लग_रेकर्ड);क्लिक_गर्नुहोस्_मान(180,16);기다리기(b'TERMINAL FOCUS 1',चलाउनुहोस्);रुजू_गर्नुहोस्_साइज()
        रिसाइज_गर्नुहोस्_तान्नुहोस्(4,(-너비,-높이));रुजू_गर्नुहोस्_साइज().save(str(मापन_बाटो/(साइज_पाठ+'-small.png')))
        # आकार परिवर्तन_मान पछाडि_मान X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        चलाउनुहोस्=len(लग_रेकर्ड);क्लिक_गर्नुहोस्_मान(सन्झ्याल[0]+सन्झ्याल[2]-20,सन्झ्याल[1]+15);기다리기(b'TERMINAL FOCUS 2',चलाउनुहोस्)
        assert 'RESIZE CLOSED' in शेल('echo RESIZE CLOSED')
        print('PASS:',साइज_पाठ,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if ट्रान्सफर_मान:ट्रान्सफर_मान.close()
        if दूर_मान:दूर_मान.close()
        if प्रक्रिया_मान.poll() is None:
            प्रक्रिया_मान.terminate()
            try:प्रक्रिया_मान.wait(timeout=8)
            except subprocess.TimeoutExpired:प्रक्रिया_मान.kill();प्रक्रिया_मान.wait()
        चयनकर्ता_a916db4e.close();प्रक्रिया_मान.stdout.close();(मापन_बाटो/(साइज_पाठ+'.log')).write_bytes(लग_रेकर्ड)


def चलाउनुहोस्():
    मापन_बाटो=परियोजना_रूट/'build/verification/resize';मापन_बाटो.mkdir(parents=True,exist_ok=True)
    लग_रेकर्ड={'passed':False,'kernel_sha256':hashlib.sha256((परियोजना_रूट/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,मापन_बाटो);लग_रेकर्ड['resolutions'].append([너비,높이])
        लग_रेकर्ड.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(मापन_बाटो/'report.json').write_text(json.dumps(लग_रेकर्ड,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':चलाउनुहोस्()
