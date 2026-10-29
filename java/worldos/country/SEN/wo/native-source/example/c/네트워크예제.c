#include "예제규약.h"
#include <통신규약.h>
int main(int 인수수,char **인수) {
    if(인수수!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned jël_xëyma=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        jël_xëyma=jël_xëyma*10+인수[1][수]-'0';if(jël_xëyma>65535)return 2;
    }
    if(!jël_xëyma)return 2;
    int 종단=통신종단점만들기(net_Njaboot,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 dëkkuwaay={0};dëkkuwaay.dëkkuwaay_Njaboot=net_Njaboot;
    if(BIND_dëkkuwaay(종단,(struct 통신주소 *)&dëkkuwaay,sizeof(dëkkuwaay))<0)return 4;
    dëkkuwaay.접속번호=망차례짧은수(jël_xëyma);dëkkuwaay.dëkkuwaayu_Internet.dëkkuwaay_xëyma=mbaal_lëmm(0x0a000202);
    const char 전문[]="C UDP wo";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&dëkkuwaay,sizeof(dëkkuwaay))!=sizeof(전문)-1)return 5;
    char tontu[512];unsigned daw=밀리초();int 받은수;
    do {
        받은수=자료전문받기(종단,tontu,sizeof(tontu),0,0,0);
        if(받은수<0&&오류번호!=다시시도오류)return 6;
    } while(받은수<0&&(unsigned)(밀리초()-daw)<700);
    Tej_bara_denc(종단);if(받은수!=sizeof(전문)-1)return 7;
    for(int 수=0;수<받은수;수++)if(전문[수]!=tontu[수])return 8;
    return 출력("C 네트워크 luñutu: UDP wo\n");
}
