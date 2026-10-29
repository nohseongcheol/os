#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 आज्ञा_कार्यवाही_करा, बिघाड_मूल्य/संसाधन_मूल्य सीमा_मूल्य चाचण्या."""
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
from प्रयोक्ता_संचारजाळे_चाचणी import व्हर्च्युअल_मशीन, जागा


def संपादन_मूल्य(मशीन, नाव, सामुग्री_मूल्य, साठवणे_मूल्य=True):
    सुरू_करा = len(मशीन.लॉग_नोंद)
    मशीन.अनुक्रमिक_मूल्य.sendall(('edit ' + नाव + '\n').encode())
    मशीन.प्रतीक्षा_करा_राज्य('...> ', सुरू_करा)
    for ओळ in सामुग्री_मूल्य.splitlines():
        assert len(ओळ) <= 128
        सुरू_करा = len(मशीन.लॉग_नोंद)
        मशीन.अनुक्रमिक_मूल्य.sendall((ओळ + '\n').encode())
        मशीन.प्रतीक्षा_करा_राज्य('...> ', सुरू_करा)
    सुरू_करा = len(मशीन.लॉग_नोंद)
    मशीन.अनुक्रमिक_मूल्य.sendall(b'.save\n' if साठवणे_मूल्य else b'.cancel\n')
    मोजमाप = मशीन.प्रतीक्षा_करा_राज्य('jkoros> ', सुरू_करा)
    assert ('Saved:' if साठवणे_मूल्य else 'Cancelled; original preserved') in मोजमाप, मोजमाप


