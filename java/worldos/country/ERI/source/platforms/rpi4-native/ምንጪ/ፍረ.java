// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class ፍረ {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int ዕማም_ተርታ;
    static int ዕማም_ጌጋ;
    static int 난수씨 = 17;

    static void ኣረጋግጽ(boolean ኩነታት, int መሐበሪ) {
        if (!ኩነታት) { 단말.ጸሓፍ("FAIL "); 단말.수(መሐበሪ); 보드.ኣቑም(መሐበሪ); }
    }
    static int ጨንፈር(int ዋጋ) {
        switch (ዋጋ) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int ዋጋ) {
        switch (ዋጋ) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] ተርታ_ዋጋ_ed437109) { return ተርታ_ዋጋ_ed437109; }
    static void 계산시험() {
        int ዋጋ = 난수씨;
        ኣረጋግጽ(ዋጋ * 7 - ዋጋ == 102 && ዋጋ / 3 == 5 && ዋጋ % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        ኣረጋግጽ(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        ኣረጋግጽ(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        ኣረጋግጽ((-ዋጋ >> 2) == -5 && (-ዋጋ >>> 2) == 1073741819 && (ዋጋ << 33) == 34, 4);
        ኣረጋግጽ((byte)(ዋጋ * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ተርታ_ዋጋ_ed437109 = new int[5];
        for (int ደጋግም_መሐበሪ = 0; ደጋግም_መሐበሪ < ተርታ_ዋጋ_ed437109.length; ደጋግም_መሐበሪ++) ተርታ_ዋጋ_ed437109[ደጋግም_መሐበሪ] = ደጋግም_መሐበሪ * ዋጋ;
        ተርታ_ዋጋ_ed437109[2]++;
        ኣረጋግጽ(배열돌려주기(ተርታ_ዋጋ_ed437109) == ተርታ_ዋጋ_ed437109 && ተርታ_ዋጋ_ed437109[2] == 35 && ተርታ_ዋጋ_ed437109[4] == 68, 6);
        ኣረጋግጽ(ጨንፈር(ዋጋ - 117) == 7 && ጨንፈር(ዋጋ - 15) == 9 && ጨንፈር(ዋጋ) == 3 && 촘촘분기(ዋጋ - 15) == 17, 7);
        String ጽሑፍ = "한글 😀";
        ኣረጋግጽ(ጽሑፍ.length() == 5 && ጽሑፍ.charAt(0) == '한' && ጽሑፍ.charAt(3) == 0xd83d, 8);
        ኣረጋግጽ(보드.시피유권한() == 1, 9);
        단말.ጸሓፍ("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int መሐበሪ) {
        // አግድ_ፕሮሰሰር 전후 ኣካባብያዊ_ዕምቆት 변수가 보존되는지 검사: 각 작업은 독립된 ማሽን 스택을 쓴다.
        int ኣካባብያዊ_ዋጋ = መሐበሪ * 100;
        for (int ደጋግም_መሐበሪ = 0; ደጋግም_መሐበሪ < 10; ደጋግም_መሐበሪ++) {
            if (ዕማም_ተርታ % 2 + 1 != መሐበሪ) ዕማም_ጌጋ++;
            ዕማም_ተርታ++;
            ኣካባብያዊ_ዋጋ += ደጋግም_መሐበሪ + መሐበሪ;
            작업합[መሐበሪ] = ኣካባብያዊ_ዋጋ;
            작업횟수[መሐበሪ]++;
            보드.አግድ_ፕሮሰሰር();
            if (ኣካባብያዊ_ዋጋ != 작업합[መሐበሪ]) ዕማም_ጌጋ++;
        }
    }
    static void 작업시험() {
        ዕማም_ተርታ = 0; ዕማም_ጌጋ = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        ኣረጋግጽ(보드.ፍጠር_ዕማም(1) == 0 && 보드.ፍጠር_ዕማም(2) == 0, 20);
        int 회전 = 0;
        while (보드.ዕማም_ደረጃ(1) != 0 || 보드.ዕማም_ደረጃ(2) != 0) {
            보드.አግድ_ፕሮሰሰር();
            ኣረጋግጽ(++회전 < 100, 21);
        }
        ኣረጋግጽ(작업횟수[1] == 10 && 작업횟수[2] == 10 && ዕማም_ተርታ == 20 && ዕማም_ጌጋ == 0, 22);
        ኣረጋግጽ(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.ጸሓፍ("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int 세로, int 너비, int 높이, int 색) {
        for (int 세로좌표 = 세로; 세로좌표 < 세로 + 높이; 세로좌표++)
            for (int 가로좌표 = 가로; 가로좌표 < 가로 + 너비; 가로좌표++) 보드.화면점(가로좌표, 세로좌표, 색);
    }
    static void 화면() {
        if (보드.화면준비() == 0) { 단말.ጸሓፍ("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.ጸሓፍ("FRAMEBUFFER PASS "); 단말.수(보드.화면너비()); 단말.문자('x');
        단말.수(보드.화면높이()); 단말.ጸሓፍ(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int 결과 = 보드.씨플러스시험();
        ኣረጋግጽ(결과 == 0, 100 + 결과);
        단말.ጸሓፍ("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        ኣረጋግጽ(보드.ፈትሽ_ተጠቃሚ_መተግበሪ() == 0, 200);
        단말.ጸሓፍ("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = 보드.ኣኺድ_ተጠቃሚ_መተግበሪ(0);
        if (처음결과 != 0) { 단말.ጸሓፍ("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        ኣረጋግጽ(처음결과 == 0, 201);
        단말.ጸሓፍ("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int መሐበሪ = 0; መሐበሪ < 예상.length; መሐበሪ++) {
            단말.ጸሓፍ("USER CHECK "); 단말.수(መሐበሪ); 단말.문자(10);
            int 결과 = 보드.ኣኺድ_ተጠቃሚ_መተግበሪ(መሐበሪ + 1);
            if (결과 != 예상[መሐበሪ]) { 단말.ጸሓፍ("USER RESULT "); 단말.수(결과); 단말.문자(10); }
            ኣረጋግጽ(결과 == 예상[መሐበሪ], 210 + መሐበሪ);
        }
        ኣረጋግጽ(보드.ኣኺድ_ተጠቃሚ_መተግበሪ(0) == 0, 220);
        단말.ጸሓፍ("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int 결과 = 보드.ኣኺድ_ተጠቃሚ_መተግበሪ(9);
        if (결과 != 0) { 단말.ጸሓፍ("UDP RESULT "); 단말.수(결과); 단말.문자(10); }
        ኣረጋግጽ(결과 == 0, 230);
    }
    static void ናይ_ስርዓት_ሓበሬታ() {
        단말.ጸሓፍ("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.ጸሓፍ("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.ጸሓፍ("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.ጸሓፍ("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.ጸሓፍ("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void ኣኺድ() {
        단말.ጸሓፍ("WorldOS ti · ሰላም · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.ጸሓፍ("NATIVE READY\n");
        명령해석기.ተግብር_ትእዛዝ();
    }
}
