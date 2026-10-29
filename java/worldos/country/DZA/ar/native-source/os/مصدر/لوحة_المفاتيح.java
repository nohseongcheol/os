// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 تحويل_مصدر 집합 1 폴링 إدخال_قيمة. قيمة_افتراضية 미국식 자판, Shift, Backspace, Enter. */
public final class لوحة_المفاتيح {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean ملحق_قيمة = false;
    static String قيمة_افتراضية = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int قراءة() {
        int حالة_قيمة = جهاز_قيمة.입출력바이트읽기(0x64);
        if ((حالة_قيمة & 1) == 0) return -1;
        int قيمة = جهاز_قيمة.입출력바이트읽기(0x60);
        if ((حالة_قيمة & 0x20) != 0) return -1;
        if (قيمة == 0xe0 || قيمة == 0xe1) { ملحق_قيمة = true; return -1; }
        if (ملحق_قيمة) { ملحق_قيمة = false; return -1; }
        if (قيمة == 42 || قيمة == 170) { 왼올림 = قيمة == 42; return -1; }
        if (قيمة == 54 || قيمة == 182) { 오른올림 = قيمة == 54; return -1; }
        if (قيمة >= قيمة_افتراضية.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(قيمة) : قيمة_افتراضية.charAt(قيمة);
        return 문자 == 0 ? -1 : 문자;
    }
}
