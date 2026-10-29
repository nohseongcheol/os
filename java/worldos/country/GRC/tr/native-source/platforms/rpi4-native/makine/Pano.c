#include "../명명/기계연결이름.h"
#include "화면정보.h"
#include <stdint.h>
#include <stddef.h>
#include "kullanıcı_alanı.h"
#include "../ağ_Yığın/ağ_Yığın.h"
typedef uintptr_t makine_Word;
#define makine_yazmaç(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 직렬장치 0xfe201000u
#define 범용입출력 0xfe200000u
#define posta_kutusu_ADRES 0xfe00b880u
static inline void 기억장벽(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t Saat_BAĞ_DEĞ_SAY(void) { uint64_t 임시값; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(임시값)); return 임시값; }
static uint64_t SIKLIK;
static volatile uint32_t posta_kutusu_veri[64] __attribute__((aligned(16)));
static unsigned 화면준비됨;
static uint32_t 팔기억킬로바이트;

void *memset(void *veri_konum, int kod_noktası, size_t öğe_BAĞ_DEĞ_SAY) { unsigned char *Sonraki_Ofset = veri_konum; while (öğe_BAĞ_DEĞ_SAY--) *Sonraki_Ofset++ = kod_noktası; return veri_konum; }
void *memcpy(void *hedef_veri, const void *dize_veri, size_t öğe_BAĞ_DEĞ_SAY) { unsigned char *첫째값 = hedef_veri; const unsigned char *SANİYE_değer = dize_veri; while (öğe_BAĞ_DEĞ_SAY--) *첫째값++ = *SANİYE_değer++; return hedef_veri; }

static int posta_kutusu(void) {
    uint32_t istek = (uint32_t)(uintptr_t)posta_kutusu_veri | 8;
    uint64_t çalıştır = Saat_BAĞ_DEĞ_SAY();
    기억장벽();
    while (makine_yazmaç(posta_kutusu_ADRES + 0x38) & 0x80000000u)
        if (Saat_BAĞ_DEĞ_SAY() - çalıştır > SIKLIK) return 0;
    makine_yazmaç(posta_kutusu_ADRES + 0x20) = istek;
    for (;;) {
        if (!(makine_yazmaç(posta_kutusu_ADRES + 0x18) & 0x40000000u)) {
            uint32_t yanıt = makine_yazmaç(posta_kutusu_ADRES);
            if (yanıt == istek) { 기억장벽(); return posta_kutusu_veri[1] == 0x80000000u; }
        }
        if (Saat_BAĞ_DEĞ_SAY() - çalıştır > SIKLIK) return 0;
    }
}

