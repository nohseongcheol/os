"""halisi_data ELF tekeleza_amri + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
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
        self.Saraka_thamani = Path(self.임시.name)

    def jenga_chanzo(self, chanzo, 추가=None, 성공=True, lengo='linux', 내보냄=None):
        njia_Orodha = []
        for Jina, maudhui_thamani in dict({'시험': chanzo}, **(추가 or {})).items():
            njia = self.Saraka_thamani / (Jina + '.java')
            njia.write_text(maudhui_thamani, encoding='utf-8')
            njia_Orodha.append(str(njia))
        amri = [sys.executable, str(컴파일러), '--target', lengo, '--entry', '시험.endesha', '-o', str(self.Saraka_thamani / 'native')]
        if 내보냄 is not None: amri += ['--export', 내보냄]
        결과 = subprocess.run(amri + njia_Orodha,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('jenga_chanzo kosa'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.Saraka_thamani / 'native')], timeout=5).returncode

    def 자바대조(self, chanzo, 추가=None):
        self.jenga_chanzo(chanzo, 추가)
        (self.Saraka_thamani / 'mwenyeji.java').write_text(
            'public class mwenyeji { public static void main(String[] 인수) { System.exit(시험.endesha()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.Saraka_thamani)] +
                       [str(njia) for njia in self.Saraka_thamani.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.Saraka_thamani), 'mwenyeji'], timeout=5).returncode
        halisi_data = self.실행결과()
        self.assertGreaterEqual(halisi_data, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 thibitisha)')
        self.assertEqual(halisi_data, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int endesha() {
                int 합 = 7;
                int thamani = 12345;
                for (int kielezo = -65; kielezo <= 65; kielezo++) {
                    thamani = thamani * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(thamani, kielezo);
                    합 += (byte)thamani + (short)thamani + (char)thamani;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] thamani = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int endesha() {
                int 합 = 13;
                for (int 가 = 0; 가 < thamani.length; 가++)
                    for (int 나 = 1; 나 < thamani.length; 나++)
                        합 = 합 * 31 + thamani[가] / thamani[나] + thamani[가] % thamani[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] unda_ingizo(int panga_ukubwa) { return new int[panga_ukubwa]; }
            public static int endesha() {
                int[] 가 = unda_ingizo(8); int[] 나 = 가; int[] tupu_kipengee = new int[0];
                if (가 != 나 || 가 == null || tupu_kipengee.length != 0 || 가[7] != 0) return 99;
                int thamani = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return thamani + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int thamani = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int endesha() { return 계산(1, 2, 3, 4, thamani) + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int thamani = 3;
            static int 초기값() { return ++thamani; }
            static int 읽기() { return thamani; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int thamani = 보조.읽기() + 1;
            public static int endesha() { return thamani * 10 + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int thamani = 시험.thamani + 2;
            static int 읽기() { return thamani; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String SMS = "한글\\u0000😀";
            public static int endesha() {
                if (SMS != "한글\\u0000😀") return 99;
                return (SMS.length() + SMS.charAt(2) + SMS.charAt(3) + SMS.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int namba_kamilifu_2474c4d7(int thamani) { return thamani <= 1 ? 1 : thamani * namba_kamilifu_2474c4d7(thamani - 1); }
            static int 연속(int thamani) {
                switch (thamani) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int thamani) {
                switch (thamani) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int endesha() { return (namba_kamilifu_2474c4d7(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        tamko = '\n'.join('int thamani{} = {};'.format(kielezo, kielezo) for kielezo in range(270))
        덧셈 = '+'.join('thamani{}'.format(kielezo) for kielezo in range(270))
        self.자바대조('public class 시험 { public static int endesha() {' + tamko +
                    'thamani_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] thamani = null; return thamani.length;', 102),
            ('int[] thamani = new int[1]; return thamani[1];', 103),
            ('int[] thamani = new int[1]; thamani[-1] = 3; return 0;', 103),
            ('int thamani = -1; return new int[thamani].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for kiini_thamani, 기대 in 경우들:
            with self.subTest(kiini_thamani=kiini_thamani):
                self.jenga_chanzo('public class 시험 { public static int endesha() { ' + kiini_thamani + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long thamani; public static int endesha() { return 0; }',
            'public static int endesha() { Object thamani = new Object(); return 0; }',
            'public static int endesha() { System.out.println("hello"); return 0; }',
            'public static int endesha() { try { return 1; } catch (Exception kosa) { return 2; } }',
            'public static synchronized int endesha() { return 0; }',
            'public static int endesha() { return new byte[3].length; }',
            'static native int 외부(); public static int endesha() { return 외부(); }',
            'int thamani; public static int endesha() { return 0; }',
        ]
        for kiini_thamani in 경우들:
            with self.subTest(kiini_thamani=kiini_thamani):
                self.jenga_chanzo('public class 시험 { ' + kiini_thamani + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.Saraka_thamani / 'native'
        출력.write_bytes(b'original-output')
        self.jenga_chanzo('public class 시험 { public static int endesha() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.jenga_chanzo('public class 시험 { public static int endesha() { return 37; } }')
        self.assertEqual((self.Saraka_thamani / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.Saraka_thamani / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.jenga_chanzo('public class 시험 { public static int endesha() { return mtumiaji.실행권한(); } }',
                    {'mtumiaji': 'public class mtumiaji { public static native int 실행권한(); }'}, lengo='user')
        data = (self.Saraka_thamani / 'native').read_bytes()
        self.assertEqual(data[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', data, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.Saraka_thamani / 'native')]))
        # mtumiaji ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.jenga_chanzo('public class 시험 { public static int endesha() { return kifaa_thamani.포트읽기(1); } }',
                    {'kifaa_thamani': 'public class kifaa_thamani { public static native int 포트읽기(int thamani); }'}, 성공=False, lengo='user')

    def test_내보내기검증(self):
        chanzo = 'public class 시험 { public static int endesha() { return 0; } static int 호출(int thamani) { return thamani; } }'
        self.jenga_chanzo(chanzo, lengo='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.Saraka_thamani / 'native')]))
        self.jenga_chanzo(chanzo, 성공=False, 내보냄='bad;name=시험.호출')
        self.jenga_chanzo(chanzo, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
