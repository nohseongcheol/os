// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 تەرجىمە_مەنبە 집합 1 폴링 입력. سۈكۈتتىكى_قىممەت 미국식 자판, Shift, Backspace, Enter. */
public final class كۇنۇپكا_تاختىسى {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean كېڭەيتمە_قىممىتى = false;
    static String سۈكۈتتىكى_قىممەت = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int ئوقۇ() {
        int ھالەت_قىممىتى = كۆچمە_قىممىتى.입출력바이트읽기(0x64);
        if ((ھالەت_قىممىتى & 1) == 0) return -1;
        int قىممىتى = كۆچمە_قىممىتى.입출력바이트읽기(0x60);
        if ((ھالەت_قىممىتى & 0x20) != 0) return -1;
        if (قىممىتى == 0xe0 || قىممىتى == 0xe1) { كېڭەيتمە_قىممىتى = true; return -1; }
        if (كېڭەيتمە_قىممىتى) { كېڭەيتمە_قىممىتى = false; return -1; }
        if (قىممىتى == 42 || قىممىتى == 170) { 왼올림 = قىممىتى == 42; return -1; }
        if (قىممىتى == 54 || قىممىتى == 182) { 오른올림 = قىممىتى == 54; return -1; }
        if (قىممىتى >= سۈكۈتتىكى_قىممەت.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(قىممىتى) : سۈكۈتتىكى_قىممەت.charAt(قىممىتى);
        return 문자 == 0 ? -1 : 문자;
    }
}
