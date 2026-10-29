"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def فتح_الرمز_البريدي_محول_برمجي(جذر_مسار, مستودع_مسار, الرمز_البريدي_محول_برمجي, برنامج_ربط_أداة, تكوين_خدمة_النقل_الذكي_في_الخلفية, ينفذ_أمر):
    مقياس_بيانات = جذر_مسار / 'build/ccompiler'; مقياس_بيانات.mkdir(exist_ok=True)
    원본자료 = جذر_مسار / 'الرمز_البريدي_محول_برمجي'
    المصدر = جذر_مسار / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    أداة_التطوير = جذر_مسار / 'vendor/sdk'
    if not (أداة_التطوير/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((أداة_التطوير/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    تكوين_خدمة_النقل_الذكي_في_الخلفية = [إعدادات_قيمة for إعدادات_قيمة in تكوين_خدمة_النقل_الذكي_في_الخلفية if إعدادات_قيمة != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', المصدر, '-I', جذر_مسار/'فضاء_المستخدم', '-I', مقياس_بيانات, '-isystem', أداة_التطوير/'usr/include']
    ينفذ_أمر([الرمز_البريدي_محول_برمجي]+تكوين_خدمة_النقل_الذكي_في_الخلفية+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'بدء_التشغيل_دعم.c','-o',مقياس_بيانات/'crt.o'])
    ينفذ_أمر([الرمز_البريدي_محول_برمجي]+تكوين_خدمة_النقل_الذكي_في_الخلفية+['-I',مستودع_مسار/'posix-kor/arm64-native/تصريحات']+포함인수+['-c',원본자료/'شجرة_مكونات_البرنامج_وقت_التشغيل.c','-o',مقياس_بيانات/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+بيانات_منصب.name,بيانات_منصب) for بيانات_منصب in sorted((مستودع_مسار/'posix-kor/arm64-native/تصريحات').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+بيانات_منصب.name,بيانات_منصب) for بيانات_منصب in sorted((المصدر/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+بيانات_منصب.name,بيانات_منصب) for بيانات_منصب in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',جذر_مسار/'build/user/start.o'),('/sdk/lib/crt.o',مقياس_بيانات/'crt.o'),('/sdk/lib/aot-runtime.o',مقياس_بيانات/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',جذر_مسار/'build/libposix-kor-user.a')]
    عنوان_قيمة_4a42eba5=['typedef struct { const char *اسم; const unsigned char *بيانات; unsigned حجم; } محول_برمجي_مصدر;']
    for 순번,(_,مسار) in enumerate(탑재자료):
        عنوان_قيمة_4a42eba5.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in مسار.read_bytes())))
    عنوان_قيمة_4a42eba5.append('static const محول_برمجي_مصدر محول_برمجي_المصادر[] = {')
    for 순번,(اسم,مسار) in enumerate(탑재자료): عنوان_قيمة_4a42eba5.append('{%s, 탑재자원_%d, %d},'%(json.dumps(اسم,ensure_ascii=False),순번,مسار.stat().st_size))
    عنوان_قيمة_4a42eba5.append('};');(مقياس_بيانات/'resources.h').write_text('\n'.join(عنوان_قيمة_4a42eba5)+'\n',encoding='utf-8')
    وجهة_الملفات=[]
    for اسم in ('محول_برمجي_أداة.c','دعمتشغيل.c','تشغيل.c','미리번역.c','إرجاع_جسر.S'):
        الملف_الوجهة=مقياس_بيانات/(Path(اسم).stem+'.o');وجهة_الملفات.append(الملف_الوجهة)
        ينفذ_أمر([الرمز_البريدي_محول_برمجي]+تكوين_خدمة_النقل_الذكي_في_الخلفية+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/اسم,'-o',الملف_الوجهة])
    실행파일=جذر_مسار/'build/user/cc.elf'
    ينفذ_أمر([برنامج_ربط_أداة,'--gc-sections','-T',جذر_مسار/'فضاء_المستخدم/تخطيط_الربط.ld','-z','max-page-size=4096','-o',실행파일,
         جذر_مسار/'build/user/start.o',جذر_مسار/'build/user/runtime.o']+وجهة_الملفات+
         [جذر_مسار/'build/user'/اسم for اسم in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
