#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Şəbəkə_Yığın.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, nəzarət = -1, əl_ilə_qoşulma = -1, verilənlər = -1;
static unsigned 로그인됨, istifadəçi_OK, xətt_ölçünü_dəyişmək, 줄오류, çıxış_proqram, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned cavab_ölçünü_dəyişmək, 응답전송량, 다음접속번호;
static uint32_t Fəaliyyət;
static char Giriş[256], 응답모음[2048], fayl_daxiletmə_ad[64], ötürmə_ad[64];
static unsigned char ötürmə_vəziyyət[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void cavab(const char *sətir_verilənlər) {
    size_t element_COUNT = strlen(sətir_verilənlər);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, cavab_ölçünü_dəyişmək - 응답전송량); cavab_ölçünü_dəyişmək -= 응답전송량; 응답전송량 = 0; }
    if (element_COUNT > sizeof(응답모음) - cavab_ölçünü_dəyişmək) { çıxış_proqram = 1; return; }
    memcpy(응답모음 + cavab_ölçünü_dəyişmək, sətir_verilənlər, element_COUNT); cavab_ölçünü_dəyişmək += element_COUNT;
}
static void 수치(unsigned VALUE, char *ölçü_verilənlər, unsigned *element_COUNT) {
    char rəqəm_COUNT[10]; unsigned daxiletmə_COUNT = 0;
    do { rəqəm_COUNT[daxiletmə_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (daxiletmə_COUNT) ölçü_verilənlər[(*element_COUNT)++] = rəqəm_COUNT[--daxiletmə_COUNT];
}
static void Dayandır_ötürmə(void) {
    if (verilənlər >= 0) bağlamaq_Şəbəkə(verilənlər); if (əl_ilə_qoşulma >= 0) bağlamaq_Şəbəkə(əl_ilə_qoşulma);
    verilənlər = əl_ilə_qoşulma = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void bağlantını_kəsmək(void) {
    Dayandır_ötürmə(); if (nəzarət >= 0) bağlamaq_Şəbəkə(nəzarət); nəzarət = -1;
    로그인됨 = istifadəçi_OK = xətt_ölçünü_dəyişmək = 줄오류 = cavab_ölçünü_dəyişmək = 응답전송량 = çıxış_proqram = 0;
}
int fayl_ötürmə_nəzarət(int Gedişat) {
    if (Gedişat == 2) return 수신창구 >= 0;
    if (Gedişat == 0) { bağlantını_kəsmək(); if (수신창구 >= 0) bağlamaq_Şəbəkə(수신창구); 수신창구 = -1; return 0; }
    if (Gedişat != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { bağlamaq_Şəbəkə(수신창구); 수신창구 = -1; } return 반환값;
}
static int Cığır(const char *Ad) {
    unsigned element_COUNT = 0; if (*Ad == '/') Ad++;
    if (!*Ad || 같은지(Ad, ".") || 같은지(Ad, "..")) return 0;
    fayl_daxiletmə_ad[element_COUNT++] = '/';
    while (*Ad) {
        unsigned char simvol_kodu = *Ad++;
        if (element_COUNT >= 63 || simvol_kodu < 32 || simvol_kodu == 127 || simvol_kodu == '/' || simvol_kodu == '\\') return 0;
        fayl_daxiletmə_ad[element_COUNT++] = simvol_kodu;
    }
    fayl_daxiletmə_ad[element_COUNT] = 0; return 1;
}
static void göndərmək_Siyahı(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int element_COUNT = 자바파일항목길이(순번); if (element_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned daxiletmə_COUNT = strlen(앞부분); memcpy(ötürmə_vəziyyət + 사용량, 앞부분, daxiletmə_COUNT); 사용량 += daxiletmə_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)ötürmə_vəziyyət, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        daxiletmə_COUNT = strlen(뒷부분); memcpy(ötürmə_vəziyyət + 사용량, 뒷부분, daxiletmə_COUNT); 사용량 += daxiletmə_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < element_COUNT; 안쪽순번++) ötürmə_vəziyyət[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        ötürmə_vəziyyət[사용량++] = '\r'; ötürmə_vəziyyət[사용량++] = '\n';
    }
}
static void Hazırla_əl_ilə_qoşulma(int 확장여부) {
    if (수행작업) { cavab("450 Transfer in progress\r\n"); return; }
    Dayandır_ötürmə(); əl_ilə_qoşulma = 통신끝점만들기(1);
    if (əl_ilə_qoşulma >= 0) 통신주소재사용(əl_ilə_qoşulma);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (əl_ilə_qoşulma < 0 || 망주소묶기(əl_ilə_qoşulma, 망상태읽기(0,0), 접속번호) || 연결기다리기(əl_ilə_qoşulma)) {
        Dayandır_ötürmə(); cavab("425 Cannot open passive listener\r\n"); return;
    }
    char video_münasibət[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned element_COUNT = strlen(앞부분); memcpy(video_münasibət, 앞부분, element_COUNT);
    if (확장여부) { 수치(접속번호, video_münasibət, &element_COUNT); video_münasibət[element_COUNT++] = '|'; }
    else {
        uint32_t ünvan=망상태읽기(0,0);
        for (int yerinə_qoymaq_INDEX=24;yerinə_qoymaq_INDEX>=0;yerinə_qoymaq_INDEX-=8) { 수치((ünvan>>yerinə_qoymaq_INDEX)&255,video_münasibət,&element_COUNT);video_münasibət[element_COUNT++]=','; }
        수치(접속번호 / 256, video_münasibət, &element_COUNT); video_münasibət[element_COUNT++] = ','; 수치(접속번호 % 256, video_münasibət, &element_COUNT);
    }
    video_münasibət[element_COUNT++] = ')'; video_münasibət[element_COUNT++] = '\r'; video_münasibət[element_COUNT++] = '\n'; video_münasibət[element_COUNT] = 0; cavab(video_münasibət);
}
static void Əmr(void) {
    Giriş[xətt_ölçünü_dəyişmək] = 0;
    char *부가인수 = Giriş; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(Giriş, "QUIT")) { Dayandır_ötürmə(); cavab("221 Goodbye\r\n"); çıxış_proqram = 1; return; }
    if (같은지(Giriş, "NOOP")) { cavab("200 OK\r\n"); return; }
    if (같은지(Giriş, "SYST")) { cavab("215 UNIX Type: L8\r\n"); return; }
    if (같은지(Giriş, "FEAT")) { cavab("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(Giriş, "USER")) { 로그인됨 = 0; istifadəçi_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); cavab(istifadəçi_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(Giriş, "PASS")) { 로그인됨 = istifadəçi_OK; cavab(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { cavab("530 Login first\r\n"); return; }
    if (같은지(Giriş, "PWD")) cavab("257 \"/\"\r\n");
    else if (같은지(Giriş, "CWD")) cavab(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(Giriş, "TYPE")) cavab(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(Giriş, "OPTS")) cavab(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(Giriş, "PASV")) Hazırla_əl_ilə_qoşulma(0);
    else if (같은지(Giriş, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) cavab("522 IPv4 only\r\n"); else Hazırla_əl_ilə_qoşulma(1); }
    else if (같은지(Giriş, "ABOR")) { Dayandır_ötürmə(); cavab("226 Transfer aborted\r\n"); }
    else if (같은지(Giriş, "DELE")) { cavab(Cığır(부가인수) && pk_unlink(fayl_daxiletmə_ad) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(Giriş, "LIST") || 같은지(Giriş, "NLST") || 같은지(Giriş, "MLSD")) {
        if (수행작업) { cavab("450 Transfer in progress\r\n"); return; }
        if (əl_ilə_qoşulma < 0 && verilənlər < 0) { cavab("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { cavab("550 Root listing only\r\n"); return; }
        göndərmək_Siyahı(같은지(Giriş,"MLSD") ? 2 : 같은지(Giriş,"LIST") ? 1 : 0); 수행작업 = 2;
        cavab("150 Opening directory listing\r\n");
    }
    else if (같은지(Giriş, "SIZE")) {
        if (!Cığır(부가인수)) { cavab("550 Invalid filename\r\n"); return; }
        int fayl_tutacaq = pk_open(fayl_daxiletmə_ad, yalnız_oxunan_VALUE, 0); if (fayl_tutacaq < 0) { cavab("550 File unavailable\r\n"); return; }
        int Böyüklük = pk_size(fayl_tutacaq); pk_close(fayl_tutacaq); char video_münasibət[32] = "213 "; unsigned element_COUNT = 4;
        수치(Böyüklük, video_münasibət, &element_COUNT); video_münasibət[element_COUNT++] = '\r'; video_münasibət[element_COUNT++] = '\n'; video_münasibət[element_COUNT] = 0; cavab(video_münasibət);
    } else if (같은지(Giriş, "STOR") || 같은지(Giriş, "RETR")) {
        if (수행작업) { cavab("450 Transfer in progress\r\n"); return; }
        if (əl_ilə_qoşulma < 0 && verilənlər < 0) { cavab("425 Use PASV or EPSV\r\n"); return; }
        if (!Cığır(부가인수)) { cavab("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(Giriş, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(ötürmə_ad, fayl_daxiletmə_ad, strlen(fayl_daxiletmə_ad) + 1);
        if (수행작업 == 2) {
            int fayl_tutacaq = pk_open(fayl_daxiletmə_ad, yalnız_oxunan_VALUE, 0);
            if (fayl_tutacaq < 0) { 수행작업 = 0; cavab("550 File unavailable\r\n"); return; }
            int element_COUNT = pk_read(fayl_tutacaq, ötürmə_vəziyyət, sizeof(ötürmə_vəziyyət)); pk_close(fayl_tutacaq);
            if (element_COUNT < 0) { 수행작업 = 0; cavab("451 Read failed\r\n"); return; } 사용량 = element_COUNT;
        }
        cavab("150 Opening binary data connection\r\n");
    } else cavab("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int Daxil_olan_qoşulma = 망연결받기(수신창구);
    if (Daxil_olan_qoşulma >= 0) {
        if (nəzarət >= 0) { 통신쓰기(Daxil_olan_qoşulma, "421 One session at a time\r\n", 27); bağlamaq_Şəbəkə(Daxil_olan_qoşulma); }
        else { nəzarət = Daxil_olan_qoşulma; Fəaliyyət = 보드밀리초(); cavab("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (nəzarət < 0) return;
    if ((uint32_t)(보드밀리초() - Fəaliyyət) > 60000) { bağlantını_kəsmək(); return; }
    if (!çıxış_proqram) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char simvol_kodu; int 반환값 = 통신읽기(nəzarət, &simvol_kodu, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { bağlantını_kəsmək(); return; } Fəaliyyət = 보드밀리초();
        if (simvol_kodu == '\n') { if (줄오류) cavab("500 Command too long or invalid\r\n"); else Əmr(); xətt_ölçünü_dəyişmək = 줄오류 = 0; if (çıxış_proqram) break; }
        else if (simvol_kodu != '\r') { if (!simvol_kodu || xətt_ölçünü_dəyişmək >= sizeof(Giriş) - 1) 줄오류 = 1; else Giriş[xətt_ölçünü_dəyişmək++] = simvol_kodu; }
    }
    if (əl_ilə_qoşulma >= 0 && verilənlər < 0) {
        int 반환값 = 망연결받기(əl_ilə_qoşulma);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(nəzarət)) bağlamaq_Şəbəkə(반환값);
            else { verilənlər = 반환값; bağlamaq_Şəbəkə(əl_ilə_qoşulma); əl_ilə_qoşulma = -1; Fəaliyyət = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && verilənlər >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char verilənlər_blokla[512]; int element_COUNT = 통신읽기(verilənlər, verilənlər_blokla, sizeof(verilənlər_blokla));
        if (element_COUNT == -11) break;
        if (element_COUNT < 0) { Dayandır_ötürmə(); cavab("426 Data connection failed\r\n"); break; }
        Fəaliyyət = 보드밀리초();
        if (element_COUNT == 0) {
            int ölçü = -1;
            if (!실패여부) {
                int fayl_tutacaq = pk_open(ötürmə_ad, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (fayl_tutacaq >= 0) { ölçü = pk_write(fayl_tutacaq, ötürmə_vəziyyət, 사용량); pk_close(fayl_tutacaq); }
            }
            int 성공여부 = !실패여부 && ölçü == (int)사용량; Dayandır_ötürmə(); cavab(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)element_COUNT > sizeof(ötürmə_vəziyyət) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(ötürmə_vəziyyət + 사용량, verilənlər_blokla, element_COUNT); 사용량 += element_COUNT; }
    }
    if (수행작업 == 2 && verilənlər >= 0) {
        int element_COUNT = 통신쓰기(verilənlər, ötürmə_vəziyyət + 보낸수, 사용량 - 보낸수);
        if (element_COUNT >= 0) { 보낸수 += element_COUNT; Fəaliyyət = 보드밀리초(); if (보낸수 == 사용량) { Dayandır_ötürmə(); cavab("226 Transfer complete\r\n"); } }
        else if (element_COUNT != -11) { Dayandır_ötürmə(); cavab("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < cavab_ölçünü_dəyişmək) {
        int element_COUNT = 통신쓰기(nəzarət, 응답모음 + 응답전송량, cavab_ölçünü_dəyişmək - 응답전송량);
        if (element_COUNT > 0) 응답전송량 += element_COUNT; else if (element_COUNT != -11) { bağlantını_kəsmək(); return; }
    }
    if (응답전송량 == cavab_ölçünü_dəyişmək) { cavab_ölçünü_dəyişmək = 응답전송량 = 0; if (çıxış_proqram) bağlantını_kəsmək(); }
}
