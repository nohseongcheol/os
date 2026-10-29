// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 终端输入输出 {
    static void 字符(int 值) {
        if (值 < 0x80) 板.写入串行(值);
        else if (值 < 0x800) {
            板.写入串行(0xc0 | (值 >> 6)); 板.写入串行(0x80 | (值 & 63));
        } else if (值 < 0x10000) {
            板.写入串行(0xe0 | (值 >> 12)); 板.写入串行(0x80 | ((值 >> 6) & 63)); 板.写入串行(0x80 | (值 & 63));
        } else {
            板.写入串行(0xf0 | (值 >> 18)); 板.写入串行(0x80 | ((值 >> 12) & 63));
            板.写入串行(0x80 | ((值 >> 6) & 63)); 板.写入串行(0x80 | (值 & 63));
        }
    }
    static void 写入(String 文本) {
        for (int 编号 = 0; 编号 < 文本.length(); 编号++) {
            int 值 = 文本.charAt(编号);
            if (值 >= 0xd800 && 值 <= 0xdbff && 编号 + 1 < 文本.length()) {
                int 底端值 = 文本.charAt(编号 + 1);
                if (底端值 >= 0xdc00 && 底端值 <= 0xdfff) {
                    值 = 0x10000 + ((值 - 0xd800) << 10) + 底端值 - 0xdc00; 编号++;
                }
            }
            if (值 >= 0xd800 && 值 <= 0xdfff) 值 = 0xfffd;
            字符(值);
        }
    }
    static void 数(int 值) {
        if (值 < 0) 字符('-'); else 值 = -值;
        int 位置索引 = 1000000000;
        boolean 运行 = false;
        while (位置索引 > 0) {
            int 数字值 = -(值 / 位置索引);
            if (数字值 != 0 || 运行 || 位置索引 == 1) { 字符('0' + 数字值); 运行 = true; }
            值 %= 位置索引; 位置索引 /= 10;
        }
    }
}
