// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Թարգմանել_աղբյուր 집합 1 폴링 입력. սկզբնադիր_արժեք 미국식 자판, Shift, Backspace, Enter. */
public final class ստեղնաշար {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean ընդլայնում_արժեք = false;
    static String սկզբնադիր_արժեք = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Ընթերցում() {
        int վիճակ_արժեք = սարք_արժեք.입출력바이트읽기(0x64);
        if ((վիճակ_արժեք & 1) == 0) return -1;
        int արժեք = սարք_արժեք.입출력바이트읽기(0x60);
        if ((վիճակ_արժեք & 0x20) != 0) return -1;
        if (արժեք == 0xe0 || արժեք == 0xe1) { ընդլայնում_արժեք = true; return -1; }
        if (ընդլայնում_արժեք) { ընդլայնում_արժեք = false; return -1; }
        if (արժեք == 42 || արժեք == 170) { 왼올림 = արժեք == 42; return -1; }
        if (արժեք == 54 || արժեք == 182) { 오른올림 = արժեք == 54; return -1; }
        if (արժեք >= սկզբնադիր_արժեք.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(արժեք) : սկզբնադիր_արժեք.charAt(արժեք);
        return 문자 == 0 ? -1 : 문자;
    }
}
