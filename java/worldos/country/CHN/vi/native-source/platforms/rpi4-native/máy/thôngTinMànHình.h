#ifndef đầuMụcThôngTinMànHìnhBảnĐịa
#define đầuMụcThôngTinMànHìnhBảnĐịa
#include <stdint.h>
/* 초기화가 끝난 dữLiệuThựcTế RGB32 MànHình cỡ. 준비되지 않았으면 0이다. */
uintptr_t rộngMànHìnhBoMạch(void);
uintptr_t caoMànHìnhBoMạch(void);
/* 0: giáTrịẨn, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void conTrỏBoMạch(int vịTríNgang, int vịTríDọc, unsigned giáTrịHình);
/* 한 번에 32줄을 완성한 giáTrịLùi, 달라진 화소만 dữLiệuThựcTế 화면에 옮긴다. */
void bảnVẽChuẩnBịBoMạch(volatile uint32_t *DữLiệu, unsigned khoảngTrảiRộng, unsigned độDài, unsigned giáTrịGiãnCáchDòng);
int cácCậnBảnVẽBoMạch(int *vịTríNgang, int *vịTríDọc, int *khoảngTrảiRộng, int *độDài);
int bảnVẽBắtChạyBoMạch(int vịTríNgang, int vịTríDọc, int khoảngTrảiRộng, int độDài);
void bảnVẽHoànThànhBoMạch(void);
void lấpHìnhChữNhậtBoMạch(int vịTríNgang, int vịTríDọc, int khoảngTrảiRộng, int độDài, uint32_t giáTrịMàu);
/* dữLiệuThựcTế hiệnGiáTrị 메모리에 기록한 điểmẢnh trịSố. conTrỏ 갱신은 제외한다. */
uint64_t sốLượngBảnVẽBoMạch(void);
uint32_t mànHìnhĐọcBoMạch(unsigned vịTríNgang, unsigned vịTríDọc);
#endif
