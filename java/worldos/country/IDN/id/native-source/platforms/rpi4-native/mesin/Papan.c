#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "ruang_pengguna.h"
#include "../jaringan_tumpuk/jaringan_tumpuk.h"
typedef uintptr_t mesin_Kata;
#define mesin_daftar(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define kotak_mail_surel 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Jam_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t kotak_mail_data[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *data_posisi, int kode_karakter, size_t item_COUNT) { unsigned char *Berikutnya_OFFSET = data_posisi; while (item_COUNT--) *Berikutnya_OFFSET++ = kode_karakter; return data_posisi; }
void *memcpy(void *tujuan_data, const void *string_data, size_t item_COUNT) { unsigned char *첫째값 = tujuan_data; const unsigned char *SECOND_VALUE = string_data; while (item_COUNT--) *첫째값++ = *SECOND_VALUE++; return tujuan_data; }

static int kotak_mail(void) {
    uint32_t permintaan = (uint32_t)(uintptr_t)kotak_mail_data | 8;
    uint64_t jalankan = Jam_COUNT();
    기억장벽();
    while (mesin_daftar(kotak_mail_surel + 0x38) & 0x80000000u)
        if (Jam_COUNT() - jalankan > FREQUENCY) return 0;
    mesin_daftar(kotak_mail_surel + 0x20) = permintaan;
    for (;;) {
        if (!(mesin_daftar(kotak_mail_surel + 0x18) & 0x40000000u)) {
            uint32_t balas = mesin_daftar(kotak_mail_surel);
            if (balas == permintaan) { 기억장벽(); return kotak_mail_data[1] == 0x80000000u; }
        }
        if (Jam_COUNT() - jalankan > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_byte(unsigned);
extern int Terminal_sedang_diproses(void);
extern void Terminal_pointer(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../jarak_jauh_VALUE/jarak_jauh_VALUE.h"
static int Aliran;
static unsigned 직렬이전글자;
mesin_Kata Papan_Aliran(mesin_Kata 사용여부) { Aliran=사용여부!=0; return 0; }
mesin_Kata Papan_Saluran(mesin_Kata Saluran, mesin_Kata kode_karakter) {
    if(Aliran && 자바셸출력((int32_t)Saluran,(int32_t)(kode_karakter&255))) return 0;
    Terminal_byte(kode_karakter&255);
    원격출력(kode_karakter&255);
    if ((kode_karakter&255)==10 && 직렬이전글자!=13) {
        while (mesin_daftar(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        mesin_daftar(직렬장치)=13;
    }
    직렬이전글자=kode_karakter&255;
    while (mesin_daftar(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    mesin_daftar(직렬장치) = (uint32_t)kode_karakter & 255;
    return 0;
}
mesin_Kata 보드글자쓰기(mesin_Kata kode_karakter) { return Papan_Saluran(1,kode_karakter); }
mesin_Kata 보드원시글자읽기(void) {
    int jarak_jauh_karakter=원격입력();if(jarak_jauh_karakter>=0)return jarak_jauh_karakter;
    if (mesin_daftar(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = mesin_daftar(직렬장치);
    if (VALUE & 0xf00) { mesin_daftar(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
mesin_Kata 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char paket_data[6];
    if(Terminal_sedang_diproses())return (uint32_t)-4096;
    if(Aliran){int32_t kode_karakter=자바셸입력();if(kode_karakter!=-3)return (uint32_t)kode_karakter;}
    for(;;){
        int kode_karakter=(int32_t)보드원시글자읽기();if(kode_karakter<0)return (uint32_t)kode_karakter;
        if(!꾸러미안쪽){if(kode_karakter!=30)return kode_karakter;꾸러미안쪽=1;사용량=0;continue;}
        paket_data[사용량++]=kode_karakter;if(사용량<6)continue;꾸러미안쪽=0;
        if(paket_data[0]==1)Terminal_pointer(paket_data[1],paket_data[2]+paket_data[3]*256,paket_data[4]+paket_data[5]*256);
        if(paket_data[0]==2)터미널바로가기키(paket_data[1]);
        if(paket_data[0]==3)터미널입력방식(paket_data[1]);
        if(Terminal_sedang_diproses())return (uint32_t)-4096;
    }
}
mesin_Kata 보드밀리초(void) { return (uint32_t)(Jam_COUNT() / (FREQUENCY / 1000)); }
mesin_Kata 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *string_data) { while (*string_data) 보드글자쓰기((unsigned char)*string_data++); }
static void 직렬열여섯진출력(mesin_Kata item_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int string_data = 60; string_data >= 0; string_data -= 4) 보드글자쓰기(열여섯진숫자[(item_COUNT >> string_data) & 15]); }
mesin_Kata Papan_Berhenti(mesin_Kata Status_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Status_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Papan_Berhenti(1); __builtin_unreachable(); }
void Papan_pengecualian(mesin_Kata pengecualian_Status, mesin_Kata perintah_posisi, mesin_Kata tidak_sahih_surel) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(pengecualian_Status);
    직렬글출력(" PC="); 직렬열여섯진출력(perintah_posisi); 직렬글출력(" FAR="); 직렬열여섯진출력(tidak_sahih_surel);
    Papan_Berhenti(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    kotak_mail_data[0]=32;kotak_mail_data[1]=0;kotak_mail_data[2]=0x10004;kotak_mail_data[3]=8;kotak_mail_data[4]=0;
    kotak_mail_data[5]=kotak_mail_data[6]=kotak_mail_data[7]=0;
    return kotak_mail()&&kotak_mail_data[4]==0x80000008u&&(kotak_mail_data[5]||kotak_mail_data[6]);
}
int Papan_mesin_surel(unsigned char *surel) {
    kotak_mail_data[0]=32;kotak_mail_data[1]=0;kotak_mail_data[2]=0x10003;kotak_mail_data[3]=8;kotak_mail_data[4]=0;
    kotak_mail_data[5]=kotak_mail_data[6]=kotak_mail_data[7]=0;
    if(!kotak_mail()||(kotak_mail_data[4]&0x80000000u)==0||(kotak_mail_data[4]&0xffff)!=6)return 0;
    const unsigned char *data=(const unsigned char*)&kotak_mail_data[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){surel[순번]=data[순번];SUM_VALUE|=data[순번];}return SUM_VALUE&&!(surel[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    mesin_daftar(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    mesin_daftar(범용입출력 + 4) = (mesin_daftar(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    mesin_daftar(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. kegagalan_VALUE 시 config.txt의 48MHz를 사용한다.
    kotak_mail_data[0] = 36; kotak_mail_data[1] = 0; kotak_mail_data[2] = 0x38002; kotak_mail_data[3] = 12;
    kotak_mail_data[4] = 0; kotak_mail_data[5] = 2; kotak_mail_data[6] = 48000000; kotak_mail_data[7] = 0; kotak_mail_data[8] = 0;
    int 시계정상 = kotak_mail();
    uint32_t 속도 = 시계정상 && kotak_mail_data[6] >= 1843200 ? kotak_mail_data[6] : 48000000;
    kotak_mail_data[0]=32; kotak_mail_data[1]=0; kotak_mail_data[2]=0x10005; kotak_mail_data[3]=8; kotak_mail_data[4]=0;
    kotak_mail_data[5]=kotak_mail_data[6]=kotak_mail_data[7]=0;
    if (kotak_mail() && kotak_mail_data[4]==0x80000008u) 팔기억킬로바이트=kotak_mail_data[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    mesin_daftar(직렬장치 + 0x44) = 0x7ff;
    mesin_daftar(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    mesin_daftar(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    mesin_daftar(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    mesin_daftar(직렬장치 + 0x38) = 0;
    mesin_daftar(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
mesin_Kata Papan_FTP(mesin_Kata Aksi) { return (uint32_t)ftp_control((int)Aksi); }
mesin_Kata Papan_jaringan_status(mesin_Kata entri_VALUE, mesin_Kata INDEX) { return 망상태읽기(entri_VALUE, INDEX); }
mesin_Kata Papan_jaringan_Pengaturan(mesin_Kata Aksi, mesin_Kata surel, mesin_Kata masker_VALUE, mesin_Kata gateway_VALUE) { return (uint32_t)konfigurasikan_jaringan(Aksi, surel, masker_VALUE, gateway_VALUE); }
mesin_Kata Papan_kirim_respons(mesin_Kata surel, mesin_Kata urutan_VALUE) { return (uint32_t)응답시험시작(surel, urutan_VALUE); }
mesin_Kata 보드응답읽기(mesin_Kata entri_VALUE) { return (uint32_t)응답시험읽기(entri_VALUE); }
mesin_Kata 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) Tutup_jaringan(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) Papan_kontrol_pengguna(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (mesin_daftar(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    mesin_daftar(0xfe100020ul)=0x5a000000u | (mesin_daftar(0xfe100020ul)&~0xfffu) | 0x555;
    mesin_daftar(0xfe100024ul)=0x5a000000u | 10;
    mesin_daftar(0xfe10001cul)=0x5a000000u | (mesin_daftar(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

mesin_Kata 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 saat_ini_item 크기를 읽는다. */
    const uint32_t kueri_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(kueri_VALUE)/4; 순번++) kotak_mail_data[순번] = kueri_VALUE[순번];
    if (kotak_mail() && kotak_mail_data[4] == 0x80000008u &&
        kotak_mail_data[5] >= 640 && kotak_mail_data[5] <= 1920 &&
        kotak_mail_data[6] >= 480 && kotak_mail_data[6] <= 1080) {
        요청너비 = kotak_mail_data[5]; 요청높이 = kotak_mail_data[6];
    }
    const uint32_t permintaan[] = {
        35 * 4, 0,
        0x48003, 8, 0, 요청너비, 요청높이,
        0x48004, 8, 0, 요청너비, 요청높이,
        0x48005, 4, 0, 32,
        0x48006, 4, 0, 1,
        0x48009, 8, 0, 0, 0,
        0x40001, 8, 0, 4096, 0,
        0x40008, 4, 0, 0,
        0
    };
    for (size_t 순번 = 0; 순번 < sizeof(permintaan)/4; 순번++) kotak_mail_data[순번] = permintaan[순번];
    // 위 메시지의 aktual_data 길이를 gunakan_VALUE: 태그 tambah_entri 시 panjang_VALUE 불일치를 방지한다.
    kotak_mail_data[0] = sizeof(permintaan);
    if (!kotak_mail()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned respons_panjang[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (kotak_mail_data[응답들[순번]] != (0x80000000u | respons_panjang[순번])) return 0;
    uint32_t wallpaper_VALUE = kotak_mail_data[28] & 0x3fffffffu;
    uint32_t Ukuran = kotak_mail_data[29];
    uint32_t 받은너비 = kotak_mail_data[5], 받은높이 = kotak_mail_data[6], RECEIVED_spasi_baris = kotak_mail_data[33];
    if (kotak_mail_data[15] != 32 || kotak_mail_data[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        kotak_mail_data[10] < 받은너비 || kotak_mail_data[11] < 받은높이 || kotak_mail_data[23] || kotak_mail_data[24] ||
        !wallpaper_VALUE || wallpaper_VALUE < 0x1000000 || (wallpaper_VALUE & 3) || RECEIVED_spasi_baris < 받은너비 * 4 || (RECEIVED_spasi_baris & 3) ||
        (uint64_t)RECEIVED_spasi_baris * 받은높이 > Ukuran || (uint64_t)wallpaper_VALUE + Ukuran > 0x40000000u)
        return 0;
    Papan_Siapkan_gambar((volatile uint32_t *)(uintptr_t)wallpaper_VALUE, 받은너비, 받은높이, RECEIVED_spasi_baris);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 alur_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } 작업문맥;
static 작업문맥 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int teknologi_informasi_Lari[3] = {1, 0, 0};
static int saat_ini_tugas;
extern void pengalihan_konteks(작업문맥 *, 작업문맥 *);
extern void 자바작업(int32_t);
mesin_Kata Papan_YIELD(void) {
    network_poll();
    int 이전 = saat_ini_tugas, Berikutnya_item = (이전 + 1) % 3;
    while (Berikutnya_item != 이전 && !teknologi_informasi_Lari[Berikutnya_item]) Berikutnya_item = (Berikutnya_item + 1) % 3;
    if (Berikutnya_item != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (teknologi_informasi_Lari[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        saat_ini_tugas = Berikutnya_item;
        pengalihan_konteks(&작업문맥들[이전], &작업문맥들[Berikutnya_item]);
    }
    return 0;
}
static void tugas_mulai(void) {
    자바작업(saat_ini_tugas);
    teknologi_informasi_Lari[saat_ini_tugas] = 0;
    Papan_YIELD();
    커널중단("finished task resumed");
}
mesin_Kata Papan_tugas_Buat(mesin_Kata pengidentifikasi_VALUE) {
    if (pengidentifikasi_VALUE < 1 || pengidentifikasi_VALUE > 2 || teknologi_informasi_Lari[pengidentifikasi_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[pengidentifikasi_VALUE], 0, sizeof(작업문맥));
    *(uint64_t *)쌓임공간들[pengidentifikasi_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[pengidentifikasi_VALUE].저장값[11] = (uintptr_t)tugas_mulai;
    작업문맥들[pengidentifikasi_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[pengidentifikasi_VALUE - 1] + sizeof(쌓임공간들[0]));
    teknologi_informasi_Lari[pengidentifikasi_VALUE] = 1;
    return 0;
}
mesin_Kata Papan_tugas_Status(mesin_Kata pengidentifikasi_VALUE) { return pengidentifikasi_VALUE < 3 ? teknologi_informasi_Lari[pengidentifikasi_VALUE] : (uint32_t)-1; }
extern mesin_Kata 미리번역기억조회(mesin_Kata);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
mesin_Kata Papan_kueri_sistem(mesin_Kata entri_VALUE, mesin_Kata INDEX) {
    if (entri_VALUE==0) return 팔기억킬로바이트;
    if (entri_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (entri_VALUE==2 || entri_VALUE==3) return 미리번역기억조회(entri_VALUE==3);
    if (entri_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (entri_VALUE==5) return 80*1024; /* Jalankan_perintah surel_wilayah 16 MiB + 네 세션 보관 surel_wilayah. */
    if (entri_VALUE>=20) return 사용자상태읽기(entri_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[saat_ini_tugas]; }
