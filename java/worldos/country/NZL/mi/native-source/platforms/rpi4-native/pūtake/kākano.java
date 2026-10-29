// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kākano {
    static int[] 작업횟수 = new int[3];
    static int[] tūmahi_SUM = new int[3];
    static int tūmahi_whakaraupapa;
    static int tūmahi_hapa;
    static int 난수씨 = 17;

    static void manatoko(boolean here, int INDEX) {
        if (!here) { 단말.Tuhia("FAIL "); 단말.수(INDEX); papa.Whakamutua(INDEX); }
    }
    static int peka(int uara) {
        switch (uara) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int uara) {
        switch (uara) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] HUĀNGA_uara) { return HUĀNGA_uara; }
    static void 계산시험() {
        int uara = 난수씨;
        manatoko(uara * 7 - uara == 102 && uara / 3 == 5 && uara % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        manatoko(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        manatoko(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        manatoko((-uara >> 2) == -5 && (-uara >>> 2) == 1073741819 && (uara << 33) == 34, 4);
        manatoko((byte)(uara * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] HUĀNGA_uara = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < HUĀNGA_uara.length; Loop_INDEX++) HUĀNGA_uara[Loop_INDEX] = Loop_INDEX * uara;
        HUĀNGA_uara[2]++;
        manatoko(배열돌려주기(HUĀNGA_uara) == HUĀNGA_uara && HUĀNGA_uara[2] == 35 && HUĀNGA_uara[4] == 68, 6);
        manatoko(peka(uara - 117) == 7 && peka(uara - 15) == 9 && peka(uara) == 3 && 촘촘분기(uara - 15) == 17, 7);
        String Ngā_kupu = "한글 😀";
        manatoko(Ngā_kupu.length() == 5 && Ngā_kupu.charAt(0) == '한' && Ngā_kupu.charAt(3) == 0xd83d, 8);
        manatoko(papa.PTM_whakaaetanga_taumata() == 1, 9);
        단말.Tuhia("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_PTM 전후 paetata_whānuitanga 변수가 보존되는지 검사: 각 작업은 독립된 mīhini 스택을 쓴다.
        int paetata_uara = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (tūmahi_whakaraupapa % 2 + 1 != INDEX) tūmahi_hapa++;
            tūmahi_whakaraupapa++;
            paetata_uara += Loop_INDEX + INDEX;
            tūmahi_SUM[INDEX] = paetata_uara;
            작업횟수[INDEX]++;
            papa.YIELD_PTM();
            if (paetata_uara != tūmahi_SUM[INDEX]) tūmahi_hapa++;
        }
    }
    static void 작업시험() {
        tūmahi_whakaraupapa = 0; tūmahi_hapa = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        manatoko(papa.Waihanga_tūmahi(1) == 0 && papa.Waihanga_tūmahi(2) == 0, 20);
        int takahuringa_COUNT = 0;
        while (papa.tūmahi_tūnga(1) != 0 || papa.tūmahi_tūnga(2) != 0) {
            papa.YIELD_PTM();
            manatoko(++takahuringa_COUNT < 100, 21);
        }
        manatoko(작업횟수[1] == 10 && 작업횟수[2] == 10 && tūmahi_whakaraupapa == 20 && tūmahi_hapa == 0, 22);
        manatoko(tūmahi_SUM[1] == 155 && tūmahi_SUM[2] == 265, 23);
        단말.Tuhia("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int Poutū_tūranga, int 너비, int 높이, int 색) {
        for (int 세로좌표 = Poutū_tūranga; 세로좌표 < Poutū_tūranga + 높이; 세로좌표++)
            for (int taunga_x = 가로; taunga_x < 가로 + 너비; taunga_x++) papa.화면점(taunga_x, 세로좌표, 색);
    }
    static void 화면() {
        if (papa.화면준비() == 0) { 단말.Tuhia("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, papa.화면너비(), papa.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Tuhia("FRAMEBUFFER PASS "); 단말.수(papa.화면너비()); 단말.문자('x');
        단말.수(papa.화면높이()); 단말.Tuhia(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int mēhua = papa.씨플러스시험();
        manatoko(mēhua == 0, 100 + mēhua);
        단말.Tuhia("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        manatoko(papa.taki_kaiwhakamahi_kaupapa() == 0, 200);
        단말.Tuhia("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = papa.whakahaere_kaiwhakamahi_kaupapa(0);
        if (처음결과 != 0) { 단말.Tuhia("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        manatoko(처음결과 == 0, 201);
        단말.Tuhia("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Tuhia("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int mēhua = papa.whakahaere_kaiwhakamahi_kaupapa(INDEX + 1);
            if (mēhua != 예상[INDEX]) { 단말.Tuhia("USER RESULT "); 단말.수(mēhua); 단말.문자(10); }
            manatoko(mēhua == 예상[INDEX], 210 + INDEX);
        }
        manatoko(papa.whakahaere_kaiwhakamahi_kaupapa(0) == 0, 220);
        단말.Tuhia("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int mēhua = papa.whakahaere_kaiwhakamahi_kaupapa(9);
        if (mēhua != 0) { 단말.Tuhia("UDP RESULT "); 단말.수(mēhua); 단말.문자(10); }
        manatoko(mēhua == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Tuhia("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Tuhia("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Tuhia("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Tuhia("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Tuhia("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void whakahaere() {
        단말.Tuhia("WorldOS mi · mi · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Tuhia("NATIVE READY\n");
        명령해석기.kawe_tono();
    }
}
