#include "예제규약.h"
int main(void) {
    const char data[]="C fajl: Malti 😀\n";
    int fajl=fetaħ_fajl("c.txt",qari_kitba|없으면만들기|내용비우기,0600);
    if(fajl<0)return 1;
    if(kiteb_fajl_data(fajl,data,sizeof(data)-1)!=sizeof(data)-1)return 2;
    if(fittex_fajl(fajl,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int tul_VALUE=파일자료읽기(fajl,읽은글,sizeof(읽은글)-1);
    agħlaq_fajl(fajl);
    if(tul_VALUE!=sizeof(data)-1)return 4;
    for(int 수=0;수<tul_VALUE;수++)if(data[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
