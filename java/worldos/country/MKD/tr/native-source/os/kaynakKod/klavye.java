// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 çevir_kaynak 집합 1 폴링 artış_değer. varsayılan_değer 미국식 자판, Shift, Backspace, Enter. */
public final class klavye {
    static boolean kaydırmak_SOLDAN = false;
    static boolean kaydırmak_hak = false;
    static boolean uzantı_değer = false;
    static String varsayılan_değer = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String kaydırmak_değer = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Okuma() {
        int Durum_değer = cihaz_değer.입출력바이트읽기(0x64);
        if ((Durum_değer & 1) == 0) return -1;
        int değer = cihaz_değer.입출력바이트읽기(0x60);
        if ((Durum_değer & 0x20) != 0) return -1;
        if (değer == 0xe0 || değer == 0xe1) { uzantı_değer = true; return -1; }
        if (uzantı_değer) { uzantı_değer = false; return -1; }
        if (değer == 42 || değer == 170) { kaydırmak_SOLDAN = değer == 42; return -1; }
        if (değer == 54 || değer == 182) { kaydırmak_hak = değer == 54; return -1; }
        if (değer >= varsayılan_değer.length()) return -1;
        int 문자 = (kaydırmak_SOLDAN || kaydırmak_hak) ? kaydırmak_değer.charAt(değer) : varsayılan_değer.charAt(değer);
        return 문자 == 0 ? -1 : 문자;
    }
}
