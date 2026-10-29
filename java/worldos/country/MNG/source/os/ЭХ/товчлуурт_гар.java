// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Орчуулах_эх 집합 1 폴링 입력. өгөгдмөл_утга 미국식 자판, Shift, Backspace, Enter. */
public final class товчлуурт_гар {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean өргөтгөл_утга = false;
    static String өгөгдмөл_утга = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Унших() {
        int төлөв_утга = гар_утас_утга.입출력바이트읽기(0x64);
        if ((төлөв_утга & 1) == 0) return -1;
        int утга = гар_утас_утга.입출력바이트읽기(0x60);
        if ((төлөв_утга & 0x20) != 0) return -1;
        if (утга == 0xe0 || утга == 0xe1) { өргөтгөл_утга = true; return -1; }
        if (өргөтгөл_утга) { өргөтгөл_утга = false; return -1; }
        if (утга == 42 || утга == 170) { 왼올림 = утга == 42; return -1; }
        if (утга == 54 || утга == 182) { 오른올림 = утга == 54; return -1; }
        if (утга >= өгөгдмөл_утга.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(утга) : өгөгдмөл_утга.charAt(утга);
        return 문자 == 0 ? -1 : 문자;
    }
}
