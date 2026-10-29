#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 לבצע_פקודה, כשל_ערך/משאב_ערך 경계 시험."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
import time
from נסה_משתמש_רשת import מחשב_וירטואלי, מיקום


def ערוך_ערך(מחשב, שם, תוכן_ערך, מאגר_ערך=True):
    הפעלה = len(מחשב.לרשום_שיא)
    מחשב.직렬.sendall(('edit ' + שם + '\n').encode())
    מחשב.מצב_המתנה('...> ', הפעלה)
    for שורה in תוכן_ערך.splitlines():
        assert len(שורה) <= 128
        הפעלה = len(מחשב.לרשום_שיא)
        מחשב.직렬.sendall((שורה + '\n').encode())
        מחשב.מצב_המתנה('...> ', הפעלה)
    הפעלה = len(מחשב.לרשום_שיא)
    מחשב.직렬.sendall(b'.save\n' if מאגר_ערך else b'.cancel\n')
    תוצאה = מחשב.מצב_המתנה('jkoros> ', הפעלה)
    assert ('Saved:' if מאגר_ערך else 'Cancelled; original preserved') in תוצאה, תוצאה


def קובץ_למען():
    תוצאה = subprocess.check_output(['nm', '-n', str(מיקום / 'build/kernel.elf')], universal_newlines=True)
    for שורה in תוצאה.splitlines():
        if שורה.endswith(' ram_files'):
            return int(שורה.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def אורח_קובץ(מחשב, חריץ_ערך_ff41a4f1, גודל, נתיב):
    # 시험 VM의 메모리에서 בפועל_נתונים 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    למען = קובץ_למען() + חריץ_ערך_ff41a4f1 * 16384
    מחשב.צג_ערך.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(למען, גודל, נתיב)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if נתיב.exists() and נתיב.stat().st_size == גודל:
            return נתיב.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def בדיקות_שהופעלו(종류):
    מחשב = מחשב_וירטואלי(מיקום / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, רשת_ערך=False)
    תוצאה = {}
    try:
        מחשב.פקודה('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        מחשב.פקודה('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        מחשב.פקודה('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        מחשב.פקודה('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        מחשב.פקודה('java Missing', ['cannot read class: -2', 'Exit: 1'])
        מחשב.פקודה('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        מחשב.פקודה('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        תוכן_ערך = '''public class Calc {
 public static int fact(int n) {
  if (n <= 1) { return 1; } else { return n * fact(n - 1); }
 }
 public static boolean check(int n) { return n == 7; }
 public static void main(String[] args) {
  int n = Integer.parseInt(args[0]);
  System.out.println(fact(n));
  int sum = 0;
  for (int i = 1; i <= n; i++) { sum = sum + i; }
  while (n > 0) { n--; }
  System.out.println(sum);
  System.out.println(n);
  System.out.println(check(7) && false || true);
  System.out.println(false && 1 / 0 == 0);
  System.out.println(true || 1 / 0 == 0);
  System.out.println(-2147483648 / -1);
  System.out.println(args[1]);
  System.out.println(args[1].length());
  System.out.println(args.length);
  String label = "sum=";
  label += sum;
  System.out.println(label);
  System.out.println(12 + "x" + false);
  System.out.println("logic=" + (true && check(7)));
  char letter = 'a';
  letter++;
  System.out.println(letter);
  System.out.println("letter=" + letter);
  int extra = 7;
  extra *= 3;
  extra -= 1;
  System.out.println(extra);
 }
}'''
        ערוך_ערך(מחשב, 'Calc.java', תוכן_ערך)
        מחשב.פקודה('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        פלטטקסט = מחשב.פקודה('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        תוצאה['guest_output'] = פלטטקסט
        ערך_רשימה = מחשב.פקודה('ls', ['Calc.class'])
        גודל = int(re.search(r'Calc\.class\s+(\d+) bytes', ערך_רשימה).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as מדריך_ערך:
            נתיב = Path(מדריך_ערך) / 'Calc.class'
            נתונים = אורח_קובץ(מחשב, 3, גודל, נתיב)
            בפועל_נתונים = subprocess.check_output(['java', '-Xverify:all', '-cp', מדריך_ערך, 'Calc', '6', 'guest'], universal_newlines=True)
            assert בפועל_נתונים.splitlines() == 기대, בפועל_נתונים
            תוצאה['class_sha256'] = hashlib.sha256(נתונים).hexdigest()
            תוצאה['openjdk_output'] = בפועל_נתונים
        # 실패한 ערוך_ערך/컴파일은 기존 class를 보존한다.
        ערוך_ערך(מחשב, 'Calc.java', 'not Java at all', מאגר_ערך=False)
        מחשב.פקודה('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for לא_חוקי_תוצאה in [
            'public class Calc { public static void main(String[] args) { int x = ; } }',
            'public class Calc { public static void main(String[] args) { int x = true; } }',
            'public class Calc { public static void main(String[] args) { int x = 2147483648; } }',
            'public class Calc { public static int f() { int x = 1; } }',
            'public class Calc { public static void main(String[] args) { Object x = new Object(); } }',
            'public class Other { public static void main(String[] args) {} }',
            'public class Calc { public static void main(String[] args) { int while = 3; } }',
            'public class Calc { public static void main(String[] args) { if (true) int x = 3; } }',
            'public class Calc { public static void main(String[] args) { int x = 010; } }',
        ]:
            ערוך_ערך(מחשב, 'Calc.java', לא_חוקי_תוצאה)
            מחשב.פקודה('javac Calc.java', ['javac error:', 'Exit: 1'])
            מחשב.פקודה('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # סבב_ערך 실행은 משתמש ערימה_ערך/프레임을 매번 초기화한다.
        for 수 in range(12):
            מחשב.פקודה('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        מחשב.פקודה('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        מחשב.פקודה('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        ערוך_ערך(מחשב, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        מחשב.פקודה('javac Calc.java', ['Compiled:', 'Exit: 0'])
        מחשב.פקודה('java Calc', ['instruction limit', 'Exit: 1'])
        מחשב.פקודה('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        ערוך_ערך(מחשב, 'Bad.class', 'garbage')
        מחשב.פקודה('java Bad', ['JVM error:', 'Exit: 1'])
        מחשב.פקודה('rm Bad.class', ['Removed'])
        מחשב.פקודה('java Bad', ['cannot read class: -2'])
        # ערוך_ערך 입력의 넘친 부분을 잘라서 저장하지 않는다.
        הפעלה = len(מחשב.לרשום_שיא)
        מחשב.직렬.sendall(b'edit Hello.java\n')
        מחשב.מצב_המתנה('...> ', הפעלה)
        הפעלה = len(מחשב.לרשום_שיא)
        מחשב.직렬.sendall(b'x' * 129 + b'\n')
        מחשב.מצב_המתנה('...> ', הפעלה)
        מחשב.פקודה('.save', ['Too much input; original preserved'])
        מחשב.פקודה('javac Hello.java', ['Compiled:', 'Exit: 0'])
        ערוך_ערך(מחשב, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            ערוך_ערך(מחשב, 'f' + str(수), 'occupied')
        מחשב.פקודה('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        מחשב.פקודה('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in מחשב.לרשום_שיא.decode('utf-8', 'replace')
        תוצאה['serial'] = מחשב.לרשום_שיא.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return תוצאה
    finally:
        מחשב.סגירה()


def 주코드(נתונים):
    """손상 시험용 main Code의 בפועל_נתונים קובץ 오프셋/길이만 읽는다."""
    עמדה_ערך = 8
    def 짧():
        nonlocal עמדה_ערך
        ערך = struct.unpack_from('>H', נתונים, עמדה_ערך)[0]
        עמדה_ערך += 2
        return ערך
    def 정():
        nonlocal עמדה_ערך
        ערך = struct.unpack_from('>I', נתונים, עמדה_ערך)[0]
        עמדה_ערך += 4
        return ערך
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = נתונים[עמדה_ערך]
        עמדה_ערך += 1
        if 종류 == 1:
            길이 = 짧()
            문자들[수] = נתונים[עמדה_ערך:עמדה_ערך + 길이]
            עמדה_ערך += 길이
        elif 종류 in (7, 8): עמדה_ערך += 2
        elif 종류 in (3, 9, 10, 12): עמדה_ערך += 4
        else: raise AssertionError(종류)
    עמדה_ערך += 6
    개수 = 짧()
    עמדה_ערך += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        שם = 짧()
        짧()
        for 수 in range(짧()):
            ערך_תכונה = 짧()
            גודל = 정()
            if 문자들[שם] == b'main' and 문자들[ערך_תכונה] == b'Code':
                return עמדה_ערך + 8, struct.unpack_from('>I', נתונים, עמדה_ערך + 4)[0]
            עמדה_ערך += גודל
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        מדריך_ערך = Path(임시)
        (מדריך_ערך / 'build').mkdir()
        קודמקור = מדריך_ערך / 'Imported.java'
        קודמקור.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(קודמקור)], check=True)
        원본 = (מדריך_ערך / 'Imported.class').read_bytes()
        קוד_ערך, 길이 = 주코드(원본)
        משתנה_ערך = {}
        נתונים = bytearray(원본); נתונים[0] = 0; משתנה_ערך['BadMagic'] = נתונים
        נתונים = bytearray(원본); נתונים[7] = 61; משתנה_ערך['BadVer'] = נתונים
        נתונים = bytearray(원본); נתונים[8:10] = b'\xff\xff'; משתנה_ערך['BadPool'] = נתונים
        נתונים = bytearray(원본); נתונים[קוד_ערך:קוד_ערך + 길이] = bytes(길이)
        נתונים[קוד_ערך:קוד_ערך + 3] = b'\xa7\x00\x01'; נתונים[קוד_ערך + 길이 - 1] = 177; משתנה_ערך['BadJump'] = נתונים
        נתונים = bytearray(원본); נתונים[קוד_ערך:קוד_ערך + 길이] = bytes(길이)
        נתונים[קוד_ערך] = 87; נתונים[קוד_ערך + 길이 - 1] = 177; משתנה_ערך['BadStack'] = נתונים
        # שם 검사를 통과시켜 בפועל_נתונים לבצע_פקודה 중의 אופרנד_רמז 오류까지 검사한다.
        משתנה_ערך['BadStack'] = משתנה_ערך['BadStack'].replace(b'Imported', b'BadStack')
        ערך_ערך = ['Imported.class=' + str(מדריך_ערך / 'Imported.class'), 'Imported.java=' + str(קודמקור)]
        for שם, נתונים in משתנה_ערך.items():
            נתיב = מדריך_ערך / (שם + '.class'); נתיב.write_bytes(נתונים)
            ערך_ערך.append(שם + '.class=' + str(נתיב))
        לקבץ_ערך = מדריך_ערך / 'build/java-files.bin'
        subprocess.run([sys.executable, str(מיקום / 'כלים/자바파일묶기.py'), '-o', str(לקבץ_ערך)] + ערך_ערך, check=True)
        subprocess.run(['as', '--32', '-o', str(מדריך_ערך / 'user.o'), str(מיקום / '부팅/משתמש.s')], cwd=str(מדריך_ערך), check=True)
        ליבה_ערך = מדריך_ערך / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(מיקום / '부팅/לקשר_ניווט.ld'), '-o', str(ליבה_ערך),
                        str(מיקום / 'build/boot.o'), str(מיקום / 'build/java.o'), str(מדריך_ערך / 'user.o'), str(מיקום / 'build/apps.o')], check=True)
        מחשב = מחשב_וירטואלי(ליבה_ערך, רשת_ערך=False)
        try:
            מחשב.פקודה('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            מחשב.פקודה('cat Imported.java', ['int[] values = new int[3]'])
            for שם, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                מחשב.פקודה('java ' + שם, [문구, 'Exit: 1'])
                מחשב.פקודה('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return מחשב.לרשום_שיא.decode('utf-8', 'replace')
        finally:
            מחשב.סגירה()


if __name__ == '__main__':
    ניתוח_מבנה_טקסט_ערך = argparse.ArgumentParser()
    ניתוח_מבנה_טקסט_ערך.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    ארגומנטים = ניתוח_מבנה_טקסט_ערך.parse_args()
    תוצאה = {종류: בדיקות_שהופעלו(종류) for 종류 in (('elf', 'iso') if ארגומנטים.boot == 'both' else (ארגומנטים.boot,))}
    תוצאה['import'] = 적재시험()
    (מיקום / 'build/자바시험.json').write_text(json.dumps(תוצאה, ensure_ascii=False, indent=2) + '\n')
