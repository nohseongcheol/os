#include "예제규약.h"
int main(void) {
    const char 자료[]="C Fíla: Faroese 😀\n";
    int Fíla=파일열기("c.txt",읽고쓰기|없으면만들기|내용비우기,0600);
    if(Fíla<0)return 1;
    if(파일자료쓰기(Fíla,자료,sizeof(자료)-1)!=sizeof(자료)-1)return 2;
    if(파일위치옮기기(Fíla,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int 길이=파일자료읽기(Fíla,읽은글,sizeof(읽은글)-1);
    파일닫기(Fíla);
    if(길이!=sizeof(자료)-1)return 4;
    for(int 수=0;수<길이;수++)if(자료[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
