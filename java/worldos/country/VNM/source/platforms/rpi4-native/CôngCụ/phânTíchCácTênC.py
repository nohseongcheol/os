#!/usr/bin/env python3
"""libclang KhaiBáo·thamChiếu 위치를 수집한다. giáTrịBênNgoài 헤더의 멤버는 변환하지 않는다."""
import ctypes as nguồnC
import hashlib
import json
from pathlib import Path

gốcCâyDựÁn = Path(__file__).resolve().parents[1]
phầnCàiĐặt = nguồnC.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class ChuỗiKýTự(nguồnC.Structure): _fields_ = [('DữLiệu',nguồnC.c_void_p),('hiệnGiáTrị',nguồnC.c_uint)]
class giáTrịConTrỏVănBản(nguồnC.Structure): _fields_ = [('giáTrịLoại',nguồnC.c_uint),('giáTrịPhụTrợ',nguồnC.c_int),('DữLiệu',nguồnC.c_void_p*3)]
class vịTrí(nguồnC.Structure): _fields_ = [('DữLiệu',nguồnC.c_void_p*2),('giáTrịĐộLệch',nguồnC.c_uint)]
def Hàm(tên, kếtQuảTrảVề, *cácĐốiSố):
    giáTrịMục = getattr(phầnCàiĐặt, tên); giáTrịMục.restype = kếtQuảTrảVề; giáTrịMục.argtypes = list(cácĐốiSố); return giáTrịMục
lấyVănBản = Hàm('clang_getCString',nguồnC.c_char_p,ChuỗiKýTự)
giảiPhóngVănBản = Hàm('clang_disposeString',None,ChuỗiKýTự)
def vănBản(giáTrị):
    kếtQuả = (lấyVănBản(giáTrị) or b'').decode('utf-8'); giảiPhóngVănBản(giáTrị); return kếtQuả
lấyTên = Hàm('clang_getCursorSpelling',ChuỗiKýTự,giáTrịConTrỏVănBản)
lấyThamChiếu = Hàm('clang_getCursorReferenced',giáTrịConTrỏVănBản,giáTrịConTrỏVănBản)
lấyVịTrí = Hàm('clang_getCursorLocation',vịTrí,giáTrịConTrỏVănBản)
vịTríTệp = Hàm('clang_getFileLocation',None,vịTrí,nguồnC.POINTER(nguồnC.c_void_p),nguồnC.POINTER(nguồnC.c_uint),nguồnC.POINTER(nguồnC.c_uint),nguồnC.POINTER(nguồnC.c_uint))
tênMụcTệp = Hàm('clang_getFileName',ChuỗiKýTự,nguồnC.c_void_p)
tênDuyNhất = Hàm('clang_getCursorUSR',ChuỗiKýTự,giáTrịConTrỏVănBản)
loạiKếtNối = Hàm('clang_getCursorLinkage',nguồnC.c_uint,giáTrịConTrỏVănBản)
kiểuĐãDuyệt = nguồnC.CFUNCTYPE(nguồnC.c_uint,giáTrịConTrỏVănBản,giáTrịConTrỏVănBản,nguồnC.c_void_p)
duyệtGiáTrị = Hàm('clang_visitChildren',nguồnC.c_uint,giáTrịConTrỏVănBản,kiểuĐãDuyệt,nguồnC.c_void_p)
sinh = Hàm('clang_createIndex',nguồnC.c_void_p,nguồnC.c_int,nguồnC.c_int)
phânTíchGiáTrị = Hàm('clang_parseTranslationUnit',nguồnC.c_void_p,nguồnC.c_void_p,nguồnC.c_char_p,nguồnC.POINTER(nguồnC.c_char_p),nguồnC.c_int,nguồnC.c_void_p,nguồnC.c_uint,nguồnC.c_uint)
giáTrịGốcCây = Hàm('clang_getTranslationUnitCursor',giáTrịConTrỏVănBản,nguồnC.c_void_p)
chươngTrìnhThoátHẳn = Hàm('clang_disposeTranslationUnit',None,nguồnC.c_void_p)
sốLượngChẩnĐoán = Hàm('clang_getNumDiagnostics',nguồnC.c_uint,nguồnC.c_void_p)
lấyChẩnĐoán = Hàm('clang_getDiagnostic',nguồnC.c_void_p,nguồnC.c_void_p,nguồnC.c_uint)
giáTrịMứcNghiêmTrọng = Hàm('clang_getDiagnosticSeverity',nguồnC.c_uint,nguồnC.c_void_p)
thôngĐiệpChẩnĐoán = Hàm('clang_getDiagnosticSpelling',ChuỗiKýTự,nguồnC.c_void_p)
giảiPhóngChẩnĐoán = Hàm('clang_disposeDiagnostic',None,nguồnC.c_void_p)

