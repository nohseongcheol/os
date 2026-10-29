// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 buýruk_setiri. 따옴표, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] setir = new int[4096], token_baha = new int[4096], 시작점 = new int[32], dowamlylyk_baha = new int[32];
    static int[] 편집내용 = new int[16384], redaktirle_at = new int[63];
    static int 토큰수, redaktirle_at_dowamlylyk, 결과;
    static boolean 앞줄;
    static void 원바이트(int baha) { 보드.직렬쓰기(baha); }
    static int 줄읽기() { return setir_Redaktor.Oka(); }
    static boolean 나누기(int Ululyk) {
        int 위치 = 0, 끝 = 0; 토큰수 = 0;
        while (위치 < Ululyk) {
            while (위치 < Ululyk && (setir[위치] == 32 || setir[위치] == 9)) 위치++;
            if (위치 == Ululyk) break;
            if (토큰수 == 16) { 단말.Ýaz("buýruk seljer_baha: 인수가 너무 많습니다\n"); return false; }
            시작점[토큰수] = 끝; int 인용 = 0;
            while (위치 < Ululyk) {
                int baha = setir[위치++];
                if (인용 == 0 && (baha == 32 || baha == 9)) break;
                if (baha == 인용) { 인용 = 0; continue; }
                if (인용 == 0 && (baha == 39 || baha == 34)) { 인용 = baha; continue; }
                token_baha[끝++] = baha;
            }
            if (인용 != 0) { 단말.Ýaz("buýruk seljer_baha: 따옴표가 닫히지 않았습니다\n"); return false; }
            dowamlylyk_baha[토큰수] = 끝 - 시작점[토큰수]; 토큰수++;
        }
        return true;
    }
    static boolean 같음(int indeks, String Söz_SMS) {
        if (indeks >= 토큰수) return false;
        int 자리=0;
        for (int 순번=0; 순번<Söz_SMS.length(); 순번++) {
            int nyşanyň_kody=Söz_SMS.charAt(순번);
            if (nyşanyň_kody>=0xd800 && nyşanyň_kody<=0xdbff && 순번+1<Söz_SMS.length()) nyşanyň_kody=0x10000+((nyşanyň_kody-0xd800)<<10)+Söz_SMS.charAt(++순번)-0xdc00;
            int 바이트수=nyşanyň_kody<128?1:nyşanyň_kody<2048?2:nyşanyň_kody<65536?3:4;
            for (int SEQUENCE_baha=바이트수-1; SEQUENCE_baha>=0; SEQUENCE_baha--) {
                int baha=바이트수==1?nyşanyň_kody:SEQUENCE_baha==바이트수-1?(바이트수==2?0xc0:바이트수==3?0xe0:0xf0)|(nyşanyň_kody>>(6*SEQUENCE_baha)):0x80|((nyşanyň_kody>>(6*SEQUENCE_baha))&63);
                if (자리>=dowamlylyk_baha[indeks] || token_baha[시작점[indeks]+자리++]!=baha) return false;
            }
        }
        return 자리==dowamlylyk_baha[indeks];
    }
    static int Ýol(int indeks) {
        if (indeks >= 토큰수) return -22;
        int 결과 = ýat_Faýllar.ýol_başlat(dowamlylyk_baha[indeks]); if (결과 < 0) return 결과;
        for (int sikl_indeks = 0; sikl_indeks < dowamlylyk_baha[indeks]; sikl_indeks++) {
            결과 = ýat_Faýllar.ýol_baýt(sikl_indeks, token_baha[시작점[indeks] + sikl_indeks]); if (결과 < 0) return 결과;
        }
        return 0;
    }
    static void Hata(int indeks) { 결과 = 1; 단말.Ýaz("Hata "); 단말.수(indeks); 단말.문자(10); }
    static void görkez_baha() {
        if (토큰수 != 2) { 단말.Ýaz("사용법: cat Faýl\n"); return; }
        int 결과 = Ýol(1); if (결과 < 0) { Hata(결과); return; }
        int Faýl = ýat_Faýllar.Aç(0); if (Faýl < 0) { Hata(Faýl); return; }
        while (true) { int baha = ýat_Faýllar.Oka(Faýl); if (baha == 256) break; if (baha < 0) { Hata(baha); break; } 원바이트(baha); }
        ýat_Faýllar.Ýap(Faýl); 단말.문자(10);
    }
    static void redaktirle_baha() {
        if (토큰수 != 2) { 단말.Ýaz("사용법: edit Faýl\n"); return; }
        int 결과 = Ýol(1); if (결과 < 0) { Hata(결과); return; }
        redaktirle_at_dowamlylyk = dowamlylyk_baha[1];
        for (int sikl_indeks = 0; sikl_indeks < redaktirle_at_dowamlylyk; sikl_indeks++) redaktirle_at[sikl_indeks] = token_baha[시작점[1] + sikl_indeks];
        단말.Ýaz("EDIT: Faýl 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Ululyk = 0;
        while (true) {
            단말.Ýaz("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Ýaz("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && setir[0] == '.') break;
            if (입력 + 1 > 편집내용.length - Ululyk) { 단말.Ýaz("EDIT CANCELLED: file too large\n"); return; }
            for (int sikl_indeks = 0; sikl_indeks < 입력; sikl_indeks++) 편집내용[Ululyk++] = setir[sikl_indeks];
            편집내용[Ululyk++] = 10;
        }
        ýat_Faýllar.ýol_başlat(redaktirle_at_dowamlylyk);
        for (int sikl_indeks = 0; sikl_indeks < redaktirle_at_dowamlylyk; sikl_indeks++) ýat_Faýllar.ýol_baýt(sikl_indeks, redaktirle_at[sikl_indeks]);
        int Faýl = ýat_Faýllar.Aç(577); if (Faýl < 0) { Hata(Faýl); return; }
        for (int sikl_indeks = 0; sikl_indeks < Ululyk; sikl_indeks++) ýat_Faýllar.Ýaz(Faýl, 편집내용[sikl_indeks]);
        ýat_Faýllar.Ýap(Faýl); 단말.Ýaz("SAVED "); 단말.수(Ululyk); 단말.Ýaz("baýt_baha(주기억 Faýl)\n");
    }
    static int 십육(int baha) {
        if (baha >= '0' && baha <= '9') return baha - '0';
        if (baha >= 'a' && baha <= 'f') return baha - 'a' + 10;
        if (baha >= 'A' && baha <= 'F') return baha - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (토큰수 != 2) { 단말.Ýaz("사용법: load Faýl | hex Faýl\n"); return; }
        int 결과 = Ýol(1); if (결과 < 0) { Hata(결과); return; }
        if (!넣기) {
            int Faýl = ýat_Faýllar.Aç(0); if (Faýl < 0) { Hata(Faýl); return; }
            단말.Ýaz("HEX BEGIN "); 단말.수(ýat_Faýllar.Ululyk(Faýl)); 단말.문자(10);
            int 항목수 = 0;
            while (true) {
                int baha = ýat_Faýllar.Oka(Faýl); if (baha < 0 || baha == 256) break;
                단말.문자("0123456789abcdef".charAt(baha >> 4)); 단말.문자("0123456789abcdef".charAt(baha & 15));
                if (++항목수 % 32 == 0) 단말.문자(10);
            }
            if (항목수 % 32 != 0) 단말.문자(10);
            ýat_Faýllar.Ýap(Faýl); 단말.Ýaz("HEX END\n"); return;
        }
        redaktirle_at_dowamlylyk = dowamlylyk_baha[1];
        for (int sikl_indeks = 0; sikl_indeks < redaktirle_at_dowamlylyk; sikl_indeks++) redaktirle_at[sikl_indeks] = token_baha[시작점[1] + sikl_indeks];
        단말.Ýaz("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Ululyk = 0;
        while (true) {
            단말.Ýaz("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Ýaz("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && setir[0] == '.') break;
            int 앞 = -1;
            for (int sikl_indeks = 0; sikl_indeks < 입력; sikl_indeks++) {
                if (setir[sikl_indeks] == 32 || setir[sikl_indeks] == 9) continue;
                int baha = 십육(setir[sikl_indeks]);
                if (baha < 0 || Ululyk >= 편집내용.length) { 단말.Ýaz("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = baha; else { 편집내용[Ululyk++] = 앞 * 16 + baha; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.Ýaz("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        ýat_Faýllar.ýol_başlat(redaktirle_at_dowamlylyk);
        for (int sikl_indeks = 0; sikl_indeks < redaktirle_at_dowamlylyk; sikl_indeks++) ýat_Faýllar.ýol_baýt(sikl_indeks, redaktirle_at[sikl_indeks]);
        int Faýl = ýat_Faýllar.Aç(577); if (Faýl < 0) { Hata(Faýl); return; }
        for (int sikl_indeks = 0; sikl_indeks < Ululyk; sikl_indeks++) ýat_Faýllar.Ýaz(Faýl, 편집내용[sikl_indeks]);
        ýat_Faýllar.Ýap(Faýl); 단말.Ýaz("LOADED "); 단말.수(Ululyk); 단말.Ýaz("baýt_baha(주기억 Faýl)\n");
    }
    static int Gurallar(int indeks) {
        return gural_girizmeklik(indeks, 1);
    }
    static int gural_girizmeklik(int indeks, int Bitir) {
        if (토큰수 - Bitir > 8) return -22;
        보드.인수준비(토큰수 - Bitir);
        for (int 첫값 = Bitir; 첫값 < 토큰수; 첫값++) {
            if (dowamlylyk_baha[첫값] > 255) return -36;
            for (int sikl_indeks = 0; sikl_indeks < dowamlylyk_baha[첫값]; sikl_indeks++) 보드.argument_baýt(첫값 - Bitir, sikl_indeks, token_baha[시작점[첫값] + sikl_indeks]);
        }
        return indeks == -2 ? 보드.리눅스파일실행() : indeks < 0 ? 보드.ýerine_ýetir_ulanyjy_faýl() : 보드.işe_goýber_ulanyjy_programma(indeks);
    }
    static int 파이썬꾸러미() {
        if (토큰수 > 8) return -22;
        보드.인수준비(토큰수);
        String Ýol = "/lib/toplum.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int 자리 = 0;
        for (int 순번 = 0; 순번 < Ýol.length(); 순번++) {
            int nyşan_baha_068c2631 = Ýol.charAt(순번);
            if (nyşan_baha_068c2631 < 128) 보드.argument_baýt(0, 자리++, nyşan_baha_068c2631);
            else { 보드.argument_baýt(0, 자리++, 0xe0 | (nyşan_baha_068c2631 >> 12)); 보드.argument_baýt(0, 자리++, 0x80 | ((nyşan_baha_068c2631 >> 6) & 63)); 보드.argument_baýt(0, 자리++, 0x80 | (nyşan_baha_068c2631 & 63)); }
        }
        for (int 순번 = 1; 순번 < 토큰수; 순번++) {
            if (dowamlylyk_baha[순번] > 255) return -36;
            for (int nyşan_baha_068c2631 = 0; nyşan_baha_068c2631 < dowamlylyk_baha[순번]; nyşan_baha_068c2631++) 보드.argument_baýt(순번, nyşan_baha_068c2631, token_baha[시작점[순번] + nyşan_baha_068c2631]);
        }
        return 보드.işe_goýber_ulanyjy_programma(12);
    }
    static int 실행형식() {
        int 처리값 = Ýol(0); if (처리값 < 0) return 처리값;
        int Faýl = ýat_Faýllar.Aç(0); if (Faýl < 0) return Faýl;
        int 첫값 = ýat_Faýllar.Oka(Faýl), baýt_maglumat = ýat_Faýllar.Oka(Faýl), nyşanyň_kody = ýat_Faýllar.Oka(Faýl), 뒷값 = ýat_Faýllar.Oka(Faýl);
        ýat_Faýllar.Ýap(Faýl);
        if (첫값 == 127 && baýt_maglumat == 'E' && nyşanyň_kody == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && baýt_maglumat == 'K' && nyşanyň_kody == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int indeks, String 인수) {
        보드.인수준비(1);
        for (int sikl_indeks = 0; sikl_indeks < 인수.length(); sikl_indeks++) 보드.argument_baýt(0, sikl_indeks, 인수.charAt(sikl_indeks));
        return 보드.işe_goýber_ulanyjy_programma(indeks);
    }
    static void SMS_baýt(int Faýl, int baha) { ýat_Faýllar.Ýaz(Faýl, baha); }
    static void statiki_faýl(String Ad, String Mazmun_baha) {
        // toplum 파일명은 ASCII. Faýl 내용은 UTF-8로 저장한다.
        ýat_Faýllar.ýol_başlat(Ad.length());
        for (int sikl_indeks = 0; sikl_indeks < Ad.length(); sikl_indeks++) ýat_Faýllar.ýol_baýt(sikl_indeks, Ad.charAt(sikl_indeks));
        int Faýl = ýat_Faýllar.Aç(193); if (Faýl < 0) return;
        for (int sikl_indeks = 0; sikl_indeks < Mazmun_baha.length(); sikl_indeks++) {
            int nyşanyň_kody = Mazmun_baha.charAt(sikl_indeks);
            if (nyşanyň_kody >= 0xd800 && nyşanyň_kody <= 0xdbff && sikl_indeks + 1 < Mazmun_baha.length()) nyşanyň_kody = 0x10000 + ((nyşanyň_kody - 0xd800) << 10) + Mazmun_baha.charAt(++sikl_indeks) - 0xdc00;
            if (nyşanyň_kody < 128) SMS_baýt(Faýl, nyşanyň_kody);
            else {
                int 수 = nyşanyň_kody < 2048 ? 2 : nyşanyň_kody < 65536 ? 3 : 4;
                SMS_baýt(Faýl, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (nyşanyň_kody >> (6 * (수 - 1))));
                for (int 항목수 = 수 - 1; 항목수 > 0; 항목수--) SMS_baýt(Faýl, 0x80 | ((nyşanyň_kody >> (6 * (항목수 - 1))) & 63));
            }
        }
        ýat_Faýllar.Ýap(Faýl);
    }
    static void 한글도움말() {
        단말.Ýaz("F9 / Shift+Space: [EN] ↔ [tk]\n");
        단말.Ýaz("  [TK] keyboard; [EN] ASCII\n");
        단말.Ýaz("  a → a\n");
        단말.Ýaz("  F9: EN ↔ tk | Ctrl+Shift+V: UTF-8\n");
        단말.Ýaz("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Ýaz("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Ad) {
        int 바이트수 = 0;
        for (int sikl_indeks = 0; sikl_indeks < Ad.length(); sikl_indeks++) { int nyşanyň_kody = Ad.charAt(sikl_indeks); if (nyşanyň_kody >= 0xd800 && nyşanyň_kody <= 0xdfff) return -22; 바이트수 += nyşanyň_kody < 128 ? 1 : nyşanyň_kody < 2048 ? 2 : 3; }
        int 처리값 = ýat_Faýllar.ýol_başlat(바이트수); if (처리값 < 0) return 처리값;
        int 자리 = 0;
        for (int sikl_indeks = 0; sikl_indeks < Ad.length(); sikl_indeks++) {
            int nyşanyň_kody = Ad.charAt(sikl_indeks);
            if (nyşanyň_kody < 128) ýat_Faýllar.ýol_baýt(자리++, nyşanyň_kody);
            else if (nyşanyň_kody < 2048) { ýat_Faýllar.ýol_baýt(자리++, 0xc0 | (nyşanyň_kody >> 6)); ýat_Faýllar.ýol_baýt(자리++, 0x80 | (nyşanyň_kody & 63)); }
            else { ýat_Faýllar.ýol_baýt(자리++, 0xe0 | (nyşanyň_kody >> 12)); ýat_Faýllar.ýol_baýt(자리++, 0x80 | ((nyşanyň_kody >> 6) & 63)); ýat_Faýllar.ýol_baýt(자리++, 0x80 | (nyşanyň_kody & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Ad) {
        int 처리값 = 예제경로(Ad); if (처리값 < 0) return 처리값;
        처리값 = ýat_Faýllar.döretmek_katalog(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Ad, String maglumat) {
        int 처리값 = 예제경로(Ad); if (처리값 < 0) return 처리값;
        int Faýl = ýat_Faýllar.Aç(193); if (Faýl == -17) return 0; if (Faýl < 0) return Faýl;
        for (int sikl_indeks = 0; sikl_indeks < maglumat.length(); sikl_indeks += 2) {
            처리값 = ýat_Faýllar.Ýaz(Faýl, 십육(maglumat.charAt(sikl_indeks)) * 16 + 십육(maglumat.charAt(sikl_indeks + 1)));
            if (처리값 < 0) { ýat_Faýllar.Ýap(Faýl); return 처리값; }
        }
        return ýat_Faýllar.Ýap(Faýl);
    }
    static void görkez_kömek() {
        ulgam_gural.görkez_kömek();
        단말.Ýaz("sshd / goragly_gabyjak start|stop|status: SSH :22 (user, 장치별 parol_baha)\n");
        단말.Ýaz("vncd / uzakdan_ekran start|stop|status: VNC :5900 (장치별 parol_baha)\n");
        단말.Ýaz("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Ýaz("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Ýaz("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Ýaz("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Ýaz("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Ýaz("모서리 + 왼쪽 버튼 süýşür_baha: 터미널 Ululyk üýtget_baha; terminal size: sütün_baha/setir_baha\n");
        단말.Ýaz("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Ýaz("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Ýaz("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Ýaz("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Ýaz("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Ýaz("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Ýaz("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Ýaz("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Ýaz("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Ýaz("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Ýaz("pip: MicroPython gor_agaç gurna_baha; esasy --network --pip 필요; /lib는 RAM\n");
        단말.Ýaz("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Ýaz("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Ýaz("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Ýaz("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void 터미널(boolean 전환여부) {
        if (전환여부 && 보드.터미널(2) != 0) { 보드.터미널(0); 단말.Ýaz("TERMINAL CLOSED\n"); }
        else if (보드.터미널(1) < 0) Hata(-19);
        else 단말.Ýaz("TERMINAL READY — tk terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void buýruk() {
        if (토큰수 == 0) return;
        if (ulgam_gural.ýerine_ýetir_buýruk()) return;
        if (같음(0,"sshd") || 같음(0,"goragly_gabyjak") || 같음(0,"vncd") || 같음(0,"uzakdan_ekran")) {
            int 종류=같음(0,"vncd")||같음(0,"uzakdan_ekran")?1:0;
            int iş=같음(1,"start")||같음(1,"Bitir")?1:같음(1,"stop")||같음(1,"Dur")?0:2;
            int ýagdaý_baha=보드.kölegelendirmek(종류,iş);
            if(ýagdaý_baha<0)Hata(ýagdaý_baha);else 단말.Ýaz(보드.kölegelendirmek(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else görkez_kömek(); }
        else if (같음(0, "info") || 같음(0, "i")) ýadro.msinfo32_exe();
        else if (같음(0, "pwd")) { ýat_Faýllar.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (토큰수 == 1) { ýat_Faýllar.ýol_başlat(1); 처리값 = ýat_Faýllar.ýol_baýt(0, '/'); } else 처리값 = 토큰수 == 2 ? Ýol(1) : -22;
            if (처리값 >= 0) 처리값 = ýat_Faýllar.üýtget_katalog(); if (처리값 < 0) Hata(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int argument_indeks = 같음(1, "-l") ? 2 : 1, 처리값;
            if (토큰수 == argument_indeks) { ýat_Faýllar.ýol_başlat(1); 처리값 = ýat_Faýllar.ýol_baýt(0, '.'); } else 처리값 = 토큰수 == argument_indeks + 1 ? Ýol(argument_indeks) : -22;
            if (처리값 >= 0) 처리값 = ýat_Faýllar.경로목록(); if (처리값 < 0) Hata(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) gabyjak_Gurallar.faýl_ýumuş(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) gabyjak_Gurallar.synp_baha(같음(0, "mv"));
        else if (같음(0, "cat")) gabyjak_Gurallar.görkez_baha();
        else if (같음(0, "wc")) gabyjak_Gurallar.세기();
        else if (같음(0, "grep")) gabyjak_Gurallar.tap_girizmeklik();
        else if (같음(0, "head") || 같음(0, "tail")) gabyjak_Gurallar.머리(같음(0, "tail"));
        else if (같음(0, "tee")) gabyjak_Gurallar.함께쓰기();
        else if (같음(0, "env")) gabyjak_sintaksis.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (토큰수 == 1) gabyjak_sintaksis.환경보기();
            for (int sikl_indeks = 1; sikl_indeks < 토큰수; sikl_indeks++) { int 처리값 = gabyjak_sintaksis.환경설정(sikl_indeks, 같음(0, "unset")); if (처리값 != 0) { 결과 = 처리값; 단말.Ýaz("buýruk seljer_baha: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) gabyjak_sintaksis.ýerine_ýetir_faýl();
        else if (같음(0, "true")) 결과 = 0;
        else if (같음(0, "false")) 결과 = 1;
        else if (같음(0, "history")) setir_Redaktor.görkez_hasaba_alyş();
        else if (같음(0, "exit")) {
            if (gabyjak_sintaksis.깊이 > 0) { 결과 = 토큰수 == 1 ? gabyjak_sintaksis.ýagdaý_baha : gabyjak_Gurallar.san_baha(1); if (결과 < 0 || 결과 > 255) 결과 = 2; gabyjak_sintaksis.skript_tamamla = true; }
            else if (보드.터미널(2) != 0) 터미널(true);
            else 단말.Ýaz("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) redaktirle_baha();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (토큰수 < 2) { 결과 = 2; 단말.Ýaz("사용법: rm Faýl...\n"); }
            for (int sikl_indeks = 1; sikl_indeks < 토큰수; sikl_indeks++) { int 처리값 = Ýol(sikl_indeks); if (처리값 == 0) 처리값 = ýat_Faýllar.지우기(); if (처리값 < 0) Hata(처리값); }
        }
        else if (같음(0, "echo")) {
            int 시작자리 = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = 시작자리; 첫값 < 토큰수; 첫값++) { if (첫값 > 시작자리) 단말.문자(32); for (int sikl_indeks = 0; sikl_indeks < dowamlylyk_baha[첫값]; sikl_indeks++) 보드.직렬쓰기(token_baha[시작점[첫값] + sikl_indeks]); }
            if (시작자리 == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Ýaz("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? 파이썬꾸러미() : Gurallar(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !gabyjak_sintaksis.연결중) { 단말.Ýaz("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Gurallar(13); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Gurallar(15); 결과 = 처리값 < 0 ? 126 : 처리값; if (!gabyjak_sintaksis.연결중) { 단말.Ýaz("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Gurallar(16); 결과 = 처리값 < 0 ? 126 : 처리값; if (!gabyjak_sintaksis.연결중) { 단말.Ýaz("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Ululyk = 보드.터미널(13); 단말.Ýaz("TERMINAL SIZE "); 단말.수(Ululyk & 65535); 단말.문자('x'); 단말.수(Ululyk >>> 16); 단말.문자(10); }
            else 터미널(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { 보드.터미널(9); iş_stoly.ýerine_ýetir_buýruk(); }
        else if (같음(0, "c")) ýadro.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) ýadro.작업시험();
        else if (같음(0, "g")) ýadro.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) ýadro.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = 보드.işe_goýber_ulanyjy_programma(0); if (처리값 == 0) 단말.Ýaz("ELF DEMO PASS\n"); else Hata(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? gural_girizmeklik(-2, 2) : Gurallar(-1); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !gabyjak_sintaksis.연결중) { 단말.Ýaz("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) ýadro.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = 보드.faýl_geçir_hyzmat(1); if (처리값 < 0) Hata(처리값); else { 단말.Ýaz("FTP listening "); ulgam_gural.ýaz_salgy(보드.Tor_ýagdaý(0,0)); 단말.Ýaz(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { 보드.faýl_geçir_hyzmat(0); 단말.Ýaz("FTP stopped\n"); }
            else 단말.Ýaz(보드.faýl_geçir_hyzmat(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { toplum.Taýýarla(); 단말.Ýaz("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Dil = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (토큰수 != 2 || Dil < 0) 단말.Ýaz("example java|c|python: 출력, Faýl, 네트워크, 그래픽, Java Swing penjire 예제\n");
            else { int 처리값 = 예제꾸러미.gurna_baha(Dil); if (처리값 < 0) { Hata(처리값); if (처리값 == -28) 단말.Ýaz("RAM full: remove unused files, then retry example\n"); } else 단말.Ýaz("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int format_baha = 실행형식();
            if (format_baha == 1 || format_baha == 2) {
                int 처리값 = gural_girizmeklik(format_baha == 1 ? -1 : 14, 0); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !gabyjak_sintaksis.연결중) { 단말.Ýaz("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (format_baha == 0) { 결과 = 126; 단말.Ýaz("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { 결과 = 127; 단말.Ýaz("Unknown command. help: commands\n"); }
        }
    }
    public static void ýerine_ýetir_buýruk() {
        toplum.Taýýarla();
        for (int Dil = 0; Dil < 3; Dil++) { int 처리값 = 예제꾸러미.gurna_baha(Dil); if (처리값 < 0) Hata(처리값); }
        görkez_kömek();
        while (true) {
            penjire_seans.Proses_baha_girizmeklik(); if (penjire_seans.재개()) continue;
            if (!penjire_seans.이어읽기) 단말.Ýaz("jkoros-native> "); setir_Redaktor.buýruk_setiri = true; 보드.원격대기(1); int Ululyk = 줄읽기(); 보드.원격대기(0); setir_Redaktor.buýruk_setiri = false;
            if (Ululyk == -3) continue;
            if (Ululyk == -2) 단말.Ýaz("buýruk seljer_baha: 명령줄이 너무 깁니다\n");
            if (Ululyk >= 0) { gabyjak_sintaksis.skript_tamamla = false; gabyjak_sintaksis.ýerine_ýetir_buýruk(setir, 0, Ululyk, 0); } else gabyjak_sintaksis.ýagdaý_baha = 130;
            보드.tamamla_uzakdan_buýruk(gabyjak_sintaksis.ýagdaý_baha);
            setir_Redaktor.Ululyk = setir_Redaktor.kursor_baha = setir_Redaktor.başlat_penjire = 0;
        }
    }
}
