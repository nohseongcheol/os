/* dữLiệuThựcTế MànHình 메모리와 기존 C gọiThựcHiện 규약만 연결한다. 합성 구현은 mãNguồn/BộGhépBộĐệmKhung.java. */
#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
#include "thôngTinMànHình.h"
static volatile uint32_t *danhSáchCácĐiểmẢnh;
static unsigned sốLượngTừHàngMànHình, rộngMànHình, caoMànHình;
extern void chuẩnBịVẽJava(int,int),kếtThúcVẽJava(void),hìnhChữNhậtVẽJava(int,int,int,int,int),conTrỏVẽJava(int,int,int);
extern int rộngVẽJava(void),caoVẽJava(void),thấpSốLượngVẽJava(void),caoTrênSốLượngVẽJava(void);
extern int cắtXénVẽJava(int,int,int,int),giáTrịCắtXénVẽJava(int),bắtĐầuVẽJava(int,int,int,int),điểmẢnhVẽJava(int,int,int);
uintptr_t đọcBộĐệmKhungBoMạch(uintptr_t vịTríNgang,uintptr_t vịTríDọc){
    return danhSáchCácĐiểmẢnh&&vịTríNgang<rộngMànHình&&vịTríDọc<caoMànHình?danhSáchCácĐiểmẢnh[vịTríDọc*sốLượngTừHàngMànHình+vịTríNgang]:0;
}
void ghiBộĐệmKhungBoMạch(uintptr_t vịTríNgang,uintptr_t vịTríDọc,uintptr_t giáTrịMàu){
    if(danhSáchCácĐiểmẢnh&&vịTríNgang<rộngMànHình&&vịTríDọc<caoMànHình)danhSáchCácĐiểmẢnh[vịTríDọc*sốLượngTừHàngMànHình+vịTríNgang]=(uint32_t)giáTrịMàu;
}
void bảnVẽChuẩnBịBoMạch(volatile uint32_t *DữLiệu,unsigned khoảngTrảiRộng,unsigned độDài,unsigned giáTrịGiãnCáchDòng){
    danhSáchCácĐiểmẢnh=DữLiệu;rộngMànHình=khoảngTrảiRộng;caoMànHình=độDài;sốLượngTừHàngMànHình=giáTrịGiãnCáchDòng/4;chuẩnBịVẽJava((int)khoảngTrảiRộng,(int)độDài);
}
uintptr_t rộngMànHìnhBoMạch(void){return (unsigned)rộngVẽJava();}
uintptr_t caoMànHìnhBoMạch(void){return (unsigned)caoVẽJava();}
uint64_t sốLượngBảnVẽBoMạch(void){return ((uint64_t)(uint32_t)caoTrênSốLượngVẽJava()<<32)|(uint32_t)thấpSốLượngVẽJava();}
uint32_t mànHìnhĐọcBoMạch(unsigned vịTríNgang,unsigned vịTríDọc){return (uint32_t)đọcBộĐệmKhungBoMạch(vịTríNgang,vịTríDọc);}
int cácCậnBảnVẽBoMạch(int *vịTríNgang,int *vịTríDọc,int *khoảngTrảiRộng,int *độDài){
    if(!cắtXénVẽJava(*vịTríNgang,*vịTríDọc,*khoảngTrảiRộng,*độDài))return 0;
    *vịTríNgang=giáTrịCắtXénVẽJava(0);*vịTríDọc=giáTrịCắtXénVẽJava(1);*khoảngTrảiRộng=giáTrịCắtXénVẽJava(2);*độDài=giáTrịCắtXénVẽJava(3);return 1;
}
int bảnVẽBắtChạyBoMạch(int vịTríNgang,int vịTríDọc,int khoảngTrảiRộng,int độDài){return bắtĐầuVẽJava(vịTríNgang,vịTríDọc,khoảngTrảiRộng,độDài);}
void bảnVẽHoànThànhBoMạch(void){kếtThúcVẽJava();}
uintptr_t điểmẢnhBoMạch(uintptr_t vịTríNgang,uintptr_t vịTríDọc,uintptr_t giáTrịMàu){return (unsigned)điểmẢnhVẽJava((int)vịTríNgang,(int)vịTríDọc,(int)giáTrịMàu);}
void lấpHìnhChữNhậtBoMạch(int vịTríNgang,int vịTríDọc,int khoảngTrảiRộng,int độDài,uint32_t giáTrịMàu){hìnhChữNhậtVẽJava(vịTríNgang,vịTríDọc,khoảngTrảiRộng,độDài,(int)giáTrịMàu);}
void conTrỏBoMạch(int vịTríNgang,int vịTríDọc,unsigned giáTrịHình){conTrỏVẽJava(vịTríNgang,vịTríDọc,(int)giáTrịHình);}
