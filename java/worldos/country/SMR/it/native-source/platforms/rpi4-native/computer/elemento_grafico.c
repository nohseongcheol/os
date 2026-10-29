#include "../명명/기계연결이름.h"
#include "schermata_info.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t scheda_pixel(uintptr_t,uintptr_t,uintptr_t),scheda_Terminale(uintptr_t);
extern void Terminale_glifo(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int Valore_categoria,padre,coordinata_x,Y_coordinata,너비값,richiesto_altezza_VALORE,보이는지,manuale_Layout,Layout_norma;unsigned testo[128],durata_VALORE; } widget_Stato;
static widget_Stato 요소들[4][32];
static int Evidenziata[4],evento_elenco[4][16];static unsigned 첫항목[4],voce_CONTA_NUMERI[4],부호없는결과[4],긴부호없는값[4];
static void Evento(int proprietario_oggetto,int VALORE){if(voce_CONTA_NUMERI[proprietario_oggetto]<16){evento_elenco[proprietario_oggetto][(첫항목[proprietario_oggetto]+voce_CONTA_NUMERI[proprietario_oggetto])%16]=VALORE;voce_CONTA_NUMERI[proprietario_oggetto]++;}}
static widget_Stato *elemento_VALORE(int proprietario_oggetto,int identificatore_VALORE){return proprietario_oggetto>=0&&proprietario_oggetto<4&&identificatore_VALORE>0&&identificatore_VALORE<=32&&요소들[proprietario_oggetto][identificatore_VALORE-1].Valore_categoria?&요소들[proprietario_oggetto][identificatore_VALORE-1]:0;}
static void 사각영역(int coordinata_x,int Y_coordinata,int 너비값,int richiesto_altezza_VALORE,unsigned 색상){scheda_rettangolo_Riempi(coordinata_x,Y_coordinata,너비값,richiesto_altezza_VALORE,색상);}
int 화면보임(int proprietario_oggetto){if(proprietario_oggetto<0||proprietario_oggetto>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[proprietario_oggetto][순번].Valore_categoria==1&&요소들[proprietario_oggetto][순번].보이는지)return 1;return 0;}
void inizializzare_schermata(int proprietario_oggetto){memset(요소들[proprietario_oggetto],0,sizeof(요소들[proprietario_oggetto]));voce_CONTA_NUMERI[proprietario_oggetto]=첫항목[proprietario_oggetto]=Evidenziata[proprietario_oggetto]=긴부호없는값[proprietario_oggetto]=0;}
static void posizione(int proprietario_oggetto,widget_Stato *너비값,int *coordinata_x,int *Y_coordinata){*coordinata_x=너비값->coordinata_x;*Y_coordinata=너비값->Y_coordinata;int dati_funzione=너비값->padre;for(int articolo_CONTA_NUMERI=0;dati_funzione&&articolo_CONTA_NUMERI<32;articolo_CONTA_NUMERI++){widget_Stato *위쪽=elemento_VALORE(proprietario_oggetto,dati_funzione);if(!위쪽)break;*coordinata_x+=위쪽->coordinata_x;*Y_coordinata+=위쪽->Y_coordinata+(위쪽->Valore_categoria==1?30:0);dati_funzione=위쪽->padre;}}
static int 표시됨(int proprietario_oggetto,widget_Stato *너비값){for(int articolo_CONTA_NUMERI=0;articolo_CONTA_NUMERI<32;articolo_CONTA_NUMERI++){if(!너비값->보이는지)return 0;if(너비값->Valore_categoria==1)return 1;너비값=elemento_VALORE(proprietario_oggetto,너비값->padre);if(!너비값)return 0;}return 0;}
static void testo(int coordinata_x,int Y_coordinata,widget_Stato *너비값,int 최대값,unsigned 색상,unsigned 배경색){int Regolari_funzione=0;for(unsigned 순번=0;순번<너비값->durata_VALORE;순번++){unsigned codifica_dei_caratteri=너비값->testo[순번],너비=codifica_dei_caratteri>=256?16:8;if(Regolari_funzione+(int)너비>최대값)break;Terminale_glifo(coordinata_x+Regolari_funzione,Y_coordinata,codifica_dei_caratteri,색상,배경색);Regolari_funzione+=너비;}}
void 화면다시그림(int proprietario_oggetto){
    if(!화면보임(proprietario_oggetto))return;
    for(int elaborazione_ordine=1;elaborazione_ordine<=5;elaborazione_ordine++)for(int 순번=0;순번<32;순번++){
        widget_Stato *너비값=&요소들[proprietario_oggetto][순번];if(너비값->Valore_categoria!=elaborazione_ordine||!표시됨(proprietario_oggetto,너비값))continue;int coordinata_x,Y_coordinata;posizione(proprietario_oggetto,너비값,&coordinata_x,&Y_coordinata);
        if(elaborazione_ordine==1){사각영역(coordinata_x,Y_coordinata,너비값->너비값,너비값->richiesto_altezza_VALORE,0xeee9e0);사각영역(coordinata_x,Y_coordinata,너비값->너비값,30,0x905020);testo(coordinata_x+10,Y_coordinata+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(coordinata_x+너비값->너비값-28,Y_coordinata+4,24,22,0x5555b8);Terminale_glifo(coordinata_x+너비값->너비값-20,Y_coordinata+7,'X',0xffffff,0x5555b8);}
        if(elaborazione_ordine==2)사각영역(coordinata_x,Y_coordinata,너비값->너비값,너비값->richiesto_altezza_VALORE,0xeee9e0);
        if(elaborazione_ordine>=3){unsigned 배경색=elaborazione_ordine==4?0xc0ab86:elaborazione_ordine==5?0xffffff:0xeee9e0;if(elaborazione_ordine!=3)사각영역(coordinata_x,Y_coordinata,너비값->너비값,너비값->richiesto_altezza_VALORE,배경색);testo(coordinata_x+4,Y_coordinata+4,너비값,너비값->너비값-8,0x201a15,배경색);if(elaborazione_ordine==5&&Evidenziata[proprietario_oggetto]==순번+1)사각영역(coordinata_x,Y_coordinata+너비값->richiesto_altezza_VALORE-2,너비값->너비값,2,0x905020);}
    }
}
int schermata_sovrimpressione(int proprietario_oggetto,int coordinata_x,int Y_coordinata){
    if(!화면보임(proprietario_oggetto))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_Stato *Finestra=&요소들[proprietario_oggetto][순번];
        if(Finestra->Valore_categoria==1&&Finestra->보이는지&&coordinata_x>=Finestra->coordinata_x&&Y_coordinata>=Finestra->Y_coordinata&&
           coordinata_x<Finestra->coordinata_x+Finestra->너비값&&Y_coordinata<Finestra->Y_coordinata+Finestra->richiesto_altezza_VALORE)return 1;
    }return 0;
}
int schermata_puntatore(int proprietario_oggetto,unsigned 눌림,int coordinata_x,int Y_coordinata){
    if(!화면보임(proprietario_oggetto))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_Stato *너비값=&요소들[proprietario_oggetto][순번];if(!너비값->Valore_categoria||!표시됨(proprietario_oggetto,너비값))continue;int finestra_X,finestra_Y;posizione(proprietario_oggetto,너비값,&finestra_X,&finestra_Y);
        if(coordinata_x<finestra_X||Y_coordinata<finestra_Y||coordinata_x>=finestra_X+너비값->너비값||Y_coordinata>=finestra_Y+너비값->richiesto_altezza_VALORE)continue;
        if(너비값->Valore_categoria==1&&Y_coordinata<finestra_Y+30&&coordinata_x>=finestra_X+너비값->너비값-28){if(너비값->Layout_norma!=0)너비값->보이는지=0;Evento(proprietario_oggetto,0x10000+순번+1);scheda_Terminale(3);return 1;}
        if(너비값->Valore_categoria==4){Evento(proprietario_oggetto,순번+1);return 1;}if(너비값->Valore_categoria==5){Evidenziata[proprietario_oggetto]=순번+1;scheda_Terminale(3);return 1;}
        if(너비값->Valore_categoria==1)return 1;
    }return 0;
}
void 화면누름(int proprietario_oggetto,unsigned SECONDO_VALORE){
    widget_Stato *너비값=elemento_VALORE(proprietario_oggetto,Evidenziata[proprietario_oggetto]);if(!너비값||너비값->Valore_categoria!=5)return;
    if(SECONDO_VALORE==13||SECONDO_VALORE==10){Evento(proprietario_oggetto,Evidenziata[proprietario_oggetto]);return;}
    if(SECONDO_VALORE==8||SECONDO_VALORE==127){if(너비값->durata_VALORE)너비값->durata_VALORE--;긴부호없는값[proprietario_oggetto]=0;}
    else{
        unsigned codifica_dei_caratteri=SECONDO_VALORE;
        if(긴부호없는값[proprietario_oggetto]){if((SECONDO_VALORE&192)!=128){긴부호없는값[proprietario_oggetto]=0;return;}부호없는결과[proprietario_oggetto]=(부호없는결과[proprietario_oggetto]<<6)|(SECONDO_VALORE&63);if(--긴부호없는값[proprietario_oggetto])return;codifica_dei_caratteri=부호없는결과[proprietario_oggetto];}
        else if(SECONDO_VALORE>=0xc2&&SECONDO_VALORE<=0xf4){긴부호없는값[proprietario_oggetto]=SECONDO_VALORE<0xe0?1:SECONDO_VALORE<0xf0?2:3;부호없는결과[proprietario_oggetto]=SECONDO_VALORE&((1u<<(6-긴부호없는값[proprietario_oggetto]))-1);return;}
        else if(SECONDO_VALORE<32||SECONDO_VALORE>=128)return;
        if(codifica_dei_caratteri>0x10ffff||(codifica_dei_caratteri>=0xd800&&codifica_dei_caratteri<=0xdfff))return;if(너비값->durata_VALORE<127)너비값->testo[너비값->durata_VALORE++]=codifica_dei_caratteri;
    }
    scheda_Terminale(3);
}
int 화면호출(int proprietario_oggetto,unsigned Azione,int identificatore_VALORE,int 첫째값,int SECONDO_VALORE,int punto_di_codice,int meta_dati){
    if(proprietario_oggetto<0||proprietario_oggetto>=4)return -22;widget_Stato *너비값=elemento_VALORE(proprietario_oggetto,identificatore_VALORE);
    if(Azione==0){if(identificatore_VALORE<1||identificatore_VALORE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[proprietario_oggetto][순번].Valore_categoria==0){너비값=&요소들[proprietario_oggetto][순번];memset(너비값,0,sizeof(*너비값));너비값->Valore_categoria=identificatore_VALORE;너비값->보이는지=identificatore_VALORE!=1;너비값->너비값=identificatore_VALORE==1?380:220;너비값->richiesto_altezza_VALORE=identificatore_VALORE==1?240:28;너비값->Layout_norma=1;너비값->coordinata_x=identificatore_VALORE==1?130:16;너비값->Y_coordinata=identificatore_VALORE==1?110:16;return 순번+1;}return -28;}
    if(Azione==5){if(!voce_CONTA_NUMERI[proprietario_oggetto])return 0;int 반환값=evento_elenco[proprietario_oggetto][첫항목[proprietario_oggetto]];첫항목[proprietario_oggetto]=(첫항목[proprietario_oggetto]+1)%16;voce_CONTA_NUMERI[proprietario_oggetto]--;return 반환값;}
    if(Azione==6)return 화면보임(proprietario_oggetto);
    if(!너비값)return -9;
    int 이전표시=표시됨(proprietario_oggetto,너비값);
    if(Azione==1){int 바탕너비=보드화면너비(),sfondo_altezza=scheda_schermata_altezza();if(첫째값<0||SECONDO_VALORE<0||punto_di_codice<1||meta_dati<1||첫째값>바탕너비||SECONDO_VALORE>sfondo_altezza||punto_di_codice>바탕너비-첫째값||meta_dati>sfondo_altezza-SECONDO_VALORE)return -22;너비값->coordinata_x=첫째값;너비값->Y_coordinata=SECONDO_VALORE;너비값->너비값=punto_di_codice;너비값->richiesto_altezza_VALORE=meta_dati;너비값->manuale_Layout=1;}
    else if(Azione==2){widget_Stato *figlio=elemento_VALORE(proprietario_oggetto,첫째값);if(!figlio||figlio==너비값||figlio->Valore_categoria==1)return -22;int dati_funzione=identificatore_VALORE;for(int 깊이=0;dati_funzione&&깊이<32;깊이++){if(dati_funzione==첫째값)return -22;widget_Stato *위쪽=elemento_VALORE(proprietario_oggetto,dati_funzione);dati_funzione=위쪽?위쪽->padre:0;}figlio->padre=identificatore_VALORE;if(!figlio->manuale_Layout){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[proprietario_oggetto][순번]!=figlio&&요소들[proprietario_oggetto][순번].padre==identificatore_VALORE)형제요소++;figlio->Y_coordinata=16+형제요소*36;}}
    else if(Azione==3)너비값->보이는지=첫째값!=0;
    else if(Azione==4)너비값->보이는지=0;
    else if(Azione==7)너비값->Layout_norma=첫째값;
    else if(Azione==8)return 너비값->durata_VALORE;
    else if(Azione==9)return 첫째값>=0&&(unsigned)첫째값<너비값->durata_VALORE?너비값->testo[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(proprietario_oggetto,너비값))scheda_Terminale(3);return 0;
}
int schermata_SMS(int proprietario_oggetto,int identificatore_VALORE,const uint32_t *dati,unsigned articolo_CONTA_NUMERI){widget_Stato *너비값=elemento_VALORE(proprietario_oggetto,identificatore_VALORE);if(!너비값)return -9;if(articolo_CONTA_NUMERI>127)return -22;for(unsigned 순번=0;순번<articolo_CONTA_NUMERI;순번++){unsigned codifica_dei_caratteri=dati[순번];if(codifica_dei_caratteri>0x10ffff||(codifica_dei_caratteri>=0xd800&&codifica_dei_caratteri<=0xdfff))return -22;}for(unsigned 순번=0;순번<articolo_CONTA_NUMERI;순번++)너비값->testo[순번]=dati[순번];너비값->durata_VALORE=articolo_CONTA_NUMERI;if(표시됨(proprietario_oggetto,너비값))scheda_Terminale(3);return 0;}
