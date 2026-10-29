#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* oma 네 Ikkuna 합성과 UTF-8 komentotulkki. 바뀐 영역의 valmis_ARVO 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t kone_Word;
extern kone_Word Taulu_kuvapiste(kone_Word,kone_Word,kone_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Pääte_fontti[];
#define 최대열수 237
#define Historia_rivi_LASKE 160
typedef struct {
    uint32_t 글자칸들[Historia_rivi_LASKE][최대열수]; uint8_t 모양들[Historia_rivi_LASKE][최대열수];
    unsigned 너비,높이,SARAKKEET,RIVI_LASKE,크기바뀜;
    unsigned 살아있음,x_koordinaatti,Y_koordinaatti,RIVI_toimi,SARAKE_toimi,맨위,vierittää,전경색,배경색,탈출상태,parametri_ARVO[4],parametri_INDEKSI,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,PIENI_ARVO,대체화면,가리개보임;
} Pääte;
static Pääte Windows_luettelo[4];
static int Aihe=-1,tulos,tilata_ARVO[4],merkintä_LASKE,vetää_ARVO=-1,vetää_X,vetää_Y;
static unsigned tietojärjestelmät_Odottaa,단추들,työpöytä_Näkymä,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Pääte *Pääte_merkintä;
static unsigned leveä_merkki(unsigned merkkikoodi){return merkkikoodi>=256?2:1;}
static void 사각영역(unsigned x_koordinaatti,unsigned Y_koordinaatti,unsigned 너비값,unsigned 높이값,unsigned 색상){
    Taulu_suorakulmio_täyttö(x_koordinaatti,Y_koordinaatti,너비값,높이값,색상);
}
void Pääte_merkki(unsigned x_koordinaatti,unsigned Y_koordinaatti,unsigned merkkikoodi,unsigned 전경색,unsigned 배경색){
    unsigned 너비=leveä_merkki(merkkikoodi)*8;if(merkkikoodi==0xffffffffu)return;
    int 왼쪽=x_koordinaatti,위쪽=Y_koordinaatti,폭=너비,kesto_ARVO=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&kesto_ARVO))return;
    if(merkkikoodi==' '){Taulu_suorakulmio_täyttö(왼쪽,위쪽,폭,kesto_ARVO,배경색);return;}
    unsigned HAKU_INDEKSI=merkkikoodi<65536?merkkikoodi:merkkikoodi>=0x1f600&&merkkikoodi<0x1f650?65536+merkkikoodi-0x1f600:0xfffd;
    const unsigned char *fontti_ARVO=Pääte_fontti+HAKU_INDEKSI*32;
    for(int syöterivi=위쪽;syöterivi<위쪽+kesto_ARVO;syöterivi++){unsigned Background_Intelligent_Transfer_Service_luettelo=fontti_ARVO[(syöterivi-Y_koordinaatti)*2]*256+fontti_ARVO[(syöterivi-Y_koordinaatti)*2+1];for(int paikka_merkintä=왼쪽;paikka_merkintä<왼쪽+폭;paikka_merkintä++)Taulu_kuvapiste(paikka_merkintä,syöterivi,(Background_Intelligent_Transfer_Service_luettelo&(0x8000>>(paikka_merkintä-x_koordinaatti)))?전경색:배경색);}
}
static void nimi_taulukko(unsigned x_koordinaatti,unsigned Y_koordinaatti,const char *merkkijono_data,unsigned 전경색,unsigned 배경색){while(*merkkijono_data){unsigned merkkikoodi=(unsigned char)*merkkijono_data++, 남은수=0;if(merkkikoodi>=0xc0){남은수=merkkikoodi<0xe0?1:merkkikoodi<0xf0?2:3;merkkikoodi&=(1u<<(6-남은수))-1;while(남은수--&&*merkkijono_data)merkkikoodi=(merkkikoodi<<6)|((unsigned char)*merkkijono_data++&63);}Pääte_merkki(x_koordinaatti,Y_koordinaatti,merkkikoodi,전경색,배경색);x_koordinaatti+=leveä_merkki(merkkikoodi)*8;}}
static unsigned 첫항목(void){return Pääte_merkintä->맨위;}
static int 보이는지(void){return Pääte_merkintä->살아있음&&Aihe>=0&&Pääte_merkintä==&Windows_luettelo[Aihe]&&!화면보임(Aihe);}
static void 그리기(unsigned RIVI_toimi,unsigned SARAKE_toimi){
    if(!보이는지()||RIVI_toimi<첫항목()-Pääte_merkintä->vierittää||RIVI_toimi>=첫항목()-Pääte_merkintä->vierittää+Pääte_merkintä->RIVI_LASKE||SARAKE_toimi>=Pääte_merkintä->SARAKKEET)return;
    unsigned merkkikoodi=Pääte_merkintä->글자칸들[RIVI_toimi%Historia_rivi_LASKE][SARAKE_toimi],merkkijono_data=Pääte_merkintä->모양들[RIVI_toimi%Historia_rivi_LASKE][SARAKE_toimi];
    if(leveä_merkki(merkkikoodi)==2&&SARAKE_toimi+1>=Pääte_merkintä->SARAKKEET)merkkikoodi=' ';
    Pääte_merkki(Pääte_merkintä->x_koordinaatti+12+SARAKE_toimi*8,Pääte_merkintä->Y_koordinaatti+36+(RIVI_toimi-첫항목()+Pääte_merkintä->vierittää)*16,merkkikoodi?merkkikoodi:' ',색상들[merkkijono_data&15],색상들[merkkijono_data>>4]);
}
static void sirkumfleksi_ARVO(int näyttää_ikkuna){if(!보이는지()||Pääte_merkintä->vierittää||Pääte_merkintä->SARAKE_toimi>=Pääte_merkintä->SARAKKEET||Pääte_merkintä->RIVI_toimi<Pääte_merkintä->맨위||Pääte_merkintä->RIVI_toimi>=Pääte_merkintä->맨위+Pääte_merkintä->RIVI_LASKE)return;
    if(!näyttää_ikkuna||!Pääte_merkintä->가리개보임)그리기(Pääte_merkintä->RIVI_toimi,Pääte_merkintä->SARAKE_toimi);else 사각영역(Pääte_merkintä->x_koordinaatti+12+Pääte_merkintä->SARAKE_toimi*8,Pääte_merkintä->Y_koordinaatti+36+(Pääte_merkintä->RIVI_toimi-Pääte_merkintä->맨위)*16+14,8,2,색상들[Pääte_merkintä->전경색]);}
