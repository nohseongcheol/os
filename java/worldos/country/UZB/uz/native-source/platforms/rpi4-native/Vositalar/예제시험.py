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
from ishchi_stol_ko_rinish import EXACT_VALUE
from 예제되돌림서버 import 되돌림서버
from bajarmoq_buyruq import Project_ildiz


def test_언어(Til,되돌림서버항목,o_lchov_ma_lumotlar):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Jarayon=subprocess.Popen(['python3',str(Project_ildiz/'Vositalar/bajarmoq_buyruq.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    tanlagich=selectors.DefaultSelector();tanlagich.register(Jarayon.stdout,selectors.EVENT_READ)
    대화기록=bytearray();mijoz=None;fayl_uzatish_aloqa=None
    def 수신하기(확인표시,Bajarish=0):
        to_xtatmoq_OFFSET=time.monotonic()+60
        while 확인표시 not in 대화기록[Bajarish:]:
            if time.monotonic()>to_xtatmoq_OFFSET or Jarayon.poll() is not None:raise AssertionError(대화기록[Bajarish:].decode('utf-8','replace'))
            for 누름값,_ in tanlagich.select(.1):
                ma_lumotlar=누름값.fileobj.read(65536)
                if ma_lumotlar:대화기록.extend(ma_lumotlar)
        return 대화기록[Bajarish:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(ramz_VALUE,누르는중=True):mijoz.sendall(struct.pack('>BBHI',4,int(누르는중),0,ramz_VALUE))
    def Start_OFFSET(satr):
        Bajarish=len(대화기록)
        for belgi_kodi in satr+'\n':
            ramz_VALUE=0xff0d if belgi_kodi=='\n' else ord(belgi_kodi) if ord(belgi_kodi)<256 else 0x1000000|ord(belgi_kodi)
            누름값(ramz_VALUE);누름값(ramz_VALUE,False)
        return Bajarish
    def qobiq(satr):return 수신하기(b'jkoros-native> ',Start_OFFSET(satr))
    def bajarmoq_buyruq(satr,예상결과):
        Matn=qobiq(satr);assert 예상결과 in Matn and 'exit 0' in Matn,(satr,Matn)
        return Matn
    def 화소들():
        mijoz.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            toifa_VALUE=EXACT_VALUE(mijoz,1)[0]
            if toifa_VALUE==2:continue
            if toifa_VALUE==3:
                element_COUNT=struct.unpack('>I',EXACT_VALUE(mijoz,7)[3:])[0];EXACT_VALUE(mijoz,element_COUNT);continue
            assert toifa_VALUE==0,toifa_VALUE
            kiritish_COUNT=struct.unpack('>H',EXACT_VALUE(mijoz,3)[1:])[0]
            for _ in range(kiritish_COUNT):
                x_koordinata,Y_tugmasi_koordinat,너비값,높이값,belgilar_to_plami=struct.unpack('>HHHHi',EXACT_VALUE(mijoz,12));assert belgilar_to_plami==0,belgilar_to_plami
                ma_lumotlar=EXACT_VALUE(mijoz,너비값*높이값*4)
                for ROW_holat in range(높이값):
                    for ustun_holat in range(너비값):
                        원본자료=(ROW_holat*너비값+ustun_holat)*4;nishon=((Y_tugmasi_koordinat+ROW_holat)*640+x_koordinata+ustun_holat)*3
                        빛삼원색[nishon:nishon+3]=bytes((ma_lumotlar[원본자료+2],ma_lumotlar[원본자료+1],ma_lumotlar[원본자료]))
            if kiritish_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        mijoz=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert EXACT_VALUE(mijoz,12)==b'RFB 003.008\n';mijoz.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(mijoz,EXACT_VALUE(mijoz,1)[0]);mijoz.sendall(b'\x01');assert EXACT_VALUE(mijoz,4)==b'\0'*4
        mijoz.sendall(b'\x01');초기값=EXACT_VALUE(mijoz,24);EXACT_VALUE(mijoz,struct.unpack('>I',초기값[20:])[0])
        mijoz.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        mijoz.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in qobiq('ftpd start')
        fayl_uzatish_aloqa=ftplib.FTP();fayl_uzatish_aloqa.encoding='utf-8';fayl_uzatish_aloqa.connect('127.0.0.1',파일전송접속번호,timeout=20);fayl_uzatish_aloqa.login()
        foydali_yuklanma_ma_lumotlar=('GUI와 FTP 동시 사용 '+Til+' 😀\n').encode()
        fayl_uzatish_aloqa.storbinary('STOR 함께.txt',io.BytesIO(foydali_yuklanma_ma_lumotlar))
        assert foydali_yuklanma_ma_lumotlar.decode().strip() in qobiq('cat /함께.txt')
        RECEIVED_COUNT=bytearray();fayl_uzatish_aloqa.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==foydali_yuklanma_ma_lumotlar;fayl_uzatish_aloqa.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        yuborish_Ro_yxat=qobiq('ls /example')
        assert all(Nomi in yuborish_Ro_yxat for Nomi in ('java/','c/','python/','README.md')),yuborish_Ro_yxat
        if Til=='java':
            꾸러미명세=json.loads((Project_ildiz/'build/examples/manifest.json').read_text())
            for yo_l,kiritish_nuqta in 꾸러미명세.items():
                qobiq('cp '+yo_l+' /example-check.bin')
                tarkib_VALUE=bytearray();fayl_uzatish_aloqa.retrbinary('RETR example-check.bin',tarkib_VALUE.extend)
                assert len(tarkib_VALUE)==kiritish_nuqta['bytes'] and hashlib.sha256(tarkib_VALUE).hexdigest()==kiritish_nuqta['sha256'],yo_l
            fayl_uzatish_aloqa.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binar=bytes(range(256))*64
            fayl_uzatish_aloqa.storbinary('STOR boundary.bin',io.BytesIO(binar))
            tarkib_VALUE=bytearray();fayl_uzatish_aloqa.retrbinary('RETR boundary.bin',tarkib_VALUE.extend)
            assert tarkib_VALUE==binar and 'boundary.bin' in fayl_uzatish_aloqa.nlst()
            qobiq('cp /boundary.bin /boundary-copy.bin')
            tarkib_VALUE=bytearray();fayl_uzatish_aloqa.retrbinary('RETR boundary-copy.bin',tarkib_VALUE.extend)
            assert tarkib_VALUE==binar
            fayl_uzatish_aloqa.delete('boundary.bin');fayl_uzatish_aloqa.delete('boundary-copy.bin')
        assert '출력예제' in qobiq('ls /example/'+Til)
        qobiq('cd /example/'+Til)
        nom_jadval={'java':'JAVA','c':'C','python':'PYTHON'}[Til]
        예상파일=nom_jadval+' Fayl: 한글 ma_lumotlar 😀\n'
        if Til=='java':
            bajarmoq_buyruq('javac 출력예제.java','Compiled:');bajarmoq_buyruq('java 출력예제','JAVA 출력: 안녕하세요 😀')
            bajarmoq_buyruq('javac 파일예제.java','Compiled:');bajarmoq_buyruq('java 파일예제',예상파일)
            bajarmoq_buyruq('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_bayonnomasi_port,되돌림서버항목.UDP_port),'JAVA 네트워크 tasdiqlamoq: TCP UDP 한글')
            grafika_buyruq='java 그래픽예제'
        elif Til=='c':
            for Nomi,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Fayl','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_port),'C 네트워크 tasdiqlamoq: UDP 한글')]:
                bajarmoq_buyruq('cc '+Nomi+'예제.c -o bajarmoq_buyruq','Compiled native ARM64 ELF:')
                bajarmoq_buyruq('./bajarmoq_buyruq'+전달값,예상결과)
            bajarmoq_buyruq('cc 그래픽예제.c -o bajarmoq_buyruq','Compiled native ARM64 ELF:');grafika_buyruq='./bajarmoq_buyruq'
        else:
            for Nomi,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Fayl','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_port),'PYTHON 네트워크 tasdiqlamoq: UDP 한글')]:
                bajarmoq_buyruq('python '+Nomi+'예제.py'+전달값,예상결과)
            grafika_buyruq='python 그래픽예제.py'
        Start_chizish=Start_OFFSET(grafika_buyruq)
        Matn=수신하기('그림을 확인한 Orqaga_VALUE Enter를 누르세요.\r\n'.encode(),Start_chizish)
        assert nom_jadval+' 그래픽: 빨강 초록 파랑' in Matn and 'exit 0' not in Matn,Matn
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        fayl_uzatish_aloqa.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();fayl_uzatish_aloqa.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';fayl_uzatish_aloqa.delete('도중.txt')
        빛삼원색=화소들()
        for Y_tugmasi_koordinat,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(Y_tugmasi_koordinat*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(Til,Y_tugmasi_koordinat,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(o_lchov_ma_lumotlar/(Til+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Start_chizish)
        if Til=='java':
            Start_oyna=Start_OFFSET('java 창예제')
            수신하기('GUI 예제 Tayyorlamoq: 창예제'.encode(),Start_oyna)
            def chertmoq_VALUE(가로,Vertikal_holat):
                for tugma in (1,0):mijoz.sendall(struct.pack('>BBHH',5,tugma,가로,Vertikal_holat))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            chertmoq_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for belgi_VALUE in '한글':누름값(0x1000000|ord(belgi_VALUE));누름값(0x1000000|ord(belgi_VALUE),False)
            for 횟수 in (1,2):
                Bajarish=len(대화기록);chertmoq_VALUE(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Bajarish)
            time.sleep(.3)
            oyna_chizish=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=oyna_chizish.crop((110,272,530,300)).tobytes()
            oyna_chizish.save(str(o_lchov_ma_lumotlar/'java-swing.png'))
            Bajarish=len(대화기록);chertmoq_VALUE(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Bajarish)
        # Download the guest-created bytes through FTP in the same GUI VM.
        fayl_kiritish_nom={'java':'java.txt','c':'c.txt','python':'python.txt'}[Til]
        qobiq('cp '+fayl_kiritish_nom+' /tasdiqlash.txt')
        RECEIVED_COUNT=bytearray();fayl_uzatish_aloqa.retrbinary('RETR tasdiqlash.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        qobiq('echo preserved > 출력예제.'+('py' if Til=='python' else Til))
        assert 'EXAMPLES READY' in qobiq('example '+Til)
        assert '\npreserved\n' in qobiq('cat 출력예제.'+('py' if Til=='python' else Til))
        assert '한/영 Kalit_VALUE, Shift+Space 또는 F9' in qobiq('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in qobiq('echo GUI NETWORK TOGETHER')
        fayl_uzatish_aloqa.quit();fayl_uzatish_aloqa=None;assert 'FTP stopped' in qobiq('ftpd stop')
        print('PASS '+Til+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if fayl_uzatish_aloqa:
            try:fayl_uzatish_aloqa.close()
            except OSError:pass
        if mijoz:mijoz.close()
        Jarayon.terminate()
        try:Jarayon.wait(timeout=8)
        except subprocess.TimeoutExpired:Jarayon.kill();Jarayon.wait()
        tanlagich.close();Jarayon.stdout.close();(o_lchov_ma_lumotlar/(Til+'-serial.log')).write_bytes(대화기록)


def Bajarish():
    o_lchov_ma_lumotlar=Project_ildiz/'build/verification/examples';o_lchov_ma_lumotlar.mkdir(parents=True,exist_ok=True)
    tasdiq_hisobot={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_ildiz/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Til in ('java','c','python'):
                test_언어(Til,되돌림서버항목,o_lchov_ma_lumotlar);tasdiq_hisobot['languages'].append(Til)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(toifa_VALUE,ma_lumotlar.encode()) for toifa_VALUE,ma_lumotlar in 예상결과],되돌림서버항목.수신됨
            tasdiq_hisobot['host_network_payloads']=[{'protocol':toifa_VALUE,'text':ma_lumotlar.decode()} for toifa_VALUE,ma_lumotlar in 되돌림서버항목.수신됨]
        tasdiq_hisobot.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(o_lchov_ma_lumotlar/'report.json').write_text(json.dumps(tasdiq_hisobot,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Bajarish()
