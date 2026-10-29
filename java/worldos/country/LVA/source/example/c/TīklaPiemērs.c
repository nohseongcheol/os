#include "예제규약.h"
#include <통신규약.h>
int main(int arg_COUNT,char **Parametri) {
    if(arg_COUNT!=2)return Izvade("사용법: ./네트워크 UDP창구번호\n");
    unsigned ports_VALUE=0;for(int numurs=0;Parametri[1][numurs];numurs++) {
        if(Parametri[1][numurs]<'0'||Parametri[1][numurs]>'9')return 2;
        ports_VALUE=ports_VALUE*10+Parametri[1][numurs]-'0';if(ports_VALUE>65535)return 2;
    }
    if(!ports_VALUE)return 2;
    int dalībnieks=atvērt_dalībnieks(mākonis_saime,datogrammas_ligzda,datogramma_protokols);if(dalībnieks<0)return 3;
    struct 인터넷통신주소 adrese={0};adrese.adrese_saime=mākonis_saime;
    if(BIND_adrese(dalībnieks,(struct 통신주소 *)&adrese,sizeof(adrese))<0)return 4;
    adrese.porta_numurs=망차례짧은수(ports_VALUE);adrese.interneta_adrese.adrese_VALUE=tīkls_vesels_skaitlis(0x0a000202);
    const char datogramma[]="C UDP Latviešu";
    if(sūtīt_datogramma_dati(dalībnieks,datogramma,sizeof(datogramma)-1,0,(struct 통신주소 *)&adrese,sizeof(adrese))!=sizeof(datogramma)-1)return 5;
    char atbilde[512];unsigned Palaist=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=saņemt_datogramma_dati(dalībnieks,atbilde,sizeof(atbilde),0,0,0);
        if(RECEIVED_COUNT<0&&kļūdas_numurs!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-Palaist)<700);
    Aizvērt_Fails(dalībnieks);if(RECEIVED_COUNT!=sizeof(datogramma)-1)return 7;
    for(int numurs=0;numurs<RECEIVED_COUNT;numurs++)if(datogramma[numurs]!=atbilde[numurs])return 8;
    return Izvade("C 네트워크 verificēt: UDP Latviešu\n");
}
