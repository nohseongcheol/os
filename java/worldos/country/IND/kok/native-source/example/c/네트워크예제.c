#include "예제규약.h"
#include <통신규약.h>
int main(int युक्तीवाद_COUNT,char **인수) {
    if(युक्तीवाद_COUNT!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned पोर्ट_मोल=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        पोर्ट_मोल=पोर्ट_मोल*10+인수[1][수]-'0';if(पोर्ट_मोल>65535)return 2;
    }
    if(!पोर्ट_मोल)return 2;
    int 종단=통신종단점만들기(कूप_कुटुंब,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 नामो={0};नामो.नामो_कुटुंब=कूप_कुटुंब;
    if(BIND_नामो(종단,(struct 통신주소 *)&नामो,sizeof(नामो))<0)return 4;
    नामो.접속번호=망차례짧은수(पोर्ट_मोल);नामो.माजाळ्याचो_नामो.नामो_मोल=नॅटवर्क_पुर्णांक(0x0a000202);
    const char 전문[]="C UDP kok";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&नामो,sizeof(नामो))!=sizeof(전문)-1)return 5;
    char जाप_दिवप[512];unsigned चलोवप=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=자료전문받기(종단,जाप_दिवप,sizeof(जाप_दिवप),0,0,0);
        if(RECEIVED_COUNT<0&&오류번호!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-चलोवप)<700);
    शेवट_फायल(종단);if(RECEIVED_COUNT!=sizeof(전문)-1)return 7;
    for(int 수=0;수<RECEIVED_COUNT;수++)if(전문[수]!=जाप_दिवप[수])return 8;
    return 출력("C 네트워크 पुनर्तपासणी_करची: UDP kok\n");
}
