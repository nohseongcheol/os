#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "gọiThựcHiện.h"
#include "GóiGộp.h"
#include "uzlib.h"
static unsigned char khoLưuTrữ[16384], đãGiảiGói[16385];
static unsigned cỡ, trungTâm, danhSáchCácMục;
static char lớpMục[256];
static unsigned đọcCácByteHai(unsigned vịTríHiệnTại) { return khoLưuTrữ[vịTríHiệnTại] | khoLưuTrữ[vịTríHiệnTại+1] << 8; }
static uint32_t đọcCácByteBốn(unsigned vịTríHiệnTại) { return đọcCácByteHai(vịTríHiệnTại) | (uint32_t)đọcCácByteHai(vịTríHiệnTại+2) << 16; }
static int cắtXén(unsigned vịTríHiệnTại, unsigned sốLượngPhầnMục, unsigned giớiHạnSứcChứa) { return vịTríHiệnTại <= giớiHạnSứcChứa && sốLượngPhầnMục <= giớiHạnSứcChứa-vịTríHiệnTại; }
static size_t độDài(const char *dữLiệuChuỗi) { size_t sốLượngPhầnMục=0; while(dữLiệuChuỗi[sốLượngPhầnMục]) sốLượngPhầnMục++; return sốLượngPhầnMục; }
static int vănBảnBằng(const unsigned char *giáTrịĐầuTiên, const unsigned char *giáTrịThứHai, unsigned sốLượngPhầnMục) { for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhầnMục;chỉSốThứBậc++)if(giáTrịĐầuTiên[chỉSốThứBậc]!=giáTrịThứHai[chỉSốThứBậc])return 0;return 1; }
static int kếtThúcTệp(void *chưaDùng) { (void)chưaDùng; return -1; }
static int dữLiệuThuộcTính(const char *dòng,unsigned sứcChứaĐãDùng,int *cóTồnTạiĐiểmMục) {
    if(sứcChứaĐãDùng>=12 && vănBảnBằng((const unsigned char*)dòng,(const unsigned char*)"Class-Path: ",12))return -95;
    if(sứcChứaĐãDùng>=12 && vănBảnBằng((const unsigned char*)dòng,(const unsigned char*)"Main-Class: ",12)) {
        unsigned giáTrị=sứcChứaĐãDùng-12;if(*cóTồnTạiĐiểmMục||!giáTrị||giáTrị>=sizeof(lớpMục))return -8;
        for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<giáTrị;chỉSốThứBậc++){unsigned char mãKýTự=dòng[12+chỉSốThứBậc];if(mãKýTự<=32||mãKýTự=='/'||mãKýTự=='\\')return -8;lớpMục[chỉSốThứBậc]=mãKýTự;}
        lớpMục[giáTrị]=0;*cóTồnTạiĐiểmMục=1;
    }
    return 0;
}
static int thànhViên(unsigned vịTríHiệnTại, unsigned char *dữLiệuKếtQuả, unsigned tốiĐaSứcChứa) {
    unsigned mụcPhươngThức=đọcCácByteHai(vịTríHiệnTại+10), cácBitCấuHình=đọcCácByteHai(vịTríHiệnTại+8), đãNén=đọcCácByteBốn(vịTríHiệnTại+20), giảiPhóngCỡ=đọcCácByteBốn(vịTríHiệnTại+24), cụcBộ=đọcCácByteBốn(vịTríHiệnTại+42);
    unsigned tên=đọcCácByteHai(vịTríHiệnTại+28);
    if(giảiPhóngCỡ>tốiĐaSứcChứa || giảiPhóngCỡ>16384 || (mụcPhươngThức!=0 && mụcPhươngThức!=8) || (cácBitCấuHình&~0x80e))return -8;
    if(!cắtXén(cụcBộ,30,trungTâm) || đọcCácByteBốn(cụcBộ)!=0x04034b50 || đọcCácByteHai(cụcBộ+8)!=mụcPhươngThức || đọcCácByteHai(cụcBộ+6)!=cácBitCấuHình || đọcCácByteHai(cụcBộ+26)!=tên)return -8;
    unsigned bắtChạyĐộLệch=cụcBộ+30, miềnBổSung=đọcCácByteHai(cụcBộ+28);
    if(!cắtXén(bắtChạyĐộLệch,tên,trungTâm) || !vănBảnBằng(khoLưuTrữ+bắtChạyĐộLệch,khoLưuTrữ+vịTríHiệnTại+46,tên))return -8;
    bắtChạyĐộLệch+=tên;if(!cắtXén(bắtChạyĐộLệch,miềnBổSung,trungTâm))return -8;bắtChạyĐộLệch+=miềnBổSung;
    if(!cắtXén(bắtChạyĐộLệch,đãNén,trungTâm))return -8;
    if(!(cácBitCấuHình&8) && (đọcCácByteBốn(cụcBộ+14)!=đọcCácByteBốn(vịTríHiệnTại+16) || đọcCácByteBốn(cụcBộ+18)!=đãNén || đọcCácByteBốn(cụcBộ+22)!=giảiPhóngCỡ))return -8;
    if(mụcPhươngThức==0) { if(đãNén!=giảiPhóngCỡ)return -8; for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<giảiPhóngCỡ;chỉSốThứBậc++)dữLiệuKếtQuả[chỉSốThứBậc]=khoLưuTrữ[bắtChạyĐộLệch+chỉSốThứBậc]; }
    else {
        uzlib_uncomp_t dữLiệuĐích={0};uzlib_uncompress_init(&dữLiệuĐích,0,0);
        dữLiệuĐích.source=khoLưuTrữ+bắtChạyĐộLệch;dữLiệuĐích.source_limit=dữLiệuĐích.source+đãNén;dữLiệuĐích.source_read_cb=kếtThúcTệp;
        /* One extra output byte lets inflate consume/check the end marker. */
        dữLiệuĐích.dest_start=dữLiệuĐích.dest=đãGiảiGói;dữLiệuĐích.dest_limit=đãGiảiGói+giảiPhóngCỡ+1;
        int giáTrịĐãTrảVề=uzlib_uncompress(&dữLiệuĐích);
        if(giáTrịĐãTrảVề!=UZLIB_DONE || dữLiệuĐích.eof || dữLiệuĐích.dest!=đãGiảiGói+giảiPhóngCỡ || dữLiệuĐích.source!=dữLiệuĐích.source_limit)return -8;
        for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<giảiPhóngCỡ;chỉSốThứBậc++)dữLiệuKếtQuả[chỉSốThứBậc]=đãGiảiGói[chỉSốThứBậc];
    }
    if((uzlib_crc32(dữLiệuKếtQuả,giảiPhóngCỡ,0xffffffffu)^0xffffffffu)!=đọcCácByteBốn(vịTríHiệnTại+16))return -8;
    return giảiPhóngCỡ;
}
int đọcJAR(const char *tên, unsigned char *dữLiệuKếtQuả, unsigned sứcChứaBộĐệm) {
    if(!danhSáchCácMục)return -2;unsigned sốLượngPhầnMục=độDài(tên),vịTríHiệnTại=trungTâm;
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<danhSáchCácMục;chỉSốThứBậc++) {
        unsigned độDàiTên=đọcCácByteHai(vịTríHiệnTại+28);
        if(độDàiTên==sốLượngPhầnMục && vănBảnBằng(khoLưuTrữ+vịTríHiệnTại+46,(const unsigned char*)tên,sốLượngPhầnMục))return thànhViên(vịTríHiệnTại,dữLiệuKếtQuả,sứcChứaBộĐệm);
        vịTríHiệnTại+=46+độDàiTên+đọcCácByteHai(vịTríHiệnTại+30)+đọcCácByteHai(vịTríHiệnTại+32);
    }
    return -2;
}
const char *chínhJAR(void) { return lớpMục; }
int mởJAR(const char *tênMụcTệp) {
    danhSáchCácMục=0;lớpMục[0]=0;
    intptr_t thẻXửLýTệp=gọiThựcHiệnNgườiDùng(3,(uintptr_t)tênMụcTệp,0,0,0,0,0);if(thẻXửLýTệp<0)return thẻXửLýTệp;
    intptr_t sốLượngPhầnMục=gọiThựcHiệnNgườiDùng(9,thẻXửLýTệp,0,0,0,0,0);
    if(sốLượngPhầnMục<22 || sốLượngPhầnMục>(intptr_t)sizeof(khoLưuTrữ)) { gọiThựcHiệnNgườiDùng(4,thẻXửLýTệp,0,0,0,0,0);return -8; }
    intptr_t sốLượngĐãNhận=gọiThựcHiệnNgườiDùng(2,thẻXửLýTệp,(uintptr_t)khoLưuTrữ,sốLượngPhầnMục,0,0,0);gọiThựcHiệnNgườiDùng(4,thẻXửLýTệp,0,0,0,0,0);
    if(sốLượngĐãNhận!=sốLượngPhầnMục)return -5;cỡ=sốLượngPhầnMục;
    unsigned độLệchKếtThúc=cỡ-22;
    for(;;) { if(đọcCácByteBốn(độLệchKếtThúc)==0x06054b50 && độLệchKếtThúc+22+đọcCácByteHai(độLệchKếtThúc+20)==cỡ)break; if(!độLệchKếtThúc)return -8;độLệchKếtThúc--; }
    unsigned sốLượngMục=đọcCácByteHai(độLệchKếtThúc+10);trungTâm=đọcCácByteBốn(độLệchKếtThúc+16);
    if(đọcCácByteHai(độLệchKếtThúc+4)||đọcCácByteHai(độLệchKếtThúc+6)||đọcCácByteHai(độLệchKếtThúc+8)!=sốLượngMục||!sốLượngMục||sốLượngMục>256||!cắtXén(trungTâm,đọcCácByteBốn(độLệchKếtThúc+12),độLệchKếtThúc)||trungTâm+đọcCácByteBốn(độLệchKếtThúc+12)!=độLệchKếtThúc)return -8;
    unsigned vịTríHiệnTại=trungTâm;
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngMục;chỉSốThứBậc++) {
        if(!cắtXén(vịTríHiệnTại,46,độLệchKếtThúc)||đọcCácByteBốn(vịTríHiệnTại)!=0x02014b50||đọcCácByteHai(vịTríHiệnTại+34))return -8;
        unsigned độDàiTên=đọcCácByteHai(vịTríHiệnTại+28),phầnMụcKếTiếp=46+độDàiTên+đọcCácByteHai(vịTríHiệnTại+30)+đọcCácByteHai(vịTríHiệnTại+32);
        if(!độDàiTên||độDàiTên>511||!cắtXén(vịTríHiệnTại,phầnMụcKếTiếp,độLệchKếtThúc)||đọcCácByteBốn(vịTríHiệnTại+24)>16384)return -8;
        for(unsigned thứBậcPhíaTrong=0;thứBậcPhíaTrong<độDàiTên;thứBậcPhíaTrong++)if(!khoLưuTrữ[vịTríHiệnTại+46+thứBậcPhíaTrong])return -8;
        unsigned mụcKhác=trungTâm;
        for(unsigned thứBậcPhíaTrong=0;thứBậcPhíaTrong<chỉSốThứBậc;thứBậcPhíaTrong++){unsigned dữLiệuĐộDài=đọcCácByteHai(mụcKhác+28);if(dữLiệuĐộDài==độDàiTên&&vănBảnBằng(khoLưuTrữ+mụcKhác+46,khoLưuTrữ+vịTríHiệnTại+46,dữLiệuĐộDài))return -8;mụcKhác+=46+dữLiệuĐộDài+đọcCácByteHai(mụcKhác+30)+đọcCácByteHai(mụcKhác+32);}
        vịTríHiệnTại+=phầnMụcKếTiếp;
    }
    if(vịTríHiệnTại!=độLệchKếtThúc)return -8;danhSáchCácMục=sốLượngMục;
    unsigned char bảnKêGóiGộp[4096];int cỡNhóm=đọcJAR("META-INF/MANIFEST.MF",bảnKêGóiGộp,sizeof(bảnKêGóiGộp)-1);if(cỡNhóm<0){danhSáchCácMục=0;return -8;}
    bảnKêGóiGộp[cỡNhóm]=0;
    char luậnLýHọc[512];unsigned sứcChứaĐãDùng=0,giáTrịChỉSố=0;int cóTồnTạiĐiểmMục=0;
    while(giáTrịChỉSố<(unsigned)cỡNhóm) {
        unsigned chạy=giáTrịChỉSố;while(giáTrịChỉSố<(unsigned)cỡNhóm && bảnKêGóiGộp[giáTrịChỉSố]!='\n')giáTrịChỉSố++;
        unsigned dữLiệuĐộDài=giáTrịChỉSố-chạy;if(giáTrịChỉSố<(unsigned)cỡNhóm)giáTrịChỉSố++;if(dữLiệuĐộDài && bảnKêGóiGộp[chạy+dữLiệuĐộDài-1]=='\r')dữLiệuĐộDài--;
        if(sứcChứaĐãDùng && dữLiệuĐộDài && bảnKêGóiGộp[chạy]==' ') {chạy++;dữLiệuĐộDài--;}
        else {
            int kếtQuả=dữLiệuThuộcTính(luậnLýHọc,sứcChứaĐãDùng,&cóTồnTạiĐiểmMục);if(kếtQuả)return kếtQuả;
            sứcChứaĐãDùng=0;if(!dữLiệuĐộDài)break;
        }
        if(dữLiệuĐộDài>sizeof(luậnLýHọc)-sứcChứaĐãDùng)return -8;
        for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<dữLiệuĐộDài;chỉSốThứBậc++)luậnLýHọc[sứcChứaĐãDùng++]=bảnKêGóiGộp[chạy+chỉSốThứBậc];
    }
    /* The last attribute may be followed by only one newline. */
    int kếtQuả=dữLiệuThuộcTính(luậnLýHọc,sứcChứaĐãDùng,&cóTồnTạiĐiểmMục);if(kếtQuả)return kếtQuả;
    return cóTồnTạiĐiểmMục?0:-8;
}
