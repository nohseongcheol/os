#include "예제규약.h"
int main(void) {
    const char datuak[]="C Fitxategia: eu 😀\n";
    int Fitxategia=ireki_fitxategi("c.txt",irakurri_idatzi|없으면만들기|내용비우기,0600);
    if(Fitxategia<0)return 1;
    if(idatzi_fitxategi_datuak(Fitxategia,datuak,sizeof(datuak)-1)!=sizeof(datuak)-1)return 2;
    if(bilatu_fitxategi(Fitxategia,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int luzera_balio=파일자료읽기(Fitxategia,읽은글,sizeof(읽은글)-1);
    itxi_fitxategi(Fitxategia);
    if(luzera_balio!=sizeof(datuak)-1)return 4;
    for(int 수=0;수<luzera_balio;수++)if(datuak[수]!=읽은글[수])return 5;
    return Irteera(읽은글);
}
