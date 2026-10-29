#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 zbatoj_komandë makinë Shtresë_VALUE. Kartelë të_dhëna/정책은 기존 AOT Java 커널에 위임한다.
#include "përdorues.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../rrjet_Stivë/rrjet_Stivë.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define makinë_regjistroj(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_shpërndarës 0xff841000ul
#define IRQ_CPU_ndërfaqe 0xff842000ul
#define përmasat_e_faqes 4096ul
#define 접근표시 (1ul << 10)
#define Jo_zbatoj_leje (1ul << 53)
#define përdorues_Jo_zbatoj (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define bërthamë_faqe (3ul | 보통기억 | Jo_zbatoj_leje | përdorues_Jo_zbatoj)
#define përdorues_lexoj_shkruaj (3ul | 보통기억 | (1ul << 6) | Jo_zbatoj_leje | përdorues_Jo_zbatoj)
#define përdorues_vetëm_për_lexim (3ul | 보통기억 | (3ul << 6) | Jo_zbatoj_leje | përdorues_Jo_zbatoj)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | Jo_zbatoj_leje)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t panel_pikëz(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t panel_Terminali(uintptr_t);
extern int Terminali_në_pritje(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int përdorues_CV(përdorues_kuadër *,void *);
extern void 사용자실수보관(void *);
extern int përdorues_fut(uintptr_t futje_p, uintptr_t Stivë_hapësira_ruajtëse, uintptr_t 전달값);
extern void përdorues_Kthe(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t rrënjë_email[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t faqe_Listë[përdorues_faqe_COUNT] __attribute__((aligned(4096)));
static uint8_t Lejet_Listë[përdorues_faqe_COUNT];
static int Aktiv, skedar_Listë[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned skedar_dorezë){return skedar_dorezë<40?자바전문닫기(skedar_dorezë):자바흐름닫기(skedar_dorezë);}
static uint64_t FREQUENCY, 마감시각;
static uintptr_t 동적기억끝;
// bërthamë_VALUE 셸이 준비한 UTF-8 Argumente. EL0에는 kopjoj_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,ndërvepruese,리눅스규약,skedar_Listë[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_ARRAY[8][256],Lejet_Listë[përdorues_faqe_COUNT];
    uintptr_t 동적기억공간; përdorues_kuadër 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int pronari_objekt,ndërvepruese;
static uint32_t numri_i_përdoruesit[4], përdorues_nis_Ora[4], 사용자누적시각[4], 사용자실행시각[4], Tjetër_numri_i_përdoruesit=10;
static unsigned char përdorues_komandë_emër[4][288];
uint32_t 사용자상태읽기(unsigned futje_VALUE, unsigned INDEX) {
    unsigned pozicioni_INDEX=INDEX&3;
    int status_VALUE=(Aktiv && pronari_objekt==(int)pozicioni_INDEX) ? 1 : 저장값[pozicioni_INDEX].멈춤상태 ? 2 : 0;
    if (futje_VALUE==0) return status_VALUE;
    if (!status_VALUE) return 0;
    if (futje_VALUE==1) return numri_i_përdoruesit[pozicioni_INDEX];
    if (futje_VALUE==2) {
        unsigned char *쪽들=status_VALUE==1?Lejet_Listë:저장값[pozicioni_INDEX].Lejet_Listë;
        unsigned faqe_COUNT=0; for (unsigned 순번=0; 순번<përdorues_faqe_COUNT; 순번++) if(쪽들[순번]) faqe_COUNT++;
        return faqe_COUNT*4;
    }
    if (futje_VALUE==3) return (uint32_t)보드밀리초()-përdorues_nis_Ora[pozicioni_INDEX];
    if (futje_VALUE==4) return 사용자누적시각[pozicioni_INDEX]+(status_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[pozicioni_INDEX]:0);
    if (futje_VALUE==5) return INDEX/4<sizeof(përdorues_komandë_emër[0])?përdorues_komandë_emër[pozicioni_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t futje_COUNT) {
    if (Aktiv || futje_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = futje_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t 현재위치, uintptr_t bajt_të_dhëna) {
    if (Aktiv || LOOKUP_INDEX >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[LOOKUP_INDEX] || !bajt_të_dhëna || bajt_të_dhëna > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][현재위치] = bajt_të_dhëna;
    전달인수길이[LOOKUP_INDEX] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Ora_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Ndal_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    makinë_regjistroj(IRQ_shpërndarës + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void nis_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, aktivizoj = 1;
    마감시각 = Ora_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(aktivizoj) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned të_dhëna_bllokoj = 0; të_dhëna_bllokoj < 4; të_dhëna_bllokoj++) {
        rrënjë_email[të_dhëna_bllokoj] = (uintptr_t)가운데[të_dhëna_bllokoj] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t email = ((uintptr_t)të_dhëna_bllokoj << 30) | ((uintptr_t)순번 << 21);
            가운데[të_dhëna_bllokoj][순번] = email | 1 | 접근표시 | përdorues_Jo_zbatoj;
            if (email >= 0xfc000000ul) 가운데[të_dhëna_bllokoj][순번] |= Jo_zbatoj_leje; // Device-nGnRnE
            else 가운데[të_dhëna_bllokoj][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < përdorues_faqe_COUNT / 512; SECOND_VALUE++)
        가운데[0][(përdorues_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(faqe_Listë + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < përdorues_faqe_COUNT; 순번++) faqe_Listë[순번] = (përdorues_BASE + 순번 * përmasat_e_faqes) | bërthamë_faqe;
    uint64_t Memorie_atribut_regjistroj = 0x4400, email_Përkthimi_kontroll = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Memorie_atribut_regjistroj), "r"(email_Përkthimi_kontroll), "r"((uintptr_t)rrënjë_email) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Ndal_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 futje_p_VALUE 때만 Lejoj_VALUE.
    makinë_regjistroj(IRQ_shpërndarës) = 0;
    makinë_regjistroj(IRQ_shpërndarës + 0x180) = 0xffffffff;
    makinë_regjistroj(IRQ_shpërndarës + 0x80) = 0xffffffff;
    makinë_regjistroj(IRQ_shpërndarës + 0x280) = 1u << 30;
    makinë_regjistroj(IRQ_shpërndarës + 0x41c) = 0x80808080;
    makinë_regjistroj(IRQ_shpërndarës + 0x100) = 1u << 30;
    makinë_regjistroj(IRQ_CPU_ndërfaqe + 4) = 0xff;
    makinë_regjistroj(IRQ_CPU_ndërfaqe + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int siguri = (makinë_regjistroj(IRQ_shpërndarës + 4) & (1u << 10)) != 0;
    makinë_regjistroj(IRQ_shpërndarës) = siguri ? 1 : 3;
    makinë_regjistroj(IRQ_CPU_ndërfaqe) = siguri ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_kategori, makinë_TYPE; uint32_t 판번호;
    uint64_t futje_p, program_Kreu_OFFSET, seksion_Kreu_OFFSET; uint32_t konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond;
    uint16_t 실행머리크기, program_Kreu_futje_ndryshoj_përmasat, program_Kreu_COUNT, seksion_Kreu_futje_ndryshoj_përmasat, seksion_Kreu_COUNT, seksion_emër_tabelë_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_kategori, konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond; uint64_t OFFSET_VALUE, email, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(përdorues_kuadër) == 272, "exception assembly layout");
static int 포함된범위(uint64_t OFFSET_VALUE, uint64_t Madhësi, uint64_t mbaroj_OFFSET) {
    return OFFSET_VALUE <= mbaroj_OFFSET && Madhësi <= mbaroj_OFFSET - OFFSET_VALUE;
}
static int 부가정보검사(const unsigned char *të_dhëna_pozicioni, size_t Madhësi) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, Madhësi)) {
        uint32_t 낱말들[3]; memcpy(낱말들, të_dhëna_pozicioni + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, Madhësi) || !포함된범위(현재위치 + 이름영역크기, 설명크기, Madhësi)) return 0;
        const unsigned char Emër[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Emër) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Emër); 순번++) if (të_dhëna_pozicioni[현재위치 + 순번] != Emër[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, të_dhëna_pozicioni + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *të_dhëna, size_t Madhësi, int 리눅스방식) {
    if (Madhësi < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, të_dhëna, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_kategori != 2 || 실행머리.makinë_TYPE != 183 || 실행머리.판번호 != 1 || 실행머리.konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.program_Kreu_futje_ndryshoj_përmasat != sizeof(실행파일구획) || !실행머리.program_Kreu_COUNT || 실행머리.program_Kreu_COUNT > 16 ||
        실행머리.program_Kreu_OFFSET < sizeof(실행머리) || !포함된범위(실행머리.program_Kreu_OFFSET, (uint64_t)실행머리.program_Kreu_COUNT * sizeof(실행파일구획), Madhësi)) return 사용자실행파일오류;
    uint8_t 사용량[(përdorues_IMAGE_mbaroj - përdorues_BASE) / përmasat_e_faqes] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.program_Kreu_COUNT; 순번++) {
        실행파일구획 të_dhëna_pozicioni; memcpy(&të_dhëna_pozicioni, të_dhëna + 실행머리.program_Kreu_OFFSET + 순번 * sizeof(të_dhëna_pozicioni), sizeof(të_dhëna_pozicioni));
        if (të_dhëna_pozicioni.TYPE_kategori == 4) {
            if (!포함된범위(të_dhëna_pozicioni.OFFSET_VALUE, të_dhëna_pozicioni.파일영역크기, Madhësi)) return 사용자실행파일오류;
            if (부가정보검사(të_dhëna + të_dhëna_pozicioni.OFFSET_VALUE, të_dhëna_pozicioni.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (të_dhëna_pozicioni.TYPE_kategori == 0 || të_dhëna_pozicioni.TYPE_kategori == 6 || (të_dhëna_pozicioni.TYPE_kategori == 0x6474e551 && !(të_dhëna_pozicioni.konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond & 1))) continue;
        if (të_dhëna_pozicioni.TYPE_kategori != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!të_dhëna_pozicioni.기억영역크기) continue;
        if (të_dhëna_pozicioni.konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond & ~7u || !(të_dhëna_pozicioni.konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond & 4) || (të_dhëna_pozicioni.konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond & 3) == 3 || të_dhëna_pozicioni.파일영역크기 > të_dhëna_pozicioni.기억영역크기 ||
            (të_dhëna_pozicioni.파일영역크기 && !포함된범위(të_dhëna_pozicioni.OFFSET_VALUE, të_dhëna_pozicioni.파일영역크기, Madhësi)) || të_dhëna_pozicioni.email < përdorues_BASE ||
            !포함된범위(të_dhëna_pozicioni.email, të_dhëna_pozicioni.기억영역크기, përdorues_IMAGE_mbaroj) ||
            (!리눅스방식 && ((të_dhëna_pozicioni.email & (përmasat_e_faqes - 1)) || (të_dhëna_pozicioni.OFFSET_VALUE & (përmasat_e_faqes - 1)) || të_dhëna_pozicioni.맞춤 != përmasat_e_faqes)) ||
            (리눅스방식 && (((të_dhëna_pozicioni.email ^ të_dhëna_pozicioni.OFFSET_VALUE) & (përmasat_e_faqes - 1)) || !të_dhëna_pozicioni.맞춤 ||
                (të_dhëna_pozicioni.맞춤 & (të_dhëna_pozicioni.맞춤 - 1)) || të_dhëna_pozicioni.맞춤 > 0x200000 || ((të_dhëna_pozicioni.email ^ të_dhëna_pozicioni.OFFSET_VALUE) & (të_dhëna_pozicioni.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (të_dhëna_pozicioni.email - përdorues_BASE) / përmasat_e_faqes;
        unsigned futje_COUNT = ((të_dhëna_pozicioni.email & (përmasat_e_faqes - 1)) + të_dhëna_pozicioni.기억영역크기 + përmasat_e_faqes - 1) / përmasat_e_faqes;
        for (unsigned faqe_VALUE = 첫항목; faqe_VALUE < 첫항목 + futje_COUNT; faqe_VALUE++) {
            if (사용량[faqe_VALUE]) return 사용자실행파일오류;
            사용량[faqe_VALUE] = 1;
        }
        if ((të_dhëna_pozicioni.konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond & 1) && 실행머리.futje_p >= të_dhëna_pozicioni.email && 실행머리.futje_p < të_dhëna_pozicioni.email + të_dhëna_pozicioni.파일영역크기 && !(실행머리.futje_p & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *të_dhëna, size_t Madhësi) { return 실행파일검사(të_dhëna, Madhësi, 0); }
static void struktura_e_faqes(uintptr_t email, uint64_t konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond, unsigned autorizime) {
    unsigned LOOKUP_INDEX = (email - përdorues_BASE) / përmasat_e_faqes;
    faqe_Listë[LOOKUP_INDEX] = email | konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond;
    Lejet_Listë[LOOKUP_INDEX] = autorizime;
}
static int 사용자범위(uintptr_t email, size_t futje_COUNT, int 쓰는중) {
    if (email < përdorues_BASE || !포함된범위(email, futje_COUNT, përdorues_mbaroj)) return 0;
    if (!futje_COUNT) return 1;
    unsigned 첫항목 = (email - përdorues_BASE) / përmasat_e_faqes, 마지막 = (email + futje_COUNT - 1 - përdorues_BASE) / përmasat_e_faqes;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Lejet_Listë[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int kopjoj_shteg(uintptr_t email, char *POZICIONI) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(email, 1, 0)) return -14;
        POZICIONI[순번] = *(const char *)email++;
        if (!POZICIONI[순번]) return 0;
    }
    return -36;
}
static intptr_t bërthamë_llogaritje(intptr_t llogaritje) { return llogaritje < 0 ? -오류번호 : llogaritje; }
static int 대응파일기술자(uint64_t skedar_dorezë) { return skedar_dorezë >= 3 && skedar_dorezë < 19 ? skedar_Listë[skedar_dorezë - 3] : -1; }
static int 통신끝점소유(uint64_t skedar_dorezë) { return skedar_dorezë >= 32 && skedar_dorezë < 56 && 통신끝점들[skedar_dorezë - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t gjatësi_VALUE, struct pk_sockaddr_in *email) {
    if (gjatësi_VALUE != sizeof(*email)) return -22;
    if (!사용자범위(가리킴값, gjatësi_VALUE, 0)) return -14;
    memcpy(email, (const void *)가리킴값, sizeof(*email));
    return email->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t gjatësi_tregues, pk_socklen_t *수용량) {
    if (!사용자범위(gjatësi_tregues, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)gjatësi_tregues, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t gjatësi_tregues, pk_socklen_t 수용량, int email, int numri_i_portës) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(numri_i_portës); VALUE.sin_addr.s_addr = pk_htonl(email);
    if (수용량) memcpy((void *)가리킴값, &VALUE, 수용량);
    pk_socklen_t gjatësi_VALUE = sizeof(VALUE); memcpy((void *)gjatësi_tregues, &gjatësi_VALUE, sizeof(gjatësi_VALUE));
}
extern uintptr_t panel_kanal(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(përdorues_kuadër *skedar_futje) {
    uintptr_t 첫째값 = skedar_futje->regjistroj_të_dhëna[0], SECOND_VALUE = skedar_futje->regjistroj_të_dhëna[1], kodi_i_karakterit = skedar_futje->regjistroj_të_dhëna[2];
    char POZICIONI[65];
    int skedar_dorezë, llogaritje;
    switch (skedar_futje->regjistroj_të_dhëna[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: tregues 전체를 검사한 PAS_VALUE 출력/Kartelë ndryshoj_VALUE
        if (kodi_i_karakterit > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, kodi_i_karakterit, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Ora_VALUE();
            for (size_t 순번 = 0; 순번 < kodi_i_karakterit; 순번++) panel_kanal(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 bërthamë_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(ndërvepruese){
                마감시각+=Ora_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return kodi_i_karakterit;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t njësi_COUNT=kodi_i_karakterit>512?512:kodi_i_karakterit;for(size_t 순번=0;순번<njësi_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,njësi_COUNT);
        }
        skedar_dorezë = 대응파일기술자(첫째값); if (skedar_dorezë < 0) return -9;
        return bërthamë_llogaritje(pk_write(skedar_dorezë, (const void *)SECOND_VALUE, kodi_i_karakterit));
    case 2:
        if (kodi_i_karakterit > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, kodi_i_karakterit, 1)) return -14;
        if (첫째값 == 0) {
            size_t njësi_COUNT = 0;
            while (njësi_COUNT < kodi_i_karakterit) {
                int karakter_VALUE = (int32_t)보드글자읽기(); if (karakter_VALUE == -2) return njësi_COUNT; if (karakter_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[njësi_COUNT++] = karakter_VALUE;
            }
            return njësi_COUNT ? (intptr_t)njësi_COUNT : (kodi_i_karakterit ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            llogaritje=자바흐름읽기(첫째값,kodi_i_karakterit>512?512:kodi_i_karakterit);if(llogaritje>0)for(int 순번=0;순번<llogaritje;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return llogaritje;
        }
        skedar_dorezë = 대응파일기술자(첫째값); if (skedar_dorezë < 0) return -9;
        return bërthamë_llogaritje(pk_read(skedar_dorezë, (void *)SECOND_VALUE, kodi_i_karakterit));
    case 3:
        llogaritje = kopjoj_shteg(첫째값, POZICIONI); if (llogaritje) return llogaritje;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (skedar_Listë[순번] < 0) {
            skedar_dorezë = pk_open(POZICIONI, (int)SECOND_VALUE, 0600);
            if (skedar_dorezë < 0) return -오류번호;
            skedar_Listë[순번] = skedar_dorezë; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { llogaritje = 통신끝점닫기(첫째값); if (!llogaritje) 통신끝점들[첫째값 - 32] = 0; return llogaritje; }
        skedar_dorezë = 대응파일기술자(첫째값); if (skedar_dorezë < 0) return -9;
        llogaritje = pk_close(skedar_dorezë); if (!llogaritje) skedar_Listë[첫째값 - 3] = -1;
        return bërthamë_llogaritje(llogaritje);
    case 5:
        skedar_dorezë = 대응파일기술자(첫째값); if (skedar_dorezë < 0) return -9;
        if (kodi_i_karakterit > 2) return -22;
        return bërthamë_llogaritje(pk_lseek(skedar_dorezë, (int64_t)SECOND_VALUE, kodi_i_karakterit));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 përdorues RW/NX 힙, 새로 노출되는 페이지는 0으로 filloj
        if (!첫째값) return 동적기억끝;
        if (첫째값 < përdorues_IMAGE_mbaroj || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + përmasat_e_faqes - 1) & ~(përmasat_e_faqes - 1);
        uintptr_t 새쪽들 = (첫째값 + përmasat_e_faqes - 1) & ~(përmasat_e_faqes - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t të_dhëna_pozicioni = 이전쪽들; të_dhëna_pozicioni < 새쪽들; të_dhëna_pozicioni += përmasat_e_faqes) struktura_e_faqes(të_dhëna_pozicioni, bërthamë_faqe, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t të_dhëna_pozicioni = 이전쪽들; të_dhëna_pozicioni < 새쪽들; të_dhëna_pozicioni += përmasat_e_faqes) struktura_e_faqes(të_dhëna_pozicioni, përdorues_lexoj_shkruaj, 3);
        } else {
            for (uintptr_t të_dhëna_pozicioni = 새쪽들; të_dhëna_pozicioni < 이전쪽들; të_dhëna_pozicioni += përmasat_e_faqes) {
                faqe_Listë[(të_dhëna_pozicioni - përdorues_BASE) / përmasat_e_faqes] = 0; Lejet_Listë[(të_dhëna_pozicioni - përdorues_BASE) / përmasat_e_faqes] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        skedar_dorezë = 대응파일기술자(첫째값); return skedar_dorezë < 0 ? -9 : bërthamë_llogaritje(pk_size(skedar_dorezë));
    case 10:
        skedar_dorezë = 대응파일기술자(첫째값); return skedar_dorezë < 0 ? -9 : bërthamë_llogaritje(pk_ftruncate(skedar_dorezë, (int64_t)SECOND_VALUE));
    case 11:
        llogaritje = kopjoj_shteg(첫째값, POZICIONI); return llogaritje ? llogaritje : bërthamë_llogaritje(pk_unlink(POZICIONI));
    case 12:
        skedar_dorezë = 대응파일기술자(첫째값); return skedar_dorezë < 0 ? -9 : bërthamë_llogaritje(pk_fsync(skedar_dorezë));
    case 13: { // 그래픽 기초 API: përdorues 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = skedar_futje->regjistroj_të_dhëna[3], 높이값 = skedar_futje->regjistroj_të_dhëna[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t Y_koordinatë = SECOND_VALUE; Y_koordinatë < SECOND_VALUE + 높이값; Y_koordinatë++) for (uintptr_t koordinata_x = 첫째값; koordinata_x < 첫째값 + 너비값; koordinata_x++) panel_pikëz(koordinata_x, Y_koordinatë, kodi_i_karakterit);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=njësi_COUNT; args(index,buffer,capacity)=UTF-8 gjatësi_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (kodi_i_karakterit <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;ndërvepruese=1;return panel_Terminali(13);}
        if(첫째값==2){ndërvepruese=0;return 0;}
        if(첫째값==3)return panel_Terminali(13);
        if(첫째값!=1||!ndërvepruese)return -22;
        llogaritje=(int32_t)보드글자읽기();
        if(llogaritje==-4096)return llogaritje;
        nis_TIMEOUT();return llogaritje<0?-11:llogaritje;
    case 17: { // 유한한 협력 Prit_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t mbaroj_Ora = Ora_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Ora_VALUE() < mbaroj_Ora);
        nis_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        llogaritje = kopjoj_shteg(첫째값, POZICIONI); if (llogaritje) return llogaritje;
        unsigned gjatësi_VALUE = 0; while (POZICIONI[gjatësi_VALUE]) gjatësi_VALUE++;
        llogaritje = 자바경로시작(gjatësi_VALUE); if (llogaritje < 0) return llogaritje;
        for (unsigned 순번 = 0; 순번 < gjatësi_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)POZICIONI[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int karakter_VALUE=(int32_t)보드글자읽기();if(karakter_VALUE==-4096)return karakter_VALUE;if(karakter_VALUE>=0)화면누름(pronari_objekt,karakter_VALUE);nis_TIMEOUT();}
        if(첫째값==3&&kodi_i_karakterit){if(!자바셸대화형())return -95;ndërvepruese=1;panel_Terminali(300);}
        return 화면호출(pronari_objekt,첫째값,SECOND_VALUE,kodi_i_karakterit,skedar_futje->regjistroj_të_dhëna[3],skedar_futje->regjistroj_të_dhëna[4],skedar_futje->regjistroj_të_dhëna[5]);
    case 21:
        if(kodi_i_karakterit>127)return -22;if(!사용자범위(SECOND_VALUE,kodi_i_karakterit*sizeof(uint32_t),0))return -14;
        return 화면글(pronari_objekt,첫째값,(const uint32_t *)SECOND_VALUE,kodi_i_karakterit);
    case 22: // 화면 Madhësi pyetja_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(kodi_i_karakterit==0||kodi_i_karakterit==6))llogaritje=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(kodi_i_karakterit==0||kodi_i_karakterit==IPPROTO_UDP))llogaritje=자바전문만들기(첫째값,SECOND_VALUE,kodi_i_karakterit);
        else return -93;
        if (llogaritje >= 32 && llogaritje < 56) 통신끝점들[llogaritje - 32] = 1;
        return llogaritje;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in email;
        llogaritje = 주소입력(SECOND_VALUE, kodi_i_karakterit, &email); if (llogaritje) return llogaritje;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(email.sin_addr.s_addr),pk_htons(email.sin_port)):자바전문묶기(첫째값, pk_htonl(email.sin_addr.s_addr), pk_htons(email.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (skedar_futje->regjistroj_të_dhëna[3]) return -95;
        if (kodi_i_karakterit > 512) return -90;
        if (kodi_i_karakterit && !사용자범위(SECOND_VALUE, kodi_i_karakterit, 0)) return -14;
        struct pk_sockaddr_in email;
        llogaritje = 주소입력(skedar_futje->regjistroj_të_dhëna[4], skedar_futje->regjistroj_të_dhëna[5], &email); if (llogaritje) return llogaritje;
        for (unsigned 순번 = 0; 순번 < kodi_i_karakterit; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(email.sin_addr.s_addr), pk_htons(email.sin_port), kodi_i_karakterit);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (skedar_futje->regjistroj_të_dhëna[3]) return -95;
        if (kodi_i_karakterit > 512) return -90;
        if (kodi_i_karakterit && !사용자범위(SECOND_VALUE, kodi_i_karakterit, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (skedar_futje->regjistroj_të_dhëna[4]) { llogaritje = 주소출력검사(skedar_futje->regjistroj_të_dhëna[4], skedar_futje->regjistroj_të_dhëna[5], &수용량); if (llogaritje) return llogaritje; }
        llogaritje = 자바전문받기(첫째값, kodi_i_karakterit); if (llogaritje < 0) return llogaritje;
        for (int 순번 = 0; 순번 < llogaritje; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (skedar_futje->regjistroj_të_dhëna[4]) 주소출력(skedar_futje->regjistroj_të_dhëna[4], skedar_futje->regjistroj_të_dhëna[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return llogaritje;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        llogaritje = 주소출력검사(SECOND_VALUE, kodi_i_karakterit, &수용량); if (llogaritje) return llogaritje;
        주소출력(SECOND_VALUE,kodi_i_karakterit,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in email;
        llogaritje=주소입력(SECOND_VALUE,kodi_i_karakterit,&email);if(llogaritje)return llogaritje;
        return 자바흐름연결(첫째값,pk_htonl(email.sin_addr.s_addr),pk_htons(email.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||kodi_i_karakterit)return -95;llogaritje=자바흐름연결받기(첫째값);if(llogaritje>=40&&llogaritje<56)통신끝점들[llogaritje-32]=1;return llogaritje;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(përdorues_kuadër *skedar_futje) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(skedar_futje) : 자체체계호출(skedar_futje);
}
static void Kthe_bërthamë(përdorues_kuadër *skedar_futje, int llogaritje) {
    Ndal_TIMEOUT();
    skedar_futje->regjistroj_të_dhëna[0] = (uint64_t)(int64_t)llogaritje;
    skedar_futje->komandë_pozicioni = (uintptr_t)përdorues_Kthe;
    skedar_futje->status_kod = 0x3c5; // EL1h, DAIF masked
}
int përdorues_përjashtim(përdorues_kuadër *skedar_futje, unsigned INTERCEPT) {
    if (!Aktiv || (skedar_futje->status_kod & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t 승인값 = makinë_regjistroj(IRQ_CPU_ndërfaqe + 0xc), identifikues_VALUE = 승인값 & 1023;
        if (identifikues_VALUE == 30) { Kthe_bërthamë(skedar_futje, përdorues_TIMEOUT); makinë_regjistroj(IRQ_CPU_ndërfaqe + 0x10) = 승인값; return 1; }
        if (identifikues_VALUE < 1020) makinë_regjistroj(IRQ_CPU_ndërfaqe + 0x10) = 승인값;
        return 1;
    }
    uint64_t përjashtim_status; __asm__ volatile("mrs %0, esr_el1" : "=r"(përjashtim_status));
    if (Ora_VALUE() >= 마감시각) { Kthe_bërthamë(skedar_futje, përdorues_TIMEOUT); return 1; }
    unsigned përjashtim_kategori = përjashtim_status >> 26;
    if (përjashtim_kategori == 0x15 && (përjashtim_status & 0xffff) == 0) {
        if (리눅스규약 ? skedar_futje->regjistroj_të_dhëna[8] == 93 || skedar_futje->regjistroj_të_dhëna[8] == 94 : skedar_futje->regjistroj_të_dhëna[8] == 6) Kthe_bërthamë(skedar_futje, (int)(skedar_futje->regjistroj_të_dhëna[0] & 255));
        else {
            intptr_t llogaritje=체계호출(skedar_futje);
            if(llogaritje==-4096&&ndërvepruese){
                저장값[pronari_objekt].실행틀=*skedar_futje;저장값[pronari_objekt].실행틀.komandë_pozicioni-=4;
                사용자실수보관(저장값[pronari_objekt].실수저장상태);Kthe_bërthamë(skedar_futje,사용자중단됨);
            }else skedar_futje->regjistroj_të_dhëna[0]=(uint64_t)llogaritje;
        }
    } else Kthe_bërthamë(skedar_futje, përjashtim_kategori == 0x24 ? përdorues_të_dhëna_gabim : përjashtim_kategori == 0x20 ? 사용자실행오류 : përdorues_i_pavlefshëm_instruksion);
    return 1;
}

// 생성된 const ELF grup_VALUE: 실행은 반드시 program_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *të_dhëna; size_t Madhësi; unsigned 전달값; } program;
#include "programs.h"
static void *foto_ekrani(unsigned pozicioni_INDEX){return (void *)(0x04000000ul+pozicioni_INDEX*(përdorues_mbaroj-përdorues_BASE));}
static int Përfundo_program(int llogaritje){
    사용자누적시각[pronari_objekt]+=(uint32_t)보드밀리초()-사용자실행시각[pronari_objekt];
    Ndal_TIMEOUT();Aktiv=0;
    if(llogaritje==사용자중단됨){
        저장된작업 *varg_të_dhëna=&저장값[pronari_objekt];varg_të_dhëna->멈춤상태=1;varg_të_dhëna->ndërvepruese=ndërvepruese;varg_të_dhëna->리눅스규약=리눅스규약;varg_të_dhëna->동적기억공간=동적기억끝;varg_të_dhëna->인수개수=전달인수개수;
        memcpy(varg_të_dhëna->Lejet_Listë,Lejet_Listë,sizeof(Lejet_Listë));memcpy(varg_të_dhëna->skedar_Listë,skedar_Listë,sizeof(skedar_Listë));memcpy(varg_të_dhëna->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(varg_të_dhëna->argument_ARRAY,전달인수,sizeof(전달인수));memcpy(varg_të_dhëna->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<përdorues_faqe_COUNT;순번++)if(Lejet_Listë[순번])memcpy((unsigned char *)foto_ekrani(pronari_objekt)+순번*përmasat_e_faqes,(void *)(përdorues_BASE+순번*përmasat_e_faqes),përmasat_e_faqes);
    }else{
        저장값[pronari_objekt].멈춤상태=0;화면초기화(pronari_objekt);
        for(unsigned 순번=0;순번<16;순번++)if(skedar_Listë[순번]>=0)pk_close(skedar_Listë[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<përdorues_faqe_COUNT;순번++){faqe_Listë[순번]=0;Lejet_Listë[순번]=0;}변환표맞추기();return llogaritje;
}
uintptr_t panel_kontroll_përdoruesi(uintptr_t Veprim){
    unsigned pozicioni_INDEX=Veprim&15;if(pozicioni_INDEX>=4||Aktiv)return (uint32_t)-22;
    저장된작업 *varg_të_dhëna=&저장값[pozicioni_INDEX];
    if(Veprim>=32){if(varg_të_dhëna->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(varg_të_dhëna->skedar_Listë[순번]>=0)pk_close(varg_të_dhëna->skedar_Listë[순번]);for(unsigned 순번=0;순번<24;순번++)if(varg_të_dhëna->통신끝점들[순번])통신끝점닫기(순번+32);}varg_të_dhëna->멈춤상태=0;화면초기화(pozicioni_INDEX);return 0;}
    if(Veprim>=16)return varg_të_dhëna->멈춤상태;
    if(!varg_të_dhëna->멈춤상태)return (uint32_t)-22;
    pronari_objekt=pozicioni_INDEX;ndërvepruese=varg_të_dhëna->ndërvepruese;리눅스규약=varg_të_dhëna->리눅스규약;동적기억끝=varg_të_dhëna->동적기억공간;전달인수개수=varg_të_dhëna->인수개수;
    memcpy(skedar_Listë,varg_të_dhëna->skedar_Listë,sizeof(skedar_Listë));memcpy(통신끝점들,varg_të_dhëna->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,varg_të_dhëna->argument_ARRAY,sizeof(전달인수));memcpy(전달인수길이,varg_të_dhëna->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<përdorues_faqe_COUNT;순번++)faqe_Listë[순번]=(përdorues_BASE+순번*përmasat_e_faqes)|bërthamë_faqe;변환표맞추기();
    memset((void *)përdorues_BASE,0,përdorues_mbaroj-përdorues_BASE);
    for(unsigned 순번=0;순번<përdorues_faqe_COUNT;순번++)if(varg_të_dhëna->Lejet_Listë[순번])memcpy((void *)(përdorues_BASE+순번*përmasat_e_faqes),(unsigned char *)foto_ekrani(pozicioni_INDEX)+순번*përmasat_e_faqes,përmasat_e_faqes);
    memcpy(Lejet_Listë,varg_të_dhëna->Lejet_Listë,sizeof(Lejet_Listë));
    for(unsigned 순번=0;순번<përdorues_faqe_COUNT;순번++){unsigned të_dhëna_pozicioni=Lejet_Listë[순번];faqe_Listë[순번]=të_dhëna_pozicioni?(përdorues_BASE+순번*përmasat_e_faqes)|(të_dhëna_pozicioni==3?përdorues_lexoj_shkruaj:të_dhëna_pozicioni==5?사용자읽고실행:përdorues_vetëm_për_lexim):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktiv=1;varg_të_dhëna->멈춤상태=0;nis_TIMEOUT();
    사용자실행시각[pronari_objekt]=보드밀리초();
    return (uint32_t)Përfundo_program(përdorues_CV(&varg_të_dhëna->실행틀,varg_të_dhëna->실수저장상태));
}
static int varg_program(const unsigned char *të_dhëna, size_t Madhësi, unsigned 전달값, int 리눅스방식, const char *Emër) {
    if (Aktiv) return -16;
    pronari_objekt=panel_Terminali(11);if(pronari_objekt<0||pronari_objekt>3||저장값[pronari_objekt].멈춤상태)return -16;ndërvepruese=0;
    int 유효함 = 실행파일검사(të_dhëna, Madhësi, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned emër_INDEX=0;
    while (*Emër && emër_INDEX<31) përdorues_komandë_emër[pronari_objekt][emër_INDEX++]=(unsigned char)*Emër++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (emër_INDEX) përdorues_komandë_emër[pronari_objekt][emër_INDEX++]=' ';
        for (unsigned pozicioni_INDEX=0; pozicioni_INDEX<전달인수길이[0]; pozicioni_INDEX++) përdorues_komandë_emër[pronari_objekt][emër_INDEX++]=전달인수[0][pozicioni_INDEX];
    }
    përdorues_komandë_emër[pronari_objekt][emër_INDEX]=0; numri_i_përdoruesit[pronari_objekt]=Tjetër_numri_i_përdoruesit++;
    if (Tjetër_numri_i_përdoruesit>0x7fffffffu) Tjetër_numri_i_përdoruesit=10;
    përdorues_nis_Ora[pronari_objekt]=보드밀리초(); 사용자누적시각[pronari_objekt]=0;
    for (unsigned 순번 = 0; 순번 < përdorues_faqe_COUNT; 순번++) faqe_Listë[순번] = (përdorues_BASE + 순번 * përmasat_e_faqes) | bërthamë_faqe;
    변환표맞추기();
    memset((void *)përdorues_BASE, 0, përdorues_mbaroj - përdorues_BASE);
    memset(Lejet_Listë, 0, sizeof(Lejet_Listë));
    실행파일머리 실행머리; memcpy(&실행머리, të_dhëna, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.program_Kreu_COUNT; 순번++) {
        실행파일구획 të_dhëna_pozicioni; memcpy(&të_dhëna_pozicioni, të_dhëna + 실행머리.program_Kreu_OFFSET + 순번 * sizeof(të_dhëna_pozicioni), sizeof(të_dhëna_pozicioni));
        if (të_dhëna_pozicioni.TYPE_kategori != 1 || !të_dhëna_pozicioni.기억영역크기) continue;
        if (të_dhëna_pozicioni.파일영역크기) memcpy((void *)(uintptr_t)të_dhëna_pozicioni.email, të_dhëna + të_dhëna_pozicioni.OFFSET_VALUE, të_dhëna_pozicioni.파일영역크기);
        for (uintptr_t 현재위치 = të_dhëna_pozicioni.email & ~(përmasat_e_faqes - 1); 현재위치 < të_dhëna_pozicioni.email + të_dhëna_pozicioni.기억영역크기; 현재위치 += përmasat_e_faqes) {
            Lejet_Listë[(현재위치 - përdorues_BASE) / përmasat_e_faqes] = (të_dhëna_pozicioni.konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond & 2) ? 3 : ((të_dhëna_pozicioni.konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = përdorues_Stivë_email; 현재위치 < përdorues_mbaroj; 현재위치 += përmasat_e_faqes) Lejet_Listë[(현재위치 - përdorues_BASE) / përmasat_e_faqes] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.futje_p) : përdorues_mbaroj;
    for (unsigned 순번 = 0; 순번 < përdorues_faqe_COUNT; 순번++) {
        unsigned autorizime = Lejet_Listë[순번];
        faqe_Listë[순번] = autorizime ? (përdorues_BASE + 순번 * përmasat_e_faqes) | (autorizime == 3 ? përdorues_lexoj_shkruaj : autorizime == 5 ? 사용자읽고실행 : përdorues_vetëm_për_lexim) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) skedar_Listë[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = përdorues_IMAGE_mbaroj;
    Aktiv = 1; nis_TIMEOUT();
    사용자실행시각[pronari_objekt]=보드밀리초();
    int llogaritje = përdorues_fut(실행머리.futje_p, 초기쌓임공간, 전달값);
    return Përfundo_program(llogaritje);
}
uintptr_t panel_përdorues_varg(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Emër=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)varg_program(실행항목들[LOOKUP_INDEX].të_dhëna, 실행항목들[LOOKUP_INDEX].Madhësi, 실행항목들[LOOKUP_INDEX].전달값, 0, Emër);
}
static uintptr_t zbatoj_skedar(int 리눅스방식) {
    static unsigned char IMAGE[16384];
    if (Aktiv || !전달인수개수) return (uint32_t)-22;
    int skedar_dorezë = pk_open((const char *)전달인수[0], vetëm_për_lexim_VALUE, 0);
    if (skedar_dorezë < 0) return (uint32_t)-오류번호;
    int Madhësi = pk_size(skedar_dorezë);
    if (Madhësi < 0 || (unsigned)Madhësi > sizeof(IMAGE)) { pk_close(skedar_dorezë); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(skedar_dorezë, IMAGE, Madhësi); pk_close(skedar_dorezë);
    if (RECEIVED_COUNT != Madhësi) return (uint32_t)-5;
    return (uint32_t)varg_program(IMAGE, Madhësi, 0, 리눅스방식, "");
}
uintptr_t panel_përdorues_skedar(void) { return zbatoj_skedar(0); }
uintptr_t 보드사용자리눅스파일(void) { return zbatoj_skedar(1); }
uintptr_t panel_përdorues_vlerësoj(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].të_dhëna, 잘못된실행항목들[순번].Madhësi) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
