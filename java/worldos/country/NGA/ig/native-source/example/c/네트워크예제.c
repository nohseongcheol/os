#include "예제규약.h"
#include <통신규약.h>
int main(int 인수수,char **인수) {
    if(인수수!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned pọọt_valuu=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        pọọt_valuu=pọọt_valuu*10+인수[1][수]-'0';if(pọọt_valuu>65535)return 2;
    }
    if(!pọọt_valuu)return 2;
    int 종단=통신종단점만들기(urukpu_Ezinụlọ,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 àdreèsì={0};àdreèsì.àdreèsì_Ezinụlọ=urukpu_Ezinụlọ;
    if(JIKỌNYE_àdreèsì(종단,(struct 통신주소 *)&àdreèsì,sizeof(àdreèsì))<0)return 4;
    àdreèsì.접속번호=망차례짧은수(pọọt_valuu);àdreèsì.adreesi_ịntaneèt.àdreèsì_valuu=Netwọọkụ_ọnụọgụ_nzùrùòkè(0x0a000202);
    const char 전문[]="C UDP ig";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&àdreèsì,sizeof(àdreèsì))!=sizeof(전문)-1)return 5;
    char nzaghachi[512];unsigned Bido=밀리초();int 받은수;
    do {
        받은수=자료전문받기(종단,nzaghachi,sizeof(nzaghachi),0,0,0);
        if(받은수<0&&오류번호!=다시시도오류)return 6;
    } while(받은수<0&&(unsigned)(밀리초()-Bido)<700);
    mmechi_ọbọakwụkwọ(종단);if(받은수!=sizeof(전문)-1)return 7;
    for(int 수=0;수<받은수;수++)if(전문[수]!=nzaghachi[수])return 8;
    return 출력("C 네트워크 nkwàdo_eziokwū: UDP ig\n");
}
