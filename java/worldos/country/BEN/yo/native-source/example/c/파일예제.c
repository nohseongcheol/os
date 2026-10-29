#include "예제규약.h"
int main(void) {
    const char détà[]="C Fáìlì: yo 😀\n";
    int Fáìlì=ṣí_fáìlì("c.txt",tí_a_lè_kà_tí_a_lè_kọ|없으면만들기|내용비우기,0600);
    if(Fáìlì<0)return 1;
    if(kọ_fáìlì_détà(Fáìlì,détà,sizeof(détà)-1)!=sizeof(détà)-1)return 2;
    if(ṣàwárí_fáìlì(Fáìlì,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int gígùn_iye=파일자료읽기(Fáìlì,읽은글,sizeof(읽은글)-1);
    pa_dé_fáìlì(Fáìlì);
    if(gígùn_iye!=sizeof(détà)-1)return 4;
    for(int 수=0;수<gígùn_iye;수++)if(détà[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
