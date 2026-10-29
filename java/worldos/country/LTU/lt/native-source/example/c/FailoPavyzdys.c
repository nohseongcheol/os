#include "예제규약.h"
int main(void) {
    const char duomenys[]="C Failas: lt 😀\n";
    int Failas=kurti_Failas("c.txt",읽고쓰기|없으면만들기|trumpinti_Turinys,0600);
    if(Failas<0)return 1;
    if(rašymas_Failas_duomenys(Failas,duomenys,sizeof(duomenys)-1)!=sizeof(duomenys)-1)return 2;
    if(ieškoti_Failas(Failas,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int 길이=파일자료읽기(Failas,읽은글,sizeof(읽은글)-1);
    Uždaryti_Failas(Failas);
    if(길이!=sizeof(duomenys)-1)return 4;
    for(int numeris=0;numeris<길이;numeris++)if(duomenys[numeris]!=읽은글[numeris])return 5;
    return Išvestis(읽은글);
}
