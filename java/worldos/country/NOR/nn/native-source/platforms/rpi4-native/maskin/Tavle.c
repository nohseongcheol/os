#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "brukar.h"
#include "../Nettverk_Stabel/Nettverk_Stabel.h"
typedef uintptr_t maskin_Word;
#define maskin_registrere(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define postboks_ADDRESS 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Klokke_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t postboks_data[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *data_plassere, int teiknkode, size_t vare_COUNT) { unsigned char *Neste_OFFSET = data_plassere; while (vare_COUNT--) *Neste_OFFSET++ = teiknkode; return data_plassere; }
void *memcpy(void *mål_data, const void *streng_data, size_t vare_COUNT) { unsigned char *첫째값 = mål_data; const unsigned char *SECOND_VALUE = streng_data; while (vare_COUNT--) *첫째값++ = *SECOND_VALUE++; return mål_data; }

static int postboks(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)postboks_data | 8;
    uint64_t Køyr_2 = Klokke_COUNT();
    기억장벽();
    while (maskin_registrere(postboks_ADDRESS + 0x38) & 0x80000000u)
        if (Klokke_COUNT() - Køyr_2 > FREQUENCY) return 0;
    maskin_registrere(postboks_ADDRESS + 0x20) = 요청;
    for (;;) {
        if (!(maskin_registrere(postboks_ADDRESS + 0x18) & 0x40000000u)) {
            uint32_t svare = maskin_registrere(postboks_ADDRESS);
            if (svare == 요청) { 기억장벽(); return postboks_data[1] == 0x80000000u; }
        }
        if (Klokke_COUNT() - Køyr_2 > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_byte(unsigned);
extern int Terminal_ventande(void);
extern void Terminal_peikar(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../fjern_VALUE/fjern_VALUE.h"
static int 흐름목록;
static unsigned 직렬이전글자;
maskin_Word 보드흐름설정(maskin_Word 사용여부) { 흐름목록=사용여부!=0; return 0; }
maskin_Word Tavle_kanal(maskin_Word kanal, maskin_Word teiknkode) {
    if(흐름목록 && 자바셸출력((int32_t)kanal,(int32_t)(teiknkode&255))) return 0;
    Terminal_byte(teiknkode&255);
    원격출력(teiknkode&255);
    if ((teiknkode&255)==10 && 직렬이전글자!=13) {
        while (maskin_registrere(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        maskin_registrere(직렬장치)=13;
    }
    직렬이전글자=teiknkode&255;
    while (maskin_registrere(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    maskin_registrere(직렬장치) = (uint32_t)teiknkode & 255;
    return 0;
}
maskin_Word 보드글자쓰기(maskin_Word teiknkode) { return Tavle_kanal(1,teiknkode); }
maskin_Word 보드원시글자읽기(void) {
    int fjern_teikn=원격입력();if(fjern_teikn>=0)return fjern_teikn;
    if (maskin_registrere(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = maskin_registrere(직렬장치);
    if (VALUE & 0xf00) { maskin_registrere(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
maskin_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char pakke_data[6];
    if(Terminal_ventande())return (uint32_t)-4096;
    if(흐름목록){int32_t teiknkode=자바셸입력();if(teiknkode!=-3)return (uint32_t)teiknkode;}
    for(;;){
        int teiknkode=(int32_t)보드원시글자읽기();if(teiknkode<0)return (uint32_t)teiknkode;
        if(!꾸러미안쪽){if(teiknkode!=30)return teiknkode;꾸러미안쪽=1;사용량=0;continue;}
        pakke_data[사용량++]=teiknkode;if(사용량<6)continue;꾸러미안쪽=0;
        if(pakke_data[0]==1)Terminal_peikar(pakke_data[1],pakke_data[2]+pakke_data[3]*256,pakke_data[4]+pakke_data[5]*256);
        if(pakke_data[0]==2)터미널바로가기키(pakke_data[1]);
        if(pakke_data[0]==3)터미널입력방식(pakke_data[1]);
        if(Terminal_ventande())return (uint32_t)-4096;
    }
}
maskin_Word 보드밀리초(void) { return (uint32_t)(Klokke_COUNT() / (FREQUENCY / 1000)); }
maskin_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *streng_data) { while (*streng_data) 보드글자쓰기((unsigned char)*streng_data++); }
static void 직렬열여섯진출력(maskin_Word vare_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int streng_data = 60; streng_data >= 0; streng_data -= 4) 보드글자쓰기(열여섯진숫자[(vare_COUNT >> streng_data) & 15]); }
maskin_Word Tavle_Stopp(maskin_Word status_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(status_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Tavle_Stopp(1); __builtin_unreachable(); }
void Tavle_unntak(maskin_Word unntak_status, maskin_Word kommando_plassere, maskin_Word ugyldig_ADDRESS) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(unntak_status);
    직렬글출력(" PC="); 직렬열여섯진출력(kommando_plassere); 직렬글출력(" FAR="); 직렬열여섯진출력(ugyldig_ADDRESS);
    Tavle_Stopp(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    postboks_data[0]=32;postboks_data[1]=0;postboks_data[2]=0x10004;postboks_data[3]=8;postboks_data[4]=0;
    postboks_data[5]=postboks_data[6]=postboks_data[7]=0;
    return postboks()&&postboks_data[4]==0x80000008u&&(postboks_data[5]||postboks_data[6]);
}
int Tavle_maskin_ADDRESS(unsigned char *ADDRESS) {
    postboks_data[0]=32;postboks_data[1]=0;postboks_data[2]=0x10003;postboks_data[3]=8;postboks_data[4]=0;
    postboks_data[5]=postboks_data[6]=postboks_data[7]=0;
    if(!postboks()||(postboks_data[4]&0x80000000u)==0||(postboks_data[4]&0xffff)!=6)return 0;
    const unsigned char *data=(const unsigned char*)&postboks_data[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){ADDRESS[순번]=data[순번];SUM_VALUE|=data[순번];}return SUM_VALUE&&!(ADDRESS[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    maskin_registrere(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    maskin_registrere(범용입출력 + 4) = (maskin_registrere(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    maskin_registrere(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. feil_VALUE 시 config.txt의 48MHz를 사용한다.
    postboks_data[0] = 36; postboks_data[1] = 0; postboks_data[2] = 0x38002; postboks_data[3] = 12;
    postboks_data[4] = 0; postboks_data[5] = 2; postboks_data[6] = 48000000; postboks_data[7] = 0; postboks_data[8] = 0;
    int 시계정상 = postboks();
    uint32_t 속도 = 시계정상 && postboks_data[6] >= 1843200 ? postboks_data[6] : 48000000;
    postboks_data[0]=32; postboks_data[1]=0; postboks_data[2]=0x10005; postboks_data[3]=8; postboks_data[4]=0;
    postboks_data[5]=postboks_data[6]=postboks_data[7]=0;
    if (postboks() && postboks_data[4]==0x80000008u) 팔기억킬로바이트=postboks_data[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    maskin_registrere(직렬장치 + 0x44) = 0x7ff;
    maskin_registrere(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    maskin_registrere(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    maskin_registrere(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    maskin_registrere(직렬장치 + 0x38) = 0;
    maskin_registrere(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
maskin_Word Tavle_FTP(maskin_Word Handling) { return (uint32_t)ftp_control((int)Handling); }
maskin_Word Tavle_Nettverk_merkje(maskin_Word oppføring_VALUE, maskin_Word INDEX) { return 망상태읽기(oppføring_VALUE, INDEX); }
maskin_Word Tavle_Nettverk_Innstillingar(maskin_Word Handling, maskin_Word ADDRESS, maskin_Word maske_VALUE, maskin_Word gateway_VALUE) { return (uint32_t)konfigurere_Nettverk(Handling, ADDRESS, maske_VALUE, gateway_VALUE); }
maskin_Word 보드응답보내기(maskin_Word ADDRESS, maskin_Word rekkjefølgje_VALUE) { return (uint32_t)응답시험시작(ADDRESS, rekkjefølgje_VALUE); }
maskin_Word 보드응답읽기(maskin_Word oppføring_VALUE) { return (uint32_t)응답시험읽기(oppføring_VALUE); }
maskin_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) Lukk_Nettverk(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) Tavle_brukarkontroll(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (maskin_registrere(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    maskin_registrere(0xfe100020ul)=0x5a000000u | (maskin_registrere(0xfe100020ul)&~0xfffu) | 0x555;
    maskin_registrere(0xfe100024ul)=0x5a000000u | 10;
    maskin_registrere(0xfe10001cul)=0x5a000000u | (maskin_registrere(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

maskin_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 betalt_vare 크기를 읽는다. */
    const uint32_t spørjing_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(spørjing_VALUE)/4; 순번++) postboks_data[순번] = spørjing_VALUE[순번];
    if (postboks() && postboks_data[4] == 0x80000008u &&
        postboks_data[5] >= 640 && postboks_data[5] <= 1920 &&
        postboks_data[6] >= 480 && postboks_data[6] <= 1080) {
        요청너비 = postboks_data[5]; 요청높이 = postboks_data[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) postboks_data[순번] = 요청[순번];
    // 위 메시지의 faktisk_data 길이를 사용: 태그 추가 시 lengd_VALUE 불일치를 방지한다.
    postboks_data[0] = sizeof(요청);
    if (!postboks()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (postboks_data[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t bakgrunn_VALUE = postboks_data[28] & 0x3fffffffu;
    uint32_t Storleik = postboks_data[29];
    uint32_t 받은너비 = postboks_data[5], 받은높이 = postboks_data[6], RECEIVED_lineavstand = postboks_data[33];
    if (postboks_data[15] != 32 || postboks_data[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        postboks_data[10] < 받은너비 || postboks_data[11] < 받은높이 || postboks_data[23] || postboks_data[24] ||
        !bakgrunn_VALUE || bakgrunn_VALUE < 0x1000000 || (bakgrunn_VALUE & 3) || RECEIVED_lineavstand < 받은너비 * 4 || (RECEIVED_lineavstand & 3) ||
        (uint64_t)RECEIVED_lineavstand * 받은높이 > Storleik || (uint64_t)bakgrunn_VALUE + Storleik > 0x40000000u)
        return 0;
    Tavle_Klargjer_teikning((volatile uint32_t *)(uintptr_t)bakgrunn_VALUE, 받은너비, 받은높이, RECEIVED_lineavstand);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 tråd_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } kontekst;
static kontekst 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int informasjonsteknologi_Løping[3] = {1, 0, 0};
static int betalt_oppgåve;
extern void kontekst_byte(kontekst *, kontekst *);
extern void 자바작업(int32_t);
maskin_Word Tavle_YIELD(void) {
    network_poll();
    int 이전 = betalt_oppgåve, Neste_vare = (이전 + 1) % 3;
    while (Neste_vare != 이전 && !informasjonsteknologi_Løping[Neste_vare]) Neste_vare = (Neste_vare + 1) % 3;
    if (Neste_vare != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (informasjonsteknologi_Løping[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        betalt_oppgåve = Neste_vare;
        kontekst_byte(&작업문맥들[이전], &작업문맥들[Neste_vare]);
    }
    return 0;
}
static void oppgåve_oppstart(void) {
    자바작업(betalt_oppgåve);
    informasjonsteknologi_Løping[betalt_oppgåve] = 0;
    Tavle_YIELD();
    커널중단("finished task resumed");
}
maskin_Word Tavle_oppgåve_Opprett(maskin_Word identifikator_VALUE) {
    if (identifikator_VALUE < 1 || identifikator_VALUE > 2 || informasjonsteknologi_Løping[identifikator_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[identifikator_VALUE], 0, sizeof(kontekst));
    *(uint64_t *)쌓임공간들[identifikator_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifikator_VALUE].저장값[11] = (uintptr_t)oppgåve_oppstart;
    작업문맥들[identifikator_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[identifikator_VALUE - 1] + sizeof(쌓임공간들[0]));
    informasjonsteknologi_Løping[identifikator_VALUE] = 1;
    return 0;
}
maskin_Word Tavle_oppgåve_status(maskin_Word identifikator_VALUE) { return identifikator_VALUE < 3 ? informasjonsteknologi_Løping[identifikator_VALUE] : (uint32_t)-1; }
extern maskin_Word 미리번역기억조회(maskin_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
maskin_Word Tavle_spørjing_system(maskin_Word oppføring_VALUE, maskin_Word INDEX) {
    if (oppføring_VALUE==0) return 팔기억킬로바이트;
    if (oppføring_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (oppføring_VALUE==2 || oppføring_VALUE==3) return 미리번역기억조회(oppføring_VALUE==3);
    if (oppføring_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (oppføring_VALUE==5) return 80*1024; /* Utfør_kommando 공간 16 MiB + 네 세션 보관 공간. */
    if (oppføring_VALUE>=20) return 사용자상태읽기(oppføring_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[betalt_oppgåve]; }
