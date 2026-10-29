#include "../명명/기계연결이름.h"
#include "../computer/schermata_info.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t scheda_Terminale(uintptr_t),scheda_pixel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminale_puntatore(unsigned,int,int),Terminale_byte(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t schermata[1080][1936],Confronto_foto[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    scheda_puntatore(0,0,0);memcpy(Confronto_foto,schermata,sizeof(schermata));
    uint64_t Indietro_articolo=scheda_disegno_CONTA_NUMERI();scheda_Terminale(3);
    assert(memcmp(Confronto_foto,schermata,sizeof(schermata))==0);
    assert(scheda_disegno_CONTA_NUMERI()==Indietro_articolo); /* 같은 화면을 retry_VALORE 그려도 mostrare_VALORE 메모리에 쓰지 않는다. */
}
static void scrivere_SMS(const char *testo){while(*testo)Terminale_byte((unsigned char)*testo++);}
int main(void){
    scheda_Prepara_disegno(&schermata[0][0],1920,1080,sizeof(schermata[0]));
    scheda_Terminale(300);scrivere_SMS("첫 창의 한글 dati\n");
    for(int INDICE=1;INDICE<4;INDICE++){scheda_Terminale(1);scheda_Terminale(100+INDICE);scrivere_SMS("겹친 창의 한글 dati\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Verticale_funzione=102,폭=568,altezza_VALORE=360;
    uint64_t spostare_LOG=0;double 이동시간=0;
    for(int SEQUENZA_VALORE=0;SEQUENZA_VALORE<80;SEQUENZA_VALORE++){
        Terminale_puntatore(1,가로+100,Verticale_funzione+15);
        int 새가로=80+(SEQUENZA_VALORE*37)%850,새세로=50+(SEQUENZA_VALORE*13)%450;
        scheda_pixel(1900,1050,0x123456); /* aggiornare area_VALORE 밖의 spazio_utente disegno_VALORE */
        uint64_t Indietro_articolo=scheda_disegno_CONTA_NUMERI();clock_t avvia=clock();
        Terminale_puntatore(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-avvia)/CLOCKS_PER_SEC;
        spostare_LOG+=scheda_disegno_CONTA_NUMERI()-Indietro_articolo;
        assert(scheda_disegno_CONTA_NUMERI()-Indietro_articolo<=2u*폭*altezza_VALORE);
        assert(schermata[1050][1900]==0x123456);
        scheda_pixel(1900,1050,0x302018);
        Terminale_puntatore(0,새가로+100,새세로+15);가로=새가로;Verticale_funzione=새세로;
        전체와비교();
    }
    for(int SEQUENZA_VALORE=0;SEQUENZA_VALORE<40;SEQUENZA_VALORE++){
        int 새폭=360+(SEQUENZA_VALORE*29)%700,새높이=216+(SEQUENZA_VALORE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Verticale_funzione)새높이=1080-Verticale_funzione;
        Terminale_puntatore(1,가로+폭-4,Verticale_funzione+altezza_VALORE-4);
        Terminale_puntatore(1,가로+새폭-4,Verticale_funzione+새높이-4);
        uint64_t Indietro_articolo=scheda_disegno_CONTA_NUMERI();
        Terminale_puntatore(1,가로+새폭-4,Verticale_funzione+새높이-4);
        assert(scheda_disegno_CONTA_NUMERI()==Indietro_articolo); /* 같은 좌표의 중복 Evento */
        Terminale_puntatore(0,가로+새폭-4,Verticale_funzione+새높이-4);폭=새폭;altezza_VALORE=새높이;
        전체와비교();
    }
    /* 잘린 범위와 effettivo_dati riga_di_ingresso 간격을 지킨다. */
    for(int riga_di_ingresso=0;riga_di_ingresso<1080;riga_di_ingresso++)for(int slot_voce=1920;slot_voce<1936;slot_voce++)assert(schermata[riga_di_ingresso][slot_voce]==0);
    assert(!scheda_START_disegno(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(spostare_LOG/80));
    return 0;
}
