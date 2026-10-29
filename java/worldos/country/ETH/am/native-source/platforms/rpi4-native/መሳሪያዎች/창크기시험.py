#!/usr/bin/env python3
"""ትክክለኛ_ውሂብ QEMU/VNC에서 ተርሚናል 모서리 ጎትት_እሴት·ጠቋሚ·동적 ቁምፊ_እሴት ማስገቢያ_ቀዳዳ_ምዝግብ·አርትዕ_እሴት ይዘት_እሴት 보존를 검사한다."""
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
from ዴስክቶፕ_እየው import 정확한값
from ፈጽም_ትእዛዝ import አሳይ_ስር


def 창크기시험(너비, 높이, ልኬት_ዱካ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); የወደብ_ቁጥር = 임시.getsockname()[1]
    መጠን_ቀይር_ጽሁፍ = '{}x{}'.format(너비, 높이)
    ሂደት_እሴት = subprocess.Popen(['python3', str(አሳይ_ስር/'መሳሪያዎች/ፈጽም_ትእዛዝ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(የወደብ_ቁጥር), '--resolution', መጠን_ቀይር_ጽሁፍ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    መራጭ_a916db4e = selectors.DefaultSelector(); መራጭ_a916db4e.register(ሂደት_እሴት.stdout, selectors.EVENT_READ)
    መዝግብ_ረድፍ = bytearray(); የሩቅ_እሴት = None; ትልልፍ_እሴት = None; ጠቋሚ_ድብቅ=[False]

    def 기다리기(አሳይ_እሴት, ማስኬጃ=0):
        마감 = time.monotonic() + 60
        while አሳይ_እሴት not in መዝግብ_ረድፍ[ማስኬጃ:]:
            if time.monotonic() > 마감 or ሂደት_እሴት.poll() is not None or b'HALTED' in መዝግብ_ረድፍ or b'PANIC:' in መዝግብ_ረድፍ:
                raise AssertionError(መዝግብ_ረድፍ[ማስኬጃ:].decode('utf-8', 'replace'))
            for ፍጻሜ, _ in መራጭ_a916db4e.select(.1):
                ውሂብ = ፍጻሜ.fileobj.read(65536)
                if ውሂብ: መዝግብ_ረድፍ.extend(ውሂብ)
        return መዝግብ_ረድፍ[ማስኬጃ:].decode('utf-8', 'replace')

    def ጠቅ_አድርግ_አዝራር(ምልክት_ad6f1a96, 눌림=True): የሩቅ_እሴት.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ምልክት_ad6f1a96))

    def ጽሁፍ_ላክ(ጽሁፍ):
        ማስኬጃ = len(መዝግብ_ረድፍ)
        for ቁምፊ_እሴት in ጽሁፍ:
            ምልክት_ad6f1a96 = 0xff0d if ቁምፊ_እሴት == '\n' else ord(ቁምፊ_እሴት) if ord(ቁምፊ_እሴት) < 256 else 0x1000000 | ord(ቁምፊ_እሴት)
            ጠቅ_አድርግ_አዝራር(ምልክት_ad6f1a96); ጠቅ_አድርግ_አዝራር(ምልክት_ad6f1a96, False)
        return ማስኬጃ

    def ሼል(ጽሁፍ): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', ጽሁፍ_ላክ(ጽሁፍ+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, ቋሚ_በቦታ_አስቀመጠ, 눌림): የሩቅ_እሴት.sendall(struct.pack('>BBHH', 5, 눌림, 가로, ቋሚ_በቦታ_አስቀመጠ))

    def ጠቅ_አድርግ_እሴት(가로, ቋሚ_በቦታ_አስቀመጠ): 가리키기(가로, ቋሚ_በቦታ_አስቀመጠ, 1); 가리키기(가로, ቋሚ_በቦታ_አስቀመጠ, 0)

    def ቢትማፕ_ምስል():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ትክክለኛ_ውሂብ 너비를 쓴다.
        የሩቅ_እሴት.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ስዕል_እሴት = Image.new('RGB', (너비, 높이)); ምድብ_እሴት_9285603e = 0
        while True:
            종류 = 정확한값(የሩቅ_እሴት, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ርዝመት_እሴት = struct.unpack('>I', 정확한값(የሩቅ_እሴት, 7)[3:])[0]; 정확한값(የሩቅ_እሴት, ርዝመት_እሴት); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(የሩቅ_እሴት, 3)[1:])[0]
            for _ in range(개수):
                가로, ቋሚ_በቦታ_አስቀመጠ, 폭, ርዝመት_እሴት, በኮድ_መክተት_እሴት = struct.unpack('>HHHHi', 정확한값(የሩቅ_እሴት, 12))
                if በኮድ_መክተት_እሴት == -239:
                    assert 폭==0 and ርዝመት_እሴት==0, 'remote cursor must be hidden'
                    ጠቋሚ_ድብቅ[0]=True
                    continue
                assert በኮድ_መክተት_እሴት == 0 and 가로+폭 <= 너비 and ቋሚ_በቦታ_አስቀመጠ+ርዝመት_እሴት <= 높이
                ስዕል_እሴት.paste(Image.frombytes('RGB', (폭, ርዝመት_እሴት), 정확한값(የሩቅ_እሴት, 폭*ርዝመት_እሴት*4), 'raw', 'BGRX'), (가로, ቋሚ_በቦታ_አስቀመጠ))
                ምድብ_እሴት_9285603e += 폭*ርዝመት_እሴት
            if ምድብ_እሴት_9285603e:
                assert ምድብ_እሴት_9285603e == 너비*높이, ምድብ_እሴት_9285603e
                return ስዕል_እሴት

    def ቼክ_ፒክስል(አቀነባብር_እሴት, 색):
        마감 = time.monotonic()+10
        while True:
            ስዕል_እሴት = ቢትማፕ_ምስል()
            if ስዕል_እሴት.getpixel(አቀነባብር_እሴት) == 색: return ስዕል_እሴት
            if time.monotonic() > 마감: raise AssertionError((አቀነባብር_እሴት, ስዕል_እሴት.getpixel(አቀነባብር_እሴት), 색))

    def መጫን_ፋይሎች(ስም, ውሂብ): ትልልፍ_እሴት.storbinary('STOR '+ስም, io.BytesIO(ውሂብ))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+መጠን_ቀይር_ጽሁፍ+' RGB32').encode() in መዝግብ_ረድፍ
        print('BOOT:', መጠን_ቀይር_ጽሁፍ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', መዝግብ_ረድፍ).group(1))
        የሩቅ_እሴት = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(የሩቅ_እሴት, 12) == b'RFB 003.008\n'; የሩቅ_እሴት.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(የሩቅ_እሴት, 정확한값(የሩቅ_እሴት, 1)[0]); የሩቅ_እሴት.sendall(b'\x01')
        assert 정확한값(የሩቅ_እሴት, 4) == b'\0'*4; የሩቅ_እሴት.sendall(b'\x01')
        초기 = 정확한값(የሩቅ_እሴት, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(የሩቅ_እሴት, struct.unpack('>I', 초기[20:])[0])
        የሩቅ_እሴት.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        የሩቅ_እሴት.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        ቼክ_ፒክስል((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for ፍጻሜ,_ in መራጭ_a916db4e.select(.02):
                    ውሂብ=ፍጻሜ.fileobj.read(65536)
                    if ውሂብ:መዝግብ_ረድፍ.extend(ውሂብ)
        መስኮት=[12,48,568,360]
        def አረጋግጥ_መጠን_ቀይር():
            አምድ_እሴት,ረድፍ_እሴት=(መስኮት[2]-24)//8,(መስኮት[3]-56)//16
            ጽሁፍ=ሼል('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(አምድ_እሴት,ረድፍ_እሴት) in ጽሁፍ,ጽሁፍ
            # ትክክለኛ_ውሂብ መስኮት 테두리: 단지 መጠን መጠይቅ_እሴት 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            ቼክ_ፒክስል((መስኮት[0],መስኮት[1]),(32,80,144))
            ስዕል_እሴት=ቼክ_ፒክስል((መስኮት[0]+መስኮት[2]-1,መስኮት[1]+መስኮት[3]-1),(39,49,64))
            return ስዕል_እሴት
        def 모서리(방향):
            return (መስኮት[0]+(3 if 방향 in (1,3) else መስኮት[2]-4),መስኮት[1]+(3 if 방향<=2 else መስኮት[3]-4))
        def መጠን_ለውጥ_ጎትት(방향,차이,አዝራር=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            ቼክ_ፒክስል(흰점,(255,255,255))
            가리키기(가,세,አዝራር)
            끝가=max(0,min(너비-1,가+차이[0]));ጨርስ_ቋሚ=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,ጨርስ_ቋሚ,አዝራር);가리키기(끝가,ጨርስ_ቋሚ,0);숨고르기()
            if አዝራር==1:
                왼,위,폭,ርዝመት_እሴት=መስኮት;오른,아래=왼+폭,위+ርዝመት_እሴት
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+ጨርስ_ቋሚ-세))
                else:아래=max(위+216,min(높이,아래+ጨርስ_ቋሚ-세))
                መስኮት[:]=[왼,위,오른-왼,아래-위]
        አረጋግጥ_መጠን_ቀይር();assert ጠቋሚ_ድብቅ[0]
        መጠን_ለውጥ_ጎትት(4,(-100,-60),4);አረጋግጥ_መጠን_ቀይር() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            መጠን_ለውጥ_ጎትት(방향,차이);አረጋግጥ_መጠን_ቀይር()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        ጽሁፍ_ላክ("echo '"+긴글+"'");숨고르기()
        መጠን_ለውጥ_ጎትት(4,(-1000,-1000));assert መስኮት[2:]==[360,216]
        መጠን_ለውጥ_ጎትት(4,(너비,높이))
        ማስኬጃ=ጽሁፍ_ላክ('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),ማስኬጃ);አረጋግጥ_መጠን_ቀይር()
        # vi가 አርትዕ_እሴት 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        ሼል('ftpd start')
        ትልልፍ_እሴት=ftplib.FTP();ትልልፍ_እሴት.encoding='utf-8';ትልልፍ_እሴት.connect('127.0.0.1',የወደብ_ቁጥር,timeout=20);ትልልፍ_እሴት.login()
        기다리기(b'NORMAL',ጽሁፍ_ላክ('vi /크기자료.txt\n'))
        기다리기(b'INSERT',ጽሁፍ_ላክ('i미저장 한글 ውሂብ\n'));숨고르기()
        መጠን_ለውጥ_ጎትት(4,(-너비,-높이))
        # ANSI ረድፍ_እሴት 이동에 새 ረድፍ_እሴት 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((መስኮት[3]-56)//16)).encode() in መዝግብ_ረድፍ[-4096:]
        ጽሁፍ_ላክ('작은 창에서도 이어 መጻፊያ\n');숨고르기()
        መጠን_ለውጥ_ጎትት(4,(너비,높이))
        ጽሁፍ_ላክ('큰 창에서도 이어 መጻፊያ\n');숨고르기()
        ጠቅ_አድርግ_አዝራር(0xff1b);ጠቅ_አድርግ_አዝራር(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',ጽሁፍ_ላክ(':wq\n'))
        ይዘት_እሴት=bytearray();ትልልፍ_እሴት.retrbinary('RETR 크기자료.txt',ይዘት_እሴት.extend)
        assert ይዘት_እሴት=='미저장 한글 ውሂብ\n작은 창에서도 이어 መጻፊያ\n큰 창에서도 이어 መጻፊያ\n'.encode(),ይዘት_እሴት
        አረጋግጥ_መጠን_ቀይር().save(str(ልኬት_ዱካ/(መጠን_ቀይር_ጽሁፍ+'-large.png')))
        # 두 번째 창은 ነባሪ_እሴት መጠን, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        ማስኬጃ=len(መዝግብ_ረድፍ);ጠቅ_አድርግ_እሴት(70,16);기다리기(b'TERMINAL FOCUS 2',ማስኬጃ)
        assert 'TERMINAL SIZE 68x19' in ሼል('terminal size')
        ማስኬጃ=len(መዝግብ_ረድፍ);ጠቅ_አድርግ_እሴት(180,16);기다리기(b'TERMINAL FOCUS 1',ማስኬጃ);አረጋግጥ_መጠን_ቀይር()
        መጠን_ለውጥ_ጎትት(4,(-너비,-높이));አረጋግጥ_መጠን_ቀይር().save(str(ልኬት_ዱካ/(መጠን_ቀይር_ጽሁፍ+'-small.png')))
        # መጠን ለውጥ_እሴት ተመለስ_እሴት X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        ማስኬጃ=len(መዝግብ_ረድፍ);ጠቅ_አድርግ_እሴት(መስኮት[0]+መስኮት[2]-20,መስኮት[1]+15);기다리기(b'TERMINAL FOCUS 2',ማስኬጃ)
        assert 'RESIZE CLOSED' in ሼል('echo RESIZE CLOSED')
        print('PASS:',መጠን_ቀይር_ጽሁፍ,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if ትልልፍ_እሴት:ትልልፍ_እሴት.close()
        if የሩቅ_እሴት:የሩቅ_እሴት.close()
        if ሂደት_እሴት.poll() is None:
            ሂደት_እሴት.terminate()
            try:ሂደት_እሴት.wait(timeout=8)
            except subprocess.TimeoutExpired:ሂደት_እሴት.kill();ሂደት_እሴት.wait()
        መራጭ_a916db4e.close();ሂደት_እሴት.stdout.close();(ልኬት_ዱካ/(መጠን_ቀይር_ጽሁፍ+'.log')).write_bytes(መዝግብ_ረድፍ)


def ማስኬጃ():
    ልኬት_ዱካ=አሳይ_ስር/'build/verification/resize';ልኬት_ዱካ.mkdir(parents=True,exist_ok=True)
    መዝግብ_ረድፍ={'passed':False,'kernel_sha256':hashlib.sha256((አሳይ_ስር/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,ልኬት_ዱካ);መዝግብ_ረድፍ['resolutions'].append([너비,높이])
        መዝግብ_ረድፍ.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(ልኬት_ዱካ/'report.json').write_text(json.dumps(መዝግብ_ረድፍ,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':ማስኬጃ()
