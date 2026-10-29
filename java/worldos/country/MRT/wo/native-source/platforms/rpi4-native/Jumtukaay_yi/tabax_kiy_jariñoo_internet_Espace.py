"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def sos_kiy_jariñoo_internet_Espace(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, denc_jumtukaay, 설정비트, def_ndigel):
    설정비트 = [Jekkal_yi_xëyma for Jekkal_yi_xëyma in 설정비트 if Jekkal_yi_xëyma != '-mgeneral-regs-only']
    tabax_Yoonu_jëmale = 기준경로 / 'build'
    출력결과 = tabax_Yoonu_jëmale / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'kiy_jariñoo_internet'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, Yoonu_jëmale, tur_253d1510 in [
            (시언어번역기, [], 원본자료 / 'daw.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'def_ndigel.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'kiy_jariñoo_internet_poŋ.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'defarkat.c', 'vi.o')]:
        def_ndigel([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', Yoonu_jëmale, '-o', 출력결과 / tur_253d1510])
    def_ndigel([denc_jumtukaay, 'rcs', tabax_Yoonu_jëmale / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for tur_253d1510 in ('demo', 'fault', 'network', 'vi'):
        def_ndigel([연결편집기, '-T', 원본자료 / 'lëkkale_Tëralin.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (tur_253d1510 + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (tur_253d1510 + '.o'), tabax_Yoonu_jëmale / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, def_ndigel)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(tabax_Yoonu_jëmale)) as 작업경로:
        maas_Yoonu_jëmale = Path(작업경로)
        def_ndigel(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', maas_Yoonu_jëmale, '-sourcepath', maas_Yoonu_jëmale, '-d', maas_Yoonu_jëmale] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/kiy_jariñoo_internet/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        def_ndigel(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'jumtukaay_dugal_xabaar.daw',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(maas_Yoonu_jëmale.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for Yoonu_jëmale, tur_253d1510 in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'takku_xéewël.c', 'jar.o')] + [(압축해제경로 / (tur_253d1510 + '.c'), tur_253d1510 + '.o') for tur_253d1510 in ('tinflate', 'crc32', 'adler32')]:
        def_ndigel([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', Yoonu_jëmale, '-o', 출력결과 / tur_253d1510])
    def_ndigel([연결편집기, '-T', 원본자료 / 'lëkkale_Tëralin.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / tur_253d1510 for tur_253d1510 in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, def_ndigel)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    jëfekaay_Tur_Randal = struct.unpack_from('<Q', 유효함, 32)[0]
    Tur_lim = [jëfekaay_Tur_Randal + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in Tur_lim if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    Tekst, mbir = 적재구획[:2]
    ndigel_dëkkuwaay = struct.unpack_from('<Q', 유효함, Tekst + 16)[0]
    mbir_dëkkuwaay = struct.unpack_from('<Q', 유효함, mbir + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', ndigel_dëkkuwaay + 1), ('data-entry', 24, 'Q', mbir_dëkkuwaay),
               ('outside-file', Tekst + 32, 'Q', len(유효함) + 1), ('short-memory', Tekst + 40, 'Q', 1),
               ('kernel-address', Tekst + 16, 'Q', 0x80000), ('memory-overflow', Tekst + 40, 'Q', 2**64 - 1),
               ('writable-code', Tekst + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Tekst, 'I', 2),
               ('unaligned-load', Tekst + 16, 'Q', ndigel_dëkkuwaay + 8),
               ('overlap', mbir + 16, 'Q', ndigel_dëkkuwaay)]
    for tur_253d1510, Randal_xëyma, melokaanub_mbir, xëyma in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + melokaanub_mbir, 바뀐자료, Randal_xëyma, xëyma)
        시험사례.append((tur_253d1510, bytes(바뀐자료)))
    탑재덩이들 = [(tur_253d1510.replace('-', '_'), 출력결과 / (tur_253d1510 + '.elf')) for tur_253d1510 in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (tur_253d1510, njoxe_yu_solowu_mbir) in enumerate(시험사례):
        Yoonu_jëmale = 출력결과 / ('invalid-{}.elf'.format(tur_253d1510)); Yoonu_jëmale.write_bytes(njoxe_yu_solowu_mbir)
        탑재덩이들.append(('invalid_{}'.format(색인), Yoonu_jëmale))
    어셈블리자료, Tur_xëyma = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for tur_253d1510, Yoonu_jëmale in 탑재덩이들:
        sembóol_xëyma = 'user_blob_' + tur_253d1510
        크기목록[tur_253d1510] = Yoonu_jëmale.stat().st_size
        # 생성한 Nàttangoo_xëyma 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + sembóol_xëyma, sembóol_xëyma + ':', '.incbin "{}"'.format(Yoonu_jëmale.relative_to(기준경로))]
        Tur_xëyma.append('extern const unsigned char {}[];'.format(sembóol_xëyma))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Tur_xëyma += ['static const jëfekaay 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Tur_xëyma += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Tur_xëyma += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Tur_xëyma += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], doxalin_anam) for doxalin_anam in (0, 1)]
    Tur_xëyma += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Tur_xëyma += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Tur_xëyma += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Tur_xëyma += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Tur_xëyma += ['};', 'static const jëfekaay 잘못된실행항목들[] = {']
    Tur_xëyma += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(njoxe_yu_solowu_mbir)) for 순번, (_, njoxe_yu_solowu_mbir) in enumerate(시험사례)]
    Tur_xëyma += ['};']
    (tabax_Yoonu_jëmale / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (tabax_Yoonu_jëmale / 'programs.h').write_text('\n'.join(Tur_xëyma) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(tur_253d1510 for tur_253d1510, _ in 시험사례) + '\n')
    def_ndigel([시언어번역기] + 설정비트 + ['-c', tabax_Yoonu_jëmale / 'programs.S', '-o', tabax_Yoonu_jëmale / 'programs.o'])
