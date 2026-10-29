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
from biro_igaragaza import 정확한값
from 예제되돌림서버 import 되돌림서버
from gukora_ibwiriza import 기준


def test_언어(Ururimi,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Inzira_a7054519=subprocess.Popen(['python3',str(기준/'Ibikoresho/gukora_ibwiriza.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    muhitamo=selectors.DefaultSelector();muhitamo.register(Inzira_a7054519.stdout,selectors.EVENT_READ)
    대화기록=bytearray();umukiriya=None;dosiye_iyimura_kwihuza=None
    def 수신하기(확인표시,ihuriro=0):
        kurangiza_Ofuseti=time.monotonic()+60
        while 확인표시 not in 대화기록[ihuriro:]:
            if time.monotonic()>kurangiza_Ofuseti or Inzira_a7054519.poll() is not None:raise AssertionError(대화기록[ihuriro:].decode('utf-8','replace'))
            for 누름값,_ in muhitamo.select(.1):
                amakurushingiro=누름값.fileobj.read(65536)
                if amakurushingiro:대화기록.extend(amakurushingiro)
        return 대화기록[ihuriro:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(ikimenyetso_agaciro,누르는중=True):umukiriya.sendall(struct.pack('>BBHI',4,int(누르는중),0,ikimenyetso_agaciro))
    def Itangira_Ofuseti(umurongo):
        ihuriro=len(대화기록)
        for 문자값 in umurongo+'\n':
            ikimenyetso_agaciro=0xff0d if 문자값=='\n' else ord(문자값) if ord(문자값)<256 else 0x1000000|ord(문자값)
            누름값(ikimenyetso_agaciro);누름값(ikimenyetso_agaciro,False)
        return ihuriro
    def insomamabwiriza(umurongo):return 수신하기(b'jkoros-native> ',Itangira_Ofuseti(umurongo))
    def gukora_ibwiriza(umurongo,예상결과):
        Umwandiko=insomamabwiriza(umurongo);assert 예상결과 in Umwandiko and 'exit 0' in Umwandiko,(umurongo,Umwandiko)
        return Umwandiko
    def 화소들():
        umukiriya.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            icyiciro_agaciro=정확한값(umukiriya,1)[0]
            if icyiciro_agaciro==2:continue
            if icyiciro_agaciro==3:
                개수=struct.unpack('>I',정확한값(umukiriya,7)[3:])[0];정확한값(umukiriya,개수);continue
            assert icyiciro_agaciro==0,icyiciro_agaciro
            항목수=struct.unpack('>H',정확한값(umukiriya,3)[1:])[0]
            for _ in range(항목수):
                Ihuza_rya_x,세로좌표,너비값,높이값,itsinda_ry_inyuguti=struct.unpack('>HHHHi',정확한값(umukiriya,12));assert itsinda_ry_inyuguti==0,itsinda_ry_inyuguti
                amakurushingiro=정확한값(umukiriya,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;gusimbuza_igishya=((세로좌표+행위치)*640+Ihuza_rya_x+열위치)*3
                        빛삼원색[gusimbuza_igishya:gusimbuza_igishya+3]=bytes((amakurushingiro[원본자료+2],amakurushingiro[원본자료+1],amakurushingiro[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        umukiriya=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(umukiriya,12)==b'RFB 003.008\n';umukiriya.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(umukiriya,정확한값(umukiriya,1)[0]);umukiriya.sendall(b'\x01');assert 정확한값(umukiriya,4)==b'\0'*4
        umukiriya.sendall(b'\x01');초기값=정확한값(umukiriya,24);정확한값(umukiriya,struct.unpack('>I',초기값[20:])[0])
        umukiriya.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        umukiriya.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in insomamabwiriza('ftpd start')
        dosiye_iyimura_kwihuza=ftplib.FTP();dosiye_iyimura_kwihuza.encoding='utf-8';dosiye_iyimura_kwihuza.connect('127.0.0.1',파일전송접속번호,timeout=20);dosiye_iyimura_kwihuza.login()
        ibitwarwa_amakurushingiro=('GUI와 FTP 동시 사용 '+Ururimi+' 😀\n').encode()
        dosiye_iyimura_kwihuza.storbinary('STOR 함께.txt',io.BytesIO(ibitwarwa_amakurushingiro))
        assert ibitwarwa_amakurushingiro.decode().strip() in insomamabwiriza('cat /함께.txt')
        받은수=bytearray();dosiye_iyimura_kwihuza.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==ibitwarwa_amakurushingiro;dosiye_iyimura_kwihuza.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        kohereza_Urutonde=insomamabwiriza('ls /example')
        assert all(Izina in kohereza_Urutonde for Izina in ('java/','c/','python/','README.md')),kohereza_Urutonde
        if Ururimi=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for Inzira,icyinjizwa_inota in 꾸러미명세.items():
                insomamabwiriza('cp '+Inzira+' /example-check.bin')
                Ibirimo_agaciro=bytearray();dosiye_iyimura_kwihuza.retrbinary('RETR example-check.bin',Ibirimo_agaciro.extend)
                assert len(Ibirimo_agaciro)==icyinjizwa_inota['bytes'] and hashlib.sha256(Ibirimo_agaciro).hexdigest()==icyinjizwa_inota['sha256'],Inzira
            dosiye_iyimura_kwihuza.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            nyabibiri=bytes(range(256))*64
            dosiye_iyimura_kwihuza.storbinary('STOR boundary.bin',io.BytesIO(nyabibiri))
            Ibirimo_agaciro=bytearray();dosiye_iyimura_kwihuza.retrbinary('RETR boundary.bin',Ibirimo_agaciro.extend)
            assert Ibirimo_agaciro==nyabibiri and 'boundary.bin' in dosiye_iyimura_kwihuza.nlst()
            insomamabwiriza('cp /boundary.bin /boundary-copy.bin')
            Ibirimo_agaciro=bytearray();dosiye_iyimura_kwihuza.retrbinary('RETR boundary-copy.bin',Ibirimo_agaciro.extend)
            assert Ibirimo_agaciro==nyabibiri
            dosiye_iyimura_kwihuza.delete('boundary.bin');dosiye_iyimura_kwihuza.delete('boundary-copy.bin')
        assert '출력예제' in insomamabwiriza('ls /example/'+Ururimi)
        insomamabwiriza('cd /example/'+Ururimi)
        izina_imbonerahamwe={'java':'JAVA','c':'C','python':'PYTHON'}[Ururimi]
        예상파일=izina_imbonerahamwe+' Idosiye: 한글 amakurushingiro 😀\n'
        if Ururimi=='java':
            gukora_ibwiriza('javac 출력예제.java','Compiled:');gukora_ibwiriza('java 출력예제','JAVA 출력: 안녕하세요 😀')
            gukora_ibwiriza('javac 파일예제.java','Compiled:');gukora_ibwiriza('java 파일예제',예상파일)
            gukora_ibwiriza('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_poti,되돌림서버항목.전문접속번호),'JAVA 네트워크 gusuzuma: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif Ururimi=='c':
            for Izina,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Idosiye','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 gusuzuma: UDP 한글')]:
                gukora_ibwiriza('cc '+Izina+'예제.c -o gukora_ibwiriza','Compiled native ARM64 ELF:')
                gukora_ibwiriza('./gukora_ibwiriza'+전달값,예상결과)
            gukora_ibwiriza('cc 그래픽예제.c -o gukora_ibwiriza','Compiled native ARM64 ELF:');그림명령='./gukora_ibwiriza'
        else:
            for Izina,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Idosiye','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 gusuzuma: UDP 한글')]:
                gukora_ibwiriza('python '+Izina+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        Itangira_igishushanyo=Itangira_Ofuseti(그림명령)
        Umwandiko=수신하기('그림을 확인한 Ikibanza_agaciro Enter를 누르세요.\r\n'.encode(),Itangira_igishushanyo)
        assert izina_imbonerahamwe+' 그래픽: 빨강 초록 파랑' in Umwandiko and 'exit 0' not in Umwandiko,Umwandiko
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        dosiye_iyimura_kwihuza.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();dosiye_iyimura_kwihuza.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';dosiye_iyimura_kwihuza.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Ofuseti_agaciro=(세로좌표*640+610)*3;assert tuple(빛삼원색[Ofuseti_agaciro:Ofuseti_agaciro+3])==색상,(Ururimi,세로좌표,tuple(빛삼원색[Ofuseti_agaciro:Ofuseti_agaciro+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(Ururimi+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Itangira_igishushanyo)
        if Ururimi=='java':
            Itangira_idirishya=Itangira_Ofuseti('java 창예제')
            수신하기('GUI 예제 Gutegura: 창예제'.encode(),Itangira_idirishya)
            def gukanda_agaciro(가로,세로):
                for buto in (1,0):umukiriya.sendall(struct.pack('>BBHH',5,buto,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            gukanda_agaciro(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for inyuguti_agaciro in '한글':누름값(0x1000000|ord(inyuguti_agaciro));누름값(0x1000000|ord(inyuguti_agaciro),False)
            for 횟수 in (1,2):
                ihuriro=len(대화기록);gukanda_agaciro(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),ihuriro)
            time.sleep(.3)
            idirishya_igishushanyo=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=idirishya_igishushanyo.crop((110,272,530,300)).tobytes()
            idirishya_igishushanyo.save(str(결과자료/'java-swing.png'))
            ihuriro=len(대화기록);gukanda_agaciro(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',ihuriro)
        # Download the guest-created bytes through FTP in the same GUI VM.
        dosiye_icyinjizwa_izina={'java':'java.txt','c':'c.txt','python':'python.txt'}[Ururimi]
        insomamabwiriza('cp '+dosiye_icyinjizwa_izina+' /kwemeza.txt')
        받은수=bytearray();dosiye_iyimura_kwihuza.retrbinary('RETR kwemeza.txt',받은수.extend);assert 받은수==예상파일.encode()
        insomamabwiriza('echo preserved > 출력예제.'+('py' if Ururimi=='python' else Ururimi))
        assert 'EXAMPLES READY' in insomamabwiriza('example '+Ururimi)
        assert '\npreserved\n' in insomamabwiriza('cat 출력예제.'+('py' if Ururimi=='python' else Ururimi))
        assert '한/영 buto_agaciro, Shift+Space 또는 F9' in insomamabwiriza('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in insomamabwiriza('echo GUI NETWORK TOGETHER')
        dosiye_iyimura_kwihuza.quit();dosiye_iyimura_kwihuza=None;assert 'FTP stopped' in insomamabwiriza('ftpd stop')
        print('PASS '+Ururimi+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if dosiye_iyimura_kwihuza:
            try:dosiye_iyimura_kwihuza.close()
            except OSError:pass
        if umukiriya:umukiriya.close()
        Inzira_a7054519.terminate()
        try:Inzira_a7054519.wait(timeout=8)
        except subprocess.TimeoutExpired:Inzira_a7054519.kill();Inzira_a7054519.wait()
        muhitamo.close();Inzira_a7054519.stdout.close();(결과자료/(Ururimi+'-serial.log')).write_bytes(대화기록)


def ihuriro():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    iyemeza_raporo={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Ururimi in ('java','c','python'):
                test_언어(Ururimi,되돌림서버항목,결과자료);iyemeza_raporo['languages'].append(Ururimi)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(icyiciro_agaciro,amakurushingiro.encode()) for icyiciro_agaciro,amakurushingiro in 예상결과],되돌림서버항목.수신됨
            iyemeza_raporo['host_network_payloads']=[{'protocol':icyiciro_agaciro,'text':amakurushingiro.decode()} for icyiciro_agaciro,amakurushingiro in 되돌림서버항목.수신됨]
        iyemeza_raporo.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(iyemeza_raporo,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ihuriro()
