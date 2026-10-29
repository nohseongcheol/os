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
from ideskithophu_buka import 정확한값
from 예제되돌림서버 import 되돌림서버
from yenza_umyalo import 기준


def test_언어(Ulimi,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Inqubo=subprocess.Popen(['python3',str(기준/'Amathuluzi/yenza_umyalo.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    isiqoki=selectors.DefaultSelector();isiqoki.register(Inqubo.stdout,selectors.EVENT_READ)
    대화기록=bytearray();iklayenti=None;ifayela_dlulisa_uxhumano=None
    def 수신하기(확인표시,Sebenzisa=0):
        yekisa_I_ofisethi=time.monotonic()+60
        while 확인표시 not in 대화기록[Sebenzisa:]:
            if time.monotonic()>yekisa_I_ofisethi or Inqubo.poll() is not None:raise AssertionError(대화기록[Sebenzisa:].decode('utf-8','replace'))
            for 누름값,_ in isiqoki.select(.1):
                imininingwane=누름값.fileobj.read(65536)
                if imininingwane:대화기록.extend(imininingwane)
        return 대화기록[Sebenzisa:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(uphawu_inani,누르는중=True):iklayenti.sendall(struct.pack('>BBHI',4,int(누르는중),0,uphawu_inani))
    def qala_I_ofisethi(umugqa):
        Sebenzisa=len(대화기록)
        for ikhodi_yohlamvu in umugqa+'\n':
            uphawu_inani=0xff0d if ikhodi_yohlamvu=='\n' else ord(ikhodi_yohlamvu) if ord(ikhodi_yohlamvu)<256 else 0x1000000|ord(ikhodi_yohlamvu)
            누름값(uphawu_inani);누름값(uphawu_inani,False)
        return Sebenzisa
    def isihumushi_miyalelo(umugqa):return 수신하기(b'jkoros-native> ',qala_I_ofisethi(umugqa))
    def yenza_umyalo(umugqa,예상결과):
        Itekisi=isihumushi_miyalelo(umugqa);assert 예상결과 in Itekisi and 'exit 0' in Itekisi,(umugqa,Itekisi)
        return Itekisi
    def 화소들():
        iklayenti.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            umunxa_inani=정확한값(iklayenti,1)[0]
            if umunxa_inani==2:continue
            if umunxa_inani==3:
                개수=struct.unpack('>I',정확한값(iklayenti,7)[3:])[0];정확한값(iklayenti,개수);continue
            assert umunxa_inani==0,umunxa_inani
            항목수=struct.unpack('>H',정확한값(iklayenti,3)[1:])[0]
            for _ in range(항목수):
                okuxhumanisa_u_x,세로좌표,너비값,높이값,iqoqo_lezinhlamvusimo=struct.unpack('>HHHHi',정확한값(iklayenti,12));assert iqoqo_lezinhlamvusimo==0,iqoqo_lezinhlamvusimo
                imininingwane=정확한값(iklayenti,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;impokophelo=((세로좌표+행위치)*640+okuxhumanisa_u_x+열위치)*3
                        빛삼원색[impokophelo:impokophelo+3]=bytes((imininingwane[원본자료+2],imininingwane[원본자료+1],imininingwane[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        iklayenti=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(iklayenti,12)==b'RFB 003.008\n';iklayenti.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(iklayenti,정확한값(iklayenti,1)[0]);iklayenti.sendall(b'\x01');assert 정확한값(iklayenti,4)==b'\0'*4
        iklayenti.sendall(b'\x01');초기값=정확한값(iklayenti,24);정확한값(iklayenti,struct.unpack('>I',초기값[20:])[0])
        iklayenti.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        iklayenti.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in isihumushi_miyalelo('ftpd start')
        ifayela_dlulisa_uxhumano=ftplib.FTP();ifayela_dlulisa_uxhumano.encoding='utf-8';ifayela_dlulisa_uxhumano.connect('127.0.0.1',파일전송접속번호,timeout=20);ifayela_dlulisa_uxhumano.login()
        ukulayisha_okukhokhelwayo_imininingwane=('GUI와 FTP 동시 사용 '+Ulimi+' 😀\n').encode()
        ifayela_dlulisa_uxhumano.storbinary('STOR 함께.txt',io.BytesIO(ukulayisha_okukhokhelwayo_imininingwane))
        assert ukulayisha_okukhokhelwayo_imininingwane.decode().strip() in isihumushi_miyalelo('cat /함께.txt')
        받은수=bytearray();ifayela_dlulisa_uxhumano.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==ukulayisha_okukhokhelwayo_imininingwane;ifayela_dlulisa_uxhumano.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        Thumela_Uhlu=isihumushi_miyalelo('ls /example')
        assert all(Igama in Thumela_Uhlu for Igama in ('java/','c/','python/','README.md')),Thumela_Uhlu
        if Ulimi=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for Indlela_2,okufakwayo_iphoyinti in 꾸러미명세.items():
                isihumushi_miyalelo('cp '+Indlela_2+' /example-check.bin')
                Okuqukethwe_inani=bytearray();ifayela_dlulisa_uxhumano.retrbinary('RETR example-check.bin',Okuqukethwe_inani.extend)
                assert len(Okuqukethwe_inani)==okufakwayo_iphoyinti['bytes'] and hashlib.sha256(Okuqukethwe_inani).hexdigest()==okufakwayo_iphoyinti['sha256'],Indlela_2
            ifayela_dlulisa_uxhumano.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            unambambili=bytes(range(256))*64
            ifayela_dlulisa_uxhumano.storbinary('STOR boundary.bin',io.BytesIO(unambambili))
            Okuqukethwe_inani=bytearray();ifayela_dlulisa_uxhumano.retrbinary('RETR boundary.bin',Okuqukethwe_inani.extend)
            assert Okuqukethwe_inani==unambambili and 'boundary.bin' in ifayela_dlulisa_uxhumano.nlst()
            isihumushi_miyalelo('cp /boundary.bin /boundary-copy.bin')
            Okuqukethwe_inani=bytearray();ifayela_dlulisa_uxhumano.retrbinary('RETR boundary-copy.bin',Okuqukethwe_inani.extend)
            assert Okuqukethwe_inani==unambambili
            ifayela_dlulisa_uxhumano.delete('boundary.bin');ifayela_dlulisa_uxhumano.delete('boundary-copy.bin')
        assert '출력예제' in isihumushi_miyalelo('ls /example/'+Ulimi)
        isihumushi_miyalelo('cd /example/'+Ulimi)
        igama_ithebula={'java':'JAVA','c':'C','python':'PYTHON'}[Ulimi]
        예상파일=igama_ithebula+' Ihele: 한글 imininingwane 😀\n'
        if Ulimi=='java':
            yenza_umyalo('javac 출력예제.java','Compiled:');yenza_umyalo('java 출력예제','JAVA 출력: 안녕하세요 😀')
            yenza_umyalo('javac 파일예제.java','Compiled:');yenza_umyalo('java 파일예제',예상파일)
            yenza_umyalo('java 네트워크예제 {} {}'.format(되돌림서버항목.i_TCP_intuba,되돌림서버항목.전문접속번호),'JAVA 네트워크 qiniseka: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif Ulimi=='c':
            for Igama,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Ihele','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 qiniseka: UDP 한글')]:
                yenza_umyalo('cc '+Igama+'예제.c -o yenza_umyalo','Compiled native ARM64 ELF:')
                yenza_umyalo('./yenza_umyalo'+전달값,예상결과)
            yenza_umyalo('cc 그래픽예제.c -o yenza_umyalo','Compiled native ARM64 ELF:');그림명령='./yenza_umyalo'
        else:
            for Igama,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Ihele','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 qiniseka: UDP 한글')]:
                yenza_umyalo('python '+Igama+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        qala_umdwebo=qala_I_ofisethi(그림명령)
        Itekisi=수신하기('그림을 확인한 Impindamuva_inani Enter를 누르세요.\r\n'.encode(),qala_umdwebo)
        assert igama_ithebula+' 그래픽: 빨강 초록 파랑' in Itekisi and 'exit 0' not in Itekisi,Itekisi
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ifayela_dlulisa_uxhumano.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ifayela_dlulisa_uxhumano.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ifayela_dlulisa_uxhumano.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            I_ofisethi_inani=(세로좌표*640+610)*3;assert tuple(빛삼원색[I_ofisethi_inani:I_ofisethi_inani+3])==색상,(Ulimi,세로좌표,tuple(빛삼원색[I_ofisethi_inani:I_ofisethi_inani+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(Ulimi+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',qala_umdwebo)
        if Ulimi=='java':
            qala_ifasitela=qala_I_ofisethi('java 창예제')
            수신하기('GUI 예제 Hlela: 창예제'.encode(),qala_ifasitela)
            def qhafaza_inani(가로,세로):
                for inkinobho in (1,0):iklayenti.sendall(struct.pack('>BBHH',5,inkinobho,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            qhafaza_inani(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for uhlamvusimo_inani in '한글':누름값(0x1000000|ord(uhlamvusimo_inani));누름값(0x1000000|ord(uhlamvusimo_inani),False)
            for 횟수 in (1,2):
                Sebenzisa=len(대화기록);qhafaza_inani(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Sebenzisa)
            time.sleep(.3)
            ifasitela_umdwebo=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=ifasitela_umdwebo.crop((110,272,530,300)).tobytes()
            ifasitela_umdwebo.save(str(결과자료/'java-swing.png'))
            Sebenzisa=len(대화기록);qhafaza_inani(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Sebenzisa)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ifayela_okufakwayo_igama={'java':'java.txt','c':'c.txt','python':'python.txt'}[Ulimi]
        isihumushi_miyalelo('cp '+ifayela_okufakwayo_igama+' /qinisekisa.txt')
        받은수=bytearray();ifayela_dlulisa_uxhumano.retrbinary('RETR qinisekisa.txt',받은수.extend);assert 받은수==예상파일.encode()
        isihumushi_miyalelo('echo preserved > 출력예제.'+('py' if Ulimi=='python' else Ulimi))
        assert 'EXAMPLES READY' in isihumushi_miyalelo('example '+Ulimi)
        assert '\npreserved\n' in isihumushi_miyalelo('cat 출력예제.'+('py' if Ulimi=='python' else Ulimi))
        assert '한/영 inkomba_inani, Shift+Space 또는 F9' in isihumushi_miyalelo('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in isihumushi_miyalelo('echo GUI NETWORK TOGETHER')
        ifayela_dlulisa_uxhumano.quit();ifayela_dlulisa_uxhumano=None;assert 'FTP stopped' in isihumushi_miyalelo('ftpd stop')
        print('PASS '+Ulimi+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ifayela_dlulisa_uxhumano:
            try:ifayela_dlulisa_uxhumano.close()
            except OSError:pass
        if iklayenti:iklayenti.close()
        Inqubo.terminate()
        try:Inqubo.wait(timeout=8)
        except subprocess.TimeoutExpired:Inqubo.kill();Inqubo.wait()
        isiqoki.close();Inqubo.stdout.close();(결과자료/(Ulimi+'-serial.log')).write_bytes(대화기록)


def Sebenzisa():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    ukufakazisa_umbiko={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Ulimi in ('java','c','python'):
                test_언어(Ulimi,되돌림서버항목,결과자료);ukufakazisa_umbiko['languages'].append(Ulimi)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(umunxa_inani,imininingwane.encode()) for umunxa_inani,imininingwane in 예상결과],되돌림서버항목.수신됨
            ukufakazisa_umbiko['host_network_payloads']=[{'protocol':umunxa_inani,'text':imininingwane.decode()} for umunxa_inani,imininingwane in 되돌림서버항목.수신됨]
        ukufakazisa_umbiko.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(ukufakazisa_umbiko,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Sebenzisa()
