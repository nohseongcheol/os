#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "NgănXếpMạng.h"
#include "string.h"
#include "ABITệp.h"
extern uintptr_t miliGiâyGọnBoMạch(void);
extern int32_t độDàiMụcHệTệpJava(int32_t), byteMụcHệTệpJava(int32_t,int32_t), cỡMụcHệTệpJava(int32_t);
extern int32_t sốLượngMụcHệTệpJava(void);
static int nhậnCổng = -1, điềuKhiển = -1, kếtNốiThủCông = -1, DữLiệu = -1;
static unsigned làTrongĐãGhiNhậtKý, ổnNgườiDùng, cỡDòng, saiDòng, chươngTrìnhThoátHẳn, tácVụĐangThựcThi, sứcChứaĐãDùng, sốLượngĐãGửi, cóThấtBại;
static unsigned cỡLờiĐáp, đãGửiLờiĐáp, sốCổngKếTiếp;
static uint32_t giờHoạtĐộng;
static char dòng[256], cácTrảLời[2048], tênMụcTệp[64], tênChuyểnGiao[64];
static unsigned char trạngTháiChuyểnGiao[16384];
static int bằng(const char *giáTrịĐầuTiên, const char *giáTrịThứHai) { while (*giáTrịĐầuTiên && *giáTrịĐầuTiên == *giáTrịThứHai) { giáTrịĐầuTiên++; giáTrịThứHai++; } return *giáTrịĐầuTiên == *giáTrịThứHai; }
static void lờiĐáp(const char *dữLiệuChuỗi) {
    size_t sốLượngPhầnMục = strlen(dữLiệuChuỗi);
    if (đãGửiLờiĐáp) { memmove(cácTrảLời, cácTrảLời + đãGửiLờiĐáp, cỡLờiĐáp - đãGửiLờiĐáp); cỡLờiĐáp -= đãGửiLờiĐáp; đãGửiLờiĐáp = 0; }
    if (sốLượngPhầnMục > sizeof(cácTrảLời) - cỡLờiĐáp) { chươngTrìnhThoátHẳn = 1; return; }
    memcpy(cácTrảLời + cỡLờiĐáp, dữLiệuChuỗi, sốLượngPhầnMục); cỡLờiĐáp += sốLượngPhầnMục;
}
static void giáTrịThuộcSố(unsigned giáTrị, char *dữLiệuKếtQuả, unsigned *sốLượngPhầnMục) {
    char sốLượngChữSố[10]; unsigned sốLượngMục = 0;
    do { sốLượngChữSố[sốLượngMục++] = '0' + giáTrị % 10; giáTrị /= 10; } while (giáTrị);
    while (sốLượngMục) dữLiệuKếtQuả[(*sốLượngPhầnMục)++] = sốLượngChữSố[--sốLượngMục];
}
static void dừngChuyểnGiao(void) {
    if (DữLiệu >= 0) đóngMạng(DữLiệu); if (kếtNốiThủCông >= 0) đóngMạng(kếtNốiThủCông);
    DữLiệu = kếtNốiThủCông = -1; tácVụĐangThựcThi = sứcChứaĐãDùng = sốLượngĐãGửi = cóThấtBại = 0;
}
static void ngắtKếtNối(void) {
    dừngChuyểnGiao(); if (điềuKhiển >= 0) đóngMạng(điềuKhiển); điềuKhiển = -1;
    làTrongĐãGhiNhậtKý = ổnNgườiDùng = cỡDòng = saiDòng = cỡLờiĐáp = đãGửiLờiĐáp = chươngTrìnhThoátHẳn = 0;
}
int điềuKhiểnChuyểnGiaoTệp(int hànhĐộng) {
    if (hànhĐộng == 2) return nhậnCổng >= 0;
    if (hànhĐộng == 0) { ngắtKếtNối(); if (nhậnCổng >= 0) đóngMạng(nhậnCổng); nhậnCổng = -1; return 0; }
    if (hànhĐộng != 1) return -22; if (nhậnCổng >= 0) return 0;
    nhậnCổng = tạoĐiểmCuốiỔCắmMạng(1); if (nhậnCổng < 0) return nhậnCổng;
    int giáTrịĐãTrảVề = ràngBuộcMạngGọn(nhậnCổng, đọcTìnhTrạngMạng(0,0), 21); if (!giáTrịĐãTrảVề) giáTrịĐãTrảVề = lắngNgheMạngGọn(nhậnCổng);
    if (giáTrịĐãTrảVề < 0) { đóngMạng(nhậnCổng); nhậnCổng = -1; } return giáTrịĐãTrảVề;
}
static int đườngDẫn(const char *tên) {
    unsigned sốLượngPhầnMục = 0; if (*tên == '/') tên++;
    if (!*tên || bằng(tên, ".") || bằng(tên, "..")) return 0;
    tênMụcTệp[sốLượngPhầnMục++] = '/';
    while (*tên) {
        unsigned char mãKýTự = *tên++;
        if (sốLượngPhầnMục >= 63 || mãKýTự < 32 || mãKýTự == 127 || mãKýTự == '/' || mãKýTự == '\\') return 0;
        tênMụcTệp[sốLượngPhầnMục++] = mãKýTự;
    }
    tênMụcTệp[sốLượngPhầnMục] = 0; return 1;
}
static void gửiDanhSách(int chiTiết) {
    sứcChứaĐãDùng = sốLượngĐãGửi = 0;
    for (int chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngMụcHệTệpJava(); chỉSốThứBậc++) {
        int sốLượngPhầnMục = độDàiMụcHệTệpJava(chỉSốThứBậc); if (sốLượngPhầnMục <= 0) continue;
        const char *phầnDẫnĐầu = chiTiết == 2 ? "type=file;size=" : chiTiết == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned sốLượngMục = strlen(phầnDẫnĐầu); memcpy(trạngTháiChuyểnGiao + sứcChứaĐãDùng, phầnDẫnĐầu, sốLượngMục); sứcChứaĐãDùng += sốLượngMục;
        if (chiTiết) giáTrịThuộcSố(cỡMụcHệTệpJava(chỉSốThứBậc), (char *)trạngTháiChuyểnGiao, &sứcChứaĐãDùng);
        const char *giáTrịHậuTố = chiTiết == 2 ? "; " : chiTiết == 1 ? " Jan 01 00:00 " : "";
        sốLượngMục = strlen(giáTrịHậuTố); memcpy(trạngTháiChuyểnGiao + sứcChứaĐãDùng, giáTrịHậuTố, sốLượngMục); sứcChứaĐãDùng += sốLượngMục;
        for (int thứBậcPhíaTrong = 0; thứBậcPhíaTrong < sốLượngPhầnMục; thứBậcPhíaTrong++) trạngTháiChuyểnGiao[sứcChứaĐãDùng++] = byteMụcHệTệpJava(chỉSốThứBậc,thứBậcPhíaTrong);
        trạngTháiChuyểnGiao[sứcChứaĐãDùng++] = '\r'; trạngTháiChuyểnGiao[sứcChứaĐãDùng++] = '\n';
    }
}
static void chuẩnBịKếtNốiThủCông(int đãMởRộng) {
    if (tácVụĐangThựcThi) { lờiĐáp("450 Transfer in progress\r\n"); return; }
    dừngChuyểnGiao(); kếtNốiThủCông = tạoĐiểmCuốiỔCắmMạng(1);
    if (kếtNốiThủCông >= 0) địaChỉỔCắmMạngDùngLại(kếtNốiThủCông);
    unsigned sốCổng = 50000 + sốCổngKếTiếp++ % 8;
    if (kếtNốiThủCông < 0 || ràngBuộcMạngGọn(kếtNốiThủCông, đọcTìnhTrạngMạng(0,0), sốCổng) || lắngNgheMạngGọn(kếtNốiThủCông)) {
        dừngChuyểnGiao(); lờiĐáp("425 Cannot open passive listener\r\n"); return;
    }
    char phảnHồi[96]; const char *phầnDẫnĐầu = đãMởRộng ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned sốLượngPhầnMục = strlen(phầnDẫnĐầu); memcpy(phảnHồi, phầnDẫnĐầu, sốLượngPhầnMục);
    if (đãMởRộng) { giáTrịThuộcSố(sốCổng, phảnHồi, &sốLượngPhầnMục); phảnHồi[sốLượngPhầnMục++] = '|'; }
    else {
        uint32_t địaChỉ=đọcTìnhTrạngMạng(0,0);
        for (int chỉSốVịTrí=24;chỉSốVịTrí>=0;chỉSốVịTrí-=8) { giáTrịThuộcSố((địaChỉ>>chỉSốVịTrí)&255,phảnHồi,&sốLượngPhầnMục);phảnHồi[sốLượngPhầnMục++]=','; }
        giáTrịThuộcSố(sốCổng / 256, phảnHồi, &sốLượngPhầnMục); phảnHồi[sốLượngPhầnMục++] = ','; giáTrịThuộcSố(sốCổng % 256, phảnHồi, &sốLượngPhầnMục);
    }
    phảnHồi[sốLượngPhầnMục++] = ')'; phảnHồi[sốLượngPhầnMục++] = '\r'; phảnHồi[sốLượngPhầnMục++] = '\n'; phảnHồi[sốLượngPhầnMục] = 0; lờiĐáp(phảnHồi);
}
static void lệnh(void) {
    dòng[cỡDòng] = 0;
    char *cácĐốiSốBổSung = dòng; while (*cácĐốiSốBổSung && *cácĐốiSốBổSung != ' ') { if (*cácĐốiSốBổSung >= 'a' && *cácĐốiSốBổSung <= 'z') *cácĐốiSốBổSung -= 32; cácĐốiSốBổSung++; }
    if (*cácĐốiSốBổSung) *cácĐốiSốBổSung++ = 0; while (*cácĐốiSốBổSung == ' ') cácĐốiSốBổSung++;
    if (bằng(dòng, "QUIT")) { dừngChuyểnGiao(); lờiĐáp("221 Goodbye\r\n"); chươngTrìnhThoátHẳn = 1; return; }
    if (bằng(dòng, "NOOP")) { lờiĐáp("200 OK\r\n"); return; }
    if (bằng(dòng, "SYST")) { lờiĐáp("215 UNIX Type: L8\r\n"); return; }
    if (bằng(dòng, "FEAT")) { lờiĐáp("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (bằng(dòng, "USER")) { làTrongĐãGhiNhậtKý = 0; ổnNgườiDùng = bằng(cácĐốiSốBổSung, "anonymous") || bằng(cácĐốiSốBổSung, "jkoros"); lờiĐáp(ổnNgườiDùng ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (bằng(dòng, "PASS")) { làTrongĐãGhiNhậtKý = ổnNgườiDùng; lờiĐáp(làTrongĐãGhiNhậtKý ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!làTrongĐãGhiNhậtKý) { lờiĐáp("530 Login first\r\n"); return; }
    if (bằng(dòng, "PWD")) lờiĐáp("257 \"/\"\r\n");
    else if (bằng(dòng, "CWD")) lờiĐáp(bằng(cácĐốiSốBổSung, "/") || bằng(cácĐốiSốBổSung, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (bằng(dòng, "TYPE")) lờiĐáp(bằng(cácĐốiSốBổSung, "I") || bằng(cácĐốiSốBổSung, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (bằng(dòng, "OPTS")) lờiĐáp(bằng(cácĐốiSốBổSung, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (bằng(dòng, "PASV")) chuẩnBịKếtNốiThủCông(0);
    else if (bằng(dòng, "EPSV")) { if (*cácĐốiSốBổSung && !bằng(cácĐốiSốBổSung, "1")) lờiĐáp("522 IPv4 only\r\n"); else chuẩnBịKếtNốiThủCông(1); }
    else if (bằng(dòng, "ABOR")) { dừngChuyểnGiao(); lờiĐáp("226 Transfer aborted\r\n"); }
    else if (bằng(dòng, "DELE")) { lờiĐáp(đườngDẫn(cácĐốiSốBổSung) && pk_unlink(tênMụcTệp) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (bằng(dòng, "LIST") || bằng(dòng, "NLST") || bằng(dòng, "MLSD")) {
        if (tácVụĐangThựcThi) { lờiĐáp("450 Transfer in progress\r\n"); return; }
        if (kếtNốiThủCông < 0 && DữLiệu < 0) { lờiĐáp("425 Use PASV or EPSV\r\n"); return; }
        if (*cácĐốiSốBổSung && !bằng(cácĐốiSốBổSung,"/") && !bằng(cácĐốiSốBổSung,".") && !bằng(cácĐốiSốBổSung,"-a") && !bằng(cácĐốiSốBổSung,"-l") && !bằng(cácĐốiSốBổSung,"-la")) { lờiĐáp("550 Root listing only\r\n"); return; }
        gửiDanhSách(bằng(dòng,"MLSD") ? 2 : bằng(dòng,"LIST") ? 1 : 0); tácVụĐangThựcThi = 2;
        lờiĐáp("150 Opening directory listing\r\n");
    }
    else if (bằng(dòng, "SIZE")) {
        if (!đườngDẫn(cácĐốiSốBổSung)) { lờiĐáp("550 Invalid filename\r\n"); return; }
        int thẻXửLýTệp = pk_open(tênMụcTệp, đọcGiáTrịChỉ, 0); if (thẻXửLýTệp < 0) { lờiĐáp("550 File unavailable\r\n"); return; }
        int cỡ = pk_size(thẻXửLýTệp); pk_close(thẻXửLýTệp); char phảnHồi[32] = "213 "; unsigned sốLượngPhầnMục = 4;
        giáTrịThuộcSố(cỡ, phảnHồi, &sốLượngPhầnMục); phảnHồi[sốLượngPhầnMục++] = '\r'; phảnHồi[sốLượngPhầnMục++] = '\n'; phảnHồi[sốLượngPhầnMục] = 0; lờiĐáp(phảnHồi);
    } else if (bằng(dòng, "STOR") || bằng(dòng, "RETR")) {
        if (tácVụĐangThựcThi) { lờiĐáp("450 Transfer in progress\r\n"); return; }
        if (kếtNốiThủCông < 0 && DữLiệu < 0) { lờiĐáp("425 Use PASV or EPSV\r\n"); return; }
        if (!đườngDẫn(cácĐốiSốBổSung)) { lờiĐáp("550 Invalid filename\r\n"); return; }
        tácVụĐangThựcThi = bằng(dòng, "STOR") ? 1 : 2; sứcChứaĐãDùng = sốLượngĐãGửi = cóThấtBại = 0;
        memcpy(tênChuyểnGiao, tênMụcTệp, strlen(tênMụcTệp) + 1);
        if (tácVụĐangThựcThi == 2) {
            int thẻXửLýTệp = pk_open(tênMụcTệp, đọcGiáTrịChỉ, 0);
            if (thẻXửLýTệp < 0) { tácVụĐangThựcThi = 0; lờiĐáp("550 File unavailable\r\n"); return; }
            int sốLượngPhầnMục = pk_read(thẻXửLýTệp, trạngTháiChuyểnGiao, sizeof(trạngTháiChuyểnGiao)); pk_close(thẻXửLýTệp);
            if (sốLượngPhầnMục < 0) { tácVụĐangThựcThi = 0; lờiĐáp("451 Read failed\r\n"); return; } sứcChứaĐãDùng = sốLượngPhầnMục;
        }
        lờiĐáp("150 Opening binary data connection\r\n");
    } else lờiĐáp("502 Command not implemented\r\n");
}
void xemXétChuyểnGiaoTệp(void) {
    if (nhậnCổng < 0) return;
    int kếtNốiĐiVào = chấpNhậnMạngGọn(nhậnCổng);
    if (kếtNốiĐiVào >= 0) {
        if (điềuKhiển >= 0) { ghiMạngGọn(kếtNốiĐiVào, "421 One session at a time\r\n", 27); đóngMạng(kếtNốiĐiVào); }
        else { điềuKhiển = kếtNốiĐiVào; giờHoạtĐộng = miliGiâyGọnBoMạch(); lờiĐáp("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (điềuKhiển < 0) return;
    if ((uint32_t)(miliGiâyGọnBoMạch() - giờHoạtĐộng) > 60000) { ngắtKếtNối(); return; }
    if (!chươngTrìnhThoátHẳn) for (unsigned hạnMức = 0; hạnMức < 256; hạnMức++) {
        unsigned char mãKýTự; int giáTrịĐãTrảVề = đọcMạngGọn(điềuKhiển, &mãKýTự, 1);
        if (giáTrịĐãTrảVề == -11) break; if (giáTrịĐãTrảVề <= 0) { ngắtKếtNối(); return; } giờHoạtĐộng = miliGiâyGọnBoMạch();
        if (mãKýTự == '\n') { if (saiDòng) lờiĐáp("500 Command too long or invalid\r\n"); else lệnh(); cỡDòng = saiDòng = 0; if (chươngTrìnhThoátHẳn) break; }
        else if (mãKýTự != '\r') { if (!mãKýTự || cỡDòng >= sizeof(dòng) - 1) saiDòng = 1; else dòng[cỡDòng++] = mãKýTự; }
    }
    if (kếtNốiThủCông >= 0 && DữLiệu < 0) {
        int giáTrịĐãTrảVề = chấpNhậnMạngGọn(kếtNốiThủCông);
        if (giáTrịĐãTrảVề >= 0) {
            if (địaChỉĐốiTácMạngGọn(giáTrịĐãTrảVề) != địaChỉĐốiTácMạngGọn(điềuKhiển)) đóngMạng(giáTrịĐãTrảVề);
            else { DữLiệu = giáTrịĐãTrảVề; đóngMạng(kếtNốiThủCông); kếtNốiThủCông = -1; giờHoạtĐộng = miliGiâyGọnBoMạch(); }
        }
    }
    if (tácVụĐangThựcThi == 1 && DữLiệu >= 0) for (unsigned hạnMức = 0; hạnMức < 8; hạnMức++) {
        unsigned char khốiDữLiệu[512]; int sốLượngPhầnMục = đọcMạngGọn(DữLiệu, khốiDữLiệu, sizeof(khốiDữLiệu));
        if (sốLượngPhầnMục == -11) break;
        if (sốLượngPhầnMục < 0) { dừngChuyểnGiao(); lờiĐáp("426 Data connection failed\r\n"); break; }
        giờHoạtĐộng = miliGiâyGọnBoMạch();
        if (sốLượngPhầnMục == 0) {
            int kếtQuả = -1;
            if (!cóThấtBại) {
                int thẻXửLýTệp = pk_open(tênChuyểnGiao, ghiGiáTrịChỉ | ThiếuNếuTạo | CácNộiDungCắtNgắn, 0600);
                if (thẻXửLýTệp >= 0) { kếtQuả = pk_write(thẻXửLýTệp, trạngTháiChuyểnGiao, sứcChứaĐãDùng); pk_close(thẻXửLýTệp); }
            }
            int làĐãThànhCông = !cóThấtBại && kếtQuả == (int)sứcChứaĐãDùng; dừngChuyểnGiao(); lờiĐáp(làĐãThànhCông ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)sốLượngPhầnMục > sizeof(trạngTháiChuyểnGiao) - sứcChứaĐãDùng) cóThấtBại = 1;
        if (!cóThấtBại) { memcpy(trạngTháiChuyểnGiao + sứcChứaĐãDùng, khốiDữLiệu, sốLượngPhầnMục); sứcChứaĐãDùng += sốLượngPhầnMục; }
    }
    if (tácVụĐangThựcThi == 2 && DữLiệu >= 0) {
        int sốLượngPhầnMục = ghiMạngGọn(DữLiệu, trạngTháiChuyểnGiao + sốLượngĐãGửi, sứcChứaĐãDùng - sốLượngĐãGửi);
        if (sốLượngPhầnMục >= 0) { sốLượngĐãGửi += sốLượngPhầnMục; giờHoạtĐộng = miliGiâyGọnBoMạch(); if (sốLượngĐãGửi == sứcChứaĐãDùng) { dừngChuyểnGiao(); lờiĐáp("226 Transfer complete\r\n"); } }
        else if (sốLượngPhầnMục != -11) { dừngChuyểnGiao(); lờiĐáp("426 Data connection failed\r\n"); }
    }
    if (đãGửiLờiĐáp < cỡLờiĐáp) {
        int sốLượngPhầnMục = ghiMạngGọn(điềuKhiển, cácTrảLời + đãGửiLờiĐáp, cỡLờiĐáp - đãGửiLờiĐáp);
        if (sốLượngPhầnMục > 0) đãGửiLờiĐáp += sốLượngPhầnMục; else if (sốLượngPhầnMục != -11) { ngắtKếtNối(); return; }
    }
    if (đãGửiLờiĐáp == cỡLờiĐáp) { cỡLờiĐáp = đãGửiLờiĐáp = 0; if (chươngTrìnhThoátHẳn) ngắtKếtNối(); }
}
