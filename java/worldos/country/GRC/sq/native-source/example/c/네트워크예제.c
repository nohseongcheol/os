#include "예제규약.h"
#include <통신규약.h>
int main(int argument_COUNT,char **Argumente) {
    if(argument_COUNT!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned portë_VALUE=0;for(int 수=0;Argumente[1][수];수++) {
        if(Argumente[1][수]<'0'||Argumente[1][수]>'9')return 2;
        portë_VALUE=portë_VALUE*10+Argumente[1][수]-'0';if(portë_VALUE>65535)return 2;
    }
    if(!portë_VALUE)return 2;
    int 종단=통신종단점만들기(Internet_Familja,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 email={0};email.email_Familja=Internet_Familja;
    if(BIND_email(종단,(struct 통신주소 *)&email,sizeof(email))<0)return 4;
    email.numri_i_portës=망차례짧은수(portë_VALUE);email.adresë_në_internet.email_VALUE=rrjet_numër_i_plotë(0x0a000202);
    const char 전문[]="C UDP sq";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&email,sizeof(email))!=sizeof(전문)-1)return 5;
    char replikë[512];unsigned Ekzekuto=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=자료전문받기(종단,replikë,sizeof(replikë),0,0,0);
        if(RECEIVED_COUNT<0&&오류번호!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-Ekzekuto)<700);
    mbyll_skedar(종단);if(RECEIVED_COUNT!=sizeof(전문)-1)return 7;
    for(int 수=0;수<RECEIVED_COUNT;수++)if(전문[수]!=replikë[수])return 8;
    return 출력("C 네트워크 verifikoj: UDP sq\n");
}
