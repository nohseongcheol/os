// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 の変換済み集合1をポーリングで読む。基本米国配列、Shift、Backspace、Enter に対応する。 */
public final class キーボード {
    static boolean シフト左 = false;
    static boolean シフト右 = false;
    static boolean 拡張子値 = false;
    static String 既定値 = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String シフト値 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 読取() {
        int 状況値 = 装置.入出力バイト読取(0x64);
        if ((状況値 & 1) == 0) return -1;
        int 値 = 装置.入出力バイト読取(0x60);
        if ((状況値 & 0x20) != 0) return -1;
        if (値 == 0xe0 || 値 == 0xe1) { 拡張子値 = true; return -1; }
        if (拡張子値) { 拡張子値 = false; return -1; }
        if (値 == 42 || 値 == 170) { シフト左 = 値 == 42; return -1; }
        if (値 == 54 || 値 == 182) { シフト右 = 値 == 54; return -1; }
        if (値 >= 既定値.length()) return -1;
        int 文字 = (シフト左 || シフト右) ? シフト値.charAt(値) : 既定値.charAt(値);
        return 文字 == 0 ? -1 : 文字;
    }
}
