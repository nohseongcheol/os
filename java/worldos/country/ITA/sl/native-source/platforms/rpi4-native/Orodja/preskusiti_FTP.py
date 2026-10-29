#!/usr/bin/env python3
"""Real host TCP client -> SLIP -> bare-metal lwIP -> FTP -> Java VFS."""
import ftplib
import hashlib
import io
import json
import selectors
import socket
import subprocess
import time
import zipfile
from most_3de4fe3a import most_3de4fe3a
from Izvedi_ukaz import pobuda_koren, Ukaz
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Zaženi():
    KR_podatki = pobuda_koren / 'build/verification/ftp'; KR_podatki.mkdir(parents=True, exist_ok=True)
    preverjanje_veljavnosti_prijavi = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((pobuda_koren / 'build/kernel8.img').read_bytes()).hexdigest()}
    prepis = bytearray()
    자바원문 = KR_podatki / 'preskusiti_sveženj.java'
    자바원문.write_text('public class preskusiti_sveženj { public static void main(String[] Argumenti) throws Exception { slovenščina.lastno.Izpis.pisati_linija("JAR Izvedi_ukaz: " + Argumenti[0]); slovenščina.lastno.Datoteka.Pisanje("jar.txt", "lastno jedro_VALUE Datoteka"); slovenščina.lastno.Izpis.pisati_linija(slovenščina.lastno.Datoteka.Branje("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(pobuda_koren/'build/java-library/classes'), '-d', str(KR_podatki), str(자바원문)])
    Arhiv = io.BytesIO()
    with zipfile.ZipFile(Arhiv, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: preskusiti_sveženj\r\n\r\n')
        자바꾸러미.write(str(KR_podatki/'preskusiti_sveženj.class'), 'preskusiti_sveženj.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); številka_vrat = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); strežnik_tok_vrata = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); strežnik_datagram_vrata = 임시자원.getsockname()[1]
    with most_3de4fe3a(številka_vrat, ['tcp:{}:9300'.format(strežnik_tok_vrata), 'udp:{}:9301'.format(strežnik_datagram_vrata)], snemati=True) as most:
        Opravilo = subprocess.Popen(Ukaz() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + most.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        izbirnik = selectors.DefaultSelector(); izbirnik.register(Opravilo.stdout, selectors.EVENT_READ)
        def sprejeti_sprejemati_prejeti_prejemati_e_pošta(oznaka=b'jkoros-native> ', 시간제한=60):
            podatki = bytearray(); končati_klic_odmik = time.monotonic() + 시간제한
            while oznaka not in podatki:
                if time.monotonic() > končati_klic_odmik or Opravilo.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + podatki.decode('utf-8', 'replace'))
                for 누름값, _ in izbirnik.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: podatki.extend(조각); prepis.extend(조각)
                if b'PANIC:' in podatki or b'FAIL ' in podatki: raise AssertionError(podatki)
            return podatki.decode('utf-8', 'replace').replace('\r\n', '\n')
        def lupina(Črtni):
            Opravilo.stdin.write(Črtni.encode() + b'\n'); Opravilo.stdin.flush(); return sprejeti_sprejemati_prejeti_prejemati_e_pošta()
        try:
            sprejeti_sprejemati_prejeti_prejemati_e_pošta(); assert 'FTP listening' in lupina('ftpd start')
            prenos_datotek_povezava = ftplib.FTP(); prenos_datotek_povezava.encoding = 'utf-8'; prenos_datotek_povezava.connect('127.0.0.1', številka_vrat, timeout=20); prenos_datotek_povezava.login()
            koristna_vsebina_podatki = bytes(range(256)) * 32
            prenos_datotek_povezava.storbinary('STOR binary.dat', io.BytesIO(koristna_vsebina_podatki))
            REZULTAT = bytearray(); prenos_datotek_povezava.retrbinary('RETR binary.dat', REZULTAT.extend)
            assert REZULTAT == koristna_vsebina_podatki; assert prenos_datotek_povezava.size('binary.dat') == len(koristna_vsebina_podatki)
            preverjanje_veljavnosti_prijavi['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            prenos_datotek_povezava.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in lupina('cat 한글.txt')
            assert '한글.txt' in prenos_datotek_povezava.nlst()
            assert dict(prenos_datotek_povezava.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            preverjanje_veljavnosti_prijavi['checks'].append('UTF-8 filename and content visible in guest shell')
            try: prenos_datotek_povezava.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            REZULTAT = bytearray(); prenos_datotek_povezava.retrbinary('RETR binary.dat', REZULTAT.extend); assert REZULTAT == koristna_vsebina_podatki
            preverjanje_veljavnosti_prijavi['checks'].append('oversized replacement rejected; previous file preserved')
            with prenos_datotek_povezava.transfercmd('STOR pending.txt') as Upload_Datoteke:
                # A control command must not change the active upload's destination.
                assert prenos_datotek_povezava.size('binary.dat') == len(koristna_vsebina_podatki)
                Upload_Datoteke.sendall(b'UPLOAD TARGET PRESERVED')
            assert prenos_datotek_povezava.voidresp().startswith('226')
            REZULTAT = bytearray(); prenos_datotek_povezava.retrbinary('RETR pending.txt', REZULTAT.extend)
            assert REZULTAT == b'UPLOAD TARGET PRESERVED'
            REZULTAT = bytearray(); prenos_datotek_povezava.retrbinary('RETR binary.dat', REZULTAT.extend)
            assert REZULTAT == koristna_vsebina_podatki
            prenos_datotek_povezava.delete('pending.txt')
            preverjanje_veljavnosti_prijavi['checks'].append('interleaved SIZE cannot change the active STOR destination')
            prenos_datotek_povezava.storbinary('STOR 인사.jar', io.BytesIO(Arhiv.getvalue()))
            Besedilo = lupina('java -jar 인사.jar 누리')
            assert 'JAR Izvedi_ukaz: 누리' in Besedilo and 'lastno jedro_VALUE Datoteka' in Besedilo and 'exit 0' in Besedilo, Besedilo
            Besedilo = lupina('./인사.jar 세상')
            assert 'JAR Izvedi_ukaz: 세상' in Besedilo and 'exit 0' in Besedilo, Besedilo
            preverjanje_veljavnosti_prijavi['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct podatki { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct podatki VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = odprto_Datoteka("cc.txt", branje_pisanje | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; pisati_Datoteka_podatki(문서, 인사, sizeof(인사)-1); Zapri_Datoteka(문서); pisati_Datoteka_podatki(1, 인사, sizeof(인사)-1); return 0; }\n'
            prenos_datotek_povezava.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Besedilo = lupina('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Besedilo and 'exit 0' in Besedilo, Besedilo
            Besedilo = lupina('run 한글.elf'); assert 'CC NATIVE PASS' in Besedilo and 'exit 0' in Besedilo, Besedilo
            assert 'CC NATIVE PASS' in lupina('cat cc.txt')
            실행파일 = bytearray(); prenos_datotek_povezava.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            prenos_datotek_povezava.storbinary('STOR kopirati_VALUE.elf', io.BytesIO(실행파일)); Besedilo = lupina('run kopirati_VALUE.elf'); assert 'CC NATIVE PASS' in Besedilo and 'exit 0' in Besedilo, Besedilo
            prenos_datotek_povezava.storbinary('STOR Izvedi_ukaz', io.BytesIO(실행파일)); Besedilo=lupina('./Izvedi_ukaz');assert 'CC NATIVE PASS' in Besedilo and 'exit 0' in Besedilo,Besedilo
            prenos_datotek_povezava.storbinary('STOR Ime.txt', io.BytesIO(실행파일)); Besedilo=lupina('./Ime.txt');assert 'CC NATIVE PASS' in Besedilo and 'exit 0' in Besedilo,Besedilo
            lupina('rm Izvedi_ukaz Ime.txt')
            preverjanje_veljavnosti_prijavi['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            lupina('rm binary.dat 한글.txt 한글.c 한글.elf kopirati_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KR_podatki/'linux-reference')
            prenos_datotek_povezava.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Besedilo=lupina('./리눅스인사');assert 'exit -8' in Besedilo,Besedilo
            Besedilo=lupina('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Besedilo,Besedilo
            assert 'LINUX ELF FILE IO' in lupina('cat linux.txt')
            prenos_datotek_povezava.delete('리눅스인사');prenos_datotek_povezava.delete('linux.txt')
            prenos_datotek_povezava.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in lupina('./FALSE_VALUE.elf');prenos_datotek_povezava.delete('FALSE_VALUE.elf')
            preverjanje_veljavnosti_prijavi['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as odmev_strežnik_vnos:
                NET_vir = KR_podatki/'바깥통신.java'
                NET_vir.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Poveži = slovenščina.lastno.연결통신.Poveži("10.0.2.2", Integer.parseInt(args[0]));
 Poveži.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] VIR = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<VIR.length;i++) if (Poveži.getInputStream().read() != (VIR[i]&255)) throw new RuntimeException("TCP mismatch");
 Poveži.close();
 DatagramSocket končna_točka = slovenščina.lastno.통신.Odpri(0); slovenščina.lastno.통신.TIMEOUT(končna_točka, 500);
 slovenščina.lastno.통신.poslati(končna_točka, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!slovenščina.lastno.통신.sprejeti_sprejemati_prejeti_prejemati(končna_točka).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 končna_točka.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(pobuda_koren/'build/java-library/classes'),'-d',str(KR_podatki),str(NET_vir)])
                prenos_datotek_povezava.storbinary('STOR 바깥통신.class', io.BytesIO((KR_podatki/'바깥통신.class').read_bytes()))
                Besedilo = lupina('java 바깥통신 {} {}'.format(odmev_strežnik_vnos.TCP_vrata, odmev_strežnik_vnos.UDP_vrata))
                assert 'EXTERNAL TCP UDP PASS' in Besedilo and '10.0.2.2' in Besedilo and 'exit 0' in Besedilo, Besedilo
                assert odmev_strežnik_vnos.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, odmev_strežnik_vnos.수신됨
                assert not odmev_strežnik_vnos.오류들, odmev_strežnik_vnos.오류들
            preverjanje_veljavnosti_prijavi['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            prenos_datotek_povezava.delete('바깥통신.class')
            strežnik_vir=KR_podatki/'strežnik_preskusiti.java'
            strežnik_vir.write_text('''import java.net.*; public class strežnik_preskusiti {
 public static void main(String[] args) throws Exception {
  ServerSocket strežnik_VALUE = new ServerSocket(9300); DatagramSocket končna_točka = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket gost_VALUE = strežnik_VALUE.accept();
  gost_VALUE.getOutputStream().write(gost_VALUE.getInputStream().read()+1); gost_VALUE.close(); strežnik_VALUE.close();
  byte[] vsebina_VALUE = new byte[8]; DatagramPacket datagram = new DatagramPacket(vsebina_VALUE, vsebina_VALUE.length); končna_točka.receive(datagram);
  končna_točka.send(datagram); končna_točka.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_podatki),str(strežnik_vir)])
            prenos_datotek_povezava.storbinary('STOR strežnik_preskusiti.class',io.BytesIO((KR_podatki/'strežnik_preskusiti.class').read_bytes()))
            Opravilo.stdin.write('java strežnik_preskusiti\n'.encode());Opravilo.stdin.flush();sprejeti_sprejemati_prejeti_prejemati_e_pošta(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',strežnik_tok_vrata),timeout=5) as enakovreden_VALUE:
                enakovreden_VALUE.sendall(b'A');assert enakovreden_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as enakovreden_VALUE:
                enakovreden_VALUE.settimeout(5);enakovreden_VALUE.sendto(b'UDP-IN',('127.0.0.1',strežnik_datagram_vrata));assert enakovreden_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Besedilo=sprejeti_sprejemati_prejeti_prejemati_e_pošta();assert 'INBOUND TCP UDP PASS' in Besedilo and 'exit 0' in Besedilo,Besedilo
            preverjanje_veljavnosti_prijavi['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            prenos_datotek_povezava.delete('strežnik_preskusiti.class')
            navodilo_SEQUENCE = 'public class 빛 { public static void main(String[] Argumenti) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } slovenščina.lastno.Izpis.수쓰기(SUM_VALUE); slovenščina.lastno.Datoteka.Pisanje("aot.txt", "한글 AOT Datoteka 😀"); slovenščina.lastno.Izpis.pisati_linija(slovenščina.lastno.Datoteka.Branje("aot.txt")); } }'
            prenos_datotek_povezava.storbinary('STOR 빛.java', io.BytesIO(navodilo_SEQUENCE.encode()))
            Besedilo = lupina('javac 빛.java'); assert 'exit 0' in Besedilo and 'Compiled:' in Besedilo, Besedilo
            Besedilo = lupina('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Besedilo and 'exit 0' in Besedilo, Besedilo
            Besedilo = lupina('run 빛.elf'); assert '\n55\n' in Besedilo and '한글 AOT Datoteka 😀' in Besedilo and 'exit 0' in Besedilo, Besedilo
            자체실행파일 = bytearray(); prenos_datotek_povezava.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Besedilo = lupina('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Besedilo and 'unsupported' in Besedilo, Besedilo
            보존자료 = bytearray(); prenos_datotek_povezava.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); prenos_datotek_povezava.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            prenos_datotek_povezava.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Besedilo = lupina('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Besedilo and 'exit 0' in Besedilo, Besedilo
            Besedilo = lupina('run 빛.elf'); assert '\n55\n' in Besedilo and '한글 AOT Datoteka 😀' in Besedilo and 'exit 0' in Besedilo, Besedilo
            preverjanje_veljavnosti_prijavi['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            preverjanje_veljavnosti_prijavi['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statičen_vir=KR_podatki/'statičen_preskusiti.java'
            statičen_vir.write_text('''public class statičen_preskusiti {
 static int pobuda_koren = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] Argumenti) {
  int[] VALUE = new int[] {pobuda_koren, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(Argumenti[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_podatki),str(statičen_vir)])
            prenos_datotek_povezava.storbinary('STOR statičen_preskusiti.class',io.BytesIO((KR_podatki/'statičen_preskusiti.class').read_bytes()))
            Besedilo=lupina('jaot statičen_preskusiti.class -o statičen_preskusiti.elf');assert 'exit 0' in Besedilo,Besedilo
            Besedilo=lupina('run statičen_preskusiti.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Besedilo,Besedilo
            prenos_datotek_povezava.delete('statičen_preskusiti.class');prenos_datotek_povezava.delete('statičen_preskusiti.elf')
            preverjanje_veljavnosti_prijavi['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arhiv.getvalue());손상자료[14]^=1
            prenos_datotek_povezava.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Besedilo=lupina('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Besedilo,Besedilo
            preverjanje_veljavnosti_prijavi['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            prenos_datotek_povezava.quit(); assert 'FTP stopped' in lupina('ftpd stop')
            assert not most.NAPAKA, most.NAPAKA
            preverjanje_veljavnosti_prijavi.update(passed=True, frames_to_guest=most.커널수신틀수, frames_from_guest=most.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in izbirnik.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: prepis.extend(조각)
            most.Premor_dogodek.set()
            Opravilo.terminate()
            try: Opravilo.wait(timeout=5)
            except subprocess.TimeoutExpired: Opravilo.kill(); Opravilo.wait()
            izbirnik.close(); Opravilo.stdin.close(); Opravilo.stdout.close()
            preverjanje_veljavnosti_prijavi['bridge_error'] = most.NAPAKA
            preverjanje_veljavnosti_prijavi['frames_to_guest'] = most.커널수신틀수; preverjanje_veljavnosti_prijavi['frames_from_guest'] = most.커널발신틀수
            (KR_podatki/'packets.json').write_text(json.dumps(most.dnevnik_sledenja,indent=2)+'\n')
            (KR_podatki / 'serial.log').write_bytes(prepis)
            (KR_podatki / 'report.json').write_text(json.dumps(preverjanje_veljavnosti_prijavi, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Zaženi()
