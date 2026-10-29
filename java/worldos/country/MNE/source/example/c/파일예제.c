#include "예제규약.h"
int main(void) {
    const char podaci[]="C Datoteka: српски 😀\n";
    int Datoteka=otvoren_Datoteka("c.txt",za_čitanje_pisanje|없으면만들기|내용비우기,0600);
    if(Datoteka<0)return 1;
    if(파일자료쓰기(Datoteka,podaci,sizeof(podaci)-1)!=sizeof(podaci)-1)return 2;
    if(tražiti_Datoteka(Datoteka,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int 길이=파일자료읽기(Datoteka,읽은글,sizeof(읽은글)-1);
    Zatvori_Datoteka(Datoteka);
    if(길이!=sizeof(podaci)-1)return 4;
    for(int 수=0;수<길이;수++)if(podaci[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
