#include "예제규약.h"
#include <통신규약.h>
int main(int argóint_COUNT,char **Argóintí) {
    if(argóint_COUNT!=2)return Aschur("사용법: ./네트워크 UDP창구번호\n");
    unsigned port_VALUE=0;for(int 수=0;Argóintí[1][수];수++) {
        if(Argóintí[1][수]<'0'||Argóintí[1][수]>'9')return 2;
        port_VALUE=port_VALUE*10+Argóintí[1][수]-'0';if(port_VALUE>65535)return 2;
    }
    if(!port_VALUE)return 2;
    int 종단=통신종단점만들기(néal_Teaghlach,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 ADDRESS={0};ADDRESS.ADDRESS_Teaghlach=néal_Teaghlach;
    if(BIND_ADDRESS(종단,(struct 통신주소 *)&ADDRESS,sizeof(ADDRESS))<0)return 4;
    ADDRESS.uimhir_phoirt=망차례짧은수(port_VALUE);ADDRESS.seoladh_Idirlín.ADDRESS_VALUE=Líonra_slánuimhir(0x0a000202);
    const char 전문[]="C UDP ga";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&ADDRESS,sizeof(ADDRESS))!=sizeof(전문)-1)return 5;
    char freagair[512];unsigned Rith_2=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=자료전문받기(종단,freagair,sizeof(freagair),0,0,0);
        if(RECEIVED_COUNT<0&&오류번호!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-Rith_2)<700);
    dún_comhad(종단);if(RECEIVED_COUNT!=sizeof(전문)-1)return 7;
    for(int 수=0;수<RECEIVED_COUNT;수++)if(전문[수]!=freagair[수])return 8;
    return Aschur("C 네트워크 fíoraigh: UDP ga\n");
}
