#include "예제규약.h"
int main(void) {
    const char raraunga[]="C Kōnae: mi 😀\n";
    int Kōnae=tiwhikete_kōnae("c.txt",읽고쓰기|없으면만들기|내용비우기,0600);
    if(Kōnae<0)return 1;
    if(tuhi_kōnae_raraunga(Kōnae,raraunga,sizeof(raraunga)-1)!=sizeof(raraunga)-1)return 2;
    if(kimi_kōnae(Kōnae,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int roa_uara=파일자료읽기(Kōnae,읽은글,sizeof(읽은글)-1);
    kati_kōnae(Kōnae);
    if(roa_uara!=sizeof(raraunga)-1)return 4;
    for(int 수=0;수<roa_uara;수++)if(raraunga[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
