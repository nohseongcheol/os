"""독립된 Öz ABI ELF64와 로더 reddetmek_değer sınamalar 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from BLD_PYTHON import açmak_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from BLD_C_derleyici import açmak_C_derleyici


def açmak_kullanıcı_yer(kök_yol, depo_yol, C_derleyici, 시플플번역기, bağlayıcı_araç, Arşiv_araç, Yapılandırma_BITS, yürütmek_komut):
    Yapılandırma_BITS = [Ayarlar_değer for Ayarlar_değer in Yapılandırma_BITS if Ayarlar_değer != '-mgeneral-regs-only']
    BLD_yol = kök_yol / 'build'
    çıktı = BLD_yol / 'user'
    çıktı.mkdir(exist_ok=True)
    원본자료 = kök_yol / 'kullanıcı_alanı'
    포직스경로 = depo_yol / 'posix-kor/arm64-native'
    içermek_yol = ['-I', 원본자료, '-I', 포직스경로 / 'bildirimler', '-I', çıktı]
    for derleyici_araç, 추가영역, yol, İsim in [
            (C_derleyici, [], 원본자료 / 'çalıştır.S', 'start.o'),
            (C_derleyici, ['-std=c11'], 원본자료 / 'yürütmek_komut.c', 'runtime.o'),
            (C_derleyici, ['-std=c11'], 포직스경로 / 'kullanıcı_köprü.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'DosyaÖrneği.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_derleyici, ['-std=c11'], 원본자료 / 'Koruma_test.c', 'fault.o'),
            (C_derleyici, ['-std=c11'], 원본자료 / 'Düzenleyici.c', 'vi.o')]:
        yürütmek_komut([derleyici_araç] + Yapılandırma_BITS + 추가영역 + içermek_yol + ['-Wall', '-Wextra', '-Werror', '-c', yol, '-o', çıktı / İsim])
    yürütmek_komut([Arşiv_araç, 'rcs', BLD_yol / 'libposix-kor-user.a', çıktı / 'posix.o'])
    for İsim in ('demo', 'fault', 'network', 'vi'):
        yürütmek_komut([bağlayıcı_araç, '-T', 원본자료 / 'bağlama_düzeni.ld', '-z', 'max-page-size=4096', '-o', çıktı / (İsim + '.elf'),
             çıktı / 'start.o', çıktı / 'runtime.o', çıktı / (İsim + '.o'), BLD_yol / 'libposix-kor-user.a'])
    자바라이브러리만들기(kök_yol, yürütmek_komut)
    # 기존 Öz Java derleyici/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(BLD_yol)) as 작업경로:
        Sınıf_yol = Path(작업경로)
        yürütmek_komut(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Sınıf_yol, '-sourcepath', Sınıf_yol, '-d', Sınıf_yol] +
            [veri_konum for veri_konum in sorted((depo_yol / 'os/kullanıcı_alanı/자바').glob('*.java')) if veri_konum.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        yürütmek_komut(['sh', depo_yol / 'compiler/미리번역.sh', '--entry', 'araç_girdi.çalıştır',
             '--profile', 'user', '--heap-words', '1048576', '-o', çıktı / 'java-tools.c'] + sorted(Sınıf_yol.glob('*.class')))
    압축해제경로 = kök_yol / 'vendor/uzlib'
    for yol, İsim in [(çıktı / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'paket_iş.c', 'jar.o')] + [(압축해제경로 / (İsim + '.c'), İsim + '.o') for İsim in ('tinflate', 'crc32', 'adler32')]:
        yürütmek_komut([C_derleyici] + Yapılandırma_BITS + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + içermek_yol + ['-c', yol, '-o', çıktı / İsim])
    yürütmek_komut([bağlayıcı_araç, '-T', 원본자료 / 'bağlama_düzeni.ld', '-z', 'max-page-size=4096', '-o', çıktı / 'java-tools.elf'] +
        [çıktı / İsim for İsim in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    açmak_PYTHON(kök_yol, C_derleyici, bağlayıcı_araç)
    açmak_C_derleyici(kök_yol, depo_yol, C_derleyici, bağlayıcı_araç, Yapılandırma_BITS, yürütmek_komut)
    geçerli = (çıktı / 'demo.elf').read_bytes()
    program_Başlık_Ofset = struct.unpack_from('<Q', geçerli, 32)[0]
    Başlık_Liste = [program_Başlık_Ofset + öğe_BAĞ_DEĞ_SAY * 56 for öğe_BAĞ_DEĞ_SAY in range(struct.unpack_from('<H', geçerli, 56)[0])]
    적재구획 = [veri_konum for veri_konum in Başlık_Liste if struct.unpack_from('<I', geçerli, veri_konum)[0] == 1]
    metin, veri = 적재구획[:2]
    komut_ADRES = struct.unpack_from('<Q', geçerli, metin + 16)[0]
    veri_ADRES = struct.unpack_from('<Q', geçerli, veri + 16)[0]
    Ara_ABI = geçerli.index(b'JKOROS\0')
    test_çalışması = [('empty', b''), ('short', geçerli[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', komut_ADRES + 1), ('data-entry', 24, 'Q', veri_ADRES),
               ('outside-file', metin + 32, 'Q', len(geçerli) + 1), ('short-memory', metin + 40, 'Q', 1),
               ('kernel-address', metin + 16, 'Q', 0x80000), ('memory-overflow', metin + 40, 'Q', 2**64 - 1),
               ('writable-code', metin + 4, 'I', 7), ('missing-abi', Ara_ABI, 'B', ord('X')),
               ('wrong-abi', Ara_ABI + 8, 'I', 2), ('dynamic', metin, 'I', 2),
               ('unaligned-load', metin + 16, 'Q', komut_ADRES + 8),
               ('overlap', veri + 16, 'Q', komut_ADRES)]
    for İsim, Ofset_değer, biçim_932e03c8, değer in 수정사항:
        바뀐자료 = bytearray(geçerli); struct.pack_into('<' + biçim_932e03c8, 바뀐자료, Ofset_değer, değer)
        test_çalışması.append((İsim, bytes(바뀐자료)))
    탑재덩이들 = [(İsim.replace('-', '_'), çıktı / (İsim + '.elf')) for İsim in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for ARA_Dizin, (İsim, yük_veri) in enumerate(test_çalışması):
        yol = çıktı / ('invalid-{}.elf'.format(İsim)); yol.write_bytes(yük_veri)
        탑재덩이들.append(('invalid_{}'.format(ARA_Dizin), yol))
    derleme, Başlık_değer = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for İsim, yol in 탑재덩이들:
        simge_değer = 'user_blob_' + İsim
        크기목록[İsim] = yol.stat().st_size
        # 생성한 eş_değer 경로만 넣어 프로젝트 경로의 공백/Alıntı 영향을 피한다.
        derleme += ['.balign 16', '.global ' + simge_değer, simge_değer + ':', '.incbin "{}"'.format(yol.relative_to(kök_yol))]
        Başlık_değer.append('extern const unsigned char {}[];'.format(simge_değer))
    derleme.append('.section .note.GNU-stack,"",%progbits')
    Başlık_değer += ['static const program 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Başlık_değer += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Başlık_değer += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Başlık_değer += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metot_mod) for metot_mod in (0, 1)]
    Başlık_değer += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Başlık_değer += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Başlık_değer += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Başlık_değer += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Başlık_değer += ['};', 'static const program 잘못된실행항목들[] = {']
    Başlık_değer += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(yük_veri)) for 순번, (_, yük_veri) in enumerate(test_çalışması)]
    Başlık_değer += ['};']
    (BLD_yol / 'programs.S').write_text('\n'.join(derleme) + '\n')
    (BLD_yol / 'programs.h').write_text('\n'.join(Başlık_değer) + '\n')
    (çıktı / 'invalid-cases.txt').write_text('\n'.join(İsim for İsim, _ in test_çalışması) + '\n')
    yürütmek_komut([C_derleyici] + Yapılandırma_BITS + ['-c', BLD_yol / 'programs.S', '-o', BLD_yol / 'programs.o'])
