// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 終端輸入輸出 {
    static void 字元(int 值) {
        if (值 < 0x80) 板.寫入串行(值);
        else if (值 < 0x800) {
            板.寫入串行(0xc0 | (值 >> 6)); 板.寫入串行(0x80 | (值 & 63));
        } else if (值 < 0x10000) {
            板.寫入串行(0xe0 | (值 >> 12)); 板.寫入串行(0x80 | ((值 >> 6) & 63)); 板.寫入串行(0x80 | (值 & 63));
        } else {
            板.寫入串行(0xf0 | (值 >> 18)); 板.寫入串行(0x80 | ((值 >> 12) & 63));
            板.寫入串行(0x80 | ((值 >> 6) & 63)); 板.寫入串行(0x80 | (值 & 63));
        }
    }
    static void 寫入(String 文本) {
        for (int 編號 = 0; 編號 < 文本.length(); 編號++) {
            int 值 = 文本.charAt(編號);
            if (值 >= 0xd800 && 值 <= 0xdbff && 編號 + 1 < 文本.length()) {
                int 底端值 = 文本.charAt(編號 + 1);
                if (底端值 >= 0xdc00 && 底端值 <= 0xdfff) {
                    值 = 0x10000 + ((值 - 0xd800) << 10) + 底端值 - 0xdc00; 編號++;
                }
            }
            if (值 >= 0xd800 && 值 <= 0xdfff) 值 = 0xfffd;
            字元(值);
        }
    }
    static void 數(int 值) {
        if (值 < 0) 字元('-'); else 值 = -值;
        int 位置索引 = 1000000000;
        boolean 運行 = false;
        while (位置索引 > 0) {
            int 數字值 = -(值 / 位置索引);
            if (數字值 != 0 || 運行 || 位置索引 == 1) { 字元('0' + 數字值); 運行 = true; }
            值 %= 位置索引; 位置索引 /= 10;
        }
    }
}
