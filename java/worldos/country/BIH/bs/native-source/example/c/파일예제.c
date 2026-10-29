#include "예제규약.h"
int main(void) {
    const char podaci[]="C Fajl: bs 😀\n";
    int Fajl=kreirati_fajl("c.txt",i_za_čitanje_i_za_pisanje|없으면만들기|내용비우기,0600);
    if(Fajl<0)return 1;
    if(pisati_fajl_podaci(Fajl,podaci,sizeof(podaci)-1)!=sizeof(podaci)-1)return 2;
    if(tražiti_fajl(Fajl,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int dužina_VALUE=파일자료읽기(Fajl,읽은글,sizeof(읽은글)-1);
    zatvoriti_fajl(Fajl);
    if(dužina_VALUE!=sizeof(podaci)-1)return 4;
    for(int 수=0;수<dužina_VALUE;수++)if(podaci[수]!=읽은글[수])return 5;
    return Ispis(읽은글);
}
