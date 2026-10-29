#!/usr/bin/env python3
"""gangan_détà QEMU/VNC에서 터미널 모서리 wọ́_iye·ìtọ́ka·동적 ẹyọ_ọ̀rọ̀_iye ààyè_ìfàyọkàsí_ìgbéwọlé·ṣàtúnṣe_iye Àkóónú_iye 보존를 검사한다."""
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
from àtẹ_iṣẹ́_wo import 정확한값
from ṣiṣẹ́_àṣẹ import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ìwọn_SMS = '{}x{}'.format(너비, 높이)
    Ìlànà_iye = subprocess.Popen(['python3', str(기준/'Àwọn_irinṣẹ́/ṣiṣẹ́_àṣẹ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ìwọn_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    olùyàn_a916db4e = selectors.DefaultSelector(); olùyàn_a916db4e.register(Ìlànà_iye.stdout, selectors.EVENT_READ)
    àkọsílẹ̀_ìṣe_ìlà_ìbú = bytearray(); Ìjìnnà_iye = None; ṣàgbélọ_iye = None; ìtọ́ka_tó_farasin=[False]

    def 기다리기(ṣàfihàn_iye, Rọ́ọ̀nù=0):
        마감 = time.monotonic() + 60
        while ṣàfihàn_iye not in àkọsílẹ̀_ìṣe_ìlà_ìbú[Rọ́ọ̀nù:]:
            if time.monotonic() > 마감 or Ìlànà_iye.poll() is not None or b'HALTED' in àkọsílẹ̀_ìṣe_ìlà_ìbú or b'PANIC:' in àkọsílẹ̀_ìṣe_ìlà_ìbú:
                raise AssertionError(àkọsílẹ̀_ìṣe_ìlà_ìbú[Rọ́ọ̀nù:].decode('utf-8', 'replace'))
            for ìgbéṣẹ̀, _ in olùyàn_a916db4e.select(.1):
                détà = ìgbéṣẹ̀.fileobj.read(65536)
                if détà: àkọsílẹ̀_ìṣe_ìlà_ìbú.extend(détà)
        return àkọsílẹ̀_ìṣe_ìlà_ìbú[Rọ́ọ̀nù:].decode('utf-8', 'replace')

    def ṣíra_tẹ_bọ́tìnnì(àmì, 눌림=True): Ìjìnnà_iye.sendall(struct.pack('>BBHI', 4, int(눌림), 0, àmì))

    def fi_SMS_ránṣẹ́(SMS):
        Rọ́ọ̀nù = len(àkọsílẹ̀_ìṣe_ìlà_ìbú)
        for ẹyọ_ọ̀rọ̀_iye in SMS:
            àmì = 0xff0d if ẹyọ_ọ̀rọ̀_iye == '\n' else ord(ẹyọ_ọ̀rọ̀_iye) if ord(ẹyọ_ọ̀rọ̀_iye) < 256 else 0x1000000 | ord(ẹyọ_ọ̀rọ̀_iye)
            ṣíra_tẹ_bọ́tìnnì(àmì); ṣíra_tẹ_bọ́tìnnì(àmì, False)
        return Rọ́ọ̀nù

    def ṣẹ́ẹ̀lì(SMS): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', fi_SMS_ránṣẹ́(SMS+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): Ìjìnnà_iye.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def ṣíra_tẹ_iye(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def bitmap_àwòrán():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 gangan_détà 너비를 쓴다.
        Ìjìnnà_iye.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        íyàwòrán_iye = Image.new('RGB', (너비, 높이)); ìsọ̀rí_iye_9285603e = 0
        while True:
            종류 = 정확한값(Ìjìnnà_iye, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                gígùn_iye = struct.unpack('>I', 정확한값(Ìjìnnà_iye, 7)[3:])[0]; 정확한값(Ìjìnnà_iye, gígùn_iye); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(Ìjìnnà_iye, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, gígùn_iye, pípàrokò_iye = struct.unpack('>HHHHi', 정확한값(Ìjìnnà_iye, 12))
                if pípàrokò_iye == -239:
                    assert 폭==0 and gígùn_iye==0, 'remote cursor must be hidden'
                    ìtọ́ka_tó_farasin[0]=True
                    continue
                assert pípàrokò_iye == 0 and 가로+폭 <= 너비 and 세로+gígùn_iye <= 높이
                íyàwòrán_iye.paste(Image.frombytes('RGB', (폭, gígùn_iye), 정확한값(Ìjìnnà_iye, 폭*gígùn_iye*4), 'raw', 'BGRX'), (가로, 세로))
                ìsọ̀rí_iye_9285603e += 폭*gígùn_iye
            if ìsọ̀rí_iye_9285603e:
                assert ìsọ̀rí_iye_9285603e == 너비*높이, ìsọ̀rí_iye_9285603e
                return íyàwòrán_iye

    def ṣàyẹ̀wò_píkísẹ̀(ibi_ìtọ́kasí_iye, 색):
        마감 = time.monotonic()+10
        while True:
            íyàwòrán_iye = bitmap_àwòrán()
            if íyàwòrán_iye.getpixel(ibi_ìtọ́kasí_iye) == 색: return íyàwòrán_iye
            if time.monotonic() > 마감: raise AssertionError((ibi_ìtọ́kasí_iye, íyàwòrán_iye.getpixel(ibi_ìtọ́kasí_iye), 색))

    def fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì(Orúkọ, détà): ṣàgbélọ_iye.storbinary('STOR '+Orúkọ, io.BytesIO(détà))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ìwọn_SMS+' RGB32').encode() in àkọsílẹ̀_ìṣe_ìlà_ìbú
        print('BOOT:', ìwọn_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', àkọsílẹ̀_ìṣe_ìlà_ìbú).group(1))
        Ìjìnnà_iye = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(Ìjìnnà_iye, 12) == b'RFB 003.008\n'; Ìjìnnà_iye.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(Ìjìnnà_iye, 정확한값(Ìjìnnà_iye, 1)[0]); Ìjìnnà_iye.sendall(b'\x01')
        assert 정확한값(Ìjìnnà_iye, 4) == b'\0'*4; Ìjìnnà_iye.sendall(b'\x01')
        초기 = 정확한값(Ìjìnnà_iye, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(Ìjìnnà_iye, struct.unpack('>I', 초기[20:])[0])
        Ìjìnnà_iye.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        Ìjìnnà_iye.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        ṣàyẹ̀wò_píkísẹ̀((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for ìgbéṣẹ̀,_ in olùyàn_a916db4e.select(.02):
                    détà=ìgbéṣẹ̀.fileobj.read(65536)
                    if détà:àkọsílẹ̀_ìṣe_ìlà_ìbú.extend(détà)
        wínńdò=[12,48,568,360]
        def ridájú_ìwọn():
            ìlà_òró_iye,ìlà_ìbú_iye=(wínńdò[2]-24)//8,(wínńdò[3]-56)//16
            SMS=ṣẹ́ẹ̀lì('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(ìlà_òró_iye,ìlà_ìbú_iye) in SMS,SMS
            # gangan_détà wínńdò 테두리: 단지 Ìwọ̀n aṣèbéèré_iye 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            ṣàyẹ̀wò_píkísẹ̀((wínńdò[0],wínńdò[1]),(32,80,144))
            íyàwòrán_iye=ṣàyẹ̀wò_píkísẹ̀((wínńdò[0]+wínńdò[2]-1,wínńdò[1]+wínńdò[3]-1),(39,49,64))
            return íyàwòrán_iye
        def 모서리(방향):
            return (wínńdò[0]+(3 if 방향 in (1,3) else wínńdò[2]-4),wínńdò[1]+(3 if 방향<=2 else wínńdò[3]-4))
        def ìṣòdíwọ̀n_wọ́(방향,차이,bọ́tìnnì=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            ṣàyẹ̀wò_píkísẹ̀(흰점,(255,255,255))
            가리키기(가,세,bọ́tìnnì)
            끝가=max(0,min(너비-1,가+차이[0]));parí_Atòlóòró=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,parí_Atòlóòró,bọ́tìnnì);가리키기(끝가,parí_Atòlóòró,0);숨고르기()
            if bọ́tìnnì==1:
                왼,위,폭,gígùn_iye=wínńdò;오른,아래=왼+폭,위+gígùn_iye
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+parí_Atòlóòró-세))
                else:아래=max(위+216,min(높이,아래+parí_Atòlóòró-세))
                wínńdò[:]=[왼,위,오른-왼,아래-위]
        ridájú_ìwọn();assert ìtọ́ka_tó_farasin[0]
        ìṣòdíwọ̀n_wọ́(4,(-100,-60),4);ridájú_ìwọn() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ìṣòdíwọ̀n_wọ́(방향,차이);ridájú_ìwọn()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        fi_SMS_ránṣẹ́("echo '"+긴글+"'");숨고르기()
        ìṣòdíwọ̀n_wọ́(4,(-1000,-1000));assert wínńdò[2:]==[360,216]
        ìṣòdíwọ̀n_wọ́(4,(너비,높이))
        Rọ́ọ̀nù=fi_SMS_ránṣẹ́('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Rọ́ọ̀nù);ridájú_ìwọn()
        # vi가 ṣàtúnṣe_iye 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        ṣẹ́ẹ̀lì('ftpd start')
        ṣàgbélọ_iye=ftplib.FTP();ṣàgbélọ_iye.encoding='utf-8';ṣàgbélọ_iye.connect('127.0.0.1',접속번호,timeout=20);ṣàgbélọ_iye.login()
        기다리기(b'NORMAL',fi_SMS_ránṣẹ́('vi /크기자료.txt\n'))
        기다리기(b'INSERT',fi_SMS_ránṣẹ́('i미저장 한글 détà\n'));숨고르기()
        ìṣòdíwọ̀n_wọ́(4,(-너비,-높이))
        # ANSI ìlà_ìbú_iye 이동에 새 ìlà_ìbú_iye 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((wínńdò[3]-56)//16)).encode() in àkọsílẹ̀_ìṣe_ìlà_ìbú[-4096:]
        fi_SMS_ránṣẹ́('작은 창에서도 이어 Kọ\n');숨고르기()
        ìṣòdíwọ̀n_wọ́(4,(너비,높이))
        fi_SMS_ránṣẹ́('큰 창에서도 이어 Kọ\n');숨고르기()
        ṣíra_tẹ_bọ́tìnnì(0xff1b);ṣíra_tẹ_bọ́tìnnì(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',fi_SMS_ránṣẹ́(':wq\n'))
        Àkóónú_iye=bytearray();ṣàgbélọ_iye.retrbinary('RETR 크기자료.txt',Àkóónú_iye.extend)
        assert Àkóónú_iye=='미저장 한글 détà\n작은 창에서도 이어 Kọ\n큰 창에서도 이어 Kọ\n'.encode(),Àkóónú_iye
        ridájú_ìwọn().save(str(결과경로/(ìwọn_SMS+'-large.png')))
        # 두 번째 창은 àdáwọ̀ Ìwọ̀n, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Rọ́ọ̀nù=len(àkọsílẹ̀_ìṣe_ìlà_ìbú);ṣíra_tẹ_iye(70,16);기다리기(b'TERMINAL FOCUS 2',Rọ́ọ̀nù)
        assert 'TERMINAL SIZE 68x19' in ṣẹ́ẹ̀lì('terminal size')
        Rọ́ọ̀nù=len(àkọsílẹ̀_ìṣe_ìlà_ìbú);ṣíra_tẹ_iye(180,16);기다리기(b'TERMINAL FOCUS 1',Rọ́ọ̀nù);ridájú_ìwọn()
        ìṣòdíwọ̀n_wọ́(4,(-너비,-높이));ridájú_ìwọn().save(str(결과경로/(ìwọn_SMS+'-small.png')))
        # Ìwọ̀n ṣàyípadà_iye Padà_sẹ́yìn_iye X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        Rọ́ọ̀nù=len(àkọsílẹ̀_ìṣe_ìlà_ìbú);ṣíra_tẹ_iye(wínńdò[0]+wínńdò[2]-20,wínńdò[1]+15);기다리기(b'TERMINAL FOCUS 2',Rọ́ọ̀nù)
        assert 'RESIZE CLOSED' in ṣẹ́ẹ̀lì('echo RESIZE CLOSED')
        print('PASS:',ìwọn_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if ṣàgbélọ_iye:ṣàgbélọ_iye.close()
        if Ìjìnnà_iye:Ìjìnnà_iye.close()
        if Ìlànà_iye.poll() is None:
            Ìlànà_iye.terminate()
            try:Ìlànà_iye.wait(timeout=8)
            except subprocess.TimeoutExpired:Ìlànà_iye.kill();Ìlànà_iye.wait()
        olùyàn_a916db4e.close();Ìlànà_iye.stdout.close();(결과경로/(ìwọn_SMS+'.log')).write_bytes(àkọsílẹ̀_ìṣe_ìlà_ìbú)


def Rọ́ọ̀nù():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    àkọsílẹ̀_ìṣe_ìlà_ìbú={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);àkọsílẹ̀_ìṣe_ìlà_ìbú['resolutions'].append([너비,높이])
        àkọsílẹ̀_ìṣe_ìlà_ìbú.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(àkọsílẹ̀_ìṣe_ìlà_ìbú,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Rọ́ọ̀nù()
