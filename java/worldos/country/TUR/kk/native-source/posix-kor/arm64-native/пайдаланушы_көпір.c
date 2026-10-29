// 동일 한국어 헤더를 사용하는 별도 EL0 кітапхана. ядро_мән 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int қате_коды;
int *pk_errno_location(void) { return &қате_коды; }
static intptr_t 결과검사(intptr_t НӘТИЖЕ) { if (НӘТИЖЕ < 0) { қате_коды = -НӘТИЖЕ; return -1; } return НӘТИЖЕ; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
файл_жылжыту_Түрі pk_lseek(int fd, файл_жылжыту_Түрі offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, файл_жылжыту_Түрі size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 нақты_деректер EL0 구현. 구조체는 SVC에서 дана_мән·검증한다. */
int жасау_қатысушы(int мекенжай_топ,int 통신방식,int аудару_протокол) {
    return 결과검사(사용자호출(32,мекенжай_топ,통신방식,аудару_протокол,0,0,0));
}
int байланыстыру_мекенжай(int қатысушы,const struct 통신주소 *мекенжай,통신주소길이형 ұзындық_мән) {
    return 결과검사(사용자호출(33,қатысушы,(uintptr_t)мекенжай,ұзындық_мән,0,0,0));
}
intptr_t 자료전문보내기(int қатысушы,const void *деректер,size_t 개수,int таңдау_мән,const struct 통신주소 *мекенжай,통신주소길이형 ұзындық_мән) {
    return 결과검사(사용자호출(34,қатысушы,(uintptr_t)деректер,개수,таңдау_мән,(uintptr_t)мекенжай,ұзындық_мән));
}
intptr_t 자료전문받기(int қатысушы,void *деректер,size_t 개수,int таңдау_мән,struct 통신주소 *мекенжай,통신주소길이형 *ұзындық_мән) {
    return 결과검사(사용자호출(35,қатысушы,(uintptr_t)деректер,개수,таңдау_мән,(uintptr_t)мекенжай,(uintptr_t)ұзындық_мән));
}
int 통신주소읽기(int қатысушы,struct 통신주소 *мекенжай,통신주소길이형 *ұзындық_мән) {
    return 결과검사(사용자호출(36,қатысушы,(uintptr_t)мекенжай,(uintptr_t)ұзындық_мән,0,0,0));
}
int қосу_желі(int қатысушы,const struct 통신주소 *мекенжай,통신주소길이형 ұзындық_мән) {
    return 결과검사(사용자호출(37,қатысушы,(uintptr_t)мекенжай,ұзындық_мән,0,0,0));
}
int 통신연결기다리기(int қатысушы,int 대기수) {
    return 결과검사(사용자호출(38,қатысушы,대기수,0,0,0,0));
}
int қабылдау_желілік_байланыс(int қатысушы,struct 통신주소 *мекенжай,통신주소길이형 *ұзындық_мән) {
    return 결과검사(사용자호출(39,қатысушы,(uintptr_t)мекенжай,(uintptr_t)ұзындық_мән,0,0,0));
}

/* Файл 함수도 독립된 한국어 функция_мән 심볼로 제공한다. */
int ашу_файл(const char *Жол_2,int әдіс_режим,...) { return 결과검사(사용자호출(3,(uintptr_t)Жол_2,әдіс_режим,0,0,0,0)); }
입출력결과형 파일자료읽기(int Файл,void *деректер,size_t 개수) { return 결과검사(사용자호출(2,Файл,(uintptr_t)деректер,개수,0,0,0)); }
입출력결과형 жазу_файл_деректер(int Файл,const void *деректер,size_t 개수) { return 결과검사(사용자호출(1,Файл,(uintptr_t)деректер,개수,0,0,0)); }
int Жабу_файл(int Файл) { return 결과검사(사용자호출(4,Файл,0,0,0,0,0)); }
файл_жылжыту_Түрі іздеу_файл(int Файл,файл_жылжыту_Түрі 거리,int жоба_түбір) { return 결과검사(사용자호출(5,Файл,거리,жоба_түбір,0,0,0)); }
int жою_файл_енгізу_аты(const char *Жол_2) { return 결과검사(사용자호출(11,(uintptr_t)Жол_2,0,0,0,0,0)); }
int жинақ_файл_ұзындық(int Файл,файл_жылжыту_Түрі Өлшемі) { return 결과검사(사용자호출(10,Файл,Өлшемі,0,0,0,0)); }
int бекіту_файл_сақтау_орны(int Файл) { return 결과검사(사용자호출(12,Файл,0,0,0,0,0)); }
int файл_өлшемі(int Файл) { return 결과검사(사용자호출(9,Файл,0,0,0,0,0)); }
