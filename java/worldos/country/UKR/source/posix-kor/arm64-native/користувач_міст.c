// 동일 українська 헤더를 사용하는 별도 EL0 бібліотека. ядро_значення 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int код_помилки;
int *pk_errno_location(void) { return &код_помилки; }
static intptr_t 결과검사(intptr_t результат) { if (результат < 0) { код_помилки = -результат; return -1; } return результат; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Файл_Зміщена_копія_Тип pk_lseek(int fd, Файл_Зміщена_копія_Тип offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Файл_Зміщена_копія_Тип size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* українська 공개 함수의 фактично_дані EL0 реалізація. 구조체는 SVC에서 екземпляр_значення·검증한다. */
int Створення_учасник(int адреса_сім_я,int 통신방식,int передача_протокол) {
    return 결과검사(사용자호출(32,адреса_сім_я,통신방식,передача_протокол,0,0,0));
}
int зв_язувати_адреса(int учасник,const struct сокет_адреса *Адреса,통신주소길이형 길이) {
    return 결과검사(사용자호출(33,учасник,(uintptr_t)Адреса,길이,0,0,0));
}
intptr_t надсилати_дейтаграма_дані(int учасник,const void *дані,size_t 개수,int вибране_значення,const struct сокет_адреса *Адреса,통신주소길이형 길이) {
    return 결과검사(사용자호출(34,учасник,(uintptr_t)дані,개수,вибране_значення,(uintptr_t)Адреса,길이));
}
intptr_t отримувати_дейтаграма_дані(int учасник,void *дані,size_t 개수,int вибране_значення,struct сокет_адреса *Адреса,통신주소길이형 *길이) {
    return 결과검사(사용자호출(35,учасник,(uintptr_t)дані,개수,вибране_значення,(uintptr_t)Адреса,(uintptr_t)길이));
}
int 통신주소읽기(int учасник,struct сокет_адреса *Адреса,통신주소길이형 *길이) {
    return 결과검사(사용자호출(36,учасник,(uintptr_t)Адреса,(uintptr_t)길이,0,0,0));
}
int зв_язок_мережа(int учасник,const struct сокет_адреса *Адреса,통신주소길이형 길이) {
    return 결과검사(사용자호출(37,учасник,(uintptr_t)Адреса,길이,0,0,0));
}
int 통신연결기다리기(int учасник,int 대기수) {
    return 결과검사(사용자호출(38,учасник,대기수,0,0,0,0));
}
int приймати_підключення_до_мережі(int учасник,struct сокет_адреса *Адреса,통신주소길이형 *길이) {
    return 결과검사(사용자호출(39,учасник,(uintptr_t)Адреса,(uintptr_t)길이,0,0,0));
}

/* файл 함수도 독립된 українська функція_значення 심볼로 제공한다. */
int відкрито_Файл(const char *шлях,int метод_режим,...) { return 결과검사(사용자호출(3,(uintptr_t)шлях,метод_режим,0,0,0,0)); }
입출력결과형 파일자료읽기(int файл,void *дані,size_t 개수) { return 결과검사(사용자호출(2,файл,(uintptr_t)дані,개수,0,0,0)); }
입출력결과형 записування_Файл_дані(int файл,const void *дані,size_t 개수) { return 결과검사(사용자호출(1,файл,(uintptr_t)дані,개수,0,0,0)); }
int Закрити_Файл(int файл) { return 결과검사(사용자호출(4,файл,0,0,0,0,0)); }
Файл_Зміщена_копія_Тип шукати_Файл(int файл,Файл_Зміщена_копія_Тип 거리,int Дії_корінь) { return 결과검사(사용자호출(5,файл,거리,Дії_корінь,0,0,0)); }
int вилучати_Файл_запис_ім_я(const char *шлях) { return 결과검사(사용자호출(11,(uintptr_t)шлях,0,0,0,0,0)); }
int 파일길이정하기(int файл,Файл_Зміщена_копія_Тип Розмір) { return 결과검사(사용자호출(10,файл,Розмір,0,0,0,0)); }
int затвердження_файлове_сховище(int файл) { return 결과검사(사용자호출(12,файл,0,0,0,0,0)); }
int розмір_файлу(int файл) { return 결과검사(사용자호출(9,файл,0,0,0,0,0)); }
