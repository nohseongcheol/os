// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 અનુવાદ_કરો_સ્રોત 집합 1 폴링 입력. ડિફૉલ્ટ_મૂલ્ય 미국식 자판, Shift, Backspace, Enter. */
public final class કીબોર્ડ {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean એક્સ્ટેંશન_મૂલ્ય = false;
    static String ડિફૉલ્ટ_મૂલ્ય = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int વાંચો() {
        int સ્થિતિ_મૂલ્ય_e10195a1 = ડિવાઇસ_મૂલ્ય.입출력바이트읽기(0x64);
        if ((સ્થિતિ_મૂલ્ય_e10195a1 & 1) == 0) return -1;
        int મૂલ્ય = ડિવાઇસ_મૂલ્ય.입출력바이트읽기(0x60);
        if ((સ્થિતિ_મૂલ્ય_e10195a1 & 0x20) != 0) return -1;
        if (મૂલ્ય == 0xe0 || મૂલ્ય == 0xe1) { એક્સ્ટેંશન_મૂલ્ય = true; return -1; }
        if (એક્સ્ટેંશન_મૂલ્ય) { એક્સ્ટેંશન_મૂલ્ય = false; return -1; }
        if (મૂલ્ય == 42 || મૂલ્ય == 170) { 왼올림 = મૂલ્ય == 42; return -1; }
        if (મૂલ્ય == 54 || મૂલ્ય == 182) { 오른올림 = મૂલ્ય == 54; return -1; }
        if (મૂલ્ય >= ડિફૉલ્ટ_મૂલ્ય.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(મૂલ્ય) : ડિફૉલ્ટ_મૂલ્ય.charAt(મૂલ્ય);
        return 문자 == 0 ? -1 : 문자;
    }
}
