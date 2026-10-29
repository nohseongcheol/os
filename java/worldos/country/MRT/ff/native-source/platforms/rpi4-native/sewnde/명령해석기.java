// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 ɓoggol_ginorde. 따옴표, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] diidol = new int[4096], 토큰 = new int[4096], 시작점 = new int[32], njuuteendi_njaru = new int[32];
    static int[] 편집내용 = new int[16384], feewnditde_innde = new int[63];
    static int 토큰수, feewnditde_innde_njuuteendi, 결과;
    static boolean 앞줄;
    static void 원바이트(int njaru) { 보드.직렬쓰기(njaru); }
    static int 줄읽기() { return diidol_feewnditirde.읽기(); }
    static boolean 나누기(int waylude_etannde) {
        int 위치 = 0, 끝 = 0; 토큰수 = 0;
        while (위치 < waylude_etannde) {
            while (위치 < waylude_etannde && (diidol[위치] == 32 || diidol[위치] == 9)) 위치++;
            if (위치 == waylude_etannde) break;
            if (토큰수 == 16) { 단말.winndude("ginol 해석: 인수가 너무 많습니다\n"); return false; }
            시작점[토큰수] = 끝; int 인용 = 0;
            while (위치 < waylude_etannde) {
                int njaru = diidol[위치++];
                if (인용 == 0 && (njaru == 32 || njaru == 9)) break;
                if (njaru == 인용) { 인용 = 0; continue; }
                if (인용 == 0 && (njaru == 39 || njaru == 34)) { 인용 = njaru; continue; }
                토큰[끝++] = njaru;
            }
            if (인용 != 0) { 단말.winndude("ginol 해석: 따옴표가 닫히지 않았습니다\n"); return false; }
            njuuteendi_njaru[토큰수] = 끝 - 시작점[토큰수]; 토큰수++;
        }
        return true;
    }
    static boolean 같음(int joopirdu, String 말) {
        if (joopirdu >= 토큰수) return false;
        int 자리=0;
        for (int 순번=0; 순번<말.length(); 순번++) {
            int 문자값=말.charAt(순번);
            if (문자값>=0xd800 && 문자값<=0xdbff && 순번+1<말.length()) 문자값=0x10000+((문자값-0xd800)<<10)+말.charAt(++순번)-0xdc00;
            int 바이트수=문자값<128?1:문자값<2048?2:문자값<65536?3:4;
            for (int 차례=바이트수-1; 차례>=0; 차례--) {
                int njaru=바이트수==1?문자값:차례==바이트수-1?(바이트수==2?0xc0:바이트수==3?0xe0:0xf0)|(문자값>>(6*차례)):0x80|((문자값>>(6*차례))&63);
                if (자리>=njuuteendi_njaru[joopirdu] || 토큰[시작점[joopirdu]+자리++]!=njaru) return false;
            }
        }
        return 자리==njuuteendi_njaru[joopirdu];
    }
    static int laawol(int joopirdu) {
        if (joopirdu >= 토큰수) return -22;
        int 결과 = 기억파일.laawol_huɓɓude(njuuteendi_njaru[joopirdu]); if (결과 < 0) return 결과;
        for (int kowal_joopirdu = 0; kowal_joopirdu < njuuteendi_njaru[joopirdu]; kowal_joopirdu++) {
            결과 = 기억파일.laawol_oktee(kowal_joopirdu, 토큰[시작점[joopirdu] + kowal_joopirdu]); if (결과 < 0) return 결과;
        }
        return 0;
    }
    static void juumre(int joopirdu) { 결과 = 1; 단말.winndude("juumre "); 단말.수(joopirdu); 단말.문자(10); }
    static void kollal_njaru() {
        if (토큰수 != 2) { 단말.winndude("사용법: cat fiilde\n"); return; }
        int 결과 = laawol(1); if (결과 < 0) { juumre(결과); return; }
        int fiilde = 기억파일.udditde(0); if (fiilde < 0) { juumre(fiilde); return; }
        while (true) { int njaru = 기억파일.읽기(fiilde); if (njaru == 256) break; if (njaru < 0) { juumre(njaru); break; } 원바이트(njaru); }
        기억파일.uddude(fiilde); 단말.문자(10);
    }
    static void feewnditde_njaru() {
        if (토큰수 != 2) { 단말.winndude("사용법: edit fiilde\n"); return; }
        int 결과 = laawol(1); if (결과 < 0) { juumre(결과); return; }
        feewnditde_innde_njuuteendi = njuuteendi_njaru[1];
        for (int kowal_joopirdu = 0; kowal_joopirdu < feewnditde_innde_njuuteendi; kowal_joopirdu++) feewnditde_innde[kowal_joopirdu] = 토큰[시작점[1] + kowal_joopirdu];
        단말.winndude("EDIT: fiilde 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int waylude_etannde = 0;
        while (true) {
            단말.winndude("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.winndude("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && diidol[0] == '.') break;
            if (입력 + 1 > 편집내용.length - waylude_etannde) { 단말.winndude("EDIT CANCELLED: file too large\n"); return; }
            for (int kowal_joopirdu = 0; kowal_joopirdu < 입력; kowal_joopirdu++) 편집내용[waylude_etannde++] = diidol[kowal_joopirdu];
            편집내용[waylude_etannde++] = 10;
        }
        기억파일.laawol_huɓɓude(feewnditde_innde_njuuteendi);
        for (int kowal_joopirdu = 0; kowal_joopirdu < feewnditde_innde_njuuteendi; kowal_joopirdu++) 기억파일.laawol_oktee(kowal_joopirdu, feewnditde_innde[kowal_joopirdu]);
        int fiilde = 기억파일.udditde(577); if (fiilde < 0) { juumre(fiilde); return; }
        for (int kowal_joopirdu = 0; kowal_joopirdu < waylude_etannde; kowal_joopirdu++) 기억파일.winndude(fiilde, 편집내용[kowal_joopirdu]);
        기억파일.uddude(fiilde); 단말.winndude("SAVED "); 단말.수(waylude_etannde); 단말.winndude("oktee_njaru(주기억 fiilde)\n");
    }
    static int 십육(int njaru) {
        if (njaru >= '0' && njaru <= '9') return njaru - '0';
        if (njaru >= 'a' && njaru <= 'f') return njaru - 'a' + 10;
        if (njaru >= 'A' && njaru <= 'F') return njaru - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (토큰수 != 2) { 단말.winndude("사용법: load fiilde | hex fiilde\n"); return; }
        int 결과 = laawol(1); if (결과 < 0) { juumre(결과); return; }
        if (!넣기) {
            int fiilde = 기억파일.udditde(0); if (fiilde < 0) { juumre(fiilde); return; }
            단말.winndude("HEX BEGIN "); 단말.수(기억파일.waylude_etannde(fiilde)); 단말.문자(10);
            int 항목수 = 0;
            while (true) {
                int njaru = 기억파일.읽기(fiilde); if (njaru < 0 || njaru == 256) break;
                단말.문자("0123456789abcdef".charAt(njaru >> 4)); 단말.문자("0123456789abcdef".charAt(njaru & 15));
                if (++항목수 % 32 == 0) 단말.문자(10);
            }
            if (항목수 % 32 != 0) 단말.문자(10);
            기억파일.uddude(fiilde); 단말.winndude("HEX END\n"); return;
        }
        feewnditde_innde_njuuteendi = njuuteendi_njaru[1];
        for (int kowal_joopirdu = 0; kowal_joopirdu < feewnditde_innde_njuuteendi; kowal_joopirdu++) feewnditde_innde[kowal_joopirdu] = 토큰[시작점[1] + kowal_joopirdu];
        단말.winndude("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int waylude_etannde = 0;
        while (true) {
            단말.winndude("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.winndude("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && diidol[0] == '.') break;
            int 앞 = -1;
            for (int kowal_joopirdu = 0; kowal_joopirdu < 입력; kowal_joopirdu++) {
                if (diidol[kowal_joopirdu] == 32 || diidol[kowal_joopirdu] == 9) continue;
                int njaru = 십육(diidol[kowal_joopirdu]);
                if (njaru < 0 || waylude_etannde >= 편집내용.length) { 단말.winndude("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = njaru; else { 편집내용[waylude_etannde++] = 앞 * 16 + njaru; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.winndude("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        기억파일.laawol_huɓɓude(feewnditde_innde_njuuteendi);
        for (int kowal_joopirdu = 0; kowal_joopirdu < feewnditde_innde_njuuteendi; kowal_joopirdu++) 기억파일.laawol_oktee(kowal_joopirdu, feewnditde_innde[kowal_joopirdu]);
        int fiilde = 기억파일.udditde(577); if (fiilde < 0) { juumre(fiilde); return; }
        for (int kowal_joopirdu = 0; kowal_joopirdu < waylude_etannde; kowal_joopirdu++) 기억파일.winndude(fiilde, 편집내용[kowal_joopirdu]);
        기억파일.uddude(fiilde); 단말.winndude("LOADED "); 단말.수(waylude_etannde); 단말.winndude("oktee_njaru(주기억 fiilde)\n");
    }
    static int 도구(int joopirdu) {
        return kuutorgal_naatnugol(joopirdu, 1);
    }
    static int kuutorgal_naatnugol(int joopirdu, int huutoraade) {
        if (토큰수 - huutoraade > 8) return -22;
        보드.인수준비(토큰수 - huutoraade);
        for (int 첫값 = huutoraade; 첫값 < 토큰수; 첫값++) {
            if (njuuteendi_njaru[첫값] > 255) return -36;
            for (int kowal_joopirdu = 0; kowal_joopirdu < njuuteendi_njaru[첫값]; kowal_joopirdu++) 보드.hujja_oktee(첫값 - huutoraade, kowal_joopirdu, 토큰[시작점[첫값] + kowal_joopirdu]);
        }
        return joopirdu == -2 ? 보드.리눅스파일실행() : joopirdu < 0 ? 보드.사용자파일실행() : 보드.huutoraade_kuutoro_tafirde(joopirdu);
    }
    static int 파이썬꾸러미() {
        if (토큰수 > 8) return -22;
        보드.인수준비(토큰수);
        String laawol = "/lib/꾸러미.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int 자리 = 0;
        for (int 순번 = 0; 순번 < laawol.length(); 순번++) {
            int alkulal_njaru = laawol.charAt(순번);
            if (alkulal_njaru < 128) 보드.hujja_oktee(0, 자리++, alkulal_njaru);
            else { 보드.hujja_oktee(0, 자리++, 0xe0 | (alkulal_njaru >> 12)); 보드.hujja_oktee(0, 자리++, 0x80 | ((alkulal_njaru >> 6) & 63)); 보드.hujja_oktee(0, 자리++, 0x80 | (alkulal_njaru & 63)); }
        }
        for (int 순번 = 1; 순번 < 토큰수; 순번++) {
            if (njuuteendi_njaru[순번] > 255) return -36;
            for (int alkulal_njaru = 0; alkulal_njaru < njuuteendi_njaru[순번]; alkulal_njaru++) 보드.hujja_oktee(순번, alkulal_njaru, 토큰[시작점[순번] + alkulal_njaru]);
        }
        return 보드.huutoraade_kuutoro_tafirde(12);
    }
    static int 실행형식() {
        int 처리값 = laawol(0); if (처리값 < 0) return 처리값;
        int fiilde = 기억파일.udditde(0); if (fiilde < 0) return fiilde;
        int 첫값 = 기억파일.읽기(fiilde), oktee_keɓe = 기억파일.읽기(fiilde), 문자값 = 기억파일.읽기(fiilde), 뒷값 = 기억파일.읽기(fiilde);
        기억파일.uddude(fiilde);
        if (첫값 == 127 && oktee_keɓe == 'E' && 문자값 == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && oktee_keɓe == 'K' && 문자값 == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int joopirdu, String 인수) {
        보드.인수준비(1);
        for (int kowal_joopirdu = 0; kowal_joopirdu < 인수.length(); kowal_joopirdu++) 보드.hujja_oktee(0, kowal_joopirdu, 인수.charAt(kowal_joopirdu));
        return 보드.huutoraade_kuutoro_tafirde(joopirdu);
    }
    static void binndi_oktee(int fiilde, int njaru) { 기억파일.winndude(fiilde, njaru); }
    static void ñiiɓ_fiilde(String innde, String loowdi_njaru) {
        // 꾸러미 파일명은 ASCII. fiilde 내용은 UTF-8로 저장한다.
        기억파일.laawol_huɓɓude(innde.length());
        for (int kowal_joopirdu = 0; kowal_joopirdu < innde.length(); kowal_joopirdu++) 기억파일.laawol_oktee(kowal_joopirdu, innde.charAt(kowal_joopirdu));
        int fiilde = 기억파일.udditde(193); if (fiilde < 0) return;
        for (int kowal_joopirdu = 0; kowal_joopirdu < loowdi_njaru.length(); kowal_joopirdu++) {
            int 문자값 = loowdi_njaru.charAt(kowal_joopirdu);
            if (문자값 >= 0xd800 && 문자값 <= 0xdbff && kowal_joopirdu + 1 < loowdi_njaru.length()) 문자값 = 0x10000 + ((문자값 - 0xd800) << 10) + loowdi_njaru.charAt(++kowal_joopirdu) - 0xdc00;
            if (문자값 < 128) binndi_oktee(fiilde, 문자값);
            else {
                int 수 = 문자값 < 2048 ? 2 : 문자값 < 65536 ? 3 : 4;
                binndi_oktee(fiilde, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (문자값 >> (6 * (수 - 1))));
                for (int 항목수 = 수 - 1; 항목수 > 0; 항목수--) binndi_oktee(fiilde, 0x80 | ((문자값 >> (6 * (항목수 - 1))) & 63));
            }
        }
        기억파일.uddude(fiilde);
    }
    static void 한글도움말() {
        단말.winndude("F9 / Shift+Space: [EN] ↔ [ff]\n");
        단말.winndude("  [FF] keyboard; [EN] ASCII\n");
        단말.winndude("  a → a\n");
        단말.winndude("  F9: EN ↔ ff | Ctrl+Shift+V: UTF-8\n");
        단말.winndude("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.winndude("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String innde) {
        int 바이트수 = 0;
        for (int kowal_joopirdu = 0; kowal_joopirdu < innde.length(); kowal_joopirdu++) { int 문자값 = innde.charAt(kowal_joopirdu); if (문자값 >= 0xd800 && 문자값 <= 0xdfff) return -22; 바이트수 += 문자값 < 128 ? 1 : 문자값 < 2048 ? 2 : 3; }
        int 처리값 = 기억파일.laawol_huɓɓude(바이트수); if (처리값 < 0) return 처리값;
        int 자리 = 0;
        for (int kowal_joopirdu = 0; kowal_joopirdu < innde.length(); kowal_joopirdu++) {
            int 문자값 = innde.charAt(kowal_joopirdu);
            if (문자값 < 128) 기억파일.laawol_oktee(자리++, 문자값);
            else if (문자값 < 2048) { 기억파일.laawol_oktee(자리++, 0xc0 | (문자값 >> 6)); 기억파일.laawol_oktee(자리++, 0x80 | (문자값 & 63)); }
            else { 기억파일.laawol_oktee(자리++, 0xe0 | (문자값 >> 12)); 기억파일.laawol_oktee(자리++, 0x80 | ((문자값 >> 6) & 63)); 기억파일.laawol_oktee(자리++, 0x80 | (문자값 & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String innde) {
        int 처리값 = 예제경로(innde); if (처리값 < 0) return 처리값;
        처리값 = 기억파일.폴더만들기(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String innde, String keɓe) {
        int 처리값 = 예제경로(innde); if (처리값 < 0) return 처리값;
        int fiilde = 기억파일.udditde(193); if (fiilde == -17) return 0; if (fiilde < 0) return fiilde;
        for (int kowal_joopirdu = 0; kowal_joopirdu < keɓe.length(); kowal_joopirdu += 2) {
            처리값 = 기억파일.winndude(fiilde, 십육(keɓe.charAt(kowal_joopirdu)) * 16 + 십육(keɓe.charAt(kowal_joopirdu + 1)));
            if (처리값 < 0) { 기억파일.uddude(fiilde); return 처리값; }
        }
        return 기억파일.uddude(fiilde);
    }
    static void hollirde_ballal() {
        yuɓɓo_kuutorgal.hollirde_ballal();
        단말.winndude("sshd / 보안셸 start|stop|status: SSH :22 (user, 장치별 finnde_njaru)\n");
        단말.winndude("vncd / 원격화면 start|stop|status: VNC :5900 (장치별 finnde_njaru)\n");
        단말.winndude("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.winndude("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.winndude("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.winndude("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.winndude("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.winndude("모서리 + 왼쪽 버튼 daasde_njaru: 터미널 waylude_etannde waklude_njaru; terminal size: darol_njaru/winndande_njaru\n");
        단말.winndude("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.winndude("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.winndude("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.winndude("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.winndude("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.winndude("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.winndude("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.winndude("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.winndude("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.winndude("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.winndude("pip: MicroPython sewnde_lekki diiñde_njaru; njaatigi --network --pip 필요; /lib는 RAM\n");
        단말.winndude("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.winndude("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.winndude("/example/java /example/c /example/python: examples ready at boot\n");
        단말.winndude("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void 터미널(boolean 전환여부) {
        if (전환여부 && 보드.터미널(2) != 0) { 보드.터미널(0); 단말.winndude("TERMINAL CLOSED\n"); }
        else if (보드.터미널(1) < 0) juumre(-19);
        else 단말.winndude("TERMINAL READY — ff terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void ginol() {
        if (토큰수 == 0) return;
        if (yuɓɓo_kuutorgal.실행()) return;
        if (같음(0,"sshd") || 같음(0,"보안셸") || 같음(0,"vncd") || 같음(0,"원격화면")) {
            int 종류=같음(0,"vncd")||같음(0,"원격화면")?1:0;
            int gollal=같음(1,"start")||같음(1,"huutoraade")?1:같음(1,"stop")||같음(1,"dartinde")?0:2;
            int ngonka_njaru=보드.원격제어(종류,gollal);
            if(ngonka_njaru<0)juumre(ngonka_njaru);else 단말.winndude(보드.원격제어(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else hollirde_ballal(); }
        else if (같음(0, "info") || 같음(0, "i")) aaluude.msinfo32_exe();
        else if (같음(0, "pwd")) { 기억파일.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (토큰수 == 1) { 기억파일.laawol_huɓɓude(1); 처리값 = 기억파일.laawol_oktee(0, '/'); } else 처리값 = 토큰수 == 2 ? laawol(1) : -22;
            if (처리값 >= 0) 처리값 = 기억파일.waklude_mooftordu(); if (처리값 < 0) juumre(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int hujja_joopirdu = 같음(1, "-l") ? 2 : 1, 처리값;
            if (토큰수 == hujja_joopirdu) { 기억파일.laawol_huɓɓude(1); 처리값 = 기억파일.laawol_oktee(0, '.'); } else 처리값 = 토큰수 == hujja_joopirdu + 1 ? laawol(hujja_joopirdu) : -22;
            if (처리값 >= 0) 처리값 = 기억파일.경로목록(); if (처리값 < 0) juumre(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) 셸도구.fiilde_haaju(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) 셸도구.waanjitaade_njaru(같음(0, "mv"));
        else if (같음(0, "cat")) 셸도구.kollal_njaru();
        else if (같음(0, "wc")) 셸도구.세기();
        else if (같음(0, "grep")) 셸도구.yiylaade_naatnugol();
        else if (같음(0, "head") || 같음(0, "tail")) 셸도구.머리(같음(0, "tail"));
        else if (같음(0, "tee")) 셸도구.함께쓰기();
        else if (같음(0, "env")) 셸문법.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (토큰수 == 1) 셸문법.환경보기();
            for (int kowal_joopirdu = 1; kowal_joopirdu < 토큰수; kowal_joopirdu++) { int 처리값 = 셸문법.환경설정(kowal_joopirdu, 같음(0, "unset")); if (처리값 != 0) { 결과 = 처리값; 단말.winndude("ginol 해석: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) 셸문법.파일실행();
        else if (같음(0, "true")) 결과 = 0;
        else if (같음(0, "false")) 결과 = 1;
        else if (같음(0, "history")) diidol_feewnditirde.hollirde_suurnal();
        else if (같음(0, "exit")) {
            if (셸문법.깊이 > 0) { 결과 = 토큰수 == 1 ? 셸문법.ngonka_njaru : 셸도구.숫자(1); if (결과 < 0 || 결과 > 255) 결과 = 2; 셸문법.eskript_taƴde = true; }
            else if (보드.터미널(2) != 0) 터미널(true);
            else 단말.winndude("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) feewnditde_njaru();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (토큰수 < 2) { 결과 = 2; 단말.winndude("사용법: rm fiilde...\n"); }
            for (int kowal_joopirdu = 1; kowal_joopirdu < 토큰수; kowal_joopirdu++) { int 처리값 = laawol(kowal_joopirdu); if (처리값 == 0) 처리값 = 기억파일.지우기(); if (처리값 < 0) juumre(처리값); }
        }
        else if (같음(0, "echo")) {
            int 시작자리 = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = 시작자리; 첫값 < 토큰수; 첫값++) { if (첫값 > 시작자리) 단말.문자(32); for (int kowal_joopirdu = 0; kowal_joopirdu < njuuteendi_njaru[첫값]; kowal_joopirdu++) 보드.직렬쓰기(토큰[시작점[첫값] + kowal_joopirdu]); }
            if (시작자리 == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.winndude("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? 파이썬꾸러미() : 도구(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !셸문법.연결중) { 단말.winndude("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = 도구(13); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = 도구(15); 결과 = 처리값 < 0 ? 126 : 처리값; if (!셸문법.연결중) { 단말.winndude("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = 도구(16); 결과 = 처리값 < 0 ? 126 : 처리값; if (!셸문법.연결중) { 단말.winndude("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int waylude_etannde = 보드.터미널(13); 단말.winndude("TERMINAL SIZE "); 단말.수(waylude_etannde & 65535); 단말.문자('x'); 단말.수(waylude_etannde >>> 16); 단말.문자(10); }
            else 터미널(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { 보드.터미널(9); biro.실행(); }
        else if (같음(0, "c")) aaluude.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) aaluude.작업시험();
        else if (같음(0, "g")) aaluude.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) aaluude.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = 보드.huutoraade_kuutoro_tafirde(0); if (처리값 == 0) 단말.winndude("ELF DEMO PASS\n"); else juumre(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? kuutorgal_naatnugol(-2, 2) : 도구(-1); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !셸문법.연결중) { 단말.winndude("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) aaluude.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = 보드.fiilde_egginde_carwol(1); if (처리값 < 0) juumre(처리값); else { 단말.winndude("FTP listening "); yuɓɓo_kuutorgal.winndude_ñiiɓirde(보드.laylaytol_ngonka(0,0)); 단말.winndude(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { 보드.fiilde_egginde_carwol(0); 단말.winndude("FTP stopped\n"); }
            else 단말.winndude(보드.fiilde_egginde_carwol(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { 꾸러미.Heblu(); 단말.winndude("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int 언어 = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (토큰수 != 2 || 언어 < 0) 단말.winndude("example java|c|python: 출력, fiilde, 네트워크, 그래픽, Java Swing falanteere 예제\n");
            else { int 처리값 = 예제꾸러미.diiñde_njaru(언어); if (처리값 < 0) { juumre(처리값); if (처리값 == -28) 단말.winndude("RAM full: remove unused files, then retry example\n"); } else 단말.winndude("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int formaa_njaru = 실행형식();
            if (formaa_njaru == 1 || formaa_njaru == 2) {
                int 처리값 = kuutorgal_naatnugol(formaa_njaru == 1 ? -1 : 14, 0); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !셸문법.연결중) { 단말.winndude("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (formaa_njaru == 0) { 결과 = 126; 단말.winndude("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { 결과 = 127; 단말.winndude("Unknown command. help: commands\n"); }
        }
    }
    public static void 실행() {
        꾸러미.Heblu();
        for (int 언어 = 0; 언어 < 3; 언어++) { int 처리값 = 예제꾸러미.diiñde_njaru(언어); if (처리값 < 0) juumre(처리값); }
        hollirde_ballal();
        while (true) {
            falanteere_jokkondiral.Yuɓɓo_golle_njaru_naatnugol(); if (falanteere_jokkondiral.재개()) continue;
            if (!falanteere_jokkondiral.이어읽기) 단말.winndude("jkoros-native> "); diidol_feewnditirde.ɓoggol_ginorde = true; 보드.원격대기(1); int waylude_etannde = 줄읽기(); 보드.원격대기(0); diidol_feewnditirde.ɓoggol_ginorde = false;
            if (waylude_etannde == -3) continue;
            if (waylude_etannde == -2) 단말.winndude("ginol 해석: 명령줄이 너무 깁니다\n");
            if (waylude_etannde >= 0) { 셸문법.eskript_taƴde = false; 셸문법.실행(diidol, 0, waylude_etannde, 0); } else 셸문법.ngonka_njaru = 130;
            보드.원격명령끝(셸문법.ngonka_njaru);
            diidol_feewnditirde.waylude_etannde = diidol_feewnditirde.kirseer_njaru = diidol_feewnditirde.huɓɓude_falanteere = 0;
        }
    }
}
