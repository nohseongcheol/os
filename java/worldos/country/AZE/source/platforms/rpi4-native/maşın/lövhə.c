#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "istifadəçi.h"
#include "../Şəbəkə_Yığın/Şəbəkə_Yığın.h"
typedef uintptr_t maşın_Söz;
#define maşın_qeydiyyatdan_keçmək(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define poçt_qutusu_ünvan 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Saat_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t poçt_qutusu_verilənlər[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *verilənlər_yerinə_qoymaq, int simvol_kodu, size_t element_COUNT) { unsigned char *Sonrakı_OFFSET = verilənlər_yerinə_qoymaq; while (element_COUNT--) *Sonrakı_OFFSET++ = simvol_kodu; return verilənlər_yerinə_qoymaq; }
void *memcpy(void *təyinat_verilənlər, const void *sətir_verilənlər, size_t element_COUNT) { unsigned char *첫째값 = təyinat_verilənlər; const unsigned char *SECOND_VALUE = sətir_verilənlər; while (element_COUNT--) *첫째값++ = *SECOND_VALUE++; return təyinat_verilənlər; }

static int poçt_qutusu(void) {
    uint32_t HTTP_sorğusu = (uint32_t)(uintptr_t)poçt_qutusu_verilənlər | 8;
    uint64_t İcra_Et = Saat_COUNT();
    기억장벽();
    while (maşın_qeydiyyatdan_keçmək(poçt_qutusu_ünvan + 0x38) & 0x80000000u)
        if (Saat_COUNT() - İcra_Et > FREQUENCY) return 0;
    maşın_qeydiyyatdan_keçmək(poçt_qutusu_ünvan + 0x20) = HTTP_sorğusu;
    for (;;) {
        if (!(maşın_qeydiyyatdan_keçmək(poçt_qutusu_ünvan + 0x18) & 0x40000000u)) {
            uint32_t cavab = maşın_qeydiyyatdan_keçmək(poçt_qutusu_ünvan);
            if (cavab == HTTP_sorğusu) { 기억장벽(); return poçt_qutusu_verilənlər[1] == 0x80000000u; }
        }
        if (Saat_COUNT() - İcra_Et > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_bayt(unsigned);
extern int Terminal_gözləyir(void);
extern void Terminal_göstərici(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../uzaq_VALUE/uzaq_VALUE.h"
static int 흐름목록;
static unsigned 직렬이전글자;
maşın_Söz 보드흐름설정(maşın_Söz 사용여부) { 흐름목록=사용여부!=0; return 0; }
maşın_Söz lövhə_kanal(maşın_Söz kanal, maşın_Söz simvol_kodu) {
    if(흐름목록 && 자바셸출력((int32_t)kanal,(int32_t)(simvol_kodu&255))) return 0;
    Terminal_bayt(simvol_kodu&255);
    원격출력(simvol_kodu&255);
    if ((simvol_kodu&255)==10 && 직렬이전글자!=13) {
        while (maşın_qeydiyyatdan_keçmək(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        maşın_qeydiyyatdan_keçmək(직렬장치)=13;
    }
    직렬이전글자=simvol_kodu&255;
    while (maşın_qeydiyyatdan_keçmək(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    maşın_qeydiyyatdan_keçmək(직렬장치) = (uint32_t)simvol_kodu & 255;
    return 0;
}
maşın_Söz 보드글자쓰기(maşın_Söz simvol_kodu) { return lövhə_kanal(1,simvol_kodu); }
maşın_Söz 보드원시글자읽기(void) {
    int uzaq_simvol=원격입력();if(uzaq_simvol>=0)return uzaq_simvol;
    if (maşın_qeydiyyatdan_keçmək(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = maşın_qeydiyyatdan_keçmək(직렬장치);
    if (VALUE & 0xf00) { maşın_qeydiyyatdan_keçmək(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
maşın_Söz 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char paket_verilənlər[6];
    if(Terminal_gözləyir())return (uint32_t)-4096;
    if(흐름목록){int32_t simvol_kodu=자바셸입력();if(simvol_kodu!=-3)return (uint32_t)simvol_kodu;}
    for(;;){
        int simvol_kodu=(int32_t)보드원시글자읽기();if(simvol_kodu<0)return (uint32_t)simvol_kodu;
        if(!꾸러미안쪽){if(simvol_kodu!=30)return simvol_kodu;꾸러미안쪽=1;사용량=0;continue;}
        paket_verilənlər[사용량++]=simvol_kodu;if(사용량<6)continue;꾸러미안쪽=0;
        if(paket_verilənlər[0]==1)Terminal_göstərici(paket_verilənlər[1],paket_verilənlər[2]+paket_verilənlər[3]*256,paket_verilənlər[4]+paket_verilənlər[5]*256);
        if(paket_verilənlər[0]==2)터미널바로가기키(paket_verilənlər[1]);
        if(paket_verilənlər[0]==3)터미널입력방식(paket_verilənlər[1]);
        if(Terminal_gözləyir())return (uint32_t)-4096;
    }
}
maşın_Söz 보드밀리초(void) { return (uint32_t)(Saat_COUNT() / (FREQUENCY / 1000)); }
maşın_Söz 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *sətir_verilənlər) { while (*sətir_verilənlər) 보드글자쓰기((unsigned char)*sətir_verilənlər++); }
static void 직렬열여섯진출력(maşın_Söz element_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int sətir_verilənlər = 60; sətir_verilənlər >= 0; sətir_verilənlər -= 4) 보드글자쓰기(열여섯진숫자[(element_COUNT >> sətir_verilənlər) & 15]); }
maşın_Söz lövhə_Dayandır(maşın_Söz vəziyyət_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(vəziyyət_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); lövhə_Dayandır(1); __builtin_unreachable(); }
void lövhə_istisna(maşın_Söz istisna_vəziyyət, maşın_Söz əmr_yerinə_qoymaq, maşın_Söz yanlış_ünvan) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(istisna_vəziyyət);
    직렬글출력(" PC="); 직렬열여섯진출력(əmr_yerinə_qoymaq); 직렬글출력(" FAR="); 직렬열여섯진출력(yanlış_ünvan);
    lövhə_Dayandır(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    poçt_qutusu_verilənlər[0]=32;poçt_qutusu_verilənlər[1]=0;poçt_qutusu_verilənlər[2]=0x10004;poçt_qutusu_verilənlər[3]=8;poçt_qutusu_verilənlər[4]=0;
    poçt_qutusu_verilənlər[5]=poçt_qutusu_verilənlər[6]=poçt_qutusu_verilənlər[7]=0;
    return poçt_qutusu()&&poçt_qutusu_verilənlər[4]==0x80000008u&&(poçt_qutusu_verilənlər[5]||poçt_qutusu_verilənlər[6]);
}
int lövhə_maşın_ünvan(unsigned char *ünvan) {
    poçt_qutusu_verilənlər[0]=32;poçt_qutusu_verilənlər[1]=0;poçt_qutusu_verilənlər[2]=0x10003;poçt_qutusu_verilənlər[3]=8;poçt_qutusu_verilənlər[4]=0;
    poçt_qutusu_verilənlər[5]=poçt_qutusu_verilənlər[6]=poçt_qutusu_verilənlər[7]=0;
    if(!poçt_qutusu()||(poçt_qutusu_verilənlər[4]&0x80000000u)==0||(poçt_qutusu_verilənlər[4]&0xffff)!=6)return 0;
    const unsigned char *verilənlər=(const unsigned char*)&poçt_qutusu_verilənlər[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){ünvan[순번]=verilənlər[순번];SUM_VALUE|=verilənlər[순번];}return SUM_VALUE&&!(ünvan[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    maşın_qeydiyyatdan_keçmək(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    maşın_qeydiyyatdan_keçmək(범용입출력 + 4) = (maşın_qeydiyyatdan_keçmək(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    maşın_qeydiyyatdan_keçmək(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. xəta_VALUE 시 config.txt의 48MHz를 사용한다.
    poçt_qutusu_verilənlər[0] = 36; poçt_qutusu_verilənlər[1] = 0; poçt_qutusu_verilənlər[2] = 0x38002; poçt_qutusu_verilənlər[3] = 12;
    poçt_qutusu_verilənlər[4] = 0; poçt_qutusu_verilənlər[5] = 2; poçt_qutusu_verilənlər[6] = 48000000; poçt_qutusu_verilənlər[7] = 0; poçt_qutusu_verilənlər[8] = 0;
    int 시계정상 = poçt_qutusu();
    uint32_t 속도 = 시계정상 && poçt_qutusu_verilənlər[6] >= 1843200 ? poçt_qutusu_verilənlər[6] : 48000000;
    poçt_qutusu_verilənlər[0]=32; poçt_qutusu_verilənlər[1]=0; poçt_qutusu_verilənlər[2]=0x10005; poçt_qutusu_verilənlər[3]=8; poçt_qutusu_verilənlər[4]=0;
    poçt_qutusu_verilənlər[5]=poçt_qutusu_verilənlər[6]=poçt_qutusu_verilənlər[7]=0;
    if (poçt_qutusu() && poçt_qutusu_verilənlər[4]==0x80000008u) 팔기억킬로바이트=poçt_qutusu_verilənlər[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    maşın_qeydiyyatdan_keçmək(직렬장치 + 0x44) = 0x7ff;
    maşın_qeydiyyatdan_keçmək(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    maşın_qeydiyyatdan_keçmək(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    maşın_qeydiyyatdan_keçmək(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    maşın_qeydiyyatdan_keçmək(직렬장치 + 0x38) = 0;
    maşın_qeydiyyatdan_keçmək(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
maşın_Söz lövhə_FTP(maşın_Söz Gedişat) { return (uint32_t)ftp_control((int)Gedişat); }
maşın_Söz lövhə_Şəbəkə_vəziyyət(maşın_Söz daxiletmə_VALUE, maşın_Söz INDEX) { return 망상태읽기(daxiletmə_VALUE, INDEX); }
maşın_Söz lövhə_Şəbəkə_Parametrlər(maşın_Söz Gedişat, maşın_Söz ünvan, maşın_Söz maska_VALUE, maşın_Söz şlüz_VALUE) { return (uint32_t)konfiqurasiya_etmək_Şəbəkə(Gedişat, ünvan, maska_VALUE, şlüz_VALUE); }
maşın_Söz lövhə_göndərmək_video_münasibət(maşın_Söz ünvan, maşın_Söz ardıcıllıq_VALUE) { return (uint32_t)응답시험시작(ünvan, ardıcıllıq_VALUE); }
maşın_Söz 보드응답읽기(maşın_Söz daxiletmə_VALUE) { return (uint32_t)응답시험읽기(daxiletmə_VALUE); }
maşın_Söz 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) bağlamaq_Şəbəkə(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) lövhə_istifadəçi_idarəetməsi(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (maşın_qeydiyyatdan_keçmək(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    maşın_qeydiyyatdan_keçmək(0xfe100020ul)=0x5a000000u | (maşın_qeydiyyatdan_keçmək(0xfe100020ul)&~0xfffu) | 0x555;
    maşın_qeydiyyatdan_keçmək(0xfe100024ul)=0x5a000000u | 10;
    maşın_qeydiyyatdan_keçmək(0xfe10001cul)=0x5a000000u | (maşın_qeydiyyatdan_keçmək(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

maşın_Söz 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t sorğu_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(sorğu_VALUE)/4; 순번++) poçt_qutusu_verilənlər[순번] = sorğu_VALUE[순번];
    if (poçt_qutusu() && poçt_qutusu_verilənlər[4] == 0x80000008u &&
        poçt_qutusu_verilənlər[5] >= 640 && poçt_qutusu_verilənlər[5] <= 1920 &&
        poçt_qutusu_verilənlər[6] >= 480 && poçt_qutusu_verilənlər[6] <= 1080) {
        요청너비 = poçt_qutusu_verilənlər[5]; 요청높이 = poçt_qutusu_verilənlər[6];
    }
    const uint32_t HTTP_sorğusu[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(HTTP_sorğusu)/4; 순번++) poçt_qutusu_verilənlər[순번] = HTTP_sorğusu[순번];
    // 위 메시지의 faktiki_verilənlər 길이를 사용: 태그 추가 시 uzunluq_VALUE 불일치를 방지한다.
    poçt_qutusu_verilənlər[0] = sizeof(HTTP_sorğusu);
    if (!poçt_qutusu()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned video_münasibət_uzunluq[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (poçt_qutusu_verilənlər[응답들[순번]] != (0x80000000u | video_münasibət_uzunluq[순번])) return 0;
    uint32_t Fon_VALUE = poçt_qutusu_verilənlər[28] & 0x3fffffffu;
    uint32_t Böyüklük = poçt_qutusu_verilənlər[29];
    uint32_t 받은너비 = poçt_qutusu_verilənlər[5], 받은높이 = poçt_qutusu_verilənlər[6], RECEIVED_aparıcı = poçt_qutusu_verilənlər[33];
    if (poçt_qutusu_verilənlər[15] != 32 || poçt_qutusu_verilənlər[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        poçt_qutusu_verilənlər[10] < 받은너비 || poçt_qutusu_verilənlər[11] < 받은높이 || poçt_qutusu_verilənlər[23] || poçt_qutusu_verilənlər[24] ||
        !Fon_VALUE || Fon_VALUE < 0x1000000 || (Fon_VALUE & 3) || RECEIVED_aparıcı < 받은너비 * 4 || (RECEIVED_aparıcı & 3) ||
        (uint64_t)RECEIVED_aparıcı * 받은높이 > Böyüklük || (uint64_t)Fon_VALUE + Böyüklük > 0x40000000u)
        return 0;
    lövhə_Hazırla_rəsm((volatile uint32_t *)(uintptr_t)Fon_VALUE, 받은너비, 받은높이, RECEIVED_aparıcı);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 axın_VALUE_5b72a632. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } kontekst;
static kontekst 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void kontekst_SWITCH(kontekst *, kontekst *);
extern void 자바작업(int32_t);
maşın_Söz lövhə_YIELD(void) {
    network_poll();
    int 이전 = 현재작업, Sonrakı_element = (이전 + 1) % 3;
    while (Sonrakı_element != 이전 && !실행중[Sonrakı_element]) Sonrakı_element = (Sonrakı_element + 1) % 3;
    if (Sonrakı_element != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = Sonrakı_element;
        kontekst_SWITCH(&작업문맥들[이전], &작업문맥들[Sonrakı_element]);
    }
    return 0;
}
static void tapşırıq_yükləmə(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    lövhə_YIELD();
    커널중단("finished task resumed");
}
maşın_Söz lövhə_tapşırıq_yarat(maşın_Söz identifikator_VALUE) {
    if (identifikator_VALUE < 1 || identifikator_VALUE > 2 || 실행중[identifikator_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[identifikator_VALUE], 0, sizeof(kontekst));
    *(uint64_t *)쌓임공간들[identifikator_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifikator_VALUE].저장값[11] = (uintptr_t)tapşırıq_yükləmə;
    작업문맥들[identifikator_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[identifikator_VALUE - 1] + sizeof(쌓임공간들[0]));
    실행중[identifikator_VALUE] = 1;
    return 0;
}
maşın_Söz lövhə_tapşırıq_vəziyyət(maşın_Söz identifikator_VALUE) { return identifikator_VALUE < 3 ? 실행중[identifikator_VALUE] : (uint32_t)-1; }
extern maşın_Söz 미리번역기억조회(maşın_Söz);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
maşın_Söz lövhə_sorğu_sistem(maşın_Söz daxiletmə_VALUE, maşın_Söz INDEX) {
    if (daxiletmə_VALUE==0) return 팔기억킬로바이트;
    if (daxiletmə_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (daxiletmə_VALUE==2 || daxiletmə_VALUE==3) return 미리번역기억조회(daxiletmə_VALUE==3);
    if (daxiletmə_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (daxiletmə_VALUE==5) return 80*1024; /* icra_etmək_əmr 공간 16 MiB + 네 세션 보관 공간. */
    if (daxiletmə_VALUE>=20) return 사용자상태읽기(daxiletmə_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
