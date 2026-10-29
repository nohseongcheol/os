"""독립된 עצמי ABI ELF64와 로더 דחייה_ערך 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from בנה_מ_מהדר import ליצור_מ_מהדר


def ליצור_משתמש_חלל(בסיס_נתיב, מאגר_נתיב, מ_מהדר, 시플플번역기, 연결편집기, ארכיון_כלי, 설정비트, לבצע_פקודה):
    설정비트 = [הגדרות_ערך for הגדרות_ערך in 설정비트 if הגדרות_ערך != '-mgeneral-regs-only']
    בנה_נתיב = בסיס_נתיב / 'build'
    פלט = בנה_נתיב / 'user'
    פלט.mkdir(exist_ok=True)
    원본자료 = בסיס_נתיב / 'משתמש'
    포직스경로 = מאגר_נתיב / 'posix-kor/arm64-native'
    לכלול_נתיב = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', פלט]
    for מהדר_כלי, 추가영역, נתיב, שם in [
            (מ_מהדר, [], 원본자료 / 'הפעלה.S', 'start.o'),
            (מ_מהדר, ['-std=c11'], 원본자료 / 'לבצע_פקודה.c', 'runtime.o'),
            (מ_מהדר, ['-std=c11'], 포직스경로 / 'משתמש_גשר.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'דוגמתקובץ.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (מ_מהדר, ['-std=c11'], 원본자료 / 'הגנה_נסה.c', 'fault.o'),
            (מ_מהדר, ['-std=c11'], 원본자료 / 'עורך.c', 'vi.o')]:
        לבצע_פקודה([מהדר_כלי] + 설정비트 + 추가영역 + לכלול_נתיב + ['-Wall', '-Wextra', '-Werror', '-c', נתיב, '-o', פלט / שם])
    לבצע_פקודה([ארכיון_כלי, 'rcs', בנה_נתיב / 'libposix-kor-user.a', פלט / 'posix.o'])
    for שם in ('demo', 'fault', 'network', 'vi'):
        לבצע_פקודה([연결편집기, '-T', 원본자료 / 'לקשר_ניווט.ld', '-z', 'max-page-size=4096', '-o', פלט / (שם + '.elf'),
             פלט / 'start.o', פלט / 'runtime.o', פלט / (שם + '.o'), בנה_נתיב / 'libposix-kor-user.a'])
    자바라이브러리만들기(בסיס_נתיב, לבצע_פקודה)
    # 기존 עצמי Java מהדר/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(בנה_נתיב)) as 작업경로:
        כיתה_נתיב = Path(작업경로)
        לבצע_פקודה(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', כיתה_נתיב, '-sourcepath', כיתה_נתיב, '-d', כיתה_נתיב] +
            [נתונים_עמדה for נתונים_עמדה in sorted((מאגר_נתיב / 'os/משתמש/자바').glob('*.java')) if נתונים_עמדה.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        לבצע_פקודה(['sh', מאגר_נתיב / 'compiler/미리번역.sh', '--entry', 'כלי_ערך.הפעלה',
             '--profile', 'user', '--heap-words', '1048576', '-o', פלט / 'java-tools.c'] + sorted(כיתה_נתיב.glob('*.class')))
    압축해제경로 = בסיס_נתיב / 'vendor/uzlib'
    for נתיב, שם in [(פלט / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'חבילה.c', 'jar.o')] + [(압축해제경로 / (שם + '.c'), שם + '.o') for שם in ('tinflate', 'crc32', 'adler32')]:
        לבצע_פקודה([מ_מהדר] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + לכלול_נתיב + ['-c', נתיב, '-o', פלט / שם])
    לבצע_פקודה([연결편집기, '-T', 원본자료 / 'לקשר_ניווט.ld', '-z', 'max-page-size=4096', '-o', פלט / 'java-tools.elf'] +
        [פלט / שם for שם in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(בסיס_נתיב, מ_מהדר, 연결편집기)
    ליצור_מ_מהדר(בסיס_נתיב, מאגר_נתיב, מ_מהדר, 연결편집기, 설정비트, לבצע_פקודה)
    유효함 = (פלט / 'demo.elf').read_bytes()
    תוכנית_כותרת_היסט = struct.unpack_from('<Q', 유효함, 32)[0]
    כותרת_רשימה = [תוכנית_כותרת_היסט + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [נתונים_עמדה for נתונים_עמדה in כותרת_רשימה if struct.unpack_from('<I', 유효함, נתונים_עמדה)[0] == 1]
    טקסט, נתונים = 적재구획[:2]
    פקודה_למען = struct.unpack_from('<Q', 유효함, טקסט + 16)[0]
    נתונים_למען = struct.unpack_from('<Q', 유효함, נתונים + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    מפרט_בדיקה = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', פקודה_למען + 1), ('data-entry', 24, 'Q', נתונים_למען),
               ('outside-file', טקסט + 32, 'Q', len(유효함) + 1), ('short-memory', טקסט + 40, 'Q', 1),
               ('kernel-address', טקסט + 16, 'Q', 0x80000), ('memory-overflow', טקסט + 40, 'Q', 2**64 - 1),
               ('writable-code', טקסט + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', טקסט, 'I', 2),
               ('unaligned-load', טקסט + 16, 'Q', פקודה_למען + 8),
               ('overlap', נתונים + 16, 'Q', פקודה_למען)]
    for שם, היסט_ערך, עיצוב, ערך in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + עיצוב, 바뀐자료, היסט_ערך, ערך)
        מפרט_בדיקה.append((שם, bytes(바뀐자료)))
    탑재덩이들 = [(שם.replace('-', '_'), פלט / (שם + '.elf')) for שם in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for חפושׂ_מדד, (שם, מטען_נתונים) in enumerate(מפרט_בדיקה):
        נתיב = פלט / ('invalid-{}.elf'.format(שם)); נתיב.write_bytes(מטען_נתונים)
        탑재덩이들.append(('invalid_{}'.format(חפושׂ_מדד), נתיב))
    הרכבה, כותרת_ערך = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for שם, נתיב in 탑재덩이들:
        סימן_ערך = 'user_blob_' + שם
        크기목록[שם] = נתיב.stat().st_size
        # 생성한 עמית_ערך 경로만 넣어 프로젝트 경로의 공백/ציטוט 영향을 피한다.
        הרכבה += ['.balign 16', '.global ' + סימן_ערך, סימן_ערך + ':', '.incbin "{}"'.format(נתיב.relative_to(בסיס_נתיב))]
        כותרת_ערך.append('extern const unsigned char {}[];'.format(סימן_ערך))
    הרכבה.append('.section .note.GNU-stack,"",%progbits')
    כותרת_ערך += ['static const תוכנית 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    כותרת_ערך += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    כותרת_ערך += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    כותרת_ערך += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], פעולת_שירות_מצב) for פעולת_שירות_מצב in (0, 1)]
    כותרת_ערך += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    כותרת_ערך += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    כותרת_ערך += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    כותרת_ערך += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    כותרת_ערך += ['};', 'static const תוכנית 잘못된실행항목들[] = {']
    כותרת_ערך += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(מטען_נתונים)) for 순번, (_, מטען_נתונים) in enumerate(מפרט_בדיקה)]
    כותרת_ערך += ['};']
    (בנה_נתיב / 'programs.S').write_text('\n'.join(הרכבה) + '\n')
    (בנה_נתיב / 'programs.h').write_text('\n'.join(כותרת_ערך) + '\n')
    (פלט / 'invalid-cases.txt').write_text('\n'.join(שם for שם, _ in מפרט_בדיקה) + '\n')
    לבצע_פקודה([מ_מהדר] + 설정비트 + ['-c', בנה_נתיב / 'programs.S', '-o', בנה_נתיב / 'programs.o'])
