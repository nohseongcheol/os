#include "예제규약.h"
int main(void) {
    const char imininingwane[]="C Ihele: zu 😀\n";
    int Ihele=vula_ifayela("c.txt",fundeka_bhaleka|없으면만들기|내용비우기,0600);
    if(Ihele<0)return 1;
    if(bhala_ifayela_imininingwane(Ihele,imininingwane,sizeof(imininingwane)-1)!=sizeof(imininingwane)-1)return 2;
    if(cinga_ifayela(Ihele,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int ubude_inani=파일자료읽기(Ihele,읽은글,sizeof(읽은글)-1);
    vala_ifayela(Ihele);
    if(ubude_inani!=sizeof(imininingwane)-1)return 4;
    for(int 수=0;수<ubude_inani;수++)if(imininingwane[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
