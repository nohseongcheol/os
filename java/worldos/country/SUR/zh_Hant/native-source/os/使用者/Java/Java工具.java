// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 客體工具共用的輸出與 ASCII 檔名處理。 */
public final class Java工具 {
    /** 在同一陣列內將 UTF-8 位元組轉成 UTF-16 單元，拒絕格式錯誤的輸入。 */
    static int 解碼原始碼(int[] 資料, int 長度) {
        int 讀取 = 0, 寫入 = 0;
        if (長度 >= 3 && 資料[0] == 239 && 資料[1] == 187 && 資料[2] == 191) 讀取 = 3;
        while (讀取 < 長度) {
            int 值 = 資料[讀取++], 數 = 0, 最小值 = 0;
            if (值 >= 194 && 值 <= 223) { 數 = 1; 最小值 = 128; 值 &= 31; }
            else if (值 >= 224 && 值 <= 239) { 數 = 2; 最小值 = 2048; 值 &= 15; }
            else if (值 >= 240 && 值 <= 244) { 數 = 3; 最小值 = 65536; 值 &= 7; }
            else if (值 >= 128 || 值 < 0) return -1;
            if (數 > 長度 - 讀取) return -1;
            for (int i = 0; i < 數; i++) {
                int 下一項目 = 資料[讀取++]; if ((下一項目 & 192) != 128) return -1;
                值 = (值 << 6) | (下一項目 & 63);
            }
            if (值 < 最小值 || 值 > 0x10ffff || (值 >= 0xd800 && 值 <= 0xdfff)) return -1;
            if (值 >= 65536) { 值 -= 65536; 資料[寫入++] = 0xd800 | (值 >> 10); 資料[寫入++] = 0xdc00 | (值 & 1023); }
            else 資料[寫入++] = 值;
        }
        return 寫入;
    }
    static void 寫入編號(int 值) {
        if (值 < 0) 使用者.寫入字元值('-'); else 值 = -值;
        int 位置索引 = 1000000000;
        boolean 運行 = false;
        while (位置索引 != 0) {
            int 數 = -(值 / 位置索引);
            if (數 != 0 || 運行 || 位置索引 == 1) { 使用者.寫入字元值('0' + 數); 運行 = true; }
            值 %= 位置索引; 位置索引 /= 10;
        }
    }
    static int 名稱(int[] 目的地址值, String 原始) {
        if (原始.length() >= 目的地址值.length) return -1;
        for (int 數 = 0; 數 < 目的地址值.length; 數++) 目的地址值[數] = 數 < 原始.length() ? 原始.charAt(數) : 0;
        return 原始.length();
    }
    static boolean 相等文本(String 首位操作數, String 第二操作數) {
        if (首位操作數.length() != 第二操作數.length()) return false;
        for (int 數 = 0; 數 < 首位操作數.length(); 數++) if (首位操作數.charAt(數) != 第二操作數.charAt(數)) return false;
        return true;
    }
}
