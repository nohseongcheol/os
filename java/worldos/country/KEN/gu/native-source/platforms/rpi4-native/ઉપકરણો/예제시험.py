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
from ડેસ્કટૉપ_જુઓ import 정확한값
from 예제되돌림서버 import 되돌림서버
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ


def test_언어(ભાષા,되돌림서버항목,પરિમાણ_ડેટા):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર=임시자원.getsockname()[1]
    પ્રક્રિયા=subprocess.Popen(['python3',str(પ્રોજેક્ટ_રૂટ/'ઉપકરણો/અમલ_કરો_આદેશ.py'),'--desktop','--network','--port','0','--ftp-port',str(ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    પસંદકર્તા=selectors.DefaultSelector();પસંદકર્તા.register(પ્રક્રિયા.stdout,selectors.EVENT_READ)
    대화기록=bytearray();ક્લાયંટ=None;ફાઇલ_સ્થાનાંતર_કનેક્શન=None
    def 수신하기(확인표시,ચલાવો_2=0):
        અંત_કરો_ઑફસેટ=time.monotonic()+60
        while 확인표시 not in 대화기록[ચલાવો_2:]:
            if time.monotonic()>અંત_કરો_ઑફસેટ or પ્રક્રિયા.poll() is not None:raise AssertionError(대화기록[ચલાવો_2:].decode('utf-8','replace'))
            for 누름값,_ in પસંદકર્તા.select(.1):
                ડેટા=누름값.fileobj.read(65536)
                if ડેટા:대화기록.extend(ડેટા)
        return 대화기록[ચલાવો_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(પ્રતીક_મૂલ્ય,누르는중=True):ક્લાયંટ.sendall(struct.pack('>BBHI',4,int(누르는중),0,પ્રતીક_મૂલ્ય))
    def પ્રારંભ_ઑફસેટ(લાઇન):
        ચલાવો_2=len(대화기록)
        for વર્ણ_કોડ in લાઇન+'\n':
            પ્રતીક_મૂલ્ય=0xff0d if વર્ણ_કોડ=='\n' else ord(વર્ણ_કોડ) if ord(વર્ણ_કોડ)<256 else 0x1000000|ord(વર્ણ_કોડ)
            누름값(પ્રતીક_મૂલ્ય);누름값(પ્રતીક_મૂલ્ય,False)
        return ચલાવો_2
    def શેલ(લાઇન):return 수신하기(b'jkoros-native> ',પ્રારંભ_ઑફસેટ(લાઇન))
    def અમલ_કરો_આદેશ(લાઇન,예상결과):
        લખાણ=શેલ(લાઇન);assert 예상결과 in લખાણ and 'exit 0' in લખાણ,(લાઇન,લખાણ)
        return લખાણ
    def 화소들():
        ક્લાયંટ.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            શ્રેણી_મૂલ્ય=정확한값(ક્લાયંટ,1)[0]
            if શ્રેણી_મૂલ્ય==2:continue
            if શ્રેણી_મૂલ્ય==3:
                개수=struct.unpack('>I',정확한값(ક્લાયંટ,7)[3:])[0];정확한값(ક્લાયંટ,개수);continue
            assert શ્રેણી_મૂલ્ય==0,શ્રેણી_મૂલ્ય
            항목수=struct.unpack('>H',정확한값(ક્લાયંટ,3)[1:])[0]
            for _ in range(항목수):
                x_યામ,세로좌표,너비값,높이값,વર્ણ_સેટ=struct.unpack('>HHHHi',정확한값(ક્લાયંટ,12));assert વર્ણ_સેટ==0,વર્ણ_સેટ
                ડેટા=정확한값(ક્લાયંટ,너비값*높이값*4)
                for પંક્તિ_સ્થિતિ in range(높이값):
                    for હરોળ_સ્થિતિ in range(너비값):
                        원본자료=(પંક્તિ_સ્થિતિ*너비값+હરોળ_સ્થિતિ)*4;લક્ષ્ય=((세로좌표+પંક્તિ_સ્થિતિ)*640+x_યામ+હરોળ_સ્થિતિ)*3
                        빛삼원색[લક્ષ્ય:લક્ષ્ય+3]=bytes((ડેટા[원본자료+2],ડેટા[원본자료+1],ડેટા[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        પોર્ટ_નંબર=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        ક્લાયંટ=socket.create_connection(('127.0.0.1',પોર્ટ_નંબર),timeout=10)
        assert 정확한값(ક્લાયંટ,12)==b'RFB 003.008\n';ક્લાયંટ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ક્લાયંટ,정확한값(ક્લાયંટ,1)[0]);ક્લાયંટ.sendall(b'\x01');assert 정확한값(ક્લાયંટ,4)==b'\0'*4
        ક્લાયંટ.sendall(b'\x01');초기값=정확한값(ક્લાયંટ,24);정확한값(ક્લાયંટ,struct.unpack('>I',초기값[20:])[0])
        ક્લાયંટ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        ક્લાયંટ.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in શેલ('ftpd start')
        ફાઇલ_સ્થાનાંતર_કનેક્શન=ftplib.FTP();ફાઇલ_સ્થાનાંતર_કનેક્શન.encoding='utf-8';ફાઇલ_સ્થાનાંતર_કનેક્શન.connect('127.0.0.1',ફાઇલ_સ્થાનાંતર_પોર્ટ_નંબર,timeout=20);ફાઇલ_સ્થાનાંતર_કનેક્શન.login()
        પેલોડ_ડેટા=('GUI와 FTP 동시 사용 '+ભાષા+' 😀\n').encode()
        ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR 함께.txt',io.BytesIO(પેલોડ_ડેટા))
        assert પેલોડ_ડેટા.decode().strip() in શેલ('cat /함께.txt')
        받은수=bytearray();ફાઇલ_સ્થાનાંતર_કનેક્શન.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==પેલોડ_ડેટા;ફાઇલ_સ્થાનાંતર_કનેક્શન.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        મોકલો_સૂચી=શેલ('ls /example')
        assert all(નામ in મોકલો_સૂચી for નામ in ('java/','c/','python/','README.md')),મોકલો_સૂચી
        if ભાષા=='java':
            꾸러미명세=json.loads((પ્રોજેક્ટ_રૂટ/'build/examples/manifest.json').read_text())
            for પથ,પ્રવેશ_બિંદુ in 꾸러미명세.items():
                શેલ('cp '+પથ+' /example-check.bin')
                સામગ્રી_મૂલ્ય=bytearray();ફાઇલ_સ્થાનાંતર_કનેક્શન.retrbinary('RETR example-check.bin',સામગ્રી_મૂલ્ય.extend)
                assert len(સામગ્રી_મૂલ્ય)==પ્રવેશ_બિંદુ['bytes'] and hashlib.sha256(સામગ્રી_મૂલ્ય).hexdigest()==પ્રવેશ_બિંદુ['sha256'],પથ
            ફાઇલ_સ્થાનાંતર_કનેક્શન.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            બાઇનરી=bytes(range(256))*64
            ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR boundary.bin',io.BytesIO(બાઇનરી))
            સામગ્રી_મૂલ્ય=bytearray();ફાઇલ_સ્થાનાંતર_કનેક્શન.retrbinary('RETR boundary.bin',સામગ્રી_મૂલ્ય.extend)
            assert સામગ્રી_મૂલ્ય==બાઇનરી and 'boundary.bin' in ફાઇલ_સ્થાનાંતર_કનેક્શન.nlst()
            શેલ('cp /boundary.bin /boundary-copy.bin')
            સામગ્રી_મૂલ્ય=bytearray();ફાઇલ_સ્થાનાંતર_કનેક્શન.retrbinary('RETR boundary-copy.bin',સામગ્રી_મૂલ્ય.extend)
            assert સામગ્રી_મૂલ્ય==બાઇનરી
            ફાઇલ_સ્થાનાંતર_કનેક્શન.delete('boundary.bin');ફાઇલ_સ્થાનાંતર_કનેક્શન.delete('boundary-copy.bin')
        assert '출력예제' in શેલ('ls /example/'+ભાષા)
        શેલ('cd /example/'+ભાષા)
        નામ_કોષ્ટક={'java':'JAVA','c':'C','python':'PYTHON'}[ભાષા]
        예상파일=નામ_કોષ્ટક+' ફાઈલ: 한글 ડેટા 😀\n'
        if ભાષા=='java':
            અમલ_કરો_આદેશ('javac 출력예제.java','Compiled:');અમલ_કરો_આદેશ('java 출력예제','JAVA આઉટપુટ: 안녕하세요 😀')
            અમલ_કરો_આદેશ('javac 파일예제.java','Compiled:');અમલ_કરો_આદેશ('java 파일예제',예상파일)
            અમલ_કરો_આદેશ('java 네트워크예제 {} {}'.format(되돌림서버항목.પ્રસારણ_નિયંત્રણ_પ્રોટોકૉલ_પૉર્ટ,되돌림서버항목.전문접속번호),'JAVA 네트워크 ચકાસવું: TCP UDP 한글')
            ગ્રાફિક્સ_આદેશ='java 그래픽예제'
        elif ભાષા=='c':
            for નામ,전달값,예상결과 in [('આઉટપુટ','', 'C આઉટપુટ: 안녕하세요 😀'),('ફાઈલ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 ચકાસવું: UDP 한글')]:
                અમલ_કરો_આદેશ('cc '+નામ+'예제.c -o અમલ_કરો_આદેશ','Compiled native ARM64 ELF:')
                અમલ_કરો_આદેશ('./અમલ_કરો_આદેશ'+전달값,예상결과)
            અમલ_કરો_આદેશ('cc 그래픽예제.c -o અમલ_કરો_આદેશ','Compiled native ARM64 ELF:');ગ્રાફિક્સ_આદેશ='./અમલ_કરો_આદેશ'
        else:
            for નામ,전달값,예상결과 in [('આઉટપુટ','','PYTHON આઉટપુટ: 안녕하세요 😀'),('ફાઈલ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 ચકાસવું: UDP 한글')]:
                અમલ_કરો_આદેશ('python '+નામ+'예제.py'+전달값,예상결과)
            ગ્રાફિક્સ_આદેશ='python 그래픽예제.py'
        પ્રારંભ_રેખાંકન=પ્રારંભ_ઑફસેટ(ગ્રાફિક્સ_આદેશ)
        લખાણ=수신하기('그림을 확인한 બેક_મૂલ્ય Enter를 누르세요.\r\n'.encode(),પ્રારંભ_રેખાંકન)
        assert નામ_કોષ્ટક+' 그래픽: 빨강 초록 파랑' in લખાણ and 'exit 0' not in લખાણ,લખાણ
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ફાઇલ_સ્થાનાંતર_કનેક્શન.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ફાઇલ_સ્થાનાંતર_કનેક્શન.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ઑફસેટ_મૂલ્ય=(세로좌표*640+610)*3;assert tuple(빛삼원색[ઑફસેટ_મૂલ્ય:ઑફસેટ_મૂલ્ય+3])==색상,(ભાષા,세로좌표,tuple(빛삼원색[ઑફસેટ_મૂલ્ય:ઑફસેટ_મૂલ્ય+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(પરિમાણ_ડેટા/(ભાષા+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',પ્રારંભ_રેખાંકન)
        if ભાષા=='java':
            પ્રારંભ_વિંડો=પ્રારંભ_ઑફસેટ('java 창예제')
            수신하기('GUI 예제 તૈયાર_કરો: 창예제'.encode(),પ્રારંભ_વિંડો)
            def ક્લિક_કરો_મૂલ્ય(가로,ઊભી_સ્થિતિ):
                for બટન in (1,0):ક્લાયંટ.sendall(struct.pack('>BBHH',5,બટન,가로,ઊભી_સ્થિતિ))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            ક્લિક_કરો_મૂલ્ય(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for વર્ણ_મૂલ્ય in '한글':누름값(0x1000000|ord(વર્ણ_મૂલ્ય));누름값(0x1000000|ord(વર્ણ_મૂલ્ય),False)
            for 횟수 in (1,2):
                ચલાવો_2=len(대화기록);ક્લિક_કરો_મૂલ્ય(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),ચલાવો_2)
            time.sleep(.3)
            વિંડો_રેખાંકન=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=વિંડો_રેખાંકન.crop((110,272,530,300)).tobytes()
            વિંડો_રેખાંકન.save(str(પરિમાણ_ડેટા/'java-swing.png'))
            ચલાવો_2=len(대화기록);ક્લિક_કરો_મૂલ્ય(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',ચલાવો_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ફાઇલ_પ્રવેશ_નામ={'java':'java.txt','c':'c.txt','python':'python.txt'}[ભાષા]
        શેલ('cp '+ફાઇલ_પ્રવેશ_નામ+' /માન્ય_કરો.txt')
        받은수=bytearray();ફાઇલ_સ્થાનાંતર_કનેક્શન.retrbinary('RETR માન્ય_કરો.txt',받은수.extend);assert 받은수==예상파일.encode()
        શેલ('echo preserved > 출력예제.'+('py' if ભાષા=='python' else ભાષા))
        assert 'EXAMPLES READY' in શેલ('example '+ભાષા)
        assert '\npreserved\n' in શેલ('cat 출력예제.'+('py' if ભાષા=='python' else ભાષા))
        assert '한/영 કી_મૂલ્ય, Shift+Space 또는 F9' in શેલ('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in શેલ('echo GUI NETWORK TOGETHER')
        ફાઇલ_સ્થાનાંતર_કનેક્શન.quit();ફાઇલ_સ્થાનાંતર_કનેક્શન=None;assert 'FTP stopped' in શેલ('ftpd stop')
        print('PASS '+ભાષા+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ફાઇલ_સ્થાનાંતર_કનેક્શન:
            try:ફાઇલ_સ્થાનાંતર_કનેક્શન.close()
            except OSError:pass
        if ક્લાયંટ:ક્લાયંટ.close()
        પ્રક્રિયા.terminate()
        try:પ્રક્રિયા.wait(timeout=8)
        except subprocess.TimeoutExpired:પ્રક્રિયા.kill();પ્રક્રિયા.wait()
        પસંદકર્તા.close();પ્રક્રિયા.stdout.close();(પરિમાણ_ડેટા/(ભાષા+'-serial.log')).write_bytes(대화기록)


def ચલાવો_2():
    પરિમાણ_ડેટા=પ્રોજેક્ટ_રૂટ/'build/verification/examples';પરિમાણ_ડેટા.mkdir(parents=True,exist_ok=True)
    માન્યતા_અહેવાલ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((પ્રોજેક્ટ_રૂટ/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for ભાષા in ('java','c','python'):
                test_언어(ભાષા,되돌림서버항목,પરિમાણ_ડેટા);માન્યતા_અહેવાલ['languages'].append(ભાષા)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(શ્રેણી_મૂલ્ય,ડેટા.encode()) for શ્રેણી_મૂલ્ય,ડેટા in 예상결과],되돌림서버항목.수신됨
            માન્યતા_અહેવાલ['host_network_payloads']=[{'protocol':શ્રેણી_મૂલ્ય,'text':ડેટા.decode()} for શ્રેણી_મૂલ્ય,ડેટા in 되돌림서버항목.수신됨]
        માન્યતા_અહેવાલ.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(પરિમાણ_ડેટા/'report.json').write_text(json.dumps(માન્યતા_અહેવાલ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ચલાવો_2()
