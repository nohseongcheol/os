"""독립된 tựThân ABI ELF64와 로더 từChốiGiáTrị KiểmThử 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from xâyDựngPython import tạoPython
from xâyDựngThưViệnJava import tạoThưViệnJava
from xâyDựngTrìnhBiênDịchC import tạoTrìnhBiênDịchC


def tạoKhôngGianNgườiDùng(đườngDẫnGốcCây, đườngDẫnKhoNguồn, TrìnhBiênDịchC, trìnhBiênDịchCộngCộng, côngCụTrìnhLiênKết, côngCụKhoLưuTrữ, cácBitCấuHình, thựcThiLệnh):
    cácBitCấuHình = [giáTrịCácThiếtLập for giáTrịCácThiếtLập in cácBitCấuHình if giáTrịCácThiếtLập != '-mgeneral-regs-only']
    xâyDựngĐườngDẫn = đườngDẫnGốcCây / 'build'
    đầuRa = xâyDựngĐườngDẫn / 'user'
    đầuRa.mkdir(exist_ok=True)
    dữLiệuNguyênBản = đườngDẫnGốcCây / 'NgườiDùng'
    pOSIX = đườngDẫnKhoNguồn / 'posix-kor/arm64-native'
    đườngDẫnBaoGồm = ['-I', dữLiệuNguyênBản, '-I', pOSIX / 'TệpĐầuMục', '-I', đầuRa]
    for côngCụTrìnhBiênDịch, miềnBổSung, đườngDẫn, tên in [
            (TrìnhBiênDịchC, [], dữLiệuNguyênBản / 'chạy.S', 'start.o'),
            (TrìnhBiênDịchC, ['-std=c11'], dữLiệuNguyênBản / 'thựcThiLệnh.c', 'runtime.o'),
            (TrìnhBiênDịchC, ['-std=c11'], pOSIX / 'cầuNốiNgườiDùng.c', 'posix.o'),
            (trìnhBiênDịchCộngCộng, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], dữLiệuNguyênBản / 'VíDụTệp.cpp', 'demo.o'),
            (trìnhBiênDịchCộngCộng, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], dữLiệuNguyênBản / 'VíDụTruyềnThông.cpp', 'network.o'),
            (TrìnhBiênDịchC, ['-std=c11'], dữLiệuNguyênBản / 'ThửSựBảoVệ.c', 'fault.o'),
            (TrìnhBiênDịchC, ['-std=c11'], dữLiệuNguyênBản / 'TrìnhSoạnThảo.c', 'vi.o')]:
        thựcThiLệnh([côngCụTrìnhBiênDịch] + cácBitCấuHình + miềnBổSung + đườngDẫnBaoGồm + ['-Wall', '-Wextra', '-Werror', '-c', đườngDẫn, '-o', đầuRa / tên])
    thựcThiLệnh([côngCụKhoLưuTrữ, 'rcs', xâyDựngĐườngDẫn / 'libposix-kor-user.a', đầuRa / 'posix.o'])
    for tên in ('demo', 'fault', 'network', 'vi'):
        thựcThiLệnh([côngCụTrìnhLiênKết, '-T', dữLiệuNguyênBản / 'BốTríLiênKết.ld', '-z', 'max-page-size=4096', '-o', đầuRa / (tên + '.elf'),
             đầuRa / 'start.o', đầuRa / 'runtime.o', đầuRa / (tên + '.o'), xâyDựngĐườngDẫn / 'libposix-kor-user.a'])
    tạoThưViệnJava(đườngDẫnGốcCây, thựcThiLệnh)
    # 기존 tựThân Java TrìnhBiênDịch/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(xâyDựngĐườngDẫn)) as đườngDẫnĐangLàmViệc:
        đườngDẫnLớp = Path(đườngDẫnĐangLàmViệc)
        thựcThiLệnh(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', đườngDẫnLớp, '-sourcepath', đườngDẫnLớp, '-d', đườngDẫnLớp] +
            [vịTríDữLiệu for vịTríDữLiệu in sorted((đườngDẫnKhoNguồn / 'os/NgườiDùng/Java').glob('*.java')) if vịTríDữLiệu.name != 'MáyẢoJava.java'] + sorted((dữLiệuNguyênBản / 'Java').glob('*.java')))
        thựcThiLệnh(['sh', đườngDẫnKhoNguồn / 'compiler/thờiGianCủaTrước.sh', '--entry', 'MụcCôngCụ.chạy',
             '--profile', 'user', '--heap-words', '1048576', '-o', đầuRa / 'java-tools.c'] + sorted(đườngDẫnLớp.glob('*.class')))
    uzlib = đườngDẫnGốcCây / 'vendor/uzlib'
    for đườngDẫn, tên in [(đầuRa / 'java-tools.c', 'java-tools.o'), (dữLiệuNguyênBản / 'cầuNốiJava.c', 'java-link.o'),
                       (dữLiệuNguyênBản / 'GóiGộp.c', 'jar.o')] + [(uzlib / (tên + '.c'), tên + '.o') for tên in ('tinflate', 'crc32', 'adler32')]:
        thựcThiLệnh([TrìnhBiênDịchC] + cácBitCấuHình + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', uzlib] + đườngDẫnBaoGồm + ['-c', đườngDẫn, '-o', đầuRa / tên])
    thựcThiLệnh([côngCụTrìnhLiênKết, '-T', dữLiệuNguyênBản / 'BốTríLiênKết.ld', '-z', 'max-page-size=4096', '-o', đầuRa / 'java-tools.elf'] +
        [đầuRa / tên for tên in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    tạoPython(đườngDẫnGốcCây, TrìnhBiênDịchC, côngCụTrìnhLiênKết)
    tạoTrìnhBiênDịchC(đườngDẫnGốcCây, đườngDẫnKhoNguồn, TrìnhBiênDịchC, côngCụTrìnhLiênKết, cácBitCấuHình, thựcThiLệnh)
    hợpLệ = (đầuRa / 'demo.elf').read_bytes()
    độLệchĐầuMụcChươngTrình = struct.unpack_from('<Q', hợpLệ, 32)[0]
    danhSáchĐầuMục = [độLệchĐầuMụcChươngTrình + sốLượngPhầnMục * 56 for sốLượngPhầnMục in range(struct.unpack_from('<H', hợpLệ, 56)[0])]
    cácLầnNạp = [vịTríDữLiệu for vịTríDữLiệu in danhSáchĐầuMục if struct.unpack_from('<I', hợpLệ, vịTríDữLiệu)[0] == 1]
    vănBản, DữLiệu = cácLầnNạp[:2]
    địaChỉLệnh = struct.unpack_from('<Q', hợpLệ, vănBản + 16)[0]
    địaChỉDữLiệu = struct.unpack_from('<Q', hợpLệ, DữLiệu + 16)[0]
    ABIGọi = hợpLệ.index(b'JKOROS\0')
    thửTrườngHợp = [('empty', b''), ('short', hợpLệ[:63])]
    cácChỉnhSửa = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', địaChỉLệnh + 1), ('data-entry', 24, 'Q', địaChỉDữLiệu),
               ('outside-file', vănBản + 32, 'Q', len(hợpLệ) + 1), ('short-memory', vănBản + 40, 'Q', 1),
               ('kernel-address', vănBản + 16, 'Q', 0x80000), ('memory-overflow', vănBản + 40, 'Q', 2**64 - 1),
               ('writable-code', vănBản + 4, 'I', 7), ('missing-abi', ABIGọi, 'B', ord('X')),
               ('wrong-abi', ABIGọi + 8, 'I', 2), ('dynamic', vănBản, 'I', 2),
               ('unaligned-load', vănBản + 16, 'Q', địaChỉLệnh + 8),
               ('overlap', DữLiệu + 16, 'Q', địaChỉLệnh)]
    for tên, giáTrịĐộLệch, địnhDạngDữLiệu, giáTrị in cácChỉnhSửa:
        đãĐổi = bytearray(hợpLệ); struct.pack_into('<' + địnhDạngDữLiệu, đãĐổi, giáTrịĐộLệch, giáTrị)
        thửTrườngHợp.append((tên, bytes(đãĐổi)))
    cácKhốiNhịPhân = [(tên.replace('-', '_'), đầuRa / (tên + '.elf')) for tên in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for chỉSốTraCứu, (tên, dữLiệuNộiTải) in enumerate(thửTrườngHợp):
        đườngDẫn = đầuRa / ('invalid-{}.elf'.format(tên)); đườngDẫn.write_bytes(dữLiệuNộiTải)
        cácKhốiNhịPhân.append(('invalid_{}'.format(chỉSốTraCứu), đườngDẫn))
    hợpNgữ, giáTrịĐầuMục = ['.section .rodata.user,"a"'], []
    cácCỡ = {}
    for tên, đườngDẫn in cácKhốiNhịPhân:
        giáTrịKýHiệu = 'user_blob_' + tên
        cácCỡ[tên] = đườngDẫn.stat().st_size
        # 생성한 giáTrịĐốiTác 경로만 넣어 프로젝트 경로의 공백/dấuTrích 영향을 피한다.
        hợpNgữ += ['.balign 16', '.global ' + giáTrịKýHiệu, giáTrịKýHiệu + ':', '.incbin "{}"'.format(đườngDẫn.relative_to(đườngDẫnGốcCây))]
        giáTrịĐầuMục.append('extern const unsigned char {}[];'.format(giáTrịKýHiệu))
    hợpNgữ.append('.section .note.GNU-stack,"",%progbits')
    giáTrịĐầuMục += ['static const chươngTrình cácMụcTệpThựcThi[] = {', '{user_blob_demo, %d, 0},' % cácCỡ['demo']]
    giáTrịĐầuMục += ['{user_blob_fault, %d, %d},' % (cácCỡ['fault'], giáTrịĐãChuyểnTiếp) for giáTrịĐãChuyểnTiếp in range(8)]
    giáTrịĐầuMục += ['{user_blob_network, %d, 0},' % cácCỡ['network']]
    giáTrịĐầuMục += ['{user_blob_java_tools, %d, %d},' % (cácCỡ['java_tools'], chếĐộPhươngThức) for chếĐộPhươngThức in (0, 1)]
    giáTrịĐầuMục += ['{user_blob_python, %d, 0},' % cácCỡ['python'], '{user_blob_vi, %d, 0},' % cácCỡ['vi']]
    giáTrịĐầuMục += ['{user_blob_java_tools, %d, 2},' % cácCỡ['java_tools']]
    giáTrịĐầuMục += ['{user_blob_cc, %d, 0},' % cácCỡ['cc']]
    giáTrịĐầuMục += ['{user_blob_cc, %d, 1},' % cácCỡ['cc']]
    giáTrịĐầuMục += ['};', 'static const chươngTrình cácTệpThựcThiKhôngHợpLệ[] = {']
    giáTrịĐầuMục += ['{user_blob_invalid_%d, %d, 0},' % (chỉSốThứBậc, len(dữLiệuNộiTải)) for chỉSốThứBậc, (_, dữLiệuNộiTải) in enumerate(thửTrườngHợp)]
    giáTrịĐầuMục += ['};']
    (xâyDựngĐườngDẫn / 'programs.S').write_text('\n'.join(hợpNgữ) + '\n')
    (xâyDựngĐườngDẫn / 'programs.h').write_text('\n'.join(giáTrịĐầuMục) + '\n')
    (đầuRa / 'invalid-cases.txt').write_text('\n'.join(tên for tên, _ in thửTrườngHợp) + '\n')
    thựcThiLệnh([TrìnhBiênDịchC] + cácBitCấuHình + ['-c', xâyDựngĐườngDẫn / 'programs.S', '-o', xâyDựngĐườngDẫn / 'programs.o'])
