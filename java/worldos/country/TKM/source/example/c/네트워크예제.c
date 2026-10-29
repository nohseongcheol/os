#include "예제규약.h"
#include <통신규약.h>
int main(int 인수수,char **인수) {
    if(인수수!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned port_baha=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        port_baha=port_baha*10+인수[1][수]-'0';if(port_baha>65535)return 2;
    }
    if(!port_baha)return 2;
    int 종단=통신종단점만들기(bulut_Maşgala,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 salgy={0};salgy.salgy_Maşgala=bulut_Maşgala;
    if(BIND_salgy(종단,(struct 통신주소 *)&salgy,sizeof(salgy))<0)return 4;
    salgy.접속번호=망차례짧은수(port_baha);salgy.Internet_salgy.salgy_baha=Tor_bitin(0x0a000202);
    const char 전문[]="C UDP Turkmen";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&salgy,sizeof(salgy))!=sizeof(전문)-1)return 5;
    char jogap_bermek[512];unsigned Bitir=밀리초();int 받은수;
    do {
        받은수=자료전문받기(종단,jogap_bermek,sizeof(jogap_bermek),0,0,0);
        if(받은수<0&&오류번호!=다시시도오류)return 6;
    } while(받은수<0&&(unsigned)(밀리초()-Bitir)<700);
    ýap_faýl(종단);if(받은수!=sizeof(전문)-1)return 7;
    for(int 수=0;수<받은수;수++)if(전문[수]!=jogap_bermek[수])return 8;
    return 출력("C 네트워크 barla: UDP Turkmen\n");
}
