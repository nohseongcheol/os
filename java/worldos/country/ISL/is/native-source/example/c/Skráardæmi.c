#include "예제규약.h"
int main(void) {
    const char gögn[]="C Skrá: is 😀\n";
    int Skrá=opið_skrá("c.txt",les_skrifheimild|없으면만들기|내용비우기,0600);
    if(Skrá<0)return 1;
    if(skrifa_skrá_gögn(Skrá,gögn,sizeof(gögn)-1)!=sizeof(gögn)-1)return 2;
    if(leita_skrá(Skrá,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int lengd_VALUE=파일자료읽기(Skrá,읽은글,sizeof(읽은글)-1);
    loka_skrá(Skrá);
    if(lengd_VALUE!=sizeof(gögn)-1)return 4;
    for(int númer=0;númer<lengd_VALUE;númer++)if(gögn[númer]!=읽은글[númer])return 5;
    return úttak(읽은글);
}
