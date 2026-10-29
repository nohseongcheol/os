#include "예제규약.h"
int main(void) {
    const char gegevens[]="C bestand: Nederlands 😀\n";
    int bestand=open_Bestand("c.txt",lezen_schrijven|없으면만들기|afkappen_Inhoud,0600);
    if(bestand<0)return 1;
    if(schrijven_Bestand_gegevens(bestand,gegevens,sizeof(gegevens)-1)!=sizeof(gegevens)-1)return 2;
    if(zoeken_Bestand(bestand,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int tijdsduur_WAARDE=파일자료읽기(bestand,읽은글,sizeof(읽은글)-1);
    Sluiten_Bestand(bestand);
    if(tijdsduur_WAARDE!=sizeof(gegevens)-1)return 4;
    for(int nummer=0;nummer<tijdsduur_WAARDE;nummer++)if(gegevens[nummer]!=읽은글[nummer])return 5;
    return tekstuitvoer(읽은글);
}
