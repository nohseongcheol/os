// 동일 한국어 헤더를 사용하는 별도 EL0 ଲାଇବ୍ରେରୀ. କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int ତୃଟି_କୋଡ୍;
int *pk_errno_location(void) { return &ତୃଟି_କୋଡ୍; }
static intptr_t 결과검사(intptr_t ମାପ) { if (ମାପ < 0) { ତୃଟି_କୋଡ୍ = -ମାପ; return -1; } return ମାପ; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ଫାଇଲ୍_ଅଫ୍_ସେଟ୍_ଟାଇପ୍_କରିବା pk_lseek(int fd, ଫାଇଲ୍_ଅଫ୍_ସେଟ୍_ଟାଇପ୍_କରିବା offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ଫାଇଲ୍_ଅଫ୍_ସେଟ୍_ଟାଇପ୍_କରିବା size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 ପ୍ରକୃତ_ଡାଟା EL0 구현. 구조체는 SVC에서 କପି_ମୂଲ୍ୟ·검증한다. */
int 통신종단점만들기(int ଠିକଣା_ପରିବାର,int 통신방식,int ସ୍ଥାନାନ୍ତର_ପ୍ରୋଟୋକଲ୍) {
    return 결과검사(사용자호출(32,ଠିକଣା_ପରିବାର,통신방식,ସ୍ଥାନାନ୍ତର_ପ୍ରୋଟୋକଲ୍,0,0,0));
}
int ବନ୍ଧନ_ଠିକଣା(int 종단,const struct 통신주소 *ଠିକଣା,통신주소길이형 ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)ଠିକଣା,ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *ଡାଟା,size_t 개수,int ଚୟନ_ମୂଲ୍ୟ,const struct 통신주소 *ଠିକଣା,통신주소길이형 ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)ଡାଟା,개수,ଚୟନ_ମୂଲ୍ୟ,(uintptr_t)ଠିକଣା,ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ));
}
intptr_t 자료전문받기(int 종단,void *ଡାଟା,size_t 개수,int ଚୟନ_ମୂଲ୍ୟ,struct 통신주소 *ଠିକଣା,통신주소길이형 *ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)ଡାଟା,개수,ଚୟନ_ମୂଲ୍ୟ,(uintptr_t)ଠିକଣା,(uintptr_t)ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ));
}
int 통신주소읽기(int 종단,struct 통신주소 *ଠିକଣା,통신주소길이형 *ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)ଠିକଣା,(uintptr_t)ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ,0,0,0));
}
int ସଂଯୋଗ_ନେଟ୍_ୱାର୍କ୍(int 종단,const struct 통신주소 *ଠିକଣା,통신주소길이형 ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)ଠିକଣା,ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int ସ୍ୱୀକାର_କରିବା_ନେଟ୍_ୱାର୍କ_ସଂଯୋଜନ(int 종단,struct 통신주소 *ଠିକଣା,통신주소길이형 *ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)ଠିକଣା,(uintptr_t)ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ,0,0,0));
}

/* ଫାଇଲ 함수도 독립된 한국어 Excel_ଟେବଲ୍_ମୂଲ୍ୟ 심볼로 제공한다. */
int ଖୋଲିବା_ଫାଇଲ୍(const char *ପଥ,int ପଦ୍ଧତି_ମୋଡ୍,...) { return 결과검사(사용자호출(3,(uintptr_t)ପଥ,ପଦ୍ଧତି_ମୋଡ୍,0,0,0,0)); }
입출력결과형 파일자료읽기(int ଫାଇଲ,void *ଡାଟା,size_t 개수) { return 결과검사(사용자호출(2,ଫାଇଲ,(uintptr_t)ଡାଟା,개수,0,0,0)); }
입출력결과형 ଲିଖନ_ଫାଇଲ୍_ଡାଟା(int ଫାଇଲ,const void *ଡାଟା,size_t 개수) { return 결과검사(사용자호출(1,ଫାଇଲ,(uintptr_t)ଡାଟା,개수,0,0,0)); }
int ବନ୍ଦ_ଫାଇଲ୍(int ଫାଇଲ) { return 결과검사(사용자호출(4,ଫାଇଲ,0,0,0,0,0)); }
ଫାଇଲ୍_ଅଫ୍_ସେଟ୍_ଟାଇପ୍_କରିବା ସୀକ୍_ଫାଇଲ୍(int ଫାଇଲ,ଫାଇଲ୍_ଅଫ୍_ସେଟ୍_ଟାଇପ୍_କରିବା 거리,int ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍) { return 결과검사(사용자호출(5,ଫାଇଲ,거리,ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍,0,0,0)); }
int ଅପସାରଣ_କରିବା_ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ(const char *ପଥ) { return 결과검사(사용자호출(11,(uintptr_t)ପଥ,0,0,0,0,0)); }
int ସେଟ୍_ଫାଇଲ୍_ଦୈର୍ଘ୍ୟ(int ଫାଇଲ,ଫାଇଲ୍_ଅଫ୍_ସେଟ୍_ଟାଇପ୍_କରିବା ଆକାର) { return 결과검사(사용자호출(10,ଫାଇଲ,ଆକାର,0,0,0,0)); }
int 파일저장확정(int ଫାଇଲ) { return 결과검사(사용자호출(12,ଫାଇଲ,0,0,0,0,0)); }
int ଫାଇଲ୍_ଅକାର(int ଫାଇଲ) { return 결과검사(사용자호출(9,ଫାଇଲ,0,0,0,0,0)); }
