#include "예제규약.h"
int main(void) {
    const char veri[]="C dosya: tr 😀\n";
    int dosya=açık_Dosya("c.txt",R_W|없으면만들기|kesmek_içindekiler,0600);
    if(dosya<0)return 1;
    if(yazma_Dosya_veri(dosya,veri,sizeof(veri)-1)!=sizeof(veri)-1)return 2;
    if(arama_Dosya(dosya,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int süre_değer=파일자료읽기(dosya,읽은글,sizeof(읽은글)-1);
    Kapat_Dosya(dosya);
    if(süre_değer!=sizeof(veri)-1)return 4;
    for(int 수=0;수<süre_değer;수++)if(veri[수]!=읽은글[수])return 5;
    return metinÇıktısı(읽은글);
}
