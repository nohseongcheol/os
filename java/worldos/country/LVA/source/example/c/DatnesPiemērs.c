#include "예제규약.h"
int main(void) {
    const char dati[]="C Fails: Latviešu 😀\n";
    int Fails=atvērt_Fails("c.txt",읽고쓰기|없으면만들기|apraut_Satura_rādītājs,0600);
    if(Fails<0)return 1;
    if(rakstīšana_Fails_dati(Fails,dati,sizeof(dati)-1)!=sizeof(dati)-1)return 2;
    if(meklēt_Fails(Fails,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int 길이=파일자료읽기(Fails,읽은글,sizeof(읽은글)-1);
    Aizvērt_Fails(Fails);
    if(길이!=sizeof(dati)-1)return 4;
    for(int numurs=0;numurs<길이;numurs++)if(dati[numurs]!=읽은글[numurs])return 5;
    return Izvade(읽은글);
}
