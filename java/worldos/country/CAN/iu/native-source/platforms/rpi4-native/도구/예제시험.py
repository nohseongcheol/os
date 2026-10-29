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
from igalaujaq_takussarurli import 정확한값
from 예제되돌림서버 import 되돌림서버
from 실행 import 기준


def test_언어(pilirijjutinut_uqausiq,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Pivallianiq=subprocess.Popen(['python3',str(기준/'도구/실행.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비선택기=selectors.DefaultSelector();준비선택기.register(Pivallianiq.stdout,selectors.EVENT_READ)
    대화기록=bytearray();pijittiqtaq=None;ini_aullaaqtilli_kasuqsimaniq=None
    def 수신하기(확인표시,시작=0):
        끝위치=time.monotonic()+60
        while 확인표시 not in 대화기록[시작:]:
            if time.monotonic()>끝위치 or Pivallianiq.poll() is not None:raise AssertionError(대화기록[시작:].decode('utf-8','replace'))
            for 누름값,_ in 준비선택기.select(.1):
                titiqqat=누름값.fileobj.read(65536)
                if titiqqat:대화기록.extend(titiqqat)
        return 대화기록[시작:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(심볼,누르는중=True):pijittiqtaq.sendall(struct.pack('>BBHI',4,int(누르는중),0,심볼))
    def 시작위치(titikutaak):
        시작=len(대화기록)
        for immikkuuqtumut_nalunaikkut in titikutaak+'\n':
            심볼=0xff0d if immikkuuqtumut_nalunaikkut=='\n' else ord(immikkuuqtumut_nalunaikkut) if ord(immikkuuqtumut_nalunaikkut)<256 else 0x1000000|ord(immikkuuqtumut_nalunaikkut)
            누름값(심볼);누름값(심볼,False)
        return 시작
    def piqujijjutiliriji(titikutaak):return 수신하기(b'jkoros-native> ',시작위치(titikutaak))
    def 실행(titikutaak,예상결과):
        titiqqaq=piqujijjutiliriji(titikutaak);assert 예상결과 in titiqqaq and 'exit 0' in titiqqaq,(titikutaak,titiqqaq)
        return titiqqaq
    def 화소들():
        pijittiqtaq.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            Ataqatigiivvik_atuutilik=정확한값(pijittiqtaq,1)[0]
            if Ataqatigiivvik_atuutilik==2:continue
            if Ataqatigiivvik_atuutilik==3:
                개수=struct.unpack('>I',정확한값(pijittiqtaq,7)[3:])[0];정확한값(pijittiqtaq,개수);continue
            assert Ataqatigiivvik_atuutilik==0,Ataqatigiivvik_atuutilik
            항목수=struct.unpack('>H',정확한값(pijittiqtaq,3)[1:])[0]
            for _ in range(항목수):
                가로좌표,세로좌표,너비값,높이값,immikkuungauqtut=struct.unpack('>HHHHi',정확한값(pijittiqtaq,12));assert immikkuungauqtut==0,immikkuungauqtut
                titiqqat=정확한값(pijittiqtaq,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;turaagaq=((세로좌표+행위치)*640+가로좌표+열위치)*3
                        빛삼원색[turaagaq:turaagaq+3]=bytes((titiqqat[원본자료+2],titiqqat[원본자료+1],titiqqat[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        pijittiqtaq=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(pijittiqtaq,12)==b'RFB 003.008\n';pijittiqtaq.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(pijittiqtaq,정확한값(pijittiqtaq,1)[0]);pijittiqtaq.sendall(b'\x01');assert 정확한값(pijittiqtaq,4)==b'\0'*4
        pijittiqtaq.sendall(b'\x01');초기값=정확한값(pijittiqtaq,24);정확한값(pijittiqtaq,struct.unpack('>I',초기값[20:])[0])
        pijittiqtaq.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        pijittiqtaq.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in piqujijjutiliriji('ftpd start')
        ini_aullaaqtilli_kasuqsimaniq=ftplib.FTP();ini_aullaaqtilli_kasuqsimaniq.encoding='utf-8';ini_aullaaqtilli_kasuqsimaniq.connect('127.0.0.1',파일전송접속번호,timeout=20);ini_aullaaqtilli_kasuqsimaniq.login()
        내용자료=('GUI와 FTP 동시 사용 '+pilirijjutinut_uqausiq+' 😀\n').encode()
        ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR 함께.txt',io.BytesIO(내용자료))
        assert 내용자료.decode().strip() in piqujijjutiliriji('cat /함께.txt')
        받은수=bytearray();ini_aullaaqtilli_kasuqsimaniq.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==내용자료;ini_aullaaqtilli_kasuqsimaniq.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        nassiutili_Titiqpalliagaq=piqujijjutiliriji('ls /example')
        assert all(atiq in nassiutili_Titiqpalliagaq for atiq in ('java/','c/','python/','README.md')),nassiutili_Titiqpalliagaq
        if pilirijjutinut_uqausiq=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for aqqut,Iliniku_puinti in 꾸러미명세.items():
                piqujijjutiliriji('cp '+aqqut+' /example-check.bin')
                Ilulingit_atuutilik=bytearray();ini_aullaaqtilli_kasuqsimaniq.retrbinary('RETR example-check.bin',Ilulingit_atuutilik.extend)
                assert len(Ilulingit_atuutilik)==Iliniku_puinti['bytes'] and hashlib.sha256(Ilulingit_atuutilik).hexdigest()==Iliniku_puinti['sha256'],aqqut
            ini_aullaaqtilli_kasuqsimaniq.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binary=bytes(range(256))*64
            ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR boundary.bin',io.BytesIO(binary))
            Ilulingit_atuutilik=bytearray();ini_aullaaqtilli_kasuqsimaniq.retrbinary('RETR boundary.bin',Ilulingit_atuutilik.extend)
            assert Ilulingit_atuutilik==binary and 'boundary.bin' in ini_aullaaqtilli_kasuqsimaniq.nlst()
            piqujijjutiliriji('cp /boundary.bin /boundary-copy.bin')
            Ilulingit_atuutilik=bytearray();ini_aullaaqtilli_kasuqsimaniq.retrbinary('RETR boundary-copy.bin',Ilulingit_atuutilik.extend)
            assert Ilulingit_atuutilik==binary
            ini_aullaaqtilli_kasuqsimaniq.delete('boundary.bin');ini_aullaaqtilli_kasuqsimaniq.delete('boundary-copy.bin')
        assert '출력예제' in piqujijjutiliriji('ls /example/'+pilirijjutinut_uqausiq)
        piqujijjutiliriji('cd /example/'+pilirijjutinut_uqausiq)
        atiq_kipu={'java':'JAVA','c':'C','python':'PYTHON'}[pilirijjutinut_uqausiq]
        예상파일=atiq_kipu+' ini: 한글 titiqqat 😀\n'
        if pilirijjutinut_uqausiq=='java':
            실행('javac 출력예제.java','Compiled:');실행('java 출력예제','JAVA 출력: 안녕하세요 😀')
            실행('javac 파일예제.java','Compiled:');실행('java 파일예제',예상파일)
            실행('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_kapputigaq,되돌림서버항목.전문접속번호),'JAVA 네트워크 nalunairli_1aacb54c: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif pilirijjutinut_uqausiq=='c':
            for atiq,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('ini','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 nalunairli_1aacb54c: UDP 한글')]:
                실행('cc '+atiq+'예제.c -o 실행','Compiled native ARM64 ELF:')
                실행('./실행'+전달값,예상결과)
            실행('cc 그래픽예제.c -o 실행','Compiled native ARM64 ELF:');그림명령='./실행'
        else:
            for atiq,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('ini','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 nalunairli_1aacb54c: UDP 한글')]:
                실행('python '+atiq+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        pigiarli_titiraujarniq=시작위치(그림명령)
        titiqqaq=수신하기('그림을 확인한 Utimut_atuutilik Enter를 누르세요.\r\n'.encode(),pigiarli_titiraujarniq)
        assert atiq_kipu+' 그래픽: 빨강 초록 파랑' in titiqqaq and 'exit 0' not in titiqqaq,titiqqaq
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ini_aullaaqtilli_kasuqsimaniq.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ini_aullaaqtilli_kasuqsimaniq.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ini_aullaaqtilli_kasuqsimaniq.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            변위=(세로좌표*640+610)*3;assert tuple(빛삼원색[변위:변위+3])==색상,(pilirijjutinut_uqausiq,세로좌표,tuple(빛삼원색[변위:변위+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(pilirijjutinut_uqausiq+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',pigiarli_titiraujarniq)
        if pilirijjutinut_uqausiq=='java':
            pigiarli_igalaangujaq=시작위치('java 창예제')
            수신하기('GUI 예제 Parnalli: 창예제'.encode(),pigiarli_igalaangujaq)
            def naqilli_atuutilik(가로,세로):
                for tikkuagaq in (1,0):pijittiqtaq.sendall(struct.pack('>BBHH',5,tikkuagaq,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            naqilli_atuutilik(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for immikkuuqtuq_atuutilik in '한글':누름값(0x1000000|ord(immikkuuqtuq_atuutilik));누름값(0x1000000|ord(immikkuuqtuq_atuutilik),False)
            for 횟수 in (1,2):
                시작=len(대화기록);naqilli_atuutilik(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),시작)
            time.sleep(.3)
            igalaangujaq_titiraujarniq=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=igalaangujaq_titiraujarniq.crop((110,272,530,300)).tobytes()
            igalaangujaq_titiraujarniq.save(str(결과자료/'java-swing.png'))
            시작=len(대화기록);naqilli_atuutilik(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',시작)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ini_Iliniku_atiq={'java':'java.txt','c':'c.txt','python':'python.txt'}[pilirijjutinut_uqausiq]
        piqujijjutiliriji('cp '+ini_Iliniku_atiq+' /naammannirarli.txt')
        받은수=bytearray();ini_aullaaqtilli_kasuqsimaniq.retrbinary('RETR naammannirarli.txt',받은수.extend);assert 받은수==예상파일.encode()
        piqujijjutiliriji('echo preserved > 출력예제.'+('py' if pilirijjutinut_uqausiq=='python' else pilirijjutinut_uqausiq))
        assert 'EXAMPLES READY' in piqujijjutiliriji('example '+pilirijjutinut_uqausiq)
        assert '\npreserved\n' in piqujijjutiliriji('cat 출력예제.'+('py' if pilirijjutinut_uqausiq=='python' else pilirijjutinut_uqausiq))
        assert '한/영 naqigaq_atuutilik, Shift+Space 또는 F9' in piqujijjutiliriji('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in piqujijjutiliriji('echo GUI NETWORK TOGETHER')
        ini_aullaaqtilli_kasuqsimaniq.quit();ini_aullaaqtilli_kasuqsimaniq=None;assert 'FTP stopped' in piqujijjutiliriji('ftpd stop')
        print('PASS '+pilirijjutinut_uqausiq+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ini_aullaaqtilli_kasuqsimaniq:
            try:ini_aullaaqtilli_kasuqsimaniq.close()
            except OSError:pass
        if pijittiqtaq:pijittiqtaq.close()
        Pivallianiq.terminate()
        try:Pivallianiq.wait(timeout=8)
        except subprocess.TimeoutExpired:Pivallianiq.kill();Pivallianiq.wait()
        준비선택기.close();Pivallianiq.stdout.close();(결과자료/(pilirijjutinut_uqausiq+'-serial.log')).write_bytes(대화기록)


def 시작():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    naammannirainiq_unikkaaq={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for pilirijjutinut_uqausiq in ('java','c','python'):
                test_언어(pilirijjutinut_uqausiq,되돌림서버항목,결과자료);naammannirainiq_unikkaaq['languages'].append(pilirijjutinut_uqausiq)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(Ataqatigiivvik_atuutilik,titiqqat.encode()) for Ataqatigiivvik_atuutilik,titiqqat in 예상결과],되돌림서버항목.수신됨
            naammannirainiq_unikkaaq['host_network_payloads']=[{'protocol':Ataqatigiivvik_atuutilik,'text':titiqqat.decode()} for Ataqatigiivvik_atuutilik,titiqqat in 되돌림서버항목.수신됨]
        naammannirainiq_unikkaaq.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(naammannirainiq_unikkaaq,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':시작()
