#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Täida_käsk arvuti kiht_VALUE. Fail andmed/정책은 기존 AOT Java 커널에 위임한다.
#include "kasutaja.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../võrk_Virn/võrk_Virn.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define arvuti_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_levitaja 0xff841000ul
#define IRQ_CPU_liides 0xff842000ul
#define lehekülje_suurus 4096ul
#define pöördus_marker (1ul << 10)
#define Ei_Täida_luba (1ul << 53)
#define kasutaja_Ei_Täida (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | pöördus_marker)
#define tuum_leht (3ul | 보통기억 | Ei_Täida_luba | kasutaja_Ei_Täida)
#define 사용자읽고쓰기 (3ul | 보통기억 | (1ul << 6) | Ei_Täida_luba | kasutaja_Ei_Täida)
#define kasutaja_kirjutuskaitstud (3ul | 보통기억 | (3ul << 6) | Ei_Täida_luba | kasutaja_Ei_Täida)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | Ei_Täida_luba)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Tahvel_piksel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Tahvel_terminal(uintptr_t);
extern int terminal_ootel(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int kasutaja_jätkama(kasutaja_raam *,void *);
extern void 사용자실수보관(void *);
extern int kasutaja_sisestama(uintptr_t kirje_p, uintptr_t Virn_salvesti, uintptr_t 전달값);
extern void kasutaja_tagasi_saatma(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t juur_ADDRESS[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t leht_Loend[kasutaja_leht_COUNT] __attribute__((aligned(4096)));
static uint8_t Õigused_Loend[kasutaja_leht_COUNT];
static int Aktiivne, Fail_Loend[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned Fail_pide){return Fail_pide<40?자바전문닫기(Fail_pide):자바흐름닫기(Fail_pide);}
static uint64_t sagedus, tähtaeg_Aeg;
static uintptr_t 동적기억끝;
// tuum_VALUE 셸이 준비한 UTF-8 Argumendid. EL0에는 eksemplar_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,대화형,리눅스규약,Fail_Loend[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argument_ARRAY[8][256],Õigused_Loend[kasutaja_leht_COUNT];
    uintptr_t 동적기억공간; kasutaja_raam 실행틀;
    unsigned char ujuv_p_Olek[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int omanik_objekt,대화형;
static uint32_t kasutajanumber[4], kasutaja_START_Aeg[4], 사용자누적시각[4], 사용자실행시각[4], Edasi_kasutajanumber=10;
static unsigned char kasutaja_käsk_nimetus[4][288];
uint32_t 사용자상태읽기(unsigned kirje_VALUE, unsigned INDEX) {
    unsigned asukohaindeks=INDEX&3;
    int Olek_VALUE=(Aktiivne && omanik_objekt==(int)asukohaindeks) ? 1 : 저장값[asukohaindeks].멈춤상태 ? 2 : 0;
    if (kirje_VALUE==0) return Olek_VALUE;
    if (!Olek_VALUE) return 0;
    if (kirje_VALUE==1) return kasutajanumber[asukohaindeks];
    if (kirje_VALUE==2) {
        unsigned char *쪽들=Olek_VALUE==1?Õigused_Loend:저장값[asukohaindeks].Õigused_Loend;
        unsigned leht_COUNT=0; for (unsigned 순번=0; 순번<kasutaja_leht_COUNT; 순번++) if(쪽들[순번]) leht_COUNT++;
        return leht_COUNT*4;
    }
    if (kirje_VALUE==3) return (uint32_t)보드밀리초()-kasutaja_START_Aeg[asukohaindeks];
    if (kirje_VALUE==4) return 사용자누적시각[asukohaindeks]+(Olek_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[asukohaindeks]:0);
    if (kirje_VALUE==5) return INDEX/4<sizeof(kasutaja_käsk_nimetus[0])?kasutaja_käsk_nimetus[asukohaindeks][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t kirje_COUNT) {
    if (Aktiivne || kirje_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = kirje_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t tähtaja_piires_ametikoht, uintptr_t bait_andmed) {
    if (Aktiivne || LOOKUP_INDEX >= 전달인수개수 || tähtaja_piires_ametikoht >= 255 || tähtaja_piires_ametikoht != 전달인수길이[LOOKUP_INDEX] || !bait_andmed || bait_andmed > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][tähtaja_piires_ametikoht] = bait_andmed;
    전달인수길이[LOOKUP_INDEX] = tähtaja_piires_ametikoht + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Kell_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Peata_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    arvuti_register(IRQ_levitaja + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void START_TIMEOUT(void) {
    uint64_t 간격 = sagedus * 2, lubama = 1;
    tähtaeg_Aeg = Kell_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(lubama) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned andmeplokk = 0; andmeplokk < 4; andmeplokk++) {
        juur_ADDRESS[andmeplokk] = (uintptr_t)가운데[andmeplokk] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t ADDRESS = ((uintptr_t)andmeplokk << 30) | ((uintptr_t)순번 << 21);
            가운데[andmeplokk][순번] = ADDRESS | 1 | pöördus_marker | kasutaja_Ei_Täida;
            if (ADDRESS >= 0xfc000000ul) 가운데[andmeplokk][순번] |= Ei_Täida_luba; // Device-nGnRnE
            else 가운데[andmeplokk][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < kasutaja_leht_COUNT / 512; SECOND_VALUE++)
        가운데[0][(kasutaja_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(leht_Loend + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < kasutaja_leht_COUNT; 순번++) leht_Loend[순번] = (kasutaja_BASE + 순번 * lehekülje_suurus) | tuum_leht;
    uint64_t Mälu_atribuut_register = 0x4400, ADDRESS_Tõlkimine_meede = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Mälu_atribuut_register), "r"(ADDRESS_Tõlkimine_meede), "r"((uintptr_t)juur_ADDRESS) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t ujuv_p_Olek = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(ujuv_p_Olek) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(sagedus));
    Peata_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 kirje_p_VALUE 때만 Luba_VALUE.
    arvuti_register(IRQ_levitaja) = 0;
    arvuti_register(IRQ_levitaja + 0x180) = 0xffffffff;
    arvuti_register(IRQ_levitaja + 0x80) = 0xffffffff;
    arvuti_register(IRQ_levitaja + 0x280) = 1u << 30;
    arvuti_register(IRQ_levitaja + 0x41c) = 0x80808080;
    arvuti_register(IRQ_levitaja + 0x100) = 1u << 30;
    arvuti_register(IRQ_CPU_liides + 4) = 0xff;
    arvuti_register(IRQ_CPU_liides + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 number 있다.
    int Turve = (arvuti_register(IRQ_levitaja + 4) & (1u << 10)) != 0;
    arvuti_register(IRQ_levitaja) = Turve ? 1 : 3;
    arvuti_register(IRQ_CPU_liides) = Turve ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_ala, arvuti_TYPE; uint32_t versiooninumber;
    uint64_t kirje_p, programm_Päis_nihe, jaotise_päis_nihe; uint32_t konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus;
    uint16_t 실행머리크기, programm_Päis_kirje_suurust_muutma, programm_Päis_COUNT, jaotise_päis_kirje_suurust_muutma, jaotise_päis_COUNT, jaotis_nimetus_tabel_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_ala, konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus; uint64_t nihe_VALUE, ADDRESS, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(kasutaja_raam) == 272, "exception assembly layout");
static int 포함된범위(uint64_t nihe_VALUE, uint64_t Suurus, uint64_t lõpeta_kõne_nihe) {
    return nihe_VALUE <= lõpeta_kõne_nihe && Suurus <= lõpeta_kõne_nihe - nihe_VALUE;
}
static int 부가정보검사(const unsigned char *andmed_ametikoht, size_t Suurus) {
    size_t tähtaja_piires_ametikoht = 0;
    while (포함된범위(tähtaja_piires_ametikoht, 12, Suurus)) {
        uint32_t 낱말들[3]; memcpy(낱말들, andmed_ametikoht + tähtaja_piires_ametikoht, 12); tähtaja_piires_ametikoht += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(tähtaja_piires_ametikoht, 이름영역크기, Suurus) || !포함된범위(tähtaja_piires_ametikoht + 이름영역크기, 설명크기, Suurus)) return 0;
        const unsigned char Nimi_2[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Nimi_2) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Nimi_2); 순번++) if (andmed_ametikoht[tähtaja_piires_ametikoht + 순번] != Nimi_2[순번]) 일치 = 0;
        uint32_t versiooninumber = 0;
        if (일치) memcpy(&versiooninumber, andmed_ametikoht + tähtaja_piires_ametikoht + 이름영역크기, 4);
        if (일치 && versiooninumber == 1) return 1;
        tähtaja_piires_ametikoht += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *andmed, size_t Suurus, int 리눅스방식) {
    if (Suurus < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, andmed, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_ala != 2 || 실행머리.arvuti_TYPE != 183 || 실행머리.versiooninumber != 1 || 실행머리.konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.programm_Päis_kirje_suurust_muutma != sizeof(실행파일구획) || !실행머리.programm_Päis_COUNT || 실행머리.programm_Päis_COUNT > 16 ||
        실행머리.programm_Päis_nihe < sizeof(실행머리) || !포함된범위(실행머리.programm_Päis_nihe, (uint64_t)실행머리.programm_Päis_COUNT * sizeof(실행파일구획), Suurus)) return 사용자실행파일오류;
    uint8_t 사용량[(kasutaja_pilt_lõpeta_kõne - kasutaja_BASE) / lehekülje_suurus] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.programm_Päis_COUNT; 순번++) {
        실행파일구획 andmed_ametikoht; memcpy(&andmed_ametikoht, andmed + 실행머리.programm_Päis_nihe + 순번 * sizeof(andmed_ametikoht), sizeof(andmed_ametikoht));
        if (andmed_ametikoht.TYPE_ala == 4) {
            if (!포함된범위(andmed_ametikoht.nihe_VALUE, andmed_ametikoht.파일영역크기, Suurus)) return 사용자실행파일오류;
            if (부가정보검사(andmed + andmed_ametikoht.nihe_VALUE, andmed_ametikoht.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (andmed_ametikoht.TYPE_ala == 0 || andmed_ametikoht.TYPE_ala == 6 || (andmed_ametikoht.TYPE_ala == 0x6474e551 && !(andmed_ametikoht.konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus & 1))) continue;
        if (andmed_ametikoht.TYPE_ala != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!andmed_ametikoht.기억영역크기) continue;
        if (andmed_ametikoht.konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus & ~7u || !(andmed_ametikoht.konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus & 4) || (andmed_ametikoht.konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus & 3) == 3 || andmed_ametikoht.파일영역크기 > andmed_ametikoht.기억영역크기 ||
            (andmed_ametikoht.파일영역크기 && !포함된범위(andmed_ametikoht.nihe_VALUE, andmed_ametikoht.파일영역크기, Suurus)) || andmed_ametikoht.ADDRESS < kasutaja_BASE ||
            !포함된범위(andmed_ametikoht.ADDRESS, andmed_ametikoht.기억영역크기, kasutaja_pilt_lõpeta_kõne) ||
            (!리눅스방식 && ((andmed_ametikoht.ADDRESS & (lehekülje_suurus - 1)) || (andmed_ametikoht.nihe_VALUE & (lehekülje_suurus - 1)) || andmed_ametikoht.맞춤 != lehekülje_suurus)) ||
            (리눅스방식 && (((andmed_ametikoht.ADDRESS ^ andmed_ametikoht.nihe_VALUE) & (lehekülje_suurus - 1)) || !andmed_ametikoht.맞춤 ||
                (andmed_ametikoht.맞춤 & (andmed_ametikoht.맞춤 - 1)) || andmed_ametikoht.맞춤 > 0x200000 || ((andmed_ametikoht.ADDRESS ^ andmed_ametikoht.nihe_VALUE) & (andmed_ametikoht.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (andmed_ametikoht.ADDRESS - kasutaja_BASE) / lehekülje_suurus;
        unsigned kirje_COUNT = ((andmed_ametikoht.ADDRESS & (lehekülje_suurus - 1)) + andmed_ametikoht.기억영역크기 + lehekülje_suurus - 1) / lehekülje_suurus;
        for (unsigned leht_VALUE = 첫항목; leht_VALUE < 첫항목 + kirje_COUNT; leht_VALUE++) {
            if (사용량[leht_VALUE]) return 사용자실행파일오류;
            사용량[leht_VALUE] = 1;
        }
        if ((andmed_ametikoht.konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus & 1) && 실행머리.kirje_p >= andmed_ametikoht.ADDRESS && 실행머리.kirje_p < andmed_ametikoht.ADDRESS + andmed_ametikoht.파일영역크기 && !(실행머리.kirje_p & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *andmed, size_t Suurus) { return 실행파일검사(andmed, Suurus, 0); }
static void küljendus(uintptr_t ADDRESS, uint64_t konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus, unsigned õigused) {
    unsigned LOOKUP_INDEX = (ADDRESS - kasutaja_BASE) / lehekülje_suurus;
    leht_Loend[LOOKUP_INDEX] = ADDRESS | konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus;
    Õigused_Loend[LOOKUP_INDEX] = õigused;
}
static int kasutaja_vahemik(uintptr_t ADDRESS, size_t kirje_COUNT, int 쓰는중) {
    if (ADDRESS < kasutaja_BASE || !포함된범위(ADDRESS, kirje_COUNT, kasutaja_lõpeta_kõne)) return 0;
    if (!kirje_COUNT) return 1;
    unsigned 첫항목 = (ADDRESS - kasutaja_BASE) / lehekülje_suurus, 마지막 = (ADDRESS + kirje_COUNT - 1 - kasutaja_BASE) / lehekülje_suurus;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Õigused_Loend[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int eksemplar_tee(uintptr_t ADDRESS, char *RADA) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!kasutaja_vahemik(ADDRESS, 1, 0)) return -14;
        RADA[순번] = *(const char *)ADDRESS++;
        if (!RADA[순번]) return 0;
    }
    return -36;
}
static intptr_t tuum_näitaja(intptr_t TULEMUS) { return TULEMUS < 0 ? -tõrke_number : TULEMUS; }
static int 대응파일기술자(uint64_t Fail_pide) { return Fail_pide >= 3 && Fail_pide < 19 ? Fail_Loend[Fail_pide - 3] : -1; }
static int 통신끝점소유(uint64_t Fail_pide) { return Fail_pide >= 32 && Fail_pide < 56 && 통신끝점들[Fail_pide - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t 길이, struct pk_sockaddr_in *ADDRESS) {
    if (길이 != sizeof(*ADDRESS)) return -22;
    if (!kasutaja_vahemik(가리킴값, 길이, 0)) return -14;
    memcpy(ADDRESS, (const void *)가리킴값, sizeof(*ADDRESS));
    return ADDRESS->sin_family == AF_INET ? 0 : -97;
}
static int ADDRESS_toodang_tšekk(uintptr_t 가리킴값, uintptr_t 길이포인터, pk_socklen_t *puhver_võimsus) {
    if (!kasutaja_vahemik(길이포인터, sizeof(*puhver_võimsus), 1)) return -14;
    memcpy(puhver_võimsus, (const void *)길이포인터, sizeof(*puhver_võimsus));
    if (*puhver_võimsus > sizeof(struct pk_sockaddr_in)) *puhver_võimsus = sizeof(struct pk_sockaddr_in);
    if (*puhver_võimsus && !kasutaja_vahemik(가리킴값, *puhver_võimsus, 1)) return -14;
    return 0;
}
static void ADDRESS_toodang(uintptr_t 가리킴값, uintptr_t 길이포인터, pk_socklen_t puhver_võimsus, int ADDRESS, int pordinumber) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(pordinumber); VALUE.sin_addr.s_addr = pk_htonl(ADDRESS);
    if (puhver_võimsus) memcpy((void *)가리킴값, &VALUE, puhver_võimsus);
    pk_socklen_t 길이 = sizeof(VALUE); memcpy((void *)길이포인터, &길이, sizeof(길이));
}
extern uintptr_t Tahvel_Kanal(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(kasutaja_raam *Fail_kirje) {
    uintptr_t 첫째값 = Fail_kirje->register_andmed[0], SECOND_VALUE = Fail_kirje->register_andmed[1], koodipunkt = Fail_kirje->register_andmed[2];
    char RADA[65];
    int Fail_pide, TULEMUS;
    switch (Fail_kirje->register_andmed[8]) {
    case 0: return 1; // oma ABI 버전
    case 1: // write: kursor 전체를 검사한 Tagasi_VALUE Väljund/Fail muutma_VALUE
        if (koodipunkt > 65536) return -22;
        if (!kasutaja_vahemik(SECOND_VALUE, koodipunkt, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t START_toodang=Kell_VALUE();
            for (size_t 순번 = 0; 순번 < koodipunkt; 순번++) Tahvel_Kanal(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 tuum_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(대화형){
                tähtaeg_Aeg+=Kell_VALUE()-START_toodang;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(tähtaeg_Aeg) : "memory");
            }
            return koodipunkt;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t kaup_COUNT=koodipunkt>512?512:koodipunkt;for(size_t 순번=0;순번<kaup_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,kaup_COUNT);
        }
        Fail_pide = 대응파일기술자(첫째값); if (Fail_pide < 0) return -9;
        return tuum_näitaja(pk_write(Fail_pide, (const void *)SECOND_VALUE, koodipunkt));
    case 2:
        if (koodipunkt > 65536) return -22;
        if (!kasutaja_vahemik(SECOND_VALUE, koodipunkt, 1)) return -14;
        if (첫째값 == 0) {
            size_t kaup_COUNT = 0;
            while (kaup_COUNT < koodipunkt) {
                int märk_VALUE = (int32_t)보드글자읽기(); if (märk_VALUE == -2) return kaup_COUNT; if (märk_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[kaup_COUNT++] = märk_VALUE;
            }
            return kaup_COUNT ? (intptr_t)kaup_COUNT : (koodipunkt ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            TULEMUS=자바흐름읽기(첫째값,koodipunkt>512?512:koodipunkt);if(TULEMUS>0)for(int 순번=0;순번<TULEMUS;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return TULEMUS;
        }
        Fail_pide = 대응파일기술자(첫째값); if (Fail_pide < 0) return -9;
        return tuum_näitaja(pk_read(Fail_pide, (void *)SECOND_VALUE, koodipunkt));
    case 3:
        TULEMUS = eksemplar_tee(첫째값, RADA); if (TULEMUS) return TULEMUS;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (Fail_Loend[순번] < 0) {
            Fail_pide = pk_open(RADA, (int)SECOND_VALUE, 0600);
            if (Fail_pide < 0) return -tõrke_number;
            Fail_Loend[순번] = Fail_pide; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { TULEMUS = 통신끝점닫기(첫째값); if (!TULEMUS) 통신끝점들[첫째값 - 32] = 0; return TULEMUS; }
        Fail_pide = 대응파일기술자(첫째값); if (Fail_pide < 0) return -9;
        TULEMUS = pk_close(Fail_pide); if (!TULEMUS) Fail_Loend[첫째값 - 3] = -1;
        return tuum_näitaja(TULEMUS);
    case 5:
        Fail_pide = 대응파일기술자(첫째값); if (Fail_pide < 0) return -9;
        if (koodipunkt > 2) return -22;
        return tuum_näitaja(pk_lseek(Fail_pide, (int64_t)SECOND_VALUE, koodipunkt));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 kasutaja RW/NX 힙, 새로 노출되는 페이지는 0으로 초기화
        if (!첫째값) return 동적기억끝;
        if (첫째값 < kasutaja_pilt_lõpeta_kõne || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + lehekülje_suurus - 1) & ~(lehekülje_suurus - 1);
        uintptr_t 새쪽들 = (첫째값 + lehekülje_suurus - 1) & ~(lehekülje_suurus - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t andmed_ametikoht = 이전쪽들; andmed_ametikoht < 새쪽들; andmed_ametikoht += lehekülje_suurus) küljendus(andmed_ametikoht, tuum_leht, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t andmed_ametikoht = 이전쪽들; andmed_ametikoht < 새쪽들; andmed_ametikoht += lehekülje_suurus) küljendus(andmed_ametikoht, 사용자읽고쓰기, 3);
        } else {
            for (uintptr_t andmed_ametikoht = 새쪽들; andmed_ametikoht < 이전쪽들; andmed_ametikoht += lehekülje_suurus) {
                leht_Loend[(andmed_ametikoht - kasutaja_BASE) / lehekülje_suurus] = 0; Õigused_Loend[(andmed_ametikoht - kasutaja_BASE) / lehekülje_suurus] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        Fail_pide = 대응파일기술자(첫째값); return Fail_pide < 0 ? -9 : tuum_näitaja(pk_size(Fail_pide));
    case 10:
        Fail_pide = 대응파일기술자(첫째값); return Fail_pide < 0 ? -9 : tuum_näitaja(pk_ftruncate(Fail_pide, (int64_t)SECOND_VALUE));
    case 11:
        TULEMUS = eksemplar_tee(첫째값, RADA); return TULEMUS ? TULEMUS : tuum_näitaja(pk_unlink(RADA));
    case 12:
        Fail_pide = 대응파일기술자(첫째값); return Fail_pide < 0 ? -9 : tuum_näitaja(pk_fsync(Fail_pide));
    case 13: { // 그래픽 기초 API: kasutaja 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Fail_kirje->register_andmed[3], 높이값 = Fail_kirje->register_andmed[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t 세로좌표 = SECOND_VALUE; 세로좌표 < SECOND_VALUE + 높이값; 세로좌표++) for (uintptr_t 가로좌표 = 첫째값; 가로좌표 < 첫째값 + 너비값; 가로좌표++) Tahvel_piksel(가로좌표, 세로좌표, koodipunkt);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=kaup_COUNT; args(index,buffer,capacity)=UTF-8 길이
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (koodipunkt <= 전달인수길이[첫째값]) return -36;
        if (!kasutaja_vahemik(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;대화형=1;return Tahvel_terminal(13);}
        if(첫째값==2){대화형=0;return 0;}
        if(첫째값==3)return Tahvel_terminal(13);
        if(첫째값!=1||!대화형)return -22;
        TULEMUS=(int32_t)보드글자읽기();
        if(TULEMUS==-4096)return TULEMUS;
        START_TIMEOUT();return TULEMUS<0?-11:TULEMUS;
    case 17: { // 유한한 협력 Oota_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t lõpeta_kõne_Aeg = Kell_VALUE() + sagedus * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Kell_VALUE() < lõpeta_kõne_Aeg);
        START_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 ema_VALUE·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        TULEMUS = eksemplar_tee(첫째값, RADA); if (TULEMUS) return TULEMUS;
        unsigned 길이 = 0; while (RADA[길이]) 길이++;
        TULEMUS = 자바경로시작(길이); if (TULEMUS < 0) return TULEMUS;
        for (unsigned 순번 = 0; 순번 < 길이; 순번++) 자바경로바이트(순번, (unsigned char)RADA[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int märk_VALUE=(int32_t)보드글자읽기();if(märk_VALUE==-4096)return märk_VALUE;if(märk_VALUE>=0)화면누름(omanik_objekt,märk_VALUE);START_TIMEOUT();}
        if(첫째값==3&&koodipunkt){if(!자바셸대화형())return -95;대화형=1;Tahvel_terminal(300);}
        return 화면호출(omanik_objekt,첫째값,SECOND_VALUE,koodipunkt,Fail_kirje->register_andmed[3],Fail_kirje->register_andmed[4],Fail_kirje->register_andmed[5]);
    case 21:
        if(koodipunkt>127)return -22;if(!kasutaja_vahemik(SECOND_VALUE,koodipunkt*sizeof(uint32_t),0))return -14;
        return 화면글(omanik_objekt,첫째값,(const uint32_t *)SECOND_VALUE,koodipunkt);
    case 22: // 화면 Suurus päring_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(koodipunkt==0||koodipunkt==6))TULEMUS=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(koodipunkt==0||koodipunkt==IPPROTO_UDP))TULEMUS=자바전문만들기(첫째값,SECOND_VALUE,koodipunkt);
        else return -93;
        if (TULEMUS >= 32 && TULEMUS < 56) 통신끝점들[TULEMUS - 32] = 1;
        return TULEMUS;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in ADDRESS;
        TULEMUS = 주소입력(SECOND_VALUE, koodipunkt, &ADDRESS); if (TULEMUS) return TULEMUS;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(ADDRESS.sin_addr.s_addr),pk_htons(ADDRESS.sin_port)):자바전문묶기(첫째값, pk_htonl(ADDRESS.sin_addr.s_addr), pk_htons(ADDRESS.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Fail_kirje->register_andmed[3]) return -95;
        if (koodipunkt > 512) return -90;
        if (koodipunkt && !kasutaja_vahemik(SECOND_VALUE, koodipunkt, 0)) return -14;
        struct pk_sockaddr_in ADDRESS;
        TULEMUS = 주소입력(Fail_kirje->register_andmed[4], Fail_kirje->register_andmed[5], &ADDRESS); if (TULEMUS) return TULEMUS;
        for (unsigned 순번 = 0; 순번 < koodipunkt; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(ADDRESS.sin_addr.s_addr), pk_htons(ADDRESS.sin_port), koodipunkt);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Fail_kirje->register_andmed[3]) return -95;
        if (koodipunkt > 512) return -90;
        if (koodipunkt && !kasutaja_vahemik(SECOND_VALUE, koodipunkt, 1)) return -14;
        pk_socklen_t puhver_võimsus = 0;
        if (Fail_kirje->register_andmed[4]) { TULEMUS = ADDRESS_toodang_tšekk(Fail_kirje->register_andmed[4], Fail_kirje->register_andmed[5], &puhver_võimsus); if (TULEMUS) return TULEMUS; }
        TULEMUS = 자바전문받기(첫째값, koodipunkt); if (TULEMUS < 0) return TULEMUS;
        for (int 순번 = 0; 순번 < TULEMUS; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (Fail_kirje->register_andmed[4]) ADDRESS_toodang(Fail_kirje->register_andmed[4], Fail_kirje->register_andmed[5], puhver_võimsus, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return TULEMUS;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t puhver_võimsus;
        TULEMUS = ADDRESS_toodang_tšekk(SECOND_VALUE, koodipunkt, &puhver_võimsus); if (TULEMUS) return TULEMUS;
        ADDRESS_toodang(SECOND_VALUE,koodipunkt,puhver_võimsus,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in ADDRESS;
        TULEMUS=주소입력(SECOND_VALUE,koodipunkt,&ADDRESS);if(TULEMUS)return TULEMUS;
        return 자바흐름연결(첫째값,pk_htonl(ADDRESS.sin_addr.s_addr),pk_htons(ADDRESS.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||koodipunkt)return -95;TULEMUS=자바흐름연결받기(첫째값);if(TULEMUS>=40&&TULEMUS<56)통신끝점들[TULEMUS-32]=1;return TULEMUS;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(kasutaja_raam *Fail_kirje) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Fail_kirje) : 자체체계호출(Fail_kirje);
}
static void tagasi_saatma_tuum(kasutaja_raam *Fail_kirje, int TULEMUS) {
    Peata_TIMEOUT();
    Fail_kirje->register_andmed[0] = (uint64_t)(int64_t)TULEMUS;
    Fail_kirje->käsk_ametikoht = (uintptr_t)kasutaja_tagasi_saatma;
    Fail_kirje->Olek_CODE = 0x3c5; // EL1h, DAIF masked
}
int kasutajaerand(kasutaja_raam *Fail_kirje, unsigned telglõik) {
    if (!Aktiivne || (Fail_kirje->Olek_CODE & 15) != 0) return 0;
    if (telglõik) {
        uint32_t 승인값 = arvuti_register(IRQ_CPU_liides + 0xc), identifikaator_VALUE = 승인값 & 1023;
        if (identifikaator_VALUE == 30) { tagasi_saatma_tuum(Fail_kirje, kasutaja_TIMEOUT); arvuti_register(IRQ_CPU_liides + 0x10) = 승인값; return 1; }
        if (identifikaator_VALUE < 1020) arvuti_register(IRQ_CPU_liides + 0x10) = 승인값;
        return 1;
    }
    uint64_t erand_Olek; __asm__ volatile("mrs %0, esr_el1" : "=r"(erand_Olek));
    if (Kell_VALUE() >= tähtaeg_Aeg) { tagasi_saatma_tuum(Fail_kirje, kasutaja_TIMEOUT); return 1; }
    unsigned erand_ala = erand_Olek >> 26;
    if (erand_ala == 0x15 && (erand_Olek & 0xffff) == 0) {
        if (리눅스규약 ? Fail_kirje->register_andmed[8] == 93 || Fail_kirje->register_andmed[8] == 94 : Fail_kirje->register_andmed[8] == 6) tagasi_saatma_tuum(Fail_kirje, (int)(Fail_kirje->register_andmed[0] & 255));
        else {
            intptr_t TULEMUS=체계호출(Fail_kirje);
            if(TULEMUS==-4096&&대화형){
                저장값[omanik_objekt].실행틀=*Fail_kirje;저장값[omanik_objekt].실행틀.käsk_ametikoht-=4;
                사용자실수보관(저장값[omanik_objekt].ujuv_p_Olek);tagasi_saatma_tuum(Fail_kirje,사용자중단됨);
            }else Fail_kirje->register_andmed[0]=(uint64_t)TULEMUS;
        }
    } else tagasi_saatma_tuum(Fail_kirje, erand_ala == 0x24 ? kasutaja_andmed_tõrge : erand_ala == 0x20 ? 사용자실행오류 : 사용자잘못된명령);
    return 1;
}

// 생성된 const ELF Rühm_VALUE: 실행은 반드시 programm_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *andmed; size_t Suurus; unsigned 전달값; } programm;
#include "programs.h"
static void *hetktõmmis(unsigned asukohaindeks){return (void *)(0x04000000ul+asukohaindeks*(kasutaja_lõpeta_kõne-kasutaja_BASE));}
static int lõpp_programm(int TULEMUS){
    사용자누적시각[omanik_objekt]+=(uint32_t)보드밀리초()-사용자실행시각[omanik_objekt];
    Peata_TIMEOUT();Aktiivne=0;
    if(TULEMUS==사용자중단됨){
        저장된작업 *string_andmed=&저장값[omanik_objekt];string_andmed->멈춤상태=1;string_andmed->대화형=대화형;string_andmed->리눅스규약=리눅스규약;string_andmed->동적기억공간=동적기억끝;string_andmed->인수개수=전달인수개수;
        memcpy(string_andmed->Õigused_Loend,Õigused_Loend,sizeof(Õigused_Loend));memcpy(string_andmed->Fail_Loend,Fail_Loend,sizeof(Fail_Loend));memcpy(string_andmed->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(string_andmed->argument_ARRAY,전달인수,sizeof(전달인수));memcpy(string_andmed->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<kasutaja_leht_COUNT;순번++)if(Õigused_Loend[순번])memcpy((unsigned char *)hetktõmmis(omanik_objekt)+순번*lehekülje_suurus,(void *)(kasutaja_BASE+순번*lehekülje_suurus),lehekülje_suurus);
    }else{
        저장값[omanik_objekt].멈춤상태=0;화면초기화(omanik_objekt);
        for(unsigned 순번=0;순번<16;순번++)if(Fail_Loend[순번]>=0)pk_close(Fail_Loend[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<kasutaja_leht_COUNT;순번++){leht_Loend[순번]=0;Õigused_Loend[순번]=0;}변환표맞추기();return TULEMUS;
}
uintptr_t Tahvel_kasutusjuhtelement(uintptr_t Nimi){
    unsigned asukohaindeks=Nimi&15;if(asukohaindeks>=4||Aktiivne)return (uint32_t)-22;
    저장된작업 *string_andmed=&저장값[asukohaindeks];
    if(Nimi>=32){if(string_andmed->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(string_andmed->Fail_Loend[순번]>=0)pk_close(string_andmed->Fail_Loend[순번]);for(unsigned 순번=0;순번<24;순번++)if(string_andmed->통신끝점들[순번])통신끝점닫기(순번+32);}string_andmed->멈춤상태=0;화면초기화(asukohaindeks);return 0;}
    if(Nimi>=16)return string_andmed->멈춤상태;
    if(!string_andmed->멈춤상태)return (uint32_t)-22;
    omanik_objekt=asukohaindeks;대화형=string_andmed->대화형;리눅스규약=string_andmed->리눅스규약;동적기억끝=string_andmed->동적기억공간;전달인수개수=string_andmed->인수개수;
    memcpy(Fail_Loend,string_andmed->Fail_Loend,sizeof(Fail_Loend));memcpy(통신끝점들,string_andmed->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,string_andmed->argument_ARRAY,sizeof(전달인수));memcpy(전달인수길이,string_andmed->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<kasutaja_leht_COUNT;순번++)leht_Loend[순번]=(kasutaja_BASE+순번*lehekülje_suurus)|tuum_leht;변환표맞추기();
    memset((void *)kasutaja_BASE,0,kasutaja_lõpeta_kõne-kasutaja_BASE);
    for(unsigned 순번=0;순번<kasutaja_leht_COUNT;순번++)if(string_andmed->Õigused_Loend[순번])memcpy((void *)(kasutaja_BASE+순번*lehekülje_suurus),(unsigned char *)hetktõmmis(asukohaindeks)+순번*lehekülje_suurus,lehekülje_suurus);
    memcpy(Õigused_Loend,string_andmed->Õigused_Loend,sizeof(Õigused_Loend));
    for(unsigned 순번=0;순번<kasutaja_leht_COUNT;순번++){unsigned andmed_ametikoht=Õigused_Loend[순번];leht_Loend[순번]=andmed_ametikoht?(kasutaja_BASE+순번*lehekülje_suurus)|(andmed_ametikoht==3?사용자읽고쓰기:andmed_ametikoht==5?사용자읽고실행:kasutaja_kirjutuskaitstud):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktiivne=1;string_andmed->멈춤상태=0;START_TIMEOUT();
    사용자실행시각[omanik_objekt]=보드밀리초();
    return (uint32_t)lõpp_programm(kasutaja_jätkama(&string_andmed->실행틀,string_andmed->ujuv_p_Olek));
}
static int sari_programm(const unsigned char *andmed, size_t Suurus, unsigned 전달값, int 리눅스방식, const char *Nimi_2) {
    if (Aktiivne) return -16;
    omanik_objekt=Tahvel_terminal(11);if(omanik_objekt<0||omanik_objekt>3||저장값[omanik_objekt].멈춤상태)return -16;대화형=0;
    int 유효함 = 실행파일검사(andmed, Suurus, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned nimetus_INDEX=0;
    while (*Nimi_2 && nimetus_INDEX<31) kasutaja_käsk_nimetus[omanik_objekt][nimetus_INDEX++]=(unsigned char)*Nimi_2++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (nimetus_INDEX) kasutaja_käsk_nimetus[omanik_objekt][nimetus_INDEX++]=' ';
        for (unsigned asukohaindeks=0; asukohaindeks<전달인수길이[0]; asukohaindeks++) kasutaja_käsk_nimetus[omanik_objekt][nimetus_INDEX++]=전달인수[0][asukohaindeks];
    }
    kasutaja_käsk_nimetus[omanik_objekt][nimetus_INDEX]=0; kasutajanumber[omanik_objekt]=Edasi_kasutajanumber++;
    if (Edasi_kasutajanumber>0x7fffffffu) Edasi_kasutajanumber=10;
    kasutaja_START_Aeg[omanik_objekt]=보드밀리초(); 사용자누적시각[omanik_objekt]=0;
    for (unsigned 순번 = 0; 순번 < kasutaja_leht_COUNT; 순번++) leht_Loend[순번] = (kasutaja_BASE + 순번 * lehekülje_suurus) | tuum_leht;
    변환표맞추기();
    memset((void *)kasutaja_BASE, 0, kasutaja_lõpeta_kõne - kasutaja_BASE);
    memset(Õigused_Loend, 0, sizeof(Õigused_Loend));
    실행파일머리 실행머리; memcpy(&실행머리, andmed, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.programm_Päis_COUNT; 순번++) {
        실행파일구획 andmed_ametikoht; memcpy(&andmed_ametikoht, andmed + 실행머리.programm_Päis_nihe + 순번 * sizeof(andmed_ametikoht), sizeof(andmed_ametikoht));
        if (andmed_ametikoht.TYPE_ala != 1 || !andmed_ametikoht.기억영역크기) continue;
        if (andmed_ametikoht.파일영역크기) memcpy((void *)(uintptr_t)andmed_ametikoht.ADDRESS, andmed + andmed_ametikoht.nihe_VALUE, andmed_ametikoht.파일영역크기);
        for (uintptr_t tähtaja_piires_ametikoht = andmed_ametikoht.ADDRESS & ~(lehekülje_suurus - 1); tähtaja_piires_ametikoht < andmed_ametikoht.ADDRESS + andmed_ametikoht.기억영역크기; tähtaja_piires_ametikoht += lehekülje_suurus) {
            Õigused_Loend[(tähtaja_piires_ametikoht - kasutaja_BASE) / lehekülje_suurus] = (andmed_ametikoht.konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus & 2) ? 3 : ((andmed_ametikoht.konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus & 1) ? 5 : 1);
        }
    }
    for (uintptr_t tähtaja_piires_ametikoht = kasutaja_Virn_ADDRESS; tähtaja_piires_ametikoht < kasutaja_lõpeta_kõne; tähtaja_piires_ametikoht += lehekülje_suurus) Õigused_Loend[(tähtaja_piires_ametikoht - kasutaja_BASE) / lehekülje_suurus] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.kirje_p) : kasutaja_lõpeta_kõne;
    for (unsigned 순번 = 0; 순번 < kasutaja_leht_COUNT; 순번++) {
        unsigned õigused = Õigused_Loend[순번];
        leht_Loend[순번] = õigused ? (kasutaja_BASE + 순번 * lehekülje_suurus) | (õigused == 3 ? 사용자읽고쓰기 : õigused == 5 ? 사용자읽고실행 : kasutaja_kirjutuskaitstud) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) Fail_Loend[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = kasutaja_pilt_lõpeta_kõne;
    Aktiivne = 1; START_TIMEOUT();
    사용자실행시각[omanik_objekt]=보드밀리초();
    int TULEMUS = kasutaja_sisestama(실행머리.kirje_p, 초기쌓임공간, 전달값);
    return lõpp_programm(TULEMUS);
}
uintptr_t Tahvel_kasutaja_sari(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Nimi_2=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)sari_programm(실행항목들[LOOKUP_INDEX].andmed, 실행항목들[LOOKUP_INDEX].Suurus, 실행항목들[LOOKUP_INDEX].전달값, 0, Nimi_2);
}
static uintptr_t Täida_Fail(int 리눅스방식) {
    static unsigned char pilt[16384];
    if (Aktiivne || !전달인수개수) return (uint32_t)-22;
    int Fail_pide = pk_open((const char *)전달인수[0], kirjutuskaitstud_VALUE, 0);
    if (Fail_pide < 0) return (uint32_t)-tõrke_number;
    int Suurus = pk_size(Fail_pide);
    if (Suurus < 0 || (unsigned)Suurus > sizeof(pilt)) { pk_close(Fail_pide); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(Fail_pide, pilt, Suurus); pk_close(Fail_pide);
    if (RECEIVED_COUNT != Suurus) return (uint32_t)-5;
    return (uint32_t)sari_programm(pilt, Suurus, 0, 리눅스방식, "");
}
uintptr_t Tahvel_kasutaja_Fail(void) { return Täida_Fail(0); }
uintptr_t 보드사용자리눅스파일(void) { return Täida_Fail(1); }
uintptr_t Tahvel_kasutaja_valideerima(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].andmed, 잘못된실행항목들[순번].Suurus) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
