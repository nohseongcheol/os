#include "예제규약.h"
int main(void) {
    const char datà[]="C Faịlụ: ig 😀\n";
    int Faịlụ=mepee_ọbọakwụkwọ("c.txt",gụọ_dèe|없으면만들기|내용비우기,0600);
    if(Faịlụ<0)return 1;
    if(dee_ọbọakwụkwọ_datà(Faịlụ,datà,sizeof(datà)-1)!=sizeof(datà)-1)return 2;
    if(ọchịchọ_ọbọakwụkwọ(Faịlụ,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int ogologo_valuu=파일자료읽기(Faịlụ,읽은글,sizeof(읽은글)-1);
    mmechi_ọbọakwụkwọ(Faịlụ);
    if(ogologo_valuu!=sizeof(datà)-1)return 4;
    for(int 수=0;수<ogologo_valuu;수++)if(datà[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
