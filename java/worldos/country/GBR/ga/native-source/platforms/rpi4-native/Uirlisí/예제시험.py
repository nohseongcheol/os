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
from deasc_Amharc import EXACT_VALUE
from 예제되돌림서버 import 되돌림서버
from Rith_ordú import teilgean_fréamh


def test_언어(Teanga,되돌림서버항목,tomhas_sonraí):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));comhad_traschur_uimhir_phoirt=임시자원.getsockname()[1]
    Próiseas=subprocess.Popen(['python3',str(teilgean_fréamh/'Uirlisí/Rith_ordú.py'),'--desktop','--network','--port','0','--ftp-port',str(comhad_traschur_uimhir_phoirt)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    roghnóir=selectors.DefaultSelector();roghnóir.register(Próiseas.stdout,selectors.EVENT_READ)
    대화기록=bytearray();cliant=None;comhad_traschur_nasc=None
    def 수신하기(확인표시,Rith_2=0):
        cuir_deireadh_le_OFFSET=time.monotonic()+60
        while 확인표시 not in 대화기록[Rith_2:]:
            if time.monotonic()>cuir_deireadh_le_OFFSET or Próiseas.poll() is not None:raise AssertionError(대화기록[Rith_2:].decode('utf-8','replace'))
            for 누름값,_ in roghnóir.select(.1):
                sonraí=누름값.fileobj.read(65536)
                if sonraí:대화기록.extend(sonraí)
        return 대화기록[Rith_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(siombail_VALUE,누르는중=True):cliant.sendall(struct.pack('>BBHI',4,int(누르는중),0,siombail_VALUE))
    def Start_OFFSET(Líne):
        Rith_2=len(대화기록)
        for pointe_cóid in Líne+'\n':
            siombail_VALUE=0xff0d if pointe_cóid=='\n' else ord(pointe_cóid) if ord(pointe_cóid)<256 else 0x1000000|ord(pointe_cóid)
            누름값(siombail_VALUE);누름값(siombail_VALUE,False)
        return Rith_2
    def blaosc(Líne):return 수신하기(b'jkoros-native> ',Start_OFFSET(Líne))
    def Rith_ordú(Líne,예상결과):
        Téacs=blaosc(Líne);assert 예상결과 in Téacs and 'exit 0' in Téacs,(Líne,Téacs)
        return Téacs
    def 화소들():
        cliant.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            catagóir_VALUE=EXACT_VALUE(cliant,1)[0]
            if catagóir_VALUE==2:continue
            if catagóir_VALUE==3:
                mír_COUNT=struct.unpack('>I',EXACT_VALUE(cliant,7)[3:])[0];EXACT_VALUE(cliant,mír_COUNT);continue
            assert catagóir_VALUE==0,catagóir_VALUE
            iontráil_COUNT=struct.unpack('>H',EXACT_VALUE(cliant,3)[1:])[0]
            for _ in range(iontráil_COUNT):
                x_chomhordanáid,세로좌표,너비값,높이값,tacar_carachtar=struct.unpack('>HHHHi',EXACT_VALUE(cliant,12));assert tacar_carachtar==0,tacar_carachtar
                sonraí=EXACT_VALUE(cliant,너비값*높이값*4)
                for ró_suíomh in range(높이값):
                    for colún_suíomh in range(너비값):
                        원본자료=(ró_suíomh*너비값+colún_suíomh)*4;sprioc=((세로좌표+ró_suíomh)*640+x_chomhordanáid+colún_suíomh)*3
                        빛삼원색[sprioc:sprioc+3]=bytes((sonraí[원본자료+2],sonraí[원본자료+1],sonraí[원본자료]))
            if iontráil_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        uimhir_phoirt=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        cliant=socket.create_connection(('127.0.0.1',uimhir_phoirt),timeout=10)
        assert EXACT_VALUE(cliant,12)==b'RFB 003.008\n';cliant.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(cliant,EXACT_VALUE(cliant,1)[0]);cliant.sendall(b'\x01');assert EXACT_VALUE(cliant,4)==b'\0'*4
        cliant.sendall(b'\x01');초기값=EXACT_VALUE(cliant,24);EXACT_VALUE(cliant,struct.unpack('>I',초기값[20:])[0])
        cliant.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        cliant.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in blaosc('ftpd start')
        comhad_traschur_nasc=ftplib.FTP();comhad_traschur_nasc.encoding='utf-8';comhad_traschur_nasc.connect('127.0.0.1',comhad_traschur_uimhir_phoirt,timeout=20);comhad_traschur_nasc.login()
        pálasta_sonraí=('GUI와 FTP 동시 사용 '+Teanga+' 😀\n').encode()
        comhad_traschur_nasc.storbinary('STOR 함께.txt',io.BytesIO(pálasta_sonraí))
        assert pálasta_sonraí.decode().strip() in blaosc('cat /함께.txt')
        RECEIVED_COUNT=bytearray();comhad_traschur_nasc.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==pálasta_sonraí;comhad_traschur_nasc.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        seol_Liosta=blaosc('ls /example')
        assert all(Ainm in seol_Liosta for Ainm in ('java/','c/','python/','README.md')),seol_Liosta
        if Teanga=='java':
            꾸러미명세=json.loads((teilgean_fréamh/'build/examples/manifest.json').read_text())
            for CONAIR,iontráil_pointe in 꾸러미명세.items():
                blaosc('cp '+CONAIR+' /example-check.bin')
                Inneachar_VALUE=bytearray();comhad_traschur_nasc.retrbinary('RETR example-check.bin',Inneachar_VALUE.extend)
                assert len(Inneachar_VALUE)==iontráil_pointe['bytes'] and hashlib.sha256(Inneachar_VALUE).hexdigest()==iontráil_pointe['sha256'],CONAIR
            comhad_traschur_nasc.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            dénártha=bytes(range(256))*64
            comhad_traschur_nasc.storbinary('STOR boundary.bin',io.BytesIO(dénártha))
            Inneachar_VALUE=bytearray();comhad_traschur_nasc.retrbinary('RETR boundary.bin',Inneachar_VALUE.extend)
            assert Inneachar_VALUE==dénártha and 'boundary.bin' in comhad_traschur_nasc.nlst()
            blaosc('cp /boundary.bin /boundary-copy.bin')
            Inneachar_VALUE=bytearray();comhad_traschur_nasc.retrbinary('RETR boundary-copy.bin',Inneachar_VALUE.extend)
            assert Inneachar_VALUE==dénártha
            comhad_traschur_nasc.delete('boundary.bin');comhad_traschur_nasc.delete('boundary-copy.bin')
        assert '출력예제' in blaosc('ls /example/'+Teanga)
        blaosc('cd /example/'+Teanga)
        ainm_tábla={'java':'JAVA','c':'C','python':'PYTHON'}[Teanga]
        예상파일=ainm_tábla+' Comhad: 한글 sonraí 😀\n'
        if Teanga=='java':
            Rith_ordú('javac 출력예제.java','Compiled:');Rith_ordú('java 출력예제','JAVA Aschur: 안녕하세요 😀')
            Rith_ordú('javac 파일예제.java','Compiled:');Rith_ordú('java 파일예제',예상파일)
            Rith_ordú('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_port,되돌림서버항목.UDP_port),'JAVA 네트워크 fíoraigh: TCP UDP 한글')
            grafaic_ordú='java 그래픽예제'
        elif Teanga=='c':
            for Ainm,전달값,예상결과 in [('Aschur','', 'C Aschur: 안녕하세요 😀'),('Comhad','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_port),'C 네트워크 fíoraigh: UDP 한글')]:
                Rith_ordú('cc '+Ainm+'예제.c -o Rith_ordú','Compiled native ARM64 ELF:')
                Rith_ordú('./Rith_ordú'+전달값,예상결과)
            Rith_ordú('cc 그래픽예제.c -o Rith_ordú','Compiled native ARM64 ELF:');grafaic_ordú='./Rith_ordú'
        else:
            for Ainm,전달값,예상결과 in [('Aschur','','PYTHON Aschur: 안녕하세요 😀'),('Comhad','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_port),'PYTHON 네트워크 fíoraigh: UDP 한글')]:
                Rith_ordú('python '+Ainm+'예제.py'+전달값,예상결과)
            grafaic_ordú='python 그래픽예제.py'
        Start_líníocht=Start_OFFSET(grafaic_ordú)
        Téacs=수신하기('그림을 확인한 Siar_VALUE Enter를 누르세요.\r\n'.encode(),Start_líníocht)
        assert ainm_tábla+' 그래픽: 빨강 초록 파랑' in Téacs and 'exit 0' not in Téacs,Téacs
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        comhad_traschur_nasc.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();comhad_traschur_nasc.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';comhad_traschur_nasc.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(세로좌표*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(Teanga,세로좌표,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(tomhas_sonraí/(Teanga+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Start_líníocht)
        if Teanga=='java':
            Start_fuinneog=Start_OFFSET('java 창예제')
            수신하기('GUI 예제 Ullmhaigh: 창예제'.encode(),Start_fuinneog)
            def cliceáil_VALUE(가로,Ingearach_suíomh):
                for cnaipe in (1,0):cliant.sendall(struct.pack('>BBHH',5,cnaipe,가로,Ingearach_suíomh))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            cliceáil_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for carachtar_VALUE in '한글':누름값(0x1000000|ord(carachtar_VALUE));누름값(0x1000000|ord(carachtar_VALUE),False)
            for 횟수 in (1,2):
                Rith_2=len(대화기록);cliceáil_VALUE(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Rith_2)
            time.sleep(.3)
            fuinneog_líníocht=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=fuinneog_líníocht.crop((110,272,530,300)).tobytes()
            fuinneog_líníocht.save(str(tomhas_sonraí/'java-swing.png'))
            Rith_2=len(대화기록);cliceáil_VALUE(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Rith_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        comhad_iontráil_ainm={'java':'java.txt','c':'c.txt','python':'python.txt'}[Teanga]
        blaosc('cp '+comhad_iontráil_ainm+' /bailíochtaigh.txt')
        RECEIVED_COUNT=bytearray();comhad_traschur_nasc.retrbinary('RETR bailíochtaigh.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        blaosc('echo preserved > 출력예제.'+('py' if Teanga=='python' else Teanga))
        assert 'EXAMPLES READY' in blaosc('example '+Teanga)
        assert '\npreserved\n' in blaosc('cat 출력예제.'+('py' if Teanga=='python' else Teanga))
        assert '한/영 eochair_VALUE, Shift+Space 또는 F9' in blaosc('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in blaosc('echo GUI NETWORK TOGETHER')
        comhad_traschur_nasc.quit();comhad_traschur_nasc=None;assert 'FTP stopped' in blaosc('ftpd stop')
        print('PASS '+Teanga+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if comhad_traschur_nasc:
            try:comhad_traschur_nasc.close()
            except OSError:pass
        if cliant:cliant.close()
        Próiseas.terminate()
        try:Próiseas.wait(timeout=8)
        except subprocess.TimeoutExpired:Próiseas.kill();Próiseas.wait()
        roghnóir.close();Próiseas.stdout.close();(tomhas_sonraí/(Teanga+'-serial.log')).write_bytes(대화기록)


def Rith_2():
    tomhas_sonraí=teilgean_fréamh/'build/verification/examples';tomhas_sonraí.mkdir(parents=True,exist_ok=True)
    bailíochtú_tuairisc={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((teilgean_fréamh/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Teanga in ('java','c','python'):
                test_언어(Teanga,되돌림서버항목,tomhas_sonraí);bailíochtú_tuairisc['languages'].append(Teanga)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(catagóir_VALUE,sonraí.encode()) for catagóir_VALUE,sonraí in 예상결과],되돌림서버항목.수신됨
            bailíochtú_tuairisc['host_network_payloads']=[{'protocol':catagóir_VALUE,'text':sonraí.decode()} for catagóir_VALUE,sonraí in 되돌림서버항목.수신됨]
        bailíochtú_tuairisc.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(tomhas_sonraí/'report.json').write_text(json.dumps(bailíochtú_tuairisc,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Rith_2()
