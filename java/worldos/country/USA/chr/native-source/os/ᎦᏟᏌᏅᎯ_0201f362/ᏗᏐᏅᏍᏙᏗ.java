// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 번역 집합 1 폴링 입력. ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ 미국식 자판, Shift, Backspace, Enter. */
public final class ᏗᏐᏅᏍᏙᏗ {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean ᎪᏯᏅᎯᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ = false;
    static String ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 읽기() {
        int ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ = ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ.입출력바이트읽기(0x64);
        if ((ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ & 1) == 0) return -1;
        int ᏧᎬᏩᎶᏗᏯ = ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ.입출력바이트읽기(0x60);
        if ((ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ & 0x20) != 0) return -1;
        if (ᏧᎬᏩᎶᏗᏯ == 0xe0 || ᏧᎬᏩᎶᏗᏯ == 0xe1) { ᎪᏯᏅᎯᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ = true; return -1; }
        if (ᎪᏯᏅᎯᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ) { ᎪᏯᏅᎯᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ = false; return -1; }
        if (ᏧᎬᏩᎶᏗᏯ == 42 || ᏧᎬᏩᎶᏗᏯ == 170) { 왼올림 = ᏧᎬᏩᎶᏗᏯ == 42; return -1; }
        if (ᏧᎬᏩᎶᏗᏯ == 54 || ᏧᎬᏩᎶᏗᏯ == 182) { 오른올림 = ᏧᎬᏩᎶᏗᏯ == 54; return -1; }
        if (ᏧᎬᏩᎶᏗᏯ >= ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(ᏧᎬᏩᎶᏗᏯ) : ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ.charAt(ᏧᎬᏩᎶᏗᏯ);
        return 문자 == 0 ? -1 : 문자;
    }
}
