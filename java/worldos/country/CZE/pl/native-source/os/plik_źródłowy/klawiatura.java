// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 TŁUMACZ_źródło 집합 1 폴링 wejście_WARTOŚĆ. wartość_domyślna 미국식 자판, Shift, Backspace, Enter. */
public final class klawiatura {
    static boolean przesunąć_LEWY = false;
    static boolean przesunąć_PRAWY = false;
    static boolean rozszerzenie_WARTOŚĆ = false;
    static String wartość_domyślna = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String przesunąć_WARTOŚĆ = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Odczyt() {
        int Stan_WARTOŚĆ = urządzenie_WARTOŚĆ.입출력바이트읽기(0x64);
        if ((Stan_WARTOŚĆ & 1) == 0) return -1;
        int WARTOŚĆ = urządzenie_WARTOŚĆ.입출력바이트읽기(0x60);
        if ((Stan_WARTOŚĆ & 0x20) != 0) return -1;
        if (WARTOŚĆ == 0xe0 || WARTOŚĆ == 0xe1) { rozszerzenie_WARTOŚĆ = true; return -1; }
        if (rozszerzenie_WARTOŚĆ) { rozszerzenie_WARTOŚĆ = false; return -1; }
        if (WARTOŚĆ == 42 || WARTOŚĆ == 170) { przesunąć_LEWY = WARTOŚĆ == 42; return -1; }
        if (WARTOŚĆ == 54 || WARTOŚĆ == 182) { przesunąć_PRAWY = WARTOŚĆ == 54; return -1; }
        if (WARTOŚĆ >= wartość_domyślna.length()) return -1;
        int 문자 = (przesunąć_LEWY || przesunąć_PRAWY) ? przesunąć_WARTOŚĆ.charAt(WARTOŚĆ) : wartość_domyślna.charAt(WARTOŚĆ);
        return 문자 == 0 ? -1 : 문자;
    }
}
