#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "ruang_pengguna.h"
#include "../rangkaian_tindan/rangkaian_tindan.h"
typedef uintptr_t mesin_Word;
#define mesin_daftar(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define peti_mel_e_mel 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Jam_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t peti_mel_data[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *data_jawatan, int titik_kod, size_t item_COUNT) { unsigned char *Seterusnya_Ofset = data_jawatan; while (item_COUNT--) *Seterusnya_Ofset++ = titik_kod; return data_jawatan; }
void *memcpy(void *destinasi_data, const void *rentetan_data, size_t item_COUNT) { unsigned char *첫째값 = destinasi_data; const unsigned char *SECOND_VALUE = rentetan_data; while (item_COUNT--) *첫째값++ = *SECOND_VALUE++; return destinasi_data; }

static int peti_mel(void) {
    uint32_t permintaan = (uint32_t)(uintptr_t)peti_mel_data | 8;
    uint64_t Jalan = Jam_COUNT();
    기억장벽();
    while (mesin_daftar(peti_mel_e_mel + 0x38) & 0x80000000u)
        if (Jam_COUNT() - Jalan > FREQUENCY) return 0;
    mesin_daftar(peti_mel_e_mel + 0x20) = permintaan;
    for (;;) {
        if (!(mesin_daftar(peti_mel_e_mel + 0x18) & 0x40000000u)) {
            uint32_t balas = mesin_daftar(peti_mel_e_mel);
            if (balas == permintaan) { 기억장벽(); return peti_mel_data[1] == 0x80000000u; }
        }
        if (Jam_COUNT() - Jalan > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_bait(unsigned);
extern int Terminal_belum_selesai(void);
extern void Terminal_penuding(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../jauh_VALUE/jauh_VALUE.h"
static int Strim;
static unsigned 직렬이전글자;
mesin_Word Papan_Strim(mesin_Word 사용여부) { Strim=사용여부!=0; return 0; }
mesin_Word Papan_Saluran(mesin_Word Saluran, mesin_Word titik_kod) {
    if(Strim && 자바셸출력((int32_t)Saluran,(int32_t)(titik_kod&255))) return 0;
    Terminal_bait(titik_kod&255);
    원격출력(titik_kod&255);
    if ((titik_kod&255)==10 && 직렬이전글자!=13) {
        while (mesin_daftar(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        mesin_daftar(직렬장치)=13;
    }
    직렬이전글자=titik_kod&255;
    while (mesin_daftar(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    mesin_daftar(직렬장치) = (uint32_t)titik_kod & 255;
    return 0;
}
mesin_Word 보드글자쓰기(mesin_Word titik_kod) { return Papan_Saluran(1,titik_kod); }
mesin_Word 보드원시글자읽기(void) {
    int jauh_aksara=원격입력();if(jauh_aksara>=0)return jauh_aksara;
    if (mesin_daftar(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = mesin_daftar(직렬장치);
    if (VALUE & 0xf00) { mesin_daftar(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
mesin_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char paket_data[6];
    if(Terminal_belum_selesai())return (uint32_t)-4096;
    if(Strim){int32_t titik_kod=자바셸입력();if(titik_kod!=-3)return (uint32_t)titik_kod;}
    for(;;){
        int titik_kod=(int32_t)보드원시글자읽기();if(titik_kod<0)return (uint32_t)titik_kod;
        if(!꾸러미안쪽){if(titik_kod!=30)return titik_kod;꾸러미안쪽=1;사용량=0;continue;}
        paket_data[사용량++]=titik_kod;if(사용량<6)continue;꾸러미안쪽=0;
        if(paket_data[0]==1)Terminal_penuding(paket_data[1],paket_data[2]+paket_data[3]*256,paket_data[4]+paket_data[5]*256);
        if(paket_data[0]==2)터미널바로가기키(paket_data[1]);
        if(paket_data[0]==3)터미널입력방식(paket_data[1]);
        if(Terminal_belum_selesai())return (uint32_t)-4096;
    }
}
mesin_Word 보드밀리초(void) { return (uint32_t)(Jam_COUNT() / (FREQUENCY / 1000)); }
mesin_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *rentetan_data) { while (*rentetan_data) 보드글자쓰기((unsigned char)*rentetan_data++); }
static void 직렬열여섯진출력(mesin_Word item_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int rentetan_data = 60; rentetan_data >= 0; rentetan_data -= 4) 보드글자쓰기(열여섯진숫자[(item_COUNT >> rentetan_data) & 15]); }
mesin_Word Papan_Henti(mesin_Word status_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(status_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Papan_Henti(1); __builtin_unreachable(); }
void Papan_pengecualian(mesin_Word pengecualian_status, mesin_Word perintah_jawatan, mesin_Word tak_sah_e_mel) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(pengecualian_status);
    직렬글출력(" PC="); 직렬열여섯진출력(perintah_jawatan); 직렬글출력(" FAR="); 직렬열여섯진출력(tak_sah_e_mel);
    Papan_Henti(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    peti_mel_data[0]=32;peti_mel_data[1]=0;peti_mel_data[2]=0x10004;peti_mel_data[3]=8;peti_mel_data[4]=0;
    peti_mel_data[5]=peti_mel_data[6]=peti_mel_data[7]=0;
    return peti_mel()&&peti_mel_data[4]==0x80000008u&&(peti_mel_data[5]||peti_mel_data[6]);
}
int Papan_mesin_e_mel(unsigned char *e_mel) {
    peti_mel_data[0]=32;peti_mel_data[1]=0;peti_mel_data[2]=0x10003;peti_mel_data[3]=8;peti_mel_data[4]=0;
    peti_mel_data[5]=peti_mel_data[6]=peti_mel_data[7]=0;
    if(!peti_mel()||(peti_mel_data[4]&0x80000000u)==0||(peti_mel_data[4]&0xffff)!=6)return 0;
    const unsigned char *data=(const unsigned char*)&peti_mel_data[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){e_mel[순번]=data[순번];SUM_VALUE|=data[순번];}return SUM_VALUE&&!(e_mel[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    mesin_daftar(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    mesin_daftar(범용입출력 + 4) = (mesin_daftar(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    mesin_daftar(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. kegagalan_VALUE 시 config.txt의 48MHz를 사용한다.
    peti_mel_data[0] = 36; peti_mel_data[1] = 0; peti_mel_data[2] = 0x38002; peti_mel_data[3] = 12;
    peti_mel_data[4] = 0; peti_mel_data[5] = 2; peti_mel_data[6] = 48000000; peti_mel_data[7] = 0; peti_mel_data[8] = 0;
    int 시계정상 = peti_mel();
    uint32_t 속도 = 시계정상 && peti_mel_data[6] >= 1843200 ? peti_mel_data[6] : 48000000;
    peti_mel_data[0]=32; peti_mel_data[1]=0; peti_mel_data[2]=0x10005; peti_mel_data[3]=8; peti_mel_data[4]=0;
    peti_mel_data[5]=peti_mel_data[6]=peti_mel_data[7]=0;
    if (peti_mel() && peti_mel_data[4]==0x80000008u) 팔기억킬로바이트=peti_mel_data[6]/1024;
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
mesin_Word Papan_FTP(mesin_Word Aksi) { return (uint32_t)ftp_control((int)Aksi); }
mesin_Word Papan_rangkaian_status(mesin_Word pemasukan_VALUE, mesin_Word INDEX) { return 망상태읽기(pemasukan_VALUE, INDEX); }
mesin_Word Papan_rangkaian_Seting(mesin_Word Aksi, mesin_Word e_mel, mesin_Word topeng_VALUE, mesin_Word get_laluan_VALUE) { return (uint32_t)konfigurasi_rangkaian(Aksi, e_mel, topeng_VALUE, get_laluan_VALUE); }
mesin_Word Papan_e_mel_respons(mesin_Word e_mel, mesin_Word tertib_VALUE) { return (uint32_t)Mula_respons_ujian(e_mel, tertib_VALUE); }
mesin_Word 보드응답읽기(mesin_Word pemasukan_VALUE) { return (uint32_t)응답시험읽기(pemasukan_VALUE); }
mesin_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) Tutup_rangkaian(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) Papan_kawalan_pengguna(32+INDEX);
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

mesin_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t pertanyaan_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(pertanyaan_VALUE)/4; 순번++) peti_mel_data[순번] = pertanyaan_VALUE[순번];
    if (peti_mel() && peti_mel_data[4] == 0x80000008u &&
        peti_mel_data[5] >= 640 && peti_mel_data[5] <= 1920 &&
        peti_mel_data[6] >= 480 && peti_mel_data[6] <= 1080) {
        요청너비 = peti_mel_data[5]; 요청높이 = peti_mel_data[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(permintaan)/4; 순번++) peti_mel_data[순번] = permintaan[순번];
    // 위 메시지의 sebenar_data 길이를 사용: 태그 Tambah_pemasukan 시 kepanjangan_VALUE 불일치를 방지한다.
    peti_mel_data[0] = sizeof(permintaan);
    if (!peti_mel()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned respons_kepanjangan[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (peti_mel_data[응답들[순번]] != (0x80000000u | respons_kepanjangan[순번])) return 0;
    uint32_t latar_VALUE = peti_mel_data[28] & 0x3fffffffu;
    uint32_t Saiz = peti_mel_data[29];
    uint32_t 받은너비 = peti_mel_data[5], 받은높이 = peti_mel_data[6], RECEIVED_jarak_baris = peti_mel_data[33];
    if (peti_mel_data[15] != 32 || peti_mel_data[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        peti_mel_data[10] < 받은너비 || peti_mel_data[11] < 받은높이 || peti_mel_data[23] || peti_mel_data[24] ||
        !latar_VALUE || latar_VALUE < 0x1000000 || (latar_VALUE & 3) || RECEIVED_jarak_baris < 받은너비 * 4 || (RECEIVED_jarak_baris & 3) ||
        (uint64_t)RECEIVED_jarak_baris * 받은높이 > Saiz || (uint64_t)latar_VALUE + Saiz > 0x40000000u)
        return 0;
    Papan_Sediakan_lukisan((volatile uint32_t *)(uintptr_t)latar_VALUE, 받은너비, 받은높이, RECEIVED_jarak_baris);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 urutan_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } konteks;
static konteks 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int teknologi_maklumat_Larian[3] = {1, 0, 0};
static int 현재작업;
extern void pertukaran_konteks(konteks *, konteks *);
extern void 자바작업(int32_t);
mesin_Word Papan_YIELD(void) {
    network_poll();
    int 이전 = 현재작업, Seterusnya_item = (이전 + 1) % 3;
    while (Seterusnya_item != 이전 && !teknologi_maklumat_Larian[Seterusnya_item]) Seterusnya_item = (Seterusnya_item + 1) % 3;
    if (Seterusnya_item != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (teknologi_maklumat_Larian[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = Seterusnya_item;
        pertukaran_konteks(&작업문맥들[이전], &작업문맥들[Seterusnya_item]);
    }
    return 0;
}
static void tugas_butstrap(void) {
    자바작업(현재작업);
    teknologi_maklumat_Larian[현재작업] = 0;
    Papan_YIELD();
    커널중단("finished task resumed");
}
mesin_Word Papan_tugas_cipta(mesin_Word 식별자) {
    if (식별자 < 1 || 식별자 > 2 || teknologi_maklumat_Larian[식별자]) return (uint32_t)-1;
    memset(&작업문맥들[식별자], 0, sizeof(konteks));
    *(uint64_t *)쌓임공간들[식별자 - 1] = 0x6b6f726f7373746bull;
    작업문맥들[식별자].저장값[11] = (uintptr_t)tugas_butstrap;
    작업문맥들[식별자].저장값[12] = (uintptr_t)(쌓임공간들[식별자 - 1] + sizeof(쌓임공간들[0]));
    teknologi_maklumat_Larian[식별자] = 1;
    return 0;
}
mesin_Word Papan_tugas_status(mesin_Word 식별자) { return 식별자 < 3 ? teknologi_maklumat_Larian[식별자] : (uint32_t)-1; }
extern mesin_Word 미리번역기억조회(mesin_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
mesin_Word Papan_pertanyaan_sistem(mesin_Word pemasukan_VALUE, mesin_Word INDEX) {
    if (pemasukan_VALUE==0) return 팔기억킬로바이트;
    if (pemasukan_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (pemasukan_VALUE==2 || pemasukan_VALUE==3) return 미리번역기억조회(pemasukan_VALUE==3);
    if (pemasukan_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (pemasukan_VALUE==5) return 80*1024; /* laksanakan_perintah e_mel_rantau 16 MiB + 네 세션 보관 e_mel_rantau. */
    if (pemasukan_VALUE>=20) return 사용자상태읽기(pemasukan_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
