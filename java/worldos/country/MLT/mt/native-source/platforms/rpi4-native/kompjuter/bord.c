#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "utent.h"
#include "../netwerk_Munzell/netwerk_Munzell.h"
typedef uintptr_t kompjuter_Word;
#define kompjuter_i_rreġistra(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define kaxxa_tal_ittri_ADDRESS 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Arloġġ_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t kaxxa_tal_ittri_data[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *data_pożizzjoni, int kodiċi_tal_karattru, size_t element_COUNT) { unsigned char *Li_Jmiss_OFFSET = data_pożizzjoni; while (element_COUNT--) *Li_Jmiss_OFFSET++ = kodiċi_tal_karattru; return data_pożizzjoni; }
void *memcpy(void *destinazzjoni_data, const void *string_data, size_t element_COUNT) { unsigned char *첫째값 = destinazzjoni_data; const unsigned char *SECOND_VALUE = string_data; while (element_COUNT--) *첫째값++ = *SECOND_VALUE++; return destinazzjoni_data; }

static int kaxxa_tal_ittri(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)kaxxa_tal_ittri_data | 8;
    uint64_t serje = Arloġġ_COUNT();
    기억장벽();
    while (kompjuter_i_rreġistra(kaxxa_tal_ittri_ADDRESS + 0x38) & 0x80000000u)
        if (Arloġġ_COUNT() - serje > FREQUENCY) return 0;
    kompjuter_i_rreġistra(kaxxa_tal_ittri_ADDRESS + 0x20) = 요청;
    for (;;) {
        if (!(kompjuter_i_rreġistra(kaxxa_tal_ittri_ADDRESS + 0x18) & 0x40000000u)) {
            uint32_t wieġeb = kompjuter_i_rreġistra(kaxxa_tal_ittri_ADDRESS);
            if (wieġeb == 요청) { 기억장벽(); return kaxxa_tal_ittri_data[1] == 0x80000000u; }
        }
        if (Arloġġ_COUNT() - serje > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_byte(unsigned);
extern int Terminal_pendenti(void);
extern void Terminal_pointer(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../mill_bogħod_VALUE/mill_bogħod_VALUE.h"
static int 흐름목록;
static unsigned 직렬이전글자;
kompjuter_Word 보드흐름설정(kompjuter_Word 사용여부) { 흐름목록=사용여부!=0; return 0; }
kompjuter_Word bord_Kanal(kompjuter_Word Kanal, kompjuter_Word kodiċi_tal_karattru) {
    if(흐름목록 && 자바셸출력((int32_t)Kanal,(int32_t)(kodiċi_tal_karattru&255))) return 0;
    Terminal_byte(kodiċi_tal_karattru&255);
    원격출력(kodiċi_tal_karattru&255);
    if ((kodiċi_tal_karattru&255)==10 && 직렬이전글자!=13) {
        while (kompjuter_i_rreġistra(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        kompjuter_i_rreġistra(직렬장치)=13;
    }
    직렬이전글자=kodiċi_tal_karattru&255;
    while (kompjuter_i_rreġistra(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    kompjuter_i_rreġistra(직렬장치) = (uint32_t)kodiċi_tal_karattru & 255;
    return 0;
}
kompjuter_Word 보드글자쓰기(kompjuter_Word kodiċi_tal_karattru) { return bord_Kanal(1,kodiċi_tal_karattru); }
kompjuter_Word 보드원시글자읽기(void) {
    int mill_bogħod_karattru=원격입력();if(mill_bogħod_karattru>=0)return mill_bogħod_karattru;
    if (kompjuter_i_rreġistra(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = kompjuter_i_rreġistra(직렬장치);
    if (VALUE & 0xf00) { kompjuter_i_rreġistra(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
kompjuter_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char pakkett_data[6];
    if(Terminal_pendenti())return (uint32_t)-4096;
    if(흐름목록){int32_t kodiċi_tal_karattru=자바셸입력();if(kodiċi_tal_karattru!=-3)return (uint32_t)kodiċi_tal_karattru;}
    for(;;){
        int kodiċi_tal_karattru=(int32_t)보드원시글자읽기();if(kodiċi_tal_karattru<0)return (uint32_t)kodiċi_tal_karattru;
        if(!꾸러미안쪽){if(kodiċi_tal_karattru!=30)return kodiċi_tal_karattru;꾸러미안쪽=1;사용량=0;continue;}
        pakkett_data[사용량++]=kodiċi_tal_karattru;if(사용량<6)continue;꾸러미안쪽=0;
        if(pakkett_data[0]==1)Terminal_pointer(pakkett_data[1],pakkett_data[2]+pakkett_data[3]*256,pakkett_data[4]+pakkett_data[5]*256);
        if(pakkett_data[0]==2)터미널바로가기키(pakkett_data[1]);
        if(pakkett_data[0]==3)터미널입력방식(pakkett_data[1]);
        if(Terminal_pendenti())return (uint32_t)-4096;
    }
}
kompjuter_Word 보드밀리초(void) { return (uint32_t)(Arloġġ_COUNT() / (FREQUENCY / 1000)); }
kompjuter_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *string_data) { while (*string_data) 보드글자쓰기((unsigned char)*string_data++); }
static void 직렬열여섯진출력(kompjuter_Word element_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int string_data = 60; string_data >= 0; string_data -= 4) 보드글자쓰기(열여섯진숫자[(element_COUNT >> string_data) & 15]); }
kompjuter_Word bord_waqqaf(kompjuter_Word stat_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(stat_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); bord_waqqaf(1); __builtin_unreachable(); }
void 보드예외(kompjuter_Word 예외상태, kompjuter_Word kmand_pożizzjoni, kompjuter_Word invalidu_ADDRESS) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(예외상태);
    직렬글출력(" PC="); 직렬열여섯진출력(kmand_pożizzjoni); 직렬글출력(" FAR="); 직렬열여섯진출력(invalidu_ADDRESS);
    bord_waqqaf(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    kaxxa_tal_ittri_data[0]=32;kaxxa_tal_ittri_data[1]=0;kaxxa_tal_ittri_data[2]=0x10004;kaxxa_tal_ittri_data[3]=8;kaxxa_tal_ittri_data[4]=0;
    kaxxa_tal_ittri_data[5]=kaxxa_tal_ittri_data[6]=kaxxa_tal_ittri_data[7]=0;
    return kaxxa_tal_ittri()&&kaxxa_tal_ittri_data[4]==0x80000008u&&(kaxxa_tal_ittri_data[5]||kaxxa_tal_ittri_data[6]);
}
int bord_kompjuter_ADDRESS(unsigned char *ADDRESS) {
    kaxxa_tal_ittri_data[0]=32;kaxxa_tal_ittri_data[1]=0;kaxxa_tal_ittri_data[2]=0x10003;kaxxa_tal_ittri_data[3]=8;kaxxa_tal_ittri_data[4]=0;
    kaxxa_tal_ittri_data[5]=kaxxa_tal_ittri_data[6]=kaxxa_tal_ittri_data[7]=0;
    if(!kaxxa_tal_ittri()||(kaxxa_tal_ittri_data[4]&0x80000000u)==0||(kaxxa_tal_ittri_data[4]&0xffff)!=6)return 0;
    const unsigned char *data=(const unsigned char*)&kaxxa_tal_ittri_data[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){ADDRESS[순번]=data[순번];SUM_VALUE|=data[순번];}return SUM_VALUE&&!(ADDRESS[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    kompjuter_i_rreġistra(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    kompjuter_i_rreġistra(범용입출력 + 4) = (kompjuter_i_rreġistra(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    kompjuter_i_rreġistra(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. żball_VALUE 시 config.txt의 48MHz를 사용한다.
    kaxxa_tal_ittri_data[0] = 36; kaxxa_tal_ittri_data[1] = 0; kaxxa_tal_ittri_data[2] = 0x38002; kaxxa_tal_ittri_data[3] = 12;
    kaxxa_tal_ittri_data[4] = 0; kaxxa_tal_ittri_data[5] = 2; kaxxa_tal_ittri_data[6] = 48000000; kaxxa_tal_ittri_data[7] = 0; kaxxa_tal_ittri_data[8] = 0;
    int 시계정상 = kaxxa_tal_ittri();
    uint32_t 속도 = 시계정상 && kaxxa_tal_ittri_data[6] >= 1843200 ? kaxxa_tal_ittri_data[6] : 48000000;
    kaxxa_tal_ittri_data[0]=32; kaxxa_tal_ittri_data[1]=0; kaxxa_tal_ittri_data[2]=0x10005; kaxxa_tal_ittri_data[3]=8; kaxxa_tal_ittri_data[4]=0;
    kaxxa_tal_ittri_data[5]=kaxxa_tal_ittri_data[6]=kaxxa_tal_ittri_data[7]=0;
    if (kaxxa_tal_ittri() && kaxxa_tal_ittri_data[4]==0x80000008u) 팔기억킬로바이트=kaxxa_tal_ittri_data[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    kompjuter_i_rreġistra(직렬장치 + 0x44) = 0x7ff;
    kompjuter_i_rreġistra(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    kompjuter_i_rreġistra(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    kompjuter_i_rreġistra(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    kompjuter_i_rreġistra(직렬장치 + 0x38) = 0;
    kompjuter_i_rreġistra(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
kompjuter_Word bord_FTP(kompjuter_Word azzjoni) { return (uint32_t)ftp_control((int)azzjoni); }
kompjuter_Word bord_netwerk_stat(kompjuter_Word entrata_VALUE, kompjuter_Word INDEX) { return 망상태읽기(entrata_VALUE, INDEX); }
kompjuter_Word bord_netwerk_Settings(kompjuter_Word azzjoni, kompjuter_Word ADDRESS, kompjuter_Word maskra_VALUE, kompjuter_Word gateway_VALUE) { return (uint32_t)kkonfigura_netwerk(azzjoni, ADDRESS, maskra_VALUE, gateway_VALUE); }
kompjuter_Word 보드응답보내기(kompjuter_Word ADDRESS, kompjuter_Word ordni_VALUE) { return (uint32_t)응답시험시작(ADDRESS, ordni_VALUE); }
kompjuter_Word 보드응답읽기(kompjuter_Word entrata_VALUE) { return (uint32_t)응답시험읽기(entrata_VALUE); }
kompjuter_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) agħlaq_netwerk(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) bord_kontroll_tal_utent(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (kompjuter_i_rreġistra(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    kompjuter_i_rreġistra(0xfe100020ul)=0x5a000000u | (kompjuter_i_rreġistra(0xfe100020ul)&~0xfffu) | 0x555;
    kompjuter_i_rreġistra(0xfe100024ul)=0x5a000000u | 10;
    kompjuter_i_rreġistra(0xfe10001cul)=0x5a000000u | (kompjuter_i_rreġistra(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

kompjuter_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t query_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(query_VALUE)/4; 순번++) kaxxa_tal_ittri_data[순번] = query_VALUE[순번];
    if (kaxxa_tal_ittri() && kaxxa_tal_ittri_data[4] == 0x80000008u &&
        kaxxa_tal_ittri_data[5] >= 640 && kaxxa_tal_ittri_data[5] <= 1920 &&
        kaxxa_tal_ittri_data[6] >= 480 && kaxxa_tal_ittri_data[6] <= 1080) {
        요청너비 = kaxxa_tal_ittri_data[5]; 요청높이 = kaxxa_tal_ittri_data[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) kaxxa_tal_ittri_data[순번] = 요청[순번];
    // 위 메시지의 attwali_data 길이를 사용: 태그 추가 시 tul_VALUE 불일치를 방지한다.
    kaxxa_tal_ittri_data[0] = sizeof(요청);
    if (!kaxxa_tal_ittri()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (kaxxa_tal_ittri_data[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Sfond_VALUE = kaxxa_tal_ittri_data[28] & 0x3fffffffu;
    uint32_t daqqas = kaxxa_tal_ittri_data[29];
    uint32_t 받은너비 = kaxxa_tal_ittri_data[5], 받은높이 = kaxxa_tal_ittri_data[6], RECEIVED_leading = kaxxa_tal_ittri_data[33];
    if (kaxxa_tal_ittri_data[15] != 32 || kaxxa_tal_ittri_data[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        kaxxa_tal_ittri_data[10] < 받은너비 || kaxxa_tal_ittri_data[11] < 받은높이 || kaxxa_tal_ittri_data[23] || kaxxa_tal_ittri_data[24] ||
        !Sfond_VALUE || Sfond_VALUE < 0x1000000 || (Sfond_VALUE & 3) || RECEIVED_leading < 받은너비 * 4 || (RECEIVED_leading & 3) ||
        (uint64_t)RECEIVED_leading * 받은높이 > daqqas || (uint64_t)Sfond_VALUE + daqqas > 0x40000000u)
        return 0;
    bord_Ħejji_tpinġija((volatile uint32_t *)(uintptr_t)Sfond_VALUE, 받은너비, 받은높이, RECEIVED_leading);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 fil_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Kuntest;
static Kuntest 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void Kuntest_qaleb(Kuntest *, Kuntest *);
extern void 자바작업(int32_t);
kompjuter_Word bord_YIELD(void) {
    network_poll();
    int 이전 = 현재작업, Li_Jmiss_element = (이전 + 1) % 3;
    while (Li_Jmiss_element != 이전 && !실행중[Li_Jmiss_element]) Li_Jmiss_element = (Li_Jmiss_element + 1) % 3;
    if (Li_Jmiss_element != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = Li_Jmiss_element;
        Kuntest_qaleb(&작업문맥들[이전], &작업문맥들[Li_Jmiss_element]);
    }
    return 0;
}
static void attività_ftuħ(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    bord_YIELD();
    커널중단("finished task resumed");
}
kompjuter_Word bord_attività_ħalaq(kompjuter_Word identifikatur_VALUE) {
    if (identifikatur_VALUE < 1 || identifikatur_VALUE > 2 || 실행중[identifikatur_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[identifikatur_VALUE], 0, sizeof(Kuntest));
    *(uint64_t *)쌓임공간들[identifikatur_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifikatur_VALUE].저장값[11] = (uintptr_t)attività_ftuħ;
    작업문맥들[identifikatur_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[identifikatur_VALUE - 1] + sizeof(쌓임공간들[0]));
    실행중[identifikatur_VALUE] = 1;
    return 0;
}
kompjuter_Word bord_attività_stat(kompjuter_Word identifikatur_VALUE) { return identifikatur_VALUE < 3 ? 실행중[identifikatur_VALUE] : (uint32_t)-1; }
extern kompjuter_Word 미리번역기억조회(kompjuter_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
kompjuter_Word bord_query_sistema(kompjuter_Word entrata_VALUE, kompjuter_Word INDEX) {
    if (entrata_VALUE==0) return 팔기억킬로바이트;
    if (entrata_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (entrata_VALUE==2 || entrata_VALUE==3) return 미리번역기억조회(entrata_VALUE==3);
    if (entrata_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (entrata_VALUE==5) return 80*1024; /* eżegwixxa_kmand 공간 16 MiB + 네 세션 보관 공간. */
    if (entrata_VALUE>=20) return 사용자상태읽기(entrata_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