def chỉSốVịTrí(giáTrịMục):
    Tệp = nguồnC.c_void_p(); dòng = nguồnC.c_uint(); mụcÔ = nguồnC.c_uint(); giáTrịĐộLệch = nguồnC.c_uint()
    vịTríTệp(lấyVịTrí(giáTrịMục),nguồnC.byref(Tệp),nguồnC.byref(dòng),nguồnC.byref(mụcÔ),nguồnC.byref(giáTrịĐộLệch))
    return (vănBản(tênMụcTệp(Tệp)) if Tệp else '', giáTrịĐộLệch.value, dòng.value)

def thựcThiLệnh():
    chỉSốTraCứu = sinh(0,0); danhSáchCácKhaiBáo = {}; danhSáchCácThamChiếu = []; cácLỗi = []
    # côngCụTrìnhBiênDịch.c는 tựThân KhaiBáo 없이 TinyCC giáTrịBênNgoài 단일 dịchThuậtNguồn 단위만 포함한다.
    # giáTrịBênNgoài 선언을 tựThân 이름으로 세지 않으며, dữLiệuThựcTế 빌드에서는 việcXửLýTiếpTục 컴파일한다.
    tệpThuộcDựÁn = {str(đườngDẫn.resolve()) for đườngDẫn in gốcCâyDựÁn.rglob('*') if đườngDẫn.suffix in ('.c','.h','.cpp','.inc')
              and not set(đườngDẫn.relative_to(gốcCâyDựÁn).parts)&{'build','dist','vendor','__pycache__'}
              and đườngDẫn.relative_to(gốcCâyDựÁn).as_posix() != 'TrìnhBiênDịchC/côngCụTrìnhBiênDịch.c'}
    giáTrịChung = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(gốcCâyDựÁn/'NgườiDùng'),
          '-I'+str(gốcCâyDựÁn.parents[1]/'posix-kor/arm64-native/TệpĐầuMục'),'-I'+str(gốcCâyDựÁn/'build'),'-I'+str(gốcCâyDựÁn/'build/user'),
          '-I'+str(gốcCâyDựÁn/'build/remote'),'-I'+str(gốcCâyDựÁn/'vendor/bearssl/inc'),
          '-I'+str(gốcCâyDựÁn/'vendor/bearssl/src'),'-I'+str(gốcCâyDựÁn/'vendor/libassh/src'),
          '-I'+str(gốcCâyDựÁn/'vendor/lwip/src/include'),'-I'+str(gốcCâyDựÁn/'NgănXếpMạng'),
          '-I'+str(gốcCâyDựÁn/'giáTrịTừXa'),'-I'+str(gốcCâyDựÁn/'TrìnhBiênDịchC')]
    for đườngDẫn in sorted(Path(tên) for tên in tệpThuộcDựÁn if tên.endswith(('.c','.cpp'))):
        cácĐốiSố = giáTrịChung + ['-std=c++11' if đườngDẫn.suffix=='.cpp' else '-std=c11']
        if 'NgănXếpMạng' in đườngDẫn.parts: cácĐốiSố += ['-I'+str(gốcCâyDựÁn/'NgănXếpMạng'),'-I'+str(gốcCâyDựÁn/'vendor/lwip/src/include')]
        if 'TrìnhBiênDịchC' in đườngDẫn.parts:
            cácĐốiSố += ['-I'+str(gốcCâyDựÁn/'TrìnhBiênDịchC'),'-I'+str(gốcCâyDựÁn/'vendor/tinycc'),'-I'+str(gốcCâyDựÁn/'build/ccompiler'),
                    '-isystem',str(gốcCâyDựÁn.parent/'rpi4/build/rootfs/usr/include')]
        if 'cầuNốiPython' in đườngDẫn.parts:
            cácĐốiSố += ['-I'+str(gốcCâyDựÁn/'cầuNốiPython'),'-I'+str(gốcCâyDựÁn/'build/micropython-1.24.1'),'-I'+str(gốcCâyDựÁn/'build/python'),'-isystem','/usr/include/newlib']
        if 'giáTrịTừXa' in đườngDẫn.parts:
            cácĐốiSố += ['-isystem', '/usr/include/newlib']
        if 'giáTrịBảnPhânPhối' in đườngDẫn.parts: cácĐốiSố += ['-D__JKOROS__=1']
        if đườngDẫn.name=='GóiGộp.c': cácĐốiSố += ['-I'+str(gốcCâyDựÁn/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        giáTrịNhóm = (nguồnC.c_char_p*len(cácĐốiSố))(*[giáTrịMục.encode() for giáTrịMục in cácĐốiSố])
        đơnVịBảnDịch = phânTíchGiáTrị(chỉSốTraCứu,str(đườngDẫn).encode(),giáTrịNhóm,len(cácĐốiSố),None,0,1)
        for sốHiệu in range(sốLượngChẩnĐoán(đơnVịBảnDịch)):
            giáTrịChẩnĐoán = lấyChẩnĐoán(đơnVịBảnDịch,sốHiệu)
            if giáTrịMứcNghiêmTrọng(giáTrịChẩnĐoán)>=3: cácLỗi.append((str(đườngDẫn.relative_to(gốcCâyDựÁn)),vănBản(thôngĐiệpChẩnĐoán(giáTrịChẩnĐoán))))
            giảiPhóngChẩnĐoán(giáTrịChẩnĐoán)
        @kiểuĐãDuyệt
        def xemXétGiáTrị(giáTrịMục,giáTrịCha,DữLiệu):
            Tệp,giáTrịĐộLệch,dòng = chỉSốVịTrí(giáTrịMục)
            if Tệp not in tệpThuộcDựÁn: return 2 if giáTrịMục.giáTrịLoại==300 else 1
            từTừVựng = vănBản(lấyTên(giáTrịMục))
            if not từTừVựng or any(ord(giáTrịKýTự)>127 for giáTrịKýTự in từTừVựng): return 2
            if giáTrịMục.giáTrịLoại in (2,3,4,5,6,7,8,9,10,20,21,501):
                giáTrịDuyNhất = vănBản(tênDuyNhất(giáTrịMục)) or Tệp+':'+str(giáTrịĐộLệch)
                danhSáchCácKhaiBáo[giáTrịDuyNhất] = {'Tệp':Tệp,'giáTrịĐộLệch':giáTrịĐộLệch,'dòng':dòng,'giáTrịLoại':giáTrịMục.giáTrịLoại,'tên':từTừVựng,'nốiKết':loạiKếtNối(giáTrịMục)}
                danhSáchCácThamChiếu.append((Tệp,giáTrịĐộLệch,từTừVựng,giáTrịDuyNhất))
            else:
                thamChiếu = lấyThamChiếu(giáTrịMục)
                tệpThamChiếu,_,_ = chỉSốVịTrí(thamChiếu)
                if tệpThamChiếu in tệpThuộcDựÁn:
                    giáTrịDuyNhất = vănBản(tênDuyNhất(thamChiếu)); danhSáchCácThamChiếu.append((Tệp,giáTrịĐộLệch,vănBản(lấyTên(thamChiếu)),giáTrịDuyNhất))
            return 2
        duyệtGiáTrị(giáTrịGốcCây(đơnVịBảnDịch),xemXétGiáTrị,None)
        chươngTrìnhThoátHẳn(đơnVịBảnDịch)
    giáTrịĐích = gốcCâyDựÁn/'build/한국어화/시언어분석.json'
    giáTrịĐích.parent.mkdir(parents=True, exist_ok=True)
    danhSáchCácMãBăm = {Tệp:hashlib.sha256(Path(Tệp).read_bytes()).hexdigest() for Tệp in sorted(tệpThuộcDựÁn)}
    giáTrịĐích.write_text(json.dumps({'KhaiBáo':danhSáchCácKhaiBáo,'thamChiếu':danhSáchCácThamChiếu,'lỗi':cácLỗi,'원문해시':danhSáchCácMãBăm},ensure_ascii=False,indent=2)+'\n')
    print('KhaiBáo',len(danhSáchCácKhaiBáo),'thamChiếu',len(danhSáchCácThamChiếu),'lỗi',len(cácLỗi))
    for lỗi in cácLỗi: print(*lỗi)

if __name__=='__main__': thựcThiLệnh()
