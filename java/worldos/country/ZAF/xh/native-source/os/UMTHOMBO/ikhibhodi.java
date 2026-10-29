// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Ukuguqulela_umthombo 집합 1 폴링 입력. ixabiso_elisisiseko 미국식 자판, Shift, Backspace, Enter. */
public final class ikhibhodi {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean isongezelelo_ixabiso = false;
    static String ixabiso_elisisiseko = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Funda() {
        int imo_ixabiso = isixhobo_ixabiso.입출력바이트읽기(0x64);
        if ((imo_ixabiso & 1) == 0) return -1;
        int ixabiso = isixhobo_ixabiso.입출력바이트읽기(0x60);
        if ((imo_ixabiso & 0x20) != 0) return -1;
        if (ixabiso == 0xe0 || ixabiso == 0xe1) { isongezelelo_ixabiso = true; return -1; }
        if (isongezelelo_ixabiso) { isongezelelo_ixabiso = false; return -1; }
        if (ixabiso == 42 || ixabiso == 170) { 왼올림 = ixabiso == 42; return -1; }
        if (ixabiso == 54 || ixabiso == 182) { 오른올림 = ixabiso == 54; return -1; }
        if (ixabiso >= ixabiso_elisisiseko.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(ixabiso) : ixabiso_elisisiseko.charAt(ixabiso);
        return 문자 == 0 ? -1 : 문자;
    }
}
