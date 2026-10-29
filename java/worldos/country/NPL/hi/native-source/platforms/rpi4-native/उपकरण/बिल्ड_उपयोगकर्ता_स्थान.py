"""독립된 निज ABI ELF64와 로더 अस्वीकृत_करें_मान 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from बिल्ड_सी_कंपाइलर import बनाएँ_सी_कंपाइलर


def बनाएँ_उपयोगकर्ता_स्थान(मूल_पथ, संग्रह_पथ, सी_कंपाइलर, 시플플번역기, 연결편집기, संग्रह_उपकरण, कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस, निष्पादित_करें_आदेश):
    कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस = [सेटिंग_मान for सेटिंग_मान in कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस if सेटिंग_मान != '-mgeneral-regs-only']
    बिल्ड_पथ = मूल_पथ / 'build'
    출력결과 = बिल्ड_पथ / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = मूल_पथ / 'उपयोगकर्ता'
    포직스경로 = संग्रह_पथ / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for कंपाइलर_उपकरण, 추가영역, पथ, नाम in [
            (सी_कंपाइलर, [], 원본자료 / 'चलाएँ.S', 'start.o'),
            (सी_कंपाइलर, ['-std=c11'], 원본자료 / 'निष्पादित_करें_आदेश.c', 'runtime.o'),
            (सी_कंपाइलर, ['-std=c11'], 포직스경로 / 'उपयोगकर्ता_ब्रिज.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'संचिकाउदाहरण.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (सी_कंपाइलर, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (सी_कंपाइलर, ['-std=c11'], 원본자료 / 'संपादक.c', 'vi.o')]:
        निष्पादित_करें_आदेश([कंपाइलर_उपकरण] + कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', पथ, '-o', 출력결과 / नाम])
    निष्पादित_करें_आदेश([संग्रह_उपकरण, 'rcs', बिल्ड_पथ / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for नाम in ('demo', 'fault', 'network', 'vi'):
        निष्पादित_करें_आदेश([연결편집기, '-T', 원본자료 / 'लिंक_लेआउट.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (नाम + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (नाम + '.o'), बिल्ड_पथ / 'libposix-kor-user.a'])
    자바라이브러리만들기(मूल_पथ, निष्पादित_करें_आदेश)
    # 기존 निज Java कंपाइलर/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(बिल्ड_पथ)) as 작업경로:
        कक्षा_पथ = Path(작업경로)
        निष्पादित_करें_आदेश(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', कक्षा_पथ, '-sourcepath', कक्षा_पथ, '-d', कक्षा_पथ] +
            [डेटा_पद for डेटा_पद in sorted((संग्रह_पथ / 'os/उपयोगकर्ता/자바').glob('*.java')) if डेटा_पद.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        निष्पादित_करें_आदेश(['sh', संग्रह_पथ / 'compiler/미리번역.sh', '--entry', 'उपकरण_एन्ट्री.चलाएँ',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(कक्षा_पथ.glob('*.class')))
    압축해제경로 = मूल_पथ / 'vendor/uzlib'
    for पथ, नाम in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'बंडल.c', 'jar.o')] + [(압축해제경로 / (नाम + '.c'), नाम + '.o') for नाम in ('tinflate', 'crc32', 'adler32')]:
        निष्पादित_करें_आदेश([सी_कंपाइलर] + कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', पथ, '-o', 출력결과 / नाम])
    निष्पादित_करें_आदेश([연결편집기, '-T', 원본자료 / 'लिंक_लेआउट.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / नाम for नाम in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(मूल_पथ, सी_कंपाइलर, 연결편집기)
    बनाएँ_सी_कंपाइलर(मूल_पथ, संग्रह_पथ, सी_कंपाइलर, 연결편집기, कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस, निष्पादित_करें_आदेश)
    वैध = (출력결과 / 'demo.elf').read_bytes()
    ऐप_हेडर_ऑफ़सेट = struct.unpack_from('<Q', वैध, 32)[0]
    हेडर_सूची = [ऐप_हेडर_ऑफ़सेट + 개수 * 56 for 개수 in range(struct.unpack_from('<H', वैध, 56)[0])]
    적재구획 = [डेटा_पद for डेटा_पद in हेडर_सूची if struct.unpack_from('<I', वैध, डेटा_पद)[0] == 1]
    पाठ, आँकड़े = 적재구획[:2]
    आदेश_पता = struct.unpack_from('<Q', वैध, पाठ + 16)[0]
    डेटा_पता = struct.unpack_from('<Q', वैध, आँकड़े + 16)[0]
    호출규약 = वैध.index(b'JKOROS\0')
    परिक्षण_विषय = [('empty', b''), ('short', वैध[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', आदेश_पता + 1), ('data-entry', 24, 'Q', डेटा_पता),
               ('outside-file', पाठ + 32, 'Q', len(वैध) + 1), ('short-memory', पाठ + 40, 'Q', 1),
               ('kernel-address', पाठ + 16, 'Q', 0x80000), ('memory-overflow', पाठ + 40, 'Q', 2**64 - 1),
               ('writable-code', पाठ + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', पाठ, 'I', 2),
               ('unaligned-load', पाठ + 16, 'Q', आदेश_पता + 8),
               ('overlap', आँकड़े + 16, 'Q', आदेश_पता)]
    for नाम, ऑफ़सेट_मान, डेटा_स्वरूप, मान in 수정사항:
        바뀐자료 = bytearray(वैध); struct.pack_into('<' + डेटा_स्वरूप, 바뀐자료, ऑफ़सेट_मान, मान)
        परिक्षण_विषय.append((नाम, bytes(바뀐자료)))
    탑재덩이들 = [(नाम.replace('-', '_'), 출력결과 / (नाम + '.elf')) for नाम in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for लुकअप_इंडेक्स, (नाम, पेलोड_डेटा) in enumerate(परिक्षण_विषय):
        पथ = 출력결과 / ('invalid-{}.elf'.format(नाम)); पथ.write_bytes(पेलोड_डेटा)
        탑재덩이들.append(('invalid_{}'.format(लुकअप_इंडेक्स), पथ))
    असेंबली, हेडर_मान = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for नाम, पथ in 탑재덩이들:
        प्रतीक_मान = 'user_blob_' + नाम
        크기목록[नाम] = पथ.stat().st_size
        # 생성한 पीअर_मान 경로만 넣어 프로젝트 경로의 공백/कोट 영향을 피한다.
        असेंबली += ['.balign 16', '.global ' + प्रतीक_मान, प्रतीक_मान + ':', '.incbin "{}"'.format(पथ.relative_to(मूल_पथ))]
        हेडर_मान.append('extern const unsigned char {}[];'.format(प्रतीक_मान))
    असेंबली.append('.section .note.GNU-stack,"",%progbits')
    हेडर_मान += ['static const ऐप 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    हेडर_मान += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    हेडर_मान += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    हेडर_मान += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], विधि_मोड) for विधि_मोड in (0, 1)]
    हेडर_मान += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    हेडर_मान += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    हेडर_मान += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    हेडर_मान += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    हेडर_मान += ['};', 'static const ऐप 잘못된실행항목들[] = {']
    हेडर_मान += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(पेलोड_डेटा)) for 순번, (_, पेलोड_डेटा) in enumerate(परिक्षण_विषय)]
    हेडर_मान += ['};']
    (बिल्ड_पथ / 'programs.S').write_text('\n'.join(असेंबली) + '\n')
    (बिल्ड_पथ / 'programs.h').write_text('\n'.join(हेडर_मान) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(नाम for नाम, _ in परिक्षण_विषय) + '\n')
    निष्पादित_करें_आदेश([सी_कंपाइलर] + कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस + ['-c', बिल्ड_पथ / 'programs.S', '-o', बिल्ड_पथ / 'programs.o'])
