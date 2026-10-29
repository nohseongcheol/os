// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Fasara_tushe 집합 1 폴링 입력. Tanadaddiyar_daraja 미국식 자판, Shift, Backspace, Enter. */
public final class kibod {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean faɗi_Daraja = false;
    static String Tanadaddiyar_daraja = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Yi_Karatu() {
        int Matsayi_Daraja = na_ura_Daraja.입출력바이트읽기(0x64);
        if ((Matsayi_Daraja & 1) == 0) return -1;
        int Daraja = na_ura_Daraja.입출력바이트읽기(0x60);
        if ((Matsayi_Daraja & 0x20) != 0) return -1;
        if (Daraja == 0xe0 || Daraja == 0xe1) { faɗi_Daraja = true; return -1; }
        if (faɗi_Daraja) { faɗi_Daraja = false; return -1; }
        if (Daraja == 42 || Daraja == 170) { 왼올림 = Daraja == 42; return -1; }
        if (Daraja == 54 || Daraja == 182) { 오른올림 = Daraja == 54; return -1; }
        if (Daraja >= Tanadaddiyar_daraja.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(Daraja) : Tanadaddiyar_daraja.charAt(Daraja);
        return 문자 == 0 ? -1 : 문자;
    }
}
