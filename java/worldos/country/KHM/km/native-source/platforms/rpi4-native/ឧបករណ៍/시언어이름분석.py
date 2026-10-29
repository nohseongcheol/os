#!/usr/bin/env python3
"""libclang ការប្រកាស·យោង 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

បញ្ចាំង_ឬស = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class សំនុំអក្សរ_តំលៃ(씨.Structure): _fields_ = [('ទិន្នន័យ',씨.c_void_p),('បង្ហាញ_តំលៃ',씨.c_uint)]
class បន្ទាត់ឈរភ្លឹបភ្លែត_តំលៃ(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('ទិន្នន័យ',씨.c_void_p*3)]
class កំណត់ទីតាំង(씨.Structure): _fields_ = [('ទិន្នន័យ',씨.c_void_p*2),('ការបែង_ភាគ_តំលៃ',씨.c_uint)]
def អនុគមន៍_តំលៃ(ឈ្មោះ, 반환, *អាគុយម៉ង់):
    ការបញ្ចូល_តំលៃ = getattr(구현, ឈ្មោះ); ការបញ្ចូល_តំលៃ.restype = 반환; ការបញ្ចូល_តំលៃ.argtypes = list(អាគុយម៉ង់); return ការបញ្ចូល_តំលៃ
ទាញ_អត្ថបទ = អនុគមន៍_តំលៃ('clang_getCString',씨.c_char_p,សំនុំអក្សរ_តំលៃ)
លែង_អត្ថបទ = អនុគមន៍_តំលៃ('clang_disposeString',None,សំនុំអក្សរ_តំលៃ)
def អត្ថបទ(តំលៃ):
    ការវាស់វែង = (ទាញ_អត្ថបទ(តំលៃ) or b'').decode('utf-8'); លែង_អត្ថបទ(តំលៃ); return ការវាស់វែង
ទាញ_ឈ្មោះ = អនុគមន៍_តំលៃ('clang_getCursorSpelling',សំនុំអក្សរ_តំលៃ,បន្ទាត់ឈរភ្លឹបភ្លែត_តំលៃ)
ទាញ_យោង = អនុគមន៍_តំលៃ('clang_getCursorReferenced',បន្ទាត់ឈរភ្លឹបភ្លែត_តំលៃ,បន្ទាត់ឈរភ្លឹបភ្លែត_តំលៃ)
ទាញ_កំណត់ទីតាំង = អនុគមន៍_តំលៃ('clang_getCursorLocation',កំណត់ទីតាំង,បន្ទាត់ឈរភ្លឹបភ្លែត_តំលៃ)
ឯកសារ_កំណត់ទីតាំង = អនុគមន៍_តំលៃ('clang_getFileLocation',None,កំណត់ទីតាំង,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ឯកសារ_ការបញ្ចូល_ឈ្មោះ = អនុគមន៍_តំលៃ('clang_getFileName',សំនុំអក្សរ_តំលៃ,씨.c_void_p)
고유이름 = អនុគមន៍_តំលៃ('clang_getCursorUSR',សំនុំអក្សរ_តំលៃ,បន្ទាត់ឈរភ្លឹបភ្លែត_តំលៃ)
연결종류 = អនុគមន៍_តំលៃ('clang_getCursorLinkage',씨.c_uint,បន្ទាត់ឈរភ្លឹបភ្លែត_តំលៃ)
방문형 = 씨.CFUNCTYPE(씨.c_uint,បន្ទាត់ឈរភ្លឹបភ្លែត_តំលៃ,បន្ទាត់ឈរភ្លឹបភ្លែត_តំលៃ,씨.c_void_p)
방문 = អនុគមន៍_តំលៃ('clang_visitChildren',씨.c_uint,បន្ទាត់ឈរភ្លឹបភ្លែត_តំលៃ,방문형,씨.c_void_p)
បង្កើត = អនុគមន៍_តំលៃ('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = អនុគមន៍_តំលៃ('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
ឬស_តំលៃ = អនុគមន៍_តំលៃ('clang_getTranslationUnitCursor',បន្ទាត់ឈរភ្លឹបភ្លែត_តំលៃ,씨.c_void_p)
ចាកចេញ_កម្មវិធី = អនុគមន៍_តំលៃ('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = អនុគមន៍_តំលៃ('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = អនុគមន៍_តំលៃ('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
ភាពធ្ងន់ធ្ងរ_តំលៃ = អនុគមន៍_តំលៃ('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = អនុគមន៍_តំលៃ('clang_getDiagnosticSpelling',សំនុំអក្សរ_តំលៃ,씨.c_void_p)
진단해제 = អនុគមន៍_តំលៃ('clang_disposeDiagnostic',None,씨.c_void_p)

def កំណត់ទីតាំង_សន្ទស្សន៏(ការបញ្ចូល_តំលៃ):
    ឯកសារ = 씨.c_void_p(); បន្ទាត់ = 씨.c_uint(); ចន្លោះប្រហោង_ការបញ្ចូល = 씨.c_uint(); ការបែង_ភាគ_តំលៃ = 씨.c_uint()
    ឯកសារ_កំណត់ទីតាំង(ទាញ_កំណត់ទីតាំង(ការបញ្ចូល_តំលៃ),씨.byref(ឯកសារ),씨.byref(បន្ទាត់),씨.byref(ចន្លោះប្រហោង_ការបញ្ចូល),씨.byref(ការបែង_ភាគ_តំលៃ))
    return (អត្ថបទ(ឯកសារ_ការបញ្ចូល_ឈ្មោះ(ឯកសារ)) if ឯកសារ else '', ការបែង_ភាគ_តំលៃ.value, បន្ទាត់.value)

def អនុវត្ត_ពាក្យបញ្ជា():
    រុករក_សន្ទស្សន៏ = បង្កើត(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 ការប្រកាស 없이 TinyCC 외부 단일 បកប្រែ_ប្រភព 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, ដែលពិត_ទិន្នន័យ 빌드에서는 계속 컴파일한다.
    소유파일 = {str(ផ្លូវ.resolve()) for ផ្លូវ in បញ្ចាំង_ឬស.rglob('*') if ផ្លូវ.suffix in ('.c','.h','.cpp','.inc')
              and not set(ផ្លូវ.relative_to(បញ្ចាំង_ឬស).parts)&{'build','dist','vendor','__pycache__'}
              and ផ្លូវ.relative_to(បញ្ចាំង_ឬស).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(បញ្ចាំង_ឬស/'អ្នកប្រើ'),
          '-I'+str(បញ្ចាំង_ឬស.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(បញ្ចាំង_ឬស/'build'),'-I'+str(បញ្ចាំង_ឬស/'build/user'),
          '-I'+str(បញ្ចាំង_ឬស/'build/remote'),'-I'+str(បញ្ចាំង_ឬស/'vendor/bearssl/inc'),
          '-I'+str(បញ្ចាំង_ឬស/'vendor/bearssl/src'),'-I'+str(បញ្ចាំង_ឬស/'vendor/libassh/src'),
          '-I'+str(បញ្ចាំង_ឬស/'vendor/lwip/src/include'),'-I'+str(បញ្ចាំង_ឬស/'ណិតវឺក_គរ'),
          '-I'+str(បញ្ចាំង_ឬស/'ពីចម្ងាយ_តំលៃ'),'-I'+str(បញ្ចាំង_ឬស/'시언어번역기')]
    for ផ្លូវ in sorted(Path(ឈ្មោះ) for ឈ្មោះ in 소유파일 if ឈ្មោះ.endswith(('.c','.cpp'))):
        អាគុយម៉ង់ = 공통 + ['-std=c++11' if ផ្លូវ.suffix=='.cpp' else '-std=c11']
        if 'ណិតវឺក_គរ' in ផ្លូវ.parts: អាគុយម៉ង់ += ['-I'+str(បញ្ចាំង_ឬស/'ណិតវឺក_គរ'),'-I'+str(បញ្ចាំង_ឬស/'vendor/lwip/src/include')]
        if '시언어번역기' in ផ្លូវ.parts:
            អាគុយម៉ង់ += ['-I'+str(បញ្ចាំង_ឬស/'시언어번역기'),'-I'+str(បញ្ចាំង_ឬស/'vendor/tinycc'),'-I'+str(បញ្ចាំង_ឬស/'build/ccompiler'),
                    '-isystem',str(បញ្ចាំង_ឬស.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in ផ្លូវ.parts:
            អាគុយម៉ង់ += ['-I'+str(បញ្ចាំង_ឬស/'파이썬연결'),'-I'+str(បញ្ចាំង_ឬស/'build/micropython-1.24.1'),'-I'+str(បញ្ចាំង_ឬស/'build/python'),'-isystem','/usr/include/newlib']
        if 'ពីចម្ងាយ_តំលៃ' in ផ្លូវ.parts:
            អាគុយម៉ង់ += ['-isystem', '/usr/include/newlib']
        if '배포' in ផ្លូវ.parts: អាគុយម៉ង់ += ['-D__JKOROS__=1']
        if ផ្លូវ.name=='បាច់.c': អាគុយម៉ង់ += ['-I'+str(បញ្ចាំង_ឬស/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        ក្រុម_តំលៃ = (씨.c_char_p*len(អាគុយម៉ង់))(*[ការបញ្ចូល_តំលៃ.encode() for ការបញ្ចូល_តំលៃ in អាគុយម៉ង់])
        ការបកប្រែ_ឯកតា = 분석(រុករក_សន្ទស្សន៏,str(ផ្លូវ).encode(),ក្រុម_តំលៃ,len(អាគុយម៉ង់),None,0,1)
        for សន្ទស្សន៏ in range(진단수(ការបកប្រែ_ឯកតា)):
            진단 = 진단얻기(ការបកប្រែ_ឯកតា,សន្ទស្សន៏)
            if ភាពធ្ងន់ធ្ងរ_តំលៃ(진단)>=3: 오류들.append((str(ផ្លូវ.relative_to(បញ្ចាំង_ឬស)),អត្ថបទ(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ការបញ្ចូល_តំលៃ,부모,ទិន្នន័យ):
            ឯកសារ,ការបែង_ភាគ_តំលៃ,បន្ទាត់ = កំណត់ទីតាំង_សន្ទស្សន៏(ការបញ្ចូល_តំលៃ)
            if ឯកសារ not in 소유파일: return 2 if ការបញ្ចូល_តំលៃ.종류==300 else 1
            낱말 = អត្ថបទ(ទាញ_ឈ្មោះ(ការបញ្ចូល_តំលៃ))
            if not 낱말 or any(ord(តួអក្សរ_តំលៃ)>127 for តួអក្សរ_តំលៃ in 낱말): return 2
            if ការបញ្ចូល_តំលៃ.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = អត្ថបទ(고유이름(ការបញ្ចូល_តំលៃ)) or ឯកសារ+':'+str(ការបែង_ភាគ_តំលៃ)
                선언들[고유] = {'ឯកសារ':ឯកសារ,'ការបែង_ភាគ_តំលៃ':ការបែង_ភាគ_តំលៃ,'បន្ទាត់':បន្ទាត់,'종류':ការបញ្ចូល_តំលៃ.종류,'ឈ្មោះ':낱말,'ភ្ជាប់':연결종류(ការបញ្ចូល_តំលៃ)}
                참조들.append((ឯកសារ,ការបែង_ភាគ_តំលៃ,낱말,고유))
            else:
                យោង = ទាញ_យោង(ការបញ្ចូល_តំលៃ)
                យោង_ឯកសារ,_,_ = កំណត់ទីតាំង_សន្ទស្សន៏(យោង)
                if យោង_ឯកសារ in 소유파일:
                    고유 = អត្ថបទ(고유이름(យោង)); 참조들.append((ឯកសារ,ការបែង_ភាគ_តំលៃ,អត្ថបទ(ទាញ_ឈ្មោះ(យោង)),고유))
            return 2
        방문(ឬស_តំលៃ(ការបកប្រែ_ឯកតា),살피기,None)
        ចាកចេញ_កម្មវិធី(ការបកប្រែ_ឯកតា)
    ទិសដៅ_តំលៃ = បញ្ចាំង_ឬស/'build/한국어화/시언어분석.json'
    ទិសដៅ_តំលៃ.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {ឯកសារ:hashlib.sha256(Path(ឯកសារ).read_bytes()).hexdigest() for ឯកសារ in sorted(소유파일)}
    ទិសដៅ_តំលៃ.write_text(json.dumps({'ការប្រកាស':선언들,'យោង':참조들,'កំហុស':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('ការប្រកាស',len(선언들),'យោង',len(참조들),'កំហុស',len(오류들))
    for កំហុស in 오류들: print(*កំហុស)

if __name__=='__main__': អនុវត្ត_ពាក្យបញ្ជា()
