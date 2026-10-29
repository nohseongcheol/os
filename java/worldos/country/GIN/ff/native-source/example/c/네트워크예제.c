#include "예제규약.h"
#include <통신규약.h>
int main(int 인수수,char **인수) {
    if(인수수!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned poor_njaru=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        poor_njaru=poor_njaru*10+인수[1][수]-'0';if(poor_njaru>65535)return 2;
    }
    if(!poor_njaru)return 2;
    int 종단=통신종단점만들기(인터넷주소갈래,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 ñiiɓirde={0};ñiiɓirde.주소갈래=인터넷주소갈래;
    if(seŋondir_ñiiɓirde(종단,(struct 통신주소 *)&ñiiɓirde,sizeof(ñiiɓirde))<0)return 4;
    ñiiɓirde.접속번호=망차례짧은수(poor_njaru);ñiiɓirde.ñiiɓirde_enternet.ñiiɓirde_njaru=망차례정수(0x0a000202);
    const char 전문[]="C UDP ff";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&ñiiɓirde,sizeof(ñiiɓirde))!=sizeof(전문)-1)return 5;
    char 응답[512];unsigned huutoraade=밀리초();int 받은수;
    do {
        받은수=자료전문받기(종단,응답,sizeof(응답),0,0,0);
        if(받은수<0&&오류번호!=다시시도오류)return 6;
    } while(받은수<0&&(unsigned)(밀리초()-huutoraade)<700);
    uddude_fiilde(종단);if(받은수!=sizeof(전문)-1)return 7;
    for(int 수=0;수<받은수;수++)if(전문[수]!=응답[수])return 8;
    return 출력("C 네트워크 ƴeewtaade: UDP ff\n");
}
