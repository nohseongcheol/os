#include <入出力と実行.h>
#include <文書制御.h>
#include <誤り番号.h>
#include <体系/文書状態.h>
int 関数集の動作を試す(void);

int main(void)
{
    char 資料緩衝領域[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int 文書記述番号 = 開く("/USER2", 読取専用で開く);
    struct 文書状態 状態資料;
    if (文書記述番号 < 0 || 開いた文書の状態を得る(文書記述番号, &状態資料) < 0 || 読む(文書記述番号, 資料緩衝領域, 4) != 4 ||
        (unsigned char)資料緩衝領域[0] != 0x7f || 資料緩衝領域[1] != 'E' || 資料緩衝領域[2] != 'L' || 資料緩衝領域[3] != 'F' ||
        読み書き位置を移す(文書記述番号, 0, 先頭基準位置) != 0 || 閉じる(文書記述番号) < 0 || 実行過程番号を得る() <= 0)
        goto 失敗判定;
    誤り番号 = 0;
    if (読む(-1, 資料緩衝領域, 1) != -1 || 誤り番号 != 誤り記述番号不正)
        goto 失敗判定;
    if (関数集の動作を試す() != 0)
        goto 失敗判定;
    if (書く(標準出力番号, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto 失敗判定;
    return 0;
失敗判定:
    書く(標準出力番号, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
