// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Terjime_gor 집합 1 폴링 입력. öňünden_kabul_edilen_baha 미국식 자판, Shift, Backspace, Enter. */
public final class klawiatura {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean giňelme_baha = false;
    static String öňünden_kabul_edilen_baha = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Oka() {
        int ýagdaý_baha = enjam_baha.입출력바이트읽기(0x64);
        if ((ýagdaý_baha & 1) == 0) return -1;
        int baha = enjam_baha.입출력바이트읽기(0x60);
        if ((ýagdaý_baha & 0x20) != 0) return -1;
        if (baha == 0xe0 || baha == 0xe1) { giňelme_baha = true; return -1; }
        if (giňelme_baha) { giňelme_baha = false; return -1; }
        if (baha == 42 || baha == 170) { 왼올림 = baha == 42; return -1; }
        if (baha == 54 || baha == 182) { 오른올림 = baha == 54; return -1; }
        if (baha >= öňünden_kabul_edilen_baha.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(baha) : öňünden_kabul_edilen_baha.charAt(baha);
        return 문자 == 0 ? -1 : 문자;
    }
}
