#include "예제규약.h"
#include <통신규약.h>
int main(int 인수수,char **인수) {
    if(인수수!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned gorogisetsa_Boleng=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        gorogisetsa_Boleng=gorogisetsa_Boleng*10+인수[1][수]-'0';if(gorogisetsa_Boleng>65535)return 2;
    }
    if(!gorogisetsa_Boleng)return 2;
    int 종단=통신종단점만들기(tlelaote_Lelapa,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 aterese={0};aterese.aterese_Lelapa=tlelaote_Lelapa;
    if(BIND_aterese(종단,(struct 통신주소 *)&aterese,sizeof(aterese))<0)return 4;
    aterese.접속번호=망차례짧은수(gorogisetsa_Boleng);aterese.aterese_ya_Inthanete.aterese_Boleng=Neteweke_Palotlalo(0x0a000202);
    const char 전문[]="C UDP tn";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&aterese,sizeof(aterese))!=sizeof(전문)-1)return 5;
    char araba[512];unsigned dirisa=밀리초();int 받은수;
    do {
        받은수=자료전문받기(종단,araba,sizeof(araba),0,0,0);
        if(받은수<0&&오류번호!=다시시도오류)return 6;
    } while(받은수<0&&(unsigned)(밀리초()-dirisa)<700);
    tswala_faele(종단);if(받은수!=sizeof(전문)-1)return 7;
    for(int 수=0;수<받은수;수++)if(전문[수]!=araba[수])return 8;
    return 출력("C 네트워크 netefatsa: UDP tn\n");
}
