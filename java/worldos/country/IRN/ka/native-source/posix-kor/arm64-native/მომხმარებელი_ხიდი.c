// 동일 한국어 헤더를 사용하는 별도 EL0 ბიბლიოთეკა. ბირთვი_მნიშვნელობა 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int შეცდომის_კოდი;
int *pk_errno_location(void) { return &შეცდომის_კოდი; }
static intptr_t 결과검사(intptr_t გაზომვა) { if (გაზომვა < 0) { შეცდომის_კოდი = -გაზომვა; return -1; } return გაზომვა; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ფაილი_ოფსეტი_აკრეფა pk_lseek(int fd, ფაილი_ოფსეტი_აკრეფა offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ფაილი_ოფსეტი_აკრეფა size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 რეალური_მონაცემები EL0 구현. 구조체는 SVC에서 ასლი_მნიშვნელობა·검증한다. */
int 통신종단점만들기(int მისამართი_ოჯახი,int 통신방식,int გადატანა_პროტოკოლი) {
    return 결과검사(사용자호출(32,მისამართი_ოჯახი,통신방식,გადატანა_პროტოკოლი,0,0,0));
}
int მიბმა_მისამართი(int 종단,const struct 통신주소 *მისამართი,통신주소길이형 სიგრძე_მნიშვნელობა) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)მისამართი,სიგრძე_მნიშვნელობა,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *მონაცემები,size_t 개수,int მონიშნული_ობიექტი_მნიშვნელობა,const struct 통신주소 *მისამართი,통신주소길이형 სიგრძე_მნიშვნელობა) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)მონაცემები,개수,მონიშნული_ობიექტი_მნიშვნელობა,(uintptr_t)მისამართი,სიგრძე_მნიშვნელობა));
}
intptr_t 자료전문받기(int 종단,void *მონაცემები,size_t 개수,int მონიშნული_ობიექტი_მნიშვნელობა,struct 통신주소 *მისამართი,통신주소길이형 *სიგრძე_მნიშვნელობა) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)მონაცემები,개수,მონიშნული_ობიექტი_მნიშვნელობა,(uintptr_t)მისამართი,(uintptr_t)სიგრძე_მნიშვნელობა));
}
int 통신주소읽기(int 종단,struct 통신주소 *მისამართი,통신주소길이형 *სიგრძე_მნიშვნელობა) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)მისამართი,(uintptr_t)სიგრძე_მნიშვნელობა,0,0,0));
}
int დაკავშირება_ქსელი(int 종단,const struct 통신주소 *მისამართი,통신주소길이형 სიგრძე_მნიშვნელობა) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)მისამართი,სიგრძე_მნიშვნელობა,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int მიღება_ქსელის_კავშირი(int 종단,struct 통신주소 *მისამართი,통신주소길이형 *სიგრძე_მნიშვნელობა) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)მისამართი,(uintptr_t)სიგრძე_მნიშვნელობა,0,0,0));
}

/* ფაილი 함수도 독립된 한국어 ფუნქცია_მნიშვნელობა 심볼로 제공한다. */
int გახსნა_ფაილი(const char *გეზი,int მეთოდი_რეჟიმი,...) { return 결과검사(사용자호출(3,(uintptr_t)გეზი,მეთოდი_რეჟიმი,0,0,0,0)); }
입출력결과형 파일자료읽기(int ფაილი,void *მონაცემები,size_t 개수) { return 결과검사(사용자호출(2,ფაილი,(uintptr_t)მონაცემები,개수,0,0,0)); }
입출력결과형 ჩაწერა_ფაილი_მონაცემები(int ფაილი,const void *მონაცემები,size_t 개수) { return 결과검사(사용자호출(1,ფაილი,(uintptr_t)მონაცემები,개수,0,0,0)); }
int დახურვა_ფაილი(int ფაილი) { return 결과검사(사용자호출(4,ფაილი,0,0,0,0,0)); }
ფაილი_ოფსეტი_აკრეფა ძებნა_ფაილი(int ფაილი,ფაილი_ოფსეტი_აკრეფა 거리,int პროეცირება_ფესვი) { return 결과검사(사용자호출(5,ფაილი,거리,პროეცირება_ფესვი,0,0,0)); }
int ამოშლა_ფაილი_შენატანი_სახელი(const char *გეზი) { return 결과검사(사용자호출(11,(uintptr_t)გეზი,0,0,0,0,0)); }
int ნაკრები_ფაილი_სიგრძე(int ფაილი,ფაილი_ოფსეტი_აკრეფა ზომა) { return 결과검사(사용자호출(10,ფაილი,ზომა,0,0,0,0)); }
int 파일저장확정(int ფაილი) { return 결과검사(사용자호출(12,ფაილი,0,0,0,0,0)); }
int ფაილი_ზომის_შეცვლა(int ფაილი) { return 결과검사(사용자호출(9,ფაილი,0,0,0,0,0)); }
