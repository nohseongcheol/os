// 동일 Indonesia 헤더를 사용하는 별도 EL0 pustaka. kernel_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int kode_galat;
int *pk_errno_location(void) { return &kode_galat; }
static intptr_t 결과검사(intptr_t hasil) { if (hasil < 0) { kode_galat = -hasil; return -1; } return hasil; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
file_OFFSET_TYPE pk_lseek(int fd, file_OFFSET_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, file_OFFSET_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
int pk_fsync(int fd) { return 결과검사(사용자호출(12, fd, 0, 0, 0, 0, 0)); }
int pk_size(int fd) { return 결과검사(사용자호출(9, fd, 0, 0, 0, 0, 0)); }
int pk_socket(int domain, int type, int protocol) { return 결과검사(사용자호출(32, domain, type, protocol, 0, 0, 0)); }
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length) {
    return 결과검사(사용자호출(33, fd, (uintptr_t)address, length, 0, 0, 0));
}
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length) {
    return 결과검사(사용자호출(34, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, length));
}
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length) {
    return 결과검사(사용자호출(35, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, (uintptr_t)length));
}
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length) {
    return 결과검사(사용자호출(36, fd, (uintptr_t)address, (uintptr_t)length, 0, 0, 0));
}
int pk_connect(int fd,const struct pk_sockaddr *address,pk_socklen_t length){return 결과검사(사용자호출(37,fd,(uintptr_t)address,length,0,0,0));}
int pk_listen(int fd,int backlog){return 결과검사(사용자호출(38,fd,backlog,0,0,0,0));}
int pk_accept(int fd,struct pk_sockaddr *address,pk_socklen_t *length){return 결과검사(사용자호출(39,fd,(uintptr_t)address,(uintptr_t)length,0,0,0));}

/* Indonesia 공개 함수의 aktual_data EL0 implementasi. 구조체는 SVC에서 salin_VALUE·검증한다. */
int Buat_peserta(int surel_famili,int komunikasi_MODE,int Transfer_protokol) {
    return 결과검사(사용자호출(32,surel_famili,komunikasi_MODE,Transfer_protokol,0,0,0));
}
int ikat_surel(int peserta,const struct 통신주소 *surel,통신주소길이형 panjang_VALUE) {
    return 결과검사(사용자호출(33,peserta,(uintptr_t)surel,panjang_VALUE,0,0,0));
}
intptr_t 자료전문보내기(int peserta,const void *data,size_t item_COUNT,int pilihan_VALUE,const struct 통신주소 *surel,통신주소길이형 panjang_VALUE) {
    return 결과검사(사용자호출(34,peserta,(uintptr_t)data,item_COUNT,pilihan_VALUE,(uintptr_t)surel,panjang_VALUE));
}
intptr_t 자료전문받기(int peserta,void *data,size_t item_COUNT,int pilihan_VALUE,struct 통신주소 *surel,통신주소길이형 *panjang_VALUE) {
    return 결과검사(사용자호출(35,peserta,(uintptr_t)data,item_COUNT,pilihan_VALUE,(uintptr_t)surel,(uintptr_t)panjang_VALUE));
}
int 통신주소읽기(int peserta,struct 통신주소 *surel,통신주소길이형 *panjang_VALUE) {
    return 결과검사(사용자호출(36,peserta,(uintptr_t)surel,(uintptr_t)panjang_VALUE,0,0,0));
}
int CONNECT_jaringan(int peserta,const struct 통신주소 *surel,통신주소길이형 panjang_VALUE) {
    return 결과검사(사용자호출(37,peserta,(uintptr_t)surel,panjang_VALUE,0,0,0));
}
int 통신연결기다리기(int peserta,int Menunggu_COUNT) {
    return 결과검사(사용자호출(38,peserta,Menunggu_COUNT,0,0,0,0));
}
int terima_koneksi_jaringan(int peserta,struct 통신주소 *surel,통신주소길이형 *panjang_VALUE) {
    return 결과검사(사용자호출(39,peserta,(uintptr_t)surel,(uintptr_t)panjang_VALUE,0,0,0));
}

/* berkas 함수도 독립된 Indonesia fungsi_VALUE 심볼로 제공한다. */
int buat_file(const char *jalur,int metode_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)jalur,metode_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int berkas,void *data,size_t item_COUNT) { return 결과검사(사용자호출(2,berkas,(uintptr_t)data,item_COUNT,0,0,0)); }
입출력결과형 tulis_file_data(int berkas,const void *data,size_t item_COUNT) { return 결과검사(사용자호출(1,berkas,(uintptr_t)data,item_COUNT,0,0,0)); }
int Tutup_file(int berkas) { return 결과검사(사용자호출(4,berkas,0,0,0,0,0)); }
file_OFFSET_TYPE cari_file(int berkas,file_OFFSET_TYPE 거리,int Tugas_akar) { return 결과검사(사용자호출(5,berkas,거리,Tugas_akar,0,0,0)); }
int hapus_file_entri_nama(const char *jalur) { return 결과검사(사용자호출(11,(uintptr_t)jalur,0,0,0,0,0)); }
int set_file_panjang(int berkas,file_OFFSET_TYPE Ukuran) { return 결과검사(사용자호출(10,berkas,Ukuran,0,0,0,0)); }
int penerapan_Files(int berkas) { return 결과검사(사용자호출(12,berkas,0,0,0,0,0)); }
int ukuran_file(int berkas) { return 결과검사(사용자호출(9,berkas,0,0,0,0,0)); }
