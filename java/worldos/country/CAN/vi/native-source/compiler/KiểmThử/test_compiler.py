"""dữLiệuThựcTế ELF thựcThiLệnh + OpenJDK kếtQuả 대조. giáTrịTạm KiểmThử 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TrìnhBiênDịch = Path(__file__).resolve().parents[1] / 'TrìnhBiênDịch.py'


class thửBảnĐịa(unittest.TestCase):
    def setUp(self):
        self.giáTrịTạm = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.giáTrịTạm.cleanup)
        self.giáTrịThưMục = Path(self.giáTrịTạm.name)

    def biênDịchNguồn(self, mãNguồn, thêmCuốiMục=None, giáTrịThànhCông=True, giáTrịĐốiĐích='linux', giáTrịĐãXuất=None):
        danhSáchĐườngDẫn = []
        for tên, giáTrịNộiDung in dict({'KiểmThử': mãNguồn}, **(thêmCuốiMục or {})).items():
            đườngDẫn = self.giáTrịThưMục / (tên + '.java')
            đườngDẫn.write_text(giáTrịNộiDung, encoding='utf-8')
            danhSáchĐườngDẫn.append(str(đườngDẫn))
        lệnh = [sys.executable, str(TrìnhBiênDịch), '--target', giáTrịĐốiĐích, '--entry', 'KiểmThử.chạy', '-o', str(self.giáTrịThưMục / 'native')]
        if giáTrịĐãXuất is not None: lệnh += ['--export', giáTrịĐãXuất]
        kếtQuả = subprocess.run(lệnh + danhSáchĐườngDẫn,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if giáTrịThànhCông:
            self.assertEqual(kếtQuả.returncode, 0, kếtQuả.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(kếtQuả.returncode, 0)
            self.assertIn('biênDịchNguồn lỗi'.encode(), kếtQuả.stderr)
        return kếtQuả

    def kếtQuảViệcThựcThi(self):
        return subprocess.run([str(self.giáTrịThưMục / 'native')], timeout=5).returncode

    def phépSoSánhJava(self, mãNguồn, thêmCuốiMục=None):
        self.biênDịchNguồn(mãNguồn, thêmCuốiMục)
        (self.giáTrịThưMục / 'Chủ.java').write_text(
            'public class Chủ { public static void main(String[] cácĐốiSố) { System.exit(KiểmThử.chạy()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.giáTrịThưMục)] +
                       [str(đườngDẫn) for đườngDẫn in self.giáTrịThưMục.glob('*.java')], check=True, timeout=30)
        kỳVọng = subprocess.run(['java', '-cp', str(self.giáTrịThưMục), 'Chủ'], timeout=5).returncode
        dữLiệuThựcTế = self.kếtQuảViệcThựcThi()
        self.assertGreaterEqual(dữLiệuThựcTế, 0, '신호로 cóĐãRa (샌드박스의 32비트 syscall giáTrịGiớiHạn 여부 xácMinh)')
        self.assertEqual(dữLiệuThựcTế, kỳVọng)

    def thửCácPhépDịchVàSốHọcSốNguyên(self):
        self.phépSoSánhJava('''public class KiểmThử {
            static int sốHọcTrộn(int toánHạngĐầuTiên, int toánHạngThứHai) {
                return ((toánHạngĐầuTiên + toánHạngThứHai) ^ (toánHạngĐầuTiên - toánHạngThứHai) ^ (toánHạngĐầuTiên * toánHạngThứHai) ^ (toánHạngĐầuTiên & toánHạngThứHai) ^ (toánHạngĐầuTiên | toánHạngThứHai))
                    + (toánHạngĐầuTiên << toánHạngThứHai) + (toánHạngĐầuTiên >> toánHạngThứHai) + (toánHạngĐầuTiên >>> toánHạngThứHai);
            }
            public static int chạy() {
                int giáTrịTổng = 7;
                int giáTrị = 12345;
                for (int sốHiệu = -65; sốHiệu <= 65; sốHiệu++) {
                    giáTrị = giáTrị * 1664525 + 1013904223;
                    giáTrịTổng = giáTrịTổng * 31 + sốHọcTrộn(giáTrị, sốHiệu);
                    giáTrịTổng += (byte)giáTrị + (short)giáTrị + (char)giáTrị;
                }
                return (giáTrịTổng & 0x7fffffff) % 251;
            }
        }''')

    def thửCácGiáTrịCựcTrịPhépChia(self):
        self.phépSoSánhJava('''public class KiểmThử {
            static int[] giáTrị = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int chạy() {
                int giáTrịTổng = 13;
                for (int toánHạngĐầuTiên = 0; toánHạngĐầuTiên < giáTrị.length; toánHạngĐầuTiên++)
                    for (int toánHạngThứHai = 1; toánHạngThứHai < giáTrị.length; toánHạngThứHai++)
                        giáTrịTổng = giáTrịTổng * 31 + giáTrị[toánHạngĐầuTiên] / giáTrị[toánHạngThứHai] + giáTrị[toánHạngĐầuTiên] % giáTrị[toánHạngThứHai];
                return (giáTrịTổng & 0x7fffffff) % 251;
            }
        }''')

    def thửCácThamChiếuVàCácMảng(self):
        self.phépSoSánhJava('''public class KiểmThử {
            static int[] tạoMục(int cỡ) { return new int[cỡ]; }
            public static int chạy() {
                int[] toánHạngĐầuTiên = tạoMục(8); int[] toánHạngThứHai = toánHạngĐầuTiên; int[] đốiTượngRỗng = new int[0];
                if (toánHạngĐầuTiên != toánHạngThứHai || toánHạngĐầuTiên == null || đốiTượngRỗng.length != 0 || toánHạngĐầuTiên[7] != 0) return 99;
                int giáTrị = (toánHạngĐầuTiên[2] = 40); toánHạngĐầuTiên[2]++; ++toánHạngĐầuTiên[3]; toánHạngĐầuTiên[2] += 7;
                return giáTrị + toánHạngThứHai[2] + toánHạngThứHai[3];
            }
        }''')

    def thửThứTựĐốiSốVàCácTrườngTĩnh(self):
        self.phépSoSánhJava('''public class KiểmThử {
            static int giáTrị = giáTrịPhụTrợ.giáTrịBanĐầu();
            static int phépTính(int toánHạngĐầuTiên, int toánHạngThứHai, int toánHạngThứBa, int toánHạngThứTư, int toánHạngThứNăm) {
                return toánHạngĐầuTiên + toánHạngThứHai * 2 + toánHạngThứBa * 3 + toánHạngThứTư * 4 + toánHạngThứNăm * 5;
            }
            public static int chạy() { return phépTính(1, 2, 3, 4, giáTrị) + giáTrịPhụTrợ.đọc(); }
        }''', {'giáTrịPhụTrợ': '''public class giáTrịPhụTrợ {
            static int giáTrị = 3;
            static int giáTrịBanĐầu() { return ++giáTrị; }
            static int đọc() { return giáTrị; }
        }'''})

    def thửChuKỳViệcKhởiTạo(self):
        self.phépSoSánhJava('''public class KiểmThử {
            static int giáTrị = giáTrịPhụTrợ.đọc() + 1;
            public static int chạy() { return giáTrị * 10 + giáTrịPhụTrợ.đọc(); }
        }''', {'giáTrịPhụTrợ': '''public class giáTrịPhụTrợ {
            static int giáTrị = KiểmThử.giáTrị + 2;
            static int đọc() { return giáTrị; }
        }'''})

    def thửCácChuỗi8UTFĐãChỉnhSửa(self):
        self.phépSoSánhJava('''public class KiểmThử {
            static String vănBản = "한글\\u0000😀";
            public static int chạy() {
                if (vănBản != "한글\\u0000😀") return 99;
                return (vănBản.length() + vănBản.charAt(2) + vănBản.charAt(3) + vănBản.charAt(4)) % 251;
            }
        }''')

    def thửĐệQuyVàChuyển(self):
        self.phépSoSánhJava('''public class KiểmThử {
            static int giaiThừa(int giáTrị) { return giáTrị <= 1 ? 1 : giáTrị * giaiThừa(giáTrị - 1); }
            static int cácTrườngHợpChuyểnDày(int giáTrị) {
                switch (giáTrị) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int cácTrườngHợpChuyểnThưa(int giáTrị) {
                switch (giáTrị) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int chạy() { return (giaiThừa(5) + cácTrườngHợpChuyểnDày(0) + cácTrườngHợpChuyểnDày(2) + cácTrườngHợpChuyểnDày(9) + cácTrườngHợpChuyểnThưa(-1000) + cácTrườngHợpChuyểnThưa(0)) % 251; }
        }''')

    def thửCácBiếnCụcBộRộngKiểu(self):
        KhaiBáo = '\n'.join('int giáTrị{} = {};'.format(sốHiệu, sốHiệu) for sốHiệu in range(270))
        kếtQuảPhépCộng = '+'.join('giáTrị{}'.format(sốHiệu) for sốHiệu in range(270))
        self.phépSoSánhJava('public class KiểmThử { public static int chạy() {' + KhaiBáo +
                    'giáTrị269 += 300; return (' + kếtQuảPhépCộng + ') % 251; } }')

    def thửCácSốLỗiMôiTrườngChạy(self):
        cácMụcTrườngHợp = [
            ('int toánHạngKhôngSố = 0; return 1 / toánHạngKhôngSố;', 101),
            ('int[] giáTrị = null; return giáTrị.length;', 102),
            ('int[] giáTrị = new int[1]; return giáTrị[1];', 103),
            ('int[] giáTrị = new int[1]; giáTrị[-1] = 3; return 0;', 103),
            ('int giáTrị = -1; return new int[giáTrị].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] toánHạngĐầuTiên = new int[65535]; return new int[1].length;', 105),
        ]
        for giáTrịThân, kỳVọng in cácMụcTrườngHợp:
            with self.subTest(giáTrịThân=giáTrịThân):
                self.biênDịchNguồn('public class KiểmThử { public static int chạy() { ' + giáTrịThân + ' } }')
                self.assertEqual(self.kếtQuảViệcThựcThi(), kỳVọng)

    def thửĐãTừChốiTínhNăngKhôngHỗTrợ(self):
        cácMụcTrườngHợp = [
            'static long giáTrị; public static int chạy() { return 0; }',
            'public static int chạy() { Object giáTrị = new Object(); return 0; }',
            'public static int chạy() { System.out.println("hello"); return 0; }',
            'public static int chạy() { try { return 1; } catch (Exception lỗi) { return 2; } }',
            'public static synchronized int chạy() { return 0; }',
            'public static int chạy() { return new byte[3].length; }',
            'static native int giáTrịBênNgoài(); public static int chạy() { return giáTrịBênNgoài(); }',
            'int giáTrị; public static int chạy() { return 0; }',
        ]
        for giáTrịThân in cácMụcTrườngHợp:
            with self.subTest(giáTrịThân=giáTrịThân):
                self.biênDịchNguồn('public class KiểmThử { ' + giáTrịThân + ' }', giáTrịThànhCông=False)

    def thửSựThấtBạiBậtTrạngTháiĐãGiữNguyênĐầuRaHiệnCó(self):
        ĐầuRa = self.giáTrịThưMục / 'native'
        ĐầuRa.write_bytes(b'original-output')
        self.biênDịchNguồn('public class KiểmThử { public static int chạy() { return missing; } }', giáTrịThànhCông=False)
        self.assertEqual(ĐầuRa.read_bytes(), b'original-output')

    def thửViệcThựcThiĐộcLậpVàELF(self):
        self.biênDịchNguồn('public class KiểmThử { public static int chạy() { return 37; } }')
        self.assertEqual((self.giáTrịThưMục / 'native').read_bytes()[:5], b'\x7fELF\x01')
        Bảng = subprocess.check_output(['readelf', '-l', str(self.giáTrịThưMục / 'native')])
        self.assertNotIn(b'INTERP', Bảng)
        self.assertEqual(self.kếtQuảViệcThựcThi(), 37)

    def thửViệcTáchABIVàELFNgườiDùng(self):
        self.biênDịchNguồn('public class KiểmThử { public static int chạy() { return NgườiDùng.quyềnViệcThựcThi(); } }',
                    {'NgườiDùng': 'public class NgườiDùng { public static native int quyềnViệcThựcThi(); }'}, giáTrịĐốiĐích='user')
        DữLiệu = (self.giáTrịThưMục / 'native').read_bytes()
        self.assertEqual(DữLiệu[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', DữLiệu, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.giáTrịThưMục / 'native')]))
        # NgườiDùng ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.biênDịchNguồn('public class KiểmThử { public static int chạy() { return ThiếtBị.đọcCổngPhầnCứng(1); } }',
                    {'ThiếtBị': 'public class ThiếtBị { public static native int đọcCổngPhầnCứng(int giáTrị); }'}, giáTrịThànhCông=False, giáTrịĐốiĐích='user')

    def thửViệcThẩmĐịnhXuất(self):
        mãNguồn = 'public class KiểmThử { public static int chạy() { return 0; } static int gọiThựcHiện(int giáTrị) { return giáTrị; } }'
        self.biênDịchNguồn(mãNguồn, giáTrịĐốiĐích='kernel', giáTrịĐãXuất='kernel_dispatch=KiểmThử.gọiThựcHiện')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.giáTrịThưMục / 'native')]))
        self.biênDịchNguồn(mãNguồn, giáTrịThànhCông=False, giáTrịĐãXuất='bad;name=KiểmThử.gọiThựcHiện')
        self.biênDịchNguồn(mãNguồn, giáTrịThànhCông=False, giáTrịĐãXuất='missing=KiểmThử.phươngThứcThiếu')


if __name__ == '__main__':
    unittest.main()
