// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 komut_satırı. Alıntı, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class KomutYorumlayıcı {
    static int[] girdi_satırı = new int[4096], belirteç_değer = new int[4096], 시작점 = new int[32], süre_değer = new int[32];
    static int[] Düzenlenen_içindekiler = new int[16384], Düzenle_ad = new int[63];
    static int belirteç_BAĞ_DEĞ_SAY, Düzenle_ad_süre, sonuç;
    static boolean Önceki_hat;
    static void 원바이트(int değer) { Pano.직렬쓰기(değer); }
    static int girdi_satırını_oku() { return satır_düzenleyicisi.Okuma(); }
    static boolean 나누기(int Boyut) {
        int konum = 0, 끝 = 0; belirteç_BAĞ_DEĞ_SAY = 0;
        while (konum < Boyut) {
            while (konum < Boyut && (girdi_satırı[konum] == 32 || girdi_satırı[konum] == 9)) konum++;
            if (konum == Boyut) break;
            if (belirteç_BAĞ_DEĞ_SAY == 16) { 단말.Yazma("komut ayrıştırmak_değer: 인수가 너무 많습니다\n"); return false; }
            시작점[belirteç_BAĞ_DEĞ_SAY] = 끝; int Alıntı_değer = 0;
            while (konum < Boyut) {
                int değer = girdi_satırı[konum++];
                if (Alıntı_değer == 0 && (değer == 32 || değer == 9)) break;
                if (değer == Alıntı_değer) { Alıntı_değer = 0; continue; }
                if (Alıntı_değer == 0 && (değer == 39 || değer == 34)) { Alıntı_değer = değer; continue; }
                belirteç_değer[끝++] = değer;
            }
            if (Alıntı_değer != 0) { 단말.Yazma("komut ayrıştırmak_değer: 따옴표가 닫히지 않았습니다\n"); return false; }
            süre_değer[belirteç_BAĞ_DEĞ_SAY] = 끝 - 시작점[belirteç_BAĞ_DEĞ_SAY]; belirteç_BAĞ_DEĞ_SAY++;
        }
        return true;
    }
    static boolean 같음(int Dizin, String Word_SMS) {
        if (Dizin >= belirteç_BAĞ_DEĞ_SAY) return false;
        int konum_dizini=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int kod_noktası=Word_SMS.charAt(순번);
            if (kod_noktası>=0xd800 && kod_noktası<=0xdbff && 순번+1<Word_SMS.length()) kod_noktası=0x10000+((kod_noktası-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int bayt_BAĞ_DEĞ_SAY=kod_noktası<128?1:kod_noktası<2048?2:kod_noktası<65536?3:4;
            for (int dizi_değer=bayt_BAĞ_DEĞ_SAY-1; dizi_değer>=0; dizi_değer--) {
                int değer=bayt_BAĞ_DEĞ_SAY==1?kod_noktası:dizi_değer==bayt_BAĞ_DEĞ_SAY-1?(bayt_BAĞ_DEĞ_SAY==2?0xc0:bayt_BAĞ_DEĞ_SAY==3?0xe0:0xf0)|(kod_noktası>>(6*dizi_değer)):0x80|((kod_noktası>>(6*dizi_değer))&63);
                if (konum_dizini>=süre_değer[Dizin] || belirteç_değer[시작점[Dizin]+konum_dizini++]!=değer) return false;
            }
        }
        return konum_dizini==süre_değer[Dizin];
    }
    static int yol(int Dizin) {
        if (Dizin >= belirteç_BAĞ_DEĞ_SAY) return -22;
        int sonuç = BellekDosyaları.yol_Start(süre_değer[Dizin]); if (sonuç < 0) return sonuç;
        for (int Loop_Dizin = 0; Loop_Dizin < süre_değer[Dizin]; Loop_Dizin++) {
            sonuç = BellekDosyaları.yol_bayt(Loop_Dizin, belirteç_değer[시작점[Dizin] + Loop_Dizin]); if (sonuç < 0) return sonuç;
        }
        return 0;
    }
    static void hata(int Dizin) { sonuç = 1; 단말.Yazma("hata "); 단말.수(Dizin); 단말.문자(10); }
    static void Görünüm_değer() {
        if (belirteç_BAĞ_DEĞ_SAY != 2) { 단말.Yazma("사용법: cat dosya\n"); return; }
        int sonuç = yol(1); if (sonuç < 0) { hata(sonuç); return; }
        int dosya = BellekDosyaları.Aç(0); if (dosya < 0) { hata(dosya); return; }
        while (true) { int değer = BellekDosyaları.Okuma(dosya); if (değer == 256) break; if (değer < 0) { hata(değer); break; } 원바이트(değer); }
        BellekDosyaları.Kapat(dosya); 단말.문자(10);
    }
    static void Düzenle_değer() {
        if (belirteç_BAĞ_DEĞ_SAY != 2) { 단말.Yazma("사용법: edit dosya\n"); return; }
        int sonuç = yol(1); if (sonuç < 0) { hata(sonuç); return; }
        Düzenle_ad_süre = süre_değer[1];
        for (int Loop_Dizin = 0; Loop_Dizin < Düzenle_ad_süre; Loop_Dizin++) Düzenle_ad[Loop_Dizin] = belirteç_değer[시작점[1] + Loop_Dizin];
        단말.Yazma("EDIT: dosya 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Boyut = 0;
        while (true) {
            단말.Yazma("edit> "); int artış_değer = girdi_satırını_oku();
            if (artış_değer < 0) { 단말.Yazma("EDIT CANCELLED\n"); return; }
            if (artış_değer == 1 && girdi_satırı[0] == '.') break;
            if (artış_değer + 1 > Düzenlenen_içindekiler.length - Boyut) { 단말.Yazma("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_Dizin = 0; Loop_Dizin < artış_değer; Loop_Dizin++) Düzenlenen_içindekiler[Boyut++] = girdi_satırı[Loop_Dizin];
            Düzenlenen_içindekiler[Boyut++] = 10;
        }
        BellekDosyaları.yol_Start(Düzenle_ad_süre);
        for (int Loop_Dizin = 0; Loop_Dizin < Düzenle_ad_süre; Loop_Dizin++) BellekDosyaları.yol_bayt(Loop_Dizin, Düzenle_ad[Loop_Dizin]);
        int dosya = BellekDosyaları.Aç(577); if (dosya < 0) { hata(dosya); return; }
        for (int Loop_Dizin = 0; Loop_Dizin < Boyut; Loop_Dizin++) BellekDosyaları.Yazma(dosya, Düzenlenen_içindekiler[Loop_Dizin]);
        BellekDosyaları.Kapat(dosya); 단말.Yazma("SAVED "); 단말.수(Boyut); 단말.Yazma("bayt_değer(주기억 dosya)\n");
    }
    static int onaltılık_değer(int değer) {
        if (değer >= '0' && değer <= '9') return değer - '0';
        if (değer >= 'a' && değer <= 'f') return değer - 'a' + 10;
        if (değer >= 'A' && değer <= 'F') return değer - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (belirteç_BAĞ_DEĞ_SAY != 2) { 단말.Yazma("사용법: load dosya | hex dosya\n"); return; }
        int sonuç = yol(1); if (sonuç < 0) { hata(sonuç); return; }
        if (!넣기) {
            int dosya = BellekDosyaları.Aç(0); if (dosya < 0) { hata(dosya); return; }
            단말.Yazma("HEX BEGIN "); 단말.수(BellekDosyaları.Boyut(dosya)); 단말.문자(10);
            int girdi_BAĞ_DEĞ_SAY = 0;
            while (true) {
                int değer = BellekDosyaları.Okuma(dosya); if (değer < 0 || değer == 256) break;
                단말.문자("0123456789abcdef".charAt(değer >> 4)); 단말.문자("0123456789abcdef".charAt(değer & 15));
                if (++girdi_BAĞ_DEĞ_SAY % 32 == 0) 단말.문자(10);
            }
            if (girdi_BAĞ_DEĞ_SAY % 32 != 0) 단말.문자(10);
            BellekDosyaları.Kapat(dosya); 단말.Yazma("HEX END\n"); return;
        }
        Düzenle_ad_süre = süre_değer[1];
        for (int Loop_Dizin = 0; Loop_Dizin < Düzenle_ad_süre; Loop_Dizin++) Düzenle_ad[Loop_Dizin] = belirteç_değer[시작점[1] + Loop_Dizin];
        단말.Yazma("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Boyut = 0;
        while (true) {
            단말.Yazma("hex> "); int artış_değer = girdi_satırını_oku();
            if (artış_değer < 0) { 단말.Yazma("LOAD CANCELLED\n"); return; }
            if (artış_değer == 1 && girdi_satırı[0] == '.') break;
            int ön_kamera_değer = -1;
            for (int Loop_Dizin = 0; Loop_Dizin < artış_değer; Loop_Dizin++) {
                if (girdi_satırı[Loop_Dizin] == 32 || girdi_satırı[Loop_Dizin] == 9) continue;
                int değer = onaltılık_değer(girdi_satırı[Loop_Dizin]);
                if (değer < 0 || Boyut >= Düzenlenen_içindekiler.length) { 단말.Yazma("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (ön_kamera_değer < 0) ön_kamera_değer = değer; else { Düzenlenen_içindekiler[Boyut++] = ön_kamera_değer * 16 + değer; ön_kamera_değer = -1; }
            }
            if (ön_kamera_değer >= 0) { 단말.Yazma("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        BellekDosyaları.yol_Start(Düzenle_ad_süre);
        for (int Loop_Dizin = 0; Loop_Dizin < Düzenle_ad_süre; Loop_Dizin++) BellekDosyaları.yol_bayt(Loop_Dizin, Düzenle_ad[Loop_Dizin]);
        int dosya = BellekDosyaları.Aç(577); if (dosya < 0) { hata(dosya); return; }
        for (int Loop_Dizin = 0; Loop_Dizin < Boyut; Loop_Dizin++) BellekDosyaları.Yazma(dosya, Düzenlenen_içindekiler[Loop_Dizin]);
        BellekDosyaları.Kapat(dosya); 단말.Yazma("LOADED "); 단말.수(Boyut); 단말.Yazma("bayt_değer(주기억 dosya)\n");
    }
    static int araçlar(int Dizin) {
        return araç_girdi(Dizin, 1);
    }
    static int araç_girdi(int Dizin, int çalıştır) {
        if (belirteç_BAĞ_DEĞ_SAY - çalıştır > 8) return -22;
        Pano.인수준비(belirteç_BAĞ_DEĞ_SAY - çalıştır);
        for (int 첫값 = çalıştır; 첫값 < belirteç_BAĞ_DEĞ_SAY; 첫값++) {
            if (süre_değer[첫값] > 255) return -36;
            for (int Loop_Dizin = 0; Loop_Dizin < süre_değer[첫값]; Loop_Dizin++) Pano.bağımsız_değişken_bayt(첫값 - çalıştır, Loop_Dizin, belirteç_değer[시작점[첫값] + Loop_Dizin]);
        }
        return Dizin == -2 ? Pano.리눅스파일실행() : Dizin < 0 ? Pano.yürütmek_kullanıcı_Dosya() : Pano.çalıştırma_kullanıcı_program(Dizin);
    }
    static int PYTHON_paket_iş() {
        if (belirteç_BAĞ_DEĞ_SAY > 8) return -22;
        Pano.인수준비(belirteç_BAĞ_DEĞ_SAY);
        String yol = "/lib/paket_iş.py";
        // Java 문자열을 셸의 UTF-8 bağımsız_değişkenler 버퍼에 기록한다.
        int konum_dizini = 0;
        for (int 순번 = 0; 순번 < yol.length(); 순번++) {
            int karakter_değer = yol.charAt(순번);
            if (karakter_değer < 128) Pano.bağımsız_değişken_bayt(0, konum_dizini++, karakter_değer);
            else { Pano.bağımsız_değişken_bayt(0, konum_dizini++, 0xe0 | (karakter_değer >> 12)); Pano.bağımsız_değişken_bayt(0, konum_dizini++, 0x80 | ((karakter_değer >> 6) & 63)); Pano.bağımsız_değişken_bayt(0, konum_dizini++, 0x80 | (karakter_değer & 63)); }
        }
        for (int 순번 = 1; 순번 < belirteç_BAĞ_DEĞ_SAY; 순번++) {
            if (süre_değer[순번] > 255) return -36;
            for (int karakter_değer = 0; karakter_değer < süre_değer[순번]; karakter_değer++) Pano.bağımsız_değişken_bayt(순번, karakter_değer, belirteç_değer[시작점[순번] + karakter_değer]);
        }
        return Pano.çalıştırma_kullanıcı_program(12);
    }
    static int yürütme_biçim() {
        int 처리값 = yol(0); if (처리값 < 0) return 처리값;
        int dosya = BellekDosyaları.Aç(0); if (dosya < 0) return dosya;
        int 첫값 = BellekDosyaları.Okuma(dosya), bayt_veri = BellekDosyaları.Okuma(dosya), kod_noktası = BellekDosyaları.Okuma(dosya), 뒷값 = BellekDosyaları.Okuma(dosya);
        BellekDosyaları.Kapat(dosya);
        if (첫값 == 127 && bayt_veri == 'E' && kod_noktası == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && bayt_veri == 'K' && kod_noktası == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int Dizin, String bağımsız_değişkenler) {
        Pano.인수준비(1);
        for (int Loop_Dizin = 0; Loop_Dizin < bağımsız_değişkenler.length(); Loop_Dizin++) Pano.bağımsız_değişken_bayt(0, Loop_Dizin, bağımsız_değişkenler.charAt(Loop_Dizin));
        return Pano.çalıştırma_kullanıcı_program(Dizin);
    }
    static void SMS_bayt(int dosya, int değer) { BellekDosyaları.Yazma(dosya, değer); }
    static void statik_Dosya(String İsim, String içerik_değer) {
        // paket_iş 파일명은 ASCII. dosya 내용은 UTF-8로 저장한다.
        BellekDosyaları.yol_Start(İsim.length());
        for (int Loop_Dizin = 0; Loop_Dizin < İsim.length(); Loop_Dizin++) BellekDosyaları.yol_bayt(Loop_Dizin, İsim.charAt(Loop_Dizin));
        int dosya = BellekDosyaları.Aç(193); if (dosya < 0) return;
        for (int Loop_Dizin = 0; Loop_Dizin < içerik_değer.length(); Loop_Dizin++) {
            int kod_noktası = içerik_değer.charAt(Loop_Dizin);
            if (kod_noktası >= 0xd800 && kod_noktası <= 0xdbff && Loop_Dizin + 1 < içerik_değer.length()) kod_noktası = 0x10000 + ((kod_noktası - 0xd800) << 10) + içerik_değer.charAt(++Loop_Dizin) - 0xdc00;
            if (kod_noktası < 128) SMS_bayt(dosya, kod_noktası);
            else {
                int 수 = kod_noktası < 2048 ? 2 : kod_noktası < 65536 ? 3 : 4;
                SMS_bayt(dosya, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (kod_noktası >> (6 * (수 - 1))));
                for (int girdi_BAĞ_DEĞ_SAY = 수 - 1; girdi_BAĞ_DEĞ_SAY > 0; girdi_BAĞ_DEĞ_SAY--) SMS_bayt(dosya, 0x80 | ((kod_noktası >> (6 * (girdi_BAĞ_DEĞ_SAY - 1))) & 63));
            }
        }
        BellekDosyaları.Kapat(dosya);
    }
    static void 한글도움말() {
        단말.Yazma("F9 veya Shift+Space ile Türkçe girişe geçebilirsiniz.\n");
        단말.Yazma("  [TR] keyboard; [EN] ASCII\n");
        단말.Yazma("  i → ı\n");
        단말.Yazma("  F9: EN ↔ Türkçe | Ctrl+Shift+V: UTF-8\n");
        단말.Yazma("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Yazma("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String İsim) {
        int bayt_BAĞ_DEĞ_SAY = 0;
        for (int Loop_Dizin = 0; Loop_Dizin < İsim.length(); Loop_Dizin++) { int kod_noktası = İsim.charAt(Loop_Dizin); if (kod_noktası >= 0xd800 && kod_noktası <= 0xdfff) return -22; bayt_BAĞ_DEĞ_SAY += kod_noktası < 128 ? 1 : kod_noktası < 2048 ? 2 : 3; }
        int 처리값 = BellekDosyaları.yol_Start(bayt_BAĞ_DEĞ_SAY); if (처리값 < 0) return 처리값;
        int konum_dizini = 0;
        for (int Loop_Dizin = 0; Loop_Dizin < İsim.length(); Loop_Dizin++) {
            int kod_noktası = İsim.charAt(Loop_Dizin);
            if (kod_noktası < 128) BellekDosyaları.yol_bayt(konum_dizini++, kod_noktası);
            else if (kod_noktası < 2048) { BellekDosyaları.yol_bayt(konum_dizini++, 0xc0 | (kod_noktası >> 6)); BellekDosyaları.yol_bayt(konum_dizini++, 0x80 | (kod_noktası & 63)); }
            else { BellekDosyaları.yol_bayt(konum_dizini++, 0xe0 | (kod_noktası >> 12)); BellekDosyaları.yol_bayt(konum_dizini++, 0x80 | ((kod_noktası >> 6) & 63)); BellekDosyaları.yol_bayt(konum_dizini++, 0x80 | (kod_noktası & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String İsim) {
        int 처리값 = 예제경로(İsim); if (처리값 < 0) return 처리값;
        처리값 = BellekDosyaları.açmak_dizin(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String İsim, String veri) {
        int 처리값 = 예제경로(İsim); if (처리값 < 0) return 처리값;
        int dosya = BellekDosyaları.Aç(193); if (dosya == -17) return 0; if (dosya < 0) return dosya;
        for (int Loop_Dizin = 0; Loop_Dizin < veri.length(); Loop_Dizin += 2) {
            처리값 = BellekDosyaları.Yazma(dosya, onaltılık_değer(veri.charAt(Loop_Dizin)) * 16 + onaltılık_değer(veri.charAt(Loop_Dizin + 1)));
            if (처리값 < 0) { BellekDosyaları.Kapat(dosya); return 처리값; }
        }
        return BellekDosyaları.Kapat(dosya);
    }
    static void yardım_göster() {
        Sistem_araç.yardım_göster();
        단말.Yazma("sshd / SSH start|stop|status: SSH :22 (user, 장치별 parola_değer)\n");
        단말.Yazma("vncd / uzak_monitör start|stop|status: VNC :5900 (장치별 parola_değer)\n");
        단말.Yazma("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Yazma("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Yazma("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Yazma("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Yazma("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Yazma("모서리 + 왼쪽 버튼 sürüklemek_değer: uçbirim Boyut değiştirmek_değer; terminal size: SÜTUN_değer/SATIR_değer\n");
        단말.Yazma("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Yazma("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Yazma("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Yazma("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Yazma("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Yazma("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Yazma("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Yazma("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Yazma("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Yazma("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Yazma("pip: MicroPython kaynak_ağaç yükle_değer; konak --network --pip 필요; /lib는 RAM\n");
        단말.Yazma("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Yazma("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Yazma("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Yazma("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void uçbirim(boolean 전환여부) {
        if (전환여부 && Pano.uçbirim(2) != 0) { Pano.uçbirim(0); 단말.Yazma("TERMINAL CLOSED\n"); }
        else if (Pano.uçbirim(1) < 0) hata(-19);
        else 단말.Yazma("TERMINAL READY — Türkçe terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void komut() {
        if (belirteç_BAĞ_DEĞ_SAY == 0) return;
        if (Sistem_araç.yürütmek_komut()) return;
        if (같음(0,"sshd") || 같음(0,"SSH") || 같음(0,"vncd") || 같음(0,"uzak_monitör")) {
            int Tip_değer=같음(0,"vncd")||같음(0,"uzak_monitör")?1:0;
            int Eylem=같음(1,"start")||같음(1,"çalıştır")?1:같음(1,"stop")||같음(1,"Durdur")?0:2;
            int Durum_değer=Pano.gölge_kullanım(Tip_değer,Eylem);
            if(Durum_değer<0)hata(Durum_değer);else 단말.Yazma(Pano.gölge_kullanım(Tip_değer,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else yardım_göster(); }
        else if (같음(0, "info") || 같음(0, "i")) Çekirdek.msinfo32_exe();
        else if (같음(0, "pwd")) { BellekDosyaları.geçerli_yazma(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (belirteç_BAĞ_DEĞ_SAY == 1) { BellekDosyaları.yol_Start(1); 처리값 = BellekDosyaları.yol_bayt(0, '/'); } else 처리값 = belirteç_BAĞ_DEĞ_SAY == 2 ? yol(1) : -22;
            if (처리값 >= 0) 처리값 = BellekDosyaları.değiştirmek_dizin(); if (처리값 < 0) hata(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int bağımsız_değişken_Dizin = 같음(1, "-l") ? 2 : 1, 처리값;
            if (belirteç_BAĞ_DEĞ_SAY == bağımsız_değişken_Dizin) { BellekDosyaları.yol_Start(1); 처리값 = BellekDosyaları.yol_bayt(0, '.'); } else 처리값 = belirteç_BAĞ_DEĞ_SAY == bağımsız_değişken_Dizin + 1 ? yol(bağımsız_değişken_Dizin) : -22;
            if (처리값 >= 0) 처리값 = BellekDosyaları.경로목록(); if (처리값 < 0) hata(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) kabuk_Araçlar.Dosya_iş(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) kabuk_Araçlar.örnek_değer(같음(0, "mv"));
        else if (같음(0, "cat")) kabuk_Araçlar.Görünüm_değer();
        else if (같음(0, "wc")) kabuk_Araçlar.세기();
        else if (같음(0, "grep")) kabuk_Araçlar.BUL_girdi();
        else if (같음(0, "head") || 같음(0, "tail")) kabuk_Araçlar.머리(같음(0, "tail"));
        else if (같음(0, "tee")) kabuk_Araçlar.yazma_Birlikte();
        else if (같음(0, "env")) kabuk_söz_dizimi.şov_ortam();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (belirteç_BAĞ_DEĞ_SAY == 1) kabuk_söz_dizimi.şov_ortam();
            for (int Loop_Dizin = 1; Loop_Dizin < belirteç_BAĞ_DEĞ_SAY; Loop_Dizin++) { int 처리값 = kabuk_söz_dizimi.ortam_Ayarlar(Loop_Dizin, 같음(0, "unset")); if (처리값 != 0) { sonuç = 처리값; 단말.Yazma("komut ayrıştırmak_değer: değişken_değer 이름이 잘못되었거나 예약된 이름이거나 ortam 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) kabuk_söz_dizimi.yürütmek_Dosya();
        else if (같음(0, "true")) sonuç = 0;
        else if (같음(0, "false")) sonuç = 1;
        else if (같음(0, "history")) satır_düzenleyicisi.şov_LOG();
        else if (같음(0, "exit")) {
            if (kabuk_söz_dizimi.깊이 > 0) { sonuç = belirteç_BAĞ_DEĞ_SAY == 1 ? kabuk_söz_dizimi.Durum_değer : kabuk_Araçlar.rakam_değer(1); if (sonuç < 0 || sonuç > 255) sonuç = 2; kabuk_söz_dizimi.betik_Bitiş = true; }
            else if (Pano.uçbirim(2) != 0) uçbirim(true);
            else 단말.Yazma("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) Düzenle_değer();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (belirteç_BAĞ_DEĞ_SAY < 2) { sonuç = 2; 단말.Yazma("사용법: rm dosya...\n"); }
            for (int Loop_Dizin = 1; Loop_Dizin < belirteç_BAĞ_DEĞ_SAY; Loop_Dizin++) { int 처리값 = yol(Loop_Dizin); if (처리값 == 0) 처리값 = BellekDosyaları.silmek_girdi(); if (처리값 < 0) hata(처리값); }
        }
        else if (같음(0, "echo")) {
            int Start_konum = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Start_konum; 첫값 < belirteç_BAĞ_DEĞ_SAY; 첫값++) { if (첫값 > Start_konum) 단말.문자(32); for (int Loop_Dizin = 0; Loop_Dizin < süre_değer[첫값]; Loop_Dizin++) Pano.직렬쓰기(belirteç_değer[시작점[첫값] + Loop_Dizin]); }
            if (Start_konum == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Yazma("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_paket_iş() : araçlar(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); sonuç = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !kabuk_söz_dizimi.연결중) { 단말.Yazma("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = araçlar(13); sonuç = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = araçlar(15); sonuç = 처리값 < 0 ? 126 : 처리값; if (!kabuk_söz_dizimi.연결중) { 단말.Yazma("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = araçlar(16); sonuç = 처리값 < 0 ? 126 : 처리값; if (!kabuk_söz_dizimi.연결중) { 단말.Yazma("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Boyut = Pano.uçbirim(13); 단말.Yazma("TERMINAL SIZE "); 단말.수(Boyut & 65535); 단말.문자('x'); 단말.수(Boyut >>> 16); 단말.문자(10); }
            else uçbirim(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Pano.uçbirim(9); Masaüstü.yürütmek_komut(); }
        else if (같음(0, "c")) Çekirdek.test_C();
        else if (같음(0, "tasks") || 같음(0, "t")) Çekirdek.test_Tasks();
        else if (같음(0, "g")) Çekirdek.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) Çekirdek.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Pano.çalıştırma_kullanıcı_program(0); if (처리값 == 0) 단말.Yazma("ELF DEMO PASS\n"); else hata(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? araç_girdi(-2, 2) : araçlar(-1); sonuç = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !kabuk_söz_dizimi.연결중) { 단말.Yazma("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) Çekirdek.test_Ağ();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Pano.dosya_aktarımı_hizmet(1); if (처리값 < 0) hata(처리값); else { 단말.Yazma("FTP listening "); Sistem_araç.yazma_ADRES(Pano.ağ_Durum(0,0)); 단말.Yazma(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Pano.dosya_aktarımı_hizmet(0); 단말.Yazma("FTP stopped\n"); }
            else 단말.Yazma(Pano.dosya_aktarımı_hizmet(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { paket_iş.Hazırlan(); 단말.Yazma("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Dil = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (belirteç_BAĞ_DEĞ_SAY != 2 || Dil < 0) 단말.Yazma("example java|c|python: metinÇıktısı, dosya, 네트워크, 그래픽, Java Swing Pencere 예제\n");
            else { int 처리값 = 예제꾸러미.yükle_değer(Dil); if (처리값 < 0) { hata(처리값); if (처리값 == -28) 단말.Yazma("RAM full: remove unused files, then retry example\n"); } else 단말.Yazma("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int biçim_değer = yürütme_biçim();
            if (biçim_değer == 1 || biçim_değer == 2) {
                int 처리값 = araç_girdi(biçim_değer == 1 ? -1 : 14, 0); sonuç = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !kabuk_söz_dizimi.연결중) { 단말.Yazma("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (biçim_değer == 0) { sonuç = 126; 단말.Yazma("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { sonuç = 127; 단말.Yazma("Unknown command. help: commands\n"); }
        }
    }
    public static void yürütmek_komut() {
        paket_iş.Hazırlan();
        for (int Dil = 0; Dil < 3; Dil++) { int 처리값 = 예제꾸러미.yükle_değer(Dil); if (처리값 < 0) hata(처리값); }
        yardım_göster();
        while (true) {
            pencere_oturum.işlem_değer_girdi(); if (pencere_oturum.özgeçmiş_yürütme()) continue;
            if (!pencere_oturum.이어읽기) 단말.Yazma("jkoros-native> "); satır_düzenleyicisi.komut_satırı = true; Pano.uzak_bekle(1); int Boyut = girdi_satırını_oku(); Pano.uzak_bekle(0); satır_düzenleyicisi.komut_satırı = false;
            if (Boyut == -3) continue;
            if (Boyut == -2) 단말.Yazma("komut ayrıştırmak_değer: 명령줄이 너무 깁니다\n");
            if (Boyut >= 0) { kabuk_söz_dizimi.betik_Bitiş = false; kabuk_söz_dizimi.yürütmek_komut(girdi_satırı, 0, Boyut, 0); } else kabuk_söz_dizimi.Durum_değer = 130;
            Pano.Bitiş_uzak_komut(kabuk_söz_dizimi.Durum_değer);
            satır_düzenleyicisi.Boyut = satır_düzenleyicisi.imleç_değer = satır_düzenleyicisi.Start_pencere = 0;
        }
    }
}
