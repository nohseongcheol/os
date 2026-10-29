#include "예제규약.h"
#include <통신규약.h>
int main(int arg_COUNT,char **인수) {
    if(arg_COUNT!=2)return Allbwn("사용법: ./네트워크 UDP창구번호\n");
    unsigned porth_VALUE=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        porth_VALUE=porth_VALUE*10+인수[1][수]-'0';if(porth_VALUE>65535)return 2;
    }
    if(!porth_VALUE)return 2;
    int 종단=통신종단점만들기(cwmwl_Teulu,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 ADDRESS={0};ADDRESS.ADDRESS_Teulu=cwmwl_Teulu;
    if(BIND_ADDRESS(종단,(struct 통신주소 *)&ADDRESS,sizeof(ADDRESS))<0)return 4;
    ADDRESS.rhif_porth=망차례짧은수(porth_VALUE);ADDRESS.cyfeiriad_rhyngrwyd.ADDRESS_VALUE=Rhwydwaith_cyfanrif(0x0a000202);
    const char 전문[]="C UDP cy";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&ADDRESS,sizeof(ADDRESS))!=sizeof(전문)-1)return 5;
    char ateb[512];unsigned Gweithredu_2=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=자료전문받기(종단,ateb,sizeof(ateb),0,0,0);
        if(RECEIVED_COUNT<0&&오류번호!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-Gweithredu_2)<700);
    cau_ffeil(종단);if(RECEIVED_COUNT!=sizeof(전문)-1)return 7;
    for(int 수=0;수<RECEIVED_COUNT;수++)if(전문[수]!=ateb[수])return 8;
    return Allbwn("C 네트워크 dilysu: UDP cy\n");
}
