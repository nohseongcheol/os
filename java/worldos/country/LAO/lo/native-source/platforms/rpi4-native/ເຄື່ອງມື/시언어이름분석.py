#!/usr/bin/env python3
"""libclang ການປະກາດ·ການ_ອ້າງ_ອີງ 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

ໂຄງ_ການ_ເລກຮາກ = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class ສະຕຣິງ_ຄ່າ(씨.Structure): _fields_ = [('ຂໍ້ມູນ',씨.c_void_p),('ລາຍການ_ຄ່າ',씨.c_uint)]
class ຈຸດສະແດງຕໍາແຫນ່ງ_ຄ່າ(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('ຂໍ້ມູນ',씨.c_void_p*3)]
class ຈັດຕໍາແຫນ່ງ(씨.Structure): _fields_ = [('ຂໍ້ມູນ',씨.c_void_p*2),('ອອບເຊັດ_ຄ່າ',씨.c_uint)]
def ຟັງ_ຄ໌_ຊັນ_ຄ່າ(ຊື່, 반환, *인수):
    ເຂົ້າໃນ_ຄ່າ = getattr(구현, ຊື່); ເຂົ້າໃນ_ຄ່າ.restype = 반환; ເຂົ້າໃນ_ຄ່າ.argtypes = list(인수); return ເຂົ້າໃນ_ຄ່າ
ຮັບ_ຂໍ້ຄວາມ = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_getCString',씨.c_char_p,ສະຕຣິງ_ຄ່າ)
ເວີຊັນ_ຂໍ້ຄວາມ = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_disposeString',None,ສະຕຣິງ_ຄ່າ)
def ຂໍ້ຄວາມ(ຄ່າ):
    ມາດຕະການ = (ຮັບ_ຂໍ້ຄວາມ(ຄ່າ) or b'').decode('utf-8'); ເວີຊັນ_ຂໍ້ຄວາມ(ຄ່າ); return ມາດຕະການ
ຮັບ_ຊື່ = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_getCursorSpelling',ສະຕຣິງ_ຄ່າ,ຈຸດສະແດງຕໍາແຫນ່ງ_ຄ່າ)
ຮັບ_ການ_ອ້າງ_ອີງ = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_getCursorReferenced',ຈຸດສະແດງຕໍາແຫນ່ງ_ຄ່າ,ຈຸດສະແດງຕໍາແຫນ່ງ_ຄ່າ)
ຮັບ_ຈັດຕໍາແຫນ່ງ = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_getCursorLocation',ຈັດຕໍາແຫນ່ງ,ຈຸດສະແດງຕໍາແຫນ່ງ_ຄ່າ)
ຟາຍ_ຈັດຕໍາແຫນ່ງ = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_getFileLocation',None,ຈັດຕໍາແຫນ່ງ,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ຟາຍ_ເຂົ້າໃນ_ຊື່ = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_getFileName',ສະຕຣິງ_ຄ່າ,씨.c_void_p)
고유이름 = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_getCursorUSR',ສະຕຣິງ_ຄ່າ,ຈຸດສະແດງຕໍາແຫນ່ງ_ຄ່າ)
연결종류 = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_getCursorLinkage',씨.c_uint,ຈຸດສະແດງຕໍາແຫນ່ງ_ຄ່າ)
방문형 = 씨.CFUNCTYPE(씨.c_uint,ຈຸດສະແດງຕໍາແຫນ່ງ_ຄ່າ,ຈຸດສະແດງຕໍາແຫນ່ງ_ຄ່າ,씨.c_void_p)
방문 = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_visitChildren',씨.c_uint,ຈຸດສະແດງຕໍາແຫນ່ງ_ຄ່າ,방문형,씨.c_void_p)
ສ້າງ_167eff27 = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
ເລກຮາກ_ຄ່າ = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_getTranslationUnitCursor',ຈຸດສະແດງຕໍາແຫນ່ງ_ຄ່າ,씨.c_void_p)
ອອກ_ແອັບ_55b3a1cd = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
ຄວາມຮ້າຍແຮງ_ຄ່າ = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_getDiagnosticSpelling',ສະຕຣິງ_ຄ່າ,씨.c_void_p)
진단해제 = ຟັງ_ຄ໌_ຊັນ_ຄ່າ('clang_disposeDiagnostic',None,씨.c_void_p)

def ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ(ເຂົ້າໃນ_ຄ່າ):
    ຟາຍ = 씨.c_void_p(); ສາຍ = 씨.c_uint(); ຊ່ອງ_ເຂົ້າໃນ = 씨.c_uint(); ອອບເຊັດ_ຄ່າ = 씨.c_uint()
    ຟາຍ_ຈັດຕໍາແຫນ່ງ(ຮັບ_ຈັດຕໍາແຫນ່ງ(ເຂົ້າໃນ_ຄ່າ),씨.byref(ຟາຍ),씨.byref(ສາຍ),씨.byref(ຊ່ອງ_ເຂົ້າໃນ),씨.byref(ອອບເຊັດ_ຄ່າ))
    return (ຂໍ້ຄວາມ(ຟາຍ_ເຂົ້າໃນ_ຊື່(ຟາຍ)) if ຟາຍ else '', ອອບເຊັດ_ຄ່າ.value, ສາຍ.value)

def ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ():
    ຄົ້ນຫາ_ດັດຊະນີ = ສ້າງ_167eff27(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 ການປະກາດ 없이 TinyCC 외부 단일 ແປພາສາ_ແຫຼ່ງທີ່ມາ 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, ຕົວ_ຈິງ_ຂໍ້ມູນ 빌드에서는 계속 컴파일한다.
    소유파일 = {str(ທາງໂຄຈອນ.resolve()) for ທາງໂຄຈອນ in ໂຄງ_ການ_ເລກຮາກ.rglob('*') if ທາງໂຄຈອນ.suffix in ('.c','.h','.cpp','.inc')
              and not set(ທາງໂຄຈອນ.relative_to(ໂຄງ_ການ_ເລກຮາກ).parts)&{'build','dist','vendor','__pycache__'}
              and ທາງໂຄຈອນ.relative_to(ໂຄງ_ການ_ເລກຮາກ).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(ໂຄງ_ການ_ເລກຮາກ/'ຜູ້ໃຊ້'),
          '-I'+str(ໂຄງ_ການ_ເລກຮາກ.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(ໂຄງ_ການ_ເລກຮາກ/'build'),'-I'+str(ໂຄງ_ການ_ເລກຮາກ/'build/user'),
          '-I'+str(ໂຄງ_ການ_ເລກຮາກ/'build/remote'),'-I'+str(ໂຄງ_ການ_ເລກຮາກ/'vendor/bearssl/inc'),
          '-I'+str(ໂຄງ_ການ_ເລກຮາກ/'vendor/bearssl/src'),'-I'+str(ໂຄງ_ການ_ເລກຮາກ/'vendor/libassh/src'),
          '-I'+str(ໂຄງ_ການ_ເລກຮາກ/'vendor/lwip/src/include'),'-I'+str(ໂຄງ_ການ_ເລກຮາກ/'ເຄືອຂ່າຍ_ກຸ່ມບັດ'),
          '-I'+str(ໂຄງ_ການ_ເລກຮາກ/'ທາງ_ໄກ_ຄ່າ'),'-I'+str(ໂຄງ_ການ_ເລກຮາກ/'시언어번역기')]
    for ທາງໂຄຈອນ in sorted(Path(ຊື່) for ຊື່ in 소유파일 if ຊື່.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if ທາງໂຄຈອນ.suffix=='.cpp' else '-std=c11']
        if 'ເຄືອຂ່າຍ_ກຸ່ມບັດ' in ທາງໂຄຈອນ.parts: 인수 += ['-I'+str(ໂຄງ_ການ_ເລກຮາກ/'ເຄືອຂ່າຍ_ກຸ່ມບັດ'),'-I'+str(ໂຄງ_ການ_ເລກຮາກ/'vendor/lwip/src/include')]
        if '시언어번역기' in ທາງໂຄຈອນ.parts:
            인수 += ['-I'+str(ໂຄງ_ການ_ເລກຮາກ/'시언어번역기'),'-I'+str(ໂຄງ_ການ_ເລກຮາກ/'vendor/tinycc'),'-I'+str(ໂຄງ_ການ_ເລກຮາກ/'build/ccompiler'),
                    '-isystem',str(ໂຄງ_ການ_ເລກຮາກ.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in ທາງໂຄຈອນ.parts:
            인수 += ['-I'+str(ໂຄງ_ການ_ເລກຮາກ/'파이썬연결'),'-I'+str(ໂຄງ_ການ_ເລກຮາກ/'build/micropython-1.24.1'),'-I'+str(ໂຄງ_ການ_ເລກຮາກ/'build/python'),'-isystem','/usr/include/newlib']
        if 'ທາງ_ໄກ_ຄ່າ' in ທາງໂຄຈອນ.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in ທາງໂຄຈອນ.parts: 인수 += ['-D__JKOROS__=1']
        if ທາງໂຄຈອນ.name=='ຊຸດ.c': 인수 += ['-I'+str(ໂຄງ_ການ_ເລກຮາກ/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        ກຸ່ມ_ຄ່າ = (씨.c_char_p*len(인수))(*[ເຂົ້າໃນ_ຄ່າ.encode() for ເຂົ້າໃນ_ຄ່າ in 인수])
        ການແປພາສາ_ບົດຮຽນ = 분석(ຄົ້ນຫາ_ດັດຊະນີ,str(ທາງໂຄຈອນ).encode(),ກຸ່ມ_ຄ່າ,len(인수),None,0,1)
        for ດັດຊະນີ in range(진단수(ການແປພາສາ_ບົດຮຽນ)):
            진단 = 진단얻기(ການແປພາສາ_ບົດຮຽນ,ດັດຊະນີ)
            if ຄວາມຮ້າຍແຮງ_ຄ່າ(진단)>=3: 오류들.append((str(ທາງໂຄຈອນ.relative_to(ໂຄງ_ການ_ເລກຮາກ)),ຂໍ້ຄວາມ(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ເຂົ້າໃນ_ຄ່າ,부모,ຂໍ້ມູນ):
            ຟາຍ,ອອບເຊັດ_ຄ່າ,ສາຍ = ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ(ເຂົ້າໃນ_ຄ່າ)
            if ຟາຍ not in 소유파일: return 2 if ເຂົ້າໃນ_ຄ່າ.종류==300 else 1
            낱말 = ຂໍ້ຄວາມ(ຮັບ_ຊື່(ເຂົ້າໃນ_ຄ່າ))
            if not 낱말 or any(ord(ຕົວອັກສອນ_ຄ່າ)>127 for ຕົວອັກສອນ_ຄ່າ in 낱말): return 2
            if ເຂົ້າໃນ_ຄ່າ.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = ຂໍ້ຄວາມ(고유이름(ເຂົ້າໃນ_ຄ່າ)) or ຟາຍ+':'+str(ອອບເຊັດ_ຄ່າ)
                선언들[고유] = {'ຟາຍ':ຟາຍ,'ອອບເຊັດ_ຄ່າ':ອອບເຊັດ_ຄ່າ,'줄':ສາຍ,'종류':ເຂົ້າໃນ_ຄ່າ.종류,'ຊື່':낱말,'ເຊື່ອມຕໍ່':연결종류(ເຂົ້າໃນ_ຄ່າ)}
                참조들.append((ຟາຍ,ອອບເຊັດ_ຄ່າ,낱말,고유))
            else:
                ການ_ອ້າງ_ອີງ = ຮັບ_ການ_ອ້າງ_ອີງ(ເຂົ້າໃນ_ຄ່າ)
                ການ_ອ້າງ_ອີງ_ຟາຍ,_,_ = ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ(ການ_ອ້າງ_ອີງ)
                if ການ_ອ້າງ_ອີງ_ຟາຍ in 소유파일:
                    고유 = ຂໍ້ຄວາມ(고유이름(ການ_ອ້າງ_ອີງ)); 참조들.append((ຟາຍ,ອອບເຊັດ_ຄ່າ,ຂໍ້ຄວາມ(ຮັບ_ຊື່(ການ_ອ້າງ_ອີງ)),고유))
            return 2
        방문(ເລກຮາກ_ຄ່າ(ການແປພາສາ_ບົດຮຽນ),살피기,None)
        ອອກ_ແອັບ_55b3a1cd(ການແປພາສາ_ບົດຮຽນ)
    ປາຍທາງ_ຄ່າ = ໂຄງ_ການ_ເລກຮາກ/'build/한국어화/시언어분석.json'
    ປາຍທາງ_ຄ່າ.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {ຟາຍ:hashlib.sha256(Path(ຟາຍ).read_bytes()).hexdigest() for ຟາຍ in sorted(소유파일)}
    ປາຍທາງ_ຄ່າ.write_text(json.dumps({'ການປະກາດ':선언들,'ການ_ອ້າງ_ອີງ':참조들,'ຂໍ້ຜິດພາດ':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('ການປະກາດ',len(선언들),'ການ_ອ້າງ_ອີງ',len(참조들),'ຂໍ້ຜິດພາດ',len(오류들))
    for ຂໍ້ຜິດພາດ in 오류들: print(*ຂໍ້ຜິດພາດ)

if __name__=='__main__': ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
