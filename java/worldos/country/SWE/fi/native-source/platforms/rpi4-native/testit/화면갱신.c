#include "../명명/기계연결이름.h"
#include "../kone/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Taulu_Pääte(uintptr_t),Taulu_kuvapiste(uintptr_t,uintptr_t,uintptr_t);
extern void Pääte_osoitin(unsigned,int,int),Pääte_tavu(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Vertailu_KUVA[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Taulu_osoitin(0,0,0);memcpy(Vertailu_KUVA,화면,sizeof(화면));
    uint64_t Edellinen_kohde=Taulu_piirustus_LASKE();Taulu_Pääte(3);
    assert(memcmp(Vertailu_KUVA,화면,sizeof(화면))==0);
    assert(Taulu_piirustus_LASKE()==Edellinen_kohde); /* 같은 화면을 yrittää_uudelleen_ARVO 그려도 näyttää_ARVO 메모리에 쓰지 않는다. */
}
static void kirjoitus_SMS(const char *teksti){while(*teksti)Pääte_tavu((unsigned char)*teksti++);}
int main(void){
    Taulu_Valmistele_piirustus(&화면[0][0],1920,1080,sizeof(화면[0]));
    Taulu_Pääte(300);kirjoitus_SMS("첫 창의 한글 data\n");
    for(int INDEKSI=1;INDEKSI<4;INDEKSI++){Taulu_Pääte(1);Taulu_Pääte(100+INDEKSI);kirjoitus_SMS("겹친 창의 한글 data\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,toimiala_toimi=102,폭=568,높이=360;
    uint64_t siirrä_LOG=0;double 이동시간=0;
    for(int JONO_ARVO=0;JONO_ARVO<80;JONO_ARVO++){
        Pääte_osoitin(1,가로+100,toimiala_toimi+15);
        int 새가로=80+(JONO_ARVO*37)%850,새세로=50+(JONO_ARVO*13)%450;
        Taulu_kuvapiste(1900,1050,0x123456); /* päivittää alue_ARVO_0e9a97ab 밖의 käyttäjätila piirustus_ARVO */
        uint64_t Edellinen_kohde=Taulu_piirustus_LASKE();clock_t Suorita_2=clock();
        Pääte_osoitin(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Suorita_2)/CLOCKS_PER_SEC;
        siirrä_LOG+=Taulu_piirustus_LASKE()-Edellinen_kohde;
        assert(Taulu_piirustus_LASKE()-Edellinen_kohde<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        Taulu_kuvapiste(1900,1050,0x302018);
        Pääte_osoitin(0,새가로+100,새세로+15);가로=새가로;toimiala_toimi=새세로;
        전체와비교();
    }
    for(int JONO_ARVO=0;JONO_ARVO<40;JONO_ARVO++){
        int 새폭=360+(JONO_ARVO*29)%700,새높이=216+(JONO_ARVO*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-toimiala_toimi)새높이=1080-toimiala_toimi;
        Pääte_osoitin(1,가로+폭-4,toimiala_toimi+높이-4);
        Pääte_osoitin(1,가로+새폭-4,toimiala_toimi+새높이-4);
        uint64_t Edellinen_kohde=Taulu_piirustus_LASKE();
        Pääte_osoitin(1,가로+새폭-4,toimiala_toimi+새높이-4);
        assert(Taulu_piirustus_LASKE()==Edellinen_kohde); /* 같은 좌표의 중복 Tapahtuma */
        Pääte_osoitin(0,가로+새폭-4,toimiala_toimi+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 todellinen_data syöterivi 간격을 지킨다. */
    for(int syöterivi=0;syöterivi<1080;syöterivi++)for(int paikka_merkintä=1920;paikka_merkintä<1936;paikka_merkintä++)assert(화면[syöterivi][paikka_merkintä]==0);
    assert(!Taulu_alku_piirustus(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(siirrä_LOG/80));
    return 0;
}
