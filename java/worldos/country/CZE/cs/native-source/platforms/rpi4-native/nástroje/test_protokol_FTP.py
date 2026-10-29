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
from Provést_příkaz import akce_kořen, příkaz
from zobrazení_výsledků_testovací_přípravek import zobrazení_výsledků_testovací_přípravek
from 실행파일시험 import 리눅스예제


def Spustit_2():
    KV_data = akce_kořen / 'build/verification/ftp'; KV_data.mkdir(parents=True, exist_ok=True)
    ověření_Zpráva = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((akce_kořen / 'build/kernel8.img').read_bytes()).hexdigest()}
    přepis = bytearray()
    자바원문 = KV_data / 'test_sada.java'
    자바원문.write_text('public class test_sada { public static void main(String[] argumenty) throws Exception { čeština.vlastní.výstupní_pozice.zápis_čára("JAR Provést_příkaz: " + argumenty[0]); čeština.vlastní.název_souboru.Zápis("jar.txt", "vlastní jádro_HODNOTA název_souboru"); čeština.vlastní.výstupní_pozice.zápis_čára(čeština.vlastní.název_souboru.Čtení("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(akce_kořen/'build/java-library/classes'), '-d', str(KV_data), str(자바원문)])
    Archiv = io.BytesIO()
    with zipfile.ZipFile(Archiv, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: test_sada\r\n\r\n')
        자바꾸러미.write(str(KV_data/'test_sada.class'), 'test_sada.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); číslo_portu = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_tok_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_datagram_port = 임시자원.getsockname()[1]
    with most_3de4fe3a(číslo_portu, ['tcp:{}:9300'.format(server_tok_port), 'udp:{}:9301'.format(server_datagram_port)], čerpat=True) as most:
        Proces = subprocess.Popen(příkaz() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + most.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selektor = selectors.DefaultSelector(); selektor.register(Proces.stdout, selectors.EVENT_READ)
        def dostat_e_mail(značka=b'jkoros-native> ', spuštění_TIMEOUT=60):
            data = bytearray(); konec_POSUN = time.monotonic() + spuštění_TIMEOUT
            while značka not in data:
                if time.monotonic() > konec_POSUN or Proces.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + data.decode('utf-8', 'replace'))
                for 누름값, _ in selektor.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); přepis.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8', 'replace').replace('\r\n', '\n')
        def prostředí(vstupní_řádek):
            Proces.stdin.write(vstupní_řádek.encode() + b'\n'); Proces.stdin.flush(); return dostat_e_mail()
        try:
            dostat_e_mail(); assert 'FTP listening' in prostředí('ftpd start')
            přenos_souborů_kontakt = ftplib.FTP(); přenos_souborů_kontakt.encoding = 'utf-8'; přenos_souborů_kontakt.connect('127.0.0.1', číslo_portu, timeout=20); přenos_souborů_kontakt.login()
            vytížení_data = bytes(range(256)) * 32
            přenos_souborů_kontakt.storbinary('STOR binary.dat', io.BytesIO(vytížení_data))
            VÝSLEDEK = bytearray(); přenos_souborů_kontakt.retrbinary('RETR binary.dat', VÝSLEDEK.extend)
            assert VÝSLEDEK == vytížení_data; assert přenos_souborů_kontakt.size('binary.dat') == len(vytížení_data)
            ověření_Zpráva['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            přenos_souborů_kontakt.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in prostředí('cat 한글.txt')
            assert '한글.txt' in přenos_souborů_kontakt.nlst()
            assert dict(přenos_souborů_kontakt.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            ověření_Zpráva['checks'].append('UTF-8 filename and content visible in guest shell')
            try: přenos_souborů_kontakt.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            VÝSLEDEK = bytearray(); přenos_souborů_kontakt.retrbinary('RETR binary.dat', VÝSLEDEK.extend); assert VÝSLEDEK == vytížení_data
            ověření_Zpráva['checks'].append('oversized replacement rejected; previous file preserved')
            with přenos_souborů_kontakt.transfercmd('STOR pending.txt') as Upload_Files:
                # A control command must not change the active upload's destination.
                assert přenos_souborů_kontakt.size('binary.dat') == len(vytížení_data)
                Upload_Files.sendall(b'UPLOAD TARGET PRESERVED')
            assert přenos_souborů_kontakt.voidresp().startswith('226')
            VÝSLEDEK = bytearray(); přenos_souborů_kontakt.retrbinary('RETR pending.txt', VÝSLEDEK.extend)
            assert VÝSLEDEK == b'UPLOAD TARGET PRESERVED'
            VÝSLEDEK = bytearray(); přenos_souborů_kontakt.retrbinary('RETR binary.dat', VÝSLEDEK.extend)
            assert VÝSLEDEK == vytížení_data
            přenos_souborů_kontakt.delete('pending.txt')
            ověření_Zpráva['checks'].append('interleaved SIZE cannot change the active STOR destination')
            přenos_souborů_kontakt.storbinary('STOR 인사.jar', io.BytesIO(Archiv.getvalue()))
            text = prostředí('java -jar 인사.jar 누리')
            assert 'JAR Provést_příkaz: 누리' in text and 'vlastní jádro_HODNOTA název_souboru' in text and 'exit 0' in text, text
            text = prostředí('./인사.jar 세상')
            assert 'JAR Provést_příkaz: 세상' in text and 'exit 0' in text, text
            ověření_Zpráva['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <Soubor_ABI.h>\nstruct data { int číslo; double 비율; };\nint SUMA_HODNOTA(int n) { return n ? n + SUMA_HODNOTA(n-1) : 0; }\nint main(void) { struct data HODNOTA = {SUMA_HODNOTA(10), 1.25}; if (HODNOTA.číslo != 55 || HODNOTA.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = otevřít_Soubor("cc.txt", pro_čtení_i_zápis | 없으면만들기 | stříhat_Obsah, 0600); if (문서 < 0) return 1; zápis_Soubor_data(문서, 인사, sizeof(인사)-1); Zavřít_Soubor(문서); zápis_Soubor_data(1, 인사, sizeof(인사)-1); return 0; }\n'
            přenos_souborů_kontakt.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            text = prostředí('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in text and 'exit 0' in text, text
            text = prostředí('run 한글.elf'); assert 'CC NATIVE PASS' in text and 'exit 0' in text, text
            assert 'CC NATIVE PASS' in prostředí('cat cc.txt')
            spustitelný_soubor = bytearray(); přenos_souborů_kontakt.retrbinary('RETR 한글.elf', spustitelný_soubor.extend)
            assert spustitelný_soubor[:4] == b'\x7fELF' and spustitelný_soubor[18:20] == b'\xb7\x00'
            přenos_souborů_kontakt.storbinary('STOR instance_HODNOTA.elf', io.BytesIO(spustitelný_soubor)); text = prostředí('run instance_HODNOTA.elf'); assert 'CC NATIVE PASS' in text and 'exit 0' in text, text
            přenos_souborů_kontakt.storbinary('STOR Provést_příkaz', io.BytesIO(spustitelný_soubor)); text=prostředí('./Provést_příkaz');assert 'CC NATIVE PASS' in text and 'exit 0' in text,text
            přenos_souborů_kontakt.storbinary('STOR Název.txt', io.BytesIO(spustitelný_soubor)); text=prostředí('./Název.txt');assert 'CC NATIVE PASS' in text and 'exit 0' in text,text
            prostředí('rm Provést_příkaz Název.txt')
            ověření_Zpráva['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            prostředí('rm binary.dat 한글.txt 한글.c 한글.elf instance_HODNOTA.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KV_data/'linux-reference')
            přenos_souborů_kontakt.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            text=prostředí('./리눅스인사');assert 'exit -8' in text,text
            text=prostředí('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in text,text
            assert 'LINUX ELF FILE IO' in prostředí('cat linux.txt')
            přenos_souborů_kontakt.delete('리눅스인사');přenos_souborů_kontakt.delete('linux.txt')
            přenos_souborů_kontakt.storbinary('STOR NEPRAVDA_HODNOTA.elf',io.BytesIO(b'plain text'))
            assert '실행할 číslo 없습니다:' in prostředí('./NEPRAVDA_HODNOTA.elf');přenos_souborů_kontakt.delete('NEPRAVDA_HODNOTA.elf')
            ověření_Zpráva['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with zobrazení_výsledků_testovací_přípravek() as zobrazení_výsledků_server_položka:
                čistý_zdroj = KV_data/'externí_komunikace.java'
                čistý_zdroj.write_text('''import java.net.*; import java.io.*;
public class externí_komunikace { public static void main(String[] args) throws Exception {
 Socket Připojit = čeština.vlastní.kontakt_přenos.Připojit("10.0.2.2", Integer.parseInt(args[0]));
 Připojit.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] zdrojový_soubor = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<zdrojový_soubor.length;i++) if (Připojit.getInputStream().read() != (zdrojový_soubor[i]&255)) throw new RuntimeException("TCP mismatch");
 Připojit.close();
 DatagramSocket účastník = čeština.vlastní.komunikace.Otevřít(0); čeština.vlastní.komunikace.TIMEOUT(účastník, 500);
 čeština.vlastní.komunikace.poslat(účastník, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!čeština.vlastní.komunikace.dostat(účastník).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 účastník.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(akce_kořen/'build/java-library/classes'),'-d',str(KV_data),str(čistý_zdroj)])
                přenos_souborů_kontakt.storbinary('STOR externí_komunikace.class', io.BytesIO((KV_data/'externí_komunikace.class').read_bytes()))
                text = prostředí('java externí_komunikace {} {}'.format(zobrazení_výsledků_server_položka.port_TCP, zobrazení_výsledků_server_položka.protokol_UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in text and '10.0.2.2' in text and 'exit 0' in text, text
                assert zobrazení_výsledků_server_položka.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, zobrazení_výsledků_server_položka.수신됨
                assert not zobrazení_výsledků_server_položka.오류들, zobrazení_výsledků_server_položka.오류들
            ověření_Zpráva['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            přenos_souborů_kontakt.delete('externí_komunikace.class')
            server_zdroj=KV_data/'server_test.java'
            server_zdroj.write_text('''import java.net.*; public class server_test {
 public static void main(String[] args) throws Exception {
  ServerSocket server_HODNOTA = new ServerSocket(9300); DatagramSocket účastník = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket host_HODNOTA = server_HODNOTA.accept();
  host_HODNOTA.getOutputStream().write(host_HODNOTA.getInputStream().read()+1); host_HODNOTA.close(); server_HODNOTA.close();
  byte[] Obsah_HODNOTA = new byte[8]; DatagramPacket datagram = new DatagramPacket(Obsah_HODNOTA, Obsah_HODNOTA.length); účastník.receive(datagram);
  účastník.send(datagram); účastník.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KV_data),str(server_zdroj)])
            přenos_souborů_kontakt.storbinary('STOR server_test.class',io.BytesIO((KV_data/'server_test.class').read_bytes()))
            Proces.stdin.write('java server_test\n'.encode());Proces.stdin.flush();dostat_e_mail(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_tok_port),timeout=5) as partner_HODNOTA:
                partner_HODNOTA.sendall(b'A');assert partner_HODNOTA.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as partner_HODNOTA:
                partner_HODNOTA.settimeout(5);partner_HODNOTA.sendto(b'UDP-IN',('127.0.0.1',server_datagram_port));assert partner_HODNOTA.recvfrom(512)[0]==b'UDP-IN'
            text=dostat_e_mail();assert 'INBOUND TCP UDP PASS' in text and 'exit 0' in text,text
            ověření_Zpráva['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            přenos_souborů_kontakt.delete('server_test.class')
            명령열 = 'public class 빛 { public static void main(String[] argumenty) throws Exception { int SUMA_HODNOTA = 0; int číslo = 1; while (číslo <= 10) { SUMA_HODNOTA = SUMA_HODNOTA + číslo; číslo = číslo + 1; } čeština.vlastní.výstupní_pozice.zápis_číslo(SUMA_HODNOTA); čeština.vlastní.název_souboru.Zápis("aot.txt", "한글 AOT název_souboru 😀"); čeština.vlastní.výstupní_pozice.zápis_čára(čeština.vlastní.název_souboru.Čtení("aot.txt")); } }'
            přenos_souborů_kontakt.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            text = prostředí('javac 빛.java'); assert 'exit 0' in text and 'Compiled:' in text, text
            text = prostředí('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in text and 'exit 0' in text, text
            text = prostředí('run 빛.elf'); assert '\n55\n' in text and '한글 AOT název_souboru 😀' in text and 'exit 0' in text, text
            nativní = bytearray(); přenos_souborů_kontakt.retrbinary('RETR 빛.elf', nativní.extend)
            text = prostředí('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in text and 'unsupported' in text, text
            보존자료 = bytearray(); přenos_souborů_kontakt.retrbinary('RETR 빛.elf', 보존자료.extend); assert nativní == 보존자료
            바이트코드 = bytearray(); přenos_souborů_kontakt.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            přenos_souborů_kontakt.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            text = prostředí('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in text and 'exit 0' in text, text
            text = prostředí('run 빛.elf'); assert '\n55\n' in text and '한글 AOT název_souboru 😀' in text and 'exit 0' in text, text
            ověření_Zpráva['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            ověření_Zpráva['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statický_zdroj=KV_data/'statický_test.java'
            statický_zdroj.write_text('''public class statický_test {
 static int akce_kořen = 3;
 static int SUMA_HODNOTA(int n) { return n == 0 ? 0 : n + SUMA_HODNOTA(n-1); }
 public static void main(String[] argumenty) {
  int[] HODNOTA = new int[] {akce_kořen, SUMA_HODNOTA(10)};
  System.out.println(HODNOTA[0] + HODNOTA[1]); System.out.println(argumenty[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KV_data),str(statický_zdroj)])
            přenos_souborů_kontakt.storbinary('STOR statický_test.class',io.BytesIO((KV_data/'statický_test.class').read_bytes()))
            text=prostředí('jaot statický_test.class -o statický_test.elf');assert 'exit 0' in text,text
            text=prostředí('run statický_test.elf 한글인수');assert '\n58\n한글인수\nexit 0' in text,text
            přenos_souborů_kontakt.delete('statický_test.class');přenos_souborů_kontakt.delete('statický_test.elf')
            ověření_Zpráva['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Archiv.getvalue());손상자료[14]^=1
            přenos_souborů_kontakt.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            text=prostředí('java -jar 인사.jar');assert 'Main-Class\nexit 1' in text,text
            ověření_Zpráva['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            přenos_souborů_kontakt.quit(); assert 'FTP stopped' in prostředí('ftpd stop')
            assert not most.chyba, most.chyba
            ověření_Zpráva.update(passed=True, frames_to_guest=most.커널수신틀수, frames_from_guest=most.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in selektor.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: přepis.extend(조각)
            most.Pozastavit_událost.set()
            Proces.terminate()
            try: Proces.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
            selektor.close(); Proces.stdin.close(); Proces.stdout.close()
            ověření_Zpráva['bridge_error'] = most.chyba
            ověření_Zpráva['frames_to_guest'] = most.커널수신틀수; ověření_Zpráva['frames_from_guest'] = most.커널발신틀수
            (KV_data/'packets.json').write_text(json.dumps(most.protokol_trasování,indent=2)+'\n')
            (KV_data / 'serial.log').write_bytes(přepis)
            (KV_data / 'report.json').write_text(json.dumps(ověření_Zpráva, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Spustit_2()
