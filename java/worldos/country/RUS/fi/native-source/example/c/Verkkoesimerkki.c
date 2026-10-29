#include "예제규약.h"
#include <통신규약.h>
int main(int argumentti_LASKE,char **argumentit) {
    if(argumentti_LASKE!=2)return tulostuspaikka("사용법: ./네트워크 UDP창구번호\n");
    unsigned portti_ARVO=0;for(int numero=0;argumentit[1][numero];numero++) {
        if(argumentit[1][numero]<'0'||argumentit[1][numero]>'9')return 2;
        portti_ARVO=portti_ARVO*10+argumentit[1][numero]-'0';if(portti_ARVO>65535)return 2;
    }
    if(!portti_ARVO)return 2;
    int päätepiste=Luo_päätepiste(pilvi_Perhe,datagrammivastake,datagrammi_protokolla);if(päätepiste<0)return 3;
    struct pilvi_vastake_OSOITE OSOITE={0};OSOITE.OSOITE_Perhe=pilvi_Perhe;
    if(BIND_OSOITE(päätepiste,(struct vastake_OSOITE *)&OSOITE,sizeof(OSOITE))<0)return 4;
    OSOITE.portin_numero=망차례짧은수(portti_ARVO);OSOITE.Internet_osoite.OSOITE_ARVO=verkko_kokonaisluku(0x0a000202);
    const char datagrammi[]="C UDP fi";
    if(lähettää_datagrammi_data(päätepiste,datagrammi,sizeof(datagrammi)-1,0,(struct vastake_OSOITE *)&OSOITE,sizeof(OSOITE))!=sizeof(datagrammi)-1)return 5;
    char palaute[512];unsigned Suorita_2=밀리초();int SAATU_HINTA_LASKE;
    do {
        SAATU_HINTA_LASKE=saada_datagrammi_data(päätepiste,palaute,sizeof(palaute),0,0,0);
        if(SAATU_HINTA_LASKE<0&&virhenumero!=다시시도오류)return 6;
    } while(SAATU_HINTA_LASKE<0&&(unsigned)(밀리초()-Suorita_2)<700);
    Sulje_Tiedosto(päätepiste);if(SAATU_HINTA_LASKE!=sizeof(datagrammi)-1)return 7;
    for(int numero=0;numero<SAATU_HINTA_LASKE;numero++)if(datagrammi[numero]!=palaute[numero])return 8;
    return tulostuspaikka("C 네트워크 tarkistaa: UDP fi\n");
}
