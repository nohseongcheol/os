#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "gebruiker.h"
#include "../Netwerk_Stapel/Netwerk_Stapel.h"
typedef uintptr_t masjien_Word;
#define masjien_registreer(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define posbus_adres 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Klok_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t posbus_data[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *data_plaas, int karakterkode, size_t item_COUNT) { unsigned char *Volgende_OFFSET = data_plaas; while (item_COUNT--) *Volgende_OFFSET++ = karakterkode; return data_plaas; }
void *memcpy(void *bestemming_data, const void *string_data, size_t item_COUNT) { unsigned char *첫째값 = bestemming_data; const unsigned char *SECOND_VALUE = string_data; while (item_COUNT--) *첫째값++ = *SECOND_VALUE++; return bestemming_data; }

static int posbus(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)posbus_data | 8;
    uint64_t Loop = Klok_COUNT();
    기억장벽();
    while (masjien_registreer(posbus_adres + 0x38) & 0x80000000u)
        if (Klok_COUNT() - Loop > FREQUENCY) return 0;
    masjien_registreer(posbus_adres + 0x20) = 요청;
    for (;;) {
        if (!(masjien_registreer(posbus_adres + 0x18) & 0x40000000u)) {
            uint32_t antwoord = masjien_registreer(posbus_adres);
            if (antwoord == 요청) { 기억장벽(); return posbus_data[1] == 0x80000000u; }
        }
        if (Klok_COUNT() - Loop > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminaal_greep(unsigned);
extern int Terminaal_hangend(void);
extern void Terminaal_wyser(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../afstands_VALUE/afstands_VALUE.h"
static int 흐름목록;
static unsigned 직렬이전글자;
masjien_Word 보드흐름설정(masjien_Word 사용여부) { 흐름목록=사용여부!=0; return 0; }
masjien_Word bord_kanaal(masjien_Word kanaal, masjien_Word karakterkode) {
    if(흐름목록 && 자바셸출력((int32_t)kanaal,(int32_t)(karakterkode&255))) return 0;
    Terminaal_greep(karakterkode&255);
    원격출력(karakterkode&255);
    if ((karakterkode&255)==10 && 직렬이전글자!=13) {
        while (masjien_registreer(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        masjien_registreer(직렬장치)=13;
    }
    직렬이전글자=karakterkode&255;
    while (masjien_registreer(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    masjien_registreer(직렬장치) = (uint32_t)karakterkode & 255;
    return 0;
}
masjien_Word 보드글자쓰기(masjien_Word karakterkode) { return bord_kanaal(1,karakterkode); }
masjien_Word 보드원시글자읽기(void) {
    int afstands_karakter=원격입력();if(afstands_karakter>=0)return afstands_karakter;
    if (masjien_registreer(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = masjien_registreer(직렬장치);
    if (VALUE & 0xf00) { masjien_registreer(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
masjien_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char pakket_data[6];
    if(Terminaal_hangend())return (uint32_t)-4096;
    if(흐름목록){int32_t karakterkode=자바셸입력();if(karakterkode!=-3)return (uint32_t)karakterkode;}
    for(;;){
        int karakterkode=(int32_t)보드원시글자읽기();if(karakterkode<0)return (uint32_t)karakterkode;
        if(!꾸러미안쪽){if(karakterkode!=30)return karakterkode;꾸러미안쪽=1;사용량=0;continue;}
        pakket_data[사용량++]=karakterkode;if(사용량<6)continue;꾸러미안쪽=0;
        if(pakket_data[0]==1)Terminaal_wyser(pakket_data[1],pakket_data[2]+pakket_data[3]*256,pakket_data[4]+pakket_data[5]*256);
        if(pakket_data[0]==2)터미널바로가기키(pakket_data[1]);
        if(pakket_data[0]==3)터미널입력방식(pakket_data[1]);
        if(Terminaal_hangend())return (uint32_t)-4096;
    }
}
masjien_Word 보드밀리초(void) { return (uint32_t)(Klok_COUNT() / (FREQUENCY / 1000)); }
masjien_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *string_data) { while (*string_data) 보드글자쓰기((unsigned char)*string_data++); }
static void 직렬열여섯진출력(masjien_Word item_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int string_data = 60; string_data >= 0; string_data -= 4) 보드글자쓰기(열여섯진숫자[(item_COUNT >> string_data) & 15]); }
masjien_Word bord_Stop(masjien_Word stand_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(stand_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); bord_Stop(1); __builtin_unreachable(); }
void bord_uitsondering(masjien_Word uitsondering_stand, masjien_Word bevel_plaas, masjien_Word ongeldig_adres) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(uitsondering_stand);
    직렬글출력(" PC="); 직렬열여섯진출력(bevel_plaas); 직렬글출력(" FAR="); 직렬열여섯진출력(ongeldig_adres);
    bord_Stop(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    posbus_data[0]=32;posbus_data[1]=0;posbus_data[2]=0x10004;posbus_data[3]=8;posbus_data[4]=0;
    posbus_data[5]=posbus_data[6]=posbus_data[7]=0;
    return posbus()&&posbus_data[4]==0x80000008u&&(posbus_data[5]||posbus_data[6]);
}
int bord_masjien_adres(unsigned char *adres) {
    posbus_data[0]=32;posbus_data[1]=0;posbus_data[2]=0x10003;posbus_data[3]=8;posbus_data[4]=0;
    posbus_data[5]=posbus_data[6]=posbus_data[7]=0;
    if(!posbus()||(posbus_data[4]&0x80000000u)==0||(posbus_data[4]&0xffff)!=6)return 0;
    const unsigned char *data=(const unsigned char*)&posbus_data[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){adres[순번]=data[순번];SUM_VALUE|=data[순번];}return SUM_VALUE&&!(adres[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    masjien_registreer(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    masjien_registreer(범용입출력 + 4) = (masjien_registreer(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    masjien_registreer(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. faling_VALUE 시 config.txt의 48MHz를 사용한다.
    posbus_data[0] = 36; posbus_data[1] = 0; posbus_data[2] = 0x38002; posbus_data[3] = 12;
    posbus_data[4] = 0; posbus_data[5] = 2; posbus_data[6] = 48000000; posbus_data[7] = 0; posbus_data[8] = 0;
    int 시계정상 = posbus();
    uint32_t 속도 = 시계정상 && posbus_data[6] >= 1843200 ? posbus_data[6] : 48000000;
    posbus_data[0]=32; posbus_data[1]=0; posbus_data[2]=0x10005; posbus_data[3]=8; posbus_data[4]=0;
    posbus_data[5]=posbus_data[6]=posbus_data[7]=0;
    if (posbus() && posbus_data[4]==0x80000008u) 팔기억킬로바이트=posbus_data[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    masjien_registreer(직렬장치 + 0x44) = 0x7ff;
    masjien_registreer(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    masjien_registreer(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    masjien_registreer(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    masjien_registreer(직렬장치 + 0x38) = 0;
    masjien_registreer(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
masjien_Word bord_FTP(masjien_Word Aksie) { return (uint32_t)ftp_control((int)Aksie); }
masjien_Word bord_Netwerk_stand(masjien_Word inskrywing_VALUE, masjien_Word INDEX) { return 망상태읽기(inskrywing_VALUE, INDEX); }
masjien_Word bord_Netwerk_Instellings(masjien_Word Aksie, masjien_Word adres, masjien_Word masker_VALUE, masjien_Word deurgang_VALUE) { return (uint32_t)konfigureer_Netwerk(Aksie, adres, masker_VALUE, deurgang_VALUE); }
masjien_Word 보드응답보내기(masjien_Word adres, masjien_Word volgorde_VALUE) { return (uint32_t)응답시험시작(adres, volgorde_VALUE); }
masjien_Word 보드응답읽기(masjien_Word inskrywing_VALUE) { return (uint32_t)응답시험읽기(inskrywing_VALUE); }
masjien_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) sluit_Netwerk(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) bord_gebruikersbeheer(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (masjien_registreer(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    masjien_registreer(0xfe100020ul)=0x5a000000u | (masjien_registreer(0xfe100020ul)&~0xfffu) | 0x555;
    masjien_registreer(0xfe100024ul)=0x5a000000u | 10;
    masjien_registreer(0xfe10001cul)=0x5a000000u | (masjien_registreer(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

masjien_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t navraag_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(navraag_VALUE)/4; 순번++) posbus_data[순번] = navraag_VALUE[순번];
    if (posbus() && posbus_data[4] == 0x80000008u &&
        posbus_data[5] >= 640 && posbus_data[5] <= 1920 &&
        posbus_data[6] >= 480 && posbus_data[6] <= 1080) {
        요청너비 = posbus_data[5]; 요청높이 = posbus_data[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) posbus_data[순번] = 요청[순번];
    // 위 메시지의 werklik_data 길이를 사용: 태그 추가 시 lengte_VALUE 불일치를 방지한다.
    posbus_data[0] = sizeof(요청);
    if (!posbus()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (posbus_data[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t muur_VALUE = posbus_data[28] & 0x3fffffffu;
    uint32_t Grootte = posbus_data[29];
    uint32_t 받은너비 = posbus_data[5], 받은높이 = posbus_data[6], RECEIVED_reëlspasiëring = posbus_data[33];
    if (posbus_data[15] != 32 || posbus_data[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        posbus_data[10] < 받은너비 || posbus_data[11] < 받은높이 || posbus_data[23] || posbus_data[24] ||
        !muur_VALUE || muur_VALUE < 0x1000000 || (muur_VALUE & 3) || RECEIVED_reëlspasiëring < 받은너비 * 4 || (RECEIVED_reëlspasiëring & 3) ||
        (uint64_t)RECEIVED_reëlspasiëring * 받은높이 > Grootte || (uint64_t)muur_VALUE + Grootte > 0x40000000u)
        return 0;
    bord_Maak_gereed_tekening((volatile uint32_t *)(uintptr_t)muur_VALUE, 받은너비, 받은높이, RECEIVED_reëlspasiëring);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 draad_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Konteks;
static Konteks 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void Konteks_SWITCH(Konteks *, Konteks *);
extern void 자바작업(int32_t);
masjien_Word bord_YIELD(void) {
    network_poll();
    int 이전 = 현재작업, Volgende_item = (이전 + 1) % 3;
    while (Volgende_item != 이전 && !실행중[Volgende_item]) Volgende_item = (Volgende_item + 1) % 3;
    if (Volgende_item != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = Volgende_item;
        Konteks_SWITCH(&작업문맥들[이전], &작업문맥들[Volgende_item]);
    }
    return 0;
}
static void taak_selflaai(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    bord_YIELD();
    커널중단("finished task resumed");
}
masjien_Word bord_taak_Skep(masjien_Word waarde_VALUE) {
    if (waarde_VALUE < 1 || waarde_VALUE > 2 || 실행중[waarde_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[waarde_VALUE], 0, sizeof(Konteks));
    *(uint64_t *)쌓임공간들[waarde_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[waarde_VALUE].저장값[11] = (uintptr_t)taak_selflaai;
    작업문맥들[waarde_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[waarde_VALUE - 1] + sizeof(쌓임공간들[0]));
    실행중[waarde_VALUE] = 1;
    return 0;
}
masjien_Word bord_taak_stand(masjien_Word waarde_VALUE) { return waarde_VALUE < 3 ? 실행중[waarde_VALUE] : (uint32_t)-1; }
extern masjien_Word 미리번역기억조회(masjien_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
masjien_Word bord_navraag_stelsel(masjien_Word inskrywing_VALUE, masjien_Word INDEX) {
    if (inskrywing_VALUE==0) return 팔기억킬로바이트;
    if (inskrywing_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (inskrywing_VALUE==2 || inskrywing_VALUE==3) return 미리번역기억조회(inskrywing_VALUE==3);
    if (inskrywing_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (inskrywing_VALUE==5) return 80*1024; /* uitvoer_bevel 공간 16 MiB + 네 세션 보관 공간. */
    if (inskrywing_VALUE>=20) return 사용자상태읽기(inskrywing_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
