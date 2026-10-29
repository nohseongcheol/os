// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class јадро {
    static int[] 작업횟수 = new int[3];
    static int[] задача_SUM = new int[3];
    static int задача_редослед;
    static int задача_грешка;
    static int 난수씨 = 17;

    static void провери(boolean услов, int INDEX) {
        if (!услов) { 단말.Запиши("FAIL "); 단말.수(INDEX); табла.Стоп(INDEX); }
    }
    static int гранка(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] низа_VALUE) { return низа_VALUE; }
    static void 계산시험() {
        int VALUE = 난수씨;
        провери(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        провери(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        провери(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        провери((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        провери((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] низа_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < низа_VALUE.length; Loop_INDEX++) низа_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        низа_VALUE[2]++;
        провери(배열돌려주기(низа_VALUE) == низа_VALUE && низа_VALUE[2] == 35 && низа_VALUE[4] == 68, 6);
        провери(гранка(VALUE - 117) == 7 && гранка(VALUE - 15) == 9 && гранка(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Текст = "한글 😀";
        провери(Текст.length() == 5 && Текст.charAt(0) == '한' && Текст.charAt(3) == 0xd83d, 8);
        провери(табла.ЦПУ_дозвола_ниво() == 1, 9);
        단말.Запиши("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_ЦПУ 전후 локален_обем 변수가 보존되는지 검사: 각 작업은 독립된 машина 스택을 쓴다.
        int локален_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (задача_редослед % 2 + 1 != INDEX) задача_грешка++;
            задача_редослед++;
            локален_VALUE += Loop_INDEX + INDEX;
            задача_SUM[INDEX] = локален_VALUE;
            작업횟수[INDEX]++;
            табла.YIELD_ЦПУ();
            if (локален_VALUE != задача_SUM[INDEX]) задача_грешка++;
        }
    }
    static void 작업시험() {
        задача_редослед = 0; задача_грешка = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        провери(табла.Create_задача(1) == 0 && табла.Create_задача(2) == 0, 20);
        int ротација_COUNT = 0;
        while (табла.задача_статус(1) != 0 || табла.задача_статус(2) != 0) {
            табла.YIELD_ЦПУ();
            провери(++ротација_COUNT < 100, 21);
        }
        провери(작업횟수[1] == 10 && 작업횟수[2] == 10 && задача_редослед == 20 && задача_грешка == 0, 22);
        провери(задача_SUM[1] == 155 && задача_SUM[2] == 265, 23);
        단말.Запиши("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int вертикала_позиционирање, int 너비, int 높이, int 색) {
        for (int 세로좌표 = вертикала_позиционирање; 세로좌표 < вертикала_позиционирање + 높이; 세로좌표++)
            for (int координата_х = 가로; координата_х < 가로 + 너비; координата_х++) табла.화면점(координата_х, 세로좌표, 색);
    }
    static void 화면() {
        if (табла.화면준비() == 0) { 단말.Запиши("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, табла.화면너비(), табла.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Запиши("FRAMEBUFFER PASS "); 단말.수(табла.화면너비()); 단말.문자('x');
        단말.수(табла.화면높이()); 단말.Запиши(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int мерка = табла.씨플러스시험();
        провери(мерка == 0, 100 + мерка);
        단말.Запиши("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        провери(табла.провери_корисник_програма() == 0, 200);
        단말.Запиши("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = табла.изврши_корисник_програма(0);
        if (처음결과 != 0) { 단말.Запиши("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        провери(처음결과 == 0, 201);
        단말.Запиши("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Запиши("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int мерка = табла.изврши_корисник_програма(INDEX + 1);
            if (мерка != 예상[INDEX]) { 단말.Запиши("USER RESULT "); 단말.수(мерка); 단말.문자(10); }
            провери(мерка == 예상[INDEX], 210 + INDEX);
        }
        провери(табла.изврши_корисник_програма(0) == 0, 220);
        단말.Запиши("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int мерка = табла.изврши_корисник_програма(9);
        if (мерка != 0) { 단말.Запиши("UDP RESULT "); 단말.수(мерка); 단말.문자(10); }
        провери(мерка == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Запиши("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Запиши("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Запиши("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Запиши("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Запиши("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Изврши_2() {
        단말.Запиши("WorldOS mk · Македонски · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Запиши("NATIVE READY\n");
        명령해석기.Изврши_наредба();
    }
}
