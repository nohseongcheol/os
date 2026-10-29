#include "예제규약.h"
int main(void) {
    const char data[]="C název_souboru: cs 😀\n";
    int název_souboru=otevřít_Soubor("c.txt",pro_čtení_i_zápis|없으면만들기|stříhat_Obsah,0600);
    if(název_souboru<0)return 1;
    if(zápis_Soubor_data(název_souboru,data,sizeof(data)-1)!=sizeof(data)-1)return 2;
    if(hledat_Soubor(název_souboru,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int délka_HODNOTA=파일자료읽기(název_souboru,읽은글,sizeof(읽은글)-1);
    Zavřít_Soubor(název_souboru);
    if(délka_HODNOTA!=sizeof(data)-1)return 4;
    for(int číslo=0;číslo<délka_HODNOTA;číslo++)if(data[číslo]!=읽은글[číslo])return 5;
    return výstupní_pozice(읽은글);
}
