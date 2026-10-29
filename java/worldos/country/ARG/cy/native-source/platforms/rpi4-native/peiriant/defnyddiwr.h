#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define defnyddiwr_BASE 0x02000000ul
#define defnyddiwr_llun_gorffen 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define defnyddiwr_pentwr_ADDRESS 0x02f00000ul
#define defnyddiwr_gorffen 0x03000000ul
#define defnyddiwr_tudalen_COUNT ((defnyddiwr_gorffen - defnyddiwr_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define defnyddiwr_data_gwall (-1001)
#define 사용자실행오류 (-1002)
#define defnyddiwr_annilys_cyfarwyddyd (-1003)
#define defnyddiwr_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t cofrestru_data[31], gorchymyn_safle, cyflwr_cod, pentwr_ADDRESS; } defnyddiwr_ffrâm;
void 사용자체계준비(void);
int defnyddiwr_eithriad(defnyddiwr_ffrâm *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t bwrdd_defnyddiwr_rhedeg(uintptr_t);
uintptr_t bwrdd_defnyddiwr_dilysu(void);
uintptr_t bwrdd_rheolaeth_defnyddiwr(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
