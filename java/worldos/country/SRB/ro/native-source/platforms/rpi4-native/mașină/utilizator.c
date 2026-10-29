#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 executa_comandă mașină strat_VALUE. Fișier date/정책은 기존 AOT Java 커널에 위임한다.
#include "utilizator.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../rețea_Teanc/rețea_Teanc.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define mașină_registru(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distribuitor 0xff841000ul
#define IRQ_CPU_interfață 0xff842000ul
#define dimensiune_pagină 4096ul
#define acces_marcaj (1ul << 10)
#define 권한실행금지 (1ul << 53)
#define 사용자실행금지 (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | acces_marcaj)
#define nucleu_pagina (3ul | 보통기억 | 권한실행금지 | 사용자실행금지)
#define utilizator_citire_scriere (3ul | 보통기억 | (1ul << 6) | 권한실행금지 | 사용자실행금지)
#define utilizator_doar_în_citire (3ul | 보통기억 | (3ul << 6) | 권한실행금지 | 사용자실행금지)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | 권한실행금지)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Avizier_element_imagine(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Avizier_Terminal(uintptr_t);
extern int Terminal_în_așteptare(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int utilizator_CV(utilizator_cadru *,void *);
extern void 사용자실수보관(void *);
extern int utilizator_introduce(uintptr_t intrare_p, uintptr_t Teanc_Stocare, uintptr_t 전달값);
extern void utilizator_restitui(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t rădăcină_adresa[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t pagina_Listă[utilizator_pagina_COUNT] __attribute__((aligned(4096)));
static uint8_t Permisiuni_Listă[utilizator_pagina_COUNT];
static int Activ, Fișier_Listă[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned Fișier_handle){return Fișier_handle<40?자바전문닫기(Fișier_handle):자바흐름닫기(Fișier_handle);}
static uint64_t FREQUENCY, dată_limită_oră;
static uintptr_t 동적기억끝;
// nucleu_VALUE 셸이 준비한 UTF-8 Argumente. EL0에는 copia_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,대화형,리눅스규약,Fișier_Listă[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_ARRAY[8][256],Permisiuni_Listă[utilizator_pagina_COUNT];
    uintptr_t 동적기억공간; utilizator_cadru executare_cadru;
    unsigned char mobil_p_Stare[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int proprietar_obiect,대화형;
static uint32_t număr_de_utilizator[4], utilizator_buta_oră[4], 사용자누적시각[4], utilizator_executare_oră[4], Următorul_număr_de_utilizator=10;
static unsigned char utilizator_comandă_nume[4][288];
uint32_t 사용자상태읽기(unsigned intrare_VALUE, unsigned INDEX) {
    unsigned index_de_poziție=INDEX&3;
    int Stare_VALUE=(Activ && proprietar_obiect==(int)index_de_poziție) ? 1 : 저장값[index_de_poziție].멈춤상태 ? 2 : 0;
    if (intrare_VALUE==0) return Stare_VALUE;
    if (!Stare_VALUE) return 0;
    if (intrare_VALUE==1) return număr_de_utilizator[index_de_poziție];
    if (intrare_VALUE==2) {
        unsigned char *쪽들=Stare_VALUE==1?Permisiuni_Listă:저장값[index_de_poziție].Permisiuni_Listă;
        unsigned pagina_COUNT=0; for (unsigned 순번=0; 순번<utilizator_pagina_COUNT; 순번++) if(쪽들[순번]) pagina_COUNT++;
        return pagina_COUNT*4;
    }
    if (intrare_VALUE==3) return (uint32_t)보드밀리초()-utilizator_buta_oră[index_de_poziție];
    if (intrare_VALUE==4) return 사용자누적시각[index_de_poziție]+(Stare_VALUE==1?(uint32_t)보드밀리초()-utilizator_executare_oră[index_de_poziție]:0);
    if (intrare_VALUE==5) return INDEX/4<sizeof(utilizator_comandă_nume[0])?utilizator_comandă_nume[index_de_poziție][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t intrare_COUNT) {
    if (Activ || intrare_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = intrare_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t curent_poziție, uintptr_t byte_date) {
    if (Activ || LOOKUP_INDEX >= 전달인수개수 || curent_poziție >= 255 || curent_poziție != 전달인수길이[LOOKUP_INDEX] || !byte_date || byte_date > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][curent_poziție] = byte_date;
    전달인수길이[LOOKUP_INDEX] = curent_poziție + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Ceas_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Stop_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    mașină_registru(IRQ_distribuitor + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void buta_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, activa = 1;
    dată_limită_oră = Ceas_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(activa) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned bloc_de_date = 0; bloc_de_date < 4; bloc_de_date++) {
        rădăcină_adresa[bloc_de_date] = (uintptr_t)가운데[bloc_de_date] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t adresa = ((uintptr_t)bloc_de_date << 30) | ((uintptr_t)순번 << 21);
            가운데[bloc_de_date][순번] = adresa | 1 | acces_marcaj | 사용자실행금지;
            if (adresa >= 0xfc000000ul) 가운데[bloc_de_date][순번] |= 권한실행금지; // Device-nGnRnE
            else 가운데[bloc_de_date][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < utilizator_pagina_COUNT / 512; SECOND_VALUE++)
        가운데[0][(utilizator_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(pagina_Listă + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < utilizator_pagina_COUNT; 순번++) pagina_Listă[순번] = (utilizator_BASE + 순번 * dimensiune_pagină) | nucleu_pagina;
    uint64_t Memorie_atribut_registru = 0x4400, adresa_Traducere_control = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Memorie_atribut_registru), "r"(adresa_Traducere_control), "r"((uintptr_t)rădăcină_adresa) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t mobil_p_Stare = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(mobil_p_Stare) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Stop_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 intrare_p_VALUE 때만 permite_VALUE.
    mașină_registru(IRQ_distribuitor) = 0;
    mașină_registru(IRQ_distribuitor + 0x180) = 0xffffffff;
    mașină_registru(IRQ_distribuitor + 0x80) = 0xffffffff;
    mașină_registru(IRQ_distribuitor + 0x280) = 1u << 30;
    mașină_registru(IRQ_distribuitor + 0x41c) = 0x80808080;
    mașină_registru(IRQ_distribuitor + 0x100) = 1u << 30;
    mașină_registru(IRQ_CPU_interfață + 4) = 0xff;
    mașină_registru(IRQ_CPU_interfață + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Securitate = (mașină_registru(IRQ_distribuitor + 4) & (1u << 10)) != 0;
    mașină_registru(IRQ_distribuitor) = Securitate ? 1 : 3;
    mașină_registru(IRQ_CPU_interfață) = Securitate ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t Tip_zonă, mașină_Tip; uint32_t număr_de_versiune;
    uint64_t intrare_p, program_Antet_OFFSET, antet_secțiune_OFFSET; uint32_t configurație_Serviciu_de_transfer_inteligent_în_fundal;
    uint16_t 실행머리크기, program_Antet_intrare_dimensiona, program_Antet_COUNT, antet_secțiune_intrare_dimensiona, antet_secțiune_COUNT, secțiune_nume_tabel_INDEX;
} 실행파일머리;
typedef struct { uint32_t Tip_zonă, configurație_Serviciu_de_transfer_inteligent_în_fundal; uint64_t OFFSET_VALUE, adresa, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(utilizator_cadru) == 272, "exception assembly layout");
static int 포함된범위(uint64_t OFFSET_VALUE, uint64_t Mărime, uint64_t termina_un_apel_OFFSET) {
    return OFFSET_VALUE <= termina_un_apel_OFFSET && Mărime <= termina_un_apel_OFFSET - OFFSET_VALUE;
}
static int 부가정보검사(const unsigned char *date_poziție, size_t Mărime) {
    size_t curent_poziție = 0;
    while (포함된범위(curent_poziție, 12, Mărime)) {
        uint32_t 낱말들[3]; memcpy(낱말들, date_poziție + curent_poziție, 12); curent_poziție += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(curent_poziție, 이름영역크기, Mărime) || !포함된범위(curent_poziție + 이름영역크기, 설명크기, Mărime)) return 0;
        const unsigned char Nume[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Nume) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Nume); 순번++) if (date_poziție[curent_poziție + 순번] != Nume[순번]) 일치 = 0;
        uint32_t număr_de_versiune = 0;
        if (일치) memcpy(&număr_de_versiune, date_poziție + curent_poziție + 이름영역크기, 4);
        if (일치 && număr_de_versiune == 1) return 1;
        curent_poziție += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *date, size_t Mărime, int 리눅스방식) {
    if (Mărime < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, date, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.Tip_zonă != 2 || 실행머리.mașină_Tip != 183 || 실행머리.număr_de_versiune != 1 || 실행머리.configurație_Serviciu_de_transfer_inteligent_în_fundal || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.program_Antet_intrare_dimensiona != sizeof(실행파일구획) || !실행머리.program_Antet_COUNT || 실행머리.program_Antet_COUNT > 16 ||
        실행머리.program_Antet_OFFSET < sizeof(실행머리) || !포함된범위(실행머리.program_Antet_OFFSET, (uint64_t)실행머리.program_Antet_COUNT * sizeof(실행파일구획), Mărime)) return 사용자실행파일오류;
    uint8_t 사용량[(utilizator_IMAGE_termina_un_apel - utilizator_BASE) / dimensiune_pagină] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.program_Antet_COUNT; 순번++) {
        실행파일구획 date_poziție; memcpy(&date_poziție, date + 실행머리.program_Antet_OFFSET + 순번 * sizeof(date_poziție), sizeof(date_poziție));
        if (date_poziție.Tip_zonă == 4) {
            if (!포함된범위(date_poziție.OFFSET_VALUE, date_poziție.파일영역크기, Mărime)) return 사용자실행파일오류;
            if (부가정보검사(date + date_poziție.OFFSET_VALUE, date_poziție.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (date_poziție.Tip_zonă == 0 || date_poziție.Tip_zonă == 6 || (date_poziție.Tip_zonă == 0x6474e551 && !(date_poziție.configurație_Serviciu_de_transfer_inteligent_în_fundal & 1))) continue;
        if (date_poziție.Tip_zonă != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!date_poziție.기억영역크기) continue;
        if (date_poziție.configurație_Serviciu_de_transfer_inteligent_în_fundal & ~7u || !(date_poziție.configurație_Serviciu_de_transfer_inteligent_în_fundal & 4) || (date_poziție.configurație_Serviciu_de_transfer_inteligent_în_fundal & 3) == 3 || date_poziție.파일영역크기 > date_poziție.기억영역크기 ||
            (date_poziție.파일영역크기 && !포함된범위(date_poziție.OFFSET_VALUE, date_poziție.파일영역크기, Mărime)) || date_poziție.adresa < utilizator_BASE ||
            !포함된범위(date_poziție.adresa, date_poziție.기억영역크기, utilizator_IMAGE_termina_un_apel) ||
            (!리눅스방식 && ((date_poziție.adresa & (dimensiune_pagină - 1)) || (date_poziție.OFFSET_VALUE & (dimensiune_pagină - 1)) || date_poziție.맞춤 != dimensiune_pagină)) ||
            (리눅스방식 && (((date_poziție.adresa ^ date_poziție.OFFSET_VALUE) & (dimensiune_pagină - 1)) || !date_poziție.맞춤 ||
                (date_poziție.맞춤 & (date_poziție.맞춤 - 1)) || date_poziție.맞춤 > 0x200000 || ((date_poziție.adresa ^ date_poziție.OFFSET_VALUE) & (date_poziție.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (date_poziție.adresa - utilizator_BASE) / dimensiune_pagină;
        unsigned intrare_COUNT = ((date_poziție.adresa & (dimensiune_pagină - 1)) + date_poziție.기억영역크기 + dimensiune_pagină - 1) / dimensiune_pagină;
        for (unsigned pagina_VALUE = 첫항목; pagina_VALUE < 첫항목 + intrare_COUNT; pagina_VALUE++) {
            if (사용량[pagina_VALUE]) return 사용자실행파일오류;
            사용량[pagina_VALUE] = 1;
        }
        if ((date_poziție.configurație_Serviciu_de_transfer_inteligent_în_fundal & 1) && 실행머리.intrare_p >= date_poziție.adresa && 실행머리.intrare_p < date_poziție.adresa + date_poziție.파일영역크기 && !(실행머리.intrare_p & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *date, size_t Mărime) { return 실행파일검사(date, Mărime, 0); }
static void aspect_pagină(uintptr_t adresa, uint64_t configurație_Serviciu_de_transfer_inteligent_în_fundal, unsigned permisiuni) {
    unsigned LOOKUP_INDEX = (adresa - utilizator_BASE) / dimensiune_pagină;
    pagina_Listă[LOOKUP_INDEX] = adresa | configurație_Serviciu_de_transfer_inteligent_în_fundal;
    Permisiuni_Listă[LOOKUP_INDEX] = permisiuni;
}
static int utilizator_zonă(uintptr_t adresa, size_t intrare_COUNT, int 쓰는중) {
    if (adresa < utilizator_BASE || !포함된범위(adresa, intrare_COUNT, utilizator_termina_un_apel)) return 0;
    if (!intrare_COUNT) return 1;
    unsigned 첫항목 = (adresa - utilizator_BASE) / dimensiune_pagină, 마지막 = (adresa + intrare_COUNT - 1 - utilizator_BASE) / dimensiune_pagină;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Permisiuni_Listă[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int copia_cale(uintptr_t adresa, char *Cale) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!utilizator_zonă(adresa, 1, 0)) return -14;
        Cale[순번] = *(const char *)adresa++;
        if (!Cale[순번]) return 0;
    }
    return -36;
}
static intptr_t nucleu_KR(intptr_t KR) { return KR < 0 ? -număr_de_eroare : KR; }
static int 대응파일기술자(uint64_t Fișier_handle) { return Fișier_handle >= 3 && Fișier_handle < 19 ? Fișier_Listă[Fișier_handle - 3] : -1; }
static int 통신끝점소유(uint64_t Fișier_handle) { return Fișier_handle >= 32 && Fișier_handle < 56 && 통신끝점들[Fișier_handle - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t lungime_VALUE, struct pk_sockaddr_in *adresa) {
    if (lungime_VALUE != sizeof(*adresa)) return -22;
    if (!utilizator_zonă(가리킴값, lungime_VALUE, 0)) return -14;
    memcpy(adresa, (const void *)가리킴값, sizeof(*adresa));
    return adresa->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t lungime_cursor, pk_socklen_t *tampon_capacitate) {
    if (!utilizator_zonă(lungime_cursor, sizeof(*tampon_capacitate), 1)) return -14;
    memcpy(tampon_capacitate, (const void *)lungime_cursor, sizeof(*tampon_capacitate));
    if (*tampon_capacitate > sizeof(struct pk_sockaddr_in)) *tampon_capacitate = sizeof(struct pk_sockaddr_in);
    if (*tampon_capacitate && !utilizator_zonă(가리킴값, *tampon_capacitate, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t lungime_cursor, pk_socklen_t tampon_capacitate, int adresa, int număr_port) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(număr_port); VALUE.sin_addr.s_addr = pk_htonl(adresa);
    if (tampon_capacitate) memcpy((void *)가리킴값, &VALUE, tampon_capacitate);
    pk_socklen_t lungime_VALUE = sizeof(VALUE); memcpy((void *)lungime_cursor, &lungime_VALUE, sizeof(lungime_VALUE));
}
extern uintptr_t Avizier_Canal(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(utilizator_cadru *Fișier_intrare) {
    uintptr_t 첫째값 = Fișier_intrare->registru_date[0], SECOND_VALUE = Fișier_intrare->registru_date[1], cod_caracter = Fișier_intrare->registru_date[2];
    char Cale[65];
    int Fișier_handle, KR;
    switch (Fișier_intrare->registru_date[8]) {
    case 0: return 1; // propriu ABI 버전
    case 1: // write: cursor 전체를 검사한 ÎNAPOI_VALUE Rezultat/Fișier schimba_VALUE
        if (cod_caracter > 65536) return -22;
        if (!utilizator_zonă(SECOND_VALUE, cod_caracter, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Ceas_VALUE();
            for (size_t 순번 = 0; 순번 < cod_caracter; 순번++) Avizier_Canal(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 nucleu_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(대화형){
                dată_limită_oră+=Ceas_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(dată_limită_oră) : "memory");
            }
            return cod_caracter;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t element_COUNT=cod_caracter>512?512:cod_caracter;for(size_t 순번=0;순번<element_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,element_COUNT);
        }
        Fișier_handle = 대응파일기술자(첫째값); if (Fișier_handle < 0) return -9;
        return nucleu_KR(pk_write(Fișier_handle, (const void *)SECOND_VALUE, cod_caracter));
    case 2:
        if (cod_caracter > 65536) return -22;
        if (!utilizator_zonă(SECOND_VALUE, cod_caracter, 1)) return -14;
        if (첫째값 == 0) {
            size_t element_COUNT = 0;
            while (element_COUNT < cod_caracter) {
                int caracter_VALUE = (int32_t)보드글자읽기(); if (caracter_VALUE == -2) return element_COUNT; if (caracter_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[element_COUNT++] = caracter_VALUE;
            }
            return element_COUNT ? (intptr_t)element_COUNT : (cod_caracter ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            KR=자바흐름읽기(첫째값,cod_caracter>512?512:cod_caracter);if(KR>0)for(int 순번=0;순번<KR;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return KR;
        }
        Fișier_handle = 대응파일기술자(첫째값); if (Fișier_handle < 0) return -9;
        return nucleu_KR(pk_read(Fișier_handle, (void *)SECOND_VALUE, cod_caracter));
    case 3:
        KR = copia_cale(첫째값, Cale); if (KR) return KR;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (Fișier_Listă[순번] < 0) {
            Fișier_handle = pk_open(Cale, (int)SECOND_VALUE, 0600);
            if (Fișier_handle < 0) return -număr_de_eroare;
            Fișier_Listă[순번] = Fișier_handle; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { KR = 통신끝점닫기(첫째값); if (!KR) 통신끝점들[첫째값 - 32] = 0; return KR; }
        Fișier_handle = 대응파일기술자(첫째값); if (Fișier_handle < 0) return -9;
        KR = pk_close(Fișier_handle); if (!KR) Fișier_Listă[첫째값 - 3] = -1;
        return nucleu_KR(KR);
    case 5:
        Fișier_handle = 대응파일기술자(첫째값); if (Fișier_handle < 0) return -9;
        if (cod_caracter > 2) return -22;
        return nucleu_KR(pk_lseek(Fișier_handle, (int64_t)SECOND_VALUE, cod_caracter));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 utilizator RW/NX 힙, 새로 노출되는 페이지는 0으로 초기화
        if (!첫째값) return 동적기억끝;
        if (첫째값 < utilizator_IMAGE_termina_un_apel || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + dimensiune_pagină - 1) & ~(dimensiune_pagină - 1);
        uintptr_t 새쪽들 = (첫째값 + dimensiune_pagină - 1) & ~(dimensiune_pagină - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t date_poziție = 이전쪽들; date_poziție < 새쪽들; date_poziție += dimensiune_pagină) aspect_pagină(date_poziție, nucleu_pagina, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t date_poziție = 이전쪽들; date_poziție < 새쪽들; date_poziție += dimensiune_pagină) aspect_pagină(date_poziție, utilizator_citire_scriere, 3);
        } else {
            for (uintptr_t date_poziție = 새쪽들; date_poziție < 이전쪽들; date_poziție += dimensiune_pagină) {
                pagina_Listă[(date_poziție - utilizator_BASE) / dimensiune_pagină] = 0; Permisiuni_Listă[(date_poziție - utilizator_BASE) / dimensiune_pagină] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        Fișier_handle = 대응파일기술자(첫째값); return Fișier_handle < 0 ? -9 : nucleu_KR(pk_size(Fișier_handle));
    case 10:
        Fișier_handle = 대응파일기술자(첫째값); return Fișier_handle < 0 ? -9 : nucleu_KR(pk_ftruncate(Fișier_handle, (int64_t)SECOND_VALUE));
    case 11:
        KR = copia_cale(첫째값, Cale); return KR ? KR : nucleu_KR(pk_unlink(Cale));
    case 12:
        Fișier_handle = 대응파일기술자(첫째값); return Fișier_handle < 0 ? -9 : nucleu_KR(pk_fsync(Fișier_handle));
    case 13: { // 그래픽 기초 API: utilizator 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Fișier_intrare->registru_date[3], 높이값 = Fișier_intrare->registru_date[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t 세로좌표 = SECOND_VALUE; 세로좌표 < SECOND_VALUE + 높이값; 세로좌표++) for (uintptr_t coordonata_X = 첫째값; coordonata_X < 첫째값 + 너비값; coordonata_X++) Avizier_element_imagine(coordonata_X, 세로좌표, cod_caracter);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=element_COUNT; args(index,buffer,capacity)=UTF-8 lungime_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (cod_caracter <= 전달인수길이[첫째값]) return -36;
        if (!utilizator_zonă(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;대화형=1;return Avizier_Terminal(13);}
        if(첫째값==2){대화형=0;return 0;}
        if(첫째값==3)return Avizier_Terminal(13);
        if(첫째값!=1||!대화형)return -22;
        KR=(int32_t)보드글자읽기();
        if(KR==-4096)return KR;
        buta_TIMEOUT();return KR<0?-11:KR;
    case 17: { // 유한한 협력 대기: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t termina_un_apel_oră = Ceas_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Ceas_VALUE() < termina_un_apel_oră);
        buta_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 părinte_VALUE·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        KR = copia_cale(첫째값, Cale); if (KR) return KR;
        unsigned lungime_VALUE = 0; while (Cale[lungime_VALUE]) lungime_VALUE++;
        KR = 자바경로시작(lungime_VALUE); if (KR < 0) return KR;
        for (unsigned 순번 = 0; 순번 < lungime_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)Cale[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int caracter_VALUE=(int32_t)보드글자읽기();if(caracter_VALUE==-4096)return caracter_VALUE;if(caracter_VALUE>=0)화면누름(proprietar_obiect,caracter_VALUE);buta_TIMEOUT();}
        if(첫째값==3&&cod_caracter){if(!자바셸대화형())return -95;대화형=1;Avizier_Terminal(300);}
        return 화면호출(proprietar_obiect,첫째값,SECOND_VALUE,cod_caracter,Fișier_intrare->registru_date[3],Fișier_intrare->registru_date[4],Fișier_intrare->registru_date[5]);
    case 21:
        if(cod_caracter>127)return -22;if(!utilizator_zonă(SECOND_VALUE,cod_caracter*sizeof(uint32_t),0))return -14;
        return 화면글(proprietar_obiect,첫째값,(const uint32_t *)SECOND_VALUE,cod_caracter);
    case 22: // 화면 Mărime interoga_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(cod_caracter==0||cod_caracter==6))KR=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(cod_caracter==0||cod_caracter==IPPROTO_UDP))KR=자바전문만들기(첫째값,SECOND_VALUE,cod_caracter);
        else return -93;
        if (KR >= 32 && KR < 56) 통신끝점들[KR - 32] = 1;
        return KR;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in adresa;
        KR = 주소입력(SECOND_VALUE, cod_caracter, &adresa); if (KR) return KR;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(adresa.sin_addr.s_addr),pk_htons(adresa.sin_port)):자바전문묶기(첫째값, pk_htonl(adresa.sin_addr.s_addr), pk_htons(adresa.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Fișier_intrare->registru_date[3]) return -95;
        if (cod_caracter > 512) return -90;
        if (cod_caracter && !utilizator_zonă(SECOND_VALUE, cod_caracter, 0)) return -14;
        struct pk_sockaddr_in adresa;
        KR = 주소입력(Fișier_intrare->registru_date[4], Fișier_intrare->registru_date[5], &adresa); if (KR) return KR;
        for (unsigned 순번 = 0; 순번 < cod_caracter; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(adresa.sin_addr.s_addr), pk_htons(adresa.sin_port), cod_caracter);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Fișier_intrare->registru_date[3]) return -95;
        if (cod_caracter > 512) return -90;
        if (cod_caracter && !utilizator_zonă(SECOND_VALUE, cod_caracter, 1)) return -14;
        pk_socklen_t tampon_capacitate = 0;
        if (Fișier_intrare->registru_date[4]) { KR = 주소출력검사(Fișier_intrare->registru_date[4], Fișier_intrare->registru_date[5], &tampon_capacitate); if (KR) return KR; }
        KR = 자바전문받기(첫째값, cod_caracter); if (KR < 0) return KR;
        for (int 순번 = 0; 순번 < KR; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (Fișier_intrare->registru_date[4]) 주소출력(Fișier_intrare->registru_date[4], Fișier_intrare->registru_date[5], tampon_capacitate, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return KR;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t tampon_capacitate;
        KR = 주소출력검사(SECOND_VALUE, cod_caracter, &tampon_capacitate); if (KR) return KR;
        주소출력(SECOND_VALUE,cod_caracter,tampon_capacitate,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in adresa;
        KR=주소입력(SECOND_VALUE,cod_caracter,&adresa);if(KR)return KR;
        return 자바흐름연결(첫째값,pk_htonl(adresa.sin_addr.s_addr),pk_htons(adresa.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||cod_caracter)return -95;KR=자바흐름연결받기(첫째값);if(KR>=40&&KR<56)통신끝점들[KR-32]=1;return KR;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(utilizator_cadru *Fișier_intrare) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Fișier_intrare) : 자체체계호출(Fișier_intrare);
}
static void restitui_nucleu(utilizator_cadru *Fișier_intrare, int KR) {
    Stop_TIMEOUT();
    Fișier_intrare->registru_date[0] = (uint64_t)(int64_t)KR;
    Fișier_intrare->comandă_poziție = (uintptr_t)utilizator_restitui;
    Fișier_intrare->Stare_cod = 0x3c5; // EL1h, DAIF masked
}
int excepție_utilizator(utilizator_cadru *Fișier_intrare, unsigned INTERCEPT) {
    if (!Activ || (Fișier_intrare->Stare_cod & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t recunoaștere_VALUE = mașină_registru(IRQ_CPU_interfață + 0xc), identificator_VALUE = recunoaștere_VALUE & 1023;
        if (identificator_VALUE == 30) { restitui_nucleu(Fișier_intrare, utilizator_TIMEOUT); mașină_registru(IRQ_CPU_interfață + 0x10) = recunoaștere_VALUE; return 1; }
        if (identificator_VALUE < 1020) mașină_registru(IRQ_CPU_interfață + 0x10) = recunoaștere_VALUE;
        return 1;
    }
    uint64_t excepție_Stare; __asm__ volatile("mrs %0, esr_el1" : "=r"(excepție_Stare));
    if (Ceas_VALUE() >= dată_limită_oră) { restitui_nucleu(Fișier_intrare, utilizator_TIMEOUT); return 1; }
    unsigned excepție_zonă = excepție_Stare >> 26;
    if (excepție_zonă == 0x15 && (excepție_Stare & 0xffff) == 0) {
        if (리눅스규약 ? Fișier_intrare->registru_date[8] == 93 || Fișier_intrare->registru_date[8] == 94 : Fișier_intrare->registru_date[8] == 6) restitui_nucleu(Fișier_intrare, (int)(Fișier_intrare->registru_date[0] & 255));
        else {
            intptr_t KR=체계호출(Fișier_intrare);
            if(KR==-4096&&대화형){
                저장값[proprietar_obiect].executare_cadru=*Fișier_intrare;저장값[proprietar_obiect].executare_cadru.comandă_poziție-=4;
                사용자실수보관(저장값[proprietar_obiect].mobil_p_Stare);restitui_nucleu(Fișier_intrare,사용자중단됨);
            }else Fișier_intrare->registru_date[0]=(uint64_t)KR;
        }
    } else restitui_nucleu(Fișier_intrare, excepție_zonă == 0x24 ? utilizator_date_eroare : excepție_zonă == 0x20 ? utilizator_executare_eroare : 사용자잘못된명령);
    return 1;
}

// 생성된 const ELF grup_VALUE: 실행은 반드시 program_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *date; size_t Mărime; unsigned 전달값; } program;
#include "programs.h"
static void *clip_video(unsigned index_de_poziție){return (void *)(0x04000000ul+index_de_poziție*(utilizator_termina_un_apel-utilizator_BASE));}
static int sfârșit_program(int KR){
    사용자누적시각[proprietar_obiect]+=(uint32_t)보드밀리초()-utilizator_executare_oră[proprietar_obiect];
    Stop_TIMEOUT();Activ=0;
    if(KR==사용자중단됨){
        저장된작업 *șir_date=&저장값[proprietar_obiect];șir_date->멈춤상태=1;șir_date->대화형=대화형;șir_date->리눅스규약=리눅스규약;șir_date->동적기억공간=동적기억끝;șir_date->인수개수=전달인수개수;
        memcpy(șir_date->Permisiuni_Listă,Permisiuni_Listă,sizeof(Permisiuni_Listă));memcpy(șir_date->Fișier_Listă,Fișier_Listă,sizeof(Fișier_Listă));memcpy(șir_date->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(șir_date->argument_ARRAY,전달인수,sizeof(전달인수));memcpy(șir_date->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<utilizator_pagina_COUNT;순번++)if(Permisiuni_Listă[순번])memcpy((unsigned char *)clip_video(proprietar_obiect)+순번*dimensiune_pagină,(void *)(utilizator_BASE+순번*dimensiune_pagină),dimensiune_pagină);
    }else{
        저장값[proprietar_obiect].멈춤상태=0;화면초기화(proprietar_obiect);
        for(unsigned 순번=0;순번<16;순번++)if(Fișier_Listă[순번]>=0)pk_close(Fișier_Listă[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<utilizator_pagina_COUNT;순번++){pagina_Listă[순번]=0;Permisiuni_Listă[순번]=0;}변환표맞추기();return KR;
}
uintptr_t Avizier_control_utilizator(uintptr_t Acțiuni){
    unsigned index_de_poziție=Acțiuni&15;if(index_de_poziție>=4||Activ)return (uint32_t)-22;
    저장된작업 *șir_date=&저장값[index_de_poziție];
    if(Acțiuni>=32){if(șir_date->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(șir_date->Fișier_Listă[순번]>=0)pk_close(șir_date->Fișier_Listă[순번]);for(unsigned 순번=0;순번<24;순번++)if(șir_date->통신끝점들[순번])통신끝점닫기(순번+32);}șir_date->멈춤상태=0;화면초기화(index_de_poziție);return 0;}
    if(Acțiuni>=16)return șir_date->멈춤상태;
    if(!șir_date->멈춤상태)return (uint32_t)-22;
    proprietar_obiect=index_de_poziție;대화형=șir_date->대화형;리눅스규약=șir_date->리눅스규약;동적기억끝=șir_date->동적기억공간;전달인수개수=șir_date->인수개수;
    memcpy(Fișier_Listă,șir_date->Fișier_Listă,sizeof(Fișier_Listă));memcpy(통신끝점들,șir_date->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,șir_date->argument_ARRAY,sizeof(전달인수));memcpy(전달인수길이,șir_date->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<utilizator_pagina_COUNT;순번++)pagina_Listă[순번]=(utilizator_BASE+순번*dimensiune_pagină)|nucleu_pagina;변환표맞추기();
    memset((void *)utilizator_BASE,0,utilizator_termina_un_apel-utilizator_BASE);
    for(unsigned 순번=0;순번<utilizator_pagina_COUNT;순번++)if(șir_date->Permisiuni_Listă[순번])memcpy((void *)(utilizator_BASE+순번*dimensiune_pagină),(unsigned char *)clip_video(index_de_poziție)+순번*dimensiune_pagină,dimensiune_pagină);
    memcpy(Permisiuni_Listă,șir_date->Permisiuni_Listă,sizeof(Permisiuni_Listă));
    for(unsigned 순번=0;순번<utilizator_pagina_COUNT;순번++){unsigned date_poziție=Permisiuni_Listă[순번];pagina_Listă[순번]=date_poziție?(utilizator_BASE+순번*dimensiune_pagină)|(date_poziție==3?utilizator_citire_scriere:date_poziție==5?사용자읽고실행:utilizator_doar_în_citire):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Activ=1;șir_date->멈춤상태=0;buta_TIMEOUT();
    utilizator_executare_oră[proprietar_obiect]=보드밀리초();
    return (uint32_t)sfârșit_program(utilizator_CV(&șir_date->executare_cadru,șir_date->mobil_p_Stare));
}
static int rula_program(const unsigned char *date, size_t Mărime, unsigned 전달값, int 리눅스방식, const char *Nume) {
    if (Activ) return -16;
    proprietar_obiect=Avizier_Terminal(11);if(proprietar_obiect<0||proprietar_obiect>3||저장값[proprietar_obiect].멈춤상태)return -16;대화형=0;
    int 유효함 = 실행파일검사(date, Mărime, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned nume_INDEX=0;
    while (*Nume && nume_INDEX<31) utilizator_comandă_nume[proprietar_obiect][nume_INDEX++]=(unsigned char)*Nume++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (nume_INDEX) utilizator_comandă_nume[proprietar_obiect][nume_INDEX++]=' ';
        for (unsigned index_de_poziție=0; index_de_poziție<전달인수길이[0]; index_de_poziție++) utilizator_comandă_nume[proprietar_obiect][nume_INDEX++]=전달인수[0][index_de_poziție];
    }
    utilizator_comandă_nume[proprietar_obiect][nume_INDEX]=0; număr_de_utilizator[proprietar_obiect]=Următorul_număr_de_utilizator++;
    if (Următorul_număr_de_utilizator>0x7fffffffu) Următorul_număr_de_utilizator=10;
    utilizator_buta_oră[proprietar_obiect]=보드밀리초(); 사용자누적시각[proprietar_obiect]=0;
    for (unsigned 순번 = 0; 순번 < utilizator_pagina_COUNT; 순번++) pagina_Listă[순번] = (utilizator_BASE + 순번 * dimensiune_pagină) | nucleu_pagina;
    변환표맞추기();
    memset((void *)utilizator_BASE, 0, utilizator_termina_un_apel - utilizator_BASE);
    memset(Permisiuni_Listă, 0, sizeof(Permisiuni_Listă));
    실행파일머리 실행머리; memcpy(&실행머리, date, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.program_Antet_COUNT; 순번++) {
        실행파일구획 date_poziție; memcpy(&date_poziție, date + 실행머리.program_Antet_OFFSET + 순번 * sizeof(date_poziție), sizeof(date_poziție));
        if (date_poziție.Tip_zonă != 1 || !date_poziție.기억영역크기) continue;
        if (date_poziție.파일영역크기) memcpy((void *)(uintptr_t)date_poziție.adresa, date + date_poziție.OFFSET_VALUE, date_poziție.파일영역크기);
        for (uintptr_t curent_poziție = date_poziție.adresa & ~(dimensiune_pagină - 1); curent_poziție < date_poziție.adresa + date_poziție.기억영역크기; curent_poziție += dimensiune_pagină) {
            Permisiuni_Listă[(curent_poziție - utilizator_BASE) / dimensiune_pagină] = (date_poziție.configurație_Serviciu_de_transfer_inteligent_în_fundal & 2) ? 3 : ((date_poziție.configurație_Serviciu_de_transfer_inteligent_în_fundal & 1) ? 5 : 1);
        }
    }
    for (uintptr_t curent_poziție = utilizator_Teanc_adresa; curent_poziție < utilizator_termina_un_apel; curent_poziție += dimensiune_pagină) Permisiuni_Listă[(curent_poziție - utilizator_BASE) / dimensiune_pagină] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.intrare_p) : utilizator_termina_un_apel;
    for (unsigned 순번 = 0; 순번 < utilizator_pagina_COUNT; 순번++) {
        unsigned permisiuni = Permisiuni_Listă[순번];
        pagina_Listă[순번] = permisiuni ? (utilizator_BASE + 순번 * dimensiune_pagină) | (permisiuni == 3 ? utilizator_citire_scriere : permisiuni == 5 ? 사용자읽고실행 : utilizator_doar_în_citire) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) Fișier_Listă[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = utilizator_IMAGE_termina_un_apel;
    Activ = 1; buta_TIMEOUT();
    utilizator_executare_oră[proprietar_obiect]=보드밀리초();
    int KR = utilizator_introduce(실행머리.intrare_p, 초기쌓임공간, 전달값);
    return sfârșit_program(KR);
}
uintptr_t Avizier_utilizator_rula(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Nume=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)rula_program(실행항목들[LOOKUP_INDEX].date, 실행항목들[LOOKUP_INDEX].Mărime, 실행항목들[LOOKUP_INDEX].전달값, 0, Nume);
}
static uintptr_t executa_Fișier(int 리눅스방식) {
    static unsigned char IMAGE[16384];
    if (Activ || !전달인수개수) return (uint32_t)-22;
    int Fișier_handle = pk_open((const char *)전달인수[0], doar_în_citire_VALUE, 0);
    if (Fișier_handle < 0) return (uint32_t)-număr_de_eroare;
    int Mărime = pk_size(Fișier_handle);
    if (Mărime < 0 || (unsigned)Mărime > sizeof(IMAGE)) { pk_close(Fișier_handle); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(Fișier_handle, IMAGE, Mărime); pk_close(Fișier_handle);
    if (RECEIVED_COUNT != Mărime) return (uint32_t)-5;
    return (uint32_t)rula_program(IMAGE, Mărime, 0, 리눅스방식, "");
}
uintptr_t Avizier_utilizator_Fișier(void) { return executa_Fișier(0); }
uintptr_t 보드사용자리눅스파일(void) { return executa_Fișier(1); }
uintptr_t Avizier_utilizator_valida(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].date, 잘못된실행항목들[순번].Mărime) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
