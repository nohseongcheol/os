// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class mkpụrụobī_kọmpùta {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int ọrụ_ùsòrò;
    static int ọrụ_mmejọ;
    static int 난수씨 = 17;

    static void nkwàdo_eziokwū(boolean ọnọdụ, int indèks) {
        if (!ọnọdụ) { 단말.Chekwaa_ozi("FAIL "); 단말.수(indèks); 보드.Kwụsị(indèks); }
    }
    static int ogbè(int valuu) {
        switch (valuu) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int valuu) {
        switch (valuu) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] MKPOKỌTA_valuu) { return MKPOKỌTA_valuu; }
    static void 계산시험() {
        int valuu = 난수씨;
        nkwàdo_eziokwū(valuu * 7 - valuu == 102 && valuu / 3 == 5 && valuu % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        nkwàdo_eziokwū(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        nkwàdo_eziokwū(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        nkwàdo_eziokwū((-valuu >> 2) == -5 && (-valuu >>> 2) == 1073741819 && (valuu << 33) == 34, 4);
        nkwàdo_eziokwū((byte)(valuu * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] MKPOKỌTA_valuu = new int[5];
        for (int memmenwè_indèks = 0; memmenwè_indèks < MKPOKỌTA_valuu.length; memmenwè_indèks++) MKPOKỌTA_valuu[memmenwè_indèks] = memmenwè_indèks * valuu;
        MKPOKỌTA_valuu[2]++;
        nkwàdo_eziokwū(배열돌려주기(MKPOKỌTA_valuu) == MKPOKỌTA_valuu && MKPOKỌTA_valuu[2] == 35 && MKPOKỌTA_valuu[4] == 68, 6);
        nkwàdo_eziokwū(ogbè(valuu - 117) == 7 && ogbè(valuu - 15) == 9 && ogbè(valuu) == 3 && 촘촘분기(valuu - 15) == 17, 7);
        String SMS = "한글 😀";
        nkwàdo_eziokwū(SMS.length() == 5 && SMS.charAt(0) == '한' && SMS.charAt(3) == 0xd83d, 8);
        nkwàdo_eziokwū(보드.CPU_ikikere_làrìì() == 1, 9);
        단말.Chekwaa_ozi("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int indèks) {
        // kwụsịtụ_CPU 전후 otù_ebe_ọgba 변수가 보존되는지 검사: 각 작업은 독립된 ngwa_komputa 스택을 쓴다.
        int otù_ebe_valuu = indèks * 100;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 10; memmenwè_indèks++) {
            if (ọrụ_ùsòrò % 2 + 1 != indèks) ọrụ_mmejọ++;
            ọrụ_ùsòrò++;
            otù_ebe_valuu += memmenwè_indèks + indèks;
            작업합[indèks] = otù_ebe_valuu;
            작업횟수[indèks]++;
            보드.kwụsịtụ_CPU();
            if (otù_ebe_valuu != 작업합[indèks]) ọrụ_mmejọ++;
        }
    }
    static void 작업시험() {
        ọrụ_ùsòrò = 0; ọrụ_mmejọ = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        nkwàdo_eziokwū(보드.mepụta_ọrụ(1) == 0 && 보드.mepụta_ọrụ(2) == 0, 20);
        int 회전 = 0;
        while (보드.ọrụ_ọnọdụ(1) != 0 || 보드.ọrụ_ọnọdụ(2) != 0) {
            보드.kwụsịtụ_CPU();
            nkwàdo_eziokwū(++회전 < 100, 21);
        }
        nkwàdo_eziokwū(작업횟수[1] == 10 && 작업횟수[2] == 10 && ọrụ_ùsòrò == 20 && ọrụ_mmejọ == 0, 22);
        nkwàdo_eziokwū(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.Chekwaa_ozi("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int 세로좌표 = 세로; 세로좌표 < 세로 + 높이; 세로좌표++)
            for (int ngakọrịta_x = 가로; ngakọrịta_x < 가로 + 너비; ngakọrịta_x++) 보드.화면점(ngakọrịta_x, 세로좌표, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.Chekwaa_ozi("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.Chekwaa_ozi("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.Chekwaa_ozi(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        nkwàdo_eziokwū(결과 == 0, 100 + 결과);
        단말.Chekwaa_ozi("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        nkwàdo_eziokwū(보드.cheèk_òjìàrụ_app() == 0, 200);
        단말.Chekwaa_ozi("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.mee_òjìàrụ_app(0);
        if (처음결과 != 0) { 단말.Chekwaa_ozi("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        nkwàdo_eziokwū(처음결과 == 0, 201);
        단말.Chekwaa_ozi("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int indèks = 0; indèks < 예상.length; indèks++) {
            단말.Chekwaa_ozi("USER CHECK "); 단말.수(indèks); 단말.문자(10);
            int 결과 = 보드.mee_òjìàrụ_app(indèks + 1);
            if (결과 != 예상[indèks]) { 단말.Chekwaa_ozi("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            nkwàdo_eziokwū(결과 == 예상[indèks], 210 + indèks);
        }
        nkwàdo_eziokwū(보드.mee_òjìàrụ_app(0) == 0, 220);
        단말.Chekwaa_ozi("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.mee_òjìàrụ_app(9);
        if (결과 != 0) { 단말.Chekwaa_ozi("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        nkwàdo_eziokwū(결과 == 0, 230);
    }
    static void Ozi_Sistèm() {
        단말.Chekwaa_ozi("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Chekwaa_ozi("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Chekwaa_ozi("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Chekwaa_ozi("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Chekwaa_ozi("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Bido() {
        단말.Chekwaa_ozi("WorldOS ig · ig · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.Chekwaa_ozi("NATIVE READY\n");
        명령해석기.mee_nnyemiwu();
    }
}
