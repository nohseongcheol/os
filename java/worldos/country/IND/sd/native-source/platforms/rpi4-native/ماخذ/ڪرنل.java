// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class ڪرنل {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int ٽاسڪ_ترتيب;
    static int ٽاسڪ_نقص;
    static int 난수씨 = 17;

    static void تصديق_ڪريو(boolean حالت, int ابتدائي) {
        if (!حالت) { 단말.لکو("FAIL "); 단말.수(ابتدائي); 보드.روڪيو(ابتدائي); }
    }
    static int شاخ(int قدر) {
        switch (قدر) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int قدر) {
        switch (قدر) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] ترتيب_قدر_ed437109) { return ترتيب_قدر_ed437109; }
    static void 계산시험() {
        int قدر = 난수씨;
        تصديق_ڪريو(قدر * 7 - قدر == 102 && قدر / 3 == 5 && قدر % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        تصديق_ڪريو(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        تصديق_ڪريو(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        تصديق_ڪريو((-قدر >> 2) == -5 && (-قدر >>> 2) == 1073741819 && (قدر << 33) == 34, 4);
        تصديق_ڪريو((byte)(قدر * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ترتيب_قدر_ed437109 = new int[5];
        for (int لوپ_ابتدائي = 0; لوپ_ابتدائي < ترتيب_قدر_ed437109.length; لوپ_ابتدائي++) ترتيب_قدر_ed437109[لوپ_ابتدائي] = لوپ_ابتدائي * قدر;
        ترتيب_قدر_ed437109[2]++;
        تصديق_ڪريو(배열돌려주기(ترتيب_قدر_ed437109) == ترتيب_قدر_ed437109 && ترتيب_قدر_ed437109[2] == 35 && ترتيب_قدر_ed437109[4] == 68, 6);
        تصديق_ڪريو(شاخ(قدر - 117) == 7 && شاخ(قدر - 15) == 9 && شاخ(قدر) == 3 && 촘촘분기(قدر - 15) == 17, 7);
        String متن = "한글 😀";
        تصديق_ڪريو(متن.length() == 5 && متن.charAt(0) == '한' && متن.charAt(3) == 0xd83d, 8);
        تصديق_ڪريو(보드.시피유권한() == 1, 9);
        단말.لکو("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int ابتدائي) {
        // معطل_ڪريو_عمل_ڪار 전후 مقامي_اسڪوپ 변수가 보존되는지 검사: 각 작업은 독립된 مشين 스택을 쓴다.
        int مقامي_قدر = ابتدائي * 100;
        for (int لوپ_ابتدائي = 0; لوپ_ابتدائي < 10; لوپ_ابتدائي++) {
            if (ٽاسڪ_ترتيب % 2 + 1 != ابتدائي) ٽاسڪ_نقص++;
            ٽاسڪ_ترتيب++;
            مقامي_قدر += لوپ_ابتدائي + ابتدائي;
            작업합[ابتدائي] = مقامي_قدر;
            작업횟수[ابتدائي]++;
            보드.معطل_ڪريو_عمل_ڪار();
            if (مقامي_قدر != 작업합[ابتدائي]) ٽاسڪ_نقص++;
        }
    }
    static void 작업시험() {
        ٽاسڪ_ترتيب = 0; ٽاسڪ_نقص = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        تصديق_ڪريو(보드.ٺاھيو_ٽاسڪ(1) == 0 && 보드.ٺاھيو_ٽاسڪ(2) == 0, 20);
        int 회전 = 0;
        while (보드.ٽاسڪ_حالت(1) != 0 || 보드.ٽاسڪ_حالت(2) != 0) {
            보드.معطل_ڪريو_عمل_ڪار();
            تصديق_ڪريو(++회전 < 100, 21);
        }
        تصديق_ڪريو(작업횟수[1] == 10 && 작업횟수[2] == 10 && ٽاسڪ_ترتيب == 20 && ٽاسڪ_نقص == 0, 22);
        تصديق_ڪريو(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.لکو("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int 세로좌표 = 세로; 세로좌표 < 세로 + 높이; 세로좌표++)
            for (int x_رطبو = 가로; x_رطبو < 가로 + 너비; x_رطبو++) 보드.화면점(x_رطبو, 세로좌표, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.لکو("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.لکو("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.لکو(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        تصديق_ڪريو(결과 == 0, 100 + 결과);
        단말.لکو("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        تصديق_ڪريو(보드.پڙتال_ڪريو_صارف_ائپ() == 0, 200);
        단말.لکو("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.هلائڻ_صارف_ائپ(0);
        if (처음결과 != 0) { 단말.لکو("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        تصديق_ڪريو(처음결과 == 0, 201);
        단말.لکو("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int ابتدائي = 0; ابتدائي < 예상.length; ابتدائي++) {
            단말.لکو("USER CHECK "); 단말.수(ابتدائي); 단말.문자(10);
            int 결과 = 보드.هلائڻ_صارف_ائپ(ابتدائي + 1);
            if (결과 != 예상[ابتدائي]) { 단말.لکو("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            تصديق_ڪريو(결과 == 예상[ابتدائي], 210 + ابتدائي);
        }
        تصديق_ڪريو(보드.هلائڻ_صارف_ائپ(0) == 0, 220);
        단말.لکو("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.هلائڻ_صارف_ائپ(9);
        if (결과 != 0) { 단말.لکو("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        تصديق_ڪريو(결과 == 0, 230);
    }
    static void سسٽم_معلومات() {
        단말.لکو("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.لکو("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.لکو("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.لکو("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.لکو("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void هلائڻ() {
        단말.لکو("WorldOS sd · sd · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.لکو("NATIVE READY\n");
        명령해석기.تعميل_ڪرڻ_حڪم();
    }
}
