#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 ausféieren_Befeel Computer Layer_VALUE. Fichier Daten/정책은 기존 AOT Java 커널에 위임한다.
#include "Benotzer.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Reseau_Stapel/Reseau_Stapel.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define Computer_registréieren(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_Distributeur 0xff841000ul
#define IRQ_CPU_Interface 0xff842000ul
#define Säitegréisst 4096ul
#define Zougrëff_Markéierung (1ul << 10)
#define Neen_ausféieren_Geneemegung (1ul << 53)
#define Benotzer_Neen_ausféieren (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | Zougrëff_Markéierung)
#define Kernel_Säit (3ul | 보통기억 | Neen_ausféieren_Geneemegung | Benotzer_Neen_ausféieren)
#define Benotzer_lies_schreiffäeg (3ul | 보통기억 | (1ul << 6) | Neen_ausféieren_Geneemegung | Benotzer_Neen_ausféieren)
#define Benotzer_schreifgeschützt (3ul | 보통기억 | (3ul << 6) | Neen_ausféieren_Geneemegung | Benotzer_Neen_ausféieren)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | Neen_ausféieren_Geneemegung)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Board_Pel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Board_Terminal(uintptr_t);
extern int Terminal_ausstoend(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int Benotzer_CV(Benotzer_Rumm *,void *);
extern void 사용자실수보관(void *);
extern int Benotzer_aginn(uintptr_t Agab_Punkt, uintptr_t Stapel_Späicher, uintptr_t 전달값);
extern void 사용자복귀(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t Racinn_Adress[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t Säit_Lëscht[Benotzer_Säit_COUNT] __attribute__((aligned(4096)));
static uint8_t Autorisatiounen_Lëscht[Benotzer_Säit_COUNT];
static int aktiv, Fichier_Lëscht[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned Fichier_Handle){return Fichier_Handle<40?자바전문닫기(Fichier_Handle):자바흐름닫기(Fichier_Handle);}
static uint64_t FREQUENCY, 마감시각;
static uintptr_t 동적기억끝;
// Kernel_VALUE 셸이 준비한 UTF-8 인수. EL0에는 Instanz_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,interaktiv,리눅스규약,Fichier_Lëscht[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char Argument_ARRAY[8][256],Autorisatiounen_Lëscht[Benotzer_Säit_COUNT];
    uintptr_t 동적기억공간; Benotzer_Rumm 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int Besëtzer_Objet,interaktiv;
static uint32_t Benotzernummer[4], Benotzer_Start_TIME[4], 사용자누적시각[4], 사용자실행시각[4], Weider_Benotzernummer=10;
static unsigned char Benotzer_Befeel_Numm[4][288];
uint32_t 사용자상태읽기(unsigned Agab_VALUE, unsigned INDEX) {
    unsigned positionéieren_INDEX=INDEX&3;
    int Status_VALUE=(aktiv && Besëtzer_Objet==(int)positionéieren_INDEX) ? 1 : 저장값[positionéieren_INDEX].멈춤상태 ? 2 : 0;
    if (Agab_VALUE==0) return Status_VALUE;
    if (!Status_VALUE) return 0;
    if (Agab_VALUE==1) return Benotzernummer[positionéieren_INDEX];
    if (Agab_VALUE==2) {
        unsigned char *쪽들=Status_VALUE==1?Autorisatiounen_Lëscht:저장값[positionéieren_INDEX].Autorisatiounen_Lëscht;
        unsigned Säit_COUNT=0; for (unsigned 순번=0; 순번<Benotzer_Säit_COUNT; 순번++) if(쪽들[순번]) Säit_COUNT++;
        return Säit_COUNT*4;
    }
    if (Agab_VALUE==3) return (uint32_t)보드밀리초()-Benotzer_Start_TIME[positionéieren_INDEX];
    if (Agab_VALUE==4) return 사용자누적시각[positionéieren_INDEX]+(Status_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[positionéieren_INDEX]:0);
    if (Agab_VALUE==5) return INDEX/4<sizeof(Benotzer_Befeel_Numm[0])?Benotzer_Befeel_Numm[positionéieren_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t Agab_COUNT) {
    if (aktiv || Agab_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = Agab_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t 현재위치, uintptr_t Byte_Daten) {
    if (aktiv || LOOKUP_INDEX >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[LOOKUP_INDEX] || !Byte_Daten || Byte_Daten > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][현재위치] = Byte_Daten;
    전달인수길이[LOOKUP_INDEX] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Auer_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stoppen_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    Computer_registréieren(IRQ_Distributeur + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void Start_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, aschalten = 1;
    마감시각 = Auer_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(aschalten) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned Daten_blockéieren = 0; Daten_blockéieren < 4; Daten_blockéieren++) {
        Racinn_Adress[Daten_blockéieren] = (uintptr_t)가운데[Daten_blockéieren] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t Adress = ((uintptr_t)Daten_blockéieren << 30) | ((uintptr_t)순번 << 21);
            가운데[Daten_blockéieren][순번] = Adress | 1 | Zougrëff_Markéierung | Benotzer_Neen_ausféieren;
            if (Adress >= 0xfc000000ul) 가운데[Daten_blockéieren][순번] |= Neen_ausféieren_Geneemegung; // Device-nGnRnE
            else 가운데[Daten_blockéieren][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < Benotzer_Säit_COUNT / 512; SECOND_VALUE++)
        가운데[0][(Benotzer_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(Säit_Lëscht + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < Benotzer_Säit_COUNT; 순번++) Säit_Lëscht[순번] = (Benotzer_BASE + 순번 * Säitegréisst) | Kernel_Säit;
    uint64_t Späicher_Attribut_registréieren = 0x4400, Adress_Iwwersetzung_Kontroll = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Späicher_Attribut_registréieren), "r"(Adress_Iwwersetzung_Kontroll), "r"((uintptr_t)Racinn_Adress) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Stoppen_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 Agab_Punkt_VALUE 때만 Erlaben_VALUE.
    Computer_registréieren(IRQ_Distributeur) = 0;
    Computer_registréieren(IRQ_Distributeur + 0x180) = 0xffffffff;
    Computer_registréieren(IRQ_Distributeur + 0x80) = 0xffffffff;
    Computer_registréieren(IRQ_Distributeur + 0x280) = 1u << 30;
    Computer_registréieren(IRQ_Distributeur + 0x41c) = 0x80808080;
    Computer_registréieren(IRQ_Distributeur + 0x100) = 1u << 30;
    Computer_registréieren(IRQ_CPU_Interface + 4) = 0xff;
    Computer_registréieren(IRQ_CPU_Interface + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Sécherheet = (Computer_registréieren(IRQ_Distributeur + 4) & (1u << 10)) != 0;
    Computer_registréieren(IRQ_Distributeur) = Sécherheet ? 1 : 3;
    Computer_registréieren(IRQ_CPU_Interface) = Sécherheet ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_Kategorie, Computer_TYPE; uint32_t 판번호;
    uint64_t Agab_Punkt, App_En_tête_OFFSET, Beräich_En_tête_OFFSET; uint32_t 설정비트;
    uint16_t 실행머리크기, App_En_tête_Agab_d_Gréisst_veränneren, App_En_tête_COUNT, Beräich_En_tête_Agab_d_Gréisst_veränneren, Beräich_En_tête_COUNT, Beräich_Numm_Tabell_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_Kategorie, 설정비트; uint64_t OFFSET_VALUE, Adress, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(Benotzer_Rumm) == 272, "exception assembly layout");
static int 포함된범위(uint64_t OFFSET_VALUE, uint64_t d_Gréisst_veränneren, uint64_t bëennegen_OFFSET) {
    return OFFSET_VALUE <= bëennegen_OFFSET && d_Gréisst_veränneren <= bëennegen_OFFSET - OFFSET_VALUE;
}
static int 부가정보검사(const unsigned char *Daten_positionéieren, size_t d_Gréisst_veränneren) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, d_Gréisst_veränneren)) {
        uint32_t 낱말들[3]; memcpy(낱말들, Daten_positionéieren + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, d_Gréisst_veränneren) || !포함된범위(현재위치 + 이름영역크기, 설명크기, d_Gréisst_veränneren)) return 0;
        const unsigned char Numm[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Numm) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Numm); 순번++) if (Daten_positionéieren[현재위치 + 순번] != Numm[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, Daten_positionéieren + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *Daten, size_t d_Gréisst_veränneren, int 리눅스방식) {
    if (d_Gréisst_veränneren < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, Daten, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_Kategorie != 2 || 실행머리.Computer_TYPE != 183 || 실행머리.판번호 != 1 || 실행머리.설정비트 || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.App_En_tête_Agab_d_Gréisst_veränneren != sizeof(실행파일구획) || !실행머리.App_En_tête_COUNT || 실행머리.App_En_tête_COUNT > 16 ||
        실행머리.App_En_tête_OFFSET < sizeof(실행머리) || !포함된범위(실행머리.App_En_tête_OFFSET, (uint64_t)실행머리.App_En_tête_COUNT * sizeof(실행파일구획), d_Gréisst_veränneren)) return 사용자실행파일오류;
    uint8_t 사용량[(Benotzer_Bild_bëennegen - Benotzer_BASE) / Säitegréisst] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.App_En_tête_COUNT; 순번++) {
        실행파일구획 Daten_positionéieren; memcpy(&Daten_positionéieren, Daten + 실행머리.App_En_tête_OFFSET + 순번 * sizeof(Daten_positionéieren), sizeof(Daten_positionéieren));
        if (Daten_positionéieren.TYPE_Kategorie == 4) {
            if (!포함된범위(Daten_positionéieren.OFFSET_VALUE, Daten_positionéieren.파일영역크기, d_Gréisst_veränneren)) return 사용자실행파일오류;
            if (부가정보검사(Daten + Daten_positionéieren.OFFSET_VALUE, Daten_positionéieren.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (Daten_positionéieren.TYPE_Kategorie == 0 || Daten_positionéieren.TYPE_Kategorie == 6 || (Daten_positionéieren.TYPE_Kategorie == 0x6474e551 && !(Daten_positionéieren.설정비트 & 1))) continue;
        if (Daten_positionéieren.TYPE_Kategorie != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!Daten_positionéieren.기억영역크기) continue;
        if (Daten_positionéieren.설정비트 & ~7u || !(Daten_positionéieren.설정비트 & 4) || (Daten_positionéieren.설정비트 & 3) == 3 || Daten_positionéieren.파일영역크기 > Daten_positionéieren.기억영역크기 ||
            (Daten_positionéieren.파일영역크기 && !포함된범위(Daten_positionéieren.OFFSET_VALUE, Daten_positionéieren.파일영역크기, d_Gréisst_veränneren)) || Daten_positionéieren.Adress < Benotzer_BASE ||
            !포함된범위(Daten_positionéieren.Adress, Daten_positionéieren.기억영역크기, Benotzer_Bild_bëennegen) ||
            (!리눅스방식 && ((Daten_positionéieren.Adress & (Säitegréisst - 1)) || (Daten_positionéieren.OFFSET_VALUE & (Säitegréisst - 1)) || Daten_positionéieren.맞춤 != Säitegréisst)) ||
            (리눅스방식 && (((Daten_positionéieren.Adress ^ Daten_positionéieren.OFFSET_VALUE) & (Säitegréisst - 1)) || !Daten_positionéieren.맞춤 ||
                (Daten_positionéieren.맞춤 & (Daten_positionéieren.맞춤 - 1)) || Daten_positionéieren.맞춤 > 0x200000 || ((Daten_positionéieren.Adress ^ Daten_positionéieren.OFFSET_VALUE) & (Daten_positionéieren.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (Daten_positionéieren.Adress - Benotzer_BASE) / Säitegréisst;
        unsigned Agab_COUNT = ((Daten_positionéieren.Adress & (Säitegréisst - 1)) + Daten_positionéieren.기억영역크기 + Säitegréisst - 1) / Säitegréisst;
        for (unsigned Säit_VALUE = 첫항목; Säit_VALUE < 첫항목 + Agab_COUNT; Säit_VALUE++) {
            if (사용량[Säit_VALUE]) return 사용자실행파일오류;
            사용량[Säit_VALUE] = 1;
        }
        if ((Daten_positionéieren.설정비트 & 1) && 실행머리.Agab_Punkt >= Daten_positionéieren.Adress && 실행머리.Agab_Punkt < Daten_positionéieren.Adress + Daten_positionéieren.파일영역크기 && !(실행머리.Agab_Punkt & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *Daten, size_t d_Gréisst_veränneren) { return 실행파일검사(Daten, d_Gréisst_veränneren, 0); }
static void Säitelayout(uintptr_t Adress, uint64_t 설정비트, unsigned Autorisatiounen) {
    unsigned LOOKUP_INDEX = (Adress - Benotzer_BASE) / Säitegréisst;
    Säit_Lëscht[LOOKUP_INDEX] = Adress | 설정비트;
    Autorisatiounen_Lëscht[LOOKUP_INDEX] = Autorisatiounen;
}
static int 사용자범위(uintptr_t Adress, size_t Agab_COUNT, int 쓰는중) {
    if (Adress < Benotzer_BASE || !포함된범위(Adress, Agab_COUNT, Benotzer_bëennegen)) return 0;
    if (!Agab_COUNT) return 1;
    unsigned 첫항목 = (Adress - Benotzer_BASE) / Säitegréisst, 마지막 = (Adress + Agab_COUNT - 1 - Benotzer_BASE) / Säitegréisst;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Autorisatiounen_Lëscht[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int Instanz_Wee(uintptr_t Adress, char *Wee) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(Adress, 1, 0)) return -14;
        Wee[순번] = *(const char *)Adress++;
        if (!Wee[순번]) return 0;
    }
    return -36;
}
static intptr_t Kernel_Mooss(intptr_t Mooss) { return Mooss < 0 ? -오류번호 : Mooss; }
static int 대응파일기술자(uint64_t Fichier_Handle) { return Fichier_Handle >= 3 && Fichier_Handle < 19 ? Fichier_Lëscht[Fichier_Handle - 3] : -1; }
static int 통신끝점소유(uint64_t Fichier_Handle) { return Fichier_Handle >= 32 && Fichier_Handle < 56 && 통신끝점들[Fichier_Handle - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t Längt_VALUE, struct pk_sockaddr_in *Adress) {
    if (Längt_VALUE != sizeof(*Adress)) return -22;
    if (!사용자범위(가리킴값, Längt_VALUE, 0)) return -14;
    memcpy(Adress, (const void *)가리킴값, sizeof(*Adress));
    return Adress->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t Längt_Uweiser, pk_socklen_t *수용량) {
    if (!사용자범위(Längt_Uweiser, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)Längt_Uweiser, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t Längt_Uweiser, pk_socklen_t 수용량, int Adress, int 접속번호) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(접속번호); VALUE.sin_addr.s_addr = pk_htonl(Adress);
    if (수용량) memcpy((void *)가리킴값, &VALUE, 수용량);
    pk_socklen_t Längt_VALUE = sizeof(VALUE); memcpy((void *)Längt_Uweiser, &Längt_VALUE, sizeof(Längt_VALUE));
}
extern uintptr_t Board_Kanal(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(Benotzer_Rumm *Fichier_Agab) {
    uintptr_t 첫째값 = Fichier_Agab->registréieren_Daten[0], SECOND_VALUE = Fichier_Agab->registréieren_Daten[1], Zeechecode = Fichier_Agab->registréieren_Daten[2];
    char Wee[65];
    int Fichier_Handle, Mooss;
    switch (Fichier_Agab->registréieren_Daten[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: Uweiser 전체를 검사한 Zeréck_VALUE 출력/Fichier änneren_VALUE
        if (Zeechecode > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, Zeechecode, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Auer_VALUE();
            for (size_t 순번 = 0; 순번 < Zeechecode; 순번++) Board_Kanal(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 Kernel_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interaktiv){
                마감시각+=Auer_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return Zeechecode;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t Element_COUNT=Zeechecode>512?512:Zeechecode;for(size_t 순번=0;순번<Element_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,Element_COUNT);
        }
        Fichier_Handle = 대응파일기술자(첫째값); if (Fichier_Handle < 0) return -9;
        return Kernel_Mooss(pk_write(Fichier_Handle, (const void *)SECOND_VALUE, Zeechecode));
    case 2:
        if (Zeechecode > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, Zeechecode, 1)) return -14;
        if (첫째값 == 0) {
            size_t Element_COUNT = 0;
            while (Element_COUNT < Zeechecode) {
                int Zeechen_VALUE = (int32_t)보드글자읽기(); if (Zeechen_VALUE == -2) return Element_COUNT; if (Zeechen_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[Element_COUNT++] = Zeechen_VALUE;
            }
            return Element_COUNT ? (intptr_t)Element_COUNT : (Zeechecode ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            Mooss=자바흐름읽기(첫째값,Zeechecode>512?512:Zeechecode);if(Mooss>0)for(int 순번=0;순번<Mooss;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return Mooss;
        }
        Fichier_Handle = 대응파일기술자(첫째값); if (Fichier_Handle < 0) return -9;
        return Kernel_Mooss(pk_read(Fichier_Handle, (void *)SECOND_VALUE, Zeechecode));
    case 3:
        Mooss = Instanz_Wee(첫째값, Wee); if (Mooss) return Mooss;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (Fichier_Lëscht[순번] < 0) {
            Fichier_Handle = pk_open(Wee, (int)SECOND_VALUE, 0600);
            if (Fichier_Handle < 0) return -오류번호;
            Fichier_Lëscht[순번] = Fichier_Handle; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { Mooss = 통신끝점닫기(첫째값); if (!Mooss) 통신끝점들[첫째값 - 32] = 0; return Mooss; }
        Fichier_Handle = 대응파일기술자(첫째값); if (Fichier_Handle < 0) return -9;
        Mooss = pk_close(Fichier_Handle); if (!Mooss) Fichier_Lëscht[첫째값 - 3] = -1;
        return Kernel_Mooss(Mooss);
    case 5:
        Fichier_Handle = 대응파일기술자(첫째값); if (Fichier_Handle < 0) return -9;
        if (Zeechecode > 2) return -22;
        return Kernel_Mooss(pk_lseek(Fichier_Handle, (int64_t)SECOND_VALUE, Zeechecode));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 Benotzer RW/NX 힙, 새로 노출되는 페이지는 0으로 initialiséieren
        if (!첫째값) return 동적기억끝;
        if (첫째값 < Benotzer_Bild_bëennegen || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + Säitegréisst - 1) & ~(Säitegréisst - 1);
        uintptr_t 새쪽들 = (첫째값 + Säitegréisst - 1) & ~(Säitegréisst - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t Daten_positionéieren = 이전쪽들; Daten_positionéieren < 새쪽들; Daten_positionéieren += Säitegréisst) Säitelayout(Daten_positionéieren, Kernel_Säit, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t Daten_positionéieren = 이전쪽들; Daten_positionéieren < 새쪽들; Daten_positionéieren += Säitegréisst) Säitelayout(Daten_positionéieren, Benotzer_lies_schreiffäeg, 3);
        } else {
            for (uintptr_t Daten_positionéieren = 새쪽들; Daten_positionéieren < 이전쪽들; Daten_positionéieren += Säitegréisst) {
                Säit_Lëscht[(Daten_positionéieren - Benotzer_BASE) / Säitegréisst] = 0; Autorisatiounen_Lëscht[(Daten_positionéieren - Benotzer_BASE) / Säitegréisst] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        Fichier_Handle = 대응파일기술자(첫째값); return Fichier_Handle < 0 ? -9 : Kernel_Mooss(pk_size(Fichier_Handle));
    case 10:
        Fichier_Handle = 대응파일기술자(첫째값); return Fichier_Handle < 0 ? -9 : Kernel_Mooss(pk_ftruncate(Fichier_Handle, (int64_t)SECOND_VALUE));
    case 11:
        Mooss = Instanz_Wee(첫째값, Wee); return Mooss ? Mooss : Kernel_Mooss(pk_unlink(Wee));
    case 12:
        Fichier_Handle = 대응파일기술자(첫째값); return Fichier_Handle < 0 ? -9 : Kernel_Mooss(pk_fsync(Fichier_Handle));
    case 13: { // 그래픽 기초 API: Benotzer 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Fichier_Agab->registréieren_Daten[3], 높이값 = Fichier_Agab->registréieren_Daten[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t 세로좌표 = SECOND_VALUE; 세로좌표 < SECOND_VALUE + 높이값; 세로좌표++) for (uintptr_t X_Koordinat = 첫째값; X_Koordinat < 첫째값 + 너비값; X_Koordinat++) Board_Pel(X_Koordinat, 세로좌표, Zeechecode);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=Element_COUNT; args(index,buffer,capacity)=UTF-8 Längt_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (Zeechecode <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interaktiv=1;return Board_Terminal(13);}
        if(첫째값==2){interaktiv=0;return 0;}
        if(첫째값==3)return Board_Terminal(13);
        if(첫째값!=1||!interaktiv)return -22;
        Mooss=(int32_t)보드글자읽기();
        if(Mooss==-4096)return Mooss;
        Start_TIMEOUT();return Mooss<0?-11:Mooss;
    case 17: { // 유한한 협력 Waart_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t bëennegen_TIME = Auer_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Auer_VALUE() < bëennegen_TIME);
        Start_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        Mooss = Instanz_Wee(첫째값, Wee); if (Mooss) return Mooss;
        unsigned Längt_VALUE = 0; while (Wee[Längt_VALUE]) Längt_VALUE++;
        Mooss = 자바경로시작(Längt_VALUE); if (Mooss < 0) return Mooss;
        for (unsigned 순번 = 0; 순번 < Längt_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)Wee[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int Zeechen_VALUE=(int32_t)보드글자읽기();if(Zeechen_VALUE==-4096)return Zeechen_VALUE;if(Zeechen_VALUE>=0)화면누름(Besëtzer_Objet,Zeechen_VALUE);Start_TIMEOUT();}
        if(첫째값==3&&Zeechecode){if(!자바셸대화형())return -95;interaktiv=1;Board_Terminal(300);}
        return 화면호출(Besëtzer_Objet,첫째값,SECOND_VALUE,Zeechecode,Fichier_Agab->registréieren_Daten[3],Fichier_Agab->registréieren_Daten[4],Fichier_Agab->registréieren_Daten[5]);
    case 21:
        if(Zeechecode>127)return -22;if(!사용자범위(SECOND_VALUE,Zeechecode*sizeof(uint32_t),0))return -14;
        return 화면글(Besëtzer_Objet,첫째값,(const uint32_t *)SECOND_VALUE,Zeechecode);
    case 22: // 화면 d_Gréisst_veränneren Requête_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(Zeechecode==0||Zeechecode==6))Mooss=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(Zeechecode==0||Zeechecode==IPPROTO_UDP))Mooss=자바전문만들기(첫째값,SECOND_VALUE,Zeechecode);
        else return -93;
        if (Mooss >= 32 && Mooss < 56) 통신끝점들[Mooss - 32] = 1;
        return Mooss;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in Adress;
        Mooss = 주소입력(SECOND_VALUE, Zeechecode, &Adress); if (Mooss) return Mooss;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(Adress.sin_addr.s_addr),pk_htons(Adress.sin_port)):자바전문묶기(첫째값, pk_htonl(Adress.sin_addr.s_addr), pk_htons(Adress.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Fichier_Agab->registréieren_Daten[3]) return -95;
        if (Zeechecode > 512) return -90;
        if (Zeechecode && !사용자범위(SECOND_VALUE, Zeechecode, 0)) return -14;
        struct pk_sockaddr_in Adress;
        Mooss = 주소입력(Fichier_Agab->registréieren_Daten[4], Fichier_Agab->registréieren_Daten[5], &Adress); if (Mooss) return Mooss;
        for (unsigned 순번 = 0; 순번 < Zeechecode; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(Adress.sin_addr.s_addr), pk_htons(Adress.sin_port), Zeechecode);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Fichier_Agab->registréieren_Daten[3]) return -95;
        if (Zeechecode > 512) return -90;
        if (Zeechecode && !사용자범위(SECOND_VALUE, Zeechecode, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (Fichier_Agab->registréieren_Daten[4]) { Mooss = 주소출력검사(Fichier_Agab->registréieren_Daten[4], Fichier_Agab->registréieren_Daten[5], &수용량); if (Mooss) return Mooss; }
        Mooss = 자바전문받기(첫째값, Zeechecode); if (Mooss < 0) return Mooss;
        for (int 순번 = 0; 순번 < Mooss; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (Fichier_Agab->registréieren_Daten[4]) 주소출력(Fichier_Agab->registréieren_Daten[4], Fichier_Agab->registréieren_Daten[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return Mooss;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        Mooss = 주소출력검사(SECOND_VALUE, Zeechecode, &수용량); if (Mooss) return Mooss;
        주소출력(SECOND_VALUE,Zeechecode,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in Adress;
        Mooss=주소입력(SECOND_VALUE,Zeechecode,&Adress);if(Mooss)return Mooss;
        return 자바흐름연결(첫째값,pk_htonl(Adress.sin_addr.s_addr),pk_htons(Adress.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||Zeechecode)return -95;Mooss=자바흐름연결받기(첫째값);if(Mooss>=40&&Mooss<56)통신끝점들[Mooss-32]=1;return Mooss;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(Benotzer_Rumm *Fichier_Agab) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Fichier_Agab) : 자체체계호출(Fichier_Agab);
}
static void 커널돌아가기(Benotzer_Rumm *Fichier_Agab, int Mooss) {
    Stoppen_TIMEOUT();
    Fichier_Agab->registréieren_Daten[0] = (uint64_t)(int64_t)Mooss;
    Fichier_Agab->Befeel_positionéieren = (uintptr_t)사용자복귀;
    Fichier_Agab->Status_CODE = 0x3c5; // EL1h, DAIF masked
}
int 사용자예외(Benotzer_Rumm *Fichier_Agab, unsigned INTERCEPT) {
    if (!aktiv || (Fichier_Agab->Status_CODE & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t 승인값 = Computer_registréieren(IRQ_CPU_Interface + 0xc), Identifikateur_VALUE = 승인값 & 1023;
        if (Identifikateur_VALUE == 30) { 커널돌아가기(Fichier_Agab, Benotzer_TIMEOUT); Computer_registréieren(IRQ_CPU_Interface + 0x10) = 승인값; return 1; }
        if (Identifikateur_VALUE < 1020) Computer_registréieren(IRQ_CPU_Interface + 0x10) = 승인값;
        return 1;
    }
    uint64_t 예외상태; __asm__ volatile("mrs %0, esr_el1" : "=r"(예외상태));
    if (Auer_VALUE() >= 마감시각) { 커널돌아가기(Fichier_Agab, Benotzer_TIMEOUT); return 1; }
    unsigned 예외분류 = 예외상태 >> 26;
    if (예외분류 == 0x15 && (예외상태 & 0xffff) == 0) {
        if (리눅스규약 ? Fichier_Agab->registréieren_Daten[8] == 93 || Fichier_Agab->registréieren_Daten[8] == 94 : Fichier_Agab->registréieren_Daten[8] == 6) 커널돌아가기(Fichier_Agab, (int)(Fichier_Agab->registréieren_Daten[0] & 255));
        else {
            intptr_t Mooss=체계호출(Fichier_Agab);
            if(Mooss==-4096&&interaktiv){
                저장값[Besëtzer_Objet].실행틀=*Fichier_Agab;저장값[Besëtzer_Objet].실행틀.Befeel_positionéieren-=4;
                사용자실수보관(저장값[Besëtzer_Objet].실수저장상태);커널돌아가기(Fichier_Agab,사용자중단됨);
            }else Fichier_Agab->registréieren_Daten[0]=(uint64_t)Mooss;
        }
    } else 커널돌아가기(Fichier_Agab, 예외분류 == 0x24 ? Benotzer_Daten_Feeler : 예외분류 == 0x20 ? 사용자실행오류 : Benotzer_ongëlteg_Instruktioun);
    return 1;
}

// 생성된 const ELF Grupp_VALUE: 실행은 반드시 App_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *Daten; size_t d_Gréisst_veränneren; unsigned 전달값; } App;
#include "programs.h"
static void *Snapshot(unsigned positionéieren_INDEX){return (void *)(0x04000000ul+positionéieren_INDEX*(Benotzer_bëennegen-Benotzer_BASE));}
static int Ofschléissen_App(int Mooss){
    사용자누적시각[Besëtzer_Objet]+=(uint32_t)보드밀리초()-사용자실행시각[Besëtzer_Objet];
    Stoppen_TIMEOUT();aktiv=0;
    if(Mooss==사용자중단됨){
        저장된작업 *Zeechefolleg_Daten=&저장값[Besëtzer_Objet];Zeechefolleg_Daten->멈춤상태=1;Zeechefolleg_Daten->interaktiv=interaktiv;Zeechefolleg_Daten->리눅스규약=리눅스규약;Zeechefolleg_Daten->동적기억공간=동적기억끝;Zeechefolleg_Daten->인수개수=전달인수개수;
        memcpy(Zeechefolleg_Daten->Autorisatiounen_Lëscht,Autorisatiounen_Lëscht,sizeof(Autorisatiounen_Lëscht));memcpy(Zeechefolleg_Daten->Fichier_Lëscht,Fichier_Lëscht,sizeof(Fichier_Lëscht));memcpy(Zeechefolleg_Daten->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(Zeechefolleg_Daten->Argument_ARRAY,전달인수,sizeof(전달인수));memcpy(Zeechefolleg_Daten->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<Benotzer_Säit_COUNT;순번++)if(Autorisatiounen_Lëscht[순번])memcpy((unsigned char *)Snapshot(Besëtzer_Objet)+순번*Säitegréisst,(void *)(Benotzer_BASE+순번*Säitegréisst),Säitegréisst);
    }else{
        저장값[Besëtzer_Objet].멈춤상태=0;화면초기화(Besëtzer_Objet);
        for(unsigned 순번=0;순번<16;순번++)if(Fichier_Lëscht[순번]>=0)pk_close(Fichier_Lëscht[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<Benotzer_Säit_COUNT;순번++){Säit_Lëscht[순번]=0;Autorisatiounen_Lëscht[순번]=0;}변환표맞추기();return Mooss;
}
uintptr_t Board_Benotzersteierelement(uintptr_t Aktioun){
    unsigned positionéieren_INDEX=Aktioun&15;if(positionéieren_INDEX>=4||aktiv)return (uint32_t)-22;
    저장된작업 *Zeechefolleg_Daten=&저장값[positionéieren_INDEX];
    if(Aktioun>=32){if(Zeechefolleg_Daten->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(Zeechefolleg_Daten->Fichier_Lëscht[순번]>=0)pk_close(Zeechefolleg_Daten->Fichier_Lëscht[순번]);for(unsigned 순번=0;순번<24;순번++)if(Zeechefolleg_Daten->통신끝점들[순번])통신끝점닫기(순번+32);}Zeechefolleg_Daten->멈춤상태=0;화면초기화(positionéieren_INDEX);return 0;}
    if(Aktioun>=16)return Zeechefolleg_Daten->멈춤상태;
    if(!Zeechefolleg_Daten->멈춤상태)return (uint32_t)-22;
    Besëtzer_Objet=positionéieren_INDEX;interaktiv=Zeechefolleg_Daten->interaktiv;리눅스규약=Zeechefolleg_Daten->리눅스규약;동적기억끝=Zeechefolleg_Daten->동적기억공간;전달인수개수=Zeechefolleg_Daten->인수개수;
    memcpy(Fichier_Lëscht,Zeechefolleg_Daten->Fichier_Lëscht,sizeof(Fichier_Lëscht));memcpy(통신끝점들,Zeechefolleg_Daten->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,Zeechefolleg_Daten->Argument_ARRAY,sizeof(전달인수));memcpy(전달인수길이,Zeechefolleg_Daten->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<Benotzer_Säit_COUNT;순번++)Säit_Lëscht[순번]=(Benotzer_BASE+순번*Säitegréisst)|Kernel_Säit;변환표맞추기();
    memset((void *)Benotzer_BASE,0,Benotzer_bëennegen-Benotzer_BASE);
    for(unsigned 순번=0;순번<Benotzer_Säit_COUNT;순번++)if(Zeechefolleg_Daten->Autorisatiounen_Lëscht[순번])memcpy((void *)(Benotzer_BASE+순번*Säitegréisst),(unsigned char *)Snapshot(positionéieren_INDEX)+순번*Säitegréisst,Säitegréisst);
    memcpy(Autorisatiounen_Lëscht,Zeechefolleg_Daten->Autorisatiounen_Lëscht,sizeof(Autorisatiounen_Lëscht));
    for(unsigned 순번=0;순번<Benotzer_Säit_COUNT;순번++){unsigned Daten_positionéieren=Autorisatiounen_Lëscht[순번];Säit_Lëscht[순번]=Daten_positionéieren?(Benotzer_BASE+순번*Säitegréisst)|(Daten_positionéieren==3?Benotzer_lies_schreiffäeg:Daten_positionéieren==5?사용자읽고실행:Benotzer_schreifgeschützt):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");aktiv=1;Zeechefolleg_Daten->멈춤상태=0;Start_TIMEOUT();
    사용자실행시각[Besëtzer_Objet]=보드밀리초();
    return (uint32_t)Ofschléissen_App(Benotzer_CV(&Zeechefolleg_Daten->실행틀,Zeechefolleg_Daten->실수저장상태));
}
static int Laf_App(const unsigned char *Daten, size_t d_Gréisst_veränneren, unsigned 전달값, int 리눅스방식, const char *Numm) {
    if (aktiv) return -16;
    Besëtzer_Objet=Board_Terminal(11);if(Besëtzer_Objet<0||Besëtzer_Objet>3||저장값[Besëtzer_Objet].멈춤상태)return -16;interaktiv=0;
    int 유효함 = 실행파일검사(Daten, d_Gréisst_veränneren, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned Numm_INDEX=0;
    while (*Numm && Numm_INDEX<31) Benotzer_Befeel_Numm[Besëtzer_Objet][Numm_INDEX++]=(unsigned char)*Numm++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (Numm_INDEX) Benotzer_Befeel_Numm[Besëtzer_Objet][Numm_INDEX++]=' ';
        for (unsigned positionéieren_INDEX=0; positionéieren_INDEX<전달인수길이[0]; positionéieren_INDEX++) Benotzer_Befeel_Numm[Besëtzer_Objet][Numm_INDEX++]=전달인수[0][positionéieren_INDEX];
    }
    Benotzer_Befeel_Numm[Besëtzer_Objet][Numm_INDEX]=0; Benotzernummer[Besëtzer_Objet]=Weider_Benotzernummer++;
    if (Weider_Benotzernummer>0x7fffffffu) Weider_Benotzernummer=10;
    Benotzer_Start_TIME[Besëtzer_Objet]=보드밀리초(); 사용자누적시각[Besëtzer_Objet]=0;
    for (unsigned 순번 = 0; 순번 < Benotzer_Säit_COUNT; 순번++) Säit_Lëscht[순번] = (Benotzer_BASE + 순번 * Säitegréisst) | Kernel_Säit;
    변환표맞추기();
    memset((void *)Benotzer_BASE, 0, Benotzer_bëennegen - Benotzer_BASE);
    memset(Autorisatiounen_Lëscht, 0, sizeof(Autorisatiounen_Lëscht));
    실행파일머리 실행머리; memcpy(&실행머리, Daten, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.App_En_tête_COUNT; 순번++) {
        실행파일구획 Daten_positionéieren; memcpy(&Daten_positionéieren, Daten + 실행머리.App_En_tête_OFFSET + 순번 * sizeof(Daten_positionéieren), sizeof(Daten_positionéieren));
        if (Daten_positionéieren.TYPE_Kategorie != 1 || !Daten_positionéieren.기억영역크기) continue;
        if (Daten_positionéieren.파일영역크기) memcpy((void *)(uintptr_t)Daten_positionéieren.Adress, Daten + Daten_positionéieren.OFFSET_VALUE, Daten_positionéieren.파일영역크기);
        for (uintptr_t 현재위치 = Daten_positionéieren.Adress & ~(Säitegréisst - 1); 현재위치 < Daten_positionéieren.Adress + Daten_positionéieren.기억영역크기; 현재위치 += Säitegréisst) {
            Autorisatiounen_Lëscht[(현재위치 - Benotzer_BASE) / Säitegréisst] = (Daten_positionéieren.설정비트 & 2) ? 3 : ((Daten_positionéieren.설정비트 & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = Benotzer_Stapel_Adress; 현재위치 < Benotzer_bëennegen; 현재위치 += Säitegréisst) Autorisatiounen_Lëscht[(현재위치 - Benotzer_BASE) / Säitegréisst] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.Agab_Punkt) : Benotzer_bëennegen;
    for (unsigned 순번 = 0; 순번 < Benotzer_Säit_COUNT; 순번++) {
        unsigned Autorisatiounen = Autorisatiounen_Lëscht[순번];
        Säit_Lëscht[순번] = Autorisatiounen ? (Benotzer_BASE + 순번 * Säitegréisst) | (Autorisatiounen == 3 ? Benotzer_lies_schreiffäeg : Autorisatiounen == 5 ? 사용자읽고실행 : Benotzer_schreifgeschützt) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) Fichier_Lëscht[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = Benotzer_Bild_bëennegen;
    aktiv = 1; Start_TIMEOUT();
    사용자실행시각[Besëtzer_Objet]=보드밀리초();
    int Mooss = Benotzer_aginn(실행머리.Agab_Punkt, 초기쌓임공간, 전달값);
    return Ofschléissen_App(Mooss);
}
uintptr_t Board_Benotzer_Laf(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Numm=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)Laf_App(실행항목들[LOOKUP_INDEX].Daten, 실행항목들[LOOKUP_INDEX].d_Gréisst_veränneren, 실행항목들[LOOKUP_INDEX].전달값, 0, Numm);
}
static uintptr_t ausféieren_Fichier(int 리눅스방식) {
    static unsigned char Bild[16384];
    if (aktiv || !전달인수개수) return (uint32_t)-22;
    int Fichier_Handle = pk_open((const char *)전달인수[0], schreifgeschützt_VALUE, 0);
    if (Fichier_Handle < 0) return (uint32_t)-오류번호;
    int d_Gréisst_veränneren = pk_size(Fichier_Handle);
    if (d_Gréisst_veränneren < 0 || (unsigned)d_Gréisst_veränneren > sizeof(Bild)) { pk_close(Fichier_Handle); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(Fichier_Handle, Bild, d_Gréisst_veränneren); pk_close(Fichier_Handle);
    if (RECEIVED_COUNT != d_Gréisst_veränneren) return (uint32_t)-5;
    return (uint32_t)Laf_App(Bild, d_Gréisst_veränneren, 0, 리눅스방식, "");
}
uintptr_t Board_Benotzer_Fichier(void) { return ausféieren_Fichier(0); }
uintptr_t 보드사용자리눅스파일(void) { return ausféieren_Fichier(1); }
uintptr_t Board_Benotzer_validéieren(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].Daten, 잘못된실행항목들[순번].d_Gréisst_veränneren) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
