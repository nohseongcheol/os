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
from destof_s import 정확한값
from 예제되돌림서버 import 되돌림서버
from gudanar_Umarni import 기준


def test_언어(yare,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));Fayil_Gusar_da_lambar_kafa=임시자원.getsockname()[1]
    haryar_aikin_na_ura=subprocess.Popen(['python3',str(기준/'Kaya/gudanar_Umarni.py'),'--desktop','--network','--port','0','--ftp-port',str(Fayil_Gusar_da_lambar_kafa)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    mai_zabe=selectors.DefaultSelector();mai_zabe.register(haryar_aikin_na_ura.stdout,selectors.EVENT_READ)
    대화기록=bytearray();abokin_hulda=None;Fayil_Gusar_da_haɗi=None
    def 수신하기(확인표시,Tafiyar_da=0):
        Ƙarshe_Sassautawa=time.monotonic()+60
        while 확인표시 not in 대화기록[Tafiyar_da:]:
            if time.monotonic()>Ƙarshe_Sassautawa or haryar_aikin_na_ura.poll() is not None:raise AssertionError(대화기록[Tafiyar_da:].decode('utf-8','replace'))
            for 누름값,_ in mai_zabe.select(.1):
                Tarin_bayani=누름값.fileobj.read(65536)
                if Tarin_bayani:대화기록.extend(Tarin_bayani)
        return 대화기록[Tafiyar_da:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(alama_Daraja,누르는중=True):abokin_hulda.sendall(struct.pack('>BBHI',4,int(누르는중),0,alama_Daraja))
    def Fara_Sassautawa(Layi):
        Tafiyar_da=len(대화기록)
        for Lambar_sirrin_harafi in Layi+'\n':
            alama_Daraja=0xff0d if Lambar_sirrin_harafi=='\n' else ord(Lambar_sirrin_harafi) if ord(Lambar_sirrin_harafi)<256 else 0x1000000|ord(Lambar_sirrin_harafi)
            누름값(alama_Daraja);누름값(alama_Daraja,False)
        return Tafiyar_da
    def Mai_fayyace_umani(Layi):return 수신하기(b'jkoros-native> ',Fara_Sassautawa(Layi))
    def gudanar_Umarni(Layi,예상결과):
        SMS=Mai_fayyace_umani(Layi);assert 예상결과 in SMS and 'exit 0' in SMS,(Layi,SMS)
        return SMS
    def 화소들():
        abokin_hulda.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            ɓangare_Daraja=정확한값(abokin_hulda,1)[0]
            if ɓangare_Daraja==2:continue
            if ɓangare_Daraja==3:
                개수=struct.unpack('>I',정확한값(abokin_hulda,7)[3:])[0];정확한값(abokin_hulda,개수);continue
            assert ɓangare_Daraja==0,ɓangare_Daraja
            항목수=struct.unpack('>H',정확한값(abokin_hulda,3)[1:])[0]
            for _ in range(항목수):
                gamayyar_x,Maɓallin_Y_Mai_tsarawa,너비값,높이값,Ƙunshin_alƙalumma=struct.unpack('>HHHHi',정확한값(abokin_hulda,12));assert Ƙunshin_alƙalumma==0,Ƙunshin_alƙalumma
                Tarin_bayani=정확한값(abokin_hulda,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;tageti=((Maɓallin_Y_Mai_tsarawa+행위치)*640+gamayyar_x+열위치)*3
                        빛삼원색[tageti:tageti+3]=bytes((Tarin_bayani[원본자료+2],Tarin_bayani[원본자료+1],Tarin_bayani[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        lambar_kafa=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        abokin_hulda=socket.create_connection(('127.0.0.1',lambar_kafa),timeout=10)
        assert 정확한값(abokin_hulda,12)==b'RFB 003.008\n';abokin_hulda.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(abokin_hulda,정확한값(abokin_hulda,1)[0]);abokin_hulda.sendall(b'\x01');assert 정확한값(abokin_hulda,4)==b'\0'*4
        abokin_hulda.sendall(b'\x01');초기값=정확한값(abokin_hulda,24);정확한값(abokin_hulda,struct.unpack('>I',초기값[20:])[0])
        abokin_hulda.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        abokin_hulda.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in Mai_fayyace_umani('ftpd start')
        Fayil_Gusar_da_haɗi=ftplib.FTP();Fayil_Gusar_da_haɗi.encoding='utf-8';Fayil_Gusar_da_haɗi.connect('127.0.0.1',Fayil_Gusar_da_lambar_kafa,timeout=20);Fayil_Gusar_da_haɗi.login()
        Kumshinbayanai_Tarin_bayani=('GUI와 FTP 동시 사용 '+yare+' 😀\n').encode()
        Fayil_Gusar_da_haɗi.storbinary('STOR 함께.txt',io.BytesIO(Kumshinbayanai_Tarin_bayani))
        assert Kumshinbayanai_Tarin_bayani.decode().strip() in Mai_fayyace_umani('cat /함께.txt')
        받은수=bytearray();Fayil_Gusar_da_haɗi.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==Kumshinbayanai_Tarin_bayani;Fayil_Gusar_da_haɗi.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        Aika_Jeri=Mai_fayyace_umani('ls /example')
        assert all(Suna in Aika_Jeri for Suna in ('java/','c/','python/','README.md')),Aika_Jeri
        if yare=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for Hanyar_shiga,Mashigar_bayanai_maki in 꾸러미명세.items():
                Mai_fayyace_umani('cp '+Hanyar_shiga+' /example-check.bin')
                kunshiya_Daraja=bytearray();Fayil_Gusar_da_haɗi.retrbinary('RETR example-check.bin',kunshiya_Daraja.extend)
                assert len(kunshiya_Daraja)==Mashigar_bayanai_maki['bytes'] and hashlib.sha256(kunshiya_Daraja).hexdigest()==Mashigar_bayanai_maki['sha256'],Hanyar_shiga
            Fayil_Gusar_da_haɗi.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            Mai_bangare_biyu=bytes(range(256))*64
            Fayil_Gusar_da_haɗi.storbinary('STOR boundary.bin',io.BytesIO(Mai_bangare_biyu))
            kunshiya_Daraja=bytearray();Fayil_Gusar_da_haɗi.retrbinary('RETR boundary.bin',kunshiya_Daraja.extend)
            assert kunshiya_Daraja==Mai_bangare_biyu and 'boundary.bin' in Fayil_Gusar_da_haɗi.nlst()
            Mai_fayyace_umani('cp /boundary.bin /boundary-copy.bin')
            kunshiya_Daraja=bytearray();Fayil_Gusar_da_haɗi.retrbinary('RETR boundary-copy.bin',kunshiya_Daraja.extend)
            assert kunshiya_Daraja==Mai_bangare_biyu
            Fayil_Gusar_da_haɗi.delete('boundary.bin');Fayil_Gusar_da_haɗi.delete('boundary-copy.bin')
        assert '출력예제' in Mai_fayyace_umani('ls /example/'+yare)
        Mai_fayyace_umani('cd /example/'+yare)
        Suna_tebur={'java':'JAVA','c':'C','python':'PYTHON'}[yare]
        예상파일=Suna_tebur+' Fayil: 한글 Tarin_bayani 😀\n'
        if yare=='java':
            gudanar_Umarni('javac 출력예제.java','Compiled:');gudanar_Umarni('java 출력예제','JAVA 출력: 안녕하세요 😀')
            gudanar_Umarni('javac 파일예제.java','Compiled:');gudanar_Umarni('java 파일예제',예상파일)
            gudanar_Umarni('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_fot,되돌림서버항목.전문접속번호),'JAVA 네트워크 Tabbatar_da: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif yare=='c':
            for Suna,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Fayil','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 Tabbatar_da: UDP 한글')]:
                gudanar_Umarni('cc '+Suna+'예제.c -o gudanar_Umarni','Compiled native ARM64 ELF:')
                gudanar_Umarni('./gudanar_Umarni'+전달값,예상결과)
            gudanar_Umarni('cc 그래픽예제.c -o gudanar_Umarni','Compiled native ARM64 ELF:');그림명령='./gudanar_Umarni'
        else:
            for Suna,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Fayil','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 Tabbatar_da: UDP 한글')]:
                gudanar_Umarni('python '+Suna+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        Fara_zane=Fara_Sassautawa(그림명령)
        SMS=수신하기('그림을 확인한 Baya_Daraja Enter를 누르세요.\r\n'.encode(),Fara_zane)
        assert Suna_tebur+' 그래픽: 빨강 초록 파랑' in SMS and 'exit 0' not in SMS,SMS
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        Fayil_Gusar_da_haɗi.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();Fayil_Gusar_da_haɗi.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';Fayil_Gusar_da_haɗi.delete('도중.txt')
        빛삼원색=화소들()
        for Maɓallin_Y_Mai_tsarawa,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Sassautawa_Daraja=(Maɓallin_Y_Mai_tsarawa*640+610)*3;assert tuple(빛삼원색[Sassautawa_Daraja:Sassautawa_Daraja+3])==색상,(yare,Maɓallin_Y_Mai_tsarawa,tuple(빛삼원색[Sassautawa_Daraja:Sassautawa_Daraja+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(yare+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Fara_zane)
        if yare=='java':
            Fara_taga=Fara_Sassautawa('java 창예제')
            수신하기('GUI 예제 Shirya: 창예제'.encode(),Fara_taga)
            def Danna_Daraja(가로,세로):
                for maɓali in (1,0):abokin_hulda.sendall(struct.pack('>BBHH',5,maɓali,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            Danna_Daraja(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for Harafi_Daraja in '한글':누름값(0x1000000|ord(Harafi_Daraja));누름값(0x1000000|ord(Harafi_Daraja),False)
            for 횟수 in (1,2):
                Tafiyar_da=len(대화기록);Danna_Daraja(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Tafiyar_da)
            time.sleep(.3)
            taga_zane=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=taga_zane.crop((110,272,530,300)).tobytes()
            taga_zane.save(str(결과자료/'java-swing.png'))
            Tafiyar_da=len(대화기록);Danna_Daraja(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Tafiyar_da)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Fayil_Mashigar_bayanai_Suna={'java':'java.txt','c':'c.txt','python':'python.txt'}[yare]
        Mai_fayyace_umani('cp '+Fayil_Mashigar_bayanai_Suna+' /inganta.txt')
        받은수=bytearray();Fayil_Gusar_da_haɗi.retrbinary('RETR inganta.txt',받은수.extend);assert 받은수==예상파일.encode()
        Mai_fayyace_umani('echo preserved > 출력예제.'+('py' if yare=='python' else yare))
        assert 'EXAMPLES READY' in Mai_fayyace_umani('example '+yare)
        assert '\npreserved\n' in Mai_fayyace_umani('cat 출력예제.'+('py' if yare=='python' else yare))
        assert '한/영 Makulli_Daraja, Shift+Space 또는 F9' in Mai_fayyace_umani('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in Mai_fayyace_umani('echo GUI NETWORK TOGETHER')
        Fayil_Gusar_da_haɗi.quit();Fayil_Gusar_da_haɗi=None;assert 'FTP stopped' in Mai_fayyace_umani('ftpd stop')
        print('PASS '+yare+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if Fayil_Gusar_da_haɗi:
            try:Fayil_Gusar_da_haɗi.close()
            except OSError:pass
        if abokin_hulda:abokin_hulda.close()
        haryar_aikin_na_ura.terminate()
        try:haryar_aikin_na_ura.wait(timeout=8)
        except subprocess.TimeoutExpired:haryar_aikin_na_ura.kill();haryar_aikin_na_ura.wait()
        mai_zabe.close();haryar_aikin_na_ura.stdout.close();(결과자료/(yare+'-serial.log')).write_bytes(대화기록)


def Tafiyar_da():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    amincewa_Rahoto={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for yare in ('java','c','python'):
                test_언어(yare,되돌림서버항목,결과자료);amincewa_Rahoto['languages'].append(yare)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(ɓangare_Daraja,Tarin_bayani.encode()) for ɓangare_Daraja,Tarin_bayani in 예상결과],되돌림서버항목.수신됨
            amincewa_Rahoto['host_network_payloads']=[{'protocol':ɓangare_Daraja,'text':Tarin_bayani.decode()} for ɓangare_Daraja,Tarin_bayani in 되돌림서버항목.수신됨]
        amincewa_Rahoto.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(amincewa_Rahoto,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Tafiyar_da()
