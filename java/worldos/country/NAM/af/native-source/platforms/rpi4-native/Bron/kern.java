// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kern {
    static int[] 작업횟수 = new int[3];
    static int[] taak_SUM = new int[3];
    static int taak_volgorde;
    static int taak_fout;
    static int 난수씨 = 17;

    static void verifieer(boolean toestand, int INDEX) {
        if (!toestand) { 단말.Skryf("FAIL "); 단말.수(INDEX); bord.Stop(INDEX); }
    }
    static int tak(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] teruggee_ARRAY(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = 난수씨;
        verifieer(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        verifieer(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        verifieer(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        verifieer((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        verifieer((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int lus_INDEX = 0; lus_INDEX < ARRAY_VALUE.length; lus_INDEX++) ARRAY_VALUE[lus_INDEX] = lus_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        verifieer(teruggee_ARRAY(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        verifieer(tak(VALUE - 117) == 7 && tak(VALUE - 15) == 9 && tak(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Teks = "한글 😀";
        verifieer(Teks.length() == 5 && Teks.charAt(0) == '한' && Teks.charAt(3) == 0xd83d, 8);
        verifieer(bord.SVE_toestemming_vlak() == 1, 9);
        단말.Skryf("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_SVE 전후 lokaal_bestek 변수가 보존되는지 검사: 각 작업은 독립된 masjien 스택을 쓴다.
        int lokaal_VALUE = INDEX * 100;
        for (int lus_INDEX = 0; lus_INDEX < 10; lus_INDEX++) {
            if (taak_volgorde % 2 + 1 != INDEX) taak_fout++;
            taak_volgorde++;
            lokaal_VALUE += lus_INDEX + INDEX;
            taak_SUM[INDEX] = lokaal_VALUE;
            작업횟수[INDEX]++;
            bord.YIELD_SVE();
            if (lokaal_VALUE != taak_SUM[INDEX]) taak_fout++;
        }
    }
    static void 작업시험() {
        taak_volgorde = 0; taak_fout = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        verifieer(bord.Skep_taak(1) == 0 && bord.Skep_taak(2) == 0, 20);
        int vingerrotasie_COUNT = 0;
        while (bord.taak_stand(1) != 0 || bord.taak_stand(2) != 0) {
            bord.YIELD_SVE();
            verifieer(++vingerrotasie_COUNT < 100, 21);
        }
        verifieer(작업횟수[1] == 10 && 작업횟수[2] == 10 && taak_volgorde == 20 && taak_fout == 0, 22);
        verifieer(taak_SUM[1] == 155 && taak_SUM[2] == 265, 23);
        단말.Skryf("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int Vertikaal_plaas, int 너비, int 높이, int 색) {
        for (int Y_koördinaat = Vertikaal_plaas; Y_koördinaat < Vertikaal_plaas + 높이; Y_koördinaat++)
            for (int x_koördinaat = 가로; x_koördinaat < 가로 + 너비; x_koördinaat++) bord.화면점(x_koördinaat, Y_koördinaat, 색);
    }
    static void 화면() {
        if (bord.화면준비() == 0) { 단말.Skryf("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, bord.화면너비(), bord.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Skryf("FRAMEBUFFER PASS "); 단말.수(bord.화면너비()); 단말.문자('x');
        단말.수(bord.화면높이()); 단말.Skryf(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int maatreël = bord.씨플러스시험();
        verifieer(maatreël == 0, 100 + maatreël);
        단말.Skryf("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        verifieer(bord.tjek_gebruiker_program() == 0, 200);
        단말.Skryf("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = bord.ry_gebruiker_program(0);
        if (처음결과 != 0) { 단말.Skryf("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        verifieer(처음결과 == 0, 201);
        단말.Skryf("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Skryf("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int maatreël = bord.ry_gebruiker_program(INDEX + 1);
            if (maatreël != 예상[INDEX]) { 단말.Skryf("USER RESULT "); 단말.수(maatreël); 단말.문자(10); }
            verifieer(maatreël == 예상[INDEX], 210 + INDEX);
        }
        verifieer(bord.ry_gebruiker_program(0) == 0, 220);
        단말.Skryf("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int maatreël = bord.ry_gebruiker_program(9);
        if (maatreël != 0) { 단말.Skryf("UDP RESULT "); 단말.수(maatreël); 단말.문자(10); }
        verifieer(maatreël == 0, 230);
    }
    static void Stelselinfo() {
        단말.Skryf("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Skryf("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Skryf("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Skryf("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Skryf("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Loop() {
        단말.Skryf("WorldOS af · af · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Skryf("NATIVE READY\n");
        명령해석기.uitvoer_bevel();
    }
}
