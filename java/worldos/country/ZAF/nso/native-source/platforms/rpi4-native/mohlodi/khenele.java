// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class khenele {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int mošomo_thulaganyo;
    static int mošomo_phošo;
    static int 난수씨 = 17;

    static void kgonthiša(boolean seemo, int lokela) {
        if (!seemo) { 단말.Ngwala("FAIL "); 단말.수(lokela); 보드.Emiša(lokela); }
    }
    static int lekala(int boleng) {
        switch (boleng) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int boleng) {
        switch (boleng) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] arei_boleng) { return arei_boleng; }
    static void 계산시험() {
        int boleng = 난수씨;
        kgonthiša(boleng * 7 - boleng == 102 && boleng / 3 == 5 && boleng % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        kgonthiša(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        kgonthiša(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        kgonthiša((-boleng >> 2) == -5 && (-boleng >>> 2) == 1073741819 && (boleng << 33) == 34, 4);
        kgonthiša((byte)(boleng * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] arei_boleng = new int[5];
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < arei_boleng.length; ditaelopoeletšwa_lokela++) arei_boleng[ditaelopoeletšwa_lokela] = ditaelopoeletšwa_lokela * boleng;
        arei_boleng[2]++;
        kgonthiša(배열돌려주기(arei_boleng) == arei_boleng && arei_boleng[2] == 35 && arei_boleng[4] == 68, 6);
        kgonthiša(lekala(boleng - 117) == 7 && lekala(boleng - 15) == 9 && lekala(boleng) == 3 && 촘촘분기(boleng - 15) == 17, 7);
        String Sengwalwa = "한글 😀";
        kgonthiša(Sengwalwa.length() == 5 && Sengwalwa.charAt(0) == '한' && Sengwalwa.charAt(3) == 0xd83d, 8);
        kgonthiša(보드.CPU_tumelelo_kgato() == 1, 9);
        단말.Ngwala("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int lokela) {
        // e_thibetšwe_CPU 전후 kgauswi_skoupo 변수가 보존되는지 검사: 각 작업은 독립된 motšhene 스택을 쓴다.
        int kgauswi_boleng = lokela * 100;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 10; ditaelopoeletšwa_lokela++) {
            if (mošomo_thulaganyo % 2 + 1 != lokela) mošomo_phošo++;
            mošomo_thulaganyo++;
            kgauswi_boleng += ditaelopoeletšwa_lokela + lokela;
            작업합[lokela] = kgauswi_boleng;
            작업횟수[lokela]++;
            보드.e_thibetšwe_CPU();
            if (kgauswi_boleng != 작업합[lokela]) mošomo_phošo++;
        }
    }
    static void 작업시험() {
        mošomo_thulaganyo = 0; mošomo_phošo = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        kgonthiša(보드.작업만들기(1) == 0 && 보드.작업만들기(2) == 0, 20);
        int 회전 = 0;
        while (보드.mošomo_boemo(1) != 0 || 보드.mošomo_boemo(2) != 0) {
            보드.e_thibetšwe_CPU();
            kgonthiša(++회전 < 100, 21);
        }
        kgonthiša(작업횟수[1] == 10 && 작업횟수[2] == 10 && mošomo_thulaganyo == 20 && mošomo_phošo == 0, 22);
        kgonthiša(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.Ngwala("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int 세로좌표 = 세로; 세로좌표 < 세로 + 높이; 세로좌표++)
            for (int kamano_ya_x = 가로; kamano_ya_x < 가로 + 너비; kamano_ya_x++) 보드.화면점(kamano_ya_x, 세로좌표, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.Ngwala("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Ngwala("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.Ngwala(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        kgonthiša(결과 == 0, 100 + 결과);
        단말.Ngwala("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        kgonthiša(보드.lekola_mošomiši_tirišo() == 0, 200);
        단말.Ngwala("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.sepetša_mošomiši_tirišo(0);
        if (처음결과 != 0) { 단말.Ngwala("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        kgonthiša(처음결과 == 0, 201);
        단말.Ngwala("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int lokela = 0; lokela < 예상.length; lokela++) {
            단말.Ngwala("USER CHECK "); 단말.수(lokela); 단말.문자(10);
            int 결과 = 보드.sepetša_mošomiši_tirišo(lokela + 1);
            if (결과 != 예상[lokela]) { 단말.Ngwala("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            kgonthiša(결과 == 예상[lokela], 210 + lokela);
        }
        kgonthiša(보드.sepetša_mošomiši_tirišo(0) == 0, 220);
        단말.Ngwala("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.sepetša_mošomiši_tirišo(9);
        if (결과 != 0) { 단말.Ngwala("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        kgonthiša(결과 == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Ngwala("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Ngwala("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Ngwala("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Ngwala("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Ngwala("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Diriša() {
        단말.Ngwala("WorldOS nso · nso · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Ngwala("NATIVE READY\n");
        명령해석기.phethagatša_taelo();
    }
}