def संचिका_पत्ता():
    मोजमाप = subprocess.check_output(['nm', '-n', str(जागा / 'build/kernel.elf')], universal_newlines=True)
    for ओळ in मोजमाप.splitlines():
        if ओळ.endswith(' ram_files'):
            return int(ओळ.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def अतिथी_संचिका(मशीन, खाच_मूल्य, आकार, मार्ग):
    # चाचण्या VM의 메모리에서 वास्तविक_डेटा 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    पत्ता = संचिका_पत्ता() + खाच_मूल्य * 16384
    मशीन.मॉनिटर_मूल्य.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(पत्ता, आकार, मार्ग)).encode())
    शेवट = time.monotonic() + 5
    while time.monotonic() < शेवट:
        if मार्ग.exists() and मार्ग.stat().st_size == आकार:
            return मार्ग.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def रन_चाचणी(प्रकार_मूल्य):
    मशीन = व्हर्च्युअल_मशीन(जागा / ('build/kernel.elf' if प्रकार_मूल्य == 'elf' else 'build/kernel.iso'), प्रकार_मूल्य, संचारजाळे_मूल्य=False)
    मोजमाप = {}
    try:
        मशीन.आदेश('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        मशीन.आदेश('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        मशीन.आदेश('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        मशीन.आदेश('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        मशीन.आदेश('java Missing', ['cannot read class: -2', 'Exit: 1'])
        मशीन.आदेश('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        मशीन.आदेश('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        सामुग्री_मूल्य = '''public class Calc {
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
        संपादन_मूल्य(मशीन, 'Calc.java', सामुग्री_मूल्य)
        मशीन.आदेश('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        अपेक्षा = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        आउटपुट = मशीन.आदेश('java Calc 6 guest', ['\r\n' + '\r\n'.join(अपेक्षा) + '\r\n', 'Exit: 0'])
        मोजमाप['guest_output'] = आउटपुट
        प्रविष्टी_यादी = मशीन.आदेश('ls', ['Calc.class'])
        आकार = int(re.search(r'Calc\.class\s+(\d+) bytes', प्रविष्टी_यादी).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as निर्देशिका_मूल्य:
            मार्ग = Path(निर्देशिका_मूल्य) / 'Calc.class'
            डेटा = अतिथी_संचिका(मशीन, 3, आकार, मार्ग)
            वास्तविक_डेटा = subprocess.check_output(['java', '-Xverify:all', '-cp', निर्देशिका_मूल्य, 'Calc', '6', 'guest'], universal_newlines=True)
            assert वास्तविक_डेटा.splitlines() == अपेक्षा, वास्तविक_डेटा
            मोजमाप['class_sha256'] = hashlib.sha256(डेटा).hexdigest()
            मोजमाप['openjdk_output'] = वास्तविक_डेटा
        # 실패한 संपादन_मूल्य/컴파일은 기존 class를 보존한다.
        संपादन_मूल्य(मशीन, 'Calc.java', 'not Java at all', साठवणे_मूल्य=False)
        मशीन.आदेश('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for अवैध_मोजमाप in [
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
            संपादन_मूल्य(मशीन, 'Calc.java', अवैध_मोजमाप)
            मशीन.आदेश('javac Calc.java', ['javac error:', 'Exit: 1'])
            मशीन.आदेश('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # पुनरावृत्ती_मूल्य 실행은 प्रयोक्ता गतिमानस्मृतिराशी_मूल्य/프레임을 매번 초기화한다.
        for संख्या in range(12):
            मशीन.आदेश('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        मशीन.आदेश('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        मशीन.आदेश('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        संपादन_मूल्य(मशीन, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        मशीन.आदेश('javac Calc.java', ['Compiled:', 'Exit: 0'])
        मशीन.आदेश('java Calc', ['instruction limit', 'Exit: 1'])
        मशीन.आदेश('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        संपादन_मूल्य(मशीन, 'Bad.class', 'garbage')
        मशीन.आदेश('java Bad', ['JVM error:', 'Exit: 1'])
        मशीन.आदेश('rm Bad.class', ['Removed'])
        मशीन.आदेश('java Bad', ['cannot read class: -2'])
        # संपादन_मूल्य 입력의 넘친 부분을 잘라서 저장하지 않는다.
        सुरू_करा = len(मशीन.लॉग_नोंद)
        मशीन.अनुक्रमिक_मूल्य.sendall(b'edit Hello.java\n')
        मशीन.प्रतीक्षा_करा_राज्य('...> ', सुरू_करा)
        सुरू_करा = len(मशीन.लॉग_नोंद)
        मशीन.अनुक्रमिक_मूल्य.sendall(b'x' * 129 + b'\n')
        मशीन.प्रतीक्षा_करा_राज्य('...> ', सुरू_करा)
        मशीन.आदेश('.save', ['Too much input; original preserved'])
        मशीन.आदेश('javac Hello.java', ['Compiled:', 'Exit: 0'])
        संपादन_मूल्य(मशीन, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for संख्या in range(3):
            संपादन_मूल्य(मशीन, 'f' + str(संख्या), 'occupied')
        मशीन.आदेश('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        मशीन.आदेश('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in मशीन.लॉग_नोंद.decode('utf-8', 'replace')
        मोजमाप['serial'] = मशीन.लॉग_नोंद.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(प्रकार_मूल्य))
        return मोजमाप
    finally:
        मशीन.बंद_करा()


def प्रमुख_संहिता(डेटा):
    """손상 시험용 main Code의 वास्तविक_डेटा फाइल 오프셋/길이만 읽는다."""
    स्थान_मूल्य = 8
    def चिन्हरहित_लघु_वाचा():
        nonlocal स्थान_मूल्य
        मूल्य = struct.unpack_from('>H', डेटा, स्थान_मूल्य)[0]
        स्थान_मूल्य += 2
        return मूल्य
    def चिन्हरहित_पूर्णांक_वाचा():
        nonlocal स्थान_मूल्य
        मूल्य = struct.unpack_from('>I', डेटा, स्थान_मूल्य)[0]
        स्थान_मूल्य += 4
        return मूल्य
    वर्ण_मूल्ये = {}
    for संख्या in range(1, चिन्हरहित_लघु_वाचा()):
        प्रकार_मूल्य = डेटा[स्थान_मूल्य]
        स्थान_मूल्य += 1
        if प्रकार_मूल्य == 1:
            लांबी_मूल्य = चिन्हरहित_लघु_वाचा()
            वर्ण_मूल्ये[संख्या] = डेटा[स्थान_मूल्य:स्थान_मूल्य + लांबी_मूल्य]
            स्थान_मूल्य += लांबी_मूल्य
        elif प्रकार_मूल्य in (7, 8): स्थान_मूल्य += 2
        elif प्रकार_मूल्य in (3, 9, 10, 12): स्थान_मूल्य += 4
        else: raise AssertionError(प्रकार_मूल्य)
    स्थान_मूल्य += 6
    आयटम_संख्या = चिन्हरहित_लघु_वाचा()
    स्थान_मूल्य += आयटम_संख्या * 2
    assert चिन्हरहित_लघु_वाचा() == 0
    for संख्या in range(चिन्हरहित_लघु_वाचा()):
        चिन्हरहित_लघु_वाचा()
        नाव = चिन्हरहित_लघु_वाचा()
        चिन्हरहित_लघु_वाचा()
        for संख्या in range(चिन्हरहित_लघु_वाचा()):
            गुणधर्म_मूल्य = चिन्हरहित_लघु_वाचा()
            आकार = चिन्हरहित_पूर्णांक_वाचा()
            if वर्ण_मूल्ये[नाव] == b'main' and वर्ण_मूल्ये[गुणधर्म_मूल्य] == b'Code':
                return स्थान_मूल्य + 8, struct.unpack_from('>I', डेटा, स्थान_मूल्य + 4)[0]
            स्थान_मूल्य += आकार
    raise AssertionError('main Code missing')


def भारणे_चाचणी():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as तात्पुरते_मूल्य:
        निर्देशिका_मूल्य = Path(तात्पुरते_मूल्य)
        (निर्देशिका_मूल्य / 'build').mkdir()
        स्रोत = निर्देशिका_मूल्य / 'Imported.java'
        स्रोत.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(स्रोत)], check=True)
        मूळ = (निर्देशिका_मूल्य / 'Imported.class').read_bytes()
        संहिता_मूल्य, लांबी_मूल्य = प्रमुख_संहिता(मूळ)
        प्रकारांतर_मूल्य = {}
        डेटा = bytearray(मूळ); डेटा[0] = 0; प्रकारांतर_मूल्य['BadMagic'] = डेटा
        डेटा = bytearray(मूळ); डेटा[7] = 61; प्रकारांतर_मूल्य['BadVer'] = डेटा
        डेटा = bytearray(मूळ); डेटा[8:10] = b'\xff\xff'; प्रकारांतर_मूल्य['BadPool'] = डेटा
        डेटा = bytearray(मूळ); डेटा[संहिता_मूल्य:संहिता_मूल्य + लांबी_मूल्य] = bytes(लांबी_मूल्य)
        डेटा[संहिता_मूल्य:संहिता_मूल्य + 3] = b'\xa7\x00\x01'; डेटा[संहिता_मूल्य + लांबी_मूल्य - 1] = 177; प्रकारांतर_मूल्य['BadJump'] = डेटा
        डेटा = bytearray(मूळ); डेटा[संहिता_मूल्य:संहिता_मूल्य + लांबी_मूल्य] = bytes(लांबी_मूल्य)
        डेटा[संहिता_मूल्य] = 87; डेटा[संहिता_मूल्य + लांबी_मूल्य - 1] = 177; प्रकारांतर_मूल्य['BadStack'] = डेटा
        # नाव 검사를 통과시켜 वास्तविक_डेटा आज्ञा_कार्यवाही_करा 중의 संकार्य_स्टॅक 오류까지 검사한다.
        प्रकारांतर_मूल्य['BadStack'] = प्रकारांतर_मूल्य['BadStack'].replace(b'Imported', b'BadStack')
        प्रविष्टी_मूल्य = ['Imported.class=' + str(निर्देशिका_मूल्य / 'Imported.class'), 'Imported.java=' + str(स्रोत)]
        for नाव, डेटा in प्रकारांतर_मूल्य.items():
            मार्ग = निर्देशिका_मूल्य / (नाव + '.class'); मार्ग.write_bytes(डेटा)
            प्रविष्टी_मूल्य.append(नाव + '.class=' + str(मार्ग))
        समूह_मूल्य = निर्देशिका_मूल्य / 'build/java-files.bin'
        subprocess.run([sys.executable, str(जागा / 'साधने/बंडल_जावा_संचिका.py'), '-o', str(समूह_मूल्य)] + प्रविष्टी_मूल्य, check=True)
        subprocess.run(['as', '--32', '-o', str(निर्देशिका_मूल्य / 'user.o'), str(जागा / 'प्रणालीप्रारंभ/प्रयोक्ता.s')], cwd=str(निर्देशिका_मूल्य), check=True)
        गाभा_मूल्य = निर्देशिका_मूल्य / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(जागा / 'प्रणालीप्रारंभ/लिंक_लेआउट.ld'), '-o', str(गाभा_मूल्य),
                        str(जागा / 'build/boot.o'), str(जागा / 'build/java.o'), str(निर्देशिका_मूल्य / 'user.o'), str(जागा / 'build/apps.o')], check=True)
        मशीन = व्हर्च्युअल_मशीन(गाभा_मूल्य, संचारजाळे_मूल्य=False)
        try:
            मशीन.आदेश('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            मशीन.आदेश('cat Imported.java', ['int[] values = new int[3]'])
            for नाव, शब्दसमूह_मूल्य in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                मशीन.आदेश('java ' + नाव, [शब्दसमूह_मूल्य, 'Exit: 1'])
                मशीन.आदेश('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return मशीन.लॉग_नोंद.decode('utf-8', 'replace')
        finally:
            मशीन.बंद_करा()


if __name__ == '__main__':
    मूल्य_पार्स_करा = argparse.ArgumentParser()
    मूल्य_पार्स_करा.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    बाबी = मूल्य_पार्स_करा.parse_args()
    मोजमाप = {प्रकार_मूल्य: रन_चाचणी(प्रकार_मूल्य) for प्रकार_मूल्य in (('elf', 'iso') if बाबी.boot == 'both' else (बाबी.boot,))}
    मोजमाप['import'] = भारणे_चाचणी()
    (जागा / 'build/जावा_चाचणी.json').write_text(json.dumps(मोजमाप, ensure_ascii=False, indent=2) + '\n')
