"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from qurmaq_PYTHON import yarat_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def yarat_istifadəçi_məkan(kök_yol, anbar_yol, 시언어번역기, 시플플번역기, 연결편집기, Arxiv_alət, konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti, icra_etmək_əmr):
    konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti = [Parametrlər_VALUE for Parametrlər_VALUE in konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti if Parametrlər_VALUE != '-mgeneral-regs-only']
    qurmaq_yol = kök_yol / 'build'
    출력결과 = qurmaq_yol / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = kök_yol / 'istifadəçi'
    포직스경로 = anbar_yol / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, Cığır, Ad in [
            (시언어번역기, [], 원본자료 / 'İcra_Et.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'icra_etmək_əmr.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'istifadəçi_körpü.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Redaktor.c', 'vi.o')]:
        icra_etmək_əmr([번역기] + konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', Cığır, '-o', 출력결과 / Ad])
    icra_etmək_əmr([Arxiv_alət, 'rcs', qurmaq_yol / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Ad in ('demo', 'fault', 'network', 'vi'):
        icra_etmək_əmr([연결편집기, '-T', 원본자료 / 'keçid_Düzüm.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Ad + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Ad + '.o'), qurmaq_yol / 'libposix-kor-user.a'])
    자바라이브러리만들기(kök_yol, icra_etmək_əmr)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(qurmaq_yol)) as 작업경로:
        Sinif_yol = Path(작업경로)
        icra_etmək_əmr(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Sinif_yol, '-sourcepath', Sinif_yol, '-d', Sinif_yol] +
            [verilənlər_yerinə_qoymaq for verilənlər_yerinə_qoymaq in sorted((anbar_yol / 'os/istifadəçi/자바').glob('*.java')) if verilənlər_yerinə_qoymaq.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        icra_etmək_əmr(['sh', anbar_yol / 'compiler/미리번역.sh', '--entry', 'alət_daxiletmə.İcra_Et',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(Sinif_yol.glob('*.class')))
    압축해제경로 = kök_yol / 'vendor/uzlib'
    for Cığır, Ad in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'paket.c', 'jar.o')] + [(압축해제경로 / (Ad + '.c'), Ad + '.o') for Ad in ('tinflate', 'crc32', 'adler32')]:
        icra_etmək_əmr([시언어번역기] + konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', Cığır, '-o', 출력결과 / Ad])
    icra_etmək_əmr([연결편집기, '-T', 원본자료 / 'keçid_Düzüm.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Ad for Ad in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    yarat_PYTHON(kök_yol, 시언어번역기, 연결편집기)
    시언어번역기만들기(kök_yol, anbar_yol, 시언어번역기, 연결편집기, konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti, icra_etmək_əmr)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    proqram_Başlıq_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    Başlıq_Siyahı = [proqram_Başlıq_OFFSET + element_COUNT * 56 for element_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [verilənlər_yerinə_qoymaq for verilənlər_yerinə_qoymaq in Başlıq_Siyahı if struct.unpack_from('<I', 유효함, verilənlər_yerinə_qoymaq)[0] == 1]
    Mətn, verilənlər = 적재구획[:2]
    əmr_ünvan = struct.unpack_from('<Q', 유효함, Mətn + 16)[0]
    verilənlər_ünvan = struct.unpack_from('<Q', 유효함, verilənlər + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', əmr_ünvan + 1), ('data-entry', 24, 'Q', verilənlər_ünvan),
               ('outside-file', Mətn + 32, 'Q', len(유효함) + 1), ('short-memory', Mətn + 40, 'Q', 1),
               ('kernel-address', Mətn + 16, 'Q', 0x80000), ('memory-overflow', Mətn + 40, 'Q', 2**64 - 1),
               ('writable-code', Mətn + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Mətn, 'I', 2),
               ('unaligned-load', Mətn + 16, 'Q', əmr_ünvan + 8),
               ('overlap', verilənlər + 16, 'Q', əmr_ünvan)]
    for Ad, OFFSET_VALUE, format_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + format_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((Ad, bytes(바뀐자료)))
    탑재덩이들 = [(Ad.replace('-', '_'), 출력결과 / (Ad + '.elf')) for Ad in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Ad, faydalı_yük_verilənlər) in enumerate(시험사례):
        Cığır = 출력결과 / ('invalid-{}.elf'.format(Ad)); Cığır.write_bytes(faydalı_yük_verilənlər)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), Cığır))
    어셈블리자료, Başlıq_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Ad, Cığır in 탑재덩이들:
        simvol_VALUE = 'user_blob_' + Ad
        크기목록[Ad] = Cığır.stat().st_size
        # 생성한 eynisəviyyəli_VALUE 경로만 넣어 프로젝트 경로의 공백/Dırnaqarası 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + simvol_VALUE, simvol_VALUE + ':', '.incbin "{}"'.format(Cığır.relative_to(kök_yol))]
        Başlıq_VALUE.append('extern const unsigned char {}[];'.format(simvol_VALUE))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Başlıq_VALUE += ['static const proqram 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Başlıq_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Başlıq_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Başlıq_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metod_MODE) for metod_MODE in (0, 1)]
    Başlıq_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Başlıq_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Başlıq_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Başlıq_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Başlıq_VALUE += ['};', 'static const proqram 잘못된실행항목들[] = {']
    Başlıq_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(faydalı_yük_verilənlər)) for 순번, (_, faydalı_yük_verilənlər) in enumerate(시험사례)]
    Başlıq_VALUE += ['};']
    (qurmaq_yol / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (qurmaq_yol / 'programs.h').write_text('\n'.join(Başlıq_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Ad for Ad, _ in 시험사례) + '\n')
    icra_etmək_əmr([시언어번역기] + konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti + ['-c', qurmaq_yol / 'programs.S', '-o', qurmaq_yol / 'programs.o'])
