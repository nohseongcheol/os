#include "예제규약.h"
int main(void) {
    const char maglumat[]="C Faýl: tk 😀\n";
    int Faýl=aç_faýl("c.txt",okalýan_ýazylýan|없으면만들기|내용비우기,0600);
    if(Faýl<0)return 1;
    if(ýaz_faýl_maglumat(Faýl,maglumat,sizeof(maglumat)-1)!=sizeof(maglumat)-1)return 2;
    if(gözle_faýl(Faýl,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int dowamlylyk_baha=파일자료읽기(Faýl,읽은글,sizeof(읽은글)-1);
    ýap_faýl(Faýl);
    if(dowamlylyk_baha!=sizeof(maglumat)-1)return 4;
    for(int 수=0;수<dowamlylyk_baha;수++)if(maglumat[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
