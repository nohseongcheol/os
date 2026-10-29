// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Μετάφραση_προέλευση 집합 1 폴링 είσοδος_τιμή. προεπιλεγμένη_τιμή 미국식 자판, Shift, Backspace, Enter. */
public final class πληκτρολόγιο {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean επέκταση_τιμή = false;
    static String προεπιλεγμένη_τιμή = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String μετακινώ_τιμή = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Ανάγνωση() {
        int Κατάσταση_τιμή = συσκευή_τιμή.입출력바이트읽기(0x64);
        if ((Κατάσταση_τιμή & 1) == 0) return -1;
        int τιμή = συσκευή_τιμή.입출력바이트읽기(0x60);
        if ((Κατάσταση_τιμή & 0x20) != 0) return -1;
        if (τιμή == 0xe0 || τιμή == 0xe1) { επέκταση_τιμή = true; return -1; }
        if (επέκταση_τιμή) { επέκταση_τιμή = false; return -1; }
        if (τιμή == 42 || τιμή == 170) { 왼올림 = τιμή == 42; return -1; }
        if (τιμή == 54 || τιμή == 182) { 오른올림 = τιμή == 54; return -1; }
        if (τιμή >= προεπιλεγμένη_τιμή.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? μετακινώ_τιμή.charAt(τιμή) : προεπιλεγμένη_τιμή.charAt(τιμή);
        return 문자 == 0 ? -1 : 문자;
    }
}
