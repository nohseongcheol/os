// 동일 Български 헤더를 사용하는 별도 EL0 библиотека. ядро_стойност 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int код_на_грешка;
int *pk_errno_location(void) { return &код_на_грешка; }
static intptr_t 결과검사(intptr_t РЕЗУЛТАТ) { if (РЕЗУЛТАТ < 0) { код_на_грешка = -РЕЗУЛТАТ; return -1; } return РЕЗУЛТАТ; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Файл_Изместване_Тип pk_lseek(int fd, Файл_Изместване_Тип offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Файл_Изместване_Тип size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Български 공개 함수의 действителен_данни EL0 구현. 구조체는 SVC에서 копирам_стойност·검증한다. */
int Създаване_участник(int адрес_семейни,int 통신방식,int прехвърлям_протокол) {
    return 결과검사(사용자호출(32,адрес_семейни,통신방식,прехвърлям_протокол,0,0,0));
}
int обвързвам_адрес(int участник,const struct 통신주소 *адрес,통신주소길이형 길이) {
    return 결과검사(사용자호출(33,участник,(uintptr_t)адрес,길이,0,0,0));
}
intptr_t изпращам_дейтаграма_данни(int участник,const void *данни,size_t 개수,int избор_стойност,const struct 통신주소 *адрес,통신주소길이형 길이) {
    return 결과검사(사용자호출(34,участник,(uintptr_t)данни,개수,избор_стойност,(uintptr_t)адрес,길이));
}
intptr_t получавам_дейтаграма_данни(int участник,void *данни,size_t 개수,int избор_стойност,struct 통신주소 *адрес,통신주소길이형 *길이) {
    return 결과검사(사용자호출(35,участник,(uintptr_t)данни,개수,избор_стойност,(uintptr_t)адрес,(uintptr_t)길이));
}
int 통신주소읽기(int участник,struct 통신주소 *адрес,통신주소길이형 *길이) {
    return 결과검사(사용자호출(36,участник,(uintptr_t)адрес,(uintptr_t)길이,0,0,0));
}
int връзка_мрежа(int участник,const struct 통신주소 *адрес,통신주소길이형 길이) {
    return 결과검사(사용자호출(37,участник,(uintptr_t)адрес,길이,0,0,0));
}
int 통신연결기다리기(int участник,int 대기수) {
    return 결과검사(사용자호출(38,участник,대기수,0,0,0,0));
}
int приемам_мрежова_връзка(int участник,struct 통신주소 *адрес,통신주소길이형 *길이) {
    return 결과검사(사용자호출(39,участник,(uintptr_t)адрес,(uintptr_t)길이,0,0,0));
}

/* Файл 함수도 독립된 Български функция_стойност 심볼로 제공한다. */
int отварям_Файл(const char *ПЪТ,int метод_режим,...) { return 결과검사(사용자호출(3,(uintptr_t)ПЪТ,метод_режим,0,0,0,0)); }
입출력결과형 파일자료읽기(int Файл,void *данни,size_t 개수) { return 결과검사(사용자호출(2,Файл,(uintptr_t)данни,개수,0,0,0)); }
입출력결과형 записване_Файл_данни(int Файл,const void *данни,size_t 개수) { return 결과검사(사용자호출(1,Файл,(uintptr_t)данни,개수,0,0,0)); }
int затварям_Файл(int Файл) { return 결과검사(사용자호출(4,Файл,0,0,0,0,0)); }
Файл_Изместване_Тип търся_Файл(int Файл,Файл_Изместване_Тип 거리,int проект_корен) { return 결과검사(사용자호출(5,Файл,거리,проект_корен,0,0,0)); }
int премахвам_Файл_запис_препратка_към_клетка(const char *ПЪТ) { return 결과검사(사용자호출(11,(uintptr_t)ПЪТ,0,0,0,0,0)); }
int 파일길이정하기(int Файл,Файл_Изместване_Тип Размер) { return 결과검사(사용자호출(10,Файл,Размер,0,0,0,0)); }
int фиксиране_място_за_съхранение_на_файлове(int Файл) { return 결과검사(사용자호출(12,Файл,0,0,0,0,0)); }
int размер_на_файл(int Файл) { return 결과검사(사용자호출(9,Файл,0,0,0,0,0)); }
