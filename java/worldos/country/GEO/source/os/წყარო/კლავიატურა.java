// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 თარგმნა_წყარო 집합 1 폴링 입력. ნაგულისხმევი_მნიშვნელობა 미국식 자판, Shift, Backspace, Enter. */
public final class კლავიატურა {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean გაფართოება_მნიშვნელობა = false;
    static String ნაგულისხმევი_მნიშვნელობა = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int კითხვა() {
        int სტატუსი_მნიშვნელობა = მობილური_მნიშვნელობა.입출력바이트읽기(0x64);
        if ((სტატუსი_მნიშვნელობა & 1) == 0) return -1;
        int მნიშვნელობა = მობილური_მნიშვნელობა.입출력바이트읽기(0x60);
        if ((სტატუსი_მნიშვნელობა & 0x20) != 0) return -1;
        if (მნიშვნელობა == 0xe0 || მნიშვნელობა == 0xe1) { გაფართოება_მნიშვნელობა = true; return -1; }
        if (გაფართოება_მნიშვნელობა) { გაფართოება_მნიშვნელობა = false; return -1; }
        if (მნიშვნელობა == 42 || მნიშვნელობა == 170) { 왼올림 = მნიშვნელობა == 42; return -1; }
        if (მნიშვნელობა == 54 || მნიშვნელობა == 182) { 오른올림 = მნიშვნელობა == 54; return -1; }
        if (მნიშვნელობა >= ნაგულისხმევი_მნიშვნელობა.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(მნიშვნელობა) : ნაგულისხმევი_მნიშვნელობა.charAt(მნიშვნელობა);
        return 문자 == 0 ? -1 : 문자;
    }
}
