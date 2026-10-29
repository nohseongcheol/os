#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 tekeleza_amri mashine tabaka_thamani. faili data/정책은 기존 AOT Java 커널에 위임한다.
#include "mtumiaji.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Mtandao_Mpororo/Mtandao_Mpororo.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define mashine_sajili(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_msambazaji 0xff841000ul
#define IRQ_CPU_kiolesura 0xff842000ul
#define ukubwa_wa_ukurasa 4096ul
#define 접근표시 (1ul << 10)
#define hapana_tekeleza_kibali (1ul << 53)
#define mtumiaji_hapana_tekeleza (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define kiini_ukurasa (3ul | 보통기억 | hapana_tekeleza_kibali | mtumiaji_hapana_tekeleza)
#define mtumiaji_soma_andika (3ul | 보통기억 | (1ul << 6) | hapana_tekeleza_kibali | mtumiaji_hapana_tekeleza)
#define mtumiaji_soma_tu (3ul | 보통기억 | (3ul << 6) | hapana_tekeleza_kibali | mtumiaji_hapana_tekeleza)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | hapana_tekeleza_kibali)
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
extern int mtumiaji_CV(mtumiaji_fremu *,void *);
extern void 사용자실수보관(void *);
extern int mtumiaji_ingiza(uintptr_t ingizo_pointi, uintptr_t Mpororo_Hifadhi, uintptr_t 전달값);
extern void 사용자복귀(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t 뿌리주소[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t ukurasa_Orodha[사용자쪽수] __attribute__((aligned(4096)));
static uint8_t Vibali_Orodha[사용자쪽수];
static int Amilifu, faili_Orodha[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned faili_kishiko){return faili_kishiko<40?자바전문닫기(faili_kishiko):자바흐름닫기(faili_kishiko);}
static uint64_t 진동수, 마감시각;
static uintptr_t 동적기억끝;
// kiini_thamani_0611a8a8 셸이 준비한 UTF-8 인수. EL0에는 mfano_thamani 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,ingiliani,리눅스규약,faili_Orodha[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char hoja_ARRAY[8][256],Vibali_Orodha[사용자쪽수];
    uintptr_t 동적기억공간; mtumiaji_fremu 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int mmiliki_kipengee,ingiliani;
static uint32_t nambari_ya_mtumiaji[4], mtumiaji_Anza_saa[4], 사용자누적시각[4], 사용자실행시각[4], 다음사용자번호=10;
static unsigned char mtumiaji_amri_jina[4][288];
uint32_t 사용자상태읽기(unsigned ingizo_thamani, unsigned kielezo) {
    unsigned 자리=kielezo&3;
    int hali_thamani=(Amilifu && mmiliki_kipengee==(int)자리) ? 1 : 저장값[자리].멈춤상태 ? 2 : 0;
    if (ingizo_thamani==0) return hali_thamani;
    if (!hali_thamani) return 0;
    if (ingizo_thamani==1) return nambari_ya_mtumiaji[자리];
    if (ingizo_thamani==2) {
        unsigned char *쪽들=hali_thamani==1?Vibali_Orodha:저장값[자리].Vibali_Orodha;
        unsigned 쪽수=0; for (unsigned 순번=0; 순번<사용자쪽수; 순번++) if(쪽들[순번]) 쪽수++;
        return 쪽수*4;
    }
    if (ingizo_thamani==3) return (uint32_t)보드밀리초()-mtumiaji_Anza_saa[자리];
    if (ingizo_thamani==4) return 사용자누적시각[자리]+(hali_thamani==1?(uint32_t)보드밀리초()-사용자실행시각[자리]:0);
    if (ingizo_thamani==5) return kielezo/4<sizeof(mtumiaji_amri_jina[0])?mtumiaji_amri_jina[자리][kielezo/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t 항목수) {
    if (Amilifu || 항목수 > 8) return (uint32_t)-22;
    전달인수개수 = 항목수;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t 색인, uintptr_t 현재위치, uintptr_t baiti_data) {
    if (Amilifu || 색인 >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[색인] || !baiti_data || baiti_data > 255)
        return (uint32_t)-22;
    전달인수[색인][현재위치] = baiti_data;
    전달인수길이[색인] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t saa_thamani(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void 시간제한멈춤(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    mashine_sajili(IRQ_msambazaji + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void 시간제한시작(void) {
    uint64_t 간격 = 진동수 * 2, washa = 1;
    마감시각 = saa_thamani() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(washa) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned data_zuia = 0; data_zuia < 4; data_zuia++) {
        뿌리주소[data_zuia] = (uintptr_t)가운데[data_zuia] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t anwani = ((uintptr_t)data_zuia << 30) | ((uintptr_t)순번 << 21);
            가운데[data_zuia][순번] = anwani | 1 | 접근표시 | mtumiaji_hapana_tekeleza;
            if (anwani >= 0xfc000000ul) 가운데[data_zuia][순번] |= hapana_tekeleza_kibali; // Device-nGnRnE
            else 가운데[data_zuia][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned 둘째값 = 0; 둘째값 < 사용자쪽수 / 512; 둘째값++)
        가운데[0][(사용자바탕 >> 21) + 둘째값] = (uintptr_t)(ukurasa_Orodha + 둘째값 * 512) | 3;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) ukurasa_Orodha[순번] = (사용자바탕 + 순번 * ukubwa_wa_ukurasa) | kiini_ukurasa;
    uint64_t kumbukumbu_sifa_sajili = 0x4400, anwani_Tafsiri_udhibiti = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(kumbukumbu_sifa_sajili), "r"(anwani_Tafsiri_udhibiti), "r"((uintptr_t)뿌리주소) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(진동수));
    시간제한멈춤();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 ingizo_pointi_thamani 때만 Ruhusu_thamani.
    mashine_sajili(IRQ_msambazaji) = 0;
    mashine_sajili(IRQ_msambazaji + 0x180) = 0xffffffff;
    mashine_sajili(IRQ_msambazaji + 0x80) = 0xffffffff;
    mashine_sajili(IRQ_msambazaji + 0x280) = 1u << 30;
    mashine_sajili(IRQ_msambazaji + 0x41c) = 0x80808080;
    mashine_sajili(IRQ_msambazaji + 0x100) = 1u << 30;
    mashine_sajili(IRQ_CPU_kiolesura + 4) = 0xff;
    mashine_sajili(IRQ_CPU_kiolesura + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Usalama = (mashine_sajili(IRQ_msambazaji + 4) & (1u << 10)) != 0;
    mashine_sajili(IRQ_msambazaji) = Usalama ? 1 : 3;
    mashine_sajili(IRQ_CPU_kiolesura) = Usalama ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t aina_kategoria, mashine_aina; uint32_t 판번호;
    uint64_t ingizo_pointi, programu_kichwa_Chipua, sehemu_kichwa_Chipua; uint32_t usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma;
    uint16_t 실행머리크기, programu_kichwa_ingizo_panga_ukubwa, 프로그램머리개수, sehemu_kichwa_ingizo_panga_ukubwa, 구역머리개수, sehemu_jina_jedwali_kielezo;
} 실행파일머리;
typedef struct { uint32_t aina_kategoria, usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma; uint64_t Chipua_thamani, anwani, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(mtumiaji_fremu) == 272, "exception assembly layout");
static int 포함된범위(uint64_t Chipua_thamani, uint64_t panga_ukubwa, uint64_t tamatia_Chipua) {
    return Chipua_thamani <= tamatia_Chipua && panga_ukubwa <= tamatia_Chipua - Chipua_thamani;
}
static int 부가정보검사(const unsigned char *자료위치, size_t panga_ukubwa) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, panga_ukubwa)) {
        uint32_t 낱말들[3]; memcpy(낱말들, 자료위치 + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, panga_ukubwa) || !포함된범위(현재위치 + 이름영역크기, 설명크기, panga_ukubwa)) return 0;
        const unsigned char Jina[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Jina) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Jina); 순번++) if (자료위치[현재위치 + 순번] != Jina[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, 자료위치 + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *data, size_t panga_ukubwa, int 리눅스방식) {
    if (panga_ukubwa < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, data, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.aina_kategoria != 2 || 실행머리.mashine_aina != 183 || 실행머리.판번호 != 1 || 실행머리.usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.programu_kichwa_ingizo_panga_ukubwa != sizeof(실행파일구획) || !실행머리.프로그램머리개수 || 실행머리.프로그램머리개수 > 16 ||
        실행머리.programu_kichwa_Chipua < sizeof(실행머리) || !포함된범위(실행머리.programu_kichwa_Chipua, (uint64_t)실행머리.프로그램머리개수 * sizeof(실행파일구획), panga_ukubwa)) return 사용자실행파일오류;
    uint8_t 사용량[(mtumiaji_picha_tamatia - 사용자바탕) / ukubwa_wa_ukurasa] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.프로그램머리개수; 순번++) {
        실행파일구획 자료위치; memcpy(&자료위치, data + 실행머리.programu_kichwa_Chipua + 순번 * sizeof(자료위치), sizeof(자료위치));
        if (자료위치.aina_kategoria == 4) {
            if (!포함된범위(자료위치.Chipua_thamani, 자료위치.파일영역크기, panga_ukubwa)) return 사용자실행파일오류;
            if (부가정보검사(data + 자료위치.Chipua_thamani, 자료위치.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (자료위치.aina_kategoria == 0 || 자료위치.aina_kategoria == 6 || (자료위치.aina_kategoria == 0x6474e551 && !(자료위치.usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma & 1))) continue;
        if (자료위치.aina_kategoria != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!자료위치.기억영역크기) continue;
        if (자료위치.usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma & ~7u || !(자료위치.usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma & 4) || (자료위치.usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma & 3) == 3 || 자료위치.파일영역크기 > 자료위치.기억영역크기 ||
            (자료위치.파일영역크기 && !포함된범위(자료위치.Chipua_thamani, 자료위치.파일영역크기, panga_ukubwa)) || 자료위치.anwani < 사용자바탕 ||
            !포함된범위(자료위치.anwani, 자료위치.기억영역크기, mtumiaji_picha_tamatia) ||
            (!리눅스방식 && ((자료위치.anwani & (ukubwa_wa_ukurasa - 1)) || (자료위치.Chipua_thamani & (ukubwa_wa_ukurasa - 1)) || 자료위치.맞춤 != ukubwa_wa_ukurasa)) ||
            (리눅스방식 && (((자료위치.anwani ^ 자료위치.Chipua_thamani) & (ukubwa_wa_ukurasa - 1)) || !자료위치.맞춤 ||
                (자료위치.맞춤 & (자료위치.맞춤 - 1)) || 자료위치.맞춤 > 0x200000 || ((자료위치.anwani ^ 자료위치.Chipua_thamani) & (자료위치.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (자료위치.anwani - 사용자바탕) / ukubwa_wa_ukurasa;
        unsigned 항목수 = ((자료위치.anwani & (ukubwa_wa_ukurasa - 1)) + 자료위치.기억영역크기 + ukubwa_wa_ukurasa - 1) / ukubwa_wa_ukurasa;
        for (unsigned ukurasa_thamani = 첫항목; ukurasa_thamani < 첫항목 + 항목수; ukurasa_thamani++) {
            if (사용량[ukurasa_thamani]) return 사용자실행파일오류;
            사용량[ukurasa_thamani] = 1;
        }
        if ((자료위치.usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma & 1) && 실행머리.ingizo_pointi >= 자료위치.anwani && 실행머리.ingizo_pointi < 자료위치.anwani + 자료위치.파일영역크기 && !(실행머리.ingizo_pointi & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *data, size_t panga_ukubwa) { return 실행파일검사(data, panga_ukubwa, 0); }
static void mpangilio_wa_ukurasa(uintptr_t anwani, uint64_t usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma, unsigned vibali) {
    unsigned 색인 = (anwani - 사용자바탕) / ukubwa_wa_ukurasa;
    ukurasa_Orodha[색인] = anwani | usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma;
    Vibali_Orodha[색인] = vibali;
}
static int 사용자범위(uintptr_t anwani, size_t 항목수, int 쓰는중) {
    if (anwani < 사용자바탕 || !포함된범위(anwani, 항목수, mtumiaji_tamatia)) return 0;
    if (!항목수) return 1;
    unsigned 첫항목 = (anwani - 사용자바탕) / ukubwa_wa_ukurasa, 마지막 = (anwani + 항목수 - 1 - 사용자바탕) / ukubwa_wa_ukurasa;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Vibali_Orodha[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int mfano_njia(uintptr_t anwani, char *njia) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(anwani, 1, 0)) return -14;
        njia[순번] = *(const char *)anwani++;
        if (!njia[순번]) return 0;
    }
    return -36;
}
static intptr_t 커널결과(intptr_t 결과) { return 결과 < 0 ? -오류번호 : 결과; }
static int 대응파일기술자(uint64_t faili_kishiko) { return faili_kishiko >= 3 && faili_kishiko < 19 ? faili_Orodha[faili_kishiko - 3] : -1; }
static int 통신끝점소유(uint64_t faili_kishiko) { return faili_kishiko >= 32 && faili_kishiko < 56 && 통신끝점들[faili_kishiko - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t urefu_thamani, struct pk_sockaddr_in *anwani) {
    if (urefu_thamani != sizeof(*anwani)) return -22;
    if (!사용자범위(가리킴값, urefu_thamani, 0)) return -14;
    memcpy(anwani, (const void *)가리킴값, sizeof(*anwani));
    return anwani->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t urefu_kielekezi, pk_socklen_t *수용량) {
    if (!사용자범위(urefu_kielekezi, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)urefu_kielekezi, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t urefu_kielekezi, pk_socklen_t 수용량, int anwani, int namba_ya_kituo) {
    struct pk_sockaddr_in thamani; memset(&thamani, 0, sizeof(thamani));
    thamani.sin_family = AF_INET; thamani.sin_port = pk_htons(namba_ya_kituo); thamani.sin_addr.s_addr = pk_htonl(anwani);
    if (수용량) memcpy((void *)가리킴값, &thamani, 수용량);
    pk_socklen_t urefu_thamani = sizeof(thamani); memcpy((void *)urefu_kielekezi, &urefu_thamani, sizeof(urefu_thamani));
}
extern uintptr_t 보드통로(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(mtumiaji_fremu *faili_ingizo) {
    uintptr_t 첫째값 = faili_ingizo->sajili_data[0], 둘째값 = faili_ingizo->sajili_data[1], msimbo_wa_kibambo = faili_ingizo->sajili_data[2];
    char njia[65];
    int faili_kishiko, 결과;
    switch (faili_ingizo->sajili_data[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: kielekezi 전체를 검사한 Nyuma_thamani 출력/faili badilisha_thamani_16f64fe4
        if (msimbo_wa_kibambo > 65536) return -22;
        if (!사용자범위(둘째값, msimbo_wa_kibambo, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=saa_thamani();
            for (size_t 순번 = 0; 순번 < msimbo_wa_kibambo; 순번++) 보드통로(첫째값, ((const unsigned char *)둘째값)[순번]);
            /* 큰 tty를 그린 kiini_thamani_0611a8a8 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(ingiliani){
                마감시각+=saa_thamani()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return msimbo_wa_kibambo;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t 개수=msimbo_wa_kibambo>512?512:msimbo_wa_kibambo;for(size_t 순번=0;순번<개수;순번++)자바전문넣기(순번,((const unsigned char *)둘째값)[순번]);return 자바흐름쓰기(첫째값,개수);
        }
        faili_kishiko = 대응파일기술자(첫째값); if (faili_kishiko < 0) return -9;
        return 커널결과(pk_write(faili_kishiko, (const void *)둘째값, msimbo_wa_kibambo));
    case 2:
        if (msimbo_wa_kibambo > 65536) return -22;
        if (!사용자범위(둘째값, msimbo_wa_kibambo, 1)) return -14;
        if (첫째값 == 0) {
            size_t 개수 = 0;
            while (개수 < msimbo_wa_kibambo) {
                int kibambo_thamani = (int32_t)보드글자읽기(); if (kibambo_thamani == -2) return 개수; if (kibambo_thamani < 0) break;
                ((unsigned char *)둘째값)[개수++] = kibambo_thamani;
            }
            return 개수 ? (intptr_t)개수 : (msimbo_wa_kibambo ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            결과=자바흐름읽기(첫째값,msimbo_wa_kibambo>512?512:msimbo_wa_kibambo);if(결과>0)for(int 순번=0;순번<결과;순번++)((unsigned char *)둘째값)[순번]=자바전문얻기(순번);return 결과;
        }
        faili_kishiko = 대응파일기술자(첫째값); if (faili_kishiko < 0) return -9;
        return 커널결과(pk_read(faili_kishiko, (void *)둘째값, msimbo_wa_kibambo));
    case 3:
        결과 = mfano_njia(첫째값, njia); if (결과) return 결과;
        if (둘째값 > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (faili_Orodha[순번] < 0) {
            faili_kishiko = pk_open(njia, (int)둘째값, 0600);
            if (faili_kishiko < 0) return -오류번호;
            faili_Orodha[순번] = faili_kishiko; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { 결과 = 통신끝점닫기(첫째값); if (!결과) 통신끝점들[첫째값 - 32] = 0; return 결과; }
        faili_kishiko = 대응파일기술자(첫째값); if (faili_kishiko < 0) return -9;
        결과 = pk_close(faili_kishiko); if (!결과) faili_Orodha[첫째값 - 3] = -1;
        return 커널결과(결과);
    case 5:
        faili_kishiko = 대응파일기술자(첫째값); if (faili_kishiko < 0) return -9;
        if (msimbo_wa_kibambo > 2) return -22;
        return 커널결과(pk_lseek(faili_kishiko, (int64_t)둘째값, msimbo_wa_kibambo));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 mtumiaji RW/NX 힙, 새로 노출되는 페이지는 0으로 anzilisha
        if (!첫째값) return 동적기억끝;
        if (첫째값 < mtumiaji_picha_tamatia || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + ukubwa_wa_ukurasa - 1) & ~(ukubwa_wa_ukurasa - 1);
        uintptr_t 새쪽들 = (첫째값 + ukubwa_wa_ukurasa - 1) & ~(ukubwa_wa_ukurasa - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t 자료위치 = 이전쪽들; 자료위치 < 새쪽들; 자료위치 += ukubwa_wa_ukurasa) mpangilio_wa_ukurasa(자료위치, kiini_ukurasa, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t 자료위치 = 이전쪽들; 자료위치 < 새쪽들; 자료위치 += ukubwa_wa_ukurasa) mpangilio_wa_ukurasa(자료위치, mtumiaji_soma_andika, 3);
        } else {
            for (uintptr_t 자료위치 = 새쪽들; 자료위치 < 이전쪽들; 자료위치 += ukubwa_wa_ukurasa) {
                ukurasa_Orodha[(자료위치 - 사용자바탕) / ukubwa_wa_ukurasa] = 0; Vibali_Orodha[(자료위치 - 사용자바탕) / ukubwa_wa_ukurasa] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        faili_kishiko = 대응파일기술자(첫째값); return faili_kishiko < 0 ? -9 : 커널결과(pk_size(faili_kishiko));
    case 10:
        faili_kishiko = 대응파일기술자(첫째값); return faili_kishiko < 0 ? -9 : 커널결과(pk_ftruncate(faili_kishiko, (int64_t)둘째값));
    case 11:
        결과 = mfano_njia(첫째값, njia); return 결과 ? 결과 : 커널결과(pk_unlink(njia));
    case 12:
        faili_kishiko = 대응파일기술자(첫째값); return faili_kishiko < 0 ? -9 : 커널결과(pk_fsync(faili_kishiko));
    case 13: { // 그래픽 기초 API: mtumiaji 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = faili_ingizo->sajili_data[3], 높이값 = faili_ingizo->sajili_data[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || 둘째값 > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - 둘째값) return -22;
        for (uintptr_t Kitufe_cha_Y_kiratibu = 둘째값; Kitufe_cha_Y_kiratibu < 둘째값 + 높이값; Kitufe_cha_Y_kiratibu++) for (uintptr_t jira_x = 첫째값; jira_x < 첫째값 + 너비값; jira_x++) 보드화소(jira_x, Kitufe_cha_Y_kiratibu, msimbo_wa_kibambo);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=개수; args(index,buffer,capacity)=UTF-8 urefu_thamani
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (msimbo_wa_kibambo <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(둘째값, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)둘째값, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;ingiliani=1;return 보드터미널(13);}
        if(첫째값==2){ingiliani=0;return 0;}
        if(첫째값==3)return 보드터미널(13);
        if(첫째값!=1||!ingiliani)return -22;
        결과=(int32_t)보드글자읽기();
        if(결과==-4096)return 결과;
        시간제한시작();return 결과<0?-11:결과;
    case 17: { // 유한한 협력 subiri_thamani: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t tamatia_saa = saa_thamani() + 진동수 * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (saa_thamani() < tamatia_saa);
        시간제한시작(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (둘째값 > 2) return -22;
        결과 = mfano_njia(첫째값, njia); if (결과) return 결과;
        unsigned urefu_thamani = 0; while (njia[urefu_thamani]) urefu_thamani++;
        결과 = 자바경로시작(urefu_thamani); if (결과 < 0) return 결과;
        for (unsigned 순번 = 0; 순번 < urefu_thamani; 순번++) 자바경로바이트(순번, (unsigned char)njia[순번]);
        return 둘째값 == 0 ? 자바항목종류() : 둘째값 == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int kibambo_thamani=(int32_t)보드글자읽기();if(kibambo_thamani==-4096)return kibambo_thamani;if(kibambo_thamani>=0)화면누름(mmiliki_kipengee,kibambo_thamani);시간제한시작();}
        if(첫째값==3&&msimbo_wa_kibambo){if(!자바셸대화형())return -95;ingiliani=1;보드터미널(300);}
        return 화면호출(mmiliki_kipengee,첫째값,둘째값,msimbo_wa_kibambo,faili_ingizo->sajili_data[3],faili_ingizo->sajili_data[4],faili_ingizo->sajili_data[5]);
    case 21:
        if(msimbo_wa_kibambo>127)return -22;if(!사용자범위(둘째값,msimbo_wa_kibambo*sizeof(uint32_t),0))return -14;
        return 화면글(mmiliki_kipengee,첫째값,(const uint32_t *)둘째값,msimbo_wa_kibambo);
    case 22: // 화면 panga_ukubwa uliza_thamani: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(둘째값==SOCK_STREAM&&(msimbo_wa_kibambo==0||msimbo_wa_kibambo==6))결과=자바흐름만들기();
        else if(둘째값==SOCK_DGRAM&&(msimbo_wa_kibambo==0||msimbo_wa_kibambo==IPPROTO_UDP))결과=자바전문만들기(첫째값,둘째값,msimbo_wa_kibambo);
        else return -93;
        if (결과 >= 32 && 결과 < 56) 통신끝점들[결과 - 32] = 1;
        return 결과;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in anwani;
        결과 = 주소입력(둘째값, msimbo_wa_kibambo, &anwani); if (결과) return 결과;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(anwani.sin_addr.s_addr),pk_htons(anwani.sin_port)):자바전문묶기(첫째값, pk_htonl(anwani.sin_addr.s_addr), pk_htons(anwani.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (faili_ingizo->sajili_data[3]) return -95;
        if (msimbo_wa_kibambo > 512) return -90;
        if (msimbo_wa_kibambo && !사용자범위(둘째값, msimbo_wa_kibambo, 0)) return -14;
        struct pk_sockaddr_in anwani;
        결과 = 주소입력(faili_ingizo->sajili_data[4], faili_ingizo->sajili_data[5], &anwani); if (결과) return 결과;
        for (unsigned 순번 = 0; 순번 < msimbo_wa_kibambo; 순번++) 자바전문넣기(순번, ((const unsigned char *)둘째값)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(anwani.sin_addr.s_addr), pk_htons(anwani.sin_port), msimbo_wa_kibambo);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (faili_ingizo->sajili_data[3]) return -95;
        if (msimbo_wa_kibambo > 512) return -90;
        if (msimbo_wa_kibambo && !사용자범위(둘째값, msimbo_wa_kibambo, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (faili_ingizo->sajili_data[4]) { 결과 = 주소출력검사(faili_ingizo->sajili_data[4], faili_ingizo->sajili_data[5], &수용량); if (결과) return 결과; }
        결과 = 자바전문받기(첫째값, msimbo_wa_kibambo); if (결과 < 0) return 결과;
        for (int 순번 = 0; 순번 < 결과; 순번++) ((unsigned char *)둘째값)[순번] = 자바전문얻기(순번);
        if (faili_ingizo->sajili_data[4]) 주소출력(faili_ingizo->sajili_data[4], faili_ingizo->sajili_data[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return 결과;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        결과 = 주소출력검사(둘째값, msimbo_wa_kibambo, &수용량); if (결과) return 결과;
        주소출력(둘째값,msimbo_wa_kibambo,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in anwani;
        결과=주소입력(둘째값,msimbo_wa_kibambo,&anwani);if(결과)return 결과;
        return 자바흐름연결(첫째값,pk_htonl(anwani.sin_addr.s_addr),pk_htons(anwani.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,둘째값):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(둘째값||msimbo_wa_kibambo)return -95;결과=자바흐름연결받기(첫째값);if(결과>=40&&결과<56)통신끝점들[결과-32]=1;return 결과;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(mtumiaji_fremu *faili_ingizo) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(faili_ingizo) : 자체체계호출(faili_ingizo);
}
static void 커널돌아가기(mtumiaji_fremu *faili_ingizo, int 결과) {
    시간제한멈춤();
    faili_ingizo->sajili_data[0] = (uint64_t)(int64_t)결과;
    faili_ingizo->명령위치 = (uintptr_t)사용자복귀;
    faili_ingizo->hali_msimbo = 0x3c5; // EL1h, DAIF masked
}
int mtumiaji_vighairi(mtumiaji_fremu *faili_ingizo, unsigned 가로채기) {
    if (!Amilifu || (faili_ingizo->hali_msimbo & 15) != 0) return 0;
    if (가로채기) {
        uint32_t 승인값 = mashine_sajili(IRQ_CPU_kiolesura + 0xc), kitambulishi_thamani = 승인값 & 1023;
        if (kitambulishi_thamani == 30) { 커널돌아가기(faili_ingizo, 사용자시간초과); mashine_sajili(IRQ_CPU_kiolesura + 0x10) = 승인값; return 1; }
        if (kitambulishi_thamani < 1020) mashine_sajili(IRQ_CPU_kiolesura + 0x10) = 승인값;
        return 1;
    }
    uint64_t vighairi_hali; __asm__ volatile("mrs %0, esr_el1" : "=r"(vighairi_hali));
    if (saa_thamani() >= 마감시각) { 커널돌아가기(faili_ingizo, 사용자시간초과); return 1; }
    unsigned vighairi_kategoria = vighairi_hali >> 26;
    if (vighairi_kategoria == 0x15 && (vighairi_hali & 0xffff) == 0) {
        if (리눅스규약 ? faili_ingizo->sajili_data[8] == 93 || faili_ingizo->sajili_data[8] == 94 : faili_ingizo->sajili_data[8] == 6) 커널돌아가기(faili_ingizo, (int)(faili_ingizo->sajili_data[0] & 255));
        else {
            intptr_t 결과=체계호출(faili_ingizo);
            if(결과==-4096&&ingiliani){
                저장값[mmiliki_kipengee].실행틀=*faili_ingizo;저장값[mmiliki_kipengee].실행틀.명령위치-=4;
                사용자실수보관(저장값[mmiliki_kipengee].실수저장상태);커널돌아가기(faili_ingizo,사용자중단됨);
            }else faili_ingizo->sajili_data[0]=(uint64_t)결과;
        }
    } else 커널돌아가기(faili_ingizo, vighairi_kategoria == 0x24 ? mtumiaji_data_kosa : vighairi_kategoria == 0x20 ? 사용자실행오류 : mtumiaji_batili_agizo);
    return 1;
}

// 생성된 const ELF Kikundi_thamani: 실행은 반드시 programu_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *data; size_t panga_ukubwa; unsigned 전달값; } programu;
#include "programs.h"
static void *picha_f57035a1(unsigned 자리){return (void *)(0x04000000ul+자리*(mtumiaji_tamatia-사용자바탕));}
static int Maliza_programu(int 결과){
    사용자누적시각[mmiliki_kipengee]+=(uint32_t)보드밀리초()-사용자실행시각[mmiliki_kipengee];
    시간제한멈춤();Amilifu=0;
    if(결과==사용자중단됨){
        저장된작업 *tungo_data=&저장값[mmiliki_kipengee];tungo_data->멈춤상태=1;tungo_data->ingiliani=ingiliani;tungo_data->리눅스규약=리눅스규약;tungo_data->동적기억공간=동적기억끝;tungo_data->인수개수=전달인수개수;
        memcpy(tungo_data->Vibali_Orodha,Vibali_Orodha,sizeof(Vibali_Orodha));memcpy(tungo_data->faili_Orodha,faili_Orodha,sizeof(faili_Orodha));memcpy(tungo_data->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(tungo_data->hoja_ARRAY,전달인수,sizeof(전달인수));memcpy(tungo_data->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<사용자쪽수;순번++)if(Vibali_Orodha[순번])memcpy((unsigned char *)picha_f57035a1(mmiliki_kipengee)+순번*ukubwa_wa_ukurasa,(void *)(사용자바탕+순번*ukubwa_wa_ukurasa),ukubwa_wa_ukurasa);
    }else{
        저장값[mmiliki_kipengee].멈춤상태=0;화면초기화(mmiliki_kipengee);
        for(unsigned 순번=0;순번<16;순번++)if(faili_Orodha[순번]>=0)pk_close(faili_Orodha[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<사용자쪽수;순번++){ukurasa_Orodha[순번]=0;Vibali_Orodha[순번]=0;}변환표맞추기();return 결과;
}
uintptr_t 보드사용자제어(uintptr_t Kitendo){
    unsigned 자리=Kitendo&15;if(자리>=4||Amilifu)return (uint32_t)-22;
    저장된작업 *tungo_data=&저장값[자리];
    if(Kitendo>=32){if(tungo_data->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(tungo_data->faili_Orodha[순번]>=0)pk_close(tungo_data->faili_Orodha[순번]);for(unsigned 순번=0;순번<24;순번++)if(tungo_data->통신끝점들[순번])통신끝점닫기(순번+32);}tungo_data->멈춤상태=0;화면초기화(자리);return 0;}
    if(Kitendo>=16)return tungo_data->멈춤상태;
    if(!tungo_data->멈춤상태)return (uint32_t)-22;
    mmiliki_kipengee=자리;ingiliani=tungo_data->ingiliani;리눅스규약=tungo_data->리눅스규약;동적기억끝=tungo_data->동적기억공간;전달인수개수=tungo_data->인수개수;
    memcpy(faili_Orodha,tungo_data->faili_Orodha,sizeof(faili_Orodha));memcpy(통신끝점들,tungo_data->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,tungo_data->hoja_ARRAY,sizeof(전달인수));memcpy(전달인수길이,tungo_data->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<사용자쪽수;순번++)ukurasa_Orodha[순번]=(사용자바탕+순번*ukubwa_wa_ukurasa)|kiini_ukurasa;변환표맞추기();
    memset((void *)사용자바탕,0,mtumiaji_tamatia-사용자바탕);
    for(unsigned 순번=0;순번<사용자쪽수;순번++)if(tungo_data->Vibali_Orodha[순번])memcpy((void *)(사용자바탕+순번*ukubwa_wa_ukurasa),(unsigned char *)picha_f57035a1(자리)+순번*ukubwa_wa_ukurasa,ukubwa_wa_ukurasa);
    memcpy(Vibali_Orodha,tungo_data->Vibali_Orodha,sizeof(Vibali_Orodha));
    for(unsigned 순번=0;순번<사용자쪽수;순번++){unsigned 자료위치=Vibali_Orodha[순번];ukurasa_Orodha[순번]=자료위치?(사용자바탕+순번*ukubwa_wa_ukurasa)|(자료위치==3?mtumiaji_soma_andika:자료위치==5?사용자읽고실행:mtumiaji_soma_tu):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Amilifu=1;tungo_data->멈춤상태=0;시간제한시작();
    사용자실행시각[mmiliki_kipengee]=보드밀리초();
    return (uint32_t)Maliza_programu(mtumiaji_CV(&tungo_data->실행틀,tungo_data->실수저장상태));
}
static int endesha_programu(const unsigned char *data, size_t panga_ukubwa, unsigned 전달값, int 리눅스방식, const char *Jina) {
    if (Amilifu) return -16;
    mmiliki_kipengee=보드터미널(11);if(mmiliki_kipengee<0||mmiliki_kipengee>3||저장값[mmiliki_kipengee].멈춤상태)return -16;ingiliani=0;
    int 유효함 = 실행파일검사(data, panga_ukubwa, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned jina_kielezo=0;
    while (*Jina && jina_kielezo<31) mtumiaji_amri_jina[mmiliki_kipengee][jina_kielezo++]=(unsigned char)*Jina++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (jina_kielezo) mtumiaji_amri_jina[mmiliki_kipengee][jina_kielezo++]=' ';
        for (unsigned 자리=0; 자리<전달인수길이[0]; 자리++) mtumiaji_amri_jina[mmiliki_kipengee][jina_kielezo++]=전달인수[0][자리];
    }
    mtumiaji_amri_jina[mmiliki_kipengee][jina_kielezo]=0; nambari_ya_mtumiaji[mmiliki_kipengee]=다음사용자번호++;
    if (다음사용자번호>0x7fffffffu) 다음사용자번호=10;
    mtumiaji_Anza_saa[mmiliki_kipengee]=보드밀리초(); 사용자누적시각[mmiliki_kipengee]=0;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) ukurasa_Orodha[순번] = (사용자바탕 + 순번 * ukubwa_wa_ukurasa) | kiini_ukurasa;
    변환표맞추기();
    memset((void *)사용자바탕, 0, mtumiaji_tamatia - 사용자바탕);
    memset(Vibali_Orodha, 0, sizeof(Vibali_Orodha));
    실행파일머리 실행머리; memcpy(&실행머리, data, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.프로그램머리개수; 순번++) {
        실행파일구획 자료위치; memcpy(&자료위치, data + 실행머리.programu_kichwa_Chipua + 순번 * sizeof(자료위치), sizeof(자료위치));
        if (자료위치.aina_kategoria != 1 || !자료위치.기억영역크기) continue;
        if (자료위치.파일영역크기) memcpy((void *)(uintptr_t)자료위치.anwani, data + 자료위치.Chipua_thamani, 자료위치.파일영역크기);
        for (uintptr_t 현재위치 = 자료위치.anwani & ~(ukubwa_wa_ukurasa - 1); 현재위치 < 자료위치.anwani + 자료위치.기억영역크기; 현재위치 += ukubwa_wa_ukurasa) {
            Vibali_Orodha[(현재위치 - 사용자바탕) / ukubwa_wa_ukurasa] = (자료위치.usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma & 2) ? 3 : ((자료위치.usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = mtumiaji_Mpororo_anwani; 현재위치 < mtumiaji_tamatia; 현재위치 += ukubwa_wa_ukurasa) Vibali_Orodha[(현재위치 - 사용자바탕) / ukubwa_wa_ukurasa] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.ingizo_pointi) : mtumiaji_tamatia;
    for (unsigned 순번 = 0; 순번 < 사용자쪽수; 순번++) {
        unsigned vibali = Vibali_Orodha[순번];
        ukurasa_Orodha[순번] = vibali ? (사용자바탕 + 순번 * ukubwa_wa_ukurasa) | (vibali == 3 ? mtumiaji_soma_andika : vibali == 5 ? 사용자읽고실행 : mtumiaji_soma_tu) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) faili_Orodha[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = mtumiaji_picha_tamatia;
    Amilifu = 1; 시간제한시작();
    사용자실행시각[mmiliki_kipengee]=보드밀리초();
    int 결과 = mtumiaji_ingiza(실행머리.ingizo_pointi, 초기쌓임공간, 전달값);
    return Maliza_programu(결과);
}
uintptr_t 보드사용자실행(uintptr_t 색인) {
    if (색인 >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Jina=색인==10?"javac":색인==11?"java":색인==12?"python":색인==13?"vi":색인==14?"jar":색인==15?"cc":색인==16?"jaot":"ELF";
    return (uint32_t)endesha_programu(실행항목들[색인].data, 실행항목들[색인].panga_ukubwa, 실행항목들[색인].전달값, 0, Jina);
}
static uintptr_t tekeleza_faili(int 리눅스방식) {
    static unsigned char picha[16384];
    if (Amilifu || !전달인수개수) return (uint32_t)-22;
    int faili_kishiko = pk_open((const char *)전달인수[0], soma_tu_thamani, 0);
    if (faili_kishiko < 0) return (uint32_t)-오류번호;
    int panga_ukubwa = pk_size(faili_kishiko);
    if (panga_ukubwa < 0 || (unsigned)panga_ukubwa > sizeof(picha)) { pk_close(faili_kishiko); return (uint32_t)-27; }
    int 받은수 = pk_read(faili_kishiko, picha, panga_ukubwa); pk_close(faili_kishiko);
    if (받은수 != panga_ukubwa) return (uint32_t)-5;
    return (uint32_t)endesha_programu(picha, panga_ukubwa, 0, 리눅스방식, "");
}
uintptr_t 보드사용자파일(void) { return tekeleza_faili(0); }
uintptr_t 보드사용자리눅스파일(void) { return tekeleza_faili(1); }
uintptr_t 보드사용자검사(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].data, 잘못된실행항목들[순번].panga_ukubwa) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
