// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Terjemah_sumber 집합 1 폴링 입력. nilai_lalai 미국식 자판, Shift, Backspace, Enter. */
public final class papan_kekunci {
    static boolean anjak_LEFT = false;
    static boolean anjak_RIGHT = false;
    static boolean sambungan_VALUE = false;
    static String nilai_lalai = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String anjak_VALUE = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Baca() {
        int status_VALUE = peranti_VALUE.입출력바이트읽기(0x64);
        if ((status_VALUE & 1) == 0) return -1;
        int VALUE = peranti_VALUE.입출력바이트읽기(0x60);
        if ((status_VALUE & 0x20) != 0) return -1;
        if (VALUE == 0xe0 || VALUE == 0xe1) { sambungan_VALUE = true; return -1; }
        if (sambungan_VALUE) { sambungan_VALUE = false; return -1; }
        if (VALUE == 42 || VALUE == 170) { anjak_LEFT = VALUE == 42; return -1; }
        if (VALUE == 54 || VALUE == 182) { anjak_RIGHT = VALUE == 54; return -1; }
        if (VALUE >= nilai_lalai.length()) return -1;
        int 문자 = (anjak_LEFT || anjak_RIGHT) ? anjak_VALUE.charAt(VALUE) : nilai_lalai.charAt(VALUE);
        return 문자 == 0 ? -1 : 문자;
    }
}
