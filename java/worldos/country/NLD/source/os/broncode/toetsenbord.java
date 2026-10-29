// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 VERTALEN_bron 집합 1 폴링 invoer_WAARDE. standaardwaarde 미국식 자판, Shift, Backspace, Enter. */
public final class toetsenbord {
    static boolean verplaatsen_LINKS = false;
    static boolean verplaatsen_recht = false;
    static boolean extensie_WAARDE = false;
    static String standaardwaarde = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String verplaatsen_WAARDE = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Lezen() {
        int Status_WAARDE = mobiel_WAARDE.입출력바이트읽기(0x64);
        if ((Status_WAARDE & 1) == 0) return -1;
        int WAARDE = mobiel_WAARDE.입출력바이트읽기(0x60);
        if ((Status_WAARDE & 0x20) != 0) return -1;
        if (WAARDE == 0xe0 || WAARDE == 0xe1) { extensie_WAARDE = true; return -1; }
        if (extensie_WAARDE) { extensie_WAARDE = false; return -1; }
        if (WAARDE == 42 || WAARDE == 170) { verplaatsen_LINKS = WAARDE == 42; return -1; }
        if (WAARDE == 54 || WAARDE == 182) { verplaatsen_recht = WAARDE == 54; return -1; }
        if (WAARDE >= standaardwaarde.length()) return -1;
        int 문자 = (verplaatsen_LINKS || verplaatsen_recht) ? verplaatsen_WAARDE.charAt(WAARDE) : standaardwaarde.charAt(WAARDE);
        return 문자 == 0 ? -1 : 문자;
    }
}
