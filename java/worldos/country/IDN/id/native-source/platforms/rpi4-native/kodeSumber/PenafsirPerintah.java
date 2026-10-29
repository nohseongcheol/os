// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 baris_perintah. Kutipan, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class PenafsirPerintah {
    static int[] baris_masukan = new int[4096], token_VALUE = new int[4096], 시작점 = new int[32], panjang_VALUE = new int[32];
    static int[] Diedit_Isi = new int[16384], Edit_nama = new int[63];
    static int token_COUNT, Edit_nama_panjang, hasil;
    static boolean 앞줄;
    static void 원바이트(int VALUE) { Papan.직렬쓰기(VALUE); }
    static int baca_baris_masukan() { return editor_baris.Baca(); }
    static boolean 나누기(int Ukuran) {
        int posisi = 0, 끝 = 0; token_COUNT = 0;
        while (posisi < Ukuran) {
            while (posisi < Ukuran && (baris_masukan[posisi] == 32 || baris_masukan[posisi] == 9)) posisi++;
            if (posisi == Ukuran) break;
            if (token_COUNT == 16) { 단말.Tulis("perintah urai_VALUE: 인수가 너무 많습니다\n"); return false; }
            시작점[token_COUNT] = 끝; int Kutipan_VALUE = 0;
            while (posisi < Ukuran) {
                int VALUE = baris_masukan[posisi++];
                if (Kutipan_VALUE == 0 && (VALUE == 32 || VALUE == 9)) break;
                if (VALUE == Kutipan_VALUE) { Kutipan_VALUE = 0; continue; }
                if (Kutipan_VALUE == 0 && (VALUE == 39 || VALUE == 34)) { Kutipan_VALUE = VALUE; continue; }
                token_VALUE[끝++] = VALUE;
            }
            if (Kutipan_VALUE != 0) { 단말.Tulis("perintah urai_VALUE: 따옴표가 닫히지 않았습니다\n"); return false; }
            panjang_VALUE[token_COUNT] = 끝 - 시작점[token_COUNT]; token_COUNT++;
        }
        return true;
    }
    static boolean 같음(int INDEX, String Kata_SMS) {
        if (INDEX >= token_COUNT) return false;
        int posisi_INDEX=0;
        for (int 순번=0; 순번<Kata_SMS.length(); 순번++) {
            int kode_karakter=Kata_SMS.charAt(순번);
            if (kode_karakter>=0xd800 && kode_karakter<=0xdbff && 순번+1<Kata_SMS.length()) kode_karakter=0x10000+((kode_karakter-0xd800)<<10)+Kata_SMS.charAt(++순번)-0xdc00;
            int byte_COUNT=kode_karakter<128?1:kode_karakter<2048?2:kode_karakter<65536?3:4;
            for (int urutan_VALUE_e9fa7815=byte_COUNT-1; urutan_VALUE_e9fa7815>=0; urutan_VALUE_e9fa7815--) {
                int VALUE=byte_COUNT==1?kode_karakter:urutan_VALUE_e9fa7815==byte_COUNT-1?(byte_COUNT==2?0xc0:byte_COUNT==3?0xe0:0xf0)|(kode_karakter>>(6*urutan_VALUE_e9fa7815)):0x80|((kode_karakter>>(6*urutan_VALUE_e9fa7815))&63);
                if (posisi_INDEX>=panjang_VALUE[INDEX] || token_VALUE[시작점[INDEX]+posisi_INDEX++]!=VALUE) return false;
            }
        }
        return posisi_INDEX==panjang_VALUE[INDEX];
    }
    static int jalur(int INDEX) {
        if (INDEX >= token_COUNT) return -22;
        int hasil = BerkasMemori.jalur_Mulai(panjang_VALUE[INDEX]); if (hasil < 0) return hasil;
        for (int Loop_INDEX = 0; Loop_INDEX < panjang_VALUE[INDEX]; Loop_INDEX++) {
            hasil = BerkasMemori.jalur_byte(Loop_INDEX, token_VALUE[시작점[INDEX] + Loop_INDEX]); if (hasil < 0) return hasil;
        }
        return 0;
    }
    static void galat(int INDEX) { hasil = 1; 단말.Tulis("galat "); 단말.수(INDEX); 단말.문자(10); }
    static void Tampilan_VALUE() {
        if (token_COUNT != 2) { 단말.Tulis("사용법: cat berkas\n"); return; }
        int hasil = jalur(1); if (hasil < 0) { galat(hasil); return; }
        int berkas = BerkasMemori.Buka(0); if (berkas < 0) { galat(berkas); return; }
        while (true) { int VALUE = BerkasMemori.Baca(berkas); if (VALUE == 256) break; if (VALUE < 0) { galat(VALUE); break; } 원바이트(VALUE); }
        BerkasMemori.Tutup(berkas); 단말.문자(10);
    }
    static void Edit_VALUE() {
        if (token_COUNT != 2) { 단말.Tulis("사용법: edit berkas\n"); return; }
        int hasil = jalur(1); if (hasil < 0) { galat(hasil); return; }
        Edit_nama_panjang = panjang_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < Edit_nama_panjang; Loop_INDEX++) Edit_nama[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.Tulis("EDIT: berkas 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Ukuran = 0;
        while (true) {
            단말.Tulis("edit> "); int 입력 = baca_baris_masukan();
            if (입력 < 0) { 단말.Tulis("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && baris_masukan[0] == '.') break;
            if (입력 + 1 > Diedit_Isi.length - Ukuran) { 단말.Tulis("EDIT CANCELLED: file too large\n"); return; }
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) Diedit_Isi[Ukuran++] = baris_masukan[Loop_INDEX];
            Diedit_Isi[Ukuran++] = 10;
        }
        BerkasMemori.jalur_Mulai(Edit_nama_panjang);
        for (int Loop_INDEX = 0; Loop_INDEX < Edit_nama_panjang; Loop_INDEX++) BerkasMemori.jalur_byte(Loop_INDEX, Edit_nama[Loop_INDEX]);
        int berkas = BerkasMemori.Buka(577); if (berkas < 0) { galat(berkas); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Ukuran; Loop_INDEX++) BerkasMemori.Tulis(berkas, Diedit_Isi[Loop_INDEX]);
        BerkasMemori.Tutup(berkas); 단말.Tulis("SAVED "); 단말.수(Ukuran); 단말.Tulis("byte_VALUE(주기억 berkas)\n");
    }
    static int heks_VALUE(int VALUE) {
        if (VALUE >= '0' && VALUE <= '9') return VALUE - '0';
        if (VALUE >= 'a' && VALUE <= 'f') return VALUE - 'a' + 10;
        if (VALUE >= 'A' && VALUE <= 'F') return VALUE - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (token_COUNT != 2) { 단말.Tulis("사용법: load berkas | hex berkas\n"); return; }
        int hasil = jalur(1); if (hasil < 0) { galat(hasil); return; }
        if (!넣기) {
            int berkas = BerkasMemori.Buka(0); if (berkas < 0) { galat(berkas); return; }
            단말.Tulis("HEX BEGIN "); 단말.수(BerkasMemori.Ukuran(berkas)); 단말.문자(10);
            int entri_COUNT = 0;
            while (true) {
                int VALUE = BerkasMemori.Baca(berkas); if (VALUE < 0 || VALUE == 256) break;
                단말.문자("0123456789abcdef".charAt(VALUE >> 4)); 단말.문자("0123456789abcdef".charAt(VALUE & 15));
                if (++entri_COUNT % 32 == 0) 단말.문자(10);
            }
            if (entri_COUNT % 32 != 0) 단말.문자(10);
            BerkasMemori.Tutup(berkas); 단말.Tulis("HEX END\n"); return;
        }
        Edit_nama_panjang = panjang_VALUE[1];
        for (int Loop_INDEX = 0; Loop_INDEX < Edit_nama_panjang; Loop_INDEX++) Edit_nama[Loop_INDEX] = token_VALUE[시작점[1] + Loop_INDEX];
        단말.Tulis("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Ukuran = 0;
        while (true) {
            단말.Tulis("hex> "); int 입력 = baca_baris_masukan();
            if (입력 < 0) { 단말.Tulis("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && baris_masukan[0] == '.') break;
            int depan_VALUE = -1;
            for (int Loop_INDEX = 0; Loop_INDEX < 입력; Loop_INDEX++) {
                if (baris_masukan[Loop_INDEX] == 32 || baris_masukan[Loop_INDEX] == 9) continue;
                int VALUE = heks_VALUE(baris_masukan[Loop_INDEX]);
                if (VALUE < 0 || Ukuran >= Diedit_Isi.length) { 단말.Tulis("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (depan_VALUE < 0) depan_VALUE = VALUE; else { Diedit_Isi[Ukuran++] = depan_VALUE * 16 + VALUE; depan_VALUE = -1; }
            }
            if (depan_VALUE >= 0) { 단말.Tulis("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        BerkasMemori.jalur_Mulai(Edit_nama_panjang);
        for (int Loop_INDEX = 0; Loop_INDEX < Edit_nama_panjang; Loop_INDEX++) BerkasMemori.jalur_byte(Loop_INDEX, Edit_nama[Loop_INDEX]);
        int berkas = BerkasMemori.Buka(577); if (berkas < 0) { galat(berkas); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Ukuran; Loop_INDEX++) BerkasMemori.Tulis(berkas, Diedit_Isi[Loop_INDEX]);
        BerkasMemori.Tutup(berkas); 단말.Tulis("LOADED "); 단말.수(Ukuran); 단말.Tulis("byte_VALUE(주기억 berkas)\n");
    }
    static int alat(int INDEX) {
        return alat_entri(INDEX, 1);
    }
    static int alat_entri(int INDEX, int jalankan) {
        if (token_COUNT - jalankan > 8) return -22;
        Papan.인수준비(token_COUNT - jalankan);
        for (int 첫값 = jalankan; 첫값 < token_COUNT; 첫값++) {
            if (panjang_VALUE[첫값] > 255) return -36;
            for (int Loop_INDEX = 0; Loop_INDEX < panjang_VALUE[첫값]; Loop_INDEX++) Papan.argumen_byte(첫값 - jalankan, Loop_INDEX, token_VALUE[시작점[첫값] + Loop_INDEX]);
        }
        return INDEX == -2 ? Papan.리눅스파일실행() : INDEX < 0 ? Papan.Jalankan_pengguna_file() : Papan.eksekusi_pengguna_apl(INDEX);
    }
    static int PYTHON_paket() {
        if (token_COUNT > 8) return -22;
        Papan.인수준비(token_COUNT);
        String jalur = "/lib/paket.py";
        // Java 문자열을 셸의 UTF-8 argumen 버퍼에 기록한다.
        int posisi_INDEX = 0;
        for (int 순번 = 0; 순번 < jalur.length(); 순번++) {
            int karakter_VALUE = jalur.charAt(순번);
            if (karakter_VALUE < 128) Papan.argumen_byte(0, posisi_INDEX++, karakter_VALUE);
            else { Papan.argumen_byte(0, posisi_INDEX++, 0xe0 | (karakter_VALUE >> 12)); Papan.argumen_byte(0, posisi_INDEX++, 0x80 | ((karakter_VALUE >> 6) & 63)); Papan.argumen_byte(0, posisi_INDEX++, 0x80 | (karakter_VALUE & 63)); }
        }
        for (int 순번 = 1; 순번 < token_COUNT; 순번++) {
            if (panjang_VALUE[순번] > 255) return -36;
            for (int karakter_VALUE = 0; karakter_VALUE < panjang_VALUE[순번]; karakter_VALUE++) Papan.argumen_byte(순번, karakter_VALUE, token_VALUE[시작점[순번] + karakter_VALUE]);
        }
        return Papan.eksekusi_pengguna_apl(12);
    }
    static int 실행형식() {
        int 처리값 = jalur(0); if (처리값 < 0) return 처리값;
        int berkas = BerkasMemori.Buka(0); if (berkas < 0) return berkas;
        int 첫값 = BerkasMemori.Baca(berkas), byte_data = BerkasMemori.Baca(berkas), kode_karakter = BerkasMemori.Baca(berkas), berikutnya_VALUE = BerkasMemori.Baca(berkas);
        BerkasMemori.Tutup(berkas);
        if (첫값 == 127 && byte_data == 'E' && kode_karakter == 'L' && berikutnya_VALUE == 'F') return 1;
        if (첫값 == 'P' && byte_data == 'K' && kode_karakter == 3 && berikutnya_VALUE == 4) return 2;
        return 0;
    }
    static int 예제실행(int INDEX, String argumen) {
        Papan.인수준비(1);
        for (int Loop_INDEX = 0; Loop_INDEX < argumen.length(); Loop_INDEX++) Papan.argumen_byte(0, Loop_INDEX, argumen.charAt(Loop_INDEX));
        return Papan.eksekusi_pengguna_apl(INDEX);
    }
    static void SMS_byte(int berkas, int VALUE) { BerkasMemori.Tulis(berkas, VALUE); }
    static void statik_file(String Nama_2, String Isi_VALUE) {
        // paket 파일명은 ASCII. berkas 내용은 UTF-8로 저장한다.
        BerkasMemori.jalur_Mulai(Nama_2.length());
        for (int Loop_INDEX = 0; Loop_INDEX < Nama_2.length(); Loop_INDEX++) BerkasMemori.jalur_byte(Loop_INDEX, Nama_2.charAt(Loop_INDEX));
        int berkas = BerkasMemori.Buka(193); if (berkas < 0) return;
        for (int Loop_INDEX = 0; Loop_INDEX < Isi_VALUE.length(); Loop_INDEX++) {
            int kode_karakter = Isi_VALUE.charAt(Loop_INDEX);
            if (kode_karakter >= 0xd800 && kode_karakter <= 0xdbff && Loop_INDEX + 1 < Isi_VALUE.length()) kode_karakter = 0x10000 + ((kode_karakter - 0xd800) << 10) + Isi_VALUE.charAt(++Loop_INDEX) - 0xdc00;
            if (kode_karakter < 128) SMS_byte(berkas, kode_karakter);
            else {
                int 수 = kode_karakter < 2048 ? 2 : kode_karakter < 65536 ? 3 : 4;
                SMS_byte(berkas, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (kode_karakter >> (6 * (수 - 1))));
                for (int entri_COUNT = 수 - 1; entri_COUNT > 0; entri_COUNT--) SMS_byte(berkas, 0x80 | ((kode_karakter >> (6 * (entri_COUNT - 1))) & 63));
            }
        }
        BerkasMemori.Tutup(berkas);
    }
    static void 한글도움말() {
        단말.Tulis("Tekan F9 atau Shift+Space untuk mengetik dalam bahasa Indonesia.\n");
        단말.Tulis("  [ID] keyboard; [EN] ASCII\n");
        단말.Tulis("  a → a\n");
        단말.Tulis("  F9: EN ↔ id | Ctrl+Shift+V: UTF-8\n");
        단말.Tulis("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Tulis("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Nama_2) {
        int byte_COUNT = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Nama_2.length(); Loop_INDEX++) { int kode_karakter = Nama_2.charAt(Loop_INDEX); if (kode_karakter >= 0xd800 && kode_karakter <= 0xdfff) return -22; byte_COUNT += kode_karakter < 128 ? 1 : kode_karakter < 2048 ? 2 : 3; }
        int 처리값 = BerkasMemori.jalur_Mulai(byte_COUNT); if (처리값 < 0) return 처리값;
        int posisi_INDEX = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Nama_2.length(); Loop_INDEX++) {
            int kode_karakter = Nama_2.charAt(Loop_INDEX);
            if (kode_karakter < 128) BerkasMemori.jalur_byte(posisi_INDEX++, kode_karakter);
            else if (kode_karakter < 2048) { BerkasMemori.jalur_byte(posisi_INDEX++, 0xc0 | (kode_karakter >> 6)); BerkasMemori.jalur_byte(posisi_INDEX++, 0x80 | (kode_karakter & 63)); }
            else { BerkasMemori.jalur_byte(posisi_INDEX++, 0xe0 | (kode_karakter >> 12)); BerkasMemori.jalur_byte(posisi_INDEX++, 0x80 | ((kode_karakter >> 6) & 63)); BerkasMemori.jalur_byte(posisi_INDEX++, 0x80 | (kode_karakter & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Nama_2) {
        int 처리값 = 예제경로(Nama_2); if (처리값 < 0) return 처리값;
        처리값 = BerkasMemori.Buat_Direktori(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Nama_2, String data) {
        int 처리값 = 예제경로(Nama_2); if (처리값 < 0) return 처리값;
        int berkas = BerkasMemori.Buka(193); if (berkas == -17) return 0; if (berkas < 0) return berkas;
        for (int Loop_INDEX = 0; Loop_INDEX < data.length(); Loop_INDEX += 2) {
            처리값 = BerkasMemori.Tulis(berkas, heks_VALUE(data.charAt(Loop_INDEX)) * 16 + heks_VALUE(data.charAt(Loop_INDEX + 1)));
            if (처리값 < 0) { BerkasMemori.Tutup(berkas); return 처리값; }
        }
        return BerkasMemori.Tutup(berkas);
    }
    static void tampilkan_bantuan() {
        sistem_alat.tampilkan_bantuan();
        단말.Tulis("sshd / aman_shell start|stop|status: SSH :22 (user, 장치별 sandi_VALUE)\n");
        단말.Tulis("vncd / jarak_jauh_tampilan start|stop|status: VNC :5900 (장치별 sandi_VALUE)\n");
        단말.Tulis("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Tulis("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Tulis("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Tulis("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Tulis("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Tulis("모서리 + 왼쪽 버튼 seret_VALUE: terminal Ukuran ubah_VALUE; terminal size: kolom_VALUE/ROW_VALUE\n");
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
        단말.Tulis("pip: MicroPython sumber_pohon instal_VALUE; host --network --pip 필요; /lib는 RAM\n");
        단말.Tulis("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Tulis("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Tulis("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Tulis("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void terminal(boolean 전환여부) {
        if (전환여부 && Papan.terminal(2) != 0) { Papan.terminal(0); 단말.Tulis("TERMINAL CLOSED\n"); }
        else if (Papan.terminal(1) < 0) galat(-19);
        else 단말.Tulis("TERMINAL READY — id terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void perintah() {
        if (token_COUNT == 0) return;
        if (sistem_alat.Jalankan_perintah()) return;
        if (같음(0,"sshd") || 같음(0,"aman_shell") || 같음(0,"vncd") || 같음(0,"jarak_jauh_tampilan")) {
            int 종류=같음(0,"vncd")||같음(0,"jarak_jauh_tampilan")?1:0;
            int Aksi=같음(1,"start")||같음(1,"jalankan")?1:같음(1,"stop")||같음(1,"Hentikan")?0:2;
            int Status_VALUE=Papan.bayangan(종류,Aksi);
            if(Status_VALUE<0)galat(Status_VALUE);else 단말.Tulis(Papan.bayangan(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else tampilkan_bantuan(); }
        else if (같음(0, "info") || 같음(0, "i")) Inti.msinfo32_exe();
        else if (같음(0, "pwd")) { BerkasMemori.saat_ini_tulis(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (token_COUNT == 1) { BerkasMemori.jalur_Mulai(1); 처리값 = BerkasMemori.jalur_byte(0, '/'); } else 처리값 = token_COUNT == 2 ? jalur(1) : -22;
            if (처리값 >= 0) 처리값 = BerkasMemori.ubah_Direktori(); if (처리값 < 0) galat(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argumen_INDEX = 같음(1, "-l") ? 2 : 1, 처리값;
            if (token_COUNT == argumen_INDEX) { BerkasMemori.jalur_Mulai(1); 처리값 = BerkasMemori.jalur_byte(0, '.'); } else 처리값 = token_COUNT == argumen_INDEX + 1 ? jalur(argumen_INDEX) : -22;
            if (처리값 >= 0) 처리값 = BerkasMemori.경로목록(); if (처리값 < 0) galat(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) shell_Alat.file_Tugas(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) shell_Alat.salin_VALUE(같음(0, "mv"));
        else if (같음(0, "cat")) shell_Alat.Tampilan_VALUE();
        else if (같음(0, "wc")) shell_Alat.세기();
        else if (같음(0, "grep")) shell_Alat.FIND_entri();
        else if (같음(0, "head") || 같음(0, "tail")) shell_Alat.kepala_VALUE(같음(0, "tail"));
        else if (같음(0, "tee")) shell_Alat.tulis_Kebersamaan();
        else if (같음(0, "env")) shell_sintaksis.show_lingkungan();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (token_COUNT == 1) shell_sintaksis.show_lingkungan();
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = shell_sintaksis.lingkungan_Pengaturan(Loop_INDEX, 같음(0, "unset")); if (처리값 != 0) { hasil = 처리값; 단말.Tulis("perintah urai_VALUE: variabel_VALUE 이름이 잘못되었거나 예약된 이름이거나 lingkungan 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) shell_sintaksis.Jalankan_file();
        else if (같음(0, "true")) hasil = 0;
        else if (같음(0, "false")) hasil = 1;
        else if (같음(0, "history")) editor_baris.show_LOG();
        else if (같음(0, "exit")) {
            if (shell_sintaksis.깊이 > 0) { hasil = token_COUNT == 1 ? shell_sintaksis.Status_VALUE : shell_Alat.angka_VALUE(1); if (hasil < 0 || hasil > 255) hasil = 2; shell_sintaksis.skrip_mengakhiri = true; }
            else if (Papan.terminal(2) != 0) terminal(true);
            else 단말.Tulis("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) Edit_VALUE();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (token_COUNT < 2) { hasil = 2; 단말.Tulis("사용법: rm berkas...\n"); }
            for (int Loop_INDEX = 1; Loop_INDEX < token_COUNT; Loop_INDEX++) { int 처리값 = jalur(Loop_INDEX); if (처리값 == 0) 처리값 = BerkasMemori.hapus_entri_c8dbc399(); if (처리값 < 0) galat(처리값); }
        }
        else if (같음(0, "echo")) {
            int Mulai_posisi = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = Mulai_posisi; 첫값 < token_COUNT; 첫값++) { if (첫값 > Mulai_posisi) 단말.문자(32); for (int Loop_INDEX = 0; Loop_INDEX < panjang_VALUE[첫값]; Loop_INDEX++) Papan.직렬쓰기(token_VALUE[시작점[첫값] + Loop_INDEX]); }
            if (Mulai_posisi == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Tulis("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? PYTHON_paket() : alat(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); hasil = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !shell_sintaksis.연결중) { 단말.Tulis("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = alat(13); hasil = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = alat(15); hasil = 처리값 < 0 ? 126 : 처리값; if (!shell_sintaksis.연결중) { 단말.Tulis("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = alat(16); hasil = 처리값 < 0 ? 126 : 처리값; if (!shell_sintaksis.연결중) { 단말.Tulis("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Ukuran = Papan.terminal(13); 단말.Tulis("TERMINAL SIZE "); 단말.수(Ukuran & 65535); 단말.문자('x'); 단말.수(Ukuran >>> 16); 단말.문자(10); }
            else terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { Papan.terminal(9); desktop.Jalankan_perintah(); }
        else if (같음(0, "c")) Inti.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) Inti.작업시험();
        else if (같음(0, "g")) Inti.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) Inti.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = Papan.eksekusi_pengguna_apl(0); if (처리값 == 0) 단말.Tulis("ELF DEMO PASS\n"); else galat(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? alat_entri(-2, 2) : alat(-1); hasil = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !shell_sintaksis.연결중) { 단말.Tulis("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) Inti.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = Papan.transfer_file_layanan(1); if (처리값 < 0) galat(처리값); else { 단말.Tulis("FTP listening "); sistem_alat.tulis_surel(Papan.jaringan_status(0,0)); 단말.Tulis(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { Papan.transfer_file_layanan(0); 단말.Tulis("FTP stopped\n"); }
            else 단말.Tulis(Papan.transfer_file_layanan(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { paket.Siapkan(); 단말.Tulis("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Bahasa = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (token_COUNT != 2 || Bahasa < 0) 단말.Tulis("example java|c|python: keluaranTeks, berkas, 네트워크, 그래픽, Java Swing Jendela 예제\n");
            else { int 처리값 = 예제꾸러미.instal_VALUE(Bahasa); if (처리값 < 0) { galat(처리값); if (처리값 == -28) 단말.Tulis("RAM full: remove unused files, then retry example\n"); } else 단말.Tulis("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_VALUE = 실행형식();
            if (format_VALUE == 1 || format_VALUE == 2) {
                int 처리값 = alat_entri(format_VALUE == 1 ? -1 : 14, 0); hasil = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !shell_sintaksis.연결중) { 단말.Tulis("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (format_VALUE == 0) { hasil = 126; 단말.Tulis("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { hasil = 127; 단말.Tulis("Unknown command. help: commands\n"); }
        }
    }
    public static void Jalankan_perintah() {
        paket.Siapkan();
        for (int Bahasa = 0; Bahasa < 3; Bahasa++) { int 처리값 = 예제꾸러미.instal_VALUE(Bahasa); if (처리값 < 0) galat(처리값); }
        tampilkan_bantuan();
        while (true) {
            jendela_sesi.Proses_VALUE_entri(); if (jendela_sesi.재개()) continue;
            if (!jendela_sesi.이어읽기) 단말.Tulis("jkoros-native> "); editor_baris.baris_perintah = true; Papan.jarak_jauh_tunggu(1); int Ukuran = baca_baris_masukan(); Papan.jarak_jauh_tunggu(0); editor_baris.baris_perintah = false;
            if (Ukuran == -3) continue;
            if (Ukuran == -2) 단말.Tulis("perintah urai_VALUE: 명령줄이 너무 깁니다\n");
            if (Ukuran >= 0) { shell_sintaksis.skrip_mengakhiri = false; shell_sintaksis.Jalankan_perintah(baris_masukan, 0, Ukuran, 0); } else shell_sintaksis.Status_VALUE = 130;
            Papan.mengakhiri_jarak_jauh_perintah(shell_sintaksis.Status_VALUE);
            editor_baris.Ukuran = editor_baris.kursor_VALUE = editor_baris.Mulai_jendela = 0;
        }
    }
}
