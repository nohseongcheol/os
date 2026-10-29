#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "kaiwhakamahi.h"
#include "../whatunga_Huinga/whatunga_Huinga.h"
typedef uintptr_t mīhini_Word;
#define mīhini_rēhita(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define pouaka_mēra_ADDRESS 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Karaka_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t pouaka_mēra_raraunga[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *raraunga_tūranga, int waehere_pūāhua, size_t tuemi_COUNT) { unsigned char *Panuku_OFFSET = raraunga_tūranga; while (tuemi_COUNT--) *Panuku_OFFSET++ = waehere_pūāhua; return raraunga_tūranga; }
void *memcpy(void *ūnga_raraunga, const void *aho_raraunga, size_t tuemi_COUNT) { unsigned char *첫째값 = ūnga_raraunga; const unsigned char *SECOND_uara = aho_raraunga; while (tuemi_COUNT--) *첫째값++ = *SECOND_uara++; return ūnga_raraunga; }

static int pouaka_mēra(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)pouaka_mēra_raraunga | 8;
    uint64_t whakahaere = Karaka_COUNT();
    기억장벽();
    while (mīhini_rēhita(pouaka_mēra_ADDRESS + 0x38) & 0x80000000u)
        if (Karaka_COUNT() - whakahaere > FREQUENCY) return 0;
    mīhini_rēhita(pouaka_mēra_ADDRESS + 0x20) = 요청;
    for (;;) {
        if (!(mīhini_rēhita(pouaka_mēra_ADDRESS + 0x18) & 0x40000000u)) {
            uint32_t whakautu = mīhini_rēhita(pouaka_mēra_ADDRESS);
            if (whakautu == 요청) { 기억장벽(); return pouaka_mēra_raraunga[1] == 0x80000000u; }
        }
        if (Karaka_COUNT() - whakahaere > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Tauranga_paita(unsigned);
extern int Tauranga_tārewa(void);
extern void Tauranga_atatohu(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../mamao_uara/mamao_uara.h"
static int 흐름목록;
static unsigned 직렬이전글자;
mīhini_Word 보드흐름설정(mīhini_Word 사용여부) { 흐름목록=사용여부!=0; return 0; }
mīhini_Word papa_hongere(mīhini_Word hongere, mīhini_Word waehere_pūāhua) {
    if(흐름목록 && 자바셸출력((int32_t)hongere,(int32_t)(waehere_pūāhua&255))) return 0;
    Tauranga_paita(waehere_pūāhua&255);
    원격출력(waehere_pūāhua&255);
    if ((waehere_pūāhua&255)==10 && 직렬이전글자!=13) {
        while (mīhini_rēhita(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        mīhini_rēhita(직렬장치)=13;
    }
    직렬이전글자=waehere_pūāhua&255;
    while (mīhini_rēhita(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    mīhini_rēhita(직렬장치) = (uint32_t)waehere_pūāhua & 255;
    return 0;
}
mīhini_Word 보드글자쓰기(mīhini_Word waehere_pūāhua) { return papa_hongere(1,waehere_pūāhua); }
mīhini_Word 보드원시글자읽기(void) {
    int mamao_pūāhua=원격입력();if(mamao_pūāhua>=0)return mamao_pūāhua;
    if (mīhini_rēhita(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t uara = mīhini_rēhita(직렬장치);
    if (uara & 0xf00) { mīhini_rēhita(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return uara & 255;
}
mīhini_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char pākete_raraunga[6];
    if(Tauranga_tārewa())return (uint32_t)-4096;
    if(흐름목록){int32_t waehere_pūāhua=자바셸입력();if(waehere_pūāhua!=-3)return (uint32_t)waehere_pūāhua;}
    for(;;){
        int waehere_pūāhua=(int32_t)보드원시글자읽기();if(waehere_pūāhua<0)return (uint32_t)waehere_pūāhua;
        if(!꾸러미안쪽){if(waehere_pūāhua!=30)return waehere_pūāhua;꾸러미안쪽=1;사용량=0;continue;}
        pākete_raraunga[사용량++]=waehere_pūāhua;if(사용량<6)continue;꾸러미안쪽=0;
        if(pākete_raraunga[0]==1)Tauranga_atatohu(pākete_raraunga[1],pākete_raraunga[2]+pākete_raraunga[3]*256,pākete_raraunga[4]+pākete_raraunga[5]*256);
        if(pākete_raraunga[0]==2)터미널바로가기키(pākete_raraunga[1]);
        if(pākete_raraunga[0]==3)터미널입력방식(pākete_raraunga[1]);
        if(Tauranga_tārewa())return (uint32_t)-4096;
    }
}
mīhini_Word 보드밀리초(void) { return (uint32_t)(Karaka_COUNT() / (FREQUENCY / 1000)); }
mīhini_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *aho_raraunga) { while (*aho_raraunga) 보드글자쓰기((unsigned char)*aho_raraunga++); }
static void 직렬열여섯진출력(mīhini_Word tuemi_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int aho_raraunga = 60; aho_raraunga >= 0; aho_raraunga -= 4) 보드글자쓰기(열여섯진숫자[(tuemi_COUNT >> aho_raraunga) & 15]); }
mīhini_Word papa_tāpu(mīhini_Word tūnga_uara) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(tūnga_uara); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); papa_tāpu(1); __builtin_unreachable(); }
void 보드예외(mīhini_Word 예외상태, mīhini_Word tono_tūranga, mīhini_Word muhu_ADDRESS) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(예외상태);
    직렬글출력(" PC="); 직렬열여섯진출력(tono_tūranga); 직렬글출력(" FAR="); 직렬열여섯진출력(muhu_ADDRESS);
    papa_tāpu(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    pouaka_mēra_raraunga[0]=32;pouaka_mēra_raraunga[1]=0;pouaka_mēra_raraunga[2]=0x10004;pouaka_mēra_raraunga[3]=8;pouaka_mēra_raraunga[4]=0;
    pouaka_mēra_raraunga[5]=pouaka_mēra_raraunga[6]=pouaka_mēra_raraunga[7]=0;
    return pouaka_mēra()&&pouaka_mēra_raraunga[4]==0x80000008u&&(pouaka_mēra_raraunga[5]||pouaka_mēra_raraunga[6]);
}
int papa_mīhini_ADDRESS(unsigned char *ADDRESS) {
    pouaka_mēra_raraunga[0]=32;pouaka_mēra_raraunga[1]=0;pouaka_mēra_raraunga[2]=0x10003;pouaka_mēra_raraunga[3]=8;pouaka_mēra_raraunga[4]=0;
    pouaka_mēra_raraunga[5]=pouaka_mēra_raraunga[6]=pouaka_mēra_raraunga[7]=0;
    if(!pouaka_mēra()||(pouaka_mēra_raraunga[4]&0x80000000u)==0||(pouaka_mēra_raraunga[4]&0xffff)!=6)return 0;
    const unsigned char *raraunga=(const unsigned char*)&pouaka_mēra_raraunga[5];unsigned SUM_uara=0;
    for(unsigned 순번=0;순번<6;순번++){ADDRESS[순번]=raraunga[순번];SUM_uara|=raraunga[순번];}return SUM_uara&&!(ADDRESS[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    mīhini_rēhita(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    mīhini_rēhita(범용입출력 + 4) = (mīhini_rēhita(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    mīhini_rēhita(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. rahunga_uara 시 config.txt의 48MHz를 사용한다.
    pouaka_mēra_raraunga[0] = 36; pouaka_mēra_raraunga[1] = 0; pouaka_mēra_raraunga[2] = 0x38002; pouaka_mēra_raraunga[3] = 12;
    pouaka_mēra_raraunga[4] = 0; pouaka_mēra_raraunga[5] = 2; pouaka_mēra_raraunga[6] = 48000000; pouaka_mēra_raraunga[7] = 0; pouaka_mēra_raraunga[8] = 0;
    int 시계정상 = pouaka_mēra();
    uint32_t 속도 = 시계정상 && pouaka_mēra_raraunga[6] >= 1843200 ? pouaka_mēra_raraunga[6] : 48000000;
    pouaka_mēra_raraunga[0]=32; pouaka_mēra_raraunga[1]=0; pouaka_mēra_raraunga[2]=0x10005; pouaka_mēra_raraunga[3]=8; pouaka_mēra_raraunga[4]=0;
    pouaka_mēra_raraunga[5]=pouaka_mēra_raraunga[6]=pouaka_mēra_raraunga[7]=0;
    if (pouaka_mēra() && pouaka_mēra_raraunga[4]==0x80000008u) 팔기억킬로바이트=pouaka_mēra_raraunga[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    mīhini_rēhita(직렬장치 + 0x44) = 0x7ff;
    mīhini_rēhita(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    mīhini_rēhita(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    mīhini_rēhita(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    mīhini_rēhita(직렬장치 + 0x38) = 0;
    mīhini_rēhita(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
mīhini_Word papa_FTP(mīhini_Word hohenga) { return (uint32_t)ftp_control((int)hohenga); }
mīhini_Word papa_whatunga_tūnga(mīhini_Word tāurunga_uara, mīhini_Word INDEX) { return 망상태읽기(tāurunga_uara, INDEX); }
mīhini_Word papa_whatunga_Ngā_Tautuhinga(mīhini_Word hohenga, mīhini_Word ADDRESS, mīhini_Word hīpoki_uara, mīhini_Word waharoa_uara) { return (uint32_t)whirihora_whatunga(hohenga, ADDRESS, hīpoki_uara, waharoa_uara); }
mīhini_Word 보드응답보내기(mīhini_Word ADDRESS, mīhini_Word whakaraupapa_uara) { return (uint32_t)응답시험시작(ADDRESS, whakaraupapa_uara); }
mīhini_Word 보드응답읽기(mīhini_Word tāurunga_uara) { return (uint32_t)응답시험읽기(tāurunga_uara); }
mīhini_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) kati_whatunga(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) papa_mana_kaiwhakamahi(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (mīhini_rēhita(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    mīhini_rēhita(0xfe100020ul)=0x5a000000u | (mīhini_rēhita(0xfe100020ul)&~0xfffu) | 0x555;
    mīhini_rēhita(0xfe100024ul)=0x5a000000u | 10;
    mīhini_rēhita(0xfe10001cul)=0x5a000000u | (mīhini_rēhita(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

mīhini_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t uiui_uara[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(uiui_uara)/4; 순번++) pouaka_mēra_raraunga[순번] = uiui_uara[순번];
    if (pouaka_mēra() && pouaka_mēra_raraunga[4] == 0x80000008u &&
        pouaka_mēra_raraunga[5] >= 640 && pouaka_mēra_raraunga[5] <= 1920 &&
        pouaka_mēra_raraunga[6] >= 480 && pouaka_mēra_raraunga[6] <= 1080) {
        요청너비 = pouaka_mēra_raraunga[5]; 요청높이 = pouaka_mēra_raraunga[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) pouaka_mēra_raraunga[순번] = 요청[순번];
    // 위 메시지의 tūturu_raraunga 길이를 사용: 태그 추가 시 roa_uara 불일치를 방지한다.
    pouaka_mēra_raraunga[0] = sizeof(요청);
    if (!pouaka_mēra()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (pouaka_mēra_raraunga[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Papamuri_uara = pouaka_mēra_raraunga[28] & 0x3fffffffu;
    uint32_t rahi = pouaka_mēra_raraunga[29];
    uint32_t 받은너비 = pouaka_mēra_raraunga[5], 받은높이 = pouaka_mēra_raraunga[6], RECEIVED_mokowā_raina = pouaka_mēra_raraunga[33];
    if (pouaka_mēra_raraunga[15] != 32 || pouaka_mēra_raraunga[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        pouaka_mēra_raraunga[10] < 받은너비 || pouaka_mēra_raraunga[11] < 받은높이 || pouaka_mēra_raraunga[23] || pouaka_mēra_raraunga[24] ||
        !Papamuri_uara || Papamuri_uara < 0x1000000 || (Papamuri_uara & 3) || RECEIVED_mokowā_raina < 받은너비 * 4 || (RECEIVED_mokowā_raina & 3) ||
        (uint64_t)RECEIVED_mokowā_raina * 받은높이 > rahi || (uint64_t)Papamuri_uara + rahi > 0x40000000u)
        return 0;
    papa_Whakarite_tātuhi((volatile uint32_t *)(uintptr_t)Papamuri_uara, 받은너비, 받은높이, RECEIVED_mokowā_raina);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 miro_uara. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Horopaki;
static Horopaki 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void Horopaki_SWITCH(Horopaki *, Horopaki *);
extern void 자바작업(int32_t);
mīhini_Word papa_YIELD(void) {
    network_poll();
    int 이전 = 현재작업, Panuku_tuemi = (이전 + 1) % 3;
    while (Panuku_tuemi != 이전 && !실행중[Panuku_tuemi]) Panuku_tuemi = (Panuku_tuemi + 1) % 3;
    if (Panuku_tuemi != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = Panuku_tuemi;
        Horopaki_SWITCH(&작업문맥들[이전], &작업문맥들[Panuku_tuemi]);
    }
    return 0;
}
static void tūmahi_whakaara(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    papa_YIELD();
    커널중단("finished task resumed");
}
mīhini_Word papa_tūmahi_Waihanga(mīhini_Word pūtāutu_uara) {
    if (pūtāutu_uara < 1 || pūtāutu_uara > 2 || 실행중[pūtāutu_uara]) return (uint32_t)-1;
    memset(&작업문맥들[pūtāutu_uara], 0, sizeof(Horopaki));
    *(uint64_t *)쌓임공간들[pūtāutu_uara - 1] = 0x6b6f726f7373746bull;
    작업문맥들[pūtāutu_uara].저장값[11] = (uintptr_t)tūmahi_whakaara;
    작업문맥들[pūtāutu_uara].저장값[12] = (uintptr_t)(쌓임공간들[pūtāutu_uara - 1] + sizeof(쌓임공간들[0]));
    실행중[pūtāutu_uara] = 1;
    return 0;
}
mīhini_Word papa_tūmahi_tūnga(mīhini_Word pūtāutu_uara) { return pūtāutu_uara < 3 ? 실행중[pūtāutu_uara] : (uint32_t)-1; }
extern mīhini_Word 미리번역기억조회(mīhini_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
mīhini_Word papa_uiui_pūnaha(mīhini_Word tāurunga_uara, mīhini_Word INDEX) {
    if (tāurunga_uara==0) return 팔기억킬로바이트;
    if (tāurunga_uara==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (tāurunga_uara==2 || tāurunga_uara==3) return 미리번역기억조회(tāurunga_uara==3);
    if (tāurunga_uara==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (tāurunga_uara==5) return 80*1024; /* kawe_tono 공간 16 MiB + 네 세션 보관 공간. */
    if (tāurunga_uara>=20) return 사용자상태읽기(tāurunga_uara-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
