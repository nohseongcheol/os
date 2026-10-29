#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 실행 기계 계층. 파일 자료/정책은 기존 AOT Java 커널에 위임한다.
#include "사용자.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../통신망/통신망.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 가로채기분배기 0xff841000ul
#define 가로채기중앙처리기 0xff842000ul
#define 쪽크기 4096ul
#define 접근표시 (1ul << 10)
#define 권한실행금지 (1ul << 53)
#define 사용자실행금지 (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define 커널쪽 (3ul | 보통기억 | 권한실행금지 | 사용자실행금지)
#define 사용자읽고쓰기 (3ul | 보통기억 | (1ul << 6) | 권한실행금지 | 사용자실행금지)
#define 사용자읽기전용 (3ul | 보통기억 | (3ul << 6) | 권한실행금지 | 사용자실행금지)
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
extern int 사용자재개(사용자실행틀 *,void *);
extern void 사용자실수보관(void *);
extern int 사용자진입(uintptr_t 진입점, uintptr_t 쌓임공간, uintptr_t 전달값);
extern void 사용자복귀(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t 뿌리주소[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t 쪽목록[사용자쪽수] __attribute__((aligned(4096)));
static uint8_t 권한목록[사용자쪽수];
static int 활성, 파일목록[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned 파일기술자){return 파일기술자<40?자바전문닫기(파일기술자):자바흐름닫기(파일기술자);}
static uint64_t 진동수, 마감시각;
static uintptr_t 동적기억끝;
// 커널 셸이 준비한 UTF-8 인수. EL0에는 복사 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,대화형,리눅스규약,파일목록[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char 인수배열[8][256],권한목록[사용자쪽수];
    uintptr_t 동적기억공간; 사용자실행틀 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int 소유자,대화형;
static uint32_t 사용자번호[4], 사용자시작시각[4], 사용자누적시각[4], 사용자실행시각[4], 다음사용자번호=10;
static unsigned char 사용자명령이름[4][288];
uint32_t 사용자상태읽기(unsigned 항목, unsigned 번호) {
    unsigned 자리=번호&3;
    int 상태=(활성 && 소유자==(int)자리) ? 1 : 저장값[자리].멈춤상태 ? 2 : 0;
    if (항목==0) return 상태;
    if (!상태) return 0;
    if (항목==1) return 사용자번호[자리];
    if (항목==2) {
        unsigned char *쪽들=상태==1?권한목록:저장값[자리].권한목록;
        unsigned 쪽수=0; for (unsigned 순번=0; 순번<사용자쪽수; 순번++) if(쪽들[순번]) 쪽수++;
        return 쪽수*4;
    }
    if (항목==3) return (uint32_t)보드밀리초()-사용자시작시각[자리];
    if (항목==4) return 사용자누적시각[자리]+(상태==1?(uint32_t)보드밀리초()-사용자실행시각[자리]:0);
    if (항목==5) return 번호/4<sizeof(사용자명령이름[0])?사용자명령이름[자리][번호/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t 항목수) {
    if (활성 || 항목수 > 8) return (uint32_t)-22;
    전달인수개수 = 항목수;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t 색인, uintptr_t 현재위치, uintptr_t 바이트값) {
    if (활성 || 색인 >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[색인] || !바이트값 || 바이트값 > 255)
        return (uint32_t)-22;
    전달인수[색인][현재위치] = 바이트값;
    전달인수길이[색인] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t 시계값(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void 시간제한멈춤(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    기계저장기(가로채기분배기 + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void 시간제한시작(void) {
    uint64_t 간격 = 진동수 * 2, 활성화 = 1;
    마감시각 = 시계값() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(활성화) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned 자료덩이 = 0; 자료덩이 < 4; 자료덩이++) {
        뿌리주소[자료덩이] = (uintptr_t)가운데[자료덩이] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t 주소 = ((uintptr_t)자료덩이 << 30) | ((uintptr_t)순번 << 21);
            가운데[자료덩이][순번] = 주소 | 1 | 접근표시 | 사용자실행금지;
            if (주소 >= 0xfc000000ul) 가운데[자료덩이][순번] |= 권한실행금지; // Device-nGnRnE
            else 가운데[자료덩이][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned 둘째값 = 0; 둘째값 < 사용자쪽수 / 512; 둘째값++)
        가운데[0][(사용자바탕 >> 21) + 둘째값] = (uintptr_t)(쪽목록 + 둘째값 * 512) | 3;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) 쪽목록[순번] = (사용자바탕 + 순번 * 쪽크기) | 커널쪽;
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
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 진입 때만 허용.
    기계저장기(가로채기분배기) = 0;
    기계저장기(가로채기분배기 + 0x180) = 0xffffffff;
    기계저장기(가로채기분배기 + 0x80) = 0xffffffff;
    기계저장기(가로채기분배기 + 0x280) = 1u << 30;
    기계저장기(가로채기분배기 + 0x41c) = 0x80808080;
    기계저장기(가로채기분배기 + 0x100) = 1u << 30;
    기계저장기(가로채기중앙처리기 + 4) = 0xff;
    기계저장기(가로채기중앙처리기 + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int 보호정책 = (기계저장기(가로채기분배기 + 4) & (1u << 10)) != 0;
    기계저장기(가로채기분배기) = 보호정책 ? 1 : 3;
    기계저장기(가로채기중앙처리기) = 보호정책 ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t 유형, 기계유형; uint32_t 판번호;
    uint64_t 진입점, 프로그램머리변위, 구역머리변위; uint32_t 설정비트;
    uint16_t 실행머리크기, 프로그램머리항목크기, 프로그램머리개수, 구역머리항목크기, 구역머리개수, 구역이름표색인;
} 실행파일머리;
typedef struct { uint32_t 유형, 설정비트; uint64_t 변위, 주소, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(사용자실행틀) == 272, "exception assembly layout");
static int 포함된범위(uint64_t 변위, uint64_t 크기, uint64_t 끝위치) {
    return 변위 <= 끝위치 && 크기 <= 끝위치 - 변위;
}
static int 부가정보검사(const unsigned char *자료위치, size_t 크기) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, 크기)) {
        uint32_t 낱말들[3]; memcpy(낱말들, 자료위치 + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, 크기) || !포함된범위(현재위치 + 이름영역크기, 설명크기, 크기)) return 0;
        const unsigned char Nome[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Nome) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Nome); 순번++) if (자료위치[현재위치 + 순번] != Nome[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, 자료위치 + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *자료, size_t 크기, int 리눅스방식) {
    if (크기 < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, 자료, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.유형 != 2 || 실행머리.기계유형 != 183 || 실행머리.판번호 != 1 || 실행머리.설정비트 || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.프로그램머리항목크기 != sizeof(실행파일구획) || !실행머리.프로그램머리개수 || 실행머리.프로그램머리개수 > 16 ||
        실행머리.프로그램머리변위 < sizeof(실행머리) || !포함된범위(실행머리.프로그램머리변위, (uint64_t)실행머리.프로그램머리개수 * sizeof(실행파일구획), 크기)) return 사용자실행파일오류;
    uint8_t 사용량[(사용자영상끝 - 사용자바탕) / 쪽크기] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.프로그램머리개수; 순번++) {
        실행파일구획 자료위치; memcpy(&자료위치, 자료 + 실행머리.프로그램머리변위 + 순번 * sizeof(자료위치), sizeof(자료위치));
        if (자료위치.유형 == 4) {
            if (!포함된범위(자료위치.변위, 자료위치.파일영역크기, 크기)) return 사용자실행파일오류;
            if (부가정보검사(자료 + 자료위치.변위, 자료위치.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (자료위치.유형 == 0 || 자료위치.유형 == 6 || (자료위치.유형 == 0x6474e551 && !(자료위치.설정비트 & 1))) continue;
        if (자료위치.유형 != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!자료위치.기억영역크기) continue;
        if (자료위치.설정비트 & ~7u || !(자료위치.설정비트 & 4) || (자료위치.설정비트 & 3) == 3 || 자료위치.파일영역크기 > 자료위치.기억영역크기 ||
            (자료위치.파일영역크기 && !포함된범위(자료위치.변위, 자료위치.파일영역크기, 크기)) || 자료위치.주소 < 사용자바탕 ||
            !포함된범위(자료위치.주소, 자료위치.기억영역크기, 사용자영상끝) ||
            (!리눅스방식 && ((자료위치.주소 & (쪽크기 - 1)) || (자료위치.변위 & (쪽크기 - 1)) || 자료위치.맞춤 != 쪽크기)) ||
            (리눅스방식 && (((자료위치.주소 ^ 자료위치.변위) & (쪽크기 - 1)) || !자료위치.맞춤 ||
                (자료위치.맞춤 & (자료위치.맞춤 - 1)) || 자료위치.맞춤 > 0x200000 || ((자료위치.주소 ^ 자료위치.변위) & (자료위치.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (자료위치.주소 - 사용자바탕) / 쪽크기;
        unsigned 항목수 = ((자료위치.주소 & (쪽크기 - 1)) + 자료위치.기억영역크기 + 쪽크기 - 1) / 쪽크기;
        for (unsigned 쪽 = 첫항목; 쪽 < 첫항목 + 항목수; 쪽++) {
            if (사용량[쪽]) return 사용자실행파일오류;
            사용량[쪽] = 1;
        }
        if ((자료위치.설정비트 & 1) && 실행머리.진입점 >= 자료위치.주소 && 실행머리.진입점 < 자료위치.주소 + 자료위치.파일영역크기 && !(실행머리.진입점 & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *자료, size_t 크기) { return 실행파일검사(자료, 크기, 0); }
static void 쪽배치(uintptr_t 주소, uint64_t 설정비트, unsigned 접근권한) {
    unsigned 색인 = (주소 - 사용자바탕) / 쪽크기;
    쪽목록[색인] = 주소 | 설정비트;
    권한목록[색인] = 접근권한;
}
static int 사용자범위(uintptr_t 주소, size_t 항목수, int 쓰는중) {
    if (주소 < 사용자바탕 || !포함된범위(주소, 항목수, 사용자끝)) return 0;
    if (!항목수) return 1;
    unsigned 첫항목 = (주소 - 사용자바탕) / 쪽크기, 마지막 = (주소 + 항목수 - 1 - 사용자바탕) / 쪽크기;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(권한목록[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int 경로복사(uintptr_t 주소, char *경로) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(주소, 1, 0)) return -14;
        경로[순번] = *(const char *)주소++;
        if (!경로[순번]) return 0;
    }
    return -36;
}
static intptr_t 커널결과(intptr_t 결과) { return 결과 < 0 ? -오류번호 : 결과; }
static int 대응파일기술자(uint64_t 파일기술자) { return 파일기술자 >= 3 && 파일기술자 < 19 ? 파일목록[파일기술자 - 3] : -1; }
static int 통신끝점소유(uint64_t 파일기술자) { return 파일기술자 >= 32 && 파일기술자 < 56 && 통신끝점들[파일기술자 - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t 길이, struct pk_sockaddr_in *주소) {
    if (길이 != sizeof(*주소)) return -22;
    if (!사용자범위(가리킴값, 길이, 0)) return -14;
    memcpy(주소, (const void *)가리킴값, sizeof(*주소));
    return 주소->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t 길이포인터, pk_socklen_t *수용량) {
    if (!사용자범위(길이포인터, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)길이포인터, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t 길이포인터, pk_socklen_t 수용량, int 주소, int 접속번호) {
    struct pk_sockaddr_in 값; memset(&값, 0, sizeof(값));
    값.sin_family = AF_INET; 값.sin_port = pk_htons(접속번호); 값.sin_addr.s_addr = pk_htonl(주소);
    if (수용량) memcpy((void *)가리킴값, &값, 수용량);
    pk_socklen_t 길이 = sizeof(값); memcpy((void *)길이포인터, &길이, sizeof(길이));
}
extern uintptr_t 보드통로(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(사용자실행틀 *파일항목) {
    uintptr_t 첫째값 = 파일항목->저장기값[0], 둘째값 = 파일항목->저장기값[1], 문자값 = 파일항목->저장기값[2];
    char 경로[65];
    int 파일기술자, 결과;
    switch (파일항목->저장기값[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: 포인터 전체를 검사한 뒤 출력/파일 변경
        if (문자값 > 65536) return -22;
        if (!사용자범위(둘째값, 문자값, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=시계값();
            for (size_t 순번 = 0; 순번 < 문자값; 순번++) 보드통로(첫째값, ((const unsigned char *)둘째값)[순번]);
            /* 큰 tty를 그린 커널 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(대화형){
                마감시각+=시계값()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return 문자값;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t 개수=문자값>512?512:문자값;for(size_t 순번=0;순번<개수;순번++)자바전문넣기(순번,((const unsigned char *)둘째값)[순번]);return 자바흐름쓰기(첫째값,개수);
        }
        파일기술자 = 대응파일기술자(첫째값); if (파일기술자 < 0) return -9;
        return 커널결과(pk_write(파일기술자, (const void *)둘째값, 문자값));
    case 2:
        if (문자값 > 65536) return -22;
        if (!사용자범위(둘째값, 문자값, 1)) return -14;
        if (첫째값 == 0) {
            size_t 개수 = 0;
            while (개수 < 문자값) {
                int 글자 = (int32_t)보드글자읽기(); if (글자 == -2) return 개수; if (글자 < 0) break;
                ((unsigned char *)둘째값)[개수++] = 글자;
            }
            return 개수 ? (intptr_t)개수 : (문자값 ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            결과=자바흐름읽기(첫째값,문자값>512?512:문자값);if(결과>0)for(int 순번=0;순번<결과;순번++)((unsigned char *)둘째값)[순번]=자바전문얻기(순번);return 결과;
        }
        파일기술자 = 대응파일기술자(첫째값); if (파일기술자 < 0) return -9;
        return 커널결과(pk_read(파일기술자, (void *)둘째값, 문자값));
    case 3:
        결과 = 경로복사(첫째값, 경로); if (결과) return 결과;
        if (둘째값 > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (파일목록[순번] < 0) {
            파일기술자 = pk_open(경로, (int)둘째값, 0600);
            if (파일기술자 < 0) return -오류번호;
            파일목록[순번] = 파일기술자; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { 결과 = 통신끝점닫기(첫째값); if (!결과) 통신끝점들[첫째값 - 32] = 0; return 결과; }
        파일기술자 = 대응파일기술자(첫째값); if (파일기술자 < 0) return -9;
        결과 = pk_close(파일기술자); if (!결과) 파일목록[첫째값 - 3] = -1;
        return 커널결과(결과);
    case 5:
        파일기술자 = 대응파일기술자(첫째값); if (파일기술자 < 0) return -9;
        if (문자값 > 2) return -22;
        return 커널결과(pk_lseek(파일기술자, (int64_t)둘째값, 문자값));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 사용자 RW/NX 힙, 새로 노출되는 페이지는 0으로 초기화
        if (!첫째값) return 동적기억끝;
        if (첫째값 < 사용자영상끝 || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + 쪽크기 - 1) & ~(쪽크기 - 1);
        uintptr_t 새쪽들 = (첫째값 + 쪽크기 - 1) & ~(쪽크기 - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t 자료위치 = 이전쪽들; 자료위치 < 새쪽들; 자료위치 += 쪽크기) 쪽배치(자료위치, 커널쪽, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t 자료위치 = 이전쪽들; 자료위치 < 새쪽들; 자료위치 += 쪽크기) 쪽배치(자료위치, 사용자읽고쓰기, 3);
        } else {
            for (uintptr_t 자료위치 = 새쪽들; 자료위치 < 이전쪽들; 자료위치 += 쪽크기) {
                쪽목록[(자료위치 - 사용자바탕) / 쪽크기] = 0; 권한목록[(자료위치 - 사용자바탕) / 쪽크기] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        파일기술자 = 대응파일기술자(첫째값); return 파일기술자 < 0 ? -9 : 커널결과(pk_size(파일기술자));
    case 10:
        파일기술자 = 대응파일기술자(첫째값); return 파일기술자 < 0 ? -9 : 커널결과(pk_ftruncate(파일기술자, (int64_t)둘째값));
    case 11:
        결과 = 경로복사(첫째값, 경로); return 결과 ? 결과 : 커널결과(pk_unlink(경로));
    case 12:
        파일기술자 = 대응파일기술자(첫째값); return 파일기술자 < 0 ? -9 : 커널결과(pk_fsync(파일기술자));
    case 13: { // 그래픽 기초 API: 사용자 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = 파일항목->저장기값[3], 높이값 = 파일항목->저장기값[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || 둘째값 > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - 둘째값) return -22;
        for (uintptr_t 세로좌표 = 둘째값; 세로좌표 < 둘째값 + 높이값; 세로좌표++) for (uintptr_t 가로좌표 = 첫째값; 가로좌표 < 첫째값 + 너비값; 가로좌표++) 보드화소(가로좌표, 세로좌표, 문자값);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=개수; args(index,buffer,capacity)=UTF-8 길이
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (문자값 <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(둘째값, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)둘째값, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;대화형=1;return 보드터미널(13);}
        if(첫째값==2){대화형=0;return 0;}
        if(첫째값==3)return 보드터미널(13);
        if(첫째값!=1||!대화형)return -22;
        결과=(int32_t)보드글자읽기();
        if(결과==-4096)return 결과;
        시간제한시작();return 결과<0?-11:결과;
    case 17: { // 유한한 협력 대기: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t 끝시각 = 시계값() + 진동수 * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (시계값() < 끝시각);
        시간제한시작(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (둘째값 > 2) return -22;
        결과 = 경로복사(첫째값, 경로); if (결과) return 결과;
        unsigned 길이 = 0; while (경로[길이]) 길이++;
        결과 = 자바경로시작(길이); if (결과 < 0) return 결과;
        for (unsigned 순번 = 0; 순번 < 길이; 순번++) 자바경로바이트(순번, (unsigned char)경로[순번]);
        return 둘째값 == 0 ? 자바항목종류() : 둘째값 == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int 글자=(int32_t)보드글자읽기();if(글자==-4096)return 글자;if(글자>=0)화면누름(소유자,글자);시간제한시작();}
        if(첫째값==3&&문자값){if(!자바셸대화형())return -95;대화형=1;보드터미널(300);}
        return 화면호출(소유자,첫째값,둘째값,문자값,파일항목->저장기값[3],파일항목->저장기값[4],파일항목->저장기값[5]);
    case 21:
        if(문자값>127)return -22;if(!사용자범위(둘째값,문자값*sizeof(uint32_t),0))return -14;
        return 화면글(소유자,첫째값,(const uint32_t *)둘째값,문자값);
    case 22: // 화면 크기 조회: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(둘째값==SOCK_STREAM&&(문자값==0||문자값==6))결과=자바흐름만들기();
        else if(둘째값==SOCK_DGRAM&&(문자값==0||문자값==IPPROTO_UDP))결과=자바전문만들기(첫째값,둘째값,문자값);
        else return -93;
        if (결과 >= 32 && 결과 < 56) 통신끝점들[결과 - 32] = 1;
        return 결과;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in 주소;
        결과 = 주소입력(둘째값, 문자값, &주소); if (결과) return 결과;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(주소.sin_addr.s_addr),pk_htons(주소.sin_port)):자바전문묶기(첫째값, pk_htonl(주소.sin_addr.s_addr), pk_htons(주소.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (파일항목->저장기값[3]) return -95;
        if (문자값 > 512) return -90;
        if (문자값 && !사용자범위(둘째값, 문자값, 0)) return -14;
        struct pk_sockaddr_in 주소;
        결과 = 주소입력(파일항목->저장기값[4], 파일항목->저장기값[5], &주소); if (결과) return 결과;
        for (unsigned 순번 = 0; 순번 < 문자값; 순번++) 자바전문넣기(순번, ((const unsigned char *)둘째값)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(주소.sin_addr.s_addr), pk_htons(주소.sin_port), 문자값);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (파일항목->저장기값[3]) return -95;
        if (문자값 > 512) return -90;
        if (문자값 && !사용자범위(둘째값, 문자값, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (파일항목->저장기값[4]) { 결과 = 주소출력검사(파일항목->저장기값[4], 파일항목->저장기값[5], &수용량); if (결과) return 결과; }
        결과 = 자바전문받기(첫째값, 문자값); if (결과 < 0) return 결과;
        for (int 순번 = 0; 순번 < 결과; 순번++) ((unsigned char *)둘째값)[순번] = 자바전문얻기(순번);
        if (파일항목->저장기값[4]) 주소출력(파일항목->저장기값[4], 파일항목->저장기값[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return 결과;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        결과 = 주소출력검사(둘째값, 문자값, &수용량); if (결과) return 결과;
        주소출력(둘째값,문자값,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in 주소;
        결과=주소입력(둘째값,문자값,&주소);if(결과)return 결과;
        return 자바흐름연결(첫째값,pk_htonl(주소.sin_addr.s_addr),pk_htons(주소.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,둘째값):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(둘째값||문자값)return -95;결과=자바흐름연결받기(첫째값);if(결과>=40&&결과<56)통신끝점들[결과-32]=1;return 결과;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(사용자실행틀 *파일항목) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(파일항목) : 자체체계호출(파일항목);
}
static void 커널돌아가기(사용자실행틀 *파일항목, int 결과) {
    시간제한멈춤();
    파일항목->저장기값[0] = (uint64_t)(int64_t)결과;
    파일항목->명령위치 = (uintptr_t)사용자복귀;
    파일항목->상태값 = 0x3c5; // EL1h, DAIF masked
}
int 사용자예외(사용자실행틀 *파일항목, unsigned 가로채기) {
    if (!활성 || (파일항목->상태값 & 15) != 0) return 0;
    if (가로채기) {
        uint32_t 승인값 = 기계저장기(가로채기중앙처리기 + 0xc), 식별자 = 승인값 & 1023;
        if (식별자 == 30) { 커널돌아가기(파일항목, 사용자시간초과); 기계저장기(가로채기중앙처리기 + 0x10) = 승인값; return 1; }
        if (식별자 < 1020) 기계저장기(가로채기중앙처리기 + 0x10) = 승인값;
        return 1;
    }
    uint64_t 예외상태; __asm__ volatile("mrs %0, esr_el1" : "=r"(예외상태));
    if (시계값() >= 마감시각) { 커널돌아가기(파일항목, 사용자시간초과); return 1; }
    unsigned 예외분류 = 예외상태 >> 26;
    if (예외분류 == 0x15 && (예외상태 & 0xffff) == 0) {
        if (리눅스규약 ? 파일항목->저장기값[8] == 93 || 파일항목->저장기값[8] == 94 : 파일항목->저장기값[8] == 6) 커널돌아가기(파일항목, (int)(파일항목->저장기값[0] & 255));
        else {
            intptr_t 결과=체계호출(파일항목);
            if(결과==-4096&&대화형){
                저장값[소유자].실행틀=*파일항목;저장값[소유자].실행틀.명령위치-=4;
                사용자실수보관(저장값[소유자].실수저장상태);커널돌아가기(파일항목,사용자중단됨);
            }else 파일항목->저장기값[0]=(uint64_t)결과;
        }
    } else 커널돌아가기(파일항목, 예외분류 == 0x24 ? 사용자자료오류 : 예외분류 == 0x20 ? 사용자실행오류 : 사용자잘못된명령);
    return 1;
}

// 생성된 const ELF 묶음: 실행은 반드시 프로그램 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *자료; size_t 크기; unsigned 전달값; } 실행항목;
#include "programs.h"
static void *상태갈무리(unsigned 자리){return (void *)(0x04000000ul+자리*(사용자끝-사용자바탕));}
static int 프로그램마치기(int 결과){
    사용자누적시각[소유자]+=(uint32_t)보드밀리초()-사용자실행시각[소유자];
    시간제한멈춤();활성=0;
    if(결과==사용자중단됨){
        저장된작업 *문자열값=&저장값[소유자];문자열값->멈춤상태=1;문자열값->대화형=대화형;문자열값->리눅스규약=리눅스규약;문자열값->동적기억공간=동적기억끝;문자열값->인수개수=전달인수개수;
        memcpy(문자열값->권한목록,권한목록,sizeof(권한목록));memcpy(문자열값->파일목록,파일목록,sizeof(파일목록));memcpy(문자열값->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(문자열값->인수배열,전달인수,sizeof(전달인수));memcpy(문자열값->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<사용자쪽수;순번++)if(권한목록[순번])memcpy((unsigned char *)상태갈무리(소유자)+순번*쪽크기,(void *)(사용자바탕+순번*쪽크기),쪽크기);
    }else{
        저장값[소유자].멈춤상태=0;화면초기화(소유자);
        for(unsigned 순번=0;순번<16;순번++)if(파일목록[순번]>=0)pk_close(파일목록[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<사용자쪽수;순번++){쪽목록[순번]=0;권한목록[순번]=0;}변환표맞추기();return 결과;
}
uintptr_t 보드사용자제어(uintptr_t 동작){
    unsigned 자리=동작&15;if(자리>=4||활성)return (uint32_t)-22;
    저장된작업 *문자열값=&저장값[자리];
    if(동작>=32){if(문자열값->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(문자열값->파일목록[순번]>=0)pk_close(문자열값->파일목록[순번]);for(unsigned 순번=0;순번<24;순번++)if(문자열값->통신끝점들[순번])통신끝점닫기(순번+32);}문자열값->멈춤상태=0;화면초기화(자리);return 0;}
    if(동작>=16)return 문자열값->멈춤상태;
    if(!문자열값->멈춤상태)return (uint32_t)-22;
    소유자=자리;대화형=문자열값->대화형;리눅스규약=문자열값->리눅스규약;동적기억끝=문자열값->동적기억공간;전달인수개수=문자열값->인수개수;
    memcpy(파일목록,문자열값->파일목록,sizeof(파일목록));memcpy(통신끝점들,문자열값->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,문자열값->인수배열,sizeof(전달인수));memcpy(전달인수길이,문자열값->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<사용자쪽수;순번++)쪽목록[순번]=(사용자바탕+순번*쪽크기)|커널쪽;변환표맞추기();
    memset((void *)사용자바탕,0,사용자끝-사용자바탕);
    for(unsigned 순번=0;순번<사용자쪽수;순번++)if(문자열값->권한목록[순번])memcpy((void *)(사용자바탕+순번*쪽크기),(unsigned char *)상태갈무리(자리)+순번*쪽크기,쪽크기);
    memcpy(권한목록,문자열값->권한목록,sizeof(권한목록));
    for(unsigned 순번=0;순번<사용자쪽수;순번++){unsigned 자료위치=권한목록[순번];쪽목록[순번]=자료위치?(사용자바탕+순번*쪽크기)|(자료위치==3?사용자읽고쓰기:자료위치==5?사용자읽고실행:사용자읽기전용):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");활성=1;문자열값->멈춤상태=0;시간제한시작();
    사용자실행시각[소유자]=보드밀리초();
    return (uint32_t)프로그램마치기(사용자재개(&문자열값->실행틀,문자열값->실수저장상태));
}
static int 프로그램실행(const unsigned char *자료, size_t 크기, unsigned 전달값, int 리눅스방식, const char *Nome) {
    if (활성) return -16;
    소유자=보드터미널(11);if(소유자<0||소유자>3||저장값[소유자].멈춤상태)return -16;대화형=0;
    int 유효함 = 실행파일검사(자료, 크기, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned 이름자리=0;
    while (*Nome && 이름자리<31) 사용자명령이름[소유자][이름자리++]=(unsigned char)*Nome++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (이름자리) 사용자명령이름[소유자][이름자리++]=' ';
        for (unsigned 자리=0; 자리<전달인수길이[0]; 자리++) 사용자명령이름[소유자][이름자리++]=전달인수[0][자리];
    }
    사용자명령이름[소유자][이름자리]=0; 사용자번호[소유자]=다음사용자번호++;
    if (다음사용자번호>0x7fffffffu) 다음사용자번호=10;
    사용자시작시각[소유자]=보드밀리초(); 사용자누적시각[소유자]=0;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) 쪽목록[순번] = (사용자바탕 + 순번 * 쪽크기) | 커널쪽;
    변환표맞추기();
    memset((void *)사용자바탕, 0, 사용자끝 - 사용자바탕);
    memset(권한목록, 0, sizeof(권한목록));
    실행파일머리 실행머리; memcpy(&실행머리, 자료, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.프로그램머리개수; 순번++) {
        실행파일구획 자료위치; memcpy(&자료위치, 자료 + 실행머리.프로그램머리변위 + 순번 * sizeof(자료위치), sizeof(자료위치));
        if (자료위치.유형 != 1 || !자료위치.기억영역크기) continue;
        if (자료위치.파일영역크기) memcpy((void *)(uintptr_t)자료위치.주소, 자료 + 자료위치.변위, 자료위치.파일영역크기);
        for (uintptr_t 현재위치 = 자료위치.주소 & ~(쪽크기 - 1); 현재위치 < 자료위치.주소 + 자료위치.기억영역크기; 현재위치 += 쪽크기) {
            권한목록[(현재위치 - 사용자바탕) / 쪽크기] = (자료위치.설정비트 & 2) ? 3 : ((자료위치.설정비트 & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = 사용자쌓임주소; 현재위치 < 사용자끝; 현재위치 += 쪽크기) 권한목록[(현재위치 - 사용자바탕) / 쪽크기] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.진입점) : 사용자끝;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) {
        unsigned 접근권한 = 권한목록[순번];
        쪽목록[순번] = 접근권한 ? (사용자바탕 + 순번 * 쪽크기) | (접근권한 == 3 ? 사용자읽고쓰기 : 접근권한 == 5 ? 사용자읽고실행 : 사용자읽기전용) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) 파일목록[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = 사용자영상끝;
    활성 = 1; 시간제한시작();
    사용자실행시각[소유자]=보드밀리초();
    int 결과 = 사용자진입(실행머리.진입점, 초기쌓임공간, 전달값);
    return 프로그램마치기(결과);
}
uintptr_t 보드사용자실행(uintptr_t 색인) {
    if (색인 >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Nome=색인==10?"javac":색인==11?"java":색인==12?"python":색인==13?"vi":색인==14?"jar":색인==15?"cc":색인==16?"jaot":"ELF";
    return (uint32_t)프로그램실행(실행항목들[색인].자료, 실행항목들[색인].크기, 실행항목들[색인].전달값, 0, Nome);
}
static uintptr_t 파일실행(int 리눅스방식) {
    static unsigned char 실행영상[16384];
    if (활성 || !전달인수개수) return (uint32_t)-22;
    int 파일기술자 = pk_open((const char *)전달인수[0], 읽기전용, 0);
    if (파일기술자 < 0) return (uint32_t)-오류번호;
    int 크기 = pk_size(파일기술자);
    if (크기 < 0 || (unsigned)크기 > sizeof(실행영상)) { pk_close(파일기술자); return (uint32_t)-27; }
    int 받은수 = pk_read(파일기술자, 실행영상, 크기); pk_close(파일기술자);
    if (받은수 != 크기) return (uint32_t)-5;
    return (uint32_t)프로그램실행(실행영상, 크기, 0, 리눅스방식, "");
}
uintptr_t 보드사용자파일(void) { return 파일실행(0); }
uintptr_t 보드사용자리눅스파일(void) { return 파일실행(1); }
uintptr_t 보드사용자검사(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].자료, 잘못된실행항목들[순번].크기) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
