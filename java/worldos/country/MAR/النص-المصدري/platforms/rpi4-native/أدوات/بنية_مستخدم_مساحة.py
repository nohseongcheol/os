"""독립된 ذاتي ABI ELF64와 로더 يرفض_قيمة اختبارات 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from بنية_الرمز_البريدي_محول_برمجي import فتح_الرمز_البريدي_محول_برمجي


def فتح_مستخدم_مساحة(جذر_مسار, مستودع_مسار, الرمز_البريدي_محول_برمجي, 시플플번역기, برنامج_ربط_أداة, أرشيف_أداة, تكوين_خدمة_النقل_الذكي_في_الخلفية, ينفذ_أمر):
    تكوين_خدمة_النقل_الذكي_في_الخلفية = [إعدادات_قيمة for إعدادات_قيمة in تكوين_خدمة_النقل_الذكي_في_الخلفية if إعدادات_قيمة != '-mgeneral-regs-only']
    بنية_مسار = جذر_مسار / 'build'
    الناتج = بنية_مسار / 'user'
    الناتج.mkdir(exist_ok=True)
    원본자료 = جذر_مسار / 'فضاء_المستخدم'
    포직스경로 = مستودع_مسار / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / 'تصريحات', '-I', الناتج]
    for محول_برمجي_أداة, 추가영역, مسار, اسم in [
            (الرمز_البريدي_محول_برمجي, [], 원본자료 / 'تشغيل.S', 'start.o'),
            (الرمز_البريدي_محول_برمجي, ['-std=c11'], 원본자료 / 'ينفذ_أمر.c', 'runtime.o'),
            (الرمز_البريدي_محول_برمجي, ['-std=c11'], 포직스경로 / 'مستخدم_جسر.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'مثالملف.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (الرمز_البريدي_محول_برمجي, ['-std=c11'], 원본자료 / 'حماية_يختبر.c', 'fault.o'),
            (الرمز_البريدي_محول_برمجي, ['-std=c11'], 원본자료 / 'محرر.c', 'vi.o')]:
        ينفذ_أمر([محول_برمجي_أداة] + تكوين_خدمة_النقل_الذكي_في_الخلفية + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', مسار, '-o', الناتج / اسم])
    ينفذ_أمر([أرشيف_أداة, 'rcs', بنية_مسار / 'libposix-kor-user.a', الناتج / 'posix.o'])
    for اسم in ('demo', 'fault', 'network', 'vi'):
        ينفذ_أمر([برنامج_ربط_أداة, '-T', 원본자료 / 'تخطيط_الربط.ld', '-z', 'max-page-size=4096', '-o', الناتج / (اسم + '.elf'),
             الناتج / 'start.o', الناتج / 'runtime.o', الناتج / (اسم + '.o'), بنية_مسار / 'libposix-kor-user.a'])
    자바라이브러리만들기(جذر_مسار, ينفذ_أمر)
    # 기존 ذاتي Java محول_برمجي/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(بنية_مسار)) as 작업경로:
        فئة_مسار = Path(작업경로)
        ينفذ_أمر(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', فئة_مسار, '-sourcepath', فئة_مسار, '-d', فئة_مسار] +
            [بيانات_منصب for بيانات_منصب in sorted((مستودع_مسار / 'os/فضاء_المستخدم/자바').glob('*.java')) if بيانات_منصب.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        ينفذ_أمر(['sh', مستودع_مسار / 'compiler/미리번역.sh', '--entry', 'أداة_إدخال.تشغيل',
             '--profile', 'user', '--heap-words', '1048576', '-o', الناتج / 'java-tools.c'] + sorted(فئة_مسار.glob('*.class')))
    압축해제경로 = جذر_مسار / 'vendor/uzlib'
    for مسار, اسم in [(الناتج / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'يُجمع.c', 'jar.o')] + [(압축해제경로 / (اسم + '.c'), اسم + '.o') for اسم in ('tinflate', 'crc32', 'adler32')]:
        ينفذ_أمر([الرمز_البريدي_محول_برمجي] + تكوين_خدمة_النقل_الذكي_في_الخلفية + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', مسار, '-o', الناتج / اسم])
    ينفذ_أمر([برنامج_ربط_أداة, '-T', 원본자료 / 'تخطيط_الربط.ld', '-z', 'max-page-size=4096', '-o', الناتج / 'java-tools.elf'] +
        [الناتج / اسم for اسم in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(جذر_مسار, الرمز_البريدي_محول_برمجي, برنامج_ربط_أداة)
    فتح_الرمز_البريدي_محول_برمجي(جذر_مسار, مستودع_مسار, الرمز_البريدي_محول_برمجي, برنامج_ربط_أداة, تكوين_خدمة_النقل_الذكي_في_الخلفية, ينفذ_أمر)
    유효함 = (الناتج / 'demo.elf').read_bytes()
    تطبيق_عنوان_إزاحة = struct.unpack_from('<Q', 유효함, 32)[0]
    عنوان_قائمة = [تطبيق_عنوان_إزاحة + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [بيانات_منصب for بيانات_منصب in عنوان_قائمة if struct.unpack_from('<I', 유효함, بيانات_منصب)[0] == 1]
    نص, بيانات = 적재구획[:2]
    أمر_عنوان = struct.unpack_from('<Q', 유효함, نص + 16)[0]
    بيانات_عنوان = struct.unpack_from('<Q', 유효함, بيانات + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    حالة_اختبار = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', أمر_عنوان + 1), ('data-entry', 24, 'Q', بيانات_عنوان),
               ('outside-file', نص + 32, 'Q', len(유효함) + 1), ('short-memory', نص + 40, 'Q', 1),
               ('kernel-address', نص + 16, 'Q', 0x80000), ('memory-overflow', نص + 40, 'Q', 2**64 - 1),
               ('writable-code', نص + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', نص, 'I', 2),
               ('unaligned-load', نص + 16, 'Q', أمر_عنوان + 8),
               ('overlap', بيانات + 16, 'Q', أمر_عنوان)]
    for اسم, إزاحة_قيمة, تنسيق, قيمة in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + تنسيق, 바뀐자료, إزاحة_قيمة, قيمة)
        حالة_اختبار.append((اسم, bytes(바뀐자료)))
    탑재덩이들 = [(اسم.replace('-', '_'), الناتج / (اسم + '.elf')) for اسم in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for البحث_فهرس, (اسم, حمولة_بيانات) in enumerate(حالة_اختبار):
        مسار = الناتج / ('invalid-{}.elf'.format(اسم)); مسار.write_bytes(حمولة_بيانات)
        탑재덩이들.append(('invalid_{}'.format(البحث_فهرس), مسار))
    تجميع, عنوان_قيمة_4a42eba5 = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for اسم, مسار in 탑재덩이들:
        رمز_قيمة = 'user_blob_' + اسم
        크기목록[اسم] = مسار.stat().st_size
        # 생성한 نظير_قيمة 경로만 넣어 프로젝트 경로의 공백/اقتباس 영향을 피한다.
        تجميع += ['.balign 16', '.global ' + رمز_قيمة, رمز_قيمة + ':', '.incbin "{}"'.format(مسار.relative_to(جذر_مسار))]
        عنوان_قيمة_4a42eba5.append('extern const unsigned char {}[];'.format(رمز_قيمة))
    تجميع.append('.section .note.GNU-stack,"",%progbits')
    عنوان_قيمة_4a42eba5 += ['static const تطبيق 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    عنوان_قيمة_4a42eba5 += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    عنوان_قيمة_4a42eba5 += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    عنوان_قيمة_4a42eba5 += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], أسلوب_الوضع) for أسلوب_الوضع in (0, 1)]
    عنوان_قيمة_4a42eba5 += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    عنوان_قيمة_4a42eba5 += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    عنوان_قيمة_4a42eba5 += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    عنوان_قيمة_4a42eba5 += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    عنوان_قيمة_4a42eba5 += ['};', 'static const تطبيق 잘못된실행항목들[] = {']
    عنوان_قيمة_4a42eba5 += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(حمولة_بيانات)) for 순번, (_, حمولة_بيانات) in enumerate(حالة_اختبار)]
    عنوان_قيمة_4a42eba5 += ['};']
    (بنية_مسار / 'programs.S').write_text('\n'.join(تجميع) + '\n')
    (بنية_مسار / 'programs.h').write_text('\n'.join(عنوان_قيمة_4a42eba5) + '\n')
    (الناتج / 'invalid-cases.txt').write_text('\n'.join(اسم for اسم, _ in حالة_اختبار) + '\n')
    ينفذ_أمر([الرمز_البريدي_محول_برمجي] + تكوين_خدمة_النقل_الذكي_في_الخلفية + ['-c', بنية_مسار / 'programs.S', '-o', بنية_مسار / 'programs.o'])
