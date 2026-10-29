#include "예제규약.h"
int main(void) {
    const char tshedimosetso[]="C faele: tn 😀\n";
    int faele=bula_faele("c.txt",buisa_kwala|없으면만들기|내용비우기,0600);
    if(faele<0)return 1;
    if(kwala_faele_tshedimosetso(faele,tshedimosetso,sizeof(tshedimosetso)-1)!=sizeof(tshedimosetso)-1)return 2;
    if(batla_faele(faele,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int boleele_Boleng=파일자료읽기(faele,읽은글,sizeof(읽은글)-1);
    tswala_faele(faele);
    if(boleele_Boleng!=sizeof(tshedimosetso)-1)return 4;
    for(int 수=0;수<boleele_Boleng;수++)if(tshedimosetso[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
