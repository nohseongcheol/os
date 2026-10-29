#include "예제규약.h"
int main(void) {
    const char data[]="C Fil: Norwegian Bokmål 😀\n";
    int Fil=åpen_Fil("c.txt",lese_og_skrive|없으면만들기|avkorte_Innhold,0600);
    if(Fil<0)return 1;
    if(skrive_Fil_data(Fil,data,sizeof(data)-1)!=sizeof(data)-1)return 2;
    if(søk_Fil(Fil,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int lengde_VERDI=파일자료읽기(Fil,읽은글,sizeof(읽은글)-1);
    Lukk_Fil(Fil);
    if(lengde_VERDI!=sizeof(data)-1)return 4;
    for(int nummer=0;nummer<lengde_VERDI;nummer++)if(data[nummer]!=읽은글[nummer])return 5;
    return Utgang(읽은글);
}
