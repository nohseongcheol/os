// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 TRANSLATE_pūtake 집합 1 폴링 입력. uara_taunoa 미국식 자판, Shift, Backspace, Enter. */
public final class papapātuhi {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean toronga_uara = false;
    static String uara_taunoa = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Pānuitia() {
        int tūnga_uara = pūkoro_uara.입출력바이트읽기(0x64);
        if ((tūnga_uara & 1) == 0) return -1;
        int uara = pūkoro_uara.입출력바이트읽기(0x60);
        if ((tūnga_uara & 0x20) != 0) return -1;
        if (uara == 0xe0 || uara == 0xe1) { toronga_uara = true; return -1; }
        if (toronga_uara) { toronga_uara = false; return -1; }
        if (uara == 42 || uara == 170) { 왼올림 = uara == 42; return -1; }
        if (uara == 54 || uara == 182) { 오른올림 = uara == 54; return -1; }
        if (uara >= uara_taunoa.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(uara) : uara_taunoa.charAt(uara);
        return 문자 == 0 ? -1 : 문자;
    }
}
