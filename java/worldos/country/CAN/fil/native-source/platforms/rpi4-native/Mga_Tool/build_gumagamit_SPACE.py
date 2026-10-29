"""독립된 자체 ABI ELF64와 로더 tanggihan_VALUE 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from build_PYTHON import Create_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Create_gumagamit_SPACE(root_path, repository_path, 시언어번역기, 시플플번역기, 연결편집기, Archive_tool, kompigurasyon_Background_Intelligent_Transfer_Service, Mag_execute_utos):
    kompigurasyon_Background_Intelligent_Transfer_Service = [Mga_Setting_VALUE for Mga_Setting_VALUE in kompigurasyon_Background_Intelligent_Transfer_Service if Mga_Setting_VALUE != '-mgeneral-regs-only']
    build_path = root_path / 'build'
    출력결과 = build_path / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = root_path / 'gumagamit'
    포직스경로 = repository_path / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, path, pangalan in [
            (시언어번역기, [], 원본자료 / 'run.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Mag_execute_utos.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'gumagamit_bridge.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Editor.c', 'vi.o')]:
        Mag_execute_utos([번역기] + kompigurasyon_Background_Intelligent_Transfer_Service + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', path, '-o', 출력결과 / pangalan])
    Mag_execute_utos([Archive_tool, 'rcs', build_path / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for pangalan in ('demo', 'fault', 'network', 'vi'):
        Mag_execute_utos([연결편집기, '-T', 원본자료 / 'Link_Layout.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (pangalan + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (pangalan + '.o'), build_path / 'libposix-kor-user.a'])
    자바라이브러리만들기(root_path, Mag_execute_utos)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(build_path)) as 작업경로:
        kategorya_path = Path(작업경로)
        Mag_execute_utos(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', kategorya_path, '-sourcepath', kategorya_path, '-d', kategorya_path] +
            [data_posisyon for data_posisyon in sorted((repository_path / 'os/gumagamit/자바').glob('*.java')) if data_posisyon.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Mag_execute_utos(['sh', repository_path / 'compiler/미리번역.sh', '--entry', 'tool_pagpasok.run',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(kategorya_path.glob('*.class')))
    압축해제경로 = root_path / 'vendor/uzlib'
    for path, pangalan in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'bundle.c', 'jar.o')] + [(압축해제경로 / (pangalan + '.c'), pangalan + '.o') for pangalan in ('tinflate', 'crc32', 'adler32')]:
        Mag_execute_utos([시언어번역기] + kompigurasyon_Background_Intelligent_Transfer_Service + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', path, '-o', 출력결과 / pangalan])
    Mag_execute_utos([연결편집기, '-T', 원본자료 / 'Link_Layout.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / pangalan for pangalan in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Create_PYTHON(root_path, 시언어번역기, 연결편집기)
    시언어번역기만들기(root_path, repository_path, 시언어번역기, 연결편집기, kompigurasyon_Background_Intelligent_Transfer_Service, Mag_execute_utos)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    app_Header_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    Header_list = [app_Header_OFFSET + item_COUNT * 56 for item_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [data_posisyon for data_posisyon in Header_list if struct.unpack_from('<I', 유효함, data_posisyon)[0] == 1]
    SMS, data = 적재구획[:2]
    utos_email = struct.unpack_from('<Q', 유효함, SMS + 16)[0]
    data_email = struct.unpack_from('<Q', 유효함, data + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', utos_email + 1), ('data-entry', 24, 'Q', data_email),
               ('outside-file', SMS + 32, 'Q', len(유효함) + 1), ('short-memory', SMS + 40, 'Q', 1),
               ('kernel-address', SMS + 16, 'Q', 0x80000), ('memory-overflow', SMS + 40, 'Q', 2**64 - 1),
               ('writable-code', SMS + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', SMS, 'I', 2),
               ('unaligned-load', SMS + 16, 'Q', utos_email + 8),
               ('overlap', data + 16, 'Q', utos_email)]
    for pangalan, OFFSET_VALUE, format_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + format_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((pangalan, bytes(바뀐자료)))
    탑재덩이들 = [(pangalan.replace('-', '_'), 출력결과 / (pangalan + '.elf')) for pangalan in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (pangalan, payload_data) in enumerate(시험사례):
        path = 출력결과 / ('invalid-{}.elf'.format(pangalan)); path.write_bytes(payload_data)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), path))
    어셈블리자료, Header_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for pangalan, path in 탑재덩이들:
        simbolo_VALUE = 'user_blob_' + pangalan
        크기목록[pangalan] = path.stat().st_size
        # 생성한 peer_VALUE 경로만 넣어 프로젝트 경로의 공백/Quote 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + simbolo_VALUE, simbolo_VALUE + ':', '.incbin "{}"'.format(path.relative_to(root_path))]
        Header_VALUE.append('extern const unsigned char {}[];'.format(simbolo_VALUE))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Header_VALUE += ['static const app 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Header_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Header_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Header_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], pamamaraan_MODE) for pamamaraan_MODE in (0, 1)]
    Header_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Header_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Header_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Header_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Header_VALUE += ['};', 'static const app 잘못된실행항목들[] = {']
    Header_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(payload_data)) for 순번, (_, payload_data) in enumerate(시험사례)]
    Header_VALUE += ['};']
    (build_path / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (build_path / 'programs.h').write_text('\n'.join(Header_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(pangalan for pangalan, _ in 시험사례) + '\n')
    Mag_execute_utos([시언어번역기] + kompigurasyon_Background_Intelligent_Transfer_Service + ['-c', build_path / 'programs.S', '-o', build_path / 'programs.o'])
