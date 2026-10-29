#include "예제규약.h"
#include <ağ_ABI.h>
int main(int bağımsız_değişken_BAĞ_DEĞ_SAY,char **bağımsız_değişkenler) {
    if(bağımsız_değişken_BAĞ_DEĞ_SAY!=2)return metinÇıktısı("사용법: ./네트워크 UDP창구번호\n");
    unsigned taşımak_değer=0;for(int 수=0;bağımsız_değişkenler[1][수];수++) {
        if(bağımsız_değişkenler[1][수]<'0'||bağımsız_değişkenler[1][수]>'9')return 2;
        taşımak_değer=taşımak_değer*10+bağımsız_değişkenler[1][수]-'0';if(taşımak_değer>65535)return 2;
    }
    if(!taşımak_değer)return 2;
    int uç_nokta=açmak_uç_nokta(bulut_Aile,veri_birimi_yuvası,veri_birimi_protokol);if(uç_nokta<0)return 3;
    struct bulut_yuva_ADRES ADRES={0};ADRES.ADRES_Aile=bulut_Aile;
    if(BIND_ADRES(uç_nokta,(struct yuva_ADRES *)&ADRES,sizeof(ADRES))<0)return 4;
    ADRES.bağlantı_noktası_numarası=망차례짧은수(taşımak_değer);ADRES.İnternet_adresi.ADRES_değer=ağ_bilgi(0x0a000202);
    const char veri_birimi[]="C UDP tr";
    if(göndermek_veri_birimi_veri(uç_nokta,veri_birimi,sizeof(veri_birimi)-1,0,(struct yuva_ADRES *)&ADRES,sizeof(ADRES))!=sizeof(veri_birimi)-1)return 5;
    char yanıt[512];unsigned çalıştır=밀리초();int GETİRİ_BAĞ_DEĞ_SAY;
    do {
        GETİRİ_BAĞ_DEĞ_SAY=almak_veri_birimi_veri(uç_nokta,yanıt,sizeof(yanıt),0,0,0);
        if(GETİRİ_BAĞ_DEĞ_SAY<0&&hata_numarası!=다시시도오류)return 6;
    } while(GETİRİ_BAĞ_DEĞ_SAY<0&&(unsigned)(밀리초()-çalıştır)<700);
    Kapat_Dosya(uç_nokta);if(GETİRİ_BAĞ_DEĞ_SAY!=sizeof(veri_birimi)-1)return 7;
    for(int 수=0;수<GETİRİ_BAĞ_DEĞ_SAY;수++)if(veri_birimi[수]!=yanıt[수])return 8;
    return metinÇıktısı("C 네트워크 doğrulamak: UDP tr\n");
}
