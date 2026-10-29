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
from desktop_wera import EXACT_VALUE
from 예제되돌림서버 import 되돌림서버
from eżegwixxa_kmand import pprojetta_għerq


def test_언어(Lingwa,되돌림서버항목,miżura_data):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Proċess=subprocess.Popen(['python3',str(pprojetta_għerq/'Għodod/eżegwixxa_kmand.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    selettur=selectors.DefaultSelector();selettur.register(Proċess.stdout,selectors.EVENT_READ)
    대화기록=bytearray();klijent=None;fajl_trasferiment_konnessjoni=None
    def 수신하기(확인표시,serje=0):
        ttermina_OFFSET=time.monotonic()+60
        while 확인표시 not in 대화기록[serje:]:
            if time.monotonic()>ttermina_OFFSET or Proċess.poll() is not None:raise AssertionError(대화기록[serje:].decode('utf-8','replace'))
            for 누름값,_ in selettur.select(.1):
                data=누름값.fileobj.read(65536)
                if data:대화기록.extend(data)
        return 대화기록[serje:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(simbolu_VALUE,누르는중=True):klijent.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbolu_VALUE))
    def Bidu_OFFSET(linja):
        serje=len(대화기록)
        for kodiċi_tal_karattru in linja+'\n':
            simbolu_VALUE=0xff0d if kodiċi_tal_karattru=='\n' else ord(kodiċi_tal_karattru) if ord(kodiċi_tal_karattru)<256 else 0x1000000|ord(kodiċi_tal_karattru)
            누름값(simbolu_VALUE);누름값(simbolu_VALUE,False)
        return serje
    def shell(linja):return 수신하기(b'jkoros-native> ',Bidu_OFFSET(linja))
    def eżegwixxa_kmand(linja,예상결과):
        SMS=shell(linja);assert 예상결과 in SMS and 'exit 0' in SMS,(linja,SMS)
        return SMS
    def 화소들():
        klijent.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            kategorija_VALUE=EXACT_VALUE(klijent,1)[0]
            if kategorija_VALUE==2:continue
            if kategorija_VALUE==3:
                element_COUNT=struct.unpack('>I',EXACT_VALUE(klijent,7)[3:])[0];EXACT_VALUE(klijent,element_COUNT);continue
            assert kategorija_VALUE==0,kategorija_VALUE
            entrata_COUNT=struct.unpack('>H',EXACT_VALUE(klijent,3)[1:])[0]
            for _ in range(entrata_COUNT):
                koordinat_x,세로좌표,너비값,높이값,sett_ta_karattri=struct.unpack('>HHHHi',EXACT_VALUE(klijent,12));assert sett_ta_karattri==0,sett_ta_karattri
                data=EXACT_VALUE(klijent,너비값*높이값*4)
                for ROW_pożizzjoni in range(높이값):
                    for COLUMN_pożizzjoni in range(너비값):
                        원본자료=(ROW_pożizzjoni*너비값+COLUMN_pożizzjoni)*4;mira=((세로좌표+ROW_pożizzjoni)*640+koordinat_x+COLUMN_pożizzjoni)*3
                        빛삼원색[mira:mira+3]=bytes((data[원본자료+2],data[원본자료+1],data[원본자료]))
            if entrata_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        klijent=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert EXACT_VALUE(klijent,12)==b'RFB 003.008\n';klijent.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(klijent,EXACT_VALUE(klijent,1)[0]);klijent.sendall(b'\x01');assert EXACT_VALUE(klijent,4)==b'\0'*4
        klijent.sendall(b'\x01');초기값=EXACT_VALUE(klijent,24);EXACT_VALUE(klijent,struct.unpack('>I',초기값[20:])[0])
        klijent.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klijent.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in shell('ftpd start')
        fajl_trasferiment_konnessjoni=ftplib.FTP();fajl_trasferiment_konnessjoni.encoding='utf-8';fajl_trasferiment_konnessjoni.connect('127.0.0.1',파일전송접속번호,timeout=20);fajl_trasferiment_konnessjoni.login()
        payload_data=('GUI와 FTP 동시 사용 '+Lingwa+' 😀\n').encode()
        fajl_trasferiment_konnessjoni.storbinary('STOR 함께.txt',io.BytesIO(payload_data))
        assert payload_data.decode().strip() in shell('cat /함께.txt')
        RECEIVED_COUNT=bytearray();fajl_trasferiment_konnessjoni.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==payload_data;fajl_trasferiment_konnessjoni.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        bagħat_Lista=shell('ls /example')
        assert all(isem in bagħat_Lista for isem in ('java/','c/','python/','README.md')),bagħat_Lista
        if Lingwa=='java':
            꾸러미명세=json.loads((pprojetta_għerq/'build/examples/manifest.json').read_text())
            for mogħdija,entrata_punt in 꾸러미명세.items():
                shell('cp '+mogħdija+' /example-check.bin')
                Kontenut_VALUE=bytearray();fajl_trasferiment_konnessjoni.retrbinary('RETR example-check.bin',Kontenut_VALUE.extend)
                assert len(Kontenut_VALUE)==entrata_punt['bytes'] and hashlib.sha256(Kontenut_VALUE).hexdigest()==entrata_punt['sha256'],mogħdija
            fajl_trasferiment_konnessjoni.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binarju=bytes(range(256))*64
            fajl_trasferiment_konnessjoni.storbinary('STOR boundary.bin',io.BytesIO(binarju))
            Kontenut_VALUE=bytearray();fajl_trasferiment_konnessjoni.retrbinary('RETR boundary.bin',Kontenut_VALUE.extend)
            assert Kontenut_VALUE==binarju and 'boundary.bin' in fajl_trasferiment_konnessjoni.nlst()
            shell('cp /boundary.bin /boundary-copy.bin')
            Kontenut_VALUE=bytearray();fajl_trasferiment_konnessjoni.retrbinary('RETR boundary-copy.bin',Kontenut_VALUE.extend)
            assert Kontenut_VALUE==binarju
            fajl_trasferiment_konnessjoni.delete('boundary.bin');fajl_trasferiment_konnessjoni.delete('boundary-copy.bin')
        assert '출력예제' in shell('ls /example/'+Lingwa)
        shell('cd /example/'+Lingwa)
        isem_tabella={'java':'JAVA','c':'C','python':'PYTHON'}[Lingwa]
        예상파일=isem_tabella+' fajl: 한글 data 😀\n'
        if Lingwa=='java':
            eżegwixxa_kmand('javac 출력예제.java','Compiled:');eżegwixxa_kmand('java 출력예제','JAVA 출력: 안녕하세요 😀')
            eżegwixxa_kmand('javac 파일예제.java','Compiled:');eżegwixxa_kmand('java 파일예제',예상파일)
            eżegwixxa_kmand('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_port,되돌림서버항목.UDP_port),'JAVA 네트워크 vverifika: TCP UDP 한글')
            grafika_kmand='java 그래픽예제'
        elif Lingwa=='c':
            for isem,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('fajl','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_port),'C 네트워크 vverifika: UDP 한글')]:
                eżegwixxa_kmand('cc '+isem+'예제.c -o eżegwixxa_kmand','Compiled native ARM64 ELF:')
                eżegwixxa_kmand('./eżegwixxa_kmand'+전달값,예상결과)
            eżegwixxa_kmand('cc 그래픽예제.c -o eżegwixxa_kmand','Compiled native ARM64 ELF:');grafika_kmand='./eżegwixxa_kmand'
        else:
            for isem,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('fajl','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_port),'PYTHON 네트워크 vverifika: UDP 한글')]:
                eżegwixxa_kmand('python '+isem+'예제.py'+전달값,예상결과)
            grafika_kmand='python 그래픽예제.py'
        Bidu_tpinġija=Bidu_OFFSET(grafika_kmand)
        SMS=수신하기('그림을 확인한 Lura_VALUE Enter를 누르세요.\r\n'.encode(),Bidu_tpinġija)
        assert isem_tabella+' 그래픽: 빨강 초록 파랑' in SMS and 'exit 0' not in SMS,SMS
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        fajl_trasferiment_konnessjoni.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();fajl_trasferiment_konnessjoni.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';fajl_trasferiment_konnessjoni.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(세로좌표*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(Lingwa,세로좌표,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(miżura_data/(Lingwa+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Bidu_tpinġija)
        if Lingwa=='java':
            Bidu_tieqa=Bidu_OFFSET('java 창예제')
            수신하기('GUI 예제 Ħejji: 창예제'.encode(),Bidu_tieqa)
            def klikkja_VALUE(가로,Vertikali_pożizzjoni):
                for buttuna in (1,0):klijent.sendall(struct.pack('>BBHH',5,buttuna,가로,Vertikali_pożizzjoni))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klikkja_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for karattru_VALUE in '한글':누름값(0x1000000|ord(karattru_VALUE));누름값(0x1000000|ord(karattru_VALUE),False)
            for 횟수 in (1,2):
                serje=len(대화기록);klikkja_VALUE(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),serje)
            time.sleep(.3)
            tieqa_tpinġija=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=tieqa_tpinġija.crop((110,272,530,300)).tobytes()
            tieqa_tpinġija.save(str(miżura_data/'java-swing.png'))
            serje=len(대화기록);klikkja_VALUE(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',serje)
        # Download the guest-created bytes through FTP in the same GUI VM.
        fajl_entrata_isem={'java':'java.txt','c':'c.txt','python':'python.txt'}[Lingwa]
        shell('cp '+fajl_entrata_isem+' /vvalida.txt')
        RECEIVED_COUNT=bytearray();fajl_trasferiment_konnessjoni.retrbinary('RETR vvalida.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        shell('echo preserved > 출력예제.'+('py' if Lingwa=='python' else Lingwa))
        assert 'EXAMPLES READY' in shell('example '+Lingwa)
        assert '\npreserved\n' in shell('cat 출력예제.'+('py' if Lingwa=='python' else Lingwa))
        assert '한/영 tast_VALUE, Shift+Space 또는 F9' in shell('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in shell('echo GUI NETWORK TOGETHER')
        fajl_trasferiment_konnessjoni.quit();fajl_trasferiment_konnessjoni=None;assert 'FTP stopped' in shell('ftpd stop')
        print('PASS '+Lingwa+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if fajl_trasferiment_konnessjoni:
            try:fajl_trasferiment_konnessjoni.close()
            except OSError:pass
        if klijent:klijent.close()
        Proċess.terminate()
        try:Proċess.wait(timeout=8)
        except subprocess.TimeoutExpired:Proċess.kill();Proċess.wait()
        selettur.close();Proċess.stdout.close();(miżura_data/(Lingwa+'-serial.log')).write_bytes(대화기록)


def serje():
    miżura_data=pprojetta_għerq/'build/verification/examples';miżura_data.mkdir(parents=True,exist_ok=True)
    validazzjoni_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((pprojetta_għerq/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Lingwa in ('java','c','python'):
                test_언어(Lingwa,되돌림서버항목,miżura_data);validazzjoni_rapport['languages'].append(Lingwa)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(kategorija_VALUE,data.encode()) for kategorija_VALUE,data in 예상결과],되돌림서버항목.수신됨
            validazzjoni_rapport['host_network_payloads']=[{'protocol':kategorija_VALUE,'text':data.decode()} for kategorija_VALUE,data in 되돌림서버항목.수신됨]
        validazzjoni_rapport.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(miżura_data/'report.json').write_text(json.dumps(validazzjoni_rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':serje()
