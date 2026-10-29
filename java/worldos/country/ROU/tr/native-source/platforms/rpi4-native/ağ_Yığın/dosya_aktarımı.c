#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "ağ_Yığın.h"
#include "string.h"
#include "Dosya_ABI.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int almak_taşımak = -1, denetim = -1, el_ile_cxn = -1, veri = -1;
static unsigned 로그인됨, kullanıcı_Tamam, hat_boyutlandırmak, 줄오류, çıkış_program, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned yanıt_boyutlandırmak, 응답전송량, Sonraki_bağlantı_noktası_numarası;
static uint32_t Etkinlik;
static char girdi_satırı[256], 응답모음[2048], Dosya_girdi_ad[64], devir_ad[64];
static unsigned char devir_Durum[16384];
static int 같은지(const char *첫째값, const char *SANİYE_değer) { while (*첫째값 && *첫째값 == *SANİYE_değer) { 첫째값++; SANİYE_değer++; } return *첫째값 == *SANİYE_değer; }
static void yanıt(const char *dize_veri) {
    size_t öğe_BAĞ_DEĞ_SAY = strlen(dize_veri);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, yanıt_boyutlandırmak - 응답전송량); yanıt_boyutlandırmak -= 응답전송량; 응답전송량 = 0; }
    if (öğe_BAĞ_DEĞ_SAY > sizeof(응답모음) - yanıt_boyutlandırmak) { çıkış_program = 1; return; }
    memcpy(응답모음 + yanıt_boyutlandırmak, dize_veri, öğe_BAĞ_DEĞ_SAY); yanıt_boyutlandırmak += öğe_BAĞ_DEĞ_SAY;
}
static void 수치(unsigned değer, char *KR_veri, unsigned *öğe_BAĞ_DEĞ_SAY) {
    char rakam_BAĞ_DEĞ_SAY[10]; unsigned girdi_BAĞ_DEĞ_SAY = 0;
    do { rakam_BAĞ_DEĞ_SAY[girdi_BAĞ_DEĞ_SAY++] = '0' + değer % 10; değer /= 10; } while (değer);
    while (girdi_BAĞ_DEĞ_SAY) KR_veri[(*öğe_BAĞ_DEĞ_SAY)++] = rakam_BAĞ_DEĞ_SAY[--girdi_BAĞ_DEĞ_SAY];
}
static void Dur_devir(void) {
    if (veri >= 0) Kapat_ağ(veri); if (el_ile_cxn >= 0) Kapat_ağ(el_ile_cxn);
    veri = el_ile_cxn = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void bağlantıyı_kesmek(void) {
    Dur_devir(); if (denetim >= 0) Kapat_ağ(denetim); denetim = -1;
    로그인됨 = kullanıcı_Tamam = hat_boyutlandırmak = 줄오류 = yanıt_boyutlandırmak = 응답전송량 = çıkış_program = 0;
}
int dosya_aktarımı_denetim(int Eylem) {
    if (Eylem == 2) return almak_taşımak >= 0;
    if (Eylem == 0) { bağlantıyı_kesmek(); if (almak_taşımak >= 0) Kapat_ağ(almak_taşımak); almak_taşımak = -1; return 0; }
    if (Eylem != 1) return -22; if (almak_taşımak >= 0) return 0;
    almak_taşımak = açmak_yuva_uç_nokta(1); if (almak_taşımak < 0) return almak_taşımak;
    int 반환값 = NET_BIND(almak_taşımak, 망상태읽기(0,0), 21); if (!반환값) 반환값 = NET_dinlemek(almak_taşımak);
    if (반환값 < 0) { Kapat_ağ(almak_taşımak); almak_taşımak = -1; } return 반환값;
}
static int yol(const char *İsim) {
    unsigned öğe_BAĞ_DEĞ_SAY = 0; if (*İsim == '/') İsim++;
    if (!*İsim || 같은지(İsim, ".") || 같은지(İsim, "..")) return 0;
    Dosya_girdi_ad[öğe_BAĞ_DEĞ_SAY++] = '/';
    while (*İsim) {
        unsigned char kod_noktası = *İsim++;
        if (öğe_BAĞ_DEĞ_SAY >= 63 || kod_noktası < 32 || kod_noktası == 127 || kod_noktası == '/' || kod_noktası == '\\') return 0;
        Dosya_girdi_ad[öğe_BAĞ_DEĞ_SAY++] = kod_noktası;
    }
    Dosya_girdi_ad[öğe_BAĞ_DEĞ_SAY] = 0; return 1;
}
static void göndermek_Liste(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int öğe_BAĞ_DEĞ_SAY = 자바파일항목길이(순번); if (öğe_BAĞ_DEĞ_SAY <= 0) continue;
        const char *satır_aralığı_parça = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned girdi_BAĞ_DEĞ_SAY = strlen(satır_aralığı_parça); memcpy(devir_Durum + 사용량, satır_aralığı_parça, girdi_BAĞ_DEĞ_SAY); 사용량 += girdi_BAĞ_DEĞ_SAY;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)devir_Durum, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        girdi_BAĞ_DEĞ_SAY = strlen(뒷부분); memcpy(devir_Durum + 사용량, 뒷부분, girdi_BAĞ_DEĞ_SAY); 사용량 += girdi_BAĞ_DEĞ_SAY;
        for (int 안쪽순번 = 0; 안쪽순번 < öğe_BAĞ_DEĞ_SAY; 안쪽순번++) devir_Durum[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        devir_Durum[사용량++] = '\r'; devir_Durum[사용량++] = '\n';
    }
}
static void Hazırlan_el_ile_cxn(int 확장여부) {
    if (수행작업) { yanıt("450 Transfer in progress\r\n"); return; }
    Dur_devir(); el_ile_cxn = açmak_yuva_uç_nokta(1);
    if (el_ile_cxn >= 0) 통신주소재사용(el_ile_cxn);
    unsigned bağlantı_noktası_numarası = 50000 + Sonraki_bağlantı_noktası_numarası++ % 8;
    if (el_ile_cxn < 0 || NET_BIND(el_ile_cxn, 망상태읽기(0,0), bağlantı_noktası_numarası) || NET_dinlemek(el_ile_cxn)) {
        Dur_devir(); yanıt("425 Cannot open passive listener\r\n"); return;
    }
    char cevap[96]; const char *satır_aralığı_parça = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned öğe_BAĞ_DEĞ_SAY = strlen(satır_aralığı_parça); memcpy(cevap, satır_aralığı_parça, öğe_BAĞ_DEĞ_SAY);
    if (확장여부) { 수치(bağlantı_noktası_numarası, cevap, &öğe_BAĞ_DEĞ_SAY); cevap[öğe_BAĞ_DEĞ_SAY++] = '|'; }
    else {
        uint32_t ADRES=망상태읽기(0,0);
        for (int konum_dizini=24;konum_dizini>=0;konum_dizini-=8) { 수치((ADRES>>konum_dizini)&255,cevap,&öğe_BAĞ_DEĞ_SAY);cevap[öğe_BAĞ_DEĞ_SAY++]=','; }
        수치(bağlantı_noktası_numarası / 256, cevap, &öğe_BAĞ_DEĞ_SAY); cevap[öğe_BAĞ_DEĞ_SAY++] = ','; 수치(bağlantı_noktası_numarası % 256, cevap, &öğe_BAĞ_DEĞ_SAY);
    }
    cevap[öğe_BAĞ_DEĞ_SAY++] = ')'; cevap[öğe_BAĞ_DEĞ_SAY++] = '\r'; cevap[öğe_BAĞ_DEĞ_SAY++] = '\n'; cevap[öğe_BAĞ_DEĞ_SAY] = 0; yanıt(cevap);
}
static void komut(void) {
    girdi_satırı[hat_boyutlandırmak] = 0;
    char *부가인수 = girdi_satırı; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(girdi_satırı, "QUIT")) { Dur_devir(); yanıt("221 Goodbye\r\n"); çıkış_program = 1; return; }
    if (같은지(girdi_satırı, "NOOP")) { yanıt("200 OK\r\n"); return; }
    if (같은지(girdi_satırı, "SYST")) { yanıt("215 UNIX Type: L8\r\n"); return; }
    if (같은지(girdi_satırı, "FEAT")) { yanıt("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(girdi_satırı, "USER")) { 로그인됨 = 0; kullanıcı_Tamam = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); yanıt(kullanıcı_Tamam ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(girdi_satırı, "PASS")) { 로그인됨 = kullanıcı_Tamam; yanıt(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { yanıt("530 Login first\r\n"); return; }
    if (같은지(girdi_satırı, "PWD")) yanıt("257 \"/\"\r\n");
    else if (같은지(girdi_satırı, "CWD")) yanıt(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(girdi_satırı, "TYPE")) yanıt(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(girdi_satırı, "OPTS")) yanıt(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(girdi_satırı, "PASV")) Hazırlan_el_ile_cxn(0);
    else if (같은지(girdi_satırı, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) yanıt("522 IPv4 only\r\n"); else Hazırlan_el_ile_cxn(1); }
    else if (같은지(girdi_satırı, "ABOR")) { Dur_devir(); yanıt("226 Transfer aborted\r\n"); }
    else if (같은지(girdi_satırı, "DELE")) { yanıt(yol(부가인수) && pk_unlink(Dosya_girdi_ad) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(girdi_satırı, "LIST") || 같은지(girdi_satırı, "NLST") || 같은지(girdi_satırı, "MLSD")) {
        if (수행작업) { yanıt("450 Transfer in progress\r\n"); return; }
        if (el_ile_cxn < 0 && veri < 0) { yanıt("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { yanıt("550 Root listing only\r\n"); return; }
        göndermek_Liste(같은지(girdi_satırı,"MLSD") ? 2 : 같은지(girdi_satırı,"LIST") ? 1 : 0); 수행작업 = 2;
        yanıt("150 Opening directory listing\r\n");
    }
    else if (같은지(girdi_satırı, "SIZE")) {
        if (!yol(부가인수)) { yanıt("550 Invalid filename\r\n"); return; }
        int dosya_tanıtıcısı = pk_open(Dosya_girdi_ad, salt_okunur_değer, 0); if (dosya_tanıtıcısı < 0) { yanıt("550 File unavailable\r\n"); return; }
        int Boyut = pk_size(dosya_tanıtıcısı); pk_close(dosya_tanıtıcısı); char cevap[32] = "213 "; unsigned öğe_BAĞ_DEĞ_SAY = 4;
        수치(Boyut, cevap, &öğe_BAĞ_DEĞ_SAY); cevap[öğe_BAĞ_DEĞ_SAY++] = '\r'; cevap[öğe_BAĞ_DEĞ_SAY++] = '\n'; cevap[öğe_BAĞ_DEĞ_SAY] = 0; yanıt(cevap);
    } else if (같은지(girdi_satırı, "STOR") || 같은지(girdi_satırı, "RETR")) {
        if (수행작업) { yanıt("450 Transfer in progress\r\n"); return; }
        if (el_ile_cxn < 0 && veri < 0) { yanıt("425 Use PASV or EPSV\r\n"); return; }
        if (!yol(부가인수)) { yanıt("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(girdi_satırı, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(devir_ad, Dosya_girdi_ad, strlen(Dosya_girdi_ad) + 1);
        if (수행작업 == 2) {
            int dosya_tanıtıcısı = pk_open(Dosya_girdi_ad, salt_okunur_değer, 0);
            if (dosya_tanıtıcısı < 0) { 수행작업 = 0; yanıt("550 File unavailable\r\n"); return; }
            int öğe_BAĞ_DEĞ_SAY = pk_read(dosya_tanıtıcısı, devir_Durum, sizeof(devir_Durum)); pk_close(dosya_tanıtıcısı);
            if (öğe_BAĞ_DEĞ_SAY < 0) { 수행작업 = 0; yanıt("451 Read failed\r\n"); return; } 사용량 = öğe_BAĞ_DEĞ_SAY;
        }
        yanıt("150 Opening binary data connection\r\n");
    } else yanıt("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (almak_taşımak < 0) return;
    int Gelen_cxn = NET_kabul_etmek(almak_taşımak);
    if (Gelen_cxn >= 0) {
        if (denetim >= 0) { NET_yazma(Gelen_cxn, "421 One session at a time\r\n", 27); Kapat_ağ(Gelen_cxn); }
        else { denetim = Gelen_cxn; Etkinlik = 보드밀리초(); yanıt("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (denetim < 0) return;
    if ((uint32_t)(보드밀리초() - Etkinlik) > 60000) { bağlantıyı_kesmek(); return; }
    if (!çıkış_program) for (unsigned bütçe = 0; bütçe < 256; bütçe++) {
        unsigned char kod_noktası; int 반환값 = 통신읽기(denetim, &kod_noktası, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { bağlantıyı_kesmek(); return; } Etkinlik = 보드밀리초();
        if (kod_noktası == '\n') { if (줄오류) yanıt("500 Command too long or invalid\r\n"); else komut(); hat_boyutlandırmak = 줄오류 = 0; if (çıkış_program) break; }
        else if (kod_noktası != '\r') { if (!kod_noktası || hat_boyutlandırmak >= sizeof(girdi_satırı) - 1) 줄오류 = 1; else girdi_satırı[hat_boyutlandırmak++] = kod_noktası; }
    }
    if (el_ile_cxn >= 0 && veri < 0) {
        int 반환값 = NET_kabul_etmek(el_ile_cxn);
        if (반환값 >= 0) {
            if (NET_eş_ADRES(반환값) != NET_eş_ADRES(denetim)) Kapat_ağ(반환값);
            else { veri = 반환값; Kapat_ağ(el_ile_cxn); el_ile_cxn = -1; Etkinlik = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && veri >= 0) for (unsigned bütçe = 0; bütçe < 8; bütçe++) {
        unsigned char veri_bloğu[512]; int öğe_BAĞ_DEĞ_SAY = 통신읽기(veri, veri_bloğu, sizeof(veri_bloğu));
        if (öğe_BAĞ_DEĞ_SAY == -11) break;
        if (öğe_BAĞ_DEĞ_SAY < 0) { Dur_devir(); yanıt("426 Data connection failed\r\n"); break; }
        Etkinlik = 보드밀리초();
        if (öğe_BAĞ_DEĞ_SAY == 0) {
            int sonuç = -1;
            if (!실패여부) {
                int dosya_tanıtıcısı = pk_open(devir_ad, sadece_yazılabilir_değer | 없으면만들기 | kesmek_içindekiler, 0600);
                if (dosya_tanıtıcısı >= 0) { sonuç = pk_write(dosya_tanıtıcısı, devir_Durum, 사용량); pk_close(dosya_tanıtıcısı); }
            }
            int 성공여부 = !실패여부 && sonuç == (int)사용량; Dur_devir(); yanıt(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)öğe_BAĞ_DEĞ_SAY > sizeof(devir_Durum) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(devir_Durum + 사용량, veri_bloğu, öğe_BAĞ_DEĞ_SAY); 사용량 += öğe_BAĞ_DEĞ_SAY; }
    }
    if (수행작업 == 2 && veri >= 0) {
        int öğe_BAĞ_DEĞ_SAY = NET_yazma(veri, devir_Durum + 보낸수, 사용량 - 보낸수);
        if (öğe_BAĞ_DEĞ_SAY >= 0) { 보낸수 += öğe_BAĞ_DEĞ_SAY; Etkinlik = 보드밀리초(); if (보낸수 == 사용량) { Dur_devir(); yanıt("226 Transfer complete\r\n"); } }
        else if (öğe_BAĞ_DEĞ_SAY != -11) { Dur_devir(); yanıt("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < yanıt_boyutlandırmak) {
        int öğe_BAĞ_DEĞ_SAY = NET_yazma(denetim, 응답모음 + 응답전송량, yanıt_boyutlandırmak - 응답전송량);
        if (öğe_BAĞ_DEĞ_SAY > 0) 응답전송량 += öğe_BAĞ_DEĞ_SAY; else if (öğe_BAĞ_DEĞ_SAY != -11) { bağlantıyı_kesmek(); return; }
    }
    if (응답전송량 == yanıt_boyutlandırmak) { yanıt_boyutlandırmak = 응답전송량 = 0; if (çıkış_program) bağlantıyı_kesmek(); }
}
