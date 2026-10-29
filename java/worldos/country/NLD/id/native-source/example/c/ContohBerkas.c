#include "예제규약.h"
int main(void) {
    const char data[]="C berkas: id 😀\n";
    int berkas=buat_file("c.txt",baca_tulis|없으면만들기|내용비우기,0600);
    if(berkas<0)return 1;
    if(tulis_file_data(berkas,data,sizeof(data)-1)!=sizeof(data)-1)return 2;
    if(cari_file(berkas,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int panjang_VALUE=파일자료읽기(berkas,읽은글,sizeof(읽은글)-1);
    Tutup_file(berkas);
    if(panjang_VALUE!=sizeof(data)-1)return 4;
    for(int 수=0;수<panjang_VALUE;수++)if(data[수]!=읽은글[수])return 5;
    return keluaranTeks(읽은글);
}
