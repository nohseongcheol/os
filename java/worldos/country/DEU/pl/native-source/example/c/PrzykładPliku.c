#include "예제규약.h"
int main(void) {
    const char dane[]="C nazwa_pliku: pl 😀\n";
    int nazwa_pliku=otwarty_Plik("c.txt",R_W|없으면만들기|obcinać_Spis_treści,0600);
    if(nazwa_pliku<0)return 1;
    if(zapis_Plik_dane(nazwa_pliku,dane,sizeof(dane)-1)!=sizeof(dane)-1)return 2;
    if(szukać_Plik(nazwa_pliku,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int długość_WARTOŚĆ=파일자료읽기(nazwa_pliku,읽은글,sizeof(읽은글)-1);
    Zamknij_Plik(nazwa_pliku);
    if(długość_WARTOŚĆ!=sizeof(dane)-1)return 4;
    for(int identyfikator=0;identyfikator<długość_WARTOŚĆ;identyfikator++)if(dane[identyfikator]!=읽은글[identyfikator])return 5;
    return pozycja_wyjścia(읽은글);
}
