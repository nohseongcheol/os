#include "예제규약.h"
#include <통신규약.h>
int main(int 인수수,char **인수) {
    if(인수수!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned kituo_thamani=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        kituo_thamani=kituo_thamani*10+인수[1][수]-'0';if(kituo_thamani>65535)return 2;
    }
    if(!kituo_thamani)return 2;
    int 종단=통신종단점만들기(wingu_Familia,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 anwani={0};anwani.anwani_Familia=wingu_Familia;
    if(FUNGA_anwani(종단,(struct 통신주소 *)&anwani,sizeof(anwani))<0)return 4;
    anwani.namba_ya_kituo=망차례짧은수(kituo_thamani);anwani.Anwani_tovuti.anwani_thamani=Mtandao_namba_kamili(0x0a000202);
    const char 전문[]="C UDP sw";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&anwani,sizeof(anwani))!=sizeof(전문)-1)return 5;
    char jibu[512];unsigned endesha=밀리초();int 받은수;
    do {
        받은수=자료전문받기(종단,jibu,sizeof(jibu),0,0,0);
        if(받은수<0&&오류번호!=다시시도오류)return 6;
    } while(받은수<0&&(unsigned)(밀리초()-endesha)<700);
    funga_faili(종단);if(받은수!=sizeof(전문)-1)return 7;
    for(int 수=0;수<받은수;수++)if(전문[수]!=jibu[수])return 8;
    return 출력("C 네트워크 thibitisha: UDP sw\n");
}
