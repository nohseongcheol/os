#include "예제규약.h"
#include <통신규약.h>
int main(int argument_COUNT,char **Argumendid) {
    if(argument_COUNT!=2)return Väljund("사용법: ./네트워크 UDP창구번호\n");
    unsigned port_VALUE=0;for(int number=0;Argumendid[1][number];number++) {
        if(Argumendid[1][number]<'0'||Argumendid[1][number]>'9')return 2;
        port_VALUE=port_VALUE*10+Argumendid[1][number]-'0';if(port_VALUE>65535)return 2;
    }
    if(!port_VALUE)return 2;
    int osaleja=avama_osaleja(pilv_Pere,datagrammisokkel,datagramm_protokoll);if(osaleja<0)return 3;
    struct 인터넷통신주소 ADDRESS={0};ADDRESS.ADDRESS_Pere=pilv_Pere;
    if(BIND_ADDRESS(osaleja,(struct 통신주소 *)&ADDRESS,sizeof(ADDRESS))<0)return 4;
    ADDRESS.pordinumber=망차례짧은수(port_VALUE);ADDRESS.Interneti_aadress.ADDRESS_VALUE=võrk_täisarv(0x0a000202);
    const char datagramm[]="C UDP et";
    if(saatma_datagramm_andmed(osaleja,datagramm,sizeof(datagramm)-1,0,(struct 통신주소 *)&ADDRESS,sizeof(ADDRESS))!=sizeof(datagramm)-1)return 5;
    char vastus[512];unsigned Käivita_2=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=saama_datagramm_andmed(osaleja,vastus,sizeof(vastus),0,0,0);
        if(RECEIVED_COUNT<0&&tõrke_number!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-Käivita_2)<700);
    Sule_Fail(osaleja);if(RECEIVED_COUNT!=sizeof(datagramm)-1)return 7;
    for(int number=0;number<RECEIVED_COUNT;number++)if(datagramm[number]!=vastus[number])return 8;
    return Väljund("C 네트워크 kinnitama: UDP et\n");
}
