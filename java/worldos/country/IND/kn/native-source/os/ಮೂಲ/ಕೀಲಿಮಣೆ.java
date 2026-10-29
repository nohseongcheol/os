// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 ಅನುವಾದಿಸು_ಮೂಲ 집합 1 폴링 입력. ಅಕ್ಷಮ_ಬೆಲೆ 미국식 자판, Shift, Backspace, Enter. */
public final class ಕೀಲಿಮಣೆ {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean ವಿಸ್ತರಣೆ_ಮೌಲ್ಯ = false;
    static String ಅಕ್ಷಮ_ಬೆಲೆ = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int ಓದು() {
        int ಸ್ಥಿತಿ_ಮೌಲ್ಯ = ಸಾಧನ_ಮೌಲ್ಯ.입출력바이트읽기(0x64);
        if ((ಸ್ಥಿತಿ_ಮೌಲ್ಯ & 1) == 0) return -1;
        int ಮೌಲ್ಯ = ಸಾಧನ_ಮೌಲ್ಯ.입출력바이트읽기(0x60);
        if ((ಸ್ಥಿತಿ_ಮೌಲ್ಯ & 0x20) != 0) return -1;
        if (ಮೌಲ್ಯ == 0xe0 || ಮೌಲ್ಯ == 0xe1) { ವಿಸ್ತರಣೆ_ಮೌಲ್ಯ = true; return -1; }
        if (ವಿಸ್ತರಣೆ_ಮೌಲ್ಯ) { ವಿಸ್ತರಣೆ_ಮೌಲ್ಯ = false; return -1; }
        if (ಮೌಲ್ಯ == 42 || ಮೌಲ್ಯ == 170) { 왼올림 = ಮೌಲ್ಯ == 42; return -1; }
        if (ಮೌಲ್ಯ == 54 || ಮೌಲ್ಯ == 182) { 오른올림 = ಮೌಲ್ಯ == 54; return -1; }
        if (ಮೌಲ್ಯ >= ಅಕ್ಷಮ_ಬೆಲೆ.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(ಮೌಲ್ಯ) : ಅಕ್ಷಮ_ಬೆಲೆ.charAt(ಮೌಲ್ಯ);
        return 문자 == 0 ? -1 : 문자;
    }
}
