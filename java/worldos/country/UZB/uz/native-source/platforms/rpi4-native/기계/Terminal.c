#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 oyna 합성과 UTF-8 Terminal. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t 기계낱말;
extern 기계낱말 yozuv_taxtasi_piksel(기계낱말,기계낱말,기계낱말),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_shrift[];
#define 최대열수 237
#define tarix_satr_COUNT 160
typedef struct {
    uint32_t 글자칸들[tarix_satr_COUNT][최대열수]; uint8_t 모양들[tarix_satr_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,x_koordinata,Y_tugmasi_koordinat,ROW_holat,ustun_holat,맨위,aylantirmoq,전경색,배경색,탈출상태,매개값[4],매개색인,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminal_d413d4bc;
static Terminal_d413d4bc Windows_Ro_yxat[4];
static int Fokus=-1,출력결과,tartib_VALUE[4],kiritish_COUNT,tortib_o_tkazmoq_VALUE=-1,tortib_o_tkazmoq_X_tugmasi,tortib_o_tkazmoq_Y_tugmasi;
static unsigned 대기중,단추들,ishchi_stol_ko_rinish,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal_d413d4bc *Terminal_kiritish;
static unsigned 넓은글자(unsigned belgi_kodi){return belgi_kodi>=256?2:1;}
static void 사각영역(unsigned x_koordinata,unsigned Y_tugmasi_koordinat,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(x_koordinata,Y_tugmasi_koordinat,너비값,높이값,색상);
}
void Terminal_glif(unsigned x_koordinata,unsigned Y_tugmasi_koordinat,unsigned belgi_kodi,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(belgi_kodi)*8;if(belgi_kodi==0xffffffffu)return;
    int 왼쪽=x_koordinata,위쪽=Y_tugmasi_koordinat,폭=너비,uzunlik_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&uzunlik_VALUE))return;
    if(belgi_kodi==' '){보드사각그림(왼쪽,위쪽,폭,uzunlik_VALUE,배경색);return;}
    unsigned LOOKUP_INDEX=belgi_kodi<65536?belgi_kodi:belgi_kodi>=0x1f600&&belgi_kodi<0x1f650?65536+belgi_kodi-0x1f600:0xfffd;
    const unsigned char *shrift_VALUE=Terminal_shrift+LOOKUP_INDEX*32;
    for(int satr=위쪽;satr<위쪽+uzunlik_VALUE;satr++){unsigned fonda_intellektual_uzatish_xizmati_Ro_yxat=shrift_VALUE[(satr-Y_tugmasi_koordinat)*2]*256+shrift_VALUE[(satr-Y_tugmasi_koordinat)*2+1];for(int in_kiritish=왼쪽;in_kiritish<왼쪽+폭;in_kiritish++)yozuv_taxtasi_piksel(in_kiritish,satr,(fonda_intellektual_uzatish_xizmati_Ro_yxat&(0x8000>>(in_kiritish-x_koordinata)))?전경색:배경색);}
}
static void nom_jadval(unsigned x_koordinata,unsigned Y_tugmasi_koordinat,const char *satr_ma_lumotlar,unsigned 전경색,unsigned 배경색){while(*satr_ma_lumotlar){unsigned belgi_kodi=(unsigned char)*satr_ma_lumotlar++, 남은수=0;if(belgi_kodi>=0xc0){남은수=belgi_kodi<0xe0?1:belgi_kodi<0xf0?2:3;belgi_kodi&=(1u<<(6-남은수))-1;while(남은수--&&*satr_ma_lumotlar)belgi_kodi=(belgi_kodi<<6)|((unsigned char)*satr_ma_lumotlar++&63);}Terminal_glif(x_koordinata,Y_tugmasi_koordinat,belgi_kodi,전경색,배경색);x_koordinata+=넓은글자(belgi_kodi)*8;}}
static unsigned 첫항목(void){return Terminal_kiritish->맨위;}
static int 보이는지(void){return Terminal_kiritish->살아있음&&Fokus>=0&&Terminal_kiritish==&Windows_Ro_yxat[Fokus]&&!화면보임(Fokus);}
static void 그리기(unsigned ROW_holat,unsigned ustun_holat){
    if(!보이는지()||ROW_holat<첫항목()-Terminal_kiritish->aylantirmoq||ROW_holat>=첫항목()-Terminal_kiritish->aylantirmoq+Terminal_kiritish->ROW_COUNT||ustun_holat>=Terminal_kiritish->COLUMNS)return;
    unsigned belgi_kodi=Terminal_kiritish->글자칸들[ROW_holat%tarix_satr_COUNT][ustun_holat],satr_ma_lumotlar=Terminal_kiritish->모양들[ROW_holat%tarix_satr_COUNT][ustun_holat];
    if(넓은글자(belgi_kodi)==2&&ustun_holat+1>=Terminal_kiritish->COLUMNS)belgi_kodi=' ';
    Terminal_glif(Terminal_kiritish->x_koordinata+12+ustun_holat*8,Terminal_kiritish->Y_tugmasi_koordinat+36+(ROW_holat-첫항목()+Terminal_kiritish->aylantirmoq)*16,belgi_kodi?belgi_kodi:' ',색상들[satr_ma_lumotlar&15],색상들[satr_ma_lumotlar>>4]);
}
static void qo_shib_qo_yish_belgisi_VALUE(int ko_rsatmoq_oyna){if(!보이는지()||Terminal_kiritish->aylantirmoq||Terminal_kiritish->ustun_holat>=Terminal_kiritish->COLUMNS||Terminal_kiritish->ROW_holat<Terminal_kiritish->맨위||Terminal_kiritish->ROW_holat>=Terminal_kiritish->맨위+Terminal_kiritish->ROW_COUNT)return;
    if(!ko_rsatmoq_oyna||!Terminal_kiritish->가리개보임)그리기(Terminal_kiritish->ROW_holat,Terminal_kiritish->ustun_holat);else 사각영역(Terminal_kiritish->x_koordinata+12+Terminal_kiritish->ustun_holat*8,Terminal_kiritish->Y_tugmasi_koordinat+36+(Terminal_kiritish->ROW_holat-Terminal_kiritish->맨위)*16+14,8,2,색상들[Terminal_kiritish->전경색]);}
