"""독립된 자체 ABI ELF64와 로더 አትቀበል_እሴት 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def ፍጠር_ተጠቃሚ_ቦታ(ስር_ዱካ, ማከማቻ_ዱካ, 시언어번역기, 시플플번역기, 연결편집기, ከዝን_መሳሪያ, ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት, ፈጽም_ትእዛዝ):
    ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት = [ቅንብሮች_እሴት for ቅንብሮች_እሴት in ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት if ቅንብሮች_እሴት != '-mgeneral-regs-only']
    ግንብ_ዱካ = ስር_ዱካ / 'build'
    출력결과 = ግንብ_ዱካ / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = ስር_ዱካ / 'ተጠቃሚ'
    포직스경로 = ማከማቻ_ዱካ / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, መተላለፊያ, ስም in [
            (시언어번역기, [], 원본자료 / 'ማስኬጃ.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ፈጽም_ትእዛዝ.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'ተጠቃሚ_ድልድይ.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'አርታዒ.c', 'vi.o')]:
        ፈጽም_ትእዛዝ([번역기] + ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', መተላለፊያ, '-o', 출력결과 / ስም])
    ፈጽም_ትእዛዝ([ከዝን_መሳሪያ, 'rcs', ግንብ_ዱካ / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for ስም in ('demo', 'fault', 'network', 'vi'):
        ፈጽም_ትእዛዝ([연결편집기, '-T', 원본자료 / 'አገናኝ_አሰሳ.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (ስም + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (ስም + '.o'), ግንብ_ዱካ / 'libposix-kor-user.a'])
    자바라이브러리만들기(ስር_ዱካ, ፈጽም_ትእዛዝ)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(ግንብ_ዱካ)) as 작업경로:
        መደብ_ዱካ = Path(작업경로)
        ፈጽም_ትእዛዝ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', መደብ_ዱካ, '-sourcepath', መደብ_ዱካ, '-d', መደብ_ዱካ] +
            [ውሂብ_በቦታ_አስቀመጠ for ውሂብ_በቦታ_አስቀመጠ in sorted((ማከማቻ_ዱካ / 'os/ተጠቃሚ/자바').glob('*.java')) if ውሂብ_በቦታ_አስቀመጠ.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        ፈጽም_ትእዛዝ(['sh', ማከማቻ_ዱካ / 'compiler/미리번역.sh', '--entry', 'መሳሪያ_ምዝግብ.ማስኬጃ',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(መደብ_ዱካ.glob('*.class')))
    압축해제경로 = ስር_ዱካ / 'vendor/uzlib'
    for መተላለፊያ, ስም in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'ቀርቅብ.c', 'jar.o')] + [(압축해제경로 / (ስም + '.c'), ስም + '.o') for ስም in ('tinflate', 'crc32', 'adler32')]:
        ፈጽም_ትእዛዝ([시언어번역기] + ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', መተላለፊያ, '-o', 출력결과 / ስም])
    ፈጽም_ትእዛዝ([연결편집기, '-T', 원본자료 / 'አገናኝ_አሰሳ.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / ስም for ስም in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(ስር_ዱካ, 시언어번역기, 연결편집기)
    시언어번역기만들기(ስር_ዱካ, ማከማቻ_ዱካ, 시언어번역기, 연결편집기, ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት, ፈጽም_ትእዛዝ)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    ፕሮግራም_ርእስ_ዝንፍ = struct.unpack_from('<Q', 유효함, 32)[0]
    ርእስ_ዝርዝር = [ፕሮግራም_ርእስ_ዝንፍ + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [ውሂብ_በቦታ_አስቀመጠ for ውሂብ_በቦታ_አስቀመጠ in ርእስ_ዝርዝር if struct.unpack_from('<I', 유효함, ውሂብ_በቦታ_አስቀመጠ)[0] == 1]
    ጽሁፍ, ውሂብ = 적재구획[:2]
    ትእዛዝ_አድራሻ = struct.unpack_from('<Q', 유효함, ጽሁፍ + 16)[0]
    ውሂብ_አድራሻ = struct.unpack_from('<Q', 유효함, ውሂብ + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', ትእዛዝ_አድራሻ + 1), ('data-entry', 24, 'Q', ውሂብ_አድራሻ),
               ('outside-file', ጽሁፍ + 32, 'Q', len(유효함) + 1), ('short-memory', ጽሁፍ + 40, 'Q', 1),
               ('kernel-address', ጽሁፍ + 16, 'Q', 0x80000), ('memory-overflow', ጽሁፍ + 40, 'Q', 2**64 - 1),
               ('writable-code', ጽሁፍ + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', ጽሁፍ, 'I', 2),
               ('unaligned-load', ጽሁፍ + 16, 'Q', ትእዛዝ_አድራሻ + 8),
               ('overlap', ውሂብ + 16, 'Q', ትእዛዝ_አድራሻ)]
    for ስም, ዝንፍ_እሴት, ቅርጸት_932e03c8, እሴት in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + ቅርጸት_932e03c8, 바뀐자료, ዝንፍ_እሴት, እሴት)
        시험사례.append((ስም, bytes(바뀐자료)))
    탑재덩이들 = [(ስም.replace('-', '_'), 출력결과 / (ስም + '.elf')) for ስም in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for ፍለጋ_መረጃ_ጠቆመ, (ስም, የክፍያ_ጫና_ውሂብ) in enumerate(시험사례):
        መተላለፊያ = 출력결과 / ('invalid-{}.elf'.format(ስም)); መተላለፊያ.write_bytes(የክፍያ_ጫና_ውሂብ)
        탑재덩이들.append(('invalid_{}'.format(ፍለጋ_መረጃ_ጠቆመ), መተላለፊያ))
    어셈블리자료, ርእስ_እሴት = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for ስም, መተላለፊያ in 탑재덩이들:
        ምልክት_እሴት = 'user_blob_' + ስም
        크기목록[ስም] = መተላለፊያ.stat().st_size
        # 생성한 አቻ_እሴት 경로만 넣어 프로젝트 경로의 공백/ጥቅስ 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + ምልክት_እሴት, ምልክት_እሴት + ':', '.incbin "{}"'.format(መተላለፊያ.relative_to(ስር_ዱካ))]
        ርእስ_እሴት.append('extern const unsigned char {}[];'.format(ምልክት_እሴት))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    ርእስ_እሴት += ['static const ፕሮግራም 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    ርእስ_እሴት += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    ርእስ_እሴት += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    ርእስ_እሴት += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], ስልት_ሁነታ) for ስልት_ሁነታ in (0, 1)]
    ርእስ_እሴት += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    ርእስ_እሴት += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    ርእስ_እሴት += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    ርእስ_እሴት += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    ርእስ_እሴት += ['};', 'static const ፕሮግራም 잘못된실행항목들[] = {']
    ርእስ_እሴት += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(የክፍያ_ጫና_ውሂብ)) for 순번, (_, የክፍያ_ጫና_ውሂብ) in enumerate(시험사례)]
    ርእስ_እሴት += ['};']
    (ግንብ_ዱካ / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (ግንብ_ዱካ / 'programs.h').write_text('\n'.join(ርእስ_እሴት) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(ስም for ስም, _ in 시험사례) + '\n')
    ፈጽም_ትእዛዝ([시언어번역기] + ውቅረት_የበስተጀርባ_ብልህ_የማስተላለፍ_አገልግሎት + ['-c', ግንብ_ዱካ / 'programs.S', '-o', ግንብ_ዱካ / 'programs.o'])
