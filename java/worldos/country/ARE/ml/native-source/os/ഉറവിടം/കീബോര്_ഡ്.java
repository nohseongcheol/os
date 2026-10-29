// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 വിവർത്തനം_ചെയ്യുക_ഉറവിടം 집합 1 폴링 입력. സ്ഥിരസ്ഥിതി_മൂല്യം 미국식 자판, Shift, Backspace, Enter. */
public final class കീബോര്_ഡ് {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean വിപുലീകരണം_മൂല്യം = false;
    static String സ്ഥിരസ്ഥിതി_മൂല്യം = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int വായന() {
        int അവസ്ഥ_മൂല്യം = മൊബൈൽ_മൂല്യം.입출력바이트읽기(0x64);
        if ((അവസ്ഥ_മൂല്യം & 1) == 0) return -1;
        int മൂല്യം = മൊബൈൽ_മൂല്യം.입출력바이트읽기(0x60);
        if ((അവസ്ഥ_മൂല്യം & 0x20) != 0) return -1;
        if (മൂല്യം == 0xe0 || മൂല്യം == 0xe1) { വിപുലീകരണം_മൂല്യം = true; return -1; }
        if (വിപുലീകരണം_മൂല്യം) { വിപുലീകരണം_മൂല്യം = false; return -1; }
        if (മൂല്യം == 42 || മൂല്യം == 170) { 왼올림 = മൂല്യം == 42; return -1; }
        if (മൂല്യം == 54 || മൂല്യം == 182) { 오른올림 = മൂല്യം == 54; return -1; }
        if (മൂല്യം >= സ്ഥിരസ്ഥിതി_മൂല്യം.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(മൂല്യം) : സ്ഥിരസ്ഥിതി_മൂല്യം.charAt(മൂല്യം);
        return 문자 == 0 ? -1 : 문자;
    }
}
