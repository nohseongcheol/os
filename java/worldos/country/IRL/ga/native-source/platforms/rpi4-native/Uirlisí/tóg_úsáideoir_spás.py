"""독립된 자체 ABI ELF64와 로더 diúltaigh_VALUE 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from tóg_PYTHON import Create_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Create_úsáideoir_spás(fréamh_cosán, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, Cartlann_uirlis, 설정비트, Rith_ordú):
    설정비트 = [Socruithe_VALUE for Socruithe_VALUE in 설정비트 if Socruithe_VALUE != '-mgeneral-regs-only']
    tóg_cosán = fréamh_cosán / 'build'
    출력결과 = tóg_cosán / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = fréamh_cosán / 'úsáideoir'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, CONAIR, Ainm in [
            (시언어번역기, [], 원본자료 / 'Rith_2.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Rith_ordú.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'úsáideoir_traschóiritheoir.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Eagarthóir.c', 'vi.o')]:
        Rith_ordú([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', CONAIR, '-o', 출력결과 / Ainm])
    Rith_ordú([Cartlann_uirlis, 'rcs', tóg_cosán / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Ainm in ('demo', 'fault', 'network', 'vi'):
        Rith_ordú([연결편집기, '-T', 원본자료 / 'Nasc_dáileadh.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Ainm + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Ainm + '.o'), tóg_cosán / 'libposix-kor-user.a'])
    자바라이브러리만들기(fréamh_cosán, Rith_ordú)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(tóg_cosán)) as 작업경로:
        aicme_cosán = Path(작업경로)
        Rith_ordú(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', aicme_cosán, '-sourcepath', aicme_cosán, '-d', aicme_cosán] +
            [sonraí_suíomh for sonraí_suíomh in sorted((저장소경로 / 'os/úsáideoir/자바').glob('*.java')) if sonraí_suíomh.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Rith_ordú(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'uirlis_iontráil.Rith_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(aicme_cosán.glob('*.class')))
    압축해제경로 = fréamh_cosán / 'vendor/uzlib'
    for CONAIR, Ainm in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'beart.c', 'jar.o')] + [(압축해제경로 / (Ainm + '.c'), Ainm + '.o') for Ainm in ('tinflate', 'crc32', 'adler32')]:
        Rith_ordú([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', CONAIR, '-o', 출력결과 / Ainm])
    Rith_ordú([연결편집기, '-T', 원본자료 / 'Nasc_dáileadh.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Ainm for Ainm in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Create_PYTHON(fréamh_cosán, 시언어번역기, 연결편집기)
    시언어번역기만들기(fréamh_cosán, 저장소경로, 시언어번역기, 연결편집기, 설정비트, Rith_ordú)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    clár_Ceanntásc_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    Ceanntásc_Liosta = [clár_Ceanntásc_OFFSET + mír_COUNT * 56 for mír_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [sonraí_suíomh for sonraí_suíomh in Ceanntásc_Liosta if struct.unpack_from('<I', 유효함, sonraí_suíomh)[0] == 1]
    Téacs, sonraí = 적재구획[:2]
    ordú_ADDRESS = struct.unpack_from('<Q', 유효함, Téacs + 16)[0]
    sonraí_ADDRESS = struct.unpack_from('<Q', 유효함, sonraí + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', ordú_ADDRESS + 1), ('data-entry', 24, 'Q', sonraí_ADDRESS),
               ('outside-file', Téacs + 32, 'Q', len(유효함) + 1), ('short-memory', Téacs + 40, 'Q', 1),
               ('kernel-address', Téacs + 16, 'Q', 0x80000), ('memory-overflow', Téacs + 40, 'Q', 2**64 - 1),
               ('writable-code', Téacs + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Téacs, 'I', 2),
               ('unaligned-load', Téacs + 16, 'Q', ordú_ADDRESS + 8),
               ('overlap', sonraí + 16, 'Q', ordú_ADDRESS)]
    for Ainm, OFFSET_VALUE, formáid_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + formáid_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((Ainm, bytes(바뀐자료)))
    탑재덩이들 = [(Ainm.replace('-', '_'), 출력결과 / (Ainm + '.elf')) for Ainm in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Ainm, pálasta_sonraí) in enumerate(시험사례):
        CONAIR = 출력결과 / ('invalid-{}.elf'.format(Ainm)); CONAIR.write_bytes(pálasta_sonraí)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), CONAIR))
    어셈블리자료, Ceanntásc_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Ainm, CONAIR in 탑재덩이들:
        siombail_VALUE = 'user_blob_' + Ainm
        크기목록[Ainm] = CONAIR.stat().st_size
        # 생성한 piara_VALUE 경로만 넣어 프로젝트 경로의 공백/Athfhriotail 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + siombail_VALUE, siombail_VALUE + ':', '.incbin "{}"'.format(CONAIR.relative_to(fréamh_cosán))]
        Ceanntásc_VALUE.append('extern const unsigned char {}[];'.format(siombail_VALUE))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Ceanntásc_VALUE += ['static const clár_f67c8751 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Ceanntásc_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Ceanntásc_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Ceanntásc_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], modh_mód) for modh_mód in (0, 1)]
    Ceanntásc_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Ceanntásc_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Ceanntásc_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Ceanntásc_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Ceanntásc_VALUE += ['};', 'static const clár_f67c8751 잘못된실행항목들[] = {']
    Ceanntásc_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(pálasta_sonraí)) for 순번, (_, pálasta_sonraí) in enumerate(시험사례)]
    Ceanntásc_VALUE += ['};']
    (tóg_cosán / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (tóg_cosán / 'programs.h').write_text('\n'.join(Ceanntásc_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Ainm for Ainm, _ in 시험사례) + '\n')
    Rith_ordú([시언어번역기] + 설정비트 + ['-c', tóg_cosán / 'programs.S', '-o', tóg_cosán / 'programs.o'])
