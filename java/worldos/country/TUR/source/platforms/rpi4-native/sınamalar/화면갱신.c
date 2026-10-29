#include "../명명/기계연결이름.h"
#include "../makine/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Pano_Terminal(uintptr_t),Pano_piksel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_işaretçi(unsigned,int,int),Terminal_bayt(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Karşılaştırma_RESİM[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Pano_işaretçi(0,0,0);memcpy(Karşılaştırma_RESİM,화면,sizeof(화면));
    uint64_t Önceki_öğe=Pano_çizim_BAĞ_DEĞ_SAY();Pano_Terminal(3);
    assert(memcmp(Karşılaştırma_RESİM,화면,sizeof(화면))==0);
    assert(Pano_çizim_BAĞ_DEĞ_SAY()==Önceki_öğe); /* 같은 화면을 yeniden_denemek_değer 그려도 şov_değer 메모리에 쓰지 않는다. */
}
static void yazma_SMS(const char *metin){while(*metin)Terminal_bayt((unsigned char)*metin++);}
int main(void){
    Pano_Hazırlan_çizim(&화면[0][0],1920,1080,sizeof(화면[0]));
    Pano_Terminal(300);yazma_SMS("첫 창의 한글 veri\n");
    for(int Dizin=1;Dizin<4;Dizin++){Pano_Terminal(1);Pano_Terminal(100+Dizin);yazma_SMS("겹친 창의 한글 veri\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Dikey_konum=102,폭=568,높이=360;
    uint64_t taşımak_LOG=0;double 이동시간=0;
    for(int dizi_değer=0;dizi_değer<80;dizi_değer++){
        Terminal_işaretçi(1,가로+100,Dikey_konum+15);
        int 새가로=80+(dizi_değer*37)%850,새세로=50+(dizi_değer*13)%450;
        Pano_piksel(1900,1050,0x123456); /* yenilemek bölge_değer 밖의 kullanıcı_alanı çizim_değer */
        uint64_t Önceki_öğe=Pano_çizim_BAĞ_DEĞ_SAY();clock_t çalıştır=clock();
        Terminal_işaretçi(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-çalıştır)/CLOCKS_PER_SEC;
        taşımak_LOG+=Pano_çizim_BAĞ_DEĞ_SAY()-Önceki_öğe;
        assert(Pano_çizim_BAĞ_DEĞ_SAY()-Önceki_öğe<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        Pano_piksel(1900,1050,0x302018);
        Terminal_işaretçi(0,새가로+100,새세로+15);가로=새가로;Dikey_konum=새세로;
        전체와비교();
    }
    for(int dizi_değer=0;dizi_değer<40;dizi_değer++){
        int 새폭=360+(dizi_değer*29)%700,새높이=216+(dizi_değer*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Dikey_konum)새높이=1080-Dikey_konum;
        Terminal_işaretçi(1,가로+폭-4,Dikey_konum+높이-4);
        Terminal_işaretçi(1,가로+새폭-4,Dikey_konum+새높이-4);
        uint64_t Önceki_öğe=Pano_çizim_BAĞ_DEĞ_SAY();
        Terminal_işaretçi(1,가로+새폭-4,Dikey_konum+새높이-4);
        assert(Pano_çizim_BAĞ_DEĞ_SAY()==Önceki_öğe); /* 같은 좌표의 중복 Olay */
        Terminal_işaretçi(0,가로+새폭-4,Dikey_konum+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 fiili_veri girdi_satırı 간격을 지킨다. */
    for(int girdi_satırı=0;girdi_satırı<1080;girdi_satırı++)for(int yuva_girdi=1920;yuva_girdi<1936;yuva_girdi++)assert(화면[girdi_satırı][yuva_girdi]==0);
    assert(!Pano_Start_çizim(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(taşımak_LOG/80));
    return 0;
}
