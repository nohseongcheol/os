// 동일 한국어 헤더를 사용하는 별도 EL0 library. kernel_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int error_code;
int *pk_errno_location(void) { return &error_code; }
static intptr_t 결과검사(intptr_t sukat) { if (sukat < 0) { error_code = -sukat; return -1; } return sukat; }
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

/* 한국어 공개 함수의 totoo_data EL0 구현. 구조체는 SVC에서 gumawa_ng_kopya_VALUE·검증한다. */
int 통신종단점만들기(int email_Pamilya,int 통신방식,int lipat_protokol) {
    return 결과검사(사용자호출(32,email_Pamilya,통신방식,lipat_protokol,0,0,0));
}
int BIND_email(int 종단,const struct 통신주소 *email,통신주소길이형 haba_VALUE) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)email,haba_VALUE,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *data,size_t item_COUNT,int seleksyon_VALUE,const struct 통신주소 *email,통신주소길이형 haba_VALUE) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)data,item_COUNT,seleksyon_VALUE,(uintptr_t)email,haba_VALUE));
}
intptr_t 자료전문받기(int 종단,void *data,size_t item_COUNT,int seleksyon_VALUE,struct 통신주소 *email,통신주소길이형 *haba_VALUE) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)data,item_COUNT,seleksyon_VALUE,(uintptr_t)email,(uintptr_t)haba_VALUE));
}
int 통신주소읽기(int 종단,struct 통신주소 *email,통신주소길이형 *haba_VALUE) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)email,(uintptr_t)haba_VALUE,0,0,0));
}
int CONNECT_Network(int 종단,const struct 통신주소 *email,통신주소길이형 haba_VALUE) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)email,haba_VALUE,0,0,0));
}
int 통신연결기다리기(int 종단,int Naghihintay_COUNT) {
    return 결과검사(사용자호출(38,종단,Naghihintay_COUNT,0,0,0,0));
}
int tanggapin_koneksyon_sa_network(int 종단,struct 통신주소 *email,통신주소길이형 *haba_VALUE) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)email,(uintptr_t)haba_VALUE,0,0,0));
}

/* file 함수도 독립된 한국어 pormula_VALUE 심볼로 제공한다. */
int buksan_file(const char *path,int pamamaraan_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)path,pamamaraan_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int file,void *data,size_t item_COUNT) { return 결과검사(사용자호출(2,file,(uintptr_t)data,item_COUNT,0,0,0)); }
입출력결과형 sumulat_file_data(int file,const void *data,size_t item_COUNT) { return 결과검사(사용자호출(1,file,(uintptr_t)data,item_COUNT,0,0,0)); }
int isara_file(int file) { return 결과검사(사용자호출(4,file,0,0,0,0,0)); }
file_OFFSET_TYPE i_seek_file(int file,file_OFFSET_TYPE 거리,int Project_root) { return 결과검사(사용자호출(5,file,거리,Project_root,0,0,0)); }
int tanggalin_file_pagpasok_pangalan(const char *path) { return 결과검사(사용자호출(11,(uintptr_t)path,0,0,0,0,0)); }
int set_file_haba(int file,file_OFFSET_TYPE sukat_82232621) { return 결과검사(사용자호출(10,file,sukat_82232621,0,0,0,0)); }
int 파일저장확정(int file) { return 결과검사(사용자호출(12,file,0,0,0,0,0)); }
int file_sukat(int file) { return 결과검사(사용자호출(9,file,0,0,0,0,0)); }
