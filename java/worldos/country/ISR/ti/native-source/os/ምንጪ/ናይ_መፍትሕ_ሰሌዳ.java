// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 ተርጉም_ምንጪ 집합 1 폴링 입력. ንቡር_ዋጋ 미국식 자판, Shift, Backspace, Enter. */
public final class ናይ_መፍትሕ_ሰሌዳ {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean ቅጥያ_ዋጋ = false;
    static String ንቡር_ዋጋ = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 읽기() {
        int ደረጃ_ዋጋ = መሳርሒ_ዋጋ.입출력바이트읽기(0x64);
        if ((ደረጃ_ዋጋ & 1) == 0) return -1;
        int ዋጋ = መሳርሒ_ዋጋ.입출력바이트읽기(0x60);
        if ((ደረጃ_ዋጋ & 0x20) != 0) return -1;
        if (ዋጋ == 0xe0 || ዋጋ == 0xe1) { ቅጥያ_ዋጋ = true; return -1; }
        if (ቅጥያ_ዋጋ) { ቅጥያ_ዋጋ = false; return -1; }
        if (ዋጋ == 42 || ዋጋ == 170) { 왼올림 = ዋጋ == 42; return -1; }
        if (ዋጋ == 54 || ዋጋ == 182) { 오른올림 = ዋጋ == 54; return -1; }
        if (ዋጋ >= ንቡር_ዋጋ.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(ዋጋ) : ንቡር_ዋጋ.charAt(ዋጋ);
        return 문자 == 0 ? -1 : 문자;
    }
}
