#include "예제규약.h"
#include <통신규약.h>
int main(int frumbreyta_COUNT,char **Viðföng) {
    if(frumbreyta_COUNT!=2)return úttak("사용법: ./네트워크 UDP창구번호\n");
    unsigned gátt_VALUE=0;for(int númer=0;Viðföng[1][númer];númer++) {
        if(Viðföng[1][númer]<'0'||Viðföng[1][númer]>'9')return 2;
        gátt_VALUE=gátt_VALUE*10+Viðföng[1][númer]-'0';if(gátt_VALUE>65535)return 2;
    }
    if(!gátt_VALUE)return 2;
    int endastöð=stofna_endastöð(skýið_Fjölskylda,전문통신,전문전송규약);if(endastöð<0)return 3;
    struct 인터넷통신주소 slóð={0};slóð.slóð_Fjölskylda=skýið_Fjölskylda;
    if(BIND_slóð(endastöð,(struct 통신주소 *)&slóð,sizeof(slóð))<0)return 4;
    slóð.tengisnúmer=망차례짧은수(gátt_VALUE);slóð.veffang.slóð_VALUE=Net_heiltala(0x0a000202);
    const char 전문[]="C UDP is";
    if(자료전문보내기(endastöð,전문,sizeof(전문)-1,0,(struct 통신주소 *)&slóð,sizeof(slóð))!=sizeof(전문)-1)return 5;
    char svara[512];unsigned Keyra_2=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=자료전문받기(endastöð,svara,sizeof(svara),0,0,0);
        if(RECEIVED_COUNT<0&&villa_númer!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-Keyra_2)<700);
    loka_skrá(endastöð);if(RECEIVED_COUNT!=sizeof(전문)-1)return 7;
    for(int númer=0;númer<RECEIVED_COUNT;númer++)if(전문[númer]!=svara[númer])return 8;
    return úttak("C 네트워크 sannprófa: UDP is\n");
}
