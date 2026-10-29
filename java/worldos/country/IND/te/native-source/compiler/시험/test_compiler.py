"""వాస్తవ_డేటా ELF అమలు_చేయి_ఆదేశం + OpenJDK ప్రమాణం 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

컴파일러 = Path(__file__).resolve().parents[1] / '컴파일러.py'


class 네이티브시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.సంచయని_మూల్యం = Path(self.임시.name)

    def నిర్మించు_మూలం(self, వనరు, 추가=None, 성공=True, లక్ష్యం='linux', 내보냄=None):
        పథం_జాబితా = []
        for పేరు, విషయం_మూల్యం in dict({'시험': వనరు}, **(추가 or {})).items():
            పాత్ = self.సంచయని_మూల్యం / (పేరు + '.java')
            పాత్.write_text(విషయం_మూల్యం, encoding='utf-8')
            పథం_జాబితా.append(str(పాత్))
        ఆదేశము = [sys.executable, str(컴파일러), '--target', లక్ష్యం, '--entry', '시험.నడుపుము', '-o', str(self.సంచయని_మూల్యం / 'native')]
        if 내보냄 is not None: ఆదేశము += ['--export', 내보냄]
        ప్రమాణం = subprocess.run(ఆదేశము + పథం_జాబితా,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(ప్రమాణం.returncode, 0, ప్రమాణం.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(ప్రమాణం.returncode, 0)
            self.assertIn('నిర్మించు_మూలం దోషం'.encode(), ప్రమాణం.stderr)
        return ప్రమాణం

    def 실행결과(self):
        return subprocess.run([str(self.సంచయని_మూల్యం / 'native')], timeout=5).returncode

    def 자바대조(self, వనరు, 추가=None):
        self.నిర్మించు_మూలం(వనరు, 추가)
        (self.సంచయని_మూల్యం / 'హోస్ట్.java').write_text(
            'public class హోస్ట్ { public static void main(String[] 인수) { System.exit(시험.నడుపుము()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.సంచయని_మూల్యం)] +
                       [str(పాత్) for పాత్ in self.సంచయని_మూల్యం.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.సంచయని_మూల్యం), 'హోస్ట్'], timeout=5).returncode
        వాస్తవ_డేటా = self.실행결과()
        self.assertGreaterEqual(వాస్తవ_డేటా, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 సరిచూడు)')
        self.assertEqual(వాస్తవ_డేటా, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int నడుపుము() {
                int 합 = 7;
                int మూల్యం = 12345;
                for (int సూచీ = -65; సూచీ <= 65; సూచీ++) {
                    మూల్యం = మూల్యం * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(మూల్యం, సూచీ);
                    합 += (byte)మూల్యం + (short)మూల్యం + (char)మూల్యం;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] మూల్యం = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int నడుపుము() {
                int 합 = 13;
                for (int 가 = 0; 가 < మూల్యం.length; 가++)
                    for (int 나 = 1; 나 < మూల్యం.length; 나++)
                        합 = 합 * 31 + మూల్యం[가] / మూల్యం[나] + మూల్యం[가] % మూల్యం[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] క్రియేట్_ప్రవేశం(int పరిమాణం) { return new int[పరిమాణం]; }
            public static int నడుపుము() {
                int[] 가 = క్రియేట్_ప్రవేశం(8); int[] 나 = 가; int[] ఖాళీ_అంశం = new int[0];
                if (가 != 나 || 가 == null || ఖాళీ_అంశం.length != 0 || 가[7] != 0) return 99;
                int మూల్యం = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return మూల్యం + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int మూల్యం = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int నడుపుము() { return 계산(1, 2, 3, 4, మూల్యం) + 보조.చదువు(); }
        }''', {'보조': '''public class 보조 {
            static int మూల్యం = 3;
            static int 초기값() { return ++మూల్యం; }
            static int చదువు() { return మూల్యం; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int మూల్యం = 보조.చదువు() + 1;
            public static int నడుపుము() { return మూల్యం * 10 + 보조.చదువు(); }
        }''', {'보조': '''public class 보조 {
            static int మూల్యం = 시험.మూల్యం + 2;
            static int చదువు() { return మూల్యం; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String పాఠ్యము = "한글\\u0000😀";
            public static int నడుపుము() {
                if (పాఠ్యము != "한글\\u0000😀") return 99;
                return (పాఠ్యము.length() + పాఠ్యము.charAt(2) + పాఠ్యము.charAt(3) + పాఠ్యము.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int క్రమగుణకం(int మూల్యం) { return మూల్యం <= 1 ? 1 : మూల్యం * క్రమగుణకం(మూల్యం - 1); }
            static int 연속(int మూల్యం) {
                switch (మూల్యం) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int మూల్యం) {
                switch (మూల్యం) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int నడుపుము() { return (క్రమగుణకం(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        ప్రకటన = '\n'.join('int మూల్యం{} = {};'.format(సూచీ, సూచీ) for సూచీ in range(270))
        덧셈 = '+'.join('మూల్యం{}'.format(సూచీ) for సూచీ in range(270))
        self.자바대조('public class 시험 { public static int నడుపుము() {' + ప్రకటన +
                    'మూల్యం_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] మూల్యం = null; return మూల్యం.length;', 102),
            ('int[] మూల్యం = new int[1]; return మూల్యం[1];', 103),
            ('int[] మూల్యం = new int[1]; మూల్యం[-1] = 3; return 0;', 103),
            ('int మూల్యం = -1; return new int[మూల్యం].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for ముఖ్యభాగము_మూల్యం, 기대 in 경우들:
            with self.subTest(ముఖ్యభాగము_మూల్యం=ముఖ్యభాగము_మూల్యం):
                self.నిర్మించు_మూలం('public class 시험 { public static int నడుపుము() { ' + ముఖ్యభాగము_మూల్యం + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long మూల్యం; public static int నడుపుము() { return 0; }',
            'public static int నడుపుము() { Object మూల్యం = new Object(); return 0; }',
            'public static int నడుపుము() { System.out.println("hello"); return 0; }',
            'public static int నడుపుము() { try { return 1; } catch (Exception దోషం) { return 2; } }',
            'public static synchronized int నడుపుము() { return 0; }',
            'public static int నడుపుము() { return new byte[3].length; }',
            'static native int 외부(); public static int నడుపుము() { return 외부(); }',
            'int మూల్యం; public static int నడుపుము() { return 0; }',
        ]
        for ముఖ్యభాగము_మూల్యం in 경우들:
            with self.subTest(ముఖ్యభాగము_మూల్యం=ముఖ్యభాగము_మూల్యం):
                self.నిర్మించు_మూలం('public class 시험 { ' + ముఖ్యభాగము_మూల్యం + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        అవుట్పుట్ = self.సంచయని_మూల్యం / 'native'
        అవుట్పుట్.write_bytes(b'original-output')
        self.నిర్మించు_మూలం('public class 시험 { public static int నడుపుము() { return missing; } }', 성공=False)
        self.assertEqual(అవుట్పుట్.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.నిర్మించు_మూలం('public class 시험 { public static int నడుపుము() { return 37; } }')
        self.assertEqual((self.సంచయని_మూల్యం / 'native').read_bytes()[:5], b'\x7fELF\x01')
        అంశం_శోధన_పట్టిక = subprocess.check_output(['readelf', '-l', str(self.సంచయని_మూల్యం / 'native')])
        self.assertNotIn(b'INTERP', అంశం_శోధన_పట్టిక)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.నిర్మించు_మూలం('public class 시험 { public static int నడుపుము() { return వినియోగదారు.실행권한(); } }',
                    {'వినియోగదారు': 'public class వినియోగదారు { public static native int 실행권한(); }'}, లక్ష్యం='user')
        డేటా = (self.సంచయని_మూల్యం / 'native').read_bytes()
        self.assertEqual(డేటా[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', డేటా, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.సంచయని_మూల్యం / 'native')]))
        # వినియోగదారు ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.నిర్మించు_మూలం('public class 시험 { public static int నడుపుము() { return పరికరం_మూల్యం.포트읽기(1); } }',
                    {'పరికరం_మూల్యం': 'public class పరికరం_మూల్యం { public static native int 포트읽기(int మూల్యం); }'}, 성공=False, లక్ష్యం='user')

    def test_내보내기검증(self):
        వనరు = 'public class 시험 { public static int నడుపుము() { return 0; } static int 호출(int మూల్యం) { return మూల్యం; } }'
        self.నిర్మించు_మూలం(వనరు, లక్ష్యం='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.సంచయని_మూల్యం / 'native')]))
        self.నిర్మించు_మూలం(వనరు, 성공=False, 내보냄='bad;name=시험.호출')
        self.నిర్మించు_మూలం(వనరు, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
