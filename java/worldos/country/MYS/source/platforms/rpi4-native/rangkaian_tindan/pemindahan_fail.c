#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "rangkaian_tindan.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int 수신창구 = -1, kawalan = -1, manual_hubungan = -1, data = -1;
static unsigned 로그인됨, pengguna_OK, baris_saiz, 줄오류, keluar_aplikasi, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned balas_saiz, 응답전송량, Seterusnya_nombor_port;
static uint32_t Aktiviti;
static char baris[256], 응답모음[2048], fail_pemasukan_nama[64], pindah_nama[64];
static unsigned char pindah_status[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void balas(const char *rentetan_data) {
    size_t item_COUNT = strlen(rentetan_data);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, balas_saiz - 응답전송량); balas_saiz -= 응답전송량; 응답전송량 = 0; }
    if (item_COUNT > sizeof(응답모음) - balas_saiz) { keluar_aplikasi = 1; return; }
    memcpy(응답모음 + balas_saiz, rentetan_data, item_COUNT); balas_saiz += item_COUNT;
}
static void 수치(unsigned VALUE, char *ukuran_data, unsigned *item_COUNT) {
    char digit_COUNT[10]; unsigned pemasukan_COUNT = 0;
    do { digit_COUNT[pemasukan_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (pemasukan_COUNT) ukuran_data[(*item_COUNT)++] = digit_COUNT[--pemasukan_COUNT];
}
static void Henti_pindah(void) {
    if (data >= 0) Tutup_rangkaian(data); if (manual_hubungan >= 0) Tutup_rangkaian(manual_hubungan);
    data = manual_hubungan = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void putuskan_sambungan(void) {
    Henti_pindah(); if (kawalan >= 0) Tutup_rangkaian(kawalan); kawalan = -1;
    로그인됨 = pengguna_OK = baris_saiz = 줄오류 = balas_saiz = 응답전송량 = keluar_aplikasi = 0;
}
int pemindahan_fail_kawalan(int Aksi) {
    if (Aksi == 2) return 수신창구 >= 0;
    if (Aksi == 0) { putuskan_sambungan(); if (수신창구 >= 0) Tutup_rangkaian(수신창구); 수신창구 = -1; return 0; }
    if (Aksi != 1) return -22; if (수신창구 >= 0) return 0;
    수신창구 = 통신끝점만들기(1); if (수신창구 < 0) return 수신창구;
    int 반환값 = 망주소묶기(수신창구, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(수신창구);
    if (반환값 < 0) { Tutup_rangkaian(수신창구); 수신창구 = -1; } return 반환값;
}
static int LALUAN(const char *Nama) {
    unsigned item_COUNT = 0; if (*Nama == '/') Nama++;
    if (!*Nama || 같은지(Nama, ".") || 같은지(Nama, "..")) return 0;
    fail_pemasukan_nama[item_COUNT++] = '/';
    while (*Nama) {
        unsigned char titik_kod = *Nama++;
        if (item_COUNT >= 63 || titik_kod < 32 || titik_kod == 127 || titik_kod == '/' || titik_kod == '\\') return 0;
        fail_pemasukan_nama[item_COUNT++] = titik_kod;
    }
    fail_pemasukan_nama[item_COUNT] = 0; return 1;
}
static void e_mel_Senarai(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int item_COUNT = 자바파일항목길이(순번); if (item_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned pemasukan_COUNT = strlen(앞부분); memcpy(pindah_status + 사용량, 앞부분, pemasukan_COUNT); 사용량 += pemasukan_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)pindah_status, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        pemasukan_COUNT = strlen(뒷부분); memcpy(pindah_status + 사용량, 뒷부분, pemasukan_COUNT); 사용량 += pemasukan_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < item_COUNT; 안쪽순번++) pindah_status[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        pindah_status[사용량++] = '\r'; pindah_status[사용량++] = '\n';
    }
}
static void Sediakan_manual_hubungan(int 확장여부) {
    if (수행작업) { balas("450 Transfer in progress\r\n"); return; }
    Henti_pindah(); manual_hubungan = 통신끝점만들기(1);
    if (manual_hubungan >= 0) 통신주소재사용(manual_hubungan);
    unsigned nombor_port = 50000 + Seterusnya_nombor_port++ % 8;
    if (manual_hubungan < 0 || 망주소묶기(manual_hubungan, 망상태읽기(0,0), nombor_port) || 연결기다리기(manual_hubungan)) {
        Henti_pindah(); balas("425 Cannot open passive listener\r\n"); return;
    }
    char respons[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned item_COUNT = strlen(앞부분); memcpy(respons, 앞부분, item_COUNT);
    if (확장여부) { 수치(nombor_port, respons, &item_COUNT); respons[item_COUNT++] = '|'; }
    else {
        uint32_t e_mel=망상태읽기(0,0);
        for (int jawatan_INDEX=24;jawatan_INDEX>=0;jawatan_INDEX-=8) { 수치((e_mel>>jawatan_INDEX)&255,respons,&item_COUNT);respons[item_COUNT++]=','; }
        수치(nombor_port / 256, respons, &item_COUNT); respons[item_COUNT++] = ','; 수치(nombor_port % 256, respons, &item_COUNT);
    }
    respons[item_COUNT++] = ')'; respons[item_COUNT++] = '\r'; respons[item_COUNT++] = '\n'; respons[item_COUNT] = 0; balas(respons);
}
static void Perintah(void) {
    baris[baris_saiz] = 0;
    char *부가인수 = baris; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(baris, "QUIT")) { Henti_pindah(); balas("221 Goodbye\r\n"); keluar_aplikasi = 1; return; }
    if (같은지(baris, "NOOP")) { balas("200 OK\r\n"); return; }
    if (같은지(baris, "SYST")) { balas("215 UNIX Type: L8\r\n"); return; }
    if (같은지(baris, "FEAT")) { balas("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(baris, "USER")) { 로그인됨 = 0; pengguna_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); balas(pengguna_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(baris, "PASS")) { 로그인됨 = pengguna_OK; balas(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { balas("530 Login first\r\n"); return; }
    if (같은지(baris, "PWD")) balas("257 \"/\"\r\n");
    else if (같은지(baris, "CWD")) balas(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(baris, "TYPE")) balas(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(baris, "OPTS")) balas(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(baris, "PASV")) Sediakan_manual_hubungan(0);
    else if (같은지(baris, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) balas("522 IPv4 only\r\n"); else Sediakan_manual_hubungan(1); }
    else if (같은지(baris, "ABOR")) { Henti_pindah(); balas("226 Transfer aborted\r\n"); }
    else if (같은지(baris, "DELE")) { balas(LALUAN(부가인수) && pk_unlink(fail_pemasukan_nama) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(baris, "LIST") || 같은지(baris, "NLST") || 같은지(baris, "MLSD")) {
        if (수행작업) { balas("450 Transfer in progress\r\n"); return; }
        if (manual_hubungan < 0 && data < 0) { balas("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { balas("550 Root listing only\r\n"); return; }
        e_mel_Senarai(같은지(baris,"MLSD") ? 2 : 같은지(baris,"LIST") ? 1 : 0); 수행작업 = 2;
        balas("150 Opening directory listing\r\n");
    }
    else if (같은지(baris, "SIZE")) {
        if (!LALUAN(부가인수)) { balas("550 Invalid filename\r\n"); return; }
        int fail_pemegang = pk_open(fail_pemasukan_nama, baca_sahaja_VALUE, 0); if (fail_pemegang < 0) { balas("550 File unavailable\r\n"); return; }
        int Saiz = pk_size(fail_pemegang); pk_close(fail_pemegang); char respons[32] = "213 "; unsigned item_COUNT = 4;
        수치(Saiz, respons, &item_COUNT); respons[item_COUNT++] = '\r'; respons[item_COUNT++] = '\n'; respons[item_COUNT] = 0; balas(respons);
    } else if (같은지(baris, "STOR") || 같은지(baris, "RETR")) {
        if (수행작업) { balas("450 Transfer in progress\r\n"); return; }
        if (manual_hubungan < 0 && data < 0) { balas("425 Use PASV or EPSV\r\n"); return; }
        if (!LALUAN(부가인수)) { balas("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(baris, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(pindah_nama, fail_pemasukan_nama, strlen(fail_pemasukan_nama) + 1);
        if (수행작업 == 2) {
            int fail_pemegang = pk_open(fail_pemasukan_nama, baca_sahaja_VALUE, 0);
            if (fail_pemegang < 0) { 수행작업 = 0; balas("550 File unavailable\r\n"); return; }
            int item_COUNT = pk_read(fail_pemegang, pindah_status, sizeof(pindah_status)); pk_close(fail_pemegang);
            if (item_COUNT < 0) { 수행작업 = 0; balas("451 Read failed\r\n"); return; } 사용량 = item_COUNT;
        }
        balas("150 Opening binary data connection\r\n");
    } else balas("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (수신창구 < 0) return;
    int Masuk_hubungan = 망연결받기(수신창구);
    if (Masuk_hubungan >= 0) {
        if (kawalan >= 0) { 통신쓰기(Masuk_hubungan, "421 One session at a time\r\n", 27); Tutup_rangkaian(Masuk_hubungan); }
        else { kawalan = Masuk_hubungan; Aktiviti = 보드밀리초(); balas("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (kawalan < 0) return;
    if ((uint32_t)(보드밀리초() - Aktiviti) > 60000) { putuskan_sambungan(); return; }
    if (!keluar_aplikasi) for (unsigned belanjawan_diperuntukkan = 0; belanjawan_diperuntukkan < 256; belanjawan_diperuntukkan++) {
        unsigned char titik_kod; int 반환값 = 통신읽기(kawalan, &titik_kod, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { putuskan_sambungan(); return; } Aktiviti = 보드밀리초();
        if (titik_kod == '\n') { if (줄오류) balas("500 Command too long or invalid\r\n"); else Perintah(); baris_saiz = 줄오류 = 0; if (keluar_aplikasi) break; }
        else if (titik_kod != '\r') { if (!titik_kod || baris_saiz >= sizeof(baris) - 1) 줄오류 = 1; else baris[baris_saiz++] = titik_kod; }
    }
    if (manual_hubungan >= 0 && data < 0) {
        int 반환값 = 망연결받기(manual_hubungan);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(kawalan)) Tutup_rangkaian(반환값);
            else { data = 반환값; Tutup_rangkaian(manual_hubungan); manual_hubungan = -1; Aktiviti = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && data >= 0) for (unsigned belanjawan_diperuntukkan = 0; belanjawan_diperuntukkan < 8; belanjawan_diperuntukkan++) {
        unsigned char blok_data[512]; int item_COUNT = 통신읽기(data, blok_data, sizeof(blok_data));
        if (item_COUNT == -11) break;
        if (item_COUNT < 0) { Henti_pindah(); balas("426 Data connection failed\r\n"); break; }
        Aktiviti = 보드밀리초();
        if (item_COUNT == 0) {
            int ukuran = -1;
            if (!실패여부) {
                int fail_pemegang = pk_open(pindah_nama, tulis_sahaja_VALUE | 없으면만들기 | potong_TOC, 0600);
                if (fail_pemegang >= 0) { ukuran = pk_write(fail_pemegang, pindah_status, 사용량); pk_close(fail_pemegang); }
            }
            int 성공여부 = !실패여부 && ukuran == (int)사용량; Henti_pindah(); balas(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)item_COUNT > sizeof(pindah_status) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(pindah_status + 사용량, blok_data, item_COUNT); 사용량 += item_COUNT; }
    }
    if (수행작업 == 2 && data >= 0) {
        int item_COUNT = 통신쓰기(data, pindah_status + 보낸수, 사용량 - 보낸수);
        if (item_COUNT >= 0) { 보낸수 += item_COUNT; Aktiviti = 보드밀리초(); if (보낸수 == 사용량) { Henti_pindah(); balas("226 Transfer complete\r\n"); } }
        else if (item_COUNT != -11) { Henti_pindah(); balas("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < balas_saiz) {
        int item_COUNT = 통신쓰기(kawalan, 응답모음 + 응답전송량, balas_saiz - 응답전송량);
        if (item_COUNT > 0) 응답전송량 += item_COUNT; else if (item_COUNT != -11) { putuskan_sambungan(); return; }
    }
    if (응답전송량 == balas_saiz) { balas_saiz = 응답전송량 = 0; if (keluar_aplikasi) putuskan_sambungan(); }
}
