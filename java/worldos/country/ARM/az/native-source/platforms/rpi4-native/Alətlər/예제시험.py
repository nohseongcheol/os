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
from iş_masası_baxmaq import EXACT_VALUE
from 예제되돌림서버 import 되돌림서버
from icra_etmək_əmr import Project_kök


def test_언어(Dil,되돌림서버항목,ölçü_verilənlər):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Proses=subprocess.Popen(['python3',str(Project_kök/'Alətlər/icra_etmək_əmr.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    seçici=selectors.DefaultSelector();seçici.register(Proses.stdout,selectors.EVENT_READ)
    대화기록=bytearray();müştəri=None;fayl_ötürmə_qoşulma=None
    def 수신하기(확인표시,İcra_Et=0):
        bitirmək_OFFSET=time.monotonic()+60
        while 확인표시 not in 대화기록[İcra_Et:]:
            if time.monotonic()>bitirmək_OFFSET or Proses.poll() is not None:raise AssertionError(대화기록[İcra_Et:].decode('utf-8','replace'))
            for 누름값,_ in seçici.select(.1):
                verilənlər=누름값.fileobj.read(65536)
                if verilənlər:대화기록.extend(verilənlər)
        return 대화기록[İcra_Et:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(simvol_VALUE,누르는중=True):müştəri.sendall(struct.pack('>BBHI',4,int(누르는중),0,simvol_VALUE))
    def Başla_OFFSET(Giriş):
        İcra_Et=len(대화기록)
        for simvol_kodu in Giriş+'\n':
            simvol_VALUE=0xff0d if simvol_kodu=='\n' else ord(simvol_kodu) if ord(simvol_kodu)<256 else 0x1000000|ord(simvol_kodu)
            누름값(simvol_VALUE);누름값(simvol_VALUE,False)
        return İcra_Et
    def örtük(Giriş):return 수신하기(b'jkoros-native> ',Başla_OFFSET(Giriş))
    def icra_etmək_əmr(Giriş,예상결과):
        Mətn=örtük(Giriş);assert 예상결과 in Mətn and 'exit 0' in Mətn,(Giriş,Mətn)
        return Mətn
    def 화소들():
        müştəri.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            sahə_VALUE=EXACT_VALUE(müştəri,1)[0]
            if sahə_VALUE==2:continue
            if sahə_VALUE==3:
                element_COUNT=struct.unpack('>I',EXACT_VALUE(müştəri,7)[3:])[0];EXACT_VALUE(müştəri,element_COUNT);continue
            assert sahə_VALUE==0,sahə_VALUE
            daxiletmə_COUNT=struct.unpack('>H',EXACT_VALUE(müştəri,3)[1:])[0]
            for _ in range(daxiletmə_COUNT):
                x_koordinatı,Y_koordinat,너비값,높이값,simvol_dəsti=struct.unpack('>HHHHi',EXACT_VALUE(müştəri,12));assert simvol_dəsti==0,simvol_dəsti
                verilənlər=EXACT_VALUE(müştəri,너비값*높이값*4)
                for ROW_yerinə_qoymaq in range(높이값):
                    for sütun_yerinə_qoymaq in range(너비값):
                        원본자료=(ROW_yerinə_qoymaq*너비값+sütun_yerinə_qoymaq)*4;hədəf=((Y_koordinat+ROW_yerinə_qoymaq)*640+x_koordinatı+sütun_yerinə_qoymaq)*3
                        빛삼원색[hədəf:hədəf+3]=bytes((verilənlər[원본자료+2],verilənlər[원본자료+1],verilənlər[원본자료]))
            if daxiletmə_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        müştəri=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert EXACT_VALUE(müştəri,12)==b'RFB 003.008\n';müştəri.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(müştəri,EXACT_VALUE(müştəri,1)[0]);müştəri.sendall(b'\x01');assert EXACT_VALUE(müştəri,4)==b'\0'*4
        müştəri.sendall(b'\x01');초기값=EXACT_VALUE(müştəri,24);EXACT_VALUE(müştəri,struct.unpack('>I',초기값[20:])[0])
        müştəri.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        müştəri.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in örtük('ftpd start')
        fayl_ötürmə_qoşulma=ftplib.FTP();fayl_ötürmə_qoşulma.encoding='utf-8';fayl_ötürmə_qoşulma.connect('127.0.0.1',파일전송접속번호,timeout=20);fayl_ötürmə_qoşulma.login()
        faydalı_yük_verilənlər=('GUI와 FTP 동시 사용 '+Dil+' 😀\n').encode()
        fayl_ötürmə_qoşulma.storbinary('STOR 함께.txt',io.BytesIO(faydalı_yük_verilənlər))
        assert faydalı_yük_verilənlər.decode().strip() in örtük('cat /함께.txt')
        RECEIVED_COUNT=bytearray();fayl_ötürmə_qoşulma.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==faydalı_yük_verilənlər;fayl_ötürmə_qoşulma.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        göndərmək_Siyahı=örtük('ls /example')
        assert all(Ad in göndərmək_Siyahı for Ad in ('java/','c/','python/','README.md')),göndərmək_Siyahı
        if Dil=='java':
            꾸러미명세=json.loads((Project_kök/'build/examples/manifest.json').read_text())
            for Cığır,daxiletmə_p in 꾸러미명세.items():
                örtük('cp '+Cığır+' /example-check.bin')
                Məzmun_VALUE=bytearray();fayl_ötürmə_qoşulma.retrbinary('RETR example-check.bin',Məzmun_VALUE.extend)
                assert len(Məzmun_VALUE)==daxiletmə_p['bytes'] and hashlib.sha256(Məzmun_VALUE).hexdigest()==daxiletmə_p['sha256'],Cığır
            fayl_ötürmə_qoşulma.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ikili=bytes(range(256))*64
            fayl_ötürmə_qoşulma.storbinary('STOR boundary.bin',io.BytesIO(ikili))
            Məzmun_VALUE=bytearray();fayl_ötürmə_qoşulma.retrbinary('RETR boundary.bin',Məzmun_VALUE.extend)
            assert Məzmun_VALUE==ikili and 'boundary.bin' in fayl_ötürmə_qoşulma.nlst()
            örtük('cp /boundary.bin /boundary-copy.bin')
            Məzmun_VALUE=bytearray();fayl_ötürmə_qoşulma.retrbinary('RETR boundary-copy.bin',Məzmun_VALUE.extend)
            assert Məzmun_VALUE==ikili
            fayl_ötürmə_qoşulma.delete('boundary.bin');fayl_ötürmə_qoşulma.delete('boundary-copy.bin')
        assert '출력예제' in örtük('ls /example/'+Dil)
        örtük('cd /example/'+Dil)
        ad_cədvəl={'java':'JAVA','c':'C','python':'PYTHON'}[Dil]
        예상파일=ad_cədvəl+' FAYL: 한글 verilənlər 😀\n'
        if Dil=='java':
            icra_etmək_əmr('javac 출력예제.java','Compiled:');icra_etmək_əmr('java 출력예제','JAVA 출력: 안녕하세요 😀')
            icra_etmək_əmr('javac 파일예제.java','Compiled:');icra_etmək_əmr('java 파일예제',예상파일)
            icra_etmək_əmr('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_port,되돌림서버항목.UDP_port),'JAVA 네트워크 yoxlamaq: TCP UDP 한글')
            qrafik_elementlər_əmr='java 그래픽예제'
        elif Dil=='c':
            for Ad,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('FAYL','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_port),'C 네트워크 yoxlamaq: UDP 한글')]:
                icra_etmək_əmr('cc '+Ad+'예제.c -o icra_etmək_əmr','Compiled native ARM64 ELF:')
                icra_etmək_əmr('./icra_etmək_əmr'+전달값,예상결과)
            icra_etmək_əmr('cc 그래픽예제.c -o icra_etmək_əmr','Compiled native ARM64 ELF:');qrafik_elementlər_əmr='./icra_etmək_əmr'
        else:
            for Ad,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('FAYL','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_port),'PYTHON 네트워크 yoxlamaq: UDP 한글')]:
                icra_etmək_əmr('python '+Ad+'예제.py'+전달값,예상결과)
            qrafik_elementlər_əmr='python 그래픽예제.py'
        Başla_rəsm=Başla_OFFSET(qrafik_elementlər_əmr)
        Mətn=수신하기('그림을 확인한 GERİ_VALUE Enter를 누르세요.\r\n'.encode(),Başla_rəsm)
        assert ad_cədvəl+' 그래픽: 빨강 초록 파랑' in Mətn and 'exit 0' not in Mətn,Mətn
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        fayl_ötürmə_qoşulma.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();fayl_ötürmə_qoşulma.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';fayl_ötürmə_qoşulma.delete('도중.txt')
        빛삼원색=화소들()
        for Y_koordinat,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(Y_koordinat*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(Dil,Y_koordinat,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(ölçü_verilənlər/(Dil+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Başla_rəsm)
        if Dil=='java':
            Başla_pəncərə=Başla_OFFSET('java 창예제')
            수신하기('GUI 예제 Hazırla: 창예제'.encode(),Başla_pəncərə)
            def klikləmə_VALUE(가로,Şaquli_yerinə_qoymaq):
                for düymə in (1,0):müştəri.sendall(struct.pack('>BBHH',5,düymə,가로,Şaquli_yerinə_qoymaq))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klikləmə_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for simvol_VALUE_068c2631 in '한글':누름값(0x1000000|ord(simvol_VALUE_068c2631));누름값(0x1000000|ord(simvol_VALUE_068c2631),False)
            for 횟수 in (1,2):
                İcra_Et=len(대화기록);klikləmə_VALUE(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),İcra_Et)
            time.sleep(.3)
            pəncərə_rəsm=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=pəncərə_rəsm.crop((110,272,530,300)).tobytes()
            pəncərə_rəsm.save(str(ölçü_verilənlər/'java-swing.png'))
            İcra_Et=len(대화기록);klikləmə_VALUE(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',İcra_Et)
        # Download the guest-created bytes through FTP in the same GUI VM.
        fayl_daxiletmə_ad={'java':'java.txt','c':'c.txt','python':'python.txt'}[Dil]
        örtük('cp '+fayl_daxiletmə_ad+' /təsdiqlə.txt')
        RECEIVED_COUNT=bytearray();fayl_ötürmə_qoşulma.retrbinary('RETR təsdiqlə.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        örtük('echo preserved > 출력예제.'+('py' if Dil=='python' else Dil))
        assert 'EXAMPLES READY' in örtük('example '+Dil)
        assert '\npreserved\n' in örtük('cat 출력예제.'+('py' if Dil=='python' else Dil))
        assert '한/영 Açar_VALUE, Shift+Space 또는 F9' in örtük('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in örtük('echo GUI NETWORK TOGETHER')
        fayl_ötürmə_qoşulma.quit();fayl_ötürmə_qoşulma=None;assert 'FTP stopped' in örtük('ftpd stop')
        print('PASS '+Dil+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if fayl_ötürmə_qoşulma:
            try:fayl_ötürmə_qoşulma.close()
            except OSError:pass
        if müştəri:müştəri.close()
        Proses.terminate()
        try:Proses.wait(timeout=8)
        except subprocess.TimeoutExpired:Proses.kill();Proses.wait()
        seçici.close();Proses.stdout.close();(ölçü_verilənlər/(Dil+'-serial.log')).write_bytes(대화기록)


def İcra_Et():
    ölçü_verilənlər=Project_kök/'build/verification/examples';ölçü_verilənlər.mkdir(parents=True,exist_ok=True)
    yoxlama_hesabat={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_kök/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Dil in ('java','c','python'):
                test_언어(Dil,되돌림서버항목,ölçü_verilənlər);yoxlama_hesabat['languages'].append(Dil)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(sahə_VALUE,verilənlər.encode()) for sahə_VALUE,verilənlər in 예상결과],되돌림서버항목.수신됨
            yoxlama_hesabat['host_network_payloads']=[{'protocol':sahə_VALUE,'text':verilənlər.decode()} for sahə_VALUE,verilənlər in 되돌림서버항목.수신됨]
        yoxlama_hesabat.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(ölçü_verilənlər/'report.json').write_text(json.dumps(yoxlama_hesabat,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':İcra_Et()
