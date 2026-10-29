// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 បកប្រែ_ប្រភព 집합 1 폴링 입력. តំលៃស្វ័យប្រវត្តិ 미국식 자판, Shift, Backspace, Enter. */
public final class ឃីបត {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean ម៉ូឌុល_តំលៃ = false;
    static String តំលៃស្វ័យប្រវត្តិ = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int អាន() {
        int ភាព_តំលៃ = ឧបករណ៍_តំលៃ.입출력바이트읽기(0x64);
        if ((ភាព_តំលៃ & 1) == 0) return -1;
        int តំលៃ = ឧបករណ៍_តំលៃ.입출력바이트읽기(0x60);
        if ((ភាព_តំលៃ & 0x20) != 0) return -1;
        if (តំលៃ == 0xe0 || តំលៃ == 0xe1) { ម៉ូឌុល_តំលៃ = true; return -1; }
        if (ម៉ូឌុល_តំលៃ) { ម៉ូឌុល_តំលៃ = false; return -1; }
        if (តំលៃ == 42 || តំលៃ == 170) { 왼올림 = តំលៃ == 42; return -1; }
        if (តំលៃ == 54 || តំលៃ == 182) { 오른올림 = តំលៃ == 54; return -1; }
        if (តំលៃ >= តំលៃស្វ័យប្រវត្តិ.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(តំលៃ) : តំលៃស្វ័យប្រវត្តិ.charAt(តំលៃ);
        return 문자 == 0 ? -1 : 문자;
    }
}
