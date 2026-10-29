// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 자체 Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class ዓንኳር {
    static int[] 작업횟수 = new int[3];
    static int[] 작업합 = new int[3];
    static int ተግባር_ቅደም_ተከተል;
    static int ተግባር_ስህተት;
    static int 난수씨 = 17;

    static void አረጋግጥ(boolean ሁኔታ, int መረጃ_ጠቆመ) {
        if (!ሁኔታ) { 단말.መጻፊያ("FAIL "); 단말.수(መረጃ_ጠቆመ); ቦርድ.ማስቆሚያ(መረጃ_ጠቆመ); }
    }
    static int ቅርንጫፍ(int እሴት) {
        switch (እሴት) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int እሴት) {
        switch (እሴት) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 배열돌려주기(int[] ድርድር_እሴት) { return ድርድር_እሴት; }
    static void 계산시험() {
        int እሴት = 난수씨;
        አረጋግጥ(እሴት * 7 - እሴት == 102 && እሴት / 3 == 5 && እሴት % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        አረጋግጥ(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        አረጋግጥ(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        አረጋግጥ((-እሴት >> 2) == -5 && (-እሴት >>> 2) == 1073741819 && (እሴት << 33) == 34, 4);
        አረጋግጥ((byte)(እሴት * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ድርድር_እሴት = new int[5];
        for (int ድግግሞሽ_መረጃ_ጠቆመ = 0; ድግግሞሽ_መረጃ_ጠቆመ < ድርድር_እሴት.length; ድግግሞሽ_መረጃ_ጠቆመ++) ድርድር_እሴት[ድግግሞሽ_መረጃ_ጠቆመ] = ድግግሞሽ_መረጃ_ጠቆመ * እሴት;
        ድርድር_እሴት[2]++;
        አረጋግጥ(배열돌려주기(ድርድር_እሴት) == ድርድር_እሴት && ድርድር_እሴት[2] == 35 && ድርድር_እሴት[4] == 68, 6);
        አረጋግጥ(ቅርንጫፍ(እሴት - 117) == 7 && ቅርንጫፍ(እሴት - 15) == 9 && ቅርንጫፍ(እሴት) == 3 && 촘촘분기(እሴት - 15) == 17, 7);
        String ጽሁፍ = "한글 😀";
        አረጋግጥ(ጽሁፍ.length() == 5 && ጽሁፍ.charAt(0) == '한' && ጽሁፍ.charAt(3) == 0xd83d, 8);
        አረጋግጥ(ቦርድ.ፕሮሰሰር_ፈቃድ_ደረጃ() == 1, 9);
        단말.መጻፊያ("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int መረጃ_ጠቆመ) {
        // አግድ_አሂያጅ 전후 የአካባቢ_ስፋት 변수가 보존되는지 검사: 각 작업은 독립된 ማሽን 스택을 쓴다.
        int የአካባቢ_እሴት = መረጃ_ጠቆመ * 100;
        for (int ድግግሞሽ_መረጃ_ጠቆመ = 0; ድግግሞሽ_መረጃ_ጠቆመ < 10; ድግግሞሽ_መረጃ_ጠቆመ++) {
            if (ተግባር_ቅደም_ተከተል % 2 + 1 != መረጃ_ጠቆመ) ተግባር_ስህተት++;
            ተግባር_ቅደም_ተከተል++;
            የአካባቢ_እሴት += ድግግሞሽ_መረጃ_ጠቆመ + መረጃ_ጠቆመ;
            작업합[መረጃ_ጠቆመ] = የአካባቢ_እሴት;
            작업횟수[መረጃ_ጠቆመ]++;
            ቦርድ.አግድ_አሂያጅ();
            if (የአካባቢ_እሴት != 작업합[መረጃ_ጠቆመ]) ተግባር_ስህተት++;
        }
    }
    static void 작업시험() {
        ተግባር_ቅደም_ተከተል = 0; ተግባር_ስህተት = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        አረጋግጥ(ቦርድ.ፍጠር_ተግባር(1) == 0 && ቦርድ.ፍጠር_ተግባር(2) == 0, 20);
        int 회전 = 0;
        while (ቦርድ.ተግባር_ዞን(1) != 0 || ቦርድ.ተግባር_ዞን(2) != 0) {
            ቦርድ.አግድ_አሂያጅ();
            አረጋግጥ(++회전 < 100, 21);
        }
        አረጋግጥ(작업횟수[1] == 10 && 작업횟수[2] == 10 && ተግባር_ቅደም_ተከተል == 20 && ተግባር_ስህተት == 0, 22);
        አረጋግጥ(작업합[1] == 155 && 작업합[2] == 265, 23);
        단말.መጻፊያ("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 사각형(int 가로, int ቋሚ_በቦታ_አስቀመጠ, int 너비, int 높이, int 색) {
        for (int 세로좌표 = ቋሚ_በቦታ_አስቀመጠ; 세로좌표 < ቋሚ_በቦታ_አስቀመጠ + 높이; 세로좌표++)
            for (int ኤክስ_አስተባባሪ = 가로; ኤክስ_አስተባባሪ < 가로 + 너비; ኤክስ_አስተባባሪ++) ቦርድ.화면점(ኤክስ_አስተባባሪ, 세로좌표, 색);
    }
    static void 화면() {
        if (ቦርድ.화면준비() == 0) { 단말.መጻፊያ("FRAMEBUFFER unavailable\n"); return; }
        사각형(0, 0, ቦርድ.화면너비(), ቦርድ.화면높이(), 0x302018);
        사각형(40, 40, 560, 400, 0xefe8e2);
        사각형(40, 40, 560, 40, 0x905020);
        사각형(60, 110, 240, 140, 0x90b050);
        사각형(320, 110, 260, 140, 0xd0a040);
        사각형(60, 290, 520, 120, 0xd8d0c8);
        단말.መጻፊያ("FRAMEBUFFER PASS "); 단말.수(ቦርድ.화면너비()); 단말.문자('x');
        단말.수(ቦርድ.화면높이()); 단말.መጻፊያ(" RGB32 (drawing only)\n");
    }
    static void 씨시험() {
        int ልኬት = ቦርድ.씨플러스시험();
        አረጋግጥ(ልኬት == 0, 100 + ልኬት);
        단말.መጻፊያ("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        አረጋግጥ(ቦርድ.ቼክ_ተጠቃሚ_ፕሮግራም() == 0, 200);
        단말.መጻፊያ("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = ቦርድ.አሂድ_ተጠቃሚ_ፕሮግራም(0);
        if (처음결과 != 0) { 단말.መጻፊያ("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        አረጋግጥ(처음결과 == 0, 201);
        단말.መጻፊያ("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int መረጃ_ጠቆመ = 0; መረጃ_ጠቆመ < 예상.length; መረጃ_ጠቆመ++) {
            단말.መጻፊያ("USER CHECK "); 단말.수(መረጃ_ጠቆመ); 단말.문자(10);
            int ልኬት = ቦርድ.አሂድ_ተጠቃሚ_ፕሮግራም(መረጃ_ጠቆመ + 1);
            if (ልኬት != 예상[መረጃ_ጠቆመ]) { 단말.መጻፊያ("USER RESULT "); 단말.수(ልኬት); 단말.문자(10); }
            አረጋግጥ(ልኬት == 예상[መረጃ_ጠቆመ], 210 + መረጃ_ጠቆመ);
        }
        አረጋግጥ(ቦርድ.አሂድ_ተጠቃሚ_ፕሮግራም(0) == 0, 220);
        단말.መጻፊያ("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 통신시험() {
        int ልኬት = ቦርድ.አሂድ_ተጠቃሚ_ፕሮግራም(9);
        if (ልኬት != 0) { 단말.መጻፊያ("UDP RESULT "); 단말.수(ልኬት); 단말.문자(10); }
        አረጋግጥ(ልኬት == 0, 230);
    }
    static void የስርዓት_መረጃ() {
        단말.መጻፊያ("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.መጻፊያ("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.መጻፊያ("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.መጻፊያ("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.መጻፊያ("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void ማስኬጃ() {
        단말.መጻፊያ("WorldOS am · ሰላም · 😀\n");
        계산시험();
        씨시험();
        작업시험();
        화면();
        사용자시험();
        통신시험();
        단말.መጻፊያ("NATIVE READY\n");
        명령해석기.ፈጽም_ትእዛዝ();
    }
}
