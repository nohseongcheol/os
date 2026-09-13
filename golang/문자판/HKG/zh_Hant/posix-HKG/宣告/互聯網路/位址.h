#ifndef _宣告_互聯網路_位址
#define _宣告_互聯網路_位址

#include <整數型別.h>
#include <系統/通訊端點.h>

typedef 無號32位整數 互聯網路位址值型別;
typedef 無號16位整數 通訊埠編號型別;

struct 互聯網路位址 {
    互聯網路位址值型別 位址值;
};

struct 互聯網路端點位址 {
    位址族型別 互聯位址族;
    通訊埠編號型別 通訊埠編號;
    struct 互聯網路位址 互聯位址內容;
    unsigned char 位址填補區[8];
};

#define 互聯網路基本協定 0
#define 使用者資料報協定 17
#define 任意本機位址 ((互聯網路位址值型別)0x00000000U)
#define 本機迴送位址 ((互聯網路位址值型別)0x7f000001U)

#endif
