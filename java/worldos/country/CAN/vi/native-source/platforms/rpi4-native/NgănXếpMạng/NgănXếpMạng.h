#ifndef đầuMụcMạngBảnĐịa
#define đầuMụcMạngBảnĐịa
#include <stdint.h>
#include <stddef.h>
void chuẩnBịMạng(void);
void xemXétMạng(void);
int tạoĐiểmCuốiỔCắmMạng(int loạiMụcKiểu);
int ràngBuộcMạngGọn(int thẻXửLýTệp, uint32_t địaChỉ, unsigned sốCổng);
int lắngNgheMạngGọn(int thẻXửLýTệp);
void địaChỉỔCắmMạngDùngLại(int thẻXửLýTệp);
int kếtNốiMạngGọn(int thẻXửLýTệp, uint32_t địaChỉ, unsigned sốCổng);
int chấpNhậnMạngGọn(int thẻXửLýTệp);
int đọcMạngGọn(int thẻXửLýTệp, void *DữLiệu, unsigned sốLượngPhầnMục);
int ghiMạngGọn(int thẻXửLýTệp, const void *DữLiệu, unsigned sốLượngPhầnMục);
int gửiĐiệnDữLiệu(int thẻXửLýTệp, const void *DữLiệu, unsigned sốLượngPhầnMục, uint32_t địaChỉ, unsigned sốCổng);
int nhậnĐiệnDữLiệu(int thẻXửLýTệp, void *DữLiệu, unsigned sốLượngPhầnMục);
unsigned sốCổngMạng(int thẻXửLýTệp);
unsigned sốCổngĐốiTác(int thẻXửLýTệp);
uint32_t địaChỉĐốiTácMạngGọn(int thẻXửLýTệp);
void đóngMạng(int thẻXửLýTệp);
int điềuKhiểnChuyểnGiaoTệp(int hànhĐộng);
void xemXétChuyểnGiaoTệp(void);
uint32_t đọcTìnhTrạngMạng(unsigned giáTrịMục, unsigned sốHiệu);
int đặtCấuHìnhMạng(unsigned hànhĐộng, uint32_t địaChỉ, uint32_t giáTrịMặtNạ, uint32_t giáTrịCổngNối);
int bắtChạyThửPhảnHồi(uint32_t địaChỉ, unsigned giáTrịThứTự);
int đọcThửPhảnHồi(unsigned giáTrịMục);
#endif
