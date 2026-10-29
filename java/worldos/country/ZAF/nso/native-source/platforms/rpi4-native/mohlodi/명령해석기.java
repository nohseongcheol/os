// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 mothalotlhako_wa_tirišo. 따옴표, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] mothaladi = new int[4096], thokene_boleng = new int[4096], 시작점 = new int[32], botelele_boleng = new int[32];
    static int[] 편집내용 = new int[16384], rulaganya_leina = new int[63];
    static int 토큰수, rulaganya_leina_botelele, 결과;
    static boolean 앞줄;
    static void 원바이트(int boleng) { 보드.직렬쓰기(boleng); }
    static int 줄읽기() { return mothaladi_Morulaganyi.Bala(); }
    static boolean 나누기(int Bogolo) {
        int 위치 = 0, 끝 = 0; 토큰수 = 0;
        while (위치 < Bogolo) {
            while (위치 < Bogolo && (mothaladi[위치] == 32 || mothaladi[위치] == 9)) 위치++;
            if (위치 == Bogolo) break;
            if (토큰수 == 16) { 단말.Ngwala("Taelo ripaganya_boleng: 인수가 너무 많습니다\n"); return false; }
            시작점[토큰수] = 끝; int 인용 = 0;
            while (위치 < Bogolo) {
                int boleng = mothaladi[위치++];
                if (인용 == 0 && (boleng == 32 || boleng == 9)) break;
                if (boleng == 인용) { 인용 = 0; continue; }
                if (인용 == 0 && (boleng == 39 || boleng == 34)) { 인용 = boleng; continue; }
                thokene_boleng[끝++] = boleng;
            }
            if (인용 != 0) { 단말.Ngwala("Taelo ripaganya_boleng: 따옴표가 닫히지 않았습니다\n"); return false; }
            botelele_boleng[토큰수] = 끝 - 시작점[토큰수]; 토큰수++;
        }
        return true;
    }
    static boolean 같음(int lokela, String Thalokontšu_SMS) {
        if (lokela >= 토큰수) return false;
        int 자리=0;
        for (int 순번=0; 순번<Thalokontšu_SMS.length(); 순번++) {
            int khouto_ya_tlhaka=Thalokontšu_SMS.charAt(순번);
            if (khouto_ya_tlhaka>=0xd800 && khouto_ya_tlhaka<=0xdbff && 순번+1<Thalokontšu_SMS.length()) khouto_ya_tlhaka=0x10000+((khouto_ya_tlhaka-0xd800)<<10)+Thalokontšu_SMS.charAt(++순번)-0xdc00;
            int 바이트수=khouto_ya_tlhaka<128?1:khouto_ya_tlhaka<2048?2:khouto_ya_tlhaka<65536?3:4;
            for (int TATELANO_boleng=바이트수-1; TATELANO_boleng>=0; TATELANO_boleng--) {
                int boleng=바이트수==1?khouto_ya_tlhaka:TATELANO_boleng==바이트수-1?(바이트수==2?0xc0:바이트수==3?0xe0:0xf0)|(khouto_ya_tlhaka>>(6*TATELANO_boleng)):0x80|((khouto_ya_tlhaka>>(6*TATELANO_boleng))&63);
                if (자리>=botelele_boleng[lokela] || thokene_boleng[시작점[lokela]+자리++]!=boleng) return false;
            }
        }
        return 자리==botelele_boleng[lokela];
    }
    static int Tsejana(int lokela) {
        if (lokela >= 토큰수) return -22;
        int 결과 = memori_Difaele.tsela_Thomišo(botelele_boleng[lokela]); if (결과 < 0) return 결과;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < botelele_boleng[lokela]; ditaelopoeletšwa_lokela++) {
            결과 = memori_Difaele.tsela_paete(ditaelopoeletšwa_lokela, thokene_boleng[시작점[lokela] + ditaelopoeletšwa_lokela]); if (결과 < 0) return 결과;
        }
        return 0;
    }
    static void Phošo(int lokela) { 결과 = 1; 단말.Ngwala("Phošo "); 단말.수(lokela); 단말.문자(10); }
    static void pogelo_boleng() {
        if (토큰수 != 2) { 단말.Ngwala("사용법: cat Faele\n"); return; }
        int 결과 = Tsejana(1); if (결과 < 0) { Phošo(결과); return; }
        int Faele = memori_Difaele.Bula(0); if (Faele < 0) { Phošo(Faele); return; }
        while (true) { int boleng = memori_Difaele.Bala(Faele); if (boleng == 256) break; if (boleng < 0) { Phošo(boleng); break; } 원바이트(boleng); }
        memori_Difaele.Tswalela(Faele); 단말.문자(10);
    }
    static void rulaganya_boleng() {
        if (토큰수 != 2) { 단말.Ngwala("사용법: edit Faele\n"); return; }
        int 결과 = Tsejana(1); if (결과 < 0) { Phošo(결과); return; }
        rulaganya_leina_botelele = botelele_boleng[1];
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < rulaganya_leina_botelele; ditaelopoeletšwa_lokela++) rulaganya_leina[ditaelopoeletšwa_lokela] = thokene_boleng[시작점[1] + ditaelopoeletšwa_lokela];
        단말.Ngwala("EDIT: Faele 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Bogolo = 0;
        while (true) {
            단말.Ngwala("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Ngwala("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && mothaladi[0] == '.') break;
            if (입력 + 1 > 편집내용.length - Bogolo) { 단말.Ngwala("EDIT CANCELLED: file too large\n"); return; }
            for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 입력; ditaelopoeletšwa_lokela++) 편집내용[Bogolo++] = mothaladi[ditaelopoeletšwa_lokela];
            편집내용[Bogolo++] = 10;
        }
        memori_Difaele.tsela_Thomišo(rulaganya_leina_botelele);
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < rulaganya_leina_botelele; ditaelopoeletšwa_lokela++) memori_Difaele.tsela_paete(ditaelopoeletšwa_lokela, rulaganya_leina[ditaelopoeletšwa_lokela]);
        int Faele = memori_Difaele.Bula(577); if (Faele < 0) { Phošo(Faele); return; }
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < Bogolo; ditaelopoeletšwa_lokela++) memori_Difaele.Ngwala(Faele, 편집내용[ditaelopoeletšwa_lokela]);
        memori_Difaele.Tswalela(Faele); 단말.Ngwala("SAVED "); 단말.수(Bogolo); 단말.Ngwala("paete_boleng(주기억 Faele)\n");
    }
    static int 십육(int boleng) {
        if (boleng >= '0' && boleng <= '9') return boleng - '0';
        if (boleng >= 'a' && boleng <= 'f') return boleng - 'a' + 10;
        if (boleng >= 'A' && boleng <= 'F') return boleng - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (토큰수 != 2) { 단말.Ngwala("사용법: load Faele | hex Faele\n"); return; }
        int 결과 = Tsejana(1); if (결과 < 0) { Phošo(결과); return; }
        if (!넣기) {
            int Faele = memori_Difaele.Bula(0); if (Faele < 0) { Phošo(Faele); return; }
            단말.Ngwala("HEX BEGIN "); 단말.수(memori_Difaele.Bogolo(Faele)); 단말.문자(10);
            int 항목수 = 0;
            while (true) {
                int boleng = memori_Difaele.Bala(Faele); if (boleng < 0 || boleng == 256) break;
                단말.문자("0123456789abcdef".charAt(boleng >> 4)); 단말.문자("0123456789abcdef".charAt(boleng & 15));
                if (++항목수 % 32 == 0) 단말.문자(10);
            }
            if (항목수 % 32 != 0) 단말.문자(10);
            memori_Difaele.Tswalela(Faele); 단말.Ngwala("HEX END\n"); return;
        }
        rulaganya_leina_botelele = botelele_boleng[1];
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < rulaganya_leina_botelele; ditaelopoeletšwa_lokela++) rulaganya_leina[ditaelopoeletšwa_lokela] = thokene_boleng[시작점[1] + ditaelopoeletšwa_lokela];
        단말.Ngwala("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Bogolo = 0;
        while (true) {
            단말.Ngwala("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Ngwala("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && mothaladi[0] == '.') break;
            int 앞 = -1;
            for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 입력; ditaelopoeletšwa_lokela++) {
                if (mothaladi[ditaelopoeletšwa_lokela] == 32 || mothaladi[ditaelopoeletšwa_lokela] == 9) continue;
                int boleng = 십육(mothaladi[ditaelopoeletšwa_lokela]);
                if (boleng < 0 || Bogolo >= 편집내용.length) { 단말.Ngwala("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = boleng; else { 편집내용[Bogolo++] = 앞 * 16 + boleng; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.Ngwala("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        memori_Difaele.tsela_Thomišo(rulaganya_leina_botelele);
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < rulaganya_leina_botelele; ditaelopoeletšwa_lokela++) memori_Difaele.tsela_paete(ditaelopoeletšwa_lokela, rulaganya_leina[ditaelopoeletšwa_lokela]);
        int Faele = memori_Difaele.Bula(577); if (Faele < 0) { Phošo(Faele); return; }
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < Bogolo; ditaelopoeletšwa_lokela++) memori_Difaele.Ngwala(Faele, 편집내용[ditaelopoeletšwa_lokela]);
        memori_Difaele.Tswalela(Faele); 단말.Ngwala("LOADED "); 단말.수(Bogolo); 단말.Ngwala("paete_boleng(주기억 Faele)\n");
    }
    static int Ditholosi(int lokela) {
        return tholosi_go_tsenya_tshedimošo(lokela, 1);
    }
    static int tholosi_go_tsenya_tshedimošo(int lokela, int Diriša) {
        if (토큰수 - Diriša > 8) return -22;
        보드.인수준비(토큰수 - Diriša);
        for (int 첫값 = Diriša; 첫값 < 토큰수; 첫값++) {
            if (botelele_boleng[첫값] > 255) return -36;
            for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < botelele_boleng[첫값]; ditaelopoeletšwa_lokela++) 보드.akumente_paete(첫값 - Diriša, ditaelopoeletšwa_lokela, thokene_boleng[시작점[첫값] + ditaelopoeletšwa_lokela]);
        }
        return lokela == -2 ? 보드.리눅스파일실행() : lokela < 0 ? 보드.phethagatša_mošomiši_faele() : 보드.sepetša_mošomiši_tirišo(lokela);
    }
    static int 파이썬꾸러미() {
        if (토큰수 > 8) return -22;
        보드.인수준비(토큰수);
        String Tsejana = "/lib/sehlopha.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int 자리 = 0;
        for (int 순번 = 0; 순번 < Tsejana.length(); 순번++) {
            int tlhaka_boleng = Tsejana.charAt(순번);
            if (tlhaka_boleng < 128) 보드.akumente_paete(0, 자리++, tlhaka_boleng);
            else { 보드.akumente_paete(0, 자리++, 0xe0 | (tlhaka_boleng >> 12)); 보드.akumente_paete(0, 자리++, 0x80 | ((tlhaka_boleng >> 6) & 63)); 보드.akumente_paete(0, 자리++, 0x80 | (tlhaka_boleng & 63)); }
        }
        for (int 순번 = 1; 순번 < 토큰수; 순번++) {
            if (botelele_boleng[순번] > 255) return -36;
            for (int tlhaka_boleng = 0; tlhaka_boleng < botelele_boleng[순번]; tlhaka_boleng++) 보드.akumente_paete(순번, tlhaka_boleng, thokene_boleng[시작점[순번] + tlhaka_boleng]);
        }
        return 보드.sepetša_mošomiši_tirišo(12);
    }
    static int 실행형식() {
        int 처리값 = Tsejana(0); if (처리값 < 0) return 처리값;
        int Faele = memori_Difaele.Bula(0); if (Faele < 0) return Faele;
        int 첫값 = memori_Difaele.Bala(Faele), paete_data = memori_Difaele.Bala(Faele), khouto_ya_tlhaka = memori_Difaele.Bala(Faele), 뒷값 = memori_Difaele.Bala(Faele);
        memori_Difaele.Tswalela(Faele);
        if (첫값 == 127 && paete_data == 'E' && khouto_ya_tlhaka == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && paete_data == 'K' && khouto_ya_tlhaka == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int lokela, String 인수) {
        보드.인수준비(1);
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 인수.length(); ditaelopoeletšwa_lokela++) 보드.akumente_paete(0, ditaelopoeletšwa_lokela, 인수.charAt(ditaelopoeletšwa_lokela));
        return 보드.sepetša_mošomiši_tirišo(lokela);
    }
    static void SMS_paete(int Faele, int boleng) { memori_Difaele.Ngwala(Faele, boleng); }
    static void ya_go_se_fetoge_faele(String Leina, String Diteng_boleng) {
        // sehlopha 파일명은 ASCII. Faele 내용은 UTF-8로 저장한다.
        memori_Difaele.tsela_Thomišo(Leina.length());
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < Leina.length(); ditaelopoeletšwa_lokela++) memori_Difaele.tsela_paete(ditaelopoeletšwa_lokela, Leina.charAt(ditaelopoeletšwa_lokela));
        int Faele = memori_Difaele.Bula(193); if (Faele < 0) return;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < Diteng_boleng.length(); ditaelopoeletšwa_lokela++) {
            int khouto_ya_tlhaka = Diteng_boleng.charAt(ditaelopoeletšwa_lokela);
            if (khouto_ya_tlhaka >= 0xd800 && khouto_ya_tlhaka <= 0xdbff && ditaelopoeletšwa_lokela + 1 < Diteng_boleng.length()) khouto_ya_tlhaka = 0x10000 + ((khouto_ya_tlhaka - 0xd800) << 10) + Diteng_boleng.charAt(++ditaelopoeletšwa_lokela) - 0xdc00;
            if (khouto_ya_tlhaka < 128) SMS_paete(Faele, khouto_ya_tlhaka);
            else {
                int 수 = khouto_ya_tlhaka < 2048 ? 2 : khouto_ya_tlhaka < 65536 ? 3 : 4;
                SMS_paete(Faele, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (khouto_ya_tlhaka >> (6 * (수 - 1))));
                for (int 항목수 = 수 - 1; 항목수 > 0; 항목수--) SMS_paete(Faele, 0x80 | ((khouto_ya_tlhaka >> (6 * (항목수 - 1))) & 63));
            }
        }
        memori_Difaele.Tswalela(Faele);
    }
    static void 한글도움말() {
        단말.Ngwala("F9 / Shift+Space: [EN] ↔ [nso]\n");
        단말.Ngwala("  [NSO] keyboard; [EN] ASCII\n");
        단말.Ngwala("  a → a\n");
        단말.Ngwala("  F9: EN ↔ nso | Ctrl+Shift+V: UTF-8\n");
        단말.Ngwala("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Ngwala("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Leina) {
        int 바이트수 = 0;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < Leina.length(); ditaelopoeletšwa_lokela++) { int khouto_ya_tlhaka = Leina.charAt(ditaelopoeletšwa_lokela); if (khouto_ya_tlhaka >= 0xd800 && khouto_ya_tlhaka <= 0xdfff) return -22; 바이트수 += khouto_ya_tlhaka < 128 ? 1 : khouto_ya_tlhaka < 2048 ? 2 : 3; }
        int 처리값 = memori_Difaele.tsela_Thomišo(바이트수); if (처리값 < 0) return 처리값;
        int 자리 = 0;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < Leina.length(); ditaelopoeletšwa_lokela++) {
            int khouto_ya_tlhaka = Leina.charAt(ditaelopoeletšwa_lokela);
            if (khouto_ya_tlhaka < 128) memori_Difaele.tsela_paete(자리++, khouto_ya_tlhaka);
            else if (khouto_ya_tlhaka < 2048) { memori_Difaele.tsela_paete(자리++, 0xc0 | (khouto_ya_tlhaka >> 6)); memori_Difaele.tsela_paete(자리++, 0x80 | (khouto_ya_tlhaka & 63)); }
            else { memori_Difaele.tsela_paete(자리++, 0xe0 | (khouto_ya_tlhaka >> 12)); memori_Difaele.tsela_paete(자리++, 0x80 | ((khouto_ya_tlhaka >> 6) & 63)); memori_Difaele.tsela_paete(자리++, 0x80 | (khouto_ya_tlhaka & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Leina) {
        int 처리값 = 예제경로(Leina); if (처리값 < 0) return 처리값;
        처리값 = memori_Difaele.폴더만들기(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Leina, String data) {
        int 처리값 = 예제경로(Leina); if (처리값 < 0) return 처리값;
        int Faele = memori_Difaele.Bula(193); if (Faele == -17) return 0; if (Faele < 0) return Faele;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < data.length(); ditaelopoeletšwa_lokela += 2) {
            처리값 = memori_Difaele.Ngwala(Faele, 십육(data.charAt(ditaelopoeletšwa_lokela)) * 16 + 십육(data.charAt(ditaelopoeletšwa_lokela + 1)));
            if (처리값 < 0) { memori_Difaele.Tswalela(Faele); return 처리값; }
        }
        return memori_Difaele.Tswalela(Faele);
    }
    static void bontšha_thušo() {
        lenaneo_tholosi.bontšha_thušo();
        단말.Ngwala("sshd / šireletšegile_šele start|stop|status: SSH :22 (user, 장치별 phasewete_boleng)\n");
        단말.Ngwala("vncd / ya_kgole_bontšha start|stop|status: VNC :5900 (장치별 phasewete_boleng)\n");
        단말.Ngwala("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Ngwala("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Ngwala("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Ngwala("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Ngwala("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Ngwala("모서리 + 왼쪽 버튼 goga_boleng: 터미널 Bogolo fetoša_boleng; terminal size: kholomo_boleng/rei_boleng\n");
        단말.Ngwala("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Ngwala("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Ngwala("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Ngwala("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Ngwala("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Ngwala("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Ngwala("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Ngwala("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Ngwala("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Ngwala("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Ngwala("pip: MicroPython mohlodi_mohlare hloma_boleng; go_nea_ditirelo --network --pip 필요; /lib는 RAM\n");
        단말.Ngwala("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Ngwala("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Ngwala("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Ngwala("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void 터미널(boolean 전환여부) {
        if (전환여부 && 보드.터미널(2) != 0) { 보드.터미널(0); 단말.Ngwala("TERMINAL CLOSED\n"); }
        else if (보드.터미널(1) < 0) Phošo(-19);
        else 단말.Ngwala("TERMINAL READY — nso terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Taelo() {
        if (토큰수 == 0) return;
        if (lenaneo_tholosi.phethagatša_taelo()) return;
        if (같음(0,"sshd") || 같음(0,"šireletšegile_šele") || 같음(0,"vncd") || 같음(0,"ya_kgole_bontšha")) {
            int 종류=같음(0,"vncd")||같음(0,"ya_kgole_bontšha")?1:0;
            int Mogato=같음(1,"start")||같음(1,"Diriša")?1:같음(1,"stop")||같음(1,"Emiša")?0:2;
            int boemo_boleng=보드.kekišo(종류,Mogato);
            if(boemo_boleng<0)Phošo(boemo_boleng);else 단말.Ngwala(보드.kekišo(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else bontšha_thušo(); }
        else if (같음(0, "info") || 같음(0, "i")) khenele.msinfo32_exe();
        else if (같음(0, "pwd")) { memori_Difaele.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (토큰수 == 1) { memori_Difaele.tsela_Thomišo(1); 처리값 = memori_Difaele.tsela_paete(0, '/'); } else 처리값 = 토큰수 == 2 ? Tsejana(1) : -22;
            if (처리값 >= 0) 처리값 = memori_Difaele.fetoša_lelokelelo(); if (처리값 < 0) Phošo(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int akumente_lokela = 같음(1, "-l") ? 2 : 1, 처리값;
            if (토큰수 == akumente_lokela) { memori_Difaele.tsela_Thomišo(1); 처리값 = memori_Difaele.tsela_paete(0, '.'); } else 처리값 = 토큰수 == akumente_lokela + 1 ? Tsejana(akumente_lokela) : -22;
            if (처리값 >= 0) 처리값 = memori_Difaele.경로목록(); if (처리값 < 0) Phošo(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) šele_Ditholosi.faele_taba(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) šele_Ditholosi.kopiša_boleng(같음(0, "mv"));
        else if (같음(0, "cat")) šele_Ditholosi.pogelo_boleng();
        else if (같음(0, "wc")) šele_Ditholosi.세기();
        else if (같음(0, "grep")) šele_Ditholosi.hwetša_go_tsenya_tshedimošo();
        else if (같음(0, "head") || 같음(0, "tail")) šele_Ditholosi.머리(같음(0, "tail"));
        else if (같음(0, "tee")) šele_Ditholosi.함께쓰기();
        else if (같음(0, "env")) šele_tatelanyotlhaka_tirišong.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (토큰수 == 1) šele_tatelanyotlhaka_tirišong.환경보기();
            for (int ditaelopoeletšwa_lokela = 1; ditaelopoeletšwa_lokela < 토큰수; ditaelopoeletšwa_lokela++) { int 처리값 = šele_tatelanyotlhaka_tirišong.환경설정(ditaelopoeletšwa_lokela, 같음(0, "unset")); if (처리값 != 0) { 결과 = 처리값; 단말.Ngwala("Taelo ripaganya_boleng: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) šele_tatelanyotlhaka_tirišong.phethagatša_faele();
        else if (같음(0, "true")) 결과 = 0;
        else if (같음(0, "false")) 결과 = 1;
        else if (같음(0, "history")) mothaladi_Morulaganyi.bontšha_pego();
        else if (같음(0, "exit")) {
            if (šele_tatelanyotlhaka_tirišong.깊이 > 0) { 결과 = 토큰수 == 1 ? šele_tatelanyotlhaka_tirišong.boemo_boleng : šele_Ditholosi.숫자(1); if (결과 < 0 || 결과 > 255) 결과 = 2; šele_tatelanyotlhaka_tirišong.skripte_fetša = true; }
            else if (보드.터미널(2) != 0) 터미널(true);
            else 단말.Ngwala("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) rulaganya_boleng();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (토큰수 < 2) { 결과 = 2; 단말.Ngwala("사용법: rm Faele...\n"); }
            for (int ditaelopoeletšwa_lokela = 1; ditaelopoeletšwa_lokela < 토큰수; ditaelopoeletšwa_lokela++) { int 처리값 = Tsejana(ditaelopoeletšwa_lokela); if (처리값 == 0) 처리값 = memori_Difaele.지우기(); if (처리값 < 0) Phošo(처리값); }
        }
        else if (같음(0, "echo")) {
            int 시작자리 = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = 시작자리; 첫값 < 토큰수; 첫값++) { if (첫값 > 시작자리) 단말.문자(32); for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < botelele_boleng[첫값]; ditaelopoeletšwa_lokela++) 보드.직렬쓰기(thokene_boleng[시작점[첫값] + ditaelopoeletšwa_lokela]); }
            if (시작자리 == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Ngwala("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? 파이썬꾸러미() : Ditholosi(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !šele_tatelanyotlhaka_tirišong.연결중) { 단말.Ngwala("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Ditholosi(13); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Ditholosi(15); 결과 = 처리값 < 0 ? 126 : 처리값; if (!šele_tatelanyotlhaka_tirišong.연결중) { 단말.Ngwala("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Ditholosi(16); 결과 = 처리값 < 0 ? 126 : 처리값; if (!šele_tatelanyotlhaka_tirišong.연결중) { 단말.Ngwala("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Bogolo = 보드.터미널(13); 단말.Ngwala("TERMINAL SIZE "); 단말.수(Bogolo & 65535); 단말.문자('x'); 단말.수(Bogolo >>> 16); 단말.문자(10); }
            else 터미널(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { 보드.터미널(9); teskethopo.phethagatša_taelo(); }
        else if (같음(0, "c")) khenele.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) khenele.작업시험();
        else if (같음(0, "g")) khenele.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) khenele.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = 보드.sepetša_mošomiši_tirišo(0); if (처리값 == 0) 단말.Ngwala("ELF DEMO PASS\n"); else Phošo(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? tholosi_go_tsenya_tshedimošo(-2, 2) : Ditholosi(-1); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !šele_tatelanyotlhaka_tirišong.연결중) { 단말.Ngwala("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) khenele.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = 보드.faele_fetišetša_tirelo(1); if (처리값 < 0) Phošo(처리값); else { 단말.Ngwala("FTP listening "); lenaneo_tholosi.ngwala_atrese(보드.Netweke_boemo(0,0)); 단말.Ngwala(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { 보드.faele_fetišetša_tirelo(0); 단말.Ngwala("FTP stopped\n"); }
            else 단말.Ngwala(보드.faele_fetišetša_tirelo(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { sehlopha.Lokišetša(); 단말.Ngwala("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Polelo = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (토큰수 != 2 || Polelo < 0) 단말.Ngwala("example java|c|python: 출력, Faele, 네트워크, 그래픽, Java Swing lefastere 예제\n");
            else { int 처리값 = 예제꾸러미.hloma_boleng(Polelo); if (처리값 < 0) { Phošo(처리값); if (처리값 == -28) 단말.Ngwala("RAM full: remove unused files, then retry example\n"); } else 단말.Ngwala("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int fomete_boleng = 실행형식();
            if (fomete_boleng == 1 || fomete_boleng == 2) {
                int 처리값 = tholosi_go_tsenya_tshedimošo(fomete_boleng == 1 ? -1 : 14, 0); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !šele_tatelanyotlhaka_tirišong.연결중) { 단말.Ngwala("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (fomete_boleng == 0) { 결과 = 126; 단말.Ngwala("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { 결과 = 127; 단말.Ngwala("Unknown command. help: commands\n"); }
        }
    }
    public static void phethagatša_taelo() {
        sehlopha.Lokišetša();
        for (int Polelo = 0; Polelo < 3; Polelo++) { int 처리값 = 예제꾸러미.hloma_boleng(Polelo); if (처리값 < 0) Phošo(처리값); }
        bontšha_thušo();
        while (true) {
            lefastere_nakotiragalo.tiragalo_boleng_go_tsenya_tshedimošo(); if (lefastere_nakotiragalo.재개()) continue;
            if (!lefastere_nakotiragalo.이어읽기) 단말.Ngwala("jkoros-native> "); mothaladi_Morulaganyi.mothalotlhako_wa_tirišo = true; 보드.원격대기(1); int Bogolo = 줄읽기(); 보드.원격대기(0); mothaladi_Morulaganyi.mothalotlhako_wa_tirišo = false;
            if (Bogolo == -3) continue;
            if (Bogolo == -2) 단말.Ngwala("Taelo ripaganya_boleng: 명령줄이 너무 깁니다\n");
            if (Bogolo >= 0) { šele_tatelanyotlhaka_tirišong.skripte_fetša = false; šele_tatelanyotlhaka_tirišong.phethagatša_taelo(mothaladi, 0, Bogolo, 0); } else šele_tatelanyotlhaka_tirišong.boemo_boleng = 130;
            보드.fetša_ya_kgole_taelo(šele_tatelanyotlhaka_tirišong.boemo_boleng);
            mothaladi_Morulaganyi.Bogolo = mothaladi_Morulaganyi.kheusa_boleng = mothaladi_Morulaganyi.Thomišo_lefastere = 0;
        }
    }
}
