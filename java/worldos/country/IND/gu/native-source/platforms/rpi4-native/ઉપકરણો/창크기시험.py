#!/usr/bin/env python3
"""વાસ્તવિક_ડેટા QEMU/VNC에서 ટર્મિનલ 모서리 ખેંચો_મૂલ્ય·સૂચક·동적 વર્ણ_મૂલ્ય સ્લૉટ_પ્રવેશ·સંપાદન_મૂલ્ય સામગ્રી_મૂલ્ય 보존를 검사한다."""
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
from ડેસ્કટૉપ_જુઓ import 정확한값
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ


def 창크기시험(너비, 높이, પરિમાણ_પાથ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); પોર્ટ_નંબર = 임시.getsockname()[1]
    આકાર_પાઠ = '{}x{}'.format(너비, 높이)
    પ્રક્રિયા_મૂલ્ય = subprocess.Popen(['python3', str(પ્રોજેક્ટ_રૂટ/'ઉપકરણો/અમલ_કરો_આદેશ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(પોર્ટ_નંબર), '--resolution', આકાર_પાઠ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    પસંદકર્તા_a916db4e = selectors.DefaultSelector(); પસંદકર્તા_a916db4e.register(પ્રક્રિયા_મૂલ્ય.stdout, selectors.EVENT_READ)
    લૉગ_પંક્તિ = bytearray(); રિમોટ_મૂલ્ય = None; સ્થાનાંતર_મૂલ્ય = None; સૂચક_છુપાવેલું=[False]

    def 기다리기(શૉ_મૂલ્ય, ચલાવો_2=0):
        마감 = time.monotonic() + 60
        while શૉ_મૂલ્ય not in લૉગ_પંક્તિ[ચલાવો_2:]:
            if time.monotonic() > 마감 or પ્રક્રિયા_મૂલ્ય.poll() is not None or b'HALTED' in લૉગ_પંક્તિ or b'PANIC:' in લૉગ_પંક્તિ:
                raise AssertionError(લૉગ_પંક્તિ[ચલાવો_2:].decode('utf-8', 'replace'))
            for ઇવેંટ, _ in પસંદકર્તા_a916db4e.select(.1):
                ડેટા = ઇવેંટ.fileobj.read(65536)
                if ડેટા: લૉગ_પંક્તિ.extend(ડેટા)
        return લૉગ_પંક્તિ[ચલાવો_2:].decode('utf-8', 'replace')

    def ક્લિક_કરો_બટન(પ્રતીક, 눌림=True): રિમોટ_મૂલ્ય.sendall(struct.pack('>BBHI', 4, int(눌림), 0, પ્રતીક))

    def SMS_મોકલો(લખાણ):
        ચલાવો_2 = len(લૉગ_પંક્તિ)
        for વર્ણ_મૂલ્ય in લખાણ:
            પ્રતીક = 0xff0d if વર્ણ_મૂલ્ય == '\n' else ord(વર્ણ_મૂલ્ય) if ord(વર્ણ_મૂલ્ય) < 256 else 0x1000000 | ord(વર્ણ_મૂલ્ય)
            ક્લિક_કરો_બટન(પ્રતીક); ક્લિક_કરો_બટન(પ્રતીક, False)
        return ચલાવો_2

    def શેલ(લખાણ): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_મોકલો(લખાણ+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, ઊભી_સ્થિતિ, 눌림): રિમોટ_મૂલ્ય.sendall(struct.pack('>BBHH', 5, 눌림, 가로, ઊભી_સ્થિતિ))

    def ક્લિક_કરો_મૂલ્ય(가로, ઊભી_સ્થિતિ): 가리키기(가로, ઊભી_સ્થિતિ, 1); 가리키기(가로, ઊભી_સ્થિતિ, 0)

    def બિટમૅપ_છબી():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 વાસ્તવિક_ડેટા 너비를 쓴다.
        રિમોટ_મૂલ્ય.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        રેખાંકન_મૂલ્ય = Image.new('RGB', (너비, 높이)); શ્રેણી_મૂલ્ય_9285603e = 0
        while True:
            종류 = 정확한값(રિમોટ_મૂલ્ય, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                લંબાઈ_મૂલ્ય = struct.unpack('>I', 정확한값(રિમોટ_મૂલ્ય, 7)[3:])[0]; 정확한값(રિમોટ_મૂલ્ય, લંબાઈ_મૂલ્ય); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(રિમોટ_મૂલ્ય, 3)[1:])[0]
            for _ in range(개수):
                가로, ઊભી_સ્થિતિ, 폭, લંબાઈ_મૂલ્ય, એન્કોડિંગ_મૂલ્ય = struct.unpack('>HHHHi', 정확한값(રિમોટ_મૂલ્ય, 12))
                if એન્કોડિંગ_મૂલ્ય == -239:
                    assert 폭==0 and લંબાઈ_મૂલ્ય==0, 'remote cursor must be hidden'
                    સૂચક_છુપાવેલું[0]=True
                    continue
                assert એન્કોડિંગ_મૂલ્ય == 0 and 가로+폭 <= 너비 and ઊભી_સ્થિતિ+લંબાઈ_મૂલ્ય <= 높이
                રેખાંકન_મૂલ્ય.paste(Image.frombytes('RGB', (폭, લંબાઈ_મૂલ્ય), 정확한값(રિમોટ_મૂલ્ય, 폭*લંબાઈ_મૂલ્ય*4), 'raw', 'BGRX'), (가로, ઊભી_સ્થિતિ))
                શ્રેણી_મૂલ્ય_9285603e += 폭*લંબાઈ_મૂલ્ય
            if શ્રેણી_મૂલ્ય_9285603e:
                assert શ્રેણી_મૂલ્ય_9285603e == 너비*높이, શ્રેણી_મૂલ્ય_9285603e
                return રેખાંકન_મૂલ્ય

    def તપાસો_પેલ(સુસંગત_બનાવવું_મૂલ્ય, 색):
        마감 = time.monotonic()+10
        while True:
            રેખાંકન_મૂલ્ય = બિટમૅપ_છબી()
            if રેખાંકન_મૂલ્ય.getpixel(સુસંગત_બનાવવું_મૂલ્ય) == 색: return રેખાંકન_મૂલ્ય
            if time.monotonic() > 마감: raise AssertionError((સુસંગત_બનાવવું_મૂલ્ય, રેખાંકન_મૂલ્ય.getpixel(સુસંગત_બનાવવું_મૂલ્ય), 색))

    def અપલોડ_કરો_ફાઇલો(નામ, ડેટા): સ્થાનાંતર_મૂલ્ય.storbinary('STOR '+નામ, io.BytesIO(ડેટા))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+આકાર_પાઠ+' RGB32').encode() in લૉગ_પંક્તિ
        print('BOOT:', આકાર_પાઠ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', લૉગ_પંક્તિ).group(1))
        રિમોટ_મૂલ્ય = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(રિમોટ_મૂલ્ય, 12) == b'RFB 003.008\n'; રિમોટ_મૂલ્ય.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(રિમોટ_મૂલ્ય, 정확한값(રિમોટ_મૂલ્ય, 1)[0]); રિમોટ_મૂલ્ય.sendall(b'\x01')
        assert 정확한값(રિમોટ_મૂલ્ય, 4) == b'\0'*4; રિમોટ_મૂલ્ય.sendall(b'\x01')
        초기 = 정확한값(રિમોટ_મૂલ્ય, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(રિમોટ_મૂલ્ય, struct.unpack('>I', 초기[20:])[0])
        રિમોટ_મૂલ્ય.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        રિમોટ_મૂલ્ય.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        તપાસો_પેલ((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for ઇવેંટ,_ in પસંદકર્તા_a916db4e.select(.02):
                    ડેટા=ઇવેંટ.fileobj.read(65536)
                    if ડેટા:લૉગ_પંક્તિ.extend(ડેટા)
        વિંડો=[12,48,568,360]
        def ચકાસવું_આકાર():
            હરોળ_મૂલ્ય,પંક્તિ_મૂલ્ય=(વિંડો[2]-24)//8,(વિંડો[3]-56)//16
            લખાણ=શેલ('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(હરોળ_મૂલ્ય,પંક્તિ_મૂલ્ય) in લખાણ,લખાણ
            # વાસ્તવિક_ડેટા વિંડો 테두리: 단지 માપ ક્વેરી_મૂલ્ય 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            તપાસો_પેલ((વિંડો[0],વિંડો[1]),(32,80,144))
            રેખાંકન_મૂલ્ય=તપાસો_પેલ((વિંડો[0]+વિંડો[2]-1,વિંડો[1]+વિંડો[3]-1),(39,49,64))
            return રેખાંકન_મૂલ્ય
        def 모서리(방향):
            return (વિંડો[0]+(3 if 방향 in (1,3) else વિંડો[2]-4),વિંડો[1]+(3 if 방향<=2 else વિંડો[3]-4))
        def આકાર_બદલો_ખેંચો(방향,차이,બટન=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            તપાસો_પેલ(흰점,(255,255,255))
            가리키기(가,세,બટન)
            끝가=max(0,min(너비-1,가+차이[0]));અંત_કરો_ઊભી=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,અંત_કરો_ઊભી,બટન);가리키기(끝가,અંત_કરો_ઊભી,0);숨고르기()
            if બટન==1:
                왼,위,폭,લંબાઈ_મૂલ્ય=વિંડો;오른,아래=왼+폭,위+લંબાઈ_મૂલ્ય
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+અંત_કરો_ઊભી-세))
                else:아래=max(위+216,min(높이,아래+અંત_કરો_ઊભી-세))
                વિંડો[:]=[왼,위,오른-왼,아래-위]
        ચકાસવું_આકાર();assert સૂચક_છુપાવેલું[0]
        આકાર_બદલો_ખેંચો(4,(-100,-60),4);ચકાસવું_આકાર() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            આકાર_બદલો_ખેંચો(방향,차이);ચકાસવું_આકાર()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_મોકલો("echo '"+긴글+"'");숨고르기()
        આકાર_બદલો_ખેંચો(4,(-1000,-1000));assert વિંડો[2:]==[360,216]
        આકાર_બદલો_ખેંચો(4,(너비,높이))
        ચલાવો_2=SMS_મોકલો('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),ચલાવો_2);ચકાસવું_આકાર()
        # vi가 સંપાદન_મૂલ્ય 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        શેલ('ftpd start')
        સ્થાનાંતર_મૂલ્ય=ftplib.FTP();સ્થાનાંતર_મૂલ્ય.encoding='utf-8';સ્થાનાંતર_મૂલ્ય.connect('127.0.0.1',પોર્ટ_નંબર,timeout=20);સ્થાનાંતર_મૂલ્ય.login()
        기다리기(b'NORMAL',SMS_મોકલો('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_મોકલો('i미저장 한글 ડેટા\n'));숨고르기()
        આકાર_બદલો_ખેંચો(4,(-너비,-높이))
        # ANSI પંક્તિ_મૂલ્ય 이동에 새 પંક્તિ_મૂલ્ય 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((વિંડો[3]-56)//16)).encode() in લૉગ_પંક્તિ[-4096:]
        SMS_મોકલો('작은 창에서도 이어 લખો\n');숨고르기()
        આકાર_બદલો_ખેંચો(4,(너비,높이))
        SMS_મોકલો('큰 창에서도 이어 લખો\n');숨고르기()
        ક્લિક_કરો_બટન(0xff1b);ક્લિક_કરો_બટન(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_મોકલો(':wq\n'))
        સામગ્રી_મૂલ્ય=bytearray();સ્થાનાંતર_મૂલ્ય.retrbinary('RETR 크기자료.txt',સામગ્રી_મૂલ્ય.extend)
        assert સામગ્રી_મૂલ્ય=='미저장 한글 ડેટા\n작은 창에서도 이어 લખો\n큰 창에서도 이어 લખો\n'.encode(),સામગ્રી_મૂલ્ય
        ચકાસવું_આકાર().save(str(પરિમાણ_પાથ/(આકાર_પાઠ+'-large.png')))
        # 두 번째 창은 ડિફૉલ્ટ_મૂલ્ય માપ, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        ચલાવો_2=len(લૉગ_પંક્તિ);ક્લિક_કરો_મૂલ્ય(70,16);기다리기(b'TERMINAL FOCUS 2',ચલાવો_2)
        assert 'TERMINAL SIZE 68x19' in શેલ('terminal size')
        ચલાવો_2=len(લૉગ_પંક્તિ);ક્લિક_કરો_મૂલ્ય(180,16);기다리기(b'TERMINAL FOCUS 1',ચલાવો_2);ચકાસવું_આકાર()
        આકાર_બદલો_ખેંચો(4,(-너비,-높이));ચકાસવું_આકાર().save(str(પરિમાણ_પાથ/(આકાર_પાઠ+'-small.png')))
        # માપ પરિવર્તન_કરો_મૂલ્ય બેક_મૂલ્ય X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        ચલાવો_2=len(લૉગ_પંક્તિ);ક્લિક_કરો_મૂલ્ય(વિંડો[0]+વિંડો[2]-20,વિંડો[1]+15);기다리기(b'TERMINAL FOCUS 2',ચલાવો_2)
        assert 'RESIZE CLOSED' in શેલ('echo RESIZE CLOSED')
        print('PASS:',આકાર_પાઠ,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if સ્થાનાંતર_મૂલ્ય:સ્થાનાંતર_મૂલ્ય.close()
        if રિમોટ_મૂલ્ય:રિમોટ_મૂલ્ય.close()
        if પ્રક્રિયા_મૂલ્ય.poll() is None:
            પ્રક્રિયા_મૂલ્ય.terminate()
            try:પ્રક્રિયા_મૂલ્ય.wait(timeout=8)
            except subprocess.TimeoutExpired:પ્રક્રિયા_મૂલ્ય.kill();પ્રક્રિયા_મૂલ્ય.wait()
        પસંદકર્તા_a916db4e.close();પ્રક્રિયા_મૂલ્ય.stdout.close();(પરિમાણ_પાથ/(આકાર_પાઠ+'.log')).write_bytes(લૉગ_પંક્તિ)


def ચલાવો_2():
    પરિમાણ_પાથ=પ્રોજેક્ટ_રૂટ/'build/verification/resize';પરિમાણ_પાથ.mkdir(parents=True,exist_ok=True)
    લૉગ_પંક્તિ={'passed':False,'kernel_sha256':hashlib.sha256((પ્રોજેક્ટ_રૂટ/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,પરિમાણ_પાથ);લૉગ_પંક્તિ['resolutions'].append([너비,높이])
        લૉગ_પંક્તિ.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(પરિમાણ_પાથ/'report.json').write_text(json.dumps(લૉગ_પંક્તિ,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':ચલાવો_2()
