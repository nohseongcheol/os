#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 kawe_tono mīhini apa_uara. Kōnae raraunga/정책은 기존 AOT Java 커널에 위임한다.
#include "kaiwhakamahi.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../whatunga_Huinga/whatunga_Huinga.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define mīhini_rēhita(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define THK_kaihora 0xff841000ul
#define THK_PTM_atanga 0xff842000ul
#define rahinga_whārangi 4096ul
#define 접근표시 (1ul << 10)
#define 권한실행금지 (1ul << 53)
#define 사용자실행금지 (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define kākano_whārangi (3ul | 보통기억 | 권한실행금지 | 사용자실행금지)
#define 사용자읽고쓰기 (3ul | 보통기억 | (1ul << 6) | 권한실행금지 | 사용자실행금지)
#define kaiwhakamahi_pānui_anake (3ul | 보통기억 | (3ul << 6) | 권한실행금지 | 사용자실행금지)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | 권한실행금지)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t papa_pika(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t papa_Tauranga(uintptr_t);
extern int Tauranga_tārewa(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int kaiwhakamahi_TāT(kaiwhakamahi_tāpare *,void *);
extern void 사용자실수보관(void *);
extern int kaiwhakamahi_tāuru(uintptr_t tāurunga_ira, uintptr_t Huinga_Rokiroki, uintptr_t 전달값);
extern void 사용자복귀(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t pūtake_ADDRESS[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t whārangi_Rārangi[kaiwhakamahi_whārangi_COUNT] __attribute__((aligned(4096)));
static uint8_t whakaaetanga_Rārangi[kaiwhakamahi_whārangi_COUNT];
static int hohe, kōnae_Rārangi[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned kōnae_raweke){return kōnae_raweke<40?자바전문닫기(kōnae_raweke):자바흐름닫기(kōnae_raweke);}
static uint64_t FREQUENCY, 마감시각;
static uintptr_t 동적기억끝;
// kākano_uara_0611a8a8 셸이 준비한 UTF-8 인수. EL0에는 tārua_uara 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,pāhekoheko,리눅스규약,kōnae_Rārangi[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char tohenga_HUĀNGA[8][256],whakaaetanga_Rārangi[kaiwhakamahi_whārangi_COUNT];
    uintptr_t 동적기억공간; kaiwhakamahi_tāpare 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int kaipupuri_ahanoa,pāhekoheko;
static uint32_t tau_kaiwhakamahi[4], kaiwhakamahi_Start_TIME[4], 사용자누적시각[4], 사용자실행시각[4], Panuku_tau_kaiwhakamahi=10;
static unsigned char kaiwhakamahi_tono_ingoa[4][288];
uint32_t 사용자상태읽기(unsigned tāurunga_uara, unsigned INDEX) {
    unsigned tūranga_INDEX=INDEX&3;
    int tūnga_uara=(hohe && kaipupuri_ahanoa==(int)tūranga_INDEX) ? 1 : 저장값[tūranga_INDEX].멈춤상태 ? 2 : 0;
    if (tāurunga_uara==0) return tūnga_uara;
    if (!tūnga_uara) return 0;
    if (tāurunga_uara==1) return tau_kaiwhakamahi[tūranga_INDEX];
    if (tāurunga_uara==2) {
        unsigned char *쪽들=tūnga_uara==1?whakaaetanga_Rārangi:저장값[tūranga_INDEX].whakaaetanga_Rārangi;
        unsigned whārangi_COUNT=0; for (unsigned 순번=0; 순번<kaiwhakamahi_whārangi_COUNT; 순번++) if(쪽들[순번]) whārangi_COUNT++;
        return whārangi_COUNT*4;
    }
    if (tāurunga_uara==3) return (uint32_t)보드밀리초()-kaiwhakamahi_Start_TIME[tūranga_INDEX];
    if (tāurunga_uara==4) return 사용자누적시각[tūranga_INDEX]+(tūnga_uara==1?(uint32_t)보드밀리초()-사용자실행시각[tūranga_INDEX]:0);
    if (tāurunga_uara==5) return INDEX/4<sizeof(kaiwhakamahi_tono_ingoa[0])?kaiwhakamahi_tono_ingoa[tūranga_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t tāurunga_COUNT) {
    if (hohe || tāurunga_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = tāurunga_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t Rapu_INDEX, uintptr_t 현재위치, uintptr_t paita_raraunga) {
    if (hohe || Rapu_INDEX >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[Rapu_INDEX] || !paita_raraunga || paita_raraunga > 255)
        return (uint32_t)-22;
    전달인수[Rapu_INDEX][현재위치] = paita_raraunga;
    전달인수길이[Rapu_INDEX] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Karaka_uara(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void tāpu_KUA_PAU_TE_WĀ(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    mīhini_rēhita(THK_kaihora + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void Start_KUA_PAU_TE_WĀ(void) {
    uint64_t 간격 = FREQUENCY * 2, whakahohe = 1;
    마감시각 = Karaka_uara() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(whakahohe) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned raraunga_aukati = 0; raraunga_aukati < 4; raraunga_aukati++) {
        pūtake_ADDRESS[raraunga_aukati] = (uintptr_t)가운데[raraunga_aukati] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t ADDRESS = ((uintptr_t)raraunga_aukati << 30) | ((uintptr_t)순번 << 21);
            가운데[raraunga_aukati][순번] = ADDRESS | 1 | 접근표시 | 사용자실행금지;
            if (ADDRESS >= 0xfc000000ul) 가운데[raraunga_aukati][순번] |= 권한실행금지; // Device-nGnRnE
            else 가운데[raraunga_aukati][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_uara = 0; SECOND_uara < kaiwhakamahi_whārangi_COUNT / 512; SECOND_uara++)
        가운데[0][(kaiwhakamahi_BASE >> 21) + SECOND_uara] = (uintptr_t)(whārangi_Rārangi + SECOND_uara * 512) | 3;
    for (unsigned 순번 = 0; 순번 < kaiwhakamahi_whārangi_COUNT; 순번++) whārangi_Rārangi[순번] = (kaiwhakamahi_BASE + 순번 * rahinga_whārangi) | kākano_whārangi;
    uint64_t Pūmahara_huanga_rēhita = 0x4400, ADDRESS_Whakawhiti_Reo_mana = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Pūmahara_huanga_rēhita), "r"(ADDRESS_Whakawhiti_Reo_mana), "r"((uintptr_t)pūtake_ADDRESS) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    tāpu_KUA_PAU_TE_WĀ();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 tāurunga_ira_uara 때만 Tuku_uara.
    mīhini_rēhita(THK_kaihora) = 0;
    mīhini_rēhita(THK_kaihora + 0x180) = 0xffffffff;
    mīhini_rēhita(THK_kaihora + 0x80) = 0xffffffff;
    mīhini_rēhita(THK_kaihora + 0x280) = 1u << 30;
    mīhini_rēhita(THK_kaihora + 0x41c) = 0x80808080;
    mīhini_rēhita(THK_kaihora + 0x100) = 1u << 30;
    mīhini_rēhita(THK_PTM_atanga + 4) = 0xff;
    mīhini_rēhita(THK_PTM_atanga + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Haumarutanga = (mīhini_rēhita(THK_kaihora + 4) & (1u << 10)) != 0;
    mīhini_rēhita(THK_kaihora) = Haumarutanga ? 1 : 3;
    mīhini_rēhita(THK_PTM_atanga) = Haumarutanga ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_kāwai, mīhini_TYPE; uint32_t 판번호;
    uint64_t tāurunga_ira, kaupapa_Pane_OFFSET, wāhanga_Pane_OFFSET; uint32_t 설정비트;
    uint16_t 실행머리크기, kaupapa_Pane_tāurunga_rahi, kaupapa_Pane_COUNT, wāhanga_Pane_tāurunga_rahi, wāhanga_Pane_COUNT, wāhanga_ingoa_ripanga_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_kāwai, 설정비트; uint64_t OFFSET_uara, ADDRESS, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(kaiwhakamahi_tāpare) == 272, "exception assembly layout");
static int 포함된범위(uint64_t OFFSET_uara, uint64_t rahi, uint64_t mutu_OFFSET) {
    return OFFSET_uara <= mutu_OFFSET && rahi <= mutu_OFFSET - OFFSET_uara;
}
static int 부가정보검사(const unsigned char *raraunga_tūranga, size_t rahi) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, rahi)) {
        uint32_t 낱말들[3]; memcpy(낱말들, raraunga_tūranga + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, rahi) || !포함된범위(현재위치 + 이름영역크기, 설명크기, rahi)) return 0;
        const unsigned char Ingoa[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Ingoa) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Ingoa); 순번++) if (raraunga_tūranga[현재위치 + 순번] != Ingoa[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, raraunga_tūranga + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *raraunga, size_t rahi, int 리눅스방식) {
    if (rahi < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, raraunga, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_kāwai != 2 || 실행머리.mīhini_TYPE != 183 || 실행머리.판번호 != 1 || 실행머리.설정비트 || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.kaupapa_Pane_tāurunga_rahi != sizeof(실행파일구획) || !실행머리.kaupapa_Pane_COUNT || 실행머리.kaupapa_Pane_COUNT > 16 ||
        실행머리.kaupapa_Pane_OFFSET < sizeof(실행머리) || !포함된범위(실행머리.kaupapa_Pane_OFFSET, (uint64_t)실행머리.kaupapa_Pane_COUNT * sizeof(실행파일구획), rahi)) return 사용자실행파일오류;
    uint8_t 사용량[(kaiwhakamahi_IMAGE_mutu - kaiwhakamahi_BASE) / rahinga_whārangi] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.kaupapa_Pane_COUNT; 순번++) {
        실행파일구획 raraunga_tūranga; memcpy(&raraunga_tūranga, raraunga + 실행머리.kaupapa_Pane_OFFSET + 순번 * sizeof(raraunga_tūranga), sizeof(raraunga_tūranga));
        if (raraunga_tūranga.TYPE_kāwai == 4) {
            if (!포함된범위(raraunga_tūranga.OFFSET_uara, raraunga_tūranga.파일영역크기, rahi)) return 사용자실행파일오류;
            if (부가정보검사(raraunga + raraunga_tūranga.OFFSET_uara, raraunga_tūranga.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (raraunga_tūranga.TYPE_kāwai == 0 || raraunga_tūranga.TYPE_kāwai == 6 || (raraunga_tūranga.TYPE_kāwai == 0x6474e551 && !(raraunga_tūranga.설정비트 & 1))) continue;
        if (raraunga_tūranga.TYPE_kāwai != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!raraunga_tūranga.기억영역크기) continue;
        if (raraunga_tūranga.설정비트 & ~7u || !(raraunga_tūranga.설정비트 & 4) || (raraunga_tūranga.설정비트 & 3) == 3 || raraunga_tūranga.파일영역크기 > raraunga_tūranga.기억영역크기 ||
            (raraunga_tūranga.파일영역크기 && !포함된범위(raraunga_tūranga.OFFSET_uara, raraunga_tūranga.파일영역크기, rahi)) || raraunga_tūranga.ADDRESS < kaiwhakamahi_BASE ||
            !포함된범위(raraunga_tūranga.ADDRESS, raraunga_tūranga.기억영역크기, kaiwhakamahi_IMAGE_mutu) ||
            (!리눅스방식 && ((raraunga_tūranga.ADDRESS & (rahinga_whārangi - 1)) || (raraunga_tūranga.OFFSET_uara & (rahinga_whārangi - 1)) || raraunga_tūranga.맞춤 != rahinga_whārangi)) ||
            (리눅스방식 && (((raraunga_tūranga.ADDRESS ^ raraunga_tūranga.OFFSET_uara) & (rahinga_whārangi - 1)) || !raraunga_tūranga.맞춤 ||
                (raraunga_tūranga.맞춤 & (raraunga_tūranga.맞춤 - 1)) || raraunga_tūranga.맞춤 > 0x200000 || ((raraunga_tūranga.ADDRESS ^ raraunga_tūranga.OFFSET_uara) & (raraunga_tūranga.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (raraunga_tūranga.ADDRESS - kaiwhakamahi_BASE) / rahinga_whārangi;
        unsigned tāurunga_COUNT = ((raraunga_tūranga.ADDRESS & (rahinga_whārangi - 1)) + raraunga_tūranga.기억영역크기 + rahinga_whārangi - 1) / rahinga_whārangi;
        for (unsigned whārangi_uara = 첫항목; whārangi_uara < 첫항목 + tāurunga_COUNT; whārangi_uara++) {
            if (사용량[whārangi_uara]) return 사용자실행파일오류;
            사용량[whārangi_uara] = 1;
        }
        if ((raraunga_tūranga.설정비트 & 1) && 실행머리.tāurunga_ira >= raraunga_tūranga.ADDRESS && 실행머리.tāurunga_ira < raraunga_tūranga.ADDRESS + raraunga_tūranga.파일영역크기 && !(실행머리.tāurunga_ira & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *raraunga, size_t rahi) { return 실행파일검사(raraunga, rahi, 0); }
static void tahora_whārangi(uintptr_t ADDRESS, uint64_t 설정비트, unsigned whakaaetanga) {
    unsigned Rapu_INDEX = (ADDRESS - kaiwhakamahi_BASE) / rahinga_whārangi;
    whārangi_Rārangi[Rapu_INDEX] = ADDRESS | 설정비트;
    whakaaetanga_Rārangi[Rapu_INDEX] = whakaaetanga;
}
static int 사용자범위(uintptr_t ADDRESS, size_t tāurunga_COUNT, int 쓰는중) {
    if (ADDRESS < kaiwhakamahi_BASE || !포함된범위(ADDRESS, tāurunga_COUNT, kaiwhakamahi_mutu)) return 0;
    if (!tāurunga_COUNT) return 1;
    unsigned 첫항목 = (ADDRESS - kaiwhakamahi_BASE) / rahinga_whārangi, 마지막 = (ADDRESS + tāurunga_COUNT - 1 - kaiwhakamahi_BASE) / rahinga_whārangi;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(whakaaetanga_Rārangi[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int tārua_ara(uintptr_t ADDRESS, char *ara) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(ADDRESS, 1, 0)) return -14;
        ara[순번] = *(const char *)ADDRESS++;
        if (!ara[순번]) return 0;
    }
    return -36;
}
static intptr_t kākano_mēhua(intptr_t mēhua) { return mēhua < 0 ? -오류번호 : mēhua; }
static int 대응파일기술자(uint64_t kōnae_raweke) { return kōnae_raweke >= 3 && kōnae_raweke < 19 ? kōnae_Rārangi[kōnae_raweke - 3] : -1; }
static int 통신끝점소유(uint64_t kōnae_raweke) { return kōnae_raweke >= 32 && kōnae_raweke < 56 && 통신끝점들[kōnae_raweke - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t roa_uara, struct pk_sockaddr_in *ADDRESS) {
    if (roa_uara != sizeof(*ADDRESS)) return -22;
    if (!사용자범위(가리킴값, roa_uara, 0)) return -14;
    memcpy(ADDRESS, (const void *)가리킴값, sizeof(*ADDRESS));
    return ADDRESS->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t roa_atatohu, pk_socklen_t *수용량) {
    if (!사용자범위(roa_atatohu, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)roa_atatohu, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t roa_atatohu, pk_socklen_t 수용량, int ADDRESS, int 접속번호) {
    struct pk_sockaddr_in uara; memset(&uara, 0, sizeof(uara));
    uara.sin_family = AF_INET; uara.sin_port = pk_htons(접속번호); uara.sin_addr.s_addr = pk_htonl(ADDRESS);
    if (수용량) memcpy((void *)가리킴값, &uara, 수용량);
    pk_socklen_t roa_uara = sizeof(uara); memcpy((void *)roa_atatohu, &roa_uara, sizeof(roa_uara));
}
extern uintptr_t papa_hongere(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(kaiwhakamahi_tāpare *kōnae_tāurunga) {
    uintptr_t 첫째값 = kōnae_tāurunga->rēhita_raraunga[0], SECOND_uara = kōnae_tāurunga->rēhita_raraunga[1], waehere_pūāhua = kōnae_tāurunga->rēhita_raraunga[2];
    char ara[65];
    int kōnae_raweke, mēhua;
    switch (kōnae_tāurunga->rēhita_raraunga[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: atatohu 전체를 검사한 Hoki_uara 출력/Kōnae huri_uara
        if (waehere_pūāhua > 65536) return -22;
        if (!사용자범위(SECOND_uara, waehere_pūāhua, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Karaka_uara();
            for (size_t 순번 = 0; 순번 < waehere_pūāhua; 순번++) papa_hongere(첫째값, ((const unsigned char *)SECOND_uara)[순번]);
            /* 큰 tty를 그린 kākano_uara_0611a8a8 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(pāhekoheko){
                마감시각+=Karaka_uara()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return waehere_pūāhua;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t tuemi_COUNT=waehere_pūāhua>512?512:waehere_pūāhua;for(size_t 순번=0;순번<tuemi_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_uara)[순번]);return 자바흐름쓰기(첫째값,tuemi_COUNT);
        }
        kōnae_raweke = 대응파일기술자(첫째값); if (kōnae_raweke < 0) return -9;
        return kākano_mēhua(pk_write(kōnae_raweke, (const void *)SECOND_uara, waehere_pūāhua));
    case 2:
        if (waehere_pūāhua > 65536) return -22;
        if (!사용자범위(SECOND_uara, waehere_pūāhua, 1)) return -14;
        if (첫째값 == 0) {
            size_t tuemi_COUNT = 0;
            while (tuemi_COUNT < waehere_pūāhua) {
                int pūāhua_uara = (int32_t)보드글자읽기(); if (pūāhua_uara == -2) return tuemi_COUNT; if (pūāhua_uara < 0) break;
                ((unsigned char *)SECOND_uara)[tuemi_COUNT++] = pūāhua_uara;
            }
            return tuemi_COUNT ? (intptr_t)tuemi_COUNT : (waehere_pūāhua ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            mēhua=자바흐름읽기(첫째값,waehere_pūāhua>512?512:waehere_pūāhua);if(mēhua>0)for(int 순번=0;순번<mēhua;순번++)((unsigned char *)SECOND_uara)[순번]=자바전문얻기(순번);return mēhua;
        }
        kōnae_raweke = 대응파일기술자(첫째값); if (kōnae_raweke < 0) return -9;
        return kākano_mēhua(pk_read(kōnae_raweke, (void *)SECOND_uara, waehere_pūāhua));
    case 3:
        mēhua = tārua_ara(첫째값, ara); if (mēhua) return mēhua;
        if (SECOND_uara > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (kōnae_Rārangi[순번] < 0) {
            kōnae_raweke = pk_open(ara, (int)SECOND_uara, 0600);
            if (kōnae_raweke < 0) return -오류번호;
            kōnae_Rārangi[순번] = kōnae_raweke; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { mēhua = 통신끝점닫기(첫째값); if (!mēhua) 통신끝점들[첫째값 - 32] = 0; return mēhua; }
        kōnae_raweke = 대응파일기술자(첫째값); if (kōnae_raweke < 0) return -9;
        mēhua = pk_close(kōnae_raweke); if (!mēhua) kōnae_Rārangi[첫째값 - 3] = -1;
        return kākano_mēhua(mēhua);
    case 5:
        kōnae_raweke = 대응파일기술자(첫째값); if (kōnae_raweke < 0) return -9;
        if (waehere_pūāhua > 2) return -22;
        return kākano_mēhua(pk_lseek(kōnae_raweke, (int64_t)SECOND_uara, waehere_pūāhua));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 kaiwhakamahi RW/NX 힙, 새로 노출되는 페이지는 0으로 arawhiti
        if (!첫째값) return 동적기억끝;
        if (첫째값 < kaiwhakamahi_IMAGE_mutu || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + rahinga_whārangi - 1) & ~(rahinga_whārangi - 1);
        uintptr_t 새쪽들 = (첫째값 + rahinga_whārangi - 1) & ~(rahinga_whārangi - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t raraunga_tūranga = 이전쪽들; raraunga_tūranga < 새쪽들; raraunga_tūranga += rahinga_whārangi) tahora_whārangi(raraunga_tūranga, kākano_whārangi, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t raraunga_tūranga = 이전쪽들; raraunga_tūranga < 새쪽들; raraunga_tūranga += rahinga_whārangi) tahora_whārangi(raraunga_tūranga, 사용자읽고쓰기, 3);
        } else {
            for (uintptr_t raraunga_tūranga = 새쪽들; raraunga_tūranga < 이전쪽들; raraunga_tūranga += rahinga_whārangi) {
                whārangi_Rārangi[(raraunga_tūranga - kaiwhakamahi_BASE) / rahinga_whārangi] = 0; whakaaetanga_Rārangi[(raraunga_tūranga - kaiwhakamahi_BASE) / rahinga_whārangi] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        kōnae_raweke = 대응파일기술자(첫째값); return kōnae_raweke < 0 ? -9 : kākano_mēhua(pk_size(kōnae_raweke));
    case 10:
        kōnae_raweke = 대응파일기술자(첫째값); return kōnae_raweke < 0 ? -9 : kākano_mēhua(pk_ftruncate(kōnae_raweke, (int64_t)SECOND_uara));
    case 11:
        mēhua = tārua_ara(첫째값, ara); return mēhua ? mēhua : kākano_mēhua(pk_unlink(ara));
    case 12:
        kōnae_raweke = 대응파일기술자(첫째값); return kōnae_raweke < 0 ? -9 : kākano_mēhua(pk_fsync(kōnae_raweke));
    case 13: { // 그래픽 기초 API: kaiwhakamahi 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = kōnae_tāurunga->rēhita_raraunga[3], 높이값 = kōnae_tāurunga->rēhita_raraunga[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_uara > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_uara) return -22;
        for (uintptr_t 세로좌표 = SECOND_uara; 세로좌표 < SECOND_uara + 높이값; 세로좌표++) for (uintptr_t taunga_x = 첫째값; taunga_x < 첫째값 + 너비값; taunga_x++) papa_pika(taunga_x, 세로좌표, waehere_pūāhua);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=tuemi_COUNT; args(index,buffer,capacity)=UTF-8 roa_uara
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (waehere_pūāhua <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(SECOND_uara, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_uara, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;pāhekoheko=1;return papa_Tauranga(13);}
        if(첫째값==2){pāhekoheko=0;return 0;}
        if(첫째값==3)return papa_Tauranga(13);
        if(첫째값!=1||!pāhekoheko)return -22;
        mēhua=(int32_t)보드글자읽기();
        if(mēhua==-4096)return mēhua;
        Start_KUA_PAU_TE_WĀ();return mēhua<0?-11:mēhua;
    case 17: { // 유한한 협력 대기: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t mutu_TIME = Karaka_uara() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Karaka_uara() < mutu_TIME);
        Start_KUA_PAU_TE_WĀ(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (SECOND_uara > 2) return -22;
        mēhua = tārua_ara(첫째값, ara); if (mēhua) return mēhua;
        unsigned roa_uara = 0; while (ara[roa_uara]) roa_uara++;
        mēhua = 자바경로시작(roa_uara); if (mēhua < 0) return mēhua;
        for (unsigned 순번 = 0; 순번 < roa_uara; 순번++) 자바경로바이트(순번, (unsigned char)ara[순번]);
        return SECOND_uara == 0 ? 자바항목종류() : SECOND_uara == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int pūāhua_uara=(int32_t)보드글자읽기();if(pūāhua_uara==-4096)return pūāhua_uara;if(pūāhua_uara>=0)화면누름(kaipupuri_ahanoa,pūāhua_uara);Start_KUA_PAU_TE_WĀ();}
        if(첫째값==3&&waehere_pūāhua){if(!자바셸대화형())return -95;pāhekoheko=1;papa_Tauranga(300);}
        return 화면호출(kaipupuri_ahanoa,첫째값,SECOND_uara,waehere_pūāhua,kōnae_tāurunga->rēhita_raraunga[3],kōnae_tāurunga->rēhita_raraunga[4],kōnae_tāurunga->rēhita_raraunga[5]);
    case 21:
        if(waehere_pūāhua>127)return -22;if(!사용자범위(SECOND_uara,waehere_pūāhua*sizeof(uint32_t),0))return -14;
        return 화면글(kaipupuri_ahanoa,첫째값,(const uint32_t *)SECOND_uara,waehere_pūāhua);
    case 22: // 화면 rahi uiui_uara: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_uara==SOCK_STREAM&&(waehere_pūāhua==0||waehere_pūāhua==6))mēhua=자바흐름만들기();
        else if(SECOND_uara==SOCK_DGRAM&&(waehere_pūāhua==0||waehere_pūāhua==IPPROTO_UDP))mēhua=자바전문만들기(첫째값,SECOND_uara,waehere_pūāhua);
        else return -93;
        if (mēhua >= 32 && mēhua < 56) 통신끝점들[mēhua - 32] = 1;
        return mēhua;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in ADDRESS;
        mēhua = 주소입력(SECOND_uara, waehere_pūāhua, &ADDRESS); if (mēhua) return mēhua;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(ADDRESS.sin_addr.s_addr),pk_htons(ADDRESS.sin_port)):자바전문묶기(첫째값, pk_htonl(ADDRESS.sin_addr.s_addr), pk_htons(ADDRESS.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (kōnae_tāurunga->rēhita_raraunga[3]) return -95;
        if (waehere_pūāhua > 512) return -90;
        if (waehere_pūāhua && !사용자범위(SECOND_uara, waehere_pūāhua, 0)) return -14;
        struct pk_sockaddr_in ADDRESS;
        mēhua = 주소입력(kōnae_tāurunga->rēhita_raraunga[4], kōnae_tāurunga->rēhita_raraunga[5], &ADDRESS); if (mēhua) return mēhua;
        for (unsigned 순번 = 0; 순번 < waehere_pūāhua; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_uara)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(ADDRESS.sin_addr.s_addr), pk_htons(ADDRESS.sin_port), waehere_pūāhua);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (kōnae_tāurunga->rēhita_raraunga[3]) return -95;
        if (waehere_pūāhua > 512) return -90;
        if (waehere_pūāhua && !사용자범위(SECOND_uara, waehere_pūāhua, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (kōnae_tāurunga->rēhita_raraunga[4]) { mēhua = 주소출력검사(kōnae_tāurunga->rēhita_raraunga[4], kōnae_tāurunga->rēhita_raraunga[5], &수용량); if (mēhua) return mēhua; }
        mēhua = 자바전문받기(첫째값, waehere_pūāhua); if (mēhua < 0) return mēhua;
        for (int 순번 = 0; 순번 < mēhua; 순번++) ((unsigned char *)SECOND_uara)[순번] = 자바전문얻기(순번);
        if (kōnae_tāurunga->rēhita_raraunga[4]) 주소출력(kōnae_tāurunga->rēhita_raraunga[4], kōnae_tāurunga->rēhita_raraunga[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return mēhua;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        mēhua = 주소출력검사(SECOND_uara, waehere_pūāhua, &수용량); if (mēhua) return mēhua;
        주소출력(SECOND_uara,waehere_pūāhua,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in ADDRESS;
        mēhua=주소입력(SECOND_uara,waehere_pūāhua,&ADDRESS);if(mēhua)return mēhua;
        return 자바흐름연결(첫째값,pk_htonl(ADDRESS.sin_addr.s_addr),pk_htons(ADDRESS.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_uara):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_uara||waehere_pūāhua)return -95;mēhua=자바흐름연결받기(첫째값);if(mēhua>=40&&mēhua<56)통신끝점들[mēhua-32]=1;return mēhua;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(kaiwhakamahi_tāpare *kōnae_tāurunga) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(kōnae_tāurunga) : 자체체계호출(kōnae_tāurunga);
}
static void 커널돌아가기(kaiwhakamahi_tāpare *kōnae_tāurunga, int mēhua) {
    tāpu_KUA_PAU_TE_WĀ();
    kōnae_tāurunga->rēhita_raraunga[0] = (uint64_t)(int64_t)mēhua;
    kōnae_tāurunga->tono_tūranga = (uintptr_t)사용자복귀;
    kōnae_tāurunga->tūnga_CODE = 0x3c5; // EL1h, DAIF masked
}
int 사용자예외(kaiwhakamahi_tāpare *kōnae_tāurunga, unsigned haukoti) {
    if (!hohe || (kōnae_tāurunga->tūnga_CODE & 15) != 0) return 0;
    if (haukoti) {
        uint32_t 승인값 = mīhini_rēhita(THK_PTM_atanga + 0xc), pūtāutu_uara = 승인값 & 1023;
        if (pūtāutu_uara == 30) { 커널돌아가기(kōnae_tāurunga, kaiwhakamahi_KUA_PAU_TE_WĀ); mīhini_rēhita(THK_PTM_atanga + 0x10) = 승인값; return 1; }
        if (pūtāutu_uara < 1020) mīhini_rēhita(THK_PTM_atanga + 0x10) = 승인값;
        return 1;
    }
    uint64_t 예외상태; __asm__ volatile("mrs %0, esr_el1" : "=r"(예외상태));
    if (Karaka_uara() >= 마감시각) { 커널돌아가기(kōnae_tāurunga, kaiwhakamahi_KUA_PAU_TE_WĀ); return 1; }
    unsigned 예외분류 = 예외상태 >> 26;
    if (예외분류 == 0x15 && (예외상태 & 0xffff) == 0) {
        if (리눅스규약 ? kōnae_tāurunga->rēhita_raraunga[8] == 93 || kōnae_tāurunga->rēhita_raraunga[8] == 94 : kōnae_tāurunga->rēhita_raraunga[8] == 6) 커널돌아가기(kōnae_tāurunga, (int)(kōnae_tāurunga->rēhita_raraunga[0] & 255));
        else {
            intptr_t mēhua=체계호출(kōnae_tāurunga);
            if(mēhua==-4096&&pāhekoheko){
                저장값[kaipupuri_ahanoa].실행틀=*kōnae_tāurunga;저장값[kaipupuri_ahanoa].실행틀.tono_tūranga-=4;
                사용자실수보관(저장값[kaipupuri_ahanoa].실수저장상태);커널돌아가기(kōnae_tāurunga,사용자중단됨);
            }else kōnae_tāurunga->rēhita_raraunga[0]=(uint64_t)mēhua;
        }
    } else 커널돌아가기(kōnae_tāurunga, 예외분류 == 0x24 ? kaiwhakamahi_raraunga_hapa : 예외분류 == 0x20 ? 사용자실행오류 : kaiwhakamahi_muhu_tohutohu);
    return 1;
}

// 생성된 const ELF rōpū_uara: 실행은 반드시 kaupapa_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *raraunga; size_t rahi; unsigned 전달값; } kaupapa;
#include "programs.h"
static void *hopuāhua(unsigned tūranga_INDEX){return (void *)(0x04000000ul+tūranga_INDEX*(kaiwhakamahi_mutu-kaiwhakamahi_BASE));}
static int Mutu_kaupapa(int mēhua){
    사용자누적시각[kaipupuri_ahanoa]+=(uint32_t)보드밀리초()-사용자실행시각[kaipupuri_ahanoa];
    tāpu_KUA_PAU_TE_WĀ();hohe=0;
    if(mēhua==사용자중단됨){
        저장된작업 *aho_raraunga=&저장값[kaipupuri_ahanoa];aho_raraunga->멈춤상태=1;aho_raraunga->pāhekoheko=pāhekoheko;aho_raraunga->리눅스규약=리눅스규약;aho_raraunga->동적기억공간=동적기억끝;aho_raraunga->인수개수=전달인수개수;
        memcpy(aho_raraunga->whakaaetanga_Rārangi,whakaaetanga_Rārangi,sizeof(whakaaetanga_Rārangi));memcpy(aho_raraunga->kōnae_Rārangi,kōnae_Rārangi,sizeof(kōnae_Rārangi));memcpy(aho_raraunga->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(aho_raraunga->tohenga_HUĀNGA,전달인수,sizeof(전달인수));memcpy(aho_raraunga->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<kaiwhakamahi_whārangi_COUNT;순번++)if(whakaaetanga_Rārangi[순번])memcpy((unsigned char *)hopuāhua(kaipupuri_ahanoa)+순번*rahinga_whārangi,(void *)(kaiwhakamahi_BASE+순번*rahinga_whārangi),rahinga_whārangi);
    }else{
        저장값[kaipupuri_ahanoa].멈춤상태=0;화면초기화(kaipupuri_ahanoa);
        for(unsigned 순번=0;순번<16;순번++)if(kōnae_Rārangi[순번]>=0)pk_close(kōnae_Rārangi[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<kaiwhakamahi_whārangi_COUNT;순번++){whārangi_Rārangi[순번]=0;whakaaetanga_Rārangi[순번]=0;}변환표맞추기();return mēhua;
}
uintptr_t papa_mana_kaiwhakamahi(uintptr_t hohenga){
    unsigned tūranga_INDEX=hohenga&15;if(tūranga_INDEX>=4||hohe)return (uint32_t)-22;
    저장된작업 *aho_raraunga=&저장값[tūranga_INDEX];
    if(hohenga>=32){if(aho_raraunga->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(aho_raraunga->kōnae_Rārangi[순번]>=0)pk_close(aho_raraunga->kōnae_Rārangi[순번]);for(unsigned 순번=0;순번<24;순번++)if(aho_raraunga->통신끝점들[순번])통신끝점닫기(순번+32);}aho_raraunga->멈춤상태=0;화면초기화(tūranga_INDEX);return 0;}
    if(hohenga>=16)return aho_raraunga->멈춤상태;
    if(!aho_raraunga->멈춤상태)return (uint32_t)-22;
    kaipupuri_ahanoa=tūranga_INDEX;pāhekoheko=aho_raraunga->pāhekoheko;리눅스규약=aho_raraunga->리눅스규약;동적기억끝=aho_raraunga->동적기억공간;전달인수개수=aho_raraunga->인수개수;
    memcpy(kōnae_Rārangi,aho_raraunga->kōnae_Rārangi,sizeof(kōnae_Rārangi));memcpy(통신끝점들,aho_raraunga->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,aho_raraunga->tohenga_HUĀNGA,sizeof(전달인수));memcpy(전달인수길이,aho_raraunga->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<kaiwhakamahi_whārangi_COUNT;순번++)whārangi_Rārangi[순번]=(kaiwhakamahi_BASE+순번*rahinga_whārangi)|kākano_whārangi;변환표맞추기();
    memset((void *)kaiwhakamahi_BASE,0,kaiwhakamahi_mutu-kaiwhakamahi_BASE);
    for(unsigned 순번=0;순번<kaiwhakamahi_whārangi_COUNT;순번++)if(aho_raraunga->whakaaetanga_Rārangi[순번])memcpy((void *)(kaiwhakamahi_BASE+순번*rahinga_whārangi),(unsigned char *)hopuāhua(tūranga_INDEX)+순번*rahinga_whārangi,rahinga_whārangi);
    memcpy(whakaaetanga_Rārangi,aho_raraunga->whakaaetanga_Rārangi,sizeof(whakaaetanga_Rārangi));
    for(unsigned 순번=0;순번<kaiwhakamahi_whārangi_COUNT;순번++){unsigned raraunga_tūranga=whakaaetanga_Rārangi[순번];whārangi_Rārangi[순번]=raraunga_tūranga?(kaiwhakamahi_BASE+순번*rahinga_whārangi)|(raraunga_tūranga==3?사용자읽고쓰기:raraunga_tūranga==5?사용자읽고실행:kaiwhakamahi_pānui_anake):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");hohe=1;aho_raraunga->멈춤상태=0;Start_KUA_PAU_TE_WĀ();
    사용자실행시각[kaipupuri_ahanoa]=보드밀리초();
    return (uint32_t)Mutu_kaupapa(kaiwhakamahi_TāT(&aho_raraunga->실행틀,aho_raraunga->실수저장상태));
}
static int whakahaere_kaupapa(const unsigned char *raraunga, size_t rahi, unsigned 전달값, int 리눅스방식, const char *Ingoa) {
    if (hohe) return -16;
    kaipupuri_ahanoa=papa_Tauranga(11);if(kaipupuri_ahanoa<0||kaipupuri_ahanoa>3||저장값[kaipupuri_ahanoa].멈춤상태)return -16;pāhekoheko=0;
    int 유효함 = 실행파일검사(raraunga, rahi, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned ingoa_INDEX=0;
    while (*Ingoa && ingoa_INDEX<31) kaiwhakamahi_tono_ingoa[kaipupuri_ahanoa][ingoa_INDEX++]=(unsigned char)*Ingoa++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (ingoa_INDEX) kaiwhakamahi_tono_ingoa[kaipupuri_ahanoa][ingoa_INDEX++]=' ';
        for (unsigned tūranga_INDEX=0; tūranga_INDEX<전달인수길이[0]; tūranga_INDEX++) kaiwhakamahi_tono_ingoa[kaipupuri_ahanoa][ingoa_INDEX++]=전달인수[0][tūranga_INDEX];
    }
    kaiwhakamahi_tono_ingoa[kaipupuri_ahanoa][ingoa_INDEX]=0; tau_kaiwhakamahi[kaipupuri_ahanoa]=Panuku_tau_kaiwhakamahi++;
    if (Panuku_tau_kaiwhakamahi>0x7fffffffu) Panuku_tau_kaiwhakamahi=10;
    kaiwhakamahi_Start_TIME[kaipupuri_ahanoa]=보드밀리초(); 사용자누적시각[kaipupuri_ahanoa]=0;
    for (unsigned 순번 = 0; 순번 < kaiwhakamahi_whārangi_COUNT; 순번++) whārangi_Rārangi[순번] = (kaiwhakamahi_BASE + 순번 * rahinga_whārangi) | kākano_whārangi;
    변환표맞추기();
    memset((void *)kaiwhakamahi_BASE, 0, kaiwhakamahi_mutu - kaiwhakamahi_BASE);
    memset(whakaaetanga_Rārangi, 0, sizeof(whakaaetanga_Rārangi));
    실행파일머리 실행머리; memcpy(&실행머리, raraunga, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.kaupapa_Pane_COUNT; 순번++) {
        실행파일구획 raraunga_tūranga; memcpy(&raraunga_tūranga, raraunga + 실행머리.kaupapa_Pane_OFFSET + 순번 * sizeof(raraunga_tūranga), sizeof(raraunga_tūranga));
        if (raraunga_tūranga.TYPE_kāwai != 1 || !raraunga_tūranga.기억영역크기) continue;
        if (raraunga_tūranga.파일영역크기) memcpy((void *)(uintptr_t)raraunga_tūranga.ADDRESS, raraunga + raraunga_tūranga.OFFSET_uara, raraunga_tūranga.파일영역크기);
        for (uintptr_t 현재위치 = raraunga_tūranga.ADDRESS & ~(rahinga_whārangi - 1); 현재위치 < raraunga_tūranga.ADDRESS + raraunga_tūranga.기억영역크기; 현재위치 += rahinga_whārangi) {
            whakaaetanga_Rārangi[(현재위치 - kaiwhakamahi_BASE) / rahinga_whārangi] = (raraunga_tūranga.설정비트 & 2) ? 3 : ((raraunga_tūranga.설정비트 & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = kaiwhakamahi_Huinga_ADDRESS; 현재위치 < kaiwhakamahi_mutu; 현재위치 += rahinga_whārangi) whakaaetanga_Rārangi[(현재위치 - kaiwhakamahi_BASE) / rahinga_whārangi] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.tāurunga_ira) : kaiwhakamahi_mutu;
    for (unsigned 순번 = 0; 순번 < kaiwhakamahi_whārangi_COUNT; 순번++) {
        unsigned whakaaetanga = whakaaetanga_Rārangi[순번];
        whārangi_Rārangi[순번] = whakaaetanga ? (kaiwhakamahi_BASE + 순번 * rahinga_whārangi) | (whakaaetanga == 3 ? 사용자읽고쓰기 : whakaaetanga == 5 ? 사용자읽고실행 : kaiwhakamahi_pānui_anake) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) kōnae_Rārangi[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = kaiwhakamahi_IMAGE_mutu;
    hohe = 1; Start_KUA_PAU_TE_WĀ();
    사용자실행시각[kaipupuri_ahanoa]=보드밀리초();
    int mēhua = kaiwhakamahi_tāuru(실행머리.tāurunga_ira, 초기쌓임공간, 전달값);
    return Mutu_kaupapa(mēhua);
}
uintptr_t papa_kaiwhakamahi_whakahaere(uintptr_t Rapu_INDEX) {
    if (Rapu_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Ingoa=Rapu_INDEX==10?"javac":Rapu_INDEX==11?"java":Rapu_INDEX==12?"python":Rapu_INDEX==13?"vi":Rapu_INDEX==14?"jar":Rapu_INDEX==15?"cc":Rapu_INDEX==16?"jaot":"ELF";
    return (uint32_t)whakahaere_kaupapa(실행항목들[Rapu_INDEX].raraunga, 실행항목들[Rapu_INDEX].rahi, 실행항목들[Rapu_INDEX].전달값, 0, Ingoa);
}
static uintptr_t kawe_kōnae(int 리눅스방식) {
    static unsigned char IMAGE[16384];
    if (hohe || !전달인수개수) return (uint32_t)-22;
    int kōnae_raweke = pk_open((const char *)전달인수[0], pānui_anake_uara, 0);
    if (kōnae_raweke < 0) return (uint32_t)-오류번호;
    int rahi = pk_size(kōnae_raweke);
    if (rahi < 0 || (unsigned)rahi > sizeof(IMAGE)) { pk_close(kōnae_raweke); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(kōnae_raweke, IMAGE, rahi); pk_close(kōnae_raweke);
    if (RECEIVED_COUNT != rahi) return (uint32_t)-5;
    return (uint32_t)whakahaere_kaupapa(IMAGE, rahi, 0, 리눅스방식, "");
}
uintptr_t papa_kaiwhakamahi_kōnae(void) { return kawe_kōnae(0); }
uintptr_t 보드사용자리눅스파일(void) { return kawe_kōnae(1); }
uintptr_t papa_kaiwhakamahi_whakamana(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].raraunga, 잘못된실행항목들[순번].rahi) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
