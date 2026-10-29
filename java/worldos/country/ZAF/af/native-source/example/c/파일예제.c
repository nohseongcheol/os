#include "예제규약.h"
int main(void) {
    const char data[]="C Lêer: af 😀\n";
    int Lêer=skep_lêer("c.txt",lees_skryf|없으면만들기|내용비우기,0600);
    if(Lêer<0)return 1;
    if(skryf_lêer_data(Lêer,data,sizeof(data)-1)!=sizeof(data)-1)return 2;
    if(soek_lêer(Lêer,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int lengte_VALUE=파일자료읽기(Lêer,읽은글,sizeof(읽은글)-1);
    sluit_lêer(Lêer);
    if(lengte_VALUE!=sizeof(data)-1)return 4;
    for(int 수=0;수<lengte_VALUE;수++)if(data[수]!=읽은글[수])return 5;
    return Afvoer(읽은글);
}
