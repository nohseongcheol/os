#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "Tarmoq_Stack.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, boshqaruv = -1, qo_llanma_aloqa = -1, ma_lumotlar = -1;
static unsigned 로그인됨, foydalanuvchi_OK, satr_o_lcham, 줄오류, tugatish_ilova, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned javob_berish_o_lcham, 응답전송량, 다음접속번호;
static uint32_t harakat;
static char satr[256], 응답모음[2048], fayl_kiritish_nom[64], uzatish_nom[64];
static unsigned char uzatish_holat[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void javob_berish(const char *satr_ma_lumotlar) {
    size_t element_COUNT = strlen(satr_ma_lumotlar);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, javob_berish_o_lcham - 응답전송량); javob_berish_o_lcham -= 응답전송량; 응답전송량 = 0; }
    if (element_COUNT > sizeof(응답모음) - javob_berish_o_lcham) { tugatish_ilova = 1; return; }
    memcpy(응답모음 + javob_berish_o_lcham, satr_ma_lumotlar, element_COUNT); javob_berish_o_lcham += element_COUNT;
}
static void 수치(unsigned VALUE, char *o_lchov_ma_lumotlar, unsigned *element_COUNT) {
    char raqam_COUNT[10]; unsigned kiritish_COUNT = 0;
    do { raqam_COUNT[kiritish_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (kiritish_COUNT) o_lchov_ma_lumotlar[(*element_COUNT)++] = raqam_COUNT[--kiritish_COUNT];
}
static void To_xtatish_uzatish(void) {
    if (ma_lumotlar >= 0) yopmoq_Tarmoq(ma_lumotlar); if (qo_llanma_aloqa >= 0) yopmoq_Tarmoq(qo_llanma_aloqa);
    ma_lumotlar = qo_llanma_aloqa = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void ulanishni_uzish(void) {
    To_xtatish_uzatish(); if (boshqaruv >= 0) yopmoq_Tarmoq(boshqaruv); boshqaruv = -1;
    로그인됨 = foydalanuvchi_OK = satr_o_lcham = 줄오류 = javob_berish_o_lcham = 응답전송량 = tugatish_ilova = 0;
}
int fayl_uzatish_boshqaruv(int Amal) {
    if (Amal == 2) return 수신창구 >= 0;
    if (Amal == 0) { ulanishni_uzish(); if (수신창구 >= 0) yopmoq_Tarmoq(수신창구); 수신창구 = -1; return 0; }
    if (Amal != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { yopmoq_Tarmoq(수신창구); 수신창구 = -1; } return 반환값;
}
static int yo_l(const char *Nomi) {
    unsigned element_COUNT = 0; if (*Nomi == '/') Nomi++;
    if (!*Nomi || 같은지(Nomi, ".") || 같은지(Nomi, "..")) return 0;
    fayl_kiritish_nom[element_COUNT++] = '/';
    while (*Nomi) {
        unsigned char belgi_kodi = *Nomi++;
        if (element_COUNT >= 63 || belgi_kodi < 32 || belgi_kodi == 127 || belgi_kodi == '/' || belgi_kodi == '\\') return 0;
        fayl_kiritish_nom[element_COUNT++] = belgi_kodi;
    }
    fayl_kiritish_nom[element_COUNT] = 0; return 1;
}
static void yuborish_Ro_yxat(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int element_COUNT = 자바파일항목길이(순번); if (element_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned kiritish_COUNT = strlen(앞부분); memcpy(uzatish_holat + 사용량, 앞부분, kiritish_COUNT); 사용량 += kiritish_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)uzatish_holat, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        kiritish_COUNT = strlen(뒷부분); memcpy(uzatish_holat + 사용량, 뒷부분, kiritish_COUNT); 사용량 += kiritish_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < element_COUNT; 안쪽순번++) uzatish_holat[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        uzatish_holat[사용량++] = '\r'; uzatish_holat[사용량++] = '\n';
    }
}
static void Tayyorlamoq_qo_llanma_aloqa(int 확장여부) {
    if (수행작업) { javob_berish("450 Transfer in progress\r\n"); return; }
    To_xtatish_uzatish(); qo_llanma_aloqa = 통신끝점만들기(1);
    if (qo_llanma_aloqa >= 0) 통신주소재사용(qo_llanma_aloqa);
    unsigned 접속번호 = 50000 + 다음접속번호++ % 8;
    if (qo_llanma_aloqa < 0 || 망주소묶기(qo_llanma_aloqa, 망상태읽기(0,0), 접속번호) || 연결기다리기(qo_llanma_aloqa)) {
        To_xtatish_uzatish(); javob_berish("425 Cannot open passive listener\r\n"); return;
    }
    char 응답자료[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned element_COUNT = strlen(앞부분); memcpy(응답자료, 앞부분, element_COUNT);
    if (확장여부) { 수치(접속번호, 응답자료, &element_COUNT); 응답자료[element_COUNT++] = '|'; }
    else {
        uint32_t manzil=망상태읽기(0,0);
        for (int holat_INDEX=24;holat_INDEX>=0;holat_INDEX-=8) { 수치((manzil>>holat_INDEX)&255,응답자료,&element_COUNT);응답자료[element_COUNT++]=','; }
        수치(접속번호 / 256, 응답자료, &element_COUNT); 응답자료[element_COUNT++] = ','; 수치(접속번호 % 256, 응답자료, &element_COUNT);
    }
    응답자료[element_COUNT++] = ')'; 응답자료[element_COUNT++] = '\r'; 응답자료[element_COUNT++] = '\n'; 응답자료[element_COUNT] = 0; javob_berish(응답자료);
}
static void Buyruq(void) {
    satr[satr_o_lcham] = 0;
    char *부가인수 = satr; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(satr, "QUIT")) { To_xtatish_uzatish(); javob_berish("221 Goodbye\r\n"); tugatish_ilova = 1; return; }
    if (같은지(satr, "NOOP")) { javob_berish("200 OK\r\n"); return; }
    if (같은지(satr, "SYST")) { javob_berish("215 UNIX Type: L8\r\n"); return; }
    if (같은지(satr, "FEAT")) { javob_berish("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(satr, "USER")) { 로그인됨 = 0; foydalanuvchi_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); javob_berish(foydalanuvchi_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(satr, "PASS")) { 로그인됨 = foydalanuvchi_OK; javob_berish(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { javob_berish("530 Login first\r\n"); return; }
    if (같은지(satr, "PWD")) javob_berish("257 \"/\"\r\n");
    else if (같은지(satr, "CWD")) javob_berish(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(satr, "TYPE")) javob_berish(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(satr, "OPTS")) javob_berish(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(satr, "PASV")) Tayyorlamoq_qo_llanma_aloqa(0);
    else if (같은지(satr, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) javob_berish("522 IPv4 only\r\n"); else Tayyorlamoq_qo_llanma_aloqa(1); }
    else if (같은지(satr, "ABOR")) { To_xtatish_uzatish(); javob_berish("226 Transfer aborted\r\n"); }
    else if (같은지(satr, "DELE")) { javob_berish(yo_l(부가인수) && pk_unlink(fayl_kiritish_nom) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(satr, "LIST") || 같은지(satr, "NLST") || 같은지(satr, "MLSD")) {
        if (수행작업) { javob_berish("450 Transfer in progress\r\n"); return; }
        if (qo_llanma_aloqa < 0 && ma_lumotlar < 0) { javob_berish("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { javob_berish("550 Root listing only\r\n"); return; }
        yuborish_Ro_yxat(같은지(satr,"MLSD") ? 2 : 같은지(satr,"LIST") ? 1 : 0); 수행작업 = 2;
        javob_berish("150 Opening directory listing\r\n");
    }
    else if (같은지(satr, "SIZE")) {
        if (!yo_l(부가인수)) { javob_berish("550 Invalid filename\r\n"); return; }
        int fayl_deskriptor = pk_open(fayl_kiritish_nom, faqat_o_qish_uchun_VALUE, 0); if (fayl_deskriptor < 0) { javob_berish("550 File unavailable\r\n"); return; }
        int Hajmi = pk_size(fayl_deskriptor); pk_close(fayl_deskriptor); char 응답자료[32] = "213 "; unsigned element_COUNT = 4;
        수치(Hajmi, 응답자료, &element_COUNT); 응답자료[element_COUNT++] = '\r'; 응답자료[element_COUNT++] = '\n'; 응답자료[element_COUNT] = 0; javob_berish(응답자료);
    } else if (같은지(satr, "STOR") || 같은지(satr, "RETR")) {
        if (수행작업) { javob_berish("450 Transfer in progress\r\n"); return; }
        if (qo_llanma_aloqa < 0 && ma_lumotlar < 0) { javob_berish("425 Use PASV or EPSV\r\n"); return; }
        if (!yo_l(부가인수)) { javob_berish("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(satr, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(uzatish_nom, fayl_kiritish_nom, strlen(fayl_kiritish_nom) + 1);
        if (수행작업 == 2) {
            int fayl_deskriptor = pk_open(fayl_kiritish_nom, faqat_o_qish_uchun_VALUE, 0);
            if (fayl_deskriptor < 0) { 수행작업 = 0; javob_berish("550 File unavailable\r\n"); return; }
            int element_COUNT = pk_read(fayl_deskriptor, uzatish_holat, sizeof(uzatish_holat)); pk_close(fayl_deskriptor);
            if (element_COUNT < 0) { 수행작업 = 0; javob_berish("451 Read failed\r\n"); return; } 사용량 = element_COUNT;
        }
        javob_berish("150 Opening binary data connection\r\n");
    } else javob_berish("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int Kirish_qo_ng_irog_i_aloqa = 망연결받기(수신창구);
    if (Kirish_qo_ng_irog_i_aloqa >= 0) {
        if (boshqaruv >= 0) { 통신쓰기(Kirish_qo_ng_irog_i_aloqa, "421 One session at a time\r\n", 27); yopmoq_Tarmoq(Kirish_qo_ng_irog_i_aloqa); }
        else { boshqaruv = Kirish_qo_ng_irog_i_aloqa; harakat = 보드밀리초(); javob_berish("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (boshqaruv < 0) return;
    if ((uint32_t)(보드밀리초() - harakat) > 60000) { ulanishni_uzish(); return; }
    if (!tugatish_ilova) for (unsigned 처리한도 = 0; 처리한도 < 256; 처리한도++) {
        unsigned char belgi_kodi; int 반환값 = 통신읽기(boshqaruv, &belgi_kodi, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { ulanishni_uzish(); return; } harakat = 보드밀리초();
        if (belgi_kodi == '\n') { if (줄오류) javob_berish("500 Command too long or invalid\r\n"); else Buyruq(); satr_o_lcham = 줄오류 = 0; if (tugatish_ilova) break; }
        else if (belgi_kodi != '\r') { if (!belgi_kodi || satr_o_lcham >= sizeof(satr) - 1) 줄오류 = 1; else satr[satr_o_lcham++] = belgi_kodi; }
    }
    if (qo_llanma_aloqa >= 0 && ma_lumotlar < 0) {
        int 반환값 = 망연결받기(qo_llanma_aloqa);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(boshqaruv)) yopmoq_Tarmoq(반환값);
            else { ma_lumotlar = 반환값; yopmoq_Tarmoq(qo_llanma_aloqa); qo_llanma_aloqa = -1; harakat = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && ma_lumotlar >= 0) for (unsigned 처리한도 = 0; 처리한도 < 8; 처리한도++) {
        unsigned char ma_lumotlar_bloklash[512]; int element_COUNT = 통신읽기(ma_lumotlar, ma_lumotlar_bloklash, sizeof(ma_lumotlar_bloklash));
        if (element_COUNT == -11) break;
        if (element_COUNT < 0) { To_xtatish_uzatish(); javob_berish("426 Data connection failed\r\n"); break; }
        harakat = 보드밀리초();
        if (element_COUNT == 0) {
            int o_lchov = -1;
            if (!실패여부) {
                int fayl_deskriptor = pk_open(uzatish_nom, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (fayl_deskriptor >= 0) { o_lchov = pk_write(fayl_deskriptor, uzatish_holat, 사용량); pk_close(fayl_deskriptor); }
            }
            int 성공여부 = !실패여부 && o_lchov == (int)사용량; To_xtatish_uzatish(); javob_berish(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)element_COUNT > sizeof(uzatish_holat) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(uzatish_holat + 사용량, ma_lumotlar_bloklash, element_COUNT); 사용량 += element_COUNT; }
    }
    if (수행작업 == 2 && ma_lumotlar >= 0) {
        int element_COUNT = 통신쓰기(ma_lumotlar, uzatish_holat + 보낸수, 사용량 - 보낸수);
        if (element_COUNT >= 0) { 보낸수 += element_COUNT; harakat = 보드밀리초(); if (보낸수 == 사용량) { To_xtatish_uzatish(); javob_berish("226 Transfer complete\r\n"); } }
        else if (element_COUNT != -11) { To_xtatish_uzatish(); javob_berish("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < javob_berish_o_lcham) {
        int element_COUNT = 통신쓰기(boshqaruv, 응답모음 + 응답전송량, javob_berish_o_lcham - 응답전송량);
        if (element_COUNT > 0) 응답전송량 += element_COUNT; else if (element_COUNT != -11) { ulanishni_uzish(); return; }
    }
    if (응답전송량 == javob_berish_o_lcham) { javob_berish_o_lcham = 응답전송량 = 0; if (tugatish_ilova) ulanishni_uzish(); }
}
