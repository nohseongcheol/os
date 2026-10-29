#!/usr/bin/env python3
"""प्रत्यक्ष_डेटा QEMU/VNC에서 टर्मिनल 모서리 ओडचें_मोल·पॉयंटर·동적 वर्ण_मोल स्लॉट_प्रवेश·संपादन_करचें_मोल अनुक्रमणिका_मोल 보존를 검사한다."""
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
from डॅस्कटॉप_दृश्य import EXACT_मोल
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट


def 창크기시험(너비, 높이, मेजप_पाथ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    आवाठ_SMS = '{}x{}'.format(너비, 높이)
    प्रक्रिया_मोल = subprocess.Popen(['python3', str(प्रॉजॅक्ट_रूट/'साधनां/पाळो_दिवचो_आदेश.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', आवाठ_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    वेंचक_a916db4e = selectors.DefaultSelector(); वेंचक_a916db4e.register(प्रक्रिया_मोल.stdout, selectors.EVENT_READ)
    LOG_नोंद = bytearray(); दुर्मीळ_मोल = None; ट्रान्सफर_मोल = None; पॉयंटर_लिपिल्लें=[False]

    def 기다리기(शो_मोल, चलोवप=0):
        마감 = time.monotonic() + 60
        while शो_मोल not in LOG_नोंद[चलोवप:]:
            if time.monotonic() > 마감 or प्रक्रिया_मोल.poll() is not None or b'HALTED' in LOG_नोंद or b'PANIC:' in LOG_नोंद:
                raise AssertionError(LOG_नोंद[चलोवप:].decode('utf-8', 'replace'))
            for प्रसंग, _ in वेंचक_a916db4e.select(.1):
                डेटा = प्रसंग.fileobj.read(65536)
                if डेटा: LOG_नोंद.extend(डेटा)
        return LOG_नोंद[चलोवप:].decode('utf-8', 'replace')

    def क्लिक_करचें_बटन(चिन्न, 눌림=True): दुर्मीळ_मोल.sendall(struct.pack('>BBHI', 4, int(눌림), 0, चिन्न))

    def SMS_धाडचो(SMS):
        चलोवप = len(LOG_नोंद)
        for वर्ण_मोल in SMS:
            चिन्न = 0xff0d if वर्ण_मोल == '\n' else ord(वर्ण_मोल) if ord(वर्ण_मोल) < 256 else 0x1000000 | ord(वर्ण_मोल)
            क्लिक_करचें_बटन(चिन्न); क्लिक_करचें_बटन(चिन्न, False)
        return चलोवप

    def शॅल(SMS): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_धाडचो(SMS+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, उबें_स्थिती, 눌림): दुर्मीळ_मोल.sendall(struct.pack('>BBHH', 5, 눌림, 가로, उबें_स्थिती))

    def क्लिक_करचें_मोल(가로, उबें_स्थिती): 가리키기(가로, उबें_स्थिती, 1); 가리키기(가로, उबें_स्थिती, 0)

    def बिटमॅप_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 प्रत्यक्ष_डेटा 너비를 쓴다.
        दुर्मीळ_मोल.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        रेखाटन_मोल = Image.new('RGB', (너비, 높이)); वर्ग_मोल_9285603e = 0
        while True:
            종류 = EXACT_मोल(दुर्मीळ_मोल, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                लांबाय_मोल = struct.unpack('>I', EXACT_मोल(दुर्मीळ_मोल, 7)[3:])[0]; EXACT_मोल(दुर्मीळ_मोल, लांबाय_मोल); continue
            assert 종류 == 0, 종류
            आयटम_COUNT = struct.unpack('>H', EXACT_मोल(दुर्मीळ_मोल, 3)[1:])[0]
            for _ in range(आयटम_COUNT):
                가로, उबें_स्थिती, 폭, लांबाय_मोल, एनकोडिंग_मोल = struct.unpack('>HHHHi', EXACT_मोल(दुर्मीळ_मोल, 12))
                if एनकोडिंग_मोल == -239:
                    assert 폭==0 and लांबाय_मोल==0, 'remote cursor must be hidden'
                    पॉयंटर_लिपिल्लें[0]=True
                    continue
                assert एनकोडिंग_मोल == 0 and 가로+폭 <= 너비 and उबें_स्थिती+लांबाय_मोल <= 높이
                रेखाटन_मोल.paste(Image.frombytes('RGB', (폭, लांबाय_मोल), EXACT_मोल(दुर्मीळ_मोल, 폭*लांबाय_मोल*4), 'raw', 'BGRX'), (가로, उबें_स्थिती))
                वर्ग_मोल_9285603e += 폭*लांबाय_मोल
            if वर्ग_मोल_9285603e:
                assert वर्ग_मोल_9285603e == 너비*높이, वर्ग_मोल_9285603e
                return रेखाटन_मोल

    def तपासचें_पिक्सॅल(कोऑर्डिनेट_मोल, 색):
        마감 = time.monotonic()+10
        while True:
            रेखाटन_मोल = बिटमॅप_IMAGE()
            if रेखाटन_मोल.getpixel(कोऑर्डिनेट_मोल) == 색: return रेखाटन_मोल
            if time.monotonic() > 마감: raise AssertionError((कोऑर्डिनेट_मोल, रेखाटन_मोल.getpixel(कोऑर्डिनेट_मोल), 색))

    def अपलोड_करचें_फायली(नांव, डेटा): ट्रान्सफर_मोल.storbinary('STOR '+नांव, io.BytesIO(डेटा))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+आवाठ_SMS+' RGB32').encode() in LOG_नोंद
        print('BOOT:', आवाठ_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_नोंद).group(1))
        दुर्मीळ_मोल = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_मोल(दुर्मीळ_मोल, 12) == b'RFB 003.008\n'; दुर्मीळ_मोल.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_मोल(दुर्मीळ_मोल, EXACT_मोल(दुर्मीळ_मोल, 1)[0]); दुर्मीळ_मोल.sendall(b'\x01')
        assert EXACT_मोल(दुर्मीळ_मोल, 4) == b'\0'*4; दुर्मीळ_मोल.sendall(b'\x01')
        초기 = EXACT_मोल(दुर्मीळ_मोल, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_मोल(दुर्मीळ_मोल, struct.unpack('>I', 초기[20:])[0])
        दुर्मीळ_मोल.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        दुर्मीळ_मोल.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        तपासचें_पिक्सॅल((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for प्रसंग,_ in वेंचक_a916db4e.select(.02):
                    डेटा=प्रसंग.fileobj.read(65536)
                    if डेटा:LOG_नोंद.extend(डेटा)
        विंडो=[12,48,568,360]
        def पुनर्तपासणी_करची_आवाठ():
            स्तंभ_मोल,ROW_मोल=(विंडो[2]-24)//8,(विंडो[3]-56)//16
            SMS=शॅल('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(स्तंभ_मोल,ROW_मोल) in SMS,SMS
            # प्रत्यक्ष_डेटा विंडो 테두리: 단지 आवाठ क्वॅरी_मोल 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            तपासचें_पिक्सॅल((विंडो[0],विंडो[1]),(32,80,144))
            रेखाटन_मोल=तपासचें_पिक्सॅल((विंडो[0]+विंडो[2]-1,विंडो[1]+विंडो[3]-1),(39,49,64))
            return रेखाटन_मोल
        def 모서리(방향):
            return (विंडो[0]+(3 if 방향 in (1,3) else विंडो[2]-4),विंडो[1]+(3 if 방향<=2 else विंडो[3]-4))
        def आकार_परतून_दिवचो_ओडचें(방향,차이,बटन=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            तपासचें_पिक्सॅल(흰점,(255,255,255))
            가리키기(가,세,बटन)
            끝가=max(0,min(너비-1,가+차이[0]));सोपोवचें_उबें=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,सोपोवचें_उबें,बटन);가리키기(끝가,सोपोवचें_उबें,0);숨고르기()
            if बटन==1:
                LEFT_मोल,위,폭,लांबाय_मोल=विंडो;RIGHT_मोल,아래=LEFT_मोल+폭,위+लांबाय_मोल
                if 방향 in (1,3):LEFT_मोल=max(0,min(RIGHT_मोल-360,LEFT_मोल+끝가-가))
                else:RIGHT_मोल=max(LEFT_मोल+360,min(너비,RIGHT_मोल+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+सोपोवचें_उबें-세))
                else:아래=max(위+216,min(높이,아래+सोपोवचें_उबें-세))
                विंडो[:]=[LEFT_मोल,위,RIGHT_मोल-LEFT_मोल,아래-위]
        पुनर्तपासणी_करची_आवाठ();assert पॉयंटर_लिपिल्लें[0]
        आकार_परतून_दिवचो_ओडचें(4,(-100,-60),4);पुनर्तपासणी_करची_आवाठ() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            आकार_परतून_दिवचो_ओडचें(방향,차이);पुनर्तपासणी_करची_आवाठ()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_धाडचो("echo '"+긴글+"'");숨고르기()
        आकार_परतून_दिवचो_ओडचें(4,(-1000,-1000));assert विंडो[2:]==[360,216]
        आकार_परतून_दिवचो_ओडचें(4,(너비,높이))
        चलोवप=SMS_धाडचो('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),चलोवप);पुनर्तपासणी_करची_आवाठ()
        # vi가 संपादन_करचें_मोल 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        शॅल('ftpd start')
        ट्रान्सफर_मोल=ftplib.FTP();ट्रान्सफर_मोल.encoding='utf-8';ट्रान्सफर_मोल.connect('127.0.0.1',접속번호,timeout=20);ट्रान्सफर_मोल.login()
        기다리기(b'NORMAL',SMS_धाडचो('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_धाडचो('i미저장 한글 डेटा\n'));숨고르기()
        आकार_परतून_दिवचो_ओडचें(4,(-너비,-높이))
        # ANSI ROW_मोल 이동에 새 ROW_मोल 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((विंडो[3]-56)//16)).encode() in LOG_नोंद[-4096:]
        SMS_धाडचो('작은 창에서도 이어 बरोवचें\n');숨고르기()
        आकार_परतून_दिवचो_ओडचें(4,(너비,높이))
        SMS_धाडचो('큰 창에서도 이어 बरोवचें\n');숨고르기()
        क्लिक_करचें_बटन(0xff1b);क्लिक_करचें_बटन(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_धाडचो(':wq\n'))
        अनुक्रमणिका_मोल=bytearray();ट्रान्सफर_मोल.retrbinary('RETR 크기자료.txt',अनुक्रमणिका_मोल.extend)
        assert अनुक्रमणिका_मोल=='미저장 한글 डेटा\n작은 창에서도 이어 बरोवचें\n큰 창에서도 이어 बरोवचें\n'.encode(),अनुक्रमणिका_मोल
        पुनर्तपासणी_करची_आवाठ().save(str(मेजप_पाथ/(आवाठ_SMS+'-large.png')))
        # 두 번째 창은 डिफॉल्ट_मोल आवाठ, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        चलोवप=len(LOG_नोंद);क्लिक_करचें_मोल(70,16);기다리기(b'TERMINAL FOCUS 2',चलोवप)
        assert 'TERMINAL SIZE 68x19' in शॅल('terminal size')
        चलोवप=len(LOG_नोंद);क्लिक_करचें_मोल(180,16);기다리기(b'TERMINAL FOCUS 1',चलोवप);पुनर्तपासणी_करची_आवाठ()
        आकार_परतून_दिवचो_ओडचें(4,(-너비,-높이));पुनर्तपासणी_करची_आवाठ().save(str(मेजप_पाथ/(आवाठ_SMS+'-small.png')))
        # आवाठ बदलचें_मोल फाटीं_मोल X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        चलोवप=len(LOG_नोंद);क्लिक_करचें_मोल(विंडो[0]+विंडो[2]-20,विंडो[1]+15);기다리기(b'TERMINAL FOCUS 2',चलोवप)
        assert 'RESIZE CLOSED' in शॅल('echo RESIZE CLOSED')
        print('PASS:',आवाठ_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if ट्रान्सफर_मोल:ट्रान्सफर_मोल.close()
        if दुर्मीळ_मोल:दुर्मीळ_मोल.close()
        if प्रक्रिया_मोल.poll() is None:
            प्रक्रिया_मोल.terminate()
            try:प्रक्रिया_मोल.wait(timeout=8)
            except subprocess.TimeoutExpired:प्रक्रिया_मोल.kill();प्रक्रिया_मोल.wait()
        वेंचक_a916db4e.close();प्रक्रिया_मोल.stdout.close();(मेजप_पाथ/(आवाठ_SMS+'.log')).write_bytes(LOG_नोंद)


def चलोवप():
    मेजप_पाथ=प्रॉजॅक्ट_रूट/'build/verification/resize';मेजप_पाथ.mkdir(parents=True,exist_ok=True)
    LOG_नोंद={'passed':False,'kernel_sha256':hashlib.sha256((प्रॉजॅक्ट_रूट/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,मेजप_पाथ);LOG_नोंद['resolutions'].append([너비,높이])
        LOG_नोंद.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(मेजप_पाथ/'report.json').write_text(json.dumps(LOG_नोंद,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':चलोवप()
