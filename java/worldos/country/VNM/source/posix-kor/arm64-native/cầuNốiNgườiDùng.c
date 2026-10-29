// 동일 tiếngViệt 헤더를 사용하는 별도 EL0 thưViện. giáTrịNhân 직접 호출판과 혼합 giáTrịCấm.
#include "ABITệp.h"
#include "gọiThựcHiện.h"
#include "ABIMạng.h"
static int mãLỗi;
int *pk_errno_location(void) { return &mãLỗi; }
static intptr_t đãKiểmTra(intptr_t kếtQuả) { if (kếtQuả < 0) { mãLỗi = -kếtQuả; return -1; } return kếtQuả; }
int pk_open(const char *path, int flags, ...) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
kiểuKếtQuảVàoRa pk_read(int fd, void *p, size_t n) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
kiểuKếtQuảVàoRa pk_write(int fd, const void *p, size_t n) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(4, fd, 0, 0, 0, 0, 0)); }
kiểuĐộLệchTệp pk_lseek(int fd, kiểuĐộLệchTệp offset, int origin) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, kiểuĐộLệchTệp size) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(10, fd, size, 0, 0, 0, 0)); }
int pk_fsync(int fd) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(12, fd, 0, 0, 0, 0, 0)); }
int pk_size(int fd) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(9, fd, 0, 0, 0, 0, 0)); }
int pk_socket(int domain, int type, int protocol) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(32, domain, type, protocol, 0, 0, 0)); }
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length) {
    return đãKiểmTra(gọiThựcHiệnNgườiDùng(33, fd, (uintptr_t)address, length, 0, 0, 0));
}
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length) {
    return đãKiểmTra(gọiThựcHiệnNgườiDùng(34, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, length));
}
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length) {
    return đãKiểmTra(gọiThựcHiệnNgườiDùng(35, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, (uintptr_t)length));
}
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length) {
    return đãKiểmTra(gọiThựcHiệnNgườiDùng(36, fd, (uintptr_t)address, (uintptr_t)length, 0, 0, 0));
}
int pk_connect(int fd,const struct pk_sockaddr *address,pk_socklen_t length){return đãKiểmTra(gọiThựcHiệnNgườiDùng(37,fd,(uintptr_t)address,length,0,0,0));}
int pk_listen(int fd,int backlog){return đãKiểmTra(gọiThựcHiệnNgườiDùng(38,fd,backlog,0,0,0,0));}
int pk_accept(int fd,struct pk_sockaddr *address,pk_socklen_t *length){return đãKiểmTra(gọiThựcHiệnNgườiDùng(39,fd,(uintptr_t)address,(uintptr_t)length,0,0,0));}

