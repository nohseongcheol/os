#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 diragatsa_Taelo motšhine boalo_Boleng. faele tshedimosetso/정책은 기존 AOT Java 커널에 위임한다.
#include "modirisi.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Neteweke_kokoanyodinepe/Neteweke_kokoanyodinepe.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define motšhine_kwadisa(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_moabi 0xff841000ul
#define IRQ_CPU_segokanyi 0xff842000ul
#define bogolo_jwa_tsebe 4096ul
#define 접근표시 (1ul << 10)
#define 권한실행금지 (1ul << 53)
#define 사용자실행금지 (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define Khenele_tsebe (3ul | 보통기억 | 권한실행금지 | 사용자실행금지)
#define modirisi_buisa_kwala (3ul | 보통기억 | (1ul << 6) | 권한실행금지 | 사용자실행금지)
#define modirisi_puiso_fela (3ul | 보통기억 | (3ul << 6) | 권한실행금지 | 사용자실행금지)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | 권한실행금지)
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
extern int modirisi_CV(modirisi_Foreimi *,void *);
extern void 사용자실수보관(void *);
extern int modirisi_kwadisa(uintptr_t tsenyo_ntlha, uintptr_t kokoanyodinepe_Polokelo, uintptr_t 전달값);
extern void 사용자복귀(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t 뿌리주소[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t tsebe_lenaane[사용자쪽수] __attribute__((aligned(4096)));
static uint8_t ditetla_lenaane[사용자쪽수];
static int e_e_dirisiwang, faele_lenaane[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned faele_mokgwakamogelo){return faele_mokgwakamogelo<40?자바전문닫기(faele_mokgwakamogelo):자바흐름닫기(faele_mokgwakamogelo);}
static uint64_t 진동수, 마감시각;
static uintptr_t 동적기억끝;
// Khenele_Boleng 셸이 준비한 UTF-8 인수. EL0에는 leloko_Boleng 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,Tirisano,리눅스규약,faele_lenaane[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char Thulaganyo_setlhopha[8][256],ditetla_lenaane[사용자쪽수];
    uintptr_t 동적기억공간; modirisi_Foreimi 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int mong_selwana,Tirisano;
static uint32_t nomoro_ya_modirisi[4], 사용자시작시각[4], 사용자누적시각[4], 사용자실행시각[4], 다음사용자번호=10;
static unsigned char modirisi_Taelo_leina[4][288];
uint32_t 사용자상태읽기(unsigned tsenyo_Boleng, unsigned tshupane) {
    unsigned 자리=tshupane&3;
    int kemo_Boleng=(e_e_dirisiwang && mong_selwana==(int)자리) ? 1 : 저장값[자리].멈춤상태 ? 2 : 0;
    if (tsenyo_Boleng==0) return kemo_Boleng;
    if (!kemo_Boleng) return 0;
    if (tsenyo_Boleng==1) return nomoro_ya_modirisi[자리];
    if (tsenyo_Boleng==2) {
        unsigned char *쪽들=kemo_Boleng==1?ditetla_lenaane:저장값[자리].ditetla_lenaane;
        unsigned 쪽수=0; for (unsigned 순번=0; 순번<사용자쪽수; 순번++) if(쪽들[순번]) 쪽수++;
        return 쪽수*4;
    }
    if (tsenyo_Boleng==3) return (uint32_t)보드밀리초()-사용자시작시각[자리];
    if (tsenyo_Boleng==4) return 사용자누적시각[자리]+(kemo_Boleng==1?(uint32_t)보드밀리초()-사용자실행시각[자리]:0);
    if (tsenyo_Boleng==5) return tshupane/4<sizeof(modirisi_Taelo_leina[0])?modirisi_Taelo_leina[자리][tshupane/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t 항목수) {
    if (e_e_dirisiwang || 항목수 > 8) return (uint32_t)-22;
    전달인수개수 = 항목수;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t 색인, uintptr_t 현재위치, uintptr_t baete_tshedimosetso) {
    if (e_e_dirisiwang || 색인 >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[색인] || !baete_tshedimosetso || baete_tshedimosetso > 255)
        return (uint32_t)-22;
    전달인수[색인][현재위치] = baete_tshedimosetso;
    전달인수길이[색인] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t tshupanako_Boleng(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void 시간제한멈춤(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    motšhine_kwadisa(IRQ_moabi + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void 시간제한시작(void) {
    uint64_t 간격 = 진동수 * 2, kgontsha = 1;
    마감시각 = tshupanako_Boleng() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(kgontsha) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned tshedimosetso_thibela = 0; tshedimosetso_thibela < 4; tshedimosetso_thibela++) {
        뿌리주소[tshedimosetso_thibela] = (uintptr_t)가운데[tshedimosetso_thibela] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t aterese = ((uintptr_t)tshedimosetso_thibela << 30) | ((uintptr_t)순번 << 21);
            가운데[tshedimosetso_thibela][순번] = aterese | 1 | 접근표시 | 사용자실행금지;
            if (aterese >= 0xfc000000ul) 가운데[tshedimosetso_thibela][순번] |= 권한실행금지; // Device-nGnRnE
            else 가운데[tshedimosetso_thibela][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned 둘째값 = 0; 둘째값 < 사용자쪽수 / 512; 둘째값++)
        가운데[0][(사용자바탕 >> 21) + 둘째값] = (uintptr_t)(tsebe_lenaane + 둘째값 * 512) | 3;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) tsebe_lenaane[순번] = (사용자바탕 + 순번 * bogolo_jwa_tsebe) | Khenele_tsebe;
    uint64_t memori_nonofo_kwadisa = 0x4400, aterese_Thanolo_taolo = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(memori_nonofo_kwadisa), "r"(aterese_Thanolo_taolo), "r"((uintptr_t)뿌리주소) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    시간제한멈춤();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 tsenyo_ntlha_Boleng 때만 letla_Boleng.
    motšhine_kwadisa(IRQ_moabi) = 0;
    motšhine_kwadisa(IRQ_moabi + 0x180) = 0xffffffff;
    motšhine_kwadisa(IRQ_moabi + 0x80) = 0xffffffff;
    motšhine_kwadisa(IRQ_moabi + 0x280) = 1u << 30;
    motšhine_kwadisa(IRQ_moabi + 0x41c) = 0x80808080;
    motšhine_kwadisa(IRQ_moabi + 0x100) = 1u << 30;
    motšhine_kwadisa(IRQ_CPU_segokanyi + 4) = 0xff;
    motšhine_kwadisa(IRQ_CPU_segokanyi + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int tshireletso = (motšhine_kwadisa(IRQ_moabi + 4) & (1u << 10)) != 0;
    motšhine_kwadisa(IRQ_moabi) = tshireletso ? 1 : 3;
    motšhine_kwadisa(IRQ_CPU_segokanyi) = tshireletso ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t tlanya_setlhopha, motšhine_tlanya; uint32_t 판번호;
    uint64_t tsenyo_ntlha, Tiriso_setlhogo_Baya_ka_Tekatekanyo, karolo_setlhogo_Baya_ka_Tekatekanyo; uint32_t 설정비트;
    uint16_t 실행머리크기, Tiriso_setlhogo_tsenyo_lekanya, 프로그램머리개수, karolo_setlhogo_tsenyo_lekanya, 구역머리개수, karolo_leina_lenaneothalo_tshupane;
} 실행파일머리;
typedef struct { uint32_t tlanya_setlhopha, 설정비트; uint64_t Baya_ka_Tekatekanyo_Boleng, aterese, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(modirisi_Foreimi) == 272, "exception assembly layout");
static int 포함된범위(uint64_t Baya_ka_Tekatekanyo_Boleng, uint64_t lekanya, uint64_t kgaola_Baya_ka_Tekatekanyo) {
    return Baya_ka_Tekatekanyo_Boleng <= kgaola_Baya_ka_Tekatekanyo && lekanya <= kgaola_Baya_ka_Tekatekanyo - Baya_ka_Tekatekanyo_Boleng;
}
static int 부가정보검사(const unsigned char *자료위치, size_t lekanya) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, lekanya)) {
        uint32_t 낱말들[3]; memcpy(낱말들, 자료위치 + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, lekanya) || !포함된범위(현재위치 + 이름영역크기, 설명크기, lekanya)) return 0;
        const unsigned char leina[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(leina) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(leina); 순번++) if (자료위치[현재위치 + 순번] != leina[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, 자료위치 + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *tshedimosetso, size_t lekanya, int 리눅스방식) {
    if (lekanya < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, tshedimosetso, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.tlanya_setlhopha != 2 || 실행머리.motšhine_tlanya != 183 || 실행머리.판번호 != 1 || 실행머리.설정비트 || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.Tiriso_setlhogo_tsenyo_lekanya != sizeof(실행파일구획) || !실행머리.프로그램머리개수 || 실행머리.프로그램머리개수 > 16 ||
        실행머리.Tiriso_setlhogo_Baya_ka_Tekatekanyo < sizeof(실행머리) || !포함된범위(실행머리.Tiriso_setlhogo_Baya_ka_Tekatekanyo, (uint64_t)실행머리.프로그램머리개수 * sizeof(실행파일구획), lekanya)) return 사용자실행파일오류;
    uint8_t 사용량[(modirisi_Setshwantsho_kgaola - 사용자바탕) / bogolo_jwa_tsebe] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.프로그램머리개수; 순번++) {
        실행파일구획 자료위치; memcpy(&자료위치, tshedimosetso + 실행머리.Tiriso_setlhogo_Baya_ka_Tekatekanyo + 순번 * sizeof(자료위치), sizeof(자료위치));
        if (자료위치.tlanya_setlhopha == 4) {
            if (!포함된범위(자료위치.Baya_ka_Tekatekanyo_Boleng, 자료위치.파일영역크기, lekanya)) return 사용자실행파일오류;
            if (부가정보검사(tshedimosetso + 자료위치.Baya_ka_Tekatekanyo_Boleng, 자료위치.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (자료위치.tlanya_setlhopha == 0 || 자료위치.tlanya_setlhopha == 6 || (자료위치.tlanya_setlhopha == 0x6474e551 && !(자료위치.설정비트 & 1))) continue;
        if (자료위치.tlanya_setlhopha != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!자료위치.기억영역크기) continue;
        if (자료위치.설정비트 & ~7u || !(자료위치.설정비트 & 4) || (자료위치.설정비트 & 3) == 3 || 자료위치.파일영역크기 > 자료위치.기억영역크기 ||
            (자료위치.파일영역크기 && !포함된범위(자료위치.Baya_ka_Tekatekanyo_Boleng, 자료위치.파일영역크기, lekanya)) || 자료위치.aterese < 사용자바탕 ||
            !포함된범위(자료위치.aterese, 자료위치.기억영역크기, modirisi_Setshwantsho_kgaola) ||
            (!리눅스방식 && ((자료위치.aterese & (bogolo_jwa_tsebe - 1)) || (자료위치.Baya_ka_Tekatekanyo_Boleng & (bogolo_jwa_tsebe - 1)) || 자료위치.맞춤 != bogolo_jwa_tsebe)) ||
            (리눅스방식 && (((자료위치.aterese ^ 자료위치.Baya_ka_Tekatekanyo_Boleng) & (bogolo_jwa_tsebe - 1)) || !자료위치.맞춤 ||
                (자료위치.맞춤 & (자료위치.맞춤 - 1)) || 자료위치.맞춤 > 0x200000 || ((자료위치.aterese ^ 자료위치.Baya_ka_Tekatekanyo_Boleng) & (자료위치.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (자료위치.aterese - 사용자바탕) / bogolo_jwa_tsebe;
        unsigned 항목수 = ((자료위치.aterese & (bogolo_jwa_tsebe - 1)) + 자료위치.기억영역크기 + bogolo_jwa_tsebe - 1) / bogolo_jwa_tsebe;
        for (unsigned tsebe_Boleng = 첫항목; tsebe_Boleng < 첫항목 + 항목수; tsebe_Boleng++) {
            if (사용량[tsebe_Boleng]) return 사용자실행파일오류;
            사용량[tsebe_Boleng] = 1;
        }
        if ((자료위치.설정비트 & 1) && 실행머리.tsenyo_ntlha >= 자료위치.aterese && 실행머리.tsenyo_ntlha < 자료위치.aterese + 자료위치.파일영역크기 && !(실행머리.tsenyo_ntlha & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *tshedimosetso, size_t lekanya) { return 실행파일검사(tshedimosetso, lekanya, 0); }
static void setshwanotsebe(uintptr_t aterese, uint64_t 설정비트, unsigned ditetla) {
    unsigned 색인 = (aterese - 사용자바탕) / bogolo_jwa_tsebe;
    tsebe_lenaane[색인] = aterese | 설정비트;
    ditetla_lenaane[색인] = ditetla;
}
static int 사용자범위(uintptr_t aterese, size_t 항목수, int 쓰는중) {
    if (aterese < 사용자바탕 || !포함된범위(aterese, 항목수, modirisi_kgaola)) return 0;
    if (!항목수) return 1;
    unsigned 첫항목 = (aterese - 사용자바탕) / bogolo_jwa_tsebe, 마지막 = (aterese + 항목수 - 1 - 사용자바탕) / bogolo_jwa_tsebe;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(ditetla_lenaane[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int leloko_tsela(uintptr_t aterese, char *tsela) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(aterese, 1, 0)) return -14;
        tsela[순번] = *(const char *)aterese++;
        if (!tsela[순번]) return 0;
    }
    return -36;
}
static intptr_t 커널결과(intptr_t 결과) { return 결과 < 0 ? -오류번호 : 결과; }
static int 대응파일기술자(uint64_t faele_mokgwakamogelo) { return faele_mokgwakamogelo >= 3 && faele_mokgwakamogelo < 19 ? faele_lenaane[faele_mokgwakamogelo - 3] : -1; }
static int 통신끝점소유(uint64_t faele_mokgwakamogelo) { return faele_mokgwakamogelo >= 32 && faele_mokgwakamogelo < 56 && 통신끝점들[faele_mokgwakamogelo - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t boleele_Boleng, struct pk_sockaddr_in *aterese) {
    if (boleele_Boleng != sizeof(*aterese)) return -22;
    if (!사용자범위(가리킴값, boleele_Boleng, 0)) return -14;
    memcpy(aterese, (const void *)가리킴값, sizeof(*aterese));
    return aterese->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t boleele_sesupi, pk_socklen_t *수용량) {
    if (!사용자범위(boleele_sesupi, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)boleele_sesupi, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t boleele_sesupi, pk_socklen_t 수용량, int aterese, int 접속번호) {
    struct pk_sockaddr_in Boleng; memset(&Boleng, 0, sizeof(Boleng));
    Boleng.sin_family = AF_INET; Boleng.sin_port = pk_htons(접속번호); Boleng.sin_addr.s_addr = pk_htonl(aterese);
    if (수용량) memcpy((void *)가리킴값, &Boleng, 수용량);
    pk_socklen_t boleele_Boleng = sizeof(Boleng); memcpy((void *)boleele_sesupi, &boleele_Boleng, sizeof(boleele_Boleng));
}
extern uintptr_t 보드통로(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(modirisi_Foreimi *faele_tsenyo) {
    uintptr_t 첫째값 = faele_tsenyo->kwadisa_tshedimosetso[0], 둘째값 = faele_tsenyo->kwadisa_tshedimosetso[1], khoutuletshwao = faele_tsenyo->kwadisa_tshedimosetso[2];
    char tsela[65];
    int faele_mokgwakamogelo, 결과;
    switch (faele_tsenyo->kwadisa_tshedimosetso[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: sesupi 전체를 검사한 Morago_Boleng 출력/faele fetola_Boleng
        if (khoutuletshwao > 65536) return -22;
        if (!사용자범위(둘째값, khoutuletshwao, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=tshupanako_Boleng();
            for (size_t 순번 = 0; 순번 < khoutuletshwao; 순번++) 보드통로(첫째값, ((const unsigned char *)둘째값)[순번]);
            /* 큰 tty를 그린 Khenele_Boleng 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(Tirisano){
                마감시각+=tshupanako_Boleng()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return khoutuletshwao;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t 개수=khoutuletshwao>512?512:khoutuletshwao;for(size_t 순번=0;순번<개수;순번++)자바전문넣기(순번,((const unsigned char *)둘째값)[순번]);return 자바흐름쓰기(첫째값,개수);
        }
        faele_mokgwakamogelo = 대응파일기술자(첫째값); if (faele_mokgwakamogelo < 0) return -9;
        return 커널결과(pk_write(faele_mokgwakamogelo, (const void *)둘째값, khoutuletshwao));
    case 2:
        if (khoutuletshwao > 65536) return -22;
        if (!사용자범위(둘째값, khoutuletshwao, 1)) return -14;
        if (첫째값 == 0) {
            size_t 개수 = 0;
            while (개수 < khoutuletshwao) {
                int Letshwao_Boleng = (int32_t)보드글자읽기(); if (Letshwao_Boleng == -2) return 개수; if (Letshwao_Boleng < 0) break;
                ((unsigned char *)둘째값)[개수++] = Letshwao_Boleng;
            }
            return 개수 ? (intptr_t)개수 : (khoutuletshwao ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            결과=자바흐름읽기(첫째값,khoutuletshwao>512?512:khoutuletshwao);if(결과>0)for(int 순번=0;순번<결과;순번++)((unsigned char *)둘째값)[순번]=자바전문얻기(순번);return 결과;
        }
        faele_mokgwakamogelo = 대응파일기술자(첫째값); if (faele_mokgwakamogelo < 0) return -9;
        return 커널결과(pk_read(faele_mokgwakamogelo, (void *)둘째값, khoutuletshwao));
    case 3:
        결과 = leloko_tsela(첫째값, tsela); if (결과) return 결과;
        if (둘째값 > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (faele_lenaane[순번] < 0) {
            faele_mokgwakamogelo = pk_open(tsela, (int)둘째값, 0600);
            if (faele_mokgwakamogelo < 0) return -오류번호;
            faele_lenaane[순번] = faele_mokgwakamogelo; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { 결과 = 통신끝점닫기(첫째값); if (!결과) 통신끝점들[첫째값 - 32] = 0; return 결과; }
        faele_mokgwakamogelo = 대응파일기술자(첫째값); if (faele_mokgwakamogelo < 0) return -9;
        결과 = pk_close(faele_mokgwakamogelo); if (!결과) faele_lenaane[첫째값 - 3] = -1;
        return 커널결과(결과);
    case 5:
        faele_mokgwakamogelo = 대응파일기술자(첫째값); if (faele_mokgwakamogelo < 0) return -9;
        if (khoutuletshwao > 2) return -22;
        return 커널결과(pk_lseek(faele_mokgwakamogelo, (int64_t)둘째값, khoutuletshwao));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 modirisi RW/NX 힙, 새로 노출되는 페이지는 0으로 go_baakanyetsa_tiriso
        if (!첫째값) return 동적기억끝;
        if (첫째값 < modirisi_Setshwantsho_kgaola || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + bogolo_jwa_tsebe - 1) & ~(bogolo_jwa_tsebe - 1);
        uintptr_t 새쪽들 = (첫째값 + bogolo_jwa_tsebe - 1) & ~(bogolo_jwa_tsebe - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t 자료위치 = 이전쪽들; 자료위치 < 새쪽들; 자료위치 += bogolo_jwa_tsebe) setshwanotsebe(자료위치, Khenele_tsebe, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t 자료위치 = 이전쪽들; 자료위치 < 새쪽들; 자료위치 += bogolo_jwa_tsebe) setshwanotsebe(자료위치, modirisi_buisa_kwala, 3);
        } else {
            for (uintptr_t 자료위치 = 새쪽들; 자료위치 < 이전쪽들; 자료위치 += bogolo_jwa_tsebe) {
                tsebe_lenaane[(자료위치 - 사용자바탕) / bogolo_jwa_tsebe] = 0; ditetla_lenaane[(자료위치 - 사용자바탕) / bogolo_jwa_tsebe] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        faele_mokgwakamogelo = 대응파일기술자(첫째값); return faele_mokgwakamogelo < 0 ? -9 : 커널결과(pk_size(faele_mokgwakamogelo));
    case 10:
        faele_mokgwakamogelo = 대응파일기술자(첫째값); return faele_mokgwakamogelo < 0 ? -9 : 커널결과(pk_ftruncate(faele_mokgwakamogelo, (int64_t)둘째값));
    case 11:
        결과 = leloko_tsela(첫째값, tsela); return 결과 ? 결과 : 커널결과(pk_unlink(tsela));
    case 12:
        faele_mokgwakamogelo = 대응파일기술자(첫째값); return faele_mokgwakamogelo < 0 ? -9 : 커널결과(pk_fsync(faele_mokgwakamogelo));
    case 13: { // 그래픽 기초 API: modirisi 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = faele_tsenyo->kwadisa_tshedimosetso[3], 높이값 = faele_tsenyo->kwadisa_tshedimosetso[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || 둘째값 > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - 둘째값) return -22;
        for (uintptr_t 세로좌표 = 둘째값; 세로좌표 < 둘째값 + 높이값; 세로좌표++) for (uintptr_t kgokagano_ya_x = 첫째값; kgokagano_ya_x < 첫째값 + 너비값; kgokagano_ya_x++) 보드화소(kgokagano_ya_x, 세로좌표, khoutuletshwao);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=개수; args(index,buffer,capacity)=UTF-8 boleele_Boleng
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (khoutuletshwao <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(둘째값, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)둘째값, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;Tirisano=1;return 보드터미널(13);}
        if(첫째값==2){Tirisano=0;return 0;}
        if(첫째값==3)return 보드터미널(13);
        if(첫째값!=1||!Tirisano)return -22;
        결과=(int32_t)보드글자읽기();
        if(결과==-4096)return 결과;
        시간제한시작();return 결과<0?-11:결과;
    case 17: { // 유한한 협력 대기: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t 끝시각 = tshupanako_Boleng() + 진동수 * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (tshupanako_Boleng() < 끝시각);
        시간제한시작(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (둘째값 > 2) return -22;
        결과 = leloko_tsela(첫째값, tsela); if (결과) return 결과;
        unsigned boleele_Boleng = 0; while (tsela[boleele_Boleng]) boleele_Boleng++;
        결과 = 자바경로시작(boleele_Boleng); if (결과 < 0) return 결과;
        for (unsigned 순번 = 0; 순번 < boleele_Boleng; 순번++) 자바경로바이트(순번, (unsigned char)tsela[순번]);
        return 둘째값 == 0 ? 자바항목종류() : 둘째값 == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int Letshwao_Boleng=(int32_t)보드글자읽기();if(Letshwao_Boleng==-4096)return Letshwao_Boleng;if(Letshwao_Boleng>=0)화면누름(mong_selwana,Letshwao_Boleng);시간제한시작();}
        if(첫째값==3&&khoutuletshwao){if(!자바셸대화형())return -95;Tirisano=1;보드터미널(300);}
        return 화면호출(mong_selwana,첫째값,둘째값,khoutuletshwao,faele_tsenyo->kwadisa_tshedimosetso[3],faele_tsenyo->kwadisa_tshedimosetso[4],faele_tsenyo->kwadisa_tshedimosetso[5]);
    case 21:
        if(khoutuletshwao>127)return -22;if(!사용자범위(둘째값,khoutuletshwao*sizeof(uint32_t),0))return -14;
        return 화면글(mong_selwana,첫째값,(const uint32_t *)둘째값,khoutuletshwao);
    case 22: // 화면 lekanya fenenkolola_Boleng: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(둘째값==SOCK_STREAM&&(khoutuletshwao==0||khoutuletshwao==6))결과=자바흐름만들기();
        else if(둘째값==SOCK_DGRAM&&(khoutuletshwao==0||khoutuletshwao==IPPROTO_UDP))결과=자바전문만들기(첫째값,둘째값,khoutuletshwao);
        else return -93;
        if (결과 >= 32 && 결과 < 56) 통신끝점들[결과 - 32] = 1;
        return 결과;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in aterese;
        결과 = 주소입력(둘째값, khoutuletshwao, &aterese); if (결과) return 결과;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(aterese.sin_addr.s_addr),pk_htons(aterese.sin_port)):자바전문묶기(첫째값, pk_htonl(aterese.sin_addr.s_addr), pk_htons(aterese.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (faele_tsenyo->kwadisa_tshedimosetso[3]) return -95;
        if (khoutuletshwao > 512) return -90;
        if (khoutuletshwao && !사용자범위(둘째값, khoutuletshwao, 0)) return -14;
        struct pk_sockaddr_in aterese;
        결과 = 주소입력(faele_tsenyo->kwadisa_tshedimosetso[4], faele_tsenyo->kwadisa_tshedimosetso[5], &aterese); if (결과) return 결과;
        for (unsigned 순번 = 0; 순번 < khoutuletshwao; 순번++) 자바전문넣기(순번, ((const unsigned char *)둘째값)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(aterese.sin_addr.s_addr), pk_htons(aterese.sin_port), khoutuletshwao);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (faele_tsenyo->kwadisa_tshedimosetso[3]) return -95;
        if (khoutuletshwao > 512) return -90;
        if (khoutuletshwao && !사용자범위(둘째값, khoutuletshwao, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (faele_tsenyo->kwadisa_tshedimosetso[4]) { 결과 = 주소출력검사(faele_tsenyo->kwadisa_tshedimosetso[4], faele_tsenyo->kwadisa_tshedimosetso[5], &수용량); if (결과) return 결과; }
        결과 = 자바전문받기(첫째값, khoutuletshwao); if (결과 < 0) return 결과;
        for (int 순번 = 0; 순번 < 결과; 순번++) ((unsigned char *)둘째값)[순번] = 자바전문얻기(순번);
        if (faele_tsenyo->kwadisa_tshedimosetso[4]) 주소출력(faele_tsenyo->kwadisa_tshedimosetso[4], faele_tsenyo->kwadisa_tshedimosetso[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return 결과;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        결과 = 주소출력검사(둘째값, khoutuletshwao, &수용량); if (결과) return 결과;
        주소출력(둘째값,khoutuletshwao,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in aterese;
        결과=주소입력(둘째값,khoutuletshwao,&aterese);if(결과)return 결과;
        return 자바흐름연결(첫째값,pk_htonl(aterese.sin_addr.s_addr),pk_htons(aterese.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,둘째값):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(둘째값||khoutuletshwao)return -95;결과=자바흐름연결받기(첫째값);if(결과>=40&&결과<56)통신끝점들[결과-32]=1;return 결과;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(modirisi_Foreimi *faele_tsenyo) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(faele_tsenyo) : 자체체계호출(faele_tsenyo);
}
static void 커널돌아가기(modirisi_Foreimi *faele_tsenyo, int 결과) {
    시간제한멈춤();
    faele_tsenyo->kwadisa_tshedimosetso[0] = (uint64_t)(int64_t)결과;
    faele_tsenyo->명령위치 = (uintptr_t)사용자복귀;
    faele_tsenyo->상태값 = 0x3c5; // EL1h, DAIF masked
}
int 사용자예외(modirisi_Foreimi *faele_tsenyo, unsigned 가로채기) {
    if (!e_e_dirisiwang || (faele_tsenyo->상태값 & 15) != 0) return 0;
    if (가로채기) {
        uint32_t 승인값 = motšhine_kwadisa(IRQ_CPU_segokanyi + 0xc), setlhaodi_Boleng = 승인값 & 1023;
        if (setlhaodi_Boleng == 30) { 커널돌아가기(faele_tsenyo, 사용자시간초과); motšhine_kwadisa(IRQ_CPU_segokanyi + 0x10) = 승인값; return 1; }
        if (setlhaodi_Boleng < 1020) motšhine_kwadisa(IRQ_CPU_segokanyi + 0x10) = 승인값;
        return 1;
    }
    uint64_t 예외상태; __asm__ volatile("mrs %0, esr_el1" : "=r"(예외상태));
    if (tshupanako_Boleng() >= 마감시각) { 커널돌아가기(faele_tsenyo, 사용자시간초과); return 1; }
    unsigned 예외분류 = 예외상태 >> 26;
    if (예외분류 == 0x15 && (예외상태 & 0xffff) == 0) {
        if (리눅스규약 ? faele_tsenyo->kwadisa_tshedimosetso[8] == 93 || faele_tsenyo->kwadisa_tshedimosetso[8] == 94 : faele_tsenyo->kwadisa_tshedimosetso[8] == 6) 커널돌아가기(faele_tsenyo, (int)(faele_tsenyo->kwadisa_tshedimosetso[0] & 255));
        else {
            intptr_t 결과=체계호출(faele_tsenyo);
            if(결과==-4096&&Tirisano){
                저장값[mong_selwana].실행틀=*faele_tsenyo;저장값[mong_selwana].실행틀.명령위치-=4;
                사용자실수보관(저장값[mong_selwana].실수저장상태);커널돌아가기(faele_tsenyo,사용자중단됨);
            }else faele_tsenyo->kwadisa_tshedimosetso[0]=(uint64_t)결과;
        }
    } else 커널돌아가기(faele_tsenyo, 예외분류 == 0x24 ? modirisi_tshedimosetso_phoso : 예외분류 == 0x20 ? 사용자실행오류 : modirisi_Ga_e_a_siama_taelo);
    return 1;
}

// 생성된 const ELF setlhopha_Boleng: 실행은 반드시 Tiriso_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *tshedimosetso; size_t lekanya; unsigned 전달값; } Tiriso;
#include "programs.h"
static void *tseosenepe(unsigned 자리){return (void *)(0x04000000ul+자리*(modirisi_kgaola-사용자바탕));}
static int Fetsa_Tiriso(int 결과){
    사용자누적시각[mong_selwana]+=(uint32_t)보드밀리초()-사용자실행시각[mong_selwana];
    시간제한멈춤();e_e_dirisiwang=0;
    if(결과==사용자중단됨){
        저장된작업 *dikwalwa_tshedimosetso=&저장값[mong_selwana];dikwalwa_tshedimosetso->멈춤상태=1;dikwalwa_tshedimosetso->Tirisano=Tirisano;dikwalwa_tshedimosetso->리눅스규약=리눅스규약;dikwalwa_tshedimosetso->동적기억공간=동적기억끝;dikwalwa_tshedimosetso->인수개수=전달인수개수;
        memcpy(dikwalwa_tshedimosetso->ditetla_lenaane,ditetla_lenaane,sizeof(ditetla_lenaane));memcpy(dikwalwa_tshedimosetso->faele_lenaane,faele_lenaane,sizeof(faele_lenaane));memcpy(dikwalwa_tshedimosetso->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(dikwalwa_tshedimosetso->Thulaganyo_setlhopha,전달인수,sizeof(전달인수));memcpy(dikwalwa_tshedimosetso->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<사용자쪽수;순번++)if(ditetla_lenaane[순번])memcpy((unsigned char *)tseosenepe(mong_selwana)+순번*bogolo_jwa_tsebe,(void *)(사용자바탕+순번*bogolo_jwa_tsebe),bogolo_jwa_tsebe);
    }else{
        저장값[mong_selwana].멈춤상태=0;화면초기화(mong_selwana);
        for(unsigned 순번=0;순번<16;순번++)if(faele_lenaane[순번]>=0)pk_close(faele_lenaane[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<사용자쪽수;순번++){tsebe_lenaane[순번]=0;ditetla_lenaane[순번]=0;}변환표맞추기();return 결과;
}
uintptr_t 보드사용자제어(uintptr_t tiro){
    unsigned 자리=tiro&15;if(자리>=4||e_e_dirisiwang)return (uint32_t)-22;
    저장된작업 *dikwalwa_tshedimosetso=&저장값[자리];
    if(tiro>=32){if(dikwalwa_tshedimosetso->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(dikwalwa_tshedimosetso->faele_lenaane[순번]>=0)pk_close(dikwalwa_tshedimosetso->faele_lenaane[순번]);for(unsigned 순번=0;순번<24;순번++)if(dikwalwa_tshedimosetso->통신끝점들[순번])통신끝점닫기(순번+32);}dikwalwa_tshedimosetso->멈춤상태=0;화면초기화(자리);return 0;}
    if(tiro>=16)return dikwalwa_tshedimosetso->멈춤상태;
    if(!dikwalwa_tshedimosetso->멈춤상태)return (uint32_t)-22;
    mong_selwana=자리;Tirisano=dikwalwa_tshedimosetso->Tirisano;리눅스규약=dikwalwa_tshedimosetso->리눅스규약;동적기억끝=dikwalwa_tshedimosetso->동적기억공간;전달인수개수=dikwalwa_tshedimosetso->인수개수;
    memcpy(faele_lenaane,dikwalwa_tshedimosetso->faele_lenaane,sizeof(faele_lenaane));memcpy(통신끝점들,dikwalwa_tshedimosetso->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,dikwalwa_tshedimosetso->Thulaganyo_setlhopha,sizeof(전달인수));memcpy(전달인수길이,dikwalwa_tshedimosetso->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<사용자쪽수;순번++)tsebe_lenaane[순번]=(사용자바탕+순번*bogolo_jwa_tsebe)|Khenele_tsebe;변환표맞추기();
    memset((void *)사용자바탕,0,modirisi_kgaola-사용자바탕);
    for(unsigned 순번=0;순번<사용자쪽수;순번++)if(dikwalwa_tshedimosetso->ditetla_lenaane[순번])memcpy((void *)(사용자바탕+순번*bogolo_jwa_tsebe),(unsigned char *)tseosenepe(자리)+순번*bogolo_jwa_tsebe,bogolo_jwa_tsebe);
    memcpy(ditetla_lenaane,dikwalwa_tshedimosetso->ditetla_lenaane,sizeof(ditetla_lenaane));
    for(unsigned 순번=0;순번<사용자쪽수;순번++){unsigned 자료위치=ditetla_lenaane[순번];tsebe_lenaane[순번]=자료위치?(사용자바탕+순번*bogolo_jwa_tsebe)|(자료위치==3?modirisi_buisa_kwala:자료위치==5?사용자읽고실행:modirisi_puiso_fela):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");e_e_dirisiwang=1;dikwalwa_tshedimosetso->멈춤상태=0;시간제한시작();
    사용자실행시각[mong_selwana]=보드밀리초();
    return (uint32_t)Fetsa_Tiriso(modirisi_CV(&dikwalwa_tshedimosetso->실행틀,dikwalwa_tshedimosetso->실수저장상태));
}
static int dirisa_Tiriso(const unsigned char *tshedimosetso, size_t lekanya, unsigned 전달값, int 리눅스방식, const char *leina) {
    if (e_e_dirisiwang) return -16;
    mong_selwana=보드터미널(11);if(mong_selwana<0||mong_selwana>3||저장값[mong_selwana].멈춤상태)return -16;Tirisano=0;
    int 유효함 = 실행파일검사(tshedimosetso, lekanya, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned leina_tshupane=0;
    while (*leina && leina_tshupane<31) modirisi_Taelo_leina[mong_selwana][leina_tshupane++]=(unsigned char)*leina++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (leina_tshupane) modirisi_Taelo_leina[mong_selwana][leina_tshupane++]=' ';
        for (unsigned 자리=0; 자리<전달인수길이[0]; 자리++) modirisi_Taelo_leina[mong_selwana][leina_tshupane++]=전달인수[0][자리];
    }
    modirisi_Taelo_leina[mong_selwana][leina_tshupane]=0; nomoro_ya_modirisi[mong_selwana]=다음사용자번호++;
    if (다음사용자번호>0x7fffffffu) 다음사용자번호=10;
    사용자시작시각[mong_selwana]=보드밀리초(); 사용자누적시각[mong_selwana]=0;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) tsebe_lenaane[순번] = (사용자바탕 + 순번 * bogolo_jwa_tsebe) | Khenele_tsebe;
    변환표맞추기();
    memset((void *)사용자바탕, 0, modirisi_kgaola - 사용자바탕);
    memset(ditetla_lenaane, 0, sizeof(ditetla_lenaane));
    실행파일머리 실행머리; memcpy(&실행머리, tshedimosetso, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.프로그램머리개수; 순번++) {
        실행파일구획 자료위치; memcpy(&자료위치, tshedimosetso + 실행머리.Tiriso_setlhogo_Baya_ka_Tekatekanyo + 순번 * sizeof(자료위치), sizeof(자료위치));
        if (자료위치.tlanya_setlhopha != 1 || !자료위치.기억영역크기) continue;
        if (자료위치.파일영역크기) memcpy((void *)(uintptr_t)자료위치.aterese, tshedimosetso + 자료위치.Baya_ka_Tekatekanyo_Boleng, 자료위치.파일영역크기);
        for (uintptr_t 현재위치 = 자료위치.aterese & ~(bogolo_jwa_tsebe - 1); 현재위치 < 자료위치.aterese + 자료위치.기억영역크기; 현재위치 += bogolo_jwa_tsebe) {
            ditetla_lenaane[(현재위치 - 사용자바탕) / bogolo_jwa_tsebe] = (자료위치.설정비트 & 2) ? 3 : ((자료위치.설정비트 & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = modirisi_kokoanyodinepe_aterese; 현재위치 < modirisi_kgaola; 현재위치 += bogolo_jwa_tsebe) ditetla_lenaane[(현재위치 - 사용자바탕) / bogolo_jwa_tsebe] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.tsenyo_ntlha) : modirisi_kgaola;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) {
        unsigned ditetla = ditetla_lenaane[순번];
        tsebe_lenaane[순번] = ditetla ? (사용자바탕 + 순번 * bogolo_jwa_tsebe) | (ditetla == 3 ? modirisi_buisa_kwala : ditetla == 5 ? 사용자읽고실행 : modirisi_puiso_fela) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) faele_lenaane[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = modirisi_Setshwantsho_kgaola;
    e_e_dirisiwang = 1; 시간제한시작();
    사용자실행시각[mong_selwana]=보드밀리초();
    int 결과 = modirisi_kwadisa(실행머리.tsenyo_ntlha, 초기쌓임공간, 전달값);
    return Fetsa_Tiriso(결과);
}
uintptr_t 보드사용자실행(uintptr_t 색인) {
    if (색인 >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *leina=색인==10?"javac":색인==11?"java":색인==12?"python":색인==13?"vi":색인==14?"jar":색인==15?"cc":색인==16?"jaot":"ELF";
    return (uint32_t)dirisa_Tiriso(실행항목들[색인].tshedimosetso, 실행항목들[색인].lekanya, 실행항목들[색인].전달값, 0, leina);
}
static uintptr_t diragatsa_faele(int 리눅스방식) {
    static unsigned char Setshwantsho[16384];
    if (e_e_dirisiwang || !전달인수개수) return (uint32_t)-22;
    int faele_mokgwakamogelo = pk_open((const char *)전달인수[0], puiso_fela_Boleng, 0);
    if (faele_mokgwakamogelo < 0) return (uint32_t)-오류번호;
    int lekanya = pk_size(faele_mokgwakamogelo);
    if (lekanya < 0 || (unsigned)lekanya > sizeof(Setshwantsho)) { pk_close(faele_mokgwakamogelo); return (uint32_t)-27; }
    int 받은수 = pk_read(faele_mokgwakamogelo, Setshwantsho, lekanya); pk_close(faele_mokgwakamogelo);
    if (받은수 != lekanya) return (uint32_t)-5;
    return (uint32_t)dirisa_Tiriso(Setshwantsho, lekanya, 0, 리눅스방식, "");
}
uintptr_t 보드사용자파일(void) { return diragatsa_faele(0); }
uintptr_t 보드사용자리눅스파일(void) { return diragatsa_faele(1); }
uintptr_t 보드사용자검사(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].tshedimosetso, 잘못된실행항목들[순번].lekanya) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
