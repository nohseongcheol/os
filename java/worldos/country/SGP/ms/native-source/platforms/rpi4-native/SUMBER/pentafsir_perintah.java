// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 baris_perintah. Petikan, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class pentafsir_perintah {
    static int[] baris = new int[4096], token_VALUE = new int[4096], 시작점 = new int[32], kepanjangan_VALUE = new int[32];
    static int[] Diedit_TOC = new int[16384], edit_nama = new int[63];
    static int token_COUNT, edit_nama_kepanjangan, ukuran;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { Papan.직렬쓰기(VALUE); }
    static int baca_baris_masukan() { return editor_baris.Baca(); }
    static boolean 나누기(int Saiz) {
        int Kedudukan = 0, 끝 = 0; token_COUNT = 0;
        while (Kedudukan < Saiz) {
            while (Kedudukan < Saiz && (baris[Kedudukan] == 32 || baris[Kedudukan] == 9)) Kedudukan++;
            if (Kedudukan == Saiz) break;
            if (token_COUNT == 16) { 단말.Tulis("Perintah hurai_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[token_COUNT] = 끝; int Petikan_VALUE = 0;
            while (Kedudukan < Saiz) {
                int VALUE = baris[Kedudukan++];
                if (Petikan_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Petikan_VALUE) { Petikan_VALUE = 0; continue; }
                if (Petikan_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Petikan_VALUE = VALUE; continue; }
                token_VALUE[끝++] = VALUE;
            }
            if (Petikan_VALUE != 0) { 단말.Tulis("Perintah hurai_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            kepanjangan_VALUE[token_COUNT] = 끝 - 시작점[token_COUNT]; token_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Word_SMS) {
        if (INDEX >= token_COUNT) return false;
        int jawatan_INDEX=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int titik_kod=Word_SMS.charAt(순번);
            if (titik_kod>=0xd800 && titik_kod<=0xdbff && 순번+1<Word_SMS.length()) titik_kod=0x10000+((titik_kod-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int bait_COUNT=titik_kod<128?1:titik_kod<2048?2:titik_kod<65536?3:4;
            for (int jujukan_VALUE=bait_COUNT-1; jujukan_VALUE>=0; jujukan_VALUE--) {
                int VALUE=bait_COUNT==1?titik_kod:jujukan_VALUE==bait_COUNT-1?(bait_COUNT==2?0xc0:bait_COUNT==3?0xe0:0xf0)|(titik_kod>>(6*jujukan_VALUE)):0x80|((titik_kod>>(6*jujukan_VALUE))&63);
                if (jawatan_INDEX>=kepanjangan_VALUE[INDEX] || token_VALUE[시작점[INDEX]+jawatan_INDEX++]!=VALUE) return false;
            }
        }
        return jawatan_INDEX==kepanjangan_VALUE[INDEX];
    }
    static int LALUAN(int INDEX) {
        if (INDEX >= token_COUNT) return -22;
        int ukuran = Memori_Fail.laluan_Mula(kepanjangan_VALUE[INDEX]); if (ukuran < 0) return ukuran;
        for (int Loop_INDEX = 0; Loop_INDEX < kepanjangan_VALUE[INDEX]; Loop_INDEX++) {
            ukuran = Memori_Fail.laluan_bait(Loop_INDEX, token_VALUE[시작점[INDEX] + Loop_INDEX]); if (ukuran < 0) return ukuran;
        }
        return 0;
    }
    static void RALAT(int INDEX) { ukuran = 1; 단말.Tulis("RALAT "); 단말.수(INDEX); 단말.문자(10); }
    static void lihat_VALUE() {
        if (token_COUNT != 2) { 단말.Tulis("사용법: cat Fail\n"); return; }
        int ukuran = LALUAN(1); if (ukuran < 0) { RALAT(ukuran); return; }
        int Fail = Memori_Fail.Buka(0); if (Fail < 0) { RALAT(Fail); return; }
        while (true) { int VALUE = Memori_Fail.Baca(Fail); if (VALUE == 256) break; if (VALUE < 0) { RALAT(VALUE); break; } 원바이트(VALUE); }
        Memori_Fail.Tutup(Fail); 단말.문자(10);
    }
    static void edit_VALUE() {
        if (token_COUNT != 2) { 단말.Tulis("사용법: edit Fail\n"); return; }
        int ukuran = LALUAN(1); if (ukuran < 0) { RALAT(ukuran); return; }
        edit_nama_kepanjangan = kepanjangan_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < edit_nama_kepanjangan; Loop_INDEX++) edit_nama[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.Tulis("EDIT: Fail 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Saiz = 0;
        while (true) {
            단말.Tulis("edit> "); int 입력 = baca_baris_masukan();
            if (입력 < 0) { 단말.Tulis("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && baris[0] == '.') break;
            if (입력 + 1 > Diedit_TOC.length - Saiz) { 단말.Tulis("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) Diedit_TOC[Saiz++] = baris[Loop_INDEX];
            Diedit_TOC[Saiz++] = 10;
        }
        Memori_Fail.laluan_Mula(edit_nama_kepanjangan);
        for (int Loop_INDEX = 0; Loop_INDEX < edit_nama_kepanjangan; Loop_INDEX++) Memori_Fail.laluan_bait(Loop_INDEX, edit_nama[Loop_INDEX]);
        int Fail = Memori_Fail.Buka(577); if (Fail < 0) { RALAT(Fail); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Saiz; Loop_INDEX++) Memori_Fail.Tulis(Fail, Diedit_TOC[Loop_INDEX]);
        Memori_Fail.Tutup(Fail); 단말.Tulis("SAVED "); 단말.수(Saiz); 단말.Tulis("bait_VALUE(주기억 Fail)\n");
    }
    static int heks_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_COUNT != 2) { 단말.Tulis("사용법: load Fail | hex Fail\n"); return; }
        int ukuran = LALUAN(1); if (ukuran < 0) { RALAT(ukuran); return; }
        if (!넣기) {
            int Fail = Memori_Fail.Buka(0); if (Fail < 0) { RALAT(Fail); return; }
            단말.Tulis("HEX BEGIN "); 단말.수(Memori_Fail.Saiz(Fail)); 단말.문자(10);
            int pemasukan_COUNT = 0;
            while (true) {
                int VALUE = Memori_Fail.Baca(Fail); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++pemasukan_COUNT % 32 == 0) 단말.문자(10);
            }
            if (pemasukan_COUNT % 32 != 0) 단말.문자(10);
            Memori_Fail.Tutup(Fail); 단말.Tulis("HEX END\n"); return;
        }
        edit_nama_kepanjangan = kepanjangan_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < edit_nama_kepanjangan; Loop_INDEX++) edit_nama[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.Tulis("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Saiz = 0;
        while (true) {
            단말.Tulis("hex> "); int 입력 = baca_baris_masukan();
            if (입력 < 0) { 단말.Tulis("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && baris[0] == '.') break;
            int hadapan_VALUE = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (baris[Loop_INDEX] == 32 || baris[Loop_INDEX] == 9) continue;
                int VALUE = heks_VALUE(baris[Loop_INDEX]);
                if (VALUE < 0 || Saiz >= Diedit_TOC.length) { 단말.Tulis("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (hadapan_VALUE < 0) hadapan_VALUE = VALUE; else { Diedit_TOC[Saiz++] = hadapan_VALUE * 16 + VALUE; hadapan_VALUE = -1; }
            }
            if (hadapan_VALUE >= 0) { 단말.Tulis("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Memori_Fail.laluan_Mula(edit_nama_kepanjangan);
        for (int Loop_INDEX = 0; Loop_INDEX < edit_nama_kepanjangan; Loop_INDEX++) Memori_Fail.laluan_bait(Loop_INDEX, edit_nama[Loop_INDEX]);
        int Fail = Memori_Fail.Buka(577); if (Fail < 0) { RALAT(Fail); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Saiz; Loop_INDEX++) Memori_Fail.Tulis(Fail, Diedit_TOC[Loop_INDEX]);
        Memori_Fail.Tutup(Fail); 단말.Tulis("LOADED "); 단말.수(Saiz); 단말.Tulis("bait_VALUE(주기억 Fail)\n");
    }
    static int alat(int INDEX) {
        return alat_pemasukan(INDEX, 1);
    }
    static int alat_pemasukan(int INDEX, int Jalan) {
        if (token_COUNT - Jalan > 8) return -22;
        Papan.인수준비(token_COUNT - Jalan);
        for (int 첫값 = Jalan; 첫값 < token_COUNT; 첫값++) {
            if (kepanjangan_VALUE[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < kepanjangan_VALUE[첫값]; Loop_INDEX++) Papan.argumen_bait(첫값 - Jalan, Loop_INDEX, token_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? Papan.리눅스파일실행() : INDEX < 0 ? Papan.laksanakan_pengguna_fail() : Papan.jalankan_pengguna_aplikasi(INDEX);
    }
    static int PYTHON_pakej() {
        if (token_COUNT > 8) return -22;
        Papan.인수준비(token_COUNT);
        String LALUAN = "/lib/pakej.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int jawatan_INDEX = 0;
        for (int 순번 = 0; 순번 < LALUAN.length(); 순번++) {
            int aksara_VALUE = LALUAN.charAt(순번);
            if (aksara_VALUE < 128) Papan.argumen_bait(0, jawatan_INDEX++, aksara_VALUE);
            else { Papan.argumen_bait(0, jawatan_INDEX++, 0xe0 | (aksara_VALUE >> 12)); Papan.argumen_bait(0, jawatan_INDEX++, 0x80 | ((aksara_VALUE >> 6) & 63)); Papan.argumen_bait(0, jawatan_INDEX++, 0x80 | (aksara_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < token_COUNT; 순번++) {
            if (kepanjangan_VALUE[순번] > 255) return -36;
            for (int aksara_VALUE = 0; aksara_VALUE < kepanjangan_VALUE[순번]; aksara_VALUE++) Papan.argumen_bait(순번, aksara_VALUE, token_VALUE[시작점[순번] + aksara_VALUE]);
        }
        return Papan.jalankan_pengguna_aplikasi(12);
    }
    static int 실행형식() {
        int 처리값 = LALUAN(0); if (처리값 < 0) return 처리값;
        int Fail = Memori_Fail.Buka(0); if (Fail < 0) return Fail;
        int 첫값 = Memori_Fail.Baca(Fail), bait_data = Memori_Fail.Baca(Fail), titik_kod = Memori_Fail.Baca(Fail), 뒷값 = Memori_Fail.Baca(Fail);
        Memori_Fail.Tutup(Fail);
        if (첫값 == 127 && bait_data == 'E' && titik_kod == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && bait_data == 'K' && titik_kod == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String 인수) {
        Papan.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < 인수.length(); Loop_INDEX++) Papan.argumen_bait(0, Loop_INDEX, 인수.charAt(Loop_INDEX));
        return Papan.jalankan_pengguna_aplikasi(INDEX);
    }
    static void SMS_bait(int Fail, int VALUE) { Memori_Fail.Tulis(Fail, VALUE); }
    static void statik_fail(String Nama, String Kandungan_VALUE) {
        // pakej 파일명은 ASCII. Fail 내용은 UTF-8로 저장한다.
        Memori_Fail.laluan_Mula(Nama.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Nama.length(); Loop_INDEX++) Memori_Fail.laluan_bait(Loop_INDEX, Nama.charAt(Loop_INDEX));
        int Fail = Memori_Fail.Buka(193); if (Fail < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Kandungan_VALUE.length(); Loop_INDEX++) {
            int titik_kod = Kandungan_VALUE.charAt(Loop_INDEX);
            if (titik_kod >= 0xd800 && titik_kod <= 0xdbff && Loop_INDEX + 1 < Kandungan_VALUE.length()) titik_kod = 0x10000 + ((titik_kod - 0xd800) << 10) + Kandungan_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (titik_kod < 128) SMS_bait(Fail, titik_kod);
            else {
                int 수 = titik_kod < 2048 ? 2 : titik_kod < 65536 ? 3 : 4;
                SMS_bait(Fail, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (titik_kod >> (6 * (수 - 1))));
                for (int pemasukan_COUNT = 수 - 1; pemasukan_COUNT > 0; pemasukan_COUNT--) SMS_bait(Fail, 0x80 | ((titik_kod >> (6 * (pemasukan_COUNT - 1))) & 63));
            }
        }
        Memori_Fail.Tutup(Fail);
    }
    static void 한글도움말() {
        단말.Tulis("F9 / Shift+Space: [EN] ↔ [ms]\n");
        단말.Tulis("  [MS] keyboard; [EN] ASCII\n");
        단말.Tulis("  a → a\n");
        단말.Tulis("  F9: EN ↔ ms | Ctrl+Shift+V: UTF-8\n");
        단말.Tulis("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Tulis("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Nama) {
        int bait_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Nama.length(); Loop_INDEX++) { int titik_kod = Nama.charAt(Loop_INDEX); if (titik_kod >= 0xd800 && titik_kod <= 0xdfff) return -22; bait_COUNT += titik_kod < 128 ? 1 : titik_kod < 2048 ? 2 : 3; }
        int 처리값 = Memori_Fail.laluan_Mula(bait_COUNT); if (처리값 < 0) return 처리값;
        int jawatan_INDEX = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Nama.length(); Loop_INDEX++) {
            int titik_kod = Nama.charAt(Loop_INDEX);
            if (titik_kod < 128) Memori_Fail.laluan_bait(jawatan_INDEX++, titik_kod);
            else if (titik_kod < 2048) { Memori_Fail.laluan_bait(jawatan_INDEX++, 0xc0 | (titik_kod >> 6)); Memori_Fail.laluan_bait(jawatan_INDEX++, 0x80 | (titik_kod & 63)); }
            else { Memori_Fail.laluan_bait(jawatan_INDEX++, 0xe0 | (titik_kod >> 12)); Memori_Fail.laluan_bait(jawatan_INDEX++, 0x80 | ((titik_kod >> 6) & 63)); Memori_Fail.laluan_bait(jawatan_INDEX++, 0x80 | (titik_kod & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Nama) {
        int 처리값 = 예제경로(Nama); if (처리값 < 0) return 처리값;
        처리값 = Memori_Fail.cipta_direktori(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Nama, String data) {
        int 처리값 = 예제경로(Nama); if (처리값 < 0) return 처리값;
        int Fail = Memori_Fail.Buka(193); if (Fail == -17) return 0; if (Fail < 0) return Fail;
        for (int Loop_INDEX = 0; Loop_INDEX < data.length(); Loop_INDEX += 2) {
            처리값 = Memori_Fail.Tulis(Fail, heks_VALUE(data.charAt(Loop_INDEX)) * 16 + heks_VALUE(data.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { Memori_Fail.Tutup(Fail); return 처리값; }
        }
        return Memori_Fail.Tutup(Fail);
    }
    static void paparkan_bantuan() {
        sistem_alat.paparkan_bantuan();
        단말.Tulis("sshd / selamat_cangkerang start|stop|status: SSH :22 (user, 장치별 kata_laluan_VALUE)\n");
        단말.Tulis("vncd / jauh_papar start|stop|status: VNC :5900 (장치별 kata_laluan_VALUE)\n");
        단말.Tulis("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Tulis("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Tulis("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Tulis("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Tulis("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Tulis("모서리 + 왼쪽 버튼 seret_VALUE: Terminal Saiz ubah_VALUE; terminal size: lajur_VALUE/ROW_VALUE\n");
        단말.Tulis("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Tulis("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Tulis("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Tulis("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Tulis("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Tulis("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Tulis("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Tulis("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Tulis("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Tulis("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Tulis("pip: MicroPython sumber_pepohon pasang_VALUE; hos --network --pip 필요; /lib는 RAM\n");
        단말.Tulis("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Tulis("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Tulis("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Tulis("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void Terminal(boolean 전환여부) {
        if (전환여부 && Papan.Terminal(2) != 0) { Papan.Terminal(0); 단말.Tulis("TERMINAL CLOSED\n"); }
        else if (Papan.Terminal(1) < 0) RALAT(-19);
        else 단말.Tulis("TERMINAL READY — ms terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Perintah() {
        if (token_COUNT == 0) return;
        if (sistem_alat.laksanakan_perintah()) return;
        if (같음(0,"sshd") || 같음(0,"selamat_cangkerang") || 같음(0,"vncd") || 같음(0,"jauh_papar")) {
            int 종류=같음(0,"vncd")||같음(0,"jauh_papar")?1:0;
            int Aksi=같음(1,"start")||같음(1,"Jalan")?1:같음(1,"stop")||같음(1,"Henti")?0:2;
            int status_VALUE=Papan.pembayangan(종류,Aksi);
            if(status_VALUE<0)RALAT(status_VALUE);else 단말.Tulis(Papan.pembayangan(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else paparkan_bantuan(); }
        else if (같음(0, "info") || 같음(0, "i")) kernel.msinfo32_exe();
        else if (같음(0, "pwd")) { Memori_Fail.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_COUNT == 1) { Memori_Fail.laluan_Mula(1); 처리값 = Memori_Fail.laluan_bait(0, '/'); } else 처리값 = token_COUNT == 2 ? LALUAN(1) : -22;
            if (처리값 >= 0) 처리값 = Memori_Fail.ubah_direktori(); if (처리값 < 0) RALAT(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argumen_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_COUNT == argumen_INDEX) { Memori_Fail.laluan_Mula(1); 처리값 = Memori_Fail.laluan_bait(0, '.'); } else 처리값 = token_COUNT == argumen_INDEX + 1 ? LALUAN(argumen_INDEX) : -22;
            if (처리값 >= 0) 처리값 = Memori_Fail.경로목록(); if (처리값 < 0) RALAT(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) cangkerang_Alat.fail_kes(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) cangkerang_Alat.tika_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) cangkerang_Alat.lihat_VALUE();
        else if (같음(0, "wc")) cangkerang_Alat.세기();
        else if (같음(0, "grep")) cangkerang_Alat.Cari_pemasukan();
        else if (같음(0, "head") || 같음(0, "tail")) cangkerang_Alat.머리(같음(0, "tail"));
        else if (같음(0, "tee")) cangkerang_Alat.tulis_Bersama_sama();
        else if (같음(0, "env")) cangkerang_sintaks.tayang_persekitaran();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_COUNT == 1) cangkerang_sintaks.tayang_persekitaran();
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = cangkerang_sintaks.persekitaran_Seting(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { ukuran = 처리값; 단말.Tulis("Perintah hurai_VALUE: pemboleh_ubah_VALUE 이름이 잘못되었거나 예약된 이름이거나 persekitaran 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) cangkerang_sintaks.laksanakan_fail();
        else if (같음(0, "true")) ukuran = 0;
        else if (같음(0, "false")) ukuran = 1;
        else if (같음(0, "history")) editor_baris.tayang_LOG();
        else if (같음(0, "exit")) {
            if (cangkerang_sintaks.깊이 > 0) { ukuran = token_COUNT == 1 ? cangkerang_sintaks.status_VALUE : cangkerang_Alat.digit_VALUE(1); if (ukuran < 0 || ukuran > 255) ukuran = 2; cangkerang_sintaks.skrip_tamat = true; }
            else if (Papan.Terminal(2) != 0) Terminal(true);
            else 단말.Tulis("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) edit_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_COUNT < 2) { ukuran = 2; 단말.Tulis("사용법: rm Fail...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = LALUAN(Loop_INDEX); if (처리값 == 0) 처리값 = Memori_Fail.padam_pemasukan(); if (처리값 < 0) RALAT(처리값); }
        }
        else if (같음(0, "echo")) {
            int Mula_jawatan = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Mula_jawatan; 첫값 < token_COUNT; 첫값++) { if (첫값 > Mula_jawatan) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < kepanjangan_VALUE[첫값]; Loop_INDEX++) Papan.직렬쓰기(token_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (Mula_jawatan == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Tulis("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_pakej() : alat(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); ukuran = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !cangkerang_sintaks.연결중) { 단말.Tulis("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = alat(13); ukuran = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = alat(15); ukuran = 처리값 < 0 ? 126 : 처리값; if (!cangkerang_sintaks.연결중) { 단말.Tulis("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = alat(16); ukuran = 처리값 < 0 ? 126 : 처리값; if (!cangkerang_sintaks.연결중) { 단말.Tulis("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Saiz = Papan.Terminal(13); 단말.Tulis("TERMINAL SIZE "); 단말.수(Saiz & 65535); 단말.문자('x'); 단말.수(Saiz >>> 16); 단말.문자(10); }
            else Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Papan.Terminal(9); meja.laksanakan_perintah(); }
        else if (같음(0, "c")) kernel.ujian_C();
        else if (같음(0, "tasks") || 같음(0, "t")) kernel.ujian_Tasks();
        else if (같음(0, "g")) kernel.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) kernel.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Papan.jalankan_pengguna_aplikasi(0); if (처리값 == 0) 단말.Tulis("ELF DEMO PASS\n"); else RALAT(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? alat_pemasukan(-2, 2) : alat(-1); ukuran = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !cangkerang_sintaks.연결중) { 단말.Tulis("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) kernel.ujian_Rangkaian();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Papan.pemindahan_fail_khidmat(1); if (처리값 < 0) RALAT(처리값); else { 단말.Tulis("FTP listening "); sistem_alat.tulis_e_mel(Papan.rangkaian_status(0,0)); 단말.Tulis(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Papan.pemindahan_fail_khidmat(0); 단말.Tulis("FTP stopped\n"); }
            else 단말.Tulis(Papan.pemindahan_fail_khidmat(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { pakej.Sediakan(); 단말.Tulis("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Bahasa = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_COUNT != 2 || Bahasa < 0) 단말.Tulis("example java|c|python: 출력, Fail, 네트워크, 그래픽, Java Swing Tetingkap 예제\n");
            else { int 처리값 = 예제꾸러미.pasang_VALUE(Bahasa); if (처리값 < 0) { RALAT(처리값); if (처리값 == -28) 단말.Tulis("RAM full: remove unused files, then retry example\n"); } else 단말.Tulis("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_VALUE = 실행형식();
            if (format_VALUE == 1 || format_VALUE == 2) {
                int 처리값 = alat_pemasukan(format_VALUE == 1 ? -1 : 14, 0); ukuran = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !cangkerang_sintaks.연결중) { 단말.Tulis("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (format_VALUE == 0) { ukuran = 126; 단말.Tulis("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { ukuran = 127; 단말.Tulis("Unknown command. help: commands\n"); }
        }
    }
    public static void laksanakan_perintah() {
        pakej.Sediakan();
        for (int Bahasa = 0; Bahasa < 3; Bahasa++) { int 처리값 = 예제꾸러미.pasang_VALUE(Bahasa); if (처리값 < 0) RALAT(처리값); }
        paparkan_bantuan();
        while (true) {
            tetingkap_sesi.Proses_VALUE_pemasukan(); if (tetingkap_sesi.재개()) continue;
            if (!tetingkap_sesi.이어읽기) 단말.Tulis("jkoros-native> "); editor_baris.baris_perintah = true; Papan.jauh_tunggu(1); int Saiz = baca_baris_masukan(); Papan.jauh_tunggu(0); editor_baris.baris_perintah = false;
            if (Saiz == -3) continue;
            if (Saiz == -2) 단말.Tulis("Perintah hurai_VALUE: 명령줄이 너무 깁니다\n");
            if (Saiz >= 0) { cangkerang_sintaks.skrip_tamat = false; cangkerang_sintaks.laksanakan_perintah(baris, 0, Saiz, 0); } else cangkerang_sintaks.status_VALUE = 130;
            Papan.tamat_jauh_perintah(cangkerang_sintaks.status_VALUE);
            editor_baris.Saiz = editor_baris.kursor_VALUE = editor_baris.Mula_tetingkap = 0;
        }
    }
}
