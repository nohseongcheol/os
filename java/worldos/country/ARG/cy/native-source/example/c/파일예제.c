#include "예제규약.h"
int main(void) {
    const char data[]="C Ffeil: cy 😀\n";
    int Ffeil=agor_ffeil("c.txt",darllen_ysgrifennu|없으면만들기|내용비우기,0600);
    if(Ffeil<0)return 1;
    if(ysgrifennu_ffeil_data(Ffeil,data,sizeof(data)-1)!=sizeof(data)-1)return 2;
    if(chwilio_ffeil(Ffeil,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int hyd_VALUE=파일자료읽기(Ffeil,읽은글,sizeof(읽은글)-1);
    cau_ffeil(Ffeil);
    if(hyd_VALUE!=sizeof(data)-1)return 4;
    for(int 수=0;수<hyd_VALUE;수++)if(data[수]!=읽은글[수])return 5;
    return Allbwn(읽은글);
}
