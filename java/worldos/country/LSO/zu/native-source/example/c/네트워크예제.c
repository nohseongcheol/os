#include "예제규약.h"
#include <통신규약.h>
int main(int 인수수,char **인수) {
    if(인수수!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned intuba_inani=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        intuba_inani=intuba_inani*10+인수[1][수]-'0';if(intuba_inani>65535)return 2;
    }
    if(!intuba_inani)return 2;
    int 종단=통신종단점만들기(I_cloud_Umndeni,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 ikheli={0};ikheli.ikheli_Umndeni=I_cloud_Umndeni;
    if(i_BIND_ikheli(종단,(struct 통신주소 *)&ikheli,sizeof(ikheli))<0)return 4;
    ikheli.접속번호=망차례짧은수(intuba_inani);ikheli.ikheli_le_inthanethi.ikheli_inani=iNethiwekhi_inamba(0x0a000202);
    const char 전문[]="C UDP zu";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&ikheli,sizeof(ikheli))!=sizeof(전문)-1)return 5;
    char phendula[512];unsigned Sebenzisa=밀리초();int 받은수;
    do {
        받은수=자료전문받기(종단,phendula,sizeof(phendula),0,0,0);
        if(받은수<0&&오류번호!=다시시도오류)return 6;
    } while(받은수<0&&(unsigned)(밀리초()-Sebenzisa)<700);
    vala_ifayela(종단);if(받은수!=sizeof(전문)-1)return 7;
    for(int 수=0;수<받은수;수++)if(전문[수]!=phendula[수])return 8;
    return 출력("C 네트워크 qiniseka: UDP zu\n");
}
