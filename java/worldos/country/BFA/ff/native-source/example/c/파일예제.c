#include "예제규약.h"
int main(void) {
    const char keɓe[]="C fiilde: ff 😀\n";
    int fiilde=udditde_fiilde("c.txt",tar_winndu|없으면만들기|내용비우기,0600);
    if(fiilde<0)return 1;
    if(winndude_fiilde_keɓe(fiilde,keɓe,sizeof(keɓe)-1)!=sizeof(keɓe)-1)return 2;
    if(파일위치옮기기(fiilde,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int njuuteendi_njaru=파일자료읽기(fiilde,읽은글,sizeof(읽은글)-1);
    uddude_fiilde(fiilde);
    if(njuuteendi_njaru!=sizeof(keɓe)-1)return 4;
    for(int 수=0;수<njuuteendi_njaru;수++)if(keɓe[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
