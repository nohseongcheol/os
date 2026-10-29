// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Yazma 없이 동작하는 작은 직렬/PS2 KomutYorumlayıcı. */
public final class KomutYorumlayıcı {
    static int[] artış_değer = new int[128];
    static int süre_değer = 0;
    static boolean 앞줄복귀 = false;
    static boolean hat_Taşma = false;

    static boolean komut(String İsim) {
        if (süre_değer < İsim.length()) return false;
        for (int Dizin = 0; Dizin < İsim.length(); Dizin++)
            if (artış_değer[Dizin] != İsim.charAt(Dizin)) return false;
        return süre_değer == İsim.length() || artış_değer[İsim.length()] == ' ';
    }

    static void yardım_göster() {
        SMS_Terminal.Yazma("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.Yazma("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.Yazma("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.Yazma("sync (연결된 JKSTORE1 depo_değer 장치에 dosya 보존)\n");
    }

    static void işlem_değer_girdi() {
        if (süre_değer == 0) return;
        if (komut("help")) yardım_göster();
        else if (komut("sync")) {
            int sonuç = 파일보존.eşitlemek();
            SMS_Terminal.Yazma("Sync: "); SMS_Terminal.수쓰기(sonuç); SMS_Terminal.문자(10);
        }
        else if (komut("ls")) Bellek_dosya_sistemi.girdi_Liste();
        else if (komut("edit")) Bellek_dosya_sistemi.komut(artış_değer, 4, süre_değer, 0);
        else if (komut("cat")) Bellek_dosya_sistemi.komut(artış_değer, 3, süre_değer, 1);
        else if (komut("rm")) Bellek_dosya_sistemi.komut(artış_değer, 2, süre_değer, 2);
        else if (komut("java") || komut("javac")) {
            int sonuç = yürütme_yönetici.yürütmek_komut(artış_değer, 0, süre_değer);
            SMS_Terminal.Yazma("Exit: "); SMS_Terminal.수쓰기(sonuç); SMS_Terminal.문자(10);
        }
        else if (komut("apps")) yürütme_yönetici.girdi_Liste();
        else if (komut("net")) ağ_Yığın.Durum_değer();
        else if (komut("run")) {
            int sonuç = yürütme_yönetici.yürütmek_komut(artış_değer, 3, süre_değer);
            SMS_Terminal.Yazma("Exit: "); SMS_Terminal.수쓰기(sonuç); SMS_Terminal.Yazma("\n");
        } else if (komut("info")) {
            SMS_Terminal.Yazma("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (komut("mem")) {
            SMS_Terminal.Yazma("위쪽 Bellek_değer ADRES_bölge(KiB): "); SMS_Terminal.수쓰기(Bellek_bölge.BÜYÜKHARF_Bellek_boyutlandırmak());
            SMS_Terminal.Yazma("\n배열 동적 Bellek_değer ADRES_bölge(bayt_değer): "); SMS_Terminal.수쓰기(cihaz_değer.DİZİ_kullanım());
            SMS_Terminal.Yazma(" / 262144\n작업 ADRES_bölge bölüm_değer_366e0bfa: "); SMS_Terminal.수쓰기(Bellek_bölge.사용개수());
            SMS_Terminal.Yazma(" / 8 (각 4096바이트)\n");
        } else if (komut("alloc")) {
            int Dizin = Bellek_bölge.ayırmak_Depolama();
            SMS_Terminal.Yazma("bölüm_değer_366e0bfa Dizin: "); SMS_Terminal.수쓰기(Dizin); SMS_Terminal.Yazma("\n");
        } else if (komut("free")) {
            if (süre_değer == 6 && artış_değer[4] == ' ' && artış_değer[5] >= '0' && artış_değer[5] <= '7') {
                SMS_Terminal.Yazma(Bellek_bölge.İade_KR(artış_değer[5] - '0') ? "반환됨\n" : "할당되지 않은 bölüm_değer_366e0bfa\n");
            } else SMS_Terminal.Yazma("사용법: free 0..7\n");
        } else if (komut("echo")) {
            for (int Dizin = 5; Dizin < süre_değer; Dizin++) SMS_Terminal.문자(artış_değer[Dizin]);
            SMS_Terminal.문자(10);
        } else if (komut("clear")) SMS_Terminal.silmek_girdi();
        else if (komut("test")) Çekirdek.sınamalar();
        else if (komut("halt")) {
            SMS_Terminal.Yazma("HALTED\n");
            cihaz_değer.정지();
        } else SMS_Terminal.Yazma("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void kabul_etmek_VE_yazma(int değer) {
        if (değer == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = değer == 13;
        if (değer == 10 || değer == 13) {
            SMS_Terminal.문자(10);
            if (Bellek_dosya_sistemi.편집중) Bellek_dosya_sistemi.Düzenlenen_hat(artış_değer, süre_değer, hat_Taşma);
            else işlem_değer_girdi();
            süre_değer = 0;
            hat_Taşma = false;
            SMS_Terminal.Yazma(Bellek_dosya_sistemi.편집중 ? "...> " : "jkoros> ");
        } else if (değer == 8 || değer == 127) {
            if (süre_değer > 0) {
                süre_değer--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (değer >= 32 && değer < 127 && süre_değer < artış_değer.length) {
            artış_değer[süre_değer++] = değer;
            SMS_Terminal.문자(değer);
        } else if (değer >= 32 && değer < 127) hat_Taşma = true;
    }

    static void çalıştır() {
        yardım_göster();
        SMS_Terminal.Yazma("READY\njkoros> ");
        while (true) {
            int değer = SMS_Terminal.직렬읽기();
            if (değer < 0) değer = klavye.Okuma();
            if (değer >= 0) kabul_etmek_VE_yazma(değer);
            else { ağ_Yığın.doğrulamak(); cihaz_değer.잠시양보(); }
        }
    }
}
