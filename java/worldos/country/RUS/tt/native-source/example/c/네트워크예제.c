#include "예제규약.h"
#include <통신규약.h>
int main(int аргумент_COUNT,char **인수) {
    if(аргумент_COUNT!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned порт_VALUE=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        порт_VALUE=порт_VALUE*10+인수[1][수]-'0';if(порт_VALUE>65535)return 2;
    }
    if(!порт_VALUE)return 2;
    int 종단=통신종단점만들기(болыт_Гаилә,전문통신,전문전송규약);if(종단<0)return 3;
    struct 인터넷통신주소 адрес={0};адрес.адрес_Гаилә=болыт_Гаилә;
    if(BIND_адрес(종단,(struct 통신주소 *)&адрес,sizeof(адрес))<0)return 4;
    адрес.접속번호=망차례짧은수(порт_VALUE);адрес.Интернеттагы_адрес.адрес_VALUE=Челтәр_бөтен_сан(0x0a000202);
    const char 전문[]="C UDP tt";
    if(자료전문보내기(종단,전문,sizeof(전문)-1,0,(struct 통신주소 *)&адрес,sizeof(адрес))!=sizeof(전문)-1)return 5;
    char җавап_бирү[512];unsigned эшләтү=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=자료전문받기(종단,җавап_бирү,sizeof(җавап_бирү),0,0,0);
        if(RECEIVED_COUNT<0&&오류번호!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-эшләтү)<700);
    чик_файл(종단);if(RECEIVED_COUNT!=sizeof(전문)-1)return 7;
    for(int 수=0;수<RECEIVED_COUNT;수++)if(전문[수]!=җавап_бирү[수])return 8;
    return 출력("C 네트워크 раслау: UDP tt\n");
}
