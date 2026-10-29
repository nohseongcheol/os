#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "lietotājs.h"
#include "../tīkls_kopa/tīkls_kopa.h"
typedef uintptr_t mašīna_Word;
#define mašīna_reģistrs(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define pastkaste_adrese 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Pulkstenis_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t pastkaste_dati[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *dati_amats, int koda_punkts, size_t krājums_COUNT) { unsigned char *Tālāk_Nobīde = dati_amats; while (krājums_COUNT--) *Tālāk_Nobīde++ = koda_punkts; return dati_amats; }
void *memcpy(void *mērķis_dati, const void *virkne_dati, size_t krājums_COUNT) { unsigned char *첫째값 = mērķis_dati; const unsigned char *SECOND_VALUE = virkne_dati; while (krājums_COUNT--) *첫째값++ = *SECOND_VALUE++; return mērķis_dati; }

static int pastkaste(void) {
    uint32_t pieprasījums = (uint32_t)(uintptr_t)pastkaste_dati | 8;
    uint64_t Palaist = Pulkstenis_COUNT();
    기억장벽();
    while (mašīna_reģistrs(pastkaste_adrese + 0x38) & 0x80000000u)
        if (Pulkstenis_COUNT() - Palaist > FREQUENCY) return 0;
    mašīna_reģistrs(pastkaste_adrese + 0x20) = pieprasījums;
    for (;;) {
        if (!(mašīna_reģistrs(pastkaste_adrese + 0x18) & 0x40000000u)) {
            uint32_t atbilde = mašīna_reģistrs(pastkaste_adrese);
            if (atbilde == pieprasījums) { 기억장벽(); return pastkaste_dati[1] == 0x80000000u; }
        }
        if (Pulkstenis_COUNT() - Palaist > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminālis_byte(unsigned);
extern int Terminālis_gaida(void);
extern void Terminālis_rādītājs(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../attāls_VALUE/attāls_VALUE.h"
static int Straumes;
static unsigned 직렬이전글자;
mašīna_Word Panelis_Straumes(mašīna_Word 사용여부) { Straumes=사용여부!=0; return 0; }
mašīna_Word Panelis_Kanāls(mašīna_Word Kanāls, mašīna_Word koda_punkts) {
    if(Straumes && 자바셸출력((int32_t)Kanāls,(int32_t)(koda_punkts&255))) return 0;
    Terminālis_byte(koda_punkts&255);
    attāls_ražojums(koda_punkts&255);
    if ((koda_punkts&255)==10 && 직렬이전글자!=13) {
        while (mašīna_reģistrs(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        mašīna_reģistrs(직렬장치)=13;
    }
    직렬이전글자=koda_punkts&255;
    while (mašīna_reģistrs(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    mašīna_reģistrs(직렬장치) = (uint32_t)koda_punkts & 255;
    return 0;
}
mašīna_Word 보드글자쓰기(mašīna_Word koda_punkts) { return Panelis_Kanāls(1,koda_punkts); }
mašīna_Word 보드원시글자읽기(void) {
    int attāls_rakstzīme=원격입력();if(attāls_rakstzīme>=0)return attāls_rakstzīme;
    if (mašīna_reģistrs(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = mašīna_reģistrs(직렬장치);
    if (VALUE & 0xf00) { mašīna_reģistrs(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
mašīna_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char pakete_dati[6];
    if(Terminālis_gaida())return (uint32_t)-4096;
    if(Straumes){int32_t koda_punkts=자바셸입력();if(koda_punkts!=-3)return (uint32_t)koda_punkts;}
    for(;;){
        int koda_punkts=(int32_t)보드원시글자읽기();if(koda_punkts<0)return (uint32_t)koda_punkts;
        if(!꾸러미안쪽){if(koda_punkts!=30)return koda_punkts;꾸러미안쪽=1;사용량=0;continue;}
        pakete_dati[사용량++]=koda_punkts;if(사용량<6)continue;꾸러미안쪽=0;
        if(pakete_dati[0]==1)Terminālis_rādītājs(pakete_dati[1],pakete_dati[2]+pakete_dati[3]*256,pakete_dati[4]+pakete_dati[5]*256);
        if(pakete_dati[0]==2)터미널바로가기키(pakete_dati[1]);
        if(pakete_dati[0]==3)터미널입력방식(pakete_dati[1]);
        if(Terminālis_gaida())return (uint32_t)-4096;
    }
}
mašīna_Word 보드밀리초(void) { return (uint32_t)(Pulkstenis_COUNT() / (FREQUENCY / 1000)); }
mašīna_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *virkne_dati) { while (*virkne_dati) 보드글자쓰기((unsigned char)*virkne_dati++); }
static void 직렬열여섯진출력(mašīna_Word krājums_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int virkne_dati = 60; virkne_dati >= 0; virkne_dati -= 4) 보드글자쓰기(열여섯진숫자[(krājums_COUNT >> virkne_dati) & 15]); }
mašīna_Word Panelis_Stop(mašīna_Word Statuss_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Statuss_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Panelis_Stop(1); __builtin_unreachable(); }
void Panelis_izņēmums(mašīna_Word izņēmums_Statuss, mašīna_Word komanda_amats, mašīna_Word nederīgs_adrese) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(izņēmums_Statuss);
    직렬글출력(" PC="); 직렬열여섯진출력(komanda_amats); 직렬글출력(" FAR="); 직렬열여섯진출력(nederīgs_adrese);
    Panelis_Stop(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    pastkaste_dati[0]=32;pastkaste_dati[1]=0;pastkaste_dati[2]=0x10004;pastkaste_dati[3]=8;pastkaste_dati[4]=0;
    pastkaste_dati[5]=pastkaste_dati[6]=pastkaste_dati[7]=0;
    return pastkaste()&&pastkaste_dati[4]==0x80000008u&&(pastkaste_dati[5]||pastkaste_dati[6]);
}
int Panelis_reālā_adrese(unsigned char *adrese) {
    pastkaste_dati[0]=32;pastkaste_dati[1]=0;pastkaste_dati[2]=0x10003;pastkaste_dati[3]=8;pastkaste_dati[4]=0;
    pastkaste_dati[5]=pastkaste_dati[6]=pastkaste_dati[7]=0;
    if(!pastkaste()||(pastkaste_dati[4]&0x80000000u)==0||(pastkaste_dati[4]&0xffff)!=6)return 0;
    const unsigned char *dati=(const unsigned char*)&pastkaste_dati[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){adrese[순번]=dati[순번];SUM_VALUE|=dati[순번];}return SUM_VALUE&&!(adrese[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    mašīna_reģistrs(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    mašīna_reģistrs(범용입출력 + 4) = (mašīna_reģistrs(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    mašīna_reģistrs(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. kļūme_VALUE 시 config.txt의 48MHz를 사용한다.
    pastkaste_dati[0] = 36; pastkaste_dati[1] = 0; pastkaste_dati[2] = 0x38002; pastkaste_dati[3] = 12;
    pastkaste_dati[4] = 0; pastkaste_dati[5] = 2; pastkaste_dati[6] = 48000000; pastkaste_dati[7] = 0; pastkaste_dati[8] = 0;
    int 시계정상 = pastkaste();
    uint32_t 속도 = 시계정상 && pastkaste_dati[6] >= 1843200 ? pastkaste_dati[6] : 48000000;
    pastkaste_dati[0]=32; pastkaste_dati[1]=0; pastkaste_dati[2]=0x10005; pastkaste_dati[3]=8; pastkaste_dati[4]=0;
    pastkaste_dati[5]=pastkaste_dati[6]=pastkaste_dati[7]=0;
    if (pastkaste() && pastkaste_dati[4]==0x80000008u) 팔기억킬로바이트=pastkaste_dati[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    mašīna_reģistrs(직렬장치 + 0x44) = 0x7ff;
    mašīna_reģistrs(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    mašīna_reģistrs(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    mašīna_reģistrs(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    mašīna_reģistrs(직렬장치 + 0x38) = 0;
    mašīna_reģistrs(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
mašīna_Word Panelis_FTP(mašīna_Word Darbība) { return (uint32_t)ftp_control((int)Darbība); }
mašīna_Word Panelis_tīkls_statuss(mašīna_Word ievade_VALUE, mašīna_Word INDEX) { return 망상태읽기(ievade_VALUE, INDEX); }
mašīna_Word Panelis_tīkls_Iestatījumi(mašīna_Word Darbība, mašīna_Word adrese, mašīna_Word maska_VALUE, mašīna_Word vārteja_VALUE) { return (uint32_t)konfigurēt_tīkls(Darbība, adrese, maska_VALUE, vārteja_VALUE); }
mašīna_Word Panelis_sūtīt_atbilde(mašīna_Word adrese, mašīna_Word secība_VALUE) { return (uint32_t)응답시험시작(adrese, secība_VALUE); }
mašīna_Word 보드응답읽기(mašīna_Word ievade_VALUE) { return (uint32_t)응답시험읽기(ievade_VALUE); }
mašīna_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) Aizvērt_tīkls(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) Panelis_lietotāja_vadīkla(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (mašīna_reģistrs(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    mašīna_reģistrs(0xfe100020ul)=0x5a000000u | (mašīna_reģistrs(0xfe100020ul)&~0xfffu) | 0x555;
    mašīna_reģistrs(0xfe100024ul)=0x5a000000u | 10;
    mašīna_reģistrs(0xfe10001cul)=0x5a000000u | (mašīna_reģistrs(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

mašīna_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 pašreizējais_krājums 크기를 읽는다. */
    const uint32_t vaicāt_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(vaicāt_VALUE)/4; 순번++) pastkaste_dati[순번] = vaicāt_VALUE[순번];
    if (pastkaste() && pastkaste_dati[4] == 0x80000008u &&
        pastkaste_dati[5] >= 640 && pastkaste_dati[5] <= 1920 &&
        pastkaste_dati[6] >= 480 && pastkaste_dati[6] <= 1080) {
        요청너비 = pastkaste_dati[5]; 요청높이 = pastkaste_dati[6];
    }
    const uint32_t pieprasījums[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(pieprasījums)/4; 순번++) pastkaste_dati[순번] = pieprasījums[순번];
    // 위 메시지의 faktisks_dati 길이를 lietot_VALUE: 태그 Pievienot_ievade 시 길이 불일치를 방지한다.
    pastkaste_dati[0] = sizeof(pieprasījums);
    if (!pastkaste()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (pastkaste_dati[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Fons_VALUE = pastkaste_dati[28] & 0x3fffffffu;
    uint32_t Izmērs = pastkaste_dati[29];
    uint32_t 받은너비 = pastkaste_dati[5], 받은높이 = pastkaste_dati[6], RECEIVED_rindstarpa = pastkaste_dati[33];
    if (pastkaste_dati[15] != 32 || pastkaste_dati[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        pastkaste_dati[10] < 받은너비 || pastkaste_dati[11] < 받은높이 || pastkaste_dati[23] || pastkaste_dati[24] ||
        !Fons_VALUE || Fons_VALUE < 0x1000000 || (Fons_VALUE & 3) || RECEIVED_rindstarpa < 받은너비 * 4 || (RECEIVED_rindstarpa & 3) ||
        (uint64_t)RECEIVED_rindstarpa * 받은높이 > Izmērs || (uint64_t)Fons_VALUE + Izmērs > 0x40000000u)
        return 0;
    Panelis_Sagatavot_zīmējums((volatile uint32_t *)(uintptr_t)Fons_VALUE, 받은너비, 받은높이, RECEIVED_rindstarpa);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 saruna_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } konteksts;
static konteksts 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int informācijas_tehnoloģija_Skriešana[3] = {1, 0, 0};
static int pašreizējais_uzdevums;
extern void konteksta_pārslēgšana(konteksts *, konteksts *);
extern void 자바작업(int32_t);
mašīna_Word Panelis_YIELD(void) {
    network_poll();
    int 이전 = pašreizējais_uzdevums, Tālāk_krājums = (이전 + 1) % 3;
    while (Tālāk_krājums != 이전 && !informācijas_tehnoloģija_Skriešana[Tālāk_krājums]) Tālāk_krājums = (Tālāk_krājums + 1) % 3;
    if (Tālāk_krājums != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (informācijas_tehnoloģija_Skriešana[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        pašreizējais_uzdevums = Tālāk_krājums;
        konteksta_pārslēgšana(&작업문맥들[이전], &작업문맥들[Tālāk_krājums]);
    }
    return 0;
}
static void uzdevums_palaišana(void) {
    자바작업(pašreizējais_uzdevums);
    informācijas_tehnoloģija_Skriešana[pašreizējais_uzdevums] = 0;
    Panelis_YIELD();
    커널중단("finished task resumed");
}
mašīna_Word Panelis_uzdevums_atvērt(mašīna_Word identifikators_VALUE) {
    if (identifikators_VALUE < 1 || identifikators_VALUE > 2 || informācijas_tehnoloģija_Skriešana[identifikators_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[identifikators_VALUE], 0, sizeof(konteksts));
    *(uint64_t *)쌓임공간들[identifikators_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifikators_VALUE].저장값[11] = (uintptr_t)uzdevums_palaišana;
    작업문맥들[identifikators_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[identifikators_VALUE - 1] + sizeof(쌓임공간들[0]));
    informācijas_tehnoloģija_Skriešana[identifikators_VALUE] = 1;
    return 0;
}
mašīna_Word Panelis_uzdevums_Statuss(mašīna_Word identifikators_VALUE) { return identifikators_VALUE < 3 ? informācijas_tehnoloģija_Skriešana[identifikators_VALUE] : (uint32_t)-1; }
extern mašīna_Word AOT_atmiņa_LOOKUP(mašīna_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
mašīna_Word Panelis_vaicāt_sistēma(mašīna_Word ievade_VALUE, mašīna_Word INDEX) {
    if (ievade_VALUE==0) return 팔기억킬로바이트;
    if (ievade_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (ievade_VALUE==2 || ievade_VALUE==3) return AOT_atmiņa_LOOKUP(ievade_VALUE==3);
    if (ievade_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (ievade_VALUE==5) return 80*1024; /* Izpildīt_komanda adrese_reģions 16 MiB + 네 세션 보관 adrese_reģions. */
    if (ievade_VALUE>=20) return 사용자상태읽기(ievade_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[pašreizējais_uzdevums]; }
