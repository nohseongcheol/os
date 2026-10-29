// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 แปล_แหล่ง 집합 1 폴링 입력. ค่าเริ่มต้น 미국식 자판, Shift, Backspace, Enter. */
public final class คีย์บอร์ด {
    static boolean 왼올림 = false;
    static boolean เลื่อน_สิทธิ์ = false;
    static boolean นามสกุล_ค่า = false;
    static String ค่าเริ่มต้น = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String เลื่อน_ค่า = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int อ่าน() {
        int สถานะ_ค่า = อุปกรณ์_ค่า.입출력바이트읽기(0x64);
        if ((สถานะ_ค่า & 1) == 0) return -1;
        int ค่า = อุปกรณ์_ค่า.입출력바이트읽기(0x60);
        if ((สถานะ_ค่า & 0x20) != 0) return -1;
        if (ค่า == 0xe0 || ค่า == 0xe1) { นามสกุล_ค่า = true; return -1; }
        if (นามสกุล_ค่า) { นามสกุล_ค่า = false; return -1; }
        if (ค่า == 42 || ค่า == 170) { 왼올림 = ค่า == 42; return -1; }
        if (ค่า == 54 || ค่า == 182) { เลื่อน_สิทธิ์ = ค่า == 54; return -1; }
        if (ค่า >= ค่าเริ่มต้น.length()) return -1;
        int 문자 = (왼올림 || เลื่อน_สิทธิ์) ? เลื่อน_ค่า.charAt(ค่า) : ค่าเริ่มต้น.charAt(ค่า);
        return 문자 == 0 ? -1 : 문자;
    }
}
