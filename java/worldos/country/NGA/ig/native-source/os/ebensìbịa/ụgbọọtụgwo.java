// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Tụgharia_ebensìbịa 집합 1 폴링 입력. Ngwa_ihe_dịadị 미국식 자판, Shift, Backspace, Enter. */
public final class ụgbọọtụgwo {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean mgbatị_valuu = false;
    static String Ngwa_ihe_dịadị = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Wepụta_ọzi() {
        int ọnọdụ_valuu = njìarụ_valuu.입출력바이트읽기(0x64);
        if ((ọnọdụ_valuu & 1) == 0) return -1;
        int valuu = njìarụ_valuu.입출력바이트읽기(0x60);
        if ((ọnọdụ_valuu & 0x20) != 0) return -1;
        if (valuu == 0xe0 || valuu == 0xe1) { mgbatị_valuu = true; return -1; }
        if (mgbatị_valuu) { mgbatị_valuu = false; return -1; }
        if (valuu == 42 || valuu == 170) { 왼올림 = valuu == 42; return -1; }
        if (valuu == 54 || valuu == 182) { 오른올림 = valuu == 54; return -1; }
        if (valuu >= Ngwa_ihe_dịadị.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(valuu) : Ngwa_ihe_dịadị.charAt(valuu);
        return 문자 == 0 ? -1 : 문자;
    }
}
