// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Перекласти_джерело 집합 1 폴링 입력. стандартне_значення 미국식 자판, Shift, Backspace, Enter. */
public final class клавіатура {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean розширення_значення = false;
    static String стандартне_значення = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Читання() {
        int Стан_значення = пристрій_значення.입출력바이트읽기(0x64);
        if ((Стан_значення & 1) == 0) return -1;
        int значення = пристрій_значення.입출력바이트읽기(0x60);
        if ((Стан_значення & 0x20) != 0) return -1;
        if (значення == 0xe0 || значення == 0xe1) { розширення_значення = true; return -1; }
        if (розширення_значення) { розширення_значення = false; return -1; }
        if (значення == 42 || значення == 170) { 왼올림 = значення == 42; return -1; }
        if (значення == 54 || значення == 182) { 오른올림 = значення == 54; return -1; }
        if (значення >= стандартне_значення.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(значення) : стандартне_значення.charAt(значення);
        return 문자 == 0 ? -1 : 문자;
    }
}
