// 동일 Татарча 헤더를 사용하는 별도 EL0 библиотека. төш_VALUE 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int хата_коды;
int *pk_errno_location(void) { return &хата_коды; }
static intptr_t 결과검사(intptr_t үлчәм) { if (үлчәм < 0) { хата_коды = -үлчәм; return -1; } return үлчәм; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
файл_OFFSET_TYPE pk_lseek(int fd, файл_OFFSET_TYPE offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, файл_OFFSET_TYPE size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Татарча 공개 함수의 фактик_мәгълүмат EL0 구현. 구조체는 SVC에서 экземпляр_VALUE·검증한다. */
int 통신종단점만들기(int адрес_Гаилә,int 통신방식,int күчерү_протокол) {
    return 결과검사(사용자호출(32,адрес_Гаилә,통신방식,күчерү_протокол,0,0,0));
}
int BIND_адрес(int 종단,const struct 통신주소 *адрес,통신주소길이형 озынлык_VALUE) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)адрес,озынлык_VALUE,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *мәгълүмат,size_t элемент_COUNT,int тамгаланган_өлеш_VALUE,const struct 통신주소 *адрес,통신주소길이형 озынлык_VALUE) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)мәгълүмат,элемент_COUNT,тамгаланган_өлеш_VALUE,(uintptr_t)адрес,озынлык_VALUE));
}
intptr_t 자료전문받기(int 종단,void *мәгълүмат,size_t элемент_COUNT,int тамгаланган_өлеш_VALUE,struct 통신주소 *адрес,통신주소길이형 *озынлык_VALUE) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)мәгълүмат,элемент_COUNT,тамгаланган_өлеш_VALUE,(uintptr_t)адрес,(uintptr_t)озынлык_VALUE));
}
int 통신주소읽기(int 종단,struct 통신주소 *адрес,통신주소길이형 *озынлык_VALUE) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)адрес,(uintptr_t)озынлык_VALUE,0,0,0));
}
int ялгау_Челтәр(int 종단,const struct 통신주소 *адрес,통신주소길이형 озынлык_VALUE) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)адрес,озынлык_VALUE,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int кабул_итү_челтәр_аша_тоташу(int 종단,struct 통신주소 *адрес,통신주소길이형 *озынлык_VALUE) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)адрес,(uintptr_t)озынлык_VALUE,0,0,0));
}

/* Birem 함수도 독립된 Татарча ФУНКЦИЯ_VALUE 심볼로 제공한다. */
int ачу_файл(const char *Yul,int ысул_MODE,...) { return 결과검사(사용자호출(3,(uintptr_t)Yul,ысул_MODE,0,0,0,0)); }
입출력결과형 파일자료읽기(int Birem,void *мәгълүмат,size_t элемент_COUNT) { return 결과검사(사용자호출(2,Birem,(uintptr_t)мәгълүмат,элемент_COUNT,0,0,0)); }
입출력결과형 язу_файл_мәгълүмат(int Birem,const void *мәгълүмат,size_t элемент_COUNT) { return 결과검사(사용자호출(1,Birem,(uintptr_t)мәгълүмат,элемент_COUNT,0,0,0)); }
int чик_файл(int Birem) { return 결과검사(사용자호출(4,Birem,0,0,0,0,0)); }
файл_OFFSET_TYPE эзләү_файл(int Birem,файл_OFFSET_TYPE 거리,int экранга_җибәрү_тамыр) { return 결과검사(사용자호출(5,Birem,거리,экранга_җибәрү_тамыр,0,0,0)); }
int бетерү_файл_кертү_исем(const char *Yul) { return 결과검사(사용자호출(11,(uintptr_t)Yul,0,0,0,0,0)); }
int җыелма_файл_озынлык(int Birem,файл_OFFSET_TYPE үлчәмен_үзгәртү) { return 결과검사(사용자호출(10,Birem,үлчәмен_үзгәртү,0,0,0,0)); }
int 파일저장확정(int Birem) { return 결과검사(사용자호출(12,Birem,0,0,0,0,0)); }
int файл_үлчәмен_үзгәртү(int Birem) { return 결과검사(사용자호출(9,Birem,0,0,0,0,0)); }
