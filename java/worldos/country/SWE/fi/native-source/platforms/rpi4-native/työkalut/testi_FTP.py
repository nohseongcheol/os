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
from silta_3de4fe3a import silta_3de4fe3a
from Suorita_komento import aloite_juuri, komento
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Suorita_2():
    KR_data = aloite_juuri / 'build/verification/ftp'; KR_data.mkdir(parents=True, exist_ok=True)
    vahvistus_raportti = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((aloite_juuri / 'build/kernel8.img').read_bytes()).hexdigest()}
    transkriptio = bytearray()
    자바원문 = KR_data / 'testi_nippu.java'
    자바원문.write_text('public class testi_nippu { public static void main(String[] argumentit) throws Exception { suomi.oma.tulostuspaikka.kirjoitus_rivi("JAR Suorita_komento: " + argumentit[0]); suomi.oma.tiedoston_nimi.Kirjoitus("jar.txt", "oma ydin_ARVO tiedoston_nimi"); suomi.oma.tulostuspaikka.kirjoitus_rivi(suomi.oma.tiedoston_nimi.Luku("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(aloite_juuri/'build/java-library/classes'), '-d', str(KR_data), str(자바원문)])
    Arkisto = io.BytesIO()
    with zipfile.ZipFile(Arkisto, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: testi_nippu\r\n\r\n')
        자바꾸러미.write(str(KR_data/'testi_nippu.class'), 'testi_nippu.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); portin_numero = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); palvelin_virta_portti = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); palvelin_datagrammi_portti = 임시자원.getsockname()[1]
    with silta_3de4fe3a(portin_numero, ['tcp:{}:9300'.format(palvelin_virta_portti), 'udp:{}:9301'.format(palvelin_datagrammi_portti)], siepata=True) as silta:
        Prosessi = subprocess.Popen(komento() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + silta.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        valitsin = selectors.DefaultSelector(); valitsin.register(Prosessi.stdout, selectors.EVENT_READ)
        def saada_sanoma(merkintä=b'jkoros-native> ', suoritus_AIKAKATKAISU=60):
            data = bytearray(); lopettaa_puhelu_SIIRTYMÄ = time.monotonic() + suoritus_AIKAKATKAISU
            while merkintä not in data:
                if time.monotonic() > lopettaa_puhelu_SIIRTYMÄ or Prosessi.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + data.decode('utf-8', 'replace'))
                for 누름값, _ in valitsin.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); transkriptio.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8', 'replace').replace('\r\n', '\n')
        def liittymä(syöterivi):
            Prosessi.stdin.write(syöterivi.encode() + b'\n'); Prosessi.stdin.flush(); return saada_sanoma()
        try:
            saada_sanoma(); assert 'FTP listening' in liittymä('ftpd start')
            tiedostonsiirto_yhteys = ftplib.FTP(); tiedostonsiirto_yhteys.encoding = 'utf-8'; tiedostonsiirto_yhteys.connect('127.0.0.1', portin_numero, timeout=20); tiedostonsiirto_yhteys.login()
            tiedot_data = bytes(range(256)) * 32
            tiedostonsiirto_yhteys.storbinary('STOR binary.dat', io.BytesIO(tiedot_data))
            TULOS = bytearray(); tiedostonsiirto_yhteys.retrbinary('RETR binary.dat', TULOS.extend)
            assert TULOS == tiedot_data; assert tiedostonsiirto_yhteys.size('binary.dat') == len(tiedot_data)
            vahvistus_raportti['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            tiedostonsiirto_yhteys.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in liittymä('cat 한글.txt')
            assert '한글.txt' in tiedostonsiirto_yhteys.nlst()
            assert dict(tiedostonsiirto_yhteys.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            vahvistus_raportti['checks'].append('UTF-8 filename and content visible in guest shell')
            try: tiedostonsiirto_yhteys.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            TULOS = bytearray(); tiedostonsiirto_yhteys.retrbinary('RETR binary.dat', TULOS.extend); assert TULOS == tiedot_data
            vahvistus_raportti['checks'].append('oversized replacement rejected; previous file preserved')
            with tiedostonsiirto_yhteys.transfercmd('STOR pending.txt') as Upload_Files:
                # A control command must not change the active upload's destination.
                assert tiedostonsiirto_yhteys.size('binary.dat') == len(tiedot_data)
                Upload_Files.sendall(b'UPLOAD TARGET PRESERVED')
            assert tiedostonsiirto_yhteys.voidresp().startswith('226')
            TULOS = bytearray(); tiedostonsiirto_yhteys.retrbinary('RETR pending.txt', TULOS.extend)
            assert TULOS == b'UPLOAD TARGET PRESERVED'
            TULOS = bytearray(); tiedostonsiirto_yhteys.retrbinary('RETR binary.dat', TULOS.extend)
            assert TULOS == tiedot_data
            tiedostonsiirto_yhteys.delete('pending.txt')
            vahvistus_raportti['checks'].append('interleaved SIZE cannot change the active STOR destination')
            tiedostonsiirto_yhteys.storbinary('STOR 인사.jar', io.BytesIO(Arkisto.getvalue()))
            teksti = liittymä('java -jar 인사.jar 누리')
            assert 'JAR Suorita_komento: 누리' in teksti and 'oma ydin_ARVO tiedoston_nimi' in teksti and 'exit 0' in teksti, teksti
            teksti = liittymä('./인사.jar 세상')
            assert 'JAR Suorita_komento: 세상' in teksti and 'exit 0' in teksti, teksti
            vahvistus_raportti['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct data { int numero; double 비율; };\nint SUM_ARVO(int n) { return n ? n + SUM_ARVO(n-1) : 0; }\nint main(void) { struct data ARVO = {SUM_ARVO(10), 1.25}; if (ARVO.numero != 55 || ARVO.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = avata_Tiedosto("cc.txt", luku_ja_kirjoitus | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; kirjoitus_Tiedosto_data(문서, 인사, sizeof(인사)-1); Sulje_Tiedosto(문서); kirjoitus_Tiedosto_data(1, 인사, sizeof(인사)-1); return 0; }\n'
            tiedostonsiirto_yhteys.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            teksti = liittymä('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in teksti and 'exit 0' in teksti, teksti
            teksti = liittymä('run 한글.elf'); assert 'CC NATIVE PASS' in teksti and 'exit 0' in teksti, teksti
            assert 'CC NATIVE PASS' in liittymä('cat cc.txt')
            suoritettava_tiedosto = bytearray(); tiedostonsiirto_yhteys.retrbinary('RETR 한글.elf', suoritettava_tiedosto.extend)
            assert suoritettava_tiedosto[:4] == b'\x7fELF' and suoritettava_tiedosto[18:20] == b'\xb7\x00'
            tiedostonsiirto_yhteys.storbinary('STOR kopioida_ARVO.elf', io.BytesIO(suoritettava_tiedosto)); teksti = liittymä('run kopioida_ARVO.elf'); assert 'CC NATIVE PASS' in teksti and 'exit 0' in teksti, teksti
            tiedostonsiirto_yhteys.storbinary('STOR Suorita_komento', io.BytesIO(suoritettava_tiedosto)); teksti=liittymä('./Suorita_komento');assert 'CC NATIVE PASS' in teksti and 'exit 0' in teksti,teksti
            tiedostonsiirto_yhteys.storbinary('STOR Nimi.txt', io.BytesIO(suoritettava_tiedosto)); teksti=liittymä('./Nimi.txt');assert 'CC NATIVE PASS' in teksti and 'exit 0' in teksti,teksti
            liittymä('rm Suorita_komento Nimi.txt')
            vahvistus_raportti['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            liittymä('rm binary.dat 한글.txt 한글.c 한글.elf kopioida_ARVO.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KR_data/'linux-reference')
            tiedostonsiirto_yhteys.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            teksti=liittymä('./리눅스인사');assert 'exit -8' in teksti,teksti
            teksti=liittymä('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in teksti,teksti
            assert 'LINUX ELF FILE IO' in liittymä('cat linux.txt')
            tiedostonsiirto_yhteys.delete('리눅스인사');tiedostonsiirto_yhteys.delete('linux.txt')
            tiedostonsiirto_yhteys.storbinary('STOR EPÄTOSI_ARVO.elf',io.BytesIO(b'plain text'))
            assert '실행할 numero 없습니다:' in liittymä('./EPÄTOSI_ARVO.elf');tiedostonsiirto_yhteys.delete('EPÄTOSI_ARVO.elf')
            vahvistus_raportti['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as päivitys_palvelin_merkintä:
                NET_lähde = KR_data/'바깥통신.java'
                NET_lähde.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Yhdistä = suomi.oma.yhteys_välitys.Yhdistä("10.0.2.2", Integer.parseInt(args[0]));
 Yhdistä.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] lähdetiedosto = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<lähdetiedosto.length;i++) if (Yhdistä.getInputStream().read() != (lähdetiedosto[i]&255)) throw new RuntimeException("TCP mismatch");
 Yhdistä.close();
 DatagramSocket päätepiste = suomi.oma.통신.Avaa(0); suomi.oma.통신.AIKAKATKAISU(päätepiste, 500);
 suomi.oma.통신.lähettää(päätepiste, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!suomi.oma.통신.saada(päätepiste).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 päätepiste.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(aloite_juuri/'build/java-library/classes'),'-d',str(KR_data),str(NET_lähde)])
                tiedostonsiirto_yhteys.storbinary('STOR 바깥통신.class', io.BytesIO((KR_data/'바깥통신.class').read_bytes()))
                teksti = liittymä('java 바깥통신 {} {}'.format(päivitys_palvelin_merkintä.TCP_portti, päivitys_palvelin_merkintä.UDP_portti))
                assert 'EXTERNAL TCP UDP PASS' in teksti and '10.0.2.2' in teksti and 'exit 0' in teksti, teksti
                assert päivitys_palvelin_merkintä.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, päivitys_palvelin_merkintä.수신됨
                assert not päivitys_palvelin_merkintä.오류들, päivitys_palvelin_merkintä.오류들
            vahvistus_raportti['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            tiedostonsiirto_yhteys.delete('바깥통신.class')
            palvelin_lähde=KR_data/'palvelin_testi.java'
            palvelin_lähde.write_text('''import java.net.*; public class palvelin_testi {
 public static void main(String[] args) throws Exception {
  ServerSocket palvelin_ARVO = new ServerSocket(9300); DatagramSocket päätepiste = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket vieras_ARVO = palvelin_ARVO.accept();
  vieras_ARVO.getOutputStream().write(vieras_ARVO.getInputStream().read()+1); vieras_ARVO.close(); palvelin_ARVO.close();
  byte[] Sisältö_ARVO = new byte[8]; DatagramPacket datagrammi = new DatagramPacket(Sisältö_ARVO, Sisältö_ARVO.length); päätepiste.receive(datagrammi);
  päätepiste.send(datagrammi); päätepiste.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_data),str(palvelin_lähde)])
            tiedostonsiirto_yhteys.storbinary('STOR palvelin_testi.class',io.BytesIO((KR_data/'palvelin_testi.class').read_bytes()))
            Prosessi.stdin.write('java palvelin_testi\n'.encode());Prosessi.stdin.flush();saada_sanoma(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',palvelin_virta_portti),timeout=5) as vertaissolmu_ARVO:
                vertaissolmu_ARVO.sendall(b'A');assert vertaissolmu_ARVO.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as vertaissolmu_ARVO:
                vertaissolmu_ARVO.settimeout(5);vertaissolmu_ARVO.sendto(b'UDP-IN',('127.0.0.1',palvelin_datagrammi_portti));assert vertaissolmu_ARVO.recvfrom(512)[0]==b'UDP-IN'
            teksti=saada_sanoma();assert 'INBOUND TCP UDP PASS' in teksti and 'exit 0' in teksti,teksti
            vahvistus_raportti['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            tiedostonsiirto_yhteys.delete('palvelin_testi.class')
            käsky_JONO = 'public class 빛 { public static void main(String[] argumentit) throws Exception { int SUM_ARVO = 0; int numero = 1; while (numero <= 10) { SUM_ARVO = SUM_ARVO + numero; numero = numero + 1; } suomi.oma.tulostuspaikka.kirjoitus_numero(SUM_ARVO); suomi.oma.tiedoston_nimi.Kirjoitus("aot.txt", "한글 AOT tiedoston_nimi 😀"); suomi.oma.tulostuspaikka.kirjoitus_rivi(suomi.oma.tiedoston_nimi.Luku("aot.txt")); } }'
            tiedostonsiirto_yhteys.storbinary('STOR 빛.java', io.BytesIO(käsky_JONO.encode()))
            teksti = liittymä('javac 빛.java'); assert 'exit 0' in teksti and 'Compiled:' in teksti, teksti
            teksti = liittymä('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in teksti and 'exit 0' in teksti, teksti
            teksti = liittymä('run 빛.elf'); assert '\n55\n' in teksti and '한글 AOT tiedoston_nimi 😀' in teksti and 'exit 0' in teksti, teksti
            alkuperäinen = bytearray(); tiedostonsiirto_yhteys.retrbinary('RETR 빛.elf', alkuperäinen.extend)
            teksti = liittymä('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in teksti and 'unsupported' in teksti, teksti
            보존자료 = bytearray(); tiedostonsiirto_yhteys.retrbinary('RETR 빛.elf', 보존자료.extend); assert alkuperäinen == 보존자료
            바이트코드 = bytearray(); tiedostonsiirto_yhteys.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            tiedostonsiirto_yhteys.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            teksti = liittymä('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in teksti and 'exit 0' in teksti, teksti
            teksti = liittymä('run 빛.elf'); assert '\n55\n' in teksti and '한글 AOT tiedoston_nimi 😀' in teksti and 'exit 0' in teksti, teksti
            vahvistus_raportti['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            vahvistus_raportti['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            staattinen_lähde=KR_data/'staattinen_testi.java'
            staattinen_lähde.write_text('''public class staattinen_testi {
 static int aloite_juuri = 3;
 static int SUM_ARVO(int n) { return n == 0 ? 0 : n + SUM_ARVO(n-1); }
 public static void main(String[] argumentit) {
  int[] ARVO = new int[] {aloite_juuri, SUM_ARVO(10)};
  System.out.println(ARVO[0] + ARVO[1]); System.out.println(argumentit[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_data),str(staattinen_lähde)])
            tiedostonsiirto_yhteys.storbinary('STOR staattinen_testi.class',io.BytesIO((KR_data/'staattinen_testi.class').read_bytes()))
            teksti=liittymä('jaot staattinen_testi.class -o staattinen_testi.elf');assert 'exit 0' in teksti,teksti
            teksti=liittymä('run staattinen_testi.elf 한글인수');assert '\n58\n한글인수\nexit 0' in teksti,teksti
            tiedostonsiirto_yhteys.delete('staattinen_testi.class');tiedostonsiirto_yhteys.delete('staattinen_testi.elf')
            vahvistus_raportti['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arkisto.getvalue());손상자료[14]^=1
            tiedostonsiirto_yhteys.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            teksti=liittymä('java -jar 인사.jar');assert 'Main-Class\nexit 1' in teksti,teksti
            vahvistus_raportti['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            tiedostonsiirto_yhteys.quit(); assert 'FTP stopped' in liittymä('ftpd stop')
            assert not silta.VIRHE, silta.VIRHE
            vahvistus_raportti.update(passed=True, frames_to_guest=silta.커널수신틀수, frames_from_guest=silta.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in valitsin.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: transkriptio.extend(조각)
            silta.Keskeytä_tapahtuma.set()
            Prosessi.terminate()
            try: Prosessi.wait(timeout=5)
            except subprocess.TimeoutExpired: Prosessi.kill(); Prosessi.wait()
            valitsin.close(); Prosessi.stdin.close(); Prosessi.stdout.close()
            vahvistus_raportti['bridge_error'] = silta.VIRHE
            vahvistus_raportti['frames_to_guest'] = silta.커널수신틀수; vahvistus_raportti['frames_from_guest'] = silta.커널발신틀수
            (KR_data/'packets.json').write_text(json.dumps(silta.tapahtumaloki,indent=2)+'\n')
            (KR_data / 'serial.log').write_bytes(transkriptio)
            (KR_data / 'report.json').write_text(json.dumps(vahvistus_raportti, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Suorita_2()
