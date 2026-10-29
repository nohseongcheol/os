// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 Превод_източник 집합 1 폴링 입력. стойност_по_подразбиране 미국식 자판, Shift, Backspace, Enter. */
public final class клавиатура {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean разширение_стойност = false;
    static String стойност_по_подразбиране = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int Четене() {
        int Състояние_стойност = устройство_стойност.입출력바이트읽기(0x64);
        if ((Състояние_стойност & 1) == 0) return -1;
        int стойност = устройство_стойност.입출력바이트읽기(0x60);
        if ((Състояние_стойност & 0x20) != 0) return -1;
        if (стойност == 0xe0 || стойност == 0xe1) { разширение_стойност = true; return -1; }
        if (разширение_стойност) { разширение_стойност = false; return -1; }
        if (стойност == 42 || стойност == 170) { 왼올림 = стойност == 42; return -1; }
        if (стойност == 54 || стойност == 182) { 오른올림 = стойност == 54; return -1; }
        if (стойност >= стойност_по_подразбиране.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(стойност) : стойност_по_подразбиране.charAt(стойност);
        return 문자 == 0 ? -1 : 문자;
    }
}
