#!/usr/bin/env python3
"""KhaiBáo 고유번호와 UTF-8 giáTrịByte 위치로 tựThân C 이름을 옮기는 일회성 이행 CôngCụ.

giáTrịBênNgoài 구조체의 멤버, ChuỗiKýTự, C 표준 Hàm, ChuyểnNền 규약은 보존한다.
입력은 đổiGiáTrị giáTrịTrướcKhi 소스에 대한 phânTíchCácTênC.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

gốcCâyDựÁn = Path(__file__).resolve().parents[1]

def thựcThiLệnh():
    phânTíchGiáTrị = json.loads((gốcCâyDựÁn/'build/한국어화/시언어분석.json').read_text())
    if phânTíchGiáTrị['lỗi']: raise SystemExit('phânTíchGiáTrị 오류를 먼저 해결해야 합니다.')
    bảngTraTên = json.loads((gốcCâyDựÁn/'cáchĐặtTên/cácTênC.json').read_text())
    địnhNghĩaChuẩn = set(json.loads((gốcCâyDựÁn/'cáchĐặtTên/cácTênChuẩn.json').read_text()))
    bảngTraKhaiBáo = phânTíchGiáTrị['KhaiBáo']
    thayĐếnKhaiBáo = {giáTrịDuyNhất:bảngTraTên[giáTrịMục['tên']] for giáTrịDuyNhất,giáTrịMục in bảngTraKhaiBáo.items()
                if giáTrịMục['tên'] in bảngTraTên and giáTrịMục['tên'] not in địnhNghĩaChuẩn}
    bảngTraKếtNối = {giáTrịMục['tên']:bảngTraTên[giáTrịMục['tên']] for giáTrịMục in bảngTraKhaiBáo.values()
              if giáTrịMục.get('nốiKết')==4 and giáTrịMục['giáTrịLoại'] in (8,9)
              and giáTrịMục['tên'] in bảngTraTên and giáTrịMục['tên'] not in địnhNghĩaChuẩn}
    # sinh AOT C·어셈블리·공개 SDK가 공유하는 바이너리 nốiKết 이름만 유지한다.
    giáTrịĐầu = ['/* tiếngViệt câyNguồn 이름과 기존 máy nốiKết giáTrịQuyƯớc. 자동 sinh: cáchĐặtTên/cácTênC.json */',
           '#ifndef đầuMụcCácTênLiênKếtMáyBảnĐịa', '#define đầuMụcCácTênLiênKếtMáyBảnĐịa']
    giáTrịĐầu += ['#define '+tênMới+' '+tênCũ for tênCũ,tênMới in sorted(bảngTraKếtNối.items())]
    giáTrịĐầu += ['#endif','']
    (gốcCâyDựÁn/'cáchĐặtTên/cácTênLiênKếtMáy.h').write_text('\n'.join(giáTrịĐầu))
    danhSáchCácThayĐổi = defaultdict(dict)
    for Tệp,giáTrịĐộLệch,tên,giáTrịDuyNhất in phânTíchGiáTrị['thamChiếu']:
        if giáTrịDuyNhất in thayĐếnKhaiBáo:
            danhSáchCácThayĐổi[Tệp][giáTrịĐộLệch] = (tên,thayĐếnKhaiBáo[giáTrịDuyNhất])
    bảnGhiNhậtKý = ['Tệp\t원래바이트위치\t이전이름\t한국어이름']
    bỏQuaGiáTrị = []
    for Tệp,đổiGiáTrị in danhSáchCácThayĐổi.items():
        đườngDẫn = Path(Tệp); nguyênBản = đườngDẫn.read_bytes(); DữLiệu = nguyênBản
        for giáTrịĐộLệch,(tênCũ,tênMới) in sorted(đổiGiáTrị.items(),reverse=True):
            phầnKết = giáTrịĐộLệch+len(tênCũ.encode())
            if nguyênBản[giáTrịĐộLệch:phầnKết] != tênCũ.encode():
                bỏQuaGiáTrị.append((str(đườngDẫn.relative_to(gốcCâyDựÁn)),giáTrịĐộLệch,tênCũ));continue
            DữLiệu = DữLiệu[:giáTrịĐộLệch]+tênMới.encode()+DữLiệu[phầnKết:]
            bảnGhiNhậtKý.append('{}\t{}\t{}\t{}'.format(đườngDẫn.relative_to(gốcCâyDựÁn),giáTrịĐộLệch,tênCũ,tênMới))
        đườngDẫn.write_bytes(DữLiệu)
    # nguồnTiềnXửLý 매개변수는 AST의 선언으로 나타나지 않는다. nguồnTiềnXửLý 줄만 보완한다.
    từTừVựng = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    giáTrịVĩLệnh = {giáTrịMục['tên']:bảngTraTên[giáTrịMục['tên']] for giáTrịMục in bảngTraKhaiBáo.values()
              if giáTrịMục['giáTrịLoại']==501 and giáTrịMục['tên'] in bảngTraTên and giáTrịMục['tên'] not in địnhNghĩaChuẩn}
    for đườngDẫn in sorted({Path(giáTrịMục['Tệp']) for giáTrịMục in bảngTraKhaiBáo.values()}):
        danhSáchDòng = đườngDẫn.read_text().splitlines(True); làSựTiếpDiễn = False
        for sốHiệu,dòng in enumerate(danhSáchDòng):
            nguồnTiềnXửLý = làSựTiếpDiễn or bool(re.match(r'\s*#',dòng))
            làSựTiếpDiễn = nguồnTiềnXửLý and dòng.rstrip().endswith('\\')
            if nguồnTiềnXửLý:
                Bảng = bảngTraTên if re.match(r'\s*#\s*define\b',dòng) or làSựTiếpDiễn else giáTrịVĩLệnh
                danhSáchDòng[sốHiệu] = từTừVựng.sub(lambda làĐãKhớp: Bảng.get(làĐãKhớp[0],làĐãKhớp[0]) if làĐãKhớp[0] not in địnhNghĩaChuẩn else làĐãKhớp[0],dòng)
        đườngDẫn.write_text(''.join(danhSáchDòng))
    # 각 tựThân dịchThuậtNguồn 단위에만 연결표를 넣는다. giáTrịBênNgoài 배포본에는 전파하지 않는다.
    for đườngDẫn in sorted({Path(giáTrịMục['Tệp']) for giáTrịMục in bảngTraKhaiBáo.values()}):
        if đườngDẫn.suffix not in ('.c','.cpp'):continue
        giáTrịĐốiTác = '../' * len(đườngDẫn.relative_to(gốcCâyDựÁn).parts[:-1]) + 'cáchĐặtTên/cácTênLiênKếtMáy.h'
        đườngDẫn.write_text('#include "'+giáTrịĐốiTác+'"\n'+đườngDẫn.read_text())
    (gốcCâyDựÁn/'cáchĐặtTên/phépÁnhXạTênC.tsv').write_text('\n'.join(bảnGhiNhậtKý)+'\n')
    (gốcCâyDựÁn/'build/한국어화/전처리참조.json').write_text(json.dumps(bỏQuaGiáTrị,ensure_ascii=False,indent=2)+'\n')
    print('đổiGiáTrị',len(bảnGhiNhậtKý)-1,'nguồnTiềnXửLý 재검토',len(bỏQuaGiáTrị),'máy nốiKết',len(bảngTraKếtNối))

if __name__=='__main__': thựcThiLệnh()