/* tiếngViệt 공개 함수의 dữLiệuThựcTế EL0 phầnCàiĐặt. 구조체는 SVC에서 saoChépGiáTrị·검증한다. */
int tạoĐiểmCuối(int họĐịaChỉ,int chếĐộTruyềnThông,int giaoThứcChuyểnGiao) {
    return đãKiểmTra(gọiThựcHiệnNgườiDùng(32,họĐịaChỉ,chếĐộTruyềnThông,giaoThứcChuyểnGiao,0,0,0));
}
int ràngBuộcĐịaChỉ(int điểmCuối,const struct ĐịaChỉỔCắmMạng *địaChỉ,kiểuĐộDàiĐịaChỉỔCắmMạng độDài) {
    return đãKiểmTra(gọiThựcHiệnNgườiDùng(33,điểmCuối,(uintptr_t)địaChỉ,độDài,0,0,0));
}
intptr_t gửiDữLiệuĐiệnDữLiệu(int điểmCuối,const void *DữLiệu,size_t sốLượngPhầnMục,int giáTrịViệcChọn,const struct ĐịaChỉỔCắmMạng *địaChỉ,kiểuĐộDàiĐịaChỉỔCắmMạng độDài) {
    return đãKiểmTra(gọiThựcHiệnNgườiDùng(34,điểmCuối,(uintptr_t)DữLiệu,sốLượngPhầnMục,giáTrịViệcChọn,(uintptr_t)địaChỉ,độDài));
}
intptr_t nhậnDữLiệuĐiệnDữLiệu(int điểmCuối,void *DữLiệu,size_t sốLượngPhầnMục,int giáTrịViệcChọn,struct ĐịaChỉỔCắmMạng *địaChỉ,kiểuĐộDàiĐịaChỉỔCắmMạng *độDài) {
    return đãKiểmTra(gọiThựcHiệnNgườiDùng(35,điểmCuối,(uintptr_t)DữLiệu,sốLượngPhầnMục,giáTrịViệcChọn,(uintptr_t)địaChỉ,(uintptr_t)độDài));
}
int đọcĐịaChỉỔCắmMạng(int điểmCuối,struct ĐịaChỉỔCắmMạng *địaChỉ,kiểuĐộDàiĐịaChỉỔCắmMạng *độDài) {
    return đãKiểmTra(gọiThựcHiệnNgườiDùng(36,điểmCuối,(uintptr_t)địaChỉ,(uintptr_t)độDài,0,0,0));
}
int kếtNốiMạng(int điểmCuối,const struct ĐịaChỉỔCắmMạng *địaChỉ,kiểuĐộDàiĐịaChỉỔCắmMạng độDài) {
    return đãKiểmTra(gọiThựcHiệnNgườiDùng(37,điểmCuối,(uintptr_t)địaChỉ,độDài,0,0,0));
}
int chờKếtNốiMạngCho(int điểmCuối,int sốLượngĐangĐợi) {
    return đãKiểmTra(gọiThựcHiệnNgườiDùng(38,điểmCuối,sốLượngĐangĐợi,0,0,0,0));
}
int chấpNhậnKếtNốiMạng(int điểmCuối,struct ĐịaChỉỔCắmMạng *địaChỉ,kiểuĐộDàiĐịaChỉỔCắmMạng *độDài) {
    return đãKiểmTra(gọiThựcHiệnNgườiDùng(39,điểmCuối,(uintptr_t)địaChỉ,(uintptr_t)độDài,0,0,0));
}

/* Tệp 함수도 독립된 tiếngViệt Hàm 심볼로 제공한다. */
int mởTệp(const char *đườngDẫn,int chếĐộPhươngThức,...) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(3,(uintptr_t)đườngDẫn,chếĐộPhươngThức,0,0,0,0)); }
kiểuKếtQuảVàoRa đọcDữLiệuTệp(int Tệp,void *DữLiệu,size_t sốLượngPhầnMục) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(2,Tệp,(uintptr_t)DữLiệu,sốLượngPhầnMục,0,0,0)); }
kiểuKếtQuảVàoRa ghiDữLiệuTệp(int Tệp,const void *DữLiệu,size_t sốLượngPhầnMục) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(1,Tệp,(uintptr_t)DữLiệu,sốLượngPhầnMục,0,0,0)); }
int đóngTệp(int Tệp) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(4,Tệp,0,0,0,0,0)); }
kiểuĐộLệchTệp dịchVịTệp(int Tệp,kiểuĐộLệchTệp giáTrịKhoảngCách,int gốcCâyDựÁn) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(5,Tệp,giáTrịKhoảngCách,gốcCâyDựÁn,0,0,0)); }
int gỡTênMụcTệp(const char *đườngDẫn) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(11,(uintptr_t)đườngDẫn,0,0,0,0,0)); }
int đặtGiáTrịĐộDàiTệp(int Tệp,kiểuĐộLệchTệp cỡ) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(10,Tệp,cỡ,0,0,0,0)); }
int lưuTrữTệpChốt(int Tệp) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(12,Tệp,0,0,0,0,0)); }
int cỡTệp(int Tệp) { return đãKiểmTra(gọiThựcHiệnNgườiDùng(9,Tệp,0,0,0,0,0)); }
