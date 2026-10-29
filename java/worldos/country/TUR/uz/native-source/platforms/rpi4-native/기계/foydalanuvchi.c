#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 bajarmoq_buyruq 기계 qatlam_VALUE. Fayl ma_lumotlar/정책은 기존 AOT Java 커널에 위임한다.
#include "foydalanuvchi.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../Tarmoq_Stack/Tarmoq_Stack.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_tarqatuvchi 0xff841000ul
#define IRQ_CPU_interfeys 0xff842000ul
#define sahifa_o_lchami 4096ul
#define 접근표시 (1ul << 10)
#define yo_q_bajarmoq_ruxsat (1ul << 53)
#define foydalanuvchi_yo_q_bajarmoq (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define o_zak_sahifa (3ul | 보통기억 | yo_q_bajarmoq_ruxsat | foydalanuvchi_yo_q_bajarmoq)
#define foydalanuvchi_o_qish_yozish_mumkin (3ul | 보통기억 | (1ul << 6) | yo_q_bajarmoq_ruxsat | foydalanuvchi_yo_q_bajarmoq)
#define foydalanuvchi_faqat_o_qish_uchun (3ul | 보통기억 | (3ul << 6) | yo_q_bajarmoq_ruxsat | foydalanuvchi_yo_q_bajarmoq)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | yo_q_bajarmoq_ruxsat)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t yozuv_taxtasi_piksel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t yozuv_taxtasi_Terminal(uintptr_t);
extern int 터미널대기(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int foydalanuvchi_CV(foydalanuvchi_kadr *,void *);
extern void 사용자실수보관(void *);
extern int foydalanuvchi_kiritmoq(uintptr_t kiritish_nuqta, uintptr_t Stack_Xotira, uintptr_t 전달값);
extern void foydalanuvchi_qaytarish(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t ildiz_manzil[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t sahifa_Ro_yxat[foydalanuvchi_sahifa_COUNT] __attribute__((aligned(4096)));
static uint8_t Ruxsatlar_Ro_yxat[foydalanuvchi_sahifa_COUNT];
static int faol, fayl_Ro_yxat[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned fayl_deskriptor){return fayl_deskriptor<40?자바전문닫기(fayl_deskriptor):자바흐름닫기(fayl_deskriptor);}
static uint64_t FREQUENCY, 마감시각;
static uintptr_t 동적기억끝;
// o_zak_VALUE 셸이 준비한 UTF-8 인수. EL0에는 namuna_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,o_zaro_faol,리눅스규약,fayl_Ro_yxat[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char dalil_ARRAY[8][256],Ruxsatlar_Ro_yxat[foydalanuvchi_sahifa_COUNT];
    uintptr_t 동적기억공간; foydalanuvchi_kadr 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int egasi_obyekt,o_zaro_faol;
static uint32_t foydalanuvchi_raqami[4], foydalanuvchi_Start_TIME[4], 사용자누적시각[4], 사용자실행시각[4], Keyingi_foydalanuvchi_raqami=10;
static unsigned char foydalanuvchi_buyruq_nom[4][288];
uint32_t 사용자상태읽기(unsigned kiritish_VALUE, unsigned INDEX) {
    unsigned holat_INDEX=INDEX&3;
    int holat_VALUE_e10195a1=(faol && egasi_obyekt==(int)holat_INDEX) ? 1 : 저장값[holat_INDEX].멈춤상태 ? 2 : 0;
    if (kiritish_VALUE==0) return holat_VALUE_e10195a1;
    if (!holat_VALUE_e10195a1) return 0;
    if (kiritish_VALUE==1) return foydalanuvchi_raqami[holat_INDEX];
    if (kiritish_VALUE==2) {
        unsigned char *쪽들=holat_VALUE_e10195a1==1?Ruxsatlar_Ro_yxat:저장값[holat_INDEX].Ruxsatlar_Ro_yxat;
        unsigned sahifa_COUNT=0; for (unsigned 순번=0; 순번<foydalanuvchi_sahifa_COUNT; 순번++) if(쪽들[순번]) sahifa_COUNT++;
        return sahifa_COUNT*4;
    }
    if (kiritish_VALUE==3) return (uint32_t)보드밀리초()-foydalanuvchi_Start_TIME[holat_INDEX];
    if (kiritish_VALUE==4) return 사용자누적시각[holat_INDEX]+(holat_VALUE_e10195a1==1?(uint32_t)보드밀리초()-사용자실행시각[holat_INDEX]:0);
    if (kiritish_VALUE==5) return INDEX/4<sizeof(foydalanuvchi_buyruq_nom[0])?foydalanuvchi_buyruq_nom[holat_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t kiritish_COUNT) {
    if (faol || kiritish_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = kiritish_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t 현재위치, uintptr_t bayt_ma_lumotlar) {
    if (faol || LOOKUP_INDEX >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[LOOKUP_INDEX] || !bayt_ma_lumotlar || bayt_ma_lumotlar > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][현재위치] = bayt_ma_lumotlar;
    전달인수길이[LOOKUP_INDEX] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Soat_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void To_xtatish_TANAFFUS(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    기계저장기(IRQ_tarqatuvchi + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void Start_TANAFFUS(void) {
    uint64_t 간격 = FREQUENCY * 2, yoqmoq = 1;
    마감시각 = Soat_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(yoqmoq) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned ma_lumotlar_bloklash = 0; ma_lumotlar_bloklash < 4; ma_lumotlar_bloklash++) {
        ildiz_manzil[ma_lumotlar_bloklash] = (uintptr_t)가운데[ma_lumotlar_bloklash] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t manzil = ((uintptr_t)ma_lumotlar_bloklash << 30) | ((uintptr_t)순번 << 21);
            가운데[ma_lumotlar_bloklash][순번] = manzil | 1 | 접근표시 | foydalanuvchi_yo_q_bajarmoq;
            if (manzil >= 0xfc000000ul) 가운데[ma_lumotlar_bloklash][순번] |= yo_q_bajarmoq_ruxsat; // Device-nGnRnE
            else 가운데[ma_lumotlar_bloklash][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < foydalanuvchi_sahifa_COUNT / 512; SECOND_VALUE++)
        가운데[0][(foydalanuvchi_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(sahifa_Ro_yxat + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < foydalanuvchi_sahifa_COUNT; 순번++) sahifa_Ro_yxat[순번] = (foydalanuvchi_BASE + 순번 * sahifa_o_lchami) | o_zak_sahifa;
    uint64_t 기억속성저장값 = 0x4400, manzil_Tarjima_boshqaruv = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(기억속성저장값), "r"(manzil_Tarjima_boshqaruv), "r"((uintptr_t)ildiz_manzil) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    To_xtatish_TANAFFUS();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 kiritish_nuqta_VALUE 때만 Ruxsatnoma_VALUE.
    기계저장기(IRQ_tarqatuvchi) = 0;
    기계저장기(IRQ_tarqatuvchi + 0x180) = 0xffffffff;
    기계저장기(IRQ_tarqatuvchi + 0x80) = 0xffffffff;
    기계저장기(IRQ_tarqatuvchi + 0x280) = 1u << 30;
    기계저장기(IRQ_tarqatuvchi + 0x41c) = 0x80808080;
    기계저장기(IRQ_tarqatuvchi + 0x100) = 1u << 30;
    기계저장기(IRQ_CPU_interfeys + 4) = 0xff;
    기계저장기(IRQ_CPU_interfeys + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Xavfsizlik = (기계저장기(IRQ_tarqatuvchi + 4) & (1u << 10)) != 0;
    기계저장기(IRQ_tarqatuvchi) = Xavfsizlik ? 1 : 3;
    기계저장기(IRQ_CPU_interfeys) = Xavfsizlik ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_toifa, 기계유형; uint32_t 판번호;
    uint64_t kiritish_nuqta, ilova_Sarlavha_OFFSET, bo_lim_Sarlavha_OFFSET; uint32_t tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati;
    uint16_t 실행머리크기, ilova_Sarlavha_kiritish_o_lcham, ilova_Sarlavha_COUNT, bo_lim_Sarlavha_kiritish_o_lcham, bo_lim_Sarlavha_COUNT, bo_lim_nom_jadval_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_toifa, tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati; uint64_t OFFSET_VALUE, manzil, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(foydalanuvchi_kadr) == 272, "exception assembly layout");
static int 포함된범위(uint64_t OFFSET_VALUE, uint64_t Hajmi, uint64_t to_xtatmoq_OFFSET) {
    return OFFSET_VALUE <= to_xtatmoq_OFFSET && Hajmi <= to_xtatmoq_OFFSET - OFFSET_VALUE;
}
static int 부가정보검사(const unsigned char *ma_lumotlar_holat, size_t Hajmi) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, Hajmi)) {
        uint32_t 낱말들[3]; memcpy(낱말들, ma_lumotlar_holat + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, Hajmi) || !포함된범위(현재위치 + 이름영역크기, 설명크기, Hajmi)) return 0;
        const unsigned char Nomi[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Nomi) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Nomi); 순번++) if (ma_lumotlar_holat[현재위치 + 순번] != Nomi[순번]) 일치 = 0;
        uint32_t 판번호 = 0;
        if (일치) memcpy(&판번호, ma_lumotlar_holat + 현재위치 + 이름영역크기, 4);
        if (일치 && 판번호 == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *ma_lumotlar, size_t Hajmi, int 리눅스방식) {
    if (Hajmi < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, ma_lumotlar, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_toifa != 2 || 실행머리.기계유형 != 183 || 실행머리.판번호 != 1 || 실행머리.tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.ilova_Sarlavha_kiritish_o_lcham != sizeof(실행파일구획) || !실행머리.ilova_Sarlavha_COUNT || 실행머리.ilova_Sarlavha_COUNT > 16 ||
        실행머리.ilova_Sarlavha_OFFSET < sizeof(실행머리) || !포함된범위(실행머리.ilova_Sarlavha_OFFSET, (uint64_t)실행머리.ilova_Sarlavha_COUNT * sizeof(실행파일구획), Hajmi)) return 사용자실행파일오류;
    uint8_t 사용량[(foydalanuvchi_rasm_to_xtatmoq - foydalanuvchi_BASE) / sahifa_o_lchami] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.ilova_Sarlavha_COUNT; 순번++) {
        실행파일구획 ma_lumotlar_holat; memcpy(&ma_lumotlar_holat, ma_lumotlar + 실행머리.ilova_Sarlavha_OFFSET + 순번 * sizeof(ma_lumotlar_holat), sizeof(ma_lumotlar_holat));
        if (ma_lumotlar_holat.TYPE_toifa == 4) {
            if (!포함된범위(ma_lumotlar_holat.OFFSET_VALUE, ma_lumotlar_holat.파일영역크기, Hajmi)) return 사용자실행파일오류;
            if (부가정보검사(ma_lumotlar + ma_lumotlar_holat.OFFSET_VALUE, ma_lumotlar_holat.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (ma_lumotlar_holat.TYPE_toifa == 0 || ma_lumotlar_holat.TYPE_toifa == 6 || (ma_lumotlar_holat.TYPE_toifa == 0x6474e551 && !(ma_lumotlar_holat.tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati & 1))) continue;
        if (ma_lumotlar_holat.TYPE_toifa != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!ma_lumotlar_holat.기억영역크기) continue;
        if (ma_lumotlar_holat.tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati & ~7u || !(ma_lumotlar_holat.tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati & 4) || (ma_lumotlar_holat.tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati & 3) == 3 || ma_lumotlar_holat.파일영역크기 > ma_lumotlar_holat.기억영역크기 ||
            (ma_lumotlar_holat.파일영역크기 && !포함된범위(ma_lumotlar_holat.OFFSET_VALUE, ma_lumotlar_holat.파일영역크기, Hajmi)) || ma_lumotlar_holat.manzil < foydalanuvchi_BASE ||
            !포함된범위(ma_lumotlar_holat.manzil, ma_lumotlar_holat.기억영역크기, foydalanuvchi_rasm_to_xtatmoq) ||
            (!리눅스방식 && ((ma_lumotlar_holat.manzil & (sahifa_o_lchami - 1)) || (ma_lumotlar_holat.OFFSET_VALUE & (sahifa_o_lchami - 1)) || ma_lumotlar_holat.맞춤 != sahifa_o_lchami)) ||
            (리눅스방식 && (((ma_lumotlar_holat.manzil ^ ma_lumotlar_holat.OFFSET_VALUE) & (sahifa_o_lchami - 1)) || !ma_lumotlar_holat.맞춤 ||
                (ma_lumotlar_holat.맞춤 & (ma_lumotlar_holat.맞춤 - 1)) || ma_lumotlar_holat.맞춤 > 0x200000 || ((ma_lumotlar_holat.manzil ^ ma_lumotlar_holat.OFFSET_VALUE) & (ma_lumotlar_holat.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (ma_lumotlar_holat.manzil - foydalanuvchi_BASE) / sahifa_o_lchami;
        unsigned kiritish_COUNT = ((ma_lumotlar_holat.manzil & (sahifa_o_lchami - 1)) + ma_lumotlar_holat.기억영역크기 + sahifa_o_lchami - 1) / sahifa_o_lchami;
        for (unsigned sahifa_VALUE = 첫항목; sahifa_VALUE < 첫항목 + kiritish_COUNT; sahifa_VALUE++) {
            if (사용량[sahifa_VALUE]) return 사용자실행파일오류;
            사용량[sahifa_VALUE] = 1;
        }
        if ((ma_lumotlar_holat.tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati & 1) && 실행머리.kiritish_nuqta >= ma_lumotlar_holat.manzil && 실행머리.kiritish_nuqta < ma_lumotlar_holat.manzil + ma_lumotlar_holat.파일영역크기 && !(실행머리.kiritish_nuqta & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *ma_lumotlar, size_t Hajmi) { return 실행파일검사(ma_lumotlar, Hajmi, 0); }
static void sahifa_belgilanishi(uintptr_t manzil, uint64_t tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati, unsigned ruxsatlar) {
    unsigned LOOKUP_INDEX = (manzil - foydalanuvchi_BASE) / sahifa_o_lchami;
    sahifa_Ro_yxat[LOOKUP_INDEX] = manzil | tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati;
    Ruxsatlar_Ro_yxat[LOOKUP_INDEX] = ruxsatlar;
}
static int 사용자범위(uintptr_t manzil, size_t kiritish_COUNT, int 쓰는중) {
    if (manzil < foydalanuvchi_BASE || !포함된범위(manzil, kiritish_COUNT, foydalanuvchi_to_xtatmoq)) return 0;
    if (!kiritish_COUNT) return 1;
    unsigned 첫항목 = (manzil - foydalanuvchi_BASE) / sahifa_o_lchami, 마지막 = (manzil + kiritish_COUNT - 1 - foydalanuvchi_BASE) / sahifa_o_lchami;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Ruxsatlar_Ro_yxat[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int namuna_yo_l(uintptr_t manzil, char *yo_l) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!사용자범위(manzil, 1, 0)) return -14;
        yo_l[순번] = *(const char *)manzil++;
        if (!yo_l[순번]) return 0;
    }
    return -36;
}
static intptr_t o_zak_o_lchov(intptr_t o_lchov) { return o_lchov < 0 ? -오류번호 : o_lchov; }
static int 대응파일기술자(uint64_t fayl_deskriptor) { return fayl_deskriptor >= 3 && fayl_deskriptor < 19 ? fayl_Ro_yxat[fayl_deskriptor - 3] : -1; }
static int 통신끝점소유(uint64_t fayl_deskriptor) { return fayl_deskriptor >= 32 && fayl_deskriptor < 56 && 통신끝점들[fayl_deskriptor - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t uzunlik_VALUE, struct pk_sockaddr_in *manzil) {
    if (uzunlik_VALUE != sizeof(*manzil)) return -22;
    if (!사용자범위(가리킴값, uzunlik_VALUE, 0)) return -14;
    memcpy(manzil, (const void *)가리킴값, sizeof(*manzil));
    return manzil->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t uzunlik_kursor, pk_socklen_t *수용량) {
    if (!사용자범위(uzunlik_kursor, sizeof(*수용량), 1)) return -14;
    memcpy(수용량, (const void *)uzunlik_kursor, sizeof(*수용량));
    if (*수용량 > sizeof(struct pk_sockaddr_in)) *수용량 = sizeof(struct pk_sockaddr_in);
    if (*수용량 && !사용자범위(가리킴값, *수용량, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t uzunlik_kursor, pk_socklen_t 수용량, int manzil, int 접속번호) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(접속번호); VALUE.sin_addr.s_addr = pk_htonl(manzil);
    if (수용량) memcpy((void *)가리킴값, &VALUE, 수용량);
    pk_socklen_t uzunlik_VALUE = sizeof(VALUE); memcpy((void *)uzunlik_kursor, &uzunlik_VALUE, sizeof(uzunlik_VALUE));
}
extern uintptr_t yozuv_taxtasi_kanal(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(foydalanuvchi_kadr *fayl_kiritish) {
    uintptr_t 첫째값 = fayl_kiritish->저장기값[0], SECOND_VALUE = fayl_kiritish->저장기값[1], belgi_kodi = fayl_kiritish->저장기값[2];
    char yo_l[65];
    int fayl_deskriptor, o_lchov;
    switch (fayl_kiritish->저장기값[8]) {
    case 0: return 1; // 자체 ABI 버전
    case 1: // write: kursor 전체를 검사한 Orqaga_VALUE 출력/Fayl o_zgartirmoq_VALUE
        if (belgi_kodi > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, belgi_kodi, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Soat_VALUE();
            for (size_t 순번 = 0; 순번 < belgi_kodi; 순번++) yozuv_taxtasi_kanal(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 o_zak_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(o_zaro_faol){
                마감시각+=Soat_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return belgi_kodi;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t element_COUNT=belgi_kodi>512?512:belgi_kodi;for(size_t 순번=0;순번<element_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,element_COUNT);
        }
        fayl_deskriptor = 대응파일기술자(첫째값); if (fayl_deskriptor < 0) return -9;
        return o_zak_o_lchov(pk_write(fayl_deskriptor, (const void *)SECOND_VALUE, belgi_kodi));
    case 2:
        if (belgi_kodi > 65536) return -22;
        if (!사용자범위(SECOND_VALUE, belgi_kodi, 1)) return -14;
        if (첫째값 == 0) {
            size_t element_COUNT = 0;
            while (element_COUNT < belgi_kodi) {
                int belgi_VALUE = (int32_t)보드글자읽기(); if (belgi_VALUE == -2) return element_COUNT; if (belgi_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[element_COUNT++] = belgi_VALUE;
            }
            return element_COUNT ? (intptr_t)element_COUNT : (belgi_kodi ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            o_lchov=자바흐름읽기(첫째값,belgi_kodi>512?512:belgi_kodi);if(o_lchov>0)for(int 순번=0;순번<o_lchov;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return o_lchov;
        }
        fayl_deskriptor = 대응파일기술자(첫째값); if (fayl_deskriptor < 0) return -9;
        return o_zak_o_lchov(pk_read(fayl_deskriptor, (void *)SECOND_VALUE, belgi_kodi));
    case 3:
        o_lchov = namuna_yo_l(첫째값, yo_l); if (o_lchov) return o_lchov;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (fayl_Ro_yxat[순번] < 0) {
            fayl_deskriptor = pk_open(yo_l, (int)SECOND_VALUE, 0600);
            if (fayl_deskriptor < 0) return -오류번호;
            fayl_Ro_yxat[순번] = fayl_deskriptor; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { o_lchov = 통신끝점닫기(첫째값); if (!o_lchov) 통신끝점들[첫째값 - 32] = 0; return o_lchov; }
        fayl_deskriptor = 대응파일기술자(첫째값); if (fayl_deskriptor < 0) return -9;
        o_lchov = pk_close(fayl_deskriptor); if (!o_lchov) fayl_Ro_yxat[첫째값 - 3] = -1;
        return o_zak_o_lchov(o_lchov);
    case 5:
        fayl_deskriptor = 대응파일기술자(첫째값); if (fayl_deskriptor < 0) return -9;
        if (belgi_kodi > 2) return -22;
        return o_zak_o_lchov(pk_lseek(fayl_deskriptor, (int64_t)SECOND_VALUE, belgi_kodi));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 foydalanuvchi RW/NX 힙, 새로 노출되는 페이지는 0으로 ishga_tushirmoq
        if (!첫째값) return 동적기억끝;
        if (첫째값 < foydalanuvchi_rasm_to_xtatmoq || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + sahifa_o_lchami - 1) & ~(sahifa_o_lchami - 1);
        uintptr_t 새쪽들 = (첫째값 + sahifa_o_lchami - 1) & ~(sahifa_o_lchami - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t ma_lumotlar_holat = 이전쪽들; ma_lumotlar_holat < 새쪽들; ma_lumotlar_holat += sahifa_o_lchami) sahifa_belgilanishi(ma_lumotlar_holat, o_zak_sahifa, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t ma_lumotlar_holat = 이전쪽들; ma_lumotlar_holat < 새쪽들; ma_lumotlar_holat += sahifa_o_lchami) sahifa_belgilanishi(ma_lumotlar_holat, foydalanuvchi_o_qish_yozish_mumkin, 3);
        } else {
            for (uintptr_t ma_lumotlar_holat = 새쪽들; ma_lumotlar_holat < 이전쪽들; ma_lumotlar_holat += sahifa_o_lchami) {
                sahifa_Ro_yxat[(ma_lumotlar_holat - foydalanuvchi_BASE) / sahifa_o_lchami] = 0; Ruxsatlar_Ro_yxat[(ma_lumotlar_holat - foydalanuvchi_BASE) / sahifa_o_lchami] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        fayl_deskriptor = 대응파일기술자(첫째값); return fayl_deskriptor < 0 ? -9 : o_zak_o_lchov(pk_size(fayl_deskriptor));
    case 10:
        fayl_deskriptor = 대응파일기술자(첫째값); return fayl_deskriptor < 0 ? -9 : o_zak_o_lchov(pk_ftruncate(fayl_deskriptor, (int64_t)SECOND_VALUE));
    case 11:
        o_lchov = namuna_yo_l(첫째값, yo_l); return o_lchov ? o_lchov : o_zak_o_lchov(pk_unlink(yo_l));
    case 12:
        fayl_deskriptor = 대응파일기술자(첫째값); return fayl_deskriptor < 0 ? -9 : o_zak_o_lchov(pk_fsync(fayl_deskriptor));
    case 13: { // 그래픽 기초 API: foydalanuvchi 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = fayl_kiritish->저장기값[3], 높이값 = fayl_kiritish->저장기값[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t Y_tugmasi_koordinat = SECOND_VALUE; Y_tugmasi_koordinat < SECOND_VALUE + 높이값; Y_tugmasi_koordinat++) for (uintptr_t x_koordinata = 첫째값; x_koordinata < 첫째값 + 너비값; x_koordinata++) yozuv_taxtasi_piksel(x_koordinata, Y_tugmasi_koordinat, belgi_kodi);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=element_COUNT; args(index,buffer,capacity)=UTF-8 uzunlik_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (belgi_kodi <= 전달인수길이[첫째값]) return -36;
        if (!사용자범위(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;o_zaro_faol=1;return yozuv_taxtasi_Terminal(13);}
        if(첫째값==2){o_zaro_faol=0;return 0;}
        if(첫째값==3)return yozuv_taxtasi_Terminal(13);
        if(첫째값!=1||!o_zaro_faol)return -22;
        o_lchov=(int32_t)보드글자읽기();
        if(o_lchov==-4096)return o_lchov;
        Start_TANAFFUS();return o_lchov<0?-11:o_lchov;
    case 17: { // 유한한 협력 bir_daqiqa_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t to_xtatmoq_TIME = Soat_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Soat_VALUE() < to_xtatmoq_TIME);
        Start_TANAFFUS(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        o_lchov = namuna_yo_l(첫째값, yo_l); if (o_lchov) return o_lchov;
        unsigned uzunlik_VALUE = 0; while (yo_l[uzunlik_VALUE]) uzunlik_VALUE++;
        o_lchov = 자바경로시작(uzunlik_VALUE); if (o_lchov < 0) return o_lchov;
        for (unsigned 순번 = 0; 순번 < uzunlik_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)yo_l[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int belgi_VALUE=(int32_t)보드글자읽기();if(belgi_VALUE==-4096)return belgi_VALUE;if(belgi_VALUE>=0)화면누름(egasi_obyekt,belgi_VALUE);Start_TANAFFUS();}
        if(첫째값==3&&belgi_kodi){if(!자바셸대화형())return -95;o_zaro_faol=1;yozuv_taxtasi_Terminal(300);}
        return 화면호출(egasi_obyekt,첫째값,SECOND_VALUE,belgi_kodi,fayl_kiritish->저장기값[3],fayl_kiritish->저장기값[4],fayl_kiritish->저장기값[5]);
    case 21:
        if(belgi_kodi>127)return -22;if(!사용자범위(SECOND_VALUE,belgi_kodi*sizeof(uint32_t),0))return -14;
        return 화면글(egasi_obyekt,첫째값,(const uint32_t *)SECOND_VALUE,belgi_kodi);
    case 22: // 화면 Hajmi so_rov_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(belgi_kodi==0||belgi_kodi==6))o_lchov=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(belgi_kodi==0||belgi_kodi==IPPROTO_UDP))o_lchov=자바전문만들기(첫째값,SECOND_VALUE,belgi_kodi);
        else return -93;
        if (o_lchov >= 32 && o_lchov < 56) 통신끝점들[o_lchov - 32] = 1;
        return o_lchov;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in manzil;
        o_lchov = 주소입력(SECOND_VALUE, belgi_kodi, &manzil); if (o_lchov) return o_lchov;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(manzil.sin_addr.s_addr),pk_htons(manzil.sin_port)):자바전문묶기(첫째값, pk_htonl(manzil.sin_addr.s_addr), pk_htons(manzil.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fayl_kiritish->저장기값[3]) return -95;
        if (belgi_kodi > 512) return -90;
        if (belgi_kodi && !사용자범위(SECOND_VALUE, belgi_kodi, 0)) return -14;
        struct pk_sockaddr_in manzil;
        o_lchov = 주소입력(fayl_kiritish->저장기값[4], fayl_kiritish->저장기값[5], &manzil); if (o_lchov) return o_lchov;
        for (unsigned 순번 = 0; 순번 < belgi_kodi; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(manzil.sin_addr.s_addr), pk_htons(manzil.sin_port), belgi_kodi);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fayl_kiritish->저장기값[3]) return -95;
        if (belgi_kodi > 512) return -90;
        if (belgi_kodi && !사용자범위(SECOND_VALUE, belgi_kodi, 1)) return -14;
        pk_socklen_t 수용량 = 0;
        if (fayl_kiritish->저장기값[4]) { o_lchov = 주소출력검사(fayl_kiritish->저장기값[4], fayl_kiritish->저장기값[5], &수용량); if (o_lchov) return o_lchov; }
        o_lchov = 자바전문받기(첫째값, belgi_kodi); if (o_lchov < 0) return o_lchov;
        for (int 순번 = 0; 순번 < o_lchov; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (fayl_kiritish->저장기값[4]) 주소출력(fayl_kiritish->저장기값[4], fayl_kiritish->저장기값[5], 수용량, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return o_lchov;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t 수용량;
        o_lchov = 주소출력검사(SECOND_VALUE, belgi_kodi, &수용량); if (o_lchov) return o_lchov;
        주소출력(SECOND_VALUE,belgi_kodi,수용량,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in manzil;
        o_lchov=주소입력(SECOND_VALUE,belgi_kodi,&manzil);if(o_lchov)return o_lchov;
        return 자바흐름연결(첫째값,pk_htonl(manzil.sin_addr.s_addr),pk_htons(manzil.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||belgi_kodi)return -95;o_lchov=자바흐름연결받기(첫째값);if(o_lchov>=40&&o_lchov<56)통신끝점들[o_lchov-32]=1;return o_lchov;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t 체계호출(foydalanuvchi_kadr *fayl_kiritish) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(fayl_kiritish) : 자체체계호출(fayl_kiritish);
}
static void qaytarish_o_zak(foydalanuvchi_kadr *fayl_kiritish, int o_lchov) {
    To_xtatish_TANAFFUS();
    fayl_kiritish->저장기값[0] = (uint64_t)(int64_t)o_lchov;
    fayl_kiritish->buyruq_holat = (uintptr_t)foydalanuvchi_qaytarish;
    fayl_kiritish->holat_kod = 0x3c5; // EL1h, DAIF masked
}
int foydalanuvchi_istisno(foydalanuvchi_kadr *fayl_kiritish, unsigned kesish) {
    if (!faol || (fayl_kiritish->holat_kod & 15) != 0) return 0;
    if (kesish) {
        uint32_t 승인값 = 기계저장기(IRQ_CPU_interfeys + 0xc), identifikator_VALUE = 승인값 & 1023;
        if (identifikator_VALUE == 30) { qaytarish_o_zak(fayl_kiritish, foydalanuvchi_TANAFFUS); 기계저장기(IRQ_CPU_interfeys + 0x10) = 승인값; return 1; }
        if (identifikator_VALUE < 1020) 기계저장기(IRQ_CPU_interfeys + 0x10) = 승인값;
        return 1;
    }
    uint64_t istisno_holat; __asm__ volatile("mrs %0, esr_el1" : "=r"(istisno_holat));
    if (Soat_VALUE() >= 마감시각) { qaytarish_o_zak(fayl_kiritish, foydalanuvchi_TANAFFUS); return 1; }
    unsigned istisno_toifa = istisno_holat >> 26;
    if (istisno_toifa == 0x15 && (istisno_holat & 0xffff) == 0) {
        if (리눅스규약 ? fayl_kiritish->저장기값[8] == 93 || fayl_kiritish->저장기값[8] == 94 : fayl_kiritish->저장기값[8] == 6) qaytarish_o_zak(fayl_kiritish, (int)(fayl_kiritish->저장기값[0] & 255));
        else {
            intptr_t o_lchov=체계호출(fayl_kiritish);
            if(o_lchov==-4096&&o_zaro_faol){
                저장값[egasi_obyekt].실행틀=*fayl_kiritish;저장값[egasi_obyekt].실행틀.buyruq_holat-=4;
                사용자실수보관(저장값[egasi_obyekt].실수저장상태);qaytarish_o_zak(fayl_kiritish,사용자중단됨);
            }else fayl_kiritish->저장기값[0]=(uint64_t)o_lchov;
        }
    } else qaytarish_o_zak(fayl_kiritish, istisno_toifa == 0x24 ? foydalanuvchi_ma_lumotlar_xato : istisno_toifa == 0x20 ? 사용자실행오류 : foydalanuvchi_xato_qo_llanma);
    return 1;
}

// 생성된 const ELF Guruh_VALUE: 실행은 반드시 ilova_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *ma_lumotlar; size_t Hajmi; unsigned 전달값; } ilova;
#include "programs.h"
static void *kadr_f57035a1(unsigned holat_INDEX){return (void *)(0x04000000ul+holat_INDEX*(foydalanuvchi_to_xtatmoq-foydalanuvchi_BASE));}
static int Tugatmoq_ilova(int o_lchov){
    사용자누적시각[egasi_obyekt]+=(uint32_t)보드밀리초()-사용자실행시각[egasi_obyekt];
    To_xtatish_TANAFFUS();faol=0;
    if(o_lchov==사용자중단됨){
        저장된작업 *satr_ma_lumotlar=&저장값[egasi_obyekt];satr_ma_lumotlar->멈춤상태=1;satr_ma_lumotlar->o_zaro_faol=o_zaro_faol;satr_ma_lumotlar->리눅스규약=리눅스규약;satr_ma_lumotlar->동적기억공간=동적기억끝;satr_ma_lumotlar->인수개수=전달인수개수;
        memcpy(satr_ma_lumotlar->Ruxsatlar_Ro_yxat,Ruxsatlar_Ro_yxat,sizeof(Ruxsatlar_Ro_yxat));memcpy(satr_ma_lumotlar->fayl_Ro_yxat,fayl_Ro_yxat,sizeof(fayl_Ro_yxat));memcpy(satr_ma_lumotlar->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(satr_ma_lumotlar->dalil_ARRAY,전달인수,sizeof(전달인수));memcpy(satr_ma_lumotlar->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<foydalanuvchi_sahifa_COUNT;순번++)if(Ruxsatlar_Ro_yxat[순번])memcpy((unsigned char *)kadr_f57035a1(egasi_obyekt)+순번*sahifa_o_lchami,(void *)(foydalanuvchi_BASE+순번*sahifa_o_lchami),sahifa_o_lchami);
    }else{
        저장값[egasi_obyekt].멈춤상태=0;화면초기화(egasi_obyekt);
        for(unsigned 순번=0;순번<16;순번++)if(fayl_Ro_yxat[순번]>=0)pk_close(fayl_Ro_yxat[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<foydalanuvchi_sahifa_COUNT;순번++){sahifa_Ro_yxat[순번]=0;Ruxsatlar_Ro_yxat[순번]=0;}변환표맞추기();return o_lchov;
}
uintptr_t yozuv_taxtasi_foydalanuvchi_nazorati(uintptr_t Amal){
    unsigned holat_INDEX=Amal&15;if(holat_INDEX>=4||faol)return (uint32_t)-22;
    저장된작업 *satr_ma_lumotlar=&저장값[holat_INDEX];
    if(Amal>=32){if(satr_ma_lumotlar->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(satr_ma_lumotlar->fayl_Ro_yxat[순번]>=0)pk_close(satr_ma_lumotlar->fayl_Ro_yxat[순번]);for(unsigned 순번=0;순번<24;순번++)if(satr_ma_lumotlar->통신끝점들[순번])통신끝점닫기(순번+32);}satr_ma_lumotlar->멈춤상태=0;화면초기화(holat_INDEX);return 0;}
    if(Amal>=16)return satr_ma_lumotlar->멈춤상태;
    if(!satr_ma_lumotlar->멈춤상태)return (uint32_t)-22;
    egasi_obyekt=holat_INDEX;o_zaro_faol=satr_ma_lumotlar->o_zaro_faol;리눅스규약=satr_ma_lumotlar->리눅스규약;동적기억끝=satr_ma_lumotlar->동적기억공간;전달인수개수=satr_ma_lumotlar->인수개수;
    memcpy(fayl_Ro_yxat,satr_ma_lumotlar->fayl_Ro_yxat,sizeof(fayl_Ro_yxat));memcpy(통신끝점들,satr_ma_lumotlar->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,satr_ma_lumotlar->dalil_ARRAY,sizeof(전달인수));memcpy(전달인수길이,satr_ma_lumotlar->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<foydalanuvchi_sahifa_COUNT;순번++)sahifa_Ro_yxat[순번]=(foydalanuvchi_BASE+순번*sahifa_o_lchami)|o_zak_sahifa;변환표맞추기();
    memset((void *)foydalanuvchi_BASE,0,foydalanuvchi_to_xtatmoq-foydalanuvchi_BASE);
    for(unsigned 순번=0;순번<foydalanuvchi_sahifa_COUNT;순번++)if(satr_ma_lumotlar->Ruxsatlar_Ro_yxat[순번])memcpy((void *)(foydalanuvchi_BASE+순번*sahifa_o_lchami),(unsigned char *)kadr_f57035a1(holat_INDEX)+순번*sahifa_o_lchami,sahifa_o_lchami);
    memcpy(Ruxsatlar_Ro_yxat,satr_ma_lumotlar->Ruxsatlar_Ro_yxat,sizeof(Ruxsatlar_Ro_yxat));
    for(unsigned 순번=0;순번<foydalanuvchi_sahifa_COUNT;순번++){unsigned ma_lumotlar_holat=Ruxsatlar_Ro_yxat[순번];sahifa_Ro_yxat[순번]=ma_lumotlar_holat?(foydalanuvchi_BASE+순번*sahifa_o_lchami)|(ma_lumotlar_holat==3?foydalanuvchi_o_qish_yozish_mumkin:ma_lumotlar_holat==5?사용자읽고실행:foydalanuvchi_faqat_o_qish_uchun):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");faol=1;satr_ma_lumotlar->멈춤상태=0;Start_TANAFFUS();
    사용자실행시각[egasi_obyekt]=보드밀리초();
    return (uint32_t)Tugatmoq_ilova(foydalanuvchi_CV(&satr_ma_lumotlar->실행틀,satr_ma_lumotlar->실수저장상태));
}
static int ishlash_ilova(const unsigned char *ma_lumotlar, size_t Hajmi, unsigned 전달값, int 리눅스방식, const char *Nomi) {
    if (faol) return -16;
    egasi_obyekt=yozuv_taxtasi_Terminal(11);if(egasi_obyekt<0||egasi_obyekt>3||저장값[egasi_obyekt].멈춤상태)return -16;o_zaro_faol=0;
    int 유효함 = 실행파일검사(ma_lumotlar, Hajmi, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned nom_INDEX=0;
    while (*Nomi && nom_INDEX<31) foydalanuvchi_buyruq_nom[egasi_obyekt][nom_INDEX++]=(unsigned char)*Nomi++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (nom_INDEX) foydalanuvchi_buyruq_nom[egasi_obyekt][nom_INDEX++]=' ';
        for (unsigned holat_INDEX=0; holat_INDEX<전달인수길이[0]; holat_INDEX++) foydalanuvchi_buyruq_nom[egasi_obyekt][nom_INDEX++]=전달인수[0][holat_INDEX];
    }
    foydalanuvchi_buyruq_nom[egasi_obyekt][nom_INDEX]=0; foydalanuvchi_raqami[egasi_obyekt]=Keyingi_foydalanuvchi_raqami++;
    if (Keyingi_foydalanuvchi_raqami>0x7fffffffu) Keyingi_foydalanuvchi_raqami=10;
    foydalanuvchi_Start_TIME[egasi_obyekt]=보드밀리초(); 사용자누적시각[egasi_obyekt]=0;
    for (unsigned 순번 = 0; 순번 < foydalanuvchi_sahifa_COUNT; 순번++) sahifa_Ro_yxat[순번] = (foydalanuvchi_BASE + 순번 * sahifa_o_lchami) | o_zak_sahifa;
    변환표맞추기();
    memset((void *)foydalanuvchi_BASE, 0, foydalanuvchi_to_xtatmoq - foydalanuvchi_BASE);
    memset(Ruxsatlar_Ro_yxat, 0, sizeof(Ruxsatlar_Ro_yxat));
    실행파일머리 실행머리; memcpy(&실행머리, ma_lumotlar, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.ilova_Sarlavha_COUNT; 순번++) {
        실행파일구획 ma_lumotlar_holat; memcpy(&ma_lumotlar_holat, ma_lumotlar + 실행머리.ilova_Sarlavha_OFFSET + 순번 * sizeof(ma_lumotlar_holat), sizeof(ma_lumotlar_holat));
        if (ma_lumotlar_holat.TYPE_toifa != 1 || !ma_lumotlar_holat.기억영역크기) continue;
        if (ma_lumotlar_holat.파일영역크기) memcpy((void *)(uintptr_t)ma_lumotlar_holat.manzil, ma_lumotlar + ma_lumotlar_holat.OFFSET_VALUE, ma_lumotlar_holat.파일영역크기);
        for (uintptr_t 현재위치 = ma_lumotlar_holat.manzil & ~(sahifa_o_lchami - 1); 현재위치 < ma_lumotlar_holat.manzil + ma_lumotlar_holat.기억영역크기; 현재위치 += sahifa_o_lchami) {
            Ruxsatlar_Ro_yxat[(현재위치 - foydalanuvchi_BASE) / sahifa_o_lchami] = (ma_lumotlar_holat.tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati & 2) ? 3 : ((ma_lumotlar_holat.tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = foydalanuvchi_Stack_manzil; 현재위치 < foydalanuvchi_to_xtatmoq; 현재위치 += sahifa_o_lchami) Ruxsatlar_Ro_yxat[(현재위치 - foydalanuvchi_BASE) / sahifa_o_lchami] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.kiritish_nuqta) : foydalanuvchi_to_xtatmoq;
    for (unsigned 순번 = 0; 순번 < foydalanuvchi_sahifa_COUNT; 순번++) {
        unsigned ruxsatlar = Ruxsatlar_Ro_yxat[순번];
        sahifa_Ro_yxat[순번] = ruxsatlar ? (foydalanuvchi_BASE + 순번 * sahifa_o_lchami) | (ruxsatlar == 3 ? foydalanuvchi_o_qish_yozish_mumkin : ruxsatlar == 5 ? 사용자읽고실행 : foydalanuvchi_faqat_o_qish_uchun) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) fayl_Ro_yxat[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = foydalanuvchi_rasm_to_xtatmoq;
    faol = 1; Start_TANAFFUS();
    사용자실행시각[egasi_obyekt]=보드밀리초();
    int o_lchov = foydalanuvchi_kiritmoq(실행머리.kiritish_nuqta, 초기쌓임공간, 전달값);
    return Tugatmoq_ilova(o_lchov);
}
uintptr_t yozuv_taxtasi_foydalanuvchi_ishlash(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Nomi=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)ishlash_ilova(실행항목들[LOOKUP_INDEX].ma_lumotlar, 실행항목들[LOOKUP_INDEX].Hajmi, 실행항목들[LOOKUP_INDEX].전달값, 0, Nomi);
}
static uintptr_t bajarmoq_fayl(int 리눅스방식) {
    static unsigned char rasm[16384];
    if (faol || !전달인수개수) return (uint32_t)-22;
    int fayl_deskriptor = pk_open((const char *)전달인수[0], faqat_o_qish_uchun_VALUE, 0);
    if (fayl_deskriptor < 0) return (uint32_t)-오류번호;
    int Hajmi = pk_size(fayl_deskriptor);
    if (Hajmi < 0 || (unsigned)Hajmi > sizeof(rasm)) { pk_close(fayl_deskriptor); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(fayl_deskriptor, rasm, Hajmi); pk_close(fayl_deskriptor);
    if (RECEIVED_COUNT != Hajmi) return (uint32_t)-5;
    return (uint32_t)ishlash_ilova(rasm, Hajmi, 0, 리눅스방식, "");
}
uintptr_t yozuv_taxtasi_foydalanuvchi_fayl(void) { return bajarmoq_fayl(0); }
uintptr_t 보드사용자리눅스파일(void) { return bajarmoq_fayl(1); }
uintptr_t yozuv_taxtasi_foydalanuvchi_tasdiqlash(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].ma_lumotlar, 잘못된실행항목들[순번].Hajmi) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