extern int32_t 자바셸출력(int32_t, int32_t), 자바셸입력(void);
extern void Terminal_bayt(unsigned);
extern int Terminal_Beklemede(void);
extern void Terminal_işaretçi(unsigned,int,int),터미널바로가기키(unsigned);
extern void Terminal_artış_mod(unsigned);
#include "../uzak_değer/uzak_değer.h"
static int Akışlar;
static unsigned 직렬이전글자;
makine_Word Pano_Akışlar(makine_Word 사용여부) { Akışlar=사용여부!=0; return 0; }
makine_Word Pano_Kanal(makine_Word Kanal, makine_Word kod_noktası) {
    if(Akışlar && 자바셸출력((int32_t)Kanal,(int32_t)(kod_noktası&255))) return 0;
    Terminal_bayt(kod_noktası&255);
    uzak_çıktı(kod_noktası&255);
    if ((kod_noktası&255)==10 && 직렬이전글자!=13) {
        while (makine_yazmaç(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
        makine_yazmaç(직렬장치)=13;
    }
    직렬이전글자=kod_noktası&255;
    while (makine_yazmaç(직렬장치 + 0x18) & 0x20) __asm__ volatile("yield");
    makine_yazmaç(직렬장치) = (uint32_t)kod_noktası & 255;
    return 0;
}
makine_Word 보드글자쓰기(makine_Word kod_noktası) { return Pano_Kanal(1,kod_noktası); }
makine_Word 보드원시글자읽기(void) {
    int uzak_karakter=uzak_artış();if(uzak_karakter>=0)return uzak_karakter;
    if (makine_yazmaç(직렬장치 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t değer = makine_yazmaç(직렬장치);
    if (değer & 0xf00) { makine_yazmaç(직렬장치 + 4) = 0; return (uint32_t)-1; }
    return değer & 255;
}
makine_Word 보드글자읽기(void) {
    network_poll();
    static unsigned 꾸러미안쪽,사용량; static unsigned char paket_veri[6];
    if(Terminal_Beklemede())return (uint32_t)-4096;
    if(Akışlar){int32_t kod_noktası=자바셸입력();if(kod_noktası!=-3)return (uint32_t)kod_noktası;}
    for(;;){
        int kod_noktası=(int32_t)보드원시글자읽기();if(kod_noktası<0)return (uint32_t)kod_noktası;
        if(!꾸러미안쪽){if(kod_noktası!=30)return kod_noktası;꾸러미안쪽=1;사용량=0;continue;}
        paket_veri[사용량++]=kod_noktası;if(사용량<6)continue;꾸러미안쪽=0;
        if(paket_veri[0]==1)Terminal_işaretçi(paket_veri[1],paket_veri[2]+paket_veri[3]*256,paket_veri[4]+paket_veri[5]*256);
        if(paket_veri[0]==2)터미널바로가기키(paket_veri[1]);
        if(paket_veri[0]==3)Terminal_artış_mod(paket_veri[1]);
        if(Terminal_Beklemede())return (uint32_t)-4096;
    }
}
makine_Word 보드밀리초(void) { return (uint32_t)(Saat_BAĞ_DEĞ_SAY() / (SIKLIK / 1000)); }
makine_Word 보드예외수준(void) { uint64_t 임시값; __asm__ volatile("mrs %0, CurrentEL" : "=r"(임시값)); return 임시값 >> 2; }
static void 직렬글출력(const char *dize_veri) { while (*dize_veri) 보드글자쓰기((unsigned char)*dize_veri++); }
static void 직렬열여섯진출력(makine_Word öğe_BAĞ_DEĞ_SAY) { const char *열여섯진숫자 = "0123456789abcdef"; for (int dize_veri = 60; dize_veri >= 0; dize_veri -= 4) 보드글자쓰기(열여섯진숫자[(öğe_BAĞ_DEĞ_SAY >> dize_veri) & 15]); }
makine_Word Pano_Dur(makine_Word Durum_değer) {
    직렬글출력("\r\nHALTED "); 직렬열여섯진출력(Durum_değer); 직렬글출력("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 커널중단(const char *까닭) __attribute__((noreturn));
void 커널중단(const char *까닭) { 직렬글출력("\r\nPANIC: "); 직렬글출력(까닭); Pano_Dur(1); __builtin_unreachable(); }
void Pano_özel_durum(makine_Word özel_durum_Durum, makine_Word komut_konum, makine_Word geçersiz_ADRES) {
    직렬글출력("\r\nEXCEPTION ESR="); 직렬열여섯진출력(özel_durum_Durum);
    직렬글출력(" PC="); 직렬열여섯진출력(komut_konum); 직렬글출력(" FAR="); 직렬열여섯진출력(geçersiz_ADRES);
    Pano_Dur(2);
}
int 보드실물(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    posta_kutusu_veri[0]=32;posta_kutusu_veri[1]=0;posta_kutusu_veri[2]=0x10004;posta_kutusu_veri[3]=8;posta_kutusu_veri[4]=0;
    posta_kutusu_veri[5]=posta_kutusu_veri[6]=posta_kutusu_veri[7]=0;
    return posta_kutusu()&&posta_kutusu_veri[4]==0x80000008u&&(posta_kutusu_veri[5]||posta_kutusu_veri[6]);
}
int Pano_mutlak_adres(unsigned char *ADRES) {
    posta_kutusu_veri[0]=32;posta_kutusu_veri[1]=0;posta_kutusu_veri[2]=0x10003;posta_kutusu_veri[3]=8;posta_kutusu_veri[4]=0;
    posta_kutusu_veri[5]=posta_kutusu_veri[6]=posta_kutusu_veri[7]=0;
    if(!posta_kutusu()||(posta_kutusu_veri[4]&0x80000000u)==0||(posta_kutusu_veri[4]&0xffff)!=6)return 0;
    const unsigned char *veri=(const unsigned char*)&posta_kutusu_veri[5];unsigned SUM_değer=0;
    for(unsigned 순번=0;순번<6;순번++){ADRES[순번]=veri[순번];SUM_değer|=veri[순번];}return SUM_değer&&!(ADRES[0]&1);
}
void 보드준비(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(SIKLIK));
    makine_yazmaç(직렬장치 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    makine_yazmaç(범용입출력 + 4) = (makine_yazmaç(범용입출력 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    makine_yazmaç(범용입출력 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. hata_değer 시 config.txt의 48MHz를 사용한다.
    posta_kutusu_veri[0] = 36; posta_kutusu_veri[1] = 0; posta_kutusu_veri[2] = 0x38002; posta_kutusu_veri[3] = 12;
    posta_kutusu_veri[4] = 0; posta_kutusu_veri[5] = 2; posta_kutusu_veri[6] = 48000000; posta_kutusu_veri[7] = 0; posta_kutusu_veri[8] = 0;
    int Saat_iyi_durumda = posta_kutusu();
    uint32_t 속도 = Saat_iyi_durumda && posta_kutusu_veri[6] >= 1843200 ? posta_kutusu_veri[6] : 48000000;
    posta_kutusu_veri[0]=32; posta_kutusu_veri[1]=0; posta_kutusu_veri[2]=0x10005; posta_kutusu_veri[3]=8; posta_kutusu_veri[4]=0;
    posta_kutusu_veri[5]=posta_kutusu_veri[6]=posta_kutusu_veri[7]=0;
    if (posta_kutusu() && posta_kutusu_veri[4]==0x80000008u) 팔기억킬로바이트=posta_kutusu_veri[6]/1024;
    uint32_t 육십사배나눔수 = (uint32_t)(((uint64_t)속도 * 4 + 57600) / 115200);
    makine_yazmaç(직렬장치 + 0x44) = 0x7ff;
    makine_yazmaç(직렬장치 + 0x24) = 육십사배나눔수 / 64;
    makine_yazmaç(직렬장치 + 0x28) = 육십사배나눔수 % 64;
    makine_yazmaç(직렬장치 + 0x2c) = (3u << 5) | (1u << 4);
    makine_yazmaç(직렬장치 + 0x38) = 0;
    makine_yazmaç(직렬장치 + 0x30) = 0x301;
    기억장벽();
    직렬글출력("JKOROS AARCH64 BARE METAL\r\n");
    사용자체계준비();
    network_init();
}
makine_Word Pano_FTP(makine_Word Eylem) { return (uint32_t)ftp_control((int)Eylem); }
makine_Word Pano_ağ_Durum(makine_Word girdi_değer, makine_Word Dizin) { return 망상태읽기(girdi_değer, Dizin); }
makine_Word Pano_ağ_Ayarlar(makine_Word Eylem, makine_Word ADRES, makine_Word maske_değer, makine_Word ağ_geçidi_değer) { return (uint32_t)yapılandırmak_ağ(Eylem, ADRES, maske_değer, ağ_geçidi_değer); }
makine_Word Pano_göndermek_cevap(makine_Word ADRES, makine_Word düzen_değer) { return (uint32_t)Start_cevap_test(ADRES, düzen_değer); }
makine_Word 보드응답읽기(makine_Word girdi_değer) { return (uint32_t)응답시험읽기(girdi_değer); }
makine_Word 보드전원끄기(void) {
    ftp_control(0);
    for (unsigned Dizin=0; Dizin<32; Dizin++) Kapat_ağ(Dizin);
    for (unsigned Dizin=0; Dizin<4; Dizin++) Pano_kullanıcı_kontrolü(32+Dizin);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    직렬글출력("\r\nPOWER OFF\r\n");
    while (makine_yazmaç(직렬장치+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    makine_yazmaç(0xfe100020ul)=0x5a000000u | (makine_yazmaç(0xfe100020ul)&~0xfffu) | 0x555;
    makine_yazmaç(0xfe100024ul)=0x5a000000u | 10;
    makine_yazmaç(0xfe10001cul)=0x5a000000u | (makine_yazmaç(0xfe10001cul)&~0x30u) | 0x20;
    기억장벽();
    for (;;) __asm__ volatile("wfe");
}

makine_Word 보드화면기억공간(void) {
    if (화면준비됨) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 geçerli_öğe 크기를 읽는다. */
    const uint32_t sorgu_değer[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 요청너비 = 640, 요청높이 = 480;
    for (size_t 순번 = 0; 순번 < sizeof(sorgu_değer)/4; 순번++) posta_kutusu_veri[순번] = sorgu_değer[순번];
    if (posta_kutusu() && posta_kutusu_veri[4] == 0x80000008u &&
        posta_kutusu_veri[5] >= 640 && posta_kutusu_veri[5] <= 1920 &&
        posta_kutusu_veri[6] >= 480 && posta_kutusu_veri[6] <= 1080) {
        요청너비 = posta_kutusu_veri[5]; 요청높이 = posta_kutusu_veri[6];
    }
    const uint32_t istek[] = {
        35 * 4, 0,
        0x48003, 8, 0, 요청너비, 요청높이,
        0x48004, 8, 0, 요청너비, 요청높이,
        0x48005, 4, 0, 32,
        0x48006, 4, 0, 1,
        0x48009, 8, 0, 0, 0,
        0x40001, 8, 0, 4096, 0,
        0x40008, 4, 0, 0,
        0
    };
    for (size_t 순번 = 0; 순번 < sizeof(istek)/4; 순번++) posta_kutusu_veri[순번] = istek[순번];
    // 위 메시지의 fiili_veri 길이를 kullanmak_değer: 태그 Ekleme_girdi 시 süre_değer 불일치를 방지한다.
    posta_kutusu_veri[0] = sizeof(istek);
    if (!posta_kutusu()) return 0;
    const unsigned 응답들[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned cevap_süre[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 순번 = 0; 순번 < sizeof(응답들)/sizeof(응답들[0]); 순번++)
        if (posta_kutusu_veri[응답들[순번]] != (0x80000000u | cevap_süre[순번])) return 0;
    uint32_t Arka_Plan_değer = posta_kutusu_veri[28] & 0x3fffffffu;
    uint32_t Boyut = posta_kutusu_veri[29];
    uint32_t 받은너비 = posta_kutusu_veri[5], 받은높이 = posta_kutusu_veri[6], GETİRİ_satır_aralığı = posta_kutusu_veri[33];
    if (posta_kutusu_veri[15] != 32 || posta_kutusu_veri[19] != 1 ||
        받은너비 < 640 || 받은너비 > 1920 || 받은높이 < 480 || 받은높이 > 1080 ||
        posta_kutusu_veri[10] < 받은너비 || posta_kutusu_veri[11] < 받은높이 || posta_kutusu_veri[23] || posta_kutusu_veri[24] ||
        !Arka_Plan_değer || Arka_Plan_değer < 0x1000000 || (Arka_Plan_değer & 3) || GETİRİ_satır_aralığı < 받은너비 * 4 || (GETİRİ_satır_aralığı & 3) ||
        (uint64_t)GETİRİ_satır_aralığı * 받은높이 > Boyut || (uint64_t)Arka_Plan_değer + Boyut > 0x40000000u)
        return 0;
    Pano_Hazırlan_çizim((volatile uint32_t *)(uintptr_t)Arka_Plan_değer, 받은너비, 받은높이, GETİRİ_satır_aralığı);
    화면준비됨 = 1;
    return 1;
}

// 단일 코어의 협력식 yazışma_değer. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 저장값[13]; } Bağlam;
static Bağlam 작업문맥들[3];
static unsigned char 쌓임공간들[2][65536] __attribute__((aligned(16)));
static int bilgi_teknolojisi_Koşu[3] = {1, 0, 0};
static int geçerli_Görev;
extern void bağlam_değiştirme(Bağlam *, Bağlam *);
extern void 자바작업(int32_t);
makine_Word Pano_ÖDEME(void) {
    network_poll();
    int Önceki_öğe = geçerli_Görev, Sonraki_öğe = (Önceki_öğe + 1) % 3;
    while (Sonraki_öğe != Önceki_öğe && !bilgi_teknolojisi_Koşu[Sonraki_öğe]) Sonraki_öğe = (Sonraki_öğe + 1) % 3;
    if (Sonraki_öğe != Önceki_öğe) {
        for (unsigned 순번 = 0; 순번 < 2; 순번++)
            if (bilgi_teknolojisi_Koşu[순번 + 1] && *(uint64_t *)쌓임공간들[순번] != 0x6b6f726f7373746bull)
                커널중단("task stack guard");
        geçerli_Görev = Sonraki_öğe;
        bağlam_değiştirme(&작업문맥들[Önceki_öğe], &작업문맥들[Sonraki_öğe]);
    }
    return 0;
}
static void Görev_IPL(void) {
    자바작업(geçerli_Görev);
    bilgi_teknolojisi_Koşu[geçerli_Görev] = 0;
    Pano_ÖDEME();
    커널중단("finished task resumed");
}
makine_Word Pano_Görev_açmak(makine_Word tanımlayıcı_değer) {
    if (tanımlayıcı_değer < 1 || tanımlayıcı_değer > 2 || bilgi_teknolojisi_Koşu[tanımlayıcı_değer]) return (uint32_t)-1;
    memset(&작업문맥들[tanımlayıcı_değer], 0, sizeof(Bağlam));
    *(uint64_t *)쌓임공간들[tanımlayıcı_değer - 1] = 0x6b6f726f7373746bull;
    작업문맥들[tanımlayıcı_değer].저장값[11] = (uintptr_t)Görev_IPL;
    작업문맥들[tanımlayıcı_değer].저장값[12] = (uintptr_t)(쌓임공간들[tanımlayıcı_değer - 1] + sizeof(쌓임공간들[0]));
    bilgi_teknolojisi_Koşu[tanımlayıcı_değer] = 1;
    return 0;
}
makine_Word Pano_Görev_Durum(makine_Word tanımlayıcı_değer) { return tanımlayıcı_değer < 3 ? bilgi_teknolojisi_Koşu[tanımlayıcı_değer] : (uint32_t)-1; }
extern makine_Word AOT_Bellek_ARA(makine_Word);
extern uint32_t 사용자상태읽기(unsigned, unsigned);
extern unsigned char 커널쌓임공간끝[];
makine_Word Pano_sorgu_Sistem(makine_Word girdi_değer, makine_Word Dizin) {
    if (girdi_değer==0) return 팔기억킬로바이트;
    if (girdi_değer==1) return ((uintptr_t)커널쌓임공간끝-0x80000+1023)/1024;
    if (girdi_değer==2 || girdi_değer==3) return AOT_Bellek_ARA(girdi_değer==3);
    if (girdi_değer==4) return 화면준비됨 ? (보드화면너비()*보드화면높이()*4+1023)/1024 : 0;
    if (girdi_değer==5) return 80*1024; /* yürütmek_komut ADRES_bölge 16 MiB + 네 세션 보관 ADRES_bölge. */
    if (girdi_değer>=20) return 사용자상태읽기(girdi_değer-20, Dizin);
    return 0;
}
int *pk_errno_location(void) { static int 오류들[3]; return &오류들[geçerli_Görev]; }
