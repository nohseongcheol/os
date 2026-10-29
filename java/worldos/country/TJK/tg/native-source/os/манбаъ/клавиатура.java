// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Тарҷума_манбаъ 집합 1 폴링 입력. қимати_пешфарз 미국식 자판, Shift, Backspace, Enter. */
public final class клавиатура {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean изофа_қимат = false;
    static String қимати_пешфарз = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Хондан() {
        int вазъият_қимат = мобилӣ_қимат.입출력바이트읽기(0x64);
        if ((вазъият_қимат & 1) == 0) return -1;
        int қимат = мобилӣ_қимат.입출력바이트읽기(0x60);
        if ((вазъият_қимат & 0x20) != 0) return -1;
        if (қимат == 0xe0 || қимат == 0xe1) { изофа_қимат = true; return -1; }
        if (изофа_қимат) { изофа_қимат = false; return -1; }
        if (қимат == 42 || қимат == 170) { 왼올림 = қимат == 42; return -1; }
        if (қимат == 54 || қимат == 182) { 오른올림 = қимат == 54; return -1; }
        if (қимат >= қимати_пешфарз.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(қимат) : қимати_пешфарз.charAt(қимат);
        return 문자 == 0 ? -1 : 문자;
    }
}
