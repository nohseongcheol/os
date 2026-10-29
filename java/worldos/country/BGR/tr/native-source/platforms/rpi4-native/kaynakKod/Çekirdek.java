// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Öz Java 커널의 Pi4 başlangıç_durumu 이식판. Linux/JVM 위에서 실행하지 않는다. */
public final class Çekirdek {
    static int[] 작업횟수 = new int[3];
    static int[] Görev_SUM = new int[3];
    static int Görev_düzen;
    static int Görev_hata;
    static int rastgele_çekirdek_değer = 17;

    static void doğrulamak(boolean koşul, int Dizin) {
        if (!koşul) { 단말.Yazma("FAIL "); 단말.수(Dizin); Pano.Durdur(Dizin); }
    }
    static int dal(int değer) {
        switch (değer) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 촘촘분기(int değer) {
        switch (değer) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] İade_DİZİ(int[] DİZİ_değer) { return DİZİ_değer; }
    static void 계산시험() {
        int değer = rastgele_çekirdek_değer;
        doğrulamak(değer * 7 - değer == 102 && değer / 3 == 5 && değer % 3 == 2, 1);
        int 작은수 = 0x80000000, 마이너스 = -1;
        doğrulamak(작은수 / 마이너스 == 작은수 && 작은수 % 마이너스 == 0, 2);
        doğrulamak(작은수 + 작은수 == 0 && -작은수 == 작은수, 3);
        doğrulamak((-değer >> 2) == -5 && (-değer >>> 2) == 1073741819 && (değer << 33) == 34, 4);
        doğrulamak((byte)(değer * 16) == 16 && (short)65535 == -1 && (char)마이너스 == 65535, 5);
        int[] DİZİ_değer = new int[5];
        for (int Loop_Dizin = 0; Loop_Dizin < DİZİ_değer.length; Loop_Dizin++) DİZİ_değer[Loop_Dizin] = Loop_Dizin * değer;
        DİZİ_değer[2]++;
        doğrulamak(İade_DİZİ(DİZİ_değer) == DİZİ_değer && DİZİ_değer[2] == 35 && DİZİ_değer[4] == 68, 6);
        doğrulamak(dal(değer - 117) == 7 && dal(değer - 15) == 9 && dal(değer) == 3 && 촘촘분기(değer - 15) == 17, 7);
        String metin = "한글 😀";
        doğrulamak(metin.length() == 5 && metin.charAt(0) == '한' && metin.charAt(3) == 0xd83d, 8);
        doğrulamak(Pano.CPU_izin_düzey() == 1, 9);
        단말.Yazma("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 작업(int Dizin) {
        // ÖDEME_CPU 전후 yerel_Scope 변수가 보존되는지 검사: 각 작업은 독립된 makine 스택을 쓴다.
        int yerel_değer = Dizin * 100;
        for (int Loop_Dizin = 0; Loop_Dizin < 10; Loop_Dizin++) {
            if (Görev_düzen % 2 + 1 != Dizin) Görev_hata++;
            Görev_düzen++;
            yerel_değer += Loop_Dizin + Dizin;
            Görev_SUM[Dizin] = yerel_değer;
            작업횟수[Dizin]++;
            Pano.ÖDEME_CPU();
            if (yerel_değer != Görev_SUM[Dizin]) Görev_hata++;
        }
    }
    static void test_Tasks() {
        Görev_düzen = 0; Görev_hata = 0;
        작업횟수[1] = 0; 작업횟수[2] = 0;
        doğrulamak(Pano.açmak_Görev(1) == 0 && Pano.açmak_Görev(2) == 0, 20);
        int döndürme_BAĞ_DEĞ_SAY = 0;
        while (Pano.Görev_Durum(1) != 0 || Pano.Görev_Durum(2) != 0) {
            Pano.ÖDEME_CPU();
            doğrulamak(++döndürme_BAĞ_DEĞ_SAY < 100, 21);
        }
        doğrulamak(작업횟수[1] == 10 && 작업횟수[2] == 10 && Görev_düzen == 20 && Görev_hata == 0, 22);
        doğrulamak(Görev_SUM[1] == 155 && Görev_SUM[2] == 265, 23);
        단말.Yazma("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void dikdörtgen(int 가로, int Dikey_konum, int 너비, int 높이, int 색) {
        for (int Y_koordinat = Dikey_konum; Y_koordinat < Dikey_konum + 높이; Y_koordinat++)
            for (int x_koordinatı = 가로; x_koordinatı < 가로 + 너비; x_koordinatı++) Pano.화면점(x_koordinatı, Y_koordinat, 색);
    }
    static void 화면() {
        if (Pano.화면준비() == 0) { 단말.Yazma("FRAMEBUFFER unavailable\n"); return; }
        dikdörtgen(0, 0, Pano.화면너비(), Pano.화면높이(), 0x302018);
        dikdörtgen(40, 40, 560, 400, 0xefe8e2);
        dikdörtgen(40, 40, 560, 40, 0x905020);
        dikdörtgen(60, 110, 240, 140, 0x90b050);
        dikdörtgen(320, 110, 260, 140, 0xd0a040);
        dikdörtgen(60, 290, 520, 120, 0xd8d0c8);
        단말.Yazma("FRAMEBUFFER PASS "); 단말.수(Pano.화면너비()); 단말.문자('x');
        단말.수(Pano.화면높이()); 단말.Yazma(" RGB32 (drawing only)\n");
    }
    static void test_C() {
        int sonuç = Pano.씨플러스시험();
        doğrulamak(sonuç == 0, 100 + sonuç);
        단말.Yazma("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 사용자시험() {
        doğrulamak(Pano.çek_kullanıcı_program() == 0, 200);
        단말.Yazma("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 처음결과 = Pano.çalıştırma_kullanıcı_program(0);
        if (처음결과 != 0) { 단말.Yazma("USER DEMO RESULT "); 단말.수(처음결과); 단말.문자(10); }
        doğrulamak(처음결과 == 0, 201);
        단말.Yazma("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 예상 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int Dizin = 0; Dizin < 예상.length; Dizin++) {
            단말.Yazma("USER CHECK "); 단말.수(Dizin); 단말.문자(10);
            int sonuç = Pano.çalıştırma_kullanıcı_program(Dizin + 1);
            if (sonuç != 예상[Dizin]) { 단말.Yazma("USER RESULT "); 단말.수(sonuç); 단말.문자(10); }
            doğrulamak(sonuç == 예상[Dizin], 210 + Dizin);
        }
        doğrulamak(Pano.çalıştırma_kullanıcı_program(0) == 0, 220);
        단말.Yazma("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void test_Ağ() {
        int sonuç = Pano.çalıştırma_kullanıcı_program(9);
        if (sonuç != 0) { 단말.Yazma("UDP RESULT "); 단말.수(sonuç); 단말.문자(10); }
        doğrulamak(sonuç == 0, 230);
    }
    static void msinfo32_exe() {
        단말.Yazma("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        단말.Yazma("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        단말.Yazma("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        단말.Yazma("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        단말.Yazma("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void çalıştır() {
        단말.Yazma("WorldOS tr · Merhaba · 😀\n");
        계산시험();
        test_C();
        test_Tasks();
        화면();
        사용자시험();
        test_Ağ();
        단말.Yazma("NATIVE READY\n");
        KomutYorumlayıcı.yürütmek_komut();
    }
}
