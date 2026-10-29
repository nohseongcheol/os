#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
#include "thôngTinMànHình.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t điểmẢnhBoMạch(uintptr_t,uintptr_t,uintptr_t),thiếtBịCuốiBoMạch(uintptr_t);
extern void hìnhChữThiếtBịCuối(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int giáTrịLoạiMục,cha,tọaĐộX,tọaĐộY,giáTrịRộngĐãYêuCầu,giáTrịCaoĐãYêuCầu,làĐãHiện,bốTríThủCông,chínhSáchBốTrí;unsigned vănBản[128],độDài; } trạngTháiThànhTốGiaoDiện;
static trạngTháiThànhTốGiaoDiện cácNútCây[4][32];
static int cóTiêuĐiểm[4],danhSáchSựKiện[4][16];static unsigned mụcĐầuTiên[4],sốLượngMục[4],kếtQuảKhôngDấu[4],giáTrịDàiKhôngDấu[4];
static void sựKiện(int đốiTượngChủSởHữu,int giáTrị){if(sốLượngMục[đốiTượngChủSởHữu]<16){danhSáchSựKiện[đốiTượngChủSởHữu][(mụcĐầuTiên[đốiTượngChủSởHữu]+sốLượngMục[đốiTượngChủSởHữu])%16]=giáTrị;sốLượngMục[đốiTượngChủSởHữu]++;}}
static trạngTháiThànhTốGiaoDiện *giáTrịPhầnTử(int đốiTượngChủSởHữu,int giáTrịĐịnhDanh){return đốiTượngChủSởHữu>=0&&đốiTượngChủSởHữu<4&&giáTrịĐịnhDanh>0&&giáTrịĐịnhDanh<=32&&cácNútCây[đốiTượngChủSởHữu][giáTrịĐịnhDanh-1].giáTrịLoạiMục?&cácNútCây[đốiTượngChủSởHữu][giáTrịĐịnhDanh-1]:0;}
static void miềnDạngChữNhật(int tọaĐộX,int tọaĐộY,int giáTrịRộngĐãYêuCầu,int giáTrịCaoĐãYêuCầu,unsigned màuĐiểmẢnh){lấpHìnhChữNhậtBoMạch(tọaĐộX,tọaĐộY,giáTrịRộngĐãYêuCầu,giáTrịCaoĐãYêuCầu,màuĐiểmẢnh);}
int hiệnĐượcMànHình(int đốiTượngChủSởHữu){if(đốiTượngChủSởHữu<0||đốiTượngChủSởHữu>=4)return 0;for(int chỉSốThứBậc=0;chỉSốThứBậc<32;chỉSốThứBậc++)if(cácNútCây[đốiTượngChủSởHữu][chỉSốThứBậc].giáTrịLoạiMục==1&&cácNútCây[đốiTượngChủSởHữu][chỉSốThứBậc].làĐãHiện)return 1;return 0;}
void khởiTạoMànHình(int đốiTượngChủSởHữu){memset(cácNútCây[đốiTượngChủSởHữu],0,sizeof(cácNútCây[đốiTượngChủSởHữu]));sốLượngMục[đốiTượngChủSởHữu]=mụcĐầuTiên[đốiTượngChủSởHữu]=cóTiêuĐiểm[đốiTượngChủSởHữu]=giáTrịDàiKhôngDấu[đốiTượngChủSởHữu]=0;}
static void vịTrí(int đốiTượngChủSởHữu,trạngTháiThànhTốGiaoDiện *giáTrịRộngĐãYêuCầu,int *tọaĐộX,int *tọaĐộY){*tọaĐộX=giáTrịRộngĐãYêuCầu->tọaĐộX;*tọaĐộY=giáTrịRộngĐãYêuCầu->tọaĐộY;int vịTríDữLiệu=giáTrịRộngĐãYêuCầu->cha;for(int sốLượngPhầnMục=0;vịTríDữLiệu&&sốLượngPhầnMục<32;sốLượngPhầnMục++){trạngTháiThànhTốGiaoDiện *bênThượng=giáTrịPhầnTử(đốiTượngChủSởHữu,vịTríDữLiệu);if(!bênThượng)break;*tọaĐộX+=bênThượng->tọaĐộX;*tọaĐộY+=bênThượng->tọaĐộY+(bênThượng->giáTrịLoạiMục==1?30:0);vịTríDữLiệu=bênThượng->cha;}}
static int làĐãHiểnThị(int đốiTượngChủSởHữu,trạngTháiThànhTốGiaoDiện *giáTrịRộngĐãYêuCầu){for(int sốLượngPhầnMục=0;sốLượngPhầnMục<32;sốLượngPhầnMục++){if(!giáTrịRộngĐãYêuCầu->làĐãHiện)return 0;if(giáTrịRộngĐãYêuCầu->giáTrịLoạiMục==1)return 1;giáTrịRộngĐãYêuCầu=giáTrịPhầnTử(đốiTượngChủSởHữu,giáTrịRộngĐãYêuCầu->cha);if(!giáTrịRộngĐãYêuCầu)return 0;}return 0;}
static void vănBản(int tọaĐộX,int tọaĐộY,trạngTháiThànhTốGiaoDiện *giáTrịRộngĐãYêuCầu,int dữLiệuTốiĐa,unsigned màuĐiểmẢnh,unsigned màuNền){int vịTríHiệnTại=0;for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<giáTrịRộngĐãYêuCầu->độDài;chỉSốThứBậc++){unsigned mãHóaKýTự=giáTrịRộngĐãYêuCầu->vănBản[chỉSốThứBậc],giáTrịRộng=mãHóaKýTự>=256?16:8;if(vịTríHiệnTại+(int)giáTrịRộng>dữLiệuTốiĐa)break;hìnhChữThiếtBịCuối(tọaĐộX+vịTríHiệnTại,tọaĐộY,mãHóaKýTự,màuĐiểmẢnh,màuNền);vịTríHiệnTại+=giáTrịRộng;}}
void mànHìnhVẽLại(int đốiTượngChủSởHữu){
    if(!hiệnĐượcMànHình(đốiTượngChủSởHữu))return;
    for(int thứTựViệcXửLý=1;thứTựViệcXửLý<=5;thứTựViệcXửLý++)for(int chỉSốThứBậc=0;chỉSốThứBậc<32;chỉSốThứBậc++){
        trạngTháiThànhTốGiaoDiện *giáTrịRộngĐãYêuCầu=&cácNútCây[đốiTượngChủSởHữu][chỉSốThứBậc];if(giáTrịRộngĐãYêuCầu->giáTrịLoạiMục!=thứTựViệcXửLý||!làĐãHiểnThị(đốiTượngChủSởHữu,giáTrịRộngĐãYêuCầu))continue;int tọaĐộX,tọaĐộY;vịTrí(đốiTượngChủSởHữu,giáTrịRộngĐãYêuCầu,&tọaĐộX,&tọaĐộY);
        if(thứTựViệcXửLý==1){miềnDạngChữNhật(tọaĐộX,tọaĐộY,giáTrịRộngĐãYêuCầu->giáTrịRộngĐãYêuCầu,giáTrịRộngĐãYêuCầu->giáTrịCaoĐãYêuCầu,0xeee9e0);miềnDạngChữNhật(tọaĐộX,tọaĐộY,giáTrịRộngĐãYêuCầu->giáTrịRộngĐãYêuCầu,30,0x905020);vănBản(tọaĐộX+10,tọaĐộY+7,giáTrịRộngĐãYêuCầu,giáTrịRộngĐãYêuCầu->giáTrịRộngĐãYêuCầu-50,0xffffff,0x905020);miềnDạngChữNhật(tọaĐộX+giáTrịRộngĐãYêuCầu->giáTrịRộngĐãYêuCầu-28,tọaĐộY+4,24,22,0x5555b8);hìnhChữThiếtBịCuối(tọaĐộX+giáTrịRộngĐãYêuCầu->giáTrịRộngĐãYêuCầu-20,tọaĐộY+7,'X',0xffffff,0x5555b8);}
        if(thứTựViệcXửLý==2)miềnDạngChữNhật(tọaĐộX,tọaĐộY,giáTrịRộngĐãYêuCầu->giáTrịRộngĐãYêuCầu,giáTrịRộngĐãYêuCầu->giáTrịCaoĐãYêuCầu,0xeee9e0);
        if(thứTựViệcXửLý>=3){unsigned màuNền=thứTựViệcXửLý==4?0xc0ab86:thứTựViệcXửLý==5?0xffffff:0xeee9e0;if(thứTựViệcXửLý!=3)miềnDạngChữNhật(tọaĐộX,tọaĐộY,giáTrịRộngĐãYêuCầu->giáTrịRộngĐãYêuCầu,giáTrịRộngĐãYêuCầu->giáTrịCaoĐãYêuCầu,màuNền);vănBản(tọaĐộX+4,tọaĐộY+4,giáTrịRộngĐãYêuCầu,giáTrịRộngĐãYêuCầu->giáTrịRộngĐãYêuCầu-8,0x201a15,màuNền);if(thứTựViệcXửLý==5&&cóTiêuĐiểm[đốiTượngChủSởHữu]==chỉSốThứBậc+1)miềnDạngChữNhật(tọaĐộX,tọaĐộY+giáTrịRộngĐãYêuCầu->giáTrịCaoĐãYêuCầu-2,giáTrịRộngĐãYêuCầu->giáTrịRộngĐãYêuCầu,2,0x905020);}
    }
}
int lớpPhủMànHình(int đốiTượngChủSởHữu,int tọaĐộX,int tọaĐộY){
    if(!hiệnĐượcMànHình(đốiTượngChủSởHữu))return 0;
    for(int chỉSốThứBậc=0;chỉSốThứBậc<32;chỉSốThứBậc++){
        trạngTháiThànhTốGiaoDiện *cửaSổ=&cácNútCây[đốiTượngChủSởHữu][chỉSốThứBậc];
        if(cửaSổ->giáTrịLoạiMục==1&&cửaSổ->làĐãHiện&&tọaĐộX>=cửaSổ->tọaĐộX&&tọaĐộY>=cửaSổ->tọaĐộY&&
           tọaĐộX<cửaSổ->tọaĐộX+cửaSổ->giáTrịRộngĐãYêuCầu&&tọaĐộY<cửaSổ->tọaĐộY+cửaSổ->giáTrịCaoĐãYêuCầu)return 1;
    }return 0;
}
int conTrỏMànHình(int đốiTượngChủSởHữu,unsigned làĐãNhấn,int tọaĐộX,int tọaĐộY){
    if(!hiệnĐượcMànHình(đốiTượngChủSởHữu))return 0;
    if(làĐãNhấn&1)for(int chỉSốThứBậc=31;chỉSốThứBậc>=0;chỉSốThứBậc--){trạngTháiThànhTốGiaoDiện *giáTrịRộngĐãYêuCầu=&cácNútCây[đốiTượngChủSởHữu][chỉSốThứBậc];if(!giáTrịRộngĐãYêuCầu->giáTrịLoạiMục||!làĐãHiểnThị(đốiTượngChủSởHữu,giáTrịRộngĐãYêuCầu))continue;int xCửaSổ,yCửaSổ;vịTrí(đốiTượngChủSởHữu,giáTrịRộngĐãYêuCầu,&xCửaSổ,&yCửaSổ);
        if(tọaĐộX<xCửaSổ||tọaĐộY<yCửaSổ||tọaĐộX>=xCửaSổ+giáTrịRộngĐãYêuCầu->giáTrịRộngĐãYêuCầu||tọaĐộY>=yCửaSổ+giáTrịRộngĐãYêuCầu->giáTrịCaoĐãYêuCầu)continue;
        if(giáTrịRộngĐãYêuCầu->giáTrịLoạiMục==1&&tọaĐộY<yCửaSổ+30&&tọaĐộX>=xCửaSổ+giáTrịRộngĐãYêuCầu->giáTrịRộngĐãYêuCầu-28){if(giáTrịRộngĐãYêuCầu->chínhSáchBốTrí!=0)giáTrịRộngĐãYêuCầu->làĐãHiện=0;sựKiện(đốiTượngChủSởHữu,0x10000+chỉSốThứBậc+1);thiếtBịCuốiBoMạch(3);return 1;}
        if(giáTrịRộngĐãYêuCầu->giáTrịLoạiMục==4){sựKiện(đốiTượngChủSởHữu,chỉSốThứBậc+1);return 1;}if(giáTrịRộngĐãYêuCầu->giáTrịLoạiMục==5){cóTiêuĐiểm[đốiTượngChủSởHữu]=chỉSốThứBậc+1;thiếtBịCuốiBoMạch(3);return 1;}
        if(giáTrịRộngĐãYêuCầu->giáTrịLoạiMục==1)return 1;
    }return 0;
}
void nhấnMànHình(int đốiTượngChủSởHữu,unsigned giáTrịThứHai){
    trạngTháiThànhTốGiaoDiện *giáTrịRộngĐãYêuCầu=giáTrịPhầnTử(đốiTượngChủSởHữu,cóTiêuĐiểm[đốiTượngChủSởHữu]);if(!giáTrịRộngĐãYêuCầu||giáTrịRộngĐãYêuCầu->giáTrịLoạiMục!=5)return;
    if(giáTrịThứHai==13||giáTrịThứHai==10){sựKiện(đốiTượngChủSởHữu,cóTiêuĐiểm[đốiTượngChủSởHữu]);return;}
    if(giáTrịThứHai==8||giáTrịThứHai==127){if(giáTrịRộngĐãYêuCầu->độDài)giáTrịRộngĐãYêuCầu->độDài--;giáTrịDàiKhôngDấu[đốiTượngChủSởHữu]=0;}
    else{
        unsigned mãHóaKýTự=giáTrịThứHai;
        if(giáTrịDàiKhôngDấu[đốiTượngChủSởHữu]){if((giáTrịThứHai&192)!=128){giáTrịDàiKhôngDấu[đốiTượngChủSởHữu]=0;return;}kếtQuảKhôngDấu[đốiTượngChủSởHữu]=(kếtQuảKhôngDấu[đốiTượngChủSởHữu]<<6)|(giáTrịThứHai&63);if(--giáTrịDàiKhôngDấu[đốiTượngChủSởHữu])return;mãHóaKýTự=kếtQuảKhôngDấu[đốiTượngChủSởHữu];}
        else if(giáTrịThứHai>=0xc2&&giáTrịThứHai<=0xf4){giáTrịDàiKhôngDấu[đốiTượngChủSởHữu]=giáTrịThứHai<0xe0?1:giáTrịThứHai<0xf0?2:3;kếtQuảKhôngDấu[đốiTượngChủSởHữu]=giáTrịThứHai&((1u<<(6-giáTrịDàiKhôngDấu[đốiTượngChủSởHữu]))-1);return;}
        else if(giáTrịThứHai<32||giáTrịThứHai>=128)return;
        if(mãHóaKýTự>0x10ffff||(mãHóaKýTự>=0xd800&&mãHóaKýTự<=0xdfff))return;if(giáTrịRộngĐãYêuCầu->độDài<127)giáTrịRộngĐãYêuCầu->vănBản[giáTrịRộngĐãYêuCầu->độDài++]=mãHóaKýTự;
    }
    thiếtBịCuốiBoMạch(3);
}
int gọiThựcHiệnMànHình(int đốiTượngChủSởHữu,unsigned hànhĐộng,int giáTrịĐịnhDanh,int giáTrịĐầuTiên,int giáTrịThứHai,int mãKýTự,int dữLiệuĐích){
    if(đốiTượngChủSởHữu<0||đốiTượngChủSởHữu>=4)return -22;trạngTháiThànhTốGiaoDiện *giáTrịRộngĐãYêuCầu=giáTrịPhầnTử(đốiTượngChủSởHữu,giáTrịĐịnhDanh);
    if(hànhĐộng==0){if(giáTrịĐịnhDanh<1||giáTrịĐịnhDanh>5)return -22;for(int chỉSốThứBậc=0;chỉSốThứBậc<32;chỉSốThứBậc++)if(cácNútCây[đốiTượngChủSởHữu][chỉSốThứBậc].giáTrịLoạiMục==0){giáTrịRộngĐãYêuCầu=&cácNútCây[đốiTượngChủSởHữu][chỉSốThứBậc];memset(giáTrịRộngĐãYêuCầu,0,sizeof(*giáTrịRộngĐãYêuCầu));giáTrịRộngĐãYêuCầu->giáTrịLoạiMục=giáTrịĐịnhDanh;giáTrịRộngĐãYêuCầu->làĐãHiện=giáTrịĐịnhDanh!=1;giáTrịRộngĐãYêuCầu->giáTrịRộngĐãYêuCầu=giáTrịĐịnhDanh==1?380:220;giáTrịRộngĐãYêuCầu->giáTrịCaoĐãYêuCầu=giáTrịĐịnhDanh==1?240:28;giáTrịRộngĐãYêuCầu->chínhSáchBốTrí=1;giáTrịRộngĐãYêuCầu->tọaĐộX=giáTrịĐịnhDanh==1?130:16;giáTrịRộngĐãYêuCầu->tọaĐộY=giáTrịĐịnhDanh==1?110:16;return chỉSốThứBậc+1;}return -28;}
    if(hànhĐộng==5){if(!sốLượngMục[đốiTượngChủSởHữu])return 0;int giáTrịĐãTrảVề=danhSáchSựKiện[đốiTượngChủSởHữu][mụcĐầuTiên[đốiTượngChủSởHữu]];mụcĐầuTiên[đốiTượngChủSởHữu]=(mụcĐầuTiên[đốiTượngChủSởHữu]+1)%16;sốLượngMục[đốiTượngChủSởHữu]--;return giáTrịĐãTrảVề;}
    if(hànhĐộng==6)return hiệnĐượcMànHình(đốiTượngChủSởHữu);
    if(!giáTrịRộngĐãYêuCầu)return -9;
    int đãHiệnĐãLà=làĐãHiểnThị(đốiTượngChủSởHữu,giáTrịRộngĐãYêuCầu);
    if(hànhĐộng==1){int rộngNền=rộngMànHìnhBoMạch(),caoNền=caoMànHìnhBoMạch();if(giáTrịĐầuTiên<0||giáTrịThứHai<0||mãKýTự<1||dữLiệuĐích<1||giáTrịĐầuTiên>rộngNền||giáTrịThứHai>caoNền||mãKýTự>rộngNền-giáTrịĐầuTiên||dữLiệuĐích>caoNền-giáTrịThứHai)return -22;giáTrịRộngĐãYêuCầu->tọaĐộX=giáTrịĐầuTiên;giáTrịRộngĐãYêuCầu->tọaĐộY=giáTrịThứHai;giáTrịRộngĐãYêuCầu->giáTrịRộngĐãYêuCầu=mãKýTự;giáTrịRộngĐãYêuCầu->giáTrịCaoĐãYêuCầu=dữLiệuĐích;giáTrịRộngĐãYêuCầu->bốTríThủCông=1;}
    else if(hànhĐộng==2){trạngTháiThànhTốGiaoDiện *phầnTửCon=giáTrịPhầnTử(đốiTượngChủSởHữu,giáTrịĐầuTiên);if(!phầnTửCon||phầnTửCon==giáTrịRộngĐãYêuCầu||phầnTửCon->giáTrịLoạiMục==1)return -22;int vịTríDữLiệu=giáTrịĐịnhDanh;for(int giáTrịĐộSâu=0;vịTríDữLiệu&&giáTrịĐộSâu<32;giáTrịĐộSâu++){if(vịTríDữLiệu==giáTrịĐầuTiên)return -22;trạngTháiThànhTốGiaoDiện *bênThượng=giáTrịPhầnTử(đốiTượngChủSởHữu,vịTríDữLiệu);vịTríDữLiệu=bênThượng?bênThượng->cha:0;}phầnTửCon->cha=giáTrịĐịnhDanh;if(!phầnTửCon->bốTríThủCông){int cácAnhEm=0;for(int chỉSốThứBậc=0;chỉSốThứBậc<32;chỉSốThứBậc++)if(&cácNútCây[đốiTượngChủSởHữu][chỉSốThứBậc]!=phầnTửCon&&cácNútCây[đốiTượngChủSởHữu][chỉSốThứBậc].cha==giáTrịĐịnhDanh)cácAnhEm++;phầnTửCon->tọaĐộY=16+cácAnhEm*36;}}
    else if(hànhĐộng==3)giáTrịRộngĐãYêuCầu->làĐãHiện=giáTrịĐầuTiên!=0;
    else if(hànhĐộng==4)giáTrịRộngĐãYêuCầu->làĐãHiện=0;
    else if(hànhĐộng==7)giáTrịRộngĐãYêuCầu->chínhSáchBốTrí=giáTrịĐầuTiên;
    else if(hànhĐộng==8)return giáTrịRộngĐãYêuCầu->độDài;
    else if(hànhĐộng==9)return giáTrịĐầuTiên>=0&&(unsigned)giáTrịĐầuTiên<giáTrịRộngĐãYêuCầu->độDài?giáTrịRộngĐãYêuCầu->vănBản[giáTrịĐầuTiên]:-22;
    else return -22;
    if(đãHiệnĐãLà||làĐãHiểnThị(đốiTượngChủSởHữu,giáTrịRộngĐãYêuCầu))thiếtBịCuốiBoMạch(3);return 0;
}
int vănBảnMànHình(int đốiTượngChủSởHữu,int giáTrịĐịnhDanh,const uint32_t *DữLiệu,unsigned sốLượngPhầnMục){trạngTháiThànhTốGiaoDiện *giáTrịRộngĐãYêuCầu=giáTrịPhầnTử(đốiTượngChủSởHữu,giáTrịĐịnhDanh);if(!giáTrịRộngĐãYêuCầu)return -9;if(sốLượngPhầnMục>127)return -22;for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhầnMục;chỉSốThứBậc++){unsigned mãHóaKýTự=DữLiệu[chỉSốThứBậc];if(mãHóaKýTự>0x10ffff||(mãHóaKýTự>=0xd800&&mãHóaKýTự<=0xdfff))return -22;}for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sốLượngPhầnMục;chỉSốThứBậc++)giáTrịRộngĐãYêuCầu->vănBản[chỉSốThứBậc]=DữLiệu[chỉSốThứBậc];giáTrịRộngĐãYêuCầu->độDài=sốLượngPhầnMục;if(làĐãHiểnThị(đốiTượngChủSởHữu,giáTrịRộngĐãYêuCầu))thiếtBịCuốiBoMạch(3);return 0;}
