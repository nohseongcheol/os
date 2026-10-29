#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 végrehajt_parancs gép réteg_ÉRTÉK. Fájl adat/정책은 기존 AOT Java 커널에 위임한다.
#include "felhasználó.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../hálózat_Sor/hálózat_Sor.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define gép_jegyzék(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define megszakítás_terjesztő 0xff841000ul
#define megszakítás_CPU_csatoló 0xff842000ul
#define oldalméret 4096ul
#define hozzáfér_jelölő (1ul << 10)
#define nem_végrehajt_engedély (1ul << 53)
#define felhasználó_nem_végrehajt (1ul << 54)
#define normál_Memória ((1ul << 2) | (3ul << 8) | hozzáfér_jelölő)
#define kernel_lap (3ul | normál_Memória | nem_végrehajt_engedély | felhasználó_nem_végrehajt)
#define 사용자읽고쓰기 (3ul | normál_Memória | (1ul << 6) | nem_végrehajt_engedély | felhasználó_nem_végrehajt)
#define felhasználó_írásvédett (3ul | normál_Memória | (3ul << 6) | nem_végrehajt_engedély | felhasználó_nem_végrehajt)
#define 사용자읽고실행 (3ul | normál_Memória | (3ul << 6) | nem_végrehajt_engedély)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t fal_képpont(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t fal_Terminál(uintptr_t);
extern int Terminál_Függő(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int felhasználó_CV(felhasználó_doboz *,void *);
extern void 사용자실수보관(void *);
extern int felhasználó_megad(uintptr_t belépési_pont, uintptr_t Sor_tár, uintptr_t 전달값);
extern void felhasználó_visszaküld(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t gyök_CÍM[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t lap_Lista[felhasználó_lap_DARAB] __attribute__((aligned(4096)));
static uint8_t Engedélyek_Lista[felhasználó_lap_DARAB];
static int Aktív, fájllista[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int bezár_szoftvercsatorna_végpont(unsigned fájlleíró){return fájlleíró<40?자바전문닫기(fájlleíró):자바흐름닫기(fájlleíró);}
static uint64_t GYAKORISÁG, határidő_IDŐ;
static uintptr_t halommemória_megszüntet;
// kernel_ÉRTÉK 셸이 준비한 UTF-8 Argumentumok. EL0에는 másol_ÉRTÉK 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int felfüggesztve_Állapot,interaktív,리눅스규약,fájllista[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argumentum_TÖMB[8][256],Engedélyek_Lista[felhasználó_lap_DARAB];
    uintptr_t halommemória_tár; felhasználó_doboz végrehajtás_doboz;
    unsigned char lebegőpontos_szám_Állapot[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int tulajdonos_objektum,interaktív;
static uint32_t felhasználói_szám[4], felhasználó_START_IDŐ[4], 사용자누적시각[4], felhasználó_végrehajtás_IDŐ[4], Tovább_felhasználói_szám=10;
static unsigned char felhasználó_parancs_név[4][288];
uint32_t 사용자상태읽기(unsigned bejegyzés_ÉRTÉK, unsigned INDEX) {
    unsigned helyzetindex=INDEX&3;
    int Állapot_ÉRTÉK=(Aktív && tulajdonos_objektum==(int)helyzetindex) ? 1 : 저장값[helyzetindex].felfüggesztve_Állapot ? 2 : 0;
    if (bejegyzés_ÉRTÉK==0) return Állapot_ÉRTÉK;
    if (!Állapot_ÉRTÉK) return 0;
    if (bejegyzés_ÉRTÉK==1) return felhasználói_szám[helyzetindex];
    if (bejegyzés_ÉRTÉK==2) {
        unsigned char *쪽들=Állapot_ÉRTÉK==1?Engedélyek_Lista:저장값[helyzetindex].Engedélyek_Lista;
        unsigned lap_DARAB=0; for (unsigned 순번=0; 순번<felhasználó_lap_DARAB; 순번++) if(쪽들[순번]) lap_DARAB++;
        return lap_DARAB*4;
    }
    if (bejegyzés_ÉRTÉK==3) return (uint32_t)보드밀리초()-felhasználó_START_IDŐ[helyzetindex];
    if (bejegyzés_ÉRTÉK==4) return 사용자누적시각[helyzetindex]+(Állapot_ÉRTÉK==1?(uint32_t)보드밀리초()-felhasználó_végrehajtás_IDŐ[helyzetindex]:0);
    if (bejegyzés_ÉRTÉK==5) return INDEX/4<sizeof(felhasználó_parancs_név[0])?felhasználó_parancs_név[helyzetindex][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t bejegyzés_DARAB) {
    if (Aktív || bejegyzés_DARAB > 8) return (uint32_t)-22;
    전달인수개수 = bejegyzés_DARAB;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t KERES_INDEX, uintptr_t aktuális_pozíció, uintptr_t bájt_adat) {
    if (Aktív || KERES_INDEX >= 전달인수개수 || aktuális_pozíció >= 255 || aktuális_pozíció != 전달인수길이[KERES_INDEX] || !bájt_adat || bájt_adat > 255)
        return (uint32_t)-22;
    전달인수[KERES_INDEX][aktuális_pozíció] = bájt_adat;
    전달인수길이[KERES_INDEX] = aktuális_pozíció + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Óra_ÉRTÉK(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Állj_IDŐTÚLLÉPÉS(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    gép_jegyzék(megszakítás_terjesztő + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_IDŐTÚLLÉPÉS(void) {
    uint64_t 간격 = GYAKORISÁG * 2, bekapcsol = 1;
    határidő_IDŐ = Óra_ÉRTÉK() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(bekapcsol) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned adatblokk = 0; adatblokk < 4; adatblokk++) {
        gyök_CÍM[adatblokk] = (uintptr_t)가운데[adatblokk] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t CÍM = ((uintptr_t)adatblokk << 30) | ((uintptr_t)순번 << 21);
            가운데[adatblokk][순번] = CÍM | 1 | hozzáfér_jelölő | felhasználó_nem_végrehajt;
            if (CÍM >= 0xfc000000ul) 가운데[adatblokk][순번] |= nem_végrehajt_engedély; // Device-nGnRnE
            else 가운데[adatblokk][순번] |= normál_Memória; // Normal, non-cacheable
        }
    }
    for (unsigned MPERC_ÉRTÉK = 0; MPERC_ÉRTÉK < felhasználó_lap_DARAB / 512; MPERC_ÉRTÉK++)
        가운데[0][(felhasználó_ALAP >> 21) + MPERC_ÉRTÉK] = (uintptr_t)(lap_Lista + MPERC_ÉRTÉK * 512) | 3;
    for (unsigned 순번 = 0; 순번 < felhasználó_lap_DARAB; 순번++) lap_Lista[순번] = (felhasználó_ALAP + 순번 * oldalméret) | kernel_lap;
    uint64_t Memória_attribútum_jegyzék = 0x4400, CÍM_Fordítás_vezérlő = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Memória_attribútum_jegyzék), "r"(CÍM_Fordítás_vezérlő), "r"((uintptr_t)gyök_CÍM) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t lebegőpontos_szám_Állapot = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(lebegőpontos_szám_Állapot) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(GYAKORISÁG));
    Állj_IDŐTÚLLÉPÉS();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 belépési_pont_ÉRTÉK 때만 engedélyez_ÉRTÉK.
    gép_jegyzék(megszakítás_terjesztő) = 0;
    gép_jegyzék(megszakítás_terjesztő + 0x180) = 0xffffffff;
    gép_jegyzék(megszakítás_terjesztő + 0x80) = 0xffffffff;
    gép_jegyzék(megszakítás_terjesztő + 0x280) = 1u << 30;
    gép_jegyzék(megszakítás_terjesztő + 0x41c) = 0x80808080;
    gép_jegyzék(megszakítás_terjesztő + 0x100) = 1u << 30;
    gép_jegyzék(megszakítás_CPU_csatoló + 4) = 0xff;
    gép_jegyzék(megszakítás_CPU_csatoló + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 informatikai_részleg_normál 확인할 szám 있다.
    int Biztonság = (gép_jegyzék(megszakítás_terjesztő + 4) & (1u << 10)) != 0;
    gép_jegyzék(megszakítás_terjesztő) = Biztonság ? 1 : 3;
    gép_jegyzék(megszakítás_CPU_csatoló) = Biztonság ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t beír_terület, gép_beír; uint32_t verziószám;
    uint64_t belépési_pont, app_fejléc_Ofszet, szakaszfejléc_Ofszet; uint32_t konfiguráció_BITS;
    uint16_t végrehajtható_fejléc_méretez, app_fejléc_bejegyzés_méretez, app_fejléc_DARAB, szakaszfejléc_bejegyzés_méretez, szakaszfejléc_DARAB, szakasz_név_tábla_INDEX;
} 실행파일머리;
typedef struct { uint32_t beír_terület, konfiguráció_BITS; uint64_t Ofszet_ÉRTÉK, CÍM, 물리주소, 파일영역크기, 기억영역크기, igazít_határ; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(felhasználó_doboz) == 272, "exception assembly layout");
static int 포함된범위(uint64_t Ofszet_ÉRTÉK, uint64_t Méret, uint64_t megszüntet_Ofszet) {
    return Ofszet_ÉRTÉK <= megszüntet_Ofszet && Méret <= megszüntet_Ofszet - Ofszet_ÉRTÉK;
}
static int 부가정보검사(const unsigned char *adat_pozíció, size_t Méret) {
    size_t aktuális_pozíció = 0;
    while (포함된범위(aktuális_pozíció, 12, Méret)) {
        uint32_t 낱말들[3]; memcpy(낱말들, adat_pozíció + aktuális_pozíció, 12); aktuális_pozíció += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(aktuális_pozíció, 이름영역크기, Méret) || !포함된범위(aktuális_pozíció + 이름영역크기, 설명크기, Méret)) return 0;
        const unsigned char Név[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Név) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Név); 순번++) if (adat_pozíció[aktuális_pozíció + 순번] != Név[순번]) 일치 = 0;
        uint32_t verziószám = 0;
        if (일치) memcpy(&verziószám, adat_pozíció + aktuális_pozíció + 이름영역크기, 4);
        if (일치 && verziószám == 1) return 1;
        aktuális_pozíció += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *adat, size_t Méret, int 리눅스방식) {
    if (Méret < sizeof(실행파일머리)) return felhasználó_végrehajtható_hiba;
    실행파일머리 végrehajtható_fejléc; memcpy(&végrehajtható_fejléc, adat, sizeof(végrehajtható_fejléc));
    if (végrehajtható_fejléc.형식식별[0] != 127 || végrehajtható_fejléc.형식식별[1] != 'E' || végrehajtható_fejléc.형식식별[2] != 'L' || végrehajtható_fejléc.형식식별[3] != 'F' ||
        végrehajtható_fejléc.형식식별[4] != 2 || végrehajtható_fejléc.형식식별[5] != 1 || végrehajtható_fejléc.형식식별[6] != 1 || (végrehajtható_fejléc.형식식별[7] != 0 && (!리눅스방식 || végrehajtható_fejléc.형식식별[7] != 3)) ||
        végrehajtható_fejléc.beír_terület != 2 || végrehajtható_fejléc.gép_beír != 183 || végrehajtható_fejléc.verziószám != 1 || végrehajtható_fejléc.konfiguráció_BITS || végrehajtható_fejléc.végrehajtható_fejléc_méretez != sizeof(végrehajtható_fejléc) ||
        végrehajtható_fejléc.app_fejléc_bejegyzés_méretez != sizeof(실행파일구획) || !végrehajtható_fejléc.app_fejléc_DARAB || végrehajtható_fejléc.app_fejléc_DARAB > 16 ||
        végrehajtható_fejléc.app_fejléc_Ofszet < sizeof(végrehajtható_fejléc) || !포함된범위(végrehajtható_fejléc.app_fejléc_Ofszet, (uint64_t)végrehajtható_fejléc.app_fejléc_DARAB * sizeof(실행파일구획), Méret)) return felhasználó_végrehajtható_hiba;
    uint8_t 사용량[(felhasználó_KÉP_megszüntet - felhasználó_ALAP) / oldalméret] = {0};
    int érvényes_belépési_pont = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < végrehajtható_fejléc.app_fejléc_DARAB; 순번++) {
        실행파일구획 adat_pozíció; memcpy(&adat_pozíció, adat + végrehajtható_fejléc.app_fejléc_Ofszet + 순번 * sizeof(adat_pozíció), sizeof(adat_pozíció));
        if (adat_pozíció.beír_terület == 4) {
            if (!포함된범위(adat_pozíció.Ofszet_ÉRTÉK, adat_pozíció.파일영역크기, Méret)) return felhasználó_végrehajtható_hiba;
            if (부가정보검사(adat + adat_pozíció.Ofszet_ÉRTÉK, adat_pozíció.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (adat_pozíció.beír_terület == 0 || adat_pozíció.beír_terület == 6 || (adat_pozíció.beír_terület == 0x6474e551 && !(adat_pozíció.konfiguráció_BITS & 1))) continue;
        if (adat_pozíció.beír_terület != 1) return felhasználó_végrehajtható_hiba; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!adat_pozíció.기억영역크기) continue;
        if (adat_pozíció.konfiguráció_BITS & ~7u || !(adat_pozíció.konfiguráció_BITS & 4) || (adat_pozíció.konfiguráció_BITS & 3) == 3 || adat_pozíció.파일영역크기 > adat_pozíció.기억영역크기 ||
            (adat_pozíció.파일영역크기 && !포함된범위(adat_pozíció.Ofszet_ÉRTÉK, adat_pozíció.파일영역크기, Méret)) || adat_pozíció.CÍM < felhasználó_ALAP ||
            !포함된범위(adat_pozíció.CÍM, adat_pozíció.기억영역크기, felhasználó_KÉP_megszüntet) ||
            (!리눅스방식 && ((adat_pozíció.CÍM & (oldalméret - 1)) || (adat_pozíció.Ofszet_ÉRTÉK & (oldalméret - 1)) || adat_pozíció.igazít_határ != oldalméret)) ||
            (리눅스방식 && (((adat_pozíció.CÍM ^ adat_pozíció.Ofszet_ÉRTÉK) & (oldalméret - 1)) || !adat_pozíció.igazít_határ ||
                (adat_pozíció.igazít_határ & (adat_pozíció.igazít_határ - 1)) || adat_pozíció.igazít_határ > 0x200000 || ((adat_pozíció.CÍM ^ adat_pozíció.Ofszet_ÉRTÉK) & (adat_pozíció.igazít_határ - 1))))) return felhasználó_végrehajtható_hiba;
        unsigned 첫항목 = (adat_pozíció.CÍM - felhasználó_ALAP) / oldalméret;
        unsigned bejegyzés_DARAB = ((adat_pozíció.CÍM & (oldalméret - 1)) + adat_pozíció.기억영역크기 + oldalméret - 1) / oldalméret;
        for (unsigned lap_ÉRTÉK = 첫항목; lap_ÉRTÉK < 첫항목 + bejegyzés_DARAB; lap_ÉRTÉK++) {
            if (사용량[lap_ÉRTÉK]) return felhasználó_végrehajtható_hiba;
            사용량[lap_ÉRTÉK] = 1;
        }
        if ((adat_pozíció.konfiguráció_BITS & 1) && végrehajtható_fejléc.belépési_pont >= adat_pozíció.CÍM && végrehajtható_fejléc.belépési_pont < adat_pozíció.CÍM + adat_pozíció.파일영역크기 && !(végrehajtható_fejléc.belépési_pont & 3)) érvényes_belépési_pont = 1;
        적재구획++;
    }
    return érvényes_belépési_pont && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : felhasználó_végrehajtható_hiba;
}
int 사용자실행파일검사(const unsigned char *adat, size_t Méret) { return 실행파일검사(adat, Méret, 0); }
static void oldalelrendezés(uintptr_t CÍM, uint64_t konfiguráció_BITS, unsigned engedélyek) {
    unsigned KERES_INDEX = (CÍM - felhasználó_ALAP) / oldalméret;
    lap_Lista[KERES_INDEX] = CÍM | konfiguráció_BITS;
    Engedélyek_Lista[KERES_INDEX] = engedélyek;
}
static int felhasználó_tartomány(uintptr_t CÍM, size_t bejegyzés_DARAB, int 쓰는중) {
    if (CÍM < felhasználó_ALAP || !포함된범위(CÍM, bejegyzés_DARAB, felhasználó_megszüntet)) return 0;
    if (!bejegyzés_DARAB) return 1;
    unsigned 첫항목 = (CÍM - felhasználó_ALAP) / oldalméret, 마지막 = (CÍM + bejegyzés_DARAB - 1 - felhasználó_ALAP) / oldalméret;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Engedélyek_Lista[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int másol_útvonal(uintptr_t CÍM, char *ÚTVONAL) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!felhasználó_tartomány(CÍM, 1, 0)) return -14;
        ÚTVONAL[순번] = *(const char *)CÍM++;
        if (!ÚTVONAL[순번]) return 0;
    }
    return -36;
}
static intptr_t kernel_KR(intptr_t KR) { return KR < 0 ? -hibaszám : KR; }
static int 대응파일기술자(uint64_t fájlleíró) { return fájlleíró >= 3 && fájlleíró < 19 ? fájllista[fájlleíró - 3] : -1; }
static int szoftvercsatorna_végpont_tulajdonos(uint64_t fájlleíró) { return fájlleíró >= 32 && fájlleíró < 56 && 통신끝점들[fájlleíró - 32]; }
static int CÍM_bevitel(uintptr_t 가리킴값, size_t hossz_ÉRTÉK, struct pk_sockaddr_in *CÍM) {
    if (hossz_ÉRTÉK != sizeof(*CÍM)) return -22;
    if (!felhasználó_tartomány(가리킴값, hossz_ÉRTÉK, 0)) return -14;
    memcpy(CÍM, (const void *)가리킴값, sizeof(*CÍM));
    return CÍM->sin_family == AF_INET ? 0 : -97;
}
static int CÍM_kimenet_csekk(uintptr_t 가리킴값, uintptr_t hossz_mutató, pk_socklen_t *puffer_kapacitás) {
    if (!felhasználó_tartomány(hossz_mutató, sizeof(*puffer_kapacitás), 1)) return -14;
    memcpy(puffer_kapacitás, (const void *)hossz_mutató, sizeof(*puffer_kapacitás));
    if (*puffer_kapacitás > sizeof(struct pk_sockaddr_in)) *puffer_kapacitás = sizeof(struct pk_sockaddr_in);
    if (*puffer_kapacitás && !felhasználó_tartomány(가리킴값, *puffer_kapacitás, 1)) return -14;
    return 0;
}
static void CÍM_kimenet(uintptr_t 가리킴값, uintptr_t hossz_mutató, pk_socklen_t puffer_kapacitás, int CÍM, int portszám) {
    struct pk_sockaddr_in ÉRTÉK; memset(&ÉRTÉK, 0, sizeof(ÉRTÉK));
    ÉRTÉK.sin_family = AF_INET; ÉRTÉK.sin_port = pk_htons(portszám); ÉRTÉK.sin_addr.s_addr = pk_htonl(CÍM);
    if (puffer_kapacitás) memcpy((void *)가리킴값, &ÉRTÉK, puffer_kapacitás);
    pk_socklen_t hossz_ÉRTÉK = sizeof(ÉRTÉK); memcpy((void *)hossz_mutató, &hossz_ÉRTÉK, sizeof(hossz_ÉRTÉK));
}
extern uintptr_t fal_Csatorna(uintptr_t, uintptr_t);
static intptr_t natív_Rendszer_hív(felhasználó_doboz *Fájl_bejegyzés) {
    uintptr_t 첫째값 = Fájl_bejegyzés->jegyzék_adat[0], MPERC_ÉRTÉK = Fájl_bejegyzés->jegyzék_adat[1], kódpont = Fájl_bejegyzés->jegyzék_adat[2];
    char ÚTVONAL[65];
    int fájlleíró, KR;
    switch (Fájl_bejegyzés->jegyzék_adat[8]) {
    case 0: return 1; // saját ABI 버전
    case 1: // write: mutató 전체를 검사한 BACK_ÉRTÉK Kimenet/Fájl módosítás_ÉRTÉK
        if (kódpont > 65536) return -22;
        if (!felhasználó_tartomány(MPERC_ÉRTÉK, kódpont, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t START_kimenet=Óra_ÉRTÉK();
            for (size_t 순번 = 0; 순번 < kódpont; 순번++) fal_Csatorna(첫째값, ((const unsigned char *)MPERC_ÉRTÉK)[순번]);
            /* 큰 tty를 그린 kernel_ÉRTÉK 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interaktív){
                határidő_IDŐ+=Óra_ÉRTÉK()-START_kimenet;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(határidő_IDŐ) : "memory");
            }
            return kódpont;
        }
        if(첫째값>=40&&szoftvercsatorna_végpont_tulajdonos(첫째값)){
            size_t cikk_DARAB=kódpont>512?512:kódpont;for(size_t 순번=0;순번<cikk_DARAB;순번++)자바전문넣기(순번,((const unsigned char *)MPERC_ÉRTÉK)[순번]);return 자바흐름쓰기(첫째값,cikk_DARAB);
        }
        fájlleíró = 대응파일기술자(첫째값); if (fájlleíró < 0) return -9;
        return kernel_KR(pk_write(fájlleíró, (const void *)MPERC_ÉRTÉK, kódpont));
    case 2:
        if (kódpont > 65536) return -22;
        if (!felhasználó_tartomány(MPERC_ÉRTÉK, kódpont, 1)) return -14;
        if (첫째값 == 0) {
            size_t cikk_DARAB = 0;
            while (cikk_DARAB < kódpont) {
                int karakter_ÉRTÉK = (int32_t)보드글자읽기(); if (karakter_ÉRTÉK == -2) return cikk_DARAB; if (karakter_ÉRTÉK < 0) break;
                ((unsigned char *)MPERC_ÉRTÉK)[cikk_DARAB++] = karakter_ÉRTÉK;
            }
            return cikk_DARAB ? (intptr_t)cikk_DARAB : (kódpont ? -11 : 0);
        }
        if(첫째값>=40&&szoftvercsatorna_végpont_tulajdonos(첫째값)){
            KR=자바흐름읽기(첫째값,kódpont>512?512:kódpont);if(KR>0)for(int 순번=0;순번<KR;순번++)((unsigned char *)MPERC_ÉRTÉK)[순번]=자바전문얻기(순번);return KR;
        }
        fájlleíró = 대응파일기술자(첫째값); if (fájlleíró < 0) return -9;
        return kernel_KR(pk_read(fájlleíró, (void *)MPERC_ÉRTÉK, kódpont));
    case 3:
        KR = másol_útvonal(첫째값, ÚTVONAL); if (KR) return KR;
        if (MPERC_ÉRTÉK > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (fájllista[순번] < 0) {
            fájlleíró = pk_open(ÚTVONAL, (int)MPERC_ÉRTÉK, 0600);
            if (fájlleíró < 0) return -hibaszám;
            fájllista[순번] = fájlleíró; return 순번 + 3;
        }
        return -24;
    case 4:
        if (szoftvercsatorna_végpont_tulajdonos(첫째값)) { KR = bezár_szoftvercsatorna_végpont(첫째값); if (!KR) 통신끝점들[첫째값 - 32] = 0; return KR; }
        fájlleíró = 대응파일기술자(첫째값); if (fájlleíró < 0) return -9;
        KR = pk_close(fájlleíró); if (!KR) fájllista[첫째값 - 3] = -1;
        return kernel_KR(KR);
    case 5:
        fájlleíró = 대응파일기술자(첫째값); if (fájlleíró < 0) return -9;
        if (kódpont > 2) return -22;
        return kernel_KR(pk_lseek(fájlleíró, (int64_t)MPERC_ÉRTÉK, kódpont));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 felhasználó RW/NX halommemória_ÉRTÉK, 새로 노출되는 페이지는 0으로 inicializál
        if (!첫째값) return halommemória_megszüntet;
        if (첫째값 < felhasználó_KÉP_megszüntet || 첫째값 > felhasználó_halommemória_megszüntet) return -12;
        uintptr_t 이전쪽들 = (halommemória_megszüntet + oldalméret - 1) & ~(oldalméret - 1);
        uintptr_t 새쪽들 = (첫째값 + oldalméret - 1) & ~(oldalméret - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t adat_pozíció = 이전쪽들; adat_pozíció < 새쪽들; adat_pozíció += oldalméret) oldalelrendezés(adat_pozíció, kernel_lap, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t adat_pozíció = 이전쪽들; adat_pozíció < 새쪽들; adat_pozíció += oldalméret) oldalelrendezés(adat_pozíció, 사용자읽고쓰기, 3);
        } else {
            for (uintptr_t adat_pozíció = 새쪽들; adat_pozíció < 이전쪽들; adat_pozíció += oldalméret) {
                lap_Lista[(adat_pozíció - felhasználó_ALAP) / oldalméret] = 0; Engedélyek_Lista[(adat_pozíció - felhasználó_ALAP) / oldalméret] = 0;
            }
        }
        halommemória_megszüntet = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        fájlleíró = 대응파일기술자(첫째값); return fájlleíró < 0 ? -9 : kernel_KR(pk_size(fájlleíró));
    case 10:
        fájlleíró = 대응파일기술자(첫째값); return fájlleíró < 0 ? -9 : kernel_KR(pk_ftruncate(fájlleíró, (int64_t)MPERC_ÉRTÉK));
    case 11:
        KR = másol_útvonal(첫째값, ÚTVONAL); return KR ? KR : kernel_KR(pk_unlink(ÚTVONAL));
    case 12:
        fájlleíró = 대응파일기술자(첫째값); return fájlleíró < 0 ? -9 : kernel_KR(pk_fsync(fájlleíró));
    case 13: { // 그래픽 기초 API: felhasználó 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Fájl_bejegyzés->jegyzék_adat[3], 높이값 = Fájl_bejegyzés->jegyzék_adat[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || MPERC_ÉRTÉK > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - MPERC_ÉRTÉK) return -22;
        for (uintptr_t Y_koordináta = MPERC_ÉRTÉK; Y_koordináta < MPERC_ÉRTÉK + 높이값; Y_koordináta++) for (uintptr_t x_koordináta = 첫째값; x_koordináta < 첫째값 + 너비값; x_koordináta++) fal_képpont(x_koordináta, Y_koordináta, kódpont);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=cikk_DARAB; args(index,buffer,capacity)=UTF-8 hossz_ÉRTÉK
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (kódpont <= 전달인수길이[첫째값]) return -36;
        if (!felhasználó_tartomány(MPERC_ÉRTÉK, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)MPERC_ÉRTÉK, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interaktív=1;return fal_Terminál(13);}
        if(첫째값==2){interaktív=0;return 0;}
        if(첫째값==3)return fal_Terminál(13);
        if(첫째값!=1||!interaktív)return -22;
        KR=(int32_t)보드글자읽기();
        if(KR==-4096)return KR;
        START_IDŐTÚLLÉPÉS();return KR<0?-11:KR;
    case 17: { // 유한한 협력 várj_ÉRTÉK: kommunikáció 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t megszüntet_IDŐ = Óra_ÉRTÉK() + GYAKORISÁG * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Óra_ÉRTÉK() < megszüntet_IDŐ);
        START_IDŐTÚLLÉPÉS(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 szülő_ÉRTÉK·빈 폴더를 검사한다.
        if (MPERC_ÉRTÉK > 2) return -22;
        KR = másol_útvonal(첫째값, ÚTVONAL); if (KR) return KR;
        unsigned hossz_ÉRTÉK = 0; while (ÚTVONAL[hossz_ÉRTÉK]) hossz_ÉRTÉK++;
        KR = 자바경로시작(hossz_ÉRTÉK); if (KR < 0) return KR;
        for (unsigned 순번 = 0; 순번 < hossz_ÉRTÉK; 순번++) 자바경로바이트(순번, (unsigned char)ÚTVONAL[순번]);
        return MPERC_ÉRTÉK == 0 ? 자바항목종류() : MPERC_ÉRTÉK == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int karakter_ÉRTÉK=(int32_t)보드글자읽기();if(karakter_ÉRTÉK==-4096)return karakter_ÉRTÉK;if(karakter_ÉRTÉK>=0)화면누름(tulajdonos_objektum,karakter_ÉRTÉK);START_IDŐTÚLLÉPÉS();}
        if(첫째값==3&&kódpont){if(!자바셸대화형())return -95;interaktív=1;fal_Terminál(300);}
        return 화면호출(tulajdonos_objektum,첫째값,MPERC_ÉRTÉK,kódpont,Fájl_bejegyzés->jegyzék_adat[3],Fájl_bejegyzés->jegyzék_adat[4],Fájl_bejegyzés->jegyzék_adat[5]);
    case 21:
        if(kódpont>127)return -22;if(!felhasználó_tartomány(MPERC_ÉRTÉK,kódpont*sizeof(uint32_t),0))return -14;
        return 화면글(tulajdonos_objektum,첫째값,(const uint32_t *)MPERC_ÉRTÉK,kódpont);
    case 22: // 화면 Méret lekérdez_ÉRTÉK: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(MPERC_ÉRTÉK==SOCK_STREAM&&(kódpont==0||kódpont==6))KR=자바흐름만들기();
        else if(MPERC_ÉRTÉK==SOCK_DGRAM&&(kódpont==0||kódpont==IPPROTO_UDP))KR=자바전문만들기(첫째값,MPERC_ÉRTÉK,kódpont);
        else return -93;
        if (KR >= 32 && KR < 56) 통신끝점들[KR - 32] = 1;
        return KR;
    case 33: {
        if (!szoftvercsatorna_végpont_tulajdonos(첫째값)) return -9;
        struct pk_sockaddr_in CÍM;
        KR = CÍM_bevitel(MPERC_ÉRTÉK, kódpont, &CÍM); if (KR) return KR;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(CÍM.sin_addr.s_addr),pk_htons(CÍM.sin_port)):자바전문묶기(첫째값, pk_htonl(CÍM.sin_addr.s_addr), pk_htons(CÍM.sin_port));
    }
    case 34: {
        if (!szoftvercsatorna_végpont_tulajdonos(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Fájl_bejegyzés->jegyzék_adat[3]) return -95;
        if (kódpont > 512) return -90;
        if (kódpont && !felhasználó_tartomány(MPERC_ÉRTÉK, kódpont, 0)) return -14;
        struct pk_sockaddr_in CÍM;
        KR = CÍM_bevitel(Fájl_bejegyzés->jegyzék_adat[4], Fájl_bejegyzés->jegyzék_adat[5], &CÍM); if (KR) return KR;
        for (unsigned 순번 = 0; 순번 < kódpont; 순번++) 자바전문넣기(순번, ((const unsigned char *)MPERC_ÉRTÉK)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(CÍM.sin_addr.s_addr), pk_htons(CÍM.sin_port), kódpont);
    }
    case 35: {
        if (!szoftvercsatorna_végpont_tulajdonos(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Fájl_bejegyzés->jegyzék_adat[3]) return -95;
        if (kódpont > 512) return -90;
        if (kódpont && !felhasználó_tartomány(MPERC_ÉRTÉK, kódpont, 1)) return -14;
        pk_socklen_t puffer_kapacitás = 0;
        if (Fájl_bejegyzés->jegyzék_adat[4]) { KR = CÍM_kimenet_csekk(Fájl_bejegyzés->jegyzék_adat[4], Fájl_bejegyzés->jegyzék_adat[5], &puffer_kapacitás); if (KR) return KR; }
        KR = 자바전문받기(첫째값, kódpont); if (KR < 0) return KR;
        for (int 순번 = 0; 순번 < KR; 순번++) ((unsigned char *)MPERC_ÉRTÉK)[순번] = 자바전문얻기(순번);
        if (Fájl_bejegyzés->jegyzék_adat[4]) CÍM_kimenet(Fájl_bejegyzés->jegyzék_adat[4], Fájl_bejegyzés->jegyzék_adat[5], puffer_kapacitás, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return KR;
    }
    case 36: {
        if (!szoftvercsatorna_végpont_tulajdonos(첫째값)) return -9;
        pk_socklen_t puffer_kapacitás;
        KR = CÍM_kimenet_csekk(MPERC_ÉRTÉK, kódpont, &puffer_kapacitás); if (KR) return KR;
        CÍM_kimenet(MPERC_ÉRTÉK,kódpont,puffer_kapacitás,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!szoftvercsatorna_végpont_tulajdonos(첫째값))return -9;struct pk_sockaddr_in CÍM;
        KR=CÍM_bevitel(MPERC_ÉRTÉK,kódpont,&CÍM);if(KR)return KR;
        return 자바흐름연결(첫째값,pk_htonl(CÍM.sin_addr.s_addr),pk_htons(CÍM.sin_port));
    }
    case 38: return 첫째값>=40&&szoftvercsatorna_végpont_tulajdonos(첫째값)?자바흐름듣기(첫째값,MPERC_ÉRTÉK):-9;
    case 39:
        if(첫째값<40||!szoftvercsatorna_végpont_tulajdonos(첫째값))return -9;
        if(MPERC_ÉRTÉK||kódpont)return -95;KR=자바흐름연결받기(첫째값);if(KR>=40&&KR<56)통신끝점들[KR-32]=1;return KR;
    case 40: return 첫째값>=40&&szoftvercsatorna_végpont_tulajdonos(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(felhasználó_doboz *Fájl_bejegyzés) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Fájl_bejegyzés) : natív_Rendszer_hív(Fájl_bejegyzés);
}
static void visszaküld_kernel(felhasználó_doboz *Fájl_bejegyzés, int KR) {
    Állj_IDŐTÚLLÉPÉS();
    Fájl_bejegyzés->jegyzék_adat[0] = (uint64_t)(int64_t)KR;
    Fájl_bejegyzés->parancs_pozíció = (uintptr_t)felhasználó_visszaküld;
    Fájl_bejegyzés->Állapot_KÓD = 0x3c5; // EL1h, DAIF masked
}
int alkalmazáskivétel(felhasználó_doboz *Fájl_bejegyzés, unsigned METSZ) {
    if (!Aktív || (Fájl_bejegyzés->Állapot_KÓD & 15) != 0) return 0;
    if (METSZ) {
        uint32_t elismerés_ÉRTÉK = gép_jegyzék(megszakítás_CPU_csatoló + 0xc), azonosító_ÉRTÉK = elismerés_ÉRTÉK & 1023;
        if (azonosító_ÉRTÉK == 30) { visszaküld_kernel(Fájl_bejegyzés, felhasználó_IDŐTÚLLÉPÉS); gép_jegyzék(megszakítás_CPU_csatoló + 0x10) = elismerés_ÉRTÉK; return 1; }
        if (azonosító_ÉRTÉK < 1020) gép_jegyzék(megszakítás_CPU_csatoló + 0x10) = elismerés_ÉRTÉK;
        return 1;
    }
    uint64_t kivétel_Állapot; __asm__ volatile("mrs %0, esr_el1" : "=r"(kivétel_Állapot));
    if (Óra_ÉRTÉK() >= határidő_IDŐ) { visszaküld_kernel(Fájl_bejegyzés, felhasználó_IDŐTÚLLÉPÉS); return 1; }
    unsigned kivétel_terület = kivétel_Állapot >> 26;
    if (kivétel_terület == 0x15 && (kivétel_Állapot & 0xffff) == 0) {
        if (리눅스규약 ? Fájl_bejegyzés->jegyzék_adat[8] == 93 || Fájl_bejegyzés->jegyzék_adat[8] == 94 : Fájl_bejegyzés->jegyzék_adat[8] == 6) visszaküld_kernel(Fájl_bejegyzés, (int)(Fájl_bejegyzés->jegyzék_adat[0] & 255));
        else {
            intptr_t KR=체계호출(Fájl_bejegyzés);
            if(KR==-4096&&interaktív){
                저장값[tulajdonos_objektum].végrehajtás_doboz=*Fájl_bejegyzés;저장값[tulajdonos_objektum].végrehajtás_doboz.parancs_pozíció-=4;
                사용자실수보관(저장값[tulajdonos_objektum].lebegőpontos_szám_Állapot);visszaküld_kernel(Fájl_bejegyzés,사용자중단됨);
            }else Fájl_bejegyzés->jegyzék_adat[0]=(uint64_t)KR;
        }
    } else visszaküld_kernel(Fájl_bejegyzés, kivétel_terület == 0x24 ? felhasználó_adat_hiba : kivétel_terület == 0x20 ? felhasználó_végrehajtás_hiba : 사용자잘못된명령);
    return 1;
}

// 생성된 const ELF Csoport_ÉRTÉK: 실행은 반드시 app_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *adat; size_t Méret; unsigned 전달값; } app;
#include "programs.h"
static void *pillanatkép(unsigned helyzetindex){return (void *)(0x04000000ul+helyzetindex*(felhasználó_megszüntet-felhasználó_ALAP));}
static int Befejezés_app(int KR){
    사용자누적시각[tulajdonos_objektum]+=(uint32_t)보드밀리초()-felhasználó_végrehajtás_IDŐ[tulajdonos_objektum];
    Állj_IDŐTÚLLÉPÉS();Aktív=0;
    if(KR==사용자중단됨){
        저장된작업 *sztring_adat=&저장값[tulajdonos_objektum];sztring_adat->felfüggesztve_Állapot=1;sztring_adat->interaktív=interaktív;sztring_adat->리눅스규약=리눅스규약;sztring_adat->halommemória_tár=halommemória_megszüntet;sztring_adat->인수개수=전달인수개수;
        memcpy(sztring_adat->Engedélyek_Lista,Engedélyek_Lista,sizeof(Engedélyek_Lista));memcpy(sztring_adat->fájllista,fájllista,sizeof(fájllista));memcpy(sztring_adat->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(sztring_adat->argumentum_TÖMB,전달인수,sizeof(전달인수));memcpy(sztring_adat->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<felhasználó_lap_DARAB;순번++)if(Engedélyek_Lista[순번])memcpy((unsigned char *)pillanatkép(tulajdonos_objektum)+순번*oldalméret,(void *)(felhasználó_ALAP+순번*oldalméret),oldalméret);
    }else{
        저장값[tulajdonos_objektum].felfüggesztve_Állapot=0;화면초기화(tulajdonos_objektum);
        for(unsigned 순번=0;순번<16;순번++)if(fájllista[순번]>=0)pk_close(fájllista[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])bezár_szoftvercsatorna_végpont(순번+32);
    }
    for(unsigned 순번=0;순번<felhasználó_lap_DARAB;순번++){lap_Lista[순번]=0;Engedélyek_Lista[순번]=0;}변환표맞추기();return KR;
}
uintptr_t fal_egyéni_vezérlőelem(uintptr_t Művelet){
    unsigned helyzetindex=Művelet&15;if(helyzetindex>=4||Aktív)return (uint32_t)-22;
    저장된작업 *sztring_adat=&저장값[helyzetindex];
    if(Művelet>=32){if(sztring_adat->felfüggesztve_Állapot){for(unsigned 순번=0;순번<16;순번++)if(sztring_adat->fájllista[순번]>=0)pk_close(sztring_adat->fájllista[순번]);for(unsigned 순번=0;순번<24;순번++)if(sztring_adat->통신끝점들[순번])bezár_szoftvercsatorna_végpont(순번+32);}sztring_adat->felfüggesztve_Állapot=0;화면초기화(helyzetindex);return 0;}
    if(Művelet>=16)return sztring_adat->felfüggesztve_Állapot;
    if(!sztring_adat->felfüggesztve_Állapot)return (uint32_t)-22;
    tulajdonos_objektum=helyzetindex;interaktív=sztring_adat->interaktív;리눅스규약=sztring_adat->리눅스규약;halommemória_megszüntet=sztring_adat->halommemória_tár;전달인수개수=sztring_adat->인수개수;
    memcpy(fájllista,sztring_adat->fájllista,sizeof(fájllista));memcpy(통신끝점들,sztring_adat->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,sztring_adat->argumentum_TÖMB,sizeof(전달인수));memcpy(전달인수길이,sztring_adat->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<felhasználó_lap_DARAB;순번++)lap_Lista[순번]=(felhasználó_ALAP+순번*oldalméret)|kernel_lap;변환표맞추기();
    memset((void *)felhasználó_ALAP,0,felhasználó_megszüntet-felhasználó_ALAP);
    for(unsigned 순번=0;순번<felhasználó_lap_DARAB;순번++)if(sztring_adat->Engedélyek_Lista[순번])memcpy((void *)(felhasználó_ALAP+순번*oldalméret),(unsigned char *)pillanatkép(helyzetindex)+순번*oldalméret,oldalméret);
    memcpy(Engedélyek_Lista,sztring_adat->Engedélyek_Lista,sizeof(Engedélyek_Lista));
    for(unsigned 순번=0;순번<felhasználó_lap_DARAB;순번++){unsigned adat_pozíció=Engedélyek_Lista[순번];lap_Lista[순번]=adat_pozíció?(felhasználó_ALAP+순번*oldalméret)|(adat_pozíció==3?사용자읽고쓰기:adat_pozíció==5?사용자읽고실행:felhasználó_írásvédett):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktív=1;sztring_adat->felfüggesztve_Állapot=0;START_IDŐTÚLLÉPÉS();
    felhasználó_végrehajtás_IDŐ[tulajdonos_objektum]=보드밀리초();
    return (uint32_t)Befejezés_app(felhasználó_CV(&sztring_adat->végrehajtás_doboz,sztring_adat->lebegőpontos_szám_Állapot));
}
static int futtat_app(const unsigned char *adat, size_t Méret, unsigned 전달값, int 리눅스방식, const char *Név) {
    if (Aktív) return -16;
    tulajdonos_objektum=fal_Terminál(11);if(tulajdonos_objektum<0||tulajdonos_objektum>3||저장값[tulajdonos_objektum].felfüggesztve_Állapot)return -16;interaktív=0;
    int érvényes = 실행파일검사(adat, Méret, 리눅스방식); if (érvényes) return érvényes;
    리눅스규약 = 리눅스방식;
    unsigned név_INDEX=0;
    while (*Név && név_INDEX<31) felhasználó_parancs_név[tulajdonos_objektum][név_INDEX++]=(unsigned char)*Név++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (név_INDEX) felhasználó_parancs_név[tulajdonos_objektum][név_INDEX++]=' ';
        for (unsigned helyzetindex=0; helyzetindex<전달인수길이[0]; helyzetindex++) felhasználó_parancs_név[tulajdonos_objektum][név_INDEX++]=전달인수[0][helyzetindex];
    }
    felhasználó_parancs_név[tulajdonos_objektum][név_INDEX]=0; felhasználói_szám[tulajdonos_objektum]=Tovább_felhasználói_szám++;
    if (Tovább_felhasználói_szám>0x7fffffffu) Tovább_felhasználói_szám=10;
    felhasználó_START_IDŐ[tulajdonos_objektum]=보드밀리초(); 사용자누적시각[tulajdonos_objektum]=0;
    for (unsigned 순번 = 0; 순번 < felhasználó_lap_DARAB; 순번++) lap_Lista[순번] = (felhasználó_ALAP + 순번 * oldalméret) | kernel_lap;
    변환표맞추기();
    memset((void *)felhasználó_ALAP, 0, felhasználó_megszüntet - felhasználó_ALAP);
    memset(Engedélyek_Lista, 0, sizeof(Engedélyek_Lista));
    실행파일머리 végrehajtható_fejléc; memcpy(&végrehajtható_fejléc, adat, sizeof(végrehajtható_fejléc));
    for (unsigned 순번 = 0; 순번 < végrehajtható_fejléc.app_fejléc_DARAB; 순번++) {
        실행파일구획 adat_pozíció; memcpy(&adat_pozíció, adat + végrehajtható_fejléc.app_fejléc_Ofszet + 순번 * sizeof(adat_pozíció), sizeof(adat_pozíció));
        if (adat_pozíció.beír_terület != 1 || !adat_pozíció.기억영역크기) continue;
        if (adat_pozíció.파일영역크기) memcpy((void *)(uintptr_t)adat_pozíció.CÍM, adat + adat_pozíció.Ofszet_ÉRTÉK, adat_pozíció.파일영역크기);
        for (uintptr_t aktuális_pozíció = adat_pozíció.CÍM & ~(oldalméret - 1); aktuális_pozíció < adat_pozíció.CÍM + adat_pozíció.기억영역크기; aktuális_pozíció += oldalméret) {
            Engedélyek_Lista[(aktuális_pozíció - felhasználó_ALAP) / oldalméret] = (adat_pozíció.konfiguráció_BITS & 2) ? 3 : ((adat_pozíció.konfiguráció_BITS & 1) ? 5 : 1);
        }
    }
    for (uintptr_t aktuális_pozíció = felhasználó_Sor_CÍM; aktuális_pozíció < felhasználó_megszüntet; aktuális_pozíció += oldalméret) Engedélyek_Lista[(aktuális_pozíció - felhasználó_ALAP) / oldalméret] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(végrehajtható_fejléc.belépési_pont) : felhasználó_megszüntet;
    for (unsigned 순번 = 0; 순번 < felhasználó_lap_DARAB; 순번++) {
        unsigned engedélyek = Engedélyek_Lista[순번];
        lap_Lista[순번] = engedélyek ? (felhasználó_ALAP + 순번 * oldalméret) | (engedélyek == 3 ? 사용자읽고쓰기 : engedélyek == 5 ? 사용자읽고실행 : felhasználó_írásvédett) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) fájllista[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    halommemória_megszüntet = felhasználó_KÉP_megszüntet;
    Aktív = 1; START_IDŐTÚLLÉPÉS();
    felhasználó_végrehajtás_IDŐ[tulajdonos_objektum]=보드밀리초();
    int KR = felhasználó_megad(végrehajtható_fejléc.belépési_pont, 초기쌓임공간, 전달값);
    return Befejezés_app(KR);
}
uintptr_t fal_felhasználó_futtat(uintptr_t KERES_INDEX) {
    if (KERES_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Név=KERES_INDEX==10?"javac":KERES_INDEX==11?"java":KERES_INDEX==12?"python":KERES_INDEX==13?"vi":KERES_INDEX==14?"jar":KERES_INDEX==15?"cc":KERES_INDEX==16?"jaot":"ELF";
    return (uint32_t)futtat_app(실행항목들[KERES_INDEX].adat, 실행항목들[KERES_INDEX].Méret, 실행항목들[KERES_INDEX].전달값, 0, Név);
}
static uintptr_t végrehajt_Fájl(int 리눅스방식) {
    static unsigned char KÉP[16384];
    if (Aktív || !전달인수개수) return (uint32_t)-22;
    int fájlleíró = pk_open((const char *)전달인수[0], írásvédett_ÉRTÉK, 0);
    if (fájlleíró < 0) return (uint32_t)-hibaszám;
    int Méret = pk_size(fájlleíró);
    if (Méret < 0 || (unsigned)Méret > sizeof(KÉP)) { pk_close(fájlleíró); return (uint32_t)-27; }
    int KAPOTT_DARAB = pk_read(fájlleíró, KÉP, Méret); pk_close(fájlleíró);
    if (KAPOTT_DARAB != Méret) return (uint32_t)-5;
    return (uint32_t)futtat_app(KÉP, Méret, 0, 리눅스방식, "");
}
uintptr_t fal_felhasználó_Fájl(void) { return végrehajt_Fájl(0); }
uintptr_t 보드사용자리눅스파일(void) { return végrehajt_Fájl(1); }
uintptr_t fal_felhasználó_ellenőriz(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].adat, 잘못된실행항목들[순번].Méret) != felhasználó_végrehajtható_hiba) return 순번 + 1;
    return 0;
}
