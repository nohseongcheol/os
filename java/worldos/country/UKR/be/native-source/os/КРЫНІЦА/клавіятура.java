// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Пераклад_крыніца 집합 1 폴링 입력. значэнне_па_змаўчанні 미국식 자판, Shift, Backspace, Enter. */
public final class клавіятура {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean пашырэнне_значэнне = false;
    static String значэнне_па_змаўчанні = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Чытанне() {
        int стан_значэнне = прылада_значэнне.입출력바이트읽기(0x64);
        if ((стан_значэнне & 1) == 0) return -1;
        int значэнне = прылада_значэнне.입출력바이트읽기(0x60);
        if ((стан_значэнне & 0x20) != 0) return -1;
        if (значэнне == 0xe0 || значэнне == 0xe1) { пашырэнне_значэнне = true; return -1; }
        if (пашырэнне_значэнне) { пашырэнне_значэнне = false; return -1; }
        if (значэнне == 42 || значэнне == 170) { 왼올림 = значэнне == 42; return -1; }
        if (значэнне == 54 || значэнне == 182) { 오른올림 = значэнне == 54; return -1; }
        if (значэнне >= значэнне_па_змаўчанні.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(значэнне) : значэнне_па_змаўчанні.charAt(значэнне);
        return 문자 == 0 ? -1 : 문자;
    }
}
