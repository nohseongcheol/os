// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class keetnerü {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int aa_innajatü_anaajiaakua_ipa;
    static int aa_innajatü_ajachitia;
    static int 난수씨 = 17;

    static void 확인(boolean mülein, int ee_iyatialujuna) {
        if (!mülein) { 단말.ashajaa("FAIL "); 단말.수(ee_iyatialujuna); 보드.eimale_eraa(ee_iyatialujuna); }
    }
    static int 분기(int ajutuu) {
        switch (ajutuu) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int ajutuu) {
        switch (ajutuu) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] matüriisü_ajutuu) { return matüriisü_ajutuu; }
    static void 계산시험() {
        int ajutuu = 난수씨;
        확인(ajutuu * 7 - ajutuu == 102 && ajutuu / 3 == 5 && ajutuu % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        확인(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        확인(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        확인((-ajutuu >> 2) == -5 && (-ajutuu >>> 2) == 1073741819 && (ajutuu << 33) == 34, 4);
        확인((byte)(ajutuu * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] matüriisü_ajutuu = new int[5];
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < matüriisü_ajutuu.length; eitawaakualü_ee_iyatialujuna++) matüriisü_ajutuu[eitawaakualü_ee_iyatialujuna] = eitawaakualü_ee_iyatialujuna * ajutuu;
        matüriisü_ajutuu[2]++;
        확인(배열돌려주기(matüriisü_ajutuu) == matüriisü_ajutuu && matüriisü_ajutuu[2] == 35 && matüriisü_ajutuu[4] == 68, 6);
        확인(분기(ajutuu - 117) == 7 && 분기(ajutuu - 15) == 9 && 분기(ajutuu) == 3 && 촘촘분기(ajutuu - 15) == 17, 7);
        String 글 = "한글 😀";
        확인(글.length() == 5 && 글.charAt(0) == '한' && 글.charAt(3) == 0xd83d, 8);
        확인(보드.시피유권한() == 1, 9);
        단말.ashajaa("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int ee_iyatialujuna) {
        // 양보 전후 지역 변수가 보존되는지 검사: 각 작업은 독립된 기계 스택을 쓴다.
        int 지역값 = ee_iyatialujuna * 100;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 10; eitawaakualü_ee_iyatialujuna++) {
            if (aa_innajatü_anaajiaakua_ipa % 2 + 1 != ee_iyatialujuna) aa_innajatü_ajachitia++;
            aa_innajatü_anaajiaakua_ipa++;
            지역값 += eitawaakualü_ee_iyatialujuna + ee_iyatialujuna;
            작업합[ee_iyatialujuna] = 지역값;
            작업횟수[ee_iyatialujuna]++;
            보드.양보();
            if (지역값 != 작업합[ee_iyatialujuna]) aa_innajatü_ajachitia++;
        }
    }
    static void 작업시험() {
        aa_innajatü_anaajiaakua_ipa = 0; aa_innajatü_ajachitia = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        확인(보드.작업만들기(1) == 0 && 보드.작업만들기(2) == 0, 20);
        int 회전 = 0;
        while (보드.aa_innajatü_jamakua_iparülein(1) != 0 || 보드.aa_innajatü_jamakua_iparülein(2) != 0) {
            보드.양보();
            확인(++회전 < 100, 21);
        }
        확인(작업횟수[1] == 10 && 작업횟수[2] == 10 && aa_innajatü_anaajiaakua_ipa == 20 && aa_innajatü_ajachitia == 0, 22);
        확인(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.ashajaa("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int 세로좌표 = 세로; 세로좌표 < 세로 + 높이; 세로좌표++)
            for (int 가로좌표 = 가로; 가로좌표 < 가로 + 너비; 가로좌표++) 보드.화면점(가로좌표, 세로좌표, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.ashajaa("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.ashajaa("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.ashajaa(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        확인(결과 == 0, 100 + 결과);
        단말.ashajaa("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        확인(보드.cheeke_ka_yataayakalü_akumajiaa() == 0, 200);
        단말.ashajaa("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.사용자실행(0);
        if (처음결과 != 0) { 단말.ashajaa("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        확인(처음결과 == 0, 201);
        단말.ashajaa("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 예상.length; ee_iyatialujuna++) {
            단말.ashajaa("USER CHECK "); 단말.수(ee_iyatialujuna); 단말.문자(10);
            int 결과 = 보드.사용자실행(ee_iyatialujuna + 1);
            if (결과 != 예상[ee_iyatialujuna]) { 단말.ashajaa("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            확인(결과 == 예상[ee_iyatialujuna], 210 + ee_iyatialujuna);
        }
        확인(보드.사용자실행(0) == 0, 220);
        단말.ashajaa("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.사용자실행(9);
        if (결과 != 0) { 단말.ashajaa("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        확인(결과 == 0, 230);
    }
    static void 정보() {
        단말.ashajaa("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.ashajaa("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.ashajaa("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.ashajaa("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.ashajaa("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void 시작() {
        단말.ashajaa("WorldOS guc · guc · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.ashajaa("NATIVE READY\n");
        명령해석기.실행();
    }
}
