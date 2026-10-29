#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Öz 네 Pencere 합성과 UTF-8 uçbirim. 바뀐 영역의 Bitenler_değer 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t makine_Word;
extern makine_Word Pano_piksel(makine_Word,makine_Word,makine_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_yazı_tipi[];
#define 최대열수 237
#define Geçmiş_hat_BAĞ_DEĞ_SAY 160
typedef struct {
    uint32_t 글자칸들[Geçmiş_hat_BAĞ_DEĞ_SAY][최대열수]; uint8_t 모양들[Geçmiş_hat_BAĞ_DEĞ_SAY][최대열수];
    unsigned 너비,높이,SÜTUNSAY,SATIR_BAĞ_DEĞ_SAY,크기바뀜;
    unsigned 살아있음,x_koordinatı,Y_koordinat,SATIR_konum,SÜTUN_konum,맨위,kaydırmak_6486617f,전경색,배경색,탈출상태,parametre_değer[4],parametre_Dizin,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,KÜÇÜK_değer,대체화면,가리개보임;
} Terminal;
static Terminal Windows_Liste[4];
static int Odak=-1,çıktı,düzen_değer[4],girdi_BAĞ_DEĞ_SAY,sürüklemek_değer=-1,sürüklemek_X,sürüklemek_Y;
static unsigned bilgi_teknolojisi_Beklemede,단추들,Masaüstü_Görünüm,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal *Terminal_girdi;
static unsigned geniş_karakter(unsigned kod_noktası){return kod_noktası>=256?2:1;}
static void 사각영역(unsigned x_koordinatı,unsigned Y_koordinat,unsigned 너비값,unsigned 높이값,unsigned 색상){
    Pano_dikdörtgen_dolgu(x_koordinatı,Y_koordinat,너비값,높이값,색상);
}
void Terminal_karakter(unsigned x_koordinatı,unsigned Y_koordinat,unsigned kod_noktası,unsigned 전경색,unsigned 배경색){
    unsigned 너비=geniş_karakter(kod_noktası)*8;if(kod_noktası==0xffffffffu)return;
    int 왼쪽=x_koordinatı,위쪽=Y_koordinat,폭=너비,süre_değer=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&süre_değer))return;
    if(kod_noktası==' '){Pano_dikdörtgen_dolgu(왼쪽,위쪽,폭,süre_değer,배경색);return;}
    unsigned ARA_Dizin=kod_noktası<65536?kod_noktası:kod_noktası>=0x1f600&&kod_noktası<0x1f650?65536+kod_noktası-0x1f600:0xfffd;
    const unsigned char *yazı_tipi_değer=Terminal_yazı_tipi+ARA_Dizin*32;
    for(int girdi_satırı=위쪽;girdi_satırı<위쪽+süre_değer;girdi_satırı++){unsigned BITS_Liste=yazı_tipi_değer[(girdi_satırı-Y_koordinat)*2]*256+yazı_tipi_değer[(girdi_satırı-Y_koordinat)*2+1];for(int yuva_girdi=왼쪽;yuva_girdi<왼쪽+폭;yuva_girdi++)Pano_piksel(yuva_girdi,girdi_satırı,(BITS_Liste&(0x8000>>(yuva_girdi-x_koordinatı)))?전경색:배경색);}
}
static void ad_tablo(unsigned x_koordinatı,unsigned Y_koordinat,const char *dize_veri,unsigned 전경색,unsigned 배경색){while(*dize_veri){unsigned kod_noktası=(unsigned char)*dize_veri++, 남은수=0;if(kod_noktası>=0xc0){남은수=kod_noktası<0xe0?1:kod_noktası<0xf0?2:3;kod_noktası&=(1u<<(6-남은수))-1;while(남은수--&&*dize_veri)kod_noktası=(kod_noktası<<6)|((unsigned char)*dize_veri++&63);}Terminal_karakter(x_koordinatı,Y_koordinat,kod_noktası,전경색,배경색);x_koordinatı+=geniş_karakter(kod_noktası)*8;}}
static unsigned 첫항목(void){return Terminal_girdi->맨위;}
static int 보이는지(void){return Terminal_girdi->살아있음&&Odak>=0&&Terminal_girdi==&Windows_Liste[Odak]&&!화면보임(Odak);}
static void 그리기(unsigned SATIR_konum,unsigned SÜTUN_konum){
    if(!보이는지()||SATIR_konum<첫항목()-Terminal_girdi->kaydırmak_6486617f||SATIR_konum>=첫항목()-Terminal_girdi->kaydırmak_6486617f+Terminal_girdi->SATIR_BAĞ_DEĞ_SAY||SÜTUN_konum>=Terminal_girdi->SÜTUNSAY)return;
    unsigned kod_noktası=Terminal_girdi->글자칸들[SATIR_konum%Geçmiş_hat_BAĞ_DEĞ_SAY][SÜTUN_konum],dize_veri=Terminal_girdi->모양들[SATIR_konum%Geçmiş_hat_BAĞ_DEĞ_SAY][SÜTUN_konum];
    if(geniş_karakter(kod_noktası)==2&&SÜTUN_konum+1>=Terminal_girdi->SÜTUNSAY)kod_noktası=' ';
    Terminal_karakter(Terminal_girdi->x_koordinatı+12+SÜTUN_konum*8,Terminal_girdi->Y_koordinat+36+(SATIR_konum-첫항목()+Terminal_girdi->kaydırmak_6486617f)*16,kod_noktası?kod_noktası:' ',색상들[dize_veri&15],색상들[dize_veri>>4]);
}
static void şapka_karakteri_değer(int şov_pencere){if(!보이는지()||Terminal_girdi->kaydırmak_6486617f||Terminal_girdi->SÜTUN_konum>=Terminal_girdi->SÜTUNSAY||Terminal_girdi->SATIR_konum<Terminal_girdi->맨위||Terminal_girdi->SATIR_konum>=Terminal_girdi->맨위+Terminal_girdi->SATIR_BAĞ_DEĞ_SAY)return;
    if(!şov_pencere||!Terminal_girdi->가리개보임)그리기(Terminal_girdi->SATIR_konum,Terminal_girdi->SÜTUN_konum);else 사각영역(Terminal_girdi->x_koordinatı+12+Terminal_girdi->SÜTUN_konum*8,Terminal_girdi->Y_koordinat+36+(Terminal_girdi->SATIR_konum-Terminal_girdi->맨위)*16+14,8,2,색상들[Terminal_girdi->전경색]);}
