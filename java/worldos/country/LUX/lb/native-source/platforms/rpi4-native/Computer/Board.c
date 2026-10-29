#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "Benotzer.h"
#include "../Reseau_Stapel/Reseau_Stapel.h"
typedef uintptr_t Computer_Word;
#define Computer_registréieren(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define Postfach_Adress 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Auer_COUNT(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t FREQUENCY;
static volatile uint32_t Postfach_Daten[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *Daten_positionéieren, int Zeechecode, size_t Element_COUNT) { unsigned char *Weider_OFFSET = Daten_positionéieren; while (Element_COUNT--) *Weider_OFFSET++ = Zeechecode; return Daten_positionéieren; }
void *memcpy(void *Zil_Daten, const void *Zeechefolleg_Daten, size_t Element_COUNT) { unsigned char *첫째값 = Zil_Daten; const unsigned char *SECOND_VALUE = Zeechefolleg_Daten; while (Element_COUNT--) *첫째값++ = *SECOND_VALUE++; return Zil_Daten; }

static int Postfach(void) {
    uint32_t 요청 = (uint32_t)(uintptr_t)Postfach_Daten | 8;
    uint64_t Laf = Auer_COUNT();
    기억장벽();
    while (Computer_registréieren(Postfach_Adress + 0x38) & 0x80000000u)
        if (Auer_COUNT() - Laf > FREQUENCY) return 0;
    Computer_registréieren(Postfach_Adress + 0x20) = 요청;
    for (;;) {
        if (!(Computer_registréieren(Postfach_Adress + 0x18) & 0x40000000u)) {
            uint32_t äntweren = Computer_registréieren(Postfach_Adress);
            if (äntweren == 요청) { 기억장벽(); return Postfach_Daten[1] == 0x80000000u; }
        }
        if (Auer_COUNT() - Laf > FREQUENCY) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_Byte(unsigned);
extern int Terminal_ausstoend(void);
extern void Terminal_Uweiser(unsigned,int,int),터미널바로가기키(unsigned);
extern void 터미널입력방식(unsigned);
#include "../extern_VALUE/extern_VALUE.h"
static int 흐름목록;
static unsigned 직렬이전글자;
Computer_Word 보드흐름설정(Computer_Word 사용여부) { 흐름목록=사용여부!=0; return 0; }
Computer_Word Board_Kanal(Computer_Word Kanal, Computer_Word Zeechecode) {
    if(흐름목록 && 자바셸출력((int32_t)Kanal,(int32_t)(Zeechecode&255))) return 0;
    Terminal_Byte(Zeechecode&255);
    원격출력(Zeechecode&255);
    if ((Zeechecode&255)==10 && 직렬이전글자!=13) {
        while (Computer_registréieren(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        Computer_registréieren(직렬장치)=13;
    }
    직렬이전글자=Zeechecode&255;
    while (Computer_registréieren(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    Computer_registréieren(직렬장치) = (uint32_t)Zeechecode & 255;
    return 0;
}
Computer_Word 보드글자쓰기(Computer_Word Zeechecode) { return Board_Kanal(1,Zeechecode); }
Computer_Word 보드원시글자읽기(void) {
    int extern_Zeechen=원격입력();if(extern_Zeechen>=0)return extern_Zeechen;
    if (Computer_registréieren(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t VALUE = Computer_registréieren(직렬장치);
    if (VALUE & 0xf00) { Computer_registréieren(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return VALUE & 255;
}
Computer_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char Pak_Daten[6];
    if(Terminal_ausstoend())return (uint32_t)-4096;
    if(흐름목록){int32_t Zeechecode=자바셸입력();if(Zeechecode!=-3)return (uint32_t)Zeechecode;}
    for(;;){
        int Zeechecode=(int32_t)보드원시글자읽기();if(Zeechecode<0)return (uint32_t)Zeechecode;
        if(!꾸러미안쪽){if(Zeechecode!=30)return Zeechecode;꾸러미안쪽=1;사용량=0;continue;}
        Pak_Daten[사용량++]=Zeechecode;if(사용량<6)continue;꾸러미안쪽=0;
        if(Pak_Daten[0]==1)Terminal_Uweiser(Pak_Daten[1],Pak_Daten[2]+Pak_Daten[3]*256,Pak_Daten[4]+Pak_Daten[5]*256);
        if(Pak_Daten[0]==2)터미널바로가기키(Pak_Daten[1]);
        if(Pak_Daten[0]==3)터미널입력방식(Pak_Daten[1]);
        if(Terminal_ausstoend())return (uint32_t)-4096;
    }
}
Computer_Word 보드밀리초(void) { return (uint32_t)(Auer_COUNT() / (FREQUENCY / 1000)); }
Computer_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *Zeechefolleg_Daten) { while (*Zeechefolleg_Daten) 보드글자쓰기((unsigned char)*Zeechefolleg_Daten++); }
static void 직렬열여섯진출력(Computer_Word Element_COUNT) { const char *열여섯진숫자 = "0123456789abcdef"; for (int Zeechefolleg_Daten = 60; Zeechefolleg_Daten >= 0; Zeechefolleg_Daten -= 4) 보드글자쓰기(열여섯진숫자[(Element_COUNT >> Zeechefolleg_Daten) & 15]); }
Computer_Word Board_Stoppen(Computer_Word Status_VALUE) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Status_VALUE); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Board_Stoppen(1); __builtin_unreachable(); }
void 보드예외(Computer_Word 예외상태, Computer_Word Befeel_positionéieren, Computer_Word ongëlteg_Adress) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(예외상태);
    직렬글출력(" PC="); 직렬열여섯진출력(Befeel_positionéieren); 직렬글출력(" FAR="); 직렬열여섯진출력(ongëlteg_Adress);
    Board_Stoppen(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    Postfach_Daten[0]=32;Postfach_Daten[1]=0;Postfach_Daten[2]=0x10004;Postfach_Daten[3]=8;Postfach_Daten[4]=0;
    Postfach_Daten[5]=Postfach_Daten[6]=Postfach_Daten[7]=0;
    return Postfach()&&Postfach_Daten[4]==0x80000008u&&(Postfach_Daten[5]||Postfach_Daten[6]);
}
int Board_Computer_Adress(unsigned char *Adress) {
    Postfach_Daten[0]=32;Postfach_Daten[1]=0;Postfach_Daten[2]=0x10003;Postfach_Daten[3]=8;Postfach_Daten[4]=0;
    Postfach_Daten[5]=Postfach_Daten[6]=Postfach_Daten[7]=0;
    if(!Postfach()||(Postfach_Daten[4]&0x80000000u)==0||(Postfach_Daten[4]&0xffff)!=6)return 0;
    const unsigned char *Daten=(const unsigned char*)&Postfach_Daten[5];unsigned SUM_VALUE=0;
    for(unsigned 순번=0;순번<6;순번++){Adress[순번]=Daten[순번];SUM_VALUE|=Daten[순번];}return SUM_VALUE&&!(Adress[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Computer_registréieren(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    Computer_registréieren(범용입출력 + 4) = (Computer_registréieren(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    Computer_registréieren(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. Feeler_VALUE 시 config.txt의 48MHz를 사용한다.
    Postfach_Daten[0] = 36; Postfach_Daten[1] = 0; Postfach_Daten[2] = 0x38002; Postfach_Daten[3] = 12;
    Postfach_Daten[4] = 0; Postfach_Daten[5] = 2; Postfach_Daten[6] = 48000000; Postfach_Daten[7] = 0; Postfach_Daten[8] = 0;
    int 시계정상 = Postfach();
    uint32_t 속도 = 시계정상 && Postfach_Daten[6] >= 1843200 ? Postfach_Daten[6] : 48000000;
    Postfach_Daten[0]=32; Postfach_Daten[1]=0; Postfach_Daten[2]=0x10005; Postfach_Daten[3]=8; Postfach_Daten[4]=0;
    Postfach_Daten[5]=Postfach_Daten[6]=Postfach_Daten[7]=0;
    if (Postfach() && Postfach_Daten[4]==0x80000008u) 팔기억킬로바이트=Postfach_Daten[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    Computer_registréieren(직렬장치 + 0x44) = 0x7ff;
    Computer_registréieren(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    Computer_registréieren(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    Computer_registréieren(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    Computer_registréieren(직렬장치 + 0x38) = 0;
    Computer_registréieren(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
Computer_Word Board_FTP(Computer_Word Aktioun) { return (uint32_t)ftp_control((int)Aktioun); }
Computer_Word Board_Reseau_Status(Computer_Word Agab_VALUE, Computer_Word INDEX) { return 망상태읽기(Agab_VALUE, INDEX); }
Computer_Word Board_Reseau_Astellungen(Computer_Word Aktioun, Computer_Word Adress, Computer_Word Mask_VALUE, Computer_Word Gateway_VALUE) { return (uint32_t)konfiguréieren_Reseau(Aktioun, Adress, Mask_VALUE, Gateway_VALUE); }
Computer_Word 보드응답보내기(Computer_Word Adress, Computer_Word Reiefolleg_VALUE) { return (uint32_t)응답시험시작(Adress, Reiefolleg_VALUE); }
Computer_Word 보드응답읽기(Computer_Word Agab_VALUE) { return (uint32_t)응답시험읽기(Agab_VALUE); }
Computer_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned INDEX=0; INDEX<32; INDEX++) Clôture_Reseau(INDEX);
    for (unsigned INDEX=0; INDEX<4; INDEX++) Board_Benotzersteierelement(32+INDEX);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (Computer_registréieren(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    Computer_registréieren(0xfe100020ul)=0x5a000000u | (Computer_registréieren(0xfe100020ul)&~0xfffu) | 0x555;
    Computer_registréieren(0xfe100024ul)=0x5a000000u | 10;
    Computer_registréieren(0xfe10001cul)=0x5a000000u | (Computer_registréieren(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

Computer_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 현재 크기를 읽는다. */
    const uint32_t Requête_VALUE[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(Requête_VALUE)/4; 순번++) Postfach_Daten[순번] = Requête_VALUE[순번];
    if (Postfach() && Postfach_Daten[4] == 0x80000008u &&
        Postfach_Daten[5] >= 640 && Postfach_Daten[5] <= 1920 &&
        Postfach_Daten[6] >= 480 && Postfach_Daten[6] <= 1080) {
        요청너비 = Postfach_Daten[5]; 요청높이 = Postfach_Daten[6];
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
    for (size_t 순번 = 0; 순번 < sizeof(요청)/4; 순번++) Postfach_Daten[순번] = 요청[순번];
    // 위 메시지의 aktuell_Daten 길이를 사용: 태그 추가 시 Längt_VALUE 불일치를 방지한다.
    Postfach_Daten[0] = sizeof(요청);
    if (!Postfach()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 응답길이[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (Postfach_Daten[응답들[순번]] != (0x80000000u | 응답길이[순번])) return 0;
    uint32_t Hannergrond_VALUE = Postfach_Daten[28] & 0x3fffffffu;
    uint32_t d_Gréisst_veränneren = Postfach_Daten[29];
    uint32_t 받은너비 = Postfach_Daten[5], 받은높이 = Postfach_Daten[6], RECEIVED_Anzuch = Postfach_Daten[33];
    if (Postfach_Daten[15] != 32 || Postfach_Daten[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        Postfach_Daten[10] < 받은너비 || Postfach_Daten[11] < 받은높이 || Postfach_Daten[23] || Postfach_Daten[24] ||
        !Hannergrond_VALUE || Hannergrond_VALUE < 0x1000000 || (Hannergrond_VALUE & 3) || RECEIVED_Anzuch < 받은너비 * 4 || (RECEIVED_Anzuch & 3) ||
        (uint64_t)RECEIVED_Anzuch * 받은높이 > d_Gréisst_veränneren || (uint64_t)Hannergrond_VALUE + d_Gréisst_veränneren > 0x40000000u)
        return 0;
    Board_Préparéieren_Zeechnung((volatile uint32_t *)(uintptr_t)Hannergrond_VALUE, 받은너비, 받은높이, RECEIVED_Anzuch);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 Thread_VALUE. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Kontext;
static Kontext 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int 실행중[3] = {1, 0, 0};
static int 현재작업;
extern void Kontext_SWITCH(Kontext *, Kontext *);
extern void 자바작업(int32_t);
Computer_Word Board_YIELD(void) {
    network_poll();
    int 이전 = 현재작업, Weider_Element = (이전 + 1) % 3;
    while (Weider_Element != 이전 && !실행중[Weider_Element]) Weider_Element = (Weider_Element + 1) % 3;
    if (Weider_Element != 이전) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (실행중[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        현재작업 = Weider_Element;
        Kontext_SWITCH(&작업문맥들[이전], &작업문맥들[Weider_Element]);
    }
    return 0;
}
static void To_do_Start(void) {
    자바작업(현재작업);
    실행중[현재작업] = 0;
    Board_YIELD();
    커널중단("finished task resumed");
}
Computer_Word Board_To_do_Create(Computer_Word Identifikateur_VALUE) {
    if (Identifikateur_VALUE < 1 || Identifikateur_VALUE > 2 || 실행중[Identifikateur_VALUE]) return (uint32_t)-1;
    memset(&작업문맥들[Identifikateur_VALUE], 0, sizeof(Kontext));
    *(uint64_t *)쌓임공간들[Identifikateur_VALUE - 1] = 0x6b6f726f7373746bull;
    작업문맥들[Identifikateur_VALUE].저장값[11] = (uintptr_t)To_do_Start;
    작업문맥들[Identifikateur_VALUE].저장값[12] = (uintptr_t)(쌓임공간들[Identifikateur_VALUE - 1] + sizeof(쌓임공간들[0]));
    실행중[Identifikateur_VALUE] = 1;
    return 0;
}
Computer_Word Board_To_do_Status(Computer_Word Identifikateur_VALUE) { return Identifikateur_VALUE < 3 ? 실행중[Identifikateur_VALUE] : (uint32_t)-1; }
extern Computer_Word 미리번역기억조회(Computer_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
Computer_Word Board_Requête_System(Computer_Word Agab_VALUE, Computer_Word INDEX) {
    if (Agab_VALUE==0) return 팔기억킬로바이트;
    if (Agab_VALUE==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (Agab_VALUE==2 || Agab_VALUE==3) return 미리번역기억조회(Agab_VALUE==3);
    if (Agab_VALUE==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (Agab_VALUE==5) return 80*1024; /* ausféieren_Befeel 공간 16 MiB + 네 세션 보관 공간. */
    if (Agab_VALUE>=20) return 사용자상태읽기(Agab_VALUE-20, INDEX);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[현재작업]; }
