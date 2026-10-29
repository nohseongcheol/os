// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class o_zak {
    static int[] 작업횟수 = new int[3];
    static int[] vazifa_SUM = new int[3];
    static int vazifa_tartib;
    static int vazifa_xato;
    static int 난수씨 = 17;

    static void tasdiqlamoq(boolean holat, int INDEX) {
        if (!holat) { 단말.Yozish("FAIL "); 단말.수(INDEX); yozuv_taxtasi.Toʻxtatish(INDEX); }
    }
    static int shox(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] qaytarish_ARRAY(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = 난수씨;
        tasdiqlamoq(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        tasdiqlamoq(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        tasdiqlamoq(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        tasdiqlamoq((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        tasdiqlamoq((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < ARRAY_VALUE.length; Loop_INDEX++) ARRAY_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        tasdiqlamoq(qaytarish_ARRAY(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        tasdiqlamoq(shox(VALUE - 117) == 7 && shox(VALUE - 15) == 9 && shox(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Matn = "한글 😀";
        tasdiqlamoq(Matn.length() == 5 && Matn.charAt(0) == '한' && Matn.charAt(3) == 0xd83d, 8);
        tasdiqlamoq(yozuv_taxtasi.CPU_ruxsat_daraja() == 1, 9);
        단말.Yozish("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 mahalliy_soha 변수가 보존되는지 검사: 각 작업은 독립된 기계 스택을 쓴다.
        int mahalliy_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (vazifa_tartib % 2 + 1 != INDEX) vazifa_xato++;
            vazifa_tartib++;
            mahalliy_VALUE += Loop_INDEX + INDEX;
            vazifa_SUM[INDEX] = mahalliy_VALUE;
            작업횟수[INDEX]++;
            yozuv_taxtasi.YIELD_CPU();
            if (mahalliy_VALUE != vazifa_SUM[INDEX]) vazifa_xato++;
        }
    }
    static void 작업시험() {
        vazifa_tartib = 0; vazifa_xato = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        tasdiqlamoq(yozuv_taxtasi.Yaratish_vazifa(1) == 0 && yozuv_taxtasi.Yaratish_vazifa(2) == 0, 20);
        int burilish_COUNT = 0;
        while (yozuv_taxtasi.vazifa_holat(1) != 0 || yozuv_taxtasi.vazifa_holat(2) != 0) {
            yozuv_taxtasi.YIELD_CPU();
            tasdiqlamoq(++burilish_COUNT < 100, 21);
        }
        tasdiqlamoq(작업횟수[1] == 10 && 작업횟수[2] == 10 && vazifa_tartib == 20 && vazifa_xato == 0, 22);
        tasdiqlamoq(vazifa_SUM[1] == 155 && vazifa_SUM[2] == 265, 23);
        단말.Yozish("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int Vertikal_holat, int 너비, int 높이, int 색) {
        for (int Y_tugmasi_koordinat = Vertikal_holat; Y_tugmasi_koordinat < Vertikal_holat + 높이; Y_tugmasi_koordinat++)
            for (int x_koordinata = 가로; x_koordinata < 가로 + 너비; x_koordinata++) yozuv_taxtasi.화면점(x_koordinata, Y_tugmasi_koordinat, 색);
    }
    static void 화면() {
        if (yozuv_taxtasi.화면준비() == 0) { 단말.Yozish("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, yozuv_taxtasi.화면너비(), yozuv_taxtasi.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Yozish("FRAMEBUFFER PASS "); 단말.수(yozuv_taxtasi.화면너비()); 단말.문자('x');
        단말.수(yozuv_taxtasi.화면높이()); 단말.Yozish(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int o_lchov = yozuv_taxtasi.씨플러스시험();
        tasdiqlamoq(o_lchov == 0, 100 + o_lchov);
        단말.Yozish("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        tasdiqlamoq(yozuv_taxtasi.chek_foydalanuvchi_ilova() == 0, 200);
        단말.Yozish("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = yozuv_taxtasi.ishlash_foydalanuvchi_ilova(0);
        if (처음결과 != 0) { 단말.Yozish("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        tasdiqlamoq(처음결과 == 0, 201);
        단말.Yozish("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Yozish("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int o_lchov = yozuv_taxtasi.ishlash_foydalanuvchi_ilova(INDEX + 1);
            if (o_lchov != 예상[INDEX]) { 단말.Yozish("USER RESULT "); 단말.수(o_lchov); 단말.문자(10); }
            tasdiqlamoq(o_lchov == 예상[INDEX], 210 + INDEX);
        }
        tasdiqlamoq(yozuv_taxtasi.ishlash_foydalanuvchi_ilova(0) == 0, 220);
        단말.Yozish("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int o_lchov = yozuv_taxtasi.ishlash_foydalanuvchi_ilova(9);
        if (o_lchov != 0) { 단말.Yozish("UDP RESULT "); 단말.수(o_lchov); 단말.문자(10); }
        tasdiqlamoq(o_lchov == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Yozish("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Yozish("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Yozish("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Yozish("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Yozish("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Bajarish() {
        단말.Yozish("WorldOS uz_Latn · Uzbek · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Yozish("NATIVE READY\n");
        명령해석기.bajarmoq_buyruq();
    }
}
