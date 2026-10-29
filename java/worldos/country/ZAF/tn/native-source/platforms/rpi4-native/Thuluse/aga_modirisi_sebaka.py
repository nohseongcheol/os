"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def tlhama_modirisi_sebaka(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, boloka_sediriswa, 설정비트, diragatsa_Taelo):
    설정비트 = [Diseting_Boleng for Diseting_Boleng in 설정비트 if Diseting_Boleng != '-mgeneral-regs-only']
    aga_tsela = 기준경로 / 'build'
    출력결과 = aga_tsela / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'modirisi'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, tsela, leina in [
            (시언어번역기, [], 원본자료 / 'dirisa.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'diragatsa_Taelo.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'modirisi_leborogo.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Setseleganyi.c', 'vi.o')]:
        diragatsa_Taelo([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', tsela, '-o', 출력결과 / leina])
    diragatsa_Taelo([boloka_sediriswa, 'rcs', aga_tsela / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for leina in ('demo', 'fault', 'network', 'vi'):
        diragatsa_Taelo([연결편집기, '-T', 원본자료 / 'Kgokagano_Boalo.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (leina + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (leina + '.o'), aga_tsela / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, diragatsa_Taelo)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(aga_tsela)) as 작업경로:
        mofuta_tsela = Path(작업경로)
        diragatsa_Taelo(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', mofuta_tsela, '-sourcepath', mofuta_tsela, '-d', mofuta_tsela] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/modirisi/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        diragatsa_Taelo(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'sediriswa_tsenyo.dirisa',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(mofuta_tsela.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for tsela, leina in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'ngatanngwe.c', 'jar.o')] + [(압축해제경로 / (leina + '.c'), leina + '.o') for leina in ('tinflate', 'crc32', 'adler32')]:
        diragatsa_Taelo([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', tsela, '-o', 출력결과 / leina])
    diragatsa_Taelo([연결편집기, '-T', 원본자료 / 'Kgokagano_Boalo.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / leina for leina in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, diragatsa_Taelo)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    Tiriso_setlhogo_Baya_ka_Tekatekanyo = struct.unpack_from('<Q', 유효함, 32)[0]
    setlhogo_lenaane = [Tiriso_setlhogo_Baya_ka_Tekatekanyo + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in setlhogo_lenaane if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    SMS, tshedimosetso = 적재구획[:2]
    Taelo_aterese = struct.unpack_from('<Q', 유효함, SMS + 16)[0]
    tshedimosetso_aterese = struct.unpack_from('<Q', 유효함, tshedimosetso + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', Taelo_aterese + 1), ('data-entry', 24, 'Q', tshedimosetso_aterese),
               ('outside-file', SMS + 32, 'Q', len(유효함) + 1), ('short-memory', SMS + 40, 'Q', 1),
               ('kernel-address', SMS + 16, 'Q', 0x80000), ('memory-overflow', SMS + 40, 'Q', 2**64 - 1),
               ('writable-code', SMS + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', SMS, 'I', 2),
               ('unaligned-load', SMS + 16, 'Q', Taelo_aterese + 8),
               ('overlap', tshedimosetso + 16, 'Q', Taelo_aterese)]
    for leina, Baya_ka_Tekatekanyo_Boleng, fomete, Boleng in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + fomete, 바뀐자료, Baya_ka_Tekatekanyo_Boleng, Boleng)
        시험사례.append((leina, bytes(바뀐자료)))
    탑재덩이들 = [(leina.replace('-', '_'), 출력결과 / (leina + '.elf')) for leina in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (leina, selekanyo_sa_tshedimosetso_tshedimosetso) in enumerate(시험사례):
        tsela = 출력결과 / ('invalid-{}.elf'.format(leina)); tsela.write_bytes(selekanyo_sa_tshedimosetso_tshedimosetso)
        탑재덩이들.append(('invalid_{}'.format(색인), tsela))
    어셈블리자료, setlhogo_Boleng = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for leina, tsela in 탑재덩이들:
        letshwao_Boleng = 'user_blob_' + leina
        크기목록[leina] = tsela.stat().st_size
        # 생성한 semphato_Boleng 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + letshwao_Boleng, letshwao_Boleng + ':', '.incbin "{}"'.format(tsela.relative_to(기준경로))]
        setlhogo_Boleng.append('extern const unsigned char {}[];'.format(letshwao_Boleng))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    setlhogo_Boleng += ['static const Tiriso 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    setlhogo_Boleng += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    setlhogo_Boleng += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    setlhogo_Boleng += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], mokgwa_mokgwa) for mokgwa_mokgwa in (0, 1)]
    setlhogo_Boleng += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    setlhogo_Boleng += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    setlhogo_Boleng += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    setlhogo_Boleng += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    setlhogo_Boleng += ['};', 'static const Tiriso 잘못된실행항목들[] = {']
    setlhogo_Boleng += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(selekanyo_sa_tshedimosetso_tshedimosetso)) for 순번, (_, selekanyo_sa_tshedimosetso_tshedimosetso) in enumerate(시험사례)]
    setlhogo_Boleng += ['};']
    (aga_tsela / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (aga_tsela / 'programs.h').write_text('\n'.join(setlhogo_Boleng) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(leina for leina, _ in 시험사례) + '\n')
    diragatsa_Taelo([시언어번역기] + 설정비트 + ['-c', aga_tsela / 'programs.S', '-o', aga_tsela / 'programs.o'])
