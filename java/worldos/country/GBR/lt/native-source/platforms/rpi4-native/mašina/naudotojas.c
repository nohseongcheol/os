#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Vykdyti_komanda mašina sluoksnis_VALUE. Failas duomenys/정책은 기존 AOT Java 커널에 위임한다.
#include "naudotojas.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../tinklas_eilė/tinklas_eilė.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define mašina_registras(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_platintojas 0xff841000ul
#define IRQ_CPU_sąsaja 0xff842000ul
#define puslapio_formatas 4096ul
#define prieiga_žymeklis (1ul << 10)
#define Ne_Vykdyti_teisė (1ul << 53)
#define naudotojas_Ne_Vykdyti (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | prieiga_žymeklis)
#define branduolys_puslapis (3ul | 보통기억 | Ne_Vykdyti_teisė | naudotojas_Ne_Vykdyti)
#define 사용자읽고쓰기 (3ul | 보통기억 | (1ul << 6) | Ne_Vykdyti_teisė | naudotojas_Ne_Vykdyti)
#define naudotojas_tik_skaitomas (3ul | 보통기억 | (3ul << 6) | Ne_Vykdyti_teisė | naudotojas_Ne_Vykdyti)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | Ne_Vykdyti_teisė)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Lenta_pikselis(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Lenta_Terminalas(uintptr_t);
extern int Terminalas_laukiama(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int naudotojas_tęsti(naudotojas_kadras *,void *);
extern void 사용자실수보관(void *);
extern int naudotojas_įvesti(uintptr_t įrašas_p, uintptr_t eilė_Saugykla, uintptr_t 전달값);
extern void naudotojas_grąžinti(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t šaknis_ADDRESS[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t puslapis_Sąrašas[naudotojas_puslapis_COUNT] __attribute__((aligned(4096)));
static uint8_t Teisės_Sąrašas[naudotojas_puslapis_COUNT];
static int Aktyvus, Failas_Sąrašas[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned Failas_rodyklė){return Failas_rodyklė<40?자바전문닫기(Failas_rodyklė):자바흐름닫기(Failas_rodyklė);}
static uint64_t dažnis, terminas_TIME;
static uintptr_t 동적기억끝;
// branduolys_VALUE 셸이 준비한 UTF-8 Argumentai. EL0에는 kopijuoti_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,대화형,리눅스규약,Failas_Sąrašas[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argumentas_ARRAY[8][256],Teisės_Sąrašas[naudotojas_puslapis_COUNT];
    uintptr_t 동적기억공간; naudotojas_kadras 실행틀;
    unsigned char slankiojantis_p_Būsena[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int savininkas_objektas,대화형;
static uint32_t vartotojo_numeris[4], naudotojas_Start_TIME[4], 사용자누적시각[4], 사용자실행시각[4], toliau_vartotojo_numeris=10;
static unsigned char naudotojas_komanda_pavadinimas[4][288];
uint32_t 사용자상태읽기(unsigned įrašas_VALUE, unsigned INDEX) {
    unsigned vietos_rodyklė=INDEX&3;
    int Būsena_VALUE=(Aktyvus && savininkas_objektas==(int)vietos_rodyklė) ? 1 : 저장값[vietos_rodyklė].멈춤상태 ? 2 : 0;
    if (įrašas_VALUE==0) return Būsena_VALUE;
    if (!Būsena_VALUE) return 0;
    if (įrašas_VALUE==1) return vartotojo_numeris[vietos_rodyklė];
    if (įrašas_VALUE==2) {
        unsigned char *쪽들=Būsena_VALUE==1?Teisės_Sąrašas:저장값[vietos_rodyklė].Teisės_Sąrašas;
        unsigned puslapis_COUNT=0; for (unsigned 순번=0; 순번<naudotojas_puslapis_COUNT; 순번++) if(쪽들[순번]) puslapis_COUNT++;
        return puslapis_COUNT*4;
    }
    if (įrašas_VALUE==3) return (uint32_t)보드밀리초()-naudotojas_Start_TIME[vietos_rodyklė];
    if (įrašas_VALUE==4) return 사용자누적시각[vietos_rodyklė]+(Būsena_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[vietos_rodyklė]:0);
    if (įrašas_VALUE==5) return INDEX/4<sizeof(naudotojas_komanda_pavadinimas[0])?naudotojas_komanda_pavadinimas[vietos_rodyklė][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t įrašas_COUNT) {
    if (Aktyvus || įrašas_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = įrašas_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t dabartinis_padėtis, uintptr_t baitas_duomenys) {
    if (Aktyvus || LOOKUP_INDEX >= 전달인수개수 || dabartinis_padėtis >= 255 || dabartinis_padėtis != 전달인수길이[LOOKUP_INDEX] || !baitas_duomenys || baitas_duomenys > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][dabartinis_padėtis] = baitas_duomenys;
    전달인수길이[LOOKUP_INDEX] = dabartinis_padėtis + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t laikrodis_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stok_SKIRTASIS_LAIKAS(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    mašina_registras(IRQ_platintojas + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void Start_SKIRTASIS_LAIKAS(void) {
    uint64_t 간격 = dažnis * 2, įjungti = 1;
    terminas_TIME = laikrodis_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(įjungti) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned duomenų_blokas = 0; duomenų_blokas < 4; duomenų_blokas++) {
        šaknis_ADDRESS[duomenų_blokas] = (uintptr_t)가운데[duomenų_blokas] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t ADDRESS = ((uintptr_t)duomenų_blokas << 30) | ((uintptr_t)순번 << 21);
            가운데[duomenų_blokas][순번] = ADDRESS | 1 | prieiga_žymeklis | naudotojas_Ne_Vykdyti;
            if (ADDRESS >= 0xfc000000ul) 가운데[duomenų_blokas][순번] |= Ne_Vykdyti_teisė; // Device-nGnRnE
            else 가운데[duomenų_blokas][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < naudotojas_puslapis_COUNT / 512; SECOND_VALUE++)
        가운데[0][(naudotojas_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(puslapis_Sąrašas + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < naudotojas_puslapis_COUNT; 순번++) puslapis_Sąrašas[순번] = (naudotojas_BASE + 순번 * puslapio_formatas) | branduolys_puslapis;
    uint64_t atmintis_atributas_registras = 0x4400, ADDRESS_Vertimas_valdymas = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(atmintis_atributas_registras), "r"(ADDRESS_Vertimas_valdymas), "r"((uintptr_t)šaknis_ADDRESS) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t slankiojantis_p_Būsena = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(slankiojantis_p_Būsena) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(dažnis));
    Stok_SKIRTASIS_LAIKAS();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 įrašas_p_VALUE 때만 Leisti_VALUE.
    mašina_registras(IRQ_platintojas) = 0;
    mašina_registras(IRQ_platintojas + 0x180) = 0xffffffff;
    mašina_registras(IRQ_platintojas + 0x80) = 0xffffffff;
    mašina_registras(IRQ_platintojas + 0x280) = 1u << 30;
    mašina_registras(IRQ_platintojas + 0x41c) = 0x80808080;
    mašina_registras(IRQ_platintojas + 0x100) = 1u << 30;
    mašina_registras(IRQ_CPU_sąsaja + 4) = 0xff;
    mašina_registras(IRQ_CPU_sąsaja + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 numeris 있다.
    int Sauga = (mašina_registras(IRQ_platintojas + 4) & (1u << 10)) != 0;
    mašina_registras(IRQ_platintojas) = Sauga ? 1 : 3;
    mašina_registras(IRQ_CPU_sąsaja) = Sauga ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_sritis, mašina_TYPE; uint32_t versijos_numeris;
    uint64_t įrašas_p, programa_Antraštė_OFFSET, sekcijos_antraštė_OFFSET; uint32_t konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba;
    uint16_t 실행머리크기, programa_Antraštė_įrašas_dydis, programa_Antraštė_COUNT, sekcijos_antraštė_įrašas_dydis, sekcijos_antraštė_COUNT, sekcija_pavadinimas_lentelė_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_sritis, konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba; uint64_t OFFSET_VALUE, ADDRESS, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(naudotojas_kadras) == 272, "exception assembly layout");
static int 포함된범위(uint64_t OFFSET_VALUE, uint64_t Dydis, uint64_t baigti_pokalbį_OFFSET) {
    return OFFSET_VALUE <= baigti_pokalbį_OFFSET && Dydis <= baigti_pokalbį_OFFSET - OFFSET_VALUE;
}
static int 부가정보검사(const unsigned char *duomenys_padėtis, size_t Dydis) {
    size_t dabartinis_padėtis = 0;
    while (포함된범위(dabartinis_padėtis, 12, Dydis)) {
        uint32_t 낱말들[3]; memcpy(낱말들, duomenys_padėtis + dabartinis_padėtis, 12); dabartinis_padėtis += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(dabartinis_padėtis, 이름영역크기, Dydis) || !포함된범위(dabartinis_padėtis + 이름영역크기, 설명크기, Dydis)) return 0;
        const unsigned char Pavadinimas_2[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Pavadinimas_2) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Pavadinimas_2); 순번++) if (duomenys_padėtis[dabartinis_padėtis + 순번] != Pavadinimas_2[순번]) 일치 = 0;
        uint32_t versijos_numeris = 0;
        if (일치) memcpy(&versijos_numeris, duomenys_padėtis + dabartinis_padėtis + 이름영역크기, 4);
        if (일치 && versijos_numeris == 1) return 1;
        dabartinis_padėtis += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *duomenys, size_t Dydis, int 리눅스방식) {
    if (Dydis < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, duomenys, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_sritis != 2 || 실행머리.mašina_TYPE != 183 || 실행머리.versijos_numeris != 1 || 실행머리.konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.programa_Antraštė_įrašas_dydis != sizeof(실행파일구획) || !실행머리.programa_Antraštė_COUNT || 실행머리.programa_Antraštė_COUNT > 16 ||
        실행머리.programa_Antraštė_OFFSET < sizeof(실행머리) || !포함된범위(실행머리.programa_Antraštė_OFFSET, (uint64_t)실행머리.programa_Antraštė_COUNT * sizeof(실행파일구획), Dydis)) return 사용자실행파일오류;
    uint8_t 사용량[(naudotojas_IMAGE_baigti_pokalbį - naudotojas_BASE) / puslapio_formatas] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.programa_Antraštė_COUNT; 순번++) {
        실행파일구획 duomenys_padėtis; memcpy(&duomenys_padėtis, duomenys + 실행머리.programa_Antraštė_OFFSET + 순번 * sizeof(duomenys_padėtis), sizeof(duomenys_padėtis));
        if (duomenys_padėtis.TYPE_sritis == 4) {
            if (!포함된범위(duomenys_padėtis.OFFSET_VALUE, duomenys_padėtis.파일영역크기, Dydis)) return 사용자실행파일오류;
            if (부가정보검사(duomenys + duomenys_padėtis.OFFSET_VALUE, duomenys_padėtis.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (duomenys_padėtis.TYPE_sritis == 0 || duomenys_padėtis.TYPE_sritis == 6 || (duomenys_padėtis.TYPE_sritis == 0x6474e551 && !(duomenys_padėtis.konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba & 1))) continue;
        if (duomenys_padėtis.TYPE_sritis != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!duomenys_padėtis.기억영역크기) continue;
        if (duomenys_padėtis.konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba & ~7u || !(duomenys_padėtis.konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba & 4) || (duomenys_padėtis.konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba & 3) == 3 || duomenys_padėtis.파일영역크기 > duomenys_padėtis.기억영역크기 ||
            (duomenys_padėtis.파일영역크기 && !포함된범위(duomenys_padėtis.OFFSET_VALUE, duomenys_padėtis.파일영역크기, Dydis)) || duomenys_padėtis.ADDRESS < naudotojas_BASE ||
            !포함된범위(duomenys_padėtis.ADDRESS, duomenys_padėtis.기억영역크기, naudotojas_IMAGE_baigti_pokalbį) ||
            (!리눅스방식 && ((duomenys_padėtis.ADDRESS & (puslapio_formatas - 1)) || (duomenys_padėtis.OFFSET_VALUE & (puslapio_formatas - 1)) || duomenys_padėtis.맞춤 != puslapio_formatas)) ||
            (리눅스방식 && (((duomenys_padėtis.ADDRESS ^ duomenys_padėtis.OFFSET_VALUE) & (puslapio_formatas - 1)) || !duomenys_padėtis.맞춤 ||
                (duomenys_padėtis.맞춤 & (duomenys_padėtis.맞춤 - 1)) || duomenys_padėtis.맞춤 > 0x200000 || ((duomenys_padėtis.ADDRESS ^ duomenys_padėtis.OFFSET_VALUE) & (duomenys_padėtis.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (duomenys_padėtis.ADDRESS - naudotojas_BASE) / puslapio_formatas;
        unsigned įrašas_COUNT = ((duomenys_padėtis.ADDRESS & (puslapio_formatas - 1)) + duomenys_padėtis.기억영역크기 + puslapio_formatas - 1) / puslapio_formatas;
        for (unsigned puslapis_VALUE = 첫항목; puslapis_VALUE < 첫항목 + įrašas_COUNT; puslapis_VALUE++) {
            if (사용량[puslapis_VALUE]) return 사용자실행파일오류;
            사용량[puslapis_VALUE] = 1;
        }
        if ((duomenys_padėtis.konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba & 1) && 실행머리.įrašas_p >= duomenys_padėtis.ADDRESS && 실행머리.įrašas_p < duomenys_padėtis.ADDRESS + duomenys_padėtis.파일영역크기 && !(실행머리.įrašas_p & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *duomenys, size_t Dydis) { return 실행파일검사(duomenys, Dydis, 0); }
static void puslapio_maketas(uintptr_t ADDRESS, uint64_t konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba, unsigned teisės) {
    unsigned LOOKUP_INDEX = (ADDRESS - naudotojas_BASE) / puslapio_formatas;
    puslapis_Sąrašas[LOOKUP_INDEX] = ADDRESS | konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba;
    Teisės_Sąrašas[LOOKUP_INDEX] = teisės;
}
static int naudotojas_diapazonas(uintptr_t ADDRESS, size_t įrašas_COUNT, int 쓰는중) {
    if (ADDRESS < naudotojas_BASE || !포함된범위(ADDRESS, įrašas_COUNT, naudotojas_baigti_pokalbį)) return 0;
    if (!įrašas_COUNT) return 1;
    unsigned 첫항목 = (ADDRESS - naudotojas_BASE) / puslapio_formatas, 마지막 = (ADDRESS + įrašas_COUNT - 1 - naudotojas_BASE) / puslapio_formatas;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Teisės_Sąrašas[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int kopijuoti_kelias(uintptr_t ADDRESS, char *KELIAS) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!naudotojas_diapazonas(ADDRESS, 1, 0)) return -14;
        KELIAS[순번] = *(const char *)ADDRESS++;
        if (!KELIAS[순번]) return 0;
    }
    return -36;
}
static intptr_t branduolys_KR(intptr_t REZULTATAS) { return REZULTATAS < 0 ? -klaidos_numeris : REZULTATAS; }
static int 대응파일기술자(uint64_t Failas_rodyklė) { return Failas_rodyklė >= 3 && Failas_rodyklė < 19 ? Failas_Sąrašas[Failas_rodyklė - 3] : -1; }
static int 통신끝점소유(uint64_t Failas_rodyklė) { return Failas_rodyklė >= 32 && Failas_rodyklė < 56 && 통신끝점들[Failas_rodyklė - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t 길이, struct pk_sockaddr_in *ADDRESS) {
    if (길이 != sizeof(*ADDRESS)) return -22;
    if (!naudotojas_diapazonas(가리킴값, 길이, 0)) return -14;
    memcpy(ADDRESS, (const void *)가리킴값, sizeof(*ADDRESS));
    return ADDRESS->sin_family == AF_INET ? 0 : -97;
}
static int ADDRESS_išeiga_čekis(uintptr_t 가리킴값, uintptr_t 길이포인터, pk_socklen_t *kaupti_pajėgumas) {
    if (!naudotojas_diapazonas(길이포인터, sizeof(*kaupti_pajėgumas), 1)) return -14;
    memcpy(kaupti_pajėgumas, (const void *)길이포인터, sizeof(*kaupti_pajėgumas));
    if (*kaupti_pajėgumas > sizeof(struct pk_sockaddr_in)) *kaupti_pajėgumas = sizeof(struct pk_sockaddr_in);
    if (*kaupti_pajėgumas && !naudotojas_diapazonas(가리킴값, *kaupti_pajėgumas, 1)) return -14;
    return 0;
}
static void ADDRESS_išeiga(uintptr_t 가리킴값, uintptr_t 길이포인터, pk_socklen_t kaupti_pajėgumas, int ADDRESS, int prievado_numeris) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(prievado_numeris); VALUE.sin_addr.s_addr = pk_htonl(ADDRESS);
    if (kaupti_pajėgumas) memcpy((void *)가리킴값, &VALUE, kaupti_pajėgumas);
    pk_socklen_t 길이 = sizeof(VALUE); memcpy((void *)길이포인터, &길이, sizeof(길이));
}
extern uintptr_t Lenta_kanalas(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(naudotojas_kadras *Failas_įrašas) {
    uintptr_t 첫째값 = Failas_įrašas->registras_duomenys[0], SECOND_VALUE = Failas_įrašas->registras_duomenys[1], simbolio_kodas = Failas_įrašas->registras_duomenys[2];
    char KELIAS[65];
    int Failas_rodyklė, REZULTATAS;
    switch (Failas_įrašas->registras_duomenys[8]) {
    case 0: return 1; // savas ABI 버전
    case 1: // write: rodyklė 전체를 검사한 ATGAL_VALUE Išvestis/Failas keisti_VALUE
        if (simbolio_kodas > 65536) return -22;
        if (!naudotojas_diapazonas(SECOND_VALUE, simbolio_kodas, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t Start_išeiga=laikrodis_VALUE();
            for (size_t 순번 = 0; 순번 < simbolio_kodas; 순번++) Lenta_kanalas(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 branduolys_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(대화형){
                terminas_TIME+=laikrodis_VALUE()-Start_išeiga;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(terminas_TIME) : "memory");
            }
            return simbolio_kodas;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t prekė_COUNT=simbolio_kodas>512?512:simbolio_kodas;for(size_t 순번=0;순번<prekė_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,prekė_COUNT);
        }
        Failas_rodyklė = 대응파일기술자(첫째값); if (Failas_rodyklė < 0) return -9;
        return branduolys_KR(pk_write(Failas_rodyklė, (const void *)SECOND_VALUE, simbolio_kodas));
    case 2:
        if (simbolio_kodas > 65536) return -22;
        if (!naudotojas_diapazonas(SECOND_VALUE, simbolio_kodas, 1)) return -14;
        if (첫째값 == 0) {
            size_t prekė_COUNT = 0;
            while (prekė_COUNT < simbolio_kodas) {
                int simbolis_VALUE_068c2631 = (int32_t)보드글자읽기(); if (simbolis_VALUE_068c2631 == -2) return prekė_COUNT; if (simbolis_VALUE_068c2631 < 0) break;
                ((unsigned char *)SECOND_VALUE)[prekė_COUNT++] = simbolis_VALUE_068c2631;
            }
            return prekė_COUNT ? (intptr_t)prekė_COUNT : (simbolio_kodas ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            REZULTATAS=자바흐름읽기(첫째값,simbolio_kodas>512?512:simbolio_kodas);if(REZULTATAS>0)for(int 순번=0;순번<REZULTATAS;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return REZULTATAS;
        }
        Failas_rodyklė = 대응파일기술자(첫째값); if (Failas_rodyklė < 0) return -9;
        return branduolys_KR(pk_read(Failas_rodyklė, (void *)SECOND_VALUE, simbolio_kodas));
    case 3:
        REZULTATAS = kopijuoti_kelias(첫째값, KELIAS); if (REZULTATAS) return REZULTATAS;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (Failas_Sąrašas[순번] < 0) {
            Failas_rodyklė = pk_open(KELIAS, (int)SECOND_VALUE, 0600);
            if (Failas_rodyklė < 0) return -klaidos_numeris;
            Failas_Sąrašas[순번] = Failas_rodyklė; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { REZULTATAS = 통신끝점닫기(첫째값); if (!REZULTATAS) 통신끝점들[첫째값 - 32] = 0; return REZULTATAS; }
        Failas_rodyklė = 대응파일기술자(첫째값); if (Failas_rodyklė < 0) return -9;
        REZULTATAS = pk_close(Failas_rodyklė); if (!REZULTATAS) Failas_Sąrašas[첫째값 - 3] = -1;
        return branduolys_KR(REZULTATAS);
    case 5:
        Failas_rodyklė = 대응파일기술자(첫째값); if (Failas_rodyklė < 0) return -9;
        if (simbolio_kodas > 2) return -22;
        return branduolys_KR(pk_lseek(Failas_rodyklė, (int64_t)SECOND_VALUE, simbolio_kodas));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 naudotojas RW/NX 힙, 새로 노출되는 페이지는 0으로 초기화
        if (!첫째값) return 동적기억끝;
        if (첫째값 < naudotojas_IMAGE_baigti_pokalbį || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + puslapio_formatas - 1) & ~(puslapio_formatas - 1);
        uintptr_t 새쪽들 = (첫째값 + puslapio_formatas - 1) & ~(puslapio_formatas - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t duomenys_padėtis = 이전쪽들; duomenys_padėtis < 새쪽들; duomenys_padėtis += puslapio_formatas) puslapio_maketas(duomenys_padėtis, branduolys_puslapis, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t duomenys_padėtis = 이전쪽들; duomenys_padėtis < 새쪽들; duomenys_padėtis += puslapio_formatas) puslapio_maketas(duomenys_padėtis, 사용자읽고쓰기, 3);
        } else {
            for (uintptr_t duomenys_padėtis = 새쪽들; duomenys_padėtis < 이전쪽들; duomenys_padėtis += puslapio_formatas) {
                puslapis_Sąrašas[(duomenys_padėtis - naudotojas_BASE) / puslapio_formatas] = 0; Teisės_Sąrašas[(duomenys_padėtis - naudotojas_BASE) / puslapio_formatas] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        Failas_rodyklė = 대응파일기술자(첫째값); return Failas_rodyklė < 0 ? -9 : branduolys_KR(pk_size(Failas_rodyklė));
    case 10:
        Failas_rodyklė = 대응파일기술자(첫째값); return Failas_rodyklė < 0 ? -9 : branduolys_KR(pk_ftruncate(Failas_rodyklė, (int64_t)SECOND_VALUE));
    case 11:
        REZULTATAS = kopijuoti_kelias(첫째값, KELIAS); return REZULTATAS ? REZULTATAS : branduolys_KR(pk_unlink(KELIAS));
    case 12:
        Failas_rodyklė = 대응파일기술자(첫째값); return Failas_rodyklė < 0 ? -9 : branduolys_KR(pk_fsync(Failas_rodyklė));
    case 13: { // 그래픽 기초 API: naudotojas 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Failas_įrašas->registras_duomenys[3], 높이값 = Failas_įrašas->registras_duomenys[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t 세로좌표 = SECOND_VALUE; 세로좌표 < SECOND_VALUE + 높이값; 세로좌표++) for (uintptr_t x_koordinatė = 첫째값; x_koordinatė < 첫째값 + 너비값; x_koordinatė++) Lenta_pikselis(x_koordinatė, 세로좌표, simbolio_kodas);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=prekė_COUNT; args(index,buffer,capacity)=UTF-8 길이
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (simbolio_kodas <= 전달인수길이[첫째값]) return -36;
        if (!naudotojas_diapazonas(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;대화형=1;return Lenta_Terminalas(13);}
        if(첫째값==2){대화형=0;return 0;}
        if(첫째값==3)return Lenta_Terminalas(13);
        if(첫째값!=1||!대화형)return -22;
        REZULTATAS=(int32_t)보드글자읽기();
        if(REZULTATAS==-4096)return REZULTATAS;
        Start_SKIRTASIS_LAIKAS();return REZULTATAS<0?-11:REZULTATAS;
    case 17: { // 유한한 협력 Palauk_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t baigti_pokalbį_TIME = laikrodis_VALUE() + dažnis * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (laikrodis_VALUE() < baigti_pokalbį_TIME);
        Start_SKIRTASIS_LAIKAS(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 pirminis_VALUE·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        REZULTATAS = kopijuoti_kelias(첫째값, KELIAS); if (REZULTATAS) return REZULTATAS;
        unsigned 길이 = 0; while (KELIAS[길이]) 길이++;
        REZULTATAS = 자바경로시작(길이); if (REZULTATAS < 0) return REZULTATAS;
        for (unsigned 순번 = 0; 순번 < 길이; 순번++) 자바경로바이트(순번, (unsigned char)KELIAS[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int simbolis_VALUE_068c2631=(int32_t)보드글자읽기();if(simbolis_VALUE_068c2631==-4096)return simbolis_VALUE_068c2631;if(simbolis_VALUE_068c2631>=0)화면누름(savininkas_objektas,simbolis_VALUE_068c2631);Start_SKIRTASIS_LAIKAS();}
        if(첫째값==3&&simbolio_kodas){if(!자바셸대화형())return -95;대화형=1;Lenta_Terminalas(300);}
        return 화면호출(savininkas_objektas,첫째값,SECOND_VALUE,simbolio_kodas,Failas_įrašas->registras_duomenys[3],Failas_įrašas->registras_duomenys[4],Failas_įrašas->registras_duomenys[5]);
    case 21:
        if(simbolio_kodas>127)return -22;if(!naudotojas_diapazonas(SECOND_VALUE,simbolio_kodas*sizeof(uint32_t),0))return -14;
        return 화면글(savininkas_objektas,첫째값,(const uint32_t *)SECOND_VALUE,simbolio_kodas);
    case 22: // 화면 Dydis užklausa_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(simbolio_kodas==0||simbolio_kodas==6))REZULTATAS=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(simbolio_kodas==0||simbolio_kodas==IPPROTO_UDP))REZULTATAS=자바전문만들기(첫째값,SECOND_VALUE,simbolio_kodas);
        else return -93;
        if (REZULTATAS >= 32 && REZULTATAS < 56) 통신끝점들[REZULTATAS - 32] = 1;
        return REZULTATAS;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in ADDRESS;
        REZULTATAS = 주소입력(SECOND_VALUE, simbolio_kodas, &ADDRESS); if (REZULTATAS) return REZULTATAS;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(ADDRESS.sin_addr.s_addr),pk_htons(ADDRESS.sin_port)):자바전문묶기(첫째값, pk_htonl(ADDRESS.sin_addr.s_addr), pk_htons(ADDRESS.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Failas_įrašas->registras_duomenys[3]) return -95;
        if (simbolio_kodas > 512) return -90;
        if (simbolio_kodas && !naudotojas_diapazonas(SECOND_VALUE, simbolio_kodas, 0)) return -14;
        struct pk_sockaddr_in ADDRESS;
        REZULTATAS = 주소입력(Failas_įrašas->registras_duomenys[4], Failas_įrašas->registras_duomenys[5], &ADDRESS); if (REZULTATAS) return REZULTATAS;
        for (unsigned 순번 = 0; 순번 < simbolio_kodas; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(ADDRESS.sin_addr.s_addr), pk_htons(ADDRESS.sin_port), simbolio_kodas);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Failas_įrašas->registras_duomenys[3]) return -95;
        if (simbolio_kodas > 512) return -90;
        if (simbolio_kodas && !naudotojas_diapazonas(SECOND_VALUE, simbolio_kodas, 1)) return -14;
        pk_socklen_t kaupti_pajėgumas = 0;
        if (Failas_įrašas->registras_duomenys[4]) { REZULTATAS = ADDRESS_išeiga_čekis(Failas_įrašas->registras_duomenys[4], Failas_įrašas->registras_duomenys[5], &kaupti_pajėgumas); if (REZULTATAS) return REZULTATAS; }
        REZULTATAS = 자바전문받기(첫째값, simbolio_kodas); if (REZULTATAS < 0) return REZULTATAS;
        for (int 순번 = 0; 순번 < REZULTATAS; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (Failas_įrašas->registras_duomenys[4]) ADDRESS_išeiga(Failas_įrašas->registras_duomenys[4], Failas_įrašas->registras_duomenys[5], kaupti_pajėgumas, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return REZULTATAS;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t kaupti_pajėgumas;
        REZULTATAS = ADDRESS_išeiga_čekis(SECOND_VALUE, simbolio_kodas, &kaupti_pajėgumas); if (REZULTATAS) return REZULTATAS;
        ADDRESS_išeiga(SECOND_VALUE,simbolio_kodas,kaupti_pajėgumas,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in ADDRESS;
        REZULTATAS=주소입력(SECOND_VALUE,simbolio_kodas,&ADDRESS);if(REZULTATAS)return REZULTATAS;
        return 자바흐름연결(첫째값,pk_htonl(ADDRESS.sin_addr.s_addr),pk_htons(ADDRESS.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||simbolio_kodas)return -95;REZULTATAS=자바흐름연결받기(첫째값);if(REZULTATAS>=40&&REZULTATAS<56)통신끝점들[REZULTATAS-32]=1;return REZULTATAS;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(naudotojas_kadras *Failas_įrašas) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Failas_įrašas) : 자체체계호출(Failas_įrašas);
}
static void grąžinti_branduolys(naudotojas_kadras *Failas_įrašas, int REZULTATAS) {
    Stok_SKIRTASIS_LAIKAS();
    Failas_įrašas->registras_duomenys[0] = (uint64_t)(int64_t)REZULTATAS;
    Failas_įrašas->komanda_padėtis = (uintptr_t)naudotojas_grąžinti;
    Failas_įrašas->Būsena_CODE = 0x3c5; // EL1h, DAIF masked
}
int vartotojo_išimtinė_situacija(naudotojas_kadras *Failas_įrašas, unsigned INTERCEPT) {
    if (!Aktyvus || (Failas_įrašas->Būsena_CODE & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t patvirtinimas_VALUE = mašina_registras(IRQ_CPU_sąsaja + 0xc), identifikatorius_VALUE = patvirtinimas_VALUE & 1023;
        if (identifikatorius_VALUE == 30) { grąžinti_branduolys(Failas_įrašas, naudotojas_SKIRTASIS_LAIKAS); mašina_registras(IRQ_CPU_sąsaja + 0x10) = patvirtinimas_VALUE; return 1; }
        if (identifikatorius_VALUE < 1020) mašina_registras(IRQ_CPU_sąsaja + 0x10) = patvirtinimas_VALUE;
        return 1;
    }
    uint64_t išimtis_Būsena; __asm__ volatile("mrs %0, esr_el1" : "=r"(išimtis_Būsena));
    if (laikrodis_VALUE() >= terminas_TIME) { grąžinti_branduolys(Failas_įrašas, naudotojas_SKIRTASIS_LAIKAS); return 1; }
    unsigned išimtis_sritis = išimtis_Būsena >> 26;
    if (išimtis_sritis == 0x15 && (išimtis_Būsena & 0xffff) == 0) {
        if (리눅스규약 ? Failas_įrašas->registras_duomenys[8] == 93 || Failas_įrašas->registras_duomenys[8] == 94 : Failas_įrašas->registras_duomenys[8] == 6) grąžinti_branduolys(Failas_įrašas, (int)(Failas_įrašas->registras_duomenys[0] & 255));
        else {
            intptr_t REZULTATAS=체계호출(Failas_įrašas);
            if(REZULTATAS==-4096&&대화형){
                저장값[savininkas_objektas].실행틀=*Failas_įrašas;저장값[savininkas_objektas].실행틀.komanda_padėtis-=4;
                사용자실수보관(저장값[savininkas_objektas].slankiojantis_p_Būsena);grąžinti_branduolys(Failas_įrašas,사용자중단됨);
            }else Failas_įrašas->registras_duomenys[0]=(uint64_t)REZULTATAS;
        }
    } else grąžinti_branduolys(Failas_įrašas, išimtis_sritis == 0x24 ? 사용자자료오류 : išimtis_sritis == 0x20 ? 사용자실행오류 : 사용자잘못된명령);
    return 1;
}

// 생성된 const ELF Grupė_VALUE: 실행은 반드시 programa_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *duomenys; size_t Dydis; unsigned 전달값; } programa;
#include "programs.h"
static void *nuotrauka(unsigned vietos_rodyklė){return (void *)(0x04000000ul+vietos_rodyklė*(naudotojas_baigti_pokalbį-naudotojas_BASE));}
static int Baigti_programa(int REZULTATAS){
    사용자누적시각[savininkas_objektas]+=(uint32_t)보드밀리초()-사용자실행시각[savininkas_objektas];
    Stok_SKIRTASIS_LAIKAS();Aktyvus=0;
    if(REZULTATAS==사용자중단됨){
        저장된작업 *eilutė_duomenys=&저장값[savininkas_objektas];eilutė_duomenys->멈춤상태=1;eilutė_duomenys->대화형=대화형;eilutė_duomenys->리눅스규약=리눅스규약;eilutė_duomenys->동적기억공간=동적기억끝;eilutė_duomenys->인수개수=전달인수개수;
        memcpy(eilutė_duomenys->Teisės_Sąrašas,Teisės_Sąrašas,sizeof(Teisės_Sąrašas));memcpy(eilutė_duomenys->Failas_Sąrašas,Failas_Sąrašas,sizeof(Failas_Sąrašas));memcpy(eilutė_duomenys->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(eilutė_duomenys->argumentas_ARRAY,전달인수,sizeof(전달인수));memcpy(eilutė_duomenys->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<naudotojas_puslapis_COUNT;순번++)if(Teisės_Sąrašas[순번])memcpy((unsigned char *)nuotrauka(savininkas_objektas)+순번*puslapio_formatas,(void *)(naudotojas_BASE+순번*puslapio_formatas),puslapio_formatas);
    }else{
        저장값[savininkas_objektas].멈춤상태=0;화면초기화(savininkas_objektas);
        for(unsigned 순번=0;순번<16;순번++)if(Failas_Sąrašas[순번]>=0)pk_close(Failas_Sąrašas[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<naudotojas_puslapis_COUNT;순번++){puslapis_Sąrašas[순번]=0;Teisės_Sąrašas[순번]=0;}변환표맞추기();return REZULTATAS;
}
uintptr_t Lenta_vartotojo_valdiklis(uintptr_t Veiksmas){
    unsigned vietos_rodyklė=Veiksmas&15;if(vietos_rodyklė>=4||Aktyvus)return (uint32_t)-22;
    저장된작업 *eilutė_duomenys=&저장값[vietos_rodyklė];
    if(Veiksmas>=32){if(eilutė_duomenys->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(eilutė_duomenys->Failas_Sąrašas[순번]>=0)pk_close(eilutė_duomenys->Failas_Sąrašas[순번]);for(unsigned 순번=0;순번<24;순번++)if(eilutė_duomenys->통신끝점들[순번])통신끝점닫기(순번+32);}eilutė_duomenys->멈춤상태=0;화면초기화(vietos_rodyklė);return 0;}
    if(Veiksmas>=16)return eilutė_duomenys->멈춤상태;
    if(!eilutė_duomenys->멈춤상태)return (uint32_t)-22;
    savininkas_objektas=vietos_rodyklė;대화형=eilutė_duomenys->대화형;리눅스규약=eilutė_duomenys->리눅스규약;동적기억끝=eilutė_duomenys->동적기억공간;전달인수개수=eilutė_duomenys->인수개수;
    memcpy(Failas_Sąrašas,eilutė_duomenys->Failas_Sąrašas,sizeof(Failas_Sąrašas));memcpy(통신끝점들,eilutė_duomenys->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,eilutė_duomenys->argumentas_ARRAY,sizeof(전달인수));memcpy(전달인수길이,eilutė_duomenys->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<naudotojas_puslapis_COUNT;순번++)puslapis_Sąrašas[순번]=(naudotojas_BASE+순번*puslapio_formatas)|branduolys_puslapis;변환표맞추기();
    memset((void *)naudotojas_BASE,0,naudotojas_baigti_pokalbį-naudotojas_BASE);
    for(unsigned 순번=0;순번<naudotojas_puslapis_COUNT;순번++)if(eilutė_duomenys->Teisės_Sąrašas[순번])memcpy((void *)(naudotojas_BASE+순번*puslapio_formatas),(unsigned char *)nuotrauka(vietos_rodyklė)+순번*puslapio_formatas,puslapio_formatas);
    memcpy(Teisės_Sąrašas,eilutė_duomenys->Teisės_Sąrašas,sizeof(Teisės_Sąrašas));
    for(unsigned 순번=0;순번<naudotojas_puslapis_COUNT;순번++){unsigned duomenys_padėtis=Teisės_Sąrašas[순번];puslapis_Sąrašas[순번]=duomenys_padėtis?(naudotojas_BASE+순번*puslapio_formatas)|(duomenys_padėtis==3?사용자읽고쓰기:duomenys_padėtis==5?사용자읽고실행:naudotojas_tik_skaitomas):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktyvus=1;eilutė_duomenys->멈춤상태=0;Start_SKIRTASIS_LAIKAS();
    사용자실행시각[savininkas_objektas]=보드밀리초();
    return (uint32_t)Baigti_programa(naudotojas_tęsti(&eilutė_duomenys->실행틀,eilutė_duomenys->slankiojantis_p_Būsena));
}
static int vykdyti_programa(const unsigned char *duomenys, size_t Dydis, unsigned 전달값, int 리눅스방식, const char *Pavadinimas_2) {
    if (Aktyvus) return -16;
    savininkas_objektas=Lenta_Terminalas(11);if(savininkas_objektas<0||savininkas_objektas>3||저장값[savininkas_objektas].멈춤상태)return -16;대화형=0;
    int 유효함 = 실행파일검사(duomenys, Dydis, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned pavadinimas_INDEX=0;
    while (*Pavadinimas_2 && pavadinimas_INDEX<31) naudotojas_komanda_pavadinimas[savininkas_objektas][pavadinimas_INDEX++]=(unsigned char)*Pavadinimas_2++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (pavadinimas_INDEX) naudotojas_komanda_pavadinimas[savininkas_objektas][pavadinimas_INDEX++]=' ';
        for (unsigned vietos_rodyklė=0; vietos_rodyklė<전달인수길이[0]; vietos_rodyklė++) naudotojas_komanda_pavadinimas[savininkas_objektas][pavadinimas_INDEX++]=전달인수[0][vietos_rodyklė];
    }
    naudotojas_komanda_pavadinimas[savininkas_objektas][pavadinimas_INDEX]=0; vartotojo_numeris[savininkas_objektas]=toliau_vartotojo_numeris++;
    if (toliau_vartotojo_numeris>0x7fffffffu) toliau_vartotojo_numeris=10;
    naudotojas_Start_TIME[savininkas_objektas]=보드밀리초(); 사용자누적시각[savininkas_objektas]=0;
    for (unsigned 순번 = 0; 순번 < naudotojas_puslapis_COUNT; 순번++) puslapis_Sąrašas[순번] = (naudotojas_BASE + 순번 * puslapio_formatas) | branduolys_puslapis;
    변환표맞추기();
    memset((void *)naudotojas_BASE, 0, naudotojas_baigti_pokalbį - naudotojas_BASE);
    memset(Teisės_Sąrašas, 0, sizeof(Teisės_Sąrašas));
    실행파일머리 실행머리; memcpy(&실행머리, duomenys, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.programa_Antraštė_COUNT; 순번++) {
        실행파일구획 duomenys_padėtis; memcpy(&duomenys_padėtis, duomenys + 실행머리.programa_Antraštė_OFFSET + 순번 * sizeof(duomenys_padėtis), sizeof(duomenys_padėtis));
        if (duomenys_padėtis.TYPE_sritis != 1 || !duomenys_padėtis.기억영역크기) continue;
        if (duomenys_padėtis.파일영역크기) memcpy((void *)(uintptr_t)duomenys_padėtis.ADDRESS, duomenys + duomenys_padėtis.OFFSET_VALUE, duomenys_padėtis.파일영역크기);
        for (uintptr_t dabartinis_padėtis = duomenys_padėtis.ADDRESS & ~(puslapio_formatas - 1); dabartinis_padėtis < duomenys_padėtis.ADDRESS + duomenys_padėtis.기억영역크기; dabartinis_padėtis += puslapio_formatas) {
            Teisės_Sąrašas[(dabartinis_padėtis - naudotojas_BASE) / puslapio_formatas] = (duomenys_padėtis.konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba & 2) ? 3 : ((duomenys_padėtis.konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba & 1) ? 5 : 1);
        }
    }
    for (uintptr_t dabartinis_padėtis = naudotojas_eilė_ADDRESS; dabartinis_padėtis < naudotojas_baigti_pokalbį; dabartinis_padėtis += puslapio_formatas) Teisės_Sąrašas[(dabartinis_padėtis - naudotojas_BASE) / puslapio_formatas] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.įrašas_p) : naudotojas_baigti_pokalbį;
    for (unsigned 순번 = 0; 순번 < naudotojas_puslapis_COUNT; 순번++) {
        unsigned teisės = Teisės_Sąrašas[순번];
        puslapis_Sąrašas[순번] = teisės ? (naudotojas_BASE + 순번 * puslapio_formatas) | (teisės == 3 ? 사용자읽고쓰기 : teisės == 5 ? 사용자읽고실행 : naudotojas_tik_skaitomas) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) Failas_Sąrašas[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = naudotojas_IMAGE_baigti_pokalbį;
    Aktyvus = 1; Start_SKIRTASIS_LAIKAS();
    사용자실행시각[savininkas_objektas]=보드밀리초();
    int REZULTATAS = naudotojas_įvesti(실행머리.įrašas_p, 초기쌓임공간, 전달값);
    return Baigti_programa(REZULTATAS);
}
uintptr_t Lenta_naudotojas_vykdyti(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Pavadinimas_2=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)vykdyti_programa(실행항목들[LOOKUP_INDEX].duomenys, 실행항목들[LOOKUP_INDEX].Dydis, 실행항목들[LOOKUP_INDEX].전달값, 0, Pavadinimas_2);
}
static uintptr_t Vykdyti_Failas(int 리눅스방식) {
    static unsigned char IMAGE[16384];
    if (Aktyvus || !전달인수개수) return (uint32_t)-22;
    int Failas_rodyklė = pk_open((const char *)전달인수[0], tik_skaitomas_VALUE, 0);
    if (Failas_rodyklė < 0) return (uint32_t)-klaidos_numeris;
    int Dydis = pk_size(Failas_rodyklė);
    if (Dydis < 0 || (unsigned)Dydis > sizeof(IMAGE)) { pk_close(Failas_rodyklė); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(Failas_rodyklė, IMAGE, Dydis); pk_close(Failas_rodyklė);
    if (RECEIVED_COUNT != Dydis) return (uint32_t)-5;
    return (uint32_t)vykdyti_programa(IMAGE, Dydis, 0, 리눅스방식, "");
}
uintptr_t Lenta_naudotojas_Failas(void) { return Vykdyti_Failas(0); }
uintptr_t 보드사용자리눅스파일(void) { return Vykdyti_Failas(1); }
uintptr_t Lenta_naudotojas_tikrinti(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].duomenys, 잘못된실행항목들[순번].Dydis) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
