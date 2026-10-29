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
from papamahi_tiro import EXACT_uara
from 예제되돌림서버 import 되돌림서버
from kawe_tono import whakaatu_pūtake


def test_언어(reo,되돌림서버항목,mēhua_raraunga):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Hātepe=subprocess.Popen(['python3',str(whakaatu_pūtake/'Ngā_Utauta/kawe_tono.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    pūtīpako=selectors.DefaultSelector();pūtīpako.register(Hātepe.stdout,selectors.EVENT_READ)
    대화기록=bytearray();kiritaki=None;kōnae_whakawhiti_hononga=None
    def 수신하기(확인표시,whakahaere=0):
        mutu_OFFSET=time.monotonic()+60
        while 확인표시 not in 대화기록[whakahaere:]:
            if time.monotonic()>mutu_OFFSET or Hātepe.poll() is not None:raise AssertionError(대화기록[whakahaere:].decode('utf-8','replace'))
            for 누름값,_ in pūtīpako.select(.1):
                raraunga=누름값.fileobj.read(65536)
                if raraunga:대화기록.extend(raraunga)
        return 대화기록[whakahaere:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(tohu_uara,누르는중=True):kiritaki.sendall(struct.pack('>BBHI',4,int(누르는중),0,tohu_uara))
    def Start_OFFSET(hononga):
        whakahaere=len(대화기록)
        for waehere_pūāhua in hononga+'\n':
            tohu_uara=0xff0d if waehere_pūāhua=='\n' else ord(waehere_pūāhua) if ord(waehere_pūāhua)<256 else 0x1000000|ord(waehere_pūāhua)
            누름값(tohu_uara);누름값(tohu_uara,False)
        return whakahaere
    def anga(hononga):return 수신하기(b'jkoros-native> ',Start_OFFSET(hononga))
    def kawe_tono(hononga,예상결과):
        Ngā_kupu=anga(hononga);assert 예상결과 in Ngā_kupu and 'exit 0' in Ngā_kupu,(hononga,Ngā_kupu)
        return Ngā_kupu
    def 화소들():
        kiritaki.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            kāwai_uara=EXACT_uara(kiritaki,1)[0]
            if kāwai_uara==2:continue
            if kāwai_uara==3:
                tuemi_COUNT=struct.unpack('>I',EXACT_uara(kiritaki,7)[3:])[0];EXACT_uara(kiritaki,tuemi_COUNT);continue
            assert kāwai_uara==0,kāwai_uara
            tāurunga_COUNT=struct.unpack('>H',EXACT_uara(kiritaki,3)[1:])[0]
            for _ in range(tāurunga_COUNT):
                taunga_x,세로좌표,너비값,높이값,rōpū_pūāhua=struct.unpack('>HHHHi',EXACT_uara(kiritaki,12));assert rōpū_pūāhua==0,rōpū_pūāhua
                raraunga=EXACT_uara(kiritaki,너비값*높이값*4)
                for ROW_tūranga in range(높이값):
                    for tīwae_tūranga in range(너비값):
                        원본자료=(ROW_tūranga*너비값+tīwae_tūranga)*4;ūnga=((세로좌표+ROW_tūranga)*640+taunga_x+tīwae_tūranga)*3
                        빛삼원색[ūnga:ūnga+3]=bytes((raraunga[원본자료+2],raraunga[원본자료+1],raraunga[원본자료]))
            if tāurunga_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        kiritaki=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert EXACT_uara(kiritaki,12)==b'RFB 003.008\n';kiritaki.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_uara(kiritaki,EXACT_uara(kiritaki,1)[0]);kiritaki.sendall(b'\x01');assert EXACT_uara(kiritaki,4)==b'\0'*4
        kiritaki.sendall(b'\x01');초기값=EXACT_uara(kiritaki,24);EXACT_uara(kiritaki,struct.unpack('>I',초기값[20:])[0])
        kiritaki.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        kiritaki.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in anga('ftpd start')
        kōnae_whakawhiti_hononga=ftplib.FTP();kōnae_whakawhiti_hononga.encoding='utf-8';kōnae_whakawhiti_hononga.connect('127.0.0.1',파일전송접속번호,timeout=20);kōnae_whakawhiti_hononga.login()
        tino_raraunga_raraunga=('GUI와 FTP 동시 사용 '+reo+' 😀\n').encode()
        kōnae_whakawhiti_hononga.storbinary('STOR 함께.txt',io.BytesIO(tino_raraunga_raraunga))
        assert tino_raraunga_raraunga.decode().strip() in anga('cat /함께.txt')
        RECEIVED_COUNT=bytearray();kōnae_whakawhiti_hononga.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==tino_raraunga_raraunga;kōnae_whakawhiti_hononga.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        tuku_Rārangi=anga('ls /example')
        assert all(Ingoa in tuku_Rārangi for Ingoa in ('java/','c/','python/','README.md')),tuku_Rārangi
        if reo=='java':
            꾸러미명세=json.loads((whakaatu_pūtake/'build/examples/manifest.json').read_text())
            for ara,tāurunga_ira in 꾸러미명세.items():
                anga('cp '+ara+' /example-check.bin')
                Ihirangi_uara=bytearray();kōnae_whakawhiti_hononga.retrbinary('RETR example-check.bin',Ihirangi_uara.extend)
                assert len(Ihirangi_uara)==tāurunga_ira['bytes'] and hashlib.sha256(Ihirangi_uara).hexdigest()==tāurunga_ira['sha256'],ara
            kōnae_whakawhiti_hononga.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ā_rua=bytes(range(256))*64
            kōnae_whakawhiti_hononga.storbinary('STOR boundary.bin',io.BytesIO(ā_rua))
            Ihirangi_uara=bytearray();kōnae_whakawhiti_hononga.retrbinary('RETR boundary.bin',Ihirangi_uara.extend)
            assert Ihirangi_uara==ā_rua and 'boundary.bin' in kōnae_whakawhiti_hononga.nlst()
            anga('cp /boundary.bin /boundary-copy.bin')
            Ihirangi_uara=bytearray();kōnae_whakawhiti_hononga.retrbinary('RETR boundary-copy.bin',Ihirangi_uara.extend)
            assert Ihirangi_uara==ā_rua
            kōnae_whakawhiti_hononga.delete('boundary.bin');kōnae_whakawhiti_hononga.delete('boundary-copy.bin')
        assert '출력예제' in anga('ls /example/'+reo)
        anga('cd /example/'+reo)
        ingoa_ripanga={'java':'JAVA','c':'C','python':'PYTHON'}[reo]
        예상파일=ingoa_ripanga+' Kōnae: 한글 raraunga 😀\n'
        if reo=='java':
            kawe_tono('javac 출력예제.java','Compiled:');kawe_tono('java 출력예제','JAVA 출력: 안녕하세요 😀')
            kawe_tono('javac 파일예제.java','Compiled:');kawe_tono('java 파일예제',예상파일)
            kawe_tono('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_kawe,되돌림서버항목.UDP_kawe),'JAVA 네트워크 manatoko: TCP UDP 한글')
            whakairoiro_tono='java 그래픽예제'
        elif reo=='c':
            for Ingoa,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Kōnae','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_kawe),'C 네트워크 manatoko: UDP 한글')]:
                kawe_tono('cc '+Ingoa+'예제.c -o kawe_tono','Compiled native ARM64 ELF:')
                kawe_tono('./kawe_tono'+전달값,예상결과)
            kawe_tono('cc 그래픽예제.c -o kawe_tono','Compiled native ARM64 ELF:');whakairoiro_tono='./kawe_tono'
        else:
            for Ingoa,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Kōnae','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_kawe),'PYTHON 네트워크 manatoko: UDP 한글')]:
                kawe_tono('python '+Ingoa+'예제.py'+전달값,예상결과)
            whakairoiro_tono='python 그래픽예제.py'
        Start_tātuhi=Start_OFFSET(whakairoiro_tono)
        Ngā_kupu=수신하기('그림을 확인한 Hoki_uara Enter를 누르세요.\r\n'.encode(),Start_tātuhi)
        assert ingoa_ripanga+' 그래픽: 빨강 초록 파랑' in Ngā_kupu and 'exit 0' not in Ngā_kupu,Ngā_kupu
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        kōnae_whakawhiti_hononga.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();kōnae_whakawhiti_hononga.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';kōnae_whakawhiti_hononga.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_uara=(세로좌표*640+610)*3;assert tuple(빛삼원색[OFFSET_uara:OFFSET_uara+3])==색상,(reo,세로좌표,tuple(빛삼원색[OFFSET_uara:OFFSET_uara+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(mēhua_raraunga/(reo+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Start_tātuhi)
        if reo=='java':
            Start_matapihi=Start_OFFSET('java 창예제')
            수신하기('GUI 예제 Whakarite: 창예제'.encode(),Start_matapihi)
            def pāwhiri_uara(가로,Poutū_tūranga):
                for pātene in (1,0):kiritaki.sendall(struct.pack('>BBHH',5,pātene,가로,Poutū_tūranga))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            pāwhiri_uara(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for pūāhua_uara in '한글':누름값(0x1000000|ord(pūāhua_uara));누름값(0x1000000|ord(pūāhua_uara),False)
            for 횟수 in (1,2):
                whakahaere=len(대화기록);pāwhiri_uara(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),whakahaere)
            time.sleep(.3)
            matapihi_tātuhi=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=matapihi_tātuhi.crop((110,272,530,300)).tobytes()
            matapihi_tātuhi.save(str(mēhua_raraunga/'java-swing.png'))
            whakahaere=len(대화기록);pāwhiri_uara(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',whakahaere)
        # Download the guest-created bytes through FTP in the same GUI VM.
        kōnae_tāurunga_ingoa={'java':'java.txt','c':'c.txt','python':'python.txt'}[reo]
        anga('cp '+kōnae_tāurunga_ingoa+' /whakamana.txt')
        RECEIVED_COUNT=bytearray();kōnae_whakawhiti_hononga.retrbinary('RETR whakamana.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        anga('echo preserved > 출력예제.'+('py' if reo=='python' else reo))
        assert 'EXAMPLES READY' in anga('example '+reo)
        assert '\npreserved\n' in anga('cat 출력예제.'+('py' if reo=='python' else reo))
        assert '한/영 kī_uara, Shift+Space 또는 F9' in anga('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in anga('echo GUI NETWORK TOGETHER')
        kōnae_whakawhiti_hononga.quit();kōnae_whakawhiti_hononga=None;assert 'FTP stopped' in anga('ftpd stop')
        print('PASS '+reo+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if kōnae_whakawhiti_hononga:
            try:kōnae_whakawhiti_hononga.close()
            except OSError:pass
        if kiritaki:kiritaki.close()
        Hātepe.terminate()
        try:Hātepe.wait(timeout=8)
        except subprocess.TimeoutExpired:Hātepe.kill();Hātepe.wait()
        pūtīpako.close();Hātepe.stdout.close();(mēhua_raraunga/(reo+'-serial.log')).write_bytes(대화기록)


def whakahaere():
    mēhua_raraunga=whakaatu_pūtake/'build/verification/examples';mēhua_raraunga.mkdir(parents=True,exist_ok=True)
    whakamana_pūrongo={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((whakaatu_pūtake/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for reo in ('java','c','python'):
                test_언어(reo,되돌림서버항목,mēhua_raraunga);whakamana_pūrongo['languages'].append(reo)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(kāwai_uara,raraunga.encode()) for kāwai_uara,raraunga in 예상결과],되돌림서버항목.수신됨
            whakamana_pūrongo['host_network_payloads']=[{'protocol':kāwai_uara,'text':raraunga.decode()} for kāwai_uara,raraunga in 되돌림서버항목.수신됨]
        whakamana_pūrongo.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(mēhua_raraunga/'report.json').write_text(json.dumps(whakamana_pūrongo,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':whakahaere()
