#include "예제규약.h"
#include <통신규약.h>
int main(int 인수수,char **인수) {
    if(인수수!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned iphothi_ixabiso=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        iphothi_ixabiso=iphothi_ixabiso*10+인수[1][수]-'0';if(iphothi_ixabiso>65535)return 2;
    }
    if(!iphothi_ixabiso)return 2;
    int 종단=통신종단점만들기(ilifu_Usapho,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 idilesi={0};idilesi.idilesi_Usapho=ilifu_Usapho;
    if(BOPHELELA_idilesi(종단,(struct 통신주소 *)&idilesi,sizeof(idilesi))<0)return 4;
    idilesi.접속번호=망차례짧은수(iphothi_ixabiso);idilesi.idilesi_yeintanethi.idilesi_ixabiso=Inethiwekhi_inani_elipheleleyo(0x0a000202);
    const char 전문[]="C UDP xh";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&idilesi,sizeof(idilesi))!=sizeof(전문)-1)return 5;
    char phendula[512];unsigned Phumeza=밀리초();int 받은수;
    do {
        받은수=자료전문받기(종단,phendula,sizeof(phendula),0,0,0);
        if(받은수<0&&오류번호!=다시시도오류)return 6;
    } while(받은수<0&&(unsigned)(밀리초()-Phumeza)<700);
    vala_ifayile(종단);if(받은수!=sizeof(전문)-1)return 7;
    for(int 수=0;수<받은수;수++)if(전문[수]!=phendula[수])return 8;
    return 출력("C 네트워크 ngqinisisa: UDP xh\n");
}
