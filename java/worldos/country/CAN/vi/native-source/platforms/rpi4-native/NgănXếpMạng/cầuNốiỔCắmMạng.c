#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "NgănXếpMạng.h"
extern int32_t ổCắmMạngMạngVòngJava(int32_t,int32_t,int32_t), ràngBuộcMạngVòngJava(int32_t,int32_t,int32_t);
extern int32_t gửiMạngVòngJava(int32_t,int32_t,int32_t,int32_t), nhậnGọnMạngVòngJava(int32_t,int32_t);
extern int32_t cổngMạngVòngJava(int32_t), địaChỉMạngVòngJava(int32_t), đốiTácMạngVòngJava(int32_t), đóngMạngVòngJava(int32_t);
extern int32_t đặtMạngJava(int32_t,int32_t),lấyMạngJava(int32_t);
extern int32_t tạoLuồngVòngJava(void),ràngBuộcLuồngVòngJava(int32_t,int32_t,int32_t),lắngNgheLuồngVòngJava(int32_t,int32_t);
extern int32_t kếtNốiLuồngVòngJava(int32_t,int32_t,int32_t),chấpNhậnLuồngVòngJava(int32_t),đọcLuồngVòngJava(int32_t,int32_t),ghiLuồngVòngJava(int32_t,int32_t);
extern int32_t cổngLuồngVòngJava(int32_t),đốiTácLuồngVòngJava(int32_t),đóngLuồngVòngJava(int32_t);
static int bênNgoài[24];
static int địaChỉBấtKỳ[24], bộLắngNgheKép[24], đốiTácBênNgoàiUDP[8], địaChỉCận[8];
static int sốBênNgoài(int thẻXửLýTệp) { return thẻXửLýTệp>=32 && thẻXửLýTệp<56 ? bênNgoài[thẻXửLýTệp-32]-1 : -1; }
static int vănBảnDán(int thẻXửLýTệp,int loạiMụcKiểu) {
    if(thẻXửLýTệp<32||thẻXửLýTệp>=56)return -9;int phầnMụcTrướcĐó=sốBênNgoài(thẻXửLýTệp);if(phầnMụcTrướcĐó>=0)return phầnMụcTrướcĐó;
    int sốLượngPhầnMục=tạoĐiểmCuốiỔCắmMạng(loạiMụcKiểu);if(sốLượngPhầnMục>=0)bênNgoài[thẻXửLýTệp-32]=sốLượngPhầnMục+1;return sốLượngPhầnMục;
}
int32_t ổCắmMạngMạngJava(int32_t giáTrịĐầuTiên,int32_t giáTrịThứHai,int32_t mãKýTự){return ổCắmMạngMạngVòngJava(giáTrịĐầuTiên,giáTrịThứHai,mãKýTự);}
int32_t ràngBuộcMạngJava(int32_t thẻXửLýTệp,int32_t ĐịaChỉLiênMạng,int32_t sốCổng){
    if(ĐịaChỉLiênMạng==0x7f000001)return ràngBuộcMạngVòngJava(thẻXửLýTệp,ĐịaChỉLiênMạng,sốCổng);
    if(ĐịaChỉLiênMạng!=0&&ĐịaChỉLiênMạng!=đọcTìnhTrạngMạng(0,0))return -99;
    int giáTrịĐãTrảVề=ràngBuộcMạngVòngJava(thẻXửLýTệp,0,sốCổng);if(giáTrịĐãTrảVề<0)return giáTrịĐãTrảVề;
    int sốLượngPhầnMục=vănBảnDán(thẻXửLýTệp,2);if(sốLượngPhầnMục<0)return sốLượngPhầnMục;giáTrịĐãTrảVề=ràngBuộcMạngGọn(sốLượngPhầnMục,đọcTìnhTrạngMạng(0,0),cổngMạngVòngJava(thẻXửLýTệp));if(!giáTrịĐãTrảVề)địaChỉCận[thẻXửLýTệp-32]=ĐịaChỉLiênMạng;return giáTrịĐãTrảVề;
}
int32_t gửiMạngJava(int32_t thẻXửLýTệp,int32_t ĐịaChỉLiênMạng,int32_t sốCổng,int32_t cỡ){
    if(ĐịaChỉLiênMạng==0x7f000001)return gửiMạngVòngJava(thẻXửLýTệp,ĐịaChỉLiênMạng,sốCổng,cỡ);
    if(cỡ<0||cỡ>512)return -90;if(sốCổng<1||sốCổng>65535)return -22;
    if(cổngMạngVòngJava(thẻXửLýTệp)<0)return -9;
    if(địaChỉMạngVòngJava(thẻXửLýTệp)==0x7f000001)return -101;
    int sốLượngPhầnMục=sốBênNgoài(thẻXửLýTệp);if(sốLượngPhầnMục<0){int giáTrịĐãTrảVề=0;if(cổngMạngVòngJava(thẻXửLýTệp)==0)giáTrịĐãTrảVề=ràngBuộcMạngVòngJava(thẻXửLýTệp,0,0);if(giáTrịĐãTrảVề<0)return giáTrịĐãTrảVề;sốLượngPhầnMục=vănBảnDán(thẻXửLýTệp,2);if(sốLượngPhầnMục<0)return sốLượngPhầnMục;giáTrịĐãTrảVề=ràngBuộcMạngGọn(sốLượngPhầnMục,đọcTìnhTrạngMạng(0,0),cổngMạngVòngJava(thẻXửLýTệp));if(giáTrịĐãTrảVề<0)return giáTrịĐãTrảVề;}
    unsigned char DữLiệu[512];for(int chỉSốThứBậc=0;chỉSốThứBậc<cỡ;chỉSốThứBậc++)DữLiệu[chỉSốThứBậc]=lấyMạngJava(chỉSốThứBậc);return gửiĐiệnDữLiệu(sốLượngPhầnMục,DữLiệu,cỡ,ĐịaChỉLiênMạng,sốCổng);
}
int32_t nhậnGọnMạngJava(int32_t thẻXửLýTệp,int32_t cỡ){
    int sốLượngPhầnMục=sốBênNgoài(thẻXửLýTệp);if(sốLượngPhầnMục<0)return nhậnGọnMạngVòngJava(thẻXửLýTệp,cỡ);if(cỡ<0||cỡ>512)return -22;
    int cụcBộ=nhậnGọnMạngVòngJava(thẻXửLýTệp,cỡ);if(cụcBộ!=-11){đốiTácBênNgoàiUDP[thẻXửLýTệp-32]=0;return cụcBộ;}
    unsigned char DữLiệu[512];int giáTrịĐãTrảVề=nhậnĐiệnDữLiệu(sốLượngPhầnMục,DữLiệu,cỡ);if(giáTrịĐãTrảVề>=0)đốiTácBênNgoàiUDP[thẻXửLýTệp-32]=1;for(int chỉSốThứBậc=0;chỉSốThứBậc<giáTrịĐãTrảVề;chỉSốThứBậc++)đặtMạngJava(chỉSốThứBậc,DữLiệu[chỉSốThứBậc]);return giáTrịĐãTrảVề;
}
int32_t cổngMạngJava(int32_t thẻXửLýTệp){int sốLượngPhầnMục=sốBênNgoài(thẻXửLýTệp);return sốLượngPhầnMục<0?cổngMạngVòngJava(thẻXửLýTệp):(int32_t)sốCổngMạng(sốLượngPhầnMục);}
int32_t địaChỉMạngJava(int32_t thẻXửLýTệp){return sốBênNgoài(thẻXửLýTệp)<0?địaChỉMạngVòngJava(thẻXửLýTệp):địaChỉCận[thẻXửLýTệp-32];}
int32_t đốiTácMạngJava(int32_t thẻXửLýTệp){int sốLượngPhầnMục=sốBênNgoài(thẻXửLýTệp);return sốLượngPhầnMục<0||!đốiTácBênNgoàiUDP[thẻXửLýTệp-32]?đốiTácMạngVòngJava(thẻXửLýTệp):(int32_t)sốCổngĐốiTác(sốLượngPhầnMục);}
int32_t từXaMạngJava(int32_t thẻXửLýTệp){int sốLượngPhầnMục=sốBênNgoài(thẻXửLýTệp);return sốLượngPhầnMục<0||!đốiTácBênNgoàiUDP[thẻXửLýTệp-32]?0x7f000001:(int32_t)địaChỉĐốiTácMạngGọn(sốLượngPhầnMục);}
int32_t đóngMạngJava(int32_t thẻXửLýTệp){int sốLượngPhầnMục=sốBênNgoài(thẻXửLýTệp);if(sốLượngPhầnMục>=0){đóngMạng(sốLượngPhầnMục);bênNgoài[thẻXửLýTệp-32]=0;}if(thẻXửLýTệp>=32&&thẻXửLýTệp<40)đốiTácBênNgoàiUDP[thẻXửLýTệp-32]=địaChỉCận[thẻXửLýTệp-32]=0;return đóngMạngVòngJava(thẻXửLýTệp);}
int32_t tạoLuồngJava(void){return tạoLuồngVòngJava();}
int32_t ràngBuộcLuồngJava(int32_t thẻXửLýTệp,int32_t ĐịaChỉLiênMạng,int32_t sốCổng){
    if(ĐịaChỉLiênMạng==0||ĐịaChỉLiênMạng==0x7f000001){int giáTrịĐãTrảVề=ràngBuộcLuồngVòngJava(thẻXửLýTệp,ĐịaChỉLiênMạng,sốCổng);if(!giáTrịĐãTrảVề)địaChỉBấtKỳ[thẻXửLýTệp-32]=ĐịaChỉLiênMạng==0;return giáTrịĐãTrảVề;}
    if(ĐịaChỉLiênMạng!=đọcTìnhTrạngMạng(0,0))return -99;int giáTrịĐãTrảVề=ràngBuộcLuồngVòngJava(thẻXửLýTệp,0,sốCổng);if(giáTrịĐãTrảVề<0)return giáTrịĐãTrảVề;
    int sốLượngPhầnMục=vănBảnDán(thẻXửLýTệp,1);return sốLượngPhầnMục<0?sốLượngPhầnMục:ràngBuộcMạngGọn(sốLượngPhầnMục,ĐịaChỉLiênMạng,cổngLuồngVòngJava(thẻXửLýTệp));
}
int32_t lắngNgheLuồngJava(int32_t thẻXửLýTệp,int32_t hàngĐợiChờ){
    int sốLượngPhầnMục=sốBênNgoài(thẻXửLýTệp);if(sốLượngPhầnMục<0){int giáTrịĐãTrảVề=lắngNgheLuồngVòngJava(thẻXửLýTệp,hàngĐợiChờ);if(giáTrịĐãTrảVề<0||!địaChỉBấtKỳ[thẻXửLýTệp-32])return giáTrịĐãTrảVề;
        sốLượngPhầnMục=vănBảnDán(thẻXửLýTệp,1);if(sốLượngPhầnMục<0)return sốLượngPhầnMục;giáTrịĐãTrảVề=ràngBuộcMạngGọn(sốLượngPhầnMục,đọcTìnhTrạngMạng(0,0),cổngLuồngVòngJava(thẻXửLýTệp));if(giáTrịĐãTrảVề<0)return giáTrịĐãTrảVề;bộLắngNgheKép[thẻXửLýTệp-32]=1;
    }return hàngĐợiChờ<1?-22:lắngNgheMạngGọn(sốLượngPhầnMục);
}
int32_t kếtNốiLuồngJava(int32_t thẻXửLýTệp,int32_t ĐịaChỉLiênMạng,int32_t sốCổng){
    if(ĐịaChỉLiênMạng==0x7f000001 && sốBênNgoài(thẻXửLýTệp)<0)return kếtNốiLuồngVòngJava(thẻXửLýTệp,ĐịaChỉLiênMạng,sốCổng);
    if(cổngLuồngVòngJava(thẻXửLýTệp)<0)return -9;int sốLượngPhầnMục=vănBảnDán(thẻXửLýTệp,1);return sốLượngPhầnMục<0?sốLượngPhầnMục:kếtNốiMạngGọn(sốLượngPhầnMục,ĐịaChỉLiênMạng,sốCổng);
}
int32_t chấpNhậnLuồngJava(int32_t thẻXửLýTệp){
    int sốLượngPhầnMục=sốBênNgoài(thẻXửLýTệp);if(sốLượngPhầnMục<0)return chấpNhậnLuồngVòngJava(thẻXửLýTệp);
    if(bộLắngNgheKép[thẻXửLýTệp-32]){int cụcBộ=chấpNhậnLuồngVòngJava(thẻXửLýTệp);if(cụcBộ!=-11)return cụcBộ;}
    int giáTrịĐốiTác=chấpNhậnMạngGọn(sốLượngPhầnMục);if(giáTrịĐốiTác<0)return giáTrịĐốiTác;
    int giáTrịĐốiĐích=tạoLuồngVòngJava();if(giáTrịĐốiĐích<0){đóngMạng(giáTrịĐốiTác);return giáTrịĐốiĐích;}bênNgoài[giáTrịĐốiĐích-32]=giáTrịĐốiTác+1;return giáTrịĐốiĐích;
}
int32_t đọcLuồngJava(int32_t thẻXửLýTệp,int32_t cỡ){
    int sốLượngPhầnMục=sốBênNgoài(thẻXửLýTệp);if(sốLượngPhầnMục<0)return đọcLuồngVòngJava(thẻXửLýTệp,cỡ);if(cỡ<0||cỡ>512)return -22;
    unsigned char DữLiệu[512];int giáTrịĐãTrảVề=đọcMạngGọn(sốLượngPhầnMục,DữLiệu,cỡ);for(int chỉSốThứBậc=0;chỉSốThứBậc<giáTrịĐãTrảVề;chỉSốThứBậc++)đặtMạngJava(chỉSốThứBậc,DữLiệu[chỉSốThứBậc]);return giáTrịĐãTrảVề;
}
int32_t ghiLuồngJava(int32_t thẻXửLýTệp,int32_t cỡ){
    int sốLượngPhầnMục=sốBênNgoài(thẻXửLýTệp);if(sốLượngPhầnMục<0)return ghiLuồngVòngJava(thẻXửLýTệp,cỡ);if(cỡ<0||cỡ>512)return -22;
    unsigned char DữLiệu[512];for(int chỉSốThứBậc=0;chỉSốThứBậc<cỡ;chỉSốThứBậc++)DữLiệu[chỉSốThứBậc]=lấyMạngJava(chỉSốThứBậc);return ghiMạngGọn(sốLượngPhầnMục,DữLiệu,cỡ);
}
int32_t cổngLuồngJava(int32_t thẻXửLýTệp){int sốLượngPhầnMục=sốBênNgoài(thẻXửLýTệp);return sốLượngPhầnMục<0?cổngLuồngVòngJava(thẻXửLýTệp):(int32_t)sốCổngMạng(sốLượngPhầnMục);}
int32_t đốiTácLuồngJava(int32_t thẻXửLýTệp){int sốLượngPhầnMục=sốBênNgoài(thẻXửLýTệp);return sốLượngPhầnMục<0?đốiTácLuồngVòngJava(thẻXửLýTệp):(int32_t)sốCổngĐốiTác(sốLượngPhầnMục);}
int32_t địaChỉLuồngJava(int32_t thẻXửLýTệp){return sốBênNgoài(thẻXửLýTệp)<0?0x7f000001:bộLắngNgheKép[thẻXửLýTệp-32]?0:đọcTìnhTrạngMạng(0,0);}
int32_t đóngLuồngJava(int32_t thẻXửLýTệp){int sốLượngPhầnMục=sốBênNgoài(thẻXửLýTệp);if(sốLượngPhầnMục>=0){đóngMạng(sốLượngPhầnMục);bênNgoài[thẻXửLýTệp-32]=0;}if(thẻXửLýTệp>=40&&thẻXửLýTệp<56)địaChỉBấtKỳ[thẻXửLýTệp-32]=bộLắngNgheKép[thẻXửLýTệp-32]=0;return đóngLuồngVòngJava(thẻXửLýTệp);}
