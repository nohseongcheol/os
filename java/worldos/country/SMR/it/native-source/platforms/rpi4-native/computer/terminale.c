#include "../명명/기계연결이름.h"
#include "schermata_info.h"
/* nativo 네 Finestra 합성과 UTF-8 terminale. 바뀐 영역의 Completate_VALORE 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t computer_Word;
extern computer_Word scheda_pixel(computer_Word,computer_Word,computer_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminale_tipo_di_carattere[];
#define 최대열수 237
#define Cronologia_riga_CONTA_NUMERI 160
typedef struct {
    uint32_t 글자칸들[Cronologia_riga_CONTA_NUMERI][최대열수]; uint8_t 모양들[Cronologia_riga_CONTA_NUMERI][최대열수];
    unsigned 너비,altezza_VALORE,COLONNE,riga_CONTA_NUMERI,크기바뀜;
    unsigned 살아있음,coordinata_x,Y_coordinata,riga_funzione,colonna_funzione,맨위,scorrere_6486617f,전경색,배경색,탈출상태,parametro_VALORE[4],parametro_INDICE,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,PICCOLO_VALORE,alternativa,가리개보임;
} Terminale;
static Terminale Windows_elenco[4];
static int Focus=-1,output,ordine_VALORE[4],voce_CONTA_NUMERI,trascinare_VALORE=-1,trascinare_X,trascinare_Y;
static unsigned reparto_IT_In_sospeso,단추들,PC_Vista,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),schermata_puntatore(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminale *Terminale_voce;
static unsigned carattere_wide(unsigned punto_di_codice){return punto_di_codice>=256?2:1;}
static void 사각영역(unsigned coordinata_x,unsigned Y_coordinata,unsigned 너비값,unsigned richiesto_altezza_VALORE,unsigned 색상){
    scheda_rettangolo_Riempi(coordinata_x,Y_coordinata,너비값,richiesto_altezza_VALORE,색상);
}
void Terminale_glifo(unsigned coordinata_x,unsigned Y_coordinata,unsigned punto_di_codice,unsigned 전경색,unsigned 배경색){
    unsigned 너비=carattere_wide(punto_di_codice)*8;if(punto_di_codice==0xffffffffu)return;
    int 왼쪽=coordinata_x,위쪽=Y_coordinata,폭=너비,durata_VALORE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&durata_VALORE))return;
    if(punto_di_codice==' '){scheda_rettangolo_Riempi(왼쪽,위쪽,폭,durata_VALORE,배경색);return;}
    unsigned CERCA_INDICE=punto_di_codice<65536?punto_di_codice:punto_di_codice>=0x1f600&&punto_di_codice<0x1f650?65536+punto_di_codice-0x1f600:0xfffd;
    const unsigned char *tipo_di_carattere_VALORE=Terminale_tipo_di_carattere+CERCA_INDICE*32;
    for(int riga_di_ingresso=위쪽;riga_di_ingresso<위쪽+durata_VALORE;riga_di_ingresso++){unsigned BITS_elenco=tipo_di_carattere_VALORE[(riga_di_ingresso-Y_coordinata)*2]*256+tipo_di_carattere_VALORE[(riga_di_ingresso-Y_coordinata)*2+1];for(int slot_voce=왼쪽;slot_voce<왼쪽+폭;slot_voce++)scheda_pixel(slot_voce,riga_di_ingresso,(BITS_elenco&(0x8000>>(slot_voce-coordinata_x)))?전경색:배경색);}
}
static void nome_tabella(unsigned coordinata_x,unsigned Y_coordinata,const char *stringa_dati,unsigned 전경색,unsigned 배경색){while(*stringa_dati){unsigned punto_di_codice=(unsigned char)*stringa_dati++, 남은수=0;if(punto_di_codice>=0xc0){남은수=punto_di_codice<0xe0?1:punto_di_codice<0xf0?2:3;punto_di_codice&=(1u<<(6-남은수))-1;while(남은수--&&*stringa_dati)punto_di_codice=(punto_di_codice<<6)|((unsigned char)*stringa_dati++&63);}Terminale_glifo(coordinata_x,Y_coordinata,punto_di_codice,전경색,배경색);coordinata_x+=carattere_wide(punto_di_codice)*8;}}
static unsigned 첫항목(void){return Terminale_voce->맨위;}
static int 보이는지(void){return Terminale_voce->살아있음&&Focus>=0&&Terminale_voce==&Windows_elenco[Focus]&&!화면보임(Focus);}
static void Paint_schermata(unsigned riga_funzione,unsigned colonna_funzione){
    if(!보이는지()||riga_funzione<첫항목()-Terminale_voce->scorrere_6486617f||riga_funzione>=첫항목()-Terminale_voce->scorrere_6486617f+Terminale_voce->riga_CONTA_NUMERI||colonna_funzione>=Terminale_voce->COLONNE)return;
    unsigned punto_di_codice=Terminale_voce->글자칸들[riga_funzione%Cronologia_riga_CONTA_NUMERI][colonna_funzione],stringa_dati=Terminale_voce->모양들[riga_funzione%Cronologia_riga_CONTA_NUMERI][colonna_funzione];
    if(carattere_wide(punto_di_codice)==2&&colonna_funzione+1>=Terminale_voce->COLONNE)punto_di_codice=' ';
    Terminale_glifo(Terminale_voce->coordinata_x+12+colonna_funzione*8,Terminale_voce->Y_coordinata+36+(riga_funzione-첫항목()+Terminale_voce->scorrere_6486617f)*16,punto_di_codice?punto_di_codice:' ',색상들[stringa_dati&15],색상들[stringa_dati>>4]);
}
static void cursore_VALORE_be8150db(int mostrare_finestra){if(!보이는지()||Terminale_voce->scorrere_6486617f||Terminale_voce->colonna_funzione>=Terminale_voce->COLONNE||Terminale_voce->riga_funzione<Terminale_voce->맨위||Terminale_voce->riga_funzione>=Terminale_voce->맨위+Terminale_voce->riga_CONTA_NUMERI)return;
    if(!mostrare_finestra||!Terminale_voce->가리개보임)Paint_schermata(Terminale_voce->riga_funzione,Terminale_voce->colonna_funzione);else 사각영역(Terminale_voce->coordinata_x+12+Terminale_voce->colonna_funzione*8,Terminale_voce->Y_coordinata+36+(Terminale_voce->riga_funzione-Terminale_voce->맨위)*16+14,8,2,색상들[Terminale_voce->전경색]);}
static void Contenuto_VALORE(void){
    사각영역(Terminale_voce->coordinata_x+12,Terminale_voce->Y_coordinata+36,Terminale_voce->COLONNE*8,Terminale_voce->riga_CONTA_NUMERI*16,색상들[0]);
    int 가로=Terminale_voce->coordinata_x+12,Verticale_funzione=Terminale_voce->Y_coordinata+36,폭=Terminale_voce->COLONNE*8,durata_VALORE=Terminale_voce->riga_CONTA_NUMERI*16;
    if(보드그림범위(&가로,&Verticale_funzione,&폭,&durata_VALORE)){
    unsigned 첫줄=(Verticale_funzione-Terminale_voce->Y_coordinata-36)/16,끝줄=(Verticale_funzione+durata_VALORE-Terminale_voce->Y_coordinata-36+15)/16;
    unsigned 첫칸=(가로-Terminale_voce->coordinata_x-12)/8,끝칸=(가로+폭-Terminale_voce->coordinata_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 limite_VALORE 왼쪽에서 시작한 두 slot_voce 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned punto_di_codice=첫칸;punto_di_codice<끝칸;punto_di_codice++){
        unsigned riga_funzione=첫항목()-Terminale_voce->scorrere_6486617f+반환값,carattere_VALORE=Terminale_voce->글자칸들[riga_funzione%Cronologia_riga_CONTA_NUMERI][punto_di_codice],stringa_dati=Terminale_voce->모양들[riga_funzione%Cronologia_riga_CONTA_NUMERI][punto_di_codice];
        if(carattere_wide(carattere_VALORE)==2&&punto_di_codice+1>=Terminale_voce->COLONNE)carattere_VALORE=' ';
        if((carattere_VALORE==0||carattere_VALORE==' ')&&(stringa_dati>>4)==0)continue;
        Terminale_glifo(Terminale_voce->coordinata_x+12+punto_di_codice*8,Terminale_voce->Y_coordinata+36+반환값*16,carattere_VALORE?carattere_VALORE:' ',색상들[stringa_dati&15],색상들[stringa_dati>>4]);
    }}
    nome_tabella(Terminale_voce->coordinata_x+12,Terminale_voce->Y_coordinata+Terminale_voce->altezza_VALORE-18,Terminale_voce->scorrere_6486617f?"PgDn: recent output":Terminale_voce->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);cursore_VALORE_be8150db(1);
}
static void esecuzione_frame(int identificatore_VALORE){
    Terminale_voce=&Windows_elenco[identificatore_VALORE];
    int 가로=Terminale_voce->coordinata_x,Verticale_funzione=Terminale_voce->Y_coordinata,폭=Terminale_voce->너비,durata_VALORE=Terminale_voce->altezza_VALORE;
    if(!보드그림범위(&가로,&Verticale_funzione,&폭,&durata_VALORE))return;
    사각영역(Terminale_voce->coordinata_x,Terminale_voce->Y_coordinata,Terminale_voce->너비,Terminale_voce->altezza_VALORE,0x403127);
    unsigned 색상=identificatore_VALORE==Focus?0x905020:0x604438;사각영역(Terminale_voce->coordinata_x,Terminale_voce->Y_coordinata,Terminale_voce->너비,30,색상);
    nome_tabella(Terminale_voce->coordinata_x+12,Terminale_voce->Y_coordinata+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identificatore_VALORE),0};nome_tabella(Terminale_voce->coordinata_x+148,Terminale_voce->Y_coordinata+7,수치,0xffffff,색상);
    nome_tabella(Terminale_voce->coordinata_x+240,Terminale_voce->Y_coordinata+7,Terminale_voce->너비>=500?(한글입력?"[IT] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[IT]":"[EN]"),0xffffff,색상);
    사각영역(Terminale_voce->coordinata_x+Terminale_voce->너비-32,Terminale_voce->Y_coordinata+4,26,22,0x5555b8);nome_tabella(Terminale_voce->coordinata_x+Terminale_voce->너비-24,Terminale_voce->Y_coordinata+7,"X",0xffffff,0x5555b8);
    Contenuto_VALORE();
}
static void Disegno_scena(void){
    if(!PC_Vista)return;사각영역(0,0,보드화면너비(),scheda_schermata_altezza(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);nome_tabella(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_elenco[순번].살아있음){unsigned punto_di_codice=Focus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,punto_di_codice);nome_tabella(160+순번*112,8,"Terminal",0xffffff,punto_di_codice);char stringa_dati[2]={(char)('1'+순번),0};nome_tabella(232+순번*112,8,stringa_dati,0xffffff,punto_di_codice);}
    if(!voce_CONTA_NUMERI)nome_tabella(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<voce_CONTA_NUMERI;순번++)esecuzione_frame(ordine_VALORE[순번]);화면다시그림(Focus);Terminale_voce=&Windows_elenco[output];
}
static void Paint_area(int 가로,int Verticale_funzione,int 폭,int durata_VALORE){
    if(!PC_Vista||!보드그림범위(&가로,&Verticale_funzione,&폭,&durata_VALORE))return;
    for(int riga_di_ingresso=Verticale_funzione;riga_di_ingresso<Verticale_funzione+durata_VALORE;riga_di_ingresso+=32){
        int banda_altezza=Verticale_funzione+durata_VALORE-riga_di_ingresso;if(banda_altezza>32)banda_altezza=32;
        if(scheda_START_disegno(가로,riga_di_ingresso,폭,banda_altezza)){Disegno_scena();scheda_Fine_disegno();}
    }
}
static void 다시그리기(void){Paint_area(0,0,보드화면너비(),scheda_schermata_altezza());}
/* 서로 겹치지 않는 새 Finestra 영역과 Indietro_articolo 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Verticale_funzione,int 폭,int durata_VALORE,Terminale *Finestra){
    int 왼쪽=가로>(int)Finestra->coordinata_x?가로:(int)Finestra->coordinata_x;
    int 위쪽=Verticale_funzione>(int)Finestra->Y_coordinata?Verticale_funzione:(int)Finestra->Y_coordinata;
    int DESTRA=가로+폭<(int)(Finestra->coordinata_x+Finestra->너비)?가로+폭:(int)(Finestra->coordinata_x+Finestra->너비);
    int 아래쪽=Verticale_funzione+durata_VALORE<(int)(Finestra->Y_coordinata+Finestra->altezza_VALORE)?Verticale_funzione+durata_VALORE:(int)(Finestra->Y_coordinata+Finestra->altezza_VALORE);
    Paint_area(Finestra->coordinata_x,Finestra->Y_coordinata,Finestra->너비,Finestra->altezza_VALORE);
    if(왼쪽>=DESTRA||위쪽>=아래쪽){Paint_area(가로,Verticale_funzione,폭,durata_VALORE);return;}
    Paint_area(가로,Verticale_funzione,폭,위쪽-Verticale_funzione);
    Paint_area(가로,아래쪽,폭,Verticale_funzione+durata_VALORE-아래쪽);
    Paint_area(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Paint_area(DESTRA,위쪽,가로+폭-DESTRA,아래쪽-위쪽);
}
static void segnale_Focus(void){reparto_IT_In_sospeso=(reparto_IT_In_sospeso&~15u)|(unsigned)(Focus+1)|0x10000;}
void Terminale_input_MODA(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Focus>=0){
        Terminale *finestra_voce=&Windows_elenco[Focus];
        nome_tabella(finestra_voce->coordinata_x+240,finestra_voce->Y_coordinata+7,finestra_voce->너비>=500?(한글입력?"[IT] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[IT]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identificatore_VALORE){if(identificatore_VALORE<0||identificatore_VALORE>=4||!Windows_elenco[identificatore_VALORE].살아있음)return;int Regolari_funzione=0;while(Regolari_funzione<voce_CONTA_NUMERI&&ordine_VALORE[Regolari_funzione]!=identificatore_VALORE)Regolari_funzione++;for(;Regolari_funzione+1<voce_CONTA_NUMERI;Regolari_funzione++)ordine_VALORE[Regolari_funzione]=ordine_VALORE[Regolari_funzione+1];ordine_VALORE[voce_CONTA_NUMERI-1]=identificatore_VALORE;Focus=identificatore_VALORE;segnale_Focus();다시그리기();}
static void spazio(unsigned riga_funzione){for(unsigned punto_di_codice=0;punto_di_codice<최대열수;punto_di_codice++){Terminale_voce->글자칸들[riga_funzione%Cronologia_riga_CONTA_NUMERI][punto_di_codice]=0;Terminale_voce->모양들[riga_funzione%Cronologia_riga_CONTA_NUMERI][punto_di_codice]=Terminale_voce->전경색|(Terminale_voce->배경색<<4);}}
static void liquidare_Sommario(void){Terminale_voce->riga_funzione=Terminale_voce->colonna_funzione=Terminale_voce->맨위=Terminale_voce->scorrere_6486617f=0;for(unsigned 반환값=0;반환값<Cronologia_riga_CONTA_NUMERI;반환값++)spazio(반환값);if(보이는지())Contenuto_VALORE();}
static int Crea_voce(void){
    if(!보드화면기억공간())return -19;int identificatore_VALORE=0;while(identificatore_VALORE<4&&Windows_elenco[identificatore_VALORE].살아있음)identificatore_VALORE++;if(identificatore_VALORE==4)return -28;
    PC_Vista=1;Terminale_voce=&Windows_elenco[identificatore_VALORE];memset(Terminale_voce,0,sizeof(*Terminale_voce));Terminale_voce->살아있음=1;Terminale_voce->너비=568;Terminale_voce->altezza_VALORE=360;Terminale_voce->COLONNE=68;Terminale_voce->riga_CONTA_NUMERI=19;Terminale_voce->coordinata_x=12+identificatore_VALORE*16;Terminale_voce->Y_coordinata=48+identificatore_VALORE*18;Terminale_voce->전경색=7;Terminale_voce->가리개보임=1;
    for(unsigned 반환값=0;반환값<Cronologia_riga_CONTA_NUMERI;반환값++)spazio(반환값);ordine_VALORE[voce_CONTA_NUMERI++]=identificatore_VALORE;Focus=identificatore_VALORE;reparto_IT_In_sospeso|=1u<<(4+identificatore_VALORE);segnale_Focus();다시그리기();return identificatore_VALORE+1;
}
static void Chiudi_finestra(int identificatore_VALORE){
    if(identificatore_VALORE<0||identificatore_VALORE>=4||!Windows_elenco[identificatore_VALORE].살아있음)return;Windows_elenco[identificatore_VALORE].살아있음=0;reparto_IT_In_sospeso|=1u<<(8+identificatore_VALORE);
    int Regolari_funzione=0;while(Regolari_funzione<voce_CONTA_NUMERI&&ordine_VALORE[Regolari_funzione]!=identificatore_VALORE)Regolari_funzione++;for(;Regolari_funzione+1<voce_CONTA_NUMERI;Regolari_funzione++)ordine_VALORE[Regolari_funzione]=ordine_VALORE[Regolari_funzione+1];voce_CONTA_NUMERI--;
    if(Focus==identificatore_VALORE)Focus=voce_CONTA_NUMERI?ordine_VALORE[voce_CONTA_NUMERI-1]:-1;segnale_Focus();다시그리기();
}
static void 줄바꿈(void){Terminale_voce->colonna_funzione=0;Terminale_voce->riga_funzione++;if(Terminale_voce->riga_funzione>=Terminale_voce->맨위+Terminale_voce->riga_CONTA_NUMERI){Terminale_voce->맨위++;spazio(Terminale_voce->riga_funzione);if(보이는지())Contenuto_VALORE();}}
static void punto_di_codice_451f2815(unsigned punto_di_codice){
    if(punto_di_codice==13){Terminale_voce->colonna_funzione=0;return;}if(punto_di_codice==10){줄바꿈();return;}if(punto_di_codice==8){if(Terminale_voce->colonna_funzione)Terminale_voce->colonna_funzione--;return;}
    if(punto_di_codice==9){unsigned articolo_CONTA_NUMERI=8-Terminale_voce->colonna_funzione%8;while(articolo_CONTA_NUMERI--)punto_di_codice_451f2815(' ');return;}if(punto_di_codice<32||punto_di_codice==127)return;
    unsigned 너비값=carattere_wide(punto_di_codice);if(Terminale_voce->colonna_funzione+너비값>Terminale_voce->COLONNE)줄바꿈();
    if(Terminale_voce->글자칸들[Terminale_voce->riga_funzione%Cronologia_riga_CONTA_NUMERI][Terminale_voce->colonna_funzione]==0xffffffffu&&Terminale_voce->colonna_funzione){Terminale_voce->글자칸들[Terminale_voce->riga_funzione%Cronologia_riga_CONTA_NUMERI][Terminale_voce->colonna_funzione-1]=' ';Paint_schermata(Terminale_voce->riga_funzione,Terminale_voce->colonna_funzione-1);}
    if(carattere_wide(Terminale_voce->글자칸들[Terminale_voce->riga_funzione%Cronologia_riga_CONTA_NUMERI][Terminale_voce->colonna_funzione])==2&&Terminale_voce->colonna_funzione+1<Terminale_voce->COLONNE){Terminale_voce->글자칸들[Terminale_voce->riga_funzione%Cronologia_riga_CONTA_NUMERI][Terminale_voce->colonna_funzione+1]=' ';Paint_schermata(Terminale_voce->riga_funzione,Terminale_voce->colonna_funzione+1);}
    Terminale_voce->글자칸들[Terminale_voce->riga_funzione%Cronologia_riga_CONTA_NUMERI][Terminale_voce->colonna_funzione]=punto_di_codice;Terminale_voce->모양들[Terminale_voce->riga_funzione%Cronologia_riga_CONTA_NUMERI][Terminale_voce->colonna_funzione]=Terminale_voce->전경색|(Terminale_voce->배경색<<4);
    if(너비값==2)Terminale_voce->글자칸들[Terminale_voce->riga_funzione%Cronologia_riga_CONTA_NUMERI][Terminale_voce->colonna_funzione+1]=0xffffffffu;
    Paint_schermata(Terminale_voce->riga_funzione,Terminale_voce->colonna_funzione);Terminale_voce->colonna_funzione+=너비값;
}
static void handle_codice_di_controllo(unsigned punto_di_codice){
    unsigned articolo_CONTA_NUMERI=Terminale_voce->parametro_VALORE[0]?Terminale_voce->parametro_VALORE[0]:1;
    if(punto_di_codice=='m')for(unsigned 순번=0;순번<=Terminale_voce->parametro_INDICE;순번++){unsigned dati_funzione=Terminale_voce->parametro_VALORE[순번];if(!dati_funzione){Terminale_voce->전경색=7;Terminale_voce->배경색=0;}if(dati_funzione==1&&Terminale_voce->전경색<8)Terminale_voce->전경색+=8;if(dati_funzione==7){unsigned mantenere_VALORE=Terminale_voce->전경색;Terminale_voce->전경색=Terminale_voce->배경색;Terminale_voce->배경색=mantenere_VALORE;}if(dati_funzione>=30&&dati_funzione<=37)Terminale_voce->전경색=dati_funzione-30;if(dati_funzione>=90&&dati_funzione<=97)Terminale_voce->전경색=dati_funzione-90+8;if(dati_funzione>=40&&dati_funzione<=47)Terminale_voce->배경색=dati_funzione-40;if(dati_funzione>=100&&dati_funzione<=107)Terminale_voce->배경색=dati_funzione-100+8;if(dati_funzione==39)Terminale_voce->전경색=7;if(dati_funzione==49)Terminale_voce->배경색=0;}
    if(punto_di_codice=='J'&&(Terminale_voce->parametro_VALORE[0]==2||Terminale_voce->parametro_VALORE[0]==3))liquidare_Sommario();
    if(punto_di_codice=='K'){unsigned 출발위치=Terminale_voce->parametro_VALORE[0]==2?0:Terminale_voce->colonna_funzione,도착위치=Terminale_voce->parametro_VALORE[0]==1?Terminale_voce->colonna_funzione+1:Terminale_voce->COLONNE;if(Terminale_voce->parametro_VALORE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminale_voce->COLONNE;순번++){
        unsigned riga_VALORE=Terminale_voce->riga_funzione%Cronologia_riga_CONTA_NUMERI,carattere_VALORE=Terminale_voce->글자칸들[riga_VALORE][순번],forma_VALORE=Terminale_voce->전경색|(Terminale_voce->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 tipo_di_carattere_VALORE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(carattere_VALORE!=0&&carattere_VALORE!=' ')||Terminale_voce->모양들[riga_VALORE][순번]!=forma_VALORE;
        Terminale_voce->글자칸들[riga_VALORE][순번]=' ';Terminale_voce->모양들[riga_VALORE][순번]=forma_VALORE;
        if(바뀜)Paint_schermata(Terminale_voce->riga_funzione,순번);
    }}
    if(punto_di_codice=='D')Terminale_voce->colonna_funzione=articolo_CONTA_NUMERI>Terminale_voce->colonna_funzione?0:Terminale_voce->colonna_funzione-articolo_CONTA_NUMERI;if(punto_di_codice=='C')Terminale_voce->colonna_funzione=Terminale_voce->colonna_funzione+articolo_CONTA_NUMERI>=Terminale_voce->COLONNE?Terminale_voce->COLONNE-1:Terminale_voce->colonna_funzione+articolo_CONTA_NUMERI;
    if(punto_di_codice=='G')Terminale_voce->colonna_funzione=articolo_CONTA_NUMERI>Terminale_voce->COLONNE?Terminale_voce->COLONNE-1:articolo_CONTA_NUMERI-1;if(punto_di_codice=='A')Terminale_voce->riga_funzione=articolo_CONTA_NUMERI>Terminale_voce->riga_funzione-Terminale_voce->맨위?Terminale_voce->맨위:Terminale_voce->riga_funzione-articolo_CONTA_NUMERI;
    if(punto_di_codice=='B')Terminale_voce->riga_funzione=Terminale_voce->riga_funzione+articolo_CONTA_NUMERI>=Terminale_voce->맨위+Terminale_voce->riga_CONTA_NUMERI?Terminale_voce->맨위+Terminale_voce->riga_CONTA_NUMERI-1:Terminale_voce->riga_funzione+articolo_CONTA_NUMERI;
    if(punto_di_codice=='H'||punto_di_codice=='f'){Terminale_voce->riga_funzione=Terminale_voce->맨위+(articolo_CONTA_NUMERI>Terminale_voce->riga_CONTA_NUMERI?Terminale_voce->riga_CONTA_NUMERI:articolo_CONTA_NUMERI)-1;unsigned coordinata_x=Terminale_voce->parametro_VALORE[1]?Terminale_voce->parametro_VALORE[1]:1;Terminale_voce->colonna_funzione=(coordinata_x>Terminale_voce->COLONNE?Terminale_voce->COLONNE:coordinata_x)-1;}
    if(punto_di_codice=='s'){Terminale_voce->저장행=Terminale_voce->riga_funzione;Terminale_voce->저장열=Terminale_voce->colonna_funzione;}if(punto_di_codice=='u'){Terminale_voce->riga_funzione=Terminale_voce->저장행;Terminale_voce->colonna_funzione=Terminale_voce->저장열<Terminale_voce->COLONNE?Terminale_voce->저장열:Terminale_voce->COLONNE-1;}
    if((punto_di_codice=='h'||punto_di_codice=='l')&&Terminale_voce->parametro_VALORE[0]==25)Terminale_voce->가리개보임=punto_di_codice=='h';
}
void Terminale_byte(unsigned SECONDO_VALORE){
    Terminale_voce=&Windows_elenco[output];if(!Terminale_voce->살아있음)return;cursore_VALORE_be8150db(0);if(Terminale_voce->scorrere_6486617f){Terminale_voce->scorrere_6486617f=0;if(보이는지())Contenuto_VALORE();}
    if(Terminale_voce->탈출상태==1){Terminale_voce->탈출상태=SECONDO_VALORE=='['?2:0;Terminale_voce->parametro_INDICE=0;for(unsigned 순번=0;순번<4;순번++)Terminale_voce->parametro_VALORE[순번]=0;}
    else if(Terminale_voce->탈출상태==2){if(SECONDO_VALORE=='?'){}else if(SECONDO_VALORE>='0'&&SECONDO_VALORE<='9'){if(Terminale_voce->parametro_VALORE[Terminale_voce->parametro_INDICE]<10000)Terminale_voce->parametro_VALORE[Terminale_voce->parametro_INDICE]=Terminale_voce->parametro_VALORE[Terminale_voce->parametro_INDICE]*10+SECONDO_VALORE-'0';}else if(SECONDO_VALORE==';'&&Terminale_voce->parametro_INDICE<3)Terminale_voce->parametro_INDICE++;else{handle_codice_di_controllo(SECONDO_VALORE);Terminale_voce->탈출상태=0;}}
    else if(SECONDO_VALORE==27){Terminale_voce->긴부호없는값=0;Terminale_voce->탈출상태=1;}else{
        if(Terminale_voce->긴부호없는값&&(SECONDO_VALORE&0xc0)!=0x80){Terminale_voce->긴부호없는값=0;punto_di_codice_451f2815(0xfffd);}
        if(Terminale_voce->긴부호없는값){Terminale_voce->부호없는결과=Terminale_voce->부호없는결과*64+(SECONDO_VALORE&63);if(--Terminale_voce->긴부호없는값==0)punto_di_codice_451f2815(Terminale_voce->부호없는결과<Terminale_voce->PICCOLO_VALORE||Terminale_voce->부호없는결과>0x10ffff||(Terminale_voce->부호없는결과>=0xd800&&Terminale_voce->부호없는결과<=0xdfff)?0xfffd:Terminale_voce->부호없는결과);}
        else if(SECONDO_VALORE<128)punto_di_codice_451f2815(SECONDO_VALORE);else if(SECONDO_VALORE>=0xc2&&SECONDO_VALORE<=0xf4){Terminale_voce->긴부호없는값=SECONDO_VALORE<0xe0?1:SECONDO_VALORE<0xf0?2:3;Terminale_voce->부호없는결과=SECONDO_VALORE&((1u<<(6-Terminale_voce->긴부호없는값))-1);Terminale_voce->PICCOLO_VALORE=Terminale_voce->긴부호없는값==1?128:Terminale_voce->긴부호없는값==2?2048:65536;}else punto_di_codice_451f2815(0xfffd);
    }cursore_VALORE_be8150db(1);
}
int Terminale_In_sospeso(void){return reparto_IT_In_sospeso!=0;}
/* 모서리 INDICE: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int ridimensionare_trascinare=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Verticale_funzione) {
    for(int SEQUENZA_VALORE=voce_CONTA_NUMERI-1;SEQUENZA_VALORE>=0;SEQUENZA_VALORE--){
        int identificatore_VALORE=ordine_VALORE[SEQUENZA_VALORE];Terminale *Finestra=&Windows_elenco[identificatore_VALORE];
        if(가로>=(int)Finestra->coordinata_x&&Verticale_funzione>=(int)Finestra->Y_coordinata&&
           가로<(int)(Finestra->coordinata_x+Finestra->너비)&&Verticale_funzione<(int)(Finestra->Y_coordinata+Finestra->altezza_VALORE))return identificatore_VALORE;
    }return -1;
}
static int 모서리찾기(int identificatore_VALORE,int 가로,int Verticale_funzione) {
    if(identificatore_VALORE<0)return 0;Terminale *Finestra=&Windows_elenco[identificatore_VALORE];
    int 왼쪽=가로<(int)Finestra->coordinata_x+8,DESTRA=가로>=(int)(Finestra->coordinata_x+Finestra->너비)-8;
    int 위쪽=Verticale_funzione<(int)Finestra->Y_coordinata+8,아래쪽=Verticale_funzione>=(int)(Finestra->Y_coordinata+Finestra->altezza_VALORE)-8;
    return (왼쪽||DESTRA)&&(위쪽||아래쪽)?1+DESTRA+아래쪽*2:0;
}
static int separatore_VALORE(int VALORE,int 최소,int 최대){return VALORE<최소?최소:VALORE>최대?최대:VALORE;}
static void spostare_ridimensionare(int 가로,int Verticale_funzione) {
    Terminale *Finestra=&Windows_elenco[ridimensionare_trascinare];int 왼쪽=처음가로,위쪽=처음세로,DESTRA=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=separatore_VALORE(처음가로+가로-잡은가로,0,DESTRA-360);
    else DESTRA=separatore_VALORE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=separatore_VALORE(처음세로+Verticale_funzione-잡은세로,34,아래쪽-216);
    else 아래쪽=separatore_VALORE(처음세로+처음높이+Verticale_funzione-잡은세로,위쪽+216,scheda_schermata_altezza());
    unsigned COLONNE=(DESTRA-왼쪽-24)/8,riga_CONTA_NUMERI=(아래쪽-위쪽-56)/16;
    if(Finestra->COLONNE!=COLONNE||Finestra->riga_CONTA_NUMERI!=riga_CONTA_NUMERI){
        Finestra->크기바뀜=1;Finestra->COLONNE=COLONNE;Finestra->riga_CONTA_NUMERI=riga_CONTA_NUMERI;
        if(Finestra->colonna_funzione>=COLONNE)Finestra->colonna_funzione=COLONNE-1;
        if(Finestra->riga_funzione>=Finestra->맨위+riga_CONTA_NUMERI)Finestra->맨위=Finestra->riga_funzione-riga_CONTA_NUMERI+1;
        unsigned 한도=Finestra->맨위;if(한도>Cronologia_riga_CONTA_NUMERI-riga_CONTA_NUMERI)한도=Cronologia_riga_CONTA_NUMERI-riga_CONTA_NUMERI;
        if(Finestra->scorrere_6486617f>한도)Finestra->scorrere_6486617f=한도;
    }
    int 옛가로=Finestra->coordinata_x,옛세로=Finestra->Y_coordinata,옛폭=Finestra->너비,옛길이=Finestra->altezza_VALORE;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==DESTRA-왼쪽&&옛길이==아래쪽-위쪽)return;
    Finestra->coordinata_x=왼쪽;Finestra->Y_coordinata=위쪽;Finestra->너비=DESTRA-왼쪽;Finestra->altezza_VALORE=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Finestra);
}
void Terminale_puntatore(unsigned Avanti_articolo,int coordinata_x,int Y_coordinata){
    unsigned 눌림=Avanti_articolo&~단추들;단추들=Avanti_articolo;
    if(!PC_Vista){trascinare_VALORE=-1;ridimensionare_trascinare=-1;scheda_puntatore(coordinata_x,Y_coordinata,1);return;}
    if(!(Avanti_articolo&1)){trascinare_VALORE=-1;ridimensionare_trascinare=-1;}
    if(ridimensionare_trascinare>=0&&!Windows_elenco[ridimensionare_trascinare].살아있음)ridimensionare_trascinare=-1;
    if(trascinare_VALORE>=0&&!Windows_elenco[trascinare_VALORE].살아있음)trascinare_VALORE=-1;
    if(ridimensionare_trascinare>=0){
        spostare_ridimensionare(coordinata_x,Y_coordinata);scheda_puntatore(coordinata_x,Y_coordinata,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    scheda_puntatore(coordinata_x,Y_coordinata,1);
    if(trascinare_VALORE>=0){
        Terminale *Finestra=&Windows_elenco[trascinare_VALORE];
        int 옛가로=Finestra->coordinata_x,옛세로=Finestra->Y_coordinata;
        Finestra->coordinata_x=separatore_VALORE(coordinata_x-trascinare_X,0,보드화면너비()-Finestra->너비);
        Finestra->Y_coordinata=separatore_VALORE(Y_coordinata-trascinare_Y,34,scheda_schermata_altezza()-Finestra->altezza_VALORE);
        if(옛가로!=(int)Finestra->coordinata_x||옛세로!=(int)Finestra->Y_coordinata)창자리그리기(옛가로,옛세로,Finestra->너비,Finestra->altezza_VALORE,Finestra);
        return;
    }
    extern int schermata_sovrimpressione(int,int,int);
    if(schermata_sovrimpressione(Focus,coordinata_x,Y_coordinata)){schermata_puntatore(Focus,눌림,coordinata_x,Y_coordinata);return;}
    int identificatore_VALORE=가리킨창(coordinata_x,Y_coordinata),모서리=모서리찾기(identificatore_VALORE,coordinata_x,Y_coordinata);
    if(모서리)scheda_puntatore(coordinata_x,Y_coordinata,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminale *Finestra=&Windows_elenco[identificatore_VALORE];ridimensionare_trascinare=identificatore_VALORE;잡은모서리=모서리;잡은가로=coordinata_x;잡은세로=Y_coordinata;
            처음가로=Finestra->coordinata_x;처음세로=Finestra->Y_coordinata;처음너비=Finestra->너비;처음높이=Finestra->altezza_VALORE;
            if(identificatore_VALORE!=Focus)앞으로올리기(identificatore_VALORE);return;
        }
        if(Y_coordinata<32&&coordinata_x>=6&&coordinata_x<142){Crea_voce();return;}
        if(Y_coordinata<32&&coordinata_x>=154&&coordinata_x<602){앞으로올리기((coordinata_x-154)/112);return;}
        if(identificatore_VALORE>=0){
            Terminale *Finestra=&Windows_elenco[identificatore_VALORE];
            if(Y_coordinata<(int)Finestra->Y_coordinata+30&&coordinata_x>=(int)(Finestra->coordinata_x+Finestra->너비)-32){Chiudi_finestra(identificatore_VALORE);return;}
            if(identificatore_VALORE!=Focus)앞으로올리기(identificatore_VALORE);
            if(Y_coordinata<(int)Finestra->Y_coordinata+30){trascinare_VALORE=identificatore_VALORE;trascinare_X=coordinata_x-Finestra->coordinata_x;trascinare_Y=Y_coordinata-Finestra->Y_coordinata;}return;
        }
    }
    if(Focus>=0&&(눌림&(8|16))){Terminale_voce=&Windows_elenco[Focus];if(눌림&8){unsigned 한도=Terminale_voce->맨위;if(한도>Cronologia_riga_CONTA_NUMERI-Terminale_voce->riga_CONTA_NUMERI)한도=Cronologia_riga_CONTA_NUMERI-Terminale_voce->riga_CONTA_NUMERI;Terminale_voce->scorrere_6486617f=Terminale_voce->scorrere_6486617f+9>한도?한도:Terminale_voce->scorrere_6486617f+9;}else Terminale_voce->scorrere_6486617f=Terminale_voce->scorrere_6486617f<9?0:Terminale_voce->scorrere_6486617f-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Crea_voce();if(누름값==2&&voce_CONTA_NUMERI)앞으로올리기(ordine_VALORE[0]);if(누름값==3)Chiudi_finestra(Focus);}
computer_Word scheda_Terminale(computer_Word Azione){
    if(Azione==300){if(!Windows_elenco[output].살아있음)return Crea_voce();PC_Vista=1;다시그리기();return 0;}
    if(Azione==0){Chiudi_finestra(Focus);return 0;}if(Azione==1)return (uint32_t)Crea_voce();if(Azione==2)return Focus>=0;
    if(Azione==9){PC_Vista=0;return 0;}if(Azione==7)return voce_CONTA_NUMERI;if(Azione==10)return Focus+1;if(Azione==11)return output;
    if(Azione==13){Terminale *Finestra=&Windows_elenco[output];return Finestra->살아있음?(Finestra->riga_CONTA_NUMERI<<16)|Finestra->COLONNE:(19<<16)|68;}
    if(Azione==14){unsigned VALORE=Windows_elenco[output].크기바뀜;Windows_elenco[output].크기바뀜=0;return VALORE;}
    if(Azione==12){unsigned VALORE=reparto_IT_In_sospeso;reparto_IT_In_sospeso=0;return VALORE;}
    if(Azione>=20&&Azione<24)return Windows_elenco[Azione-20].살아있음;
    if(Azione>=100&&Azione<104){output=Azione-100;Terminale_voce=&Windows_elenco[output];return 0;}
    if(Azione>=200&&Azione<204){앞으로올리기(Azione-200);return 0;}
    if(Azione==3){다시그리기();return 0;}Terminale_voce=&Windows_elenco[output];if(!Terminale_voce->살아있음)return 0;
    if(Azione==4)liquidare_Sommario();if(Azione==5||Azione==6){unsigned Indietro_articolo=단추들;Terminale_puntatore(Azione==5?8:16,0,0);단추들=Indietro_articolo;}return 1;
}
