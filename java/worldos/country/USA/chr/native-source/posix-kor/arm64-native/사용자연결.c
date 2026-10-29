// 동일 한국어 헤더를 사용하는 별도 EL0 ᏧᏂᎪᎵᏰᏗᎢ. kernel_ᏧᎬᏩᎶᏗᏯ 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int 오류값;
int *pk_errno_location(void) { return &오류값; }
static intptr_t 결과검사(intptr_t 결과) { if (결과 < 0) { 오류값 = -결과; return -1; } return 결과; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
파일위치형 pk_lseek(int fd, 파일위치형 offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, 파일위치형 size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ EL0 구현. 구조체는 SVC에서 ᏗᏟᎶᏍᏔᏅᎯ_ᏧᎬᏩᎶᏗᏯ·검증한다. */
int 통신종단점만들기(int 주소갈래,int 통신방식,int ᎠᎲᏍᏗ_ᏗᎧᏃᏩᏛᏍᏗ) {
    return 결과검사(사용자호출(32,주소갈래,통신방식,ᎠᎲᏍᏗ_ᏗᎧᏃᏩᏛᏍᏗ,0,0,0));
}
int BIND_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ(int 종단,const struct 통신주소 *ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,통신주소길이형 ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *ᎦᏟᏌᏅᎯ,size_t 개수,int ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ,const struct 통신주소 *ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,통신주소길이형 ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)ᎦᏟᏌᏅᎯ,개수,ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ,(uintptr_t)ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ));
}
intptr_t 자료전문받기(int 종단,void *ᎦᏟᏌᏅᎯ,size_t 개수,int ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ,struct 통신주소 *ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,통신주소길이형 *ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)ᎦᏟᏌᏅᎯ,개수,ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ,(uintptr_t)ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,(uintptr_t)ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ));
}
int 통신주소읽기(int 종단,struct 통신주소 *ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,통신주소길이형 *ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,(uintptr_t)ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ,0,0,0));
}
int ᎫᏓᎳ_ᏧᎾᏚᏓᎵ(int 종단,const struct 통신주소 *ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,통신주소길이형 ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int 통신연결받기(int 종단,struct 통신주소 *ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,통신주소길이형 *ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ᎪᏪᎵ_ᏫᏗᎦᏅᏗ,(uintptr_t)ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ,0,0,0));
}

/* ᎠᏍᏆᏂᎪᏙᏗ 함수도 독립된 한국어 ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ 심볼로 제공한다. */
int ᎯᏍᏚᎢ_ᎠᏍᏆᏂᎪᏙᏗ(const char *ᎠᏍᏓᏩᏛᏍᏗ,int method_ᎬᏙᏗ,...) { return 결과검사(사용자호출(3,(uintptr_t)ᎠᏍᏓᏩᏛᏍᏗ,method_ᎬᏙᏗ,0,0,0,0)); }
입출력결과형 파일자료읽기(int ᎠᏍᏆᏂᎪᏙᏗ,void *ᎦᏟᏌᏅᎯ,size_t 개수) { return 결과검사(사용자호출(2,ᎠᏍᏆᏂᎪᏙᏗ,(uintptr_t)ᎦᏟᏌᏅᎯ,개수,0,0,0)); }
입출력결과형 ᎪᏪᎶᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᎦᏟᏌᏅᎯ(int ᎠᏍᏆᏂᎪᏙᏗ,const void *ᎦᏟᏌᏅᎯ,size_t 개수) { return 결과검사(사용자호출(1,ᎠᏍᏆᏂᎪᏙᏗ,(uintptr_t)ᎦᏟᏌᏅᎯ,개수,0,0,0)); }
int ᎯᏍᏚᎲᎦ_ᎠᏍᏆᏂᎪᏙᏗ(int ᎠᏍᏆᏂᎪᏙᏗ) { return 결과검사(사용자호출(4,ᎠᏍᏆᏂᎪᏙᏗ,0,0,0,0,0)); }
파일위치형 파일위치옮기기(int ᎠᏍᏆᏂᎪᏙᏗ,파일위치형 거리,int 기준) { return 결과검사(사용자호출(5,ᎠᏍᏆᏂᎪᏙᏗ,거리,기준,0,0,0)); }
int ᎯᎲᎾ_ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ(const char *ᎠᏍᏓᏩᏛᏍᏗ) { return 결과검사(사용자호출(11,(uintptr_t)ᎠᏍᏓᏩᏛᏍᏗ,0,0,0,0,0)); }
int ᎦᎪᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᏱᎦᏅᎯᏓ(int ᎠᏍᏆᏂᎪᏙᏗ,파일위치형 ᎢᎩᏓ) { return 결과검사(사용자호출(10,ᎠᏍᏆᏂᎪᏙᏗ,ᎢᎩᏓ,0,0,0,0)); }
int 파일저장확정(int ᎠᏍᏆᏂᎪᏙᏗ) { return 결과검사(사용자호출(12,ᎠᏍᏆᏂᎪᏙᏗ,0,0,0,0,0)); }
int ᎠᏍᏆᏂᎪᏙᏗ_ᎢᎩᏓ(int ᎠᏍᏆᏂᎪᏙᏗ) { return 결과검사(사용자호출(9,ᎠᏍᏆᏂᎪᏙᏗ,0,0,0,0,0)); }
