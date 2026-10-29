// 동일 русский 헤더를 사용하는 별도 EL0 библиотека. ядро_ЗНАЧЕН 직접 호출판과 혼합 금지.
#include "файл_ABI.h"
#include "호출.h"
#include "сеть_ABI.h"
static int код_ошибки;
int *pk_errno_location(void) { return &код_ошибки; }
static intptr_t 결과검사(intptr_t результат) { if (результат < 0) { код_ошибки = -результат; return -1; } return результат; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
файл_СМЕЩ_ТИП pk_lseek(int fd, файл_СМЕЩ_ТИП offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, файл_СМЕЩ_ТИП size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* русский 공개 함수의 фактический_данные EL0 реализация. 구조체는 SVC에서 экземпляр_ЗНАЧЕН·검증한다. */
int Create_участник(int АДРЕС_Семья,int коммуникация_МОДА,int передать_протокол) {
    return 결과검사(사용자호출(32,АДРЕС_Семья,коммуникация_МОДА,передать_протокол,0,0,0));
}
int BIND_АДРЕС(int участник,const struct сокет_АДРЕС *АДРЕС,сокет_АДРЕС_длина_ТИП длина_ЗНАЧЕН) {
    return 결과검사(사용자호출(33,участник,(uintptr_t)АДРЕС,длина_ЗНАЧЕН,0,0,0));
}
intptr_t написать_датаграмма_данные(int участник,const void *данные,size_t товар_СЧЁТ,int выделение_ЗНАЧЕН,const struct сокет_АДРЕС *АДРЕС,сокет_АДРЕС_длина_ТИП длина_ЗНАЧЕН) {
    return 결과검사(사용자호출(34,участник,(uintptr_t)данные,товар_СЧЁТ,выделение_ЗНАЧЕН,(uintptr_t)АДРЕС,длина_ЗНАЧЕН));
}
intptr_t получить_датаграмма_данные(int участник,void *данные,size_t товар_СЧЁТ,int выделение_ЗНАЧЕН,struct сокет_АДРЕС *АДРЕС,сокет_АДРЕС_длина_ТИП *длина_ЗНАЧЕН) {
    return 결과검사(사용자호출(35,участник,(uintptr_t)данные,товар_СЧЁТ,выделение_ЗНАЧЕН,(uintptr_t)АДРЕС,(uintptr_t)длина_ЗНАЧЕН));
}
int чтение_сокет_АДРЕС(int участник,struct сокет_АДРЕС *АДРЕС,сокет_АДРЕС_длина_ТИП *длина_ЗНАЧЕН) {
    return 결과검사(사용자호출(36,участник,(uintptr_t)АДРЕС,(uintptr_t)длина_ЗНАЧЕН,0,0,0));
}
int Connect_сеть(int участник,const struct сокет_АДРЕС *АДРЕС,сокет_АДРЕС_длина_ТИП длина_ЗНАЧЕН) {
    return 결과검사(사용자호출(37,участник,(uintptr_t)АДРЕС,длина_ЗНАЧЕН,0,0,0));
}
int 통신연결기다리기(int участник,int Заждался_СЧЁТ) {
    return 결과검사(사용자호출(38,участник,Заждался_СЧЁТ,0,0,0,0));
}
int принять_сетевое_подключение(int участник,struct сокет_АДРЕС *АДРЕС,сокет_АДРЕС_длина_ТИП *длина_ЗНАЧЕН) {
    return 결과검사(사용자호출(39,участник,(uintptr_t)АДРЕС,(uintptr_t)длина_ЗНАЧЕН,0,0,0));
}

/* файл 함수도 독립된 русский ФУНКЦИЯ_ЗНАЧЕН 심볼로 제공한다. */
int открыть_файл(const char *путь,int метод_МОДА,...) { return 결과검사(사용자호출(3,(uintptr_t)путь,метод_МОДА,0,0,0,0)); }
입출력결과형 чтение_файл_данные(int файл,void *данные,size_t товар_СЧЁТ) { return 결과검사(사용자호출(2,файл,(uintptr_t)данные,товар_СЧЁТ,0,0,0)); }
입출력결과형 запись_файл_данные(int файл,const void *данные,size_t товар_СЧЁТ) { return 결과검사(사용자호출(1,файл,(uintptr_t)данные,товар_СЧЁТ,0,0,0)); }
int Close_файл(int файл) { return 결과검사(사용자호출(4,файл,0,0,0,0,0)); }
файл_СМЕЩ_ТИП поиск_файл(int файл,файл_СМЕЩ_ТИП 거리,int задача_корень) { return 결과검사(사용자호출(5,файл,거리,задача_корень,0,0,0)); }
int удалить_файл_ввод_имя(const char *путь) { return 결과검사(사용자호출(11,(uintptr_t)путь,0,0,0,0,0)); }
int сет_файл_длина(int файл,файл_СМЕЩ_ТИП Размер) { return 결과검사(사용자호출(10,файл,Размер,0,0,0,0)); }
int фиксация_Файлы(int файл) { return 결과검사(사용자호출(12,файл,0,0,0,0,0)); }
int размер_файла(int файл) { return 결과검사(사용자호출(9,файл,0,0,0,0,0)); }
