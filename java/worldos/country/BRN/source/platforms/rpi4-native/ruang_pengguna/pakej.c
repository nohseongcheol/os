#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "pakej.h"
#include "uzlib.h"
static unsigned char Arkib[16384], 풀린자료[16385];
static unsigned Saiz, 중앙목록, 항목들;
static char pemasukan_Kelas[256];
static unsigned 두바이트읽기(unsigned 현재위치) { return Arkib[현재위치] | Arkib[현재위치+1] << 8; }
static uint32_t 네바이트읽기(unsigned 현재위치) { return 두바이트읽기(현재위치) | (uint32_t)두바이트읽기(현재위치+2) << 16; }
static int klip(unsigned 현재위치, unsigned item_COUNT, unsigned 한도) { return 현재위치 <= 한도 && item_COUNT <= 한도-현재위치; }
static size_t kepanjangan_VALUE(const char *rentetan_data) { size_t item_COUNT=0; while(rentetan_data[item_COUNT]) item_COUNT++; return item_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned item_COUNT) { for(unsigned 순번=0;순번<item_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int fail_tamat(void *미사용값) { (void)미사용값; return -1; }
static int atribut_data(const char *baris,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)baris,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)baris,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(pemasukan_Kelas))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char titik_kod=baris[12+순번];if(titik_kod<=32||titik_kod=='/'||titik_kod=='\\')return -8;pemasukan_Kelas[순번]=titik_kod;}
        pemasukan_Kelas[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int ahli(unsigned 현재위치, unsigned char *ukuran_data, unsigned 용량한도) {
    unsigned kaedah_pemasukan=두바이트읽기(현재위치+10), konfigurasi_Background_Intelligent_Transfer_Service=두바이트읽기(현재위치+8), 압축크기=네바이트읽기(현재위치+20), keluaran_saiz=네바이트읽기(현재위치+24), setempat=네바이트읽기(현재위치+42);
    unsigned Nama=두바이트읽기(현재위치+28);
    if(keluaran_saiz>용량한도 || keluaran_saiz>16384 || (kaedah_pemasukan!=0 && kaedah_pemasukan!=8) || (konfigurasi_Background_Intelligent_Transfer_Service&~0x80e))return -8;
    if(!klip(setempat,30,중앙목록) || 네바이트읽기(setempat)!=0x04034b50 || 두바이트읽기(setempat+8)!=kaedah_pemasukan || 두바이트읽기(setempat+6)!=konfigurasi_Background_Intelligent_Transfer_Service || 두바이트읽기(setempat+26)!=Nama)return -8;
    unsigned Mula_Ofset=setempat+30, 추가영역=두바이트읽기(setempat+28);
    if(!klip(Mula_Ofset,Nama,중앙목록) || !같음(Arkib+Mula_Ofset,Arkib+현재위치+46,Nama))return -8;
    Mula_Ofset+=Nama;if(!klip(Mula_Ofset,추가영역,중앙목록))return -8;Mula_Ofset+=추가영역;
    if(!klip(Mula_Ofset,압축크기,중앙목록))return -8;
    if(!(konfigurasi_Background_Intelligent_Transfer_Service&8) && (네바이트읽기(setempat+14)!=네바이트읽기(현재위치+16) || 네바이트읽기(setempat+18)!=압축크기 || 네바이트읽기(setempat+22)!=keluaran_saiz))return -8;
    if(kaedah_pemasukan==0) { if(압축크기!=keluaran_saiz)return -8; for(unsigned 순번=0;순번<keluaran_saiz;순번++)ukuran_data[순번]=Arkib[Mula_Ofset+순번]; }
    else {
        uzlib_uncomp_t destinasi_data={0};uzlib_uncompress_init(&destinasi_data,0,0);
        destinasi_data.source=Arkib+Mula_Ofset;destinasi_data.source_limit=destinasi_data.source+압축크기;destinasi_data.source_read_cb=fail_tamat;
        /* One extra output byte lets inflate consume/check the end marker. */
        destinasi_data.dest_start=destinasi_data.dest=풀린자료;destinasi_data.dest_limit=풀린자료+keluaran_saiz+1;
        int 반환값=uzlib_uncompress(&destinasi_data);
        if(반환값!=UZLIB_DONE || destinasi_data.eof || destinasi_data.dest!=풀린자료+keluaran_saiz || destinasi_data.source!=destinasi_data.source_limit)return -8;
        for(unsigned 순번=0;순번<keluaran_saiz;순번++)ukuran_data[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(ukuran_data,keluaran_saiz,0xffffffffu)^0xffffffffu)!=네바이트읽기(현재위치+16))return -8;
    return keluaran_saiz;
}
int 꾸러미읽기(const char *Nama, unsigned char *ukuran_data, unsigned penimbal_kapasiti) {
    if(!항목들)return -2;unsigned item_COUNT=kepanjangan_VALUE(Nama),현재위치=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(현재위치+28);
        if(이름길이==item_COUNT && 같음(Arkib+현재위치+46,(const unsigned char*)Nama,item_COUNT))return ahli(현재위치,ukuran_data,penimbal_kapasiti);
        현재위치+=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return pemasukan_Kelas; }
int 꾸러미열기(const char *fail_pemasukan_nama) {
    항목들=0;pemasukan_Kelas[0]=0;
    intptr_t fail_pemegang=사용자호출(3,(uintptr_t)fail_pemasukan_nama,0,0,0,0,0);if(fail_pemegang<0)return fail_pemegang;
    intptr_t item_COUNT=사용자호출(9,fail_pemegang,0,0,0,0,0);
    if(item_COUNT<22 || item_COUNT>(intptr_t)sizeof(Arkib)) { 사용자호출(4,fail_pemegang,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,fail_pemegang,(uintptr_t)Arkib,item_COUNT,0,0,0);사용자호출(4,fail_pemegang,0,0,0,0,0);
    if(RECEIVED_COUNT!=item_COUNT)return -5;Saiz=item_COUNT;
    unsigned tamat_Ofset=Saiz-22;
    for(;;) { if(네바이트읽기(tamat_Ofset)==0x06054b50 && tamat_Ofset+22+두바이트읽기(tamat_Ofset+20)==Saiz)break; if(!tamat_Ofset)return -8;tamat_Ofset--; }
    unsigned pemasukan_COUNT=두바이트읽기(tamat_Ofset+10);중앙목록=네바이트읽기(tamat_Ofset+16);
    if(두바이트읽기(tamat_Ofset+4)||두바이트읽기(tamat_Ofset+6)||두바이트읽기(tamat_Ofset+8)!=pemasukan_COUNT||!pemasukan_COUNT||pemasukan_COUNT>256||!klip(중앙목록,네바이트읽기(tamat_Ofset+12),tamat_Ofset)||중앙목록+네바이트읽기(tamat_Ofset+12)!=tamat_Ofset)return -8;
    unsigned 현재위치=중앙목록;
    for(unsigned 순번=0;순번<pemasukan_COUNT;순번++) {
        if(!klip(현재위치,46,tamat_Ofset)||네바이트읽기(현재위치)!=0x02014b50||두바이트읽기(현재위치+34))return -8;
        unsigned 이름길이=두바이트읽기(현재위치+28),Seterusnya_item=46+이름길이+두바이트읽기(현재위치+30)+두바이트읽기(현재위치+32);
        if(!이름길이||이름길이>511||!klip(현재위치,Seterusnya_item,tamat_Ofset)||네바이트읽기(현재위치+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arkib[현재위치+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned kepanjangan_data=두바이트읽기(다른항목+28);if(kepanjangan_data==이름길이&&같음(Arkib+다른항목+46,Arkib+현재위치+46,kepanjangan_data))return -8;다른항목+=46+kepanjangan_data+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        현재위치+=Seterusnya_item;
    }
    if(현재위치!=tamat_Ofset)return -8;항목들=pemasukan_COUNT;
    unsigned char pakej_manifes_aplikasi[4096];int Kumpulan_saiz=꾸러미읽기("META-INF/MANIFEST.MF",pakej_manifes_aplikasi,sizeof(pakej_manifes_aplikasi)-1);if(Kumpulan_saiz<0){항목들=0;return -8;}
    pakej_manifes_aplikasi[Kumpulan_saiz]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)Kumpulan_saiz) {
        unsigned Jalan=INDEX_VALUE;while(INDEX_VALUE<(unsigned)Kumpulan_saiz && pakej_manifes_aplikasi[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned kepanjangan_data=INDEX_VALUE-Jalan;if(INDEX_VALUE<(unsigned)Kumpulan_saiz)INDEX_VALUE++;if(kepanjangan_data && pakej_manifes_aplikasi[Jalan+kepanjangan_data-1]=='\r')kepanjangan_data--;
        if(사용량 && kepanjangan_data && pakej_manifes_aplikasi[Jalan]==' ') {Jalan++;kepanjangan_data--;}
        else {
            int ukuran=atribut_data(논리크기,사용량,&진입점있음);if(ukuran)return ukuran;
            사용량=0;if(!kepanjangan_data)break;
        }
        if(kepanjangan_data>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<kepanjangan_data;순번++)논리크기[사용량++]=pakej_manifes_aplikasi[Jalan+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int ukuran=atribut_data(논리크기,사용량,&진입점있음);if(ukuran)return ukuran;
    return 진입점있음?0:-8;
}
