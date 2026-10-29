// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Asli Java 커널의 Pi4 초기 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class kernel {
    static int[] 작업횟수 = new int[3];
    static int[] tugas_SUM = new int[3];
    static int tugas_tertib;
    static int tugas_ralat;
    static int rawak_semai = 17;

    static void tentu_sahkan(boolean syarat, int INDEX) {
        if (!syarat) { 단말.Tulis("FAIL "); 단말.수(INDEX); Papan.Henti(INDEX); }
    }
    static int cabang(int VALUE) {
        switch (VALUE) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int VALUE) {
        switch (VALUE) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] kembalikan_ARRAY(int[] ARRAY_VALUE) { return ARRAY_VALUE; }
    static void 계산시험() {
        int VALUE = rawak_semai;
        tentu_sahkan(VALUE * 7 - VALUE == 102 && VALUE / 3 == 5 && VALUE % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        tentu_sahkan(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        tentu_sahkan(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        tentu_sahkan((-VALUE >> 2) == -5 && (-VALUE >>> 2) == 1073741819 && (VALUE << 33) == 34, 4);
        tentu_sahkan((byte)(VALUE * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] ARRAY_VALUE = new int[5];
        for (int Loop_INDEX = 0; Loop_INDEX < ARRAY_VALUE.length; Loop_INDEX++) ARRAY_VALUE[Loop_INDEX] = Loop_INDEX * VALUE;
        ARRAY_VALUE[2]++;
        tentu_sahkan(kembalikan_ARRAY(ARRAY_VALUE) == ARRAY_VALUE && ARRAY_VALUE[2] == 35 && ARRAY_VALUE[4] == 68, 6);
        tentu_sahkan(cabang(VALUE - 117) == 7 && cabang(VALUE - 15) == 9 && cabang(VALUE) == 3 && 촘촘분기(VALUE - 15) == 17, 7);
        String Teks = "한글 😀";
        tentu_sahkan(Teks.length() == 5 && Teks.charAt(0) == '한' && Teks.charAt(3) == 0xd83d, 8);
        tentu_sahkan(Papan.CPU_keizinan_aras() == 1, 9);
        단말.Tulis("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int INDEX) {
        // YIELD_CPU 전후 setempat_Skop 변수가 보존되는지 검사: 각 작업은 독립된 mesin 스택을 쓴다.
        int setempat_VALUE = INDEX * 100;
        for (int Loop_INDEX = 0; Loop_INDEX < 10; Loop_INDEX++) {
            if (tugas_tertib % 2 + 1 != INDEX) tugas_ralat++;
            tugas_tertib++;
            setempat_VALUE += Loop_INDEX + INDEX;
            tugas_SUM[INDEX] = setempat_VALUE;
            작업횟수[INDEX]++;
            Papan.YIELD_CPU();
            if (setempat_VALUE != tugas_SUM[INDEX]) tugas_ralat++;
        }
    }
    static void ujian_Tasks() {
        tugas_tertib = 0; tugas_ralat = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        tentu_sahkan(Papan.cipta_tugas(1) == 0 && Papan.cipta_tugas(2) == 0, 20);
        int putaran_COUNT = 0;
        while (Papan.tugas_status(1) != 0 || Papan.tugas_status(2) != 0) {
            Papan.YIELD_CPU();
            tentu_sahkan(++putaran_COUNT < 100, 21);
        }
        tentu_sahkan(작업횟수[1] == 10 && 작업횟수[2] == 10 && tugas_tertib == 20 && tugas_ralat == 0, 22);
        tentu_sahkan(tugas_SUM[1] == 155 && tugas_SUM[2] == 265, 23);
        단말.Tulis("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void segi_empat_tepat(int 가로, int Menegak_jawatan, int 너비, int 높이, int 색) {
        for (int Y_koordinat = Menegak_jawatan; Y_koordinat < Menegak_jawatan + 높이; Y_koordinat++)
            for (int koordinat_x = 가로; koordinat_x < 가로 + 너비; koordinat_x++) Papan.화면점(koordinat_x, Y_koordinat, 색);
    }
    static void 화면() {
        if (Papan.화면준비() == 0) { 단말.Tulis("FRAMEBUFFER unavailable\n"); return; }
        segi_empat_tepat(0, 0, Papan.화면너비(), Papan.화면높이(), 0x302018);
        segi_empat_tepat(40, 40, 560, 400, 0xefe8e2);
        segi_empat_tepat(40, 40, 560, 40, 0x905020);
        segi_empat_tepat(60, 110, 240, 140, 0x90b050);
        segi_empat_tepat(320, 110, 260, 140, 0xd0a040);
        segi_empat_tepat(60, 290, 520, 120, 0xd8d0c8);
        단말.Tulis("FRAMEBUFFER PASS "); 단말.수(Papan.화면너비()); 단말.문자('x');
        단말.수(Papan.화면높이()); 단말.Tulis(" RGB32 (drawing only)\n");
    }
    static void ujian_C() {
        int ukuran = Papan.씨플러스시험();
        tentu_sahkan(ukuran == 0, 100 + ukuran);
        단말.Tulis("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        tentu_sahkan(Papan.cek_pengguna_aplikasi() == 0, 200);
        단말.Tulis("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Papan.jalankan_pengguna_aplikasi(0);
        if (처음결과 != 0) { 단말.Tulis("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        tentu_sahkan(처음결과 == 0, 201);
        단말.Tulis("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int INDEX = 0; INDEX < 예상.length; INDEX++) {
            단말.Tulis("USER CHECK "); 단말.수(INDEX); 단말.문자(10);
            int ukuran = Papan.jalankan_pengguna_aplikasi(INDEX + 1);
            if (ukuran != 예상[INDEX]) { 단말.Tulis("USER RESULT "); 단말.수(ukuran); 단말.문자(10); }
            tentu_sahkan(ukuran == 예상[INDEX], 210 + INDEX);
        }
        tentu_sahkan(Papan.jalankan_pengguna_aplikasi(0) == 0, 220);
        단말.Tulis("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void ujian_Rangkaian() {
        int ukuran = Papan.jalankan_pengguna_aplikasi(9);
        if (ukuran != 0) { 단말.Tulis("UDP RESULT "); 단말.수(ukuran); 단말.문자(10); }
        tentu_sahkan(ukuran == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Tulis("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Tulis("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Tulis("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Tulis("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Tulis("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void Jalan() {
        단말.Tulis("WorldOS ms_Latn · Selamat datang · 😀\n");
        계산시험();
        ujian_C();
        ujian_Tasks();
        화면();
        사용자시험();
        ujian_Rangkaian();
        단말.Tulis("NATIVE READY\n");
        pentafsir_perintah.laksanakan_perintah();
    }
}
