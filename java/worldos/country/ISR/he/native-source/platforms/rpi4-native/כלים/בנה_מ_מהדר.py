"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def ליצור_מ_מהדר(בסיס_נתיב, מאגר_נתיב, מ_מהדר, 연결편집기, 설정비트, לבצע_פקודה):
    תוצאה_נתונים = בסיס_נתיב / 'build/ccompiler'; תוצאה_נתונים.mkdir(exist_ok=True)
    원본자료 = בסיס_נתיב / 'מ_מהדר'
    במעלה = בסיס_נתיב / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    ערכת_פיתוח = בסיס_נתיב / 'vendor/sdk'
    if not (ערכת_פיתוח/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((ערכת_פיתוח/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [הגדרות_ערך for הגדרות_ערך in 설정비트 if הגדרות_ערך != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', במעלה, '-I', בסיס_נתיב/'משתמש', '-I', תוצאה_נתונים, '-isystem', ערכת_פיתוח/'usr/include']
    לבצע_פקודה([מ_מהדר]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'시작지원.c','-o',תוצאה_נתונים/'crt.o'])
    לבצע_פקודה([מ_מהדר]+설정비트+['-I',מאגר_נתיב/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'עץ_אובייקטי_יישומים_זמן_ריצה.c','-o',תוצאה_נתונים/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+נתונים_עמדה.name,נתונים_עמדה) for נתונים_עמדה in sorted((מאגר_נתיב/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+נתונים_עמדה.name,נתונים_עמדה) for נתונים_עמדה in sorted((במעלה/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+נתונים_עמדה.name,נתונים_עמדה) for נתונים_עמדה in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',בסיס_נתיב/'build/user/start.o'),('/sdk/lib/crt.o',תוצאה_נתונים/'crt.o'),('/sdk/lib/aot-runtime.o',תוצאה_נתונים/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',בסיס_נתיב/'build/libposix-kor-user.a')]
    כותרת_ערך=['typedef struct { const char *שם; const unsigned char *נתונים; unsigned גודל; } מהדר_משאב;']
    for 순번,(_,נתיב) in enumerate(탑재자료):
        כותרת_ערך.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in נתיב.read_bytes())))
    כותרת_ערך.append('static const מהדר_משאב מהדר_משאבים[] = {')
    for 순번,(שם,נתיב) in enumerate(탑재자료): כותרת_ערך.append('{%s, 탑재자원_%d, %d},'%(json.dumps(שם,ensure_ascii=False),순번,נתיב.stat().st_size))
    כותרת_ערך.append('};');(תוצאה_נתונים/'resources.h').write_text('\n'.join(כותרת_ערך)+'\n',encoding='utf-8')
    יעד_קבצים=[]
    for שם in ('מהדר_כלי.c','זמן_ריצה_תמך.c','הפעלה.c','미리번역.c','החזר_גשר.S'):
        קובץ_יעד_ffac9b48=תוצאה_נתונים/(Path(שם).stem+'.o');יעד_קבצים.append(קובץ_יעד_ffac9b48)
        לבצע_פקודה([מ_מהדר]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/שם,'-o',קובץ_יעד_ffac9b48])
    실행파일=בסיס_נתיב/'build/user/cc.elf'
    לבצע_פקודה([연결편집기,'--gc-sections','-T',בסיס_נתיב/'משתמש/לקשר_ניווט.ld','-z','max-page-size=4096','-o',실행파일,
         בסיס_נתיב/'build/user/start.o',בסיס_נתיב/'build/user/runtime.o']+יעד_קבצים+
         [בסיס_נתיב/'build/user'/שם for שם in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
