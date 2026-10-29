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
from սեղան_տեսք import 정확한값
from 예제되돌림서버 import 되돌림서버
from կատարել_հրաման import արձակել_արմատ


def test_언어(Լեզու,되돌림서버항목,չափ_տվյալ):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Գործընթաց=subprocess.Popen(['python3',str(արձակել_արմատ/'Գործիքներ/կատարել_հրաման.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    ընտրիչ=selectors.DefaultSelector();ընտրիչ.register(Գործընթաց.stdout,selectors.EVENT_READ)
    대화기록=bytearray();սպասառու=None;նիշք_փոխանցել_կապ=None
    def 수신하기(확인표시,Գործարկել=0):
        վերջացնել_Տեղաշարժում=time.monotonic()+60
        while 확인표시 not in 대화기록[Գործարկել:]:
            if time.monotonic()>վերջացնել_Տեղաշարժում or Գործընթաց.poll() is not None:raise AssertionError(대화기록[Գործարկել:].decode('utf-8','replace'))
            for 누름값,_ in ընտրիչ.select(.1):
                տվյալ=누름값.fileobj.read(65536)
                if տվյալ:대화기록.extend(տվյալ)
        return 대화기록[Գործարկել:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(նշան_արժեք,누르는중=True):սպասառու.sendall(struct.pack('>BBHI',4,int(누르는중),0,նշան_արժեք))
    def Մեկնարկ_Տեղաշարժում(կապ):
        Գործարկել=len(대화기록)
        for գրանշանի_կոդ in կապ+'\n':
            նշան_արժեք=0xff0d if գրանշանի_կոդ=='\n' else ord(գրանշանի_կոդ) if ord(գրանշանի_կոդ)<256 else 0x1000000|ord(գրանշանի_կոդ)
            누름값(նշան_արժեք);누름값(նշան_արժեք,False)
        return Գործարկել
    def խեցի(կապ):return 수신하기(b'jkoros-native> ',Մեկնարկ_Տեղաշարժում(կապ))
    def կատարել_հրաման(կապ,예상결과):
        Տեքստ=խեցի(կապ);assert 예상결과 in Տեքստ and 'exit 0' in Տեքստ,(կապ,Տեքստ)
        return Տեքստ
    def 화소들():
        սպասառու.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            անվանակարգ_արժեք=정확한값(սպասառու,1)[0]
            if անվանակարգ_արժեք==2:continue
            if անվանակարգ_արժեք==3:
                개수=struct.unpack('>I',정확한값(սպասառու,7)[3:])[0];정확한값(սպասառու,개수);continue
            assert անվանակարգ_արժեք==0,անվանակարգ_արժեք
            항목수=struct.unpack('>H',정확한값(սպասառու,3)[1:])[0]
            for _ in range(항목수):
                x_կոորդինատ,세로좌표,너비값,높이값,գրանշանների_կազմ=struct.unpack('>HHHHi',정확한값(սպասառու,12));assert գրանշանների_կազմ==0,գրանշանների_կազմ
                տվյալ=정확한값(սպասառու,너비값*높이값*4)
                for տող_դիրք in range(높이값):
                    for սյունակ_դիրք in range(너비값):
                        원본자료=(տող_դիրք*너비값+սյունակ_դիրք)*4;թիրախ=((세로좌표+տող_դիրք)*640+x_կոորդինատ+սյունակ_դիրք)*3
                        빛삼원색[թիրախ:թիրախ+3]=bytes((տվյալ[원본자료+2],տվյալ[원본자료+1],տվյալ[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        սպասառու=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(սպասառու,12)==b'RFB 003.008\n';սպասառու.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(սպասառու,정확한값(սպասառու,1)[0]);սպասառու.sendall(b'\x01');assert 정확한값(սպասառու,4)==b'\0'*4
        սպասառու.sendall(b'\x01');초기값=정확한값(սպասառու,24);정확한값(սպասառու,struct.unpack('>I',초기값[20:])[0])
        սպասառու.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        սպասառու.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in խեցի('ftpd start')
        նիշք_փոխանցել_կապ=ftplib.FTP();նիշք_փոխանցել_կապ.encoding='utf-8';նիշք_փոխանցել_կապ.connect('127.0.0.1',파일전송접속번호,timeout=20);նիշք_փոխանցել_կապ.login()
        օգտակար_բեռնվածք_տվյալ=('GUI와 FTP 동시 사용 '+Լեզու+' 😀\n').encode()
        նիշք_փոխանցել_կապ.storbinary('STOR 함께.txt',io.BytesIO(օգտակար_բեռնվածք_տվյալ))
        assert օգտակար_բեռնվածք_տվյալ.decode().strip() in խեցի('cat /함께.txt')
        받은수=bytearray();նիշք_փոխանցել_կապ.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==օգտակար_բեռնվածք_տվյալ;նիշք_փոխանցել_կապ.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        ուղարկել_Ցուցակ=խեցի('ls /example')
        assert all(Անուն in ուղարկել_Ցուցակ for Անուն in ('java/','c/','python/','README.md')),ուղարկել_Ցուցակ
        if Լեզու=='java':
            꾸러미명세=json.loads((արձակել_արմատ/'build/examples/manifest.json').read_text())
            for Ճանապարհ,մուտքագրում_կետ in 꾸러미명세.items():
                խեցի('cp '+Ճանապարհ+' /example-check.bin')
                Բովանդակություն_արժեք=bytearray();նիշք_փոխանցել_կապ.retrbinary('RETR example-check.bin',Բովանդակություն_արժեք.extend)
                assert len(Բովանդակություն_արժեք)==մուտքագրում_կետ['bytes'] and hashlib.sha256(Բովանդակություն_արժեք).hexdigest()==մուտքագրում_կետ['sha256'],Ճանապարհ
            նիշք_փոխանցել_կապ.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            երկուական=bytes(range(256))*64
            նիշք_փոխանցել_կապ.storbinary('STOR boundary.bin',io.BytesIO(երկուական))
            Բովանդակություն_արժեք=bytearray();նիշք_փոխանցել_կապ.retrbinary('RETR boundary.bin',Բովանդակություն_արժեք.extend)
            assert Բովանդակություն_արժեք==երկուական and 'boundary.bin' in նիշք_փոխանցել_կապ.nlst()
            խեցի('cp /boundary.bin /boundary-copy.bin')
            Բովանդակություն_արժեք=bytearray();նիշք_փոխանցել_կապ.retrbinary('RETR boundary-copy.bin',Բովանդակություն_արժեք.extend)
            assert Բովանդակություն_արժեք==երկուական
            նիշք_փոխանցել_կապ.delete('boundary.bin');նիշք_փոխանցել_կապ.delete('boundary-copy.bin')
        assert '출력예제' in խեցի('ls /example/'+Լեզու)
        խեցի('cd /example/'+Լեզու)
        անուն_աղյուսակ={'java':'JAVA','c':'C','python':'PYTHON'}[Լեզու]
        예상파일=անուն_աղյուսակ+' Ֆայլ: 한글 տվյալ 😀\n'
        if Լեզու=='java':
            կատարել_հրաման('javac 출력예제.java','Compiled:');կատարել_հրաման('java 출력예제','JAVA Ելք: 안녕하세요 😀')
            կատարել_հրաման('javac 파일예제.java','Compiled:');կատարել_հրաման('java 파일예제',예상파일)
            կատարել_հրաման('java 네트워크예제 {} {}'.format(되돌림서버항목.Փոխանցման_կառավարման_հաղորդակարգ_միացք,되돌림서버항목.전문접속번호),'JAVA 네트워크 հաստատել: TCP UDP 한글')
            պատկերանյութ_հրաման='java 그래픽예제'
        elif Լեզու=='c':
            for Անուն,전달값,예상결과 in [('Ելք','', 'C Ելք: 안녕하세요 😀'),('Ֆայլ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 հաստատել: UDP 한글')]:
                կատարել_հրաման('cc '+Անուն+'예제.c -o կատարել_հրաման','Compiled native ARM64 ELF:')
                կատարել_հրաման('./կատարել_հրաման'+전달값,예상결과)
            կատարել_հրաման('cc 그래픽예제.c -o կատարել_հրաման','Compiled native ARM64 ELF:');պատկերանյութ_հրաման='./կատարել_հրաման'
        else:
            for Անուն,전달값,예상결과 in [('Ելք','','PYTHON Ելք: 안녕하세요 😀'),('Ֆայլ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 հաստատել: UDP 한글')]:
                կատարել_հրաման('python '+Անուն+'예제.py'+전달값,예상결과)
            պատկերանյութ_հրաման='python 그래픽예제.py'
        Մեկնարկ_նկար=Մեկնարկ_Տեղաշարժում(պատկերանյութ_հրաման)
        Տեքստ=수신하기('그림을 확인한 Հետ_արժեք Enter를 누르세요.\r\n'.encode(),Մեկնարկ_նկար)
        assert անուն_աղյուսակ+' 그래픽: 빨강 초록 파랑' in Տեքստ and 'exit 0' not in Տեքստ,Տեքստ
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        նիշք_փոխանցել_կապ.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();նիշք_փոխանցել_կապ.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';նիշք_փոխանցել_կապ.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Տեղաշարժում_արժեք=(세로좌표*640+610)*3;assert tuple(빛삼원색[Տեղաշարժում_արժեք:Տեղաշարժում_արժեք+3])==색상,(Լեզու,세로좌표,tuple(빛삼원색[Տեղաշարժում_արժեք:Տեղաշարժում_արժեք+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(չափ_տվյալ/(Լեզու+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Մեկնարկ_նկար)
        if Լեզու=='java':
            Մեկնարկ_պատուհան=Մեկնարկ_Տեղաշարժում('java 창예제')
            수신하기('GUI 예제 Պատրաստել: 창예제'.encode(),Մեկնարկ_պատուհան)
            def կտտացնել_արժեք(가로,Ուղղահայաց_դիրք):
                for կոճակ in (1,0):սպասառու.sendall(struct.pack('>BBHH',5,կոճակ,가로,Ուղղահայաց_դիրք))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            կտտացնել_արժեք(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for գրանշան_արժեք in '한글':누름값(0x1000000|ord(գրանշան_արժեք));누름값(0x1000000|ord(գրանշան_արժեք),False)
            for 횟수 in (1,2):
                Գործարկել=len(대화기록);կտտացնել_արժեք(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Գործարկել)
            time.sleep(.3)
            պատուհան_նկար=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=պատուհան_նկար.crop((110,272,530,300)).tobytes()
            պատուհան_նկար.save(str(չափ_տվյալ/'java-swing.png'))
            Գործարկել=len(대화기록);կտտացնել_արժեք(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Գործարկել)
        # Download the guest-created bytes through FTP in the same GUI VM.
        նիշք_մուտքագրում_անուն={'java':'java.txt','c':'c.txt','python':'python.txt'}[Լեզու]
        խեցի('cp '+նիշք_մուտքագրում_անուն+' /վավերացնել.txt')
        받은수=bytearray();նիշք_փոխանցել_կապ.retrbinary('RETR վավերացնել.txt',받은수.extend);assert 받은수==예상파일.encode()
        խեցի('echo preserved > 출력예제.'+('py' if Լեզու=='python' else Լեզու))
        assert 'EXAMPLES READY' in խեցի('example '+Լեզու)
        assert '\npreserved\n' in խեցի('cat 출력예제.'+('py' if Լեզու=='python' else Լեզու))
        assert '한/영 ստեղն_արժեք, Shift+Space 또는 F9' in խեցի('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in խեցի('echo GUI NETWORK TOGETHER')
        նիշք_փոխանցել_կապ.quit();նիշք_փոխանցել_կապ=None;assert 'FTP stopped' in խեցի('ftpd stop')
        print('PASS '+Լեզու+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if նիշք_փոխանցել_կապ:
            try:նիշք_փոխանցել_կապ.close()
            except OSError:pass
        if սպասառու:սպասառու.close()
        Գործընթաց.terminate()
        try:Գործընթաց.wait(timeout=8)
        except subprocess.TimeoutExpired:Գործընթաց.kill();Գործընթաց.wait()
        ընտրիչ.close();Գործընթաց.stdout.close();(չափ_տվյալ/(Լեզու+'-serial.log')).write_bytes(대화기록)


def Գործարկել():
    չափ_տվյալ=արձակել_արմատ/'build/verification/examples';չափ_տվյալ.mkdir(parents=True,exist_ok=True)
    վավերացում_զեկույց={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((արձակել_արմատ/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Լեզու in ('java','c','python'):
                test_언어(Լեզու,되돌림서버항목,չափ_տվյալ);վավերացում_զեկույց['languages'].append(Լեզու)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(անվանակարգ_արժեք,տվյալ.encode()) for անվանակարգ_արժեք,տվյալ in 예상결과],되돌림서버항목.수신됨
            վավերացում_զեկույց['host_network_payloads']=[{'protocol':անվանակարգ_արժեք,'text':տվյալ.decode()} for անվանակարգ_արժեք,տվյալ in 되돌림서버항목.수신됨]
        վավերացում_զեկույց.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(չափ_տվյալ/'report.json').write_text(json.dumps(վավերացում_զեկույց,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Գործարկել()
