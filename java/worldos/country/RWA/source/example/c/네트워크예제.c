#include "예제규약.h"
#include <통신규약.h>
int main(int 인수수,char **인수) {
    if(인수수!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned poti_agaciro=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        poti_agaciro=poti_agaciro*10+인수[1][수]-'0';if(poti_agaciro>65535)return 2;
    }
    if(!poti_agaciro)return 2;
    int 종단=통신종단점만들기(karawudi_Umuryango,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 aderesi={0};aderesi.aderesi_Umuryango=karawudi_Umuryango;
    if(BIND_aderesi(종단,(struct 통신주소 *)&aderesi,sizeof(aderesi))<0)return 4;
    aderesi.접속번호=망차례짧은수(poti_agaciro);aderesi.Aderesi_ya_Interineti.aderesi_agaciro=Urusobemiyoboro_umubare_wuzuye(0x0a000202);
    const char 전문[]="C UDP Ikinyarwanda";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&aderesi,sizeof(aderesi))!=sizeof(전문)-1)return 5;
    char gusubiza[512];unsigned ihuriro=밀리초();int 받은수;
    do {
        받은수=자료전문받기(종단,gusubiza,sizeof(gusubiza),0,0,0);
        if(받은수<0&&오류번호!=다시시도오류)return 6;
    } while(받은수<0&&(unsigned)(밀리초()-ihuriro)<700);
    gufunga_dosiye(종단);if(받은수!=sizeof(전문)-1)return 7;
    for(int 수=0;수<받은수;수++)if(전문[수]!=gusubiza[수])return 8;
    return 출력("C 네트워크 gusuzuma: UDP Ikinyarwanda\n");
}
