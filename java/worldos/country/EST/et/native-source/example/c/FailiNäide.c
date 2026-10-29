#include "예제규약.h"
int main(void) {
    const char andmed[]="C Fail: et 😀\n";
    int Fail=avama_Fail("c.txt",읽고쓰기|없으면만들기|lühendama_Sisu,0600);
    if(Fail<0)return 1;
    if(kirjutamine_Fail_andmed(Fail,andmed,sizeof(andmed)-1)!=sizeof(andmed)-1)return 2;
    if(otsima_Fail(Fail,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int 길이=파일자료읽기(Fail,읽은글,sizeof(읽은글)-1);
    Sule_Fail(Fail);
    if(길이!=sizeof(andmed)-1)return 4;
    for(int number=0;number<길이;number++)if(andmed[number]!=읽은글[number])return 5;
    return Väljund(읽은글);
}
