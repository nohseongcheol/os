#include "예제규약.h"
#include <통신규약.h>
int main(int аргумент_COUNT,char **Аргументи) {
    if(аргумент_COUNT!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned порта_VALUE=0;for(int 수=0;Аргументи[1][수];수++) {
        if(Аргументи[1][수]<'0'||Аргументи[1][수]>'9')return 2;
        порта_VALUE=порта_VALUE*10+Аргументи[1][수]-'0';if(порта_VALUE>65535)return 2;
    }
    if(!порта_VALUE)return 2;
    int 종단=통신종단점만들기(облак_семејни,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 адреса={0};адреса.адреса_семејни=облак_семејни;
    if(БИНД_адреса(종단,(struct 통신주소 *)&адреса,sizeof(адреса))<0)return 4;
    адреса.број_на_порта=망차례짧은수(порта_VALUE);адреса.Интернет_адреса.адреса_VALUE=Мрежа_цел_број(0x0a000202);
    const char 전문[]="C UDP mk";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&адреса,sizeof(адреса))!=sizeof(전문)-1)return 5;
    char одговори[512];unsigned Изврши_2=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=자료전문받기(종단,одговори,sizeof(одговори),0,0,0);
        if(RECEIVED_COUNT<0&&오류번호!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-Изврши_2)<700);
    затвори_датотека(종단);if(RECEIVED_COUNT!=sizeof(전문)-1)return 7;
    for(int 수=0;수<RECEIVED_COUNT;수++)if(전문[수]!=одговори[수])return 8;
    return 출력("C 네트워크 провери: UDP mk\n");
}
