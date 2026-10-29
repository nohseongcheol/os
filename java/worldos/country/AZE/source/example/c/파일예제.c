#include "예제규약.h"
int main(void) {
    const char verilənlər[]="C FAYL: Azerbaijani 😀\n";
    int FAYL=açmaq_fayl("c.txt",oxunan_yazılan|없으면만들기|내용비우기,0600);
    if(FAYL<0)return 1;
    if(yazmaq_fayl_verilənlər(FAYL,verilənlər,sizeof(verilənlər)-1)!=sizeof(verilənlər)-1)return 2;
    if(axtarmaq_fayl(FAYL,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int uzunluq_VALUE=파일자료읽기(FAYL,읽은글,sizeof(읽은글)-1);
    bağlamaq_fayl(FAYL);
    if(uzunluq_VALUE!=sizeof(verilənlər)-1)return 4;
    for(int 수=0;수<uzunluq_VALUE;수++)if(verilənlər[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
