// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 komentorivi. Lainaus, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] syöterivi = new int[4096], tunnus_ARVO_eb540501 = new int[4096], 시작점 = new int[32], kesto_ARVO = new int[32];
    static int[] Muokattu_Sisällys = new int[16384], muutos_nimi = new int[63];
    static int tunnus_LASKE, muutos_nimi_kesto, TULOS;
    static boolean Edellinen_rivi;
    static void 원바이트(int ARVO) { Taulu.직렬쓰기(ARVO); }
    static int lue_syöterivi() { return rivi_editori.Luku(); }
    static boolean 나누기(int Koko) {
        int paikka = 0, 끝 = 0; tunnus_LASKE = 0;
        while (paikka < Koko) {
            while (paikka < Koko && (syöterivi[paikka] == 32 || syöterivi[paikka] == 9)) paikka++;
            if (paikka == Koko) break;
            if (tunnus_LASKE == 16) { 단말.Kirjoitus("komento jäsentää_ARVO: 인수가 너무 많습니다\n"); return false; }
            시작점[tunnus_LASKE] = 끝; int Lainaus_ARVO = 0;
            while (paikka < Koko) {
                int ARVO = syöterivi[paikka++];
                if (Lainaus_ARVO == 0 && (ARVO == 32 || ARVO == 9)) break;
                if (ARVO == Lainaus_ARVO) { Lainaus_ARVO = 0; continue; }
                if (Lainaus_ARVO == 0 && (ARVO == 39 || ARVO == 34)) { Lainaus_ARVO = ARVO; continue; }
                tunnus_ARVO_eb540501[끝++] = ARVO;
            }
            if (Lainaus_ARVO != 0) { 단말.Kirjoitus("komento jäsentää_ARVO: 따옴표가 닫히지 않았습니다\n"); return false; }
            kesto_ARVO[tunnus_LASKE] = 끝 - 시작점[tunnus_LASKE]; tunnus_LASKE++;
        }
        return true;
    }
    static boolean 같음(int INDEKSI, String Word_SMS) {
        if (INDEKSI >= tunnus_LASKE) return false;
        int sijainti=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int merkkikoodi=Word_SMS.charAt(순번);
            if (merkkikoodi>=0xd800 && merkkikoodi<=0xdbff && 순번+1<Word_SMS.length()) merkkikoodi=0x10000+((merkkikoodi-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int tavu_LASKE=merkkikoodi<128?1:merkkikoodi<2048?2:merkkikoodi<65536?3:4;
            for (int JONO_ARVO=tavu_LASKE-1; JONO_ARVO>=0; JONO_ARVO--) {
                int ARVO=tavu_LASKE==1?merkkikoodi:JONO_ARVO==tavu_LASKE-1?(tavu_LASKE==2?0xc0:tavu_LASKE==3?0xe0:0xf0)|(merkkikoodi>>(6*JONO_ARVO)):0x80|((merkkikoodi>>(6*JONO_ARVO))&63);
                if (sijainti>=kesto_ARVO[INDEKSI] || tunnus_ARVO_eb540501[시작점[INDEKSI]+sijainti++]!=ARVO) return false;
            }
        }
        return sijainti==kesto_ARVO[INDEKSI];
    }
    static int polku_2(int INDEKSI) {
        if (INDEKSI >= tunnus_LASKE) return -22;
        int TULOS = Muisti_Files.polku_alku(kesto_ARVO[INDEKSI]); if (TULOS < 0) return TULOS;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < kesto_ARVO[INDEKSI]; Loop_INDEKSI++) {
            TULOS = Muisti_Files.polku_tavu(Loop_INDEKSI, tunnus_ARVO_eb540501[시작점[INDEKSI] + Loop_INDEKSI]); if (TULOS < 0) return TULOS;
        }
        return 0;
    }
    static void VIRHE(int INDEKSI) { TULOS = 1; 단말.Kirjoitus("VIRHE "); 단말.numero(INDEKSI); 단말.문자(10); }
    static void Näkymä_ARVO() {
        if (tunnus_LASKE != 2) { 단말.Kirjoitus("사용법: cat tiedoston_nimi\n"); return; }
        int TULOS = polku_2(1); if (TULOS < 0) { VIRHE(TULOS); return; }
        int tiedoston_nimi = Muisti_Files.Avaa(0); if (tiedoston_nimi < 0) { VIRHE(tiedoston_nimi); return; }
        while (true) { int ARVO = Muisti_Files.Luku(tiedoston_nimi); if (ARVO == 256) break; if (ARVO < 0) { VIRHE(ARVO); break; } 원바이트(ARVO); }
        Muisti_Files.Sulje(tiedoston_nimi); 단말.문자(10);
    }
    static void muutos_ARVO() {
        if (tunnus_LASKE != 2) { 단말.Kirjoitus("사용법: edit tiedoston_nimi\n"); return; }
        int TULOS = polku_2(1); if (TULOS < 0) { VIRHE(TULOS); return; }
        muutos_nimi_kesto = kesto_ARVO[1];
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < muutos_nimi_kesto; Loop_INDEKSI++) muutos_nimi[Loop_INDEKSI] = tunnus_ARVO_eb540501[시작점[1] + Loop_INDEKSI];
        단말.Kirjoitus("EDIT: tiedoston_nimi 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Koko = 0;
        while (true) {
            단말.Kirjoitus("edit> "); int syöte_ARVO = lue_syöterivi();
            if (syöte_ARVO < 0) { 단말.Kirjoitus("EDIT CANCELLED\n"); return; }
            if (syöte_ARVO == 1 && syöterivi[0] == '.') break;
            if (syöte_ARVO + 1 > Muokattu_Sisällys.length - Koko) { 단말.Kirjoitus("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEKSI = 0; Loop_INDEKSI < syöte_ARVO; Loop_INDEKSI++) Muokattu_Sisällys[Koko++] = syöterivi[Loop_INDEKSI];
            Muokattu_Sisällys[Koko++] = 10;
        }
        Muisti_Files.polku_alku(muutos_nimi_kesto);
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < muutos_nimi_kesto; Loop_INDEKSI++) Muisti_Files.polku_tavu(Loop_INDEKSI, muutos_nimi[Loop_INDEKSI]);
        int tiedoston_nimi = Muisti_Files.Avaa(577); if (tiedoston_nimi < 0) { VIRHE(tiedoston_nimi); return; }
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < Koko; Loop_INDEKSI++) Muisti_Files.Kirjoitus(tiedoston_nimi, Muokattu_Sisällys[Loop_INDEKSI]);
        Muisti_Files.Sulje(tiedoston_nimi); 단말.Kirjoitus("SAVED "); 단말.numero(Koko); 단말.Kirjoitus("tavu_ARVO(주기억 tiedoston_nimi)\n");
    }
    static int heksa_ARVO(int ARVO) {
        if (ARVO >= '0' && ARVO <= '9') return ARVO - '0';
        if (ARVO >= 'a' && ARVO <= 'f') return ARVO - 'a' + 10;
        if (ARVO >= 'A' && ARVO <= 'F') return ARVO - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (tunnus_LASKE != 2) { 단말.Kirjoitus("사용법: load tiedoston_nimi | hex tiedoston_nimi\n"); return; }
        int TULOS = polku_2(1); if (TULOS < 0) { VIRHE(TULOS); return; }
        if (!넣기) {
            int tiedoston_nimi = Muisti_Files.Avaa(0); if (tiedoston_nimi < 0) { VIRHE(tiedoston_nimi); return; }
            단말.Kirjoitus("HEX BEGIN "); 단말.numero(Muisti_Files.Koko(tiedoston_nimi)); 단말.문자(10);
            int merkintä_LASKE = 0;
            while (true) {
                int ARVO = Muisti_Files.Luku(tiedoston_nimi); if (ARVO < 0 || ARVO == 256) break;
                단말.문자("0123456789abcdef".charAt(ARVO >> 4)); 단말.문자("0123456789abcdef".charAt(ARVO & 15));
                if (++merkintä_LASKE % 32 == 0) 단말.문자(10);
            }
            if (merkintä_LASKE % 32 != 0) 단말.문자(10);
            Muisti_Files.Sulje(tiedoston_nimi); 단말.Kirjoitus("HEX END\n"); return;
        }
        muutos_nimi_kesto = kesto_ARVO[1];
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < muutos_nimi_kesto; Loop_INDEKSI++) muutos_nimi[Loop_INDEKSI] = tunnus_ARVO_eb540501[시작점[1] + Loop_INDEKSI];
        단말.Kirjoitus("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Koko = 0;
        while (true) {
            단말.Kirjoitus("hex> "); int syöte_ARVO = lue_syöterivi();
            if (syöte_ARVO < 0) { 단말.Kirjoitus("LOAD CANCELLED\n"); return; }
            if (syöte_ARVO == 1 && syöterivi[0] == '.') break;
            int etukamera_ARVO = -1;
            for (int Loop_INDEKSI = 0; Loop_INDEKSI < syöte_ARVO; Loop_INDEKSI++) {
                if (syöterivi[Loop_INDEKSI] == 32 || syöterivi[Loop_INDEKSI] == 9) continue;
                int ARVO = heksa_ARVO(syöterivi[Loop_INDEKSI]);
                if (ARVO < 0 || Koko >= Muokattu_Sisällys.length) { 단말.Kirjoitus("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (etukamera_ARVO < 0) etukamera_ARVO = ARVO; else { Muokattu_Sisällys[Koko++] = etukamera_ARVO * 16 + ARVO; etukamera_ARVO = -1; }
            }
            if (etukamera_ARVO >= 0) { 단말.Kirjoitus("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Muisti_Files.polku_alku(muutos_nimi_kesto);
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < muutos_nimi_kesto; Loop_INDEKSI++) Muisti_Files.polku_tavu(Loop_INDEKSI, muutos_nimi[Loop_INDEKSI]);
        int tiedoston_nimi = Muisti_Files.Avaa(577); if (tiedoston_nimi < 0) { VIRHE(tiedoston_nimi); return; }
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < Koko; Loop_INDEKSI++) Muisti_Files.Kirjoitus(tiedoston_nimi, Muokattu_Sisällys[Loop_INDEKSI]);
        Muisti_Files.Sulje(tiedoston_nimi); 단말.Kirjoitus("LOADED "); 단말.numero(Koko); 단말.Kirjoitus("tavu_ARVO(주기억 tiedoston_nimi)\n");
    }
    static int työkalut(int INDEKSI) {
        return työkalu_merkintä(INDEKSI, 1);
    }
    static int työkalu_merkintä(int INDEKSI, int Suorita_2) {
        if (tunnus_LASKE - Suorita_2 > 8) return -22;
        Taulu.인수준비(tunnus_LASKE - Suorita_2);
        for (int 첫값 = Suorita_2; 첫값 < tunnus_LASKE; 첫값++) {
            if (kesto_ARVO[첫값] > 255) return -36;
            for (int Loop_INDEKSI = 0; Loop_INDEKSI < kesto_ARVO[첫값]; Loop_INDEKSI++) Taulu.argumentti_tavu(첫값 - Suorita_2, Loop_INDEKSI, tunnus_ARVO_eb540501[시작점[첫값] + Loop_INDEKSI]);
        }
        return INDEKSI == -2 ? Taulu.리눅스파일실행() : INDEKSI < 0 ? Taulu.Suorita_käyttäjä_Tiedosto() : Taulu.suorittaa_käyttäjä_ohjelma(INDEKSI);
    }
    static int PYTHON_nippu() {
        if (tunnus_LASKE > 8) return -22;
        Taulu.인수준비(tunnus_LASKE);
        String polku_2 = "/lib/nippu.py";
        // Java 문자열을 셸의 UTF-8 argumentit 버퍼에 기록한다.
        int sijainti = 0;
        for (int 순번 = 0; 순번 < polku_2.length(); 순번++) {
            int merkki_ARVO = polku_2.charAt(순번);
            if (merkki_ARVO < 128) Taulu.argumentti_tavu(0, sijainti++, merkki_ARVO);
            else { Taulu.argumentti_tavu(0, sijainti++, 0xe0 | (merkki_ARVO >> 12)); Taulu.argumentti_tavu(0, sijainti++, 0x80 | ((merkki_ARVO >> 6) & 63)); Taulu.argumentti_tavu(0, sijainti++, 0x80 | (merkki_ARVO & 63)); }
        }
        for (int 순번 = 1; 순번 < tunnus_LASKE; 순번++) {
            if (kesto_ARVO[순번] > 255) return -36;
            for (int merkki_ARVO = 0; merkki_ARVO < kesto_ARVO[순번]; merkki_ARVO++) Taulu.argumentti_tavu(순번, merkki_ARVO, tunnus_ARVO_eb540501[시작점[순번] + merkki_ARVO]);
        }
        return Taulu.suorittaa_käyttäjä_ohjelma(12);
    }
    static int suoritus_muoto() {
        int 처리값 = polku_2(0); if (처리값 < 0) return 처리값;
        int tiedoston_nimi = Muisti_Files.Avaa(0); if (tiedoston_nimi < 0) return tiedoston_nimi;
        int 첫값 = Muisti_Files.Luku(tiedoston_nimi), tavu_data = Muisti_Files.Luku(tiedoston_nimi), merkkikoodi = Muisti_Files.Luku(tiedoston_nimi), seuraava_ARVO = Muisti_Files.Luku(tiedoston_nimi);
        Muisti_Files.Sulje(tiedoston_nimi);
        if (첫값 == 127 && tavu_data == 'E' && merkkikoodi == 'L' && seuraava_ARVO == 'F') return 1;
        if (첫값 == 'P' && tavu_data == 'K' && merkkikoodi == 3 && seuraava_ARVO == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEKSI, String argumentit) {
        Taulu.인수준비(1);
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < argumentit.length(); Loop_INDEKSI++) Taulu.argumentti_tavu(0, Loop_INDEKSI, argumentit.charAt(Loop_INDEKSI));
        return Taulu.suorittaa_käyttäjä_ohjelma(INDEKSI);
    }
    static void SMS_tavu(int tiedoston_nimi, int ARVO) { Muisti_Files.Kirjoitus(tiedoston_nimi, ARVO); }
    static void staattinen_Tiedosto(String Nimi, String Sisältö_ARVO) {
        // nippu 파일명은 ASCII. tiedoston_nimi 내용은 UTF-8로 저장한다.
        Muisti_Files.polku_alku(Nimi.length());
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < Nimi.length(); Loop_INDEKSI++) Muisti_Files.polku_tavu(Loop_INDEKSI, Nimi.charAt(Loop_INDEKSI));
        int tiedoston_nimi = Muisti_Files.Avaa(193); if (tiedoston_nimi < 0) return;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < Sisältö_ARVO.length(); Loop_INDEKSI++) {
            int merkkikoodi = Sisältö_ARVO.charAt(Loop_INDEKSI);
            if (merkkikoodi >= 0xd800 && merkkikoodi <= 0xdbff && Loop_INDEKSI + 1 < Sisältö_ARVO.length()) merkkikoodi = 0x10000 + ((merkkikoodi - 0xd800) << 10) + Sisältö_ARVO.charAt(++Loop_INDEKSI) - 0xdc00;
            if (merkkikoodi < 128) SMS_tavu(tiedoston_nimi, merkkikoodi);
            else {
                int numero = merkkikoodi < 2048 ? 2 : merkkikoodi < 65536 ? 3 : 4;
                SMS_tavu(tiedoston_nimi, (numero == 2 ? 0xc0 : numero == 3 ? 0xe0 : 0xf0) | (merkkikoodi >> (6 * (numero - 1))));
                for (int merkintä_LASKE = numero - 1; merkintä_LASKE > 0; merkintä_LASKE--) SMS_tavu(tiedoston_nimi, 0x80 | ((merkkikoodi >> (6 * (merkintä_LASKE - 1))) & 63));
            }
        }
        Muisti_Files.Sulje(tiedoston_nimi);
    }
    static void 한글도움말() {
        단말.Kirjoitus("F9 tai Shift+Space vaihtaa suomenkieliseen näppäimistöön.\n");
        단말.Kirjoitus("  [FI] keyboard; [EN] ASCII\n");
        단말.Kirjoitus("  $ → ¤\n");
        단말.Kirjoitus("  F9: EN ↔ suomi | Ctrl+Shift+V: UTF-8\n");
        단말.Kirjoitus("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Kirjoitus("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Nimi) {
        int tavu_LASKE = 0;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < Nimi.length(); Loop_INDEKSI++) { int merkkikoodi = Nimi.charAt(Loop_INDEKSI); if (merkkikoodi >= 0xd800 && merkkikoodi <= 0xdfff) return -22; tavu_LASKE += merkkikoodi < 128 ? 1 : merkkikoodi < 2048 ? 2 : 3; }
        int 처리값 = Muisti_Files.polku_alku(tavu_LASKE); if (처리값 < 0) return 처리값;
        int sijainti = 0;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < Nimi.length(); Loop_INDEKSI++) {
            int merkkikoodi = Nimi.charAt(Loop_INDEKSI);
            if (merkkikoodi < 128) Muisti_Files.polku_tavu(sijainti++, merkkikoodi);
            else if (merkkikoodi < 2048) { Muisti_Files.polku_tavu(sijainti++, 0xc0 | (merkkikoodi >> 6)); Muisti_Files.polku_tavu(sijainti++, 0x80 | (merkkikoodi & 63)); }
            else { Muisti_Files.polku_tavu(sijainti++, 0xe0 | (merkkikoodi >> 12)); Muisti_Files.polku_tavu(sijainti++, 0x80 | ((merkkikoodi >> 6) & 63)); Muisti_Files.polku_tavu(sijainti++, 0x80 | (merkkikoodi & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Nimi) {
        int 처리값 = 예제경로(Nimi); if (처리값 < 0) return 처리값;
        처리값 = Muisti_Files.Luo_Directory(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Nimi, String data) {
        int 처리값 = 예제경로(Nimi); if (처리값 < 0) return 처리값;
        int tiedoston_nimi = Muisti_Files.Avaa(193); if (tiedoston_nimi == -17) return 0; if (tiedoston_nimi < 0) return tiedoston_nimi;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < data.length(); Loop_INDEKSI += 2) {
            처리값 = Muisti_Files.Kirjoitus(tiedoston_nimi, heksa_ARVO(data.charAt(Loop_INDEKSI)) * 16 + heksa_ARVO(data.charAt(Loop_INDEKSI + 1)));
            if (처리값 < 0) { Muisti_Files.Sulje(tiedoston_nimi); return 처리값; }
        }
        return Muisti_Files.Sulje(tiedoston_nimi);
    }
    static void näytä_ohje() {
        Järjestelmä_työkalu.näytä_ohje();
        단말.Kirjoitus("sshd / suojattu_liittymä start|stop|status: SSH :22 (user, 장치별 salasana_ARVO)\n");
        단말.Kirjoitus("vncd / etä_näyttö start|stop|status: VNC :5900 (장치별 salasana_ARVO)\n");
        단말.Kirjoitus("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Kirjoitus("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Kirjoitus("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Kirjoitus("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Kirjoitus("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Kirjoitus("모서리 + 왼쪽 버튼 vetää_ARVO: komentotulkki Koko muuttaa_ARVO; terminal size: SARAKE_ARVO/RIVI_ARVO\n");
        단말.Kirjoitus("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Kirjoitus("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Kirjoitus("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Kirjoitus("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Kirjoitus("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Kirjoitus("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Kirjoitus("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Kirjoitus("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Kirjoitus("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Kirjoitus("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Kirjoitus("pip: MicroPython lähde_puu asentaa_ARVO; isäntä --network --pip 필요; /lib는 RAM\n");
        단말.Kirjoitus("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Kirjoitus("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Kirjoitus("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Kirjoitus("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void komentotulkki(boolean 전환여부) {
        if (전환여부 && Taulu.komentotulkki(2) != 0) { Taulu.komentotulkki(0); 단말.Kirjoitus("TERMINAL CLOSED\n"); }
        else if (Taulu.komentotulkki(1) < 0) VIRHE(-19);
        else 단말.Kirjoitus("TERMINAL READY — suomi terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void komento() {
        if (tunnus_LASKE == 0) return;
        if (Järjestelmä_työkalu.Suorita_komento()) return;
        if (같음(0,"sshd") || 같음(0,"suojattu_liittymä") || 같음(0,"vncd") || 같음(0,"etä_näyttö")) {
            int 종류=같음(0,"vncd")||같음(0,"etä_näyttö")?1:0;
            int Toiminto=같음(1,"start")||같음(1,"Suorita_2")?1:같음(1,"stop")||같음(1,"Pysäytä")?0:2;
            int Tila_ARVO=Taulu.etähallinta(종류,Toiminto);
            if(Tila_ARVO<0)VIRHE(Tila_ARVO);else 단말.Kirjoitus(Taulu.etähallinta(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else näytä_ohje(); }
        else if (같음(0, "info") || 같음(0, "i")) ydin.msinfo32_exe();
        else if (같음(0, "pwd")) { Muisti_Files.nykyinen_kirjoitus(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (tunnus_LASKE == 1) { Muisti_Files.polku_alku(1); 처리값 = Muisti_Files.polku_tavu(0, '/'); } else 처리값 = tunnus_LASKE == 2 ? polku_2(1) : -22;
            if (처리값 >= 0) 처리값 = Muisti_Files.muuttaa_Directory(); if (처리값 < 0) VIRHE(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argumentti_INDEKSI = 같음(1, "-l") ? 2 : 1, 처리값;
            if (tunnus_LASKE == argumentti_INDEKSI) { Muisti_Files.polku_alku(1); 처리값 = Muisti_Files.polku_tavu(0, '.'); } else 처리값 = tunnus_LASKE == argumentti_INDEKSI + 1 ? polku_2(argumentti_INDEKSI) : -22;
            if (처리값 >= 0) 처리값 = Muisti_Files.경로목록(); if (처리값 < 0) VIRHE(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) liittymä_Työkalut.Tiedosto_työ(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) liittymä_Työkalut.kopioida_ARVO(같음(0, "mv"));
        else if (같음(0, "cat")) liittymä_Työkalut.Näkymä_ARVO();
        else if (같음(0, "wc")) liittymä_Työkalut.세기();
        else if (같음(0, "grep")) liittymä_Työkalut.ETSI_merkintä();
        else if (같음(0, "head") || 같음(0, "tail")) liittymä_Työkalut.머리(같음(0, "tail"));
        else if (같음(0, "tee")) liittymä_Työkalut.kirjoitus_Yhdessä();
        else if (같음(0, "env")) liittymä_syntaksi.näyttää_ympäristö();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (tunnus_LASKE == 1) liittymä_syntaksi.näyttää_ympäristö();
            for (int Loop_INDEKSI = 1; Loop_INDEKSI < tunnus_LASKE; Loop_INDEKSI++) { int 처리값 = liittymä_syntaksi.ympäristö_Asetukset(Loop_INDEKSI, 같음(0, "unset")); if (처리값 != 0) { TULOS = 처리값; 단말.Kirjoitus("komento jäsentää_ARVO: muuttuja_ARVO 이름이 잘못되었거나 예약된 이름이거나 ympäristö 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) liittymä_syntaksi.Suorita_Tiedosto();
        else if (같음(0, "true")) TULOS = 0;
        else if (같음(0, "false")) TULOS = 1;
        else if (같음(0, "history")) rivi_editori.näyttää_LOG();
        else if (같음(0, "exit")) {
            if (liittymä_syntaksi.깊이 > 0) { TULOS = tunnus_LASKE == 1 ? liittymä_syntaksi.Tila_ARVO : liittymä_Työkalut.numero_ARVO(1); if (TULOS < 0 || TULOS > 255) TULOS = 2; liittymä_syntaksi.komentosarja_lopettaa_puhelu = true; }
            else if (Taulu.komentotulkki(2) != 0) komentotulkki(true);
            else 단말.Kirjoitus("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) muutos_ARVO();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (tunnus_LASKE < 2) { TULOS = 2; 단말.Kirjoitus("사용법: rm tiedoston_nimi...\n"); }
            for (int Loop_INDEKSI = 1; Loop_INDEKSI < tunnus_LASKE; Loop_INDEKSI++) { int 처리값 = polku_2(Loop_INDEKSI); if (처리값 == 0) 처리값 = Muisti_Files.poistaa_merkintä_c8dbc399(); if (처리값 < 0) VIRHE(처리값); }
        }
        else if (같음(0, "echo")) {
            int alku_toimi = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = alku_toimi; 첫값 < tunnus_LASKE; 첫값++) { if (첫값 > alku_toimi) 단말.문자(32); for (int Loop_INDEKSI = 0; Loop_INDEKSI < kesto_ARVO[첫값]; Loop_INDEKSI++) Taulu.직렬쓰기(tunnus_ARVO_eb540501[시작점[첫값] + Loop_INDEKSI]); }
            if (alku_toimi == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Kirjoitus("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_nippu() : työkalut(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); TULOS = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !liittymä_syntaksi.연결중) { 단말.Kirjoitus("exit "); 단말.numero(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = työkalut(13); TULOS = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = työkalut(15); TULOS = 처리값 < 0 ? 126 : 처리값; if (!liittymä_syntaksi.연결중) { 단말.Kirjoitus("exit "); 단말.numero(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = työkalut(16); TULOS = 처리값 < 0 ? 126 : 처리값; if (!liittymä_syntaksi.연결중) { 단말.Kirjoitus("exit "); 단말.numero(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Koko = Taulu.komentotulkki(13); 단말.Kirjoitus("TERMINAL SIZE "); 단말.numero(Koko & 65535); 단말.문자('x'); 단말.numero(Koko >>> 16); 단말.문자(10); }
            else komentotulkki(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Taulu.komentotulkki(9); työpöytä.Suorita_komento(); }
        else if (같음(0, "c")) ydin.testi_C();
        else if (같음(0, "tasks") || 같음(0, "t")) ydin.testi_Tasks();
        else if (같음(0, "g")) ydin.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) ydin.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Taulu.suorittaa_käyttäjä_ohjelma(0); if (처리값 == 0) 단말.Kirjoitus("ELF DEMO PASS\n"); else VIRHE(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? työkalu_merkintä(-2, 2) : työkalut(-1); TULOS = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !liittymä_syntaksi.연결중) { 단말.Kirjoitus("exit "); 단말.numero(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) ydin.testi_Verkot();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Taulu.tiedostonsiirto_palvelu(1); if (처리값 < 0) VIRHE(처리값); else { 단말.Kirjoitus("FTP listening "); Järjestelmä_työkalu.kirjoitus_OSOITE(Taulu.verkko_tila(0,0)); 단말.Kirjoitus(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Taulu.tiedostonsiirto_palvelu(0); 단말.Kirjoitus("FTP stopped\n"); }
            else 단말.Kirjoitus(Taulu.tiedostonsiirto_palvelu(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { nippu.Valmistele(); 단말.Kirjoitus("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Kieli = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (tunnus_LASKE != 2 || Kieli < 0) 단말.Kirjoitus("example java|c|python: tulostuspaikka, tiedoston_nimi, 네트워크, 그래픽, Java Swing Ikkuna 예제\n");
            else { int 처리값 = 예제꾸러미.asentaa_ARVO(Kieli); if (처리값 < 0) { VIRHE(처리값); if (처리값 == -28) 단말.Kirjoitus("RAM full: remove unused files, then retry example\n"); } else 단말.Kirjoitus("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int muoto_ARVO = suoritus_muoto();
            if (muoto_ARVO == 1 || muoto_ARVO == 2) {
                int 처리값 = työkalu_merkintä(muoto_ARVO == 1 ? -1 : 14, 0); TULOS = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !liittymä_syntaksi.연결중) { 단말.Kirjoitus("exit "); 단말.numero(처리값); 단말.문자(10); }
            } else if (muoto_ARVO == 0) { TULOS = 126; 단말.Kirjoitus("실행할 numero 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { TULOS = 127; 단말.Kirjoitus("Unknown command. help: commands\n"); }
        }
    }
    public static void Suorita_komento() {
        nippu.Valmistele();
        for (int Kieli = 0; Kieli < 3; Kieli++) { int 처리값 = 예제꾸러미.asentaa_ARVO(Kieli); if (처리값 < 0) VIRHE(처리값); }
        näytä_ohje();
        while (true) {
            ikkuna_istunto.prosessi_ARVO_merkintä(); if (ikkuna_istunto.jatka_suoritus()) continue;
            if (!ikkuna_istunto.이어읽기) 단말.Kirjoitus("jkoros-native> "); rivi_editori.komentorivi = true; Taulu.etä_odottaa(1); int Koko = lue_syöterivi(); Taulu.etä_odottaa(0); rivi_editori.komentorivi = false;
            if (Koko == -3) continue;
            if (Koko == -2) 단말.Kirjoitus("komento jäsentää_ARVO: 명령줄이 너무 깁니다\n");
            if (Koko >= 0) { liittymä_syntaksi.komentosarja_lopettaa_puhelu = false; liittymä_syntaksi.Suorita_komento(syöterivi, 0, Koko, 0); } else liittymä_syntaksi.Tila_ARVO = 130;
            Taulu.lopettaa_puhelu_etä_komento(liittymä_syntaksi.Tila_ARVO);
            rivi_editori.Koko = rivi_editori.kohdistin_ARVO = rivi_editori.alku_ikkuna = 0;
        }
    }
}
