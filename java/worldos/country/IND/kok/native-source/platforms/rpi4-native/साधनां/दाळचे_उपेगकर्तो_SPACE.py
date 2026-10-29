"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from दाळचे_PYTHON import निर्माण_करचें_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def निर्माण_करचें_उपेगकर्तो_SPACE(रूट_पाथ, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, संग्रह_साधन, 설정비트, पाळो_दिवचो_आदेश):
    설정비트 = [मांडावळी_मोल for मांडावळी_मोल in 설정비트 if मांडावळी_मोल != '-mgeneral-regs-only']
    दाळचे_पाथ = रूट_पाथ / 'build'
    출력결과 = दाळचे_पाथ / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = रूट_पाथ / 'उपेगकर्तो'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, पाथ, नांव in [
            (시언어번역기, [], 원본자료 / 'चलोवप.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'पाळो_दिवचो_आदेश.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'उपेगकर्तो_ब्रिज.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'संपादक.c', 'vi.o')]:
        पाळो_दिवचो_आदेश([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', पाथ, '-o', 출력결과 / नांव])
    पाळो_दिवचो_आदेश([संग्रह_साधन, 'rcs', दाळचे_पाथ / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for नांव in ('demo', 'fault', 'network', 'vi'):
        पाळो_दिवचो_आदेश([연결편집기, '-T', 원본자료 / 'लिंक_रचणाय.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (नांव + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (नांव + '.o'), दाळचे_पाथ / 'libposix-kor-user.a'])
    자바라이브러리만들기(रूट_पाथ, पाळो_दिवचो_आदेश)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(दाळचे_पाथ)) as 작업경로:
        वर्ग_पाथ = Path(작업경로)
        पाळो_दिवचो_आदेश(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', वर्ग_पाथ, '-sourcepath', वर्ग_पाथ, '-d', वर्ग_पाथ] +
            [डेटा_स्थिती for डेटा_स्थिती in sorted((저장소경로 / 'os/उपेगकर्तो/자바').glob('*.java')) if डेटा_स्थिती.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        पाळो_दिवचो_आदेश(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'साधन_प्रवेश.चलोवप',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(वर्ग_पाथ.glob('*.class')))
    압축해제경로 = रूट_पाथ / 'vendor/uzlib'
    for पाथ, नांव in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'रास.c', 'jar.o')] + [(압축해제경로 / (नांव + '.c'), नांव + '.o') for नांव in ('tinflate', 'crc32', 'adler32')]:
        पाळो_दिवचो_आदेश([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', पाथ, '-o', 출력결과 / नांव])
    पाळो_दिवचो_आदेश([연결편집기, '-T', 원본자료 / 'लिंक_रचणाय.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / नांव for नांव in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    निर्माण_करचें_PYTHON(रूट_पाथ, 시언어번역기, 연결편집기)
    시언어번역기만들기(रूट_पाथ, 저장소경로, 시언어번역기, 연결편집기, 설정비트, पाळो_दिवचो_आदेश)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    एप्लिकेशन_माथाळो_ऑफसॅट = struct.unpack_from('<Q', 유효함, 32)[0]
    माथाळो_सुची = [एप्लिकेशन_माथाळो_ऑफसॅट + आयटम_COUNT * 56 for आयटम_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [डेटा_स्थिती for डेटा_स्थिती in माथाळो_सुची if struct.unpack_from('<I', 유효함, डेटा_स्थिती)[0] == 1]
    SMS, डेटा = 적재구획[:2]
    आदेश_नामो = struct.unpack_from('<Q', 유효함, SMS + 16)[0]
    डेटा_नामो = struct.unpack_from('<Q', 유효함, डेटा + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', आदेश_नामो + 1), ('data-entry', 24, 'Q', डेटा_नामो),
               ('outside-file', SMS + 32, 'Q', len(유효함) + 1), ('short-memory', SMS + 40, 'Q', 1),
               ('kernel-address', SMS + 16, 'Q', 0x80000), ('memory-overflow', SMS + 40, 'Q', 2**64 - 1),
               ('writable-code', SMS + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', SMS, 'I', 2),
               ('unaligned-load', SMS + 16, 'Q', आदेश_नामो + 8),
               ('overlap', डेटा + 16, 'Q', आदेश_नामो)]
    for नांव, ऑफसॅट_मोल, स्वरूप_932e03c8, मोल in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + स्वरूप_932e03c8, 바뀐자료, ऑफसॅट_मोल, मोल)
        시험사례.append((नांव, bytes(바뀐자료)))
    탑재덩이들 = [(नांव.replace('-', '_'), 출력결과 / (नांव + '.elf')) for नांव in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for लूकअप_INDEX, (नांव, पेलोड_डेटा) in enumerate(시험사례):
        पाथ = 출력결과 / ('invalid-{}.elf'.format(नांव)); पाथ.write_bytes(पेलोड_डेटा)
        탑재덩이들.append(('invalid_{}'.format(लूकअप_INDEX), पाथ))
    어셈블리자료, माथाळो_मोल = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for नांव, पाथ in 탑재덩이들:
        चिन्न_मोल = 'user_blob_' + नांव
        크기목록[नांव] = पाथ.stat().st_size
        # 생성한 पीयर_मोल 경로만 넣어 프로젝트 경로의 공백/उतारो 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + चिन्न_मोल, चिन्न_मोल + ':', '.incbin "{}"'.format(पाथ.relative_to(रूट_पाथ))]
        माथाळो_मोल.append('extern const unsigned char {}[];'.format(चिन्न_मोल))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    माथाळो_मोल += ['static const एप्लिकेशन 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    माथाळो_मोल += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    माथाळो_मोल += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    माथाळो_मोल += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], पद्दत_मोड) for पद्दत_मोड in (0, 1)]
    माथाळो_मोल += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    माथाळो_मोल += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    माथाळो_मोल += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    माथाळो_मोल += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    माथाळो_मोल += ['};', 'static const एप्लिकेशन 잘못된실행항목들[] = {']
    माथाळो_मोल += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(पेलोड_डेटा)) for 순번, (_, पेलोड_डेटा) in enumerate(시험사례)]
    माथाळो_मोल += ['};']
    (दाळचे_पाथ / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (दाळचे_पाथ / 'programs.h').write_text('\n'.join(माथाळो_मोल) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(नांव for नांव, _ in 시험사례) + '\n')
    पाळो_दिवचो_आदेश([시언어번역기] + 설정비트 + ['-c', दाळचे_पाथ / 'programs.S', '-o', दाळचे_पाथ / 'programs.o'])
