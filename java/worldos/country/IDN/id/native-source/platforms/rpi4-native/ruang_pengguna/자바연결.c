#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 berkas/keluaranTeks/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "paket.h"
typedef uintptr_t mesin_Kata;
static int area_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static mesin_Kata 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned item_COUNT, mesin_Kata 첫째값, mesin_Kata SECOND_VALUE, mesin_Kata kode_karakter) {
    return 사용자호출(item_COUNT, 첫째값, SECOND_VALUE, kode_karakter, 0, 0, 0);
}
static void 바이트들(const char *data_posisi, size_t item_COUNT) { 호출(1, 1, (mesin_Kata)data_posisi, item_COUNT); }
static void karakter(unsigned kode_karakter) {
    unsigned char data[4]; unsigned item_COUNT = 0;
    if (kode_karakter < 128) data[item_COUNT++] = kode_karakter;
    else if (kode_karakter < 2048) { data[item_COUNT++] = 0xc0 | (kode_karakter >> 6); data[item_COUNT++] = 0x80 | (kode_karakter & 63); }
    else if (kode_karakter < 65536) { data[item_COUNT++] = 0xe0 | (kode_karakter >> 12); data[item_COUNT++] = 0x80 | ((kode_karakter >> 6) & 63); data[item_COUNT++] = 0x80 | (kode_karakter & 63); }
    else { data[item_COUNT++] = 0xf0 | (kode_karakter >> 18); data[item_COUNT++] = 0x80 | ((kode_karakter >> 12) & 63); data[item_COUNT++] = 0x80 | ((kode_karakter >> 6) & 63); data[item_COUNT++] = 0x80 | (kode_karakter & 63); }
    바이트들((const char *)data, item_COUNT);
}
mesin_Kata alat_karakter(mesin_Kata VALUE) {
    unsigned kode_karakter = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (kode_karakter >= 0xdc00 && kode_karakter <= 0xdfff) { karakter(0x10000 + ((높은부분 - 0xd800) << 10) + kode_karakter - 0xdc00); return 1; }
        karakter(0xfffd);
    }
    if (kode_karakter >= 0xd800 && kode_karakter <= 0xdbff) 대기중짝글자 = kode_karakter;
    else karakter(kode_karakter > 0x10ffff || (kode_karakter >= 0xdc00 && kode_karakter <= 0xdfff) ? 0xfffd : kode_karakter);
    return 1;
}
mesin_Kata alat_cetak(mesin_Kata VALUE) {
    const mesin_Kata *string_data = (const mesin_Kata *)VALUE;
    for (mesin_Kata 순번 = 0; 순번 < string_data[0]; 순번++) alat_karakter(string_data[순번 + 1]);
    return string_data[0];
}
static int jalur(mesin_Kata objek_Referensi, char KR_data[512]) {
    const mesin_Kata *첫째값 = (const mesin_Kata *)objek_Referensi;
    unsigned 사용량 = 0;
    for (mesin_Kata 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned kode_karakter = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] metode_MODE 경로와 호환한다.
        if (kode_karakter >= 0xd800 && kode_karakter <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; kode_karakter = 0x10000 + ((kode_karakter - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (kode_karakter >= 0xd800 && kode_karakter <= 0xdfff) return -22;
        unsigned item_COUNT = kode_karakter < 128 ? 1 : kode_karakter < 2048 ? 2 : kode_karakter < 65536 ? 3 : 4;
        if (사용량 + item_COUNT > 511) return -36;
        if (item_COUNT == 1) KR_data[사용량++] = kode_karakter;
        else {
            KR_data[사용량++] = (item_COUNT == 2 ? 0xc0 : item_COUNT == 3 ? 0xe0 : 0xf0) | (kode_karakter >> (6 * (item_COUNT - 1)));
            for (unsigned 안쪽순번 = item_COUNT - 1; 안쪽순번; 안쪽순번--) KR_data[사용량++] = 0x80 | ((kode_karakter >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    KR_data[사용량] = 0; return 사용량 ? 0 : -22;
}
mesin_Kata alat_buat(mesin_Kata Nama_2, mesin_Kata konfigurasi_Background_Intelligent_Transfer_Service) {
    char data_posisi[512]; int galat = jalur(Nama_2, data_posisi);
    return (uint32_t)(galat ? galat : 호출(3, (mesin_Kata)data_posisi, konfigurasi_Background_Intelligent_Transfer_Service, 0));
}
mesin_Kata alat_Tutup(mesin_Kata file_handel) { return (uint32_t)호출(4, file_handel, 0, 0); }
mesin_Kata 도구바이트읽기(mesin_Kata file_handel) {
    unsigned char SECOND_VALUE; intptr_t item_COUNT = 호출(2, file_handel, (mesin_Kata)&SECOND_VALUE, 1);
    return (uint32_t)(item_COUNT == 1 ? SECOND_VALUE : item_COUNT == 0 ? 256 : item_COUNT);
}
mesin_Kata alat_tulis_byte(mesin_Kata file_handel, mesin_Kata VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, file_handel, (mesin_Kata)&SECOND_VALUE, 1);
}
mesin_Kata 도구읽기(mesin_Kata Nama_2, mesin_Kata tujuan_data_surel) {
    if (꾸러미사용중) {
        char data_posisi[512]; int galat = jalur(Nama_2, data_posisi); if (galat) return (uint32_t)galat;
        unsigned item_COUNT = 0; while (data_posisi[item_COUNT]) item_COUNT++;
        if (item_COUNT >= 6) for (unsigned 순번 = 0; 순번 < item_COUNT - 6; 순번++) if (data_posisi[순번] == '.') data_posisi[순번] = '/';
        unsigned char 바이트들[16384]; mesin_Kata *tujuan_VALUE_posisi = (mesin_Kata *)tujuan_data_surel;
        int RECEIVED_COUNT = 꾸러미읽기(data_posisi, 바이트들, tujuan_VALUE_posisi[0] < sizeof(바이트들) ? tujuan_VALUE_posisi[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) tujuan_VALUE_posisi[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int file_handel = 꾸러미사용중 ? -2 : (int32_t)alat_buat(Nama_2, 0);
    if (file_handel < 0) {
        char data_posisi[512]; int galat = jalur(Nama_2, data_posisi); if (galat) return (uint32_t)galat;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Berikutnya_OFFSET = 자바클래스들[순번].Nama_2; unsigned 안쪽순번 = 0;
            while (data_posisi[안쪽순번] && data_posisi[안쪽순번] == Berikutnya_OFFSET[안쪽순번]) 안쪽순번++;
            if (data_posisi[안쪽순번] || Berikutnya_OFFSET[안쪽순번]) continue;
            mesin_Kata *tujuan_VALUE_posisi = (mesin_Kata *)tujuan_data_surel;
            if (tujuan_VALUE_posisi[0] < 자바클래스들[순번].Ukuran) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Ukuran; 안쪽순번++) tujuan_VALUE_posisi[안쪽순번 + 1] = 자바클래스들[순번].data[안쪽순번];
            return 자바클래스들[순번].Ukuran;
        }
        return (uint32_t)file_handel;
    }
    mesin_Kata *첫째값 = (mesin_Kata *)tujuan_data_surel;
    intptr_t Ukuran = 호출(9, file_handel, 0, 0), Selesai_jumlah = 0;
    if (Ukuran < 0 || (mesin_Kata)Ukuran > 첫째값[0]) { alat_Tutup(file_handel); return (uint32_t)(Ukuran < 0 ? Ukuran : -27); }
    unsigned char blok_data[256];
    while (Selesai_jumlah < Ukuran) {
        intptr_t item_COUNT = 호출(2, file_handel, (mesin_Kata)blok_data, Ukuran - Selesai_jumlah < 256 ? Ukuran - Selesai_jumlah : 256);
        if (item_COUNT <= 0) { alat_Tutup(file_handel); return (uint32_t)(item_COUNT ? item_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < item_COUNT; 순번++) 첫째값[1 + Selesai_jumlah + 순번] = blok_data[순번];
        Selesai_jumlah += item_COUNT;
    }
    alat_Tutup(file_handel); return Selesai_jumlah;
}
mesin_Kata alat_tulis(mesin_Kata Nama_2, mesin_Kata 원본자료, mesin_Kata entri_COUNT) {
    const mesin_Kata *첫째값 = (const mesin_Kata *)원본자료;
    if (entri_COUNT > 첫째값[0] || entri_COUNT > 16384) return (uint32_t)-27;
    int file_handel = (int32_t)alat_buat(Nama_2, 577); if (file_handel < 0) return (uint32_t)file_handel;
    unsigned char blok_data[256]; mesin_Kata Selesai_jumlah = 0;
    while (Selesai_jumlah < entri_COUNT) {
        mesin_Kata item_COUNT = entri_COUNT - Selesai_jumlah < 256 ? entri_COUNT - Selesai_jumlah : 256;
        for (mesin_Kata 순번 = 0; 순번 < item_COUNT; 순번++) blok_data[순번] = 첫째값[1 + Selesai_jumlah + 순번];
        intptr_t hasil = 호출(1, file_handel, (mesin_Kata)blok_data, item_COUNT);
        if (hasil <= 0) { alat_Tutup(file_handel); return (uint32_t)(hasil ? hasil : -5); }
        Selesai_jumlah += hasil;
    }
    alat_Tutup(file_handel); return entri_COUNT;
}
mesin_Kata 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
mesin_Kata alat_argumen(mesin_Kata LOOKUP_INDEX) {
    static const mesin_Kata kosong_VALUE[1] = {0};
    if (LOOKUP_INDEX >= 8) return (mesin_Kata)kosong_VALUE;
    unsigned char 입력결과[256]; intptr_t item_COUNT;
    if (꾸러미사용중 && LOOKUP_INDEX == 0) { const char *data_posisi = 꾸러미진입클래스(); item_COUNT = 0; while (data_posisi[item_COUNT] && item_COUNT < 255) { 입력결과[item_COUNT] = data_posisi[item_COUNT]; item_COUNT++; } }
    else item_COUNT = 호출(15, LOOKUP_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (mesin_Kata)입력결과, sizeof(입력결과));
    if (item_COUNT < 0) return (mesin_Kata)kosong_VALUE;
    mesin_Kata *KR_data = 전달인수[LOOKUP_INDEX]; unsigned entri_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < item_COUNT;) {
        unsigned kode_karakter = 입력결과[순번++], 더있음 = kode_karakter < 128 ? 0 : kode_karakter >= 0xc2 && kode_karakter < 0xe0 ? 1 : kode_karakter < 0xf0 && kode_karakter >= 0xe0 ? 2 : kode_karakter >= 0xf0 && kode_karakter <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > item_COUNT) { KR_data[++entri_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) kode_karakter &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { kode_karakter = (kode_karakter << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || kode_karakter < 최소값 || kode_karakter > 0x10ffff || (kode_karakter >= 0xd800 && kode_karakter <= 0xdfff)) kode_karakter = 0xfffd;
        if (kode_karakter >= 65536) { kode_karakter -= 65536; KR_data[++entri_COUNT] = 0xd800 | (kode_karakter >> 10); KR_data[++entri_COUNT] = 0xdc00 | (kode_karakter & 1023); }
        else KR_data[++entri_COUNT] = kode_karakter;
    }
    KR_data[0] = entri_COUNT; return (mesin_Kata)KR_data;
}
mesin_Kata 도구분류(void) { return area_VALUE; }
void 커널중단(const char *알림문) {
    const char *data_posisi = 알림문; while (*data_posisi) data_posisi++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, data_posisi - 알림문); karakter(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Mulai_pengguna_apl(int metode_MODE) {
    area_VALUE = metode_MODE;
    unsigned char 첫항목[256]; intptr_t item_COUNT = 호출(15, 0, (mesin_Kata)첫항목, sizeof(첫항목));
    if (metode_MODE == 2 || (metode_MODE == 1 && item_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = metode_MODE == 2 ? 0 : 1;
        char file_entri_nama[256]; intptr_t panjang_data = 호출(15, 꾸러미인수이동, (mesin_Kata)file_entri_nama, sizeof(file_entri_nama));
        if (panjang_data <= 0 || 꾸러미열기(file_entri_nama) < 0) {
            static const char galat[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(galat, sizeof(galat) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int hasil = 자바진입();
    if (대기중짝글자) karakter(0xfffd);
    return hasil;
}

// UDP는 Asli 커널의 SVC를 통과하며 saat_ini_item 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t famili, nomor_port; uint32_t surel; unsigned char nilai_nol[8]; };
static struct 자바주소 UDP_surel(unsigned nomor_port) {
    struct 자바주소 첫째값 = {2, (uint16_t)((nomor_port << 8) | (nomor_port >> 8)), 0x0100007f, {0}}; return 첫째값;
}
mesin_Kata alat_UDP_buat(mesin_Kata nomor_port) {
    intptr_t file_handel = 호출(32, 2, 2, 17); if (file_handel < 0) return (uint32_t)file_handel;
    struct 자바주소 첫째값 = UDP_surel(nomor_port);
    첫째값.surel = 0;
    intptr_t Status_VALUE = 호출(33, file_handel, (mesin_Kata)&첫째값, sizeof(첫째값));
    if (Status_VALUE < 0) { alat_Tutup(file_handel); return (uint32_t)Status_VALUE; }
    return file_handel;
}
mesin_Kata alat_UDP_kirim(mesin_Kata file_handel, mesin_Kata nomor_port, mesin_Kata ARRAY_VALUE, mesin_Kata panjang_VALUE) {
    const mesin_Kata *원본주소 = (const mesin_Kata *)ARRAY_VALUE; unsigned char data[512];
    if (panjang_VALUE > 512 || panjang_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (mesin_Kata 순번 = 0; 순번 < panjang_VALUE; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_surel(nomor_port);
    return (uint32_t)사용자호출(34, file_handel, (mesin_Kata)data, panjang_VALUE, 0, (mesin_Kata)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t item_COUNT) { return (item_COUNT>>24)|((item_COUNT>>8)&0xff00)|((item_COUNT<<8)&0xff0000)|(item_COUNT<<24); }
mesin_Kata alat_UDP_kirim_surel(mesin_Kata file_handel, mesin_Kata surel, mesin_Kata nomor_port, mesin_Kata ARRAY_VALUE, mesin_Kata panjang_VALUE) {
    const mesin_Kata *원본주소 = (const mesin_Kata *)ARRAY_VALUE; unsigned char data[512];
    if (panjang_VALUE > 512 || panjang_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (mesin_Kata 순번 = 0; 순번 < panjang_VALUE; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_surel(nomor_port); 첫째값.surel = 바이트순서뒤집기(surel);
    return (uint32_t)사용자호출(34, file_handel, (mesin_Kata)data, panjang_VALUE, 0, (mesin_Kata)&첫째값, sizeof(첫째값));
}
mesin_Kata alat_CONNECT(mesin_Kata file_handel, mesin_Kata surel, mesin_Kata nomor_port) {
    struct 자바주소 첫째값 = UDP_surel(nomor_port); 첫째값.surel = 바이트순서뒤집기(surel);
    uint32_t jalankan = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t hasil = 호출(37, file_handel, (mesin_Kata)&첫째값, sizeof(첫째값));
        if (hasil != -115) return (uint32_t)hasil;
        if ((uint32_t)(호출(7, 0, 0, 0) - jalankan) >= 1000) return (uint32_t)-110;
    }
}
mesin_Kata 도구전문받기(mesin_Kata file_handel, mesin_Kata ARRAY_VALUE, mesin_Kata buffer_kapasitas) {
    mesin_Kata *tujuan_surel = (mesin_Kata *)ARRAY_VALUE; unsigned char data[512];
    if (buffer_kapasitas > 512 || tujuan_surel[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned panjang_data = sizeof(첫째값);
    intptr_t item_COUNT = 사용자호출(35, file_handel, (mesin_Kata)data, buffer_kapasitas, 0, (mesin_Kata)&첫째값, (mesin_Kata)&panjang_data);
    if (item_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < item_COUNT; 순번++) tujuan_surel[순번 + 1] = data[순번]; tujuan_surel[513] = (첫째값.nomor_port << 8 | 첫째값.nomor_port >> 8) & 65535; tujuan_surel[514] = 바이트순서뒤집기(첫째값.surel); }
    return (uint32_t)item_COUNT;
}
mesin_Kata alat_UDP_port(mesin_Kata file_handel) {
    struct 자바주소 첫째값; unsigned panjang_data = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, file_handel, (mesin_Kata)&첫째값, (mesin_Kata)&panjang_data);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.nomor_port << 8 | 첫째값.nomor_port >> 8) & 65535);
}
mesin_Kata 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
mesin_Kata 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
mesin_Kata 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
mesin_Kata alat_grafis_tunggu(void) { return (uint32_t)화면키기다리기(); }
mesin_Kata alat_persegi(mesin_Kata koordinat_x, mesin_Kata Y_koordinat, mesin_Kata 너비값, mesin_Kata 높이값, mesin_Kata 색상) {
    return (uint32_t)사용자호출(13, koordinat_x, Y_koordinat, 색상, 너비값, 높이값, 0);
}

mesin_Kata alat_Stream(mesin_Kata Aksi,mesin_Kata file_handel,mesin_Kata VALUE){
    if(Aksi==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_surel(VALUE);
    if(Aksi==1){첫째값.surel=0;intptr_t 반환값=호출(33,file_handel,(mesin_Kata)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,file_handel,4,0));}
    if(Aksi==2)return (uint32_t)호출(37,file_handel,(mesin_Kata)&첫째값,sizeof(첫째값));
    if(Aksi==3)return (uint32_t)호출(39,file_handel,0,0);
    if(Aksi==4)return alat_UDP_port(file_handel);
    if(Aksi==5)return (uint32_t)호출(40,file_handel,0,0);
    return (uint32_t)-22;
}
mesin_Kata alat_GUI(mesin_Kata Aksi,mesin_Kata pengidentifikasi_VALUE,mesin_Kata 첫째값,mesin_Kata SECOND_VALUE,mesin_Kata kode_karakter,mesin_Kata tujuan_data){return (uint32_t)사용자호출(20,Aksi,pengidentifikasi_VALUE,첫째값,SECOND_VALUE,kode_karakter,tujuan_data);}
mesin_Kata alat_GUI_SMS(mesin_Kata pengidentifikasi_VALUE,mesin_Kata ARRAY_VALUE,mesin_Kata item_COUNT){
    const mesin_Kata *원본주소=(const mesin_Kata *)ARRAY_VALUE;uint32_t data[127];unsigned entri_COUNT=0;
    if(item_COUNT>원본주소[0])return (uint32_t)-22;
    for(mesin_Kata 순번=0;순번<item_COUNT;순번++){unsigned pengodean_karakter=원본주소[순번+1];if(pengodean_karakter>=0xd800&&pengodean_karakter<=0xdbff&&순번+1<item_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;pengodean_karakter=0x10000+((pengodean_karakter-0xd800)<<10)+낮은값-0xdc00;}if(entri_COUNT==127)return (uint32_t)-22;data[entri_COUNT++]=pengodean_karakter;}
    return (uint32_t)사용자호출(21,pengidentifikasi_VALUE,(mesin_Kata)data,entri_COUNT,0,0,0);
}
