// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 மொழியாக்கம்_மூலம் 집합 1 폴링 입력. இயல்புநிலை_மதிப்பு 미국식 자판, Shift, Backspace, Enter. */
public final class விசைப்பலகை {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean நீட்டிப்பு_மதிப்பு = false;
    static String இயல்புநிலை_மதிப்பு = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int படி() {
        int நிலை_மதிப்பு_e10195a1 = சாதனம்_மதிப்பு.입출력바이트읽기(0x64);
        if ((நிலை_மதிப்பு_e10195a1 & 1) == 0) return -1;
        int மதிப்பு = சாதனம்_மதிப்பு.입출력바이트읽기(0x60);
        if ((நிலை_மதிப்பு_e10195a1 & 0x20) != 0) return -1;
        if (மதிப்பு == 0xe0 || மதிப்பு == 0xe1) { நீட்டிப்பு_மதிப்பு = true; return -1; }
        if (நீட்டிப்பு_மதிப்பு) { நீட்டிப்பு_மதிப்பு = false; return -1; }
        if (மதிப்பு == 42 || மதிப்பு == 170) { 왼올림 = மதிப்பு == 42; return -1; }
        if (மதிப்பு == 54 || மதிப்பு == 182) { 오른올림 = மதிப்பு == 54; return -1; }
        if (மதிப்பு >= இயல்புநிலை_மதிப்பு.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(மதிப்பு) : இயல்புநிலை_மதிப்பு.charAt(மதிப்பு);
        return 문자 == 0 ? -1 : 문자;
    }
}
