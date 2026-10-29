#include "예제규약.h"
int main(void) {
    const char data[]="C file: fil 😀\n";
    int file=buksan_file("c.txt",nababasa_nasusulatan|없으면만들기|내용비우기,0600);
    if(file<0)return 1;
    if(sumulat_file_data(file,data,sizeof(data)-1)!=sizeof(data)-1)return 2;
    if(i_seek_file(file,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int haba_VALUE=파일자료읽기(file,읽은글,sizeof(읽은글)-1);
    isara_file(file);
    if(haba_VALUE!=sizeof(data)-1)return 4;
    for(int 수=0;수<haba_VALUE;수++)if(data[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
