// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kánẹ́ẹ̀lì {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int iṣẹ́_ìtodátà;
    static int iṣẹ́_àṣìṣe;
    static int 난수씨 = 17;

    static void ridájú(boolean kání, int wá_atọ̀ka_àkóónú) {
        if (!kání) { 단말.Kọ("FAIL "); 단말.수(wá_atọ̀ka_àkóónú); 보드.Dúró(wá_atọ̀ka_àkóónú); }
    }
    static int ẹ̀ka(int iye) {
        switch (iye) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int iye) {
        switch (iye) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] ÀRÉÈ_iye) { return ÀRÉÈ_iye; }
    static void 계산시험() {
        int iye = 난수씨;
        ridájú(iye * 7 - iye == 102 && iye / 3 == 5 && iye % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        ridájú(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        ridájú(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        ridájú((-iye >> 2) == -5 && (-iye >>> 2) == 1073741819 && (iye << 33) == 34, 4);
        ridájú((byte)(iye * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ÀRÉÈ_iye = new int[5];
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < ÀRÉÈ_iye.length; ṣetúnṣe_wá_atọ̀ka_àkóónú++) ÀRÉÈ_iye[ṣetúnṣe_wá_atọ̀ka_àkóónú] = ṣetúnṣe_wá_atọ̀ka_àkóónú * iye;
        ÀRÉÈ_iye[2]++;
        ridájú(배열돌려주기(ÀRÉÈ_iye) == ÀRÉÈ_iye && ÀRÉÈ_iye[2] == 35 && ÀRÉÈ_iye[4] == 68, 6);
        ridájú(ẹ̀ka(iye - 117) == 7 && ẹ̀ka(iye - 15) == 9 && ẹ̀ka(iye) == 3 && 촘촘분기(iye - 15) == 17, 7);
        String SMS = "한글 😀";
        ridájú(SMS.length() == 5 && SMS.charAt(0) == '한' && SMS.charAt(3) == 0xd83d, 8);
        ridájú(보드.CPU_ìgbaniláàyè_ìpele() == 1, 9);
        단말.Kọ("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int wá_atọ̀ka_àkóónú) {
        // ti_dádúró_díẹ̀_CPU 전후 agbègbè_sàkání 변수가 보존되는지 검사: 각 작업은 독립된 maṣíìnì 스택을 쓴다.
        int agbègbè_iye = wá_atọ̀ka_àkóónú * 100;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 10; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
            if (iṣẹ́_ìtodátà % 2 + 1 != wá_atọ̀ka_àkóónú) iṣẹ́_àṣìṣe++;
            iṣẹ́_ìtodátà++;
            agbègbè_iye += ṣetúnṣe_wá_atọ̀ka_àkóónú + wá_atọ̀ka_àkóónú;
            작업합[wá_atọ̀ka_àkóónú] = agbègbè_iye;
            작업횟수[wá_atọ̀ka_àkóónú]++;
            보드.ti_dádúró_díẹ̀_CPU();
            if (agbègbè_iye != 작업합[wá_atọ̀ka_àkóónú]) iṣẹ́_àṣìṣe++;
        }
    }
    static void 작업시험() {
        iṣẹ́_ìtodátà = 0; iṣẹ́_àṣìṣe = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        ridájú(보드.Ṣẹ̀dá_iṣẹ́(1) == 0 && 보드.Ṣẹ̀dá_iṣẹ́(2) == 0, 20);
        int 회전 = 0;
        while (보드.iṣẹ́_ipò(1) != 0 || 보드.iṣẹ́_ipò(2) != 0) {
            보드.ti_dádúró_díẹ̀_CPU();
            ridájú(++회전 < 100, 21);
        }
        ridájú(작업횟수[1] == 10 && 작업횟수[2] == 10 && iṣẹ́_ìtodátà == 20 && iṣẹ́_àṣìṣe == 0, 22);
        ridájú(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.Kọ("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int 세로좌표 = 세로; 세로좌표 < 세로 + 높이; 세로좌표++)
            for (int ibi_ìtọ́kasí_x = 가로; ibi_ìtọ́kasí_x < 가로 + 너비; ibi_ìtọ́kasí_x++) 보드.화면점(ibi_ìtọ́kasí_x, 세로좌표, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.Kọ("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Kọ("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.Kọ(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        ridájú(결과 == 0, 100 + 결과);
        단말.Kọ("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        ridájú(보드.ṣàyẹ̀wò_aṣàmúlò_àtòjọ_ètò() == 0, 200);
        단말.Kọ("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.ṣiṣẹ́_aṣàmúlò_àtòjọ_ètò(0);
        if (처음결과 != 0) { 단말.Kọ("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        ridájú(처음결과 == 0, 201);
        단말.Kọ("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 예상.length; wá_atọ̀ka_àkóónú++) {
            단말.Kọ("USER CHECK "); 단말.수(wá_atọ̀ka_àkóónú); 단말.문자(10);
            int 결과 = 보드.ṣiṣẹ́_aṣàmúlò_àtòjọ_ètò(wá_atọ̀ka_àkóónú + 1);
            if (결과 != 예상[wá_atọ̀ka_àkóónú]) { 단말.Kọ("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            ridájú(결과 == 예상[wá_atọ̀ka_àkóónú], 210 + wá_atọ̀ka_àkóónú);
        }
        ridájú(보드.ṣiṣẹ́_aṣàmúlò_àtòjọ_ètò(0) == 0, 220);
        단말.Kọ("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.ṣiṣẹ́_aṣàmúlò_àtòjọ_ètò(9);
        if (결과 != 0) { 단말.Kọ("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        ridájú(결과 == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Kọ("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Kọ("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Kọ("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Kọ("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Kọ("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Rọ́ọ̀nù() {
        단말.Kọ("WorldOS yo · yo · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Kọ("NATIVE READY\n");
        명령해석기.ṣiṣẹ́_àṣẹ();
    }
}
