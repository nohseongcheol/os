// 동일 한국어 헤더를 사용하는 별도 EL0 లైబ్రరీ. കെര്_ണല്_മൂല്യം 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int തെറ്റ്_കോഡ്;
int *pk_errno_location(void) { return &തെറ്റ്_കോഡ്; }
static intptr_t 결과검사(intptr_t അളവ്) { if (അളവ് < 0) { തെറ്റ്_കോഡ് = -അളവ്; return -1; } return അളവ്; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ഫയല്_ഓഫ്_സെറ്റ്_ടൈപ്പ്_ചെയ്യുക pk_lseek(int fd, ഫയല്_ഓഫ്_സെറ്റ്_ടൈപ്പ്_ചെയ്യുക offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ഫയല്_ഓഫ്_സെറ്റ്_ടൈപ്പ്_ചെയ്യുക size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 വാസ്തവമായ_ഡാറ്റാ EL0 구현. 구조체는 SVC에서 ദൃഷ്ടാന്തം_മൂല്യം·검증한다. */
int സൃഷ്_ടിക്കുക_അവസാനബിന്ദു(int ഇമെയിൽ_കുടുംബം,int 통신방식,int കൈമാറുക_പ്രോട്ടോക്കോള്) {
    return 결과검사(사용자호출(32,ഇമെയിൽ_കുടുംബം,통신방식,കൈമാറുക_പ്രോട്ടോക്കോള്,0,0,0));
}
int బైండ్_చేయి_ഇമെയിൽ(int അവസാനബിന്ദു,const struct 통신주소 *ഇമെയിൽ,통신주소길이형 ദൈര്_ഘ്യം_മൂല്യം) {
    return 결과검사(사용자호출(33,അവസാനബിന്ദു,(uintptr_t)ഇമെയിൽ,ദൈര്_ഘ്യം_മൂല്യം,0,0,0));
}
intptr_t 자료전문보내기(int അവസാനബിന്ദു,const void *ഡാറ്റാ,size_t 개수,int തിരഞ്ഞെടുക്കല്_മൂല്യം,const struct 통신주소 *ഇമെയിൽ,통신주소길이형 ദൈര്_ഘ്യം_മൂല്യം) {
    return 결과검사(사용자호출(34,അവസാനബിന്ദു,(uintptr_t)ഡാറ്റാ,개수,തിരഞ്ഞെടുക്കല്_മൂല്യം,(uintptr_t)ഇമെയിൽ,ദൈര്_ഘ്യം_മൂല്യം));
}
intptr_t 자료전문받기(int അവസാനബിന്ദു,void *ഡാറ്റാ,size_t 개수,int തിരഞ്ഞെടുക്കല്_മൂല്യം,struct 통신주소 *ഇമെയിൽ,통신주소길이형 *ദൈര്_ഘ്യം_മൂല്യം) {
    return 결과검사(사용자호출(35,അവസാനബിന്ദു,(uintptr_t)ഡാറ്റാ,개수,തിരഞ്ഞെടുക്കല്_മൂല്യം,(uintptr_t)ഇമെയിൽ,(uintptr_t)ദൈര്_ഘ്യം_മൂല്യം));
}
int 통신주소읽기(int അവസാനബിന്ദു,struct 통신주소 *ഇമെയിൽ,통신주소길이형 *ദൈര്_ഘ്യം_മൂല്യം) {
    return 결과검사(사용자호출(36,അവസാനബിന്ദു,(uintptr_t)ഇമെയിൽ,(uintptr_t)ദൈര്_ഘ്യം_മൂല്യം,0,0,0));
}
int കണക്റ്റ്_നെറ്റ്_വർക്ക്(int അവസാനബിന്ദു,const struct 통신주소 *ഇമെയിൽ,통신주소길이형 ദൈര്_ഘ്യം_മൂല്യം) {
    return 결과검사(사용자호출(37,അവസാനബിന്ദു,(uintptr_t)ഇമെയിൽ,ദൈര്_ഘ്യം_മൂല്യം,0,0,0));
}
int 통신연결기다리기(int അവസാനബിന്ദു,int 대기수) {
    return 결과검사(사용자호출(38,അവസാനബിന്ദു,대기수,0,0,0,0));
}
int സ്വീകരിക്കുക_നെറ്റ്_വർക്ക്_കണക്ഷൻ(int അവസാനബിന്ദു,struct 통신주소 *ഇമെയിൽ,통신주소길이형 *ദൈര്_ഘ്യം_മൂല്യം) {
    return 결과검사(사용자호출(39,അവസാനബിന്ദു,(uintptr_t)ഇമെയിൽ,(uintptr_t)ദൈര്_ഘ്യം_മൂല്യം,0,0,0));
}

/* ഫയല് 함수도 독립된 한국어 കാര്യപ്രവര്_ത്തനം_മൂല്യം 심볼로 제공한다. */
int തുറക്കുക_ഫയല്(const char *വഴി,int విధానం_മോഡ്,...) { return 결과검사(사용자호출(3,(uintptr_t)വഴി,విధానం_മോഡ്,0,0,0,0)); }
입출력결과형 파일자료읽기(int ഫയല്,void *ഡാറ്റാ,size_t 개수) { return 결과검사(사용자호출(2,ഫയല്,(uintptr_t)ഡാറ്റാ,개수,0,0,0)); }
입출력결과형 റൈറ്റ്_ചെയ്യുക_ഫയല്_ഡാറ്റാ(int ഫയല്,const void *ഡാറ്റാ,size_t 개수) { return 결과검사(사용자호출(1,ഫയല്,(uintptr_t)ഡാറ്റാ,개수,0,0,0)); }
int അടയ്ക്കുക_ഫയല്(int ഫയല്) { return 결과검사(사용자호출(4,ഫയല്,0,0,0,0,0)); }
ഫയല്_ഓഫ്_സെറ്റ്_ടൈപ്പ്_ചെയ്യുക തിരയുക_ഫയല്(int ഫയല്,ഫയല്_ഓഫ്_സെറ്റ്_ടൈപ്പ്_ചെയ്യുക 거리,int പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം) { return 결과검사(사용자호출(5,ഫയല്,거리,പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം,0,0,0)); }
int നീക്കംചെയ്യുക_ഫയല്_എന്_ട്രി_നാ_മം(const char *വഴി) { return 결과검사(사용자호출(11,(uintptr_t)വഴി,0,0,0,0,0)); }
int ഗണം_ഫയല്_ദൈര്_ഘ്യം(int ഫയല്,ഫയല്_ഓഫ്_സെറ്റ്_ടൈപ്പ്_ചെയ്യുക വലിപ്പം) { return 결과검사(사용자호출(10,ഫയല്,വലിപ്പം,0,0,0,0)); }
int 파일저장확정(int ഫയല്) { return 결과검사(사용자호출(12,ഫയല്,0,0,0,0,0)); }
int ഫയല്_വലുപ്പം_ക്രമീകരിക്കുക(int ഫയല്) { return 결과검사(사용자호출(9,ഫയല്,0,0,0,0,0)); }
