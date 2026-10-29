#!/usr/bin/env python3
"""фактический_данные QEMU/VNC에서 экран Размер·граница_ЗНАЧЕН·Окно переместить_ЗНАЧЕН·Swing·언어별 그리기를 검사한다."""
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
from PIL import Image
from компьютер_Вид import СОВПАД_ЗНАЧЕН
from 실행 import задача_корень


def разрешение_тест(너비, 높이, KR_путь):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); номер_порта = 임시.getsockname()[1]
    изменить_размер_SMS = '{}x{}'.format(너비, 높이)
    Процесс_ЗНАЧЕН = subprocess.Popen(['python3', str(задача_корень/'инструменты/실행.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(номер_порта), '--resolution', изменить_размер_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектор_a916db4e = selectors.DefaultSelector(); селектор_a916db4e.register(Процесс_ЗНАЧЕН.stdout, selectors.EVENT_READ)
    LOG_ЗАПИСЬ = bytearray(); удаленный_ЗНАЧЕН = None; передать_ЗНАЧЕН_630ba093 = None

    def 기다리기(выпуск_ЗНАЧЕН, запустить=0):
        крайний_срок_ЗНАЧЕН = time.monotonic() + 60
        while выпуск_ЗНАЧЕН not in LOG_ЗАПИСЬ[запустить:]:
            if time.monotonic() > крайний_срок_ЗНАЧЕН or Процесс_ЗНАЧЕН.poll() is not None or b'HALTED' in LOG_ЗАПИСЬ or b'PANIC:' in LOG_ЗАПИСЬ:
                raise AssertionError(LOG_ЗАПИСЬ[запустить:].decode('utf-8', 'replace'))
            for Событие, _ in селектор_a916db4e.select(.1):
                данные = Событие.fileobj.read(65536)
                if данные: LOG_ЗАПИСЬ.extend(данные)
        return LOG_ЗАПИСЬ[запустить:].decode('utf-8', 'replace')

    def клик_кнопка(символ, 눌림=True): удаленный_ЗНАЧЕН.sendall(struct.pack('>BBHI', 4, int(눌림), 0, символ))

    def отправить_SMS_сообщение(текст):
        запустить = len(LOG_ЗАПИСЬ)
        for знак_ЗНАЧЕН in текст:
            символ = 0xff0d if знак_ЗНАЧЕН == '\n' else ord(знак_ЗНАЧЕН) if ord(знак_ЗНАЧЕН) < 256 else 0x1000000 | ord(знак_ЗНАЧЕН)
            клик_кнопка(символ); клик_кнопка(символ, False)
        return запустить

    def оболочка(текст): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', отправить_SMS_сообщение(текст+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Вертикаль_позиция, 눌림): удаленный_ЗНАЧЕН.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Вертикаль_позиция))

    def клик_ЗНАЧЕН(가로, Вертикаль_позиция): 가리키기(가로, Вертикаль_позиция, 1); 가리키기(가로, Вертикаль_позиция, 0)

    def точечный_рисунок_фото():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 фактический_данные 너비를 쓴다.
        удаленный_ЗНАЧЕН.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        рисунок_ЗНАЧЕН = Image.new('RGB', (너비, 높이)); область_ЗНАЧЕН_9285603e = 0
        while True:
            Вид_ЗНАЧЕН = СОВПАД_ЗНАЧЕН(удаленный_ЗНАЧЕН, 1)[0]
            if Вид_ЗНАЧЕН == 2: continue
            if Вид_ЗНАЧЕН == 3:
                длина_ЗНАЧЕН = struct.unpack('>I', СОВПАД_ЗНАЧЕН(удаленный_ЗНАЧЕН, 7)[3:])[0]; СОВПАД_ЗНАЧЕН(удаленный_ЗНАЧЕН, длина_ЗНАЧЕН); continue
            assert Вид_ЗНАЧЕН == 0, Вид_ЗНАЧЕН
            товар_СЧЁТ = struct.unpack('>H', СОВПАД_ЗНАЧЕН(удаленный_ЗНАЧЕН, 3)[1:])[0]
            for _ in range(товар_СЧЁТ):
                가로, Вертикаль_позиция, 폭, длина_ЗНАЧЕН, кодирование_ЗНАЧЕН = struct.unpack('>HHHHi', СОВПАД_ЗНАЧЕН(удаленный_ЗНАЧЕН, 12))
                assert кодирование_ЗНАЧЕН == 0 and 가로+폭 <= 너비 and Вертикаль_позиция+длина_ЗНАЧЕН <= 높이
                рисунок_ЗНАЧЕН.paste(Image.frombytes('RGB', (폭, длина_ЗНАЧЕН), СОВПАД_ЗНАЧЕН(удаленный_ЗНАЧЕН, 폭*длина_ЗНАЧЕН*4), 'raw', 'BGRX'), (가로, Вертикаль_позиция))
                область_ЗНАЧЕН_9285603e += 폭*длина_ЗНАЧЕН
            if область_ЗНАЧЕН_9285603e:
                assert область_ЗНАЧЕН_9285603e == 너비*높이, область_ЗНАЧЕН_9285603e
                return рисунок_ЗНАЧЕН

    def чек_пиксель(координата_ЗНАЧЕН, 색):
        крайний_срок_ЗНАЧЕН = time.monotonic()+10
        while True:
            рисунок_ЗНАЧЕН = точечный_рисунок_фото()
            if рисунок_ЗНАЧЕН.getpixel(координата_ЗНАЧЕН) == 색: return рисунок_ЗНАЧЕН
            if time.monotonic() > крайний_срок_ЗНАЧЕН: raise AssertionError((координата_ЗНАЧЕН, рисунок_ЗНАЧЕН.getpixel(координата_ЗНАЧЕН), 색))

    def Upload_Файлы(Название, данные): передать_ЗНАЧЕН_630ba093.storbinary('STOR '+Название, io.BytesIO(данные))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+изменить_размер_SMS+' RGB32').encode() in LOG_ЗАПИСЬ
        print('BOOT:', изменить_размер_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_ЗАПИСЬ).group(1))
        удаленный_ЗНАЧЕН = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert СОВПАД_ЗНАЧЕН(удаленный_ЗНАЧЕН, 12) == b'RFB 003.008\n'; удаленный_ЗНАЧЕН.sendall(b'RFB 003.008\n')
        assert 1 in СОВПАД_ЗНАЧЕН(удаленный_ЗНАЧЕН, СОВПАД_ЗНАЧЕН(удаленный_ЗНАЧЕН, 1)[0]); удаленный_ЗНАЧЕН.sendall(b'\x01')
        assert СОВПАД_ЗНАЧЕН(удаленный_ЗНАЧЕН, 4) == b'\0'*4; удаленный_ЗНАЧЕН.sendall(b'\x01')
        начальное_состояние = СОВПАД_ЗНАЧЕН(удаленный_ЗНАЧЕН, 24); assert struct.unpack('>HH', начальное_состояние[:4]) == (너비, 높이)
        СОВПАД_ЗНАЧЕН(удаленный_ЗНАЧЕН, struct.unpack('>I', начальное_состояние[20:])[0])
        удаленный_ЗНАЧЕН.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        удаленный_ЗНАЧЕН.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        чек_пиксель((너비-1, 높이-1), (24, 32, 48))
        # экран право 아래까지 이동한다. Назад_товар 640×480 граница_ЗНАЧЕН 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        чек_пиксель((너비-568, 높이-360), (32, 80, 144))
        запустить = len(LOG_ЗАПИСЬ); клик_ЗНАЧЕН(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', запустить)
        чек_пиксель((너비-568, 높이-360), (24, 32, 48))
        запустить = len(LOG_ЗАПИСЬ); клик_ЗНАЧЕН(80, 16); 기다리기(b'TERMINAL FOCUS 1', запустить)
        оболочка('ftpd start')
        передать_ЗНАЧЕН_630ba093 = ftplib.FTP(); передать_ЗНАЧЕН_630ba093.encoding = 'utf-8'; передать_ЗНАЧЕН_630ba093.connect('127.0.0.1', номер_порта, timeout=20); передать_ЗНАЧЕН_630ba093.login()
        # C граница_ЗНАЧЕН 검사는 32비트 unsigned 음수 ПРЕОБР_ЗНАЧЕН·клип 밖·빈 사각형을 포함한다.
        исходныйКод = '''#include <экран_ABI.h>
#include <файл_ABI.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(выписать_прямоугольник(너비,높이,0,0,0)) return 2;
    if(выписать_прямоугольник(너비,높이-1,1,1,0)!=-22) return 3;
    if(выписать_прямоугольник(너비-1,높이,1,1,0)!=-22) return 4;
    if(выписать_прямоугольник(-1,0,1,1,0)!=-22) return 5;
    if(выписать_прямоугольник(0,0,-1,1,0)!=-22) return 6;
    if(выписать_прямоугольник(너비-1,높이-1,1,1,0x332211)) return 7;
    запись_файл_данные(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Файлы('тест_экран.c', исходныйКод.encode())
        assert 'exit 0' in оболочка('cc /тест_экран.c -o /тест_экран')
        기다리기(b'C RESOLUTION PASS', отправить_SMS_сообщение('run /тест_экран\n'))
        чек_пиксель((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', отправить_SMS_сообщение('q'))
        исходныйКод = '''from русский import экран_изменить_размер, выписать_прямоугольник, 그림기다리기, текстовыйВывод, системная_ошибка
너비, 높이 = экран_изменить_размер()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    выписать_прямоугольник(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except системная_ошибка as ошибка:
    assert ошибка.ИНДЕКС == 22
выписать_прямоугольник(너비-1, 높이-1, 1, 1, 0x665544)
текстовыйВывод("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Файлы('тест_экран.py', исходныйКод.encode())
        기다리기(b'PYTHON RESOLUTION PASS', отправить_SMS_сообщение('python /тест_экран.py\n'))
        чек_пиксель((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', отправить_SMS_сообщение('q'))
        исходныйКод = '''import русский.свой.*;
public class разрешение_тест {
    public static void main(String[] аргументы) {
        int 너비=экран.너비(), 높이=экран.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Состояние_исключение("Размер");
        try { экран.прямоугольник(너비,높이-1,1,1,0); throw new Состояние_исключение("клип"); }
        catch (неверный_аргумент_исключение ошибка) { }
        экран.удалить_ввод_c8dbc399(0x302018);
        экран.прямоугольник(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        экран.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # исключение 처리는 узел javac 결과를 свой JVM에 올려 검사한다.
        граница_источник = KR_путь/'해상도경계시험.java'
        граница_источник.write_text(исходныйКод.replace('class разрешение_тест', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(задача_корень/'dist/jkoros-native-korean.jar'), '-d', str(KR_путь), str(граница_источник)])
        Upload_Файлы('해상도경계시험.class', (KR_путь/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', отправить_SMS_сообщение('java 해상도경계시험\n'))
        чек_пиксель((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', отправить_SMS_сообщение('q'))
        # 게스트 javac의 опора_ЗНАЧЕН 문법으로 Размер запрос_ЗНАЧЕН·удалить_ввод_c8dbc399·다섯 аргументы 그리기를 컴파일한다.
        исходныйКод = '''public class разрешение_тест {
    public static void main(String[] аргументы) {
        int 너비=русский.свой.экран.너비();
        int 높이=русский.свой.экран.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        русский.свой.экран.удалить_ввод_c8dbc399(3153944);
        русский.свой.экран.прямоугольник(너비-1,높이-1,1,1,10061943);
        русский.свой.текстовыйВывод.запись_линия("JAVA RESOLUTION PASS");
        русский.свой.экран.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Файлы('разрешение_тест.java', исходныйКод.encode())
        результат = оболочка('javac разрешение_тест.java'); assert 'exit 0' in результат, результат
        기다리기(b'JAVA RESOLUTION PASS', отправить_SMS_сообщение('java разрешение_тест\n'))
        чек_пиксель((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', отправить_SMS_сообщение('q'))
        Upload_Файлы('свинг_тест.class', (KR_путь/'свинг_тест.class').read_bytes())
        기다리기(b'SWING READY', отправить_SMS_сообщение('java свинг_тест\n'))
        가로, Вертикаль_позиция = (너비-400)//2, (높이-280)//2
        рисунок_ЗНАЧЕН = чек_пиксель((가로, Вертикаль_позиция), (32, 80, 144))
        рисунок_ЗНАЧЕН.save(str(KR_путь/(изменить_размер_SMS+'.png')))
        запустить = len(LOG_ЗАПИСЬ); клик_ЗНАЧЕН(가로+80, Вертикаль_позиция+155)
        기다리기('SWING CLICK Название'.encode(), запустить)
        запустить = len(LOG_ЗАПИСЬ); клик_ЗНАЧЕН(가로+385, Вертикаль_позиция+15); 기다리기(b'jkoros-native> ', запустить)
        assert 'AFTER_RESOLUTION' in оболочка('echo AFTER_RESOLUTION')
        print('PASS:', изменить_размер_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if передать_ЗНАЧЕН_630ba093: передать_ЗНАЧЕН_630ba093.close()
        if удаленный_ЗНАЧЕН: удаленный_ЗНАЧЕН.close()
        if Процесс_ЗНАЧЕН.poll() is None:
            Процесс_ЗНАЧЕН.terminate()
            try: Процесс_ЗНАЧЕН.wait(timeout=8)
            except subprocess.TimeoutExpired: Процесс_ЗНАЧЕН.kill(); Процесс_ЗНАЧЕН.wait()
        селектор_a916db4e.close(); Процесс_ЗНАЧЕН.stdout.close()
        (KR_путь/(изменить_размер_SMS+'.log')).write_bytes(LOG_ЗАПИСЬ)


def запустить():
    KR_путь = задача_корень/'build/verification/resolution'; KR_путь.mkdir(parents=True, exist_ok=True)
    LOG_ЗАПИСЬ = {'passed': False, 'kernel_sha256': hashlib.sha256((задача_корень/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for неверный_ЗНАЧЕН in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            результат = subprocess.run(['python3', str(задача_корень/'инструменты/실행.py'), '--resolution', неверный_ЗНАЧЕН], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert результат.returncode == 2 and b'--resolution' in результат.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(KR_путь), str(задача_корень/'испытания/자바/свинг_тест.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            разрешение_тест(너비, 높이, KR_путь); LOG_ЗАПИСЬ['resolutions'].append([너비, 높이])
        LOG_ЗАПИСЬ.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (KR_путь/'report.json').write_text(json.dumps(LOG_ЗАПИСЬ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': запустить()
