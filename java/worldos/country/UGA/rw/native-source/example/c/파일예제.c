#include "예제규약.h"
int main(void) {
    const char amakurushingiro[]="C Idosiye: rw 😀\n";
    int Idosiye=kurema_dosiye("c.txt",gusoma_kwandika|없으면만들기|내용비우기,0600);
    if(Idosiye<0)return 1;
    if(kwandika_dosiye_amakurushingiro(Idosiye,amakurushingiro,sizeof(amakurushingiro)-1)!=sizeof(amakurushingiro)-1)return 2;
    if(파일위치옮기기(Idosiye,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int uburebure_agaciro=파일자료읽기(Idosiye,읽은글,sizeof(읽은글)-1);
    gufunga_dosiye(Idosiye);
    if(uburebure_agaciro!=sizeof(amakurushingiro)-1)return 4;
    for(int 수=0;수<uburebure_agaciro;수++)if(amakurushingiro[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
