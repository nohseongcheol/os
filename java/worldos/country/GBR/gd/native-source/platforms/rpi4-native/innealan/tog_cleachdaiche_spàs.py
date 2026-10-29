"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from tog_PYTHON import Create_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Create_cleachdaiche_spàs(freumh_slighe, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, taisg_inneal, 설정비트, gnìomhaich_àithne):
    설정비트 = [roghainnean_VALUE for roghainnean_VALUE in 설정비트 if roghainnean_VALUE != '-mgeneral-regs-only']
    tog_slighe = freumh_slighe / 'build'
    출력결과 = tog_slighe / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = freumh_slighe / 'cleachdaiche'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, Slighe, Ainm in [
            (시언어번역기, [], 원본자료 / 'ruith.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'gnìomhaich_àithne.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'cleachdaiche_drochaid.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'deasaiche.c', 'vi.o')]:
        gnìomhaich_àithne([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', Slighe, '-o', 출력결과 / Ainm])
    gnìomhaich_àithne([taisg_inneal, 'rcs', tog_slighe / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Ainm in ('demo', 'fault', 'network', 'vi'):
        gnìomhaich_àithne([연결편집기, '-T', 원본자료 / 'ceangal_co_dhealbhachd.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Ainm + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Ainm + '.o'), tog_slighe / 'libposix-kor-user.a'])
    자바라이브러리만들기(freumh_slighe, gnìomhaich_àithne)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(tog_slighe)) as 작업경로:
        clas_slighe = Path(작업경로)
        gnìomhaich_àithne(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', clas_slighe, '-sourcepath', clas_slighe, '-d', clas_slighe] +
            [dàta_suidhich for dàta_suidhich in sorted((저장소경로 / 'os/cleachdaiche/자바').glob('*.java')) if dàta_suidhich.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        gnìomhaich_àithne(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'inneal_cur_a_steach.ruith',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(clas_slighe.glob('*.class')))
    압축해제경로 = freumh_slighe / 'vendor/uzlib'
    for Slighe, Ainm in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'trusgan.c', 'jar.o')] + [(압축해제경로 / (Ainm + '.c'), Ainm + '.o') for Ainm in ('tinflate', 'crc32', 'adler32')]:
        gnìomhaich_àithne([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', Slighe, '-o', 출력결과 / Ainm])
    gnìomhaich_àithne([연결편집기, '-T', 원본자료 / 'ceangal_co_dhealbhachd.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Ainm for Ainm in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Create_PYTHON(freumh_slighe, 시언어번역기, 연결편집기)
    시언어번역기만들기(freumh_slighe, 저장소경로, 시언어번역기, 연결편집기, 설정비트, gnìomhaich_àithne)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    ap_bann_cinn_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    bann_cinn_Liosta = [ap_bann_cinn_OFFSET + nì_COUNT * 56 for nì_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [dàta_suidhich for dàta_suidhich in bann_cinn_Liosta if struct.unpack_from('<I', 유효함, dàta_suidhich)[0] == 1]
    SMS, dàta = 적재구획[:2]
    àithne_ADDRESS = struct.unpack_from('<Q', 유효함, SMS + 16)[0]
    dàta_ADDRESS = struct.unpack_from('<Q', 유효함, dàta + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', àithne_ADDRESS + 1), ('data-entry', 24, 'Q', dàta_ADDRESS),
               ('outside-file', SMS + 32, 'Q', len(유효함) + 1), ('short-memory', SMS + 40, 'Q', 1),
               ('kernel-address', SMS + 16, 'Q', 0x80000), ('memory-overflow', SMS + 40, 'Q', 2**64 - 1),
               ('writable-code', SMS + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', SMS, 'I', 2),
               ('unaligned-load', SMS + 16, 'Q', àithne_ADDRESS + 8),
               ('overlap', dàta + 16, 'Q', àithne_ADDRESS)]
    for Ainm, OFFSET_VALUE, fòrmat_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + fòrmat_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((Ainm, bytes(바뀐자료)))
    탑재덩이들 = [(Ainm.replace('-', '_'), 출력결과 / (Ainm + '.elf')) for Ainm in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Ainm, payload_dàta) in enumerate(시험사례):
        Slighe = 출력결과 / ('invalid-{}.elf'.format(Ainm)); Slighe.write_bytes(payload_dàta)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), Slighe))
    어셈블리자료, bann_cinn_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Ainm, Slighe in 탑재덩이들:
        samhla_VALUE = 'user_blob_' + Ainm
        크기목록[Ainm] = Slighe.stat().st_size
        # 생성한 seise_VALUE 경로만 넣어 프로젝트 경로의 공백/comharran_labhairt 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + samhla_VALUE, samhla_VALUE + ':', '.incbin "{}"'.format(Slighe.relative_to(freumh_slighe))]
        bann_cinn_VALUE.append('extern const unsigned char {}[];'.format(samhla_VALUE))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    bann_cinn_VALUE += ['static const ap 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    bann_cinn_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    bann_cinn_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    bann_cinn_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], dòigh_MODE) for dòigh_MODE in (0, 1)]
    bann_cinn_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    bann_cinn_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    bann_cinn_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    bann_cinn_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    bann_cinn_VALUE += ['};', 'static const ap 잘못된실행항목들[] = {']
    bann_cinn_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(payload_dàta)) for 순번, (_, payload_dàta) in enumerate(시험사례)]
    bann_cinn_VALUE += ['};']
    (tog_slighe / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (tog_slighe / 'programs.h').write_text('\n'.join(bann_cinn_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Ainm for Ainm, _ in 시험사례) + '\n')
    gnìomhaich_àithne([시언어번역기] + 설정비트 + ['-c', tog_slighe / 'programs.S', '-o', tog_slighe / 'programs.o'])
