// 동일 한국어 헤더를 사용하는 별도 EL0 បណ្ណាល័យ. ខឺណេល_តំលៃ 직접 호출판과 혼합 금지.
#include "파일규약.h"
#include "호출.h"
#include "통신규약.h"
static int កំហុសកូដ;
int *pk_errno_location(void) { return &កំហុសកូដ; }
static intptr_t 결과검사(intptr_t ការវាស់វែង) { if (ការវាស់វែង < 0) { កំហុសកូដ = -ការវាស់វែង; return -1; } return ការវាស់វែង; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
ឯកសារ_ការបែង_ភាគ_វាយបញ្ចូល pk_lseek(int fd, ឯកសារ_ការបែង_ភាគ_វាយបញ្ចូល offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ឯកសារ_ការបែង_ភាគ_វាយបញ្ចូល size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* 한국어 공개 함수의 ដែលពិត_ទិន្នន័យ EL0 구현. 구조체는 SVC에서 ចំលង_តំលៃ·검증한다. */
int 통신종단점만들기(int អ៊ីម៉ែល_គ្រួសារ,int 통신방식,int ផ្ទេរ_ប្រូតូកូល) {
    return 결과검사(사용자호출(32,អ៊ីម៉ែល_គ្រួសារ,통신방식,ផ្ទេរ_ប្រូតូកូល,0,0,0));
}
int ចង_អ៊ីម៉ែល(int 종단,const struct 통신주소 *អ៊ីម៉ែល,통신주소길이형 ប្រវែង_តំលៃ) {
    return 결과검사(사용자호출(33,종단,(uintptr_t)អ៊ីម៉ែល,ប្រវែង_តំលៃ,0,0,0));
}
intptr_t 자료전문보내기(int 종단,const void *ទិន្នន័យ,size_t 개수,int ការជ្រើស_តំលៃ,const struct 통신주소 *អ៊ីម៉ែល,통신주소길이형 ប្រវែង_តំលៃ) {
    return 결과검사(사용자호출(34,종단,(uintptr_t)ទិន្នន័យ,개수,ការជ្រើស_តំលៃ,(uintptr_t)អ៊ីម៉ែល,ប្រវែង_តំលៃ));
}
intptr_t 자료전문받기(int 종단,void *ទិន្នន័យ,size_t 개수,int ការជ្រើស_តំលៃ,struct 통신주소 *អ៊ីម៉ែល,통신주소길이형 *ប្រវែង_តំលៃ) {
    return 결과검사(사용자호출(35,종단,(uintptr_t)ទិន្នន័យ,개수,ការជ្រើស_តំលៃ,(uintptr_t)អ៊ីម៉ែល,(uintptr_t)ប្រវែង_តំលៃ));
}
int 통신주소읽기(int 종단,struct 통신주소 *អ៊ីម៉ែល,통신주소길이형 *ប្រវែង_តំលៃ) {
    return 결과검사(사용자호출(36,종단,(uintptr_t)អ៊ីម៉ែល,(uintptr_t)ប្រវែង_តំលៃ,0,0,0));
}
int ភ្ជាប់_ណិតវឺក(int 종단,const struct 통신주소 *អ៊ីម៉ែល,통신주소길이형 ប្រវែង_តំលៃ) {
    return 결과검사(사용자호출(37,종단,(uintptr_t)អ៊ីម៉ែល,ប្រវែង_តំលៃ,0,0,0));
}
int 통신연결기다리기(int 종단,int 대기수) {
    return 결과검사(사용자호출(38,종단,대기수,0,0,0,0));
}
int ទទួល_យក_ភ្ជាប់_បណ្ដាញ(int 종단,struct 통신주소 *អ៊ីម៉ែល,통신주소길이형 *ប្រវែង_តំលៃ) {
    return 결과검사(사용자호출(39,종단,(uintptr_t)អ៊ីម៉ែល,(uintptr_t)ប្រវែង_តំលៃ,0,0,0));
}

/* ឯកសារ 함수도 독립된 한국어 អនុគមន៍_តំលៃ 심볼로 제공한다. */
int បើក_ឯកសារ(const char *ផ្លូវ,int វិធីសាស្រ្ត_ម៉ូដ,...) { return 결과검사(사용자호출(3,(uintptr_t)ផ្លូវ,វិធីសាស្រ្ត_ម៉ូដ,0,0,0,0)); }
입출력결과형 파일자료읽기(int ឯកសារ,void *ទិន្នន័យ,size_t 개수) { return 결과검사(사용자호출(2,ឯកសារ,(uintptr_t)ទិន្នន័យ,개수,0,0,0)); }
입출력결과형 សរសេរ_ឯកសារ_ទិន្នន័យ(int ឯកសារ,const void *ទិន្នន័យ,size_t 개수) { return 결과검사(사용자호출(1,ឯកសារ,(uintptr_t)ទិន្នន័យ,개수,0,0,0)); }
int បិទ_ឯកសារ(int ឯកសារ) { return 결과검사(사용자호출(4,ឯកសារ,0,0,0,0,0)); }
ឯកសារ_ការបែង_ភាគ_វាយបញ្ចូល ស្វែងរក_ឯកសារ(int ឯកសារ,ឯកសារ_ការបែង_ភាគ_វាយបញ្ចូល 거리,int បញ្ចាំង_ឬស) { return 결과검사(사용자호출(5,ឯកសារ,거리,បញ្ចាំង_ឬស,0,0,0)); }
int យកចេញ_ឯកសារ_ការបញ្ចូល_ឈ្មោះ(const char *ផ្លូវ) { return 결과검사(사용자호출(11,(uintptr_t)ផ្លូវ,0,0,0,0,0)); }
int កំណត់_ឯកសារ_ប្រវែង(int ឯកសារ,ឯកសារ_ការបែង_ភាគ_វាយបញ្ចូល ដាក់ទំហំ) { return 결과검사(사용자호출(10,ឯកសារ,ដាក់ទំហំ,0,0,0,0)); }
int 파일저장확정(int ឯកសារ) { return 결과검사(사용자호출(12,ឯកសារ,0,0,0,0,0)); }
int ឯកសារ_ដាក់ទំហំ(int ឯកសារ) { return 결과검사(사용자호출(9,ឯកសារ,0,0,0,0,0)); }
