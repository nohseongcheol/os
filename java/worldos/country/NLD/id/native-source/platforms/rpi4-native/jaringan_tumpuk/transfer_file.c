#include "../명명/기계연결이름.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "jaringan_tumpuk.h"
#include "string.h"
#include "파일규약.h"
extern uintptr_t 보드밀리초(void);
extern int32_t 자바파일항목길이(int32_t), 자바파일항목바이트(int32_t,int32_t), 자바파일항목크기(int32_t);
extern int32_t 자바파일항목개수(void);
static int terima_port = -1, kontrol = -1, manual_koneksi = -1, data = -1;
static unsigned 로그인됨, pengguna_OK, baris_ukuran, 줄오류, berhenti_apl, 수행작업, 사용량, 보낸수, 실패여부;
static unsigned balas_ukuran, 응답전송량, Berikutnya_nomor_port;
static uint32_t Aktivitas;
static char baris_masukan[256], 응답모음[2048], file_entri_nama[64], Transfer_nama[64];
static unsigned char Transfer_Status[16384];
static int 같은지(const char *첫째값, const char *SECOND_VALUE) { while (*첫째값 && *첫째값 == *SECOND_VALUE) { 첫째값++; SECOND_VALUE++; } return *첫째값 == *SECOND_VALUE; }
static void balas(const char *string_data) {
    size_t item_COUNT = strlen(string_data);
    if (응답전송량) { memmove(응답모음, 응답모음 + 응답전송량, balas_ukuran - 응답전송량); balas_ukuran -= 응답전송량; 응답전송량 = 0; }
    if (item_COUNT > sizeof(응답모음) - balas_ukuran) { berhenti_apl = 1; return; }
    memcpy(응답모음 + balas_ukuran, string_data, item_COUNT); balas_ukuran += item_COUNT;
}
static void 수치(unsigned VALUE, char *KR_data, unsigned *item_COUNT) {
    char angka_COUNT[10]; unsigned entri_COUNT = 0;
    do { angka_COUNT[entri_COUNT++] = '0' + VALUE % 10; VALUE /= 10; } while (VALUE);
    while (entri_COUNT) KR_data[(*item_COUNT)++] = angka_COUNT[--entri_COUNT];
}
static void Berhenti_Transfer(void) {
    if (data >= 0) Tutup_jaringan(data); if (manual_koneksi >= 0) Tutup_jaringan(manual_koneksi);
    data = manual_koneksi = -1; 수행작업 = 사용량 = 보낸수 = 실패여부 = 0;
}
static void putuskan_sambungan(void) {
    Berhenti_Transfer(); if (kontrol >= 0) Tutup_jaringan(kontrol); kontrol = -1;
    로그인됨 = pengguna_OK = baris_ukuran = 줄오류 = balas_ukuran = 응답전송량 = berhenti_apl = 0;
}
int transfer_file_kontrol(int Aksi) {
    if (Aksi == 2) return terima_port >= 0;
    if (Aksi == 0) { putuskan_sambungan(); if (terima_port >= 0) Tutup_jaringan(terima_port); terima_port = -1; return 0; }
    if (Aksi != 1) return -22; if (terima_port >= 0) return 0;
    terima_port = 통신끝점만들기(1); if (terima_port < 0) return terima_port;
    int 반환값 = 망주소묶기(terima_port, 망상태읽기(0,0), 21); if (!반환값) 반환값 = 연결기다리기(terima_port);
    if (반환값 < 0) { Tutup_jaringan(terima_port); terima_port = -1; } return 반환값;
}
static int jalur(const char *Nama_2) {
    unsigned item_COUNT = 0; if (*Nama_2 == '/') Nama_2++;
    if (!*Nama_2 || 같은지(Nama_2, ".") || 같은지(Nama_2, "..")) return 0;
    file_entri_nama[item_COUNT++] = '/';
    while (*Nama_2) {
        unsigned char kode_karakter = *Nama_2++;
        if (item_COUNT >= 63 || kode_karakter < 32 || kode_karakter == 127 || kode_karakter == '/' || kode_karakter == '\\') return 0;
        file_entri_nama[item_COUNT++] = kode_karakter;
    }
    file_entri_nama[item_COUNT] = 0; return 1;
}
static void kirim_Daftar(int 상세정보) {
    사용량 = 보낸수 = 0;
    for (int 순번 = 0; 순번 < 자바파일항목개수(); 순번++) {
        int item_COUNT = 자바파일항목길이(순번); if (item_COUNT <= 0) continue;
        const char *앞부분 = 상세정보 == 2 ? "type=file;size=" : 상세정보 == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned entri_COUNT = strlen(앞부분); memcpy(Transfer_Status + 사용량, 앞부분, entri_COUNT); 사용량 += entri_COUNT;
        if (상세정보) 수치(자바파일항목크기(순번), (char *)Transfer_Status, &사용량);
        const char *뒷부분 = 상세정보 == 2 ? "; " : 상세정보 == 1 ? " Jan 01 00:00 " : "";
        entri_COUNT = strlen(뒷부분); memcpy(Transfer_Status + 사용량, 뒷부분, entri_COUNT); 사용량 += entri_COUNT;
        for (int 안쪽순번 = 0; 안쪽순번 < item_COUNT; 안쪽순번++) Transfer_Status[사용량++] = 자바파일항목바이트(순번,안쪽순번);
        Transfer_Status[사용량++] = '\r'; Transfer_Status[사용량++] = '\n';
    }
}
static void Siapkan_manual_koneksi(int 확장여부) {
    if (수행작업) { balas("450 Transfer in progress\r\n"); return; }
    Berhenti_Transfer(); manual_koneksi = 통신끝점만들기(1);
    if (manual_koneksi >= 0) 통신주소재사용(manual_koneksi);
    unsigned nomor_port = 50000 + Berikutnya_nomor_port++ % 8;
    if (manual_koneksi < 0 || 망주소묶기(manual_koneksi, 망상태읽기(0,0), nomor_port) || 연결기다리기(manual_koneksi)) {
        Berhenti_Transfer(); balas("425 Cannot open passive listener\r\n"); return;
    }
    char respons[96]; const char *앞부분 = 확장여부 ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned item_COUNT = strlen(앞부분); memcpy(respons, 앞부분, item_COUNT);
    if (확장여부) { 수치(nomor_port, respons, &item_COUNT); respons[item_COUNT++] = '|'; }
    else {
        uint32_t surel=망상태읽기(0,0);
        for (int posisi_INDEX=24;posisi_INDEX>=0;posisi_INDEX-=8) { 수치((surel>>posisi_INDEX)&255,respons,&item_COUNT);respons[item_COUNT++]=','; }
        수치(nomor_port / 256, respons, &item_COUNT); respons[item_COUNT++] = ','; 수치(nomor_port % 256, respons, &item_COUNT);
    }
    respons[item_COUNT++] = ')'; respons[item_COUNT++] = '\r'; respons[item_COUNT++] = '\n'; respons[item_COUNT] = 0; balas(respons);
}
static void perintah(void) {
    baris_masukan[baris_ukuran] = 0;
    char *부가인수 = baris_masukan; while (*부가인수 && *부가인수 != ' ') { if (*부가인수 >= 'a' && *부가인수 <= 'z') *부가인수 -= 32; 부가인수++; }
    if (*부가인수) *부가인수++ = 0; while (*부가인수 == ' ') 부가인수++;
    if (같은지(baris_masukan, "QUIT")) { Berhenti_Transfer(); balas("221 Goodbye\r\n"); berhenti_apl = 1; return; }
    if (같은지(baris_masukan, "NOOP")) { balas("200 OK\r\n"); return; }
    if (같은지(baris_masukan, "SYST")) { balas("215 UNIX Type: L8\r\n"); return; }
    if (같은지(baris_masukan, "FEAT")) { balas("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (같은지(baris_masukan, "USER")) { 로그인됨 = 0; pengguna_OK = 같은지(부가인수, "anonymous") || 같은지(부가인수, "jkoros"); balas(pengguna_OK ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (같은지(baris_masukan, "PASS")) { 로그인됨 = pengguna_OK; balas(로그인됨 ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!로그인됨) { balas("530 Login first\r\n"); return; }
    if (같은지(baris_masukan, "PWD")) balas("257 \"/\"\r\n");
    else if (같은지(baris_masukan, "CWD")) balas(같은지(부가인수, "/") || 같은지(부가인수, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (같은지(baris_masukan, "TYPE")) balas(같은지(부가인수, "I") || 같은지(부가인수, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (같은지(baris_masukan, "OPTS")) balas(같은지(부가인수, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (같은지(baris_masukan, "PASV")) Siapkan_manual_koneksi(0);
    else if (같은지(baris_masukan, "EPSV")) { if (*부가인수 && !같은지(부가인수, "1")) balas("522 IPv4 only\r\n"); else Siapkan_manual_koneksi(1); }
    else if (같은지(baris_masukan, "ABOR")) { Berhenti_Transfer(); balas("226 Transfer aborted\r\n"); }
    else if (같은지(baris_masukan, "DELE")) { balas(jalur(부가인수) && pk_unlink(file_entri_nama) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (같은지(baris_masukan, "LIST") || 같은지(baris_masukan, "NLST") || 같은지(baris_masukan, "MLSD")) {
        if (수행작업) { balas("450 Transfer in progress\r\n"); return; }
        if (manual_koneksi < 0 && data < 0) { balas("425 Use PASV or EPSV\r\n"); return; }
        if (*부가인수 && !같은지(부가인수,"/") && !같은지(부가인수,".") && !같은지(부가인수,"-a") && !같은지(부가인수,"-l") && !같은지(부가인수,"-la")) { balas("550 Root listing only\r\n"); return; }
        kirim_Daftar(같은지(baris_masukan,"MLSD") ? 2 : 같은지(baris_masukan,"LIST") ? 1 : 0); 수행작업 = 2;
        balas("150 Opening directory listing\r\n");
    }
    else if (같은지(baris_masukan, "SIZE")) {
        if (!jalur(부가인수)) { balas("550 Invalid filename\r\n"); return; }
        int file_handel = pk_open(file_entri_nama, baca_saja_VALUE, 0); if (file_handel < 0) { balas("550 File unavailable\r\n"); return; }
        int Ukuran = pk_size(file_handel); pk_close(file_handel); char respons[32] = "213 "; unsigned item_COUNT = 4;
        수치(Ukuran, respons, &item_COUNT); respons[item_COUNT++] = '\r'; respons[item_COUNT++] = '\n'; respons[item_COUNT] = 0; balas(respons);
    } else if (같은지(baris_masukan, "STOR") || 같은지(baris_masukan, "RETR")) {
        if (수행작업) { balas("450 Transfer in progress\r\n"); return; }
        if (manual_koneksi < 0 && data < 0) { balas("425 Use PASV or EPSV\r\n"); return; }
        if (!jalur(부가인수)) { balas("550 Invalid filename\r\n"); return; }
        수행작업 = 같은지(baris_masukan, "STOR") ? 1 : 2; 사용량 = 보낸수 = 실패여부 = 0;
        memcpy(Transfer_nama, file_entri_nama, strlen(file_entri_nama) + 1);
        if (수행작업 == 2) {
            int file_handel = pk_open(file_entri_nama, baca_saja_VALUE, 0);
            if (file_handel < 0) { 수행작업 = 0; balas("550 File unavailable\r\n"); return; }
            int item_COUNT = pk_read(file_handel, Transfer_Status, sizeof(Transfer_Status)); pk_close(file_handel);
            if (item_COUNT < 0) { 수행작업 = 0; balas("451 Read failed\r\n"); return; } 사용량 = item_COUNT;
        }
        balas("150 Opening binary data connection\r\n");
    } else balas("502 Command not implemented\r\n");
}
void 파일전송살피기(void) {
    if (terima_port < 0) return;
    int Masuk_koneksi = 망연결받기(terima_port);
    if (Masuk_koneksi >= 0) {
        if (kontrol >= 0) { 통신쓰기(Masuk_koneksi, "421 One session at a time\r\n", 27); Tutup_jaringan(Masuk_koneksi); }
        else { kontrol = Masuk_koneksi; Aktivitas = 보드밀리초(); balas("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (kontrol < 0) return;
    if ((uint32_t)(보드밀리초() - Aktivitas) > 60000) { putuskan_sambungan(); return; }
    if (!berhenti_apl) for (unsigned anggaran = 0; anggaran < 256; anggaran++) {
        unsigned char kode_karakter; int 반환값 = 통신읽기(kontrol, &kode_karakter, 1);
        if (반환값 == -11) break; if (반환값 <= 0) { putuskan_sambungan(); return; } Aktivitas = 보드밀리초();
        if (kode_karakter == '\n') { if (줄오류) balas("500 Command too long or invalid\r\n"); else perintah(); baris_ukuran = 줄오류 = 0; if (berhenti_apl) break; }
        else if (kode_karakter != '\r') { if (!kode_karakter || baris_ukuran >= sizeof(baris_masukan) - 1) 줄오류 = 1; else baris_masukan[baris_ukuran++] = kode_karakter; }
    }
    if (manual_koneksi >= 0 && data < 0) {
        int 반환값 = 망연결받기(manual_koneksi);
        if (반환값 >= 0) {
            if (상대통신주소(반환값) != 상대통신주소(kontrol)) Tutup_jaringan(반환값);
            else { data = 반환값; Tutup_jaringan(manual_koneksi); manual_koneksi = -1; Aktivitas = 보드밀리초(); }
        }
    }
    if (수행작업 == 1 && data >= 0) for (unsigned anggaran = 0; anggaran < 8; anggaran++) {
        unsigned char blok_data[512]; int item_COUNT = 통신읽기(data, blok_data, sizeof(blok_data));
        if (item_COUNT == -11) break;
        if (item_COUNT < 0) { Berhenti_Transfer(); balas("426 Data connection failed\r\n"); break; }
        Aktivitas = 보드밀리초();
        if (item_COUNT == 0) {
            int hasil = -1;
            if (!실패여부) {
                int file_handel = pk_open(Transfer_nama, 쓰기전용 | 없으면만들기 | 내용비우기, 0600);
                if (file_handel >= 0) { hasil = pk_write(file_handel, Transfer_Status, 사용량); pk_close(file_handel); }
            }
            int 성공여부 = !실패여부 && hasil == (int)사용량; Berhenti_Transfer(); balas(성공여부 ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)item_COUNT > sizeof(Transfer_Status) - 사용량) 실패여부 = 1;
        if (!실패여부) { memcpy(Transfer_Status + 사용량, blok_data, item_COUNT); 사용량 += item_COUNT; }
    }
    if (수행작업 == 2 && data >= 0) {
        int item_COUNT = 통신쓰기(data, Transfer_Status + 보낸수, 사용량 - 보낸수);
        if (item_COUNT >= 0) { 보낸수 += item_COUNT; Aktivitas = 보드밀리초(); if (보낸수 == 사용량) { Berhenti_Transfer(); balas("226 Transfer complete\r\n"); } }
        else if (item_COUNT != -11) { Berhenti_Transfer(); balas("426 Data connection failed\r\n"); }
    }
    if (응답전송량 < balas_ukuran) {
        int item_COUNT = 통신쓰기(kontrol, 응답모음 + 응답전송량, balas_ukuran - 응답전송량);
        if (item_COUNT > 0) 응답전송량 += item_COUNT; else if (item_COUNT != -11) { putuskan_sambungan(); return; }
    }
    if (응답전송량 == balas_ukuran) { balas_ukuran = 응답전송량 = 0; if (berhenti_apl) putuskan_sambungan(); }
}
