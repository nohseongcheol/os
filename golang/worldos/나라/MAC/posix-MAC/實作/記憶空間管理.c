#include <通用函式.h>
#include <字串與記憶內容.h>
#include <輸入輸出與執行.h>
#include <整數型別.h>
#include <整數極限.h>
#include <錯誤編號.h>

/* Single-thread runtime. Reuse and coalesce freed blocks; do not shrink brk.
 * A block header and every returned address are 16-byte aligned on i386.
 * Callers must not move brk backwards across live allocations. */
struct 記憶區塊 {
    大小型別 容量;
    struct 記憶區塊 *下一區塊;
    int 可用旗標;
    unsigned int 對齊填補長度;
};
static struct 記憶區塊 *首個區塊;

void *配置記憶空間(大小型別 大小)
{
    struct 記憶區塊 *目前位置 = 首個區塊, *最後區塊 = 空位址, *配置原位址;
    大小型別 總長度, 對齊填補長度;
    void *位址;
    if (!大小) 大小 = 1;
    if (大小 > (大小型別)整數最大值 - 2 * sizeof(struct 記憶區塊)) { 錯誤編號 = 錯誤記憶體不足; return 空位址; }
    大小 = (大小 + 15U) & ~15U;
    while (目前位置) {
        if (目前位置->可用旗標 && 目前位置->容量 >= 大小) {
            if (目前位置->容量 - 大小 >= sizeof(struct 記憶區塊) + 16U) {
                配置原位址 = (struct 記憶區塊 *)((unsigned char *)(目前位置 + 1) + 大小);
                配置原位址->容量 = 目前位置->容量 - 大小 - sizeof(*配置原位址);
                配置原位址->下一區塊 = 目前位置->下一區塊;
                配置原位址->可用旗標 = 1;
                目前位置->下一區塊 = 配置原位址;
                目前位置->容量 = 大小;
            }
            目前位置->可用旗標 = 0;
            return 目前位置 + 1;
        }
        最後區塊 = 目前位置; 目前位置 = 目前位置->下一區塊;
    }
    位址 = 移動動態記憶末端(0);
    if (位址 == (void *)-1) return 空位址;
    對齊填補長度 = (0U - (位址寬度無號整數)位址) & 15U;
    總長度 = 對齊填補長度 + sizeof(struct 記憶區塊) + 大小;
    if ((位址寬度無號整數)位址 > (位址寬度無號整數)整數最大值 - 總長度) { 錯誤編號 = 錯誤記憶體不足; return 空位址; }
    位址 = 移動動態記憶末端((int)總長度);
    if (位址 == (void *)-1) return 空位址;
    配置原位址 = (struct 記憶區塊 *)((unsigned char *)位址 + 對齊填補長度);
    配置原位址->容量 = 大小; 配置原位址->下一區塊 = 空位址; 配置原位址->可用旗標 = 0;
    if (最後區塊) 最後區塊->下一區塊 = 配置原位址;
    else 首個區塊 = 配置原位址;
    return 配置原位址 + 1;
}

void 釋放記憶空間(void *位址)
{
    struct 記憶區塊 *目前位置;
    if (!位址) return;
    ((struct 記憶區塊 *)位址 - 1)->可用旗標 = 1;
    目前位置 = 首個區塊;
    while (目前位置 && 目前位置->下一區塊) {
        struct 記憶區塊 *下一區塊 = 目前位置->下一區塊;
        if (目前位置->可用旗標 && 下一區塊->可用旗標 &&
            (unsigned char *)(目前位置 + 1) + 目前位置->容量 == (unsigned char *)下一區塊) {
            目前位置->容量 += sizeof(*下一區塊) + 下一區塊->容量;
            目前位置->下一區塊 = 下一區塊->下一區塊;
        } else 目前位置 = 下一區塊;
    }
}

void *配置清零陣列空間(大小型別 數量, 大小型別 元素大小)
{
    void *位址;
    if (元素大小 && 數量 > (大小型別)-1 / 元素大小) { 錯誤編號 = 錯誤記憶體不足; return 空位址; }
    位址 = 配置記憶空間(數量 * 元素大小);
    if (位址) 以值填滿記憶區域(位址, 0, 數量 * 元素大小);
    return 位址;
}

void *調整記憶空間大小(void *位址, 大小型別 大小)
{
    void *目標位置;
    struct 記憶區塊 *目前位置;
    if (!位址) return 配置記憶空間(大小);
    /* Documented zero-size choice: retain a valid, freeable minimum block. */
    if (!大小) 大小 = 1;
    目前位置 = (struct 記憶區塊 *)位址 - 1;
    if (大小 <= 目前位置->容量) return 位址;
    目標位置 = 配置記憶空間(大小);
    if (!目標位置) return 空位址;
    複製記憶內容(目標位置, 位址, 目前位置->容量);
    釋放記憶空間(位址);
    return 目標位置;
}
