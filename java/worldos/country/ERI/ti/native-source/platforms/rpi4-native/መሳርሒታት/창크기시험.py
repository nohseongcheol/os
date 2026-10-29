#!/usr/bin/env python3
"""ትኽክለኛ_ሓበሬታ QEMU/VNC에서 터미널 모서리 ጉተት_ዋጋ·ኣመልካቲ·동적 ፊደል_ዋጋ መሰኩዒ_ምእታው·ምዕራይ_ዋጋ ትሕዝቶ_ዋጋ 보존를 검사한다."""
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
from ዴስክቶፕ_ትርኢት import 정확한값
from ተግብር_ትእዛዝ import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    መጠን_ጽሑፍ_cdfada26 = '{}x{}'.format(너비, 높이)
    መስርሕ_ዋጋ = subprocess.Popen(['python3', str(기준/'መሳርሒታት/ተግብር_ትእዛዝ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', መጠን_ጽሑፍ_cdfada26], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    መራፂ_a916db4e = selectors.DefaultSelector(); መራፂ_a916db4e.register(መስርሕ_ዋጋ.stdout, selectors.EVENT_READ)
    ምዝጉብ_ሪጋ = bytearray(); ርሑቕ_ዋጋ = None; ምስጋር_ዋጋ = None; ኣመልካቲ_ሕቡእ=[False]

    def 기다리기(ኣርእይ_ዋጋ, ኣኺድ=0):
        마감 = time.monotonic() + 60
        while ኣርእይ_ዋጋ not in ምዝጉብ_ሪጋ[ኣኺድ:]:
            if time.monotonic() > 마감 or መስርሕ_ዋጋ.poll() is not None or b'HALTED' in ምዝጉብ_ሪጋ or b'PANIC:' in ምዝጉብ_ሪጋ:
                raise AssertionError(ምዝጉብ_ሪጋ[ኣኺድ:].decode('utf-8', 'replace'))
            for ፍጻመ, _ in መራፂ_a916db4e.select(.1):
                ሓበሬታ = ፍጻመ.fileobj.read(65536)
                if ሓበሬታ: ምዝጉብ_ሪጋ.extend(ሓበሬታ)
        return ምዝጉብ_ሪጋ[ኣኺድ:].decode('utf-8', 'replace')

    def ጠዉቕ_መጠወቒ(ምልክት, 눌림=True): ርሑቕ_ዋጋ.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ምልክት))

    def SMS_ስደድ(ጽሑፍ):
        ኣኺድ = len(ምዝጉብ_ሪጋ)
        for ፊደል_ዋጋ in ጽሑፍ:
            ምልክት = 0xff0d if ፊደል_ዋጋ == '\n' else ord(ፊደል_ዋጋ) if ord(ፊደል_ዋጋ) < 256 else 0x1000000 | ord(ፊደል_ዋጋ)
            ጠዉቕ_መጠወቒ(ምልክት); ጠዉቕ_መጠወቒ(ምልክት, False)
        return ኣኺድ

    def ሽፋን(ጽሑፍ): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_ስደድ(ጽሑፍ+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): ርሑቕ_ዋጋ.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def ጠዉቕ_ዋጋ(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def ቢትማፕ_ምስሊ():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ትኽክለኛ_ሓበሬታ 너비를 쓴다.
        ርሑቕ_ዋጋ.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ስእሊ_ዋጋ = Image.new('RGB', (너비, 높이)); ቦታ_ዋጋ = 0
        while True:
            종류 = 정확한값(ርሑቕ_ዋጋ, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ንውሓት_ዋጋ = struct.unpack('>I', 정확한값(ርሑቕ_ዋጋ, 7)[3:])[0]; 정확한값(ርሑቕ_ዋጋ, ንውሓት_ዋጋ); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ርሑቕ_ዋጋ, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, ንውሓት_ዋጋ, ምምስጣር_ዋጋ = struct.unpack('>HHHHi', 정확한값(ርሑቕ_ዋጋ, 12))
                if ምምስጣር_ዋጋ == -239:
                    assert 폭==0 and ንውሓት_ዋጋ==0, 'remote cursor must be hidden'
                    ኣመልካቲ_ሕቡእ[0]=True
                    continue
                assert ምምስጣር_ዋጋ == 0 and 가로+폭 <= 너비 and 세로+ንውሓት_ዋጋ <= 높이
                ስእሊ_ዋጋ.paste(Image.frombytes('RGB', (폭, ንውሓት_ዋጋ), 정확한값(ርሑቕ_ዋጋ, 폭*ንውሓት_ዋጋ*4), 'raw', 'BGRX'), (가로, 세로))
                ቦታ_ዋጋ += 폭*ንውሓት_ዋጋ
            if ቦታ_ዋጋ:
                assert ቦታ_ዋጋ == 너비*높이, ቦታ_ዋጋ
                return ስእሊ_ዋጋ

    def ፈትሽ_ንጣብ(좌표, 색):
        마감 = time.monotonic()+10
        while True:
            ስእሊ_ዋጋ = ቢትማፕ_ምስሊ()
            if ስእሊ_ዋጋ.getpixel(좌표) == 색: return ስእሊ_ዋጋ
            if time.monotonic() > 마감: raise AssertionError((좌표, ስእሊ_ዋጋ.getpixel(좌표), 색))

    def ስቐል_ፋይላት(ሽም, ሓበሬታ): ምስጋር_ዋጋ.storbinary('STOR '+ሽም, io.BytesIO(ሓበሬታ))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+መጠን_ጽሑፍ_cdfada26+' RGB32').encode() in ምዝጉብ_ሪጋ
        print('BOOT:', መጠን_ጽሑፍ_cdfada26, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ምዝጉብ_ሪጋ).group(1))
        ርሑቕ_ዋጋ = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ርሑቕ_ዋጋ, 12) == b'RFB 003.008\n'; ርሑቕ_ዋጋ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ርሑቕ_ዋጋ, 정확한값(ርሑቕ_ዋጋ, 1)[0]); ርሑቕ_ዋጋ.sendall(b'\x01')
        assert 정확한값(ርሑቕ_ዋጋ, 4) == b'\0'*4; ርሑቕ_ዋጋ.sendall(b'\x01')
        초기 = 정확한값(ርሑቕ_ዋጋ, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ርሑቕ_ዋጋ, struct.unpack('>I', 초기[20:])[0])
        ርሑቕ_ዋጋ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ርሑቕ_ዋጋ.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        ፈትሽ_ንጣብ((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for ፍጻመ,_ in መራፂ_a916db4e.select(.02):
                    ሓበሬታ=ፍጻመ.fileobj.read(65536)
                    if ሓበሬታ:ምዝጉብ_ሪጋ.extend(ሓበሬታ)
        መስኮት=[12,48,568,360]
        def ኣረጋግጽ_መጠን():
            ዓምዲ_ዋጋ,ሪጋ_ዋጋ=(መስኮት[2]-24)//8,(መስኮት[3]-56)//16
            ጽሑፍ=ሽፋን('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(ዓምዲ_ዋጋ,ሪጋ_ዋጋ) in ጽሑፍ,ጽሑፍ
            # ትኽክለኛ_ሓበሬታ መስኮት 테두리: 단지 መጠን ሕቶ_ዋጋ 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            ፈትሽ_ንጣብ((መስኮት[0],መስኮት[1]),(32,80,144))
            ስእሊ_ዋጋ=ፈትሽ_ንጣብ((መስኮት[0]+መስኮት[2]-1,መስኮት[1]+መስኮት[3]-1),(39,49,64))
            return ስእሊ_ዋጋ
        def 모서리(방향):
            return (መስኮት[0]+(3 if 방향 in (1,3) else መስኮት[2]-4),መስኮት[1]+(3 if 방향<=2 else መስኮት[3]-4))
        def መጠን_ለውጥ_ጉተት(방향,차이,መጠወቒ=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            ፈትሽ_ንጣብ(흰점,(255,255,255))
            가리키기(가,세,መጠወቒ)
            끝가=max(0,min(너비-1,가+차이[0]));ኣቑም_ትኹል=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,ኣቑም_ትኹል,መጠወቒ);가리키기(끝가,ኣቑም_ትኹል,0);숨고르기()
            if መጠወቒ==1:
                왼,위,폭,ንውሓት_ዋጋ=መስኮት;오른,아래=왼+폭,위+ንውሓት_ዋጋ
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+ኣቑም_ትኹል-세))
                else:아래=max(위+216,min(높이,아래+ኣቑም_ትኹል-세))
                መስኮት[:]=[왼,위,오른-왼,아래-위]
        ኣረጋግጽ_መጠን();assert ኣመልካቲ_ሕቡእ[0]
        መጠን_ለውጥ_ጉተት(4,(-100,-60),4);ኣረጋግጽ_መጠን() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            መጠን_ለውጥ_ጉተት(방향,차이);ኣረጋግጽ_መጠን()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_ስደድ("echo '"+긴글+"'");숨고르기()
        መጠን_ለውጥ_ጉተት(4,(-1000,-1000));assert መስኮት[2:]==[360,216]
        መጠን_ለውጥ_ጉተት(4,(너비,높이))
        ኣኺድ=SMS_ስደድ('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),ኣኺድ);ኣረጋግጽ_መጠን()
        # vi가 ምዕራይ_ዋጋ 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        ሽፋን('ftpd start')
        ምስጋር_ዋጋ=ftplib.FTP();ምስጋር_ዋጋ.encoding='utf-8';ምስጋር_ዋጋ.connect('127.0.0.1',접속번호,timeout=20);ምስጋር_ዋጋ.login()
        기다리기(b'NORMAL',SMS_ስደድ('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_ስደድ('i미저장 한글 ሓበሬታ\n'));숨고르기()
        መጠን_ለውጥ_ጉተት(4,(-너비,-높이))
        # ANSI ሪጋ_ዋጋ 이동에 새 ሪጋ_ዋጋ 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((መስኮት[3]-56)//16)).encode() in ምዝጉብ_ሪጋ[-4096:]
        SMS_ስደድ('작은 창에서도 이어 ጸሓፍ\n');숨고르기()
        መጠን_ለውጥ_ጉተት(4,(너비,높이))
        SMS_ስደድ('큰 창에서도 이어 ጸሓፍ\n');숨고르기()
        ጠዉቕ_መጠወቒ(0xff1b);ጠዉቕ_መጠወቒ(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_ስደድ(':wq\n'))
        ትሕዝቶ_ዋጋ=bytearray();ምስጋር_ዋጋ.retrbinary('RETR 크기자료.txt',ትሕዝቶ_ዋጋ.extend)
        assert ትሕዝቶ_ዋጋ=='미저장 한글 ሓበሬታ\n작은 창에서도 이어 ጸሓፍ\n큰 창에서도 이어 ጸሓፍ\n'.encode(),ትሕዝቶ_ዋጋ
        ኣረጋግጽ_መጠን().save(str(결과경로/(መጠን_ጽሑፍ_cdfada26+'-large.png')))
        # 두 번째 창은 ንቡር_ዋጋ መጠን, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        ኣኺድ=len(ምዝጉብ_ሪጋ);ጠዉቕ_ዋጋ(70,16);기다리기(b'TERMINAL FOCUS 2',ኣኺድ)
        assert 'TERMINAL SIZE 68x19' in ሽፋን('terminal size')
        ኣኺድ=len(ምዝጉብ_ሪጋ);ጠዉቕ_ዋጋ(180,16);기다리기(b'TERMINAL FOCUS 1',ኣኺድ);ኣረጋግጽ_መጠን()
        መጠን_ለውጥ_ጉተት(4,(-너비,-높이));ኣረጋግጽ_መጠን().save(str(결과경로/(መጠን_ጽሑፍ_cdfada26+'-small.png')))
        # መጠን ለውጥ_ዋጋ ድሕሪት_ዋጋ X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        ኣኺድ=len(ምዝጉብ_ሪጋ);ጠዉቕ_ዋጋ(መስኮት[0]+መስኮት[2]-20,መስኮት[1]+15);기다리기(b'TERMINAL FOCUS 2',ኣኺድ)
        assert 'RESIZE CLOSED' in ሽፋን('echo RESIZE CLOSED')
        print('PASS:',መጠን_ጽሑፍ_cdfada26,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if ምስጋር_ዋጋ:ምስጋር_ዋጋ.close()
        if ርሑቕ_ዋጋ:ርሑቕ_ዋጋ.close()
        if መስርሕ_ዋጋ.poll() is None:
            መስርሕ_ዋጋ.terminate()
            try:መስርሕ_ዋጋ.wait(timeout=8)
            except subprocess.TimeoutExpired:መስርሕ_ዋጋ.kill();መስርሕ_ዋጋ.wait()
        መራፂ_a916db4e.close();መስርሕ_ዋጋ.stdout.close();(결과경로/(መጠን_ጽሑፍ_cdfada26+'.log')).write_bytes(ምዝጉብ_ሪጋ)


def ኣኺድ():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    ምዝጉብ_ሪጋ={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);ምዝጉብ_ሪጋ['resolutions'].append([너비,높이])
        ምዝጉብ_ሪጋ.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(ምዝጉብ_ሪጋ,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':ኣኺድ()
