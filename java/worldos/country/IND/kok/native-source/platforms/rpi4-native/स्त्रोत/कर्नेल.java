// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class कर्नेल {
    static int[] 작업횟수 = new int[3];
    static int[] कार्य_SUM = new int[3];
    static int कार्य_क्रम;
    static int कार्य_चूक;
    static int 난수씨 = 17;

    static void पुनर्तपासणी_करची(boolean स्थिती_291ac971, int INDEX) {
        if (!स्थिती_291ac971) { 단말.बरोवचें("FAIL "); 단말.수(INDEX); बोर्ड.थांबचें(INDEX); }
    }
    static int शाखा(int मोल) {
        switch (मोल) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int मोल) {
        switch (मोल) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] return_क्रम(int[] क्रम_मोल_ed437109) { return क्रम_मोल_ed437109; }
    static void 계산시험() {
        int मोल = 난수씨;
        पुनर्तपासणी_करची(मोल * 7 - मोल == 102 && मोल / 3 == 5 && मोल % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        पुनर्तपासणी_करची(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        पुनर्तपासणी_करची(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        पुनर्तपासणी_करची((-मोल >> 2) == -5 && (-मोल >>> 2) == 1073741819 && (मोल << 33) == 34, 4);
        पुनर्तपासणी_करची((byte)(मोल * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] क्रम_मोल_ed437109 = new int[5];
        for (int लूप_INDEX = 0; लूप_INDEX < क्रम_मोल_ed437109.length; लूप_INDEX++) क्रम_मोल_ed437109[लूप_INDEX] = लूप_INDEX * मोल;
        क्रम_मोल_ed437109[2]++;
        पुनर्तपासणी_करची(return_क्रम(क्रम_मोल_ed437109) == क्रम_मोल_ed437109 && क्रम_मोल_ed437109[2] == 35 && क्रम_मोल_ed437109[4] == 68, 6);
        पुनर्तपासणी_करची(शाखा(मोल - 117) == 7 && शाखा(मोल - 15) == 9 && शाखा(मोल) == 3 && 촘촘분기(मोल - 15) == 17, 7);
        String SMS = "한글 😀";
        पुनर्तपासणी_करची(SMS.length() == 5 && SMS.charAt(0) == '한' && SMS.charAt(3) == 0xd83d, 8);
        पुनर्तपासणी_करची(बोर्ड.CPU_अनुमती_पांवडो() == 1, 9);
        단말.बरोवचें("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 थळावो_मळ 변수가 보존되는지 검사: 각 작업은 독립된 यंत्र 스택을 쓴다.
        int थळावो_मोल = INDEX * 100;
        for (int लूप_INDEX = 0; लूप_INDEX < 10; लूप_INDEX++) {
            if (कार्य_क्रम % 2 + 1 != INDEX) कार्य_चूक++;
            कार्य_क्रम++;
            थळावो_मोल += लूप_INDEX + INDEX;
            कार्य_SUM[INDEX] = थळावो_मोल;
            작업횟수[INDEX]++;
            बोर्ड.YIELD_CPU();
            if (थळावो_मोल != कार्य_SUM[INDEX]) कार्य_चूक++;
        }
    }
    static void 작업시험() {
        कार्य_क्रम = 0; कार्य_चूक = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        पुनर्तपासणी_करची(बोर्ड.निर्माण_करचें_कार्य(1) == 0 && बोर्ड.निर्माण_करचें_कार्य(2) == 0, 20);
        int फेरो_COUNT = 0;
        while (बोर्ड.कार्य_स्थिती(1) != 0 || बोर्ड.कार्य_स्थिती(2) != 0) {
            बोर्ड.YIELD_CPU();
            पुनर्तपासणी_करची(++फेरो_COUNT < 100, 21);
        }
        पुनर्तपासणी_करची(작업횟수[1] == 10 && 작업횟수[2] == 10 && कार्य_क्रम == 20 && कार्य_चूक == 0, 22);
        पुनर्तपासणी_करची(कार्य_SUM[1] == 155 && कार्य_SUM[2] == 265, 23);
        단말.बरोवचें("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int उबें_स्थिती, int 너비, int 높이, int 색) {
        for (int 세로좌표 = उबें_स्थिती; 세로좌표 < उबें_स्थिती + 높이; 세로좌표++)
            for (int x_coordinate = 가로; x_coordinate < 가로 + 너비; x_coordinate++) बोर्ड.화면점(x_coordinate, 세로좌표, 색);
    }
    static void 화면() {
        if (बोर्ड.화면준비() == 0) { 단말.बरोवचें("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, बोर्ड.화면너비(), बोर्ड.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.बरोवचें("FRAMEBUFFER PASS "); 단말.수(बोर्ड.화면너비()); 단말.문자('x');
        단말.수(बोर्ड.화면높이()); 단말.बरोवचें(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int मेजप = बोर्ड.씨플러스시험();
        पुनर्तपासणी_करची(मेजप == 0, 100 + मेजप);
        단말.बरोवचें("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        पुनर्तपासणी_करची(बोर्ड.तपासचें_उपेगकर्तो_एप्लिकेशन() == 0, 200);
        단말.बरोवचें("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = बोर्ड.चलोवप_उपेगकर्तो_एप्लिकेशन(0);
        if (처음결과 != 0) { 단말.बरोवचें("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        पुनर्तपासणी_करची(처음결과 == 0, 201);
        단말.बरोवचें("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.बरोवचें("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int मेजप = बोर्ड.चलोवप_उपेगकर्तो_एप्लिकेशन(INDEX + 1);
            if (मेजप != 예상[INDEX]) { 단말.बरोवचें("USER RESULT "); 단말.수(मेजप); 단말.문자(10); }
            पुनर्तपासणी_करची(मेजप == 예상[INDEX], 210 + INDEX);
        }
        पुनर्तपासणी_करची(बोर्ड.चलोवप_उपेगकर्तो_एप्लिकेशन(0) == 0, 220);
        단말.बरोवचें("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int मेजप = बोर्ड.चलोवप_उपेगकर्तो_एप्लिकेशन(9);
        if (मेजप != 0) { 단말.बरोवचें("UDP RESULT "); 단말.수(मेजप); 단말.문자(10); }
        पुनर्तपासणी_करची(मेजप == 0, 230);
    }
    static void msinfo32_exe() {
        단말.बरोवचें("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.बरोवचें("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.बरोवचें("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.बरोवचें("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.बरोवचें("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void चलोवप() {
        단말.बरोवचें("WorldOS kok · kok · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.बरोवचें("NATIVE READY\n");
        명령해석기.पाळो_दिवचो_आदेश();
    }
}
