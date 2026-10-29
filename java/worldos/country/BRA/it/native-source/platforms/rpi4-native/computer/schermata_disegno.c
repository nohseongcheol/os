/* effettivo_dati schermata 메모리와 기존 C 호출 규약만 연결한다. 합성 구현은 codiceSorgente/화면합성.java. */
#include "../명명/기계연결이름.h"
#include "schermata_info.h"
static volatile uint32_t *화소들;
static unsigned schermata_riga_Conteggio_parole, 화면너비, schermata_altezza;
extern void 자바그림준비(int,int),자바그림마침(void),자바사각그림(int,int,int,int,int),자바포인터(int,int,int);
extern int 자바그림너비(void),자바그림높이(void),자바그림기록아래(void),자바그림기록위(void);
extern int 자바그림범위(int,int,int,int),자바그림범위값(int),자바그림시작(int,int,int,int),자바그림화소(int,int,int);
uintptr_t 보드표시화소읽기(uintptr_t 가로,uintptr_t Verticale_funzione){
    return 화소들&&가로<화면너비&&Verticale_funzione<schermata_altezza?화소들[Verticale_funzione*schermata_riga_Conteggio_parole+가로]:0;
}
void 보드표시화소쓰기(uintptr_t 가로,uintptr_t Verticale_funzione,uintptr_t 색){
    if(화소들&&가로<화면너비&&Verticale_funzione<schermata_altezza)화소들[Verticale_funzione*schermata_riga_Conteggio_parole+가로]=(uint32_t)색;
}
void scheda_Prepara_disegno(volatile uint32_t *dati,unsigned 폭,unsigned durata_VALORE,unsigned interlinea_VALORE){
    화소들=dati;화면너비=폭;schermata_altezza=durata_VALORE;schermata_riga_Conteggio_parole=interlinea_VALORE/4;자바그림준비((int)폭,(int)durata_VALORE);
}
uintptr_t 보드화면너비(void){return (unsigned)자바그림너비();}
uintptr_t scheda_schermata_altezza(void){return (unsigned)자바그림높이();}
uint64_t scheda_disegno_CONTA_NUMERI(void){return ((uint64_t)(uint32_t)자바그림기록위()<<32)|(uint32_t)자바그림기록아래();}
uint32_t 보드화면읽기(unsigned 가로,unsigned Verticale_funzione){return (uint32_t)보드표시화소읽기(가로,Verticale_funzione);}
int 보드그림범위(int *가로,int *Verticale_funzione,int *폭,int *durata_VALORE){
    if(!자바그림범위(*가로,*Verticale_funzione,*폭,*durata_VALORE))return 0;
    *가로=자바그림범위값(0);*Verticale_funzione=자바그림범위값(1);*폭=자바그림범위값(2);*durata_VALORE=자바그림범위값(3);return 1;
}
int scheda_START_disegno(int 가로,int Verticale_funzione,int 폭,int durata_VALORE){return 자바그림시작(가로,Verticale_funzione,폭,durata_VALORE);}
void scheda_Fine_disegno(void){자바그림마침();}
uintptr_t scheda_pixel(uintptr_t 가로,uintptr_t Verticale_funzione,uintptr_t 색){return (unsigned)자바그림화소((int)가로,(int)Verticale_funzione,(int)색);}
void scheda_rettangolo_Riempi(int 가로,int Verticale_funzione,int 폭,int durata_VALORE,uint32_t 색){자바사각그림(가로,Verticale_funzione,폭,durata_VALORE,(int)색);}
void scheda_puntatore(int 가로,int Verticale_funzione,unsigned forma_VALORE){자바포인터(가로,Verticale_funzione,(int)forma_VALORE);}