static void tarkib_VALUE(void){
    사각영역(Terminal_kiritish->x_koordinata+12,Terminal_kiritish->Y_tugmasi_koordinat+36,Terminal_kiritish->COLUMNS*8,Terminal_kiritish->ROW_COUNT*16,색상들[0]);
    int 가로=Terminal_kiritish->x_koordinata+12,Vertikal_holat=Terminal_kiritish->Y_tugmasi_koordinat+36,폭=Terminal_kiritish->COLUMNS*8,uzunlik_VALUE=Terminal_kiritish->ROW_COUNT*16;
    if(보드그림범위(&가로,&Vertikal_holat,&폭,&uzunlik_VALUE)){
    unsigned 첫줄=(Vertikal_holat-Terminal_kiritish->Y_tugmasi_koordinat-36)/16,끝줄=(Vertikal_holat+uzunlik_VALUE-Terminal_kiritish->Y_tugmasi_koordinat-36+15)/16;
    unsigned 첫칸=(가로-Terminal_kiritish->x_koordinata-12)/8,끝칸=(가로+폭-Terminal_kiritish->x_koordinata-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 in_kiritish 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned belgi_kodi=첫칸;belgi_kodi<끝칸;belgi_kodi++){
        unsigned ROW_holat=첫항목()-Terminal_kiritish->aylantirmoq+반환값,belgi_VALUE=Terminal_kiritish->글자칸들[ROW_holat%tarix_satr_COUNT][belgi_kodi],satr_ma_lumotlar=Terminal_kiritish->모양들[ROW_holat%tarix_satr_COUNT][belgi_kodi];
        if(넓은글자(belgi_VALUE)==2&&belgi_kodi+1>=Terminal_kiritish->COLUMNS)belgi_VALUE=' ';
        if((belgi_VALUE==0||belgi_VALUE==' ')&&(satr_ma_lumotlar>>4)==0)continue;
        Terminal_glif(Terminal_kiritish->x_koordinata+12+belgi_kodi*8,Terminal_kiritish->Y_tugmasi_koordinat+36+반환값*16,belgi_VALUE?belgi_VALUE:' ',색상들[satr_ma_lumotlar&15],색상들[satr_ma_lumotlar>>4]);
    }}
    nom_jadval(Terminal_kiritish->x_koordinata+12,Terminal_kiritish->Y_tugmasi_koordinat+Terminal_kiritish->높이-18,Terminal_kiritish->aylantirmoq?"PgDn: recent output":Terminal_kiritish->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);qo_shib_qo_yish_belgisi_VALUE(1);
}
static void 실행틀(int identifikator_VALUE){
    Terminal_kiritish=&Windows_Ro_yxat[identifikator_VALUE];
    int 가로=Terminal_kiritish->x_koordinata,Vertikal_holat=Terminal_kiritish->Y_tugmasi_koordinat,폭=Terminal_kiritish->너비,uzunlik_VALUE=Terminal_kiritish->높이;
    if(!보드그림범위(&가로,&Vertikal_holat,&폭,&uzunlik_VALUE))return;
    사각영역(Terminal_kiritish->x_koordinata,Terminal_kiritish->Y_tugmasi_koordinat,Terminal_kiritish->너비,Terminal_kiritish->높이,0x403127);
    unsigned 색상=identifikator_VALUE==Fokus?0x905020:0x604438;사각영역(Terminal_kiritish->x_koordinata,Terminal_kiritish->Y_tugmasi_koordinat,Terminal_kiritish->너비,30,색상);
    nom_jadval(Terminal_kiritish->x_koordinata+12,Terminal_kiritish->Y_tugmasi_koordinat+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikator_VALUE),0};nom_jadval(Terminal_kiritish->x_koordinata+148,Terminal_kiritish->Y_tugmasi_koordinat+7,수치,0xffffff,색상);
    nom_jadval(Terminal_kiritish->x_koordinata+240,Terminal_kiritish->Y_tugmasi_koordinat+7,Terminal_kiritish->너비>=500?(한글입력?"[UZ] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[UZ]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_kiritish->x_koordinata+Terminal_kiritish->너비-32,Terminal_kiritish->Y_tugmasi_koordinat+4,26,22,0x5555b8);nom_jadval(Terminal_kiritish->x_koordinata+Terminal_kiritish->너비-24,Terminal_kiritish->Y_tugmasi_koordinat+7,"X",0xffffff,0x5555b8);
    tarkib_VALUE();
}
static void 장면그리기(void){
    if(!ishchi_stol_ko_rinish)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);nom_jadval(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Ro_yxat[순번].살아있음){unsigned belgi_kodi=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,belgi_kodi);nom_jadval(160+순번*112,8,"Terminal",0xffffff,belgi_kodi);char satr_ma_lumotlar[2]={(char)('1'+순번),0};nom_jadval(232+순번*112,8,satr_ma_lumotlar,0xffffff,belgi_kodi);}
    if(!kiritish_COUNT)nom_jadval(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<kiritish_COUNT;순번++)실행틀(tartib_VALUE[순번]);화면다시그림(Fokus);Terminal_kiritish=&Windows_Ro_yxat[출력결과];
}
static void 영역그리기(int 가로,int Vertikal_holat,int 폭,int uzunlik_VALUE){
    if(!ishchi_stol_ko_rinish||!보드그림범위(&가로,&Vertikal_holat,&폭,&uzunlik_VALUE))return;
    for(int satr=Vertikal_holat;satr<Vertikal_holat+uzunlik_VALUE;satr+=32){
        int 띠높이=Vertikal_holat+uzunlik_VALUE-satr;if(띠높이>32)띠높이=32;
        if(yozuv_taxtasi_Start_chizish(가로,satr,폭,띠높이)){장면그리기();yozuv_taxtasi_Tugatmoq_chizish();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 oyna 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Vertikal_holat,int 폭,int uzunlik_VALUE,Terminal_d413d4bc *oyna){
    int 왼쪽=가로>(int)oyna->x_koordinata?가로:(int)oyna->x_koordinata;
    int 위쪽=Vertikal_holat>(int)oyna->Y_tugmasi_koordinat?Vertikal_holat:(int)oyna->Y_tugmasi_koordinat;
    int RIGHT=가로+폭<(int)(oyna->x_koordinata+oyna->너비)?가로+폭:(int)(oyna->x_koordinata+oyna->너비);
    int 아래쪽=Vertikal_holat+uzunlik_VALUE<(int)(oyna->Y_tugmasi_koordinat+oyna->높이)?Vertikal_holat+uzunlik_VALUE:(int)(oyna->Y_tugmasi_koordinat+oyna->높이);
    영역그리기(oyna->x_koordinata,oyna->Y_tugmasi_koordinat,oyna->너비,oyna->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){영역그리기(가로,Vertikal_holat,폭,uzunlik_VALUE);return;}
    영역그리기(가로,Vertikal_holat,폭,위쪽-Vertikal_holat);
    영역그리기(가로,아래쪽,폭,Vertikal_holat+uzunlik_VALUE-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void 초점알리기(void){대기중=(대기중&~15u)|(unsigned)(Fokus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        Terminal_d413d4bc *oyna_kiritish=&Windows_Ro_yxat[Fokus];
        nom_jadval(oyna_kiritish->x_koordinata+240,oyna_kiritish->Y_tugmasi_koordinat+7,oyna_kiritish->너비>=500?(한글입력?"[UZ] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[UZ]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikator_VALUE){if(identifikator_VALUE<0||identifikator_VALUE>=4||!Windows_Ro_yxat[identifikator_VALUE].살아있음)return;int 현재위치=0;while(현재위치<kiritish_COUNT&&tartib_VALUE[현재위치]!=identifikator_VALUE)현재위치++;for(;현재위치+1<kiritish_COUNT;현재위치++)tartib_VALUE[현재위치]=tartib_VALUE[현재위치+1];tartib_VALUE[kiritish_COUNT-1]=identifikator_VALUE;Fokus=identifikator_VALUE;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned ROW_holat){for(unsigned belgi_kodi=0;belgi_kodi<최대열수;belgi_kodi++){Terminal_kiritish->글자칸들[ROW_holat%tarix_satr_COUNT][belgi_kodi]=0;Terminal_kiritish->모양들[ROW_holat%tarix_satr_COUNT][belgi_kodi]=Terminal_kiritish->전경색|(Terminal_kiritish->배경색<<4);}}
static void tozalamoq_TOC(void){Terminal_kiritish->ROW_holat=Terminal_kiritish->ustun_holat=Terminal_kiritish->맨위=Terminal_kiritish->aylantirmoq=0;for(unsigned 반환값=0;반환값<tarix_satr_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())tarkib_VALUE();}
static int Yaratish_kiritish(void){
    if(!보드화면기억공간())return -19;int identifikator_VALUE=0;while(identifikator_VALUE<4&&Windows_Ro_yxat[identifikator_VALUE].살아있음)identifikator_VALUE++;if(identifikator_VALUE==4)return -28;
    ishchi_stol_ko_rinish=1;Terminal_kiritish=&Windows_Ro_yxat[identifikator_VALUE];memset(Terminal_kiritish,0,sizeof(*Terminal_kiritish));Terminal_kiritish->살아있음=1;Terminal_kiritish->너비=568;Terminal_kiritish->높이=360;Terminal_kiritish->COLUMNS=68;Terminal_kiritish->ROW_COUNT=19;Terminal_kiritish->x_koordinata=12+identifikator_VALUE*16;Terminal_kiritish->Y_tugmasi_koordinat=48+identifikator_VALUE*18;Terminal_kiritish->전경색=7;Terminal_kiritish->가리개보임=1;
    for(unsigned 반환값=0;반환값<tarix_satr_COUNT;반환값++)빈칸채우기(반환값);tartib_VALUE[kiritish_COUNT++]=identifikator_VALUE;Fokus=identifikator_VALUE;대기중|=1u<<(4+identifikator_VALUE);초점알리기();다시그리기();return identifikator_VALUE+1;
}
static void yopmoq_oyna(int identifikator_VALUE){
    if(identifikator_VALUE<0||identifikator_VALUE>=4||!Windows_Ro_yxat[identifikator_VALUE].살아있음)return;Windows_Ro_yxat[identifikator_VALUE].살아있음=0;대기중|=1u<<(8+identifikator_VALUE);
    int 현재위치=0;while(현재위치<kiritish_COUNT&&tartib_VALUE[현재위치]!=identifikator_VALUE)현재위치++;for(;현재위치+1<kiritish_COUNT;현재위치++)tartib_VALUE[현재위치]=tartib_VALUE[현재위치+1];kiritish_COUNT--;
    if(Fokus==identifikator_VALUE)Fokus=kiritish_COUNT?tartib_VALUE[kiritish_COUNT-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){Terminal_kiritish->ustun_holat=0;Terminal_kiritish->ROW_holat++;if(Terminal_kiritish->ROW_holat>=Terminal_kiritish->맨위+Terminal_kiritish->ROW_COUNT){Terminal_kiritish->맨위++;빈칸채우기(Terminal_kiritish->ROW_holat);if(보이는지())tarkib_VALUE();}}
static void belgi_kodi_451f2815(unsigned belgi_kodi){
    if(belgi_kodi==13){Terminal_kiritish->ustun_holat=0;return;}if(belgi_kodi==10){줄바꿈();return;}if(belgi_kodi==8){if(Terminal_kiritish->ustun_holat)Terminal_kiritish->ustun_holat--;return;}
    if(belgi_kodi==9){unsigned element_COUNT=8-Terminal_kiritish->ustun_holat%8;while(element_COUNT--)belgi_kodi_451f2815(' ');return;}if(belgi_kodi<32||belgi_kodi==127)return;
    unsigned 너비값=넓은글자(belgi_kodi);if(Terminal_kiritish->ustun_holat+너비값>Terminal_kiritish->COLUMNS)줄바꿈();
    if(Terminal_kiritish->글자칸들[Terminal_kiritish->ROW_holat%tarix_satr_COUNT][Terminal_kiritish->ustun_holat]==0xffffffffu&&Terminal_kiritish->ustun_holat){Terminal_kiritish->글자칸들[Terminal_kiritish->ROW_holat%tarix_satr_COUNT][Terminal_kiritish->ustun_holat-1]=' ';그리기(Terminal_kiritish->ROW_holat,Terminal_kiritish->ustun_holat-1);}
    if(넓은글자(Terminal_kiritish->글자칸들[Terminal_kiritish->ROW_holat%tarix_satr_COUNT][Terminal_kiritish->ustun_holat])==2&&Terminal_kiritish->ustun_holat+1<Terminal_kiritish->COLUMNS){Terminal_kiritish->글자칸들[Terminal_kiritish->ROW_holat%tarix_satr_COUNT][Terminal_kiritish->ustun_holat+1]=' ';그리기(Terminal_kiritish->ROW_holat,Terminal_kiritish->ustun_holat+1);}
    Terminal_kiritish->글자칸들[Terminal_kiritish->ROW_holat%tarix_satr_COUNT][Terminal_kiritish->ustun_holat]=belgi_kodi;Terminal_kiritish->모양들[Terminal_kiritish->ROW_holat%tarix_satr_COUNT][Terminal_kiritish->ustun_holat]=Terminal_kiritish->전경색|(Terminal_kiritish->배경색<<4);
    if(너비값==2)Terminal_kiritish->글자칸들[Terminal_kiritish->ROW_holat%tarix_satr_COUNT][Terminal_kiritish->ustun_holat+1]=0xffffffffu;
    그리기(Terminal_kiritish->ROW_holat,Terminal_kiritish->ustun_holat);Terminal_kiritish->ustun_holat+=너비값;
}
static void deskriptor_boshqaruv_SEQUENCE(unsigned belgi_kodi){
    unsigned element_COUNT=Terminal_kiritish->매개값[0]?Terminal_kiritish->매개값[0]:1;
    if(belgi_kodi=='m')for(unsigned 순번=0;순번<=Terminal_kiritish->매개색인;순번++){unsigned ma_lumotlar_holat=Terminal_kiritish->매개값[순번];if(!ma_lumotlar_holat){Terminal_kiritish->전경색=7;Terminal_kiritish->배경색=0;}if(ma_lumotlar_holat==1&&Terminal_kiritish->전경색<8)Terminal_kiritish->전경색+=8;if(ma_lumotlar_holat==7){unsigned 유지=Terminal_kiritish->전경색;Terminal_kiritish->전경색=Terminal_kiritish->배경색;Terminal_kiritish->배경색=유지;}if(ma_lumotlar_holat>=30&&ma_lumotlar_holat<=37)Terminal_kiritish->전경색=ma_lumotlar_holat-30;if(ma_lumotlar_holat>=90&&ma_lumotlar_holat<=97)Terminal_kiritish->전경색=ma_lumotlar_holat-90+8;if(ma_lumotlar_holat>=40&&ma_lumotlar_holat<=47)Terminal_kiritish->배경색=ma_lumotlar_holat-40;if(ma_lumotlar_holat>=100&&ma_lumotlar_holat<=107)Terminal_kiritish->배경색=ma_lumotlar_holat-100+8;if(ma_lumotlar_holat==39)Terminal_kiritish->전경색=7;if(ma_lumotlar_holat==49)Terminal_kiritish->배경색=0;}
    if(belgi_kodi=='J'&&(Terminal_kiritish->매개값[0]==2||Terminal_kiritish->매개값[0]==3))tozalamoq_TOC();
    if(belgi_kodi=='K'){unsigned 출발위치=Terminal_kiritish->매개값[0]==2?0:Terminal_kiritish->ustun_holat,도착위치=Terminal_kiritish->매개값[0]==1?Terminal_kiritish->ustun_holat+1:Terminal_kiritish->COLUMNS;if(Terminal_kiritish->매개값[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_kiritish->COLUMNS;순번++){
        unsigned ROW_VALUE=Terminal_kiritish->ROW_holat%tarix_satr_COUNT,belgi_VALUE=Terminal_kiritish->글자칸들[ROW_VALUE][순번],shakl_VALUE=Terminal_kiritish->전경색|(Terminal_kiritish->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 shrift_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(belgi_VALUE!=0&&belgi_VALUE!=' ')||Terminal_kiritish->모양들[ROW_VALUE][순번]!=shakl_VALUE;
        Terminal_kiritish->글자칸들[ROW_VALUE][순번]=' ';Terminal_kiritish->모양들[ROW_VALUE][순번]=shakl_VALUE;
        if(바뀜)그리기(Terminal_kiritish->ROW_holat,순번);
    }}
    if(belgi_kodi=='D')Terminal_kiritish->ustun_holat=element_COUNT>Terminal_kiritish->ustun_holat?0:Terminal_kiritish->ustun_holat-element_COUNT;if(belgi_kodi=='C')Terminal_kiritish->ustun_holat=Terminal_kiritish->ustun_holat+element_COUNT>=Terminal_kiritish->COLUMNS?Terminal_kiritish->COLUMNS-1:Terminal_kiritish->ustun_holat+element_COUNT;
    if(belgi_kodi=='G')Terminal_kiritish->ustun_holat=element_COUNT>Terminal_kiritish->COLUMNS?Terminal_kiritish->COLUMNS-1:element_COUNT-1;if(belgi_kodi=='A')Terminal_kiritish->ROW_holat=element_COUNT>Terminal_kiritish->ROW_holat-Terminal_kiritish->맨위?Terminal_kiritish->맨위:Terminal_kiritish->ROW_holat-element_COUNT;
    if(belgi_kodi=='B')Terminal_kiritish->ROW_holat=Terminal_kiritish->ROW_holat+element_COUNT>=Terminal_kiritish->맨위+Terminal_kiritish->ROW_COUNT?Terminal_kiritish->맨위+Terminal_kiritish->ROW_COUNT-1:Terminal_kiritish->ROW_holat+element_COUNT;
    if(belgi_kodi=='H'||belgi_kodi=='f'){Terminal_kiritish->ROW_holat=Terminal_kiritish->맨위+(element_COUNT>Terminal_kiritish->ROW_COUNT?Terminal_kiritish->ROW_COUNT:element_COUNT)-1;unsigned x_koordinata=Terminal_kiritish->매개값[1]?Terminal_kiritish->매개값[1]:1;Terminal_kiritish->ustun_holat=(x_koordinata>Terminal_kiritish->COLUMNS?Terminal_kiritish->COLUMNS:x_koordinata)-1;}
    if(belgi_kodi=='s'){Terminal_kiritish->저장행=Terminal_kiritish->ROW_holat;Terminal_kiritish->저장열=Terminal_kiritish->ustun_holat;}if(belgi_kodi=='u'){Terminal_kiritish->ROW_holat=Terminal_kiritish->저장행;Terminal_kiritish->ustun_holat=Terminal_kiritish->저장열<Terminal_kiritish->COLUMNS?Terminal_kiritish->저장열:Terminal_kiritish->COLUMNS-1;}
    if((belgi_kodi=='h'||belgi_kodi=='l')&&Terminal_kiritish->매개값[0]==25)Terminal_kiritish->가리개보임=belgi_kodi=='h';
}
void Terminal_bayt(unsigned SECOND_VALUE){
    Terminal_kiritish=&Windows_Ro_yxat[출력결과];if(!Terminal_kiritish->살아있음)return;qo_shib_qo_yish_belgisi_VALUE(0);if(Terminal_kiritish->aylantirmoq){Terminal_kiritish->aylantirmoq=0;if(보이는지())tarkib_VALUE();}
    if(Terminal_kiritish->탈출상태==1){Terminal_kiritish->탈출상태=SECOND_VALUE=='['?2:0;Terminal_kiritish->매개색인=0;for(unsigned 순번=0;순번<4;순번++)Terminal_kiritish->매개값[순번]=0;}
    else if(Terminal_kiritish->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminal_kiritish->매개값[Terminal_kiritish->매개색인]<10000)Terminal_kiritish->매개값[Terminal_kiritish->매개색인]=Terminal_kiritish->매개값[Terminal_kiritish->매개색인]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminal_kiritish->매개색인<3)Terminal_kiritish->매개색인++;else{deskriptor_boshqaruv_SEQUENCE(SECOND_VALUE);Terminal_kiritish->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminal_kiritish->긴부호없는값=0;Terminal_kiritish->탈출상태=1;}else{
        if(Terminal_kiritish->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminal_kiritish->긴부호없는값=0;belgi_kodi_451f2815(0xfffd);}
        if(Terminal_kiritish->긴부호없는값){Terminal_kiritish->부호없는결과=Terminal_kiritish->부호없는결과*64+(SECOND_VALUE&63);if(--Terminal_kiritish->긴부호없는값==0)belgi_kodi_451f2815(Terminal_kiritish->부호없는결과<Terminal_kiritish->SMALL_VALUE||Terminal_kiritish->부호없는결과>0x10ffff||(Terminal_kiritish->부호없는결과>=0xd800&&Terminal_kiritish->부호없는결과<=0xdfff)?0xfffd:Terminal_kiritish->부호없는결과);}
        else if(SECOND_VALUE<128)belgi_kodi_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminal_kiritish->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminal_kiritish->부호없는결과=SECOND_VALUE&((1u<<(6-Terminal_kiritish->긴부호없는값))-1);Terminal_kiritish->SMALL_VALUE=Terminal_kiritish->긴부호없는값==1?128:Terminal_kiritish->긴부호없는값==2?2048:65536;}else belgi_kodi_451f2815(0xfffd);
    }qo_shib_qo_yish_belgisi_VALUE(1);
}
int 터미널대기(void){return 대기중!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int o_lchamni_o_zgartirmoq_tortib_o_tkazmoq=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Vertikal_holat) {
    for(int SEQUENCE_VALUE=kiritish_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int identifikator_VALUE=tartib_VALUE[SEQUENCE_VALUE];Terminal_d413d4bc *oyna=&Windows_Ro_yxat[identifikator_VALUE];
        if(가로>=(int)oyna->x_koordinata&&Vertikal_holat>=(int)oyna->Y_tugmasi_koordinat&&
           가로<(int)(oyna->x_koordinata+oyna->너비)&&Vertikal_holat<(int)(oyna->Y_tugmasi_koordinat+oyna->높이))return identifikator_VALUE;
    }return -1;
}
static int 모서리찾기(int identifikator_VALUE,int 가로,int Vertikal_holat) {
    if(identifikator_VALUE<0)return 0;Terminal_d413d4bc *oyna=&Windows_Ro_yxat[identifikator_VALUE];
    int 왼쪽=가로<(int)oyna->x_koordinata+8,RIGHT=가로>=(int)(oyna->x_koordinata+oyna->너비)-8;
    int 위쪽=Vertikal_holat<(int)oyna->Y_tugmasi_koordinat+8,아래쪽=Vertikal_holat>=(int)(oyna->Y_tugmasi_koordinat+oyna->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int ajratgich_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void ko_chirmoq_o_lchamni_o_zgartirmoq(int 가로,int Vertikal_holat) {
    Terminal_d413d4bc *oyna=&Windows_Ro_yxat[o_lchamni_o_zgartirmoq_tortib_o_tkazmoq];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=ajratgich_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=ajratgich_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=ajratgich_VALUE(처음세로+Vertikal_holat-잡은세로,34,아래쪽-216);
    else 아래쪽=ajratgich_VALUE(처음세로+처음높이+Vertikal_holat-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(oyna->COLUMNS!=COLUMNS||oyna->ROW_COUNT!=ROW_COUNT){
        oyna->크기바뀜=1;oyna->COLUMNS=COLUMNS;oyna->ROW_COUNT=ROW_COUNT;
        if(oyna->ustun_holat>=COLUMNS)oyna->ustun_holat=COLUMNS-1;
        if(oyna->ROW_holat>=oyna->맨위+ROW_COUNT)oyna->맨위=oyna->ROW_holat-ROW_COUNT+1;
        unsigned 한도=oyna->맨위;if(한도>tarix_satr_COUNT-ROW_COUNT)한도=tarix_satr_COUNT-ROW_COUNT;
        if(oyna->aylantirmoq>한도)oyna->aylantirmoq=한도;
    }
    int 옛가로=oyna->x_koordinata,옛세로=oyna->Y_tugmasi_koordinat,옛폭=oyna->너비,옛길이=oyna->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    oyna->x_koordinata=왼쪽;oyna->Y_tugmasi_koordinat=위쪽;oyna->너비=RIGHT-왼쪽;oyna->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,oyna);
}
void Terminal_kursor(unsigned Keyingi_element,int x_koordinata,int Y_tugmasi_koordinat){
    unsigned 눌림=Keyingi_element&~단추들;단추들=Keyingi_element;
    if(!ishchi_stol_ko_rinish){tortib_o_tkazmoq_VALUE=-1;o_lchamni_o_zgartirmoq_tortib_o_tkazmoq=-1;yozuv_taxtasi_kursor(x_koordinata,Y_tugmasi_koordinat,1);return;}
    if(!(Keyingi_element&1)){tortib_o_tkazmoq_VALUE=-1;o_lchamni_o_zgartirmoq_tortib_o_tkazmoq=-1;}
    if(o_lchamni_o_zgartirmoq_tortib_o_tkazmoq>=0&&!Windows_Ro_yxat[o_lchamni_o_zgartirmoq_tortib_o_tkazmoq].살아있음)o_lchamni_o_zgartirmoq_tortib_o_tkazmoq=-1;
    if(tortib_o_tkazmoq_VALUE>=0&&!Windows_Ro_yxat[tortib_o_tkazmoq_VALUE].살아있음)tortib_o_tkazmoq_VALUE=-1;
    if(o_lchamni_o_zgartirmoq_tortib_o_tkazmoq>=0){
        ko_chirmoq_o_lchamni_o_zgartirmoq(x_koordinata,Y_tugmasi_koordinat);yozuv_taxtasi_kursor(x_koordinata,Y_tugmasi_koordinat,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    yozuv_taxtasi_kursor(x_koordinata,Y_tugmasi_koordinat,1);
    if(tortib_o_tkazmoq_VALUE>=0){
        Terminal_d413d4bc *oyna=&Windows_Ro_yxat[tortib_o_tkazmoq_VALUE];
        int 옛가로=oyna->x_koordinata,옛세로=oyna->Y_tugmasi_koordinat;
        oyna->x_koordinata=ajratgich_VALUE(x_koordinata-tortib_o_tkazmoq_X_tugmasi,0,보드화면너비()-oyna->너비);
        oyna->Y_tugmasi_koordinat=ajratgich_VALUE(Y_tugmasi_koordinat-tortib_o_tkazmoq_Y_tugmasi,34,보드화면높이()-oyna->높이);
        if(옛가로!=(int)oyna->x_koordinata||옛세로!=(int)oyna->Y_tugmasi_koordinat)창자리그리기(옛가로,옛세로,oyna->너비,oyna->높이,oyna);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokus,x_koordinata,Y_tugmasi_koordinat)){화면가리킴(Fokus,눌림,x_koordinata,Y_tugmasi_koordinat);return;}
    int identifikator_VALUE=가리킨창(x_koordinata,Y_tugmasi_koordinat),모서리=모서리찾기(identifikator_VALUE,x_koordinata,Y_tugmasi_koordinat);
    if(모서리)yozuv_taxtasi_kursor(x_koordinata,Y_tugmasi_koordinat,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal_d413d4bc *oyna=&Windows_Ro_yxat[identifikator_VALUE];o_lchamni_o_zgartirmoq_tortib_o_tkazmoq=identifikator_VALUE;잡은모서리=모서리;잡은가로=x_koordinata;잡은세로=Y_tugmasi_koordinat;
            처음가로=oyna->x_koordinata;처음세로=oyna->Y_tugmasi_koordinat;처음너비=oyna->너비;처음높이=oyna->높이;
            if(identifikator_VALUE!=Fokus)앞으로올리기(identifikator_VALUE);return;
        }
        if(Y_tugmasi_koordinat<32&&x_koordinata>=6&&x_koordinata<142){Yaratish_kiritish();return;}
        if(Y_tugmasi_koordinat<32&&x_koordinata>=154&&x_koordinata<602){앞으로올리기((x_koordinata-154)/112);return;}
        if(identifikator_VALUE>=0){
            Terminal_d413d4bc *oyna=&Windows_Ro_yxat[identifikator_VALUE];
            if(Y_tugmasi_koordinat<(int)oyna->Y_tugmasi_koordinat+30&&x_koordinata>=(int)(oyna->x_koordinata+oyna->너비)-32){yopmoq_oyna(identifikator_VALUE);return;}
            if(identifikator_VALUE!=Fokus)앞으로올리기(identifikator_VALUE);
            if(Y_tugmasi_koordinat<(int)oyna->Y_tugmasi_koordinat+30){tortib_o_tkazmoq_VALUE=identifikator_VALUE;tortib_o_tkazmoq_X_tugmasi=x_koordinata-oyna->x_koordinata;tortib_o_tkazmoq_Y_tugmasi=Y_tugmasi_koordinat-oyna->Y_tugmasi_koordinat;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){Terminal_kiritish=&Windows_Ro_yxat[Fokus];if(눌림&8){unsigned 한도=Terminal_kiritish->맨위;if(한도>tarix_satr_COUNT-Terminal_kiritish->ROW_COUNT)한도=tarix_satr_COUNT-Terminal_kiritish->ROW_COUNT;Terminal_kiritish->aylantirmoq=Terminal_kiritish->aylantirmoq+9>한도?한도:Terminal_kiritish->aylantirmoq+9;}else Terminal_kiritish->aylantirmoq=Terminal_kiritish->aylantirmoq<9?0:Terminal_kiritish->aylantirmoq-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Yaratish_kiritish();if(누름값==2&&kiritish_COUNT)앞으로올리기(tartib_VALUE[0]);if(누름값==3)yopmoq_oyna(Fokus);}
기계낱말 yozuv_taxtasi_Terminal(기계낱말 Amal){
    if(Amal==300){if(!Windows_Ro_yxat[출력결과].살아있음)return Yaratish_kiritish();ishchi_stol_ko_rinish=1;다시그리기();return 0;}
    if(Amal==0){yopmoq_oyna(Fokus);return 0;}if(Amal==1)return (uint32_t)Yaratish_kiritish();if(Amal==2)return Fokus>=0;
    if(Amal==9){ishchi_stol_ko_rinish=0;return 0;}if(Amal==7)return kiritish_COUNT;if(Amal==10)return Fokus+1;if(Amal==11)return 출력결과;
    if(Amal==13){Terminal_d413d4bc *oyna=&Windows_Ro_yxat[출력결과];return oyna->살아있음?(oyna->ROW_COUNT<<16)|oyna->COLUMNS:(19<<16)|68;}
    if(Amal==14){unsigned VALUE=Windows_Ro_yxat[출력결과].크기바뀜;Windows_Ro_yxat[출력결과].크기바뀜=0;return VALUE;}
    if(Amal==12){unsigned VALUE=대기중;대기중=0;return VALUE;}
    if(Amal>=20&&Amal<24)return Windows_Ro_yxat[Amal-20].살아있음;
    if(Amal>=100&&Amal<104){출력결과=Amal-100;Terminal_kiritish=&Windows_Ro_yxat[출력결과];return 0;}
    if(Amal>=200&&Amal<204){앞으로올리기(Amal-200);return 0;}
    if(Amal==3){다시그리기();return 0;}Terminal_kiritish=&Windows_Ro_yxat[출력결과];if(!Terminal_kiritish->살아있음)return 0;
    if(Amal==4)tozalamoq_TOC();if(Amal==5||Amal==6){unsigned 이전=단추들;Terminal_kursor(Amal==5?8:16,0,0);단추들=이전;}return 1;
}
