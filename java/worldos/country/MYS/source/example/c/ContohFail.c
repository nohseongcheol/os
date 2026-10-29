#include "예제규약.h"
int main(void) {
    const char data[]="C Fail: Malay (macrolanguage) 😀\n";
    int Fail=buka_fail("c.txt",baca_tulis|없으면만들기|potong_TOC,0600);
    if(Fail<0)return 1;
    if(tulis_fail_data(Fail,data,sizeof(data)-1)!=sizeof(data)-1)return 2;
    if(cari_fail(Fail,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int kepanjangan_VALUE=파일자료읽기(Fail,읽은글,sizeof(읽은글)-1);
    Tutup_fail(Fail);
    if(kepanjangan_VALUE!=sizeof(data)-1)return 4;
    for(int 수=0;수<kepanjangan_VALUE;수++)if(data[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
