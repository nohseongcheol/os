#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "foydalanuvchi.h"
#include "../Tarmoq_Stack/Tarmoq_Stack.h"
typedef uintptr_t 기계낱말;
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define pochta_qutisi_manzil 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Soat_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t pochta_qutisi_ma_lumotlar[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *ma_lumotlar_holat, int belgi_kodi, size_t element_COUNT) { unsigned char *Keyingi_OFFSET = ma_lumotlar_holat; while (element_COUNT--) *Keyingi_OFFSET++ = belgi_kodi; return ma_lumotlar_holat; }
void *memcpy(void *ko_chirish_joyi_ma_lumotlar, const void *satr_ma_lumotlar, size_t element_COUNT) { unsigned char *첫째값 = ko_chirish_joyi_ma_lumotlar; const unsigned char *SECOND_VALUE = satr_ma_lumotlar; while (element_COUNT--) *첫째값++ = *SECOND_VALUE++; return ko_chirish_joyi_ma_lumotlar; }

static int pochta_qutisi(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)pochta_qutisi_ma_lumotlar | 8;
    uint64_t Bajarish = Soat_COUNT();
    기억장벽();
    while (기계저장기(pochta_qutisi_manzil + 0x38) & 0x80000000u)
        if (Soat_COUNT() - Bajarish > FREQUENCY) return 0;
    기계저장기(pochta_qutisi_manzil + 0x20) = 요청;
    for (;;) {
        if (!(기계저장기(pochta_qutisi_manzil + 0x18) & 0x40000000u)) {
            uint32_t javob_berish = 기계저장기(pochta_qutisi_manzil);
            if (javob_berish == 요청) { 기억장벽(); return pochta_qutisi_ma_lumotlar[1] == 0x80000000u; }
        }
        if (Soat_COUNT() - Bajarish > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_bayt(unsigned);
extern int 터미널대기(void);
extern void Terminal_kursor(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../masofaviy_VALUE/masofaviy_VALUE.h"
static int 흐름목록;
static unsigned 직렬이전글자;
기계낱말 보드흐름설정(기계낱말 사용여부) { 흐름목록=사용여부!=0; return 0; }
기계낱말 yozuv_taxtasi_kanal(기계낱말 kanal, 기계낱말 belgi_kodi) {
    if(흐름목록 && 자바셸출력((int32_t)kanal,(int32_t)(belgi_kodi&255))) return 0;
    Terminal_bayt(belgi_kodi&255);
    원격출력(belgi_kodi&255);
    if ((belgi_kodi&255)==10 && 직렬이전글자!=13) {
        while (기계저장기(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        기계저장기(직렬장치)=13;
    }
    직렬이전글자=belgi_kodi&255;
    while (기계저장기(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    기계저장기(직렬장치) = (uint32_t)belgi_kodi & 255;
    return 0;
}
기계낱말 보드글자쓰기(기계낱말 belgi_kodi) { return yozuv_taxtasi_kanal(1,belgi_kodi); }
기계낱말 보드원시글자읽기(void) {
    int masofaviy_belgi=원격입력();if(masofaviy_belgi>=0)return masofaviy_belgi;
    if (기계저장기(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = 기계저장기(직렬장치);
    if (VALUE & 0xf00) { 기계저장기(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
기계낱말 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char 꾸러미자료[6];
    if(터미널대기())return (uint32_t)-4096;
    if(흐름목록){int32_t belgi_kodi=자바셸입력();if(belgi_kodi!=-3)return (uint32_t)belgi_kodi;}
    for(;;){
        int belgi_kodi=(int32_t)보드원시글자읽기();if(belgi_kodi<0)return (uint32_t)belgi_kodi;
        if(!꾸러미안쪽){if(belgi_kodi!=30)return belgi_kodi;꾸러미안쪽=1;사용량=0;continue;}
        꾸러미자료[사용량++]=belgi_kodi;if(사용량<6)continue;꾸러미안쪽=0;
        if(꾸러미자료[0]==1)Terminal_kursor(꾸러미자료[1],꾸러미자료[2]+꾸러미자료[3]*256,꾸러미자료[4]+꾸러미자료[5]*256);
        if(꾸러미자료[0]==2)터미널바로가기키(꾸러미자료[1]);
        if(꾸러미자료[0]==3)터미널입력방식(꾸러미자료[1]);
        if(터미널대기())return (uint32_t)-4096;
    }
}
기계낱말 보드밀리초(void) { return (uint32_t)(Soat_COUNT() / (FREQUENCY / 1000)); }
기계낱말 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *satr_ma_lumotlar) { while (*satr_ma_lumotlar) 보드글자쓰기((unsigned char)*satr_ma_lumotlar++); }
static void 직렬열여섯진출력(기계낱말 element_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int satr_ma_lumotlar = 60; satr_ma_lumotlar >= 0; satr_ma_lumotlar -= 4) 보드글자쓰기(열여섯진숫자[(element_COUNT >> satr_ma_lumotlar) & 15]); }
기계낱말 yozuv_taxtasi_To_xtatish(기계낱말 holat_VALUE_e10195a1) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(holat_VALUE_e10195a1); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); yozuv_taxtasi_To_xtatish(1); __builtin_unreachable(); }
void yozuv_taxtasi_istisno(기계낱말 istisno_holat, 기계낱말 buyruq_holat, 기계낱말 xato_manzil) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(istisno_holat);
    직렬글출력(" PC="); 직렬열여섯진출력(buyruq_holat); 직렬글출력(" FAR="); 직렬열여섯진출력(xato_manzil);
    yozuv_taxtasi_To_xtatish(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    pochta_qutisi_ma_lumotlar[0]=32;pochta_qutisi_ma_lumotlar[1]=0;pochta_qutisi_ma_lumotlar[2]=0x10004;pochta_qutisi_ma_lumotlar[3]=8;pochta_qutisi_ma_lumotlar[4]=0;
    pochta_qutisi_ma_lumotlar[5]=pochta_qutisi_ma_lumotlar[6]=pochta_qutisi_ma_lumotlar[7]=0;
    return pochta_qutisi()&&pochta_qutisi_ma_lumotlar[4]==0x80000008u&&(pochta_qutisi_ma_lumotlar[5]||pochta_qutisi_ma_lumotlar[6]);
}
int 보드기계주소(unsigned char *manzil) {
    pochta_qutisi_ma_lumotlar[0]=32;pochta_qutisi_ma_lumotlar[1]=0;pochta_qutisi_ma_lumotlar[2]=0x10003;pochta_qutisi_ma_lumotlar[3]=8;pochta_qutisi_ma_lumotlar[4]=0;
    pochta_qutisi_ma_lumotlar[5]=pochta_qutisi_ma_lumotlar[6]=pochta_qutisi_ma_lumotlar[7]=0;
    if(!pochta_qutisi()||(pochta_qutisi_ma_lumotlar[4]&0x80000000u)==0||(pochta_qutisi_ma_lumotlar[4]&0xffff)!=6)return 0;
    const unsigned char *ma_lumotlar=(const unsigned char*)&pochta_qutisi_ma_lumotlar[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){manzil[순번]=ma_lumotlar[순번];SUM_VALUE|=ma_lumotlar[순번];}return SUM_VALUE&&!(manzil[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    기계저장기(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    기계저장기(범용입출력 + 4) = (기계저장기(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    기계저장기(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. to_xtab_qolish_VALUE 시 config.txt의 48MHz를 사용한다.
    pochta_qutisi_ma_lumotlar[0] = 36; pochta_qutisi_ma_lumotlar[1] = 0; pochta_qutisi_ma_lumotlar[2] = 0x38002; pochta_qutisi_ma_lumotlar[3] = 12;
    pochta_qutisi_ma_lumotlar[4] = 0; pochta_qutisi_ma_lumotlar[5] = 2; pochta_qutisi_ma_lumotlar[6] = 48000000; pochta_qutisi_ma_lumotlar[7] = 0; pochta_qutisi_ma_lumotlar[8] = 0;
    int 시계정상 = pochta_qutisi();
    uint32_t 속도 = 시계정상 && pochta_qutisi_ma_lumotlar[6] >= 1843200 ? pochta_qutisi_ma_lumotlar[6] : 48000000;
    pochta_qutisi_ma_lumotlar[0]=32; pochta_qutisi_ma_lumotlar[1]=0; pochta_qutisi_ma_lumotlar[2]=0x10005; pochta_qutisi_ma_lumotlar[3]=8; pochta_qutisi_ma_lumotlar[4]=0;
    pochta_qutisi_ma_lumotlar[5]=pochta_qutisi_ma_lumotlar[6]=pochta_qutisi_ma_lumotlar[7]=0;
    if (pochta_qutisi() && pochta_qutisi_ma_lumotlar[4]==0x80000008u) 팔기억킬로바이트=pochta_qutisi_ma_lumotlar[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    기계저장기(직렬장치 + 0x44) = 0x7ff;
    기계저장기(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    기계저장기(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    기계저장기(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    기계저장기(직렬장치 + 0x38) = 0;
    기계저장기(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
기계낱말 yozuv_taxtasi_FTP(기계낱말 Amal) { return (uint32_t)ftp_control((int)Amal); }
기계낱말 yozuv_taxtasi_Tarmoq_holat(기계낱말 kiritish_VALUE, 기계낱말 INDEX) { return 망상태읽기(kiritish_VALUE, INDEX); }
기계낱말 yozuv_taxtasi_Tarmoq_Sozlamalar(기계낱말 Amal, 기계낱말 manzil, 기계낱말 niqob_VALUE, 기계낱말 shluz_VALUE) { return (uint32_t)sozlamoq_Tarmoq(Amal, manzil, niqob_VALUE, shluz_VALUE); }
기계낱말 보드응답보내기(기계낱말 manzil, 기계낱말 tartib_VALUE) { return (uint32_t)응답시험시작(manzil, tartib_VALUE); }
기계낱말 보드응답읽기(기계낱말 kiritish_VALUE) { return (uint32_t)응답시험읽기(kiritish_VALUE); }
기계낱말 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) yopmoq_Tarmoq(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) yozuv_taxtasi_foydalanuvchi_nazorati(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (기계저장기(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    기계저장기(0xfe100020ul)=0x5a000000u | (기계저장기(0xfe100020ul)&~0xfffu) | 0x555;
    기계저장기(0xfe100024ul)=0x5a000000u | 10;
    기계저장기(0xfe10001cul)=0x5a000000u | (기계저장기(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

기계낱말 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t so_rov_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(so_rov_VALUE)/4; 순번++) pochta_qutisi_ma_lumotlar[순번] = so_rov_VALUE[순번];
    if (pochta_qutisi() && pochta_qutisi_ma_lumotlar[4] == 0x80000008u &&
        pochta_qutisi_ma_lumotlar[5] >= 640 && pochta_qutisi_ma_lumotlar[5] <= 1920 &&
        pochta_qutisi_ma_lumotlar[6] >= 480 && pochta_qutisi_ma_lumotlar[6] <= 1080) {
        요청너비 = pochta_qutisi_ma_lumotlar[5]; 요청높이 = pochta_qutisi_ma_lumotlar[6];
    }
    const uint32_t 요청[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) pochta_qutisi_ma_lumotlar[순번] = 요청[순번];
    // 위 메시지의 real_ma_lumotlar 길이를 사용: 태그 추가 시 uzunlik_VALUE 불일치를 방지한다.
    pochta_qutisi_ma_lumotlar[0] = sizeof(요청);
    if (!pochta_qutisi()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (pochta_qutisi_ma_lumotlar[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Fon_VALUE = pochta_qutisi_ma_lumotlar[28] & 0x3fffffffu;
    uint32_t Hajmi = pochta_qutisi_ma_lumotlar[29];
    uint32_t 받은너비 = pochta_qutisi_ma_lumotlar[5], 받은높이 = pochta_qutisi_ma_lumotlar[6], RECEIVED_yetakchi = pochta_qutisi_ma_lumotlar[33];
    if (pochta_qutisi_ma_lumotlar[15] != 32 || pochta_qutisi_ma_lumotlar[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        pochta_qutisi_ma_lumotlar[10] < 받은너비 || pochta_qutisi_ma_lumotlar[11] < 받은높이 || pochta_qutisi_ma_lumotlar[23] || pochta_qutisi_ma_lumotlar[24] ||
        !Fon_VALUE || Fon_VALUE < 0x1000000 || (Fon_VALUE & 3) || RECEIVED_yetakchi < 받은너비 * 4 || (RECEIVED_yetakchi & 3) ||
        (uint64_t)RECEIVED_yetakchi * 받은높이 > Hajmi || (uint64_t)Fon_VALUE + Hajmi > 0x40000000u)
        return 0;
    yozuv_taxtasi_Tayyorlamoq_chizish((volatile uint32_t *)(uintptr_t)Fon_VALUE, 받은너비, 받은높이, RECEIVED_yetakchi);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 oqim_VALUE_5b72a632. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Kontekst;
static Kontekst 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void Kontekst_SWITCH(Kontekst *, Kontekst *);
extern void 자바작업(int32_t);
기계낱말 yozuv_taxtasi_YIELD(void) {
    network_poll();
    int 이전 = 현재작업, Keyingi_element = (이전 + 1) % 3;
    while (Keyingi_element != 이전 && !실행중[Keyingi_element]) Keyingi_element = (Keyingi_element + 1) % 3;
    if (Keyingi_element != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = Keyingi_element;
        Kontekst_SWITCH(&작업문맥들[이전], &작업문맥들[Keyingi_element]);
    }
    return 0;
}
static void vazifa_yuklash(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    yozuv_taxtasi_YIELD();
    커널중단("finished task resumed");
}
기계낱말 yozuv_taxtasi_vazifa_Yaratish(기계낱말 identifikator_VALUE) {
    if (identifikator_VALUE < 1 || identifikator_VALUE > 2 || 실행중[identifikator_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[identifikator_VALUE], 0, sizeof(Kontekst));
    *(uint64_t *)쌓임공간들[identifikator_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifikator_VALUE].저장값[11] = (uintptr_t)vazifa_yuklash;
    작업문맥들[identifikator_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[identifikator_VALUE - 1] + sizeof(쌓임공간들[0]));
    실행중[identifikator_VALUE] = 1;
    return 0;
}
기계낱말 yozuv_taxtasi_vazifa_holat(기계낱말 identifikator_VALUE) { return identifikator_VALUE < 3 ? 실행중[identifikator_VALUE] : (uint32_t)-1; }
extern 기계낱말 미리번역기억조회(기계낱말);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
기계낱말 yozuv_taxtasi_so_rov_tizim(기계낱말 kiritish_VALUE, 기계낱말 INDEX) {
    if (kiritish_VALUE==0) return 팔기억킬로바이트;
    if (kiritish_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (kiritish_VALUE==2 || kiritish_VALUE==3) return 미리번역기억조회(kiritish_VALUE==3);
    if (kiritish_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (kiritish_VALUE==5) return 80*1024; /* bajarmoq_buyruq 공간 16 MiB + 네 세션 보관 공간. */
    if (kiritish_VALUE>=20) return 사용자상태읽기(kiritish_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
