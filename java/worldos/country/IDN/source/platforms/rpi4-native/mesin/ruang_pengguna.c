#include "../명명/기계연결이름.h"
#include "화면정보.h"
// EL0 Jalankan_perintah mesin lapisan_VALUE. berkas data/정책은 기존 AOT Java 커널에 위임한다.
#include "ruang_pengguna.h"
#include "파일규약.h"
#include "통신규약.h"
#include "../jaringan_tumpuk/jaringan_tumpuk.h"
extern int32_t 자바전문원격주소(int32_t), 자바흐름주소(int32_t);
#define mesin_daftar(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define IRQ_distributor 0xff841000ul
#define IRQ_CPU_antarmuka 0xff842000ul
#define ukuran_halaman 4096ul
#define 접근표시 (1ul << 10)
#define tidak_Jalankan_izin (1ul << 53)
#define pengguna_tidak_Jalankan (1ul << 54)
#define 보통기억 ((1ul << 2) | (3ul << 8) | 접근표시)
#define kernel_halaman (3ul | 보통기억 | tidak_Jalankan_izin | pengguna_tidak_Jalankan)
#define pengguna_baca_tulis (3ul | 보통기억 | (1ul << 6) | tidak_Jalankan_izin | pengguna_tidak_Jalankan)
#define pengguna_baca_saja (3ul | 보통기억 | (3ul << 6) | tidak_Jalankan_izin | pengguna_tidak_Jalankan)
#define 사용자읽고실행 (3ul | 보통기억 | (3ul << 6) | tidak_Jalankan_izin)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 보드글자쓰기(uintptr_t), 보드글자읽기(void), 보드밀리초(void);
extern uintptr_t Papan_elgam(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 보드화면기억공간(void);
extern uintptr_t Papan_Terminal(uintptr_t);
extern int Terminal_sedang_diproses(void);
extern int32_t 자바셸대화형(void);
extern int32_t 자바경로시작(int32_t), 자바경로바이트(int32_t,int32_t);
extern int32_t 자바폴더만들기(void), 자바폴더지우기(void), 자바항목종류(void);
extern int 화면호출(int,unsigned,int,int,int,int,int),화면글(int,int,const uint32_t *,unsigned);
extern void 화면초기화(int),화면누름(int,unsigned);
extern int pengguna_CV(pengguna_bingkai *,void *);
extern void 사용자실수보관(void *);
extern int pengguna_masukkan(uintptr_t entri_p, uintptr_t memori_tumpukan, uintptr_t 전달값);
extern void pengguna_kembalikan(void);
extern void 커널중단(const char *) __attribute__((noreturn));
static uint64_t akar_surel[512] __attribute__((aligned(4096)));
static uint64_t 가운데[4][512] __attribute__((aligned(4096)));
static uint64_t halaman_Daftar[pengguna_halaman_COUNT] __attribute__((aligned(4096)));
static uint8_t Izin_Daftar[pengguna_halaman_COUNT];
static int Aktif, file_Daftar[16], 리눅스규약;
static unsigned 통신끝점들[24];
extern int32_t 자바전문만들기(int32_t, int32_t, int32_t), 자바전문묶기(int32_t, int32_t, int32_t);
extern int32_t 자바전문넣기(int32_t, int32_t), 자바전문얻기(int32_t), 자바전문보내기(int32_t, int32_t, int32_t, int32_t);
extern int32_t 자바전문받기(int32_t, int32_t), 자바전문접속번호(int32_t), 자바전문주소(int32_t), 자바전문상대(int32_t), 자바전문닫기(int32_t);
extern int32_t 자바흐름만들기(void),자바흐름묶기(int32_t,int32_t,int32_t),자바흐름듣기(int32_t,int32_t),자바흐름연결(int32_t,int32_t,int32_t),자바흐름연결받기(int32_t),자바흐름읽기(int32_t,int32_t),자바흐름쓰기(int32_t,int32_t),자바흐름접속번호(int32_t),자바흐름상대(int32_t),자바흐름닫기(int32_t);
static int 통신끝점닫기(unsigned file_handel){return file_handel<40?자바전문닫기(file_handel):자바흐름닫기(file_handel);}
static uint64_t FREQUENCY, tenggat_waktu_TIME;
static uintptr_t 동적기억끝;
// kernel_VALUE 셸이 준비한 UTF-8 argumen. EL0에는 salin_VALUE 호출만 제공한다.
static unsigned 전달인수개수, 전달인수길이[8];
static unsigned char 전달인수[8][256];
typedef struct {
    int 멈춤상태,interaktif,리눅스규약,file_Daftar[16]; unsigned 통신끝점들[24],인수개수,인수길이[8];
    unsigned char argumen_ARRAY[8][256],Izin_Daftar[pengguna_halaman_COUNT];
    uintptr_t memori_dinamis; pengguna_bingkai 실행틀;
    unsigned char terapung_p_Status[528] __attribute__((aligned(16)));
} 저장된작업;
static 저장된작업 저장값[4];
static int pemilik_objek,interaktif;
static uint32_t nomor_pengguna[4], pengguna_Mulai_TIME[4], 사용자누적시각[4], 사용자실행시각[4], Berikutnya_nomor_pengguna=10;
static unsigned char pengguna_perintah_nama[4][288];
uint32_t 사용자상태읽기(unsigned entri_VALUE, unsigned INDEX) {
    unsigned posisi_INDEX=INDEX&3;
    int Status_VALUE=(Aktif && pemilik_objek==(int)posisi_INDEX) ? 1 : 저장값[posisi_INDEX].멈춤상태 ? 2 : 0;
    if (entri_VALUE==0) return Status_VALUE;
    if (!Status_VALUE) return 0;
    if (entri_VALUE==1) return nomor_pengguna[posisi_INDEX];
    if (entri_VALUE==2) {
        unsigned char *쪽들=Status_VALUE==1?Izin_Daftar:저장값[posisi_INDEX].Izin_Daftar;
        unsigned halaman_COUNT=0; for (unsigned 순번=0; 순번<pengguna_halaman_COUNT; 순번++) if(쪽들[순번]) halaman_COUNT++;
        return halaman_COUNT*4;
    }
    if (entri_VALUE==3) return (uint32_t)보드밀리초()-pengguna_Mulai_TIME[posisi_INDEX];
    if (entri_VALUE==4) return 사용자누적시각[posisi_INDEX]+(Status_VALUE==1?(uint32_t)보드밀리초()-사용자실행시각[posisi_INDEX]:0);
    if (entri_VALUE==5) return INDEX/4<sizeof(pengguna_perintah_nama[0])?pengguna_perintah_nama[posisi_INDEX][INDEX/4]:0;
    return 0;
}
uintptr_t 보드인수시작(uintptr_t entri_COUNT) {
    if (Aktif || entri_COUNT > 8) return (uint32_t)-22;
    전달인수개수 = entri_COUNT;
    memset(전달인수길이, 0, sizeof(전달인수길이));
    memset(전달인수, 0, sizeof(전달인수));
    return 0;
}
uintptr_t 보드인수바이트(uintptr_t LOOKUP_INDEX, uintptr_t saat_ini_posisi, uintptr_t byte_data) {
    if (Aktif || LOOKUP_INDEX >= 전달인수개수 || saat_ini_posisi >= 255 || saat_ini_posisi != 전달인수길이[LOOKUP_INDEX] || !byte_data || byte_data > 255)
        return (uint32_t)-22;
    전달인수[LOOKUP_INDEX][saat_ini_posisi] = byte_data;
    전달인수길이[LOOKUP_INDEX] = saat_ini_posisi + 1;
    return 0;
}
static void 변환표맞추기(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t Jam_VALUE(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static void Berhenti_TIMEOUT(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    mesin_daftar(IRQ_distributor + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void Mulai_TIMEOUT(void) {
    uint64_t 간격 = FREQUENCY * 2, aktifkan = 1;
    tenggat_waktu_TIME = Jam_VALUE() + 간격;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(간격), "r"(aktifkan) : "memory");
}
void 사용자체계준비(void) {
    for (unsigned blok_data = 0; blok_data < 4; blok_data++) {
        akar_surel[blok_data] = (uintptr_t)가운데[blok_data] | 3;
        for (unsigned 순번 = 0; 순번 < 512; 순번++) {
            uintptr_t surel = ((uintptr_t)blok_data << 30) | ((uintptr_t)순번 << 21);
            가운데[blok_data][순번] = surel | 1 | 접근표시 | pengguna_tidak_Jalankan;
            if (surel >= 0xfc000000ul) 가운데[blok_data][순번] |= tidak_Jalankan_izin; // Device-nGnRnE
            else 가운데[blok_data][순번] |= 보통기억; // Normal, non-cacheable
        }
    }
    for (unsigned SECOND_VALUE = 0; SECOND_VALUE < pengguna_halaman_COUNT / 512; SECOND_VALUE++)
        가운데[0][(pengguna_BASE >> 21) + SECOND_VALUE] = (uintptr_t)(halaman_Daftar + SECOND_VALUE * 512) | 3;
    for (unsigned 순번 = 0; 순번 < pengguna_halaman_COUNT; 순번++) halaman_Daftar[순번] = (pengguna_BASE + 순번 * ukuran_halaman) | kernel_halaman;
    uint64_t Memori_atribut_daftar = 0x4400, surel_Terjemahan_kontrol = 32 | (3ul << 12) | (1ul << 23), 체계제어저장값;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(Memori_atribut_daftar), "r"(surel_Terjemahan_kontrol), "r"((uintptr_t)akar_surel) : "memory");
    변환표맞추기();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(체계제어저장값));
    체계제어저장값 = (체계제어저장값 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(체계제어저장값) : "memory");
    uint64_t terapung_p_Status = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(terapung_p_Status) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(FREQUENCY));
    Berhenti_TIMEOUT();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 entri_p_VALUE 때만 Perbolehkan_VALUE.
    mesin_daftar(IRQ_distributor) = 0;
    mesin_daftar(IRQ_distributor + 0x180) = 0xffffffff;
    mesin_daftar(IRQ_distributor + 0x80) = 0xffffffff;
    mesin_daftar(IRQ_distributor + 0x280) = 1u << 30;
    mesin_daftar(IRQ_distributor + 0x41c) = 0x80808080;
    mesin_daftar(IRQ_distributor + 0x100) = 1u << 30;
    mesin_daftar(IRQ_CPU_antarmuka + 4) = 0xff;
    mesin_daftar(IRQ_CPU_antarmuka + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 정상 확인할 수 있다.
    int Keamanan = (mesin_daftar(IRQ_distributor + 4) & (1u << 10)) != 0;
    mesin_daftar(IRQ_distributor) = Keamanan ? 1 : 3;
    mesin_daftar(IRQ_CPU_antarmuka) = Keamanan ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 형식식별[16]; uint16_t TYPE_area, mesin_TYPE; uint32_t nomor_versi;
    uint64_t entri_p, apl_judul_OFFSET, header_bagian_OFFSET; uint32_t konfigurasi_Background_Intelligent_Transfer_Service;
    uint16_t 실행머리크기, apl_judul_entri_ukuran, apl_judul_COUNT, header_bagian_entri_ukuran, header_bagian_COUNT, seksi_nama_tabel_INDEX;
} 실행파일머리;
typedef struct { uint32_t TYPE_area, konfigurasi_Background_Intelligent_Transfer_Service; uint64_t OFFSET_VALUE, surel, 물리주소, 파일영역크기, 기억영역크기, 맞춤; } 실행파일구획;
_Static_assert(sizeof(실행파일머리) == 64 && sizeof(실행파일구획) == 56, "ELF layout");
_Static_assert(sizeof(pengguna_bingkai) == 272, "exception assembly layout");
static int 포함된범위(uint64_t OFFSET_VALUE, uint64_t Ukuran, uint64_t mengakhiri_OFFSET) {
    return OFFSET_VALUE <= mengakhiri_OFFSET && Ukuran <= mengakhiri_OFFSET - OFFSET_VALUE;
}
static int 부가정보검사(const unsigned char *data_posisi, size_t Ukuran) {
    size_t saat_ini_posisi = 0;
    while (포함된범위(saat_ini_posisi, 12, Ukuran)) {
        uint32_t 낱말들[3]; memcpy(낱말들, data_posisi + saat_ini_posisi, 12); saat_ini_posisi += 12;
        uint64_t 이름영역크기 = ((uint64_t)낱말들[0] + 3) & ~3ul;
        uint64_t 설명크기 = ((uint64_t)낱말들[1] + 3) & ~3ul;
        if (!포함된범위(saat_ini_posisi, 이름영역크기, Ukuran) || !포함된범위(saat_ini_posisi + 이름영역크기, 설명크기, Ukuran)) return 0;
        const unsigned char Nama_2[] = {'J','K','O','R','O','S',0};
        int 일치 = 낱말들[0] == sizeof(Nama_2) && 낱말들[1] == 4 && 낱말들[2] == 1;
        if (일치) for (unsigned 순번 = 0; 순번 < sizeof(Nama_2); 순번++) if (data_posisi[saat_ini_posisi + 순번] != Nama_2[순번]) 일치 = 0;
        uint32_t nomor_versi = 0;
        if (일치) memcpy(&nomor_versi, data_posisi + saat_ini_posisi + 이름영역크기, 4);
        if (일치 && nomor_versi == 1) return 1;
        saat_ini_posisi += 이름영역크기 + 설명크기;
    }
    return 0;
}
static int 실행파일검사(const unsigned char *data, size_t Ukuran, int 리눅스방식) {
    if (Ukuran < sizeof(실행파일머리)) return 사용자실행파일오류;
    실행파일머리 실행머리; memcpy(&실행머리, data, sizeof(실행머리));
    if (실행머리.형식식별[0] != 127 || 실행머리.형식식별[1] != 'E' || 실행머리.형식식별[2] != 'L' || 실행머리.형식식별[3] != 'F' ||
        실행머리.형식식별[4] != 2 || 실행머리.형식식별[5] != 1 || 실행머리.형식식별[6] != 1 || (실행머리.형식식별[7] != 0 && (!리눅스방식 || 실행머리.형식식별[7] != 3)) ||
        실행머리.TYPE_area != 2 || 실행머리.mesin_TYPE != 183 || 실행머리.nomor_versi != 1 || 실행머리.konfigurasi_Background_Intelligent_Transfer_Service || 실행머리.실행머리크기 != sizeof(실행머리) ||
        실행머리.apl_judul_entri_ukuran != sizeof(실행파일구획) || !실행머리.apl_judul_COUNT || 실행머리.apl_judul_COUNT > 16 ||
        실행머리.apl_judul_OFFSET < sizeof(실행머리) || !포함된범위(실행머리.apl_judul_OFFSET, (uint64_t)실행머리.apl_judul_COUNT * sizeof(실행파일구획), Ukuran)) return 사용자실행파일오류;
    uint8_t 사용량[(pengguna_foto_mengakhiri - pengguna_BASE) / ukuran_halaman] = {0};
    int 진입점정상 = 0, 호출규약정상 = 0, 적재구획 = 0;
    for (unsigned 순번 = 0; 순번 < 실행머리.apl_judul_COUNT; 순번++) {
        실행파일구획 data_posisi; memcpy(&data_posisi, data + 실행머리.apl_judul_OFFSET + 순번 * sizeof(data_posisi), sizeof(data_posisi));
        if (data_posisi.TYPE_area == 4) {
            if (!포함된범위(data_posisi.OFFSET_VALUE, data_posisi.파일영역크기, Ukuran)) return 사용자실행파일오류;
            if (부가정보검사(data + data_posisi.OFFSET_VALUE, data_posisi.파일영역크기)) 호출규약정상 = 1;
            continue;
        }
        if (data_posisi.TYPE_area == 0 || data_posisi.TYPE_area == 6 || (data_posisi.TYPE_area == 0x6474e551 && !(data_posisi.konfigurasi_Background_Intelligent_Transfer_Service & 1))) continue;
        if (data_posisi.TYPE_area != 1) return 사용자실행파일오류; // PT_INTERP, DYNAMIC, TLS 미지원
        if (!data_posisi.기억영역크기) continue;
        if (data_posisi.konfigurasi_Background_Intelligent_Transfer_Service & ~7u || !(data_posisi.konfigurasi_Background_Intelligent_Transfer_Service & 4) || (data_posisi.konfigurasi_Background_Intelligent_Transfer_Service & 3) == 3 || data_posisi.파일영역크기 > data_posisi.기억영역크기 ||
            (data_posisi.파일영역크기 && !포함된범위(data_posisi.OFFSET_VALUE, data_posisi.파일영역크기, Ukuran)) || data_posisi.surel < pengguna_BASE ||
            !포함된범위(data_posisi.surel, data_posisi.기억영역크기, pengguna_foto_mengakhiri) ||
            (!리눅스방식 && ((data_posisi.surel & (ukuran_halaman - 1)) || (data_posisi.OFFSET_VALUE & (ukuran_halaman - 1)) || data_posisi.맞춤 != ukuran_halaman)) ||
            (리눅스방식 && (((data_posisi.surel ^ data_posisi.OFFSET_VALUE) & (ukuran_halaman - 1)) || !data_posisi.맞춤 ||
                (data_posisi.맞춤 & (data_posisi.맞춤 - 1)) || data_posisi.맞춤 > 0x200000 || ((data_posisi.surel ^ data_posisi.OFFSET_VALUE) & (data_posisi.맞춤 - 1))))) return 사용자실행파일오류;
        unsigned 첫항목 = (data_posisi.surel - pengguna_BASE) / ukuran_halaman;
        unsigned entri_COUNT = ((data_posisi.surel & (ukuran_halaman - 1)) + data_posisi.기억영역크기 + ukuran_halaman - 1) / ukuran_halaman;
        for (unsigned halaman_VALUE = 첫항목; halaman_VALUE < 첫항목 + entri_COUNT; halaman_VALUE++) {
            if (사용량[halaman_VALUE]) return 사용자실행파일오류;
            사용량[halaman_VALUE] = 1;
        }
        if ((data_posisi.konfigurasi_Background_Intelligent_Transfer_Service & 1) && 실행머리.entri_p >= data_posisi.surel && 실행머리.entri_p < data_posisi.surel + data_posisi.파일영역크기 && !(실행머리.entri_p & 3)) 진입점정상 = 1;
        적재구획++;
    }
    return 진입점정상 && (리눅스방식 ? !호출규약정상 : 호출규약정상) && 적재구획 ? 0 : 사용자실행파일오류;
}
int 사용자실행파일검사(const unsigned char *data, size_t Ukuran) { return 실행파일검사(data, Ukuran, 0); }
static void tata_letak_halaman(uintptr_t surel, uint64_t konfigurasi_Background_Intelligent_Transfer_Service, unsigned izin) {
    unsigned LOOKUP_INDEX = (surel - pengguna_BASE) / ukuran_halaman;
    halaman_Daftar[LOOKUP_INDEX] = surel | konfigurasi_Background_Intelligent_Transfer_Service;
    Izin_Daftar[LOOKUP_INDEX] = izin;
}
static int pengguna_rentang(uintptr_t surel, size_t entri_COUNT, int 쓰는중) {
    if (surel < pengguna_BASE || !포함된범위(surel, entri_COUNT, pengguna_mengakhiri)) return 0;
    if (!entri_COUNT) return 1;
    unsigned 첫항목 = (surel - pengguna_BASE) / ukuran_halaman, 마지막 = (surel + entri_COUNT - 1 - pengguna_BASE) / ukuran_halaman;
    for (unsigned 순번 = 첫항목; 순번 <= 마지막; 순번++) if (!(Izin_Daftar[순번] & (쓰는중 ? 2 : 1))) return 0;
    return 1;
}
static int salin_jalur(uintptr_t surel, char *jalur) {
    for (unsigned 순번 = 0; 순번 < 65; 순번++) {
        if (!pengguna_rentang(surel, 1, 0)) return -14;
        jalur[순번] = *(const char *)surel++;
        if (!jalur[순번]) return 0;
    }
    return -36;
}
static intptr_t kernel_KR(intptr_t hasil) { return hasil < 0 ? -nomor_kesalahan : hasil; }
static int 대응파일기술자(uint64_t file_handel) { return file_handel >= 3 && file_handel < 19 ? file_Daftar[file_handel - 3] : -1; }
static int 통신끝점소유(uint64_t file_handel) { return file_handel >= 32 && file_handel < 56 && 통신끝점들[file_handel - 32]; }
static int 주소입력(uintptr_t 가리킴값, size_t panjang_VALUE, struct pk_sockaddr_in *surel) {
    if (panjang_VALUE != sizeof(*surel)) return -22;
    if (!pengguna_rentang(가리킴값, panjang_VALUE, 0)) return -14;
    memcpy(surel, (const void *)가리킴값, sizeof(*surel));
    return surel->sin_family == AF_INET ? 0 : -97;
}
static int 주소출력검사(uintptr_t 가리킴값, uintptr_t panjang_pointer, pk_socklen_t *buffer_kapasitas) {
    if (!pengguna_rentang(panjang_pointer, sizeof(*buffer_kapasitas), 1)) return -14;
    memcpy(buffer_kapasitas, (const void *)panjang_pointer, sizeof(*buffer_kapasitas));
    if (*buffer_kapasitas > sizeof(struct pk_sockaddr_in)) *buffer_kapasitas = sizeof(struct pk_sockaddr_in);
    if (*buffer_kapasitas && !pengguna_rentang(가리킴값, *buffer_kapasitas, 1)) return -14;
    return 0;
}
static void 주소출력(uintptr_t 가리킴값, uintptr_t panjang_pointer, pk_socklen_t buffer_kapasitas, int surel, int nomor_port) {
    struct pk_sockaddr_in VALUE; memset(&VALUE, 0, sizeof(VALUE));
    VALUE.sin_family = AF_INET; VALUE.sin_port = pk_htons(nomor_port); VALUE.sin_addr.s_addr = pk_htonl(surel);
    if (buffer_kapasitas) memcpy((void *)가리킴값, &VALUE, buffer_kapasitas);
    pk_socklen_t panjang_VALUE = sizeof(VALUE); memcpy((void *)panjang_pointer, &panjang_VALUE, sizeof(panjang_VALUE));
}
extern uintptr_t Papan_Saluran(uintptr_t, uintptr_t);
static intptr_t 자체체계호출(pengguna_bingkai *file_entri) {
    uintptr_t 첫째값 = file_entri->daftar_data[0], SECOND_VALUE = file_entri->daftar_data[1], kode_karakter = file_entri->daftar_data[2];
    char jalur[65];
    int file_handel, hasil;
    switch (file_entri->daftar_data[8]) {
    case 0: return 1; // Asli ABI 버전
    case 1: // write: pointer 전체를 검사한 BACK_VALUE keluaranTeks/berkas ubah_VALUE
        if (kode_karakter > 65536) return -22;
        if (!pengguna_rentang(SECOND_VALUE, kode_karakter, 0)) return -14;
        if (첫째값 == 1 || 첫째값 == 2) {
            uint64_t 출력시작=Jam_VALUE();
            for (size_t 순번 = 0; 순번 < kode_karakter; 순번++) Papan_Saluran(첫째값, ((const unsigned char *)SECOND_VALUE)[순번]);
            /* 큰 tty를 그린 kernel_VALUE 시간만 돌려준다. EL0 계산 기한은 늘리지 않는다. */
            if(interaktif){
                tenggat_waktu_TIME+=Jam_VALUE()-출력시작;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(tenggat_waktu_TIME) : "memory");
            }
            return kode_karakter;
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            size_t item_COUNT=kode_karakter>512?512:kode_karakter;for(size_t 순번=0;순번<item_COUNT;순번++)자바전문넣기(순번,((const unsigned char *)SECOND_VALUE)[순번]);return 자바흐름쓰기(첫째값,item_COUNT);
        }
        file_handel = 대응파일기술자(첫째값); if (file_handel < 0) return -9;
        return kernel_KR(pk_write(file_handel, (const void *)SECOND_VALUE, kode_karakter));
    case 2:
        if (kode_karakter > 65536) return -22;
        if (!pengguna_rentang(SECOND_VALUE, kode_karakter, 1)) return -14;
        if (첫째값 == 0) {
            size_t item_COUNT = 0;
            while (item_COUNT < kode_karakter) {
                int karakter_VALUE = (int32_t)보드글자읽기(); if (karakter_VALUE == -2) return item_COUNT; if (karakter_VALUE < 0) break;
                ((unsigned char *)SECOND_VALUE)[item_COUNT++] = karakter_VALUE;
            }
            return item_COUNT ? (intptr_t)item_COUNT : (kode_karakter ? -11 : 0);
        }
        if(첫째값>=40&&통신끝점소유(첫째값)){
            hasil=자바흐름읽기(첫째값,kode_karakter>512?512:kode_karakter);if(hasil>0)for(int 순번=0;순번<hasil;순번++)((unsigned char *)SECOND_VALUE)[순번]=자바전문얻기(순번);return hasil;
        }
        file_handel = 대응파일기술자(첫째값); if (file_handel < 0) return -9;
        return kernel_KR(pk_read(file_handel, (void *)SECOND_VALUE, kode_karakter));
    case 3:
        hasil = salin_jalur(첫째값, jalur); if (hasil) return hasil;
        if (SECOND_VALUE > 0x7ff) return -22;
        for (unsigned 순번 = 0; 순번 < 16; 순번++) if (file_Daftar[순번] < 0) {
            file_handel = pk_open(jalur, (int)SECOND_VALUE, 0600);
            if (file_handel < 0) return -nomor_kesalahan;
            file_Daftar[순번] = file_handel; return 순번 + 3;
        }
        return -24;
    case 4:
        if (통신끝점소유(첫째값)) { hasil = 통신끝점닫기(첫째값); if (!hasil) 통신끝점들[첫째값 - 32] = 0; return hasil; }
        file_handel = 대응파일기술자(첫째값); if (file_handel < 0) return -9;
        hasil = pk_close(file_handel); if (!hasil) file_Daftar[첫째값 - 3] = -1;
        return kernel_KR(hasil);
    case 5:
        file_handel = 대응파일기술자(첫째값); if (file_handel < 0) return -9;
        if (kode_karakter > 2) return -22;
        return kernel_KR(pk_lseek(file_handel, (int64_t)SECOND_VALUE, kode_karakter));
    case 7: return 보드밀리초();
    case 8: { // brk: 별도 ruang_pengguna RW/NX 힙, 새로 노출되는 페이지는 0으로 inisialisasi
        if (!첫째값) return 동적기억끝;
        if (첫째값 < pengguna_foto_mengakhiri || 첫째값 > 사용자동적기억끝) return -12;
        uintptr_t 이전쪽들 = (동적기억끝 + ukuran_halaman - 1) & ~(ukuran_halaman - 1);
        uintptr_t 새쪽들 = (첫째값 + ukuran_halaman - 1) & ~(ukuran_halaman - 1);
        if (새쪽들 > 이전쪽들) {
            for (uintptr_t data_posisi = 이전쪽들; data_posisi < 새쪽들; data_posisi += ukuran_halaman) tata_letak_halaman(data_posisi, kernel_halaman, 0);
            변환표맞추기();
            memset((void *)이전쪽들, 0, 새쪽들 - 이전쪽들);
            for (uintptr_t data_posisi = 이전쪽들; data_posisi < 새쪽들; data_posisi += ukuran_halaman) tata_letak_halaman(data_posisi, pengguna_baca_tulis, 3);
        } else {
            for (uintptr_t data_posisi = 새쪽들; data_posisi < 이전쪽들; data_posisi += ukuran_halaman) {
                halaman_Daftar[(data_posisi - pengguna_BASE) / ukuran_halaman] = 0; Izin_Daftar[(data_posisi - pengguna_BASE) / ukuran_halaman] = 0;
            }
        }
        동적기억끝 = 첫째값; 변환표맞추기(); return 첫째값;
    }
    case 9:
        file_handel = 대응파일기술자(첫째값); return file_handel < 0 ? -9 : kernel_KR(pk_size(file_handel));
    case 10:
        file_handel = 대응파일기술자(첫째값); return file_handel < 0 ? -9 : kernel_KR(pk_ftruncate(file_handel, (int64_t)SECOND_VALUE));
    case 11:
        hasil = salin_jalur(첫째값, jalur); return hasil ? hasil : kernel_KR(pk_unlink(jalur));
    case 12:
        file_handel = 대응파일기술자(첫째값); return file_handel < 0 ? -9 : kernel_KR(pk_fsync(file_handel));
    case 13: { // 그래픽 기초 API: ruang_pengguna 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 너비값 = file_entri->daftar_data[3], 높이값 = file_entri->daftar_data[4];
        if (!보드화면기억공간()) return -19;
        uintptr_t 화면폭 = 보드화면너비(), 화면길이 = 보드화면높이();
        if (첫째값 > 화면폭 || SECOND_VALUE > 화면길이 || 너비값 > 화면폭 - 첫째값 || 높이값 > 화면길이 - SECOND_VALUE) return -22;
        for (uintptr_t Y_koordinat = SECOND_VALUE; Y_koordinat < SECOND_VALUE + 높이값; Y_koordinat++) for (uintptr_t koordinat_x = 첫째값; koordinat_x < 첫째값 + 너비값; koordinat_x++) Papan_elgam(koordinat_x, Y_koordinat, kode_karakter);
        return 0;
    }
    case 14: return (int32_t)보드글자읽기();
    case 15: // args(-1,0,0)=item_COUNT; args(index,buffer,capacity)=UTF-8 panjang_VALUE
        if (첫째값 == UINTPTR_MAX) return 전달인수개수;
        if (첫째값 >= 전달인수개수) return -22;
        if (kode_karakter <= 전달인수길이[첫째값]) return -36;
        if (!pengguna_rentang(SECOND_VALUE, 전달인수길이[첫째값] + 1, 1)) return -14;
        memcpy((void *)SECOND_VALUE, 전달인수[첫째값], 전달인수길이[첫째값] + 1);
        return 전달인수길이[첫째값];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(첫째값==0){if(!자바셸대화형())return -95;interaktif=1;return Papan_Terminal(13);}
        if(첫째값==2){interaktif=0;return 0;}
        if(첫째값==3)return Papan_Terminal(13);
        if(첫째값!=1||!interaktif)return -22;
        hasil=(int32_t)보드글자읽기();
        if(hasil==-4096)return hasil;
        Mulai_TIMEOUT();return hasil<0?-11:hasil;
    case 17: { // 유한한 협력 tunggu_VALUE: komunikasi 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (첫째값 > 100) return -22;
        uint64_t mengakhiri_TIME = Jam_VALUE() + FREQUENCY * 첫째값 / 1000;
        do { 통신망살피기(); 파일전송살피기(); __asm__ volatile("yield"); } while (Jam_VALUE() < mengakhiri_TIME);
        Mulai_TIMEOUT(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 induk_VALUE·빈 폴더를 검사한다.
        if (SECOND_VALUE > 2) return -22;
        hasil = salin_jalur(첫째값, jalur); if (hasil) return hasil;
        unsigned panjang_VALUE = 0; while (jalur[panjang_VALUE]) panjang_VALUE++;
        hasil = 자바경로시작(panjang_VALUE); if (hasil < 0) return hasil;
        for (unsigned 순번 = 0; 순번 < panjang_VALUE; 순번++) 자바경로바이트(순번, (unsigned char)jalur[순번]);
        return SECOND_VALUE == 0 ? 자바항목종류() : SECOND_VALUE == 1 ? 자바폴더만들기() : 자바폴더지우기();
    }
    case 20:
        if(첫째값==5){int karakter_VALUE=(int32_t)보드글자읽기();if(karakter_VALUE==-4096)return karakter_VALUE;if(karakter_VALUE>=0)화면누름(pemilik_objek,karakter_VALUE);Mulai_TIMEOUT();}
        if(첫째값==3&&kode_karakter){if(!자바셸대화형())return -95;interaktif=1;Papan_Terminal(300);}
        return 화면호출(pemilik_objek,첫째값,SECOND_VALUE,kode_karakter,file_entri->daftar_data[3],file_entri->daftar_data[4],file_entri->daftar_data[5]);
    case 21:
        if(kode_karakter>127)return -22;if(!pengguna_rentang(SECOND_VALUE,kode_karakter*sizeof(uint32_t),0))return -14;
        return 화면글(pemilik_objek,첫째값,(const uint32_t *)SECOND_VALUE,kode_karakter);
    case 22: // 화면 Ukuran kueri_VALUE: 0=너비, 1=높이. 사용자에게 주소를 노출하지 않는다.
        if (첫째값 > 1) return -22;
        if (!보드화면기억공간()) return -19;
        return 첫째값 == 0 ? 보드화면너비() : 보드화면높이();
    case 32:
        if (첫째값 != AF_INET) return -97;
        if(SECOND_VALUE==SOCK_STREAM&&(kode_karakter==0||kode_karakter==6))hasil=자바흐름만들기();
        else if(SECOND_VALUE==SOCK_DGRAM&&(kode_karakter==0||kode_karakter==IPPROTO_UDP))hasil=자바전문만들기(첫째값,SECOND_VALUE,kode_karakter);
        else return -93;
        if (hasil >= 32 && hasil < 56) 통신끝점들[hasil - 32] = 1;
        return hasil;
    case 33: {
        if (!통신끝점소유(첫째값)) return -9;
        struct pk_sockaddr_in surel;
        hasil = 주소입력(SECOND_VALUE, kode_karakter, &surel); if (hasil) return hasil;
        return 첫째값>=40?자바흐름묶기(첫째값,pk_htonl(surel.sin_addr.s_addr),pk_htons(surel.sin_port)):자바전문묶기(첫째값, pk_htonl(surel.sin_addr.s_addr), pk_htons(surel.sin_port));
    }
    case 34: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (file_entri->daftar_data[3]) return -95;
        if (kode_karakter > 512) return -90;
        if (kode_karakter && !pengguna_rentang(SECOND_VALUE, kode_karakter, 0)) return -14;
        struct pk_sockaddr_in surel;
        hasil = 주소입력(file_entri->daftar_data[4], file_entri->daftar_data[5], &surel); if (hasil) return hasil;
        for (unsigned 순번 = 0; 순번 < kode_karakter; 순번++) 자바전문넣기(순번, ((const unsigned char *)SECOND_VALUE)[순번]);
        return 자바전문보내기(첫째값, pk_htonl(surel.sin_addr.s_addr), pk_htons(surel.sin_port), kode_karakter);
    }
    case 35: {
        if (!통신끝점소유(첫째값)) return -9;
        if(첫째값>=40)return -95;
        if (file_entri->daftar_data[3]) return -95;
        if (kode_karakter > 512) return -90;
        if (kode_karakter && !pengguna_rentang(SECOND_VALUE, kode_karakter, 1)) return -14;
        pk_socklen_t buffer_kapasitas = 0;
        if (file_entri->daftar_data[4]) { hasil = 주소출력검사(file_entri->daftar_data[4], file_entri->daftar_data[5], &buffer_kapasitas); if (hasil) return hasil; }
        hasil = 자바전문받기(첫째값, kode_karakter); if (hasil < 0) return hasil;
        for (int 순번 = 0; 순번 < hasil; 순번++) ((unsigned char *)SECOND_VALUE)[순번] = 자바전문얻기(순번);
        if (file_entri->daftar_data[4]) 주소출력(file_entri->daftar_data[4], file_entri->daftar_data[5], buffer_kapasitas, 자바전문원격주소(첫째값), 자바전문상대(첫째값));
        return hasil;
    }
    case 36: {
        if (!통신끝점소유(첫째값)) return -9;
        pk_socklen_t buffer_kapasitas;
        hasil = 주소출력검사(SECOND_VALUE, kode_karakter, &buffer_kapasitas); if (hasil) return hasil;
        주소출력(SECOND_VALUE,kode_karakter,buffer_kapasitas,첫째값>=40?자바흐름주소(첫째값):자바전문주소(첫째값),첫째값>=40?자바흐름접속번호(첫째값):자바전문접속번호(첫째값)); return 0;
    }
    case 37: {
        if(첫째값<40||!통신끝점소유(첫째값))return -9;struct pk_sockaddr_in surel;
        hasil=주소입력(SECOND_VALUE,kode_karakter,&surel);if(hasil)return hasil;
        return 자바흐름연결(첫째값,pk_htonl(surel.sin_addr.s_addr),pk_htons(surel.sin_port));
    }
    case 38: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름듣기(첫째값,SECOND_VALUE):-9;
    case 39:
        if(첫째값<40||!통신끝점소유(첫째값))return -9;
        if(SECOND_VALUE||kode_karakter)return -95;hasil=자바흐름연결받기(첫째값);if(hasil>=40&&hasil<56)통신끝점들[hasil-32]=1;return hasil;
    case 40: return 첫째값>=40&&통신끝점소유(첫째값)?자바흐름상대(첫째값):-9;
    default: return -38; // 미지원 기능을 성공으로 가장하지 않음
    }
}
#include "리눅스호환.inc"
static intptr_t panggilan_sistem(pengguna_bingkai *file_entri) {
    network_poll();
    return 리눅스규약 ? 리눅스체계호출(file_entri) : 자체체계호출(file_entri);
}
static void kembalikan_kernel(pengguna_bingkai *file_entri, int hasil) {
    Berhenti_TIMEOUT();
    file_entri->daftar_data[0] = (uint64_t)(int64_t)hasil;
    file_entri->perintah_posisi = (uintptr_t)pengguna_kembalikan;
    file_entri->Status_CODE = 0x3c5; // EL1h, DAIF masked
}
int pengguna_pengecualian(pengguna_bingkai *file_entri, unsigned INTERCEPT) {
    if (!Aktif || (file_entri->Status_CODE & 15) != 0) return 0;
    if (INTERCEPT) {
        uint32_t 승인값 = mesin_daftar(IRQ_CPU_antarmuka + 0xc), pengidentifikasi_VALUE = 승인값 & 1023;
        if (pengidentifikasi_VALUE == 30) { kembalikan_kernel(file_entri, pengguna_TIMEOUT); mesin_daftar(IRQ_CPU_antarmuka + 0x10) = 승인값; return 1; }
        if (pengidentifikasi_VALUE < 1020) mesin_daftar(IRQ_CPU_antarmuka + 0x10) = 승인값;
        return 1;
    }
    uint64_t pengecualian_Status; __asm__ volatile("mrs %0, esr_el1" : "=r"(pengecualian_Status));
    if (Jam_VALUE() >= tenggat_waktu_TIME) { kembalikan_kernel(file_entri, pengguna_TIMEOUT); return 1; }
    unsigned pengecualian_area = pengecualian_Status >> 26;
    if (pengecualian_area == 0x15 && (pengecualian_Status & 0xffff) == 0) {
        if (리눅스규약 ? file_entri->daftar_data[8] == 93 || file_entri->daftar_data[8] == 94 : file_entri->daftar_data[8] == 6) kembalikan_kernel(file_entri, (int)(file_entri->daftar_data[0] & 255));
        else {
            intptr_t hasil=panggilan_sistem(file_entri);
            if(hasil==-4096&&interaktif){
                저장값[pemilik_objek].실행틀=*file_entri;저장값[pemilik_objek].실행틀.perintah_posisi-=4;
                사용자실수보관(저장값[pemilik_objek].terapung_p_Status);kembalikan_kernel(file_entri,사용자중단됨);
            }else file_entri->daftar_data[0]=(uint64_t)hasil;
        }
    } else kembalikan_kernel(file_entri, pengecualian_area == 0x24 ? pengguna_data_kesalahan : pengecualian_area == 0x20 ? 사용자실행오류 : pengguna_tidak_sahih_instruksi);
    return 1;
}

// 생성된 const ELF grup_VALUE: 실행은 반드시 apl_f5044b9b 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *data; size_t Ukuran; unsigned 전달값; } apl;
#include "programs.h"
static void *snapshot(unsigned posisi_INDEX){return (void *)(0x04000000ul+posisi_INDEX*(pengguna_mengakhiri-pengguna_BASE));}
static int Selesai_apl(int hasil){
    사용자누적시각[pemilik_objek]+=(uint32_t)보드밀리초()-사용자실행시각[pemilik_objek];
    Berhenti_TIMEOUT();Aktif=0;
    if(hasil==사용자중단됨){
        저장된작업 *string_data=&저장값[pemilik_objek];string_data->멈춤상태=1;string_data->interaktif=interaktif;string_data->리눅스규약=리눅스규약;string_data->memori_dinamis=동적기억끝;string_data->인수개수=전달인수개수;
        memcpy(string_data->Izin_Daftar,Izin_Daftar,sizeof(Izin_Daftar));memcpy(string_data->file_Daftar,file_Daftar,sizeof(file_Daftar));memcpy(string_data->통신끝점들,통신끝점들,sizeof(통신끝점들));
        memcpy(string_data->argumen_ARRAY,전달인수,sizeof(전달인수));memcpy(string_data->인수길이,전달인수길이,sizeof(전달인수길이));
        for(unsigned 순번=0;순번<pengguna_halaman_COUNT;순번++)if(Izin_Daftar[순번])memcpy((unsigned char *)snapshot(pemilik_objek)+순번*ukuran_halaman,(void *)(pengguna_BASE+순번*ukuran_halaman),ukuran_halaman);
    }else{
        저장값[pemilik_objek].멈춤상태=0;화면초기화(pemilik_objek);
        for(unsigned 순번=0;순번<16;순번++)if(file_Daftar[순번]>=0)pk_close(file_Daftar[순번]);
        for(unsigned 순번=0;순번<24;순번++)if(통신끝점들[순번])통신끝점닫기(순번+32);
    }
    for(unsigned 순번=0;순번<pengguna_halaman_COUNT;순번++){halaman_Daftar[순번]=0;Izin_Daftar[순번]=0;}변환표맞추기();return hasil;
}
uintptr_t Papan_kontrol_pengguna(uintptr_t Aksi){
    unsigned posisi_INDEX=Aksi&15;if(posisi_INDEX>=4||Aktif)return (uint32_t)-22;
    저장된작업 *string_data=&저장값[posisi_INDEX];
    if(Aksi>=32){if(string_data->멈춤상태){for(unsigned 순번=0;순번<16;순번++)if(string_data->file_Daftar[순번]>=0)pk_close(string_data->file_Daftar[순번]);for(unsigned 순번=0;순번<24;순번++)if(string_data->통신끝점들[순번])통신끝점닫기(순번+32);}string_data->멈춤상태=0;화면초기화(posisi_INDEX);return 0;}
    if(Aksi>=16)return string_data->멈춤상태;
    if(!string_data->멈춤상태)return (uint32_t)-22;
    pemilik_objek=posisi_INDEX;interaktif=string_data->interaktif;리눅스규약=string_data->리눅스규약;동적기억끝=string_data->memori_dinamis;전달인수개수=string_data->인수개수;
    memcpy(file_Daftar,string_data->file_Daftar,sizeof(file_Daftar));memcpy(통신끝점들,string_data->통신끝점들,sizeof(통신끝점들));memcpy(전달인수,string_data->argumen_ARRAY,sizeof(전달인수));memcpy(전달인수길이,string_data->인수길이,sizeof(전달인수길이));
    for(unsigned 순번=0;순번<pengguna_halaman_COUNT;순번++)halaman_Daftar[순번]=(pengguna_BASE+순번*ukuran_halaman)|kernel_halaman;변환표맞추기();
    memset((void *)pengguna_BASE,0,pengguna_mengakhiri-pengguna_BASE);
    for(unsigned 순번=0;순번<pengguna_halaman_COUNT;순번++)if(string_data->Izin_Daftar[순번])memcpy((void *)(pengguna_BASE+순번*ukuran_halaman),(unsigned char *)snapshot(posisi_INDEX)+순번*ukuran_halaman,ukuran_halaman);
    memcpy(Izin_Daftar,string_data->Izin_Daftar,sizeof(Izin_Daftar));
    for(unsigned 순번=0;순번<pengguna_halaman_COUNT;순번++){unsigned data_posisi=Izin_Daftar[순번];halaman_Daftar[순번]=data_posisi?(pengguna_BASE+순번*ukuran_halaman)|(data_posisi==3?pengguna_baca_tulis:data_posisi==5?사용자읽고실행:pengguna_baca_saja):0;}
    변환표맞추기();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");Aktif=1;string_data->멈춤상태=0;Mulai_TIMEOUT();
    사용자실행시각[pemilik_objek]=보드밀리초();
    return (uint32_t)Selesai_apl(pengguna_CV(&string_data->실행틀,string_data->terapung_p_Status));
}
static int eksekusi_apl(const unsigned char *data, size_t Ukuran, unsigned 전달값, int 리눅스방식, const char *Nama_2) {
    if (Aktif) return -16;
    pemilik_objek=Papan_Terminal(11);if(pemilik_objek<0||pemilik_objek>3||저장값[pemilik_objek].멈춤상태)return -16;interaktif=0;
    int 유효함 = 실행파일검사(data, Ukuran, 리눅스방식); if (유효함) return 유효함;
    리눅스규약 = 리눅스방식;
    unsigned nama_INDEX=0;
    while (*Nama_2 && nama_INDEX<31) pengguna_perintah_nama[pemilik_objek][nama_INDEX++]=(unsigned char)*Nama_2++;
    if (전달인수개수 && 전달인수길이[0]) {
        if (nama_INDEX) pengguna_perintah_nama[pemilik_objek][nama_INDEX++]=' ';
        for (unsigned posisi_INDEX=0; posisi_INDEX<전달인수길이[0]; posisi_INDEX++) pengguna_perintah_nama[pemilik_objek][nama_INDEX++]=전달인수[0][posisi_INDEX];
    }
    pengguna_perintah_nama[pemilik_objek][nama_INDEX]=0; nomor_pengguna[pemilik_objek]=Berikutnya_nomor_pengguna++;
    if (Berikutnya_nomor_pengguna>0x7fffffffu) Berikutnya_nomor_pengguna=10;
    pengguna_Mulai_TIME[pemilik_objek]=보드밀리초(); 사용자누적시각[pemilik_objek]=0;
    for (unsigned 순번 = 0; 순번 < pengguna_halaman_COUNT; 순번++) halaman_Daftar[순번] = (pengguna_BASE + 순번 * ukuran_halaman) | kernel_halaman;
    변환표맞추기();
    memset((void *)pengguna_BASE, 0, pengguna_mengakhiri - pengguna_BASE);
    memset(Izin_Daftar, 0, sizeof(Izin_Daftar));
    실행파일머리 실행머리; memcpy(&실행머리, data, sizeof(실행머리));
    for (unsigned 순번 = 0; 순번 < 실행머리.apl_judul_COUNT; 순번++) {
        실행파일구획 data_posisi; memcpy(&data_posisi, data + 실행머리.apl_judul_OFFSET + 순번 * sizeof(data_posisi), sizeof(data_posisi));
        if (data_posisi.TYPE_area != 1 || !data_posisi.기억영역크기) continue;
        if (data_posisi.파일영역크기) memcpy((void *)(uintptr_t)data_posisi.surel, data + data_posisi.OFFSET_VALUE, data_posisi.파일영역크기);
        for (uintptr_t saat_ini_posisi = data_posisi.surel & ~(ukuran_halaman - 1); saat_ini_posisi < data_posisi.surel + data_posisi.기억영역크기; saat_ini_posisi += ukuran_halaman) {
            Izin_Daftar[(saat_ini_posisi - pengguna_BASE) / ukuran_halaman] = (data_posisi.konfigurasi_Background_Intelligent_Transfer_Service & 2) ? 3 : ((data_posisi.konfigurasi_Background_Intelligent_Transfer_Service & 1) ? 5 : 1);
        }
    }
    for (uintptr_t saat_ini_posisi = pengguna_tumpuk_surel; saat_ini_posisi < pengguna_mengakhiri; saat_ini_posisi += ukuran_halaman) Izin_Daftar[(saat_ini_posisi - pengguna_BASE) / ukuran_halaman] = 3;
    uintptr_t 초기쌓임공간 = 리눅스방식 ? 리눅스시작쌓임(실행머리.entri_p) : pengguna_mengakhiri;
    for (unsigned 순번 = 0; 순번 < pengguna_halaman_COUNT; 순번++) {
        unsigned izin = Izin_Daftar[순번];
        halaman_Daftar[순번] = izin ? (pengguna_BASE + 순번 * ukuran_halaman) | (izin == 3 ? pengguna_baca_tulis : izin == 5 ? 사용자읽고실행 : pengguna_baca_saja) : 0;
    }
    변환표맞추기();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 순번 = 0; 순번 < 16; 순번++) file_Daftar[순번] = -1;
    memset(통신끝점들, 0, sizeof(통신끝점들));
    동적기억끝 = pengguna_foto_mengakhiri;
    Aktif = 1; Mulai_TIMEOUT();
    사용자실행시각[pemilik_objek]=보드밀리초();
    int hasil = pengguna_masukkan(실행머리.entri_p, 초기쌓임공간, 전달값);
    return Selesai_apl(hasil);
}
uintptr_t Papan_pengguna_eksekusi(uintptr_t LOOKUP_INDEX) {
    if (LOOKUP_INDEX >= sizeof(실행항목들) / sizeof(실행항목들[0])) return (uint32_t)-22;
    const char *Nama_2=LOOKUP_INDEX==10?"javac":LOOKUP_INDEX==11?"java":LOOKUP_INDEX==12?"python":LOOKUP_INDEX==13?"vi":LOOKUP_INDEX==14?"jar":LOOKUP_INDEX==15?"cc":LOOKUP_INDEX==16?"jaot":"ELF";
    return (uint32_t)eksekusi_apl(실행항목들[LOOKUP_INDEX].data, 실행항목들[LOOKUP_INDEX].Ukuran, 실행항목들[LOOKUP_INDEX].전달값, 0, Nama_2);
}
static uintptr_t Jalankan_file(int 리눅스방식) {
    static unsigned char foto[16384];
    if (Aktif || !전달인수개수) return (uint32_t)-22;
    int file_handel = pk_open((const char *)전달인수[0], baca_saja_VALUE, 0);
    if (file_handel < 0) return (uint32_t)-nomor_kesalahan;
    int Ukuran = pk_size(file_handel);
    if (Ukuran < 0 || (unsigned)Ukuran > sizeof(foto)) { pk_close(file_handel); return (uint32_t)-27; }
    int RECEIVED_COUNT = pk_read(file_handel, foto, Ukuran); pk_close(file_handel);
    if (RECEIVED_COUNT != Ukuran) return (uint32_t)-5;
    return (uint32_t)eksekusi_apl(foto, Ukuran, 0, 리눅스방식, "");
}
uintptr_t Papan_pengguna_file(void) { return Jalankan_file(0); }
uintptr_t 보드사용자리눅스파일(void) { return Jalankan_file(1); }
uintptr_t Papan_pengguna_validasi(void) {
    for (unsigned 순번 = 0; 순번 < sizeof(잘못된실행항목들) / sizeof(잘못된실행항목들[0]); 순번++)
        if (사용자실행파일검사(잘못된실행항목들[순번].data, 잘못된실행항목들[순번].Ukuran) != 사용자실행파일오류) return 순번 + 1;
    return 0;
}
