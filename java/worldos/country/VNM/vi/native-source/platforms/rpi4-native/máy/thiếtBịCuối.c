#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
#include "thôngTinMànHình.h"
/* tựThân 네 cửaSổ 합성과 UTF-8 thiếtBịCuối. 바뀐 영역의 giáTrịĐãHoànTất 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t từMáy;
extern từMáy điểmẢnhBoMạch(từMáy,từMáy,từMáy),bộĐệmKhungBoMạch(void);
extern void *memset(void *,int,size_t);
extern const unsigned char phôngChữThiếtBịCuối[];
#define cácCộtTốiĐa 237
#define sốLượngDòngLịchSử 160
typedef struct {
    uint32_t cácÔKýTự[sốLượngDòngLịchSử][cácCộtTốiĐa]; uint8_t danhSáchCácHình[sốLượngDòngLịchSử][cácCộtTốiĐa];
    unsigned giáTrịRộng,giáTrịCao,cácCột,sốLượngHàng,đãĐổiCỡĐãLà;
    unsigned làĐangSống,tọaĐộX,tọaĐộY,vịTríHàng,vịTríCột,mụcĐỉnh,cuộn,màuTiềnCảnh,màuNền,thoát,giáTrịThamSố[4],chỉSốThamSố,hàngĐãLưu,cộtGọnĐãLưu;
    unsigned kếtQuảKhôngDấu,giáTrịDàiKhôngDấu,giáTrịBé,thayThế,hiệnĐượcDấuNháy;
} ThiếtBịCuối;
static ThiếtBịCuối danhSáchCácCửaSổ[4];
static int tiêuĐiểm=-1,đầuRa,giáTrịThứTự[4],sốLượngMục,giáTrịKéo=-1,xKéo,yKéo;
static unsigned làĐangChờ,cácNút,khungNhìnMànLàmViệc,đầuVàoHangul;
static const uint32_t cácMàuĐiểmẢnh[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int hiệnĐượcMànHình(int),conTrỏMànHình(int,unsigned,int,int);
extern void mànHìnhVẽLại(int);
static ThiếtBịCuối *mụcThiếtBịCuối;
static unsigned kýTựRộngKiểu(unsigned mãKýTự){return mãKýTự>=256?2:1;}
static void miềnDạngChữNhật(unsigned tọaĐộX,unsigned tọaĐộY,unsigned giáTrịRộngĐãYêuCầu,unsigned giáTrịCaoĐãYêuCầu,unsigned màuĐiểmẢnh){
    lấpHìnhChữNhậtBoMạch(tọaĐộX,tọaĐộY,giáTrịRộngĐãYêuCầu,giáTrịCaoĐãYêuCầu,màuĐiểmẢnh);
}
void hìnhChữThiếtBịCuối(unsigned tọaĐộX,unsigned tọaĐộY,unsigned mãKýTự,unsigned màuTiềnCảnh,unsigned màuNền){
    unsigned giáTrịRộng=kýTựRộngKiểu(mãKýTự)*8;if(mãKýTự==0xffffffffu)return;
    int bênTrái=tọaĐộX,bênThượng=tọaĐộY,khoảngTrảiRộng=giáTrịRộng,độDài=16;
    if(!cácCậnBảnVẽBoMạch(&bênTrái,&bênThượng,&khoảngTrảiRộng,&độDài))return;
    if(mãKýTự==' '){lấpHìnhChữNhậtBoMạch(bênTrái,bênThượng,khoảngTrảiRộng,độDài,màuNền);return;}
    unsigned chỉSốTraCứu=mãKýTự<65536?mãKýTự:mãKýTự>=0x1f600&&mãKýTự<0x1f650?65536+mãKýTự-0x1f600:0xfffd;
    const unsigned char *giáTrịPhôngChữ=phôngChữThiếtBịCuối+chỉSốTraCứu*32;
    for(int dòng=bênThượng;dòng<bênThượng+độDài;dòng++){unsigned danhSáchCácBit=giáTrịPhôngChữ[(dòng-tọaĐộY)*2]*256+giáTrịPhôngChữ[(dòng-tọaĐộY)*2+1];for(int mụcÔ=bênTrái;mụcÔ<bênTrái+khoảngTrảiRộng;mụcÔ++)điểmẢnhBoMạch(mụcÔ,dòng,(danhSáchCácBit&(0x8000>>(mụcÔ-tọaĐộX)))?màuTiềnCảnh:màuNền);}
}
static void bảngTraTên(unsigned tọaĐộX,unsigned tọaĐộY,const char *dữLiệuChuỗi,unsigned màuTiềnCảnh,unsigned màuNền){while(*dữLiệuChuỗi){unsigned mãKýTự=(unsigned char)*dữLiệuChuỗi++, sốLượngCònLại=0;if(mãKýTự>=0xc0){sốLượngCònLại=mãKýTự<0xe0?1:mãKýTự<0xf0?2:3;mãKýTự&=(1u<<(6-sốLượngCònLại))-1;while(sốLượngCònLại--&&*dữLiệuChuỗi)mãKýTự=(mãKýTự<<6)|((unsigned char)*dữLiệuChuỗi++&63);}hìnhChữThiếtBịCuối(tọaĐộX,tọaĐộY,mãKýTự,màuTiềnCảnh,màuNền);tọaĐộX+=kýTựRộngKiểu(mãKýTự)*8;}}
static unsigned mụcĐầuTiên(void){return mụcThiếtBịCuối->mụcĐỉnh;}
static int làĐãHiện(void){return mụcThiếtBịCuối->làĐangSống&&tiêuĐiểm>=0&&mụcThiếtBịCuối==&danhSáchCácCửaSổ[tiêuĐiểm]&&!hiệnĐượcMànHình(tiêuĐiểm);}
static void mànHìnhTô(unsigned vịTríHàng,unsigned vịTríCột){
    if(!làĐãHiện()||vịTríHàng<mụcĐầuTiên()-mụcThiếtBịCuối->cuộn||vịTríHàng>=mụcĐầuTiên()-mụcThiếtBịCuối->cuộn+mụcThiếtBịCuối->sốLượngHàng||vịTríCột>=mụcThiếtBịCuối->cácCột)return;
    unsigned mãKýTự=mụcThiếtBịCuối->cácÔKýTự[vịTríHàng%sốLượngDòngLịchSử][vịTríCột],dữLiệuChuỗi=mụcThiếtBịCuối->danhSáchCácHình[vịTríHàng%sốLượngDòngLịchSử][vịTríCột];
    if(kýTựRộngKiểu(mãKýTự)==2&&vịTríCột+1>=mụcThiếtBịCuối->cácCột)mãKýTự=' ';
    hìnhChữThiếtBịCuối(mụcThiếtBịCuối->tọaĐộX+12+vịTríCột*8,mụcThiếtBịCuối->tọaĐộY+36+(vịTríHàng-mụcĐầuTiên()+mụcThiếtBịCuối->cuộn)*16,mãKýTự?mãKýTự:' ',cácMàuĐiểmẢnh[dữLiệuChuỗi&15],cácMàuĐiểmẢnh[dữLiệuChuỗi>>4]);
}
static void giáTrịDấuNháy(int hiệnCửaSổ){if(!làĐãHiện()||mụcThiếtBịCuối->cuộn||mụcThiếtBịCuối->vịTríCột>=mụcThiếtBịCuối->cácCột||mụcThiếtBịCuối->vịTríHàng<mụcThiếtBịCuối->mụcĐỉnh||mụcThiếtBịCuối->vịTríHàng>=mụcThiếtBịCuối->mụcĐỉnh+mụcThiếtBịCuối->sốLượngHàng)return;
    if(!hiệnCửaSổ||!mụcThiếtBịCuối->hiệnĐượcDấuNháy)mànHìnhTô(mụcThiếtBịCuối->vịTríHàng,mụcThiếtBịCuối->vịTríCột);else miềnDạngChữNhật(mụcThiếtBịCuối->tọaĐộX+12+mụcThiếtBịCuối->vịTríCột*8,mụcThiếtBịCuối->tọaĐộY+36+(mụcThiếtBịCuối->vịTríHàng-mụcThiếtBịCuối->mụcĐỉnh)*16+14,8,2,cácMàuĐiểmẢnh[mụcThiếtBịCuối->màuTiềnCảnh]);}
static void giáTrịNộiDung(void){
    miềnDạngChữNhật(mụcThiếtBịCuối->tọaĐộX+12,mụcThiếtBịCuối->tọaĐộY+36,mụcThiếtBịCuối->cácCột*8,mụcThiếtBịCuối->sốLượngHàng*16,cácMàuĐiểmẢnh[0]);
    int vịTríNgang=mụcThiếtBịCuối->tọaĐộX+12,vịTríDọc=mụcThiếtBịCuối->tọaĐộY+36,khoảngTrảiRộng=mụcThiếtBịCuối->cácCột*8,độDài=mụcThiếtBịCuối->sốLượngHàng*16;
    if(cácCậnBảnVẽBoMạch(&vịTríNgang,&vịTríDọc,&khoảngTrảiRộng,&độDài)){
    unsigned dòngĐầuTiên=(vịTríDọc-mụcThiếtBịCuối->tọaĐộY-36)/16,dòngCuối=(vịTríDọc+độDài-mụcThiếtBịCuối->tọaĐộY-36+15)/16;
    unsigned ôĐầuTiên=(vịTríNgang-mụcThiếtBịCuối->tọaĐộX-12)/8,ôCuối=(vịTríNgang+khoảngTrảiRộng-mụcThiếtBịCuối->tọaĐộX-12+7)/8;
    if(ôĐầuTiên)ôĐầuTiên--; /* 잘림 giáTrịRanhGiới 왼쪽에서 시작한 두 mụcÔ 글자도 그린다. */
    for(unsigned giáTrịĐãTrảVề=dòngĐầuTiên;giáTrịĐãTrảVề<dòngCuối;giáTrịĐãTrảVề++)for(unsigned mãKýTự=ôĐầuTiên;mãKýTự<ôCuối;mãKýTự++){
        unsigned vịTríHàng=mụcĐầuTiên()-mụcThiếtBịCuối->cuộn+giáTrịĐãTrảVề,giáTrịKýTự=mụcThiếtBịCuối->cácÔKýTự[vịTríHàng%sốLượngDòngLịchSử][mãKýTự],dữLiệuChuỗi=mụcThiếtBịCuối->danhSáchCácHình[vịTríHàng%sốLượngDòngLịchSử][mãKýTự];
        if(kýTựRộngKiểu(giáTrịKýTự)==2&&mãKýTự+1>=mụcThiếtBịCuối->cácCột)giáTrịKýTự=' ';
        if((giáTrịKýTự==0||giáTrịKýTự==' ')&&(dữLiệuChuỗi>>4)==0)continue;
        hìnhChữThiếtBịCuối(mụcThiếtBịCuối->tọaĐộX+12+mãKýTự*8,mụcThiếtBịCuối->tọaĐộY+36+giáTrịĐãTrảVề*16,giáTrịKýTự?giáTrịKýTự:' ',cácMàuĐiểmẢnh[dữLiệuChuỗi&15],cácMàuĐiểmẢnh[dữLiệuChuỗi>>4]);
    }}
    bảngTraTên(mụcThiếtBịCuối->tọaĐộX+12,mụcThiếtBịCuối->tọaĐộY+mụcThiếtBịCuối->giáTrịCao-18,mụcThiếtBịCuối->cuộn?"PgDn: recent output":mụcThiếtBịCuối->giáTrịRộng>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);giáTrịDấuNháy(1);
}
static void khungViệcThựcThi(int giáTrịĐịnhDanh){
    mụcThiếtBịCuối=&danhSáchCácCửaSổ[giáTrịĐịnhDanh];
    int vịTríNgang=mụcThiếtBịCuối->tọaĐộX,vịTríDọc=mụcThiếtBịCuối->tọaĐộY,khoảngTrảiRộng=mụcThiếtBịCuối->giáTrịRộng,độDài=mụcThiếtBịCuối->giáTrịCao;
    if(!cácCậnBảnVẽBoMạch(&vịTríNgang,&vịTríDọc,&khoảngTrảiRộng,&độDài))return;
    miềnDạngChữNhật(mụcThiếtBịCuối->tọaĐộX,mụcThiếtBịCuối->tọaĐộY,mụcThiếtBịCuối->giáTrịRộng,mụcThiếtBịCuối->giáTrịCao,0x403127);
    unsigned màuĐiểmẢnh=giáTrịĐịnhDanh==tiêuĐiểm?0x905020:0x604438;miềnDạngChữNhật(mụcThiếtBịCuối->tọaĐộX,mụcThiếtBịCuối->tọaĐộY,mụcThiếtBịCuối->giáTrịRộng,30,màuĐiểmẢnh);
    bảngTraTên(mụcThiếtBịCuối->tọaĐộX+12,mụcThiếtBịCuối->tọaĐộY+7,"JKOROS Terminal",0xffffff,màuĐiểmẢnh);
    char giáTrịThuộcSố[2]={(char)('1'+giáTrịĐịnhDanh),0};bảngTraTên(mụcThiếtBịCuối->tọaĐộX+148,mụcThiếtBịCuối->tọaĐộY+7,giáTrịThuộcSố,0xffffff,màuĐiểmẢnh);
    bảngTraTên(mụcThiếtBịCuối->tọaĐộX+240,mụcThiếtBịCuối->tọaĐộY+7,mụcThiếtBịCuối->giáTrịRộng>=500?(đầuVàoHangul?"[VI] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(đầuVàoHangul?"[VI]":"[EN]"),0xffffff,màuĐiểmẢnh);
    miềnDạngChữNhật(mụcThiếtBịCuối->tọaĐộX+mụcThiếtBịCuối->giáTrịRộng-32,mụcThiếtBịCuối->tọaĐộY+4,26,22,0x5555b8);bảngTraTên(mụcThiếtBịCuối->tọaĐộX+mụcThiếtBịCuối->giáTrịRộng-24,mụcThiếtBịCuối->tọaĐộY+7,"X",0xffffff,0x5555b8);
    giáTrịNộiDung();
}
static void vẽCảnh(void){
    if(!khungNhìnMànLàmViệc)return;miềnDạngChữNhật(0,0,rộngMànHìnhBoMạch(),caoMànHìnhBoMạch(),0x302018);miềnDạngChữNhật(0,0,rộngMànHìnhBoMạch(),32,0x403127);
    miềnDạngChữNhật(6,4,136,24,0x905020);bảngTraTên(14,8,"+ New terminal",0xffffff,0x905020);
    for(int chỉSốThứBậc=0;chỉSốThứBậc<4;chỉSốThứBậc++)if(danhSáchCácCửaSổ[chỉSốThứBậc].làĐangSống){unsigned mãKýTự=tiêuĐiểm==chỉSốThứBậc?0x905020:0x604438;miềnDạngChữNhật(154+chỉSốThứBậc*112,4,106,24,mãKýTự);bảngTraTên(160+chỉSốThứBậc*112,8,"Terminal",0xffffff,mãKýTự);char dữLiệuChuỗi[2]={(char)('1'+chỉSốThứBậc),0};bảngTraTên(232+chỉSốThứBậc*112,8,dữLiệuChuỗi,0xffffff,mãKýTự);}
    if(!sốLượngMục)bảngTraTên(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int chỉSốThứBậc=0;chỉSốThứBậc<sốLượngMục;chỉSốThứBậc++)khungViệcThựcThi(giáTrịThứTự[chỉSốThứBậc]);mànHìnhVẽLại(tiêuĐiểm);mụcThiếtBịCuối=&danhSáchCácCửaSổ[đầuRa];
}
static void miềnTô(int vịTríNgang,int vịTríDọc,int khoảngTrảiRộng,int độDài){
    if(!khungNhìnMànLàmViệc||!cácCậnBảnVẽBoMạch(&vịTríNgang,&vịTríDọc,&khoảngTrảiRộng,&độDài))return;
    for(int dòng=vịTríDọc;dòng<vịTríDọc+độDài;dòng+=32){
        int caoDải=vịTríDọc+độDài-dòng;if(caoDải>32)caoDải=32;
        if(bảnVẽBắtChạyBoMạch(vịTríNgang,dòng,khoảngTrảiRộng,caoDải)){vẽCảnh();bảnVẽHoànThànhBoMạch();}
    }
}
static void vẽLại(void){miềnTô(0,0,rộngMànHìnhBoMạch(),caoMànHìnhBoMạch());}
/* 서로 겹치지 않는 새 cửaSổ 영역과 phầnMụcTrướcĐó 자리의 네 띠를 복구한다. */
static void cácCậnCửaSổTô(int vịTríNgang,int vịTríDọc,int khoảngTrảiRộng,int độDài,ThiếtBịCuối *cửaSổ){
    int bênTrái=vịTríNgang>(int)cửaSổ->tọaĐộX?vịTríNgang:(int)cửaSổ->tọaĐộX;
    int bênThượng=vịTríDọc>(int)cửaSổ->tọaĐộY?vịTríDọc:(int)cửaSổ->tọaĐộY;
    int phải=vịTríNgang+khoảngTrảiRộng<(int)(cửaSổ->tọaĐộX+cửaSổ->giáTrịRộng)?vịTríNgang+khoảngTrảiRộng:(int)(cửaSổ->tọaĐộX+cửaSổ->giáTrịRộng);
    int bênHạ=vịTríDọc+độDài<(int)(cửaSổ->tọaĐộY+cửaSổ->giáTrịCao)?vịTríDọc+độDài:(int)(cửaSổ->tọaĐộY+cửaSổ->giáTrịCao);
    miềnTô(cửaSổ->tọaĐộX,cửaSổ->tọaĐộY,cửaSổ->giáTrịRộng,cửaSổ->giáTrịCao);
    if(bênTrái>=phải||bênThượng>=bênHạ){miềnTô(vịTríNgang,vịTríDọc,khoảngTrảiRộng,độDài);return;}
    miềnTô(vịTríNgang,vịTríDọc,khoảngTrảiRộng,bênThượng-vịTríDọc);
    miềnTô(vịTríNgang,bênHạ,khoảngTrảiRộng,vịTríDọc+độDài-bênHạ);
    miềnTô(vịTríNgang,bênThượng,bênTrái-vịTríNgang,bênHạ-bênThượng);
    miềnTô(phải,bênThượng,vịTríNgang+khoảngTrảiRộng-phải,bênHạ-bênThượng);
}
static void tiêuĐiểmTínHiệu(void){làĐangChờ=(làĐangChờ&~15u)|(unsigned)(tiêuĐiểm+1)|0x10000;}
void chếĐộĐầuVàoThiếtBịCuối(unsigned tiếngHàn){
    đầuVàoHangul=tiếngHàn!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(tiêuĐiểm>=0){
        ThiếtBịCuối *mụcCửaSổ=&danhSáchCácCửaSổ[tiêuĐiểm];
        bảngTraTên(mụcCửaSổ->tọaĐộX+240,mụcCửaSổ->tọaĐộY+7,mụcCửaSổ->giáTrịRộng>=500?(đầuVàoHangul?"[VI] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(đầuVàoHangul?"[VI]":"[EN]"),0xffffff,0x905020);
    }
}
static void phíaTrướcĐếnĐưa(int giáTrịĐịnhDanh){if(giáTrịĐịnhDanh<0||giáTrịĐịnhDanh>=4||!danhSáchCácCửaSổ[giáTrịĐịnhDanh].làĐangSống)return;int vịTríHiệnTại=0;while(vịTríHiệnTại<sốLượngMục&&giáTrịThứTự[vịTríHiệnTại]!=giáTrịĐịnhDanh)vịTríHiệnTại++;for(;vịTríHiệnTại+1<sốLượngMục;vịTríHiệnTại++)giáTrịThứTự[vịTríHiệnTại]=giáTrịThứTự[vịTríHiệnTại+1];giáTrịThứTự[sốLượngMục-1]=giáTrịĐịnhDanh;tiêuĐiểm=giáTrịĐịnhDanh;tiêuĐiểmTínHiệu();vẽLại();}
static void trống(unsigned vịTríHàng){for(unsigned mãKýTự=0;mãKýTự<cácCộtTốiĐa;mãKýTự++){mụcThiếtBịCuối->cácÔKýTự[vịTríHàng%sốLượngDòngLịchSử][mãKýTự]=0;mụcThiếtBịCuối->danhSáchCácHình[vịTríHàng%sốLượngDòngLịchSử][mãKýTự]=mụcThiếtBịCuối->màuTiềnCảnh|(mụcThiếtBịCuối->màuNền<<4);}}
static void xóaSạchCácNộiDung(void){mụcThiếtBịCuối->vịTríHàng=mụcThiếtBịCuối->vịTríCột=mụcThiếtBịCuối->mụcĐỉnh=mụcThiếtBịCuối->cuộn=0;for(unsigned giáTrịĐãTrảVề=0;giáTrịĐãTrảVề<sốLượngDòngLịchSử;giáTrịĐãTrảVề++)trống(giáTrịĐãTrảVề);if(làĐãHiện())giáTrịNộiDung();}
static int tạoMục(void){
    if(!bộĐệmKhungBoMạch())return -19;int giáTrịĐịnhDanh=0;while(giáTrịĐịnhDanh<4&&danhSáchCácCửaSổ[giáTrịĐịnhDanh].làĐangSống)giáTrịĐịnhDanh++;if(giáTrịĐịnhDanh==4)return -28;
    khungNhìnMànLàmViệc=1;mụcThiếtBịCuối=&danhSáchCácCửaSổ[giáTrịĐịnhDanh];memset(mụcThiếtBịCuối,0,sizeof(*mụcThiếtBịCuối));mụcThiếtBịCuối->làĐangSống=1;mụcThiếtBịCuối->giáTrịRộng=568;mụcThiếtBịCuối->giáTrịCao=360;mụcThiếtBịCuối->cácCột=68;mụcThiếtBịCuối->sốLượngHàng=19;mụcThiếtBịCuối->tọaĐộX=12+giáTrịĐịnhDanh*16;mụcThiếtBịCuối->tọaĐộY=48+giáTrịĐịnhDanh*18;mụcThiếtBịCuối->màuTiềnCảnh=7;mụcThiếtBịCuối->hiệnĐượcDấuNháy=1;
    for(unsigned giáTrịĐãTrảVề=0;giáTrịĐãTrảVề<sốLượngDòngLịchSử;giáTrịĐãTrảVề++)trống(giáTrịĐãTrảVề);giáTrịThứTự[sốLượngMục++]=giáTrịĐịnhDanh;tiêuĐiểm=giáTrịĐịnhDanh;làĐangChờ|=1u<<(4+giáTrịĐịnhDanh);tiêuĐiểmTínHiệu();vẽLại();return giáTrịĐịnhDanh+1;
}
static void đóngCửaSổ(int giáTrịĐịnhDanh){
    if(giáTrịĐịnhDanh<0||giáTrịĐịnhDanh>=4||!danhSáchCácCửaSổ[giáTrịĐịnhDanh].làĐangSống)return;danhSáchCácCửaSổ[giáTrịĐịnhDanh].làĐangSống=0;làĐangChờ|=1u<<(8+giáTrịĐịnhDanh);
    int vịTríHiệnTại=0;while(vịTríHiệnTại<sốLượngMục&&giáTrịThứTự[vịTríHiệnTại]!=giáTrịĐịnhDanh)vịTríHiệnTại++;for(;vịTríHiệnTại+1<sốLượngMục;vịTríHiệnTại++)giáTrịThứTự[vịTríHiệnTại]=giáTrịThứTự[vịTríHiệnTại+1];sốLượngMục--;
    if(tiêuĐiểm==giáTrịĐịnhDanh)tiêuĐiểm=sốLượngMục?giáTrịThứTự[sốLượngMục-1]:-1;tiêuĐiểmTínHiệu();vẽLại();
}
static void xuốngDòng(void){mụcThiếtBịCuối->vịTríCột=0;mụcThiếtBịCuối->vịTríHàng++;if(mụcThiếtBịCuối->vịTríHàng>=mụcThiếtBịCuối->mụcĐỉnh+mụcThiếtBịCuối->sốLượngHàng){mụcThiếtBịCuối->mụcĐỉnh++;trống(mụcThiếtBịCuối->vịTríHàng);if(làĐãHiện())giáTrịNộiDung();}}
static void điểmMã(unsigned mãKýTự){
    if(mãKýTự==13){mụcThiếtBịCuối->vịTríCột=0;return;}if(mãKýTự==10){xuốngDòng();return;}if(mãKýTự==8){if(mụcThiếtBịCuối->vịTríCột)mụcThiếtBịCuối->vịTríCột--;return;}
    if(mãKýTự==9){unsigned sốLượngPhầnMục=8-mụcThiếtBịCuối->vịTríCột%8;while(sốLượngPhầnMục--)điểmMã(' ');return;}if(mãKýTự<32||mãKýTự==127)return;
    unsigned giáTrịRộngĐãYêuCầu=kýTựRộngKiểu(mãKýTự);if(mụcThiếtBịCuối->vịTríCột+giáTrịRộngĐãYêuCầu>mụcThiếtBịCuối->cácCột)xuốngDòng();
    if(mụcThiếtBịCuối->cácÔKýTự[mụcThiếtBịCuối->vịTríHàng%sốLượngDòngLịchSử][mụcThiếtBịCuối->vịTríCột]==0xffffffffu&&mụcThiếtBịCuối->vịTríCột){mụcThiếtBịCuối->cácÔKýTự[mụcThiếtBịCuối->vịTríHàng%sốLượngDòngLịchSử][mụcThiếtBịCuối->vịTríCột-1]=' ';mànHìnhTô(mụcThiếtBịCuối->vịTríHàng,mụcThiếtBịCuối->vịTríCột-1);}
    if(kýTựRộngKiểu(mụcThiếtBịCuối->cácÔKýTự[mụcThiếtBịCuối->vịTríHàng%sốLượngDòngLịchSử][mụcThiếtBịCuối->vịTríCột])==2&&mụcThiếtBịCuối->vịTríCột+1<mụcThiếtBịCuối->cácCột){mụcThiếtBịCuối->cácÔKýTự[mụcThiếtBịCuối->vịTríHàng%sốLượngDòngLịchSử][mụcThiếtBịCuối->vịTríCột+1]=' ';mànHìnhTô(mụcThiếtBịCuối->vịTríHàng,mụcThiếtBịCuối->vịTríCột+1);}
    mụcThiếtBịCuối->cácÔKýTự[mụcThiếtBịCuối->vịTríHàng%sốLượngDòngLịchSử][mụcThiếtBịCuối->vịTríCột]=mãKýTự;mụcThiếtBịCuối->danhSáchCácHình[mụcThiếtBịCuối->vịTríHàng%sốLượngDòngLịchSử][mụcThiếtBịCuối->vịTríCột]=mụcThiếtBịCuối->màuTiềnCảnh|(mụcThiếtBịCuối->màuNền<<4);
    if(giáTrịRộngĐãYêuCầu==2)mụcThiếtBịCuối->cácÔKýTự[mụcThiếtBịCuối->vịTríHàng%sốLượngDòngLịchSử][mụcThiếtBịCuối->vịTríCột+1]=0xffffffffu;
    mànHìnhTô(mụcThiếtBịCuối->vịTríHàng,mụcThiếtBịCuối->vịTríCột);mụcThiếtBịCuối->vịTríCột+=giáTrịRộngĐãYêuCầu;
}
static void dãyĐiềuKhiểnThẻXửLý(unsigned mãKýTự){
    unsigned sốLượngPhầnMục=mụcThiếtBịCuối->giáTrịThamSố[0]?mụcThiếtBịCuối->giáTrịThamSố[0]:1;
    if(mãKýTự=='m')for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<=mụcThiếtBịCuối->chỉSốThamSố;chỉSốThứBậc++){unsigned vịTríDữLiệu=mụcThiếtBịCuối->giáTrịThamSố[chỉSốThứBậc];if(!vịTríDữLiệu){mụcThiếtBịCuối->màuTiềnCảnh=7;mụcThiếtBịCuối->màuNền=0;}if(vịTríDữLiệu==1&&mụcThiếtBịCuối->màuTiềnCảnh<8)mụcThiếtBịCuối->màuTiềnCảnh+=8;if(vịTríDữLiệu==7){unsigned giữLạiGiáTrị=mụcThiếtBịCuối->màuTiềnCảnh;mụcThiếtBịCuối->màuTiềnCảnh=mụcThiếtBịCuối->màuNền;mụcThiếtBịCuối->màuNền=giữLạiGiáTrị;}if(vịTríDữLiệu>=30&&vịTríDữLiệu<=37)mụcThiếtBịCuối->màuTiềnCảnh=vịTríDữLiệu-30;if(vịTríDữLiệu>=90&&vịTríDữLiệu<=97)mụcThiếtBịCuối->màuTiềnCảnh=vịTríDữLiệu-90+8;if(vịTríDữLiệu>=40&&vịTríDữLiệu<=47)mụcThiếtBịCuối->màuNền=vịTríDữLiệu-40;if(vịTríDữLiệu>=100&&vịTríDữLiệu<=107)mụcThiếtBịCuối->màuNền=vịTríDữLiệu-100+8;if(vịTríDữLiệu==39)mụcThiếtBịCuối->màuTiềnCảnh=7;if(vịTríDữLiệu==49)mụcThiếtBịCuối->màuNền=0;}
    if(mãKýTự=='J'&&(mụcThiếtBịCuối->giáTrịThamSố[0]==2||mụcThiếtBịCuối->giáTrịThamSố[0]==3))xóaSạchCácNộiDung();
    if(mãKýTự=='K'){unsigned vịTríRờiĐi=mụcThiếtBịCuối->giáTrịThamSố[0]==2?0:mụcThiếtBịCuối->vịTríCột,vịTríĐến=mụcThiếtBịCuối->giáTrịThamSố[0]==1?mụcThiếtBịCuối->vịTríCột+1:mụcThiếtBịCuối->cácCột;if(mụcThiếtBịCuối->giáTrịThamSố[0]==1)vịTríRờiĐi=0;for(unsigned chỉSốThứBậc=vịTríRờiĐi;chỉSốThứBậc<vịTríĐến&&chỉSốThứBậc<mụcThiếtBịCuối->cácCột;chỉSốThứBậc++){
        unsigned giáTrịHàng=mụcThiếtBịCuối->vịTríHàng%sốLượngDòngLịchSử,giáTrịKýTự=mụcThiếtBịCuối->cácÔKýTự[giáTrịHàng][chỉSốThứBậc],giáTrịHình=mụcThiếtBịCuối->màuTiềnCảnh|(mụcThiếtBịCuối->màuNền<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 giáTrịPhôngChữ 화소를 되풀이해 칠하지 않는다. */
        int làĐãChỉnhSửa=(giáTrịKýTự!=0&&giáTrịKýTự!=' ')||mụcThiếtBịCuối->danhSáchCácHình[giáTrịHàng][chỉSốThứBậc]!=giáTrịHình;
        mụcThiếtBịCuối->cácÔKýTự[giáTrịHàng][chỉSốThứBậc]=' ';mụcThiếtBịCuối->danhSáchCácHình[giáTrịHàng][chỉSốThứBậc]=giáTrịHình;
        if(làĐãChỉnhSửa)mànHìnhTô(mụcThiếtBịCuối->vịTríHàng,chỉSốThứBậc);
    }}
    if(mãKýTự=='D')mụcThiếtBịCuối->vịTríCột=sốLượngPhầnMục>mụcThiếtBịCuối->vịTríCột?0:mụcThiếtBịCuối->vịTríCột-sốLượngPhầnMục;if(mãKýTự=='C')mụcThiếtBịCuối->vịTríCột=mụcThiếtBịCuối->vịTríCột+sốLượngPhầnMục>=mụcThiếtBịCuối->cácCột?mụcThiếtBịCuối->cácCột-1:mụcThiếtBịCuối->vịTríCột+sốLượngPhầnMục;
    if(mãKýTự=='G')mụcThiếtBịCuối->vịTríCột=sốLượngPhầnMục>mụcThiếtBịCuối->cácCột?mụcThiếtBịCuối->cácCột-1:sốLượngPhầnMục-1;if(mãKýTự=='A')mụcThiếtBịCuối->vịTríHàng=sốLượngPhầnMục>mụcThiếtBịCuối->vịTríHàng-mụcThiếtBịCuối->mụcĐỉnh?mụcThiếtBịCuối->mụcĐỉnh:mụcThiếtBịCuối->vịTríHàng-sốLượngPhầnMục;
    if(mãKýTự=='B')mụcThiếtBịCuối->vịTríHàng=mụcThiếtBịCuối->vịTríHàng+sốLượngPhầnMục>=mụcThiếtBịCuối->mụcĐỉnh+mụcThiếtBịCuối->sốLượngHàng?mụcThiếtBịCuối->mụcĐỉnh+mụcThiếtBịCuối->sốLượngHàng-1:mụcThiếtBịCuối->vịTríHàng+sốLượngPhầnMục;
    if(mãKýTự=='H'||mãKýTự=='f'){mụcThiếtBịCuối->vịTríHàng=mụcThiếtBịCuối->mụcĐỉnh+(sốLượngPhầnMục>mụcThiếtBịCuối->sốLượngHàng?mụcThiếtBịCuối->sốLượngHàng:sốLượngPhầnMục)-1;unsigned tọaĐộX=mụcThiếtBịCuối->giáTrịThamSố[1]?mụcThiếtBịCuối->giáTrịThamSố[1]:1;mụcThiếtBịCuối->vịTríCột=(tọaĐộX>mụcThiếtBịCuối->cácCột?mụcThiếtBịCuối->cácCột:tọaĐộX)-1;}
    if(mãKýTự=='s'){mụcThiếtBịCuối->hàngĐãLưu=mụcThiếtBịCuối->vịTríHàng;mụcThiếtBịCuối->cộtGọnĐãLưu=mụcThiếtBịCuối->vịTríCột;}if(mãKýTự=='u'){mụcThiếtBịCuối->vịTríHàng=mụcThiếtBịCuối->hàngĐãLưu;mụcThiếtBịCuối->vịTríCột=mụcThiếtBịCuối->cộtGọnĐãLưu<mụcThiếtBịCuối->cácCột?mụcThiếtBịCuối->cộtGọnĐãLưu:mụcThiếtBịCuối->cácCột-1;}
    if((mãKýTự=='h'||mãKýTự=='l')&&mụcThiếtBịCuối->giáTrịThamSố[0]==25)mụcThiếtBịCuối->hiệnĐượcDấuNháy=mãKýTự=='h';
}
void byteThiếtBịCuối(unsigned giáTrịThứHai){
    mụcThiếtBịCuối=&danhSáchCácCửaSổ[đầuRa];if(!mụcThiếtBịCuối->làĐangSống)return;giáTrịDấuNháy(0);if(mụcThiếtBịCuối->cuộn){mụcThiếtBịCuối->cuộn=0;if(làĐãHiện())giáTrịNộiDung();}
    if(mụcThiếtBịCuối->thoát==1){mụcThiếtBịCuối->thoát=giáTrịThứHai=='['?2:0;mụcThiếtBịCuối->chỉSốThamSố=0;for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<4;chỉSốThứBậc++)mụcThiếtBịCuối->giáTrịThamSố[chỉSốThứBậc]=0;}
    else if(mụcThiếtBịCuối->thoát==2){if(giáTrịThứHai=='?'){}else if(giáTrịThứHai>='0'&&giáTrịThứHai<='9'){if(mụcThiếtBịCuối->giáTrịThamSố[mụcThiếtBịCuối->chỉSốThamSố]<10000)mụcThiếtBịCuối->giáTrịThamSố[mụcThiếtBịCuối->chỉSốThamSố]=mụcThiếtBịCuối->giáTrịThamSố[mụcThiếtBịCuối->chỉSốThamSố]*10+giáTrịThứHai-'0';}else if(giáTrịThứHai==';'&&mụcThiếtBịCuối->chỉSốThamSố<3)mụcThiếtBịCuối->chỉSốThamSố++;else{dãyĐiềuKhiểnThẻXửLý(giáTrịThứHai);mụcThiếtBịCuối->thoát=0;}}
    else if(giáTrịThứHai==27){mụcThiếtBịCuối->giáTrịDàiKhôngDấu=0;mụcThiếtBịCuối->thoát=1;}else{
        if(mụcThiếtBịCuối->giáTrịDàiKhôngDấu&&(giáTrịThứHai&0xc0)!=0x80){mụcThiếtBịCuối->giáTrịDàiKhôngDấu=0;điểmMã(0xfffd);}
        if(mụcThiếtBịCuối->giáTrịDàiKhôngDấu){mụcThiếtBịCuối->kếtQuảKhôngDấu=mụcThiếtBịCuối->kếtQuảKhôngDấu*64+(giáTrịThứHai&63);if(--mụcThiếtBịCuối->giáTrịDàiKhôngDấu==0)điểmMã(mụcThiếtBịCuối->kếtQuảKhôngDấu<mụcThiếtBịCuối->giáTrịBé||mụcThiếtBịCuối->kếtQuảKhôngDấu>0x10ffff||(mụcThiếtBịCuối->kếtQuảKhôngDấu>=0xd800&&mụcThiếtBịCuối->kếtQuảKhôngDấu<=0xdfff)?0xfffd:mụcThiếtBịCuối->kếtQuảKhôngDấu);}
        else if(giáTrịThứHai<128)điểmMã(giáTrịThứHai);else if(giáTrịThứHai>=0xc2&&giáTrịThứHai<=0xf4){mụcThiếtBịCuối->giáTrịDàiKhôngDấu=giáTrịThứHai<0xe0?1:giáTrịThứHai<0xf0?2:3;mụcThiếtBịCuối->kếtQuảKhôngDấu=giáTrịThứHai&((1u<<(6-mụcThiếtBịCuối->giáTrịDàiKhôngDấu))-1);mụcThiếtBịCuối->giáTrịBé=mụcThiếtBịCuối->giáTrịDàiKhôngDấu==1?128:mụcThiếtBịCuối->giáTrịDàiKhôngDấu==2?2048:65536;}else điểmMã(0xfffd);
    }giáTrịDấuNháy(1);
}
int đangChờThiếtBịCuối(void){return làĐangChờ!=0;}
/* giáTrịGóc sốHiệu: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int kéoĐổiCỡ=-1,gócĐãGiữ,xĐãGiữ,yĐãGiữ,vịTríNgangBanĐầu,vịTríDọcBanĐầu,giáTrịRộngBanĐầu,giáTrịCaoBanĐầu;
static int cửaSổĐượcTrỏ(int vịTríNgang,int vịTríDọc) {
    for(int giáTrịDãy=sốLượngMục-1;giáTrịDãy>=0;giáTrịDãy--){
        int giáTrịĐịnhDanh=giáTrịThứTự[giáTrịDãy];ThiếtBịCuối *cửaSổ=&danhSáchCácCửaSổ[giáTrịĐịnhDanh];
        if(vịTríNgang>=(int)cửaSổ->tọaĐộX&&vịTríDọc>=(int)cửaSổ->tọaĐộY&&
           vịTríNgang<(int)(cửaSổ->tọaĐộX+cửaSổ->giáTrịRộng)&&vịTríDọc<(int)(cửaSổ->tọaĐộY+cửaSổ->giáTrịCao))return giáTrịĐịnhDanh;
    }return -1;
}
static int tìmGóc(int giáTrịĐịnhDanh,int vịTríNgang,int vịTríDọc) {
    if(giáTrịĐịnhDanh<0)return 0;ThiếtBịCuối *cửaSổ=&danhSáchCácCửaSổ[giáTrịĐịnhDanh];
    int bênTrái=vịTríNgang<(int)cửaSổ->tọaĐộX+8,phải=vịTríNgang>=(int)(cửaSổ->tọaĐộX+cửaSổ->giáTrịRộng)-8;
    int bênThượng=vịTríDọc<(int)cửaSổ->tọaĐộY+8,bênHạ=vịTríDọc>=(int)(cửaSổ->tọaĐộY+cửaSổ->giáTrịCao)-8;
    return (bênTrái||phải)&&(bênThượng||bênHạ)?1+phải+bênHạ*2:0;
}
static int giáTrịBộPhânCách(int giáTrị,int giáTrịTốiThiểu,int giáTrịTốiĐa){return giáTrị<giáTrịTốiThiểu?giáTrịTốiThiểu:giáTrị>giáTrịTốiĐa?giáTrịTốiĐa:giáTrị;}
static void đổiCỡDiChuyển(int vịTríNgang,int vịTríDọc) {
    ThiếtBịCuối *cửaSổ=&danhSáchCácCửaSổ[kéoĐổiCỡ];int bênTrái=vịTríNgangBanĐầu,bênThượng=vịTríDọcBanĐầu,phải=vịTríNgangBanĐầu+giáTrịRộngBanĐầu,bênHạ=vịTríDọcBanĐầu+giáTrịCaoBanĐầu;
    if(gócĐãGiữ==1||gócĐãGiữ==3)bênTrái=giáTrịBộPhânCách(vịTríNgangBanĐầu+vịTríNgang-xĐãGiữ,0,phải-360);
    else phải=giáTrịBộPhânCách(vịTríNgangBanĐầu+giáTrịRộngBanĐầu+vịTríNgang-xĐãGiữ,bênTrái+360,rộngMànHìnhBoMạch());
    if(gócĐãGiữ<=2)bênThượng=giáTrịBộPhânCách(vịTríDọcBanĐầu+vịTríDọc-yĐãGiữ,34,bênHạ-216);
    else bênHạ=giáTrịBộPhânCách(vịTríDọcBanĐầu+giáTrịCaoBanĐầu+vịTríDọc-yĐãGiữ,bênThượng+216,caoMànHìnhBoMạch());
    unsigned cácCột=(phải-bênTrái-24)/8,sốLượngHàng=(bênHạ-bênThượng-56)/16;
    if(cửaSổ->cácCột!=cácCột||cửaSổ->sốLượngHàng!=sốLượngHàng){
        cửaSổ->đãĐổiCỡĐãLà=1;cửaSổ->cácCột=cácCột;cửaSổ->sốLượngHàng=sốLượngHàng;
        if(cửaSổ->vịTríCột>=cácCột)cửaSổ->vịTríCột=cácCột-1;
        if(cửaSổ->vịTríHàng>=cửaSổ->mụcĐỉnh+sốLượngHàng)cửaSổ->mụcĐỉnh=cửaSổ->vịTríHàng-sốLượngHàng+1;
        unsigned giớiHạnSứcChứa=cửaSổ->mụcĐỉnh;if(giớiHạnSứcChứa>sốLượngDòngLịchSử-sốLượngHàng)giớiHạnSứcChứa=sốLượngDòngLịchSử-sốLượngHàng;
        if(cửaSổ->cuộn>giớiHạnSứcChứa)cửaSổ->cuộn=giớiHạnSứcChứa;
    }
    int vịTríNgangCũ=cửaSổ->tọaĐộX,vịTríDọcCũ=cửaSổ->tọaĐộY,rộngCũ=cửaSổ->giáTrịRộng,độDàiCũ=cửaSổ->giáTrịCao;
    if(vịTríNgangCũ==bênTrái&&vịTríDọcCũ==bênThượng&&rộngCũ==phải-bênTrái&&độDàiCũ==bênHạ-bênThượng)return;
    cửaSổ->tọaĐộX=bênTrái;cửaSổ->tọaĐộY=bênThượng;cửaSổ->giáTrịRộng=phải-bênTrái;cửaSổ->giáTrịCao=bênHạ-bênThượng;
    cácCậnCửaSổTô(vịTríNgangCũ,vịTríDọcCũ,rộngCũ,độDàiCũ,cửaSổ);
}
void conTrỏThiếtBịCuối(unsigned phầnMụcKếTiếp,int tọaĐộX,int tọaĐộY){
    unsigned làĐãNhấn=phầnMụcKếTiếp&~cácNút;cácNút=phầnMụcKếTiếp;
    if(!khungNhìnMànLàmViệc){giáTrịKéo=-1;kéoĐổiCỡ=-1;conTrỏBoMạch(tọaĐộX,tọaĐộY,1);return;}
    if(!(phầnMụcKếTiếp&1)){giáTrịKéo=-1;kéoĐổiCỡ=-1;}
    if(kéoĐổiCỡ>=0&&!danhSáchCácCửaSổ[kéoĐổiCỡ].làĐangSống)kéoĐổiCỡ=-1;
    if(giáTrịKéo>=0&&!danhSáchCácCửaSổ[giáTrịKéo].làĐangSống)giáTrịKéo=-1;
    if(kéoĐổiCỡ>=0){
        đổiCỡDiChuyển(tọaĐộX,tọaĐộY);conTrỏBoMạch(tọaĐộX,tọaĐộY,gócĐãGiữ==1||gócĐãGiữ==4?2:3);return;
    }
    conTrỏBoMạch(tọaĐộX,tọaĐộY,1);
    if(giáTrịKéo>=0){
        ThiếtBịCuối *cửaSổ=&danhSáchCácCửaSổ[giáTrịKéo];
        int vịTríNgangCũ=cửaSổ->tọaĐộX,vịTríDọcCũ=cửaSổ->tọaĐộY;
        cửaSổ->tọaĐộX=giáTrịBộPhânCách(tọaĐộX-xKéo,0,rộngMànHìnhBoMạch()-cửaSổ->giáTrịRộng);
        cửaSổ->tọaĐộY=giáTrịBộPhânCách(tọaĐộY-yKéo,34,caoMànHìnhBoMạch()-cửaSổ->giáTrịCao);
        if(vịTríNgangCũ!=(int)cửaSổ->tọaĐộX||vịTríDọcCũ!=(int)cửaSổ->tọaĐộY)cácCậnCửaSổTô(vịTríNgangCũ,vịTríDọcCũ,cửaSổ->giáTrịRộng,cửaSổ->giáTrịCao,cửaSổ);
        return;
    }
    extern int lớpPhủMànHình(int,int,int);
    if(lớpPhủMànHình(tiêuĐiểm,tọaĐộX,tọaĐộY)){conTrỏMànHình(tiêuĐiểm,làĐãNhấn,tọaĐộX,tọaĐộY);return;}
    int giáTrịĐịnhDanh=cửaSổĐượcTrỏ(tọaĐộX,tọaĐộY),giáTrịGóc=tìmGóc(giáTrịĐịnhDanh,tọaĐộX,tọaĐộY);
    if(giáTrịGóc)conTrỏBoMạch(tọaĐộX,tọaĐộY,giáTrịGóc==1||giáTrịGóc==4?2:3);
    if(làĐãNhấn&1){
        if(giáTrịGóc){
            ThiếtBịCuối *cửaSổ=&danhSáchCácCửaSổ[giáTrịĐịnhDanh];kéoĐổiCỡ=giáTrịĐịnhDanh;gócĐãGiữ=giáTrịGóc;xĐãGiữ=tọaĐộX;yĐãGiữ=tọaĐộY;
            vịTríNgangBanĐầu=cửaSổ->tọaĐộX;vịTríDọcBanĐầu=cửaSổ->tọaĐộY;giáTrịRộngBanĐầu=cửaSổ->giáTrịRộng;giáTrịCaoBanĐầu=cửaSổ->giáTrịCao;
            if(giáTrịĐịnhDanh!=tiêuĐiểm)phíaTrướcĐếnĐưa(giáTrịĐịnhDanh);return;
        }
        if(tọaĐộY<32&&tọaĐộX>=6&&tọaĐộX<142){tạoMục();return;}
        if(tọaĐộY<32&&tọaĐộX>=154&&tọaĐộX<602){phíaTrướcĐếnĐưa((tọaĐộX-154)/112);return;}
        if(giáTrịĐịnhDanh>=0){
            ThiếtBịCuối *cửaSổ=&danhSáchCácCửaSổ[giáTrịĐịnhDanh];
            if(tọaĐộY<(int)cửaSổ->tọaĐộY+30&&tọaĐộX>=(int)(cửaSổ->tọaĐộX+cửaSổ->giáTrịRộng)-32){đóngCửaSổ(giáTrịĐịnhDanh);return;}
            if(giáTrịĐịnhDanh!=tiêuĐiểm)phíaTrướcĐếnĐưa(giáTrịĐịnhDanh);
            if(tọaĐộY<(int)cửaSổ->tọaĐộY+30){giáTrịKéo=giáTrịĐịnhDanh;xKéo=tọaĐộX-cửaSổ->tọaĐộX;yKéo=tọaĐộY-cửaSổ->tọaĐộY;}return;
        }
    }
    if(tiêuĐiểm>=0&&(làĐãNhấn&(8|16))){mụcThiếtBịCuối=&danhSáchCácCửaSổ[tiêuĐiểm];if(làĐãNhấn&8){unsigned giớiHạnSứcChứa=mụcThiếtBịCuối->mụcĐỉnh;if(giớiHạnSứcChứa>sốLượngDòngLịchSử-mụcThiếtBịCuối->sốLượngHàng)giớiHạnSứcChứa=sốLượngDòngLịchSử-mụcThiếtBịCuối->sốLượngHàng;mụcThiếtBịCuối->cuộn=mụcThiếtBịCuối->cuộn+9>giớiHạnSứcChứa?giớiHạnSứcChứa:mụcThiếtBịCuối->cuộn+9;}else mụcThiếtBịCuối->cuộn=mụcThiếtBịCuối->cuộn<9?0:mụcThiếtBịCuối->cuộn-9;vẽLại();}
}
void phímTắtThiếtBịCuối(unsigned giáTrịĐãNhấn){if(giáTrịĐãNhấn==1)tạoMục();if(giáTrịĐãNhấn==2&&sốLượngMục)phíaTrướcĐếnĐưa(giáTrịThứTự[0]);if(giáTrịĐãNhấn==3)đóngCửaSổ(tiêuĐiểm);}
từMáy thiếtBịCuốiBoMạch(từMáy hànhĐộng){
    if(hànhĐộng==300){if(!danhSáchCácCửaSổ[đầuRa].làĐangSống)return tạoMục();khungNhìnMànLàmViệc=1;vẽLại();return 0;}
    if(hànhĐộng==0){đóngCửaSổ(tiêuĐiểm);return 0;}if(hànhĐộng==1)return (uint32_t)tạoMục();if(hànhĐộng==2)return tiêuĐiểm>=0;
    if(hànhĐộng==9){khungNhìnMànLàmViệc=0;return 0;}if(hànhĐộng==7)return sốLượngMục;if(hànhĐộng==10)return tiêuĐiểm+1;if(hànhĐộng==11)return đầuRa;
    if(hànhĐộng==13){ThiếtBịCuối *cửaSổ=&danhSáchCácCửaSổ[đầuRa];return cửaSổ->làĐangSống?(cửaSổ->sốLượngHàng<<16)|cửaSổ->cácCột:(19<<16)|68;}
    if(hànhĐộng==14){unsigned giáTrị=danhSáchCácCửaSổ[đầuRa].đãĐổiCỡĐãLà;danhSáchCácCửaSổ[đầuRa].đãĐổiCỡĐãLà=0;return giáTrị;}
    if(hànhĐộng==12){unsigned giáTrị=làĐangChờ;làĐangChờ=0;return giáTrị;}
    if(hànhĐộng>=20&&hànhĐộng<24)return danhSáchCácCửaSổ[hànhĐộng-20].làĐangSống;
    if(hànhĐộng>=100&&hànhĐộng<104){đầuRa=hànhĐộng-100;mụcThiếtBịCuối=&danhSáchCácCửaSổ[đầuRa];return 0;}
    if(hànhĐộng>=200&&hànhĐộng<204){phíaTrướcĐếnĐưa(hànhĐộng-200);return 0;}
    if(hànhĐộng==3){vẽLại();return 0;}mụcThiếtBịCuối=&danhSáchCácCửaSổ[đầuRa];if(!mụcThiếtBịCuối->làĐangSống)return 0;
    if(hànhĐộng==4)xóaSạchCácNộiDung();if(hànhĐộng==5||hànhĐộng==6){unsigned phầnMụcTrướcĐó=cácNút;conTrỏThiếtBịCuối(hànhĐộng==5?8:16,0,0);cácNút=phầnMụcTrướcĐó;}return 1;
}