static void Sisältö_ARVO(void){
    사각영역(Pääte_merkintä->x_koordinaatti+12,Pääte_merkintä->Y_koordinaatti+36,Pääte_merkintä->SARAKKEET*8,Pääte_merkintä->RIVI_LASKE*16,색상들[0]);
    int 가로=Pääte_merkintä->x_koordinaatti+12,toimiala_toimi=Pääte_merkintä->Y_koordinaatti+36,폭=Pääte_merkintä->SARAKKEET*8,kesto_ARVO=Pääte_merkintä->RIVI_LASKE*16;
    if(보드그림범위(&가로,&toimiala_toimi,&폭,&kesto_ARVO)){
    unsigned 첫줄=(toimiala_toimi-Pääte_merkintä->Y_koordinaatti-36)/16,끝줄=(toimiala_toimi+kesto_ARVO-Pääte_merkintä->Y_koordinaatti-36+15)/16;
    unsigned 첫칸=(가로-Pääte_merkintä->x_koordinaatti-12)/8,끝칸=(가로+폭-Pääte_merkintä->x_koordinaatti-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 rajattu_alue_ARVO 왼쪽에서 시작한 두 paikka_merkintä 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned merkkikoodi=첫칸;merkkikoodi<끝칸;merkkikoodi++){
        unsigned RIVI_toimi=첫항목()-Pääte_merkintä->vierittää+반환값,merkki_ARVO=Pääte_merkintä->글자칸들[RIVI_toimi%Historia_rivi_LASKE][merkkikoodi],merkkijono_data=Pääte_merkintä->모양들[RIVI_toimi%Historia_rivi_LASKE][merkkikoodi];
        if(leveä_merkki(merkki_ARVO)==2&&merkkikoodi+1>=Pääte_merkintä->SARAKKEET)merkki_ARVO=' ';
        if((merkki_ARVO==0||merkki_ARVO==' ')&&(merkkijono_data>>4)==0)continue;
        Pääte_merkki(Pääte_merkintä->x_koordinaatti+12+merkkikoodi*8,Pääte_merkintä->Y_koordinaatti+36+반환값*16,merkki_ARVO?merkki_ARVO:' ',색상들[merkkijono_data&15],색상들[merkkijono_data>>4]);
    }}
    nimi_taulukko(Pääte_merkintä->x_koordinaatti+12,Pääte_merkintä->Y_koordinaatti+Pääte_merkintä->높이-18,Pääte_merkintä->vierittää?"PgDn: recent output":Pääte_merkintä->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);sirkumfleksi_ARVO(1);
}
static void suoritus_kuva(int tunniste_ARVO){
    Pääte_merkintä=&Windows_luettelo[tunniste_ARVO];
    int 가로=Pääte_merkintä->x_koordinaatti,toimiala_toimi=Pääte_merkintä->Y_koordinaatti,폭=Pääte_merkintä->너비,kesto_ARVO=Pääte_merkintä->높이;
    if(!보드그림범위(&가로,&toimiala_toimi,&폭,&kesto_ARVO))return;
    사각영역(Pääte_merkintä->x_koordinaatti,Pääte_merkintä->Y_koordinaatti,Pääte_merkintä->너비,Pääte_merkintä->높이,0x403127);
    unsigned 색상=tunniste_ARVO==Aihe?0x905020:0x604438;사각영역(Pääte_merkintä->x_koordinaatti,Pääte_merkintä->Y_koordinaatti,Pääte_merkintä->너비,30,색상);
    nimi_taulukko(Pääte_merkintä->x_koordinaatti+12,Pääte_merkintä->Y_koordinaatti+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+tunniste_ARVO),0};nimi_taulukko(Pääte_merkintä->x_koordinaatti+148,Pääte_merkintä->Y_koordinaatti+7,수치,0xffffff,색상);
    nimi_taulukko(Pääte_merkintä->x_koordinaatti+240,Pääte_merkintä->Y_koordinaatti+7,Pääte_merkintä->너비>=500?(한글입력?"[FI] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[FI]":"[EN]"),0xffffff,색상);
    사각영역(Pääte_merkintä->x_koordinaatti+Pääte_merkintä->너비-32,Pääte_merkintä->Y_koordinaatti+4,26,22,0x5555b8);nimi_taulukko(Pääte_merkintä->x_koordinaatti+Pääte_merkintä->너비-24,Pääte_merkintä->Y_koordinaatti+7,"X",0xffffff,0x5555b8);
    Sisältö_ARVO();
}
static void Piirrä_taustanäkymä(void){
    if(!työpöytä_Näkymä)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);nimi_taulukko(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_luettelo[순번].살아있음){unsigned merkkikoodi=Aihe==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,merkkikoodi);nimi_taulukko(160+순번*112,8,"Terminal",0xffffff,merkkikoodi);char merkkijono_data[2]={(char)('1'+순번),0};nimi_taulukko(232+순번*112,8,merkkijono_data,0xffffff,merkkikoodi);}
    if(!merkintä_LASKE)nimi_taulukko(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<merkintä_LASKE;순번++)suoritus_kuva(tilata_ARVO[순번]);화면다시그림(Aihe);Pääte_merkintä=&Windows_luettelo[tulos];
}
static void Paint_alue(int 가로,int toimiala_toimi,int 폭,int kesto_ARVO){
    if(!työpöytä_Näkymä||!보드그림범위(&가로,&toimiala_toimi,&폭,&kesto_ARVO))return;
    for(int syöterivi=toimiala_toimi;syöterivi<toimiala_toimi+kesto_ARVO;syöterivi+=32){
        int 띠높이=toimiala_toimi+kesto_ARVO-syöterivi;if(띠높이>32)띠높이=32;
        if(Taulu_alku_piirustus(가로,syöterivi,폭,띠높이)){Piirrä_taustanäkymä();Taulu_loppu_piirustus();}
    }
}
static void 다시그리기(void){Paint_alue(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Ikkuna 영역과 Edellinen_kohde 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int toimiala_toimi,int 폭,int kesto_ARVO,Pääte *Ikkuna){
    int 왼쪽=가로>(int)Ikkuna->x_koordinaatti?가로:(int)Ikkuna->x_koordinaatti;
    int 위쪽=toimiala_toimi>(int)Ikkuna->Y_koordinaatti?toimiala_toimi:(int)Ikkuna->Y_koordinaatti;
    int OIKEA=가로+폭<(int)(Ikkuna->x_koordinaatti+Ikkuna->너비)?가로+폭:(int)(Ikkuna->x_koordinaatti+Ikkuna->너비);
    int 아래쪽=toimiala_toimi+kesto_ARVO<(int)(Ikkuna->Y_koordinaatti+Ikkuna->높이)?toimiala_toimi+kesto_ARVO:(int)(Ikkuna->Y_koordinaatti+Ikkuna->높이);
    Paint_alue(Ikkuna->x_koordinaatti,Ikkuna->Y_koordinaatti,Ikkuna->너비,Ikkuna->높이);
    if(왼쪽>=OIKEA||위쪽>=아래쪽){Paint_alue(가로,toimiala_toimi,폭,kesto_ARVO);return;}
    Paint_alue(가로,toimiala_toimi,폭,위쪽-toimiala_toimi);
    Paint_alue(가로,아래쪽,폭,toimiala_toimi+kesto_ARVO-아래쪽);
    Paint_alue(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Paint_alue(OIKEA,위쪽,가로+폭-OIKEA,아래쪽-위쪽);
}
static void ilmoitus_Aihe(void){tietojärjestelmät_Odottaa=(tietojärjestelmät_Odottaa&~15u)|(unsigned)(Aihe+1)|0x10000;}
void Pääte_syöte_tila(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Aihe>=0){
        Pääte *ikkuna_merkintä=&Windows_luettelo[Aihe];
        nimi_taulukko(ikkuna_merkintä->x_koordinaatti+240,ikkuna_merkintä->Y_koordinaatti+7,ikkuna_merkintä->너비>=500?(한글입력?"[FI] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[FI]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int tunniste_ARVO){if(tunniste_ARVO<0||tunniste_ARVO>=4||!Windows_luettelo[tunniste_ARVO].살아있음)return;int nykyinen_toimi=0;while(nykyinen_toimi<merkintä_LASKE&&tilata_ARVO[nykyinen_toimi]!=tunniste_ARVO)nykyinen_toimi++;for(;nykyinen_toimi+1<merkintä_LASKE;nykyinen_toimi++)tilata_ARVO[nykyinen_toimi]=tilata_ARVO[nykyinen_toimi+1];tilata_ARVO[merkintä_LASKE-1]=tunniste_ARVO;Aihe=tunniste_ARVO;ilmoitus_Aihe();다시그리기();}
static void 빈칸채우기(unsigned RIVI_toimi){for(unsigned merkkikoodi=0;merkkikoodi<최대열수;merkkikoodi++){Pääte_merkintä->글자칸들[RIVI_toimi%Historia_rivi_LASKE][merkkikoodi]=0;Pääte_merkintä->모양들[RIVI_toimi%Historia_rivi_LASKE][merkkikoodi]=Pääte_merkintä->전경색|(Pääte_merkintä->배경색<<4);}}
static void selvittää_Sisällys(void){Pääte_merkintä->RIVI_toimi=Pääte_merkintä->SARAKE_toimi=Pääte_merkintä->맨위=Pääte_merkintä->vierittää=0;for(unsigned 반환값=0;반환값<Historia_rivi_LASKE;반환값++)빈칸채우기(반환값);if(보이는지())Sisältö_ARVO();}
static int Luo_merkintä(void){
    if(!보드화면기억공간())return -19;int tunniste_ARVO=0;while(tunniste_ARVO<4&&Windows_luettelo[tunniste_ARVO].살아있음)tunniste_ARVO++;if(tunniste_ARVO==4)return -28;
    työpöytä_Näkymä=1;Pääte_merkintä=&Windows_luettelo[tunniste_ARVO];memset(Pääte_merkintä,0,sizeof(*Pääte_merkintä));Pääte_merkintä->살아있음=1;Pääte_merkintä->너비=568;Pääte_merkintä->높이=360;Pääte_merkintä->SARAKKEET=68;Pääte_merkintä->RIVI_LASKE=19;Pääte_merkintä->x_koordinaatti=12+tunniste_ARVO*16;Pääte_merkintä->Y_koordinaatti=48+tunniste_ARVO*18;Pääte_merkintä->전경색=7;Pääte_merkintä->가리개보임=1;
    for(unsigned 반환값=0;반환값<Historia_rivi_LASKE;반환값++)빈칸채우기(반환값);tilata_ARVO[merkintä_LASKE++]=tunniste_ARVO;Aihe=tunniste_ARVO;tietojärjestelmät_Odottaa|=1u<<(4+tunniste_ARVO);ilmoitus_Aihe();다시그리기();return tunniste_ARVO+1;
}
static void Sulje_ikkuna(int tunniste_ARVO){
    if(tunniste_ARVO<0||tunniste_ARVO>=4||!Windows_luettelo[tunniste_ARVO].살아있음)return;Windows_luettelo[tunniste_ARVO].살아있음=0;tietojärjestelmät_Odottaa|=1u<<(8+tunniste_ARVO);
    int nykyinen_toimi=0;while(nykyinen_toimi<merkintä_LASKE&&tilata_ARVO[nykyinen_toimi]!=tunniste_ARVO)nykyinen_toimi++;for(;nykyinen_toimi+1<merkintä_LASKE;nykyinen_toimi++)tilata_ARVO[nykyinen_toimi]=tilata_ARVO[nykyinen_toimi+1];merkintä_LASKE--;
    if(Aihe==tunniste_ARVO)Aihe=merkintä_LASKE?tilata_ARVO[merkintä_LASKE-1]:-1;ilmoitus_Aihe();다시그리기();
}
static void 줄바꿈(void){Pääte_merkintä->SARAKE_toimi=0;Pääte_merkintä->RIVI_toimi++;if(Pääte_merkintä->RIVI_toimi>=Pääte_merkintä->맨위+Pääte_merkintä->RIVI_LASKE){Pääte_merkintä->맨위++;빈칸채우기(Pääte_merkintä->RIVI_toimi);if(보이는지())Sisältö_ARVO();}}
static void koodipiste(unsigned merkkikoodi){
    if(merkkikoodi==13){Pääte_merkintä->SARAKE_toimi=0;return;}if(merkkikoodi==10){줄바꿈();return;}if(merkkikoodi==8){if(Pääte_merkintä->SARAKE_toimi)Pääte_merkintä->SARAKE_toimi--;return;}
    if(merkkikoodi==9){unsigned kohde_LASKE=8-Pääte_merkintä->SARAKE_toimi%8;while(kohde_LASKE--)koodipiste(' ');return;}if(merkkikoodi<32||merkkikoodi==127)return;
    unsigned 너비값=leveä_merkki(merkkikoodi);if(Pääte_merkintä->SARAKE_toimi+너비값>Pääte_merkintä->SARAKKEET)줄바꿈();
    if(Pääte_merkintä->글자칸들[Pääte_merkintä->RIVI_toimi%Historia_rivi_LASKE][Pääte_merkintä->SARAKE_toimi]==0xffffffffu&&Pääte_merkintä->SARAKE_toimi){Pääte_merkintä->글자칸들[Pääte_merkintä->RIVI_toimi%Historia_rivi_LASKE][Pääte_merkintä->SARAKE_toimi-1]=' ';그리기(Pääte_merkintä->RIVI_toimi,Pääte_merkintä->SARAKE_toimi-1);}
    if(leveä_merkki(Pääte_merkintä->글자칸들[Pääte_merkintä->RIVI_toimi%Historia_rivi_LASKE][Pääte_merkintä->SARAKE_toimi])==2&&Pääte_merkintä->SARAKE_toimi+1<Pääte_merkintä->SARAKKEET){Pääte_merkintä->글자칸들[Pääte_merkintä->RIVI_toimi%Historia_rivi_LASKE][Pääte_merkintä->SARAKE_toimi+1]=' ';그리기(Pääte_merkintä->RIVI_toimi,Pääte_merkintä->SARAKE_toimi+1);}
    Pääte_merkintä->글자칸들[Pääte_merkintä->RIVI_toimi%Historia_rivi_LASKE][Pääte_merkintä->SARAKE_toimi]=merkkikoodi;Pääte_merkintä->모양들[Pääte_merkintä->RIVI_toimi%Historia_rivi_LASKE][Pääte_merkintä->SARAKE_toimi]=Pääte_merkintä->전경색|(Pääte_merkintä->배경색<<4);
    if(너비값==2)Pääte_merkintä->글자칸들[Pääte_merkintä->RIVI_toimi%Historia_rivi_LASKE][Pääte_merkintä->SARAKE_toimi+1]=0xffffffffu;
    그리기(Pääte_merkintä->RIVI_toimi,Pääte_merkintä->SARAKE_toimi);Pääte_merkintä->SARAKE_toimi+=너비값;
}
static void kahva_ohjain_JONO(unsigned merkkikoodi){
    unsigned kohde_LASKE=Pääte_merkintä->parametri_ARVO[0]?Pääte_merkintä->parametri_ARVO[0]:1;
    if(merkkikoodi=='m')for(unsigned 순번=0;순번<=Pääte_merkintä->parametri_INDEKSI;순번++){unsigned data_toimi=Pääte_merkintä->parametri_ARVO[순번];if(!data_toimi){Pääte_merkintä->전경색=7;Pääte_merkintä->배경색=0;}if(data_toimi==1&&Pääte_merkintä->전경색<8)Pääte_merkintä->전경색+=8;if(data_toimi==7){unsigned 유지=Pääte_merkintä->전경색;Pääte_merkintä->전경색=Pääte_merkintä->배경색;Pääte_merkintä->배경색=유지;}if(data_toimi>=30&&data_toimi<=37)Pääte_merkintä->전경색=data_toimi-30;if(data_toimi>=90&&data_toimi<=97)Pääte_merkintä->전경색=data_toimi-90+8;if(data_toimi>=40&&data_toimi<=47)Pääte_merkintä->배경색=data_toimi-40;if(data_toimi>=100&&data_toimi<=107)Pääte_merkintä->배경색=data_toimi-100+8;if(data_toimi==39)Pääte_merkintä->전경색=7;if(data_toimi==49)Pääte_merkintä->배경색=0;}
    if(merkkikoodi=='J'&&(Pääte_merkintä->parametri_ARVO[0]==2||Pääte_merkintä->parametri_ARVO[0]==3))selvittää_Sisällys();
    if(merkkikoodi=='K'){unsigned 출발위치=Pääte_merkintä->parametri_ARVO[0]==2?0:Pääte_merkintä->SARAKE_toimi,도착위치=Pääte_merkintä->parametri_ARVO[0]==1?Pääte_merkintä->SARAKE_toimi+1:Pääte_merkintä->SARAKKEET;if(Pääte_merkintä->parametri_ARVO[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Pääte_merkintä->SARAKKEET;순번++){
        unsigned RIVI_ARVO=Pääte_merkintä->RIVI_toimi%Historia_rivi_LASKE,merkki_ARVO=Pääte_merkintä->글자칸들[RIVI_ARVO][순번],muoto_ARVO_f1cd655a=Pääte_merkintä->전경색|(Pääte_merkintä->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 fontti_ARVO 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(merkki_ARVO!=0&&merkki_ARVO!=' ')||Pääte_merkintä->모양들[RIVI_ARVO][순번]!=muoto_ARVO_f1cd655a;
        Pääte_merkintä->글자칸들[RIVI_ARVO][순번]=' ';Pääte_merkintä->모양들[RIVI_ARVO][순번]=muoto_ARVO_f1cd655a;
        if(바뀜)그리기(Pääte_merkintä->RIVI_toimi,순번);
    }}
    if(merkkikoodi=='D')Pääte_merkintä->SARAKE_toimi=kohde_LASKE>Pääte_merkintä->SARAKE_toimi?0:Pääte_merkintä->SARAKE_toimi-kohde_LASKE;if(merkkikoodi=='C')Pääte_merkintä->SARAKE_toimi=Pääte_merkintä->SARAKE_toimi+kohde_LASKE>=Pääte_merkintä->SARAKKEET?Pääte_merkintä->SARAKKEET-1:Pääte_merkintä->SARAKE_toimi+kohde_LASKE;
    if(merkkikoodi=='G')Pääte_merkintä->SARAKE_toimi=kohde_LASKE>Pääte_merkintä->SARAKKEET?Pääte_merkintä->SARAKKEET-1:kohde_LASKE-1;if(merkkikoodi=='A')Pääte_merkintä->RIVI_toimi=kohde_LASKE>Pääte_merkintä->RIVI_toimi-Pääte_merkintä->맨위?Pääte_merkintä->맨위:Pääte_merkintä->RIVI_toimi-kohde_LASKE;
    if(merkkikoodi=='B')Pääte_merkintä->RIVI_toimi=Pääte_merkintä->RIVI_toimi+kohde_LASKE>=Pääte_merkintä->맨위+Pääte_merkintä->RIVI_LASKE?Pääte_merkintä->맨위+Pääte_merkintä->RIVI_LASKE-1:Pääte_merkintä->RIVI_toimi+kohde_LASKE;
    if(merkkikoodi=='H'||merkkikoodi=='f'){Pääte_merkintä->RIVI_toimi=Pääte_merkintä->맨위+(kohde_LASKE>Pääte_merkintä->RIVI_LASKE?Pääte_merkintä->RIVI_LASKE:kohde_LASKE)-1;unsigned x_koordinaatti=Pääte_merkintä->parametri_ARVO[1]?Pääte_merkintä->parametri_ARVO[1]:1;Pääte_merkintä->SARAKE_toimi=(x_koordinaatti>Pääte_merkintä->SARAKKEET?Pääte_merkintä->SARAKKEET:x_koordinaatti)-1;}
    if(merkkikoodi=='s'){Pääte_merkintä->저장행=Pääte_merkintä->RIVI_toimi;Pääte_merkintä->저장열=Pääte_merkintä->SARAKE_toimi;}if(merkkikoodi=='u'){Pääte_merkintä->RIVI_toimi=Pääte_merkintä->저장행;Pääte_merkintä->SARAKE_toimi=Pääte_merkintä->저장열<Pääte_merkintä->SARAKKEET?Pääte_merkintä->저장열:Pääte_merkintä->SARAKKEET-1;}
    if((merkkikoodi=='h'||merkkikoodi=='l')&&Pääte_merkintä->parametri_ARVO[0]==25)Pääte_merkintä->가리개보임=merkkikoodi=='h';
}
void Pääte_tavu(unsigned SEKUNNIT_ARVO){
    Pääte_merkintä=&Windows_luettelo[tulos];if(!Pääte_merkintä->살아있음)return;sirkumfleksi_ARVO(0);if(Pääte_merkintä->vierittää){Pääte_merkintä->vierittää=0;if(보이는지())Sisältö_ARVO();}
    if(Pääte_merkintä->탈출상태==1){Pääte_merkintä->탈출상태=SEKUNNIT_ARVO=='['?2:0;Pääte_merkintä->parametri_INDEKSI=0;for(unsigned 순번=0;순번<4;순번++)Pääte_merkintä->parametri_ARVO[순번]=0;}
    else if(Pääte_merkintä->탈출상태==2){if(SEKUNNIT_ARVO=='?'){}else if(SEKUNNIT_ARVO>='0'&&SEKUNNIT_ARVO<='9'){if(Pääte_merkintä->parametri_ARVO[Pääte_merkintä->parametri_INDEKSI]<10000)Pääte_merkintä->parametri_ARVO[Pääte_merkintä->parametri_INDEKSI]=Pääte_merkintä->parametri_ARVO[Pääte_merkintä->parametri_INDEKSI]*10+SEKUNNIT_ARVO-'0';}else if(SEKUNNIT_ARVO==';'&&Pääte_merkintä->parametri_INDEKSI<3)Pääte_merkintä->parametri_INDEKSI++;else{kahva_ohjain_JONO(SEKUNNIT_ARVO);Pääte_merkintä->탈출상태=0;}}
    else if(SEKUNNIT_ARVO==27){Pääte_merkintä->긴부호없는값=0;Pääte_merkintä->탈출상태=1;}else{
        if(Pääte_merkintä->긴부호없는값&&(SEKUNNIT_ARVO&0xc0)!=0x80){Pääte_merkintä->긴부호없는값=0;koodipiste(0xfffd);}
        if(Pääte_merkintä->긴부호없는값){Pääte_merkintä->부호없는결과=Pääte_merkintä->부호없는결과*64+(SEKUNNIT_ARVO&63);if(--Pääte_merkintä->긴부호없는값==0)koodipiste(Pääte_merkintä->부호없는결과<Pääte_merkintä->PIENI_ARVO||Pääte_merkintä->부호없는결과>0x10ffff||(Pääte_merkintä->부호없는결과>=0xd800&&Pääte_merkintä->부호없는결과<=0xdfff)?0xfffd:Pääte_merkintä->부호없는결과);}
        else if(SEKUNNIT_ARVO<128)koodipiste(SEKUNNIT_ARVO);else if(SEKUNNIT_ARVO>=0xc2&&SEKUNNIT_ARVO<=0xf4){Pääte_merkintä->긴부호없는값=SEKUNNIT_ARVO<0xe0?1:SEKUNNIT_ARVO<0xf0?2:3;Pääte_merkintä->부호없는결과=SEKUNNIT_ARVO&((1u<<(6-Pääte_merkintä->긴부호없는값))-1);Pääte_merkintä->PIENI_ARVO=Pääte_merkintä->긴부호없는값==1?128:Pääte_merkintä->긴부호없는값==2?2048:65536;}else koodipiste(0xfffd);
    }sirkumfleksi_ARVO(1);
}
int Pääte_Odottaa(void){return tietojärjestelmät_Odottaa!=0;}
/* 모서리 INDEKSI: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int muuttaa_kokoa_vetää=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int toimiala_toimi) {
    for(int JONO_ARVO=merkintä_LASKE-1;JONO_ARVO>=0;JONO_ARVO--){
        int tunniste_ARVO=tilata_ARVO[JONO_ARVO];Pääte *Ikkuna=&Windows_luettelo[tunniste_ARVO];
        if(가로>=(int)Ikkuna->x_koordinaatti&&toimiala_toimi>=(int)Ikkuna->Y_koordinaatti&&
           가로<(int)(Ikkuna->x_koordinaatti+Ikkuna->너비)&&toimiala_toimi<(int)(Ikkuna->Y_koordinaatti+Ikkuna->높이))return tunniste_ARVO;
    }return -1;
}
static int 모서리찾기(int tunniste_ARVO,int 가로,int toimiala_toimi) {
    if(tunniste_ARVO<0)return 0;Pääte *Ikkuna=&Windows_luettelo[tunniste_ARVO];
    int 왼쪽=가로<(int)Ikkuna->x_koordinaatti+8,OIKEA=가로>=(int)(Ikkuna->x_koordinaatti+Ikkuna->너비)-8;
    int 위쪽=toimiala_toimi<(int)Ikkuna->Y_koordinaatti+8,아래쪽=toimiala_toimi>=(int)(Ikkuna->Y_koordinaatti+Ikkuna->높이)-8;
    return (왼쪽||OIKEA)&&(위쪽||아래쪽)?1+OIKEA+아래쪽*2:0;
}
static int erotin_ARVO(int ARVO,int 최소,int 최대){return ARVO<최소?최소:ARVO>최대?최대:ARVO;}
static void siirrä_muuttaa_kokoa(int 가로,int toimiala_toimi) {
    Pääte *Ikkuna=&Windows_luettelo[muuttaa_kokoa_vetää];int 왼쪽=처음가로,위쪽=처음세로,OIKEA=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=erotin_ARVO(처음가로+가로-잡은가로,0,OIKEA-360);
    else OIKEA=erotin_ARVO(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=erotin_ARVO(처음세로+toimiala_toimi-잡은세로,34,아래쪽-216);
    else 아래쪽=erotin_ARVO(처음세로+처음높이+toimiala_toimi-잡은세로,위쪽+216,보드화면높이());
    unsigned SARAKKEET=(OIKEA-왼쪽-24)/8,RIVI_LASKE=(아래쪽-위쪽-56)/16;
    if(Ikkuna->SARAKKEET!=SARAKKEET||Ikkuna->RIVI_LASKE!=RIVI_LASKE){
        Ikkuna->크기바뀜=1;Ikkuna->SARAKKEET=SARAKKEET;Ikkuna->RIVI_LASKE=RIVI_LASKE;
        if(Ikkuna->SARAKE_toimi>=SARAKKEET)Ikkuna->SARAKE_toimi=SARAKKEET-1;
        if(Ikkuna->RIVI_toimi>=Ikkuna->맨위+RIVI_LASKE)Ikkuna->맨위=Ikkuna->RIVI_toimi-RIVI_LASKE+1;
        unsigned 한도=Ikkuna->맨위;if(한도>Historia_rivi_LASKE-RIVI_LASKE)한도=Historia_rivi_LASKE-RIVI_LASKE;
        if(Ikkuna->vierittää>한도)Ikkuna->vierittää=한도;
    }
    int 옛가로=Ikkuna->x_koordinaatti,옛세로=Ikkuna->Y_koordinaatti,옛폭=Ikkuna->너비,옛길이=Ikkuna->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==OIKEA-왼쪽&&옛길이==아래쪽-위쪽)return;
    Ikkuna->x_koordinaatti=왼쪽;Ikkuna->Y_koordinaatti=위쪽;Ikkuna->너비=OIKEA-왼쪽;Ikkuna->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Ikkuna);
}
void Pääte_osoitin(unsigned Seuraava_kohde,int x_koordinaatti,int Y_koordinaatti){
    unsigned 눌림=Seuraava_kohde&~단추들;단추들=Seuraava_kohde;
    if(!työpöytä_Näkymä){vetää_ARVO=-1;muuttaa_kokoa_vetää=-1;Taulu_osoitin(x_koordinaatti,Y_koordinaatti,1);return;}
    if(!(Seuraava_kohde&1)){vetää_ARVO=-1;muuttaa_kokoa_vetää=-1;}
    if(muuttaa_kokoa_vetää>=0&&!Windows_luettelo[muuttaa_kokoa_vetää].살아있음)muuttaa_kokoa_vetää=-1;
    if(vetää_ARVO>=0&&!Windows_luettelo[vetää_ARVO].살아있음)vetää_ARVO=-1;
    if(muuttaa_kokoa_vetää>=0){
        siirrä_muuttaa_kokoa(x_koordinaatti,Y_koordinaatti);Taulu_osoitin(x_koordinaatti,Y_koordinaatti,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Taulu_osoitin(x_koordinaatti,Y_koordinaatti,1);
    if(vetää_ARVO>=0){
        Pääte *Ikkuna=&Windows_luettelo[vetää_ARVO];
        int 옛가로=Ikkuna->x_koordinaatti,옛세로=Ikkuna->Y_koordinaatti;
        Ikkuna->x_koordinaatti=erotin_ARVO(x_koordinaatti-vetää_X,0,보드화면너비()-Ikkuna->너비);
        Ikkuna->Y_koordinaatti=erotin_ARVO(Y_koordinaatti-vetää_Y,34,보드화면높이()-Ikkuna->높이);
        if(옛가로!=(int)Ikkuna->x_koordinaatti||옛세로!=(int)Ikkuna->Y_koordinaatti)창자리그리기(옛가로,옛세로,Ikkuna->너비,Ikkuna->높이,Ikkuna);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Aihe,x_koordinaatti,Y_koordinaatti)){화면가리킴(Aihe,눌림,x_koordinaatti,Y_koordinaatti);return;}
    int tunniste_ARVO=가리킨창(x_koordinaatti,Y_koordinaatti),모서리=모서리찾기(tunniste_ARVO,x_koordinaatti,Y_koordinaatti);
    if(모서리)Taulu_osoitin(x_koordinaatti,Y_koordinaatti,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Pääte *Ikkuna=&Windows_luettelo[tunniste_ARVO];muuttaa_kokoa_vetää=tunniste_ARVO;잡은모서리=모서리;잡은가로=x_koordinaatti;잡은세로=Y_koordinaatti;
            처음가로=Ikkuna->x_koordinaatti;처음세로=Ikkuna->Y_koordinaatti;처음너비=Ikkuna->너비;처음높이=Ikkuna->높이;
            if(tunniste_ARVO!=Aihe)앞으로올리기(tunniste_ARVO);return;
        }
        if(Y_koordinaatti<32&&x_koordinaatti>=6&&x_koordinaatti<142){Luo_merkintä();return;}
        if(Y_koordinaatti<32&&x_koordinaatti>=154&&x_koordinaatti<602){앞으로올리기((x_koordinaatti-154)/112);return;}
        if(tunniste_ARVO>=0){
            Pääte *Ikkuna=&Windows_luettelo[tunniste_ARVO];
            if(Y_koordinaatti<(int)Ikkuna->Y_koordinaatti+30&&x_koordinaatti>=(int)(Ikkuna->x_koordinaatti+Ikkuna->너비)-32){Sulje_ikkuna(tunniste_ARVO);return;}
            if(tunniste_ARVO!=Aihe)앞으로올리기(tunniste_ARVO);
            if(Y_koordinaatti<(int)Ikkuna->Y_koordinaatti+30){vetää_ARVO=tunniste_ARVO;vetää_X=x_koordinaatti-Ikkuna->x_koordinaatti;vetää_Y=Y_koordinaatti-Ikkuna->Y_koordinaatti;}return;
        }
    }
    if(Aihe>=0&&(눌림&(8|16))){Pääte_merkintä=&Windows_luettelo[Aihe];if(눌림&8){unsigned 한도=Pääte_merkintä->맨위;if(한도>Historia_rivi_LASKE-Pääte_merkintä->RIVI_LASKE)한도=Historia_rivi_LASKE-Pääte_merkintä->RIVI_LASKE;Pääte_merkintä->vierittää=Pääte_merkintä->vierittää+9>한도?한도:Pääte_merkintä->vierittää+9;}else Pääte_merkintä->vierittää=Pääte_merkintä->vierittää<9?0:Pääte_merkintä->vierittää-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Luo_merkintä();if(누름값==2&&merkintä_LASKE)앞으로올리기(tilata_ARVO[0]);if(누름값==3)Sulje_ikkuna(Aihe);}
kone_Word Taulu_Pääte(kone_Word Toiminto){
    if(Toiminto==300){if(!Windows_luettelo[tulos].살아있음)return Luo_merkintä();työpöytä_Näkymä=1;다시그리기();return 0;}
    if(Toiminto==0){Sulje_ikkuna(Aihe);return 0;}if(Toiminto==1)return (uint32_t)Luo_merkintä();if(Toiminto==2)return Aihe>=0;
    if(Toiminto==9){työpöytä_Näkymä=0;return 0;}if(Toiminto==7)return merkintä_LASKE;if(Toiminto==10)return Aihe+1;if(Toiminto==11)return tulos;
    if(Toiminto==13){Pääte *Ikkuna=&Windows_luettelo[tulos];return Ikkuna->살아있음?(Ikkuna->RIVI_LASKE<<16)|Ikkuna->SARAKKEET:(19<<16)|68;}
    if(Toiminto==14){unsigned ARVO=Windows_luettelo[tulos].크기바뀜;Windows_luettelo[tulos].크기바뀜=0;return ARVO;}
    if(Toiminto==12){unsigned ARVO=tietojärjestelmät_Odottaa;tietojärjestelmät_Odottaa=0;return ARVO;}
    if(Toiminto>=20&&Toiminto<24)return Windows_luettelo[Toiminto-20].살아있음;
    if(Toiminto>=100&&Toiminto<104){tulos=Toiminto-100;Pääte_merkintä=&Windows_luettelo[tulos];return 0;}
    if(Toiminto>=200&&Toiminto<204){앞으로올리기(Toiminto-200);return 0;}
    if(Toiminto==3){다시그리기();return 0;}Pääte_merkintä=&Windows_luettelo[tulos];if(!Pääte_merkintä->살아있음)return 0;
    if(Toiminto==4)selvittää_Sisällys();if(Toiminto==5||Toiminto==6){unsigned Edellinen_kohde=단추들;Pääte_osoitin(Toiminto==5?8:16,0,0);단추들=Edellinen_kohde;}return 1;
}
