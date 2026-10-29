#include "예제규약.h"
#include <통신규약.h>
int main(int 인수수,char **인수) {
    if(인수수!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned fot_Daraja=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        fot_Daraja=fot_Daraja*10+인수[1][수]-'0';if(fot_Daraja>65535)return 2;
    }
    if(!fot_Daraja)return 2;
    int 종단=통신종단점만들기(Intanet_Iyali,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 imel={0};imel.imel_Iyali=Intanet_Iyali;
    if(BIND_imel(종단,(struct 통신주소 *)&imel,sizeof(imel))<0)return 4;
    imel.lambar_kafa=망차례짧은수(fot_Daraja);imel.Adireshin_yanar_gizo.imel_Daraja=Hanyar_sadarwa_Lamba_mara(0x0a000202);
    const char 전문[]="C UDP ha";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&imel,sizeof(imel))!=sizeof(전문)-1)return 5;
    char mayar_da_martani[512];unsigned Tafiyar_da=밀리초();int 받은수;
    do {
        받은수=자료전문받기(종단,mayar_da_martani,sizeof(mayar_da_martani),0,0,0);
        if(받은수<0&&오류번호!=다시시도오류)return 6;
    } while(받은수<0&&(unsigned)(밀리초()-Tafiyar_da)<700);
    Rufe_Fayil(종단);if(받은수!=sizeof(전문)-1)return 7;
    for(int 수=0;수<받은수;수++)if(전문[수]!=mayar_da_martani[수])return 8;
    return 출력("C 네트워크 Tabbatar_da: UDP ha\n");
}
