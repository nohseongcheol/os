// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Tafsiri_chanzo 집합 1 폴링 입력. hali_ya_chaguo_msingi 미국식 자판, Shift, Backspace, Enter. */
public final class kibodi {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean kiendelezi_thamani = false;
    static String hali_ya_chaguo_msingi = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 읽기() {
        int hali_thamani = kifaa_thamani.입출력바이트읽기(0x64);
        if ((hali_thamani & 1) == 0) return -1;
        int thamani = kifaa_thamani.입출력바이트읽기(0x60);
        if ((hali_thamani & 0x20) != 0) return -1;
        if (thamani == 0xe0 || thamani == 0xe1) { kiendelezi_thamani = true; return -1; }
        if (kiendelezi_thamani) { kiendelezi_thamani = false; return -1; }
        if (thamani == 42 || thamani == 170) { 왼올림 = thamani == 42; return -1; }
        if (thamani == 54 || thamani == 182) { 오른올림 = thamani == 54; return -1; }
        if (thamani >= hali_ya_chaguo_msingi.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(thamani) : hali_ya_chaguo_msingi.charAt(thamani);
        return 문자 == 0 ? -1 : 문자;
    }
}
