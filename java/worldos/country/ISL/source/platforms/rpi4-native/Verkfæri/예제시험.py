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
from skjáborð_Sýn import EXACT_VALUE
from 예제되돌림서버 import 되돌림서버
from keyra_skipun import verk_rót


def test_언어(Tungumál,되돌림서버항목,mæld_stærð_gögn):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));skrá_flytja_tengisnúmer=임시자원.getsockname()[1]
    Ferli=subprocess.Popen(['python3',str(verk_rót/'Verkfæri/keyra_skipun.py'),'--desktop','--network','--port','0','--ftp-port',str(skrá_flytja_tengisnúmer)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    val=selectors.DefaultSelector();val.register(Ferli.stdout,selectors.EVENT_READ)
    대화기록=bytearray();biðlari=None;skrá_flytja_tenging=None
    def 수신하기(확인표시,Keyra_2=0):
        ljúka_OFFSET=time.monotonic()+60
        while 확인표시 not in 대화기록[Keyra_2:]:
            if time.monotonic()>ljúka_OFFSET or Ferli.poll() is not None:raise AssertionError(대화기록[Keyra_2:].decode('utf-8','replace'))
            for 누름값,_ in val.select(.1):
                gögn=누름값.fileobj.read(65536)
                if gögn:대화기록.extend(gögn)
        return 대화기록[Keyra_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(tákn_VALUE,누르는중=True):biðlari.sendall(struct.pack('>BBHI',4,int(누르는중),0,tákn_VALUE))
    def Opna_OFFSET(Lína):
        Keyra_2=len(대화기록)
        for stafkóði in Lína+'\n':
            tákn_VALUE=0xff0d if stafkóði=='\n' else ord(stafkóði) if ord(stafkóði)<256 else 0x1000000|ord(stafkóði)
            누름값(tákn_VALUE);누름값(tákn_VALUE,False)
        return Keyra_2
    def skel(Lína):return 수신하기(b'jkoros-native> ',Opna_OFFSET(Lína))
    def keyra_skipun(Lína,예상결과):
        Texti=skel(Lína);assert 예상결과 in Texti and 'exit 0' in Texti,(Lína,Texti)
        return Texti
    def 화소들():
        biðlari.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            tegund_VALUE=EXACT_VALUE(biðlari,1)[0]
            if tegund_VALUE==2:continue
            if tegund_VALUE==3:
                vara_COUNT=struct.unpack('>I',EXACT_VALUE(biðlari,7)[3:])[0];EXACT_VALUE(biðlari,vara_COUNT);continue
            assert tegund_VALUE==0,tegund_VALUE
            færsla_COUNT=struct.unpack('>H',EXACT_VALUE(biðlari,3)[1:])[0]
            for _ in range(færsla_COUNT):
                x_hnit,Y_hnit,너비값,높이값,stafamengi=struct.unpack('>HHHHi',EXACT_VALUE(biðlari,12));assert stafamengi==0,stafamengi
                gögn=EXACT_VALUE(biðlari,너비값*높이값*4)
                for ROW_staða in range(높이값):
                    for COLUMN_staða in range(너비값):
                        원본자료=(ROW_staða*너비값+COLUMN_staða)*4;markmið=((Y_hnit+ROW_staða)*640+x_hnit+COLUMN_staða)*3
                        빛삼원색[markmið:markmið+3]=bytes((gögn[원본자료+2],gögn[원본자료+1],gögn[원본자료]))
            if færsla_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        tengisnúmer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        biðlari=socket.create_connection(('127.0.0.1',tengisnúmer),timeout=10)
        assert EXACT_VALUE(biðlari,12)==b'RFB 003.008\n';biðlari.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(biðlari,EXACT_VALUE(biðlari,1)[0]);biðlari.sendall(b'\x01');assert EXACT_VALUE(biðlari,4)==b'\0'*4
        biðlari.sendall(b'\x01');초기값=EXACT_VALUE(biðlari,24);EXACT_VALUE(biðlari,struct.unpack('>I',초기값[20:])[0])
        biðlari.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        biðlari.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in skel('ftpd start')
        skrá_flytja_tenging=ftplib.FTP();skrá_flytja_tenging.encoding='utf-8';skrá_flytja_tenging.connect('127.0.0.1',skrá_flytja_tengisnúmer,timeout=20);skrá_flytja_tenging.login()
        farmur_gögn=('GUI와 FTP 동시 사용 '+Tungumál+' 😀\n').encode()
        skrá_flytja_tenging.storbinary('STOR 함께.txt',io.BytesIO(farmur_gögn))
        assert farmur_gögn.decode().strip() in skel('cat /함께.txt')
        RECEIVED_COUNT=bytearray();skrá_flytja_tenging.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==farmur_gögn;skrá_flytja_tenging.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        senda_Listi=skel('ls /example')
        assert all(Heiti in senda_Listi for Heiti in ('java/','c/','python/','README.md')),senda_Listi
        if Tungumál=='java':
            búnt_skrá=json.loads((verk_rót/'build/examples/manifest.json').read_text())
            for SLÓÐ,færsla_P in búnt_skrá.items():
                skel('cp '+SLÓÐ+' /example-check.bin')
                Efni_VALUE=bytearray();skrá_flytja_tenging.retrbinary('RETR example-check.bin',Efni_VALUE.extend)
                assert len(Efni_VALUE)==færsla_P['bytes'] and hashlib.sha256(Efni_VALUE).hexdigest()==færsla_P['sha256'],SLÓÐ
            skrá_flytja_tenging.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            tvíundar=bytes(range(256))*64
            skrá_flytja_tenging.storbinary('STOR boundary.bin',io.BytesIO(tvíundar))
            Efni_VALUE=bytearray();skrá_flytja_tenging.retrbinary('RETR boundary.bin',Efni_VALUE.extend)
            assert Efni_VALUE==tvíundar and 'boundary.bin' in skrá_flytja_tenging.nlst()
            skel('cp /boundary.bin /boundary-copy.bin')
            Efni_VALUE=bytearray();skrá_flytja_tenging.retrbinary('RETR boundary-copy.bin',Efni_VALUE.extend)
            assert Efni_VALUE==tvíundar
            skrá_flytja_tenging.delete('boundary.bin');skrá_flytja_tenging.delete('boundary-copy.bin')
        assert 'Úttaksdæmi' in skel('ls /example/'+Tungumál)
        skel('cd /example/'+Tungumál)
        heiti_tafla={'java':'JAVA','c':'C','python':'PYTHON'}[Tungumál]
        예상파일=heiti_tafla+' Skrá: 한글 gögn 😀\n'
        if Tungumál=='java':
            keyra_skipun('javac Úttaksdæmi.java','Compiled:');keyra_skipun('java Úttaksdæmi','JAVA úttak: 안녕하세요 😀')
            keyra_skipun('javac Skráardæmi.java','Compiled:');keyra_skipun('java Skráardæmi',예상파일)
            keyra_skipun('java Netdæmi {} {}'.format(되돌림서버항목.TCP_gátt,되돌림서버항목.UDP_gátt),'JAVA 네트워크 sannprófa: TCP UDP 한글')
            myndefni_skipun='java Teiknidæmi'
        elif Tungumál=='c':
            for Heiti,전달값,예상결과 in [('úttak','', 'C úttak: 안녕하세요 😀'),('Skrá','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_gátt),'C 네트워크 sannprófa: UDP 한글')]:
                keyra_skipun('cc '+Heiti+'예제.c -o keyra_skipun','Compiled native ARM64 ELF:')
                keyra_skipun('./keyra_skipun'+전달값,예상결과)
            keyra_skipun('cc Teiknidæmi.c -o keyra_skipun','Compiled native ARM64 ELF:');myndefni_skipun='./keyra_skipun'
        else:
            for Heiti,전달값,예상결과 in [('úttak','','PYTHON úttak: 안녕하세요 😀'),('Skrá','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_gátt),'PYTHON 네트워크 sannprófa: UDP 한글')]:
                keyra_skipun('python '+Heiti+'예제.py'+전달값,예상결과)
            myndefni_skipun='python Teiknidæmi.py'
        Opna_teikning=Opna_OFFSET(myndefni_skipun)
        Texti=수신하기('그림을 확인한 TIL_BAKA_VALUE Enter를 누르세요.\r\n'.encode(),Opna_teikning)
        assert heiti_tafla+' 그래픽: 빨강 초록 파랑' in Texti and 'exit 0' not in Texti,Texti
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        skrá_flytja_tenging.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();skrá_flytja_tenging.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';skrá_flytja_tenging.delete('도중.txt')
        빛삼원색=화소들()
        for Y_hnit,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(Y_hnit*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(Tungumál,Y_hnit,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(mæld_stærð_gögn/(Tungumál+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Opna_teikning)
        if Tungumál=='java':
            Opna_gluggi=Opna_OFFSET('java Gluggadæmi')
            수신하기('GUI 예제 Undirbúa: Gluggadæmi'.encode(),Opna_gluggi)
            def smella_VALUE(가로,Lóðrétt_staða):
                for hnappur in (1,0):biðlari.sendall(struct.pack('>BBHH',5,hnappur,가로,Lóðrétt_staða))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            smella_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for stafur_VALUE in '한글':누름값(0x1000000|ord(stafur_VALUE));누름값(0x1000000|ord(stafur_VALUE),False)
            for 횟수 in (1,2):
                Keyra_2=len(대화기록);smella_VALUE(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Keyra_2)
            time.sleep(.3)
            gluggi_teikning=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=gluggi_teikning.crop((110,272,530,300)).tobytes()
            gluggi_teikning.save(str(mæld_stærð_gögn/'java-swing.png'))
            Keyra_2=len(대화기록);smella_VALUE(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Keyra_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        skrá_færsla_heiti={'java':'java.txt','c':'c.txt','python':'python.txt'}[Tungumál]
        skel('cp '+skrá_færsla_heiti+' /staðfesta.txt')
        RECEIVED_COUNT=bytearray();skrá_flytja_tenging.retrbinary('RETR staðfesta.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        skel('echo preserved > Úttaksdæmi.'+('py' if Tungumál=='python' else Tungumál))
        assert 'EXAMPLES READY' in skel('example '+Tungumál)
        assert '\npreserved\n' in skel('cat Úttaksdæmi.'+('py' if Tungumál=='python' else Tungumál))
        assert '한/영 Lykill_VALUE, Shift+Space 또는 F9' in skel('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in skel('echo GUI NETWORK TOGETHER')
        skrá_flytja_tenging.quit();skrá_flytja_tenging=None;assert 'FTP stopped' in skel('ftpd stop')
        print('PASS '+Tungumál+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if skrá_flytja_tenging:
            try:skrá_flytja_tenging.close()
            except OSError:pass
        if biðlari:biðlari.close()
        Ferli.terminate()
        try:Ferli.wait(timeout=8)
        except subprocess.TimeoutExpired:Ferli.kill();Ferli.wait()
        val.close();Ferli.stdout.close();(mæld_stærð_gögn/(Tungumál+'-serial.log')).write_bytes(대화기록)


def Keyra_2():
    mæld_stærð_gögn=verk_rót/'build/verification/examples';mæld_stærð_gögn.mkdir(parents=True,exist_ok=True)
    prófun_skrá={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((verk_rót/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Tungumál in ('java','c','python'):
                test_언어(Tungumál,되돌림서버항목,mæld_stærð_gögn);prófun_skrá['languages'].append(Tungumál)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(tegund_VALUE,gögn.encode()) for tegund_VALUE,gögn in 예상결과],되돌림서버항목.수신됨
            prófun_skrá['host_network_payloads']=[{'protocol':tegund_VALUE,'text':gögn.decode()} for tegund_VALUE,gögn in 되돌림서버항목.수신됨]
        prófun_skrá.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(mæld_stærð_gögn/'report.json').write_text(json.dumps(prófun_skrá,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Keyra_2()