static void içerik_değer(void){
    사각영역(Terminal_girdi->x_koordinatı+12,Terminal_girdi->Y_koordinat+36,Terminal_girdi->SÜTUNSAY*8,Terminal_girdi->SATIR_BAĞ_DEĞ_SAY*16,색상들[0]);
    int 가로=Terminal_girdi->x_koordinatı+12,Dikey_konum=Terminal_girdi->Y_koordinat+36,폭=Terminal_girdi->SÜTUNSAY*8,süre_değer=Terminal_girdi->SATIR_BAĞ_DEĞ_SAY*16;
    if(보드그림범위(&가로,&Dikey_konum,&폭,&süre_değer)){
    unsigned 첫줄=(Dikey_konum-Terminal_girdi->Y_koordinat-36)/16,끝줄=(Dikey_konum+süre_değer-Terminal_girdi->Y_koordinat-36+15)/16;
    unsigned 첫칸=(가로-Terminal_girdi->x_koordinatı-12)/8,끝칸=(가로+폭-Terminal_girdi->x_koordinatı-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 sınır_değer 왼쪽에서 시작한 두 yuva_girdi 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned kod_noktası=첫칸;kod_noktası<끝칸;kod_noktası++){
        unsigned SATIR_konum=첫항목()-Terminal_girdi->kaydırmak_6486617f+반환값,karakter_değer=Terminal_girdi->글자칸들[SATIR_konum%Geçmiş_hat_BAĞ_DEĞ_SAY][kod_noktası],dize_veri=Terminal_girdi->모양들[SATIR_konum%Geçmiş_hat_BAĞ_DEĞ_SAY][kod_noktası];
        if(geniş_karakter(karakter_değer)==2&&kod_noktası+1>=Terminal_girdi->SÜTUNSAY)karakter_değer=' ';
        if((karakter_değer==0||karakter_değer==' ')&&(dize_veri>>4)==0)continue;
        Terminal_karakter(Terminal_girdi->x_koordinatı+12+kod_noktası*8,Terminal_girdi->Y_koordinat+36+반환값*16,karakter_değer?karakter_değer:' ',색상들[dize_veri&15],색상들[dize_veri>>4]);
    }}
    ad_tablo(Terminal_girdi->x_koordinatı+12,Terminal_girdi->Y_koordinat+Terminal_girdi->높이-18,Terminal_girdi->kaydırmak_6486617f?"PgDn: recent output":Terminal_girdi->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);şapka_karakteri_değer(1);
}
static void yürütme_kare(int tanımlayıcı_değer){
    Terminal_girdi=&Windows_Liste[tanımlayıcı_değer];
    int 가로=Terminal_girdi->x_koordinatı,Dikey_konum=Terminal_girdi->Y_koordinat,폭=Terminal_girdi->너비,süre_değer=Terminal_girdi->높이;
    if(!보드그림범위(&가로,&Dikey_konum,&폭,&süre_değer))return;
    사각영역(Terminal_girdi->x_koordinatı,Terminal_girdi->Y_koordinat,Terminal_girdi->너비,Terminal_girdi->높이,0x403127);
    unsigned 색상=tanımlayıcı_değer==Odak?0x905020:0x604438;사각영역(Terminal_girdi->x_koordinatı,Terminal_girdi->Y_koordinat,Terminal_girdi->너비,30,색상);
    ad_tablo(Terminal_girdi->x_koordinatı+12,Terminal_girdi->Y_koordinat+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+tanımlayıcı_değer),0};ad_tablo(Terminal_girdi->x_koordinatı+148,Terminal_girdi->Y_koordinat+7,수치,0xffffff,색상);
    ad_tablo(Terminal_girdi->x_koordinatı+240,Terminal_girdi->Y_koordinat+7,Terminal_girdi->너비>=500?(한글입력?"[TR] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[TR]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_girdi->x_koordinatı+Terminal_girdi->너비-32,Terminal_girdi->Y_koordinat+4,26,22,0x5555b8);ad_tablo(Terminal_girdi->x_koordinatı+Terminal_girdi->너비-24,Terminal_girdi->Y_koordinat+7,"X",0xffffff,0x5555b8);
    içerik_değer();
}
static void Çizim_sahne(void){
    if(!Masaüstü_Görünüm)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);ad_tablo(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Liste[순번].살아있음){unsigned kod_noktası=Odak==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,kod_noktası);ad_tablo(160+순번*112,8,"Terminal",0xffffff,kod_noktası);char dize_veri[2]={(char)('1'+순번),0};ad_tablo(232+순번*112,8,dize_veri,0xffffff,kod_noktası);}
    if(!girdi_BAĞ_DEĞ_SAY)ad_tablo(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<girdi_BAĞ_DEĞ_SAY;순번++)yürütme_kare(düzen_değer[순번]);화면다시그림(Odak);Terminal_girdi=&Windows_Liste[çıktı];
}
static void Paint_bölge(int 가로,int Dikey_konum,int 폭,int süre_değer){
    if(!Masaüstü_Görünüm||!보드그림범위(&가로,&Dikey_konum,&폭,&süre_değer))return;
    for(int girdi_satırı=Dikey_konum;girdi_satırı<Dikey_konum+süre_değer;girdi_satırı+=32){
        int 띠높이=Dikey_konum+süre_değer-girdi_satırı;if(띠높이>32)띠높이=32;
        if(Pano_Start_çizim(가로,girdi_satırı,폭,띠높이)){Çizim_sahne();Pano_Son_çizim();}
    }
}
static void 다시그리기(void){Paint_bölge(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Pencere 영역과 Önceki_öğe 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Dikey_konum,int 폭,int süre_değer,Terminal *Pencere){
    int 왼쪽=가로>(int)Pencere->x_koordinatı?가로:(int)Pencere->x_koordinatı;
    int 위쪽=Dikey_konum>(int)Pencere->Y_koordinat?Dikey_konum:(int)Pencere->Y_koordinat;
    int hak=가로+폭<(int)(Pencere->x_koordinatı+Pencere->너비)?가로+폭:(int)(Pencere->x_koordinatı+Pencere->너비);
    int 아래쪽=Dikey_konum+süre_değer<(int)(Pencere->Y_koordinat+Pencere->높이)?Dikey_konum+süre_değer:(int)(Pencere->Y_koordinat+Pencere->높이);
    Paint_bölge(Pencere->x_koordinatı,Pencere->Y_koordinat,Pencere->너비,Pencere->높이);
    if(왼쪽>=hak||위쪽>=아래쪽){Paint_bölge(가로,Dikey_konum,폭,süre_değer);return;}
    Paint_bölge(가로,Dikey_konum,폭,위쪽-Dikey_konum);
    Paint_bölge(가로,아래쪽,폭,Dikey_konum+süre_değer-아래쪽);
    Paint_bölge(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Paint_bölge(hak,위쪽,가로+폭-hak,아래쪽-위쪽);
}
static void sinyal_Odak(void){bilgi_teknolojisi_Beklemede=(bilgi_teknolojisi_Beklemede&~15u)|(unsigned)(Odak+1)|0x10000;}
void Terminal_artış_mod(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Odak>=0){
        Terminal *pencere_girdi=&Windows_Liste[Odak];
        ad_tablo(pencere_girdi->x_koordinatı+240,pencere_girdi->Y_koordinat+7,pencere_girdi->너비>=500?(한글입력?"[TR] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[TR]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int tanımlayıcı_değer){if(tanımlayıcı_değer<0||tanımlayıcı_değer>=4||!Windows_Liste[tanımlayıcı_değer].살아있음)return;int geçerli_konum=0;while(geçerli_konum<girdi_BAĞ_DEĞ_SAY&&düzen_değer[geçerli_konum]!=tanımlayıcı_değer)geçerli_konum++;for(;geçerli_konum+1<girdi_BAĞ_DEĞ_SAY;geçerli_konum++)düzen_değer[geçerli_konum]=düzen_değer[geçerli_konum+1];düzen_değer[girdi_BAĞ_DEĞ_SAY-1]=tanımlayıcı_değer;Odak=tanımlayıcı_değer;sinyal_Odak();다시그리기();}
static void 빈칸채우기(unsigned SATIR_konum){for(unsigned kod_noktası=0;kod_noktası<최대열수;kod_noktası++){Terminal_girdi->글자칸들[SATIR_konum%Geçmiş_hat_BAĞ_DEĞ_SAY][kod_noktası]=0;Terminal_girdi->모양들[SATIR_konum%Geçmiş_hat_BAĞ_DEĞ_SAY][kod_noktası]=Terminal_girdi->전경색|(Terminal_girdi->배경색<<4);}}
static void takas_içindekiler(void){Terminal_girdi->SATIR_konum=Terminal_girdi->SÜTUN_konum=Terminal_girdi->맨위=Terminal_girdi->kaydırmak_6486617f=0;for(unsigned 반환값=0;반환값<Geçmiş_hat_BAĞ_DEĞ_SAY;반환값++)빈칸채우기(반환값);if(보이는지())içerik_değer();}
static int açmak_girdi(void){
    if(!보드화면기억공간())return -19;int tanımlayıcı_değer=0;while(tanımlayıcı_değer<4&&Windows_Liste[tanımlayıcı_değer].살아있음)tanımlayıcı_değer++;if(tanımlayıcı_değer==4)return -28;
    Masaüstü_Görünüm=1;Terminal_girdi=&Windows_Liste[tanımlayıcı_değer];memset(Terminal_girdi,0,sizeof(*Terminal_girdi));Terminal_girdi->살아있음=1;Terminal_girdi->너비=568;Terminal_girdi->높이=360;Terminal_girdi->SÜTUNSAY=68;Terminal_girdi->SATIR_BAĞ_DEĞ_SAY=19;Terminal_girdi->x_koordinatı=12+tanımlayıcı_değer*16;Terminal_girdi->Y_koordinat=48+tanımlayıcı_değer*18;Terminal_girdi->전경색=7;Terminal_girdi->가리개보임=1;
    for(unsigned 반환값=0;반환값<Geçmiş_hat_BAĞ_DEĞ_SAY;반환값++)빈칸채우기(반환값);düzen_değer[girdi_BAĞ_DEĞ_SAY++]=tanımlayıcı_değer;Odak=tanımlayıcı_değer;bilgi_teknolojisi_Beklemede|=1u<<(4+tanımlayıcı_değer);sinyal_Odak();다시그리기();return tanımlayıcı_değer+1;
}
static void Kapat_pencere(int tanımlayıcı_değer){
    if(tanımlayıcı_değer<0||tanımlayıcı_değer>=4||!Windows_Liste[tanımlayıcı_değer].살아있음)return;Windows_Liste[tanımlayıcı_değer].살아있음=0;bilgi_teknolojisi_Beklemede|=1u<<(8+tanımlayıcı_değer);
    int geçerli_konum=0;while(geçerli_konum<girdi_BAĞ_DEĞ_SAY&&düzen_değer[geçerli_konum]!=tanımlayıcı_değer)geçerli_konum++;for(;geçerli_konum+1<girdi_BAĞ_DEĞ_SAY;geçerli_konum++)düzen_değer[geçerli_konum]=düzen_değer[geçerli_konum+1];girdi_BAĞ_DEĞ_SAY--;
    if(Odak==tanımlayıcı_değer)Odak=girdi_BAĞ_DEĞ_SAY?düzen_değer[girdi_BAĞ_DEĞ_SAY-1]:-1;sinyal_Odak();다시그리기();
}
static void 줄바꿈(void){Terminal_girdi->SÜTUN_konum=0;Terminal_girdi->SATIR_konum++;if(Terminal_girdi->SATIR_konum>=Terminal_girdi->맨위+Terminal_girdi->SATIR_BAĞ_DEĞ_SAY){Terminal_girdi->맨위++;빈칸채우기(Terminal_girdi->SATIR_konum);if(보이는지())içerik_değer();}}
static void kod_öğesi(unsigned kod_noktası){
    if(kod_noktası==13){Terminal_girdi->SÜTUN_konum=0;return;}if(kod_noktası==10){줄바꿈();return;}if(kod_noktası==8){if(Terminal_girdi->SÜTUN_konum)Terminal_girdi->SÜTUN_konum--;return;}
    if(kod_noktası==9){unsigned öğe_BAĞ_DEĞ_SAY=8-Terminal_girdi->SÜTUN_konum%8;while(öğe_BAĞ_DEĞ_SAY--)kod_öğesi(' ');return;}if(kod_noktası<32||kod_noktası==127)return;
    unsigned 너비값=geniş_karakter(kod_noktası);if(Terminal_girdi->SÜTUN_konum+너비값>Terminal_girdi->SÜTUNSAY)줄바꿈();
    if(Terminal_girdi->글자칸들[Terminal_girdi->SATIR_konum%Geçmiş_hat_BAĞ_DEĞ_SAY][Terminal_girdi->SÜTUN_konum]==0xffffffffu&&Terminal_girdi->SÜTUN_konum){Terminal_girdi->글자칸들[Terminal_girdi->SATIR_konum%Geçmiş_hat_BAĞ_DEĞ_SAY][Terminal_girdi->SÜTUN_konum-1]=' ';그리기(Terminal_girdi->SATIR_konum,Terminal_girdi->SÜTUN_konum-1);}
    if(geniş_karakter(Terminal_girdi->글자칸들[Terminal_girdi->SATIR_konum%Geçmiş_hat_BAĞ_DEĞ_SAY][Terminal_girdi->SÜTUN_konum])==2&&Terminal_girdi->SÜTUN_konum+1<Terminal_girdi->SÜTUNSAY){Terminal_girdi->글자칸들[Terminal_girdi->SATIR_konum%Geçmiş_hat_BAĞ_DEĞ_SAY][Terminal_girdi->SÜTUN_konum+1]=' ';그리기(Terminal_girdi->SATIR_konum,Terminal_girdi->SÜTUN_konum+1);}
    Terminal_girdi->글자칸들[Terminal_girdi->SATIR_konum%Geçmiş_hat_BAĞ_DEĞ_SAY][Terminal_girdi->SÜTUN_konum]=kod_noktası;Terminal_girdi->모양들[Terminal_girdi->SATIR_konum%Geçmiş_hat_BAĞ_DEĞ_SAY][Terminal_girdi->SÜTUN_konum]=Terminal_girdi->전경색|(Terminal_girdi->배경색<<4);
    if(너비값==2)Terminal_girdi->글자칸들[Terminal_girdi->SATIR_konum%Geçmiş_hat_BAĞ_DEĞ_SAY][Terminal_girdi->SÜTUN_konum+1]=0xffffffffu;
    그리기(Terminal_girdi->SATIR_konum,Terminal_girdi->SÜTUN_konum);Terminal_girdi->SÜTUN_konum+=너비값;
}
static void sap_denetim_dizi(unsigned kod_noktası){
    unsigned öğe_BAĞ_DEĞ_SAY=Terminal_girdi->parametre_değer[0]?Terminal_girdi->parametre_değer[0]:1;
    if(kod_noktası=='m')for(unsigned 순번=0;순번<=Terminal_girdi->parametre_Dizin;순번++){unsigned veri_konum=Terminal_girdi->parametre_değer[순번];if(!veri_konum){Terminal_girdi->전경색=7;Terminal_girdi->배경색=0;}if(veri_konum==1&&Terminal_girdi->전경색<8)Terminal_girdi->전경색+=8;if(veri_konum==7){unsigned 유지=Terminal_girdi->전경색;Terminal_girdi->전경색=Terminal_girdi->배경색;Terminal_girdi->배경색=유지;}if(veri_konum>=30&&veri_konum<=37)Terminal_girdi->전경색=veri_konum-30;if(veri_konum>=90&&veri_konum<=97)Terminal_girdi->전경색=veri_konum-90+8;if(veri_konum>=40&&veri_konum<=47)Terminal_girdi->배경색=veri_konum-40;if(veri_konum>=100&&veri_konum<=107)Terminal_girdi->배경색=veri_konum-100+8;if(veri_konum==39)Terminal_girdi->전경색=7;if(veri_konum==49)Terminal_girdi->배경색=0;}
    if(kod_noktası=='J'&&(Terminal_girdi->parametre_değer[0]==2||Terminal_girdi->parametre_değer[0]==3))takas_içindekiler();
    if(kod_noktası=='K'){unsigned 출발위치=Terminal_girdi->parametre_değer[0]==2?0:Terminal_girdi->SÜTUN_konum,도착위치=Terminal_girdi->parametre_değer[0]==1?Terminal_girdi->SÜTUN_konum+1:Terminal_girdi->SÜTUNSAY;if(Terminal_girdi->parametre_değer[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_girdi->SÜTUNSAY;순번++){
        unsigned SATIR_değer=Terminal_girdi->SATIR_konum%Geçmiş_hat_BAĞ_DEĞ_SAY,karakter_değer=Terminal_girdi->글자칸들[SATIR_değer][순번],şekil_değer=Terminal_girdi->전경색|(Terminal_girdi->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 yazı_tipi_değer 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(karakter_değer!=0&&karakter_değer!=' ')||Terminal_girdi->모양들[SATIR_değer][순번]!=şekil_değer;
        Terminal_girdi->글자칸들[SATIR_değer][순번]=' ';Terminal_girdi->모양들[SATIR_değer][순번]=şekil_değer;
        if(바뀜)그리기(Terminal_girdi->SATIR_konum,순번);
    }}
    if(kod_noktası=='D')Terminal_girdi->SÜTUN_konum=öğe_BAĞ_DEĞ_SAY>Terminal_girdi->SÜTUN_konum?0:Terminal_girdi->SÜTUN_konum-öğe_BAĞ_DEĞ_SAY;if(kod_noktası=='C')Terminal_girdi->SÜTUN_konum=Terminal_girdi->SÜTUN_konum+öğe_BAĞ_DEĞ_SAY>=Terminal_girdi->SÜTUNSAY?Terminal_girdi->SÜTUNSAY-1:Terminal_girdi->SÜTUN_konum+öğe_BAĞ_DEĞ_SAY;
    if(kod_noktası=='G')Terminal_girdi->SÜTUN_konum=öğe_BAĞ_DEĞ_SAY>Terminal_girdi->SÜTUNSAY?Terminal_girdi->SÜTUNSAY-1:öğe_BAĞ_DEĞ_SAY-1;if(kod_noktası=='A')Terminal_girdi->SATIR_konum=öğe_BAĞ_DEĞ_SAY>Terminal_girdi->SATIR_konum-Terminal_girdi->맨위?Terminal_girdi->맨위:Terminal_girdi->SATIR_konum-öğe_BAĞ_DEĞ_SAY;
    if(kod_noktası=='B')Terminal_girdi->SATIR_konum=Terminal_girdi->SATIR_konum+öğe_BAĞ_DEĞ_SAY>=Terminal_girdi->맨위+Terminal_girdi->SATIR_BAĞ_DEĞ_SAY?Terminal_girdi->맨위+Terminal_girdi->SATIR_BAĞ_DEĞ_SAY-1:Terminal_girdi->SATIR_konum+öğe_BAĞ_DEĞ_SAY;
    if(kod_noktası=='H'||kod_noktası=='f'){Terminal_girdi->SATIR_konum=Terminal_girdi->맨위+(öğe_BAĞ_DEĞ_SAY>Terminal_girdi->SATIR_BAĞ_DEĞ_SAY?Terminal_girdi->SATIR_BAĞ_DEĞ_SAY:öğe_BAĞ_DEĞ_SAY)-1;unsigned x_koordinatı=Terminal_girdi->parametre_değer[1]?Terminal_girdi->parametre_değer[1]:1;Terminal_girdi->SÜTUN_konum=(x_koordinatı>Terminal_girdi->SÜTUNSAY?Terminal_girdi->SÜTUNSAY:x_koordinatı)-1;}
    if(kod_noktası=='s'){Terminal_girdi->저장행=Terminal_girdi->SATIR_konum;Terminal_girdi->저장열=Terminal_girdi->SÜTUN_konum;}if(kod_noktası=='u'){Terminal_girdi->SATIR_konum=Terminal_girdi->저장행;Terminal_girdi->SÜTUN_konum=Terminal_girdi->저장열<Terminal_girdi->SÜTUNSAY?Terminal_girdi->저장열:Terminal_girdi->SÜTUNSAY-1;}
    if((kod_noktası=='h'||kod_noktası=='l')&&Terminal_girdi->parametre_değer[0]==25)Terminal_girdi->가리개보임=kod_noktası=='h';
}
void Terminal_bayt(unsigned SANİYE_değer){
    Terminal_girdi=&Windows_Liste[çıktı];if(!Terminal_girdi->살아있음)return;şapka_karakteri_değer(0);if(Terminal_girdi->kaydırmak_6486617f){Terminal_girdi->kaydırmak_6486617f=0;if(보이는지())içerik_değer();}
    if(Terminal_girdi->탈출상태==1){Terminal_girdi->탈출상태=SANİYE_değer=='['?2:0;Terminal_girdi->parametre_Dizin=0;for(unsigned 순번=0;순번<4;순번++)Terminal_girdi->parametre_değer[순번]=0;}
    else if(Terminal_girdi->탈출상태==2){if(SANİYE_değer=='?'){}else if(SANİYE_değer>='0'&&SANİYE_değer<='9'){if(Terminal_girdi->parametre_değer[Terminal_girdi->parametre_Dizin]<10000)Terminal_girdi->parametre_değer[Terminal_girdi->parametre_Dizin]=Terminal_girdi->parametre_değer[Terminal_girdi->parametre_Dizin]*10+SANİYE_değer-'0';}else if(SANİYE_değer==';'&&Terminal_girdi->parametre_Dizin<3)Terminal_girdi->parametre_Dizin++;else{sap_denetim_dizi(SANİYE_değer);Terminal_girdi->탈출상태=0;}}
    else if(SANİYE_değer==27){Terminal_girdi->긴부호없는값=0;Terminal_girdi->탈출상태=1;}else{
        if(Terminal_girdi->긴부호없는값&&(SANİYE_değer&0xc0)!=0x80){Terminal_girdi->긴부호없는값=0;kod_öğesi(0xfffd);}
        if(Terminal_girdi->긴부호없는값){Terminal_girdi->부호없는결과=Terminal_girdi->부호없는결과*64+(SANİYE_değer&63);if(--Terminal_girdi->긴부호없는값==0)kod_öğesi(Terminal_girdi->부호없는결과<Terminal_girdi->KÜÇÜK_değer||Terminal_girdi->부호없는결과>0x10ffff||(Terminal_girdi->부호없는결과>=0xd800&&Terminal_girdi->부호없는결과<=0xdfff)?0xfffd:Terminal_girdi->부호없는결과);}
        else if(SANİYE_değer<128)kod_öğesi(SANİYE_değer);else if(SANİYE_değer>=0xc2&&SANİYE_değer<=0xf4){Terminal_girdi->긴부호없는값=SANİYE_değer<0xe0?1:SANİYE_değer<0xf0?2:3;Terminal_girdi->부호없는결과=SANİYE_değer&((1u<<(6-Terminal_girdi->긴부호없는값))-1);Terminal_girdi->KÜÇÜK_değer=Terminal_girdi->긴부호없는값==1?128:Terminal_girdi->긴부호없는값==2?2048:65536;}else kod_öğesi(0xfffd);
    }şapka_karakteri_değer(1);
}
int Terminal_Beklemede(void){return bilgi_teknolojisi_Beklemede!=0;}
/* 모서리 Dizin: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int yeniden_boyutlandırmak_sürüklemek=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Dikey_konum) {
    for(int dizi_değer=girdi_BAĞ_DEĞ_SAY-1;dizi_değer>=0;dizi_değer--){
        int tanımlayıcı_değer=düzen_değer[dizi_değer];Terminal *Pencere=&Windows_Liste[tanımlayıcı_değer];
        if(가로>=(int)Pencere->x_koordinatı&&Dikey_konum>=(int)Pencere->Y_koordinat&&
           가로<(int)(Pencere->x_koordinatı+Pencere->너비)&&Dikey_konum<(int)(Pencere->Y_koordinat+Pencere->높이))return tanımlayıcı_değer;
    }return -1;
}
static int 모서리찾기(int tanımlayıcı_değer,int 가로,int Dikey_konum) {
    if(tanımlayıcı_değer<0)return 0;Terminal *Pencere=&Windows_Liste[tanımlayıcı_değer];
    int 왼쪽=가로<(int)Pencere->x_koordinatı+8,hak=가로>=(int)(Pencere->x_koordinatı+Pencere->너비)-8;
    int 위쪽=Dikey_konum<(int)Pencere->Y_koordinat+8,아래쪽=Dikey_konum>=(int)(Pencere->Y_koordinat+Pencere->높이)-8;
    return (왼쪽||hak)&&(위쪽||아래쪽)?1+hak+아래쪽*2:0;
}
static int ayıraç_değer(int değer,int 최소,int 최대){return değer<최소?최소:değer>최대?최대:değer;}
static void taşımak_yeniden_boyutlandırmak(int 가로,int Dikey_konum) {
    Terminal *Pencere=&Windows_Liste[yeniden_boyutlandırmak_sürüklemek];int 왼쪽=처음가로,위쪽=처음세로,hak=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=ayıraç_değer(처음가로+가로-잡은가로,0,hak-360);
    else hak=ayıraç_değer(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=ayıraç_değer(처음세로+Dikey_konum-잡은세로,34,아래쪽-216);
    else 아래쪽=ayıraç_değer(처음세로+처음높이+Dikey_konum-잡은세로,위쪽+216,보드화면높이());
    unsigned SÜTUNSAY=(hak-왼쪽-24)/8,SATIR_BAĞ_DEĞ_SAY=(아래쪽-위쪽-56)/16;
    if(Pencere->SÜTUNSAY!=SÜTUNSAY||Pencere->SATIR_BAĞ_DEĞ_SAY!=SATIR_BAĞ_DEĞ_SAY){
        Pencere->크기바뀜=1;Pencere->SÜTUNSAY=SÜTUNSAY;Pencere->SATIR_BAĞ_DEĞ_SAY=SATIR_BAĞ_DEĞ_SAY;
        if(Pencere->SÜTUN_konum>=SÜTUNSAY)Pencere->SÜTUN_konum=SÜTUNSAY-1;
        if(Pencere->SATIR_konum>=Pencere->맨위+SATIR_BAĞ_DEĞ_SAY)Pencere->맨위=Pencere->SATIR_konum-SATIR_BAĞ_DEĞ_SAY+1;
        unsigned 한도=Pencere->맨위;if(한도>Geçmiş_hat_BAĞ_DEĞ_SAY-SATIR_BAĞ_DEĞ_SAY)한도=Geçmiş_hat_BAĞ_DEĞ_SAY-SATIR_BAĞ_DEĞ_SAY;
        if(Pencere->kaydırmak_6486617f>한도)Pencere->kaydırmak_6486617f=한도;
    }
    int 옛가로=Pencere->x_koordinatı,옛세로=Pencere->Y_koordinat,옛폭=Pencere->너비,옛길이=Pencere->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==hak-왼쪽&&옛길이==아래쪽-위쪽)return;
    Pencere->x_koordinatı=왼쪽;Pencere->Y_koordinat=위쪽;Pencere->너비=hak-왼쪽;Pencere->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Pencere);
}
void Terminal_işaretçi(unsigned Sonraki_öğe,int x_koordinatı,int Y_koordinat){
    unsigned 눌림=Sonraki_öğe&~단추들;단추들=Sonraki_öğe;
    if(!Masaüstü_Görünüm){sürüklemek_değer=-1;yeniden_boyutlandırmak_sürüklemek=-1;Pano_işaretçi(x_koordinatı,Y_koordinat,1);return;}
    if(!(Sonraki_öğe&1)){sürüklemek_değer=-1;yeniden_boyutlandırmak_sürüklemek=-1;}
    if(yeniden_boyutlandırmak_sürüklemek>=0&&!Windows_Liste[yeniden_boyutlandırmak_sürüklemek].살아있음)yeniden_boyutlandırmak_sürüklemek=-1;
    if(sürüklemek_değer>=0&&!Windows_Liste[sürüklemek_değer].살아있음)sürüklemek_değer=-1;
    if(yeniden_boyutlandırmak_sürüklemek>=0){
        taşımak_yeniden_boyutlandırmak(x_koordinatı,Y_koordinat);Pano_işaretçi(x_koordinatı,Y_koordinat,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Pano_işaretçi(x_koordinatı,Y_koordinat,1);
    if(sürüklemek_değer>=0){
        Terminal *Pencere=&Windows_Liste[sürüklemek_değer];
        int 옛가로=Pencere->x_koordinatı,옛세로=Pencere->Y_koordinat;
        Pencere->x_koordinatı=ayıraç_değer(x_koordinatı-sürüklemek_X,0,보드화면너비()-Pencere->너비);
        Pencere->Y_koordinat=ayıraç_değer(Y_koordinat-sürüklemek_Y,34,보드화면높이()-Pencere->높이);
        if(옛가로!=(int)Pencere->x_koordinatı||옛세로!=(int)Pencere->Y_koordinat)창자리그리기(옛가로,옛세로,Pencere->너비,Pencere->높이,Pencere);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Odak,x_koordinatı,Y_koordinat)){화면가리킴(Odak,눌림,x_koordinatı,Y_koordinat);return;}
    int tanımlayıcı_değer=가리킨창(x_koordinatı,Y_koordinat),모서리=모서리찾기(tanımlayıcı_değer,x_koordinatı,Y_koordinat);
    if(모서리)Pano_işaretçi(x_koordinatı,Y_koordinat,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal *Pencere=&Windows_Liste[tanımlayıcı_değer];yeniden_boyutlandırmak_sürüklemek=tanımlayıcı_değer;잡은모서리=모서리;잡은가로=x_koordinatı;잡은세로=Y_koordinat;
            처음가로=Pencere->x_koordinatı;처음세로=Pencere->Y_koordinat;처음너비=Pencere->너비;처음높이=Pencere->높이;
            if(tanımlayıcı_değer!=Odak)앞으로올리기(tanımlayıcı_değer);return;
        }
        if(Y_koordinat<32&&x_koordinatı>=6&&x_koordinatı<142){açmak_girdi();return;}
        if(Y_koordinat<32&&x_koordinatı>=154&&x_koordinatı<602){앞으로올리기((x_koordinatı-154)/112);return;}
        if(tanımlayıcı_değer>=0){
            Terminal *Pencere=&Windows_Liste[tanımlayıcı_değer];
            if(Y_koordinat<(int)Pencere->Y_koordinat+30&&x_koordinatı>=(int)(Pencere->x_koordinatı+Pencere->너비)-32){Kapat_pencere(tanımlayıcı_değer);return;}
            if(tanımlayıcı_değer!=Odak)앞으로올리기(tanımlayıcı_değer);
            if(Y_koordinat<(int)Pencere->Y_koordinat+30){sürüklemek_değer=tanımlayıcı_değer;sürüklemek_X=x_koordinatı-Pencere->x_koordinatı;sürüklemek_Y=Y_koordinat-Pencere->Y_koordinat;}return;
        }
    }
    if(Odak>=0&&(눌림&(8|16))){Terminal_girdi=&Windows_Liste[Odak];if(눌림&8){unsigned 한도=Terminal_girdi->맨위;if(한도>Geçmiş_hat_BAĞ_DEĞ_SAY-Terminal_girdi->SATIR_BAĞ_DEĞ_SAY)한도=Geçmiş_hat_BAĞ_DEĞ_SAY-Terminal_girdi->SATIR_BAĞ_DEĞ_SAY;Terminal_girdi->kaydırmak_6486617f=Terminal_girdi->kaydırmak_6486617f+9>한도?한도:Terminal_girdi->kaydırmak_6486617f+9;}else Terminal_girdi->kaydırmak_6486617f=Terminal_girdi->kaydırmak_6486617f<9?0:Terminal_girdi->kaydırmak_6486617f-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)açmak_girdi();if(누름값==2&&girdi_BAĞ_DEĞ_SAY)앞으로올리기(düzen_değer[0]);if(누름값==3)Kapat_pencere(Odak);}
makine_Word Pano_Terminal(makine_Word Eylem){
    if(Eylem==300){if(!Windows_Liste[çıktı].살아있음)return açmak_girdi();Masaüstü_Görünüm=1;다시그리기();return 0;}
    if(Eylem==0){Kapat_pencere(Odak);return 0;}if(Eylem==1)return (uint32_t)açmak_girdi();if(Eylem==2)return Odak>=0;
    if(Eylem==9){Masaüstü_Görünüm=0;return 0;}if(Eylem==7)return girdi_BAĞ_DEĞ_SAY;if(Eylem==10)return Odak+1;if(Eylem==11)return çıktı;
    if(Eylem==13){Terminal *Pencere=&Windows_Liste[çıktı];return Pencere->살아있음?(Pencere->SATIR_BAĞ_DEĞ_SAY<<16)|Pencere->SÜTUNSAY:(19<<16)|68;}
    if(Eylem==14){unsigned değer=Windows_Liste[çıktı].크기바뀜;Windows_Liste[çıktı].크기바뀜=0;return değer;}
    if(Eylem==12){unsigned değer=bilgi_teknolojisi_Beklemede;bilgi_teknolojisi_Beklemede=0;return değer;}
    if(Eylem>=20&&Eylem<24)return Windows_Liste[Eylem-20].살아있음;
    if(Eylem>=100&&Eylem<104){çıktı=Eylem-100;Terminal_girdi=&Windows_Liste[çıktı];return 0;}
    if(Eylem>=200&&Eylem<204){앞으로올리기(Eylem-200);return 0;}
    if(Eylem==3){다시그리기();return 0;}Terminal_girdi=&Windows_Liste[çıktı];if(!Terminal_girdi->살아있음)return 0;
    if(Eylem==4)takas_içindekiler();if(Eylem==5||Eylem==6){unsigned Önceki_öğe=단추들;Terminal_işaretçi(Eylem==5?8:16,0,0);단추들=Önceki_öğe;}return 1;
}
