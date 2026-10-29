// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** עצמי Java 커널의 Pi4 מצב_התחלתי 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class ליבה {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int משימה_סדר;
    static int משימה_שגיאה;
    static int 난수씨 = 17;

    static void ודא_אמת(boolean תנאי, int מדד) {
        if (!תנאי) { 단말.כתוב("FAIL "); 단말.수(מדד); לוח.עצירה(מדד); }
    }
    static int ענף(int ערך) {
        switch (ערך) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int ערך) {
        switch (ערך) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] החזר_מערך(int[] מערך_ערך) { return מערך_ערך; }
    static void 계산시험() {
        int ערך = 난수씨;
        ודא_אמת(ערך * 7 - ערך == 102 && ערך / 3 == 5 && ערך % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        ודא_אמת(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        ודא_אמת(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        ודא_אמת((-ערך >> 2) == -5 && (-ערך >>> 2) == 1073741819 && (ערך << 33) == 34, 4);
        ודא_אמת((byte)(ערך * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] מערך_ערך = new int[5];
        for (int לולאה_מדד = 0; לולאה_מדד < מערך_ערך.length; לולאה_מדד++) מערך_ערך[לולאה_מדד] = לולאה_מדד * ערך;
        מערך_ערך[2]++;
        ודא_אמת(החזר_מערך(מערך_ערך) == מערך_ערך && מערך_ערך[2] == 35 && מערך_ערך[4] == 68, 6);
        ודא_אמת(ענף(ערך - 117) == 7 && ענף(ערך - 15) == 9 && ענף(ערך) == 3 && 촘촘분기(ערך - 15) == 17, 7);
        String טקסט = "한글 😀";
        ודא_אמת(טקסט.length() == 5 && טקסט.charAt(0) == '한' && טקסט.charAt(3) == 0xd83d, 8);
        ודא_אמת(לוח.מעבד_הרשאה_רמה() == 1, 9);
        단말.כתוב("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int מדד) {
        // רווח_מעבד 전후 מקומי_היקף 변수가 보존되는지 검사: 각 작업은 독립된 מחשב 스택을 쓴다.
        int מקומי_ערך = מדד * 100;
        for (int לולאה_מדד = 0; לולאה_מדד < 10; לולאה_מדד++) {
            if (משימה_סדר % 2 + 1 != מדד) משימה_שגיאה++;
            משימה_סדר++;
            מקומי_ערך += לולאה_מדד + מדד;
            작업합[מדד] = מקומי_ערך;
            작업횟수[מדד]++;
            לוח.רווח_מעבד();
            if (מקומי_ערך != 작업합[מדד]) משימה_שגיאה++;
        }
    }
    static void 작업시험() {
        משימה_סדר = 0; משימה_שגיאה = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        ודא_אמת(לוח.ליצור_משימה(1) == 0 && לוח.ליצור_משימה(2) == 0, 20);
        int 회전 = 0;
        while (לוח.משימה_מצב(1) != 0 || לוח.משימה_מצב(2) != 0) {
            לוח.רווח_מעבד();
            ודא_אמת(++회전 < 100, 21);
        }
        ודא_אמת(작업횟수[1] == 10 && 작업횟수[2] == 10 && משימה_סדר == 20 && משימה_שגיאה == 0, 22);
        ודא_אמת(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.כתוב("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void מלבן(int 가로, int אנכי_עמדה, int 너비, int גובה_ערך, int 색) {
        for (int 세로좌표 = אנכי_עמדה; 세로좌표 < אנכי_עמדה + גובה_ערך; 세로좌표++)
            for (int קואורדינטת_x = 가로; קואורדינטת_x < 가로 + 너비; קואורדינטת_x++) לוח.화면점(קואורדינטת_x, 세로좌표, 색);
    }
    static void 화면() {
        if (לוח.화면준비() == 0) { 단말.כתוב("FRAMEBUFFER unavailable\n"); return; }
        מלבן(0, 0, לוח.화면너비(), לוח.화면높이(), 0x302018);
        מלבן(40, 40, 560, 400, 0xefe8e2);
        מלבן(40, 40, 560, 40, 0x905020);
        מלבן(60, 110, 240, 140, 0x90b050);
        מלבן(320, 110, 260, 140, 0xd0a040);
        מלבן(60, 290, 520, 120, 0xd8d0c8);
        단말.כתוב("FRAMEBUFFER PASS "); 단말.수(לוח.화면너비()); 단말.문자('x');
        단말.수(לוח.화면높이()); 단말.כתוב(" RGB32 (drawing only)\n");
    }
    static void נסה_מ() {
        int תוצאה = לוח.씨플러스시험();
        ודא_אמת(תוצאה == 0, 100 + תוצאה);
        단말.כתוב("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        ודא_אמת(לוח.שיק_משתמש_תוכנית() == 0, 200);
        단말.כתוב("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = לוח.להפעיל_משתמש_תוכנית(0);
        if (처음결과 != 0) { 단말.כתוב("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        ודא_אמת(처음결과 == 0, 201);
        단말.כתוב("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int מדד = 0; מדד < 예상.length; מדד++) {
            단말.כתוב("USER CHECK "); 단말.수(מדד); 단말.문자(10);
            int תוצאה = לוח.להפעיל_משתמש_תוכנית(מדד + 1);
            if (תוצאה != 예상[מדד]) { 단말.כתוב("USER RESULT "); 단말.수(תוצאה); 단말.문자(10); }
            ודא_אמת(תוצאה == 예상[מדד], 210 + מדד);
        }
        ודא_אמת(לוח.להפעיל_משתמש_תוכנית(0) == 0, 220);
        단말.כתוב("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void נסה_עבודה_ברשת() {
        int תוצאה = לוח.להפעיל_משתמש_תוכנית(9);
        if (תוצאה != 0) { 단말.כתוב("UDP RESULT "); 단말.수(תוצאה); 단말.문자(10); }
        ודא_אמת(תוצאה == 0, 230);
    }
    static void מידע_מערכת() {
        단말.כתוב("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.כתוב("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.כתוב("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.כתוב("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.כתוב("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void הפעלה() {
        단말.כתוב("WorldOS he · שלום · 😀\n");
        계산시험();
        נסה_מ();
        작업시험();
        화면();
        사용자시험();
        נסה_עבודה_ברשת();
        단말.כתוב("NATIVE READY\n");
        מפרשפקודות.לבצע_פקודה();
    }
}
