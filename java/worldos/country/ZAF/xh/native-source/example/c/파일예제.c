#include "예제규약.h"
int main(void) {
    const char iingcombolo[]="C iFayili: xh 😀\n";
    int iFayili=vula_ifayile("c.txt",funda_bhala|없으면만들기|내용비우기,0600);
    if(iFayili<0)return 1;
    if(bhala_ifayile_iingcombolo(iFayili,iingcombolo,sizeof(iingcombolo)-1)!=sizeof(iingcombolo)-1)return 2;
    if(khangela_ifayile(iFayili,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int ubude_ixabiso=파일자료읽기(iFayili,읽은글,sizeof(읽은글)-1);
    vala_ifayile(iFayili);
    if(ubude_ixabiso!=sizeof(iingcombolo)-1)return 4;
    for(int 수=0;수<ubude_ixabiso;수++)if(iingcombolo[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
