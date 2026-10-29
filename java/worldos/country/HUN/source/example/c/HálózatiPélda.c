#include "예제규약.h"
#include <통신규약.h>
int main(int argumentum_DARAB,char **Argumentumok) {
    if(argumentum_DARAB!=2)return Kimenet("사용법: ./네트워크 UDP창구번호\n");
    unsigned port_ÉRTÉK=0;for(int szám=0;Argumentumok[1][szám];szám++) {
        if(Argumentumok[1][szám]<'0'||Argumentumok[1][szám]>'9')return 2;
        port_ÉRTÉK=port_ÉRTÉK*10+Argumentumok[1][szám]-'0';if(port_ÉRTÉK>65535)return 2;
    }
    if(!port_ÉRTÉK)return 2;
    int végpont=készít_végpont(háló_Család,datagram_szoftvercsatorna,datagram_protokoll);if(végpont<0)return 3;
    struct háló_szoftvercsatorna_CÍM CÍM={0};CÍM.CÍM_Család=háló_Család;
    if(BIND_CÍM(végpont,(struct szoftvercsatorna_CÍM *)&CÍM,sizeof(CÍM))<0)return 4;
    CÍM.portszám=망차례짧은수(port_ÉRTÉK);CÍM.internetcím.CÍM_ÉRTÉK=hálózat_egész_szám(0x0a000202);
    const char datagram[]="C UDP magyar";
    if(küld_datagram_adat(végpont,datagram,sizeof(datagram)-1,0,(struct szoftvercsatorna_CÍM *)&CÍM,sizeof(CÍM))!=sizeof(datagram)-1)return 5;
    char válasz[512];unsigned Futtatás=밀리초();int KAPOTT_DARAB;
    do {
        KAPOTT_DARAB=fogad_datagram_adat(végpont,válasz,sizeof(válasz),0,0,0);
        if(KAPOTT_DARAB<0&&hibaszám!=다시시도오류)return 6;
    } while(KAPOTT_DARAB<0&&(unsigned)(밀리초()-Futtatás)<700);
    bezár_Fájl(végpont);if(KAPOTT_DARAB!=sizeof(datagram)-1)return 7;
    for(int szám=0;szám<KAPOTT_DARAB;szám++)if(datagram[szám]!=válasz[szám])return 8;
    return Kimenet("C 네트워크 igazol: UDP magyar\n");
}
