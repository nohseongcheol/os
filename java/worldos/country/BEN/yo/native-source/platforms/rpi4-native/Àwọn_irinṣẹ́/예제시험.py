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
from àtẹ_iṣẹ́_wo import 정확한값
from 예제되돌림서버 import 되돌림서버
from ṣiṣẹ́_àṣẹ import 기준


def test_언어(Èdè,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Ìlànà=subprocess.Popen(['python3',str(기준/'Àwọn_irinṣẹ́/ṣiṣẹ́_àṣẹ.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    olùyàn=selectors.DefaultSelector();olùyàn.register(Ìlànà.stdout,selectors.EVENT_READ)
    대화기록=bytearray();aṣojú=None;fáìlì_ṣàgbélọ_Ìsomọ́=None
    def 수신하기(확인표시,Rọ́ọ̀nù=0):
        parí_Ìtayọ=time.monotonic()+60
        while 확인표시 not in 대화기록[Rọ́ọ̀nù:]:
            if time.monotonic()>parí_Ìtayọ or Ìlànà.poll() is not None:raise AssertionError(대화기록[Rọ́ọ̀nù:].decode('utf-8','replace'))
            for 누름값,_ in olùyàn.select(.1):
                détà=누름값.fileobj.read(65536)
                if détà:대화기록.extend(détà)
        return 대화기록[Rọ́ọ̀nù:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(àmì_iye,누르는중=True):aṣojú.sendall(struct.pack('>BBHI',4,int(누르는중),0,àmì_iye))
    def bẹ̀rẹ̀_Ìtayọ(ìlà):
        Rọ́ọ̀nù=len(대화기록)
        for kóòdù_ẹyọ_ọ̀rọ̀ in ìlà+'\n':
            àmì_iye=0xff0d if kóòdù_ẹyọ_ọ̀rọ̀=='\n' else ord(kóòdù_ẹyọ_ọ̀rọ̀) if ord(kóòdù_ẹyọ_ọ̀rọ̀)<256 else 0x1000000|ord(kóòdù_ẹyọ_ọ̀rọ̀)
            누름값(àmì_iye);누름값(àmì_iye,False)
        return Rọ́ọ̀nù
    def ṣẹ́ẹ̀lì(ìlà):return 수신하기(b'jkoros-native> ',bẹ̀rẹ̀_Ìtayọ(ìlà))
    def ṣiṣẹ́_àṣẹ(ìlà,예상결과):
        SMS=ṣẹ́ẹ̀lì(ìlà);assert 예상결과 in SMS and 'exit 0' in SMS,(ìlà,SMS)
        return SMS
    def 화소들():
        aṣojú.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            ìsọ̀rí_iye=정확한값(aṣojú,1)[0]
            if ìsọ̀rí_iye==2:continue
            if ìsọ̀rí_iye==3:
                개수=struct.unpack('>I',정확한값(aṣojú,7)[3:])[0];정확한값(aṣojú,개수);continue
            assert ìsọ̀rí_iye==0,ìsọ̀rí_iye
            항목수=struct.unpack('>H',정확한값(aṣojú,3)[1:])[0]
            for _ in range(항목수):
                ibi_ìtọ́kasí_x,세로좌표,너비값,높이값,àkójọpọ̀_ẹyọ_ọ̀rọ̀=struct.unpack('>HHHHi',정확한값(aṣojú,12));assert àkójọpọ̀_ẹyọ_ọ̀rọ̀==0,àkójọpọ̀_ẹyọ_ọ̀rọ̀
                détà=정확한값(aṣojú,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;àfojúsùn=((세로좌표+행위치)*640+ibi_ìtọ́kasí_x+열위치)*3
                        빛삼원색[àfojúsùn:àfojúsùn+3]=bytes((détà[원본자료+2],détà[원본자료+1],détà[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        aṣojú=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(aṣojú,12)==b'RFB 003.008\n';aṣojú.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(aṣojú,정확한값(aṣojú,1)[0]);aṣojú.sendall(b'\x01');assert 정확한값(aṣojú,4)==b'\0'*4
        aṣojú.sendall(b'\x01');초기값=정확한값(aṣojú,24);정확한값(aṣojú,struct.unpack('>I',초기값[20:])[0])
        aṣojú.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        aṣojú.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in ṣẹ́ẹ̀lì('ftpd start')
        fáìlì_ṣàgbélọ_Ìsomọ́=ftplib.FTP();fáìlì_ṣàgbélọ_Ìsomọ́.encoding='utf-8';fáìlì_ṣàgbélọ_Ìsomọ́.connect('127.0.0.1',파일전송접속번호,timeout=20);fáìlì_ṣàgbélọ_Ìsomọ́.login()
        ojúlówó_détà_détà=('GUI와 FTP 동시 사용 '+Èdè+' 😀\n').encode()
        fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR 함께.txt',io.BytesIO(ojúlówó_détà_détà))
        assert ojúlówó_détà_détà.decode().strip() in ṣẹ́ẹ̀lì('cat /함께.txt')
        받은수=bytearray();fáìlì_ṣàgbélọ_Ìsomọ́.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==ojúlówó_détà_détà;fáìlì_ṣàgbélọ_Ìsomọ́.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        í_meèlì_Àtòkọ=ṣẹ́ẹ̀lì('ls /example')
        assert all(Orúkọ in í_meèlì_Àtòkọ for Orúkọ in ('java/','c/','python/','README.md')),í_meèlì_Àtòkọ
        if Èdè=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for ọ̀nà,ìgbéwọlé_kókó in 꾸러미명세.items():
                ṣẹ́ẹ̀lì('cp '+ọ̀nà+' /example-check.bin')
                Àkóónú_iye=bytearray();fáìlì_ṣàgbélọ_Ìsomọ́.retrbinary('RETR example-check.bin',Àkóónú_iye.extend)
                assert len(Àkóónú_iye)==ìgbéwọlé_kókó['bytes'] and hashlib.sha256(Àkóónú_iye).hexdigest()==ìgbéwọlé_kókó['sha256'],ọ̀nà
            fáìlì_ṣàgbélọ_Ìsomọ́.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            abèjì=bytes(range(256))*64
            fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR boundary.bin',io.BytesIO(abèjì))
            Àkóónú_iye=bytearray();fáìlì_ṣàgbélọ_Ìsomọ́.retrbinary('RETR boundary.bin',Àkóónú_iye.extend)
            assert Àkóónú_iye==abèjì and 'boundary.bin' in fáìlì_ṣàgbélọ_Ìsomọ́.nlst()
            ṣẹ́ẹ̀lì('cp /boundary.bin /boundary-copy.bin')
            Àkóónú_iye=bytearray();fáìlì_ṣàgbélọ_Ìsomọ́.retrbinary('RETR boundary-copy.bin',Àkóónú_iye.extend)
            assert Àkóónú_iye==abèjì
            fáìlì_ṣàgbélọ_Ìsomọ́.delete('boundary.bin');fáìlì_ṣàgbélọ_Ìsomọ́.delete('boundary-copy.bin')
        assert '출력예제' in ṣẹ́ẹ̀lì('ls /example/'+Èdè)
        ṣẹ́ẹ̀lì('cd /example/'+Èdè)
        orúkọ_atọ́ka={'java':'JAVA','c':'C','python':'PYTHON'}[Èdè]
        예상파일=orúkọ_atọ́ka+' Fáìlì: 한글 détà 😀\n'
        if Èdè=='java':
            ṣiṣẹ́_àṣẹ('javac 출력예제.java','Compiled:');ṣiṣẹ́_àṣẹ('java 출력예제','JAVA 출력: 안녕하세요 😀')
            ṣiṣẹ́_àṣẹ('javac 파일예제.java','Compiled:');ṣiṣẹ́_àṣẹ('java 파일예제',예상파일)
            ṣiṣẹ́_àṣẹ('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_ojú,되돌림서버항목.전문접속번호),'JAVA 네트워크 ridájú: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif Èdè=='c':
            for Orúkọ,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Fáìlì','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 ridájú: UDP 한글')]:
                ṣiṣẹ́_àṣẹ('cc '+Orúkọ+'예제.c -o ṣiṣẹ́_àṣẹ','Compiled native ARM64 ELF:')
                ṣiṣẹ́_àṣẹ('./ṣiṣẹ́_àṣẹ'+전달값,예상결과)
            ṣiṣẹ́_àṣẹ('cc 그래픽예제.c -o ṣiṣẹ́_àṣẹ','Compiled native ARM64 ELF:');그림명령='./ṣiṣẹ́_àṣẹ'
        else:
            for Orúkọ,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Fáìlì','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 ridájú: UDP 한글')]:
                ṣiṣẹ́_àṣẹ('python '+Orúkọ+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        bẹ̀rẹ̀_íyàwòrán=bẹ̀rẹ̀_Ìtayọ(그림명령)
        SMS=수신하기('그림을 확인한 Padà_sẹ́yìn_iye Enter를 누르세요.\r\n'.encode(),bẹ̀rẹ̀_íyàwòrán)
        assert orúkọ_atọ́ka+' 그래픽: 빨강 초록 파랑' in SMS and 'exit 0' not in SMS,SMS
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        fáìlì_ṣàgbélọ_Ìsomọ́.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();fáìlì_ṣàgbélọ_Ìsomọ́.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';fáìlì_ṣàgbélọ_Ìsomọ́.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Ìtayọ_iye=(세로좌표*640+610)*3;assert tuple(빛삼원색[Ìtayọ_iye:Ìtayọ_iye+3])==색상,(Èdè,세로좌표,tuple(빛삼원색[Ìtayọ_iye:Ìtayọ_iye+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(Èdè+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',bẹ̀rẹ̀_íyàwòrán)
        if Èdè=='java':
            bẹ̀rẹ̀_wínńdò=bẹ̀rẹ̀_Ìtayọ('java 창예제')
            수신하기('GUI 예제 gbaradì: 창예제'.encode(),bẹ̀rẹ̀_wínńdò)
            def ṣíra_tẹ_iye(가로,세로):
                for bọ́tìnnì in (1,0):aṣojú.sendall(struct.pack('>BBHH',5,bọ́tìnnì,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            ṣíra_tẹ_iye(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for ẹyọ_ọ̀rọ̀_iye in '한글':누름값(0x1000000|ord(ẹyọ_ọ̀rọ̀_iye));누름값(0x1000000|ord(ẹyọ_ọ̀rọ̀_iye),False)
            for 횟수 in (1,2):
                Rọ́ọ̀nù=len(대화기록);ṣíra_tẹ_iye(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Rọ́ọ̀nù)
            time.sleep(.3)
            wínńdò_íyàwòrán=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=wínńdò_íyàwòrán.crop((110,272,530,300)).tobytes()
            wínńdò_íyàwòrán.save(str(결과자료/'java-swing.png'))
            Rọ́ọ̀nù=len(대화기록);ṣíra_tẹ_iye(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Rọ́ọ̀nù)
        # Download the guest-created bytes through FTP in the same GUI VM.
        fáìlì_ìgbéwọlé_orúkọ={'java':'java.txt','c':'c.txt','python':'python.txt'}[Èdè]
        ṣẹ́ẹ̀lì('cp '+fáìlì_ìgbéwọlé_orúkọ+' /ìfọwọ́síìwé.txt')
        받은수=bytearray();fáìlì_ṣàgbélọ_Ìsomọ́.retrbinary('RETR ìfọwọ́síìwé.txt',받은수.extend);assert 받은수==예상파일.encode()
        ṣẹ́ẹ̀lì('echo preserved > 출력예제.'+('py' if Èdè=='python' else Èdè))
        assert 'EXAMPLES READY' in ṣẹ́ẹ̀lì('example '+Èdè)
        assert '\npreserved\n' in ṣẹ́ẹ̀lì('cat 출력예제.'+('py' if Èdè=='python' else Èdè))
        assert '한/영 bọ́tìnnì_iye, Shift+Space 또는 F9' in ṣẹ́ẹ̀lì('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in ṣẹ́ẹ̀lì('echo GUI NETWORK TOGETHER')
        fáìlì_ṣàgbélọ_Ìsomọ́.quit();fáìlì_ṣàgbélọ_Ìsomọ́=None;assert 'FTP stopped' in ṣẹ́ẹ̀lì('ftpd stop')
        print('PASS '+Èdè+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if fáìlì_ṣàgbélọ_Ìsomọ́:
            try:fáìlì_ṣàgbélọ_Ìsomọ́.close()
            except OSError:pass
        if aṣojú:aṣojú.close()
        Ìlànà.terminate()
        try:Ìlànà.wait(timeout=8)
        except subprocess.TimeoutExpired:Ìlànà.kill();Ìlànà.wait()
        olùyàn.close();Ìlànà.stdout.close();(결과자료/(Èdè+'-serial.log')).write_bytes(대화기록)


def Rọ́ọ̀nù():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    Àfọwọ́sí_ìjábọ̀={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Èdè in ('java','c','python'):
                test_언어(Èdè,되돌림서버항목,결과자료);Àfọwọ́sí_ìjábọ̀['languages'].append(Èdè)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(ìsọ̀rí_iye,détà.encode()) for ìsọ̀rí_iye,détà in 예상결과],되돌림서버항목.수신됨
            Àfọwọ́sí_ìjábọ̀['host_network_payloads']=[{'protocol':ìsọ̀rí_iye,'text':détà.decode()} for ìsọ̀rí_iye,détà in 되돌림서버항목.수신됨]
        Àfọwọ́sí_ìjábọ̀.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(Àfọwọ́sí_ìjábọ̀,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Rọ́ọ̀nù()
