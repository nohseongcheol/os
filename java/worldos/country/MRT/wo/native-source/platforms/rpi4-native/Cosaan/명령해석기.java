// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 Tegtalu_ndigel. 따옴표, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] buum = new int[4096], jeton_xëyma = new int[4096], 시작점 = new int[32], diir_xëyma = new int[32];
    static int[] 편집내용 = new int[16384], soppi_tur = new int[63];
    static int 토큰수, soppi_tur_diir, 결과;
    static boolean 앞줄;
    static void 원바이트(int xëyma) { 보드.직렬쓰기(xëyma); }
    static int 줄읽기() { return buum_defarkat.읽기(); }
    static boolean 나누기(int tolluwaay) {
        int 위치 = 0, 끝 = 0; 토큰수 = 0;
        while (위치 < tolluwaay) {
            while (위치 < tolluwaay && (buum[위치] == 32 || buum[위치] == 9)) 위치++;
            if (위치 == tolluwaay) break;
            if (토큰수 == 16) { 단말.biir("ndigel Segg_xëyma: 인수가 너무 많습니다\n"); return false; }
            시작점[토큰수] = 끝; int 인용 = 0;
            while (위치 < tolluwaay) {
                int xëyma = buum[위치++];
                if (인용 == 0 && (xëyma == 32 || xëyma == 9)) break;
                if (xëyma == 인용) { 인용 = 0; continue; }
                if (인용 == 0 && (xëyma == 39 || xëyma == 34)) { 인용 = xëyma; continue; }
                jeton_xëyma[끝++] = xëyma;
            }
            if (인용 != 0) { 단말.biir("ndigel Segg_xëyma: 따옴표가 닫히지 않았습니다\n"); return false; }
            diir_xëyma[토큰수] = 끝 - 시작점[토큰수]; 토큰수++;
        }
        return true;
    }
    static boolean 같음(int àlluwa_tur, String Word_SMS) {
        if (àlluwa_tur >= 토큰수) return false;
        int 자리=0;
        for (int 순번=0; 순번<Word_SMS.length(); 순번++) {
            int kotu_araf=Word_SMS.charAt(순번);
            if (kotu_araf>=0xd800 && kotu_araf<=0xdbff && 순번+1<Word_SMS.length()) kotu_araf=0x10000+((kotu_araf-0xd800)<<10)+Word_SMS.charAt(++순번)-0xdc00;
            int 바이트수=kotu_araf<128?1:kotu_araf<2048?2:kotu_araf<65536?3:4;
            for (int SEQUENCE_xëyma=바이트수-1; SEQUENCE_xëyma>=0; SEQUENCE_xëyma--) {
                int xëyma=바이트수==1?kotu_araf:SEQUENCE_xëyma==바이트수-1?(바이트수==2?0xc0:바이트수==3?0xe0:0xf0)|(kotu_araf>>(6*SEQUENCE_xëyma)):0x80|((kotu_araf>>(6*SEQUENCE_xëyma))&63);
                if (자리>=diir_xëyma[àlluwa_tur] || jeton_xëyma[시작점[àlluwa_tur]+자리++]!=xëyma) return false;
            }
        }
        return 자리==diir_xëyma[àlluwa_tur];
    }
    static int Yoonu_jëmale(int àlluwa_tur) {
        if (àlluwa_tur >= 토큰수) return -22;
        int 결과 = fatlekookaay_Fisiye_yi.Yoonu_jëmale_Door(diir_xëyma[àlluwa_tur]); if (결과 < 0) return 결과;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < diir_xëyma[àlluwa_tur]; wërngël_àlluwa_tur++) {
            결과 = fatlekookaay_Fisiye_yi.Yoonu_jëmale_okte(wërngël_àlluwa_tur, jeton_xëyma[시작점[àlluwa_tur] + wërngël_àlluwa_tur]); if (결과 < 0) return 결과;
        }
        return 0;
    }
    static void njumte(int àlluwa_tur) { 결과 = 1; 단말.biir("njumte "); 단말.수(àlluwa_tur); 단말.문자(10); }
    static void wonin_xëyma() {
        if (토큰수 != 2) { 단말.biir("사용법: cat bara_denc\n"); return; }
        int 결과 = Yoonu_jëmale(1); if (결과 < 0) { njumte(결과); return; }
        int bara_denc = fatlekookaay_Fisiye_yi.sos(0); if (bara_denc < 0) { njumte(bara_denc); return; }
        while (true) { int xëyma = fatlekookaay_Fisiye_yi.읽기(bara_denc); if (xëyma == 256) break; if (xëyma < 0) { njumte(xëyma); break; } 원바이트(xëyma); }
        fatlekookaay_Fisiye_yi.Tej(bara_denc); 단말.문자(10);
    }
    static void soppi_xëyma() {
        if (토큰수 != 2) { 단말.biir("사용법: edit bara_denc\n"); return; }
        int 결과 = Yoonu_jëmale(1); if (결과 < 0) { njumte(결과); return; }
        soppi_tur_diir = diir_xëyma[1];
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < soppi_tur_diir; wërngël_àlluwa_tur++) soppi_tur[wërngël_àlluwa_tur] = jeton_xëyma[시작점[1] + wërngël_àlluwa_tur];
        단말.biir("EDIT: bara_denc 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int tolluwaay = 0;
        while (true) {
            단말.biir("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.biir("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && buum[0] == '.') break;
            if (입력 + 1 > 편집내용.length - tolluwaay) { 단말.biir("EDIT CANCELLED: file too large\n"); return; }
            for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 입력; wërngël_àlluwa_tur++) 편집내용[tolluwaay++] = buum[wërngël_àlluwa_tur];
            편집내용[tolluwaay++] = 10;
        }
        fatlekookaay_Fisiye_yi.Yoonu_jëmale_Door(soppi_tur_diir);
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < soppi_tur_diir; wërngël_àlluwa_tur++) fatlekookaay_Fisiye_yi.Yoonu_jëmale_okte(wërngël_àlluwa_tur, soppi_tur[wërngël_àlluwa_tur]);
        int bara_denc = fatlekookaay_Fisiye_yi.sos(577); if (bara_denc < 0) { njumte(bara_denc); return; }
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < tolluwaay; wërngël_àlluwa_tur++) fatlekookaay_Fisiye_yi.biir(bara_denc, 편집내용[wërngël_àlluwa_tur]);
        fatlekookaay_Fisiye_yi.Tej(bara_denc); 단말.biir("SAVED "); 단말.수(tolluwaay); 단말.biir("okte_xëyma(주기억 bara_denc)\n");
    }
    static int 십육(int xëyma) {
        if (xëyma >= '0' && xëyma <= '9') return xëyma - '0';
        if (xëyma >= 'a' && xëyma <= 'f') return xëyma - 'a' + 10;
        if (xëyma >= 'A' && xëyma <= 'F') return xëyma - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (토큰수 != 2) { 단말.biir("사용법: load bara_denc | hex bara_denc\n"); return; }
        int 결과 = Yoonu_jëmale(1); if (결과 < 0) { njumte(결과); return; }
        if (!넣기) {
            int bara_denc = fatlekookaay_Fisiye_yi.sos(0); if (bara_denc < 0) { njumte(bara_denc); return; }
            단말.biir("HEX BEGIN "); 단말.수(fatlekookaay_Fisiye_yi.tolluwaay(bara_denc)); 단말.문자(10);
            int 항목수 = 0;
            while (true) {
                int xëyma = fatlekookaay_Fisiye_yi.읽기(bara_denc); if (xëyma < 0 || xëyma == 256) break;
                단말.문자("0123456789abcdef".charAt(xëyma >> 4)); 단말.문자("0123456789abcdef".charAt(xëyma & 15));
                if (++항목수 % 32 == 0) 단말.문자(10);
            }
            if (항목수 % 32 != 0) 단말.문자(10);
            fatlekookaay_Fisiye_yi.Tej(bara_denc); 단말.biir("HEX END\n"); return;
        }
        soppi_tur_diir = diir_xëyma[1];
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < soppi_tur_diir; wërngël_àlluwa_tur++) soppi_tur[wërngël_àlluwa_tur] = jeton_xëyma[시작점[1] + wërngël_àlluwa_tur];
        단말.biir("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int tolluwaay = 0;
        while (true) {
            단말.biir("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.biir("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && buum[0] == '.') break;
            int 앞 = -1;
            for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 입력; wërngël_àlluwa_tur++) {
                if (buum[wërngël_àlluwa_tur] == 32 || buum[wërngël_àlluwa_tur] == 9) continue;
                int xëyma = 십육(buum[wërngël_àlluwa_tur]);
                if (xëyma < 0 || tolluwaay >= 편집내용.length) { 단말.biir("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = xëyma; else { 편집내용[tolluwaay++] = 앞 * 16 + xëyma; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.biir("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        fatlekookaay_Fisiye_yi.Yoonu_jëmale_Door(soppi_tur_diir);
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < soppi_tur_diir; wërngël_àlluwa_tur++) fatlekookaay_Fisiye_yi.Yoonu_jëmale_okte(wërngël_àlluwa_tur, soppi_tur[wërngël_àlluwa_tur]);
        int bara_denc = fatlekookaay_Fisiye_yi.sos(577); if (bara_denc < 0) { njumte(bara_denc); return; }
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < tolluwaay; wërngël_àlluwa_tur++) fatlekookaay_Fisiye_yi.biir(bara_denc, 편집내용[wërngël_àlluwa_tur]);
        fatlekookaay_Fisiye_yi.Tej(bara_denc); 단말.biir("LOADED "); 단말.수(tolluwaay); 단말.biir("okte_xëyma(주기억 bara_denc)\n");
    }
    static int Jumtukaay_yi(int àlluwa_tur) {
        return jumtukaay_dugal_xabaar(àlluwa_tur, 1);
    }
    static int jumtukaay_dugal_xabaar(int àlluwa_tur, int daw) {
        if (토큰수 - daw > 8) return -22;
        보드.인수준비(토큰수 - daw);
        for (int 첫값 = daw; 첫값 < 토큰수; 첫값++) {
            if (diir_xëyma[첫값] > 255) return -36;
            for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < diir_xëyma[첫값]; wërngël_àlluwa_tur++) 보드.Tegtal_okte(첫값 - daw, wërngël_àlluwa_tur, jeton_xëyma[시작점[첫값] + wërngël_àlluwa_tur]);
        }
        return àlluwa_tur == -2 ? 보드.리눅스파일실행() : àlluwa_tur < 0 ? 보드.def_kiy_jariñoo_internet_bara_denc() : 보드.daw_kiy_jariñoo_internet_jëfekaay(àlluwa_tur);
    }
    static int 파이썬꾸러미() {
        if (토큰수 > 8) return -22;
        보드.인수준비(토큰수);
        String Yoonu_jëmale = "/lib/takku_xéewël.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int 자리 = 0;
        for (int 순번 = 0; 순번 < Yoonu_jëmale.length(); 순번++) {
            int Araf_xëyma = Yoonu_jëmale.charAt(순번);
            if (Araf_xëyma < 128) 보드.Tegtal_okte(0, 자리++, Araf_xëyma);
            else { 보드.Tegtal_okte(0, 자리++, 0xe0 | (Araf_xëyma >> 12)); 보드.Tegtal_okte(0, 자리++, 0x80 | ((Araf_xëyma >> 6) & 63)); 보드.Tegtal_okte(0, 자리++, 0x80 | (Araf_xëyma & 63)); }
        }
        for (int 순번 = 1; 순번 < 토큰수; 순번++) {
            if (diir_xëyma[순번] > 255) return -36;
            for (int Araf_xëyma = 0; Araf_xëyma < diir_xëyma[순번]; Araf_xëyma++) 보드.Tegtal_okte(순번, Araf_xëyma, jeton_xëyma[시작점[순번] + Araf_xëyma]);
        }
        return 보드.daw_kiy_jariñoo_internet_jëfekaay(12);
    }
    static int 실행형식() {
        int 처리값 = Yoonu_jëmale(0); if (처리값 < 0) return 처리값;
        int bara_denc = fatlekookaay_Fisiye_yi.sos(0); if (bara_denc < 0) return bara_denc;
        int 첫값 = fatlekookaay_Fisiye_yi.읽기(bara_denc), okte_mbir = fatlekookaay_Fisiye_yi.읽기(bara_denc), kotu_araf = fatlekookaay_Fisiye_yi.읽기(bara_denc), 뒷값 = fatlekookaay_Fisiye_yi.읽기(bara_denc);
        fatlekookaay_Fisiye_yi.Tej(bara_denc);
        if (첫값 == 127 && okte_mbir == 'E' && kotu_araf == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && okte_mbir == 'K' && kotu_araf == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int àlluwa_tur, String 인수) {
        보드.인수준비(1);
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 인수.length(); wërngël_àlluwa_tur++) 보드.Tegtal_okte(0, wërngël_àlluwa_tur, 인수.charAt(wërngël_àlluwa_tur));
        return 보드.daw_kiy_jariñoo_internet_jëfekaay(àlluwa_tur);
    }
    static void SMS_okte(int bara_denc, int xëyma) { fatlekookaay_Fisiye_yi.biir(bara_denc, xëyma); }
    static void Soppeekoodi_bara_denc(String tur_253d1510, String Këmb_xëyma) {
        // takku_xéewël 파일명은 ASCII. bara_denc 내용은 UTF-8로 저장한다.
        fatlekookaay_Fisiye_yi.Yoonu_jëmale_Door(tur_253d1510.length());
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < tur_253d1510.length(); wërngël_àlluwa_tur++) fatlekookaay_Fisiye_yi.Yoonu_jëmale_okte(wërngël_àlluwa_tur, tur_253d1510.charAt(wërngël_àlluwa_tur));
        int bara_denc = fatlekookaay_Fisiye_yi.sos(193); if (bara_denc < 0) return;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < Këmb_xëyma.length(); wërngël_àlluwa_tur++) {
            int kotu_araf = Këmb_xëyma.charAt(wërngël_àlluwa_tur);
            if (kotu_araf >= 0xd800 && kotu_araf <= 0xdbff && wërngël_àlluwa_tur + 1 < Këmb_xëyma.length()) kotu_araf = 0x10000 + ((kotu_araf - 0xd800) << 10) + Këmb_xëyma.charAt(++wërngël_àlluwa_tur) - 0xdc00;
            if (kotu_araf < 128) SMS_okte(bara_denc, kotu_araf);
            else {
                int 수 = kotu_araf < 2048 ? 2 : kotu_araf < 65536 ? 3 : 4;
                SMS_okte(bara_denc, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (kotu_araf >> (6 * (수 - 1))));
                for (int 항목수 = 수 - 1; 항목수 > 0; 항목수--) SMS_okte(bara_denc, 0x80 | ((kotu_araf >> (6 * (항목수 - 1))) & 63));
            }
        }
        fatlekookaay_Fisiye_yi.Tej(bara_denc);
    }
    static void 한글도움말() {
        단말.biir("F9 / Shift+Space: [EN] ↔ [wo]\n");
        단말.biir("  [WO] keyboard; [EN] ASCII\n");
        단말.biir("  a → a\n");
        단말.biir("  F9: EN ↔ wo | Ctrl+Shift+V: UTF-8\n");
        단말.biir("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.biir("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String tur_253d1510) {
        int 바이트수 = 0;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < tur_253d1510.length(); wërngël_àlluwa_tur++) { int kotu_araf = tur_253d1510.charAt(wërngël_àlluwa_tur); if (kotu_araf >= 0xd800 && kotu_araf <= 0xdfff) return -22; 바이트수 += kotu_araf < 128 ? 1 : kotu_araf < 2048 ? 2 : 3; }
        int 처리값 = fatlekookaay_Fisiye_yi.Yoonu_jëmale_Door(바이트수); if (처리값 < 0) return 처리값;
        int 자리 = 0;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < tur_253d1510.length(); wërngël_àlluwa_tur++) {
            int kotu_araf = tur_253d1510.charAt(wërngël_àlluwa_tur);
            if (kotu_araf < 128) fatlekookaay_Fisiye_yi.Yoonu_jëmale_okte(자리++, kotu_araf);
            else if (kotu_araf < 2048) { fatlekookaay_Fisiye_yi.Yoonu_jëmale_okte(자리++, 0xc0 | (kotu_araf >> 6)); fatlekookaay_Fisiye_yi.Yoonu_jëmale_okte(자리++, 0x80 | (kotu_araf & 63)); }
            else { fatlekookaay_Fisiye_yi.Yoonu_jëmale_okte(자리++, 0xe0 | (kotu_araf >> 12)); fatlekookaay_Fisiye_yi.Yoonu_jëmale_okte(자리++, 0x80 | ((kotu_araf >> 6) & 63)); fatlekookaay_Fisiye_yi.Yoonu_jëmale_okte(자리++, 0x80 | (kotu_araf & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String tur_253d1510) {
        int 처리값 = 예제경로(tur_253d1510); if (처리값 < 0) return 처리값;
        처리값 = fatlekookaay_Fisiye_yi.sos_dàmb(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String tur_253d1510, String mbir) {
        int 처리값 = 예제경로(tur_253d1510); if (처리값 < 0) return 처리값;
        int bara_denc = fatlekookaay_Fisiye_yi.sos(193); if (bara_denc == -17) return 0; if (bara_denc < 0) return bara_denc;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < mbir.length(); wërngël_àlluwa_tur += 2) {
            처리값 = fatlekookaay_Fisiye_yi.biir(bara_denc, 십육(mbir.charAt(wërngël_àlluwa_tur)) * 16 + 십육(mbir.charAt(wërngël_àlluwa_tur + 1)));
            if (처리값 < 0) { fatlekookaay_Fisiye_yi.Tej(bara_denc); return 처리값; }
        }
        return fatlekookaay_Fisiye_yi.Tej(bara_denc);
    }
    static void féeñal_ndimbal() {
        kureel_jumtukaay.féeñal_ndimbal();
        단말.biir("sshd / wóor_Wëreef start|stop|status: SSH :22 (user, 장치별 pasu_dugg_xëyma)\n");
        단말.biir("vncd / lu_soree_laa start|stop|status: VNC :5900 (장치별 pasu_dugg_xëyma)\n");
        단말.biir("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.biir("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.biir("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.biir("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.biir("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.biir("모서리 + 왼쪽 버튼 randal_xëyma: 터미널 tolluwaay soppi_xëyma_16f64fe4; terminal size: Jen_xëyma/Dënk_xëyma\n");
        단말.biir("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.biir("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.biir("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.biir("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.biir("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.biir("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.biir("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.biir("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.biir("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.biir("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.biir("pip: MicroPython Cosaan_tëralinuy_pàcc samp_xëyma; dalal --network --pip 필요; /lib는 RAM\n");
        단말.biir("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.biir("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.biir("/example/java /example/c /example/python: examples ready at boot\n");
        단말.biir("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void 터미널(boolean 전환여부) {
        if (전환여부 && 보드.터미널(2) != 0) { 보드.터미널(0); 단말.biir("TERMINAL CLOSED\n"); }
        else if (보드.터미널(1) < 0) njumte(-19);
        else 단말.biir("TERMINAL READY — wo terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void ndigel() {
        if (토큰수 == 0) return;
        if (kureel_jumtukaay.def_ndigel()) return;
        if (같음(0,"sshd") || 같음(0,"wóor_Wëreef") || 같음(0,"vncd") || 같음(0,"lu_soree_laa")) {
            int 종류=같음(0,"vncd")||같음(0,"lu_soree_laa")?1:0;
            int jëf=같음(1,"start")||같음(1,"daw")?1:같음(1,"stop")||같음(1,"tees")?0:2;
            int nekkin_xëyma=보드.suufu(종류,jëf);
            if(nekkin_xëyma<0)njumte(nekkin_xëyma);else 단말.biir(보드.suufu(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else féeñal_ndimbal(); }
        else if (같음(0, "info") || 같음(0, "i")) xoox.msinfo32_exe();
        else if (같음(0, "pwd")) { fatlekookaay_Fisiye_yi.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (토큰수 == 1) { fatlekookaay_Fisiye_yi.Yoonu_jëmale_Door(1); 처리값 = fatlekookaay_Fisiye_yi.Yoonu_jëmale_okte(0, '/'); } else 처리값 = 토큰수 == 2 ? Yoonu_jëmale(1) : -22;
            if (처리값 >= 0) 처리값 = fatlekookaay_Fisiye_yi.soppi_dàmb(); if (처리값 < 0) njumte(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int Tegtal_àlluwa_tur = 같음(1, "-l") ? 2 : 1, 처리값;
            if (토큰수 == Tegtal_àlluwa_tur) { fatlekookaay_Fisiye_yi.Yoonu_jëmale_Door(1); 처리값 = fatlekookaay_Fisiye_yi.Yoonu_jëmale_okte(0, '.'); } else 처리값 = 토큰수 == Tegtal_àlluwa_tur + 1 ? Yoonu_jëmale(Tegtal_àlluwa_tur) : -22;
            if (처리값 >= 0) 처리값 = fatlekookaay_Fisiye_yi.경로목록(); if (처리값 < 0) njumte(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) Wëreef_Jumtukaay_yi.bara_denc_ay(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) Wëreef_Jumtukaay_yi.mbokk_xëyma(같음(0, "mv"));
        else if (같음(0, "cat")) Wëreef_Jumtukaay_yi.wonin_xëyma();
        else if (같음(0, "wc")) Wëreef_Jumtukaay_yi.세기();
        else if (같음(0, "grep")) Wëreef_Jumtukaay_yi.seet_dugal_xabaar();
        else if (같음(0, "head") || 같음(0, "tail")) Wëreef_Jumtukaay_yi.머리(같음(0, "tail"));
        else if (같음(0, "tee")) Wëreef_Jumtukaay_yi.함께쓰기();
        else if (같음(0, "env")) Wëreef_tëgg_waxin.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (토큰수 == 1) Wëreef_tëgg_waxin.환경보기();
            for (int wërngël_àlluwa_tur = 1; wërngël_àlluwa_tur < 토큰수; wërngël_àlluwa_tur++) { int 처리값 = Wëreef_tëgg_waxin.환경설정(wërngël_àlluwa_tur, 같음(0, "unset")); if (처리값 != 0) { 결과 = 처리값; 단말.biir("ndigel Segg_xëyma: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) Wëreef_tëgg_waxin.def_bara_denc();
        else if (같음(0, "true")) 결과 = 0;
        else if (같음(0, "false")) 결과 = 1;
        else if (같음(0, "history")) buum_defarkat.féeñal_làq();
        else if (같음(0, "exit")) {
            if (Wëreef_tëgg_waxin.깊이 > 0) { 결과 = 토큰수 == 1 ? Wëreef_tëgg_waxin.nekkin_xëyma : Wëreef_Jumtukaay_yi.siifar_xëyma(1); if (결과 < 0 || 결과 > 255) 결과 = 2; Wëreef_tëgg_waxin.ndigali_doxalin_jeexal = true; }
            else if (보드.터미널(2) != 0) 터미널(true);
            else 단말.biir("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) soppi_xëyma();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (토큰수 < 2) { 결과 = 2; 단말.biir("사용법: rm bara_denc...\n"); }
            for (int wërngël_àlluwa_tur = 1; wërngël_àlluwa_tur < 토큰수; wërngël_àlluwa_tur++) { int 처리값 = Yoonu_jëmale(wërngël_àlluwa_tur); if (처리값 == 0) 처리값 = fatlekookaay_Fisiye_yi.지우기(); if (처리값 < 0) njumte(처리값); }
        }
        else if (같음(0, "echo")) {
            int 시작자리 = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = 시작자리; 첫값 < 토큰수; 첫값++) { if (첫값 > 시작자리) 단말.문자(32); for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < diir_xëyma[첫값]; wërngël_àlluwa_tur++) 보드.직렬쓰기(jeton_xëyma[시작점[첫값] + wërngël_àlluwa_tur]); }
            if (시작자리 == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.biir("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? 파이썬꾸러미() : Jumtukaay_yi(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !Wëreef_tëgg_waxin.연결중) { 단말.biir("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Jumtukaay_yi(13); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Jumtukaay_yi(15); 결과 = 처리값 < 0 ? 126 : 처리값; if (!Wëreef_tëgg_waxin.연결중) { 단말.biir("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Jumtukaay_yi(16); 결과 = 처리값 < 0 ? 126 : 처리값; if (!Wëreef_tëgg_waxin.연결중) { 단말.biir("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int tolluwaay = 보드.터미널(13); 단말.biir("TERMINAL SIZE "); 단말.수(tolluwaay & 65535); 단말.문자('x'); 단말.수(tolluwaay >>> 16); 단말.문자(10); }
            else 터미널(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { 보드.터미널(9); Biro.def_ndigel(); }
        else if (같음(0, "c")) xoox.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) xoox.작업시험();
        else if (같음(0, "g")) xoox.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) xoox.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = 보드.daw_kiy_jariñoo_internet_jëfekaay(0); if (처리값 == 0) 단말.biir("ELF DEMO PASS\n"); else njumte(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? jumtukaay_dugal_xabaar(-2, 2) : Jumtukaay_yi(-1); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !Wëreef_tëgg_waxin.연결중) { 단말.biir("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) xoox.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = 보드.bara_denc_toxal_cër(1); if (처리값 < 0) njumte(처리값); else { 단말.biir("FTP listening "); kureel_jumtukaay.biir_dëkkuwaay(보드.mbaal_nekkin(0,0)); 단말.biir(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { 보드.bara_denc_toxal_cër(0); 단말.biir("FTP stopped\n"); }
            else 단말.biir(보드.bara_denc_toxal_cër(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { takku_xéewël.jël_matuwaay(); 단말.biir("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Làkk = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (토큰수 != 2 || Làkk < 0) 단말.biir("example java|c|python: 출력, bara_denc, 네트워크, 그래픽, Java Swing palanteer 예제\n");
            else { int 처리값 = 예제꾸러미.samp_xëyma(Làkk); if (처리값 < 0) { njumte(처리값); if (처리값 == -28) 단말.biir("RAM full: remove unused files, then retry example\n"); } else 단말.biir("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int dayo_xëyma = 실행형식();
            if (dayo_xëyma == 1 || dayo_xëyma == 2) {
                int 처리값 = jumtukaay_dugal_xabaar(dayo_xëyma == 1 ? -1 : 14, 0); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !Wëreef_tëgg_waxin.연결중) { 단말.biir("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (dayo_xëyma == 0) { 결과 = 126; 단말.biir("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { 결과 = 127; 단말.biir("Unknown command. help: commands\n"); }
        }
    }
    public static void def_ndigel() {
        takku_xéewël.jël_matuwaay();
        for (int Làkk = 0; Làkk < 3; Làkk++) { int 처리값 = 예제꾸러미.samp_xëyma(Làkk); if (처리값 < 0) njumte(처리값); }
        féeñal_ndimbal();
        while (true) {
            palanteer_lël.yokkute_xëyma_dugal_xabaar(); if (palanteer_lël.재개()) continue;
            if (!palanteer_lël.이어읽기) 단말.biir("jkoros-native> "); buum_defarkat.Tegtalu_ndigel = true; 보드.원격대기(1); int tolluwaay = 줄읽기(); 보드.원격대기(0); buum_defarkat.Tegtalu_ndigel = false;
            if (tolluwaay == -3) continue;
            if (tolluwaay == -2) 단말.biir("ndigel Segg_xëyma: 명령줄이 너무 깁니다\n");
            if (tolluwaay >= 0) { Wëreef_tëgg_waxin.ndigali_doxalin_jeexal = false; Wëreef_tëgg_waxin.def_ndigel(buum, 0, tolluwaay, 0); } else Wëreef_tëgg_waxin.nekkin_xëyma = 130;
            보드.jeexal_lu_soree_ndigel(Wëreef_tëgg_waxin.nekkin_xëyma);
            buum_defarkat.tolluwaay = buum_defarkat.barab_bees_mën_a_bind_xëyma = buum_defarkat.Door_palanteer = 0;
        }
    }
}
