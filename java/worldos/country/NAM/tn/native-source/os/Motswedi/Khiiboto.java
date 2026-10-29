// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Ranola_Motswedi 집합 1 폴링 입력. boleng_jo_bo_rulaganyeditsweng_ruri 미국식 자판, Shift, Backspace, Enter. */
public final class Khiiboto {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean katoloso_Boleng = false;
    static String boleng_jo_bo_rulaganyeditsweng_ruri = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 읽기() {
        int kemo_Boleng = mobaele_Boleng.입출력바이트읽기(0x64);
        if ((kemo_Boleng & 1) == 0) return -1;
        int Boleng = mobaele_Boleng.입출력바이트읽기(0x60);
        if ((kemo_Boleng & 0x20) != 0) return -1;
        if (Boleng == 0xe0 || Boleng == 0xe1) { katoloso_Boleng = true; return -1; }
        if (katoloso_Boleng) { katoloso_Boleng = false; return -1; }
        if (Boleng == 42 || Boleng == 170) { 왼올림 = Boleng == 42; return -1; }
        if (Boleng == 54 || Boleng == 182) { 오른올림 = Boleng == 54; return -1; }
        if (Boleng >= boleng_jo_bo_rulaganyeditsweng_ruri.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(Boleng) : boleng_jo_bo_rulaganyeditsweng_ruri.charAt(Boleng);
        return 문자 == 0 ? -1 : 문자;
    }
}
