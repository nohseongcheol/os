// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 अनुवाद_स्रोत 집합 1 폴링 입력. पूर्वनिर्धारित_मान 미국식 자판, Shift, Backspace, Enter. */
public final class कुञ्जीपाटी {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean विस्तार_मान = false;
    static String पूर्वनिर्धारित_मान = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int पढनुहोस्() {
        int स्थिति_मान = मोबाइल_मान.입출력바이트읽기(0x64);
        if ((स्थिति_मान & 1) == 0) return -1;
        int मान = मोबाइल_मान.입출력바이트읽기(0x60);
        if ((स्थिति_मान & 0x20) != 0) return -1;
        if (मान == 0xe0 || मान == 0xe1) { विस्तार_मान = true; return -1; }
        if (विस्तार_मान) { विस्तार_मान = false; return -1; }
        if (मान == 42 || मान == 170) { 왼올림 = मान == 42; return -1; }
        if (मान == 54 || मान == 182) { 오른올림 = मान == 54; return -1; }
        if (मान >= पूर्वनिर्धारित_मान.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(मान) : पूर्वनिर्धारित_मान.charAt(मान);
        return 문자 == 0 ? -1 : 문자;
    }
}
