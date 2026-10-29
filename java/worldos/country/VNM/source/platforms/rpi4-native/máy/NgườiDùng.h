#ifndef đầuMụcNgườiDùngBảnĐịa
#define đầuMụcNgườiDùngBảnĐịa
#include <stdint.h>
#include <stddef.h>
#define cơSởNgườiDùng 0x02000000ul
#define kếtThúcẢnhNgườiDùng 0x02c00000ul
#define kếtThúcVùngNhớĐộngNgườiDùng 0x02ed0000ul
#define địaChỉNgănXếpNgườiDùng 0x02f00000ul
#define kếtThúcNgườiDùng 0x03000000ul
#define sốLượngTrangNgườiDùng ((kếtThúcNgườiDùng - cơSởNgườiDùng) / 4096ul)
#define lỗiTệpThựcThiNgườiDùng (-8)
#define lỗiDữLiệuNgườiDùng (-1001)
#define lỗiViệcThựcThiNgườiDùng (-1002)
#define chỉLệnhKhôngHợpLệNgườiDùng (-1003)
#define hếtGiờNgườiDùng (-1004)
#define đãBịNgắtNgườiDùng (-1005)
typedef struct { uint64_t thanhGhiDữLiệu[31], vịTríLệnh, mãTrạngThái, địaChỉNgănXếp; } khungNgườiDùng;
void khởiTạoGọnHệThốngNgườiDùng(void);
int ngoạiLệNgườiDùng(khungNgườiDùng *, unsigned);
int eLFThẩmĐịnhNgườiDùng(const unsigned char *, size_t);
uintptr_t chạyNgườiDùngBoMạch(uintptr_t);
uintptr_t thẩmĐịnhNgườiDùngBoMạch(void);
uintptr_t điềuKhiểnNgườiDùngBoMạch(uintptr_t);
uint32_t đọcTrạngTháiNgườiDùng(unsigned, unsigned);
#endif
