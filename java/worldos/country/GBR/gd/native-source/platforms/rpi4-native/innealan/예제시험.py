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
from deasg_seall import EXACT_VALUE
from 예제되돌림서버 import 되돌림서버
from gnìomhaich_àithne import tilg_freumh


def test_언어(cànan,되돌림서버항목,tomhas_dàta):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Pròiseas=subprocess.Popen(['python3',str(tilg_freumh/'innealan/gnìomhaich_àithne.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    roghnaichear=selectors.DefaultSelector();roghnaichear.register(Pròiseas.stdout,selectors.EVENT_READ)
    대화기록=bytearray();cliant=None;faidhle_tar_chur_ceangal=None
    def 수신하기(확인표시,ruith=0):
        crìochnaich_OFFSET=time.monotonic()+60
        while 확인표시 not in 대화기록[ruith:]:
            if time.monotonic()>crìochnaich_OFFSET or Pròiseas.poll() is not None:raise AssertionError(대화기록[ruith:].decode('utf-8','replace'))
            for 누름값,_ in roghnaichear.select(.1):
                dàta=누름값.fileobj.read(65536)
                if dàta:대화기록.extend(dàta)
        return 대화기록[ruith:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(samhla_VALUE,누르는중=True):cliant.sendall(struct.pack('>BBHI',4,int(누르는중),0,samhla_VALUE))
    def Start_OFFSET(loidhne):
        ruith=len(대화기록)
        for còd_a_charactair in loidhne+'\n':
            samhla_VALUE=0xff0d if còd_a_charactair=='\n' else ord(còd_a_charactair) if ord(còd_a_charactair)<256 else 0x1000000|ord(còd_a_charactair)
            누름값(samhla_VALUE);누름값(samhla_VALUE,False)
        return ruith
    def slige(loidhne):return 수신하기(b'jkoros-native> ',Start_OFFSET(loidhne))
    def gnìomhaich_àithne(loidhne,예상결과):
        SMS=slige(loidhne);assert 예상결과 in SMS and 'exit 0' in SMS,(loidhne,SMS)
        return SMS
    def 화소들():
        cliant.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            roinn_seòrsa_VALUE=EXACT_VALUE(cliant,1)[0]
            if roinn_seòrsa_VALUE==2:continue
            if roinn_seòrsa_VALUE==3:
                nì_COUNT=struct.unpack('>I',EXACT_VALUE(cliant,7)[3:])[0];EXACT_VALUE(cliant,nì_COUNT);continue
            assert roinn_seòrsa_VALUE==0,roinn_seòrsa_VALUE
            cur_a_steach_COUNT=struct.unpack('>H',EXACT_VALUE(cliant,3)[1:])[0]
            for _ in range(cur_a_steach_COUNT):
                co_chomharra_x,세로좌표,너비값,높이값,seata_charactaran=struct.unpack('>HHHHi',EXACT_VALUE(cliant,12));assert seata_charactaran==0,seata_charactaran
                dàta=EXACT_VALUE(cliant,너비값*높이값*4)
                for ROW_suidhich in range(높이값):
                    for colbh_suidhich in range(너비값):
                        원본자료=(ROW_suidhich*너비값+colbh_suidhich)*4;targaid=((세로좌표+ROW_suidhich)*640+co_chomharra_x+colbh_suidhich)*3
                        빛삼원색[targaid:targaid+3]=bytes((dàta[원본자료+2],dàta[원본자료+1],dàta[원본자료]))
            if cur_a_steach_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        cliant=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert EXACT_VALUE(cliant,12)==b'RFB 003.008\n';cliant.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(cliant,EXACT_VALUE(cliant,1)[0]);cliant.sendall(b'\x01');assert EXACT_VALUE(cliant,4)==b'\0'*4
        cliant.sendall(b'\x01');초기값=EXACT_VALUE(cliant,24);EXACT_VALUE(cliant,struct.unpack('>I',초기값[20:])[0])
        cliant.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        cliant.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in slige('ftpd start')
        faidhle_tar_chur_ceangal=ftplib.FTP();faidhle_tar_chur_ceangal.encoding='utf-8';faidhle_tar_chur_ceangal.connect('127.0.0.1',파일전송접속번호,timeout=20);faidhle_tar_chur_ceangal.login()
        payload_dàta=('GUI와 FTP 동시 사용 '+cànan+' 😀\n').encode()
        faidhle_tar_chur_ceangal.storbinary('STOR 함께.txt',io.BytesIO(payload_dàta))
        assert payload_dàta.decode().strip() in slige('cat /함께.txt')
        RECEIVED_COUNT=bytearray();faidhle_tar_chur_ceangal.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==payload_dàta;faidhle_tar_chur_ceangal.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        cuir_Liosta=slige('ls /example')
        assert all(Ainm in cuir_Liosta for Ainm in ('java/','c/','python/','README.md')),cuir_Liosta
        if cànan=='java':
            꾸러미명세=json.loads((tilg_freumh/'build/examples/manifest.json').read_text())
            for Slighe,cur_a_steach_puing in 꾸러미명세.items():
                slige('cp '+Slighe+' /example-check.bin')
                susbaint_VALUE=bytearray();faidhle_tar_chur_ceangal.retrbinary('RETR example-check.bin',susbaint_VALUE.extend)
                assert len(susbaint_VALUE)==cur_a_steach_puing['bytes'] and hashlib.sha256(susbaint_VALUE).hexdigest()==cur_a_steach_puing['sha256'],Slighe
            faidhle_tar_chur_ceangal.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            bìnearaidh=bytes(range(256))*64
            faidhle_tar_chur_ceangal.storbinary('STOR boundary.bin',io.BytesIO(bìnearaidh))
            susbaint_VALUE=bytearray();faidhle_tar_chur_ceangal.retrbinary('RETR boundary.bin',susbaint_VALUE.extend)
            assert susbaint_VALUE==bìnearaidh and 'boundary.bin' in faidhle_tar_chur_ceangal.nlst()
            slige('cp /boundary.bin /boundary-copy.bin')
            susbaint_VALUE=bytearray();faidhle_tar_chur_ceangal.retrbinary('RETR boundary-copy.bin',susbaint_VALUE.extend)
            assert susbaint_VALUE==bìnearaidh
            faidhle_tar_chur_ceangal.delete('boundary.bin');faidhle_tar_chur_ceangal.delete('boundary-copy.bin')
        assert '출력예제' in slige('ls /example/'+cànan)
        slige('cd /example/'+cànan)
        ainm_clàr={'java':'JAVA','c':'C','python':'PYTHON'}[cànan]
        예상파일=ainm_clàr+' faidhle: 한글 dàta 😀\n'
        if cànan=='java':
            gnìomhaich_àithne('javac 출력예제.java','Compiled:');gnìomhaich_àithne('java 출력예제','JAVA 출력: 안녕하세요 😀')
            gnìomhaich_àithne('javac 파일예제.java','Compiled:');gnìomhaich_àithne('java 파일예제',예상파일)
            gnìomhaich_àithne('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_port,되돌림서버항목.UDP_port),'JAVA 네트워크 dearbh: TCP UDP 한글')
            grafaigean_àithne='java 그래픽예제'
        elif cànan=='c':
            for Ainm,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('faidhle','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_port),'C 네트워크 dearbh: UDP 한글')]:
                gnìomhaich_àithne('cc '+Ainm+'예제.c -o gnìomhaich_àithne','Compiled native ARM64 ELF:')
                gnìomhaich_àithne('./gnìomhaich_àithne'+전달값,예상결과)
            gnìomhaich_àithne('cc 그래픽예제.c -o gnìomhaich_àithne','Compiled native ARM64 ELF:');grafaigean_àithne='./gnìomhaich_àithne'
        else:
            for Ainm,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('faidhle','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_port),'PYTHON 네트워크 dearbh: UDP 한글')]:
                gnìomhaich_àithne('python '+Ainm+'예제.py'+전달값,예상결과)
            grafaigean_àithne='python 그래픽예제.py'
        Start_tarraing=Start_OFFSET(grafaigean_àithne)
        SMS=수신하기('그림을 확인한 Air_ais_VALUE Enter를 누르세요.\r\n'.encode(),Start_tarraing)
        assert ainm_clàr+' 그래픽: 빨강 초록 파랑' in SMS and 'exit 0' not in SMS,SMS
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        faidhle_tar_chur_ceangal.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();faidhle_tar_chur_ceangal.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';faidhle_tar_chur_ceangal.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(세로좌표*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(cànan,세로좌표,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(tomhas_dàta/(cànan+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Start_tarraing)
        if cànan=='java':
            Start_uinneag=Start_OFFSET('java 창예제')
            수신하기('GUI 예제 Ullaich: 창예제'.encode(),Start_uinneag)
            def briog_VALUE(가로,inghearach_suidhich):
                for putan in (1,0):cliant.sendall(struct.pack('>BBHH',5,putan,가로,inghearach_suidhich))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            briog_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for caractar_VALUE in '한글':누름값(0x1000000|ord(caractar_VALUE));누름값(0x1000000|ord(caractar_VALUE),False)
            for 횟수 in (1,2):
                ruith=len(대화기록);briog_VALUE(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),ruith)
            time.sleep(.3)
            uinneag_tarraing=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=uinneag_tarraing.crop((110,272,530,300)).tobytes()
            uinneag_tarraing.save(str(tomhas_dàta/'java-swing.png'))
            ruith=len(대화기록);briog_VALUE(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',ruith)
        # Download the guest-created bytes through FTP in the same GUI VM.
        faidhle_cur_a_steach_ainm={'java':'java.txt','c':'c.txt','python':'python.txt'}[cànan]
        slige('cp '+faidhle_cur_a_steach_ainm+' /dearbh_5fb2b747.txt')
        RECEIVED_COUNT=bytearray();faidhle_tar_chur_ceangal.retrbinary('RETR dearbh_5fb2b747.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        slige('echo preserved > 출력예제.'+('py' if cànan=='python' else cànan))
        assert 'EXAMPLES READY' in slige('example '+cànan)
        assert '\npreserved\n' in slige('cat 출력예제.'+('py' if cànan=='python' else cànan))
        assert '한/영 Iuchair_VALUE, Shift+Space 또는 F9' in slige('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in slige('echo GUI NETWORK TOGETHER')
        faidhle_tar_chur_ceangal.quit();faidhle_tar_chur_ceangal=None;assert 'FTP stopped' in slige('ftpd stop')
        print('PASS '+cànan+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if faidhle_tar_chur_ceangal:
            try:faidhle_tar_chur_ceangal.close()
            except OSError:pass
        if cliant:cliant.close()
        Pròiseas.terminate()
        try:Pròiseas.wait(timeout=8)
        except subprocess.TimeoutExpired:Pròiseas.kill();Pròiseas.wait()
        roghnaichear.close();Pròiseas.stdout.close();(tomhas_dàta/(cànan+'-serial.log')).write_bytes(대화기록)


def ruith():
    tomhas_dàta=tilg_freumh/'build/verification/examples';tomhas_dàta.mkdir(parents=True,exist_ok=True)
    dearbhadh_aithisg={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((tilg_freumh/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for cànan in ('java','c','python'):
                test_언어(cànan,되돌림서버항목,tomhas_dàta);dearbhadh_aithisg['languages'].append(cànan)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(roinn_seòrsa_VALUE,dàta.encode()) for roinn_seòrsa_VALUE,dàta in 예상결과],되돌림서버항목.수신됨
            dearbhadh_aithisg['host_network_payloads']=[{'protocol':roinn_seòrsa_VALUE,'text':dàta.decode()} for roinn_seòrsa_VALUE,dàta in 되돌림서버항목.수신됨]
        dearbhadh_aithisg.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(tomhas_dàta/'report.json').write_text(json.dumps(dearbhadh_aithisg,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ruith()
