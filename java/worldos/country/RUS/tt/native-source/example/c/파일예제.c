#include "예제규약.h"
int main(void) {
    const char мәгълүмат[]="C Birem: tt 😀\n";
    int Birem=ачу_файл("c.txt",укымалы_язмалы|없으면만들기|내용비우기,0600);
    if(Birem<0)return 1;
    if(язу_файл_мәгълүмат(Birem,мәгълүмат,sizeof(мәгълүмат)-1)!=sizeof(мәгълүмат)-1)return 2;
    if(эзләү_файл(Birem,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int озынлык_VALUE=파일자료읽기(Birem,읽은글,sizeof(읽은글)-1);
    чик_файл(Birem);
    if(озынлык_VALUE!=sizeof(мәгълүмат)-1)return 4;
    for(int 수=0;수<озынлык_VALUE;수++)if(мәгълүмат[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
