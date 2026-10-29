#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "erabiltzaile.h"
#include "../sare_pila/sare_pila.h"
typedef uintptr_t gailu_Word;
#define gailu_izena_eman(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define postontzi_helbide 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t erloju_ZENBATU(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t MAIZTASUNA;
static volatile uint32_t postontzi_datuak[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *datuak_kargu, int karaktere_kode, size_t elementu_ZENBATU) { unsigned char *Hurrengoa_Geruzak = datuak_kargu; while (elementu_ZENBATU--) *Hurrengoa_Geruzak++ = karaktere_kode; return datuak_kargu; }
void *memcpy(void *helburu_datuak, const void *kate_datuak, size_t elementu_ZENBATU) { unsigned char *첫째값 = helburu_datuak; const unsigned char *SEGUNDOA_balio = kate_datuak; while (elementu_ZENBATU--) *첫째값++ = *SEGUNDOA_balio++; return helburu_datuak; }

static int postontzi(void) {
    uint32_t eskaera = (uint32_t)(uintptr_t)postontzi_datuak | 8;
    uint64_t Exekutatu_2 = erloju_ZENBATU();
    기억장벽();
    while (gailu_izena_eman(postontzi_helbide + 0x38) & 0x80000000u)
        if (erloju_ZENBATU() - Exekutatu_2 > MAIZTASUNA) return 0;
    gailu_izena_eman(postontzi_helbide + 0x20) = eskaera;
    for (;;) {
        if (!(gailu_izena_eman(postontzi_helbide + 0x18) & 0x40000000u)) {
            uint32_t erantzun = gailu_izena_eman(postontzi_helbide);
            if (erantzun == eskaera) { 기억장벽(); return postontzi_datuak[1] == 0x80000000u; }
        }
        if (erloju_ZENBATU() - Exekutatu_2 > MAIZTASUNA) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_byte(unsigned);
extern int Terminal_zain(void);
extern void Terminal_erakusle(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../urruneko_balio/urruneko_balio.h"
static int Korronteak;
static unsigned 직렬이전글자;
gailu_Word arbel_Korronteak(gailu_Word 사용여부) { Korronteak=사용여부!=0; return 0; }
gailu_Word arbel_kanal(gailu_Word kanal, gailu_Word karaktere_kode) {
    if(Korronteak && 자바셸출력((int32_t)kanal,(int32_t)(karaktere_kode&255))) return 0;
    Terminal_byte(karaktere_kode&255);
    원격출력(karaktere_kode&255);
    if ((karaktere_kode&255)==10 && 직렬이전글자!=13) {
        while (gailu_izena_eman(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        gailu_izena_eman(직렬장치)=13;
    }
    직렬이전글자=karaktere_kode&255;
    while (gailu_izena_eman(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    gailu_izena_eman(직렬장치) = (uint32_t)karaktere_kode & 255;
    return 0;
}
gailu_Word 보드글자쓰기(gailu_Word karaktere_kode) { return arbel_kanal(1,karaktere_kode); }
gailu_Word 보드원시글자읽기(void) {
    int urruneko_karaktere=원격입력();if(urruneko_karaktere>=0)return urruneko_karaktere;
    if (gailu_izena_eman(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t balio = gailu_izena_eman(직렬장치);
    if (balio & 0xf00) { gailu_izena_eman(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return balio & 255;
}
gailu_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char pakete_datuak[6];
    if(Terminal_zain())return (uint32_t)-4096;
    if(Korronteak){int32_t karaktere_kode=자바셸입력();if(karaktere_kode!=-3)return (uint32_t)karaktere_kode;}
    for(;;){
        int karaktere_kode=(int32_t)보드원시글자읽기();if(karaktere_kode<0)return (uint32_t)karaktere_kode;
        if(!꾸러미안쪽){if(karaktere_kode!=30)return karaktere_kode;꾸러미안쪽=1;사용량=0;continue;}
        pakete_datuak[사용량++]=karaktere_kode;if(사용량<6)continue;꾸러미안쪽=0;
        if(pakete_datuak[0]==1)Terminal_erakusle(pakete_datuak[1],pakete_datuak[2]+pakete_datuak[3]*256,pakete_datuak[4]+pakete_datuak[5]*256);
        if(pakete_datuak[0]==2)터미널바로가기키(pakete_datuak[1]);
        if(pakete_datuak[0]==3)터미널입력방식(pakete_datuak[1]);
        if(Terminal_zain())return (uint32_t)-4096;
    }
}
gailu_Word 보드밀리초(void) { return (uint32_t)(erloju_ZENBATU() / (MAIZTASUNA / 1000)); }
gailu_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *kate_datuak) { while (*kate_datuak) 보드글자쓰기((unsigned char)*kate_datuak++); }
static void 직렬열여섯진출력(gailu_Word elementu_ZENBATU) { const char *열여섯진숫자 = "0123456789abcdef"; for (int kate_datuak = 60; kate_datuak >= 0; kate_datuak -= 4) 보드글자쓰기(열여섯진숫자[(elementu_ZENBATU >> kate_datuak) & 15]); }
gailu_Word arbel_Stop(gailu_Word Egoera_balio) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Egoera_balio); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); arbel_Stop(1); __builtin_unreachable(); }
void arbel_salbuespen(gailu_Word salbuespen_Egoera, gailu_Word komando_kargu, gailu_Word baliogabe_helbide) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(salbuespen_Egoera);
    직렬글출력(" PC="); 직렬열여섯진출력(komando_kargu); 직렬글출력(" FAR="); 직렬열여섯진출력(baliogabe_helbide);
    arbel_Stop(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    postontzi_datuak[0]=32;postontzi_datuak[1]=0;postontzi_datuak[2]=0x10004;postontzi_datuak[3]=8;postontzi_datuak[4]=0;
    postontzi_datuak[5]=postontzi_datuak[6]=postontzi_datuak[7]=0;
    return postontzi()&&postontzi_datuak[4]==0x80000008u&&(postontzi_datuak[5]||postontzi_datuak[6]);
}
int arbel_gailu_helbide(unsigned char *helbide) {
    postontzi_datuak[0]=32;postontzi_datuak[1]=0;postontzi_datuak[2]=0x10003;postontzi_datuak[3]=8;postontzi_datuak[4]=0;
    postontzi_datuak[5]=postontzi_datuak[6]=postontzi_datuak[7]=0;
    if(!postontzi()||(postontzi_datuak[4]&0x80000000u)==0||(postontzi_datuak[4]&0xffff)!=6)return 0;
    const unsigned char *datuak=(const unsigned char*)&postontzi_datuak[5];unsigned BATU_balio=0;
    for(unsigned 순번=0;순번<6;순번++){helbide[순번]=datuak[순번];BATU_balio|=datuak[순번];}return BATU_balio&&!(helbide[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(MAIZTASUNA));
    gailu_izena_eman(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    gailu_izena_eman(범용입출력 + 4) = (gailu_izena_eman(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    gailu_izena_eman(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. hutsegite_balio 시 config.txt의 48MHz를 사용한다.
    postontzi_datuak[0] = 36; postontzi_datuak[1] = 0; postontzi_datuak[2] = 0x38002; postontzi_datuak[3] = 12;
    postontzi_datuak[4] = 0; postontzi_datuak[5] = 2; postontzi_datuak[6] = 48000000; postontzi_datuak[7] = 0; postontzi_datuak[8] = 0;
    int 시계정상 = postontzi();
    uint32_t 속도 = 시계정상 && postontzi_datuak[6] >= 1843200 ? postontzi_datuak[6] : 48000000;
    postontzi_datuak[0]=32; postontzi_datuak[1]=0; postontzi_datuak[2]=0x10005; postontzi_datuak[3]=8; postontzi_datuak[4]=0;
    postontzi_datuak[5]=postontzi_datuak[6]=postontzi_datuak[7]=0;
    if (postontzi() && postontzi_datuak[4]==0x80000008u) 팔기억킬로바이트=postontzi_datuak[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    gailu_izena_eman(직렬장치 + 0x44) = 0x7ff;
    gailu_izena_eman(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    gailu_izena_eman(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    gailu_izena_eman(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    gailu_izena_eman(직렬장치 + 0x38) = 0;
    gailu_izena_eman(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
gailu_Word arbel_FTP(gailu_Word Ekintza) { return (uint32_t)ftp_control((int)Ekintza); }
gailu_Word arbel_sare_egoera(gailu_Word sarrera_balio, gailu_Word INDIZE) { return 망상태읽기(sarrera_balio, INDIZE); }
gailu_Word arbel_sare_Ezarpenak(gailu_Word Ekintza, gailu_Word helbide, gailu_Word maskara_balio, gailu_Word atebide_balio) { return (uint32_t)konfiguratu_sare(Ekintza, helbide, maskara_balio, atebide_balio); }
gailu_Word arbel_bidali_erantzun(gailu_Word helbide, gailu_Word ordena_balio) { return (uint32_t)응답시험시작(helbide, ordena_balio); }
gailu_Word 보드응답읽기(gailu_Word sarrera_balio) { return (uint32_t)응답시험읽기(sarrera_balio); }
gailu_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDIZE=0; INDIZE<32; INDIZE++) itxi_sare(INDIZE);
    for (unsigned INDIZE=0; INDIZE<4; INDIZE++) arbel_erabiltzaile_kontrola(32+INDIZE);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (gailu_izena_eman(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    gailu_izena_eman(0xfe100020ul)=0x5a000000u | (gailu_izena_eman(0xfe100020ul)&~0xfffu) | 0x555;
    gailu_izena_eman(0xfe100024ul)=0x5a000000u | 10;
    gailu_izena_eman(0xfe10001cul)=0x5a000000u | (gailu_izena_eman(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

gailu_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t kontsulta_balio[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(kontsulta_balio)/4; 순번++) postontzi_datuak[순번] = kontsulta_balio[순번];
    if (postontzi() && postontzi_datuak[4] == 0x80000008u &&
        postontzi_datuak[5] >= 640 && postontzi_datuak[5] <= 1920 &&
        postontzi_datuak[6] >= 480 && postontzi_datuak[6] <= 1080) {
        요청너비 = postontzi_datuak[5]; 요청높이 = postontzi_datuak[6];
    }
    const uint32_t eskaera[] = {
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
    for (size_t 순번 = 0; 순번 < sizeof(eskaera)/4; 순번++) postontzi_datuak[순번] = eskaera[순번];
    // 위 메시지의 benetako_datuak 길이를 사용: 태그 Erantsi_sarrera 시 luzera_balio 불일치를 방지한다.
    postontzi_datuak[0] = sizeof(eskaera);
    if (!postontzi()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned erantzun_luzera[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (postontzi_datuak[응답들[순번]] != (0x80000000u | erantzun_luzera[순번])) return 0;
    uint32_t horma_paper_balio = postontzi_datuak[28] & 0x3fffffffu;
    uint32_t Tamaina = postontzi_datuak[29];
    uint32_t 받은너비 = postontzi_datuak[5], 받은높이 = postontzi_datuak[6], RECEIVED_lerroarte = postontzi_datuak[33];
    if (postontzi_datuak[15] != 32 || postontzi_datuak[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        postontzi_datuak[10] < 받은너비 || postontzi_datuak[11] < 받은높이 || postontzi_datuak[23] || postontzi_datuak[24] ||
        !horma_paper_balio || horma_paper_balio < 0x1000000 || (horma_paper_balio & 3) || RECEIVED_lerroarte < 받은너비 * 4 || (RECEIVED_lerroarte & 3) ||
        (uint64_t)RECEIVED_lerroarte * 받은높이 > Tamaina || (uint64_t)horma_paper_balio + Tamaina > 0x40000000u)
        return 0;
    보드그림준비((volatile uint32_t *)(uintptr_t)horma_paper_balio, 받은너비, 받은높이, RECEIVED_lerroarte);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 hari_balio. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } 작업문맥;
static 작업문맥 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int informatika_Korrika_egitea[3] = {1, 0, 0};
static int 현재작업;
extern void 작업문맥바꾸기(작업문맥 *, 작업문맥 *);
extern void 자바작업(int32_t);
gailu_Word arbel_YIELD(void) {
    network_poll();
    int 이전 = 현재작업, Hurrengoa_elementu = (이전 + 1) % 3;
    while (Hurrengoa_elementu != 이전 && !informatika_Korrika_egitea[Hurrengoa_elementu]) Hurrengoa_elementu = (Hurrengoa_elementu + 1) % 3;
    if (Hurrengoa_elementu != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (informatika_Korrika_egitea[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = Hurrengoa_elementu;
        작업문맥바꾸기(&작업문맥들[이전], &작업문맥들[Hurrengoa_elementu]);
    }
    return 0;
}
static void ataza_abio(void) {
    자바작업(현재작업);
    informatika_Korrika_egitea[현재작업] = 0;
    arbel_YIELD();
    커널중단("finished task resumed");
}
gailu_Word arbel_ataza_sortu(gailu_Word identifikatzaile_balio) {
    if (identifikatzaile_balio < 1 || identifikatzaile_balio > 2 || informatika_Korrika_egitea[identifikatzaile_balio]) return (uint32_t)-1;
    memset(&작업문맥들[identifikatzaile_balio], 0, sizeof(작업문맥));
    *(uint64_t *)쌓임공간들[identifikatzaile_balio - 1] = 0x6b6f726f7373746bull;
    작업문맥들[identifikatzaile_balio].저장값[11] = (uintptr_t)ataza_abio;
    작업문맥들[identifikatzaile_balio].저장값[12] = (uintptr_t)(쌓임공간들[identifikatzaile_balio - 1] + sizeof(쌓임공간들[0]));
    informatika_Korrika_egitea[identifikatzaile_balio] = 1;
    return 0;
}
gailu_Word arbel_ataza_Egoera(gailu_Word identifikatzaile_balio) { return identifikatzaile_balio < 3 ? informatika_Korrika_egitea[identifikatzaile_balio] : (uint32_t)-1; }
extern gailu_Word 미리번역기억조회(gailu_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
gailu_Word arbel_kontsulta_sistema(gailu_Word sarrera_balio, gailu_Word INDIZE) {
    if (sarrera_balio==0) return 팔기억킬로바이트;
    if (sarrera_balio==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (sarrera_balio==2 || sarrera_balio==3) return 미리번역기억조회(sarrera_balio==3);
    if (sarrera_balio==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (sarrera_balio==5) return 80*1024; /* exekutatu_komando 공간 16 MiB + 네 세션 보관 공간. */
    if (sarrera_balio>=20) return 사용자상태읽기(sarrera_balio-20, INDIZE);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
