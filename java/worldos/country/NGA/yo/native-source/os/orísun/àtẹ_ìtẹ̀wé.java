// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Aṣàtúmọ̀_èdè_orísun 집합 1 폴링 입력. àdáwọ̀ 미국식 자판, Shift, Backspace, Enter. */
public final class àtẹ_ìtẹ̀wé {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean Àfikún_iye = false;
    static String àdáwọ̀ = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Kàá() {
        int ipò_iye = ohun_èlò_iye.입출력바이트읽기(0x64);
        if ((ipò_iye & 1) == 0) return -1;
        int iye = ohun_èlò_iye.입출력바이트읽기(0x60);
        if ((ipò_iye & 0x20) != 0) return -1;
        if (iye == 0xe0 || iye == 0xe1) { Àfikún_iye = true; return -1; }
        if (Àfikún_iye) { Àfikún_iye = false; return -1; }
        if (iye == 42 || iye == 170) { 왼올림 = iye == 42; return -1; }
        if (iye == 54 || iye == 182) { 오른올림 = iye == 54; return -1; }
        if (iye >= àdáwọ̀.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(iye) : àdáwọ̀.charAt(iye);
        return 문자 == 0 ? -1 : 문자;
    }
}
