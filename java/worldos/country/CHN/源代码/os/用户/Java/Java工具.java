// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 客户机工具共用的输出和 ASCII 文件名处理。 */
public final class Java工具 {
    /** 在同一数组内把 UTF-8 字节转换成 UTF-16 单元，拒绝格式错误的输入。 */
    static int 解码源代码(int[] 数据, int 长度) {
        int 读取 = 0, 写入 = 0;
        if (长度 >= 3 && 数据[0] == 239 && 数据[1] == 187 && 数据[2] == 191) 读取 = 3;
        while (读取 < 长度) {
            int 值 = 数据[读取++], 数 = 0, 最小值 = 0;
            if (值 >= 194 && 值 <= 223) { 数 = 1; 最小值 = 128; 值 &= 31; }
            else if (值 >= 224 && 值 <= 239) { 数 = 2; 最小值 = 2048; 值 &= 15; }
            else if (值 >= 240 && 值 <= 244) { 数 = 3; 最小值 = 65536; 值 &= 7; }
            else if (值 >= 128 || 值 < 0) return -1;
            if (数 > 长度 - 读取) return -1;
            for (int i = 0; i < 数; i++) {
                int 下一项目 = 数据[读取++]; if ((下一项目 & 192) != 128) return -1;
                值 = (值 << 6) | (下一项目 & 63);
            }
            if (值 < 最小值 || 值 > 0x10ffff || (值 >= 0xd800 && 值 <= 0xdfff)) return -1;
            if (值 >= 65536) { 值 -= 65536; 数据[写入++] = 0xd800 | (值 >> 10); 数据[写入++] = 0xdc00 | (值 & 1023); }
            else 数据[写入++] = 值;
        }
        return 写入;
    }
    static void 写入编号(int 值) {
        if (值 < 0) 用户.写入字符值('-'); else 值 = -值;
        int 位置索引 = 1000000000;
        boolean 运行 = false;
        while (位置索引 != 0) {
            int 数 = -(值 / 位置索引);
            if (数 != 0 || 运行 || 位置索引 == 1) { 用户.写入字符值('0' + 数); 运行 = true; }
            值 %= 位置索引; 位置索引 /= 10;
        }
    }
    static int 名称(int[] 目的地址值, String 原始) {
        if (原始.length() >= 目的地址值.length) return -1;
        for (int 数 = 0; 数 < 目的地址值.length; 数++) 目的地址值[数] = 数 < 原始.length() ? 原始.charAt(数) : 0;
        return 原始.length();
    }
    static boolean 相等文本(String 首位操作数, String 第二操作数) {
        if (首位操作数.length() != 第二操作数.length()) return false;
        for (int 数 = 0; 数 < 首位操作数.length(); 数++) if (首位操作数.charAt(数) != 第二操作数.charAt(数)) return false;
        return true;
    }
}
