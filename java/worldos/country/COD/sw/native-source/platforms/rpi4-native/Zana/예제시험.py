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
from Eneo_kazi_Onesha import 정확한값
from 예제되돌림서버 import 되돌림서버
from tekeleza_amri import 기준


def test_언어(Lugha,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));faili_hamisha_namba_ya_kituo=임시자원.getsockname()[1]
    Mchakato=subprocess.Popen(['python3',str(기준/'Zana/tekeleza_amri.py'),'--desktop','--network','--port','0','--ftp-port',str(faili_hamisha_namba_ya_kituo)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    kiteuzi=selectors.DefaultSelector();kiteuzi.register(Mchakato.stdout,selectors.EVENT_READ)
    대화기록=bytearray();teja=None;faili_hamisha_muunganisho=None
    def 수신하기(확인표시,endesha=0):
        tamatia_Chipua=time.monotonic()+60
        while 확인표시 not in 대화기록[endesha:]:
            if time.monotonic()>tamatia_Chipua or Mchakato.poll() is not None:raise AssertionError(대화기록[endesha:].decode('utf-8','replace'))
            for 누름값,_ in kiteuzi.select(.1):
                data=누름값.fileobj.read(65536)
                if data:대화기록.extend(data)
        return 대화기록[endesha:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(ishara_thamani,누르는중=True):teja.sendall(struct.pack('>BBHI',4,int(누르는중),0,ishara_thamani))
    def Anza_Chipua(laini):
        endesha=len(대화기록)
        for msimbo_wa_kibambo in laini+'\n':
            ishara_thamani=0xff0d if msimbo_wa_kibambo=='\n' else ord(msimbo_wa_kibambo) if ord(msimbo_wa_kibambo)<256 else 0x1000000|ord(msimbo_wa_kibambo)
            누름값(ishara_thamani);누름값(ishara_thamani,False)
        return endesha
    def sheli(laini):return 수신하기(b'jkoros-native> ',Anza_Chipua(laini))
    def tekeleza_amri(laini,예상결과):
        SMS=sheli(laini);assert 예상결과 in SMS and 'exit 0' in SMS,(laini,SMS)
        return SMS
    def 화소들():
        teja.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            kategoria_thamani=정확한값(teja,1)[0]
            if kategoria_thamani==2:continue
            if kategoria_thamani==3:
                개수=struct.unpack('>I',정확한값(teja,7)[3:])[0];정확한값(teja,개수);continue
            assert kategoria_thamani==0,kategoria_thamani
            항목수=struct.unpack('>H',정확한값(teja,3)[1:])[0]
            for _ in range(항목수):
                jira_x,Kitufe_cha_Y_kiratibu,너비값,높이값,seti_kibambo=struct.unpack('>HHHHi',정확한값(teja,12));assert seti_kibambo==0,seti_kibambo
                data=정확한값(teja,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;lengo=((Kitufe_cha_Y_kiratibu+행위치)*640+jira_x+열위치)*3
                        빛삼원색[lengo:lengo+3]=bytes((data[원본자료+2],data[원본자료+1],data[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        namba_ya_kituo=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        teja=socket.create_connection(('127.0.0.1',namba_ya_kituo),timeout=10)
        assert 정확한값(teja,12)==b'RFB 003.008\n';teja.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(teja,정확한값(teja,1)[0]);teja.sendall(b'\x01');assert 정확한값(teja,4)==b'\0'*4
        teja.sendall(b'\x01');초기값=정확한값(teja,24);정확한값(teja,struct.unpack('>I',초기값[20:])[0])
        teja.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        teja.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in sheli('ftpd start')
        faili_hamisha_muunganisho=ftplib.FTP();faili_hamisha_muunganisho.encoding='utf-8';faili_hamisha_muunganisho.connect('127.0.0.1',faili_hamisha_namba_ya_kituo,timeout=20);faili_hamisha_muunganisho.login()
        data_muhimu_data=('GUI와 FTP 동시 사용 '+Lugha+' 😀\n').encode()
        faili_hamisha_muunganisho.storbinary('STOR 함께.txt',io.BytesIO(data_muhimu_data))
        assert data_muhimu_data.decode().strip() in sheli('cat /함께.txt')
        받은수=bytearray();faili_hamisha_muunganisho.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==data_muhimu_data;faili_hamisha_muunganisho.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        tuma_Orodha=sheli('ls /example')
        assert all(Jina in tuma_Orodha for Jina in ('java/','c/','python/','README.md')),tuma_Orodha
        if Lugha=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for njia,ingizo_pointi in 꾸러미명세.items():
                sheli('cp '+njia+' /example-check.bin')
                maudhui_thamani=bytearray();faili_hamisha_muunganisho.retrbinary('RETR example-check.bin',maudhui_thamani.extend)
                assert len(maudhui_thamani)==ingizo_pointi['bytes'] and hashlib.sha256(maudhui_thamani).hexdigest()==ingizo_pointi['sha256'],njia
            faili_hamisha_muunganisho.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            jozi=bytes(range(256))*64
            faili_hamisha_muunganisho.storbinary('STOR boundary.bin',io.BytesIO(jozi))
            maudhui_thamani=bytearray();faili_hamisha_muunganisho.retrbinary('RETR boundary.bin',maudhui_thamani.extend)
            assert maudhui_thamani==jozi and 'boundary.bin' in faili_hamisha_muunganisho.nlst()
            sheli('cp /boundary.bin /boundary-copy.bin')
            maudhui_thamani=bytearray();faili_hamisha_muunganisho.retrbinary('RETR boundary-copy.bin',maudhui_thamani.extend)
            assert maudhui_thamani==jozi
            faili_hamisha_muunganisho.delete('boundary.bin');faili_hamisha_muunganisho.delete('boundary-copy.bin')
        assert '출력예제' in sheli('ls /example/'+Lugha)
        sheli('cd /example/'+Lugha)
        jina_jedwali={'java':'JAVA','c':'C','python':'PYTHON'}[Lugha]
        예상파일=jina_jedwali+' faili: 한글 data 😀\n'
        if Lugha=='java':
            tekeleza_amri('javac 출력예제.java','Compiled:');tekeleza_amri('java 출력예제','JAVA 출력: 안녕하세요 😀')
            tekeleza_amri('javac 파일예제.java','Compiled:');tekeleza_amri('java 파일예제',예상파일)
            tekeleza_amri('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_kituo,되돌림서버항목.전문접속번호),'JAVA 네트워크 thibitisha: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif Lugha=='c':
            for Jina,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('faili','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 thibitisha: UDP 한글')]:
                tekeleza_amri('cc '+Jina+'예제.c -o tekeleza_amri','Compiled native ARM64 ELF:')
                tekeleza_amri('./tekeleza_amri'+전달값,예상결과)
            tekeleza_amri('cc 그래픽예제.c -o tekeleza_amri','Compiled native ARM64 ELF:');그림명령='./tekeleza_amri'
        else:
            for Jina,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('faili','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 thibitisha: UDP 한글')]:
                tekeleza_amri('python '+Jina+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        Anza_mchoro=Anza_Chipua(그림명령)
        SMS=수신하기('그림을 확인한 Nyuma_thamani Enter를 누르세요.\r\n'.encode(),Anza_mchoro)
        assert jina_jedwali+' 그래픽: 빨강 초록 파랑' in SMS and 'exit 0' not in SMS,SMS
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        faili_hamisha_muunganisho.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();faili_hamisha_muunganisho.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';faili_hamisha_muunganisho.delete('도중.txt')
        빛삼원색=화소들()
        for Kitufe_cha_Y_kiratibu,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Chipua_thamani=(Kitufe_cha_Y_kiratibu*640+610)*3;assert tuple(빛삼원색[Chipua_thamani:Chipua_thamani+3])==색상,(Lugha,Kitufe_cha_Y_kiratibu,tuple(빛삼원색[Chipua_thamani:Chipua_thamani+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(Lugha+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Anza_mchoro)
        if Lugha=='java':
            Anza_dirisha=Anza_Chipua('java 창예제')
            수신하기('GUI 예제 Andaa: 창예제'.encode(),Anza_dirisha)
            def bofya_thamani(가로,세로):
                for kitufe in (1,0):teja.sendall(struct.pack('>BBHH',5,kitufe,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            bofya_thamani(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for kibambo_thamani in '한글':누름값(0x1000000|ord(kibambo_thamani));누름값(0x1000000|ord(kibambo_thamani),False)
            for 횟수 in (1,2):
                endesha=len(대화기록);bofya_thamani(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),endesha)
            time.sleep(.3)
            dirisha_mchoro=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=dirisha_mchoro.crop((110,272,530,300)).tobytes()
            dirisha_mchoro.save(str(결과자료/'java-swing.png'))
            endesha=len(대화기록);bofya_thamani(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',endesha)
        # Download the guest-created bytes through FTP in the same GUI VM.
        faili_ingizo_jina={'java':'java.txt','c':'c.txt','python':'python.txt'}[Lugha]
        sheli('cp '+faili_ingizo_jina+' /hakikisha.txt')
        받은수=bytearray();faili_hamisha_muunganisho.retrbinary('RETR hakikisha.txt',받은수.extend);assert 받은수==예상파일.encode()
        sheli('echo preserved > 출력예제.'+('py' if Lugha=='python' else Lugha))
        assert 'EXAMPLES READY' in sheli('example '+Lugha)
        assert '\npreserved\n' in sheli('cat 출력예제.'+('py' if Lugha=='python' else Lugha))
        assert '한/영 Kitufe_thamani, Shift+Space 또는 F9' in sheli('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in sheli('echo GUI NETWORK TOGETHER')
        faili_hamisha_muunganisho.quit();faili_hamisha_muunganisho=None;assert 'FTP stopped' in sheli('ftpd stop')
        print('PASS '+Lugha+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if faili_hamisha_muunganisho:
            try:faili_hamisha_muunganisho.close()
            except OSError:pass
        if teja:teja.close()
        Mchakato.terminate()
        try:Mchakato.wait(timeout=8)
        except subprocess.TimeoutExpired:Mchakato.kill();Mchakato.wait()
        kiteuzi.close();Mchakato.stdout.close();(결과자료/(Lugha+'-serial.log')).write_bytes(대화기록)


def endesha():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    uhakikishi_ripoti={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Lugha in ('java','c','python'):
                test_언어(Lugha,되돌림서버항목,결과자료);uhakikishi_ripoti['languages'].append(Lugha)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(kategoria_thamani,data.encode()) for kategoria_thamani,data in 예상결과],되돌림서버항목.수신됨
            uhakikishi_ripoti['host_network_payloads']=[{'protocol':kategoria_thamani,'text':data.decode()} for kategoria_thamani,data in 되돌림서버항목.수신됨]
        uhakikishi_ripoti.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(uhakikishi_ripoti,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':endesha()
