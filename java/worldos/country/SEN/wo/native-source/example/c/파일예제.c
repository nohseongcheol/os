#include "예제규약.h"
int main(void) {
    const char mbir[]="C bara_denc: wo 😀\n";
    int bara_denc=sos_bara_denc("c.txt",jàng_bind|없으면만들기|내용비우기,0600);
    if(bara_denc<0)return 1;
    if(biir_bara_denc_mbir(bara_denc,mbir,sizeof(mbir)-1)!=sizeof(mbir)-1)return 2;
    if(seet_bara_denc(bara_denc,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int diir_xëyma=파일자료읽기(bara_denc,읽은글,sizeof(읽은글)-1);
    Tej_bara_denc(bara_denc);
    if(diir_xëyma!=sizeof(mbir)-1)return 4;
    for(int 수=0;수<diir_xëyma;수++)if(mbir[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
