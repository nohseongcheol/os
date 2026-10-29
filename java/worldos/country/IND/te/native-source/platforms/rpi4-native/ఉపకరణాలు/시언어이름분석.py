#!/usr/bin/env python3
"""libclang ప్రకటన·సూచన 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

ప్రొజెక్ట్_మూలం = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class అక్షరసరం_మూల్యం(씨.Structure): _fields_ = [('డేటా',씨.c_void_p),('చూపించు_మూల్యం',씨.c_uint)]
class కర్సర్_మూల్యం(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('డేటా',씨.c_void_p*3)]
class స్థానము(씨.Structure): _fields_ = [('డేటా',씨.c_void_p*2),('ఆఫ్_సెట్_మూల్యం',씨.c_uint)]
def కార్యం_మూల్యం(పేరు, 반환, *인수):
    ప్రవేశం_మూల్యం = getattr(구현, పేరు); ప్రవేశం_మూల్యం.restype = 반환; ప్రవేశం_మూల్యం.argtypes = list(인수); return ప్రవేశం_మూల్యం
పొందు_పాఠం = కార్యం_మూల్యం('clang_getCString',씨.c_char_p,అక్షరసరం_మూల్యం)
విడుదల_పాఠం = కార్యం_మూల్యం('clang_disposeString',None,అక్షరసరం_మూల్యం)
def పాఠ్యము(మూల్యం):
    ప్రమాణం = (పొందు_పాఠం(మూల్యం) or b'').decode('utf-8'); విడుదల_పాఠం(మూల్యం); return ప్రమాణం
పొందు_పేరు = కార్యం_మూల్యం('clang_getCursorSpelling',అక్షరసరం_మూల్యం,కర్సర్_మూల్యం)
పొందు_సూచన = కార్యం_మూల్యం('clang_getCursorReferenced',కర్సర్_మూల్యం,కర్సర్_మూల్యం)
పొందు_స్థాయి = కార్యం_మూల్యం('clang_getCursorLocation',స్థానము,కర్సర్_మూల్యం)
ఫైలు_స్థాయి = కార్యం_మూల్యం('clang_getFileLocation',None,స్థానము,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ఫైలు_ప్రవేశం_పేరు = కార్యం_మూల్యం('clang_getFileName',అక్షరసరం_మూల్యం,씨.c_void_p)
고유이름 = కార్యం_మూల్యం('clang_getCursorUSR',అక్షరసరం_మూల్యం,కర్సర్_మూల్యం)
연결종류 = కార్యం_మూల్యం('clang_getCursorLinkage',씨.c_uint,కర్సర్_మూల్యం)
방문형 = 씨.CFUNCTYPE(씨.c_uint,కర్సర్_మూల్యం,కర్సర్_మూల్యం,씨.c_void_p)
방문 = కార్యం_మూల్యం('clang_visitChildren',씨.c_uint,కర్సర్_మూల్యం,방문형,씨.c_void_p)
రూపొందించు = కార్యం_మూల్యం('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = కార్యం_మూల్యం('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
మూలం_మూల్యం = కార్యం_మూల్యం('clang_getTranslationUnitCursor',కర్సర్_మూల్యం,씨.c_void_p)
నిష్క్రమణ_అనువర్తనం_55b3a1cd = కార్యం_మూల్యం('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = కార్యం_మూల్యం('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = కార్యం_మూల్యం('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
తీవ్రత_మూల్యం = కార్యం_మూల్యం('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = కార్యం_మూల్యం('clang_getDiagnosticSpelling',అక్షరసరం_మూల్యం,씨.c_void_p)
진단해제 = కార్యం_మూల్యం('clang_disposeDiagnostic',None,씨.c_void_p)

def స్థాయి_సూచీ(ప్రవేశం_మూల్యం):
    దస్త్రం = 씨.c_void_p(); పంక్తి = 씨.c_uint(); స్లాట్_ప్రవేశం = 씨.c_uint(); ఆఫ్_సెట్_మూల్యం = 씨.c_uint()
    ఫైలు_స్థాయి(పొందు_స్థాయి(ప్రవేశం_మూల్యం),씨.byref(దస్త్రం),씨.byref(పంక్తి),씨.byref(స్లాట్_ప్రవేశం),씨.byref(ఆఫ్_సెట్_మూల్యం))
    return (పాఠ్యము(ఫైలు_ప్రవేశం_పేరు(దస్త్రం)) if దస్త్రం else '', ఆఫ్_సెట్_మూల్యం.value, పంక్తి.value)

def అమలు_చేయి_ఆదేశం():
    అంశం_శోధన_సూచీ = రూపొందించు(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 ప్రకటన 없이 TinyCC 외부 단일 అనువదించు_మూలం 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, వాస్తవ_డేటా 빌드에서는 계속 컴파일한다.
    소유파일 = {str(పాత్.resolve()) for పాత్ in ప్రొజెక్ట్_మూలం.rglob('*') if పాత్.suffix in ('.c','.h','.cpp','.inc')
              and not set(పాత్.relative_to(ప్రొజెక్ట్_మూలం).parts)&{'build','dist','vendor','__pycache__'}
              and పాత్.relative_to(ప్రొజెక్ట్_మూలం).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(ప్రొజెక్ట్_మూలం/'వినియోగదారు'),
          '-I'+str(ప్రొజెక్ట్_మూలం.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(ప్రొజెక్ట్_మూలం/'build'),'-I'+str(ప్రొజెక్ట్_మూలం/'build/user'),
          '-I'+str(ప్రొజెక్ట్_మూలం/'build/remote'),'-I'+str(ప్రొజెక్ట్_మూలం/'vendor/bearssl/inc'),
          '-I'+str(ప్రొజెక్ట్_మూలం/'vendor/bearssl/src'),'-I'+str(ప్రొజెక్ట్_మూలం/'vendor/libassh/src'),
          '-I'+str(ప్రొజెక్ట్_మూలం/'vendor/lwip/src/include'),'-I'+str(ప్రొజెక్ట్_మూలం/'నెట్_వర్క్_దొంతర'),
          '-I'+str(ప్రొజెక్ట్_మూలం/'రిమోట్_మూల్యం'),'-I'+str(ప్రొజెక్ట్_మూలం/'시언어번역기')]
    for పాత్ in sorted(Path(పేరు) for పేరు in 소유파일 if పేరు.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if పాత్.suffix=='.cpp' else '-std=c11']
        if 'నెట్_వర్క్_దొంతర' in పాత్.parts: 인수 += ['-I'+str(ప్రొజెక్ట్_మూలం/'నెట్_వర్క్_దొంతర'),'-I'+str(ప్రొజెక్ట్_మూలం/'vendor/lwip/src/include')]
        if '시언어번역기' in పాత్.parts:
            인수 += ['-I'+str(ప్రొజెక్ట్_మూలం/'시언어번역기'),'-I'+str(ప్రొజెక్ట్_మూలం/'vendor/tinycc'),'-I'+str(ప్రొజెక్ట్_మూలం/'build/ccompiler'),
                    '-isystem',str(ప్రొజెక్ట్_మూలం.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in పాత్.parts:
            인수 += ['-I'+str(ప్రొజెక్ట్_మూలం/'파이썬연결'),'-I'+str(ప్రొజెక్ట్_మూలం/'build/micropython-1.24.1'),'-I'+str(ప్రొజెక్ట్_మూలం/'build/python'),'-isystem','/usr/include/newlib']
        if 'రిమోట్_మూల్యం' in పాత్.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in పాత్.parts: 인수 += ['-D__JKOROS__=1']
        if పాత్.name=='బండిల్.c': 인수 += ['-I'+str(ప్రొజెక్ట్_మూలం/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        సమూహం_మూల్యం = (씨.c_char_p*len(인수))(*[ప్రవేశం_మూల్యం.encode() for ప్రవేశం_మూల్యం in 인수])
        అనువాదం_పాఠం = 분석(అంశం_శోధన_సూచీ,str(పాత్).encode(),సమూహం_మూల్యం,len(인수),None,0,1)
        for సూచీ in range(진단수(అనువాదం_పాఠం)):
            진단 = 진단얻기(అనువాదం_పాఠం,సూచీ)
            if తీవ్రత_మూల్యం(진단)>=3: 오류들.append((str(పాత్.relative_to(ప్రొజెక్ట్_మూలం)),పాఠ్యము(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ప్రవేశం_మూల్యం,부모,డేటా):
            దస్త్రం,ఆఫ్_సెట్_మూల్యం,పంక్తి = స్థాయి_సూచీ(ప్రవేశం_మూల్యం)
            if దస్త్రం not in 소유파일: return 2 if ప్రవేశం_మూల్యం.종류==300 else 1
            낱말 = పాఠ్యము(పొందు_పేరు(ప్రవేశం_మూల్యం))
            if not 낱말 or any(ord(అక్షరం_మూల్యం)>127 for అక్షరం_మూల్యం in 낱말): return 2
            if ప్రవేశం_మూల్యం.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = పాఠ్యము(고유이름(ప్రవేశం_మూల్యం)) or దస్త్రం+':'+str(ఆఫ్_సెట్_మూల్యం)
                선언들[고유] = {'దస్త్రం':దస్త్రం,'ఆఫ్_సెట్_మూల్యం':ఆఫ్_సెట్_మూల్యం,'줄':పంక్తి,'종류':ప్రవేశం_మూల్యం.종류,'పేరు':낱말,'కనెక్టుచేయి':연결종류(ప్రవేశం_మూల్యం)}
                참조들.append((దస్త్రం,ఆఫ్_సెట్_మూల్యం,낱말,고유))
            else:
                సూచన = పొందు_సూచన(ప్రవేశం_మూల్యం)
                సూచన_ఫైలు,_,_ = స్థాయి_సూచీ(సూచన)
                if సూచన_ఫైలు in 소유파일:
                    고유 = పాఠ్యము(고유이름(సూచన)); 참조들.append((దస్త్రం,ఆఫ్_సెట్_మూల్యం,పాఠ్యము(పొందు_పేరు(సూచన)),고유))
            return 2
        방문(మూలం_మూల్యం(అనువాదం_పాఠం),살피기,None)
        నిష్క్రమణ_అనువర్తనం_55b3a1cd(అనువాదం_పాఠం)
    గమ్యం_మూల్యం = ప్రొజెక్ట్_మూలం/'build/한국어화/시언어분석.json'
    గమ్యం_మూల్యం.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {దస్త్రం:hashlib.sha256(Path(దస్త్రం).read_bytes()).hexdigest() for దస్త్రం in sorted(소유파일)}
    గమ్యం_మూల్యం.write_text(json.dumps({'ప్రకటన':선언들,'సూచన':참조들,'దోషం':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('ప్రకటన',len(선언들),'సూచన',len(참조들),'దోషం',len(오류들))
    for దోషం in 오류들: print(*దోషం)

if __name__=='__main__': అమలు_చేయి_ఆదేశం()
