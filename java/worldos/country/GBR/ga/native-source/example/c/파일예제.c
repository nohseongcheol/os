#include "예제규약.h"
int main(void) {
    const char sonraí[]="C Comhad: ga 😀\n";
    int Comhad=oscail_comhad("c.txt",inléite_inscríofa|없으면만들기|내용비우기,0600);
    if(Comhad<0)return 1;
    if(scríobh_comhad_sonraí(Comhad,sonraí,sizeof(sonraí)-1)!=sizeof(sonraí)-1)return 2;
    if(lorg_comhad(Comhad,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int fad_VALUE=파일자료읽기(Comhad,읽은글,sizeof(읽은글)-1);
    dún_comhad(Comhad);
    if(fad_VALUE!=sizeof(sonraí)-1)return 4;
    for(int 수=0;수<fad_VALUE;수++)if(sonraí[수]!=읽은글[수])return 5;
    return Aschur(읽은글);
}
