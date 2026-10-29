#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 ṣiṣẹ́_àṣẹ maṣíìnì ìpele_iye. Fáìlì détà/정책은 기존 AOT Java 커널에 위임한다.
#include "aṣàmúlò.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Alásopọ̀_kójọ/Alásopọ̀_kójọ.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define maṣíìnì_forúkọsílẹ̀(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_olùpín 0xff841000ul
#define IRQ_CPU_atọ́kùn 0xff842000ul
#define ìwọ̀n_ojú_ìwé 4096ul
#define 접근표시 (1ul << 10)
#define 권한실행금지 (1ul << 53)
#define 사용자실행금지 (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define kánẹ́ẹ̀lì_ojú_ìwé (3ul | 보통기억 | 권한실행금지 | 사용자실행금지)
#define aṣàmúlò_tí_a_lè_kà_tí_a_lè_kọ (3ul | 보통기억 | (1ul << 6) | 권한실행금지 | 사용자실행금지)
#define aṣàmúlò_kàn_kàá (3ul | 보통기억 | (3ul << 6) | 권한실행금지 | 사용자실행금지)
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
extern int aṣàmúlò_CV(aṣàmúlò_férèmù *,void *);
extern void 사용자실수보관(void *);
extern int aṣàmúlò_ṣàtẹ̀wọlé(uintptr_t ìgbéwọlé_kókó, uintptr_t kójọ_Ibi_ìpamọ́, uintptr_t 전달값);
extern void 사용자복귀(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t 뿌리주소[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t ojú_ìwé_Àtòkọ[사용자쪽수] __attribute__((aligned(4096)));
static uint8_t ìyànda_Àtòkọ[사용자쪽수];
static int tó_ń_ṣiṣẹ́, fáìlì_Àtòkọ[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned fáìlì_èkù){return fáìlì_èkù<40?자바전문닫기(fáìlì_èkù):자바흐름닫기(fáìlì_èkù);}
static uint64_t 진동수, 마감시각;
static uintptr_t 동적기억끝;
// kánẹ́ẹ̀lì_iye 셸이 준비한 UTF-8 인수. EL0에는 ṣẹ̀dà_iye 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,ìjọṣepọ̀,리눅스규약,fáìlì_Àtòkọ[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char ágúmẹ́ntì_ÀRÉÈ[8][256],ìyànda_Àtòkọ[사용자쪽수];
    uintptr_t 동적기억공간; aṣàmúlò_férèmù 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int Oníǹkan_nǹkan,ìjọṣepọ̀;
static uint32_t nọ́ńbà_aṣàmúlò[4], 사용자시작시각[4], 사용자누적시각[4], 사용자실행시각[4], 다음사용자번호=10;
static unsigned char aṣàmúlò_àṣẹ_orúkọ[4][288];
uint32_t 사용자상태읽기(unsigned ìgbéwọlé_iye, unsigned wá_atọ̀ka_àkóónú) {
    unsigned 자리=wá_atọ̀ka_àkóónú&3;
    int ipò_iye=(tó_ń_ṣiṣẹ́ && Oníǹkan_nǹkan==(int)자리) ? 1 : 저장값[자리].멈춤상태 ? 2 : 0;
    if (ìgbéwọlé_iye==0) return ipò_iye;
    if (!ipò_iye) return 0;
    if (ìgbéwọlé_iye==1) return nọ́ńbà_aṣàmúlò[자리];
    if (ìgbéwọlé_iye==2) {
        unsigned char *쪽들=ipò_iye==1?ìyànda_Àtòkọ:저장값[자리].ìyànda_Àtòkọ;
        unsigned 쪽수=0; for (unsigned 순번=0; 순번<사용자쪽수; 순번++) if(쪽들[순번]) 쪽수++;
        return 쪽수*4;
    }
    if (ìgbéwọlé_iye==3) return (uint32_t)보드밀리초()-사용자시작시각[자리];
    if (ìgbéwọlé_iye==4) return 사용자누적시각[자리]+(ipò_iye==1?(uint32_t)보드밀리초()-사용자실행시각[자리]:0);
    if (ìgbéwọlé_iye==5) return wá_atọ̀ka_àkóónú/4<sizeof(aṣàmúlò_àṣẹ_orúkọ[0])?aṣàmúlò_àṣẹ_orúkọ[자리][wá_atọ̀ka_àkóónú/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t 항목수) {
    if (tó_ń_ṣiṣẹ́ || 항목수 > 8) return (uint32_t)-22;
    전달인수개수 = 항목수;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t 색인, uintptr_t 현재위치, uintptr_t báìtì_détà) {
    if (tó_ń_ṣiṣẹ́ || 색인 >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[색인] || !báìtì_détà || báìtì_détà > 255)
        return (uint32_t)-22;
    전달인수[색인][현재위치] = báìtì_détà;
    전달인수길이[색인] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t aago_iye(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void 시간제한멈춤(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    maṣíìnì_forúkọsílẹ̀(IRQ_olùpín + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void 시간제한시작(void) {
    uint64_t 간격 = 진동수 * 2, mu_ṣiṣẹ́ = 1;
    마감시각 = aago_iye() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(mu_ṣiṣẹ́) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned détà_sèdíwọ = 0; détà_sèdíwọ < 4; détà_sèdíwọ++) {
        뿌리주소[détà_sèdíwọ] = (uintptr_t)가운데[détà_sèdíwọ] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t àdírẹ́ẹ̀sì = ((uintptr_t)détà_sèdíwọ << 30) | ((uintptr_t)순번 << 21);
            가운데[détà_sèdíwọ][순번] = àdírẹ́ẹ̀sì | 1 | 접근표시 | 사용자실행금지;
            if (àdírẹ́ẹ̀sì >= 0xfc000000ul) 가운데[détà_sèdíwọ][순번] |= 권한실행금지; // Device-nGnRnE
            else 가운데[détà_sèdíwọ][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned 둘째값 = 0; 둘째값 < 사용자쪽수 / 512; 둘째값++)
        가운데[0][(사용자바탕 >> 21) + 둘째값] = (uintptr_t)(ojú_ìwé_Àtòkọ + 둘째값 * 512) | 3;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) ojú_ìwé_Àtòkọ[순번] = (사용자바탕 + 순번 * ìwọ̀n_ojú_ìwé) | kánẹ́ẹ̀lì_ojú_ìwé;
    uint64_t ibi_ìpamọ́_àwòmọ́_forúkọsílẹ̀ = 0x4400, àdírẹ́ẹ̀sì_Ìtumọ̀_ìdarí = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(ibi_ìpamọ́_àwòmọ́_forúkọsílẹ̀), "r"(àdírẹ́ẹ̀sì_Ìtumọ̀_ìdarí), "r"((uintptr_t)뿌리주소) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    시간제한멈춤();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 ìgbéwọlé_kókó_iye 때만 Fún_Lááyè_iye.
    maṣíìnì_forúkọsílẹ̀(IRQ_olùpín) = 0;
    maṣíìnì_forúkọsílẹ̀(IRQ_olùpín + 0x180) = 0xffffffff;
    maṣíìnì_forúkọsílẹ̀(IRQ_olùpín + 0x80) = 0xffffffff;
    maṣíìnì_forúkọsílẹ̀(IRQ_olùpín + 0x280) = 1u << 30;
    maṣíìnì_forúkọsílẹ̀(IRQ_olùpín + 0x41c) = 0x80808080;
    maṣíìnì_forúkọsílẹ̀(IRQ_olùpín + 0x100) = 1u << 30;
    maṣíìnì_forúkọsílẹ̀(IRQ_CPU_atọ́kùn + 4) = 0xff;
    maṣíìnì_forúkọsílẹ̀(IRQ_CPU_atọ́kùn + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Ààbò = (maṣíìnì_forúkọsílẹ̀(IRQ_olùpín + 4) & (1u << 10)) != 0;
    maṣíìnì_forúkọsílẹ̀(IRQ_olùpín) = Ààbò ? 1 : 3;
    maṣíìnì_forúkọsílẹ̀(IRQ_CPU_atọ́kùn) = Ààbò ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t irú_ìsọ̀rí, maṣíìnì_irú; uint32_t 판번호;
    uint64_t ìgbéwọlé_kókó, àtòjọ_ètò_àkọlé_Ìtayọ, abala_àkọlé_Ìtayọ; uint32_t 설정비트;
    uint16_t 실행머리크기, àtòjọ_ètò_àkọlé_ìgbéwọlé_ìwọn, 프로그램머리개수, abala_àkọlé_ìgbéwọlé_ìwọn, 구역머리개수, abala_orúkọ_atọ́ka_wá_atọ̀ka_àkóónú;
} 실행파일머리;
typedef struct { uint32_t irú_ìsọ̀rí, 설정비트; uint64_t Ìtayọ_iye, àdírẹ́ẹ̀sì, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(aṣàmúlò_férèmù) == 272, "exception assembly layout");
static int 포함된범위(uint64_t Ìtayọ_iye, uint64_t Ìwọ̀n, uint64_t parí_Ìtayọ) {
    return Ìtayọ_iye <= parí_Ìtayọ && Ìwọ̀n <= parí_Ìtayọ - Ìtayọ_iye;
}
static int 부가정보검사(const unsigned char *자료위치, size_t Ìwọ̀n) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, Ìwọ̀n)) {
        uint32_t 낱말들[3]; memcpy(낱말들, 자료위치 + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, Ìwọ̀n) || !포함된범위(현재위치 + 이름영역크기, 설명크기, Ìwọ̀n)) return 0;
        const unsigned char Orúkọ[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Orúkọ) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Orúkọ); 순번++) if (자료위치[현재위치 + 순번] != Orúkọ[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, 자료위치 + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *détà, size_t Ìwọ̀n, int 리눅스방식) {
    if (Ìwọ̀n < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, détà, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.irú_ìsọ̀rí != 2 || 실행머리.maṣíìnì_irú != 183 || 실행머리.판번호 != 1 || 실행머리.설정비트 || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.àtòjọ_ètò_àkọlé_ìgbéwọlé_ìwọn != sizeof(실행파일구획) || !실행머리.프로그램머리개수 || 실행머리.프로그램머리개수 > 16 ||
        실행머리.àtòjọ_ètò_àkọlé_Ìtayọ < sizeof(실행머리) || !포함된범위(실행머리.àtòjọ_ètò_àkọlé_Ìtayọ, (uint64_t)실행머리.프로그램머리개수 * sizeof(실행파일구획), Ìwọ̀n)) return 사용자실행파일오류;
    uint8_t 사용량[(aṣàmúlò_àwòrán_parí - 사용자바탕) / ìwọ̀n_ojú_ìwé] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.프로그램머리개수; 순번++) {
        실행파일구획 자료위치; memcpy(&자료위치, détà + 실행머리.àtòjọ_ètò_àkọlé_Ìtayọ + 순번 * sizeof(자료위치), sizeof(자료위치));
        if (자료위치.irú_ìsọ̀rí == 4) {
            if (!포함된범위(자료위치.Ìtayọ_iye, 자료위치.파일영역크기, Ìwọ̀n)) return 사용자실행파일오류;
            if (부가정보검사(détà + 자료위치.Ìtayọ_iye, 자료위치.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (자료위치.irú_ìsọ̀rí == 0 || 자료위치.irú_ìsọ̀rí == 6 || (자료위치.irú_ìsọ̀rí == 0x6474e551 && !(자료위치.설정비트 & 1))) continue;
        if (자료위치.irú_ìsọ̀rí != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!자료위치.기억영역크기) continue;
        if (자료위치.설정비트 & ~7u || !(자료위치.설정비트 & 4) || (자료위치.설정비트 & 3) == 3 || 자료위치.파일영역크기 > 자료위치.기억영역크기 ||
            (자료위치.파일영역크기 && !포함된범위(자료위치.Ìtayọ_iye, 자료위치.파일영역크기, Ìwọ̀n)) || 자료위치.àdírẹ́ẹ̀sì < 사용자바탕 ||
            !포함된범위(자료위치.àdírẹ́ẹ̀sì, 자료위치.기억영역크기, aṣàmúlò_àwòrán_parí) ||
            (!리눅스방식 && ((자료위치.àdírẹ́ẹ̀sì & (ìwọ̀n_ojú_ìwé - 1)) || (자료위치.Ìtayọ_iye & (ìwọ̀n_ojú_ìwé - 1)) || 자료위치.맞춤 != ìwọ̀n_ojú_ìwé)) ||
            (리눅스방식 && (((자료위치.àdírẹ́ẹ̀sì ^ 자료위치.Ìtayọ_iye) & (ìwọ̀n_ojú_ìwé - 1)) || !자료위치.맞춤 ||
                (자료위치.맞춤 & (자료위치.맞춤 - 1)) || 자료위치.맞춤 > 0x200000 || ((자료위치.àdírẹ́ẹ̀sì ^ 자료위치.Ìtayọ_iye) & (자료위치.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (자료위치.àdírẹ́ẹ̀sì - 사용자바탕) / ìwọ̀n_ojú_ìwé;
        unsigned 항목수 = ((자료위치.àdírẹ́ẹ̀sì & (ìwọ̀n_ojú_ìwé - 1)) + 자료위치.기억영역크기 + ìwọ̀n_ojú_ìwé - 1) / ìwọ̀n_ojú_ìwé;
        for (unsigned ojú_ìwé_iye = 첫항목; ojú_ìwé_iye < 첫항목 + 항목수; ojú_ìwé_iye++) {
            if (사용량[ojú_ìwé_iye]) return 사용자실행파일오류;
            사용량[ojú_ìwé_iye] = 1;
        }
        if ((자료위치.설정비트 & 1) && 실행머리.ìgbéwọlé_kókó >= 자료위치.àdírẹ́ẹ̀sì && 실행머리.ìgbéwọlé_kókó < 자료위치.àdírẹ́ẹ̀sì + 자료위치.파일영역크기 && !(실행머리.ìgbéwọlé_kókó & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *détà, size_t Ìwọ̀n) { return 실행파일검사(détà, Ìwọ̀n, 0); }
static void àgbékalẹ̀_ìwò_ojú_ìwé(uintptr_t àdírẹ́ẹ̀sì, uint64_t 설정비트, unsigned ìyànda) {
    unsigned 색인 = (àdírẹ́ẹ̀sì - 사용자바탕) / ìwọ̀n_ojú_ìwé;
    ojú_ìwé_Àtòkọ[색인] = àdírẹ́ẹ̀sì | 설정비트;
    ìyànda_Àtòkọ[색인] = ìyànda;
}
static int 사용자범위(uintptr_t àdírẹ́ẹ̀sì, size_t 항목수, int 쓰는중) {
    if (àdírẹ́ẹ̀sì < 사용자바탕 || !포함된범위(àdírẹ́ẹ̀sì, 항목수, aṣàmúlò_parí)) return 0;
    if (!항목수) return 1;
    unsigned 첫항목 = (àdírẹ́ẹ̀sì - 사용자바탕) / ìwọ̀n_ojú_ìwé, 마지막 = (àdírẹ́ẹ̀sì + 항목수 - 1 - 사용자바탕) / ìwọ̀n_ojú_ìwé;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(ìyànda_Àtòkọ[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int ṣẹ̀dà_ọ̀nà(uintptr_t àdírẹ́ẹ̀sì, char *ọ̀nà) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(àdírẹ́ẹ̀sì, 1, 0)) return -14;
        ọ̀nà[순번] = *(const char *)àdírẹ́ẹ̀sì++;
        if (!ọ̀nà[순번]) return 0;
    }
    return -36;
}
static intptr_t 커널결과(intptr_t 결과) { return 결과 < 0 ? -오류번호 : 결과; }
static int 대응파일기술자(uint64_t fáìlì_èkù) { return fáìlì_èkù >= 3 && fáìlì_èkù < 19 ? fáìlì_Àtòkọ[fáìlì_èkù - 3] : -1; }
static int 통신끝점소유(uint64_t fáìlì_èkù) { return fáìlì_èkù >= 32 && fáìlì_èkù < 56 && 통신끝점들[fáìlì_èkù - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t gígùn_iye, struct pk_sockaddr_in *àdírẹ́ẹ̀sì) {
    if (gígùn_iye != sizeof(*àdírẹ́ẹ̀sì)) return -22;
    if (!사용자범위(가리킴값, gígùn_iye, 0)) return -14;
    memcpy(àdírẹ́ẹ̀sì, (const void *)가리킴값, sizeof(*àdírẹ́ẹ̀sì));
    return àdírẹ́ẹ̀sì->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t gígùn_ìtọ́ka, pk_socklen_t *수용량) {
    if (!사용자범위(gígùn_ìtọ́ka, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)gígùn_ìtọ́ka, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t gígùn_ìtọ́ka, pk_socklen_t 수용량, int àdírẹ́ẹ̀sì, int 접속번호) {
    struct pk_sockaddr_in iye; memset(&iye, 0, sizeof(iye));
    iye.sin_family = AF_INET; iye.sin_port = pk_htons(접속번호); iye.sin_addr.s_addr = pk_htonl(àdírẹ́ẹ̀sì);
    if (수용량) memcpy((void *)가리킴값, &iye, 수용량);
    pk_socklen_t gígùn_iye = sizeof(iye); memcpy((void *)gígùn_ìtọ́ka, &gígùn_iye, sizeof(gígùn_iye));
}
extern uintptr_t 보드통로(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(aṣàmúlò_férèmù *fáìlì_ìgbéwọlé) {
    uintptr_t 첫째값 = fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[0], 둘째값 = fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[1], kóòdù_ẹyọ_ọ̀rọ̀ = fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[2];
    char ọ̀nà[65];
    int fáìlì_èkù, 결과;
    switch (fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: ìtọ́ka 전체를 검사한 Padà_sẹ́yìn_iye 출력/Fáìlì ṣàyípadà_iye
        if (kóòdù_ẹyọ_ọ̀rọ̀ > 65536) return -22;
        if (!사용자범위(둘째값, kóòdù_ẹyọ_ọ̀rọ̀, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=aago_iye();
            for (size_t 순번 = 0; 순번 < kóòdù_ẹyọ_ọ̀rọ̀; 순번++) 보드통로(첫째값, ((const unsigned char *)둘째값)[순번]);
            /* 큰 tty를 그린 kánẹ́ẹ̀lì_iye 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(ìjọṣepọ̀){
                마감시각+=aago_iye()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return kóòdù_ẹyọ_ọ̀rọ̀;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t 개수=kóòdù_ẹyọ_ọ̀rọ̀>512?512:kóòdù_ẹyọ_ọ̀rọ̀;for(size_t 순번=0;순번<개수;순번++)자바전문넣기(순번,((const unsigned char *)둘째값)[순번]);return 자바흐름쓰기(첫째값,개수);
        }
        fáìlì_èkù = 대응파일기술자(첫째값); if (fáìlì_èkù < 0) return -9;
        return 커널결과(pk_write(fáìlì_èkù, (const void *)둘째값, kóòdù_ẹyọ_ọ̀rọ̀));
    case 2:
        if (kóòdù_ẹyọ_ọ̀rọ̀ > 65536) return -22;
        if (!사용자범위(둘째값, kóòdù_ẹyọ_ọ̀rọ̀, 1)) return -14;
        if (첫째값 == 0) {
            size_t 개수 = 0;
            while (개수 < kóòdù_ẹyọ_ọ̀rọ̀) {
                int ẹyọ_ọ̀rọ̀_iye = (int32_t)보드글자읽기(); if (ẹyọ_ọ̀rọ̀_iye == -2) return 개수; if (ẹyọ_ọ̀rọ̀_iye < 0) break;
                ((unsigned char *)둘째값)[개수++] = ẹyọ_ọ̀rọ̀_iye;
            }
            return 개수 ? (intptr_t)개수 : (kóòdù_ẹyọ_ọ̀rọ̀ ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            결과=자바흐름읽기(첫째값,kóòdù_ẹyọ_ọ̀rọ̀>512?512:kóòdù_ẹyọ_ọ̀rọ̀);if(결과>0)for(int 순번=0;순번<결과;순번++)((unsigned char *)둘째값)[순번]=자바전문얻기(순번);return 결과;
        }
        fáìlì_èkù = 대응파일기술자(첫째값); if (fáìlì_èkù < 0) return -9;
        return 커널결과(pk_read(fáìlì_èkù, (void *)둘째값, kóòdù_ẹyọ_ọ̀rọ̀));
    case 3:
        결과 = ṣẹ̀dà_ọ̀nà(첫째값, ọ̀nà); if (결과) return 결과;
        if (둘째값 > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (fáìlì_Àtòkọ[순번] < 0) {
            fáìlì_èkù = pk_open(ọ̀nà, (int)둘째값, 0600);
            if (fáìlì_èkù < 0) return -오류번호;
            fáìlì_Àtòkọ[순번] = fáìlì_èkù; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { 결과 = 통신끝점닫기(첫째값); if (!결과) 통신끝점들[첫째값 - 32] = 0; return 결과; }
        fáìlì_èkù = 대응파일기술자(첫째값); if (fáìlì_èkù < 0) return -9;
        결과 = pk_close(fáìlì_èkù); if (!결과) fáìlì_Àtòkọ[첫째값 - 3] = -1;
        return 커널결과(결과);
    case 5:
        fáìlì_èkù = 대응파일기술자(첫째값); if (fáìlì_èkù < 0) return -9;
        if (kóòdù_ẹyọ_ọ̀rọ̀ > 2) return -22;
        return 커널결과(pk_lseek(fáìlì_èkù, (int64_t)둘째값, kóòdù_ẹyọ_ọ̀rọ̀));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 aṣàmúlò RW/NX 힙, 새로 노출되는 페이지는 0으로 pàjùbà
        if (!첫째값) return 동적기억끝;
        if (첫째값 < aṣàmúlò_àwòrán_parí || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + ìwọ̀n_ojú_ìwé - 1) & ~(ìwọ̀n_ojú_ìwé - 1);
        uintptr_t 새쪽들 = (첫째값 + ìwọ̀n_ojú_ìwé - 1) & ~(ìwọ̀n_ojú_ìwé - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t 자료위치 = 이전쪽들; 자료위치 < 새쪽들; 자료위치 += ìwọ̀n_ojú_ìwé) àgbékalẹ̀_ìwò_ojú_ìwé(자료위치, kánẹ́ẹ̀lì_ojú_ìwé, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t 자료위치 = 이전쪽들; 자료위치 < 새쪽들; 자료위치 += ìwọ̀n_ojú_ìwé) àgbékalẹ̀_ìwò_ojú_ìwé(자료위치, aṣàmúlò_tí_a_lè_kà_tí_a_lè_kọ, 3);
        } else {
            for (uintptr_t 자료위치 = 새쪽들; 자료위치 < 이전쪽들; 자료위치 += ìwọ̀n_ojú_ìwé) {
                ojú_ìwé_Àtòkọ[(자료위치 - 사용자바탕) / ìwọ̀n_ojú_ìwé] = 0; ìyànda_Àtòkọ[(자료위치 - 사용자바탕) / ìwọ̀n_ojú_ìwé] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        fáìlì_èkù = 대응파일기술자(첫째값); return fáìlì_èkù < 0 ? -9 : 커널결과(pk_size(fáìlì_èkù));
    case 10:
        fáìlì_èkù = 대응파일기술자(첫째값); return fáìlì_èkù < 0 ? -9 : 커널결과(pk_ftruncate(fáìlì_èkù, (int64_t)둘째값));
    case 11:
        결과 = ṣẹ̀dà_ọ̀nà(첫째값, ọ̀nà); return 결과 ? 결과 : 커널결과(pk_unlink(ọ̀nà));
    case 12:
        fáìlì_èkù = 대응파일기술자(첫째값); return fáìlì_èkù < 0 ? -9 : 커널결과(pk_fsync(fáìlì_èkù));
    case 13: { // 그래픽 기초 API: aṣàmúlò 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[3], 높이값 = fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || 둘째값 > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - 둘째값) return -22;
        for (uintptr_t 세로좌표 = 둘째값; 세로좌표 < 둘째값 + 높이값; 세로좌표++) for (uintptr_t ibi_ìtọ́kasí_x = 첫째값; ibi_ìtọ́kasí_x < 첫째값 + 너비값; ibi_ìtọ́kasí_x++) 보드화소(ibi_ìtọ́kasí_x, 세로좌표, kóòdù_ẹyọ_ọ̀rọ̀);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=개수; args(index,buffer,capacity)=UTF-8 gígùn_iye
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (kóòdù_ẹyọ_ọ̀rọ̀ <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(둘째값, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)둘째값, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;ìjọṣepọ̀=1;return 보드터미널(13);}
        if(첫째값==2){ìjọṣepọ̀=0;return 0;}
        if(첫째값==3)return 보드터미널(13);
        if(첫째값!=1||!ìjọṣepọ̀)return -22;
        결과=(int32_t)보드글자읽기();
        if(결과==-4096)return 결과;
        시간제한시작();return 결과<0?-11:결과;
    case 17: { // 유한한 협력 대기: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t 끝시각 = aago_iye() + 진동수 * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (aago_iye() < 끝시각);
        시간제한시작(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (둘째값 > 2) return -22;
        결과 = ṣẹ̀dà_ọ̀nà(첫째값, ọ̀nà); if (결과) return 결과;
        unsigned gígùn_iye = 0; while (ọ̀nà[gígùn_iye]) gígùn_iye++;
        결과 = 자바경로시작(gígùn_iye); if (결과 < 0) return 결과;
        for (unsigned 순번 = 0; 순번 < gígùn_iye; 순번++) 자바경로바이트(순번, (unsigned char)ọ̀nà[순번]);
        return 둘째값 == 0 ? 자바항목종류() : 둘째값 == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int ẹyọ_ọ̀rọ̀_iye=(int32_t)보드글자읽기();if(ẹyọ_ọ̀rọ̀_iye==-4096)return ẹyọ_ọ̀rọ̀_iye;if(ẹyọ_ọ̀rọ̀_iye>=0)화면누름(Oníǹkan_nǹkan,ẹyọ_ọ̀rọ̀_iye);시간제한시작();}
        if(첫째값==3&&kóòdù_ẹyọ_ọ̀rọ̀){if(!자바셸대화형())return -95;ìjọṣepọ̀=1;보드터미널(300);}
        return 화면호출(Oníǹkan_nǹkan,첫째값,둘째값,kóòdù_ẹyọ_ọ̀rọ̀,fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[3],fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[4],fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[5]);
    case 21:
        if(kóòdù_ẹyọ_ọ̀rọ̀>127)return -22;if(!사용자범위(둘째값,kóòdù_ẹyọ_ọ̀rọ̀*sizeof(uint32_t),0))return -14;
        return 화면글(Oníǹkan_nǹkan,첫째값,(const uint32_t *)둘째값,kóòdù_ẹyọ_ọ̀rọ̀);
    case 22: // 화면 Ìwọ̀n aṣèbéèré_iye: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(둘째값==SOCK_STREAM&&(kóòdù_ẹyọ_ọ̀rọ̀==0||kóòdù_ẹyọ_ọ̀rọ̀==6))결과=자바흐름만들기();
        else if(둘째값==SOCK_DGRAM&&(kóòdù_ẹyọ_ọ̀rọ̀==0||kóòdù_ẹyọ_ọ̀rọ̀==IPPROTO_UDP))결과=자바전문만들기(첫째값,둘째값,kóòdù_ẹyọ_ọ̀rọ̀);
        else return -93;
        if (결과 >= 32 && 결과 < 56) 통신끝점들[결과 - 32] = 1;
        return 결과;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in àdírẹ́ẹ̀sì;
        결과 = 주소입력(둘째값, kóòdù_ẹyọ_ọ̀rọ̀, &àdírẹ́ẹ̀sì); if (결과) return 결과;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(àdírẹ́ẹ̀sì.sin_addr.s_addr),pk_htons(àdírẹ́ẹ̀sì.sin_port)):자바전문묶기(첫째값, pk_htonl(àdírẹ́ẹ̀sì.sin_addr.s_addr), pk_htons(àdírẹ́ẹ̀sì.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[3]) return -95;
        if (kóòdù_ẹyọ_ọ̀rọ̀ > 512) return -90;
        if (kóòdù_ẹyọ_ọ̀rọ̀ && !사용자범위(둘째값, kóòdù_ẹyọ_ọ̀rọ̀, 0)) return -14;
        struct pk_sockaddr_in àdírẹ́ẹ̀sì;
        결과 = 주소입력(fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[4], fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[5], &àdírẹ́ẹ̀sì); if (결과) return 결과;
        for (unsigned 순번 = 0; 순번 < kóòdù_ẹyọ_ọ̀rọ̀; 순번++) 자바전문넣기(순번, ((const unsigned char *)둘째값)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(àdírẹ́ẹ̀sì.sin_addr.s_addr), pk_htons(àdírẹ́ẹ̀sì.sin_port), kóòdù_ẹyọ_ọ̀rọ̀);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[3]) return -95;
        if (kóòdù_ẹyọ_ọ̀rọ̀ > 512) return -90;
        if (kóòdù_ẹyọ_ọ̀rọ̀ && !사용자범위(둘째값, kóòdù_ẹyọ_ọ̀rọ̀, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[4]) { 결과 = 주소출력검사(fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[4], fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[5], &수용량); if (결과) return 결과; }
        결과 = 자바전문받기(첫째값, kóòdù_ẹyọ_ọ̀rọ̀); if (결과 < 0) return 결과;
        for (int 순번 = 0; 순번 < 결과; 순번++) ((unsigned char *)둘째값)[순번] = 자바전문얻기(순번);
        if (fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[4]) 주소출력(fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[4], fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return 결과;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        결과 = 주소출력검사(둘째값, kóòdù_ẹyọ_ọ̀rọ̀, &수용량); if (결과) return 결과;
        주소출력(둘째값,kóòdù_ẹyọ_ọ̀rọ̀,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in àdírẹ́ẹ̀sì;
        결과=주소입력(둘째값,kóòdù_ẹyọ_ọ̀rọ̀,&àdírẹ́ẹ̀sì);if(결과)return 결과;
        return 자바흐름연결(첫째값,pk_htonl(àdírẹ́ẹ̀sì.sin_addr.s_addr),pk_htons(àdírẹ́ẹ̀sì.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,둘째값):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(둘째값||kóòdù_ẹyọ_ọ̀rọ̀)return -95;결과=자바흐름연결받기(첫째값);if(결과>=40&&결과<56)통신끝점들[결과-32]=1;return 결과;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(aṣàmúlò_férèmù *fáìlì_ìgbéwọlé) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(fáìlì_ìgbéwọlé) : 자체체계호출(fáìlì_ìgbéwọlé);
}
static void 커널돌아가기(aṣàmúlò_férèmù *fáìlì_ìgbéwọlé, int 결과) {
    시간제한멈춤();
    fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[0] = (uint64_t)(int64_t)결과;
    fáìlì_ìgbéwọlé->명령위치 = (uintptr_t)사용자복귀;
    fáìlì_ìgbéwọlé->상태값 = 0x3c5; // EL1h, DAIF masked
}
int 사용자예외(aṣàmúlò_férèmù *fáìlì_ìgbéwọlé, unsigned 가로채기) {
    if (!tó_ń_ṣiṣẹ́ || (fáìlì_ìgbéwọlé->상태값 & 15) != 0) return 0;
    if (가로채기) {
        uint32_t 승인값 = maṣíìnì_forúkọsílẹ̀(IRQ_CPU_atọ́kùn + 0xc), Àfidámọ̀_iye = 승인값 & 1023;
        if (Àfidámọ̀_iye == 30) { 커널돌아가기(fáìlì_ìgbéwọlé, 사용자시간초과); maṣíìnì_forúkọsílẹ̀(IRQ_CPU_atọ́kùn + 0x10) = 승인값; return 1; }
        if (Àfidámọ̀_iye < 1020) maṣíìnì_forúkọsílẹ̀(IRQ_CPU_atọ́kùn + 0x10) = 승인값;
        return 1;
    }
    uint64_t 예외상태; __asm__ volatile("mrs %0, esr_el1" : "=r"(예외상태));
    if (aago_iye() >= 마감시각) { 커널돌아가기(fáìlì_ìgbéwọlé, 사용자시간초과); return 1; }
    unsigned 예외분류 = 예외상태 >> 26;
    if (예외분류 == 0x15 && (예외상태 & 0xffff) == 0) {
        if (리눅스규약 ? fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[8] == 93 || fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[8] == 94 : fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[8] == 6) 커널돌아가기(fáìlì_ìgbéwọlé, (int)(fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[0] & 255));
        else {
            intptr_t 결과=체계호출(fáìlì_ìgbéwọlé);
            if(결과==-4096&&ìjọṣepọ̀){
                저장값[Oníǹkan_nǹkan].실행틀=*fáìlì_ìgbéwọlé;저장값[Oníǹkan_nǹkan].실행틀.명령위치-=4;
                사용자실수보관(저장값[Oníǹkan_nǹkan].실수저장상태);커널돌아가기(fáìlì_ìgbéwọlé,사용자중단됨);
            }else fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[0]=(uint64_t)결과;
        }
    } else 커널돌아가기(fáìlì_ìgbéwọlé, 예외분류 == 0x24 ? aṣàmúlò_détà_àṣìṣe : 예외분류 == 0x20 ? 사용자실행오류 : aṣàmúlò_aláìbẹgbẹmu_ìtọ́sọ́nà);
    return 1;
}

// 생성된 const ELF Àjọṣe_iye: 실행은 반드시 àtòjọ_ètò_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *détà; size_t Ìwọ̀n; unsigned 전달값; } àtòjọ_ètò;
#include "programs.h"
static void *ẹ̀dà(unsigned 자리){return (void *)(0x04000000ul+자리*(aṣàmúlò_parí-사용자바탕));}
static int Parí_àtòjọ_ètò(int 결과){
    사용자누적시각[Oníǹkan_nǹkan]+=(uint32_t)보드밀리초()-사용자실행시각[Oníǹkan_nǹkan];
    시간제한멈춤();tó_ń_ṣiṣẹ́=0;
    if(결과==사용자중단됨){
        저장된작업 *fọ́nrán_détà=&저장값[Oníǹkan_nǹkan];fọ́nrán_détà->멈춤상태=1;fọ́nrán_détà->ìjọṣepọ̀=ìjọṣepọ̀;fọ́nrán_détà->리눅스규약=리눅스규약;fọ́nrán_détà->동적기억공간=동적기억끝;fọ́nrán_détà->인수개수=전달인수개수;
        memcpy(fọ́nrán_détà->ìyànda_Àtòkọ,ìyànda_Àtòkọ,sizeof(ìyànda_Àtòkọ));memcpy(fọ́nrán_détà->fáìlì_Àtòkọ,fáìlì_Àtòkọ,sizeof(fáìlì_Àtòkọ));memcpy(fọ́nrán_détà->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(fọ́nrán_détà->ágúmẹ́ntì_ÀRÉÈ,전달인수,sizeof(전달인수));memcpy(fọ́nrán_détà->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<사용자쪽수;순번++)if(ìyànda_Àtòkọ[순번])memcpy((unsigned char *)ẹ̀dà(Oníǹkan_nǹkan)+순번*ìwọ̀n_ojú_ìwé,(void *)(사용자바탕+순번*ìwọ̀n_ojú_ìwé),ìwọ̀n_ojú_ìwé);
    }else{
        저장값[Oníǹkan_nǹkan].멈춤상태=0;화면초기화(Oníǹkan_nǹkan);
        for(unsigned 순번=0;순번<16;순번++)if(fáìlì_Àtòkọ[순번]>=0)pk_close(fáìlì_Àtòkọ[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<사용자쪽수;순번++){ojú_ìwé_Àtòkọ[순번]=0;ìyànda_Àtòkọ[순번]=0;}변환표맞추기();return 결과;
}
uintptr_t 보드사용자제어(uintptr_t ìṣe){
    unsigned 자리=ìṣe&15;if(자리>=4||tó_ń_ṣiṣẹ́)return (uint32_t)-22;
    저장된작업 *fọ́nrán_détà=&저장값[자리];
    if(ìṣe>=32){if(fọ́nrán_détà->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(fọ́nrán_détà->fáìlì_Àtòkọ[순번]>=0)pk_close(fọ́nrán_détà->fáìlì_Àtòkọ[순번]);for(unsigned 순번=0;순번<24;순번++)if(fọ́nrán_détà->통신끝점들[순번])통신끝점닫기(순번+32);}fọ́nrán_détà->멈춤상태=0;화면초기화(자리);return 0;}
    if(ìṣe>=16)return fọ́nrán_détà->멈춤상태;
    if(!fọ́nrán_détà->멈춤상태)return (uint32_t)-22;
    Oníǹkan_nǹkan=자리;ìjọṣepọ̀=fọ́nrán_détà->ìjọṣepọ̀;리눅스규약=fọ́nrán_détà->리눅스규약;동적기억끝=fọ́nrán_détà->동적기억공간;전달인수개수=fọ́nrán_détà->인수개수;
    memcpy(fáìlì_Àtòkọ,fọ́nrán_détà->fáìlì_Àtòkọ,sizeof(fáìlì_Àtòkọ));memcpy(통신끝점들,fọ́nrán_détà->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,fọ́nrán_détà->ágúmẹ́ntì_ÀRÉÈ,sizeof(전달인수));memcpy(전달인수길이,fọ́nrán_détà->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<사용자쪽수;순번++)ojú_ìwé_Àtòkọ[순번]=(사용자바탕+순번*ìwọ̀n_ojú_ìwé)|kánẹ́ẹ̀lì_ojú_ìwé;변환표맞추기();
    memset((void *)사용자바탕,0,aṣàmúlò_parí-사용자바탕);
    for(unsigned 순번=0;순번<사용자쪽수;순번++)if(fọ́nrán_détà->ìyànda_Àtòkọ[순번])memcpy((void *)(사용자바탕+순번*ìwọ̀n_ojú_ìwé),(unsigned char *)ẹ̀dà(자리)+순번*ìwọ̀n_ojú_ìwé,ìwọ̀n_ojú_ìwé);
    memcpy(ìyànda_Àtòkọ,fọ́nrán_détà->ìyànda_Àtòkọ,sizeof(ìyànda_Àtòkọ));
    for(unsigned 순번=0;순번<사용자쪽수;순번++){unsigned 자료위치=ìyànda_Àtòkọ[순번];ojú_ìwé_Àtòkọ[순번]=자료위치?(사용자바탕+순번*ìwọ̀n_ojú_ìwé)|(자료위치==3?aṣàmúlò_tí_a_lè_kà_tí_a_lè_kọ:자료위치==5?사용자읽고실행:aṣàmúlò_kàn_kàá):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");tó_ń_ṣiṣẹ́=1;fọ́nrán_détà->멈춤상태=0;시간제한시작();
    사용자실행시각[Oníǹkan_nǹkan]=보드밀리초();
    return (uint32_t)Parí_àtòjọ_ètò(aṣàmúlò_CV(&fọ́nrán_détà->실행틀,fọ́nrán_détà->실수저장상태));
}
static int ṣiṣẹ́_àtòjọ_ètò(const unsigned char *détà, size_t Ìwọ̀n, unsigned 전달값, int 리눅스방식, const char *Orúkọ) {
    if (tó_ń_ṣiṣẹ́) return -16;
    Oníǹkan_nǹkan=보드터미널(11);if(Oníǹkan_nǹkan<0||Oníǹkan_nǹkan>3||저장값[Oníǹkan_nǹkan].멈춤상태)return -16;ìjọṣepọ̀=0;
    int 유효함 = 실행파일검사(détà, Ìwọ̀n, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned orúkọ_wá_atọ̀ka_àkóónú=0;
    while (*Orúkọ && orúkọ_wá_atọ̀ka_àkóónú<31) aṣàmúlò_àṣẹ_orúkọ[Oníǹkan_nǹkan][orúkọ_wá_atọ̀ka_àkóónú++]=(unsigned char)*Orúkọ++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (orúkọ_wá_atọ̀ka_àkóónú) aṣàmúlò_àṣẹ_orúkọ[Oníǹkan_nǹkan][orúkọ_wá_atọ̀ka_àkóónú++]=' ';
        for (unsigned 자리=0; 자리<전달인수길이[0]; 자리++) aṣàmúlò_àṣẹ_orúkọ[Oníǹkan_nǹkan][orúkọ_wá_atọ̀ka_àkóónú++]=전달인수[0][자리];
    }
    aṣàmúlò_àṣẹ_orúkọ[Oníǹkan_nǹkan][orúkọ_wá_atọ̀ka_àkóónú]=0; nọ́ńbà_aṣàmúlò[Oníǹkan_nǹkan]=다음사용자번호++;
    if (다음사용자번호>0x7fffffffu) 다음사용자번호=10;
    사용자시작시각[Oníǹkan_nǹkan]=보드밀리초(); 사용자누적시각[Oníǹkan_nǹkan]=0;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) ojú_ìwé_Àtòkọ[순번] = (사용자바탕 + 순번 * ìwọ̀n_ojú_ìwé) | kánẹ́ẹ̀lì_ojú_ìwé;
    변환표맞추기();
    memset((void *)사용자바탕, 0, aṣàmúlò_parí - 사용자바탕);
    memset(ìyànda_Àtòkọ, 0, sizeof(ìyànda_Àtòkọ));
    실행파일머리 실행머리; memcpy(&실행머리, détà, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.프로그램머리개수; 순번++) {
        실행파일구획 자료위치; memcpy(&자료위치, détà + 실행머리.àtòjọ_ètò_àkọlé_Ìtayọ + 순번 * sizeof(자료위치), sizeof(자료위치));
        if (자료위치.irú_ìsọ̀rí != 1 || !자료위치.기억영역크기) continue;
        if (자료위치.파일영역크기) memcpy((void *)(uintptr_t)자료위치.àdírẹ́ẹ̀sì, détà + 자료위치.Ìtayọ_iye, 자료위치.파일영역크기);
        for (uintptr_t 현재위치 = 자료위치.àdírẹ́ẹ̀sì & ~(ìwọ̀n_ojú_ìwé - 1); 현재위치 < 자료위치.àdírẹ́ẹ̀sì + 자료위치.기억영역크기; 현재위치 += ìwọ̀n_ojú_ìwé) {
            ìyànda_Àtòkọ[(현재위치 - 사용자바탕) / ìwọ̀n_ojú_ìwé] = (자료위치.설정비트 & 2) ? 3 : ((자료위치.설정비트 & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = aṣàmúlò_kójọ_àdírẹ́ẹ̀sì; 현재위치 < aṣàmúlò_parí; 현재위치 += ìwọ̀n_ojú_ìwé) ìyànda_Àtòkọ[(현재위치 - 사용자바탕) / ìwọ̀n_ojú_ìwé] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.ìgbéwọlé_kókó) : aṣàmúlò_parí;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) {
        unsigned ìyànda = ìyànda_Àtòkọ[순번];
        ojú_ìwé_Àtòkọ[순번] = ìyànda ? (사용자바탕 + 순번 * ìwọ̀n_ojú_ìwé) | (ìyànda == 3 ? aṣàmúlò_tí_a_lè_kà_tí_a_lè_kọ : ìyànda == 5 ? 사용자읽고실행 : aṣàmúlò_kàn_kàá) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) fáìlì_Àtòkọ[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = aṣàmúlò_àwòrán_parí;
    tó_ń_ṣiṣẹ́ = 1; 시간제한시작();
    사용자실행시각[Oníǹkan_nǹkan]=보드밀리초();
    int 결과 = aṣàmúlò_ṣàtẹ̀wọlé(실행머리.ìgbéwọlé_kókó, 초기쌓임공간, 전달값);
    return Parí_àtòjọ_ètò(결과);
}
uintptr_t 보드사용자실행(uintptr_t 색인) {
    if (색인 >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Orúkọ=색인==10?"javac":색인==11?"java":색인==12?"python":색인==13?"vi":색인==14?"jar":색인==15?"cc":색인==16?"jaot":"ELF";
    return (uint32_t)ṣiṣẹ́_àtòjọ_ètò(실행항목들[색인].détà, 실행항목들[색인].Ìwọ̀n, 실행항목들[색인].전달값, 0, Orúkọ);
}
static uintptr_t ṣiṣẹ́_fáìlì(int 리눅스방식) {
    static unsigned char àwòrán[16384];
    if (tó_ń_ṣiṣẹ́ || !전달인수개수) return (uint32_t)-22;
    int fáìlì_èkù = pk_open((const char *)전달인수[0], kàn_kàá_iye, 0);
    if (fáìlì_èkù < 0) return (uint32_t)-오류번호;
    int Ìwọ̀n = pk_size(fáìlì_èkù);
    if (Ìwọ̀n < 0 || (unsigned)Ìwọ̀n > sizeof(àwòrán)) { pk_close(fáìlì_èkù); return (uint32_t)-27; }
    int 받은수 = pk_read(fáìlì_èkù, àwòrán, Ìwọ̀n); pk_close(fáìlì_èkù);
    if (받은수 != Ìwọ̀n) return (uint32_t)-5;
    return (uint32_t)ṣiṣẹ́_àtòjọ_ètò(àwòrán, Ìwọ̀n, 0, 리눅스방식, "");
}
uintptr_t 보드사용자파일(void) { return ṣiṣẹ́_fáìlì(0); }
uintptr_t 보드사용자리눅스파일(void) { return ṣiṣẹ́_fáìlì(1); }
uintptr_t 보드사용자검사(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].détà, 잘못된실행항목들[순번].Ìwọ̀n) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
