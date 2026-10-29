// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 ተርጉም_ምንጭ 집합 1 폴링 입력. ነባሪ_እሴት 미국식 자판, Shift, Backspace, Enter. */
public final class የቁልፍ_ሰሌዳ {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean ቅጥያ_እሴት = false;
    static String ነባሪ_እሴት = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int ማንበቢያ() {
        int ዞን_እሴት = መሳሪያ_እሴት.입출력바이트읽기(0x64);
        if ((ዞን_እሴት & 1) == 0) return -1;
        int እሴት = መሳሪያ_እሴት.입출력바이트읽기(0x60);
        if ((ዞን_እሴት & 0x20) != 0) return -1;
        if (እሴት == 0xe0 || እሴት == 0xe1) { ቅጥያ_እሴት = true; return -1; }
        if (ቅጥያ_እሴት) { ቅጥያ_እሴት = false; return -1; }
        if (እሴት == 42 || እሴት == 170) { 왼올림 = እሴት == 42; return -1; }
        if (እሴት == 54 || እሴት == 182) { 오른올림 = እሴት == 54; return -1; }
        if (እሴት >= ነባሪ_እሴት.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(እሴት) : ነባሪ_እሴት.charAt(እሴት);
        return 문자 == 0 ? -1 : 문자;
    }
}
