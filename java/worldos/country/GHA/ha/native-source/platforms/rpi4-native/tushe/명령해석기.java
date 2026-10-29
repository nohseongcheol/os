// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 Layin_umurni. 따옴표, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Layi = new int[4096], token_Daraja = new int[4096], 시작점 = new int[32], Tsawo_Daraja = new int[32];
    static int[] 편집내용 = new int[16384], gyaran_Suna = new int[63];
    static int 토큰수, gyaran_Suna_Tsawo, 결과;
    static boolean 앞줄;
    static void 원바이트(int Daraja) { 보드.직렬쓰기(Daraja); }
    static int 줄읽기() { return Layi_Edita.Yi_Karatu(); }
    static boolean 나누기(int Girma) {
        int 위치 = 0, 끝 = 0; 토큰수 = 0;
        while (위치 < Girma) {
            while (위치 < Girma && (Layi[위치] == 32 || Layi[위치] == 9)) 위치++;
            if (위치 == Girma) break;
            if (토큰수 == 16) { 단말.Yi_Rubutu("Umarni Daddatse_Daraja: 인수가 너무 많습니다\n"); return false; }
            시작점[토큰수] = 끝; int 인용 = 0;
            while (위치 < Girma) {
                int Daraja = Layi[위치++];
                if (인용 == 0 && (Daraja == 32 || Daraja == 9)) break;
                if (Daraja == 인용) { 인용 = 0; continue; }
                if (인용 == 0 && (Daraja == 39 || Daraja == 34)) { 인용 = Daraja; continue; }
                token_Daraja[끝++] = Daraja;
            }
            if (인용 != 0) { 단말.Yi_Rubutu("Umarni Daddatse_Daraja: 따옴표가 닫히지 않았습니다\n"); return false; }
            Tsawo_Daraja[토큰수] = 끝 - 시작점[토큰수]; 토큰수++;
        }
        return true;
    }
    static boolean 같음(int Indes, String Microsoft_Word_SMS) {
        if (Indes >= 토큰수) return false;
        int 자리=0;
        for (int 순번=0; 순번<Microsoft_Word_SMS.length(); 순번++) {
            int Lambar_sirrin_harafi=Microsoft_Word_SMS.charAt(순번);
            if (Lambar_sirrin_harafi>=0xd800 && Lambar_sirrin_harafi<=0xdbff && 순번+1<Microsoft_Word_SMS.length()) Lambar_sirrin_harafi=0x10000+((Lambar_sirrin_harafi-0xd800)<<10)+Microsoft_Word_SMS.charAt(++순번)-0xdc00;
            int 바이트수=Lambar_sirrin_harafi<128?1:Lambar_sirrin_harafi<2048?2:Lambar_sirrin_harafi<65536?3:4;
            for (int JERI_Daraja=바이트수-1; JERI_Daraja>=0; JERI_Daraja--) {
                int Daraja=바이트수==1?Lambar_sirrin_harafi:JERI_Daraja==바이트수-1?(바이트수==2?0xc0:바이트수==3?0xe0:0xf0)|(Lambar_sirrin_harafi>>(6*JERI_Daraja)):0x80|((Lambar_sirrin_harafi>>(6*JERI_Daraja))&63);
                if (자리>=Tsawo_Daraja[Indes] || token_Daraja[시작점[Indes]+자리++]!=Daraja) return false;
            }
        }
        return 자리==Tsawo_Daraja[Indes];
    }
    static int Hanyar_shiga(int Indes) {
        if (Indes >= 토큰수) return -22;
        int 결과 = Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_Fara(Tsawo_Daraja[Indes]); if (결과 < 0) return 결과;
        for (int Warware_Indes = 0; Warware_Indes < Tsawo_Daraja[Indes]; Warware_Indes++) {
            결과 = Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_bayit(Warware_Indes, token_Daraja[시작점[Indes] + Warware_Indes]); if (결과 < 0) return 결과;
        }
        return 0;
    }
    static void Kuskure(int Indes) { 결과 = 1; 단말.Yi_Rubutu("Kuskure "); 단말.수(Indes); 단말.문자(10); }
    static void s_Daraja() {
        if (토큰수 != 2) { 단말.Yi_Rubutu("사용법: cat Fayil\n"); return; }
        int 결과 = Hanyar_shiga(1); if (결과 < 0) { Kuskure(결과); return; }
        int Fayil = Mahardatar_kwamfuta_Fayiloli.Buɗe(0); if (Fayil < 0) { Kuskure(Fayil); return; }
        while (true) { int Daraja = Mahardatar_kwamfuta_Fayiloli.Yi_Karatu(Fayil); if (Daraja == 256) break; if (Daraja < 0) { Kuskure(Daraja); break; } 원바이트(Daraja); }
        Mahardatar_kwamfuta_Fayiloli.Rufe(Fayil); 단말.문자(10);
    }
    static void gyaran_Daraja() {
        if (토큰수 != 2) { 단말.Yi_Rubutu("사용법: edit Fayil\n"); return; }
        int 결과 = Hanyar_shiga(1); if (결과 < 0) { Kuskure(결과); return; }
        gyaran_Suna_Tsawo = Tsawo_Daraja[1];
        for (int Warware_Indes = 0; Warware_Indes < gyaran_Suna_Tsawo; Warware_Indes++) gyaran_Suna[Warware_Indes] = token_Daraja[시작점[1] + Warware_Indes];
        단말.Yi_Rubutu("EDIT: Fayil 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Girma = 0;
        while (true) {
            단말.Yi_Rubutu("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Yi_Rubutu("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && Layi[0] == '.') break;
            if (입력 + 1 > 편집내용.length - Girma) { 단말.Yi_Rubutu("EDIT CANCELLED: file too large\n"); return; }
            for (int Warware_Indes = 0; Warware_Indes < 입력; Warware_Indes++) 편집내용[Girma++] = Layi[Warware_Indes];
            편집내용[Girma++] = 10;
        }
        Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_Fara(gyaran_Suna_Tsawo);
        for (int Warware_Indes = 0; Warware_Indes < gyaran_Suna_Tsawo; Warware_Indes++) Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_bayit(Warware_Indes, gyaran_Suna[Warware_Indes]);
        int Fayil = Mahardatar_kwamfuta_Fayiloli.Buɗe(577); if (Fayil < 0) { Kuskure(Fayil); return; }
        for (int Warware_Indes = 0; Warware_Indes < Girma; Warware_Indes++) Mahardatar_kwamfuta_Fayiloli.Yi_Rubutu(Fayil, 편집내용[Warware_Indes]);
        Mahardatar_kwamfuta_Fayiloli.Rufe(Fayil); 단말.Yi_Rubutu("SAVED "); 단말.수(Girma); 단말.Yi_Rubutu("bayit_Daraja(주기억 Fayil)\n");
    }
    static int 십육(int Daraja) {
        if (Daraja >= '0' && Daraja <= '9') return Daraja - '0';
        if (Daraja >= 'a' && Daraja <= 'f') return Daraja - 'a' + 10;
        if (Daraja >= 'A' && Daraja <= 'F') return Daraja - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (토큰수 != 2) { 단말.Yi_Rubutu("사용법: load Fayil | hex Fayil\n"); return; }
        int 결과 = Hanyar_shiga(1); if (결과 < 0) { Kuskure(결과); return; }
        if (!넣기) {
            int Fayil = Mahardatar_kwamfuta_Fayiloli.Buɗe(0); if (Fayil < 0) { Kuskure(Fayil); return; }
            단말.Yi_Rubutu("HEX BEGIN "); 단말.수(Mahardatar_kwamfuta_Fayiloli.Girma(Fayil)); 단말.문자(10);
            int 항목수 = 0;
            while (true) {
                int Daraja = Mahardatar_kwamfuta_Fayiloli.Yi_Karatu(Fayil); if (Daraja < 0 || Daraja == 256) break;
                단말.문자("0123456789abcdef".charAt(Daraja >> 4)); 단말.문자("0123456789abcdef".charAt(Daraja & 15));
                if (++항목수 % 32 == 0) 단말.문자(10);
            }
            if (항목수 % 32 != 0) 단말.문자(10);
            Mahardatar_kwamfuta_Fayiloli.Rufe(Fayil); 단말.Yi_Rubutu("HEX END\n"); return;
        }
        gyaran_Suna_Tsawo = Tsawo_Daraja[1];
        for (int Warware_Indes = 0; Warware_Indes < gyaran_Suna_Tsawo; Warware_Indes++) gyaran_Suna[Warware_Indes] = token_Daraja[시작점[1] + Warware_Indes];
        단말.Yi_Rubutu("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Girma = 0;
        while (true) {
            단말.Yi_Rubutu("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Yi_Rubutu("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && Layi[0] == '.') break;
            int kyamarar_gaba_Daraja = -1;
            for (int Warware_Indes = 0; Warware_Indes < 입력; Warware_Indes++) {
                if (Layi[Warware_Indes] == 32 || Layi[Warware_Indes] == 9) continue;
                int Daraja = 십육(Layi[Warware_Indes]);
                if (Daraja < 0 || Girma >= 편집내용.length) { 단말.Yi_Rubutu("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (kyamarar_gaba_Daraja < 0) kyamarar_gaba_Daraja = Daraja; else { 편집내용[Girma++] = kyamarar_gaba_Daraja * 16 + Daraja; kyamarar_gaba_Daraja = -1; }
            }
            if (kyamarar_gaba_Daraja >= 0) { 단말.Yi_Rubutu("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_Fara(gyaran_Suna_Tsawo);
        for (int Warware_Indes = 0; Warware_Indes < gyaran_Suna_Tsawo; Warware_Indes++) Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_bayit(Warware_Indes, gyaran_Suna[Warware_Indes]);
        int Fayil = Mahardatar_kwamfuta_Fayiloli.Buɗe(577); if (Fayil < 0) { Kuskure(Fayil); return; }
        for (int Warware_Indes = 0; Warware_Indes < Girma; Warware_Indes++) Mahardatar_kwamfuta_Fayiloli.Yi_Rubutu(Fayil, 편집내용[Warware_Indes]);
        Mahardatar_kwamfuta_Fayiloli.Rufe(Fayil); 단말.Yi_Rubutu("LOADED "); 단말.수(Girma); 단말.Yi_Rubutu("bayit_Daraja(주기억 Fayil)\n");
    }
    static int Kaya(int Indes) {
        return kayan_aiki_Mashigar_bayanai(Indes, 1);
    }
    static int kayan_aiki_Mashigar_bayanai(int Indes, int Tafiyar_da) {
        if (토큰수 - Tafiyar_da > 8) return -22;
        보드.인수준비(토큰수 - Tafiyar_da);
        for (int 첫값 = Tafiyar_da; 첫값 < 토큰수; 첫값++) {
            if (Tsawo_Daraja[첫값] > 255) return -36;
            for (int Warware_Indes = 0; Warware_Indes < Tsawo_Daraja[첫값]; Warware_Indes++) 보드.Tubalin_aiki_bayit(첫값 - Tafiyar_da, Warware_Indes, token_Daraja[시작점[첫값] + Warware_Indes]);
        }
        return Indes == -2 ? 보드.리눅스파일실행() : Indes < 0 ? 보드.gudanar_Mai_anfani_da_kwamfuta_Fayil() : 보드.Gudanar_da_Mai_anfani_da_kwamfuta_Shiri(Indes);
    }
    static int 파이썬꾸러미() {
        if (토큰수 > 8) return -22;
        보드.인수준비(토큰수);
        String Hanyar_shiga = "/lib/dami.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int 자리 = 0;
        for (int 순번 = 0; 순번 < Hanyar_shiga.length(); 순번++) {
            int Harafi_Daraja = Hanyar_shiga.charAt(순번);
            if (Harafi_Daraja < 128) 보드.Tubalin_aiki_bayit(0, 자리++, Harafi_Daraja);
            else { 보드.Tubalin_aiki_bayit(0, 자리++, 0xe0 | (Harafi_Daraja >> 12)); 보드.Tubalin_aiki_bayit(0, 자리++, 0x80 | ((Harafi_Daraja >> 6) & 63)); 보드.Tubalin_aiki_bayit(0, 자리++, 0x80 | (Harafi_Daraja & 63)); }
        }
        for (int 순번 = 1; 순번 < 토큰수; 순번++) {
            if (Tsawo_Daraja[순번] > 255) return -36;
            for (int Harafi_Daraja = 0; Harafi_Daraja < Tsawo_Daraja[순번]; Harafi_Daraja++) 보드.Tubalin_aiki_bayit(순번, Harafi_Daraja, token_Daraja[시작점[순번] + Harafi_Daraja]);
        }
        return 보드.Gudanar_da_Mai_anfani_da_kwamfuta_Shiri(12);
    }
    static int 실행형식() {
        int 처리값 = Hanyar_shiga(0); if (처리값 < 0) return 처리값;
        int Fayil = Mahardatar_kwamfuta_Fayiloli.Buɗe(0); if (Fayil < 0) return Fayil;
        int 첫값 = Mahardatar_kwamfuta_Fayiloli.Yi_Karatu(Fayil), bayit_Tarin_bayani = Mahardatar_kwamfuta_Fayiloli.Yi_Karatu(Fayil), Lambar_sirrin_harafi = Mahardatar_kwamfuta_Fayiloli.Yi_Karatu(Fayil), 뒷값 = Mahardatar_kwamfuta_Fayiloli.Yi_Karatu(Fayil);
        Mahardatar_kwamfuta_Fayiloli.Rufe(Fayil);
        if (첫값 == 127 && bayit_Tarin_bayani == 'E' && Lambar_sirrin_harafi == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && bayit_Tarin_bayani == 'K' && Lambar_sirrin_harafi == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int Indes, String 인수) {
        보드.인수준비(1);
        for (int Warware_Indes = 0; Warware_Indes < 인수.length(); Warware_Indes++) 보드.Tubalin_aiki_bayit(0, Warware_Indes, 인수.charAt(Warware_Indes));
        return 보드.Gudanar_da_Mai_anfani_da_kwamfuta_Shiri(Indes);
    }
    static void SMS_bayit(int Fayil, int Daraja) { Mahardatar_kwamfuta_Fayiloli.Yi_Rubutu(Fayil, Daraja); }
    static void Tsaye_cik_Fayil(String Suna, String kunshiya_Daraja) {
        // dami 파일명은 ASCII. Fayil 내용은 UTF-8로 저장한다.
        Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_Fara(Suna.length());
        for (int Warware_Indes = 0; Warware_Indes < Suna.length(); Warware_Indes++) Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_bayit(Warware_Indes, Suna.charAt(Warware_Indes));
        int Fayil = Mahardatar_kwamfuta_Fayiloli.Buɗe(193); if (Fayil < 0) return;
        for (int Warware_Indes = 0; Warware_Indes < kunshiya_Daraja.length(); Warware_Indes++) {
            int Lambar_sirrin_harafi = kunshiya_Daraja.charAt(Warware_Indes);
            if (Lambar_sirrin_harafi >= 0xd800 && Lambar_sirrin_harafi <= 0xdbff && Warware_Indes + 1 < kunshiya_Daraja.length()) Lambar_sirrin_harafi = 0x10000 + ((Lambar_sirrin_harafi - 0xd800) << 10) + kunshiya_Daraja.charAt(++Warware_Indes) - 0xdc00;
            if (Lambar_sirrin_harafi < 128) SMS_bayit(Fayil, Lambar_sirrin_harafi);
            else {
                int 수 = Lambar_sirrin_harafi < 2048 ? 2 : Lambar_sirrin_harafi < 65536 ? 3 : 4;
                SMS_bayit(Fayil, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (Lambar_sirrin_harafi >> (6 * (수 - 1))));
                for (int 항목수 = 수 - 1; 항목수 > 0; 항목수--) SMS_bayit(Fayil, 0x80 | ((Lambar_sirrin_harafi >> (6 * (항목수 - 1))) & 63));
            }
        }
        Mahardatar_kwamfuta_Fayiloli.Rufe(Fayil);
    }
    static void 한글도움말() {
        단말.Yi_Rubutu("F9 / Shift+Space: [EN] ↔ [ha]\n");
        단말.Yi_Rubutu("  [HA] keyboard; [EN] ASCII\n");
        단말.Yi_Rubutu("  a → a\n");
        단말.Yi_Rubutu("  F9: EN ↔ ha | Ctrl+Shift+V: UTF-8\n");
        단말.Yi_Rubutu("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Yi_Rubutu("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Suna) {
        int 바이트수 = 0;
        for (int Warware_Indes = 0; Warware_Indes < Suna.length(); Warware_Indes++) { int Lambar_sirrin_harafi = Suna.charAt(Warware_Indes); if (Lambar_sirrin_harafi >= 0xd800 && Lambar_sirrin_harafi <= 0xdfff) return -22; 바이트수 += Lambar_sirrin_harafi < 128 ? 1 : Lambar_sirrin_harafi < 2048 ? 2 : 3; }
        int 처리값 = Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_Fara(바이트수); if (처리값 < 0) return 처리값;
        int 자리 = 0;
        for (int Warware_Indes = 0; Warware_Indes < Suna.length(); Warware_Indes++) {
            int Lambar_sirrin_harafi = Suna.charAt(Warware_Indes);
            if (Lambar_sirrin_harafi < 128) Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_bayit(자리++, Lambar_sirrin_harafi);
            else if (Lambar_sirrin_harafi < 2048) { Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_bayit(자리++, 0xc0 | (Lambar_sirrin_harafi >> 6)); Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_bayit(자리++, 0x80 | (Lambar_sirrin_harafi & 63)); }
            else { Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_bayit(자리++, 0xe0 | (Lambar_sirrin_harafi >> 12)); Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_bayit(자리++, 0x80 | ((Lambar_sirrin_harafi >> 6) & 63)); Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_bayit(자리++, 0x80 | (Lambar_sirrin_harafi & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Suna) {
        int 처리값 = 예제경로(Suna); if (처리값 < 0) return 처리값;
        처리값 = Mahardatar_kwamfuta_Fayiloli.ƙirƙíra_ma_ajiya(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Suna, String Tarin_bayani) {
        int 처리값 = 예제경로(Suna); if (처리값 < 0) return 처리값;
        int Fayil = Mahardatar_kwamfuta_Fayiloli.Buɗe(193); if (Fayil == -17) return 0; if (Fayil < 0) return Fayil;
        for (int Warware_Indes = 0; Warware_Indes < Tarin_bayani.length(); Warware_Indes += 2) {
            처리값 = Mahardatar_kwamfuta_Fayiloli.Yi_Rubutu(Fayil, 십육(Tarin_bayani.charAt(Warware_Indes)) * 16 + 십육(Tarin_bayani.charAt(Warware_Indes + 1)));
            if (처리값 < 0) { Mahardatar_kwamfuta_Fayiloli.Rufe(Fayil); return 처리값; }
        }
        return Mahardatar_kwamfuta_Fayiloli.Rufe(Fayil);
    }
    static void Nuna_Taimako() {
        na_ura_kayan_aiki.Nuna_Taimako();
        단말.Yi_Rubutu("sshd / kararre_Mai_fayyace_umani start|stop|status: SSH :22 (user, 장치별 kalmar_sirri_Daraja)\n");
        단말.Yi_Rubutu("vncd / na_nesa_Nuna start|stop|status: VNC :5900 (장치별 kalmar_sirri_Daraja)\n");
        단말.Yi_Rubutu("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Yi_Rubutu("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Yi_Rubutu("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Yi_Rubutu("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Yi_Rubutu("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Yi_Rubutu("모서리 + 왼쪽 버튼 Jawo_abu_Daraja: 터미널 Girma Canza_Daraja; terminal size: ginshiƙi_Daraja/layin_kwance_Daraja\n");
        단말.Yi_Rubutu("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Yi_Rubutu("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Yi_Rubutu("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Yi_Rubutu("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Yi_Rubutu("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Yi_Rubutu("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Yi_Rubutu("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Yi_Rubutu("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Yi_Rubutu("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Yi_Rubutu("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Yi_Rubutu("pip: MicroPython tushe_Li_irabin_tarin_bayanai Girka_Daraja; sauka --network --pip 필요; /lib는 RAM\n");
        단말.Yi_Rubutu("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Yi_Rubutu("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Yi_Rubutu("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Yi_Rubutu("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void 터미널(boolean 전환여부) {
        if (전환여부 && 보드.터미널(2) != 0) { 보드.터미널(0); 단말.Yi_Rubutu("TERMINAL CLOSED\n"); }
        else if (보드.터미널(1) < 0) Kuskure(-19);
        else 단말.Yi_Rubutu("TERMINAL READY — ha terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Umarni() {
        if (토큰수 == 0) return;
        if (na_ura_kayan_aiki.gudanar_Umarni()) return;
        if (같음(0,"sshd") || 같음(0,"kararre_Mai_fayyace_umani") || 같음(0,"vncd") || 같음(0,"na_nesa_Nuna")) {
            int 종류=같음(0,"vncd")||같음(0,"na_nesa_Nuna")?1:0;
            int Aiki=같음(1,"start")||같음(1,"Tafiyar_da")?1:같음(1,"stop")||같음(1,"Tsai_da")?0:2;
            int Matsayi_Daraja=보드.yin_inuwa(종류,Aiki);
            if(Matsayi_Daraja<0)Kuskure(Matsayi_Daraja);else 단말.Yi_Rubutu(보드.yin_inuwa(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else Nuna_Taimako(); }
        else if (같음(0, "info") || 같음(0, "i")) Kwara.msinfo32_exe();
        else if (같음(0, "pwd")) { Mahardatar_kwamfuta_Fayiloli.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (토큰수 == 1) { Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_Fara(1); 처리값 = Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_bayit(0, '/'); } else 처리값 = 토큰수 == 2 ? Hanyar_shiga(1) : -22;
            if (처리값 >= 0) 처리값 = Mahardatar_kwamfuta_Fayiloli.Canza_ma_ajiya(); if (처리값 < 0) Kuskure(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int Tubalin_aiki_Indes = 같음(1, "-l") ? 2 : 1, 처리값;
            if (토큰수 == Tubalin_aiki_Indes) { Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_Fara(1); 처리값 = Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_bayit(0, '.'); } else 처리값 = 토큰수 == Tubalin_aiki_Indes + 1 ? Hanyar_shiga(Tubalin_aiki_Indes) : -22;
            if (처리값 >= 0) 처리값 = Mahardatar_kwamfuta_Fayiloli.경로목록(); if (처리값 < 0) Kuskure(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) Mai_fayyace_umani_Kaya.Fayil_Kes(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) Mai_fayyace_umani_Kaya.Kwafi_Daraja(같음(0, "mv"));
        else if (같음(0, "cat")) Mai_fayyace_umani_Kaya.s_Daraja();
        else if (같음(0, "wc")) Mai_fayyace_umani_Kaya.세기();
        else if (같음(0, "grep")) Mai_fayyace_umani_Kaya.nema_Mashigar_bayanai();
        else if (같음(0, "head") || 같음(0, "tail")) Mai_fayyace_umani_Kaya.머리(같음(0, "tail"));
        else if (같음(0, "tee")) Mai_fayyace_umani_Kaya.함께쓰기();
        else if (같음(0, "env")) Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (토큰수 == 1) Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.환경보기();
            for (int Warware_Indes = 1; Warware_Indes < 토큰수; Warware_Indes++) { int 처리값 = Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.환경설정(Warware_Indes, 같음(0, "unset")); if (처리값 != 0) { 결과 = 처리값; 단말.Yi_Rubutu("Umarni Daddatse_Daraja: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.gudanar_Fayil();
        else if (같음(0, "true")) 결과 = 0;
        else if (같음(0, "false")) 결과 = 1;
        else if (같음(0, "history")) Layi_Edita.Nuna_logu();
        else if (같음(0, "exit")) {
            if (Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.깊이 > 0) { 결과 = 토큰수 == 1 ? Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.Matsayi_Daraja : Mai_fayyace_umani_Kaya.lamba_Daraja(1); if (결과 < 0 || 결과 > 255) 결과 = 2; Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.skript_Ƙarshe = true; }
            else if (보드.터미널(2) != 0) 터미널(true);
            else 단말.Yi_Rubutu("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) gyaran_Daraja();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (토큰수 < 2) { 결과 = 2; 단말.Yi_Rubutu("사용법: rm Fayil...\n"); }
            for (int Warware_Indes = 1; Warware_Indes < 토큰수; Warware_Indes++) { int 처리값 = Hanyar_shiga(Warware_Indes); if (처리값 == 0) 처리값 = Mahardatar_kwamfuta_Fayiloli.share_Mashigar_bayanai(); if (처리값 < 0) Kuskure(처리값); }
        }
        else if (같음(0, "echo")) {
            int 시작자리 = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = 시작자리; 첫값 < 토큰수; 첫값++) { if (첫값 > 시작자리) 단말.문자(32); for (int Warware_Indes = 0; Warware_Indes < Tsawo_Daraja[첫값]; Warware_Indes++) 보드.직렬쓰기(token_Daraja[시작점[첫값] + Warware_Indes]); }
            if (시작자리 == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Yi_Rubutu("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? 파이썬꾸러미() : Kaya(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.연결중) { 단말.Yi_Rubutu("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Kaya(13); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Kaya(15); 결과 = 처리값 < 0 ? 126 : 처리값; if (!Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.연결중) { 단말.Yi_Rubutu("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Kaya(16); 결과 = 처리값 < 0 ? 126 : 처리값; if (!Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.연결중) { 단말.Yi_Rubutu("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Girma = 보드.터미널(13); 단말.Yi_Rubutu("TERMINAL SIZE "); 단말.수(Girma & 65535); 단말.문자('x'); 단말.수(Girma >>> 16); 단말.문자(10); }
            else 터미널(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { 보드.터미널(9); destof.gudanar_Umarni(); }
        else if (같음(0, "c")) Kwara.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) Kwara.작업시험();
        else if (같음(0, "g")) Kwara.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) Kwara.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = 보드.Gudanar_da_Mai_anfani_da_kwamfuta_Shiri(0); if (처리값 == 0) 단말.Yi_Rubutu("ELF DEMO PASS\n"); else Kuskure(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? kayan_aiki_Mashigar_bayanai(-2, 2) : Kaya(-1); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.연결중) { 단말.Yi_Rubutu("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) Kwara.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = 보드.Fayil_Gusar_da_sabis(1); if (처리값 < 0) Kuskure(처리값); else { 단말.Yi_Rubutu("FTP listening "); na_ura_kayan_aiki.Rubuta_imel(보드.Hanyar_sadarwa_samuwa(0,0)); 단말.Yi_Rubutu(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { 보드.Fayil_Gusar_da_sabis(0); 단말.Yi_Rubutu("FTP stopped\n"); }
            else 단말.Yi_Rubutu(보드.Fayil_Gusar_da_sabis(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { dami.Shirya(); 단말.Yi_Rubutu("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int yare = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (토큰수 != 2 || yare < 0) 단말.Yi_Rubutu("example java|c|python: 출력, Fayil, 네트워크, 그래픽, Java Swing taga 예제\n");
            else { int 처리값 = 예제꾸러미.Girka_Daraja(yare); if (처리값 < 0) { Kuskure(처리값); if (처리값 == -28) 단말.Yi_Rubutu("RAM full: remove unused files, then retry example\n"); } else 단말.Yi_Rubutu("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int zubi_Daraja = 실행형식();
            if (zubi_Daraja == 1 || zubi_Daraja == 2) {
                int 처리값 = kayan_aiki_Mashigar_bayanai(zubi_Daraja == 1 ? -1 : 14, 0); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.연결중) { 단말.Yi_Rubutu("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (zubi_Daraja == 0) { 결과 = 126; 단말.Yi_Rubutu("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { 결과 = 127; 단말.Yi_Rubutu("Unknown command. help: commands\n"); }
        }
    }
    public static void gudanar_Umarni() {
        dami.Shirya();
        for (int yare = 0; yare < 3; yare++) { int 처리값 = 예제꾸러미.Girka_Daraja(yare); if (처리값 < 0) Kuskure(처리값); }
        Nuna_Taimako();
        while (true) {
            taga_Mahadin_canjin_bayanai.haryar_aikin_na_ura_Daraja_Mashigar_bayanai(); if (taga_Mahadin_canjin_bayanai.재개()) continue;
            if (!taga_Mahadin_canjin_bayanai.이어읽기) 단말.Yi_Rubutu("jkoros-native> "); Layi_Edita.Layin_umurni = true; 보드.na_nesa_jira(1); int Girma = 줄읽기(); 보드.na_nesa_jira(0); Layi_Edita.Layin_umurni = false;
            if (Girma == -3) continue;
            if (Girma == -2) 단말.Yi_Rubutu("Umarni Daddatse_Daraja: 명령줄이 너무 깁니다\n");
            if (Girma >= 0) { Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.skript_Ƙarshe = false; Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.gudanar_Umarni(Layi, 0, Girma, 0); } else Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.Matsayi_Daraja = 130;
            보드.Ƙarshe_na_nesa_Umarni(Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta.Matsayi_Daraja);
            Layi_Edita.Girma = Layi_Edita.Ɗan_jagora_Daraja = Layi_Edita.Fara_taga = 0;
        }
    }
}
