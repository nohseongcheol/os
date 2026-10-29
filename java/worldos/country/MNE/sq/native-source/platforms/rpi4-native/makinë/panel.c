#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "përdorues.h"
#include "../rrjet_Stivë/rrjet_Stivë.h"
typedef uintptr_t makinë_Word;
#define makinë_regjistroj(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define kuti_postare_email 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Ora_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t kuti_postare_të_dhëna[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *të_dhëna_pozicioni, int kodi_i_karakterit, size_t njësi_COUNT) { unsigned char *Tjetër_OFFSET = të_dhëna_pozicioni; while (njësi_COUNT--) *Tjetër_OFFSET++ = kodi_i_karakterit; return të_dhëna_pozicioni; }
void *memcpy(void *vendmbërritje_të_dhëna, const void *varg_të_dhëna, size_t njësi_COUNT) { unsigned char *첫째값 = vendmbërritje_të_dhëna; const unsigned char *SECOND_VALUE = varg_të_dhëna; while (njësi_COUNT--) *첫째값++ = *SECOND_VALUE++; return vendmbërritje_të_dhëna; }

static int kuti_postare(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)kuti_postare_të_dhëna | 8;
    uint64_t Ekzekuto = Ora_COUNT();
    기억장벽();
    while (makinë_regjistroj(kuti_postare_email + 0x38) & 0x80000000u)
        if (Ora_COUNT() - Ekzekuto > FREQUENCY) return 0;
    makinë_regjistroj(kuti_postare_email + 0x20) = 요청;
    for (;;) {
        if (!(makinë_regjistroj(kuti_postare_email + 0x18) & 0x40000000u)) {
            uint32_t replikë = makinë_regjistroj(kuti_postare_email);
            if (replikë == 요청) { 기억장벽(); return kuti_postare_të_dhëna[1] == 0x80000000u; }
        }
        if (Ora_COUNT() - Ekzekuto > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminali_bajt(unsigned);
extern int Terminali_në_pritje(void);
extern void Terminali_tregues(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../në_largësi_VALUE/në_largësi_VALUE.h"
static int 흐름목록;
static unsigned 직렬이전글자;
makinë_Word 보드흐름설정(makinë_Word 사용여부) { 흐름목록=사용여부!=0; return 0; }
makinë_Word panel_kanal(makinë_Word kanal, makinë_Word kodi_i_karakterit) {
    if(흐름목록 && 자바셸출력((int32_t)kanal,(int32_t)(kodi_i_karakterit&255))) return 0;
    Terminali_bajt(kodi_i_karakterit&255);
    원격출력(kodi_i_karakterit&255);
    if ((kodi_i_karakterit&255)==10 && 직렬이전글자!=13) {
        while (makinë_regjistroj(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        makinë_regjistroj(직렬장치)=13;
    }
    직렬이전글자=kodi_i_karakterit&255;
    while (makinë_regjistroj(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    makinë_regjistroj(직렬장치) = (uint32_t)kodi_i_karakterit & 255;
    return 0;
}
makinë_Word 보드글자쓰기(makinë_Word kodi_i_karakterit) { return panel_kanal(1,kodi_i_karakterit); }
makinë_Word 보드원시글자읽기(void) {
    int në_largësi_karakter=원격입력();if(në_largësi_karakter>=0)return në_largësi_karakter;
    if (makinë_regjistroj(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = makinë_regjistroj(직렬장치);
    if (VALUE & 0xf00) { makinë_regjistroj(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
makinë_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char paketë_të_dhëna[6];
    if(Terminali_në_pritje())return (uint32_t)-4096;
    if(흐름목록){int32_t kodi_i_karakterit=자바셸입력();if(kodi_i_karakterit!=-3)return (uint32_t)kodi_i_karakterit;}
    for(;;){
        int kodi_i_karakterit=(int32_t)보드원시글자읽기();if(kodi_i_karakterit<0)return (uint32_t)kodi_i_karakterit;
        if(!꾸러미안쪽){if(kodi_i_karakterit!=30)return kodi_i_karakterit;꾸러미안쪽=1;사용량=0;continue;}
        paketë_të_dhëna[사용량++]=kodi_i_karakterit;if(사용량<6)continue;꾸러미안쪽=0;
        if(paketë_të_dhëna[0]==1)Terminali_tregues(paketë_të_dhëna[1],paketë_të_dhëna[2]+paketë_të_dhëna[3]*256,paketë_të_dhëna[4]+paketë_të_dhëna[5]*256);
        if(paketë_të_dhëna[0]==2)터미널바로가기키(paketë_të_dhëna[1]);
        if(paketë_të_dhëna[0]==3)터미널입력방식(paketë_të_dhëna[1]);
        if(Terminali_në_pritje())return (uint32_t)-4096;
    }
}
makinë_Word 보드밀리초(void) { return (uint32_t)(Ora_COUNT() / (FREQUENCY / 1000)); }
makinë_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *varg_të_dhëna) { while (*varg_të_dhëna) 보드글자쓰기((unsigned char)*varg_të_dhëna++); }
static void 직렬열여섯진출력(makinë_Word njësi_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int varg_të_dhëna = 60; varg_të_dhëna >= 0; varg_të_dhëna -= 4) 보드글자쓰기(열여섯진숫자[(njësi_COUNT >> varg_të_dhëna) & 15]); }
makinë_Word panel_Ndal(makinë_Word status_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(status_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); panel_Ndal(1); __builtin_unreachable(); }
void panel_përjashtim(makinë_Word përjashtim_status, makinë_Word komandë_pozicioni, makinë_Word i_pavlefshëm_email) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(përjashtim_status);
    직렬글출력(" PC="); 직렬열여섯진출력(komandë_pozicioni); 직렬글출력(" FAR="); 직렬열여섯진출력(i_pavlefshëm_email);
    panel_Ndal(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    kuti_postare_të_dhëna[0]=32;kuti_postare_të_dhëna[1]=0;kuti_postare_të_dhëna[2]=0x10004;kuti_postare_të_dhëna[3]=8;kuti_postare_të_dhëna[4]=0;
    kuti_postare_të_dhëna[5]=kuti_postare_të_dhëna[6]=kuti_postare_të_dhëna[7]=0;
    return kuti_postare()&&kuti_postare_të_dhëna[4]==0x80000008u&&(kuti_postare_të_dhëna[5]||kuti_postare_të_dhëna[6]);
}
int panel_makinë_email(unsigned char *email) {
    kuti_postare_të_dhëna[0]=32;kuti_postare_të_dhëna[1]=0;kuti_postare_të_dhëna[2]=0x10003;kuti_postare_të_dhëna[3]=8;kuti_postare_të_dhëna[4]=0;
    kuti_postare_të_dhëna[5]=kuti_postare_të_dhëna[6]=kuti_postare_të_dhëna[7]=0;
    if(!kuti_postare()||(kuti_postare_të_dhëna[4]&0x80000000u)==0||(kuti_postare_të_dhëna[4]&0xffff)!=6)return 0;
    const unsigned char *të_dhëna=(const unsigned char*)&kuti_postare_të_dhëna[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){email[순번]=të_dhëna[순번];SUM_VALUE|=të_dhëna[순번];}return SUM_VALUE&&!(email[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    makinë_regjistroj(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    makinë_regjistroj(범용입출력 + 4) = (makinë_regjistroj(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    makinë_regjistroj(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. dështim_VALUE 시 config.txt의 48MHz를 사용한다.
    kuti_postare_të_dhëna[0] = 36; kuti_postare_të_dhëna[1] = 0; kuti_postare_të_dhëna[2] = 0x38002; kuti_postare_të_dhëna[3] = 12;
    kuti_postare_të_dhëna[4] = 0; kuti_postare_të_dhëna[5] = 2; kuti_postare_të_dhëna[6] = 48000000; kuti_postare_të_dhëna[7] = 0; kuti_postare_të_dhëna[8] = 0;
    int 시계정상 = kuti_postare();
    uint32_t 속도 = 시계정상 && kuti_postare_të_dhëna[6] >= 1843200 ? kuti_postare_të_dhëna[6] : 48000000;
    kuti_postare_të_dhëna[0]=32; kuti_postare_të_dhëna[1]=0; kuti_postare_të_dhëna[2]=0x10005; kuti_postare_të_dhëna[3]=8; kuti_postare_të_dhëna[4]=0;
    kuti_postare_të_dhëna[5]=kuti_postare_të_dhëna[6]=kuti_postare_të_dhëna[7]=0;
    if (kuti_postare() && kuti_postare_të_dhëna[4]==0x80000008u) 팔기억킬로바이트=kuti_postare_të_dhëna[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    makinë_regjistroj(직렬장치 + 0x44) = 0x7ff;
    makinë_regjistroj(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    makinë_regjistroj(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    makinë_regjistroj(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    makinë_regjistroj(직렬장치 + 0x38) = 0;
    makinë_regjistroj(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
makinë_Word panel_FTP(makinë_Word Veprim) { return (uint32_t)ftp_control((int)Veprim); }
makinë_Word panel_rrjet_status(makinë_Word futje_VALUE, makinë_Word INDEX) { return 망상태읽기(futje_VALUE, INDEX); }
makinë_Word panel_rrjet_cilësimet(makinë_Word Veprim, makinë_Word email, makinë_Word maskë_VALUE, makinë_Word portëkalimi_VALUE) { return (uint32_t)konfiguroj_rrjet(Veprim, email, maskë_VALUE, portëkalimi_VALUE); }
makinë_Word panel_dërgoj_përgjigje(makinë_Word email, makinë_Word renditja_VALUE) { return (uint32_t)응답시험시작(email, renditja_VALUE); }
makinë_Word 보드응답읽기(makinë_Word futje_VALUE) { return (uint32_t)응답시험읽기(futje_VALUE); }
makinë_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) mbyll_rrjet(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) panel_kontroll_përdoruesi(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (makinë_regjistroj(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    makinë_regjistroj(0xfe100020ul)=0x5a000000u | (makinë_regjistroj(0xfe100020ul)&~0xfffu) | 0x555;
    makinë_regjistroj(0xfe100024ul)=0x5a000000u | 10;
    makinë_regjistroj(0xfe10001cul)=0x5a000000u | (makinë_regjistroj(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

makinë_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t pyetja_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(pyetja_VALUE)/4; 순번++) kuti_postare_të_dhëna[순번] = pyetja_VALUE[순번];
    if (kuti_postare() && kuti_postare_të_dhëna[4] == 0x80000008u &&
        kuti_postare_të_dhëna[5] >= 640 && kuti_postare_të_dhëna[5] <= 1920 &&
        kuti_postare_të_dhëna[6] >= 480 && kuti_postare_të_dhëna[6] <= 1080) {
        요청너비 = kuti_postare_të_dhëna[5]; 요청높이 = kuti_postare_të_dhëna[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) kuti_postare_të_dhëna[순번] = 요청[순번];
    // 위 메시지의 aktual_të_dhëna 길이를 사용: 태그 추가 시 gjatësi_VALUE 불일치를 방지한다.
    kuti_postare_të_dhëna[0] = sizeof(요청);
    if (!kuti_postare()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned përgjigje_gjatësi[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (kuti_postare_të_dhëna[응답들[순번]] != (0x80000000u | përgjigje_gjatësi[순번])) return 0;
    uint32_t Sfond_VALUE = kuti_postare_të_dhëna[28] & 0x3fffffffu;
    uint32_t Madhësi = kuti_postare_të_dhëna[29];
    uint32_t 받은너비 = kuti_postare_të_dhëna[5], 받은높이 = kuti_postare_të_dhëna[6], RECEIVED_hapësira_midis_rreshtave = kuti_postare_të_dhëna[33];
    if (kuti_postare_të_dhëna[15] != 32 || kuti_postare_të_dhëna[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        kuti_postare_të_dhëna[10] < 받은너비 || kuti_postare_të_dhëna[11] < 받은높이 || kuti_postare_të_dhëna[23] || kuti_postare_të_dhëna[24] ||
        !Sfond_VALUE || Sfond_VALUE < 0x1000000 || (Sfond_VALUE & 3) || RECEIVED_hapësira_midis_rreshtave < 받은너비 * 4 || (RECEIVED_hapësira_midis_rreshtave & 3) ||
        (uint64_t)RECEIVED_hapësira_midis_rreshtave * 받은높이 > Madhësi || (uint64_t)Sfond_VALUE + Madhësi > 0x40000000u)
        return 0;
    panel_Përgatit_vizatim((volatile uint32_t *)(uintptr_t)Sfond_VALUE, 받은너비, 받은높이, RECEIVED_hapësira_midis_rreshtave);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 thread_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Konteksti;
static Konteksti 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int teknologjia_e_informacionit_Vrap[3] = {1, 0, 0};
static int 현재작업;
extern void Konteksti_SWITCH(Konteksti *, Konteksti *);
extern void 자바작업(int32_t);
makinë_Word panel_YIELD(void) {
    network_poll();
    int 이전 = 현재작업, Tjetër_njësi = (이전 + 1) % 3;
    while (Tjetër_njësi != 이전 && !teknologjia_e_informacionit_Vrap[Tjetër_njësi]) Tjetër_njësi = (Tjetër_njësi + 1) % 3;
    if (Tjetër_njësi != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (teknologjia_e_informacionit_Vrap[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = Tjetër_njësi;
        Konteksti_SWITCH(&작업문맥들[이전], &작업문맥들[Tjetër_njësi]);
    }
    return 0;
}
static void detyrë_nisje(void) {
    자바작업(현재작업);
    teknologjia_e_informacionit_Vrap[현재작업] = 0;
    panel_YIELD();
    커널중단("finished task resumed");
}
makinë_Word panel_detyrë_Krijo(makinë_Word identifikues_VALUE) {
    if (identifikues_VALUE < 1 || identifikues_VALUE > 2 || teknologjia_e_informacionit_Vrap[identifikues_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[identifikues_VALUE], 0, sizeof(Konteksti));
    *(uint64_t *)쌓임공간들[identifikues_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifikues_VALUE].저장값[11] = (uintptr_t)detyrë_nisje;
    작업문맥들[identifikues_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[identifikues_VALUE - 1] + sizeof(쌓임공간들[0]));
    teknologjia_e_informacionit_Vrap[identifikues_VALUE] = 1;
    return 0;
}
makinë_Word panel_detyrë_status(makinë_Word identifikues_VALUE) { return identifikues_VALUE < 3 ? teknologjia_e_informacionit_Vrap[identifikues_VALUE] : (uint32_t)-1; }
extern makinë_Word 미리번역기억조회(makinë_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
makinë_Word panel_pyetja_sistem(makinë_Word futje_VALUE, makinë_Word INDEX) {
    if (futje_VALUE==0) return 팔기억킬로바이트;
    if (futje_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (futje_VALUE==2 || futje_VALUE==3) return 미리번역기억조회(futje_VALUE==3);
    if (futje_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (futje_VALUE==5) return 80*1024; /* zbatoj_komandë 공간 16 MiB + 네 세션 보관 공간. */
    if (futje_VALUE>=20) return 사용자상태읽기(futje_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
