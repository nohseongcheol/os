#include "../명명/기계연결이름.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "호출.h"
#include "paket.h"
#include "uzlib.h"
static unsigned char Arsip[16384], 풀린자료[16385];
static unsigned Ukuran, 중앙목록, 항목들;
static char entri_Kelas[256];
static unsigned 두바이트읽기(unsigned saat_ini_posisi) { return Arsip[saat_ini_posisi] | Arsip[saat_ini_posisi+1] << 8; }
static uint32_t 네바이트읽기(unsigned saat_ini_posisi) { return 두바이트읽기(saat_ini_posisi) | (uint32_t)두바이트읽기(saat_ini_posisi+2) << 16; }
static int klip(unsigned saat_ini_posisi, unsigned item_COUNT, unsigned 한도) { return saat_ini_posisi <= 한도 && item_COUNT <= 한도-saat_ini_posisi; }
static size_t panjang_VALUE(const char *string_data) { size_t item_COUNT=0; while(string_data[item_COUNT]) item_COUNT++; return item_COUNT; }
static int 같음(const unsigned char *첫째값, const unsigned char *SECOND_VALUE, unsigned item_COUNT) { for(unsigned 순번=0;순번<item_COUNT;순번++)if(첫째값[순번]!=SECOND_VALUE[순번])return 0;return 1; }
static int file_mengakhiri(void *미사용값) { (void)미사용값; return -1; }
static int atribut_data(const char *baris_masukan,unsigned 사용량,int *진입점있음) {
    if(사용량>=12 && 같음((const unsigned char*)baris_masukan,(const unsigned char*)"Class-Path: ",12))return -95;
    if(사용량>=12 && 같음((const unsigned char*)baris_masukan,(const unsigned char*)"Main-Class: ",12)) {
        unsigned VALUE=사용량-12;if(*진입점있음||!VALUE||VALUE>=sizeof(entri_Kelas))return -8;
        for(unsigned 순번=0;순번<VALUE;순번++){unsigned char kode_karakter=baris_masukan[12+순번];if(kode_karakter<=32||kode_karakter=='/'||kode_karakter=='\\')return -8;entri_Kelas[순번]=kode_karakter;}
        entri_Kelas[VALUE]=0;*진입점있음=1;
    }
    return 0;
}
static int anggota(unsigned saat_ini_posisi, unsigned char *KR_data, unsigned 용량한도) {
    unsigned metode_entri=두바이트읽기(saat_ini_posisi+10), konfigurasi_Background_Intelligent_Transfer_Service=두바이트읽기(saat_ini_posisi+8), 압축크기=네바이트읽기(saat_ini_posisi+20), lepas_ukuran=네바이트읽기(saat_ini_posisi+24), lokal=네바이트읽기(saat_ini_posisi+42);
    unsigned Nama_2=두바이트읽기(saat_ini_posisi+28);
    if(lepas_ukuran>용량한도 || lepas_ukuran>16384 || (metode_entri!=0 && metode_entri!=8) || (konfigurasi_Background_Intelligent_Transfer_Service&~0x80e))return -8;
    if(!klip(lokal,30,중앙목록) || 네바이트읽기(lokal)!=0x04034b50 || 두바이트읽기(lokal+8)!=metode_entri || 두바이트읽기(lokal+6)!=konfigurasi_Background_Intelligent_Transfer_Service || 두바이트읽기(lokal+26)!=Nama_2)return -8;
    unsigned Mulai_OFFSET=lokal+30, 추가영역=두바이트읽기(lokal+28);
    if(!klip(Mulai_OFFSET,Nama_2,중앙목록) || !같음(Arsip+Mulai_OFFSET,Arsip+saat_ini_posisi+46,Nama_2))return -8;
    Mulai_OFFSET+=Nama_2;if(!klip(Mulai_OFFSET,추가영역,중앙목록))return -8;Mulai_OFFSET+=추가영역;
    if(!klip(Mulai_OFFSET,압축크기,중앙목록))return -8;
    if(!(konfigurasi_Background_Intelligent_Transfer_Service&8) && (네바이트읽기(lokal+14)!=네바이트읽기(saat_ini_posisi+16) || 네바이트읽기(lokal+18)!=압축크기 || 네바이트읽기(lokal+22)!=lepas_ukuran))return -8;
    if(metode_entri==0) { if(압축크기!=lepas_ukuran)return -8; for(unsigned 순번=0;순번<lepas_ukuran;순번++)KR_data[순번]=Arsip[Mulai_OFFSET+순번]; }
    else {
        uzlib_uncomp_t tujuan_data={0};uzlib_uncompress_init(&tujuan_data,0,0);
        tujuan_data.source=Arsip+Mulai_OFFSET;tujuan_data.source_limit=tujuan_data.source+압축크기;tujuan_data.source_read_cb=file_mengakhiri;
        /* One extra output byte lets inflate consume/check the end marker. */
        tujuan_data.dest_start=tujuan_data.dest=풀린자료;tujuan_data.dest_limit=풀린자료+lepas_ukuran+1;
        int 반환값=uzlib_uncompress(&tujuan_data);
        if(반환값!=UZLIB_DONE || tujuan_data.eof || tujuan_data.dest!=풀린자료+lepas_ukuran || tujuan_data.source!=tujuan_data.source_limit)return -8;
        for(unsigned 순번=0;순번<lepas_ukuran;순번++)KR_data[순번]=풀린자료[순번];
    }
    if((uzlib_crc32(KR_data,lepas_ukuran,0xffffffffu)^0xffffffffu)!=네바이트읽기(saat_ini_posisi+16))return -8;
    return lepas_ukuran;
}
int 꾸러미읽기(const char *Nama_2, unsigned char *KR_data, unsigned buffer_kapasitas) {
    if(!항목들)return -2;unsigned item_COUNT=panjang_VALUE(Nama_2),saat_ini_posisi=중앙목록;
    for(unsigned 순번=0;순번<항목들;순번++) {
        unsigned 이름길이=두바이트읽기(saat_ini_posisi+28);
        if(이름길이==item_COUNT && 같음(Arsip+saat_ini_posisi+46,(const unsigned char*)Nama_2,item_COUNT))return anggota(saat_ini_posisi,KR_data,buffer_kapasitas);
        saat_ini_posisi+=46+이름길이+두바이트읽기(saat_ini_posisi+30)+두바이트읽기(saat_ini_posisi+32);
    }
    return -2;
}
const char *꾸러미진입클래스(void) { return entri_Kelas; }
int 꾸러미열기(const char *file_entri_nama) {
    항목들=0;entri_Kelas[0]=0;
    intptr_t file_handel=사용자호출(3,(uintptr_t)file_entri_nama,0,0,0,0,0);if(file_handel<0)return file_handel;
    intptr_t item_COUNT=사용자호출(9,file_handel,0,0,0,0,0);
    if(item_COUNT<22 || item_COUNT>(intptr_t)sizeof(Arsip)) { 사용자호출(4,file_handel,0,0,0,0,0);return -8; }
    intptr_t RECEIVED_COUNT=사용자호출(2,file_handel,(uintptr_t)Arsip,item_COUNT,0,0,0);사용자호출(4,file_handel,0,0,0,0,0);
    if(RECEIVED_COUNT!=item_COUNT)return -5;Ukuran=item_COUNT;
    unsigned mengakhiri_OFFSET=Ukuran-22;
    for(;;) { if(네바이트읽기(mengakhiri_OFFSET)==0x06054b50 && mengakhiri_OFFSET+22+두바이트읽기(mengakhiri_OFFSET+20)==Ukuran)break; if(!mengakhiri_OFFSET)return -8;mengakhiri_OFFSET--; }
    unsigned entri_COUNT=두바이트읽기(mengakhiri_OFFSET+10);중앙목록=네바이트읽기(mengakhiri_OFFSET+16);
    if(두바이트읽기(mengakhiri_OFFSET+4)||두바이트읽기(mengakhiri_OFFSET+6)||두바이트읽기(mengakhiri_OFFSET+8)!=entri_COUNT||!entri_COUNT||entri_COUNT>256||!klip(중앙목록,네바이트읽기(mengakhiri_OFFSET+12),mengakhiri_OFFSET)||중앙목록+네바이트읽기(mengakhiri_OFFSET+12)!=mengakhiri_OFFSET)return -8;
    unsigned saat_ini_posisi=중앙목록;
    for(unsigned 순번=0;순번<entri_COUNT;순번++) {
        if(!klip(saat_ini_posisi,46,mengakhiri_OFFSET)||네바이트읽기(saat_ini_posisi)!=0x02014b50||두바이트읽기(saat_ini_posisi+34))return -8;
        unsigned 이름길이=두바이트읽기(saat_ini_posisi+28),Berikutnya_item=46+이름길이+두바이트읽기(saat_ini_posisi+30)+두바이트읽기(saat_ini_posisi+32);
        if(!이름길이||이름길이>511||!klip(saat_ini_posisi,Berikutnya_item,mengakhiri_OFFSET)||네바이트읽기(saat_ini_posisi+24)>16384)return -8;
        for(unsigned 안쪽순번=0;안쪽순번<이름길이;안쪽순번++)if(!Arsip[saat_ini_posisi+46+안쪽순번])return -8;
        unsigned 다른항목=중앙목록;
        for(unsigned 안쪽순번=0;안쪽순번<순번;안쪽순번++){unsigned panjang_data=두바이트읽기(다른항목+28);if(panjang_data==이름길이&&같음(Arsip+다른항목+46,Arsip+saat_ini_posisi+46,panjang_data))return -8;다른항목+=46+panjang_data+두바이트읽기(다른항목+30)+두바이트읽기(다른항목+32);}
        saat_ini_posisi+=Berikutnya_item;
    }
    if(saat_ini_posisi!=mengakhiri_OFFSET)return -8;항목들=entri_COUNT;
    unsigned char 꾸러미명세[4096];int grup_ukuran=꾸러미읽기("META-INF/MANIFEST.MF",꾸러미명세,sizeof(꾸러미명세)-1);if(grup_ukuran<0){항목들=0;return -8;}
    꾸러미명세[grup_ukuran]=0;
    char 논리크기[512];unsigned 사용량=0,INDEX_VALUE=0;int 진입점있음=0;
    while(INDEX_VALUE<(unsigned)grup_ukuran) {
        unsigned jalankan=INDEX_VALUE;while(INDEX_VALUE<(unsigned)grup_ukuran && 꾸러미명세[INDEX_VALUE]!='\n')INDEX_VALUE++;
        unsigned panjang_data=INDEX_VALUE-jalankan;if(INDEX_VALUE<(unsigned)grup_ukuran)INDEX_VALUE++;if(panjang_data && 꾸러미명세[jalankan+panjang_data-1]=='\r')panjang_data--;
        if(사용량 && panjang_data && 꾸러미명세[jalankan]==' ') {jalankan++;panjang_data--;}
        else {
            int hasil=atribut_data(논리크기,사용량,&진입점있음);if(hasil)return hasil;
            사용량=0;if(!panjang_data)break;
        }
        if(panjang_data>sizeof(논리크기)-사용량)return -8;
        for(unsigned 순번=0;순번<panjang_data;순번++)논리크기[사용량++]=꾸러미명세[jalankan+순번];
    }
    /* The last attribute may be followed by only one newline. */
    int hasil=atribut_data(논리크기,사용량,&진입점있음);if(hasil)return hasil;
    return 진입점있음?0:-8;
}
