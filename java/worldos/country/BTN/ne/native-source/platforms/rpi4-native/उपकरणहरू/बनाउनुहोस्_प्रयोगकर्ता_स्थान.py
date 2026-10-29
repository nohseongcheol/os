"""독립된 निज ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def सिर्जना_प्रयोगकर्ता_स्थान(रूट_बाटो, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, सङ्ग्रह_उपकरण, 설정비트, कार्यान्वयन_गर्नुहोस्_आदेश):
    설정비트 = [सेटिङहरू_मान for सेटिङहरू_मान in 설정비트 if सेटिङहरू_मान != '-mgeneral-regs-only']
    बनाउनुहोस्_बाटो = रूट_बाटो / 'build'
    출력결과 = बनाउनुहोस्_बाटो / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = रूट_बाटो / 'प्रयोगकर्ता'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, मार्ग, नाम in [
            (시언어번역기, [], 원본자료 / 'चलाउनुहोस्.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'कार्यान्वयन_गर्नुहोस्_आदेश.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'प्रयोगकर्ता_ब्रिज.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'फाइलउदाहरण.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'सम्पादक.c', 'vi.o')]:
        कार्यान्वयन_गर्नुहोस्_आदेश([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', मार्ग, '-o', 출력결과 / नाम])
    कार्यान्वयन_गर्नुहोस्_आदेश([सङ्ग्रह_उपकरण, 'rcs', बनाउनुहोस्_बाटो / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for नाम in ('demo', 'fault', 'network', 'vi'):
        कार्यान्वयन_गर्नुहोस्_आदेश([연결편집기, '-T', 원본자료 / 'लिङ्क_लेआउट.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (नाम + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (नाम + '.o'), बनाउनुहोस्_बाटो / 'libposix-kor-user.a'])
    자바라이브러리만들기(रूट_बाटो, कार्यान्वयन_गर्नुहोस्_आदेश)
    # 기존 निज Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(बनाउनुहोस्_बाटो)) as 작업경로:
        वर्ग_बाटो = Path(작업경로)
        कार्यान्वयन_गर्नुहोस्_आदेश(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', वर्ग_बाटो, '-sourcepath', वर्ग_बाटो, '-d', वर्ग_बाटो] +
            [लगत_राख्नुहोस् for लगत_राख्नुहोस् in sorted((저장소경로 / 'os/प्रयोगकर्ता/자바').glob('*.java')) if लगत_राख्नुहोस्.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        कार्यान्वयन_गर्नुहोस्_आदेश(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'उपकरण_प्रविष्टि.चलाउनुहोस्',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(वर्ग_बाटो.glob('*.class')))
    압축해제경로 = रूट_बाटो / 'vendor/uzlib'
    for मार्ग, नाम in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'पोको.c', 'jar.o')] + [(압축해제경로 / (नाम + '.c'), नाम + '.o') for नाम in ('tinflate', 'crc32', 'adler32')]:
        कार्यान्वयन_गर्नुहोस्_आदेश([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', मार्ग, '-o', 출력결과 / नाम])
    कार्यान्वयन_गर्नुहोस्_आदेश([연결편집기, '-T', 원본자료 / 'लिङ्क_लेआउट.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / नाम for नाम in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(रूट_बाटो, 시언어번역기, 연결편집기)
    시언어번역기만들기(रूट_बाटो, 저장소경로, 시언어번역기, 연결편집기, 설정비트, कार्यान्वयन_गर्नुहोस्_आदेश)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    अनुप्रयोग_हेडर_अफसेट = struct.unpack_from('<Q', 유효함, 32)[0]
    हेडर_सूची = [अनुप्रयोग_हेडर_अफसेट + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [लगत_राख्नुहोस् for लगत_राख्नुहोस् in हेडर_सूची if struct.unpack_from('<I', 유효함, लगत_राख्नुहोस्)[0] == 1]
    पाठ, लगत = 적재구획[:2]
    आदेश_ठेगाना = struct.unpack_from('<Q', 유효함, पाठ + 16)[0]
    लगत_ठेगाना = struct.unpack_from('<Q', 유효함, लगत + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', आदेश_ठेगाना + 1), ('data-entry', 24, 'Q', लगत_ठेगाना),
               ('outside-file', पाठ + 32, 'Q', len(유효함) + 1), ('short-memory', पाठ + 40, 'Q', 1),
               ('kernel-address', पाठ + 16, 'Q', 0x80000), ('memory-overflow', पाठ + 40, 'Q', 2**64 - 1),
               ('writable-code', पाठ + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', पाठ, 'I', 2),
               ('unaligned-load', पाठ + 16, 'Q', आदेश_ठेगाना + 8),
               ('overlap', लगत + 16, 'Q', आदेश_ठेगाना)]
    for नाम, अफसेट_मान, स्वरूप, मान in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + स्वरूप, 바뀐자료, अफसेट_मान, मान)
        시험사례.append((नाम, bytes(바뀐자료)))
    탑재덩이들 = [(नाम.replace('-', '_'), 출력결과 / (नाम + '.elf')) for नाम in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for विवरण_हेर्ने_सुविधा_अनुक्रमणिका, (नाम, पेलोड_लगत) in enumerate(시험사례):
        मार्ग = 출력결과 / ('invalid-{}.elf'.format(नाम)); मार्ग.write_bytes(पेलोड_लगत)
        탑재덩이들.append(('invalid_{}'.format(विवरण_हेर्ने_सुविधा_अनुक्रमणिका), मार्ग))
    어셈블리자료, हेडर_मान = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for नाम, मार्ग in 탑재덩이들:
        चिन्ह_मान = 'user_blob_' + नाम
        크기목록[नाम] = मार्ग.stat().st_size
        # 생성한 समान_मान 경로만 넣어 프로젝트 경로의 공백/उद्धरण 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + चिन्ह_मान, चिन्ह_मान + ':', '.incbin "{}"'.format(मार्ग.relative_to(रूट_बाटो))]
        हेडर_मान.append('extern const unsigned char {}[];'.format(चिन्ह_मान))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    हेडर_मान += ['static const अनुप्रयोग 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    हेडर_मान += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    हेडर_मान += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    हेडर_मान += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], तरिका_मोड) for तरिका_मोड in (0, 1)]
    हेडर_मान += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    हेडर_मान += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    हेडर_मान += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    हेडर_मान += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    हेडर_मान += ['};', 'static const अनुप्रयोग 잘못된실행항목들[] = {']
    हेडर_मान += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(पेलोड_लगत)) for 순번, (_, पेलोड_लगत) in enumerate(시험사례)]
    हेडर_मान += ['};']
    (बनाउनुहोस्_बाटो / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (बनाउनुहोस्_बाटो / 'programs.h').write_text('\n'.join(हेडर_मान) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(नाम for नाम, _ in 시험사례) + '\n')
    कार्यान्वयन_गर्नुहोस्_आदेश([시언어번역기] + 설정비트 + ['-c', बनाउनुहोस्_बाटो / 'programs.S', '-o', बनाउनुहोस्_बाटो / 'programs.o'])
