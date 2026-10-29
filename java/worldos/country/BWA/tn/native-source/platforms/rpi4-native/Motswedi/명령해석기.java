// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 mokwalotaelo. 따옴표, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] Mola = new int[4096], papetlana_Boleng = new int[4096], 시작점 = new int[32], boleele_Boleng = new int[32];
    static int[] 편집내용 = new int[16384], Tseleganya_leina = new int[63];
    static int 토큰수, Tseleganya_leina_boleele, 결과;
    static boolean 앞줄;
    static void 원바이트(int Boleng) { 보드.직렬쓰기(Boleng); }
    static int 줄읽기() { return Mola_Setseleganyi.읽기(); }
    static boolean 나누기(int lekanya) {
        int 위치 = 0, 끝 = 0; 토큰수 = 0;
        while (위치 < lekanya) {
            while (위치 < lekanya && (Mola[위치] == 32 || Mola[위치] == 9)) 위치++;
            if (위치 == lekanya) break;
            if (토큰수 == 16) { 단말.kwala("Taelo go_lokolola_Boleng: 인수가 너무 많습니다\n"); return false; }
            시작점[토큰수] = 끝; int 인용 = 0;
            while (위치 < lekanya) {
                int Boleng = Mola[위치++];
                if (인용 == 0 && (Boleng == 32 || Boleng == 9)) break;
                if (Boleng == 인용) { 인용 = 0; continue; }
                if (인용 == 0 && (Boleng == 39 || Boleng == 34)) { 인용 = Boleng; continue; }
                papetlana_Boleng[끝++] = Boleng;
            }
            if (인용 != 0) { 단말.kwala("Taelo go_lokolola_Boleng: 따옴표가 닫히지 않았습니다\n"); return false; }
            boleele_Boleng[토큰수] = 끝 - 시작점[토큰수]; 토큰수++;
        }
        return true;
    }
    static boolean 같음(int tshupane, String Lefoko_SMS) {
        if (tshupane >= 토큰수) return false;
        int 자리=0;
        for (int 순번=0; 순번<Lefoko_SMS.length(); 순번++) {
            int khoutuletshwao=Lefoko_SMS.charAt(순번);
            if (khoutuletshwao>=0xd800 && khoutuletshwao<=0xdbff && 순번+1<Lefoko_SMS.length()) khoutuletshwao=0x10000+((khoutuletshwao-0xd800)<<10)+Lefoko_SMS.charAt(++순번)-0xdc00;
            int 바이트수=khoutuletshwao<128?1:khoutuletshwao<2048?2:khoutuletshwao<65536?3:4;
            for (int TATELANO_Boleng=바이트수-1; TATELANO_Boleng>=0; TATELANO_Boleng--) {
                int Boleng=바이트수==1?khoutuletshwao:TATELANO_Boleng==바이트수-1?(바이트수==2?0xc0:바이트수==3?0xe0:0xf0)|(khoutuletshwao>>(6*TATELANO_Boleng)):0x80|((khoutuletshwao>>(6*TATELANO_Boleng))&63);
                if (자리>=boleele_Boleng[tshupane] || papetlana_Boleng[시작점[tshupane]+자리++]!=Boleng) return false;
            }
        }
        return 자리==boleele_Boleng[tshupane];
    }
    static int tsela(int tshupane) {
        if (tshupane >= 토큰수) return -22;
        int 결과 = memori_Difaele.tsela_simolola(boleele_Boleng[tshupane]); if (결과 < 0) return 결과;
        for (int lupu_tshupane = 0; lupu_tshupane < boleele_Boleng[tshupane]; lupu_tshupane++) {
            결과 = memori_Difaele.tsela_baete(lupu_tshupane, papetlana_Boleng[시작점[tshupane] + lupu_tshupane]); if (결과 < 0) return 결과;
        }
        return 0;
    }
    static void phoso(int tshupane) { 결과 = 1; 단말.kwala("phoso "); 단말.수(tshupane); 단말.문자(10); }
    static void Tebego_Boleng() {
        if (토큰수 != 2) { 단말.kwala("사용법: cat faele\n"); return; }
        int 결과 = tsela(1); if (결과 < 0) { phoso(결과); return; }
        int faele = memori_Difaele.bula(0); if (faele < 0) { phoso(faele); return; }
        while (true) { int Boleng = memori_Difaele.읽기(faele); if (Boleng == 256) break; if (Boleng < 0) { phoso(Boleng); break; } 원바이트(Boleng); }
        memori_Difaele.tswala(faele); 단말.문자(10);
    }
    static void Tseleganya_Boleng() {
        if (토큰수 != 2) { 단말.kwala("사용법: edit faele\n"); return; }
        int 결과 = tsela(1); if (결과 < 0) { phoso(결과); return; }
        Tseleganya_leina_boleele = boleele_Boleng[1];
        for (int lupu_tshupane = 0; lupu_tshupane < Tseleganya_leina_boleele; lupu_tshupane++) Tseleganya_leina[lupu_tshupane] = papetlana_Boleng[시작점[1] + lupu_tshupane];
        단말.kwala("EDIT: faele 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int lekanya = 0;
        while (true) {
            단말.kwala("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.kwala("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && Mola[0] == '.') break;
            if (입력 + 1 > 편집내용.length - lekanya) { 단말.kwala("EDIT CANCELLED: file too large\n"); return; }
            for (int lupu_tshupane = 0; lupu_tshupane < 입력; lupu_tshupane++) 편집내용[lekanya++] = Mola[lupu_tshupane];
            편집내용[lekanya++] = 10;
        }
        memori_Difaele.tsela_simolola(Tseleganya_leina_boleele);
        for (int lupu_tshupane = 0; lupu_tshupane < Tseleganya_leina_boleele; lupu_tshupane++) memori_Difaele.tsela_baete(lupu_tshupane, Tseleganya_leina[lupu_tshupane]);
        int faele = memori_Difaele.bula(577); if (faele < 0) { phoso(faele); return; }
        for (int lupu_tshupane = 0; lupu_tshupane < lekanya; lupu_tshupane++) memori_Difaele.kwala(faele, 편집내용[lupu_tshupane]);
        memori_Difaele.tswala(faele); 단말.kwala("SAVED "); 단말.수(lekanya); 단말.kwala("baete_Boleng(주기억 faele)\n");
    }
    static int 십육(int Boleng) {
        if (Boleng >= '0' && Boleng <= '9') return Boleng - '0';
        if (Boleng >= 'a' && Boleng <= 'f') return Boleng - 'a' + 10;
        if (Boleng >= 'A' && Boleng <= 'F') return Boleng - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (토큰수 != 2) { 단말.kwala("사용법: load faele | hex faele\n"); return; }
        int 결과 = tsela(1); if (결과 < 0) { phoso(결과); return; }
        if (!넣기) {
            int faele = memori_Difaele.bula(0); if (faele < 0) { phoso(faele); return; }
            단말.kwala("HEX BEGIN "); 단말.수(memori_Difaele.lekanya(faele)); 단말.문자(10);
            int 항목수 = 0;
            while (true) {
                int Boleng = memori_Difaele.읽기(faele); if (Boleng < 0 || Boleng == 256) break;
                단말.문자("0123456789abcdef".charAt(Boleng >> 4)); 단말.문자("0123456789abcdef".charAt(Boleng & 15));
                if (++항목수 % 32 == 0) 단말.문자(10);
            }
            if (항목수 % 32 != 0) 단말.문자(10);
            memori_Difaele.tswala(faele); 단말.kwala("HEX END\n"); return;
        }
        Tseleganya_leina_boleele = boleele_Boleng[1];
        for (int lupu_tshupane = 0; lupu_tshupane < Tseleganya_leina_boleele; lupu_tshupane++) Tseleganya_leina[lupu_tshupane] = papetlana_Boleng[시작점[1] + lupu_tshupane];
        단말.kwala("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int lekanya = 0;
        while (true) {
            단말.kwala("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.kwala("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && Mola[0] == '.') break;
            int 앞 = -1;
            for (int lupu_tshupane = 0; lupu_tshupane < 입력; lupu_tshupane++) {
                if (Mola[lupu_tshupane] == 32 || Mola[lupu_tshupane] == 9) continue;
                int Boleng = 십육(Mola[lupu_tshupane]);
                if (Boleng < 0 || lekanya >= 편집내용.length) { 단말.kwala("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = Boleng; else { 편집내용[lekanya++] = 앞 * 16 + Boleng; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.kwala("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        memori_Difaele.tsela_simolola(Tseleganya_leina_boleele);
        for (int lupu_tshupane = 0; lupu_tshupane < Tseleganya_leina_boleele; lupu_tshupane++) memori_Difaele.tsela_baete(lupu_tshupane, Tseleganya_leina[lupu_tshupane]);
        int faele = memori_Difaele.bula(577); if (faele < 0) { phoso(faele); return; }
        for (int lupu_tshupane = 0; lupu_tshupane < lekanya; lupu_tshupane++) memori_Difaele.kwala(faele, 편집내용[lupu_tshupane]);
        memori_Difaele.tswala(faele); 단말.kwala("LOADED "); 단말.수(lekanya); 단말.kwala("baete_Boleng(주기억 faele)\n");
    }
    static int Thuluse(int tshupane) {
        return sediriswa_tsenyo(tshupane, 1);
    }
    static int sediriswa_tsenyo(int tshupane, int dirisa) {
        if (토큰수 - dirisa > 8) return -22;
        보드.인수준비(토큰수 - dirisa);
        for (int 첫값 = dirisa; 첫값 < 토큰수; 첫값++) {
            if (boleele_Boleng[첫값] > 255) return -36;
            for (int lupu_tshupane = 0; lupu_tshupane < boleele_Boleng[첫값]; lupu_tshupane++) 보드.Thulaganyo_baete(첫값 - dirisa, lupu_tshupane, papetlana_Boleng[시작점[첫값] + lupu_tshupane]);
        }
        return tshupane == -2 ? 보드.리눅스파일실행() : tshupane < 0 ? 보드.diragatsa_modirisi_faele() : 보드.dirisa_modirisi_Tiriso(tshupane);
    }
    static int 파이썬꾸러미() {
        if (토큰수 > 8) return -22;
        보드.인수준비(토큰수);
        String tsela = "/lib/ngatanngwe.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int 자리 = 0;
        for (int 순번 = 0; 순번 < tsela.length(); 순번++) {
            int Letshwao_Boleng = tsela.charAt(순번);
            if (Letshwao_Boleng < 128) 보드.Thulaganyo_baete(0, 자리++, Letshwao_Boleng);
            else { 보드.Thulaganyo_baete(0, 자리++, 0xe0 | (Letshwao_Boleng >> 12)); 보드.Thulaganyo_baete(0, 자리++, 0x80 | ((Letshwao_Boleng >> 6) & 63)); 보드.Thulaganyo_baete(0, 자리++, 0x80 | (Letshwao_Boleng & 63)); }
        }
        for (int 순번 = 1; 순번 < 토큰수; 순번++) {
            if (boleele_Boleng[순번] > 255) return -36;
            for (int Letshwao_Boleng = 0; Letshwao_Boleng < boleele_Boleng[순번]; Letshwao_Boleng++) 보드.Thulaganyo_baete(순번, Letshwao_Boleng, papetlana_Boleng[시작점[순번] + Letshwao_Boleng]);
        }
        return 보드.dirisa_modirisi_Tiriso(12);
    }
    static int 실행형식() {
        int 처리값 = tsela(0); if (처리값 < 0) return 처리값;
        int faele = memori_Difaele.bula(0); if (faele < 0) return faele;
        int 첫값 = memori_Difaele.읽기(faele), baete_tshedimosetso = memori_Difaele.읽기(faele), khoutuletshwao = memori_Difaele.읽기(faele), 뒷값 = memori_Difaele.읽기(faele);
        memori_Difaele.tswala(faele);
        if (첫값 == 127 && baete_tshedimosetso == 'E' && khoutuletshwao == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && baete_tshedimosetso == 'K' && khoutuletshwao == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int tshupane, String 인수) {
        보드.인수준비(1);
        for (int lupu_tshupane = 0; lupu_tshupane < 인수.length(); lupu_tshupane++) 보드.Thulaganyo_baete(0, lupu_tshupane, 인수.charAt(lupu_tshupane));
        return 보드.dirisa_modirisi_Tiriso(tshupane);
    }
    static void SMS_baete(int faele, int Boleng) { memori_Difaele.kwala(faele, Boleng); }
    static void e_e_emeng_faele(String leina, String Diteng_Boleng) {
        // ngatanngwe 파일명은 ASCII. faele 내용은 UTF-8로 저장한다.
        memori_Difaele.tsela_simolola(leina.length());
        for (int lupu_tshupane = 0; lupu_tshupane < leina.length(); lupu_tshupane++) memori_Difaele.tsela_baete(lupu_tshupane, leina.charAt(lupu_tshupane));
        int faele = memori_Difaele.bula(193); if (faele < 0) return;
        for (int lupu_tshupane = 0; lupu_tshupane < Diteng_Boleng.length(); lupu_tshupane++) {
            int khoutuletshwao = Diteng_Boleng.charAt(lupu_tshupane);
            if (khoutuletshwao >= 0xd800 && khoutuletshwao <= 0xdbff && lupu_tshupane + 1 < Diteng_Boleng.length()) khoutuletshwao = 0x10000 + ((khoutuletshwao - 0xd800) << 10) + Diteng_Boleng.charAt(++lupu_tshupane) - 0xdc00;
            if (khoutuletshwao < 128) SMS_baete(faele, khoutuletshwao);
            else {
                int 수 = khoutuletshwao < 2048 ? 2 : khoutuletshwao < 65536 ? 3 : 4;
                SMS_baete(faele, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (khoutuletshwao >> (6 * (수 - 1))));
                for (int 항목수 = 수 - 1; 항목수 > 0; 항목수--) SMS_baete(faele, 0x80 | ((khoutuletshwao >> (6 * (항목수 - 1))) & 63));
            }
        }
        memori_Difaele.tswala(faele);
    }
    static void 한글도움말() {
        단말.kwala("F9 / Shift+Space: [EN] ↔ [tn]\n");
        단말.kwala("  [TN] keyboard; [EN] ASCII\n");
        단말.kwala("  a → a\n");
        단말.kwala("  F9: EN ↔ tn | Ctrl+Shift+V: UTF-8\n");
        단말.kwala("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.kwala("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String leina) {
        int 바이트수 = 0;
        for (int lupu_tshupane = 0; lupu_tshupane < leina.length(); lupu_tshupane++) { int khoutuletshwao = leina.charAt(lupu_tshupane); if (khoutuletshwao >= 0xd800 && khoutuletshwao <= 0xdfff) return -22; 바이트수 += khoutuletshwao < 128 ? 1 : khoutuletshwao < 2048 ? 2 : 3; }
        int 처리값 = memori_Difaele.tsela_simolola(바이트수); if (처리값 < 0) return 처리값;
        int 자리 = 0;
        for (int lupu_tshupane = 0; lupu_tshupane < leina.length(); lupu_tshupane++) {
            int khoutuletshwao = leina.charAt(lupu_tshupane);
            if (khoutuletshwao < 128) memori_Difaele.tsela_baete(자리++, khoutuletshwao);
            else if (khoutuletshwao < 2048) { memori_Difaele.tsela_baete(자리++, 0xc0 | (khoutuletshwao >> 6)); memori_Difaele.tsela_baete(자리++, 0x80 | (khoutuletshwao & 63)); }
            else { memori_Difaele.tsela_baete(자리++, 0xe0 | (khoutuletshwao >> 12)); memori_Difaele.tsela_baete(자리++, 0x80 | ((khoutuletshwao >> 6) & 63)); memori_Difaele.tsela_baete(자리++, 0x80 | (khoutuletshwao & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String leina) {
        int 처리값 = 예제경로(leina); if (처리값 < 0) return 처리값;
        처리값 = memori_Difaele.tlhama_Lenaneofaele(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String leina, String tshedimosetso) {
        int 처리값 = 예제경로(leina); if (처리값 < 0) return 처리값;
        int faele = memori_Difaele.bula(193); if (faele == -17) return 0; if (faele < 0) return faele;
        for (int lupu_tshupane = 0; lupu_tshupane < tshedimosetso.length(); lupu_tshupane += 2) {
            처리값 = memori_Difaele.kwala(faele, 십육(tshedimosetso.charAt(lupu_tshupane)) * 16 + 십육(tshedimosetso.charAt(lupu_tshupane + 1)));
            if (처리값 < 0) { memori_Difaele.tswala(faele); return 처리값; }
        }
        return memori_Difaele.tswala(faele);
    }
    static void bontsha_thuso() {
        tsamaiso_sediriswa.bontsha_thuso();
        단말.kwala("sshd / sireletsegile_setlhalosataelo start|stop|status: SSH :22 (user, 장치별 khoututseno_Boleng)\n");
        단말.kwala("vncd / kgakala_bontsha start|stop|status: VNC :5900 (장치별 khoututseno_Boleng)\n");
        단말.kwala("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.kwala("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.kwala("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.kwala("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.kwala("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.kwala("모서리 + 왼쪽 버튼 Goga_Boleng: 터미널 lekanya fetola_Boleng; terminal size: Kholomo_Boleng/mola_Boleng\n");
        단말.kwala("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.kwala("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.kwala("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.kwala("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.kwala("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.kwala("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.kwala("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.kwala("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.kwala("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.kwala("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.kwala("pip: MicroPython Motswedi_sebopego_sa_tshedimosetso tsenya_Boleng; pinagare --network --pip 필요; /lib는 RAM\n");
        단말.kwala("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.kwala("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.kwala("/example/java /example/c /example/python: examples ready at boot\n");
        단말.kwala("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void 터미널(boolean 전환여부) {
        if (전환여부 && 보드.터미널(2) != 0) { 보드.터미널(0); 단말.kwala("TERMINAL CLOSED\n"); }
        else if (보드.터미널(1) < 0) phoso(-19);
        else 단말.kwala("TERMINAL READY — tn terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Taelo() {
        if (토큰수 == 0) return;
        if (tsamaiso_sediriswa.diragatsa_Taelo()) return;
        if (같음(0,"sshd") || 같음(0,"sireletsegile_setlhalosataelo") || 같음(0,"vncd") || 같음(0,"kgakala_bontsha")) {
            int 종류=같음(0,"vncd")||같음(0,"kgakala_bontsha")?1:0;
            int tiro=같음(1,"start")||같음(1,"dirisa")?1:같음(1,"stop")||같음(1,"emisa")?0:2;
            int kemo_Boleng=보드.ritifatsa(종류,tiro);
            if(kemo_Boleng<0)phoso(kemo_Boleng);else 단말.kwala(보드.ritifatsa(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else bontsha_thuso(); }
        else if (같음(0, "info") || 같음(0, "i")) Khenele.msinfo32_exe();
        else if (같음(0, "pwd")) { memori_Difaele.ga_jaana_kwala(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (토큰수 == 1) { memori_Difaele.tsela_simolola(1); 처리값 = memori_Difaele.tsela_baete(0, '/'); } else 처리값 = 토큰수 == 2 ? tsela(1) : -22;
            if (처리값 >= 0) 처리값 = memori_Difaele.fetola_Lenaneofaele(); if (처리값 < 0) phoso(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int Thulaganyo_tshupane = 같음(1, "-l") ? 2 : 1, 처리값;
            if (토큰수 == Thulaganyo_tshupane) { memori_Difaele.tsela_simolola(1); 처리값 = memori_Difaele.tsela_baete(0, '.'); } else 처리값 = 토큰수 == Thulaganyo_tshupane + 1 ? tsela(Thulaganyo_tshupane) : -22;
            if (처리값 >= 0) 처리값 = memori_Difaele.경로목록(); if (처리값 < 0) phoso(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) setlhalosataelo_Thuluse.faele_Tiro(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) setlhalosataelo_Thuluse.leloko_Boleng(같음(0, "mv"));
        else if (같음(0, "cat")) setlhalosataelo_Thuluse.Tebego_Boleng();
        else if (같음(0, "wc")) setlhalosataelo_Thuluse.세기();
        else if (같음(0, "grep")) setlhalosataelo_Thuluse.batla_tsenyo();
        else if (같음(0, "head") || 같음(0, "tail")) setlhalosataelo_Thuluse.머리(같음(0, "tail"));
        else if (같음(0, "tee")) setlhalosataelo_Thuluse.함께쓰기();
        else if (같음(0, "env")) setlhalosataelo_popapolelo.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (토큰수 == 1) setlhalosataelo_popapolelo.환경보기();
            for (int lupu_tshupane = 1; lupu_tshupane < 토큰수; lupu_tshupane++) { int 처리값 = setlhalosataelo_popapolelo.환경설정(lupu_tshupane, 같음(0, "unset")); if (처리값 != 0) { 결과 = 처리값; 단말.kwala("Taelo go_lokolola_Boleng: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) setlhalosataelo_popapolelo.diragatsa_faele();
        else if (같음(0, "true")) 결과 = 0;
        else if (같음(0, "false")) 결과 = 1;
        else if (같음(0, "history")) Mola_Setseleganyi.bontsha_rekota();
        else if (같음(0, "exit")) {
            if (setlhalosataelo_popapolelo.깊이 > 0) { 결과 = 토큰수 == 1 ? setlhalosataelo_popapolelo.kemo_Boleng : setlhalosataelo_Thuluse.dijite_Boleng(1); if (결과 < 0 || 결과 > 255) 결과 = 2; setlhalosataelo_popapolelo.Sekeripiti_kgaola = true; }
            else if (보드.터미널(2) != 0) 터미널(true);
            else 단말.kwala("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) Tseleganya_Boleng();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (토큰수 < 2) { 결과 = 2; 단말.kwala("사용법: rm faele...\n"); }
            for (int lupu_tshupane = 1; lupu_tshupane < 토큰수; lupu_tshupane++) { int 처리값 = tsela(lupu_tshupane); if (처리값 == 0) 처리값 = memori_Difaele.지우기(); if (처리값 < 0) phoso(처리값); }
        }
        else if (같음(0, "echo")) {
            int 시작자리 = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = 시작자리; 첫값 < 토큰수; 첫값++) { if (첫값 > 시작자리) 단말.문자(32); for (int lupu_tshupane = 0; lupu_tshupane < boleele_Boleng[첫값]; lupu_tshupane++) 보드.직렬쓰기(papetlana_Boleng[시작점[첫값] + lupu_tshupane]); }
            if (시작자리 == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.kwala("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? 파이썬꾸러미() : Thuluse(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !setlhalosataelo_popapolelo.연결중) { 단말.kwala("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Thuluse(13); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Thuluse(15); 결과 = 처리값 < 0 ? 126 : 처리값; if (!setlhalosataelo_popapolelo.연결중) { 단말.kwala("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Thuluse(16); 결과 = 처리값 < 0 ? 126 : 처리값; if (!setlhalosataelo_popapolelo.연결중) { 단말.kwala("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int lekanya = 보드.터미널(13); 단말.kwala("TERMINAL SIZE "); 단말.수(lekanya & 65535); 단말.문자('x'); 단말.수(lekanya >>> 16); 단말.문자(10); }
            else 터미널(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { 보드.터미널(9); desekethopo.diragatsa_Taelo(); }
        else if (같음(0, "c")) Khenele.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) Khenele.작업시험();
        else if (같음(0, "g")) Khenele.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) Khenele.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = 보드.dirisa_modirisi_Tiriso(0); if (처리값 == 0) 단말.kwala("ELF DEMO PASS\n"); else phoso(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? sediriswa_tsenyo(-2, 2) : Thuluse(-1); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !setlhalosataelo_popapolelo.연결중) { 단말.kwala("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) Khenele.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = 보드.faele_fudusa_Tirelo(1); if (처리값 < 0) phoso(처리값); else { 단말.kwala("FTP listening "); tsamaiso_sediriswa.kwala_aterese(보드.Neteweke_kemo(0,0)); 단말.kwala(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { 보드.faele_fudusa_Tirelo(0); 단말.kwala("FTP stopped\n"); }
            else 단말.kwala(보드.faele_fudusa_Tirelo(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { ngatanngwe.Baakanya(); 단말.kwala("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Puo = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (토큰수 != 2 || Puo < 0) 단말.kwala("example java|c|python: 출력, faele, 네트워크, 그래픽, Java Swing fensetere 예제\n");
            else { int 처리값 = 예제꾸러미.tsenya_Boleng(Puo); if (처리값 < 0) { phoso(처리값); if (처리값 == -28) 단말.kwala("RAM full: remove unused files, then retry example\n"); } else 단말.kwala("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int fometa_Boleng = 실행형식();
            if (fometa_Boleng == 1 || fometa_Boleng == 2) {
                int 처리값 = sediriswa_tsenyo(fometa_Boleng == 1 ? -1 : 14, 0); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !setlhalosataelo_popapolelo.연결중) { 단말.kwala("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (fometa_Boleng == 0) { 결과 = 126; 단말.kwala("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { 결과 = 127; 단말.kwala("Unknown command. help: commands\n"); }
        }
    }
    public static void diragatsa_Taelo() {
        ngatanngwe.Baakanya();
        for (int Puo = 0; Puo < 3; Puo++) { int 처리값 = 예제꾸러미.tsenya_Boleng(Puo); if (처리값 < 0) phoso(처리값); }
        bontsha_thuso();
        while (true) {
            fensetere_nakotiriso.Thulaganyo_Boleng_tsenyo(); if (fensetere_nakotiriso.재개()) continue;
            if (!fensetere_nakotiriso.이어읽기) 단말.kwala("jkoros-native> "); Mola_Setseleganyi.mokwalotaelo = true; 보드.원격대기(1); int lekanya = 줄읽기(); 보드.원격대기(0); Mola_Setseleganyi.mokwalotaelo = false;
            if (lekanya == -3) continue;
            if (lekanya == -2) 단말.kwala("Taelo go_lokolola_Boleng: 명령줄이 너무 깁니다\n");
            if (lekanya >= 0) { setlhalosataelo_popapolelo.Sekeripiti_kgaola = false; setlhalosataelo_popapolelo.diragatsa_Taelo(Mola, 0, lekanya, 0); } else setlhalosataelo_popapolelo.kemo_Boleng = 130;
            보드.kgaola_kgakala_Taelo(setlhalosataelo_popapolelo.kemo_Boleng);
            Mola_Setseleganyi.lekanya = Mola_Setseleganyi.khesara_Boleng = Mola_Setseleganyi.simolola_fensetere = 0;
        }
    }
}
