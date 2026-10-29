"""독립된 بومی ABI ELF64와 로더 رد_کردن_مقدار 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def ایجاد_کاربر_فضا(جذر_مسیر, مخزن_مسیر, 시언어번역기, 시플플번역기, 연결편집기, آرشیو_ابزار, 설정비트, اجرا_فرمان):
    설정비트 = [تنظیمات_مقدار for تنظیمات_مقدار in 설정비트 if تنظیمات_مقدار != '-mgeneral-regs-only']
    ساخت_مسیر = جذر_مسیر / 'build'
    출력결과 = ساخت_مسیر / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = جذر_مسیر / 'کاربر'
    포직스경로 = مخزن_مسیر / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, مسیر, نام in [
            (시언어번역기, [], 원본자료 / 'اجرا_2.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'اجرا_فرمان.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'کاربر_پل.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'نمونهپرونده.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ویرایشگر.c', 'vi.o')]:
        اجرا_فرمان([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', مسیر, '-o', 출력결과 / نام])
    اجرا_فرمان([آرشیو_ابزار, 'rcs', ساخت_مسیر / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for نام in ('demo', 'fault', 'network', 'vi'):
        اجرا_فرمان([연결편집기, '-T', 원본자료 / 'پیوند_پیمایش.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (نام + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (نام + '.o'), ساخت_مسیر / 'libposix-kor-user.a'])
    자바라이브러리만들기(جذر_مسیر, اجرا_فرمان)
    # 기존 بومی Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(ساخت_مسیر)) as 작업경로:
        کلاس_مسیر = Path(작업경로)
        اجرا_فرمان(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', کلاس_مسیر, '-sourcepath', کلاس_مسیر, '-d', کلاس_مسیر] +
            [داده_ها_مرتب_کردن for داده_ها_مرتب_کردن in sorted((مخزن_مسیر / 'os/کاربر/자바').glob('*.java')) if داده_ها_مرتب_کردن.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        اجرا_فرمان(['sh', مخزن_مسیر / 'compiler/미리번역.sh', '--entry', 'ابزار_ورودی.اجرا_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(کلاس_مسیر.glob('*.class')))
    압축해제경로 = جذر_مسیر / 'vendor/uzlib'
    for مسیر, نام in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'دسته_کردن.c', 'jar.o')] + [(압축해제경로 / (نام + '.c'), نام + '.o') for نام in ('tinflate', 'crc32', 'adler32')]:
        اجرا_فرمان([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', مسیر, '-o', 출력결과 / نام])
    اجرا_فرمان([연결편집기, '-T', 원본자료 / 'پیوند_پیمایش.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / نام for نام in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(جذر_مسیر, 시언어번역기, 연결편집기)
    시언어번역기만들기(جذر_مسیر, مخزن_مسیر, 시언어번역기, 연결편집기, 설정비트, اجرا_فرمان)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    برنامه_سرصفحه_جابجایی_لایه_ای = struct.unpack_from('<Q', 유효함, 32)[0]
    سرصفحه_لیست = [برنامه_سرصفحه_جابجایی_لایه_ای + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [داده_ها_مرتب_کردن for داده_ها_مرتب_کردن in سرصفحه_لیست if struct.unpack_from('<I', 유효함, داده_ها_مرتب_کردن)[0] == 1]
    متن, داده_ها = 적재구획[:2]
    فرمان_آدرس = struct.unpack_from('<Q', 유효함, متن + 16)[0]
    داده_ها_آدرس = struct.unpack_from('<Q', 유효함, داده_ها + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', فرمان_آدرس + 1), ('data-entry', 24, 'Q', داده_ها_آدرس),
               ('outside-file', متن + 32, 'Q', len(유효함) + 1), ('short-memory', متن + 40, 'Q', 1),
               ('kernel-address', متن + 16, 'Q', 0x80000), ('memory-overflow', متن + 40, 'Q', 2**64 - 1),
               ('writable-code', متن + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', متن, 'I', 2),
               ('unaligned-load', متن + 16, 'Q', فرمان_آدرس + 8),
               ('overlap', داده_ها + 16, 'Q', فرمان_آدرس)]
    for نام, جابجایی_لایه_ای_مقدار, قالب_932e03c8, مقدار in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + قالب_932e03c8, 바뀐자료, جابجایی_لایه_ای_مقدار, مقدار)
        시험사례.append((نام, bytes(바뀐자료)))
    탑재덩이들 = [(نام.replace('-', '_'), 출력결과 / (نام + '.elf')) for نام in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for جستجو_فهرست, (نام, داده_های_ضروری_داده_ها) in enumerate(시험사례):
        مسیر = 출력결과 / ('invalid-{}.elf'.format(نام)); مسیر.write_bytes(داده_های_ضروری_داده_ها)
        탑재덩이들.append(('invalid_{}'.format(جستجو_فهرست), مسیر))
    어셈블리자료, سرصفحه_مقدار = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for نام, مسیر in 탑재덩이들:
        نماد_مقدار = 'user_blob_' + نام
        크기목록[نام] = مسیر.stat().st_size
        # 생성한 مشابه_مقدار 경로만 넣어 프로젝트 경로의 공백/نقل_قول 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + نماد_مقدار, نماد_مقدار + ':', '.incbin "{}"'.format(مسیر.relative_to(جذر_مسیر))]
        سرصفحه_مقدار.append('extern const unsigned char {}[];'.format(نماد_مقدار))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    سرصفحه_مقدار += ['static const برنامه 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    سرصفحه_مقدار += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    سرصفحه_مقدار += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    سرصفحه_مقدار += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], روش_حالت) for روش_حالت in (0, 1)]
    سرصفحه_مقدار += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    سرصفحه_مقدار += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    سرصفحه_مقدار += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    سرصفحه_مقدار += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    سرصفحه_مقدار += ['};', 'static const برنامه 잘못된실행항목들[] = {']
    سرصفحه_مقدار += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(داده_های_ضروری_داده_ها)) for 순번, (_, داده_های_ضروری_داده_ها) in enumerate(시험사례)]
    سرصفحه_مقدار += ['};']
    (ساخت_مسیر / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (ساخت_مسیر / 'programs.h').write_text('\n'.join(سرصفحه_مقدار) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(نام for نام, _ in 시험사례) + '\n')
    اجرا_فرمان([시언어번역기] + 설정비트 + ['-c', ساخت_مسیر / 'programs.S', '-o', ساخت_مسیر / 'programs.o'])
