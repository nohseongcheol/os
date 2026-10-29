// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 převést_zdroj 집합 1 폴링 vstup_HODNOTA. výchozí_hodnota 미국식 자판, Shift, Backspace, Enter. */
public final class klávesnice {
    static boolean posunout_ZLEVA = false;
    static boolean posunout_právo = false;
    static boolean přípona_HODNOTA = false;
    static String výchozí_hodnota = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String posunout_HODNOTA = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Čtení() {
        int Stav_HODNOTA = mobilní_HODNOTA.입출력바이트읽기(0x64);
        if ((Stav_HODNOTA & 1) == 0) return -1;
        int HODNOTA = mobilní_HODNOTA.입출력바이트읽기(0x60);
        if ((Stav_HODNOTA & 0x20) != 0) return -1;
        if (HODNOTA == 0xe0 || HODNOTA == 0xe1) { přípona_HODNOTA = true; return -1; }
        if (přípona_HODNOTA) { přípona_HODNOTA = false; return -1; }
        if (HODNOTA == 42 || HODNOTA == 170) { posunout_ZLEVA = HODNOTA == 42; return -1; }
        if (HODNOTA == 54 || HODNOTA == 182) { posunout_právo = HODNOTA == 54; return -1; }
        if (HODNOTA >= výchozí_hodnota.length()) return -1;
        int 문자 = (posunout_ZLEVA || posunout_právo) ? posunout_HODNOTA.charAt(HODNOTA) : výchozí_hodnota.charAt(HODNOTA);
        return 문자 == 0 ? -1 : 문자;
    }
}
