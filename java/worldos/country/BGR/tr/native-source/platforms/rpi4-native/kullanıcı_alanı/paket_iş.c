#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "paket_iş.h"
#include "uzlib.h"
static unsigned char Arşiv[16384], 풀린자료[16385];
static unsigned Boyut, 중앙목록, 항목들;
static char girdi_Sınıf[256];
static unsigned 두바이트읽기(unsigned geçerli_konum) { return Arşiv[geçerli_konum] | Arşiv[geçerli_konum+1] << 8; }
static uint32_t 네바이트읽기(unsigned geçerli_konum) { return 두바이트읽기(geçerli_konum) | (uint32_t)두바이트읽기(geçerli_konum+2) << 16; }
static int klip(unsigned geçerli_konum, unsigned öğe_BAĞ_DEĞ_SAY, unsigned 한도) { return geçerli_konum <= 한도 && öğe_BAĞ_DEĞ_SAY <= 한도-geçerli_konum; }
static size_t süre_değer(const char *dize_veri) { size_t öğe_BAĞ_DEĞ_SAY=0; while(dize_veri[öğe_BAĞ_DEĞ_SAY]) öğe_BAĞ_DEĞ_SAY++; return öğe_BAĞ_DEĞ_SAY; }
static int 같음(const unsigned char *첫째값, const unsigned char *SANİYE_değer, unsigned öğe_BAĞ_DEĞ_SAY) { for(unsigned 순번=0;순번<öğe_BAĞ_DEĞ_SAY;순번++)if(첫째값[순번]!=SANİYE_değer[순번])return 0;return 1; }
static int Dosya_Bitiş(void *미사용값) { (void)미사용값; return -1; }
static int öznitelik_veri(const char *girdi_satırı,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)girdi_satırı,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)girdi_satırı,(const unsigned char*)"Main-Class: ",12)) {
        unsigned değer=사용량-12;if(*진입점있음||!değer||değer>=sizeof(girdi_Sınıf))return -8;
        for(unsigned 순번=0;순번<değer;순번++){unsigned char kod_noktası=girdi_satırı[12+순번];if(kod_noktası<=32||kod_noktası=='/'||kod_noktası=='\\')return -8;girdi_Sınıf[순번]=kod_noktası;}
        girdi_Sınıf[değer]=0;*진입점있음=1;
    }
    return 0;
}
static int üye(unsigned geçerli_konum, unsigned char *KR_veri, unsigned 용량한도) {
    unsigned metot_girdi=두바이트읽기(geçerli_konum+10), Yapılandırma_BITS=두바이트읽기(geçerli_konum+8), 압축크기=네바이트읽기(geçerli_konum+20), sürüm_boyutlandırmak=네바이트읽기(geçerli_konum+24), yerel=네바이트읽기(geçerli_konum+42);
    unsigned İsim=두바이트읽기(geçerli_konum+28);
    if(sürüm_boyutlandırmak>용량한도 || sürüm_boyutlandırmak>16384 || (metot_girdi!=0 && metot_girdi!=8) || (Yapılandırma_BITS&~0x80e))return -8;
    if(!klip(yerel,30,중앙목록) || 네바이트읽기(yerel)!=0x04034b50 || 두바이트읽기(yerel+8)!=metot_girdi || 두바이트읽기(yerel+6)!=Yapılandırma_BITS || 두바이트읽기(yerel+26)!=İsim)return -8;
    unsigned Start_Ofset=yerel+30, 추가영역=두바이트읽기(yerel+28);
    if(!klip(Start_Ofset,İsim,중앙목록) || !같음(Arşiv+Start_Ofset,Arşiv+geçerli_konum+46,İsim))return -8;
    Start_Ofset+=İsim;if(!klip(Start_Ofset,추가영역,중앙목록))return -8;Start_Ofset+=추가영역;
    if(!klip(Start_Ofset,압축크기,중앙목록))return -8;
    if(!(Yapılandırma_BITS&8) && (네바이트읽기(yerel+14)!=네바이트읽기(geçerli_konum+16) || 네바이트읽기(yerel+18)!=압축크기 || 네바이트읽기(yerel+22)!=sürüm_boyutlandırmak))return -8;
    if(metot_girdi==0) { if(압축크기!=sürüm_boyutlandırmak)return -8; for(unsigned 순번=0;순번<sürüm_boyutlandırmak;순번++)KR_veri[순번]=Arşiv[Start_Ofset+순번]; }
    else {
        uzlib_uncomp_t hedef_veri={0};uzlib_uncompress_init(&hedef_veri,0,0);
        hedef_veri.source=Arşiv+Start_Ofset;hedef_veri.source_limit=hedef_veri.source+압축크기;hedef_veri.source_read_cb=Dosya_Bitiş;
        /* One extra output byte lets inflate consume/check the end marker. */
        hedef_veri.dest_start=hedef_veri.dest=풀린자료;hedef_veri.dest_limit=풀린자료+sürüm_boyutlandırmak+1;
        int 반환값=uzlib_uncompress(&hedef_veri);
        if(반환값!=UZLIB_DONE || hedef_veri.eof || hedef_veri.dest!=풀린자료+sürüm_boyutlandırmak || hedef_veri.source!=hedef_veri.source_limit)return -8;
        for(unsigned 순번=0;순번<sürüm_boyutlandırmak;순번++)KR_veri[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(KR_veri,sürüm_boyutlandırmak,0xffffffffu)^0xffffffffu)!=네바이트읽기(geçerli_konum+16))return -8;
    return sürüm_boyutlandırmak;
}
int 꾸러미읽기(const char *İsim, unsigned char *KR_veri, unsigned tampon_kapasite) {
    if(!항목들)return -2;unsigned öğe_BAĞ_DEĞ_SAY=süre_değer(İsim),geçerli_konum=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(geçerli_konum+28);
        if(이름길이==öğe_BAĞ_DEĞ_SAY && 같음(Arşiv+geçerli_konum+46,(const unsigned char*)İsim,öğe_BAĞ_DEĞ_SAY))return üye(geçerli_konum,KR_veri,tampon_kapasite);
        geçerli_konum+=46+이름길이+두바이트읽기(geçerli_konum+30)+두바이트읽기(geçerli_konum+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return girdi_Sınıf; }
int 꾸러미열기(const char *Dosya_girdi_ad) {
    항목들=0;girdi_Sınıf[0]=0;
    intptr_t dosya_tanıtıcısı=사용자호출(3,(uintptr_t)Dosya_girdi_ad,0,0,0,0,0);if(dosya_tanıtıcısı<0)return dosya_tanıtıcısı;
    intptr_t öğe_BAĞ_DEĞ_SAY=사용자호출(9,dosya_tanıtıcısı,0,0,0,0,0);
    if(öğe_BAĞ_DEĞ_SAY<22 || öğe_BAĞ_DEĞ_SAY>(intptr_t)sizeof(Arşiv)) { 사용자호출(4,dosya_tanıtıcısı,0,0,0,0,0);return -8; }
    intptr_t GETİRİ_BAĞ_DEĞ_SAY=사용자호출(2,dosya_tanıtıcısı,(uintptr_t)Arşiv,öğe_BAĞ_DEĞ_SAY,0,0,0);사용자호출(4,dosya_tanıtıcısı,0,0,0,0,0);
    if(GETİRİ_BAĞ_DEĞ_SAY!=öğe_BAĞ_DEĞ_SAY)return -5;Boyut=öğe_BAĞ_DEĞ_SAY;
    unsigned Bitiş_Ofset=Boyut-22;
    for(;;) { if(네바이트읽기(Bitiş_Ofset)==0x06054b50 && Bitiş_Ofset+22+두바이트읽기(Bitiş_Ofset+20)==Boyut)break; if(!Bitiş_Ofset)return -8;Bitiş_Ofset--; }
    unsigned girdi_BAĞ_DEĞ_SAY=두바이트읽기(Bitiş_Ofset+10);중앙목록=네바이트읽기(Bitiş_Ofset+16);
    if(두바이트읽기(Bitiş_Ofset+4)||두바이트읽기(Bitiş_Ofset+6)||두바이트읽기(Bitiş_Ofset+8)!=girdi_BAĞ_DEĞ_SAY||!girdi_BAĞ_DEĞ_SAY||girdi_BAĞ_DEĞ_SAY>256||!klip(중앙목록,네바이트읽기(Bitiş_Ofset+12),Bitiş_Ofset)||중앙목록+네바이트읽기(Bitiş_Ofset+12)!=Bitiş_Ofset)return -8;
    unsigned geçerli_konum=중앙목록;
    for(unsigned 순번=0;순번<girdi_BAĞ_DEĞ_SAY;순번++) {
        if(!klip(geçerli_konum,46,Bitiş_Ofset)||네바이트읽기(geçerli_konum)!=0x02014b50||두바이트읽기(geçerli_konum+34))return -8;
        unsigned 이름길이=두바이트읽기(geçerli_konum+28),Sonraki_öğe=46+이름길이+두바이트읽기(geçerli_konum+30)+두바이트읽기(geçerli_konum+32);
        if(!이름길이||이름길이>511||!klip(geçerli_konum,Sonraki_öğe,Bitiş_Ofset)||네바이트읽기(geçerli_konum+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arşiv[geçerli_konum+46+안쪽순번])return -8;
        unsigned Diğer_girdi=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned süre_veri=두바이트읽기(Diğer_girdi+28);if(süre_veri==이름길이&&같음(Arşiv+Diğer_girdi+46,Arşiv+geçerli_konum+46,süre_veri))return -8;Diğer_girdi+=46+süre_veri+두바이트읽기(Diğer_girdi+30)+두바이트읽기(Diğer_girdi+32);}
        geçerli_konum+=Sonraki_öğe;
    }
    if(geçerli_konum!=Bitiş_Ofset)return -8;항목들=girdi_BAĞ_DEĞ_SAY;
    unsigned char paket_iş_bildirim[4096];int Grup_boyutlandırmak=꾸러미읽기("META-INF/MANIFEST.MF",paket_iş_bildirim,sizeof(paket_iş_bildirim)-1);if(Grup_boyutlandırmak<0){항목들=0;return -8;}
    paket_iş_bildirim[Grup_boyutlandırmak]=0;
    char 논리크기[512];unsigned 사용량=0,Dizin_değer=0;int 진입점있음=0;
    while(Dizin_değer<(unsigned)Grup_boyutlandırmak) {
        unsigned çalıştır=Dizin_değer;while(Dizin_değer<(unsigned)Grup_boyutlandırmak && paket_iş_bildirim[Dizin_değer]!='\n')Dizin_değer++;
        unsigned süre_veri=Dizin_değer-çalıştır;if(Dizin_değer<(unsigned)Grup_boyutlandırmak)Dizin_değer++;if(süre_veri && paket_iş_bildirim[çalıştır+süre_veri-1]=='\r')süre_veri--;
        if(사용량 && süre_veri && paket_iş_bildirim[çalıştır]==' ') {çalıştır++;süre_veri--;}
        else {
            int sonuç=öznitelik_veri(논리크기,사용량,&진입점있음);if(sonuç)return sonuç;
            사용량=0;if(!süre_veri)break;
        }
        if(süre_veri>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<süre_veri;순번++)논리크기[사용량++]=paket_iş_bildirim[çalıştır+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int sonuç=öznitelik_veri(논리크기,사용량,&진입점있음);if(sonuç)return sonuç;
    return 진입점있음?0:-8;
}
