// 동일 Türkçe 헤더를 사용하는 별도 EL0 kitaplık. çekirdek_değer 직접 호출판과 혼합 금지.
#include "Dosya_ABI.h"
#include "호출.h"
#include "ağ_ABI.h"
static int hata_kodu;
int *pk_errno_location(void) { return &hata_kodu; }
static intptr_t 결과검사(intptr_t sonuç) { if (sonuç < 0) { hata_kodu = -sonuç; return -1; } return sonuç; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Dosya_Ofset_TÜR pk_lseek(int fd, Dosya_Ofset_TÜR offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Dosya_Ofset_TÜR size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
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

/* Türkçe 공개 함수의 fiili_veri EL0 gerçekleme. 구조체는 SVC에서 örnek_değer·검증한다. */
int açmak_uç_nokta(int ADRES_Aile,int iletişim_mod,int devir_protokol) {
    return 결과검사(사용자호출(32,ADRES_Aile,iletişim_mod,devir_protokol,0,0,0));
}
int BIND_ADRES(int uç_nokta,const struct yuva_ADRES *ADRES,yuva_ADRES_süre_TÜR süre_değer) {
    return 결과검사(사용자호출(33,uç_nokta,(uintptr_t)ADRES,süre_değer,0,0,0));
}
intptr_t göndermek_veri_birimi_veri(int uç_nokta,const void *veri,size_t öğe_BAĞ_DEĞ_SAY,int seçim_değer,const struct yuva_ADRES *ADRES,yuva_ADRES_süre_TÜR süre_değer) {
    return 결과검사(사용자호출(34,uç_nokta,(uintptr_t)veri,öğe_BAĞ_DEĞ_SAY,seçim_değer,(uintptr_t)ADRES,süre_değer));
}
intptr_t almak_veri_birimi_veri(int uç_nokta,void *veri,size_t öğe_BAĞ_DEĞ_SAY,int seçim_değer,struct yuva_ADRES *ADRES,yuva_ADRES_süre_TÜR *süre_değer) {
    return 결과검사(사용자호출(35,uç_nokta,(uintptr_t)veri,öğe_BAĞ_DEĞ_SAY,seçim_değer,(uintptr_t)ADRES,(uintptr_t)süre_değer));
}
int 통신주소읽기(int uç_nokta,struct yuva_ADRES *ADRES,yuva_ADRES_süre_TÜR *süre_değer) {
    return 결과검사(사용자호출(36,uç_nokta,(uintptr_t)ADRES,(uintptr_t)süre_değer,0,0,0));
}
int bağla_ağ(int uç_nokta,const struct yuva_ADRES *ADRES,yuva_ADRES_süre_TÜR süre_değer) {
    return 결과검사(사용자호출(37,uç_nokta,(uintptr_t)ADRES,süre_değer,0,0,0));
}
int 통신연결기다리기(int uç_nokta,int Bekliyor_BAĞ_DEĞ_SAY) {
    return 결과검사(사용자호출(38,uç_nokta,Bekliyor_BAĞ_DEĞ_SAY,0,0,0,0));
}
int kabul_etmek_ağ_bağlantısı(int uç_nokta,struct yuva_ADRES *ADRES,yuva_ADRES_süre_TÜR *süre_değer) {
    return 결과검사(사용자호출(39,uç_nokta,(uintptr_t)ADRES,(uintptr_t)süre_değer,0,0,0));
}

/* dosya 함수도 독립된 Türkçe işlev_değer 심볼로 제공한다. */
int açık_Dosya(const char *yol,int metot_mod,...) { return 결과검사(사용자호출(3,(uintptr_t)yol,metot_mod,0,0,0,0)); }
입출력결과형 파일자료읽기(int dosya,void *veri,size_t öğe_BAĞ_DEĞ_SAY) { return 결과검사(사용자호출(2,dosya,(uintptr_t)veri,öğe_BAĞ_DEĞ_SAY,0,0,0)); }
입출력결과형 yazma_Dosya_veri(int dosya,const void *veri,size_t öğe_BAĞ_DEĞ_SAY) { return 결과검사(사용자호출(1,dosya,(uintptr_t)veri,öğe_BAĞ_DEĞ_SAY,0,0,0)); }
int Kapat_Dosya(int dosya) { return 결과검사(사용자호출(4,dosya,0,0,0,0,0)); }
Dosya_Ofset_TÜR arama_Dosya(int dosya,Dosya_Ofset_TÜR 거리,int işlem_kök) { return 결과검사(사용자호출(5,dosya,거리,işlem_kök,0,0,0)); }
int kaldırmak_Dosya_girdi_ad(const char *yol) { return 결과검사(사용자호출(11,(uintptr_t)yol,0,0,0,0,0)); }
int küme_Dosya_süre(int dosya,Dosya_Ofset_TÜR Boyut) { return 결과검사(사용자호출(10,dosya,Boyut,0,0,0,0)); }
int commit_Dosyalar(int dosya) { return 결과검사(사용자호출(12,dosya,0,0,0,0,0)); }
int dosya_boyutu(int dosya) { return 결과검사(사용자호출(9,dosya,0,0,0,0,0)); }
