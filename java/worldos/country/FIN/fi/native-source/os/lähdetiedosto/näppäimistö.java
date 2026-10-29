// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 KÄÄNNÄ_lähde 집합 1 폴링 syöte_ARVO. oletusarvo 미국식 자판, Shift, Backspace, Enter. */
public final class näppäimistö {
    static boolean siirrä_VASEN = false;
    static boolean siirrä_OIKEA = false;
    static boolean tarkenne_ARVO = false;
    static String oletusarvo = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String siirrä_ARVO = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Luku() {
        int Tila_ARVO = laite_ARVO.입출력바이트읽기(0x64);
        if ((Tila_ARVO & 1) == 0) return -1;
        int ARVO = laite_ARVO.입출력바이트읽기(0x60);
        if ((Tila_ARVO & 0x20) != 0) return -1;
        if (ARVO == 0xe0 || ARVO == 0xe1) { tarkenne_ARVO = true; return -1; }
        if (tarkenne_ARVO) { tarkenne_ARVO = false; return -1; }
        if (ARVO == 42 || ARVO == 170) { siirrä_VASEN = ARVO == 42; return -1; }
        if (ARVO == 54 || ARVO == 182) { siirrä_OIKEA = ARVO == 54; return -1; }
        if (ARVO >= oletusarvo.length()) return -1;
        int 문자 = (siirrä_VASEN || siirrä_OIKEA) ? siirrä_ARVO.charAt(ARVO) : oletusarvo.charAt(ARVO);
        return 문자 == 0 ? -1 : 문자;
    }
}
