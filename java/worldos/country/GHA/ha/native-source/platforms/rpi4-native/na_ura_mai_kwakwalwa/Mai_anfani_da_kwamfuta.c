#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 gudanar_Umarni na_ura_mai_kwakwalwa Tsarkiya_Daraja. Fayil Tarin_bayani/정책은 기존 AOT Java 커널에 위임한다.
#include "Mai_anfani_da_kwamfuta.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Hanyar_sadarwa_tara/Hanyar_sadarwa_tara.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_mai_rabawa 0xff841000ul
#define IRQ_CPU_Farfajiya 0xff842000ul
#define Girman_shafi 4096ul
#define 접근표시 (1ul << 10)
#define a_a_gudanar_izini (1ul << 53)
#define Mai_anfani_da_kwamfuta_a_a_gudanar (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define Kwara_shafi (3ul | 보통기억 | a_a_gudanar_izini | Mai_anfani_da_kwamfuta_a_a_gudanar)
#define Mai_anfani_da_kwamfuta_Rubutuwa_karantuwa (3ul | 보통기억 | (1ul << 6) | a_a_gudanar_izini | Mai_anfani_da_kwamfuta_a_a_gudanar)
#define Mai_anfani_da_kwamfuta_karanta_kawai (3ul | 보통기억 | (3ul << 6) | a_a_gudanar_izini | Mai_anfani_da_kwamfuta_a_a_gudanar)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | a_a_gudanar_izini)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t 보드화소(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t 보드터미널(uintptr_t);
extern int 터미널대기(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int Mai_anfani_da_kwamfuta_CV(Mai_anfani_da_kwamfuta_allo *,void *);
extern void 사용자실수보관(void *);
extern int Mai_anfani_da_kwamfuta_Shiga(uintptr_t Mashigar_bayanai_maki, uintptr_t tara_Wurin_adana, uintptr_t 전달값);
extern void 사용자복귀(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t 뿌리주소[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t shafi_Jeri[사용자쪽수] __attribute__((aligned(4096)));
static uint8_t Izini_Jeri[사용자쪽수];
static int Aiki_d9ba6551, Fayil_Jeri[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned Fayil_Mariki){return Fayil_Mariki<40?자바전문닫기(Fayil_Mariki):자바흐름닫기(Fayil_Mariki);}
static uint64_t 진동수, 마감시각;
static uintptr_t 동적기억끝;
// Kwara_Daraja 셸이 준비한 UTF-8 인수. EL0에는 Kwafi_Daraja 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,Shigar_da_umarni_na_kwamfuta,리눅스규약,Fayil_Jeri[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char Tubalin_aiki_TSARI[8][256],Izini_Jeri[사용자쪽수];
    uintptr_t 동적기억공간; Mai_anfani_da_kwamfuta_allo 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int mamallaki_abu,Shigar_da_umarni_na_kwamfuta;
static uint32_t 사용자번호[4], Mai_anfani_da_kwamfuta_Fara_lokaci[4], 사용자누적시각[4], 사용자실행시각[4], 다음사용자번호=10;
static unsigned char Mai_anfani_da_kwamfuta_Umarni_Suna[4][288];
uint32_t 사용자상태읽기(unsigned Mashigar_bayanai_Daraja, unsigned Indes) {
    unsigned 자리=Indes&3;
    int Matsayi_Daraja=(Aiki_d9ba6551 && mamallaki_abu==(int)자리) ? 1 : 저장값[자리].멈춤상태 ? 2 : 0;
    if (Mashigar_bayanai_Daraja==0) return Matsayi_Daraja;
    if (!Matsayi_Daraja) return 0;
    if (Mashigar_bayanai_Daraja==1) return 사용자번호[자리];
    if (Mashigar_bayanai_Daraja==2) {
        unsigned char *쪽들=Matsayi_Daraja==1?Izini_Jeri:저장값[자리].Izini_Jeri;
        unsigned 쪽수=0; for (unsigned 순번=0; 순번<사용자쪽수; 순번++) if(쪽들[순번]) 쪽수++;
        return 쪽수*4;
    }
    if (Mashigar_bayanai_Daraja==3) return (uint32_t)보드밀리초()-Mai_anfani_da_kwamfuta_Fara_lokaci[자리];
    if (Mashigar_bayanai_Daraja==4) return 사용자누적시각[자리]+(Matsayi_Daraja==1?(uint32_t)보드밀리초()-사용자실행시각[자리]:0);
    if (Mashigar_bayanai_Daraja==5) return Indes/4<sizeof(Mai_anfani_da_kwamfuta_Umarni_Suna[0])?Mai_anfani_da_kwamfuta_Umarni_Suna[자리][Indes/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t 항목수) {
    if (Aiki_d9ba6551 || 항목수 > 8) return (uint32_t)-22;
    전달인수개수 = 항목수;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t 색인, uintptr_t 현재위치, uintptr_t bayit_Tarin_bayani) {
    if (Aiki_d9ba6551 || 색인 >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[색인] || !bayit_Tarin_bayani || bayit_Tarin_bayani > 255)
        return (uint32_t)-22;
    전달인수[색인][현재위치] = bayit_Tarin_bayani;
    전달인수길이[색인] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t agogo_Daraja(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void 시간제한멈춤(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    기계저장기(IRQ_mai_rabawa + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void 시간제한시작(void) {
    uint64_t 간격 = 진동수 * 2, kunna = 1;
    마감시각 = agogo_Daraja() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(kunna) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned Tarin_bayani_bulo = 0; Tarin_bayani_bulo < 4; Tarin_bayani_bulo++) {
        뿌리주소[Tarin_bayani_bulo] = (uintptr_t)가운데[Tarin_bayani_bulo] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t imel = ((uintptr_t)Tarin_bayani_bulo << 30) | ((uintptr_t)순번 << 21);
            가운데[Tarin_bayani_bulo][순번] = imel | 1 | 접근표시 | Mai_anfani_da_kwamfuta_a_a_gudanar;
            if (imel >= 0xfc000000ul) 가운데[Tarin_bayani_bulo][순번] |= a_a_gudanar_izini; // Device-nGnRnE
            else 가운데[Tarin_bayani_bulo][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned 둘째값 = 0; 둘째값 < 사용자쪽수 / 512; 둘째값++)
        가운데[0][(사용자바탕 >> 21) + 둘째값] = (uintptr_t)(shafi_Jeri + 둘째값 * 512) | 3;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) shafi_Jeri[순번] = (사용자바탕 + 순번 * Girman_shafi) | Kwara_shafi;
    uint64_t 기억속성저장값 = 0x4400, 주소변환제어 = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(기억속성저장값), "r"(주소변환제어), "r"((uintptr_t)뿌리주소) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    시간제한멈춤();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 Mashigar_bayanai_maki_Daraja 때만 Bada_izini_Daraja.
    기계저장기(IRQ_mai_rabawa) = 0;
    기계저장기(IRQ_mai_rabawa + 0x180) = 0xffffffff;
    기계저장기(IRQ_mai_rabawa + 0x80) = 0xffffffff;
    기계저장기(IRQ_mai_rabawa + 0x280) = 1u << 30;
    기계저장기(IRQ_mai_rabawa + 0x41c) = 0x80808080;
    기계저장기(IRQ_mai_rabawa + 0x100) = 1u << 30;
    기계저장기(IRQ_CPU_Farfajiya + 4) = 0xff;
    기계저장기(IRQ_CPU_Farfajiya + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Tsaro = (기계저장기(IRQ_mai_rabawa + 4) & (1u << 10)) != 0;
    기계저장기(IRQ_mai_rabawa) = Tsaro ? 1 : 3;
    기계저장기(IRQ_CPU_Farfajiya) = Tsaro ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t rubuta_ɓangare, na_ura_mai_kwakwalwa_rubuta; uint32_t 판번호;
    uint64_t Mashigar_bayanai_maki, Shiri_Kai_Sassautawa, Sashi_Kai_Sassautawa; uint32_t saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango;
    uint16_t 실행머리크기, Shiri_Kai_Mashigar_bayanai_girma, 프로그램머리개수, Sashi_Kai_Mashigar_bayanai_girma, 구역머리개수, Sashi_Suna_tebur_Indes;
} 실행파일머리;
typedef struct { uint32_t rubuta_ɓangare, saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango; uint64_t Sassautawa_Daraja, imel, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(Mai_anfani_da_kwamfuta_allo) == 272, "exception assembly layout");
static int 포함된범위(uint64_t Sassautawa_Daraja, uint64_t Girma, uint64_t Ƙarshe_Sassautawa) {
    return Sassautawa_Daraja <= Ƙarshe_Sassautawa && Girma <= Ƙarshe_Sassautawa - Sassautawa_Daraja;
}
static int 부가정보검사(const unsigned char *자료위치, size_t Girma) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, Girma)) {
        uint32_t 낱말들[3]; memcpy(낱말들, 자료위치 + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, Girma) || !포함된범위(현재위치 + 이름영역크기, 설명크기, Girma)) return 0;
        const unsigned char Suna[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Suna) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Suna); 순번++) if (자료위치[현재위치 + 순번] != Suna[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, 자료위치 + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *Tarin_bayani, size_t Girma, int 리눅스방식) {
    if (Girma < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, Tarin_bayani, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.rubuta_ɓangare != 2 || 실행머리.na_ura_mai_kwakwalwa_rubuta != 183 || 실행머리.판번호 != 1 || 실행머리.saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.Shiri_Kai_Mashigar_bayanai_girma != sizeof(실행파일구획) || !실행머리.프로그램머리개수 || 실행머리.프로그램머리개수 > 16 ||
        실행머리.Shiri_Kai_Sassautawa < sizeof(실행머리) || !포함된범위(실행머리.Shiri_Kai_Sassautawa, (uint64_t)실행머리.프로그램머리개수 * sizeof(실행파일구획), Girma)) return 사용자실행파일오류;
    uint8_t 사용량[(Mai_anfani_da_kwamfuta_Hoto_Ƙarshe - 사용자바탕) / Girman_shafi] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.프로그램머리개수; 순번++) {
        실행파일구획 자료위치; memcpy(&자료위치, Tarin_bayani + 실행머리.Shiri_Kai_Sassautawa + 순번 * sizeof(자료위치), sizeof(자료위치));
        if (자료위치.rubuta_ɓangare == 4) {
            if (!포함된범위(자료위치.Sassautawa_Daraja, 자료위치.파일영역크기, Girma)) return 사용자실행파일오류;
            if (부가정보검사(Tarin_bayani + 자료위치.Sassautawa_Daraja, 자료위치.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (자료위치.rubuta_ɓangare == 0 || 자료위치.rubuta_ɓangare == 6 || (자료위치.rubuta_ɓangare == 0x6474e551 && !(자료위치.saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango & 1))) continue;
        if (자료위치.rubuta_ɓangare != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!자료위치.기억영역크기) continue;
        if (자료위치.saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango & ~7u || !(자료위치.saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango & 4) || (자료위치.saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango & 3) == 3 || 자료위치.파일영역크기 > 자료위치.기억영역크기 ||
            (자료위치.파일영역크기 && !포함된범위(자료위치.Sassautawa_Daraja, 자료위치.파일영역크기, Girma)) || 자료위치.imel < 사용자바탕 ||
            !포함된범위(자료위치.imel, 자료위치.기억영역크기, Mai_anfani_da_kwamfuta_Hoto_Ƙarshe) ||
            (!리눅스방식 && ((자료위치.imel & (Girman_shafi - 1)) || (자료위치.Sassautawa_Daraja & (Girman_shafi - 1)) || 자료위치.맞춤 != Girman_shafi)) ||
            (리눅스방식 && (((자료위치.imel ^ 자료위치.Sassautawa_Daraja) & (Girman_shafi - 1)) || !자료위치.맞춤 ||
                (자료위치.맞춤 & (자료위치.맞춤 - 1)) || 자료위치.맞춤 > 0x200000 || ((자료위치.imel ^ 자료위치.Sassautawa_Daraja) & (자료위치.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (자료위치.imel - 사용자바탕) / Girman_shafi;
        unsigned 항목수 = ((자료위치.imel & (Girman_shafi - 1)) + 자료위치.기억영역크기 + Girman_shafi - 1) / Girman_shafi;
        for (unsigned shafi_Daraja = 첫항목; shafi_Daraja < 첫항목 + 항목수; shafi_Daraja++) {
            if (사용량[shafi_Daraja]) return 사용자실행파일오류;
            사용량[shafi_Daraja] = 1;
        }
        if ((자료위치.saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango & 1) && 실행머리.Mashigar_bayanai_maki >= 자료위치.imel && 실행머리.Mashigar_bayanai_maki < 자료위치.imel + 자료위치.파일영역크기 && !(실행머리.Mashigar_bayanai_maki & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *Tarin_bayani, size_t Girma) { return 실행파일검사(Tarin_bayani, Girma, 0); }
static void Shinfiɗar_shafi(uintptr_t imel, uint64_t saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango, unsigned umurni) {
    unsigned 색인 = (imel - 사용자바탕) / Girman_shafi;
    shafi_Jeri[색인] = imel | saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango;
    Izini_Jeri[색인] = umurni;
}
static int 사용자범위(uintptr_t imel, size_t 항목수, int 쓰는중) {
    if (imel < 사용자바탕 || !포함된범위(imel, 항목수, Mai_anfani_da_kwamfuta_Ƙarshe)) return 0;
    if (!항목수) return 1;
    unsigned 첫항목 = (imel - 사용자바탕) / Girman_shafi, 마지막 = (imel + 항목수 - 1 - 사용자바탕) / Girman_shafi;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Izini_Jeri[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int Kwafi_Hanyar_shiga(uintptr_t imel, char *Hanyar_shiga) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(imel, 1, 0)) return -14;
        Hanyar_shiga[순번] = *(const char *)imel++;
        if (!Hanyar_shiga[순번]) return 0;
    }
    return -36;
}
static intptr_t 커널결과(intptr_t 결과) { return 결과 < 0 ? -오류번호 : 결과; }
static int 대응파일기술자(uint64_t Fayil_Mariki) { return Fayil_Mariki >= 3 && Fayil_Mariki < 19 ? Fayil_Jeri[Fayil_Mariki - 3] : -1; }
static int 통신끝점소유(uint64_t Fayil_Mariki) { return Fayil_Mariki >= 32 && Fayil_Mariki < 56 && 통신끝점들[Fayil_Mariki - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t Tsawo_Daraja, struct pk_sockaddr_in *imel) {
    if (Tsawo_Daraja != sizeof(*imel)) return -22;
    if (!사용자범위(가리킴값, Tsawo_Daraja, 0)) return -14;
    memcpy(imel, (const void *)가리킴값, sizeof(*imel));
    return imel->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t Tsawo_manuni, pk_socklen_t *수용량) {
    if (!사용자범위(Tsawo_manuni, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)Tsawo_manuni, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t Tsawo_manuni, pk_socklen_t 수용량, int imel, int lambar_kafa) {
    struct pk_sockaddr_in Daraja; memset(&Daraja, 0, sizeof(Daraja));
    Daraja.sin_family = AF_INET; Daraja.sin_port = pk_htons(lambar_kafa); Daraja.sin_addr.s_addr = pk_htonl(imel);
    if (수용량) memcpy((void *)가리킴값, &Daraja, 수용량);
    pk_socklen_t Tsawo_Daraja = sizeof(Daraja); memcpy((void *)Tsawo_manuni, &Tsawo_Daraja, sizeof(Tsawo_Daraja));
}
extern uintptr_t 보드통로(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(Mai_anfani_da_kwamfuta_allo *Fayil_Mashigar_bayanai) {
    uintptr_t 첫째값 = Fayil_Mashigar_bayanai->저장기값[0], 둘째값 = Fayil_Mashigar_bayanai->저장기값[1], Lambar_sirrin_harafi = Fayil_Mashigar_bayanai->저장기값[2];
    char Hanyar_shiga[65];
    int Fayil_Mariki, 결과;
    switch (Fayil_Mashigar_bayanai->저장기값[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: manuni 전체를 검사한 Baya_Daraja 출력/Fayil Canza_Daraja
        if (Lambar_sirrin_harafi > 65536) return -22;
        if (!사용자범위(둘째값, Lambar_sirrin_harafi, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=agogo_Daraja();
            for (size_t 순번 = 0; 순번 < Lambar_sirrin_harafi; 순번++) 보드통로(첫째값, ((const unsigned char *)둘째값)[순번]);
            /* 큰 tty를 그린 Kwara_Daraja 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(Shigar_da_umarni_na_kwamfuta){
                마감시각+=agogo_Daraja()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return Lambar_sirrin_harafi;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t 개수=Lambar_sirrin_harafi>512?512:Lambar_sirrin_harafi;for(size_t 순번=0;순번<개수;순번++)자바전문넣기(순번,((const unsigned char *)둘째값)[순번]);return 자바흐름쓰기(첫째값,개수);
        }
        Fayil_Mariki = 대응파일기술자(첫째값); if (Fayil_Mariki < 0) return -9;
        return 커널결과(pk_write(Fayil_Mariki, (const void *)둘째값, Lambar_sirrin_harafi));
    case 2:
        if (Lambar_sirrin_harafi > 65536) return -22;
        if (!사용자범위(둘째값, Lambar_sirrin_harafi, 1)) return -14;
        if (첫째값 == 0) {
            size_t 개수 = 0;
            while (개수 < Lambar_sirrin_harafi) {
                int Harafi_Daraja = (int32_t)보드글자읽기(); if (Harafi_Daraja == -2) return 개수; if (Harafi_Daraja < 0) break;
                ((unsigned char *)둘째값)[개수++] = Harafi_Daraja;
            }
            return 개수 ? (intptr_t)개수 : (Lambar_sirrin_harafi ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            결과=자바흐름읽기(첫째값,Lambar_sirrin_harafi>512?512:Lambar_sirrin_harafi);if(결과>0)for(int 순번=0;순번<결과;순번++)((unsigned char *)둘째값)[순번]=자바전문얻기(순번);return 결과;
        }
        Fayil_Mariki = 대응파일기술자(첫째값); if (Fayil_Mariki < 0) return -9;
        return 커널결과(pk_read(Fayil_Mariki, (void *)둘째값, Lambar_sirrin_harafi));
    case 3:
        결과 = Kwafi_Hanyar_shiga(첫째값, Hanyar_shiga); if (결과) return 결과;
        if (둘째값 > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (Fayil_Jeri[순번] < 0) {
            Fayil_Mariki = pk_open(Hanyar_shiga, (int)둘째값, 0600);
            if (Fayil_Mariki < 0) return -오류번호;
            Fayil_Jeri[순번] = Fayil_Mariki; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { 결과 = 통신끝점닫기(첫째값); if (!결과) 통신끝점들[첫째값 - 32] = 0; return 결과; }
        Fayil_Mariki = 대응파일기술자(첫째값); if (Fayil_Mariki < 0) return -9;
        결과 = pk_close(Fayil_Mariki); if (!결과) Fayil_Jeri[첫째값 - 3] = -1;
        return 커널결과(결과);
    case 5:
        Fayil_Mariki = 대응파일기술자(첫째값); if (Fayil_Mariki < 0) return -9;
        if (Lambar_sirrin_harafi > 2) return -22;
        return 커널결과(pk_lseek(Fayil_Mariki, (int64_t)둘째값, Lambar_sirrin_harafi));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 Mai_anfani_da_kwamfuta RW/NX 힙, 새로 노출되는 페이지는 0으로 Farko
        if (!첫째값) return 동적기억끝;
        if (첫째값 < Mai_anfani_da_kwamfuta_Hoto_Ƙarshe || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + Girman_shafi - 1) & ~(Girman_shafi - 1);
        uintptr_t 새쪽들 = (첫째값 + Girman_shafi - 1) & ~(Girman_shafi - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t 자료위치 = 이전쪽들; 자료위치 < 새쪽들; 자료위치 += Girman_shafi) Shinfiɗar_shafi(자료위치, Kwara_shafi, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t 자료위치 = 이전쪽들; 자료위치 < 새쪽들; 자료위치 += Girman_shafi) Shinfiɗar_shafi(자료위치, Mai_anfani_da_kwamfuta_Rubutuwa_karantuwa, 3);
        } else {
            for (uintptr_t 자료위치 = 새쪽들; 자료위치 < 이전쪽들; 자료위치 += Girman_shafi) {
                shafi_Jeri[(자료위치 - 사용자바탕) / Girman_shafi] = 0; Izini_Jeri[(자료위치 - 사용자바탕) / Girman_shafi] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        Fayil_Mariki = 대응파일기술자(첫째값); return Fayil_Mariki < 0 ? -9 : 커널결과(pk_size(Fayil_Mariki));
    case 10:
        Fayil_Mariki = 대응파일기술자(첫째값); return Fayil_Mariki < 0 ? -9 : 커널결과(pk_ftruncate(Fayil_Mariki, (int64_t)둘째값));
    case 11:
        결과 = Kwafi_Hanyar_shiga(첫째값, Hanyar_shiga); return 결과 ? 결과 : 커널결과(pk_unlink(Hanyar_shiga));
    case 12:
        Fayil_Mariki = 대응파일기술자(첫째값); return Fayil_Mariki < 0 ? -9 : 커널결과(pk_fsync(Fayil_Mariki));
    case 13: { // 그래픽 기초 API: Mai_anfani_da_kwamfuta 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = Fayil_Mashigar_bayanai->저장기값[3], 높이값 = Fayil_Mashigar_bayanai->저장기값[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || 둘째값 > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - 둘째값) return -22;
        for (uintptr_t Maɓallin_Y_Mai_tsarawa = 둘째값; Maɓallin_Y_Mai_tsarawa < 둘째값 + 높이값; Maɓallin_Y_Mai_tsarawa++) for (uintptr_t gamayyar_x = 첫째값; gamayyar_x < 첫째값 + 너비값; gamayyar_x++) 보드화소(gamayyar_x, Maɓallin_Y_Mai_tsarawa, Lambar_sirrin_harafi);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=개수; args(index,buffer,capacity)=UTF-8 Tsawo_Daraja
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (Lambar_sirrin_harafi <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(둘째값, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)둘째값, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;Shigar_da_umarni_na_kwamfuta=1;return 보드터미널(13);}
        if(첫째값==2){Shigar_da_umarni_na_kwamfuta=0;return 0;}
        if(첫째값==3)return 보드터미널(13);
        if(첫째값!=1||!Shigar_da_umarni_na_kwamfuta)return -22;
        결과=(int32_t)보드글자읽기();
        if(결과==-4096)return 결과;
        시간제한시작();return 결과<0?-11:결과;
    case 17: { // 유한한 협력 jira_Daraja: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t Ƙarshe_lokaci = agogo_Daraja() + 진동수 * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (agogo_Daraja() < Ƙarshe_lokaci);
        시간제한시작(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (둘째값 > 2) return -22;
        결과 = Kwafi_Hanyar_shiga(첫째값, Hanyar_shiga); if (결과) return 결과;
        unsigned Tsawo_Daraja = 0; while (Hanyar_shiga[Tsawo_Daraja]) Tsawo_Daraja++;
        결과 = 자바경로시작(Tsawo_Daraja); if (결과 < 0) return 결과;
        for (unsigned 순번 = 0; 순번 < Tsawo_Daraja; 순번++) 자바경로바이트(순번, (unsigned char)Hanyar_shiga[순번]);
        return 둘째값 == 0 ? 자바항목종류() : 둘째값 == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int Harafi_Daraja=(int32_t)보드글자읽기();if(Harafi_Daraja==-4096)return Harafi_Daraja;if(Harafi_Daraja>=0)화면누름(mamallaki_abu,Harafi_Daraja);시간제한시작();}
        if(첫째값==3&&Lambar_sirrin_harafi){if(!자바셸대화형())return -95;Shigar_da_umarni_na_kwamfuta=1;보드터미널(300);}
        return 화면호출(mamallaki_abu,첫째값,둘째값,Lambar_sirrin_harafi,Fayil_Mashigar_bayanai->저장기값[3],Fayil_Mashigar_bayanai->저장기값[4],Fayil_Mashigar_bayanai->저장기값[5]);
    case 21:
        if(Lambar_sirrin_harafi>127)return -22;if(!사용자범위(둘째값,Lambar_sirrin_harafi*sizeof(uint32_t),0))return -14;
        return 화면글(mamallaki_abu,첫째값,(const uint32_t *)둘째값,Lambar_sirrin_harafi);
    case 22: // 화면 Girma Matantanci_Daraja: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(둘째값==SOCK_STREAM&&(Lambar_sirrin_harafi==0||Lambar_sirrin_harafi==6))결과=자바흐름만들기();
        else if(둘째값==SOCK_DGRAM&&(Lambar_sirrin_harafi==0||Lambar_sirrin_harafi==IPPROTO_UDP))결과=자바전문만들기(첫째값,둘째값,Lambar_sirrin_harafi);
        else return -93;
        if (결과 >= 32 && 결과 < 56) 통신끝점들[결과 - 32] = 1;
        return 결과;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in imel;
        결과 = 주소입력(둘째값, Lambar_sirrin_harafi, &imel); if (결과) return 결과;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(imel.sin_addr.s_addr),pk_htons(imel.sin_port)):자바전문묶기(첫째값, pk_htonl(imel.sin_addr.s_addr), pk_htons(imel.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Fayil_Mashigar_bayanai->저장기값[3]) return -95;
        if (Lambar_sirrin_harafi > 512) return -90;
        if (Lambar_sirrin_harafi && !사용자범위(둘째값, Lambar_sirrin_harafi, 0)) return -14;
        struct pk_sockaddr_in imel;
        결과 = 주소입력(Fayil_Mashigar_bayanai->저장기값[4], Fayil_Mashigar_bayanai->저장기값[5], &imel); if (결과) return 결과;
        for (unsigned 순번 = 0; 순번 < Lambar_sirrin_harafi; 순번++) 자바전문넣기(순번, ((const unsigned char *)둘째값)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(imel.sin_addr.s_addr), pk_htons(imel.sin_port), Lambar_sirrin_harafi);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (Fayil_Mashigar_bayanai->저장기값[3]) return -95;
        if (Lambar_sirrin_harafi > 512) return -90;
        if (Lambar_sirrin_harafi && !사용자범위(둘째값, Lambar_sirrin_harafi, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (Fayil_Mashigar_bayanai->저장기값[4]) { 결과 = 주소출력검사(Fayil_Mashigar_bayanai->저장기값[4], Fayil_Mashigar_bayanai->저장기값[5], &수용량); if (결과) return 결과; }
        결과 = 자바전문받기(첫째값, Lambar_sirrin_harafi); if (결과 < 0) return 결과;
        for (int 순번 = 0; 순번 < 결과; 순번++) ((unsigned char *)둘째값)[순번] = 자바전문얻기(순번);
        if (Fayil_Mashigar_bayanai->저장기값[4]) 주소출력(Fayil_Mashigar_bayanai->저장기값[4], Fayil_Mashigar_bayanai->저장기값[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return 결과;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        결과 = 주소출력검사(둘째값, Lambar_sirrin_harafi, &수용량); if (결과) return 결과;
        주소출력(둘째값,Lambar_sirrin_harafi,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in imel;
        결과=주소입력(둘째값,Lambar_sirrin_harafi,&imel);if(결과)return 결과;
        return 자바흐름연결(첫째값,pk_htonl(imel.sin_addr.s_addr),pk_htons(imel.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,둘째값):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(둘째값||Lambar_sirrin_harafi)return -95;결과=자바흐름연결받기(첫째값);if(결과>=40&&결과<56)통신끝점들[결과-32]=1;return 결과;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(Mai_anfani_da_kwamfuta_allo *Fayil_Mashigar_bayanai) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(Fayil_Mashigar_bayanai) : 자체체계호출(Fayil_Mashigar_bayanai);
}
static void 커널돌아가기(Mai_anfani_da_kwamfuta_allo *Fayil_Mashigar_bayanai, int 결과) {
    시간제한멈춤();
    Fayil_Mashigar_bayanai->저장기값[0] = (uint64_t)(int64_t)결과;
    Fayil_Mashigar_bayanai->명령위치 = (uintptr_t)사용자복귀;
    Fayil_Mashigar_bayanai->Matsayi_lambar_sirri = 0x3c5; // EL1h, DAIF masked
}
int Mai_anfani_da_kwamfuta_banbanchi(Mai_anfani_da_kwamfuta_allo *Fayil_Mashigar_bayanai, unsigned 가로채기) {
    if (!Aiki_d9ba6551 || (Fayil_Mashigar_bayanai->Matsayi_lambar_sirri & 15) != 0) return 0;
    if (가로채기) {
        uint32_t 승인값 = 기계저장기(IRQ_CPU_Farfajiya + 0xc), mai_ganewa_Daraja = 승인값 & 1023;
        if (mai_ganewa_Daraja == 30) { 커널돌아가기(Fayil_Mashigar_bayanai, 사용자시간초과); 기계저장기(IRQ_CPU_Farfajiya + 0x10) = 승인값; return 1; }
        if (mai_ganewa_Daraja < 1020) 기계저장기(IRQ_CPU_Farfajiya + 0x10) = 승인값;
        return 1;
    }
    uint64_t banbanchi_Matsayi; __asm__ volatile("mrs %0, esr_el1" : "=r"(banbanchi_Matsayi));
    if (agogo_Daraja() >= 마감시각) { 커널돌아가기(Fayil_Mashigar_bayanai, 사용자시간초과); return 1; }
    unsigned banbanchi_ɓangare = banbanchi_Matsayi >> 26;
    if (banbanchi_ɓangare == 0x15 && (banbanchi_Matsayi & 0xffff) == 0) {
        if (리눅스규약 ? Fayil_Mashigar_bayanai->저장기값[8] == 93 || Fayil_Mashigar_bayanai->저장기값[8] == 94 : Fayil_Mashigar_bayanai->저장기값[8] == 6) 커널돌아가기(Fayil_Mashigar_bayanai, (int)(Fayil_Mashigar_bayanai->저장기값[0] & 255));
        else {
            intptr_t 결과=체계호출(Fayil_Mashigar_bayanai);
            if(결과==-4096&&Shigar_da_umarni_na_kwamfuta){
                저장값[mamallaki_abu].실행틀=*Fayil_Mashigar_bayanai;저장값[mamallaki_abu].실행틀.명령위치-=4;
                사용자실수보관(저장값[mamallaki_abu].실수저장상태);커널돌아가기(Fayil_Mashigar_bayanai,사용자중단됨);
            }else Fayil_Mashigar_bayanai->저장기값[0]=(uint64_t)결과;
        }
    } else 커널돌아가기(Fayil_Mashigar_bayanai, banbanchi_ɓangare == 0x24 ? Mai_anfani_da_kwamfuta_Tarin_bayani_Kuskure : banbanchi_ɓangare == 0x20 ? 사용자실행오류 : Mai_anfani_da_kwamfuta_mara_ƙarfi_Sharadi);
    return 1;
}

// 생성된 const ELF gungu_Daraja: 실행은 반드시 Shiri_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *Tarin_bayani; size_t Girma; unsigned 전달값; } Shiri;
#include "programs.h"
static void *ɗaukar_hoto(unsigned 자리){return (void *)(0x04000000ul+자리*(Mai_anfani_da_kwamfuta_Ƙarshe-사용자바탕));}
static int Gama_Shiri(int 결과){
    사용자누적시각[mamallaki_abu]+=(uint32_t)보드밀리초()-사용자실행시각[mamallaki_abu];
    시간제한멈춤();Aiki_d9ba6551=0;
    if(결과==사용자중단됨){
        저장된작업 *Zare_Tarin_bayani=&저장값[mamallaki_abu];Zare_Tarin_bayani->멈춤상태=1;Zare_Tarin_bayani->Shigar_da_umarni_na_kwamfuta=Shigar_da_umarni_na_kwamfuta;Zare_Tarin_bayani->리눅스규약=리눅스규약;Zare_Tarin_bayani->동적기억공간=동적기억끝;Zare_Tarin_bayani->인수개수=전달인수개수;
        memcpy(Zare_Tarin_bayani->Izini_Jeri,Izini_Jeri,sizeof(Izini_Jeri));memcpy(Zare_Tarin_bayani->Fayil_Jeri,Fayil_Jeri,sizeof(Fayil_Jeri));memcpy(Zare_Tarin_bayani->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(Zare_Tarin_bayani->Tubalin_aiki_TSARI,전달인수,sizeof(전달인수));memcpy(Zare_Tarin_bayani->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<사용자쪽수;순번++)if(Izini_Jeri[순번])memcpy((unsigned char *)ɗaukar_hoto(mamallaki_abu)+순번*Girman_shafi,(void *)(사용자바탕+순번*Girman_shafi),Girman_shafi);
    }else{
        저장값[mamallaki_abu].멈춤상태=0;화면초기화(mamallaki_abu);
        for(unsigned 순번=0;순번<16;순번++)if(Fayil_Jeri[순번]>=0)pk_close(Fayil_Jeri[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<사용자쪽수;순번++){shafi_Jeri[순번]=0;Izini_Jeri[순번]=0;}변환표맞추기();return 결과;
}
uintptr_t 보드사용자제어(uintptr_t Aiki){
    unsigned 자리=Aiki&15;if(자리>=4||Aiki_d9ba6551)return (uint32_t)-22;
    저장된작업 *Zare_Tarin_bayani=&저장값[자리];
    if(Aiki>=32){if(Zare_Tarin_bayani->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(Zare_Tarin_bayani->Fayil_Jeri[순번]>=0)pk_close(Zare_Tarin_bayani->Fayil_Jeri[순번]);for(unsigned 순번=0;순번<24;순번++)if(Zare_Tarin_bayani->통신끝점들[순번])통신끝점닫기(순번+32);}Zare_Tarin_bayani->멈춤상태=0;화면초기화(자리);return 0;}
    if(Aiki>=16)return Zare_Tarin_bayani->멈춤상태;
    if(!Zare_Tarin_bayani->멈춤상태)return (uint32_t)-22;
    mamallaki_abu=자리;Shigar_da_umarni_na_kwamfuta=Zare_Tarin_bayani->Shigar_da_umarni_na_kwamfuta;리눅스규약=Zare_Tarin_bayani->리눅스규약;동적기억끝=Zare_Tarin_bayani->동적기억공간;전달인수개수=Zare_Tarin_bayani->인수개수;
    memcpy(Fayil_Jeri,Zare_Tarin_bayani->Fayil_Jeri,sizeof(Fayil_Jeri));memcpy(통신끝점들,Zare_Tarin_bayani->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,Zare_Tarin_bayani->Tubalin_aiki_TSARI,sizeof(전달인수));memcpy(전달인수길이,Zare_Tarin_bayani->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<사용자쪽수;순번++)shafi_Jeri[순번]=(사용자바탕+순번*Girman_shafi)|Kwara_shafi;변환표맞추기();
    memset((void *)사용자바탕,0,Mai_anfani_da_kwamfuta_Ƙarshe-사용자바탕);
    for(unsigned 순번=0;순번<사용자쪽수;순번++)if(Zare_Tarin_bayani->Izini_Jeri[순번])memcpy((void *)(사용자바탕+순번*Girman_shafi),(unsigned char *)ɗaukar_hoto(자리)+순번*Girman_shafi,Girman_shafi);
    memcpy(Izini_Jeri,Zare_Tarin_bayani->Izini_Jeri,sizeof(Izini_Jeri));
    for(unsigned 순번=0;순번<사용자쪽수;순번++){unsigned 자료위치=Izini_Jeri[순번];shafi_Jeri[순번]=자료위치?(사용자바탕+순번*Girman_shafi)|(자료위치==3?Mai_anfani_da_kwamfuta_Rubutuwa_karantuwa:자료위치==5?사용자읽고실행:Mai_anfani_da_kwamfuta_karanta_kawai):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aiki_d9ba6551=1;Zare_Tarin_bayani->멈춤상태=0;시간제한시작();
    사용자실행시각[mamallaki_abu]=보드밀리초();
    return (uint32_t)Gama_Shiri(Mai_anfani_da_kwamfuta_CV(&Zare_Tarin_bayani->실행틀,Zare_Tarin_bayani->실수저장상태));
}
static int Gudanar_da_Shiri(const unsigned char *Tarin_bayani, size_t Girma, unsigned 전달값, int 리눅스방식, const char *Suna) {
    if (Aiki_d9ba6551) return -16;
    mamallaki_abu=보드터미널(11);if(mamallaki_abu<0||mamallaki_abu>3||저장값[mamallaki_abu].멈춤상태)return -16;Shigar_da_umarni_na_kwamfuta=0;
    int 유효함 = 실행파일검사(Tarin_bayani, Girma, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned Suna_Indes=0;
    while (*Suna && Suna_Indes<31) Mai_anfani_da_kwamfuta_Umarni_Suna[mamallaki_abu][Suna_Indes++]=(unsigned char)*Suna++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (Suna_Indes) Mai_anfani_da_kwamfuta_Umarni_Suna[mamallaki_abu][Suna_Indes++]=' ';
        for (unsigned 자리=0; 자리<전달인수길이[0]; 자리++) Mai_anfani_da_kwamfuta_Umarni_Suna[mamallaki_abu][Suna_Indes++]=전달인수[0][자리];
    }
    Mai_anfani_da_kwamfuta_Umarni_Suna[mamallaki_abu][Suna_Indes]=0; 사용자번호[mamallaki_abu]=다음사용자번호++;
    if (다음사용자번호>0x7fffffffu) 다음사용자번호=10;
    Mai_anfani_da_kwamfuta_Fara_lokaci[mamallaki_abu]=보드밀리초(); 사용자누적시각[mamallaki_abu]=0;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) shafi_Jeri[순번] = (사용자바탕 + 순번 * Girman_shafi) | Kwara_shafi;
    변환표맞추기();
    memset((void *)사용자바탕, 0, Mai_anfani_da_kwamfuta_Ƙarshe - 사용자바탕);
    memset(Izini_Jeri, 0, sizeof(Izini_Jeri));
    실행파일머리 실행머리; memcpy(&실행머리, Tarin_bayani, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.프로그램머리개수; 순번++) {
        실행파일구획 자료위치; memcpy(&자료위치, Tarin_bayani + 실행머리.Shiri_Kai_Sassautawa + 순번 * sizeof(자료위치), sizeof(자료위치));
        if (자료위치.rubuta_ɓangare != 1 || !자료위치.기억영역크기) continue;
        if (자료위치.파일영역크기) memcpy((void *)(uintptr_t)자료위치.imel, Tarin_bayani + 자료위치.Sassautawa_Daraja, 자료위치.파일영역크기);
        for (uintptr_t 현재위치 = 자료위치.imel & ~(Girman_shafi - 1); 현재위치 < 자료위치.imel + 자료위치.기억영역크기; 현재위치 += Girman_shafi) {
            Izini_Jeri[(현재위치 - 사용자바탕) / Girman_shafi] = (자료위치.saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango & 2) ? 3 : ((자료위치.saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = Mai_anfani_da_kwamfuta_tara_imel; 현재위치 < Mai_anfani_da_kwamfuta_Ƙarshe; 현재위치 += Girman_shafi) Izini_Jeri[(현재위치 - 사용자바탕) / Girman_shafi] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.Mashigar_bayanai_maki) : Mai_anfani_da_kwamfuta_Ƙarshe;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) {
        unsigned umurni = Izini_Jeri[순번];
        shafi_Jeri[순번] = umurni ? (사용자바탕 + 순번 * Girman_shafi) | (umurni == 3 ? Mai_anfani_da_kwamfuta_Rubutuwa_karantuwa : umurni == 5 ? 사용자읽고실행 : Mai_anfani_da_kwamfuta_karanta_kawai) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) Fayil_Jeri[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = Mai_anfani_da_kwamfuta_Hoto_Ƙarshe;
    Aiki_d9ba6551 = 1; 시간제한시작();
    사용자실행시각[mamallaki_abu]=보드밀리초();
    int 결과 = Mai_anfani_da_kwamfuta_Shiga(실행머리.Mashigar_bayanai_maki, 초기쌓임공간, 전달값);
    return Gama_Shiri(결과);
}
uintptr_t 보드사용자실행(uintptr_t 색인) {
    if (색인 >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Suna=색인==10?"javac":색인==11?"java":색인==12?"python":색인==13?"vi":색인==14?"jar":색인==15?"cc":색인==16?"jaot":"ELF";
    return (uint32_t)Gudanar_da_Shiri(실행항목들[색인].Tarin_bayani, 실행항목들[색인].Girma, 실행항목들[색인].전달값, 0, Suna);
}
static uintptr_t gudanar_Fayil(int 리눅스방식) {
    static unsigned char Hoto[16384];
    if (Aiki_d9ba6551 || !전달인수개수) return (uint32_t)-22;
    int Fayil_Mariki = pk_open((const char *)전달인수[0], karanta_kawai_Daraja, 0);
    if (Fayil_Mariki < 0) return (uint32_t)-오류번호;
    int Girma = pk_size(Fayil_Mariki);
    if (Girma < 0 || (unsigned)Girma > sizeof(Hoto)) { pk_close(Fayil_Mariki); return (uint32_t)-27; }
    int 받은수 = pk_read(Fayil_Mariki, Hoto, Girma); pk_close(Fayil_Mariki);
    if (받은수 != Girma) return (uint32_t)-5;
    return (uint32_t)Gudanar_da_Shiri(Hoto, Girma, 0, 리눅스방식, "");
}
uintptr_t 보드사용자파일(void) { return gudanar_Fayil(0); }
uintptr_t 보드사용자리눅스파일(void) { return gudanar_Fayil(1); }
uintptr_t 보드사용자검사(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].Tarin_bayani, 잘못된실행항목들[순번].Girma) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
