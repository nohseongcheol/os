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
from мост_3de4fe3a import мост_3de4fe3a
from 실행 import задача_корень, команда
from вывод_на_экран_средство import вывод_на_экран_средство
from 실행파일시험 import 리눅스예제


def запустить():
    KR_данные = задача_корень / 'build/verification/ftp'; KR_данные.mkdir(parents=True, exist_ok=True)
    проверка_Отчет = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((задача_корень / 'build/kernel8.img').read_bytes()).hexdigest()}
    расшифровка = bytearray()
    자바원문 = KR_данные / 'тест_пакет.java'
    자바원문.write_text('public class тест_пакет { public static void main(String[] аргументы) throws Exception { русский.свой.текстовыйВывод.запись_линия("JAR 실행: " + аргументы[0]); русский.свой.файл.Запись("jar.txt", "свой ядро_ЗНАЧЕН файл"); русский.свой.текстовыйВывод.запись_линия(русский.свой.файл.Чтение("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(задача_корень/'build/java-library/classes'), '-d', str(KR_данные), str(자바원문)])
    Архив = io.BytesIO()
    with zipfile.ZipFile(Архив, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: тест_пакет\r\n\r\n')
        자바꾸러미.write(str(KR_данные/'тест_пакет.class'), 'тест_пакет.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); номер_порта = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); сервер_поток_порт = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); сервер_датаграмма_порт = 임시자원.getsockname()[1]
    with мост_3de4fe3a(номер_порта, ['tcp:{}:9300'.format(сервер_поток_порт), 'udp:{}:9301'.format(сервер_датаграмма_порт)], Сбор=True) as мост:
        Процесс = subprocess.Popen(команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + мост.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        селектор = selectors.DefaultSelector(); селектор.register(Процесс.stdout, selectors.EVENT_READ)
        def получить_письмо(метка=b'jkoros-native> ', выполнение_ТАЙМАУТ=60):
            данные = bytearray(); элемент_СМЕЩ = time.monotonic() + выполнение_ТАЙМАУТ
            while метка not in данные:
                if time.monotonic() > элемент_СМЕЩ or Процесс.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + данные.decode('utf-8', 'replace'))
                for 누름값, _ in селектор.select(.1):
                    блок_ЗНАЧЕН_652d4b53 = 누름값.fileobj.read(4096)
                    if блок_ЗНАЧЕН_652d4b53: данные.extend(блок_ЗНАЧЕН_652d4b53); расшифровка.extend(блок_ЗНАЧЕН_652d4b53)
                if b'PANIC:' in данные or b'FAIL ' in данные: raise AssertionError(данные)
            return данные.decode('utf-8', 'replace').replace('\r\n', '\n')
        def оболочка(строка_ввода):
            Процесс.stdin.write(строка_ввода.encode() + b'\n'); Процесс.stdin.flush(); return получить_письмо()
        try:
            получить_письмо(); assert 'FTP listening' in оболочка('ftpd start')
            передача_файла_контакт = ftplib.FTP(); передача_файла_контакт.encoding = 'utf-8'; передача_файла_контакт.connect('127.0.0.1', номер_порта, timeout=20); передача_файла_контакт.login()
            полезные_данные_данные = bytes(range(256)) * 32
            передача_файла_контакт.storbinary('STOR binary.dat', io.BytesIO(полезные_данные_данные))
            результат = bytearray(); передача_файла_контакт.retrbinary('RETR binary.dat', результат.extend)
            assert результат == полезные_данные_данные; assert передача_файла_контакт.size('binary.dat') == len(полезные_данные_данные)
            проверка_Отчет['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            передача_файла_контакт.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in оболочка('cat 한글.txt')
            assert '한글.txt' in передача_файла_контакт.nlst()
            assert dict(передача_файла_контакт.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            проверка_Отчет['checks'].append('UTF-8 filename and content visible in guest shell')
            try: передача_файла_контакт.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            результат = bytearray(); передача_файла_контакт.retrbinary('RETR binary.dat', результат.extend); assert результат == полезные_данные_данные
            проверка_Отчет['checks'].append('oversized replacement rejected; previous file preserved')
            with передача_файла_контакт.transfercmd('STOR pending.txt') as Upload_Файлы:
                # A control command must not change the active upload's destination.
                assert передача_файла_контакт.size('binary.dat') == len(полезные_данные_данные)
                Upload_Файлы.sendall(b'UPLOAD TARGET PRESERVED')
            assert передача_файла_контакт.voidresp().startswith('226')
            результат = bytearray(); передача_файла_контакт.retrbinary('RETR pending.txt', результат.extend)
            assert результат == b'UPLOAD TARGET PRESERVED'
            результат = bytearray(); передача_файла_контакт.retrbinary('RETR binary.dat', результат.extend)
            assert результат == полезные_данные_данные
            передача_файла_контакт.delete('pending.txt')
            проверка_Отчет['checks'].append('interleaved SIZE cannot change the active STOR destination')
            передача_файла_контакт.storbinary('STOR приветствие_ae353e94.jar', io.BytesIO(Архив.getvalue()))
            текст = оболочка('java -jar приветствие_ae353e94.jar 누리')
            assert 'JAR 실행: 누리' in текст and 'свой ядро_ЗНАЧЕН файл' in текст and 'exit 0' in текст, текст
            текст = оболочка('./приветствие_ae353e94.jar 세상')
            assert 'JAR 실행: 세상' in текст and 'exit 0' in текст, текст
            проверка_Отчет['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <файл_ABI.h>\nstruct данные { int 수; double 비율; };\nint SUM_ЗНАЧЕН(int n) { return n ? n + SUM_ЗНАЧЕН(n-1) : 0; }\nint main(void) { struct данные ЗНАЧЕН = {SUM_ЗНАЧЕН(10), 1.25}; if (ЗНАЧЕН.수 != 55 || ЗНАЧЕН.비율 * 2 != 2.5) return 3; const char приветствие_ae353e94[] = "CC NATIVE PASS\\n"; int 문서 = открыть_файл("cc.txt", для_чтения_и_записи | 없으면만들기 | усечь_Оглавление, 0600); if (문서 < 0) return 1; запись_файл_данные(문서, приветствие_ae353e94, sizeof(приветствие_ae353e94)-1); Close_файл(문서); запись_файл_данные(1, приветствие_ae353e94, sizeof(приветствие_ae353e94)-1); return 0; }\n'
            передача_файла_контакт.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            текст = оболочка('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in текст and 'exit 0' in текст, текст
            текст = оболочка('run 한글.elf'); assert 'CC NATIVE PASS' in текст and 'exit 0' in текст, текст
            assert 'CC NATIVE PASS' in оболочка('cat cc.txt')
            исполняемый_файл = bytearray(); передача_файла_контакт.retrbinary('RETR 한글.elf', исполняемый_файл.extend)
            assert исполняемый_файл[:4] == b'\x7fELF' and исполняемый_файл[18:20] == b'\xb7\x00'
            передача_файла_контакт.storbinary('STOR экземпляр_ЗНАЧЕН.elf', io.BytesIO(исполняемый_файл)); текст = оболочка('run экземпляр_ЗНАЧЕН.elf'); assert 'CC NATIVE PASS' in текст and 'exit 0' in текст, текст
            передача_файла_контакт.storbinary('STOR 실행', io.BytesIO(исполняемый_файл)); текст=оболочка('./실행');assert 'CC NATIVE PASS' in текст and 'exit 0' in текст,текст
            передача_файла_контакт.storbinary('STOR Название.txt', io.BytesIO(исполняемый_файл)); текст=оболочка('./Название.txt');assert 'CC NATIVE PASS' in текст and 'exit 0' in текст,текст
            оболочка('rm 실행 Название.txt')
            проверка_Отчет['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            оболочка('rm binary.dat 한글.txt 한글.c 한글.elf экземпляр_ЗНАЧЕН.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KR_данные/'linux-reference')
            передача_файла_контакт.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            текст=оболочка('./리눅스인사');assert 'exit -8' in текст,текст
            текст=оболочка('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in текст,текст
            assert 'LINUX ELF FILE IO' in оболочка('cat linux.txt')
            передача_файла_контакт.delete('리눅스인사');передача_файла_контакт.delete('linux.txt')
            передача_файла_контакт.storbinary('STOR ЛОЖЬ_ЗНАЧЕН.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in оболочка('./ЛОЖЬ_ЗНАЧЕН.elf');передача_файла_контакт.delete('ЛОЖЬ_ЗНАЧЕН.elf')
            проверка_Отчет['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with вывод_на_экран_средство() as вывод_на_экран_сервер_ввод:
                NET_источник = KR_данные/'внешний_коммуникация.java'
                NET_источник.write_text('''import java.net.*; import java.io.*;
public class внешний_коммуникация { public static void main(String[] args) throws Exception {
 Socket Подключить = русский.свой.контакт_транспортировка.Подключить("10.0.2.2", Integer.parseInt(args[0]));
 Подключить.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] исходныйКод = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<исходныйКод.length;i++) if (Подключить.getInputStream().read() != (исходныйКод[i]&255)) throw new RuntimeException("TCP mismatch");
 Подключить.close();
 DatagramSocket участник = русский.свой.коммуникация.Открыть(0); русский.свой.коммуникация.ТАЙМАУТ(участник, 500);
 русский.свой.коммуникация.написать(участник, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!русский.свой.коммуникация.получить(участник).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 участник.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(задача_корень/'build/java-library/classes'),'-d',str(KR_данные),str(NET_источник)])
                передача_файла_контакт.storbinary('STOR внешний_коммуникация.class', io.BytesIO((KR_данные/'внешний_коммуникация.class').read_bytes()))
                текст = оболочка('java внешний_коммуникация {} {}'.format(вывод_на_экран_сервер_ввод.TCP_порт, вывод_на_экран_сервер_ввод.UDP_порт))
                assert 'EXTERNAL TCP UDP PASS' in текст and '10.0.2.2' in текст and 'exit 0' in текст, текст
                assert вывод_на_экран_сервер_ввод.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, вывод_на_экран_сервер_ввод.수신됨
                assert not вывод_на_экран_сервер_ввод.오류들, вывод_на_экран_сервер_ввод.오류들
            проверка_Отчет['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            передача_файла_контакт.delete('внешний_коммуникация.class')
            сервер_источник=KR_данные/'сервер_тест.java'
            сервер_источник.write_text('''import java.net.*; public class сервер_тест {
 public static void main(String[] args) throws Exception {
  ServerSocket сервер_ЗНАЧЕН = new ServerSocket(9300); DatagramSocket участник = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket гость_ЗНАЧЕН = сервер_ЗНАЧЕН.accept();
  гость_ЗНАЧЕН.getOutputStream().write(гость_ЗНАЧЕН.getInputStream().read()+1); гость_ЗНАЧЕН.close(); сервер_ЗНАЧЕН.close();
  byte[] контент_ЗНАЧЕН = new byte[8]; DatagramPacket датаграмма = new DatagramPacket(контент_ЗНАЧЕН, контент_ЗНАЧЕН.length); участник.receive(датаграмма);
  участник.send(датаграмма); участник.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_данные),str(сервер_источник)])
            передача_файла_контакт.storbinary('STOR сервер_тест.class',io.BytesIO((KR_данные/'сервер_тест.class').read_bytes()))
            Процесс.stdin.write('java сервер_тест\n'.encode());Процесс.stdin.flush();получить_письмо(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',сервер_поток_порт),timeout=5) as одноранговый_ЗНАЧЕН:
                одноранговый_ЗНАЧЕН.sendall(b'A');assert одноранговый_ЗНАЧЕН.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as одноранговый_ЗНАЧЕН:
                одноранговый_ЗНАЧЕН.settimeout(5);одноранговый_ЗНАЧЕН.sendto(b'UDP-IN',('127.0.0.1',сервер_датаграмма_порт));assert одноранговый_ЗНАЧЕН.recvfrom(512)[0]==b'UDP-IN'
            текст=получить_письмо();assert 'INBOUND TCP UDP PASS' in текст and 'exit 0' in текст,текст
            проверка_Отчет['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            передача_файла_контакт.delete('сервер_тест.class')
            명령열 = 'public class 빛 { public static void main(String[] аргументы) throws Exception { int SUM_ЗНАЧЕН = 0; int 수 = 1; while (수 <= 10) { SUM_ЗНАЧЕН = SUM_ЗНАЧЕН + 수; 수 = 수 + 1; } русский.свой.текстовыйВывод.수쓰기(SUM_ЗНАЧЕН); русский.свой.файл.Запись("aot.txt", "한글 AOT файл 😀"); русский.свой.текстовыйВывод.запись_линия(русский.свой.файл.Чтение("aot.txt")); } }'
            передача_файла_контакт.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            текст = оболочка('javac 빛.java'); assert 'exit 0' in текст and 'Compiled:' in текст, текст
            текст = оболочка('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in текст and 'exit 0' in текст, текст
            текст = оболочка('run 빛.elf'); assert '\n55\n' in текст and '한글 AOT файл 😀' in текст and 'exit 0' in текст, текст
            собственный = bytearray(); передача_файла_контакт.retrbinary('RETR 빛.elf', собственный.extend)
            текст = оболочка('jaot приветствие_ae353e94.jar -o 빛.elf'); assert 'exit 1' in текст and 'unsupported' in текст, текст
            보존자료 = bytearray(); передача_файла_контакт.retrbinary('RETR 빛.elf', 보존자료.extend); assert собственный == 보존자료
            바이트코드 = bytearray(); передача_файла_контакт.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            передача_файла_контакт.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            текст = оболочка('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in текст and 'exit 0' in текст, текст
            текст = оболочка('run 빛.elf'); assert '\n55\n' in текст and '한글 AOT файл 😀' in текст and 'exit 0' in текст, текст
            проверка_Отчет['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            проверка_Отчет['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            статический_источник=KR_данные/'статический_тест.java'
            статический_источник.write_text('''public class статический_тест {
 static int задача_корень = 3;
 static int SUM_ЗНАЧЕН(int n) { return n == 0 ? 0 : n + SUM_ЗНАЧЕН(n-1); }
 public static void main(String[] аргументы) {
  int[] ЗНАЧЕН = new int[] {задача_корень, SUM_ЗНАЧЕН(10)};
  System.out.println(ЗНАЧЕН[0] + ЗНАЧЕН[1]); System.out.println(аргументы[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_данные),str(статический_источник)])
            передача_файла_контакт.storbinary('STOR статический_тест.class',io.BytesIO((KR_данные/'статический_тест.class').read_bytes()))
            текст=оболочка('jaot статический_тест.class -o статический_тест.elf');assert 'exit 0' in текст,текст
            текст=оболочка('run статический_тест.elf 한글인수');assert '\n58\n한글인수\nexit 0' in текст,текст
            передача_файла_контакт.delete('статический_тест.class');передача_файла_контакт.delete('статический_тест.elf')
            проверка_Отчет['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Архив.getvalue());손상자료[14]^=1
            передача_файла_контакт.storbinary('STOR приветствие_ae353e94.jar',io.BytesIO(손상자료))
            текст=оболочка('java -jar приветствие_ae353e94.jar');assert 'Main-Class\nexit 1' in текст,текст
            проверка_Отчет['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            передача_файла_контакт.quit(); assert 'FTP stopped' in оболочка('ftpd stop')
            assert not мост.ошибка, мост.ошибка
            проверка_Отчет.update(passed=True, frames_to_guest=мост.커널수신틀수, frames_from_guest=мост.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in селектор.select(0):
                блок_ЗНАЧЕН_652d4b53=누름값.fileobj.read(65536)
                if блок_ЗНАЧЕН_652d4b53: расшифровка.extend(блок_ЗНАЧЕН_652d4b53)
            мост.пауза_Событие.set()
            Процесс.terminate()
            try: Процесс.wait(timeout=5)
            except subprocess.TimeoutExpired: Процесс.kill(); Процесс.wait()
            селектор.close(); Процесс.stdin.close(); Процесс.stdout.close()
            проверка_Отчет['bridge_error'] = мост.ошибка
            проверка_Отчет['frames_to_guest'] = мост.커널수신틀수; проверка_Отчет['frames_from_guest'] = мост.커널발신틀수
            (KR_данные/'packets.json').write_text(json.dumps(мост.журнал_трассировки,indent=2)+'\n')
            (KR_данные / 'serial.log').write_bytes(расшифровка)
            (KR_данные / 'report.json').write_text(json.dumps(проверка_Отчет, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': запустить()
