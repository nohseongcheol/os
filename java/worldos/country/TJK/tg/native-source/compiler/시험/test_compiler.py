"""воқеӣ_иттилоот ELF иҷро_кардан_фармон + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.директория_қимат = Path(self.임시.name)

    def сохтан_манбаъ(self, манбаъ, 추가=None, 성공=True, ҳадаф='linux', 내보냄=None):
        масир_Рӯйхат = []
        for Ном, Мӯҳтаво_қимат in dict({'시험': манбаъ}, **(추가 or {})).items():
            масир = self.директория_қимат / (Ном + '.java')
            масир.write_text(Мӯҳтаво_қимат, encoding='utf-8')
            масир_Рӯйхат.append(str(масир))
        фармон = [sys.executable, str(컴파일러), '--target', ҳадаф, '--entry', '시험.порча', '-o', str(self.директория_қимат / 'native')]
        if 내보냄 is not None: фармон += ['--export', 내보냄]
        결과 = subprocess.run(фармон + масир_Рӯйхат,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('сохтан_манбаъ Хато'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.директория_қимат / 'native')], timeout=5).returncode

    def 자바대조(self, манбаъ, 추가=None):
        self.сохтан_манбаъ(манбаъ, 추가)
        (self.директория_қимат / 'мизбон.java').write_text(
            'public class мизбон { public static void main(String[] 인수) { System.exit(시험.порча()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.директория_қимат)] +
                       [str(масир) for масир in self.директория_қимат.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.директория_қимат), 'мизбон'], timeout=5).returncode
        воқеӣ_иттилоот = self.실행결과()
        self.assertGreaterEqual(воқеӣ_иттилоот, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 тасдиқ_кардан)')
        self.assertEqual(воқеӣ_иттилоот, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int порча() {
                int 합 = 7;
                int қимат = 12345;
                for (int индекс = -65; индекс <= 65; индекс++) {
                    қимат = қимат * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(қимат, индекс);
                    합 += (byte)қимат + (short)қимат + (char)қимат;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] қимат = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int порча() {
                int 합 = 13;
                for (int 가 = 0; 가 < қимат.length; 가++)
                    for (int 나 = 1; 나 < қимат.length; 나++)
                        합 = 합 * 31 + қимат[가] / қимат[나] + қимат[가] % қимат[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] эҷод_кардан_ворида(int андоза_кардан) { return new int[андоза_кардан]; }
            public static int порча() {
                int[] 가 = эҷод_кардан_ворида(8); int[] 나 = 가; int[] холӣ_объект = new int[0];
                if (가 != 나 || 가 == null || холӣ_объект.length != 0 || 가[7] != 0) return 99;
                int қимат = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return қимат + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int қимат = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int порча() { return 계산(1, 2, 3, 4, қимат) + 보조.Хондан(); }
        }''', {'보조': '''public class 보조 {
            static int қимат = 3;
            static int 초기값() { return ++қимат; }
            static int Хондан() { return қимат; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int қимат = 보조.Хондан() + 1;
            public static int порча() { return қимат * 10 + 보조.Хондан(); }
        }''', {'보조': '''public class 보조 {
            static int қимат = 시험.қимат + 2;
            static int Хондан() { return қимат; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Матн = "한글\\u0000😀";
            public static int порча() {
                if (Матн != "한글\\u0000😀") return 99;
                return (Матн.length() + Матн.charAt(2) + Матн.charAt(3) + Матн.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int факториал(int қимат) { return қимат <= 1 ? 1 : қимат * факториал(қимат - 1); }
            static int 연속(int қимат) {
                switch (қимат) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int қимат) {
                switch (қимат) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int порча() { return (факториал(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int қимат{} = {};'.format(индекс, индекс) for индекс in range(270))
        덧셈 = '+'.join('қимат{}'.format(индекс) for индекс in range(270))
        self.자바대조('public class 시험 { public static int порча() {' + 선언 +
                    'қимат_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] қимат = null; return қимат.length;', 102),
            ('int[] қимат = new int[1]; return қимат[1];', 103),
            ('int[] қимат = new int[1]; қимат[-1] = 3; return 0;', 103),
            ('int қимат = -1; return new int[қимат].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.сохтан_манбаъ('public class 시험 { public static int порча() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long қимат; public static int порча() { return 0; }',
            'public static int порча() { Object қимат = new Object(); return 0; }',
            'public static int порча() { System.out.println("hello"); return 0; }',
            'public static int порча() { try { return 1; } catch (Exception Хато) { return 2; } }',
            'public static synchronized int порча() { return 0; }',
            'public static int порча() { return new byte[3].length; }',
            'static native int 외부(); public static int порча() { return 외부(); }',
            'int қимат; public static int порча() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.сохтан_манбаъ('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.директория_қимат / 'native'
        출력.write_bytes(b'original-output')
        self.сохтан_манбаъ('public class 시험 { public static int порча() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.сохтан_манбаъ('public class 시험 { public static int порча() { return 37; } }')
        self.assertEqual((self.директория_қимат / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.директория_қимат / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.сохтан_манбаъ('public class 시험 { public static int порча() { return корбар.실행권한(); } }',
                    {'корбар': 'public class корбар { public static native int 실행권한(); }'}, ҳадаф='user')
        иттилоот = (self.директория_қимат / 'native').read_bytes()
        self.assertEqual(иттилоот[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', иттилоот, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.директория_қимат / 'native')]))
        # корбар ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.сохтан_манбаъ('public class 시험 { public static int порча() { return мобилӣ_қимат.포트읽기(1); } }',
                    {'мобилӣ_қимат': 'public class мобилӣ_қимат { public static native int 포트읽기(int қимат); }'}, 성공=False, ҳадаф='user')

    def test_내보내기검증(self):
        манбаъ = 'public class 시험 { public static int порча() { return 0; } static int 호출(int қимат) { return қимат; } }'
        self.сохтан_манбаъ(манбаъ, ҳадаф='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.директория_қимат / 'native')]))
        self.сохтан_манбаъ(манбаъ, 성공=False, 내보냄='bad;name=시험.호출')
        self.сохтан_манбаъ(манбаъ, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
