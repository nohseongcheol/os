#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 laksanakan_perintah mesin lapisan_VALUE. Fail data/정책은 기존 AOT Java 커널에 위임한다.
#include "ruang_pengguna.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../rangkaian_tindan/rangkaian_tindan.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define mesin_daftar(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_pengagih 0xff841000ul
#define IRQ_CPU_antara_muka 0xff842000ul
#define saiz_halaman 4096ul
#define capai_penanda (1ul << 10)
#define tidak_laksanakan_keizinan (1ul << 53)
#define pengguna_tidak_laksanakan (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | capai_penanda)
#define kernel_halaman (3ul | 보통기억 | tidak_laksanakan_keizinan | pengguna_tidak_laksanakan)
#define pengguna_baca_tulis (3ul | 보통기억 | (1ul << 6) | tidak_laksanakan_keizinan | pengguna_tidak_laksanakan)
#define pengguna_baca_sahaja (3ul | 보통기억 | (3ul << 6) | tidak_laksanakan_keizinan | pengguna_tidak_laksanakan)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | tidak_laksanakan_keizinan)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Papan_pel(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Papan_Terminal(uintptr_t);
extern int Terminal_belum_selesai(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int pengguna_CV(pengguna_bingkai *,void *);
extern void 사용자실수보관(void *);
extern int pengguna_masuk(uintptr_t titik_permulaan, uintptr_t ingatan_tindanan, uintptr_t 전달값);
extern void pengguna_kembalikan(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t akar_e_mel[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t halaman_Senarai[pengguna_halaman_COUNT] __attribute__((aligned(4096)));
static uint8_t Keizinan_Senarai[pengguna_halaman_COUNT];
static int Ada, fail_Senarai[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned fail_pemegang){return fail_pemegang<40?자바전문닫기(fail_pemegang):자바흐름닫기(fail_pemegang);}
static uint64_t FREQUENCY, 마감시각;
static uintptr_t timbunan_tamat;
// kernel_VALUE 셸이 준비한 UTF-8 인수. EL0에는 tika_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,interaktif,리눅스규약,fail_Senarai[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argumen_ARRAY[8][256],Keizinan_Senarai[pengguna_halaman_COUNT];
    uintptr_t ingatan_dinamik; pengguna_bingkai 실행틀;
    unsigned char 실수저장상태[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int pemilik_objek,interaktif;
static uint32_t nombor_pengguna[4], pengguna_Mula_TIME[4], 사용자누적시각[4], 사용자실행시각[4], Seterusnya_nombor_pengguna=10;
static unsigned char pengguna_perintah_nama[4][288];
uint32_t 사용자상태읽기(unsigned pemasukan_VALUE, unsigned INDEX) {
    unsigned jawatan_INDEX=INDEX&3;
    int status_VALUE=(Ada && pemilik_objek==(int)jawatan_INDEX) ? 1 : 저장값[jawatan_INDEX].멈춤상태 ? 2 : 0;
    if (pemasukan_VALUE==0) return status_VALUE;
    if (!status_VALUE) return 0;
    if (pemasukan_VALUE==1) return nombor_pengguna[jawatan_INDEX];
    if (pemasukan_VALUE==2) {
        unsigned char *쪽들=status_VALUE==1?Keizinan_Senarai:저장값[jawatan_INDEX].Keizinan_Senarai;
        unsigned halaman_COUNT=0; for (unsigned 순번=0; 순번<pengguna_halaman_COUNT; 순번++) if(쪽들[순번]) halaman_COUNT++;
        return halaman_COUNT*4;
    }
    if (pemasukan_VALUE==3) return (uint32_t)보드밀리초()-pengguna_Mula_TIME[jawatan_INDEX];
    if (pemasukan_VALUE==4) return 사용자누적시각[jawatan_INDEX]+(status_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[jawatan_INDEX]:0);
    if (pemasukan_VALUE==5) return INDEX/4<sizeof(pengguna_perintah_nama[0])?pengguna_perintah_nama[jawatan_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t pemasukan_COUNT) {
    if (Ada || pemasukan_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = pemasukan_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t Carian_INDEX, uintptr_t 현재위치, uintptr_t bait_data) {
    if (Ada || Carian_INDEX >= 전달인수개수 || 현재위치 >= 255 || 현재위치 != 전달인수길이[Carian_INDEX] || !bait_data || bait_data > 255)
        return (uint32_t)-22;
    전달인수[Carian_INDEX][현재위치] = bait_data;
    전달인수길이[Carian_INDEX] = 현재위치 + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Jam_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Henti_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    mesin_daftar(IRQ_pengagih + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void Mula_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, mendayakan = 1;
    마감시각 = Jam_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(mendayakan) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned blok_data = 0; blok_data < 4; blok_data++) {
        akar_e_mel[blok_data] = (uintptr_t)가운데[blok_data] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t e_mel = ((uintptr_t)blok_data << 30) | ((uintptr_t)순번 << 21);
            가운데[blok_data][순번] = e_mel | 1 | capai_penanda | pengguna_tidak_laksanakan;
            if (e_mel >= 0xfc000000ul) 가운데[blok_data][순번] |= tidak_laksanakan_keizinan; // Device-nGnRnE
            else 가운데[blok_data][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < pengguna_halaman_COUNT / 512; SECOND_VALUE++)
        가운데[0][(pengguna_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(halaman_Senarai + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < pengguna_halaman_COUNT; 순번++) halaman_Senarai[순번] = (pengguna_BASE + 순번 * saiz_halaman) | kernel_halaman;
    uint64_t Memori_atribut_daftar = 0x4400, e_mel_Terjemahan_kawalan = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Memori_atribut_daftar), "r"(e_mel_Terjemahan_kawalan), "r"((uintptr_t)akar_e_mel) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t 실수저장상태 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(실수저장상태) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Henti_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 titik_permulaan_VALUE 때만 Izin_VALUE.
    mesin_daftar(IRQ_pengagih) = 0;
    mesin_daftar(IRQ_pengagih + 0x180) = 0xffffffff;
    mesin_daftar(IRQ_pengagih + 0x80) = 0xffffffff;
    mesin_daftar(IRQ_pengagih + 0x280) = 1u << 30;
    mesin_daftar(IRQ_pengagih + 0x41c) = 0x80808080;
    mesin_daftar(IRQ_pengagih + 0x100) = 1u << 30;
    mesin_daftar(IRQ_CPU_antara_muka + 4) = 0xff;
    mesin_daftar(IRQ_CPU_antara_muka + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Keselamatan = (mesin_daftar(IRQ_pengagih + 4) & (1u << 10)) != 0;
    mesin_daftar(IRQ_pengagih) = Keselamatan ? 1 : 3;
    mesin_daftar(IRQ_CPU_antara_muka) = Keselamatan ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_bidang, mesin_TYPE; uint32_t nombor_versi;
    uint64_t titik_permulaan, aplikasi_Pengepala_Ofset, seksyen_Pengepala_Ofset; uint32_t konfigurasi_Background_Intelligent_Transfer_Service;
    uint16_t fail_boleh_laku_Pengepala_saiz, aplikasi_Pengepala_pemasukan_saiz, aplikasi_Pengepala_COUNT, seksyen_Pengepala_pemasukan_saiz, seksyen_Pengepala_COUNT, seksyen_nama_jadual_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_bidang, konfigurasi_Background_Intelligent_Transfer_Service; uint64_t Ofset_VALUE, e_mel, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(pengguna_bingkai) == 272, "exception assembly layout");
static int 포함된범위(uint64_t Ofset_VALUE, uint64_t Saiz, uint64_t tamat_Ofset) {
    return Ofset_VALUE <= tamat_Ofset && Saiz <= tamat_Ofset - Ofset_VALUE;
}
static int 부가정보검사(const unsigned char *data_jawatan, size_t Saiz) {
    size_t 현재위치 = 0;
    while (포함된범위(현재위치, 12, Saiz)) {
        uint32_t 낱말들[3]; memcpy(낱말들, data_jawatan + 현재위치, 12); 현재위치 += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(현재위치, 이름영역크기, Saiz) || !포함된범위(현재위치 + 이름영역크기, 설명크기, Saiz)) return 0;
        const unsigned char Nama[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Nama) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Nama); 순번++) if (data_jawatan[현재위치 + 순번] != Nama[순번]) 일치 = 0;
        uint32_t nombor_versi = 0;
        if (일치) memcpy(&nombor_versi, data_jawatan + 현재위치 + 이름영역크기, 4);
        if (일치 && nombor_versi == 1) return 1;
        현재위치 += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *data, size_t Saiz, int 리눅스방식) {
    if (Saiz < sizeof(실행파일머리)) return pengguna_fail_boleh_laku_ralat;
    실행파일머리 fail_boleh_laku_Pengepala; memcpy(&fail_boleh_laku_Pengepala, data, sizeof(fail_boleh_laku_Pengepala));
    if (fail_boleh_laku_Pengepala.형식식별[0] != 127 || fail_boleh_laku_Pengepala.형식식별[1] != 'E' || fail_boleh_laku_Pengepala.형식식별[2] != 'L' || fail_boleh_laku_Pengepala.형식식별[3] != 'F' ||
        fail_boleh_laku_Pengepala.형식식별[4] != 2 || fail_boleh_laku_Pengepala.형식식별[5] != 1 || fail_boleh_laku_Pengepala.형식식별[6] != 1 || (fail_boleh_laku_Pengepala.형식식별[7] != 0 && (!리눅스방식 || fail_boleh_laku_Pengepala.형식식별[7] != 3)) ||
        fail_boleh_laku_Pengepala.TYPE_bidang != 2 || fail_boleh_laku_Pengepala.mesin_TYPE != 183 || fail_boleh_laku_Pengepala.nombor_versi != 1 || fail_boleh_laku_Pengepala.konfigurasi_Background_Intelligent_Transfer_Service || fail_boleh_laku_Pengepala.fail_boleh_laku_Pengepala_saiz != sizeof(fail_boleh_laku_Pengepala) ||
        fail_boleh_laku_Pengepala.aplikasi_Pengepala_pemasukan_saiz != sizeof(실행파일구획) || !fail_boleh_laku_Pengepala.aplikasi_Pengepala_COUNT || fail_boleh_laku_Pengepala.aplikasi_Pengepala_COUNT > 16 ||
        fail_boleh_laku_Pengepala.aplikasi_Pengepala_Ofset < sizeof(fail_boleh_laku_Pengepala) || !포함된범위(fail_boleh_laku_Pengepala.aplikasi_Pengepala_Ofset, (uint64_t)fail_boleh_laku_Pengepala.aplikasi_Pengepala_COUNT * sizeof(실행파일구획), Saiz)) return pengguna_fail_boleh_laku_ralat;
    uint8_t 사용량[(pengguna_imej_tamat - pengguna_BASE) / saiz_halaman] = {0};
    int sah_titik_permulaan = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < fail_boleh_laku_Pengepala.aplikasi_Pengepala_COUNT; 순번++) {
        실행파일구획 data_jawatan; memcpy(&data_jawatan, data + fail_boleh_laku_Pengepala.aplikasi_Pengepala_Ofset + 순번 * sizeof(data_jawatan), sizeof(data_jawatan));
        if (data_jawatan.TYPE_bidang == 4) {
            if (!포함된범위(data_jawatan.Ofset_VALUE, data_jawatan.파일영역크기, Saiz)) return pengguna_fail_boleh_laku_ralat;
            if (부가정보검사(data + data_jawatan.Ofset_VALUE, data_jawatan.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (data_jawatan.TYPE_bidang == 0 || data_jawatan.TYPE_bidang == 6 || (data_jawatan.TYPE_bidang == 0x6474e551 && !(data_jawatan.konfigurasi_Background_Intelligent_Transfer_Service & 1))) continue;
        if (data_jawatan.TYPE_bidang != 1) return pengguna_fail_boleh_laku_ralat; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!data_jawatan.기억영역크기) continue;
        if (data_jawatan.konfigurasi_Background_Intelligent_Transfer_Service & ~7u || !(data_jawatan.konfigurasi_Background_Intelligent_Transfer_Service & 4) || (data_jawatan.konfigurasi_Background_Intelligent_Transfer_Service & 3) == 3 || data_jawatan.파일영역크기 > data_jawatan.기억영역크기 ||
            (data_jawatan.파일영역크기 && !포함된범위(data_jawatan.Ofset_VALUE, data_jawatan.파일영역크기, Saiz)) || data_jawatan.e_mel < pengguna_BASE ||
            !포함된범위(data_jawatan.e_mel, data_jawatan.기억영역크기, pengguna_imej_tamat) ||
            (!리눅스방식 && ((data_jawatan.e_mel & (saiz_halaman - 1)) || (data_jawatan.Ofset_VALUE & (saiz_halaman - 1)) || data_jawatan.맞춤 != saiz_halaman)) ||
            (리눅스방식 && (((data_jawatan.e_mel ^ data_jawatan.Ofset_VALUE) & (saiz_halaman - 1)) || !data_jawatan.맞춤 ||
                (data_jawatan.맞춤 & (data_jawatan.맞춤 - 1)) || data_jawatan.맞춤 > 0x200000 || ((data_jawatan.e_mel ^ data_jawatan.Ofset_VALUE) & (data_jawatan.맞춤 - 1))))) return pengguna_fail_boleh_laku_ralat;
        unsigned 첫항목 = (data_jawatan.e_mel - pengguna_BASE) / saiz_halaman;
        unsigned pemasukan_COUNT = ((data_jawatan.e_mel & (saiz_halaman - 1)) + data_jawatan.기억영역크기 + saiz_halaman - 1) / saiz_halaman;
        for (unsigned halaman_VALUE = 첫항목; halaman_VALUE < 첫항목 + pemasukan_COUNT; halaman_VALUE++) {
            if (사용량[halaman_VALUE]) return pengguna_fail_boleh_laku_ralat;
            사용량[halaman_VALUE] = 1;
        }
        if ((data_jawatan.konfigurasi_Background_Intelligent_Transfer_Service & 1) && fail_boleh_laku_Pengepala.titik_permulaan >= data_jawatan.e_mel && fail_boleh_laku_Pengepala.titik_permulaan < data_jawatan.e_mel + data_jawatan.파일영역크기 && !(fail_boleh_laku_Pengepala.titik_permulaan & 3)) sah_titik_permulaan = 1;
        적재구획++;
    }
    return sah_titik_permulaan && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : pengguna_fail_boleh_laku_ralat;
}
int 사용자실행파일검사(const unsigned char *data, size_t Saiz) { return 실행파일검사(data, Saiz, 0); }
static void tataletak_halaman(uintptr_t e_mel, uint64_t konfigurasi_Background_Intelligent_Transfer_Service, unsigned keizinan) {
    unsigned Carian_INDEX = (e_mel - pengguna_BASE) / saiz_halaman;
    halaman_Senarai[Carian_INDEX] = e_mel | konfigurasi_Background_Intelligent_Transfer_Service;
    Keizinan_Senarai[Carian_INDEX] = keizinan;
}
static int pengguna_julat(uintptr_t e_mel, size_t pemasukan_COUNT, int 쓰는중) {
    if (e_mel < pengguna_BASE || !포함된범위(e_mel, pemasukan_COUNT, pengguna_tamat)) return 0;
    if (!pemasukan_COUNT) return 1;
    unsigned 첫항목 = (e_mel - pengguna_BASE) / saiz_halaman, 마지막 = (e_mel + pemasukan_COUNT - 1 - pengguna_BASE) / saiz_halaman;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Keizinan_Senarai[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int tika_laluan(uintptr_t e_mel, char *LALUAN) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!pengguna_julat(e_mel, 1, 0)) return -14;
        LALUAN[순번] = *(const char *)e_mel++;
        if (!LALUAN[순번]) return 0;
    }
    return -36;
}
static intptr_t kernel_ukuran(intptr_t ukuran) { return ukuran < 0 ? -오류번호 : ukuran; }
static int 대응파일기술자(uint64_t fail_pemegang) { return fail_pemegang >= 3 && fail_pemegang < 19 ? fail_Senarai[fail_pemegang - 3] : -1; }
static int 통신끝점소유(uint64_t fail_pemegang) { return fail_pemegang >= 32 && fail_pemegang < 56 && 통신끝점들[fail_pemegang - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t kepanjangan_VALUE, struct pk_sockaddr_in *e_mel) {
    if (kepanjangan_VALUE != sizeof(*e_mel)) return -22;
    if (!pengguna_julat(가리킴값, kepanjangan_VALUE, 0)) return -14;
    memcpy(e_mel, (const void *)가리킴값, sizeof(*e_mel));
    return e_mel->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t kepanjangan_penuding, pk_socklen_t *penimbal_kapasiti) {
    if (!pengguna_julat(kepanjangan_penuding, sizeof(*penimbal_kapasiti), 1)) return -14;
    memcpy(penimbal_kapasiti, (const void *)kepanjangan_penuding, sizeof(*penimbal_kapasiti));
    if (*penimbal_kapasiti > sizeof(struct pk_sockaddr_in)) *penimbal_kapasiti = sizeof(struct pk_sockaddr_in);
    if (*penimbal_kapasiti && !pengguna_julat(가리킴값, *penimbal_kapasiti, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t kepanjangan_penuding, pk_socklen_t penimbal_kapasiti, int e_mel, int nombor_port) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(nombor_port); VALUE.sin_addr.s_addr = pk_htonl(e_mel);
    if (penimbal_kapasiti) memcpy((void *)가리킴값, &VALUE, penimbal_kapasiti);
    pk_socklen_t kepanjangan_VALUE = sizeof(VALUE); memcpy((void *)kepanjangan_penuding, &kepanjangan_VALUE, sizeof(kepanjangan_VALUE));
}
extern uintptr_t Papan_Saluran(uintptr_t, uintptr_t);
static intptr_t asal_sistem_CALL(pengguna_bingkai *fail_pemasukan) {
    uintptr_t 첫째값 = fail_pemasukan->daftar_data[0], SECOND_VALUE = fail_pemasukan->daftar_data[1], titik_kod = fail_pemasukan->daftar_data[2];
    char LALUAN[65];
    int fail_pemegang, ukuran;
    switch (fail_pemasukan->daftar_data[8]) {
    case 0: return 1; // Asli ABI 버전
    case 1: // write: penuding 전체를 검사한 BACK_VALUE 출력/Fail ubah_VALUE
        if (titik_kod > 65536) return -22;
        if (!pengguna_julat(SECOND_VALUE, titik_kod, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Jam_VALUE();
            for (size_t 순번 = 0; 순번 < titik_kod; 순번++) Papan_Saluran(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 kernel_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interaktif){
                마감시각+=Jam_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(마감시각) : "memory");
            }
            return titik_kod;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t item_COUNT=titik_kod>512?512:titik_kod;for(size_t 순번=0;순번<item_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,item_COUNT);
        }
        fail_pemegang = 대응파일기술자(첫째값); if (fail_pemegang < 0) return -9;
        return kernel_ukuran(pk_write(fail_pemegang, (const void *)SECOND_VALUE, titik_kod));
    case 2:
        if (titik_kod > 65536) return -22;
        if (!pengguna_julat(SECOND_VALUE, titik_kod, 1)) return -14;
        if (첫째값 == 0) {
            size_t item_COUNT = 0;
            while (item_COUNT < titik_kod) {
                int aksara_VALUE = (int32_t)보드글자읽기(); if (aksara_VALUE == -2) return item_COUNT; if (aksara_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[item_COUNT++] = aksara_VALUE;
            }
            return item_COUNT ? (intptr_t)item_COUNT : (titik_kod ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            ukuran=자바흐름읽기(첫째값,titik_kod>512?512:titik_kod);if(ukuran>0)for(int 순번=0;순번<ukuran;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return ukuran;
        }
        fail_pemegang = 대응파일기술자(첫째값); if (fail_pemegang < 0) return -9;
        return kernel_ukuran(pk_read(fail_pemegang, (void *)SECOND_VALUE, titik_kod));
    case 3:
        ukuran = tika_laluan(첫째값, LALUAN); if (ukuran) return ukuran;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (fail_Senarai[순번] < 0) {
            fail_pemegang = pk_open(LALUAN, (int)SECOND_VALUE, 0600);
            if (fail_pemegang < 0) return -오류번호;
            fail_Senarai[순번] = fail_pemegang; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { ukuran = 통신끝점닫기(첫째값); if (!ukuran) 통신끝점들[첫째값 - 32] = 0; return ukuran; }
        fail_pemegang = 대응파일기술자(첫째값); if (fail_pemegang < 0) return -9;
        ukuran = pk_close(fail_pemegang); if (!ukuran) fail_Senarai[첫째값 - 3] = -1;
        return kernel_ukuran(ukuran);
    case 5:
        fail_pemegang = 대응파일기술자(첫째값); if (fail_pemegang < 0) return -9;
        if (titik_kod > 2) return -22;
        return kernel_ukuran(pk_lseek(fail_pemegang, (int64_t)SECOND_VALUE, titik_kod));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 ruang_pengguna RW/NX timbunan_VALUE, 새로 노출되는 페이지는 0으로 mengasal
        if (!첫째값) return timbunan_tamat;
        if (첫째값 < pengguna_imej_tamat || 첫째값 > pengguna_timbunan_tamat) return -12;
        uintptr_t 이전쪽들 = (timbunan_tamat + saiz_halaman - 1) & ~(saiz_halaman - 1);
        uintptr_t 새쪽들 = (첫째값 + saiz_halaman - 1) & ~(saiz_halaman - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t data_jawatan = 이전쪽들; data_jawatan < 새쪽들; data_jawatan += saiz_halaman) tataletak_halaman(data_jawatan, kernel_halaman, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t data_jawatan = 이전쪽들; data_jawatan < 새쪽들; data_jawatan += saiz_halaman) tataletak_halaman(data_jawatan, pengguna_baca_tulis, 3);
        } else {
            for (uintptr_t data_jawatan = 새쪽들; data_jawatan < 이전쪽들; data_jawatan += saiz_halaman) {
                halaman_Senarai[(data_jawatan - pengguna_BASE) / saiz_halaman] = 0; Keizinan_Senarai[(data_jawatan - pengguna_BASE) / saiz_halaman] = 0;
            }
        }
        timbunan_tamat = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        fail_pemegang = 대응파일기술자(첫째값); return fail_pemegang < 0 ? -9 : kernel_ukuran(pk_size(fail_pemegang));
    case 10:
        fail_pemegang = 대응파일기술자(첫째값); return fail_pemegang < 0 ? -9 : kernel_ukuran(pk_ftruncate(fail_pemegang, (int64_t)SECOND_VALUE));
    case 11:
        ukuran = tika_laluan(첫째값, LALUAN); return ukuran ? ukuran : kernel_ukuran(pk_unlink(LALUAN));
    case 12:
        fail_pemegang = 대응파일기술자(첫째값); return fail_pemegang < 0 ? -9 : kernel_ukuran(pk_fsync(fail_pemegang));
    case 13: { // 그래픽 기초 API: ruang_pengguna 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = fail_pemasukan->daftar_data[3], 높이값 = fail_pemasukan->daftar_data[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t Y_koordinat = SECOND_VALUE; Y_koordinat < SECOND_VALUE + 높이값; Y_koordinat++) for (uintptr_t koordinat_x = 첫째값; koordinat_x < 첫째값 + 너비값; koordinat_x++) Papan_pel(koordinat_x, Y_koordinat, titik_kod);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=item_COUNT; args(index,buffer,capacity)=UTF-8 kepanjangan_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (titik_kod <= 전달인수길이[첫째값]) return -36;
        if (!pengguna_julat(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interaktif=1;return Papan_Terminal(13);}
        if(첫째값==2){interaktif=0;return 0;}
        if(첫째값==3)return Papan_Terminal(13);
        if(첫째값!=1||!interaktif)return -22;
        ukuran=(int32_t)보드글자읽기();
        if(ukuran==-4096)return ukuran;
        Mula_TIMEOUT();return ukuran<0?-11:ukuran;
    case 17: { // 유한한 협력 tunggu_VALUE: 통신 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t tamat_TIME = Jam_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Jam_VALUE() < tamat_TIME);
        Mula_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 부모·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        ukuran = tika_laluan(첫째값, LALUAN); if (ukuran) return ukuran;
        unsigned kepanjangan_VALUE = 0; while (LALUAN[kepanjangan_VALUE]) kepanjangan_VALUE++;
        ukuran = 자바경로시작(kepanjangan_VALUE); if (ukuran < 0) return ukuran;
        for (unsigned 순번 = 0; 순번 < kepanjangan_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)LALUAN[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int aksara_VALUE=(int32_t)보드글자읽기();if(aksara_VALUE==-4096)return aksara_VALUE;if(aksara_VALUE>=0)화면누름(pemilik_objek,aksara_VALUE);Mula_TIMEOUT();}
        if(첫째값==3&&titik_kod){if(!자바셸대화형())return -95;interaktif=1;Papan_Terminal(300);}
        return 화면호출(pemilik_objek,첫째값,SECOND_VALUE,titik_kod,fail_pemasukan->daftar_data[3],fail_pemasukan->daftar_data[4],fail_pemasukan->daftar_data[5]);
    case 21:
        if(titik_kod>127)return -22;if(!pengguna_julat(SECOND_VALUE,titik_kod*sizeof(uint32_t),0))return -14;
        return 화면글(pemilik_objek,첫째값,(const uint32_t *)SECOND_VALUE,titik_kod);
    case 22: // 화면 Saiz pertanyaan_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(titik_kod==0||titik_kod==6))ukuran=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(titik_kod==0||titik_kod==IPPROTO_UDP))ukuran=자바전문만들기(첫째값,SECOND_VALUE,titik_kod);
        else return -93;
        if (ukuran >= 32 && ukuran < 56) 통신끝점들[ukuran - 32] = 1;
        return ukuran;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in e_mel;
        ukuran = 주소입력(SECOND_VALUE, titik_kod, &e_mel); if (ukuran) return ukuran;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(e_mel.sin_addr.s_addr),pk_htons(e_mel.sin_port)):자바전문묶기(첫째값, pk_htonl(e_mel.sin_addr.s_addr), pk_htons(e_mel.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fail_pemasukan->daftar_data[3]) return -95;
        if (titik_kod > 512) return -90;
        if (titik_kod && !pengguna_julat(SECOND_VALUE, titik_kod, 0)) return -14;
        struct pk_sockaddr_in e_mel;
        ukuran = 주소입력(fail_pemasukan->daftar_data[4], fail_pemasukan->daftar_data[5], &e_mel); if (ukuran) return ukuran;
        for (unsigned 순번 = 0; 순번 < titik_kod; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(e_mel.sin_addr.s_addr), pk_htons(e_mel.sin_port), titik_kod);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (fail_pemasukan->daftar_data[3]) return -95;
        if (titik_kod > 512) return -90;
        if (titik_kod && !pengguna_julat(SECOND_VALUE, titik_kod, 1)) return -14;
        pk_socklen_t penimbal_kapasiti = 0;
        if (fail_pemasukan->daftar_data[4]) { ukuran = 주소출력검사(fail_pemasukan->daftar_data[4], fail_pemasukan->daftar_data[5], &penimbal_kapasiti); if (ukuran) return ukuran; }
        ukuran = 자바전문받기(첫째값, titik_kod); if (ukuran < 0) return ukuran;
        for (int 순번 = 0; 순번 < ukuran; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (fail_pemasukan->daftar_data[4]) 주소출력(fail_pemasukan->daftar_data[4], fail_pemasukan->daftar_data[5], penimbal_kapasiti, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return ukuran;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t penimbal_kapasiti;
        ukuran = 주소출력검사(SECOND_VALUE, titik_kod, &penimbal_kapasiti); if (ukuran) return ukuran;
        주소출력(SECOND_VALUE,titik_kod,penimbal_kapasiti,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in e_mel;
        ukuran=주소입력(SECOND_VALUE,titik_kod,&e_mel);if(ukuran)return ukuran;
        return 자바흐름연결(첫째값,pk_htonl(e_mel.sin_addr.s_addr),pk_htons(e_mel.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||titik_kod)return -95;ukuran=자바흐름연결받기(첫째값);if(ukuran>=40&&ukuran<56)통신끝점들[ukuran-32]=1;return ukuran;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t panggilan_sistem(pengguna_bingkai *fail_pemasukan) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(fail_pemasukan) : asal_sistem_CALL(fail_pemasukan);
}
static void kembalikan_kernel(pengguna_bingkai *fail_pemasukan, int ukuran) {
    Henti_TIMEOUT();
    fail_pemasukan->daftar_data[0] = (uint64_t)(int64_t)ukuran;
    fail_pemasukan->perintah_jawatan = (uintptr_t)pengguna_kembalikan;
    fail_pemasukan->status_kod = 0x3c5; // EL1h, DAIF masked
}
int pengguna_pengecualian(pengguna_bingkai *fail_pemasukan, unsigned pintasan) {
    if (!Ada || (fail_pemasukan->status_kod & 15) != 0) return 0;
    if (pintasan) {
        uint32_t 승인값 = mesin_daftar(IRQ_CPU_antara_muka + 0xc), 식별자 = 승인값 & 1023;
        if (식별자 == 30) { kembalikan_kernel(fail_pemasukan, pengguna_TIMEOUT); mesin_daftar(IRQ_CPU_antara_muka + 0x10) = 승인값; return 1; }
        if (식별자 < 1020) mesin_daftar(IRQ_CPU_antara_muka + 0x10) = 승인값;
        return 1;
    }
    uint64_t pengecualian_status; __asm__ volatile("mrs %0, esr_el1" : "=r"(pengecualian_status));
    if (Jam_VALUE() >= 마감시각) { kembalikan_kernel(fail_pemasukan, pengguna_TIMEOUT); return 1; }
    unsigned pengecualian_bidang = pengecualian_status >> 26;
    if (pengecualian_bidang == 0x15 && (pengecualian_status & 0xffff) == 0) {
        if (리눅스규약 ? fail_pemasukan->daftar_data[8] == 93 || fail_pemasukan->daftar_data[8] == 94 : fail_pemasukan->daftar_data[8] == 6) kembalikan_kernel(fail_pemasukan, (int)(fail_pemasukan->daftar_data[0] & 255));
        else {
            intptr_t ukuran=panggilan_sistem(fail_pemasukan);
            if(ukuran==-4096&&interaktif){
                저장값[pemilik_objek].실행틀=*fail_pemasukan;저장값[pemilik_objek].실행틀.perintah_jawatan-=4;
                사용자실수보관(저장값[pemilik_objek].실수저장상태);kembalikan_kernel(fail_pemasukan,사용자중단됨);
            }else fail_pemasukan->daftar_data[0]=(uint64_t)ukuran;
        }
    } else kembalikan_kernel(fail_pemasukan, pengecualian_bidang == 0x24 ? pengguna_data_ralat : pengecualian_bidang == 0x20 ? 사용자실행오류 : pengguna_tak_sah_suruhan);
    return 1;
}

// 생성된 const ELF Kumpulan_VALUE: 실행은 반드시 aplikasi_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *data; size_t Saiz; unsigned 전달값; } aplikasi;
#include "programs.h"
static void *gambar(unsigned jawatan_INDEX){return (void *)(0x04000000ul+jawatan_INDEX*(pengguna_tamat-pengguna_BASE));}
static int Tamat_aplikasi(int ukuran){
    사용자누적시각[pemilik_objek]+=(uint32_t)보드밀리초()-사용자실행시각[pemilik_objek];
    Henti_TIMEOUT();Ada=0;
    if(ukuran==사용자중단됨){
        저장된작업 *rentetan_data=&저장값[pemilik_objek];rentetan_data->멈춤상태=1;rentetan_data->interaktif=interaktif;rentetan_data->리눅스규약=리눅스규약;rentetan_data->ingatan_dinamik=timbunan_tamat;rentetan_data->인수개수=전달인수개수;
        memcpy(rentetan_data->Keizinan_Senarai,Keizinan_Senarai,sizeof(Keizinan_Senarai));memcpy(rentetan_data->fail_Senarai,fail_Senarai,sizeof(fail_Senarai));memcpy(rentetan_data->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(rentetan_data->argumen_ARRAY,전달인수,sizeof(전달인수));memcpy(rentetan_data->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<pengguna_halaman_COUNT;순번++)if(Keizinan_Senarai[순번])memcpy((unsigned char *)gambar(pemilik_objek)+순번*saiz_halaman,(void *)(pengguna_BASE+순번*saiz_halaman),saiz_halaman);
    }else{
        저장값[pemilik_objek].멈춤상태=0;화면초기화(pemilik_objek);
        for(unsigned 순번=0;순번<16;순번++)if(fail_Senarai[순번]>=0)pk_close(fail_Senarai[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<pengguna_halaman_COUNT;순번++){halaman_Senarai[순번]=0;Keizinan_Senarai[순번]=0;}변환표맞추기();return ukuran;
}
uintptr_t Papan_kawalan_pengguna(uintptr_t Aksi){
    unsigned jawatan_INDEX=Aksi&15;if(jawatan_INDEX>=4||Ada)return (uint32_t)-22;
    저장된작업 *rentetan_data=&저장값[jawatan_INDEX];
    if(Aksi>=32){if(rentetan_data->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(rentetan_data->fail_Senarai[순번]>=0)pk_close(rentetan_data->fail_Senarai[순번]);for(unsigned 순번=0;순번<24;순번++)if(rentetan_data->통신끝점들[순번])통신끝점닫기(순번+32);}rentetan_data->멈춤상태=0;화면초기화(jawatan_INDEX);return 0;}
    if(Aksi>=16)return rentetan_data->멈춤상태;
    if(!rentetan_data->멈춤상태)return (uint32_t)-22;
    pemilik_objek=jawatan_INDEX;interaktif=rentetan_data->interaktif;리눅스규약=rentetan_data->리눅스규약;timbunan_tamat=rentetan_data->ingatan_dinamik;전달인수개수=rentetan_data->인수개수;
    memcpy(fail_Senarai,rentetan_data->fail_Senarai,sizeof(fail_Senarai));memcpy(통신끝점들,rentetan_data->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,rentetan_data->argumen_ARRAY,sizeof(전달인수));memcpy(전달인수길이,rentetan_data->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<pengguna_halaman_COUNT;순번++)halaman_Senarai[순번]=(pengguna_BASE+순번*saiz_halaman)|kernel_halaman;변환표맞추기();
    memset((void *)pengguna_BASE,0,pengguna_tamat-pengguna_BASE);
    for(unsigned 순번=0;순번<pengguna_halaman_COUNT;순번++)if(rentetan_data->Keizinan_Senarai[순번])memcpy((void *)(pengguna_BASE+순번*saiz_halaman),(unsigned char *)gambar(jawatan_INDEX)+순번*saiz_halaman,saiz_halaman);
    memcpy(Keizinan_Senarai,rentetan_data->Keizinan_Senarai,sizeof(Keizinan_Senarai));
    for(unsigned 순번=0;순번<pengguna_halaman_COUNT;순번++){unsigned data_jawatan=Keizinan_Senarai[순번];halaman_Senarai[순번]=data_jawatan?(pengguna_BASE+순번*saiz_halaman)|(data_jawatan==3?pengguna_baca_tulis:data_jawatan==5?사용자읽고실행:pengguna_baca_sahaja):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Ada=1;rentetan_data->멈춤상태=0;Mula_TIMEOUT();
    사용자실행시각[pemilik_objek]=보드밀리초();
    return (uint32_t)Tamat_aplikasi(pengguna_CV(&rentetan_data->실행틀,rentetan_data->실수저장상태));
}
static int jalankan_aplikasi(const unsigned char *data, size_t Saiz, unsigned 전달값, int 리눅스방식, const char *Nama) {
    if (Ada) return -16;
    pemilik_objek=Papan_Terminal(11);if(pemilik_objek<0||pemilik_objek>3||저장값[pemilik_objek].멈춤상태)return -16;interaktif=0;
    int sah = 실행파일검사(data, Saiz, 리눅스방식); if (sah) return sah;
    리눅스규약 = 리눅스방식;
    unsigned nama_INDEX=0;
    while (*Nama && nama_INDEX<31) pengguna_perintah_nama[pemilik_objek][nama_INDEX++]=(unsigned char)*Nama++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (nama_INDEX) pengguna_perintah_nama[pemilik_objek][nama_INDEX++]=' ';
        for (unsigned jawatan_INDEX=0; jawatan_INDEX<전달인수길이[0]; jawatan_INDEX++) pengguna_perintah_nama[pemilik_objek][nama_INDEX++]=전달인수[0][jawatan_INDEX];
    }
    pengguna_perintah_nama[pemilik_objek][nama_INDEX]=0; nombor_pengguna[pemilik_objek]=Seterusnya_nombor_pengguna++;
    if (Seterusnya_nombor_pengguna>0x7fffffffu) Seterusnya_nombor_pengguna=10;
    pengguna_Mula_TIME[pemilik_objek]=보드밀리초(); 사용자누적시각[pemilik_objek]=0;
    for (unsigned 순번 = 0; 순번 < pengguna_halaman_COUNT; 순번++) halaman_Senarai[순번] = (pengguna_BASE + 순번 * saiz_halaman) | kernel_halaman;
    변환표맞추기();
    memset((void *)pengguna_BASE, 0, pengguna_tamat - pengguna_BASE);
    memset(Keizinan_Senarai, 0, sizeof(Keizinan_Senarai));
    실행파일머리 fail_boleh_laku_Pengepala; memcpy(&fail_boleh_laku_Pengepala, data, sizeof(fail_boleh_laku_Pengepala));
    for (unsigned 순번 = 0; 순번 < fail_boleh_laku_Pengepala.aplikasi_Pengepala_COUNT; 순번++) {
        실행파일구획 data_jawatan; memcpy(&data_jawatan, data + fail_boleh_laku_Pengepala.aplikasi_Pengepala_Ofset + 순번 * sizeof(data_jawatan), sizeof(data_jawatan));
        if (data_jawatan.TYPE_bidang != 1 || !data_jawatan.기억영역크기) continue;
        if (data_jawatan.파일영역크기) memcpy((void *)(uintptr_t)data_jawatan.e_mel, data + data_jawatan.Ofset_VALUE, data_jawatan.파일영역크기);
        for (uintptr_t 현재위치 = data_jawatan.e_mel & ~(saiz_halaman - 1); 현재위치 < data_jawatan.e_mel + data_jawatan.기억영역크기; 현재위치 += saiz_halaman) {
            Keizinan_Senarai[(현재위치 - pengguna_BASE) / saiz_halaman] = (data_jawatan.konfigurasi_Background_Intelligent_Transfer_Service & 2) ? 3 : ((data_jawatan.konfigurasi_Background_Intelligent_Transfer_Service & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 현재위치 = pengguna_tindan_e_mel; 현재위치 < pengguna_tamat; 현재위치 += saiz_halaman) Keizinan_Senarai[(현재위치 - pengguna_BASE) / saiz_halaman] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(fail_boleh_laku_Pengepala.titik_permulaan) : pengguna_tamat;
    for (unsigned 순번 = 0; 순번 < pengguna_halaman_COUNT; 순번++) {
        unsigned keizinan = Keizinan_Senarai[순번];
        halaman_Senarai[순번] = keizinan ? (pengguna_BASE + 순번 * saiz_halaman) | (keizinan == 3 ? pengguna_baca_tulis : keizinan == 5 ? 사용자읽고실행 : pengguna_baca_sahaja) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) fail_Senarai[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    timbunan_tamat = pengguna_imej_tamat;
    Ada = 1; Mula_TIMEOUT();
    사용자실행시각[pemilik_objek]=보드밀리초();
    int ukuran = pengguna_masuk(fail_boleh_laku_Pengepala.titik_permulaan, 초기쌓임공간, 전달값);
    return Tamat_aplikasi(ukuran);
}
uintptr_t Papan_pengguna_jalankan(uintptr_t Carian_INDEX) {
    if (Carian_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Nama=Carian_INDEX==10?"javac":Carian_INDEX==11?"java":Carian_INDEX==12?"python":Carian_INDEX==13?"vi":Carian_INDEX==14?"jar":Carian_INDEX==15?"cc":Carian_INDEX==16?"jaot":"ELF";
    return (uint32_t)jalankan_aplikasi(실행항목들[Carian_INDEX].data, 실행항목들[Carian_INDEX].Saiz, 실행항목들[Carian_INDEX].전달값, 0, Nama);
}
static uintptr_t laksanakan_fail(int 리눅스방식) {
    static unsigned char imej[16384];
    if (Ada || !전달인수개수) return (uint32_t)-22;
    int fail_pemegang = pk_open((const char *)전달인수[0], baca_sahaja_VALUE, 0);
    if (fail_pemegang < 0) return (uint32_t)-오류번호;
    int Saiz = pk_size(fail_pemegang);
    if (Saiz < 0 || (unsigned)Saiz > sizeof(imej)) { pk_close(fail_pemegang); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(fail_pemegang, imej, Saiz); pk_close(fail_pemegang);
    if (RECEIVED_COUNT != Saiz) return (uint32_t)-5;
    return (uint32_t)jalankan_aplikasi(imej, Saiz, 0, 리눅스방식, "");
}
uintptr_t Papan_pengguna_fail(void) { return laksanakan_fail(0); }
uintptr_t 보드사용자리눅스파일(void) { return laksanakan_fail(1); }
uintptr_t Papan_pengguna_sahkan(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].data, 잘못된실행항목들[순번].Saiz) != pengguna_fail_boleh_laku_ralat) return 순번 + 1;
    return 0;
}
