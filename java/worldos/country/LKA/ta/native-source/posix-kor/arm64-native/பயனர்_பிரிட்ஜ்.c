// 동일 தமிழ் 헤더를 사용하는 별도 EL0 நூலகம். கரு_மதிப்பு 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int பிழைக்_குறியீடு;
int *pk_errno_location(void) { return &பிழைக்_குறியீடு; }
static intptr_t 결과검사(intptr_t அளவிடக்கூடியது) { if (அளவிடக்கூடியது < 0) { பிழைக்_குறியீடு = -அளவிடக்கூடியது; return -1; } return அளவிடக்கூடியது; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
கோப்பு_ஆஃப்செட்_வகை pk_lseek(int fd, கோப்பு_ஆஃப்செட்_வகை offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, கோப்பு_ஆஃப்செட்_வகை size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* தமிழ் 공개 함수의 அசல்_தரவு EL0 구현. 구조체는 SVC에서 நகலெடு_மதிப்பு·검증한다. */
int உருவாக்கு_முடிவுப்_புள்ளி(int முகவரி_குடும்பம்,int 통신방식,int இடமாற்று_நெறிமுறை) {
    return 결과검사(사용자호출(32,முகவரி_குடும்பம்,통신방식,இடமாற்று_நெறிமுறை,0,0,0));
}
int கட்டு_முகவரி(int முடிவுப்_புள்ளி,const struct 통신주소 *முகவரி,통신주소길이형 நீளம்_மதிப்பு) {
    return 결과검사(사용자호출(33,முடிவுப்_புள்ளி,(uintptr_t)முகவரி,நீளம்_மதிப்பு,0,0,0));
}
intptr_t 자료전문보내기(int முடிவுப்_புள்ளி,const void *தரவு,size_t 개수,int தேர்வு_மதிப்பு,const struct 통신주소 *முகவரி,통신주소길이형 நீளம்_மதிப்பு) {
    return 결과검사(사용자호출(34,முடிவுப்_புள்ளி,(uintptr_t)தரவு,개수,தேர்வு_மதிப்பு,(uintptr_t)முகவரி,நீளம்_மதிப்பு));
}
intptr_t 자료전문받기(int முடிவுப்_புள்ளி,void *தரவு,size_t 개수,int தேர்வு_மதிப்பு,struct 통신주소 *முகவரி,통신주소길이형 *நீளம்_மதிப்பு) {
    return 결과검사(사용자호출(35,முடிவுப்_புள்ளி,(uintptr_t)தரவு,개수,தேர்வு_மதிப்பு,(uintptr_t)முகவரி,(uintptr_t)நீளம்_மதிப்பு));
}
int 통신주소읽기(int முடிவுப்_புள்ளி,struct 통신주소 *முகவரி,통신주소길이형 *நீளம்_மதிப்பு) {
    return 결과검사(사용자호출(36,முடிவுப்_புள்ளி,(uintptr_t)முகவரி,(uintptr_t)நீளம்_மதிப்பு,0,0,0));
}
int இணை_பிணையம்(int முடிவுப்_புள்ளி,const struct 통신주소 *முகவரி,통신주소길이형 நீளம்_மதிப்பு) {
    return 결과검사(사용자호출(37,முடிவுப்_புள்ளி,(uintptr_t)முகவரி,நீளம்_மதிப்பு,0,0,0));
}
int 통신연결기다리기(int முடிவுப்_புள்ளி,int 대기수) {
    return 결과검사(사용자호출(38,முடிவுப்_புள்ளி,대기수,0,0,0,0));
}
int ஏற்றுக்கொள்_நெட்வொர்க்_இணைப்பு(int முடிவுப்_புள்ளி,struct 통신주소 *முகவரி,통신주소길이형 *நீளம்_மதிப்பு) {
    return 결과검사(사용자호출(39,முடிவுப்_புள்ளி,(uintptr_t)முகவரி,(uintptr_t)நீளம்_மதிப்பு,0,0,0));
}

/* கோப்பின்_பெயர் 함수도 독립된 தமிழ் செயல்பாடு_மதிப்பு 심볼로 제공한다. */
int திற_கோப்பு(const char *பாதை_2,int முறை_பயன்முறை,...) { return 결과검사(사용자호출(3,(uintptr_t)பாதை_2,முறை_பயன்முறை,0,0,0,0)); }
입출력결과형 파일자료읽기(int கோப்பின்_பெயர்,void *தரவு,size_t 개수) { return 결과검사(사용자호출(2,கோப்பின்_பெயர்,(uintptr_t)தரவு,개수,0,0,0)); }
입출력결과형 எழுது_கோப்பு_தரவு(int கோப்பின்_பெயர்,const void *தரவு,size_t 개수) { return 결과검사(사용자호출(1,கோப்பின்_பெயர்,(uintptr_t)தரவு,개수,0,0,0)); }
int மூடு_கோப்பு(int கோப்பின்_பெயர்) { return 결과검사(사용자호출(4,கோப்பின்_பெயர்,0,0,0,0,0)); }
கோப்பு_ஆஃப்செட்_வகை தேடு_கோப்பு(int கோப்பின்_பெயர்,கோப்பு_ஆஃப்செட்_வகை 거리,int திட்டப்பணி_மூலம்) { return 결과검사(사용자호출(5,கோப்பின்_பெயர்,거리,திட்டப்பணி_மூலம்,0,0,0)); }
int அகற்று_கோப்பு_உள்ளீடு_பெயர்(const char *பாதை_2) { return 결과검사(사용자호출(11,(uintptr_t)பாதை_2,0,0,0,0,0)); }
int அமை_கோப்பு_நீளம்(int கோப்பின்_பெயர்,கோப்பு_ஆஃப்செட்_வகை அளவு) { return 결과검사(사용자호출(10,கோப்பின்_பெயர்,அளவு,0,0,0,0)); }
int 파일저장확정(int கோப்பின்_பெயர்) { return 결과검사(사용자호출(12,கோப்பின்_பெயர்,0,0,0,0,0)); }
int கோப்பு_அளவு(int கோப்பின்_பெயர்) { return 결과검사(사용자호출(9,கோப்பின்_பெயர்,0,0,0,0,0)); }
