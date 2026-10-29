#include "예제규약.h"
int main(void) {
    const char data[]="C Faele: nso 😀\n";
    int Faele=bula_faele("c.txt",bala_ngwala|없으면만들기|내용비우기,0600);
    if(Faele<0)return 1;
    if(ngwala_faele_data(Faele,data,sizeof(data)-1)!=sizeof(data)-1)return 2;
    if(nyaka_faele(Faele,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int botelele_boleng=파일자료읽기(Faele,읽은글,sizeof(읽은글)-1);
    tswalela_faele(Faele);
    if(botelele_boleng!=sizeof(data)-1)return 4;
    for(int 수=0;수<botelele_boleng;수++)if(data[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
