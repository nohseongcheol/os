#include "예제규약.h"
int main(void) {
    const char data[]="C Fil: nn 😀\n";
    int Fil=opne_fil("c.txt",lese_og_skrivetilgang|없으면만들기|내용비우기,0600);
    if(Fil<0)return 1;
    if(skrive_fil_data(Fil,data,sizeof(data)-1)!=sizeof(data)-1)return 2;
    if(søk_fil(Fil,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int lengd_VALUE=파일자료읽기(Fil,읽은글,sizeof(읽은글)-1);
    Lukk_fil(Fil);
    if(lengd_VALUE!=sizeof(data)-1)return 4;
    for(int 수=0;수<lengd_VALUE;수++)if(data[수]!=읽은글[수])return 5;
    return Utdata(읽은글);
}
