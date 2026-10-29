// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 轮询 PC/AT PS/2 转换扫描码集 1；支持基本美式键盘布局、Shift、Backspace 和 Enter。 */
public final class 键盘 {
    static boolean 移位左 = false;
    static boolean 移位右 = false;
    static boolean 扩展名值 = false;
    static String 默认值 = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 移位值 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 读取() {
        int 状态值 = 设备.读取输入输出字节(0x64);
        if ((状态值 & 1) == 0) return -1;
        int 值 = 设备.读取输入输出字节(0x60);
        if ((状态值 & 0x20) != 0) return -1;
        if (值 == 0xe0 || 值 == 0xe1) { 扩展名值 = true; return -1; }
        if (扩展名值) { 扩展名值 = false; return -1; }
        if (值 == 42 || 值 == 170) { 移位左 = 值 == 42; return -1; }
        if (值 == 54 || 值 == 182) { 移位右 = 值 == 54; return -1; }
        if (值 >= 默认值.length()) return -1;
        int 字符 = (移位左 || 移位右) ? 移位值.charAt(值) : 默认值.charAt(值);
        return 字符 == 0 ? -1 : 字符;
    }
}
