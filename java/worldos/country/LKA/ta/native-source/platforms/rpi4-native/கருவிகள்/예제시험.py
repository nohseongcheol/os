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
from டெஸ்க்டாப்_காட்சி import 정확한값
from 예제되돌림서버 import 되돌림서버
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம்


def test_언어(மொழி,되돌림서버항목,அளவிடக்கூடியது_தரவு):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));கோப்பு_இடமாற்று_முனைய_எண்=임시자원.getsockname()[1]
    செயல்பாடு=subprocess.Popen(['python3',str(திட்டப்பணி_மூலம்/'கருவிகள்/இயக்கு_கட்டளை.py'),'--desktop','--network','--port','0','--ftp-port',str(கோப்பு_இடமாற்று_முனைய_எண்)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    தேர்வி=selectors.DefaultSelector();தேர்வி.register(செயல்பாடு.stdout,selectors.EVENT_READ)
    대화기록=bytearray();பயனகம்=None;கோப்பு_இடமாற்று_இணைப்பு=None
    def 수신하기(확인표시,செயல்படுத்துக=0):
        முடி_ஆஃப்செட்=time.monotonic()+60
        while 확인표시 not in 대화기록[செயல்படுத்துக:]:
            if time.monotonic()>முடி_ஆஃப்செட் or செயல்பாடு.poll() is not None:raise AssertionError(대화기록[செயல்படுத்துக:].decode('utf-8','replace'))
            for 누름값,_ in தேர்வி.select(.1):
                தரவு=누름값.fileobj.read(65536)
                if தரவு:대화기록.extend(தரவு)
        return 대화기록[செயல்படுத்துக:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(சின்னம்_மதிப்பு,누르는중=True):பயனகம்.sendall(struct.pack('>BBHI',4,int(누르는중),0,சின்னம்_மதிப்பு))
    def தொடங்கு_ஆஃப்செட்(உள்ளீட்டு_வரி):
        செயல்படுத்துக=len(대화기록)
        for எழுத்துக்குறி_குறியீடு in உள்ளீட்டு_வரி+'\n':
            சின்னம்_மதிப்பு=0xff0d if எழுத்துக்குறி_குறியீடு=='\n' else ord(எழுத்துக்குறி_குறியீடு) if ord(எழுத்துக்குறி_குறியீடு)<256 else 0x1000000|ord(எழுத்துக்குறி_குறியீடு)
            누름값(சின்னம்_மதிப்பு);누름값(சின்னம்_மதிப்பு,False)
        return செயல்படுத்துக
    def கூடு(உள்ளீட்டு_வரி):return 수신하기(b'jkoros-native> ',தொடங்கு_ஆஃப்செட்(உள்ளீட்டு_வரி))
    def இயக்கு_கட்டளை(உள்ளீட்டு_வரி,예상결과):
        உரை=கூடு(உள்ளீட்டு_வரி);assert 예상결과 in உரை and 'exit 0' in உரை,(உள்ளீட்டு_வரி,உரை)
        return உரை
    def 화소들():
        பயனகம்.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            வகை_மதிப்பு_4b6d6445=정확한값(பயனகம்,1)[0]
            if வகை_மதிப்பு_4b6d6445==2:continue
            if வகை_மதிப்பு_4b6d6445==3:
                개수=struct.unpack('>I',정확한값(பயனகம்,7)[3:])[0];정확한값(பயனகம்,개수);continue
            assert வகை_மதிப்பு_4b6d6445==0,வகை_மதிப்பு_4b6d6445
            항목수=struct.unpack('>H',정확한값(பயனகம்,3)[1:])[0]
            for _ in range(항목수):
                x_ஒத்ததரமுள்ளது,Y_பொத்தான்_அச்சுத்_தொகுப்பு,너비값,높이값,எழுத்துக்குறி_குழு=struct.unpack('>HHHHi',정확한값(பயனகம்,12));assert எழுத்துக்குறி_குழு==0,எழுத்துக்குறி_குழு
                தரவு=정확한값(பயனகம்,너비값*높이값*4)
                for வரிசை_நிலை in range(높이값):
                    for நெடுவரிசை_நிலை in range(너비값):
                        원본자료=(வரிசை_நிலை*너비값+நெடுவரிசை_நிலை)*4;இலக்கு=((Y_பொத்தான்_அச்சுத்_தொகுப்பு+வரிசை_நிலை)*640+x_ஒத்ததரமுள்ளது+நெடுவரிசை_நிலை)*3
                        빛삼원색[இலக்கு:இலக்கு+3]=bytes((தரவு[원본자료+2],தரவு[원본자료+1],தரவு[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        முனைய_எண்=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        பயனகம்=socket.create_connection(('127.0.0.1',முனைய_எண்),timeout=10)
        assert 정확한값(பயனகம்,12)==b'RFB 003.008\n';பயனகம்.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(பயனகம்,정확한값(பயனகம்,1)[0]);பயனகம்.sendall(b'\x01');assert 정확한값(பயனகம்,4)==b'\0'*4
        பயனகம்.sendall(b'\x01');초기값=정확한값(பயனகம்,24);정확한값(பயனகம்,struct.unpack('>I',초기값[20:])[0])
        பயனகம்.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        பயனகம்.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in கூடு('ftpd start')
        கோப்பு_இடமாற்று_இணைப்பு=ftplib.FTP();கோப்பு_இடமாற்று_இணைப்பு.encoding='utf-8';கோப்பு_இடமாற்று_இணைப்பு.connect('127.0.0.1',கோப்பு_இடமாற்று_முனைய_எண்,timeout=20);கோப்பு_இடமாற்று_இணைப்பு.login()
        பேலோட்_தரவு=('GUI와 FTP 동시 사용 '+மொழி+' 😀\n').encode()
        கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR 함께.txt',io.BytesIO(பேலோட்_தரவு))
        assert பேலோட்_தரவு.decode().strip() in கூடு('cat /함께.txt')
        받은수=bytearray();கோப்பு_இடமாற்று_இணைப்பு.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==பேலோட்_தரவு;கோப்பு_இடமாற்று_இணைப்பு.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        அனுப்பு_பட்டியல்=கூடு('ls /example')
        assert all(பெயர் in அனுப்பு_பட்டியல் for பெயர் in ('java/','c/','python/','README.md')),அனுப்பு_பட்டியல்
        if மொழி=='java':
            மூட்டை_தொற்றம்=json.loads((திட்டப்பணி_மூலம்/'build/examples/manifest.json').read_text())
            for பாதை_2,நுழைவுப்_புள்ளி in மூட்டை_தொற்றம்.items():
                கூடு('cp '+பாதை_2+' /example-check.bin')
                உள்ளடக்கம்_மதிப்பு=bytearray();கோப்பு_இடமாற்று_இணைப்பு.retrbinary('RETR example-check.bin',உள்ளடக்கம்_மதிப்பு.extend)
                assert len(உள்ளடக்கம்_மதிப்பு)==நுழைவுப்_புள்ளி['bytes'] and hashlib.sha256(உள்ளடக்கம்_மதிப்பு).hexdigest()==நுழைவுப்_புள்ளி['sha256'],பாதை_2
            கோப்பு_இடமாற்று_இணைப்பு.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            பைனரி=bytes(range(256))*64
            கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR boundary.bin',io.BytesIO(பைனரி))
            உள்ளடக்கம்_மதிப்பு=bytearray();கோப்பு_இடமாற்று_இணைப்பு.retrbinary('RETR boundary.bin',உள்ளடக்கம்_மதிப்பு.extend)
            assert உள்ளடக்கம்_மதிப்பு==பைனரி and 'boundary.bin' in கோப்பு_இடமாற்று_இணைப்பு.nlst()
            கூடு('cp /boundary.bin /boundary-copy.bin')
            உள்ளடக்கம்_மதிப்பு=bytearray();கோப்பு_இடமாற்று_இணைப்பு.retrbinary('RETR boundary-copy.bin',உள்ளடக்கம்_மதிப்பு.extend)
            assert உள்ளடக்கம்_மதிப்பு==பைனரி
            கோப்பு_இடமாற்று_இணைப்பு.delete('boundary.bin');கோப்பு_இடமாற்று_இணைப்பு.delete('boundary-copy.bin')
        assert '출력예제' in கூடு('ls /example/'+மொழி)
        கூடு('cd /example/'+மொழி)
        பெயர்_அட்டவணை={'java':'JAVA','c':'C','python':'PYTHON'}[மொழி]
        예상파일=பெயர்_அட்டவணை+' கோப்பின்_பெயர்: 한글 தரவு 😀\n'
        if மொழி=='java':
            இயக்கு_கட்டளை('javac 출력예제.java','Compiled:');இயக்கு_கட்டளை('java 출력예제','JAVA வெளியீட்டு_இடம்: 안녕하세요 😀')
            இயக்கு_கட்டளை('javac 파일예제.java','Compiled:');இயக்கு_கட்டளை('java 파일예제',예상파일)
            இயக்கு_கட்டளை('java 네트워크예제 {} {}'.format(되돌림서버항목.டிரான்ஸ்மிஷன்_கண்ட்ரோல்_புரோட்டோகால்_முணையம்,되돌림서버항목.전문접속번호),'JAVA 네트워크 சரிபார்: TCP UDP 한글')
            கிராஃபிக்ஸ்_கட்டளை='java 그래픽예제'
        elif மொழி=='c':
            for பெயர்,전달값,예상결과 in [('வெளியீட்டு_இடம்','', 'C வெளியீட்டு_இடம்: 안녕하세요 😀'),('கோப்பின்_பெயர்','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 சரிபார்: UDP 한글')]:
                இயக்கு_கட்டளை('cc '+பெயர்+'예제.c -o இயக்கு_கட்டளை','Compiled native ARM64 ELF:')
                இயக்கு_கட்டளை('./இயக்கு_கட்டளை'+전달값,예상결과)
            இயக்கு_கட்டளை('cc 그래픽예제.c -o இயக்கு_கட்டளை','Compiled native ARM64 ELF:');கிராஃபிக்ஸ்_கட்டளை='./இயக்கு_கட்டளை'
        else:
            for பெயர்,전달값,예상결과 in [('வெளியீட்டு_இடம்','','PYTHON வெளியீட்டு_இடம்: 안녕하세요 😀'),('கோப்பின்_பெயர்','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 சரிபார்: UDP 한글')]:
                இயக்கு_கட்டளை('python '+பெயர்+'예제.py'+전달값,예상결과)
            கிராஃபிக்ஸ்_கட்டளை='python 그래픽예제.py'
        தொடங்கு_வரைதல்=தொடங்கு_ஆஃப்செட்(கிராஃபிக்ஸ்_கட்டளை)
        உரை=수신하기('그림을 확인한 பின்_மதிப்பு Enter를 누르세요.\r\n'.encode(),தொடங்கு_வரைதல்)
        assert பெயர்_அட்டவணை+' 그래픽: 빨강 초록 파랑' in உரை and 'exit 0' not in உரை,உரை
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();கோப்பு_இடமாற்று_இணைப்பு.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';கோப்பு_இடமாற்று_இணைப்பு.delete('도중.txt')
        빛삼원색=화소들()
        for Y_பொத்தான்_அச்சுத்_தொகுப்பு,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ஆஃப்செட்_மதிப்பு=(Y_பொத்தான்_அச்சுத்_தொகுப்பு*640+610)*3;assert tuple(빛삼원색[ஆஃப்செட்_மதிப்பு:ஆஃப்செட்_மதிப்பு+3])==색상,(மொழி,Y_பொத்தான்_அச்சுத்_தொகுப்பு,tuple(빛삼원색[ஆஃப்செட்_மதிப்பு:ஆஃப்செட்_மதிப்பு+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(அளவிடக்கூடியது_தரவு/(மொழி+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',தொடங்கு_வரைதல்)
        if மொழி=='java':
            தொடங்கு_சாளரம்=தொடங்கு_ஆஃப்செட்('java 창예제')
            수신하기('GUI 예제 தயார்படுத்த: 창예제'.encode(),தொடங்கு_சாளரம்)
            def கிளிக்_செய்_மதிப்பு(가로,வெர்டிகல்_நிலை):
                for பொத்தான் in (1,0):பயனகம்.sendall(struct.pack('>BBHH',5,பொத்தான்,가로,வெர்டிகல்_நிலை))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            கிளிக்_செய்_மதிப்பு(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for எழுத்துக்குறி_மதிப்பு in '한글':누름값(0x1000000|ord(எழுத்துக்குறி_மதிப்பு));누름값(0x1000000|ord(எழுத்துக்குறி_மதிப்பு),False)
            for 횟수 in (1,2):
                செயல்படுத்துக=len(대화기록);கிளிக்_செய்_மதிப்பு(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),செயல்படுத்துக)
            time.sleep(.3)
            சாளரம்_வரைதல்=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=சாளரம்_வரைதல்.crop((110,272,530,300)).tobytes()
            சாளரம்_வரைதல்.save(str(அளவிடக்கூடியது_தரவு/'java-swing.png'))
            செயல்படுத்துக=len(대화기록);கிளிக்_செய்_மதிப்பு(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',செயல்படுத்துக)
        # Download the guest-created bytes through FTP in the same GUI VM.
        கோப்பு_உள்ளீடு_பெயர்={'java':'java.txt','c':'c.txt','python':'python.txt'}[மொழி]
        கூடு('cp '+கோப்பு_உள்ளீடு_பெயர்+' /சரிபார்_5fb2b747.txt')
        받은수=bytearray();கோப்பு_இடமாற்று_இணைப்பு.retrbinary('RETR சரிபார்_5fb2b747.txt',받은수.extend);assert 받은수==예상파일.encode()
        கூடு('echo preserved > 출력예제.'+('py' if மொழி=='python' else மொழி))
        assert 'EXAMPLES READY' in கூடு('example '+மொழி)
        assert '\npreserved\n' in கூடு('cat 출력예제.'+('py' if மொழி=='python' else மொழி))
        assert '한/영 சாவி_மதிப்பு, Shift+Space 또는 F9' in கூடு('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in கூடு('echo GUI NETWORK TOGETHER')
        கோப்பு_இடமாற்று_இணைப்பு.quit();கோப்பு_இடமாற்று_இணைப்பு=None;assert 'FTP stopped' in கூடு('ftpd stop')
        print('PASS '+மொழி+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if கோப்பு_இடமாற்று_இணைப்பு:
            try:கோப்பு_இடமாற்று_இணைப்பு.close()
            except OSError:pass
        if பயனகம்:பயனகம்.close()
        செயல்பாடு.terminate()
        try:செயல்பாடு.wait(timeout=8)
        except subprocess.TimeoutExpired:செயல்பாடு.kill();செயல்பாடு.wait()
        தேர்வி.close();செயல்பாடு.stdout.close();(அளவிடக்கூடியது_தரவு/(மொழி+'-serial.log')).write_bytes(대화기록)


def செயல்படுத்துக():
    அளவிடக்கூடியது_தரவு=திட்டப்பணி_மூலம்/'build/verification/examples';அளவிடக்கூடியது_தரவு.mkdir(parents=True,exist_ok=True)
    செல்லுபடியாக்கம்_அறிக்கை={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((திட்டப்பணி_மூலம்/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for மொழி in ('java','c','python'):
                test_언어(மொழி,되돌림서버항목,அளவிடக்கூடியது_தரவு);செல்லுபடியாக்கம்_அறிக்கை['languages'].append(மொழி)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(வகை_மதிப்பு_4b6d6445,தரவு.encode()) for வகை_மதிப்பு_4b6d6445,தரவு in 예상결과],되돌림서버항목.수신됨
            செல்லுபடியாக்கம்_அறிக்கை['host_network_payloads']=[{'protocol':வகை_மதிப்பு_4b6d6445,'text':தரவு.decode()} for வகை_மதிப்பு_4b6d6445,தரவு in 되돌림서버항목.수신됨]
        செல்லுபடியாக்கம்_அறிக்கை.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(அளவிடக்கூடியது_தரவு/'report.json').write_text(json.dumps(செல்லுபடியாக்கம்_அறிக்கை,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':செயல்படுத்துக()
