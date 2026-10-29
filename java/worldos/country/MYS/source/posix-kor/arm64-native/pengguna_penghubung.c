// 동일 Melayu 헤더를 사용하는 별도 EL0 pustaka. kernel_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int kod_ralat;
int *pk_errno_location(void) { return &kod_ralat; }
static intptr_t 결과검사(intptr_t ukuran) { if (ukuran < 0) { kod_ralat = -ukuran; return -1; } return ukuran; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
fail_Ofset_TYPE pk_lseek(int fd, fail_Ofset_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, fail_Ofset_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Melayu 공개 함수의 sebenar_data EL0 pelaksanaan. 구조체는 SVC에서 tika_VALUE·검증한다. */
int cipta_peserta(int e_mel_Keluarga,int 통신방식,int pindah_protokol) {
    return 결과검사(사용자호출(32,e_mel_Keluarga,통신방식,pindah_protokol,0,0,0));
}
int ikat_e_mel(int peserta,const struct 통신주소 *e_mel,통신주소길이형 kepanjangan_VALUE) {
    return 결과검사(사용자호출(33,peserta,(uintptr_t)e_mel,kepanjangan_VALUE,0,0,0));
}
intptr_t 자료전문보내기(int peserta,const void *data,size_t item_COUNT,int pilihan_VALUE,const struct 통신주소 *e_mel,통신주소길이형 kepanjangan_VALUE) {
    return 결과검사(사용자호출(34,peserta,(uintptr_t)data,item_COUNT,pilihan_VALUE,(uintptr_t)e_mel,kepanjangan_VALUE));
}
intptr_t 자료전문받기(int peserta,void *data,size_t item_COUNT,int pilihan_VALUE,struct 통신주소 *e_mel,통신주소길이형 *kepanjangan_VALUE) {
    return 결과검사(사용자호출(35,peserta,(uintptr_t)data,item_COUNT,pilihan_VALUE,(uintptr_t)e_mel,(uintptr_t)kepanjangan_VALUE));
}
int 통신주소읽기(int peserta,struct 통신주소 *e_mel,통신주소길이형 *kepanjangan_VALUE) {
    return 결과검사(사용자호출(36,peserta,(uintptr_t)e_mel,(uintptr_t)kepanjangan_VALUE,0,0,0));
}
int CONNECT_rangkaian(int peserta,const struct 통신주소 *e_mel,통신주소길이형 kepanjangan_VALUE) {
    return 결과검사(사용자호출(37,peserta,(uintptr_t)e_mel,kepanjangan_VALUE,0,0,0));
}
int 통신연결기다리기(int peserta,int Menunggu_COUNT) {
    return 결과검사(사용자호출(38,peserta,Menunggu_COUNT,0,0,0,0));
}
int terima_sambungan_rangkaian(int peserta,struct 통신주소 *e_mel,통신주소길이형 *kepanjangan_VALUE) {
    return 결과검사(사용자호출(39,peserta,(uintptr_t)e_mel,(uintptr_t)kepanjangan_VALUE,0,0,0));
}

/* Fail 함수도 독립된 Melayu fungsi_VALUE 심볼로 제공한다. */
int buka_fail(const char *LALUAN,int kaedah_mod,...) { return 결과검사(사용자호출(3,(uintptr_t)LALUAN,kaedah_mod,0,0,0,0)); }
입출력결과형 파일자료읽기(int Fail,void *data,size_t item_COUNT) { return 결과검사(사용자호출(2,Fail,(uintptr_t)data,item_COUNT,0,0,0)); }
입출력결과형 tulis_fail_data(int Fail,const void *data,size_t item_COUNT) { return 결과검사(사용자호출(1,Fail,(uintptr_t)data,item_COUNT,0,0,0)); }
int Tutup_fail(int Fail) { return 결과검사(사용자호출(4,Fail,0,0,0,0,0)); }
fail_Ofset_TYPE cari_fail(int Fail,fail_Ofset_TYPE 거리,int projek_akar) { return 결과검사(사용자호출(5,Fail,거리,projek_akar,0,0,0)); }
int alih_keluar_fail_pemasukan_nama(const char *LALUAN) { return 결과검사(사용자호출(11,(uintptr_t)LALUAN,0,0,0,0,0)); }
int set_fail_kepanjangan(int Fail,fail_Ofset_TYPE Saiz) { return 결과검사(사용자호출(10,Fail,Saiz,0,0,0,0)); }
int lakukan_storan_fail(int Fail) { return 결과검사(사용자호출(12,Fail,0,0,0,0,0)); }
int saiz_fail(int Fail) { return 결과검사(사용자호출(9,Fail,0,0,0,0,0)); }
