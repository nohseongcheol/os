#include "../명명/기계연결이름.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Fail/출력/인수는 모두 EL0 SVC를 거친다.
#include "호출.h"
#include "java-resources.h"
#include "pakej.h"
typedef uintptr_t mesin_Word;
static int bidang_VALUE;
static int 꾸러미사용중, 꾸러미인수이동;
static mesin_Word 전달인수[8][257];
static unsigned 대기중짝글자;
extern int32_t 자바진입(void);
static intptr_t 호출(unsigned item_COUNT, mesin_Word 첫째값, mesin_Word SECOND_VALUE, mesin_Word titik_kod) {
    return 사용자호출(item_COUNT, 첫째값, SECOND_VALUE, titik_kod, 0, 0, 0);
}
static void 바이트들(const char *data_jawatan, size_t item_COUNT) { 호출(1, 1, (mesin_Word)data_jawatan, item_COUNT); }
static void aksara(unsigned titik_kod) {
    unsigned char data[4]; unsigned item_COUNT = 0;
    if (titik_kod < 128) data[item_COUNT++] = titik_kod;
    else if (titik_kod < 2048) { data[item_COUNT++] = 0xc0 | (titik_kod >> 6); data[item_COUNT++] = 0x80 | (titik_kod & 63); }
    else if (titik_kod < 65536) { data[item_COUNT++] = 0xe0 | (titik_kod >> 12); data[item_COUNT++] = 0x80 | ((titik_kod >> 6) & 63); data[item_COUNT++] = 0x80 | (titik_kod & 63); }
    else { data[item_COUNT++] = 0xf0 | (titik_kod >> 18); data[item_COUNT++] = 0x80 | ((titik_kod >> 12) & 63); data[item_COUNT++] = 0x80 | ((titik_kod >> 6) & 63); data[item_COUNT++] = 0x80 | (titik_kod & 63); }
    바이트들((const char *)data, item_COUNT);
}
mesin_Word alat_aksara(mesin_Word VALUE) {
    unsigned titik_kod = VALUE;
    if (대기중짝글자) {
        unsigned 높은부분 = 대기중짝글자; 대기중짝글자 = 0;
        if (titik_kod >= 0xdc00 && titik_kod <= 0xdfff) { aksara(0x10000 + ((높은부분 - 0xd800) << 10) + titik_kod - 0xdc00); return 1; }
        aksara(0xfffd);
    }
    if (titik_kod >= 0xd800 && titik_kod <= 0xdbff) 대기중짝글자 = titik_kod;
    else aksara(titik_kod > 0x10ffff || (titik_kod >= 0xdc00 && titik_kod <= 0xdfff) ? 0xfffd : titik_kod);
    return 1;
}
mesin_Word 도구출력(mesin_Word VALUE) {
    const mesin_Word *rentetan_data = (const mesin_Word *)VALUE;
    for (mesin_Word 순번 = 0; 순번 < rentetan_data[0]; 순번++) alat_aksara(rentetan_data[순번 + 1]);
    return rentetan_data[0];
}
static int LALUAN(mesin_Word objek_Rujukan, char ukuran_data[512]) {
    const mesin_Word *첫째값 = (const mesin_Word *)objek_Rujukan;
    unsigned 사용량 = 0;
    for (mesin_Word 순번 = 1; 순번 <= 첫째값[0] && 첫째값[순번]; 순번++) {
        unsigned titik_kod = 첫째값[순번];
        // UTF-16 -> UTF-8. 기존 도구의 char[] kaedah_mod 경로와 호환한다.
        if (titik_kod >= 0xd800 && titik_kod <= 0xdbff && 순번 < 첫째값[0] && 첫째값[순번 + 1] >= 0xdc00 && 첫째값[순번 + 1] <= 0xdfff)
            { unsigned 낮은값 = 첫째값[++순번]; titik_kod = 0x10000 + ((titik_kod - 0xd800) << 10) + 낮은값 - 0xdc00; }
        else if (titik_kod >= 0xd800 && titik_kod <= 0xdfff) return -22;
        unsigned item_COUNT = titik_kod < 128 ? 1 : titik_kod < 2048 ? 2 : titik_kod < 65536 ? 3 : 4;
        if (사용량 + item_COUNT > 511) return -36;
        if (item_COUNT == 1) ukuran_data[사용량++] = titik_kod;
        else {
            ukuran_data[사용량++] = (item_COUNT == 2 ? 0xc0 : item_COUNT == 3 ? 0xe0 : 0xf0) | (titik_kod >> (6 * (item_COUNT - 1)));
            for (unsigned 안쪽순번 = item_COUNT - 1; 안쪽순번; 안쪽순번--) ukuran_data[사용량++] = 0x80 | ((titik_kod >> (6 * (안쪽순번 - 1))) & 63);
        }
    }
    ukuran_data[사용량] = 0; return 사용량 ? 0 : -22;
}
mesin_Word alat_buka(mesin_Word Nama, mesin_Word konfigurasi_Background_Intelligent_Transfer_Service) {
    char data_jawatan[512]; int RALAT = LALUAN(Nama, data_jawatan);
    return (uint32_t)(RALAT ? RALAT : 호출(3, (mesin_Word)data_jawatan, konfigurasi_Background_Intelligent_Transfer_Service, 0));
}
mesin_Word alat_Tutup(mesin_Word fail_pemegang) { return (uint32_t)호출(4, fail_pemegang, 0, 0); }
mesin_Word 도구바이트읽기(mesin_Word fail_pemegang) {
    unsigned char SECOND_VALUE; intptr_t item_COUNT = 호출(2, fail_pemegang, (mesin_Word)&SECOND_VALUE, 1);
    return (uint32_t)(item_COUNT == 1 ? SECOND_VALUE : item_COUNT == 0 ? 256 : item_COUNT);
}
mesin_Word alat_tulis_bait(mesin_Word fail_pemegang, mesin_Word VALUE) {
    unsigned char SECOND_VALUE = VALUE; return (uint32_t)호출(1, fail_pemegang, (mesin_Word)&SECOND_VALUE, 1);
}
mesin_Word 도구읽기(mesin_Word Nama, mesin_Word destinasi_data_e_mel) {
    if (꾸러미사용중) {
        char data_jawatan[512]; int RALAT = LALUAN(Nama, data_jawatan); if (RALAT) return (uint32_t)RALAT;
        unsigned item_COUNT = 0; while (data_jawatan[item_COUNT]) item_COUNT++;
        if (item_COUNT >= 6) for (unsigned 순번 = 0; 순번 < item_COUNT - 6; 순번++) if (data_jawatan[순번] == '.') data_jawatan[순번] = '/';
        unsigned char 바이트들[16384]; mesin_Word *destinasi_VALUE_jawatan = (mesin_Word *)destinasi_data_e_mel;
        int RECEIVED_COUNT = 꾸러미읽기(data_jawatan, 바이트들, destinasi_VALUE_jawatan[0] < sizeof(바이트들) ? destinasi_VALUE_jawatan[0] : sizeof(바이트들));
        if (RECEIVED_COUNT >= 0) { for (int 순번 = 0; 순번 < RECEIVED_COUNT; 순번++) destinasi_VALUE_jawatan[순번 + 1] = 바이트들[순번]; return RECEIVED_COUNT; }
        if (RECEIVED_COUNT != -2) return (uint32_t)RECEIVED_COUNT;
    }
    int fail_pemegang = 꾸러미사용중 ? -2 : (int32_t)alat_buka(Nama, 0);
    if (fail_pemegang < 0) {
        char data_jawatan[512]; int RALAT = LALUAN(Nama, data_jawatan); if (RALAT) return (uint32_t)RALAT;
        for (unsigned 순번 = 0; 순번 < sizeof(자바클래스들) / sizeof(자바클래스들[0]); 순번++) {
            const char *Seterusnya_Ofset = 자바클래스들[순번].Nama; unsigned 안쪽순번 = 0;
            while (data_jawatan[안쪽순번] && data_jawatan[안쪽순번] == Seterusnya_Ofset[안쪽순번]) 안쪽순번++;
            if (data_jawatan[안쪽순번] || Seterusnya_Ofset[안쪽순번]) continue;
            mesin_Word *destinasi_VALUE_jawatan = (mesin_Word *)destinasi_data_e_mel;
            if (destinasi_VALUE_jawatan[0] < 자바클래스들[순번].Saiz) return (uint32_t)-27;
            for (안쪽순번 = 0; 안쪽순번 < 자바클래스들[순번].Saiz; 안쪽순번++) destinasi_VALUE_jawatan[안쪽순번 + 1] = 자바클래스들[순번].data[안쪽순번];
            return 자바클래스들[순번].Saiz;
        }
        return (uint32_t)fail_pemegang;
    }
    mesin_Word *첫째값 = (mesin_Word *)destinasi_data_e_mel;
    intptr_t Saiz = 호출(9, fail_pemegang, 0, 0), Selesai_amaun = 0;
    if (Saiz < 0 || (mesin_Word)Saiz > 첫째값[0]) { alat_Tutup(fail_pemegang); return (uint32_t)(Saiz < 0 ? Saiz : -27); }
    unsigned char blok_data[256];
    while (Selesai_amaun < Saiz) {
        intptr_t item_COUNT = 호출(2, fail_pemegang, (mesin_Word)blok_data, Saiz - Selesai_amaun < 256 ? Saiz - Selesai_amaun : 256);
        if (item_COUNT <= 0) { alat_Tutup(fail_pemegang); return (uint32_t)(item_COUNT ? item_COUNT : -5); }
        for (intptr_t 순번 = 0; 순번 < item_COUNT; 순번++) 첫째값[1 + Selesai_amaun + 순번] = blok_data[순번];
        Selesai_amaun += item_COUNT;
    }
    alat_Tutup(fail_pemegang); return Selesai_amaun;
}
mesin_Word alat_tulis(mesin_Word Nama, mesin_Word 원본자료, mesin_Word pemasukan_COUNT) {
    const mesin_Word *첫째값 = (const mesin_Word *)원본자료;
    if (pemasukan_COUNT > 첫째값[0] || pemasukan_COUNT > 16384) return (uint32_t)-27;
    int fail_pemegang = (int32_t)alat_buka(Nama, 577); if (fail_pemegang < 0) return (uint32_t)fail_pemegang;
    unsigned char blok_data[256]; mesin_Word Selesai_amaun = 0;
    while (Selesai_amaun < pemasukan_COUNT) {
        mesin_Word item_COUNT = pemasukan_COUNT - Selesai_amaun < 256 ? pemasukan_COUNT - Selesai_amaun : 256;
        for (mesin_Word 순번 = 0; 순번 < item_COUNT; 순번++) blok_data[순번] = 첫째값[1 + Selesai_amaun + 순번];
        intptr_t ukuran = 호출(1, fail_pemegang, (mesin_Word)blok_data, item_COUNT);
        if (ukuran <= 0) { alat_Tutup(fail_pemegang); return (uint32_t)(ukuran ? ukuran : -5); }
        Selesai_amaun += ukuran;
    }
    alat_Tutup(fail_pemegang); return pemasukan_COUNT;
}
mesin_Word 도구인수개수(void) { return 호출(15, UINTPTR_MAX, 0, 0) - (꾸러미사용중 ? 꾸러미인수이동 : 0); }
mesin_Word alat_argumen(mesin_Word Carian_INDEX) {
    static const mesin_Word 빈값[1] = {0};
    if (Carian_INDEX >= 8) return (mesin_Word)빈값;
    unsigned char 입력결과[256]; intptr_t item_COUNT;
    if (꾸러미사용중 && Carian_INDEX == 0) { const char *data_jawatan = 꾸러미진입클래스(); item_COUNT = 0; while (data_jawatan[item_COUNT] && item_COUNT < 255) { 입력결과[item_COUNT] = data_jawatan[item_COUNT]; item_COUNT++; } }
    else item_COUNT = 호출(15, Carian_INDEX + (꾸러미사용중 ? 꾸러미인수이동 : 0), (mesin_Word)입력결과, sizeof(입력결과));
    if (item_COUNT < 0) return (mesin_Word)빈값;
    mesin_Word *ukuran_data = 전달인수[Carian_INDEX]; unsigned pemasukan_COUNT = 0;
    for (intptr_t 순번 = 0; 순번 < item_COUNT;) {
        unsigned titik_kod = 입력결과[순번++], 더있음 = titik_kod < 128 ? 0 : titik_kod >= 0xc2 && titik_kod < 0xe0 ? 1 : titik_kod < 0xf0 && titik_kod >= 0xe0 ? 2 : titik_kod >= 0xf0 && titik_kod <= 0xf4 ? 3 : 4;
        if (더있음 == 4 || 순번 + 더있음 > item_COUNT) { ukuran_data[++pemasukan_COUNT] = 0xfffd; continue; }
        unsigned 최소값 = 더있음 == 1 ? 128 : 더있음 == 2 ? 2048 : 더있음 == 3 ? 65536 : 0;
        if (더있음) titik_kod &= (1u << (6 - 더있음)) - 1;
        unsigned 안쪽순번 = 0;
        while (안쪽순번 < 더있음 && (입력결과[순번] & 0xc0) == 0x80) { titik_kod = (titik_kod << 6) | (입력결과[순번++] & 63); 안쪽순번++; }
        if (안쪽순번 != 더있음 || titik_kod < 최소값 || titik_kod > 0x10ffff || (titik_kod >= 0xd800 && titik_kod <= 0xdfff)) titik_kod = 0xfffd;
        if (titik_kod >= 65536) { titik_kod -= 65536; ukuran_data[++pemasukan_COUNT] = 0xd800 | (titik_kod >> 10); ukuran_data[++pemasukan_COUNT] = 0xdc00 | (titik_kod & 1023); }
        else ukuran_data[++pemasukan_COUNT] = titik_kod;
    }
    ukuran_data[0] = pemasukan_COUNT; return (mesin_Word)ukuran_data;
}
mesin_Word 도구분류(void) { return bidang_VALUE; }
void 커널중단(const char *알림문) {
    const char *data_jawatan = 알림문; while (*data_jawatan) data_jawatan++;
    바이트들("Java tool runtime error: ", 25); 바이트들(알림문, data_jawatan - 알림문); aksara(10);
    호출(6, 1, 0, 0); for (;;) {}
}
int Mula_pengguna_aplikasi(int kaedah_mod) {
    bidang_VALUE = kaedah_mod;
    unsigned char 첫항목[256]; intptr_t item_COUNT = 호출(15, 0, (mesin_Word)첫항목, sizeof(첫항목));
    if (kaedah_mod == 2 || (kaedah_mod == 1 && item_COUNT == 4 && 첫항목[0] == '-' && 첫항목[1] == 'j' && 첫항목[2] == 'a' && 첫항목[3] == 'r')) {
        꾸러미인수이동 = kaedah_mod == 2 ? 0 : 1;
        char fail_pemasukan_nama[256]; intptr_t kepanjangan_data = 호출(15, 꾸러미인수이동, (mesin_Word)fail_pemasukan_nama, sizeof(fail_pemasukan_nama));
        if (kepanjangan_data <= 0 || 꾸러미열기(fail_pemasukan_nama) < 0) {
            static const char RALAT[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            바이트들(RALAT, sizeof(RALAT) - 1); return 1;
        }
        꾸러미사용중 = 1;
    }
    int ukuran = 자바진입();
    if (대기중짝글자) aksara(0xfffd);
    return ukuran;
}

// UDP는 Asli 커널의 SVC를 통과하며 현재 127.0.0.1만 제공한다.
struct 자바주소 { uint16_t Keluarga, nombor_port; uint32_t e_mel; unsigned char 영값[8]; };
static struct 자바주소 UDP_e_mel(unsigned nombor_port) {
    struct 자바주소 첫째값 = {2, (uint16_t)((nombor_port << 8) | (nombor_port >> 8)), 0x0100007f, {0}}; return 첫째값;
}
mesin_Word alat_UDP_buka(mesin_Word nombor_port) {
    intptr_t fail_pemegang = 호출(32, 2, 2, 17); if (fail_pemegang < 0) return (uint32_t)fail_pemegang;
    struct 자바주소 첫째값 = UDP_e_mel(nombor_port);
    첫째값.e_mel = 0;
    intptr_t status_VALUE = 호출(33, fail_pemegang, (mesin_Word)&첫째값, sizeof(첫째값));
    if (status_VALUE < 0) { alat_Tutup(fail_pemegang); return (uint32_t)status_VALUE; }
    return fail_pemegang;
}
mesin_Word alat_UDP_e_mel(mesin_Word fail_pemegang, mesin_Word nombor_port, mesin_Word ARRAY_VALUE, mesin_Word kepanjangan_VALUE) {
    const mesin_Word *원본주소 = (const mesin_Word *)ARRAY_VALUE; unsigned char data[512];
    if (kepanjangan_VALUE > 512 || kepanjangan_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (mesin_Word 순번 = 0; 순번 < kepanjangan_VALUE; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_e_mel(nombor_port);
    return (uint32_t)사용자호출(34, fail_pemegang, (mesin_Word)data, kepanjangan_VALUE, 0, (mesin_Word)&첫째값, sizeof(첫째값));
}
static uint32_t 바이트순서뒤집기(uint32_t item_COUNT) { return (item_COUNT>>24)|((item_COUNT>>8)&0xff00)|((item_COUNT<<8)&0xff0000)|(item_COUNT<<24); }
mesin_Word alat_UDP_e_mel_e_mel(mesin_Word fail_pemegang, mesin_Word e_mel, mesin_Word nombor_port, mesin_Word ARRAY_VALUE, mesin_Word kepanjangan_VALUE) {
    const mesin_Word *원본주소 = (const mesin_Word *)ARRAY_VALUE; unsigned char data[512];
    if (kepanjangan_VALUE > 512 || kepanjangan_VALUE > 원본주소[0]) return (uint32_t)-90;
    for (mesin_Word 순번 = 0; 순번 < kepanjangan_VALUE; 순번++) data[순번] = 원본주소[순번 + 1];
    struct 자바주소 첫째값 = UDP_e_mel(nombor_port); 첫째값.e_mel = 바이트순서뒤집기(e_mel);
    return (uint32_t)사용자호출(34, fail_pemegang, (mesin_Word)data, kepanjangan_VALUE, 0, (mesin_Word)&첫째값, sizeof(첫째값));
}
mesin_Word alat_CONNECT(mesin_Word fail_pemegang, mesin_Word e_mel, mesin_Word nombor_port) {
    struct 자바주소 첫째값 = UDP_e_mel(nombor_port); 첫째값.e_mel = 바이트순서뒤집기(e_mel);
    uint32_t Jalan = 호출(7, 0, 0, 0);
    for (;;) {
        intptr_t ukuran = 호출(37, fail_pemegang, (mesin_Word)&첫째값, sizeof(첫째값));
        if (ukuran != -115) return (uint32_t)ukuran;
        if ((uint32_t)(호출(7, 0, 0, 0) - Jalan) >= 1000) return (uint32_t)-110;
    }
}
mesin_Word 도구전문받기(mesin_Word fail_pemegang, mesin_Word ARRAY_VALUE, mesin_Word penimbal_kapasiti) {
    mesin_Word *destinasi_e_mel = (mesin_Word *)ARRAY_VALUE; unsigned char data[512];
    if (penimbal_kapasiti > 512 || destinasi_e_mel[0] < 514) return (uint32_t)-90;
    struct 자바주소 첫째값; unsigned kepanjangan_data = sizeof(첫째값);
    intptr_t item_COUNT = 사용자호출(35, fail_pemegang, (mesin_Word)data, penimbal_kapasiti, 0, (mesin_Word)&첫째값, (mesin_Word)&kepanjangan_data);
    if (item_COUNT >= 0) { for (intptr_t 순번 = 0; 순번 < item_COUNT; 순번++) destinasi_e_mel[순번 + 1] = data[순번]; destinasi_e_mel[513] = (첫째값.nombor_port << 8 | 첫째값.nombor_port >> 8) & 65535; destinasi_e_mel[514] = 바이트순서뒤집기(첫째값.e_mel); }
    return (uint32_t)item_COUNT;
}
mesin_Word alat_UDP_port(mesin_Word fail_pemegang) {
    struct 자바주소 첫째값; unsigned kepanjangan_data = sizeof(첫째값);
    intptr_t 반환값 = 호출(36, fail_pemegang, (mesin_Word)&첫째값, (mesin_Word)&kepanjangan_data);
    return (uint32_t)(반환값 < 0 ? 반환값 : (첫째값.nombor_port << 8 | 첫째값.nombor_port >> 8) & 65535);
}
mesin_Word 도구밀리초(void) { return (uint32_t)호출(7, 0, 0, 0); }
mesin_Word 도구화면너비(void) { return (uint32_t)화면너비읽기(); }
mesin_Word 도구화면높이(void) { return (uint32_t)화면높이읽기(); }
mesin_Word alat_grafik_tunggu(void) { return (uint32_t)화면키기다리기(); }
mesin_Word alat_segi_empat_tepat(mesin_Word koordinat_x, mesin_Word Y_koordinat, mesin_Word 너비값, mesin_Word 높이값, mesin_Word 색상) {
    return (uint32_t)사용자호출(13, koordinat_x, Y_koordinat, 색상, 너비값, 높이값, 0);
}

mesin_Word alat_strim(mesin_Word Aksi,mesin_Word fail_pemegang,mesin_Word VALUE){
    if(Aksi==0)return (uint32_t)호출(32,2,1,6);
    struct 자바주소 첫째값=UDP_e_mel(VALUE);
    if(Aksi==1){첫째값.e_mel=0;intptr_t 반환값=호출(33,fail_pemegang,(mesin_Word)&첫째값,sizeof(첫째값));return (uint32_t)(반환값<0?반환값:호출(38,fail_pemegang,4,0));}
    if(Aksi==2)return (uint32_t)호출(37,fail_pemegang,(mesin_Word)&첫째값,sizeof(첫째값));
    if(Aksi==3)return (uint32_t)호출(39,fail_pemegang,0,0);
    if(Aksi==4)return alat_UDP_port(fail_pemegang);
    if(Aksi==5)return (uint32_t)호출(40,fail_pemegang,0,0);
    return (uint32_t)-22;
}
mesin_Word alat_GUI(mesin_Word Aksi,mesin_Word 식별자,mesin_Word 첫째값,mesin_Word SECOND_VALUE,mesin_Word titik_kod,mesin_Word destinasi_data){return (uint32_t)사용자호출(20,Aksi,식별자,첫째값,SECOND_VALUE,titik_kod,destinasi_data);}
mesin_Word alat_GUI_SMS(mesin_Word 식별자,mesin_Word ARRAY_VALUE,mesin_Word item_COUNT){
    const mesin_Word *원본주소=(const mesin_Word *)ARRAY_VALUE;uint32_t data[127];unsigned pemasukan_COUNT=0;
    if(item_COUNT>원본주소[0])return (uint32_t)-22;
    for(mesin_Word 순번=0;순번<item_COUNT;순번++){unsigned pengekodan_aksara=원본주소[순번+1];if(pengekodan_aksara>=0xd800&&pengekodan_aksara<=0xdbff&&순번+1<item_COUNT){unsigned 낮은값=원본주소[++순번+1];if(낮은값<0xdc00||낮은값>0xdfff)return (uint32_t)-22;pengekodan_aksara=0x10000+((pengekodan_aksara-0xd800)<<10)+낮은값-0xdc00;}if(pemasukan_COUNT==127)return (uint32_t)-22;data[pemasukan_COUNT++]=pengekodan_aksara;}
    return (uint32_t)사용자호출(21,식별자,(mesin_Word)data,pemasukan_COUNT,0,0,0);
}
