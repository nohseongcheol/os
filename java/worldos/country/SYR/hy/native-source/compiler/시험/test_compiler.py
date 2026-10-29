"""իրական_տվյալ ELF կատարել_հրաման + OpenJDK չափ 대조. 임시 시험 자료만 생성한다."""
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
        self.գրացուցակ_արժեք = Path(self.임시.name)

    def կառուցել_աղբյուր(self, ԱՂԲՅՈՒՐ, 추가=None, 성공=True, թիրախ='linux', 내보냄=None):
        ուղի_Ցուցակ = []
        for Անուն, Բովանդակություն_արժեք in dict({'시험': ԱՂԲՅՈՒՐ}, **(추가 or {})).items():
            Ճանապարհ = self.գրացուցակ_արժեք / (Անուն + '.java')
            Ճանապարհ.write_text(Բովանդակություն_արժեք, encoding='utf-8')
            ուղի_Ցուցակ.append(str(Ճանապարհ))
        Հրահանգ = [sys.executable, str(컴파일러), '--target', թիրախ, '--entry', '시험.Գործարկել', '-o', str(self.գրացուցակ_արժեք / 'native')]
        if 내보냄 is not None: Հրահանգ += ['--export', 내보냄]
        չափ = subprocess.run(Հրահանգ + ուղի_Ցուցակ,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(չափ.returncode, 0, չափ.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(չափ.returncode, 0)
            self.assertIn('կառուցել_աղբյուր Սխալ'.encode(), չափ.stderr)
        return չափ

    def 실행결과(self):
        return subprocess.run([str(self.գրացուցակ_արժեք / 'native')], timeout=5).returncode

    def 자바대조(self, ԱՂԲՅՈՒՐ, 추가=None):
        self.կառուցել_աղբյուր(ԱՂԲՅՈՒՐ, 추가)
        (self.գրացուցակ_արժեք / 'հոստ.java').write_text(
            'public class հոստ { public static void main(String[] 인수) { System.exit(시험.Գործարկել()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.գրացուցակ_արժեք)] +
                       [str(Ճանապարհ) for Ճանապարհ in self.գրացուցակ_արժեք.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.գրացուցակ_արժեք), 'հոստ'], timeout=5).returncode
        իրական_տվյալ = self.실행결과()
        self.assertGreaterEqual(իրական_տվյալ, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 հաստատել)')
        self.assertEqual(իրական_տվյալ, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int Գործարկել() {
                int 합 = 7;
                int արժեք = 12345;
                for (int դասիչ = -65; դասիչ <= 65; դասիչ++) {
                    արժեք = արժեք * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(արժեք, դասիչ);
                    합 += (byte)արժեք + (short)արժեք + (char)արժեք;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] արժեք = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int Գործարկել() {
                int 합 = 13;
                for (int 가 = 0; 가 < արժեք.length; 가++)
                    for (int 나 = 1; 나 < արժեք.length; 나++)
                        합 = 합 * 31 + արժեք[가] / արժեք[나] + արժեք[가] % արժեք[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] Կերտի_ր_մուտքագրում(int Չափս) { return new int[Չափս]; }
            public static int Գործարկել() {
                int[] 가 = Կերտի_ր_մուտքագրում(8); int[] 나 = 가; int[] դատարկ_առարկա = new int[0];
                if (가 != 나 || 가 == null || դատարկ_առարկա.length != 0 || 가[7] != 0) return 99;
                int արժեք = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return արժեք + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int արժեք = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int Գործարկել() { return 계산(1, 2, 3, 4, արժեք) + 보조.Ընթերցում(); }
        }''', {'보조': '''public class 보조 {
            static int արժեք = 3;
            static int 초기값() { return ++արժեք; }
            static int Ընթերցում() { return արժեք; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int արժեք = 보조.Ընթերցում() + 1;
            public static int Գործարկել() { return արժեք * 10 + 보조.Ընթերցում(); }
        }''', {'보조': '''public class 보조 {
            static int արժեք = 시험.արժեք + 2;
            static int Ընթերցում() { return արժեք; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Տեքստ = "한글\\u0000😀";
            public static int Գործարկել() {
                if (Տեքստ != "한글\\u0000😀") return 99;
                return (Տեքստ.length() + Տեքստ.charAt(2) + Տեքստ.charAt(3) + Տեքստ.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ֆակտորիալ(int արժեք) { return արժեք <= 1 ? 1 : արժեք * ֆակտորիալ(արժեք - 1); }
            static int 연속(int արժեք) {
                switch (արժեք) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int արժեք) {
                switch (արժեք) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int Գործարկել() { return (ֆակտորիալ(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int արժեք{} = {};'.format(դասիչ, դասիչ) for դասիչ in range(270))
        덧셈 = '+'.join('արժեք{}'.format(դասիչ) for դասիչ in range(270))
        self.자바대조('public class 시험 { public static int Գործարկել() {' + 선언 +
                    'արժեք_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] արժեք = null; return արժեք.length;', 102),
            ('int[] արժեք = new int[1]; return արժեք[1];', 103),
            ('int[] արժեք = new int[1]; արժեք[-1] = 3; return 0;', 103),
            ('int արժեք = -1; return new int[արժեք].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.կառուցել_աղբյուր('public class 시험 { public static int Գործարկել() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long արժեք; public static int Գործարկել() { return 0; }',
            'public static int Գործարկել() { Object արժեք = new Object(); return 0; }',
            'public static int Գործարկել() { System.out.println("hello"); return 0; }',
            'public static int Գործարկել() { try { return 1; } catch (Exception Սխալ) { return 2; } }',
            'public static synchronized int Գործարկել() { return 0; }',
            'public static int Գործարկել() { return new byte[3].length; }',
            'static native int 외부(); public static int Գործարկել() { return 외부(); }',
            'int արժեք; public static int Գործարկել() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.կառուցել_աղբյուր('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        Ելք = self.գրացուցակ_արժեք / 'native'
        Ելք.write_bytes(b'original-output')
        self.կառուցել_աղբյուր('public class 시험 { public static int Գործարկել() { return missing; } }', 성공=False)
        self.assertEqual(Ելք.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.կառուցել_աղբյուր('public class 시험 { public static int Գործարկել() { return 37; } }')
        self.assertEqual((self.գրացուցակ_արժեք / 'native').read_bytes()[:5], b'\x7fELF\x01')
        Փնտրում_աղյուսակ = subprocess.check_output(['readelf', '-l', str(self.գրացուցակ_արժեք / 'native')])
        self.assertNotIn(b'INTERP', Փնտրում_աղյուսակ)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.կառուցել_աղբյուր('public class 시험 { public static int Գործարկել() { return օգտվող.실행권한(); } }',
                    {'օգտվող': 'public class օգտվող { public static native int 실행권한(); }'}, թիրախ='user')
        տվյալ = (self.գրացուցակ_արժեք / 'native').read_bytes()
        self.assertEqual(տվյալ[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', տվյալ, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.գրացուցակ_արժեք / 'native')]))
        # օգտվող ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.կառուցել_աղբյուր('public class 시험 { public static int Գործարկել() { return սարք_արժեք.포트읽기(1); } }',
                    {'սարք_արժեք': 'public class սարք_արժեք { public static native int 포트읽기(int արժեք); }'}, 성공=False, թիրախ='user')

    def test_내보내기검증(self):
        ԱՂԲՅՈՒՐ = 'public class 시험 { public static int Գործարկել() { return 0; } static int 호출(int արժեք) { return արժեք; } }'
        self.կառուցել_աղբյուր(ԱՂԲՅՈՒՐ, թիրախ='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.գրացուցակ_արժեք / 'native')]))
        self.կառուցել_աղբյուր(ԱՂԲՅՈՒՐ, 성공=False, 내보냄='bad;name=시험.호출')
        self.կառուցել_աղբյուր(ԱՂԲՅՈՒՐ, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
