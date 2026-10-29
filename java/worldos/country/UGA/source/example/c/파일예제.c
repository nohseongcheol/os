#include "예제규약.h"
int main(void) {
    const char data[]="C faili: Swahili (macrolanguage) 😀\n";
    int faili=unda_faili("c.txt",soma_andika|없으면만들기|내용비우기,0600);
    if(faili<0)return 1;
    if(andika_faili_data(faili,data,sizeof(data)-1)!=sizeof(data)-1)return 2;
    if(tafuta_faili(faili,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int urefu_thamani=파일자료읽기(faili,읽은글,sizeof(읽은글)-1);
    funga_faili(faili);
    if(urefu_thamani!=sizeof(data)-1)return 4;
    for(int 수=0;수<urefu_thamani;수++)if(data[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
