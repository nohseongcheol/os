#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
#include "gọiThựcHiện.h"
typedef void (*phươngThứcBộKhởiTạo)(void);
extern phươngThứcBộKhởiTạo __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int bắtChạyChươngTrìnhNgườiDùng(int);
int bắtChạyNgườiDùng(int giáTrịĐãChuyểnTiếp) {
    for (phươngThứcBộKhởiTạo *vịTríDữLiệu = __init_array_start; vịTríDữLiệu < __init_array_end; vịTríDữLiệu++) (*vịTríDữLiệu)();
    int kếtQuả = bắtChạyChươngTrìnhNgườiDùng(giáTrịĐãChuyểnTiếp);
    for (phươngThứcBộKhởiTạo *vịTríDữLiệu = __fini_array_end; vịTríDữLiệu != __fini_array_start;) (*--vịTríDữLiệu)();
    return kếtQuả;
}
void *memset(void *vịTríDữLiệu, int giáTrị, size_t sốLượngMục) { unsigned char *dữLiệuĐích = vịTríDữLiệu; while (sốLượngMục--) *dữLiệuĐích++ = giáTrị; return vịTríDữLiệu; }
void *memcpy(void *dữLiệuĐích, const void *dữLiệuChuỗi, size_t sốLượngMục) { unsigned char *giáTrịĐầuTiên = dữLiệuĐích; const unsigned char *giáTrịThứHai = dữLiệuChuỗi; while (sốLượngMục--) *giáTrịĐầuTiên++ = *giáTrịThứHai++; return dữLiệuĐích; }
