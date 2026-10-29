#include "예제규약.h"
#include <통신규약.h>
int main(int argument_COUNT,char **인수) {
    if(argument_COUNT!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned port_VALUE=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        port_VALUE=port_VALUE*10+인수[1][수]-'0';if(port_VALUE>65535)return 2;
    }
    if(!port_VALUE)return 2;
    int 종단=통신종단점만들기(cloud_Familja,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 ADDRESS={0};ADDRESS.ADDRESS_Familja=cloud_Familja;
    if(BIND_ADDRESS(종단,(struct 통신주소 *)&ADDRESS,sizeof(ADDRESS))<0)return 4;
    ADDRESS.접속번호=망차례짧은수(port_VALUE);ADDRESS.indirizz_tal_Internet.ADDRESS_VALUE=netwerk_numru_sħiħ(0x0a000202);
    const char 전문[]="C UDP mt";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&ADDRESS,sizeof(ADDRESS))!=sizeof(전문)-1)return 5;
    char wieġeb[512];unsigned serje=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=자료전문받기(종단,wieġeb,sizeof(wieġeb),0,0,0);
        if(RECEIVED_COUNT<0&&오류번호!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-serje)<700);
    agħlaq_fajl(종단);if(RECEIVED_COUNT!=sizeof(전문)-1)return 7;
    for(int 수=0;수<RECEIVED_COUNT;수++)if(전문[수]!=wieġeb[수])return 8;
    return 출력("C 네트워크 vverifika: UDP mt\n");
}
