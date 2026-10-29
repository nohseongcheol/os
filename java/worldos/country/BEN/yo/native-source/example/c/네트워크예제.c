#include "예제규약.h"
#include <통신규약.h>
int main(int 인수수,char **인수) {
    if(인수수!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned ojú_iye=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        ojú_iye=ojú_iye*10+인수[1][수]-'0';if(ojú_iye>65535)return 2;
    }
    if(!ojú_iye)return 2;
    int 종단=통신종단점만들기(Íntánẹ́ẹ̀tì_Ẹbí,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 àdírẹ́ẹ̀sì={0};àdírẹ́ẹ̀sì.àdírẹ́ẹ̀sì_Ẹbí=Íntánẹ́ẹ̀tì_Ẹbí;
    if(BIND_àdírẹ́ẹ̀sì(종단,(struct 통신주소 *)&àdírẹ́ẹ̀sì,sizeof(àdírẹ́ẹ̀sì))<0)return 4;
    àdírẹ́ẹ̀sì.접속번호=망차례짧은수(ojú_iye);àdírẹ́ẹ̀sì.àdíréẹ̀sì_íntánẹ́ẹ̀tì.àdírẹ́ẹ̀sì_iye=Alásopọ̀_nọ́ńbà_odindi(0x0a000202);
    const char 전문[]="C UDP yo";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&àdírẹ́ẹ̀sì,sizeof(àdírẹ́ẹ̀sì))!=sizeof(전문)-1)return 5;
    char Fèsì[512];unsigned Rọ́ọ̀nù=밀리초();int 받은수;
    do {
        받은수=자료전문받기(종단,Fèsì,sizeof(Fèsì),0,0,0);
        if(받은수<0&&오류번호!=다시시도오류)return 6;
    } while(받은수<0&&(unsigned)(밀리초()-Rọ́ọ̀nù)<700);
    pa_dé_fáìlì(종단);if(받은수!=sizeof(전문)-1)return 7;
    for(int 수=0;수<받은수;수++)if(전문[수]!=Fèsì[수])return 8;
    return 출력("C 네트워크 ridájú: UDP yo\n");
}
