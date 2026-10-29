// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 輪詢 PC/AT PS/2 轉換掃描碼集 1；支援基本美式鍵盤配置、Shift、Backspace 與 Enter。 */
public final class 鍵盤 {
    static boolean 移位左 = false;
    static boolean 移位右 = false;
    static boolean 擴展名值 = false;
    static String 默認值 = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 移位值 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 讀取() {
        int 狀態值 = 設備.讀取輸入輸出位元組(0x64);
        if ((狀態值 & 1) == 0) return -1;
        int 值 = 設備.讀取輸入輸出位元組(0x60);
        if ((狀態值 & 0x20) != 0) return -1;
        if (值 == 0xe0 || 值 == 0xe1) { 擴展名值 = true; return -1; }
        if (擴展名值) { 擴展名值 = false; return -1; }
        if (值 == 42 || 值 == 170) { 移位左 = 值 == 42; return -1; }
        if (值 == 54 || 值 == 182) { 移位右 = 值 == 54; return -1; }
        if (值 >= 默認值.length()) return -1;
        int 字元 = (移位左 || 移位右) ? 移位值.charAt(值) : 默認值.charAt(值);
        return 字元 == 0 ? -1 : 字元;
    }
}
