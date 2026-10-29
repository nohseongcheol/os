// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 అనువదించు_మూలం 집합 1 폴링 입력. స్వయంసిద్ధ_విలువ 미국식 자판, Shift, Backspace, Enter. */
public final class కీబోర్డు {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean పొడిగింపు_మూల్యం = false;
    static String స్వయంసిద్ధ_విలువ = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int చదువు() {
        int స్థితి_మూల్యం = పరికరం_మూల్యం.입출력바이트읽기(0x64);
        if ((స్థితి_మూల్యం & 1) == 0) return -1;
        int మూల్యం = పరికరం_మూల్యం.입출력바이트읽기(0x60);
        if ((స్థితి_మూల్యం & 0x20) != 0) return -1;
        if (మూల్యం == 0xe0 || మూల్యం == 0xe1) { పొడిగింపు_మూల్యం = true; return -1; }
        if (పొడిగింపు_మూల్యం) { పొడిగింపు_మూల్యం = false; return -1; }
        if (మూల్యం == 42 || మూల్యం == 170) { 왼올림 = మూల్యం == 42; return -1; }
        if (మూల్యం == 54 || మూల్యం == 182) { 오른올림 = మూల్యం == 54; return -1; }
        if (మూల్యం >= స్వయంసిద్ధ_విలువ.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(మూల్యం) : స్వయంసిద్ధ_విలువ.charAt(మూల్యం);
        return 문자 == 0 ? -1 : 문자;
    }
}
