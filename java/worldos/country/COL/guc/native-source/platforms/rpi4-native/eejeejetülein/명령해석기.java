// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 liinia_aluwataayapala. 따옴표, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] liinia = new int[4096], 토큰 = new int[4096], 시작점 = new int[32], akaliaa_ajutuu = new int[32];
    static int[] 편집내용 = new int[16384], 편집이름 = new int[63];
    static int 토큰수, 편집이름길이, 결과;
    static boolean 앞줄;
    static void 원바이트(int ajutuu) { 보드.직렬쓰기(ajutuu); }
    static int 줄읽기() { return liinia_anaatülü.읽기(); }
    static boolean 나누기(int 크기) {
        int 위치 = 0, 끝 = 0; 토큰수 = 0;
        while (위치 < 크기) {
            while (위치 < 크기 && (liinia[위치] == 32 || liinia[위치] == 9)) 위치++;
            if (위치 == 크기) break;
            if (토큰수 == 16) { 단말.ashajaa("aluwataaya akatajaa_ajutuu: 인수가 너무 많습니다\n"); return false; }
            시작점[토큰수] = 끝; int 인용 = 0;
            while (위치 < 크기) {
                int ajutuu = liinia[위치++];
                if (인용 == 0 && (ajutuu == 32 || ajutuu == 9)) break;
                if (ajutuu == 인용) { 인용 = 0; continue; }
                if (인용 == 0 && (ajutuu == 39 || ajutuu == 34)) { 인용 = ajutuu; continue; }
                토큰[끝++] = ajutuu;
            }
            if (인용 != 0) { 단말.ashajaa("aluwataaya akatajaa_ajutuu: 따옴표가 닫히지 않았습니다\n"); return false; }
            akaliaa_ajutuu[토큰수] = 끝 - 시작점[토큰수]; 토큰수++;
        }
        return true;
    }
    static boolean 같음(int ee_iyatialujuna, String 말) {
        if (ee_iyatialujuna >= 토큰수) return false;
        int 자리=0;
        for (int 순번=0; 순번<말.length(); 순번++) {
            int 문자값=말.charAt(순번);
            if (문자값>=0xd800 && 문자값<=0xdbff && 순번+1<말.length()) 문자값=0x10000+((문자값-0xd800)<<10)+말.charAt(++순번)-0xdc00;
            int 바이트수=문자값<128?1:문자값<2048?2:문자값<65536?3:4;
            for (int 차례=바이트수-1; 차례>=0; 차례--) {
                int ajutuu=바이트수==1?문자값:차례==바이트수-1?(바이트수==2?0xc0:바이트수==3?0xe0:0xf0)|(문자값>>(6*차례)):0x80|((문자값>>(6*차례))&63);
                if (자리>=akaliaa_ajutuu[ee_iyatialujuna] || 토큰[시작점[ee_iyatialujuna]+자리++]!=ajutuu) return false;
            }
        }
        return 자리==akaliaa_ajutuu[ee_iyatialujuna];
    }
    static int wopu_a_ttaaleemüin(int ee_iyatialujuna) {
        if (ee_iyatialujuna >= 토큰수) return -22;
        int 결과 = 기억파일.wopu_a_ttaaleemüin_achuwalaa(akaliaa_ajutuu[ee_iyatialujuna]); if (결과 < 0) return 결과;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < akaliaa_ajutuu[ee_iyatialujuna]; eitawaakualü_ee_iyatialujuna++) {
            결과 = 기억파일.wopu_a_ttaaleemüin_waai(eitawaakualü_ee_iyatialujuna, 토큰[시작점[ee_iyatialujuna] + eitawaakualü_ee_iyatialujuna]); if (결과 < 0) return 결과;
        }
        return 0;
    }
    static void ajachitia(int ee_iyatialujuna) { 결과 = 1; 단말.ashajaa("ajachitia "); 단말.수(ee_iyatialujuna); 단말.문자(10); }
    static void e_rajaa_ajutuu() {
        if (토큰수 != 2) { 단말.ashajaa("사용법: cat anaajaalaa\n"); return; }
        int 결과 = wopu_a_ttaaleemüin(1); if (결과 < 0) { ajachitia(결과); return; }
        int anaajaalaa = 기억파일.열기(0); if (anaajaalaa < 0) { ajachitia(anaajaalaa); return; }
        while (true) { int ajutuu = 기억파일.읽기(anaajaalaa); if (ajutuu == 256) break; if (ajutuu < 0) { ajachitia(ajutuu); break; } 원바이트(ajutuu); }
        기억파일.asürülaa(anaajaalaa); 단말.문자(10);
    }
    static void anaataa_ajutuu() {
        if (토큰수 != 2) { 단말.ashajaa("사용법: edit anaajaalaa\n"); return; }
        int 결과 = wopu_a_ttaaleemüin(1); if (결과 < 0) { ajachitia(결과); return; }
        편집이름길이 = akaliaa_ajutuu[1];
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 편집이름길이; eitawaakualü_ee_iyatialujuna++) 편집이름[eitawaakualü_ee_iyatialujuna] = 토큰[시작점[1] + eitawaakualü_ee_iyatialujuna];
        단말.ashajaa("EDIT: anaajaalaa 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int 크기 = 0;
        while (true) {
            단말.ashajaa("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.ashajaa("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && liinia[0] == '.') break;
            if (입력 + 1 > 편집내용.length - 크기) { 단말.ashajaa("EDIT CANCELLED: file too large\n"); return; }
            for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 입력; eitawaakualü_ee_iyatialujuna++) 편집내용[크기++] = liinia[eitawaakualü_ee_iyatialujuna];
            편집내용[크기++] = 10;
        }
        기억파일.wopu_a_ttaaleemüin_achuwalaa(편집이름길이);
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 편집이름길이; eitawaakualü_ee_iyatialujuna++) 기억파일.wopu_a_ttaaleemüin_waai(eitawaakualü_ee_iyatialujuna, 편집이름[eitawaakualü_ee_iyatialujuna]);
        int anaajaalaa = 기억파일.열기(577); if (anaajaalaa < 0) { ajachitia(anaajaalaa); return; }
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 크기; eitawaakualü_ee_iyatialujuna++) 기억파일.ashajaa(anaajaalaa, 편집내용[eitawaakualü_ee_iyatialujuna]);
        기억파일.asürülaa(anaajaalaa); 단말.ashajaa("SAVED "); 단말.수(크기); 단말.ashajaa("waai_ajutuu(주기억 anaajaalaa)\n");
    }
    static int 십육(int ajutuu) {
        if (ajutuu >= '0' && ajutuu <= '9') return ajutuu - '0';
        if (ajutuu >= 'a' && ajutuu <= 'f') return ajutuu - 'a' + 10;
        if (ajutuu >= 'A' && ajutuu <= 'F') return ajutuu - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (토큰수 != 2) { 단말.ashajaa("사용법: load anaajaalaa | hex anaajaalaa\n"); return; }
        int 결과 = wopu_a_ttaaleemüin(1); if (결과 < 0) { ajachitia(결과); return; }
        if (!넣기) {
            int anaajaalaa = 기억파일.열기(0); if (anaajaalaa < 0) { ajachitia(anaajaalaa); return; }
            단말.ashajaa("HEX BEGIN "); 단말.수(기억파일.크기(anaajaalaa)); 단말.문자(10);
            int 항목수 = 0;
            while (true) {
                int ajutuu = 기억파일.읽기(anaajaalaa); if (ajutuu < 0 || ajutuu == 256) break;
                단말.문자("0123456789abcdef".charAt(ajutuu >> 4)); 단말.문자("0123456789abcdef".charAt(ajutuu & 15));
                if (++항목수 % 32 == 0) 단말.문자(10);
            }
            if (항목수 % 32 != 0) 단말.문자(10);
            기억파일.asürülaa(anaajaalaa); 단말.ashajaa("HEX END\n"); return;
        }
        편집이름길이 = akaliaa_ajutuu[1];
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 편집이름길이; eitawaakualü_ee_iyatialujuna++) 편집이름[eitawaakualü_ee_iyatialujuna] = 토큰[시작점[1] + eitawaakualü_ee_iyatialujuna];
        단말.ashajaa("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int 크기 = 0;
        while (true) {
            단말.ashajaa("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.ashajaa("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && liinia[0] == '.') break;
            int 앞 = -1;
            for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 입력; eitawaakualü_ee_iyatialujuna++) {
                if (liinia[eitawaakualü_ee_iyatialujuna] == 32 || liinia[eitawaakualü_ee_iyatialujuna] == 9) continue;
                int ajutuu = 십육(liinia[eitawaakualü_ee_iyatialujuna]);
                if (ajutuu < 0 || 크기 >= 편집내용.length) { 단말.ashajaa("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = ajutuu; else { 편집내용[크기++] = 앞 * 16 + ajutuu; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.ashajaa("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        기억파일.wopu_a_ttaaleemüin_achuwalaa(편집이름길이);
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 편집이름길이; eitawaakualü_ee_iyatialujuna++) 기억파일.wopu_a_ttaaleemüin_waai(eitawaakualü_ee_iyatialujuna, 편집이름[eitawaakualü_ee_iyatialujuna]);
        int anaajaalaa = 기억파일.열기(577); if (anaajaalaa < 0) { ajachitia(anaajaalaa); return; }
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 크기; eitawaakualü_ee_iyatialujuna++) 기억파일.ashajaa(anaajaalaa, 편집내용[eitawaakualü_ee_iyatialujuna]);
        기억파일.asürülaa(anaajaalaa); 단말.ashajaa("LOADED "); 단말.수(크기); 단말.ashajaa("waai_ajutuu(주기억 anaajaalaa)\n");
    }
    static int 도구(int ee_iyatialujuna) {
        return a_yataaya_ekeroliaa(ee_iyatialujuna, 1);
    }
    static int a_yataaya_ekeroliaa(int ee_iyatialujuna, int 시작) {
        if (토큰수 - 시작 > 8) return -22;
        보드.인수준비(토큰수 - 시작);
        for (int 첫값 = 시작; 첫값 < 토큰수; 첫값++) {
            if (akaliaa_ajutuu[첫값] > 255) return -36;
            for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < akaliaa_ajutuu[첫값]; eitawaakualü_ee_iyatialujuna++) 보드.ajutuu_waai(첫값 - 시작, eitawaakualü_ee_iyatialujuna, 토큰[시작점[첫값] + eitawaakualü_ee_iyatialujuna]);
        }
        return ee_iyatialujuna == -2 ? 보드.리눅스파일실행() : ee_iyatialujuna < 0 ? 보드.사용자파일실행() : 보드.사용자실행(ee_iyatialujuna);
    }
    static int 파이썬꾸러미() {
        if (토큰수 > 8) return -22;
        보드.인수준비(토큰수);
        String wopu_a_ttaaleemüin = "/lib/꾸러미.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int 자리 = 0;
        for (int 순번 = 0; 순번 < wopu_a_ttaaleemüin.length(); 순번++) {
            int jeerü_ajutuu = wopu_a_ttaaleemüin.charAt(순번);
            if (jeerü_ajutuu < 128) 보드.ajutuu_waai(0, 자리++, jeerü_ajutuu);
            else { 보드.ajutuu_waai(0, 자리++, 0xe0 | (jeerü_ajutuu >> 12)); 보드.ajutuu_waai(0, 자리++, 0x80 | ((jeerü_ajutuu >> 6) & 63)); 보드.ajutuu_waai(0, 자리++, 0x80 | (jeerü_ajutuu & 63)); }
        }
        for (int 순번 = 1; 순번 < 토큰수; 순번++) {
            if (akaliaa_ajutuu[순번] > 255) return -36;
            for (int jeerü_ajutuu = 0; jeerü_ajutuu < akaliaa_ajutuu[순번]; jeerü_ajutuu++) 보드.ajutuu_waai(순번, jeerü_ajutuu, 토큰[시작점[순번] + jeerü_ajutuu]);
        }
        return 보드.사용자실행(12);
    }
    static int 실행형식() {
        int 처리값 = wopu_a_ttaaleemüin(0); if (처리값 < 0) return 처리값;
        int anaajaalaa = 기억파일.열기(0); if (anaajaalaa < 0) return anaajaalaa;
        int 첫값 = 기억파일.읽기(anaajaalaa), waai_atijaaya = 기억파일.읽기(anaajaalaa), 문자값 = 기억파일.읽기(anaajaalaa), 뒷값 = 기억파일.읽기(anaajaalaa);
        기억파일.asürülaa(anaajaalaa);
        if (첫값 == 127 && waai_atijaaya == 'E' && 문자값 == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && waai_atijaaya == 'K' && 문자값 == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int ee_iyatialujuna, String 인수) {
        보드.인수준비(1);
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 인수.length(); eitawaakualü_ee_iyatialujuna++) 보드.ajutuu_waai(0, eitawaakualü_ee_iyatialujuna, 인수.charAt(eitawaakualü_ee_iyatialujuna));
        return 보드.사용자실행(ee_iyatialujuna);
    }
    static void 글바이트(int anaajaalaa, int ajutuu) { 기억파일.ashajaa(anaajaalaa, ajutuu); }
    static void jimatüsü_anaajaalaa(String 이름, String alu_ujatüü_ajutuu) {
        // 꾸러미 파일명은 ASCII. anaajaalaa 내용은 UTF-8로 저장한다.
        기억파일.wopu_a_ttaaleemüin_achuwalaa(이름.length());
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 이름.length(); eitawaakualü_ee_iyatialujuna++) 기억파일.wopu_a_ttaaleemüin_waai(eitawaakualü_ee_iyatialujuna, 이름.charAt(eitawaakualü_ee_iyatialujuna));
        int anaajaalaa = 기억파일.열기(193); if (anaajaalaa < 0) return;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < alu_ujatüü_ajutuu.length(); eitawaakualü_ee_iyatialujuna++) {
            int 문자값 = alu_ujatüü_ajutuu.charAt(eitawaakualü_ee_iyatialujuna);
            if (문자값 >= 0xd800 && 문자값 <= 0xdbff && eitawaakualü_ee_iyatialujuna + 1 < alu_ujatüü_ajutuu.length()) 문자값 = 0x10000 + ((문자값 - 0xd800) << 10) + alu_ujatüü_ajutuu.charAt(++eitawaakualü_ee_iyatialujuna) - 0xdc00;
            if (문자값 < 128) 글바이트(anaajaalaa, 문자값);
            else {
                int 수 = 문자값 < 2048 ? 2 : 문자값 < 65536 ? 3 : 4;
                글바이트(anaajaalaa, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (문자값 >> (6 * (수 - 1))));
                for (int 항목수 = 수 - 1; 항목수 > 0; 항목수--) 글바이트(anaajaalaa, 0x80 | ((문자값 >> (6 * (항목수 - 1))) & 63));
            }
        }
        기억파일.asürülaa(anaajaalaa);
    }
    static void 한글도움말() {
        단말.ashajaa("F9 / Shift+Space: [EN] ↔ [guc]\n");
        단말.ashajaa("  [GUC] keyboard; [EN] ASCII\n");
        단말.ashajaa("  a → a\n");
        단말.ashajaa("  F9: EN ↔ guc | Ctrl+Shift+V: UTF-8\n");
        단말.ashajaa("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.ashajaa("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String 이름) {
        int 바이트수 = 0;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 이름.length(); eitawaakualü_ee_iyatialujuna++) { int 문자값 = 이름.charAt(eitawaakualü_ee_iyatialujuna); if (문자값 >= 0xd800 && 문자값 <= 0xdfff) return -22; 바이트수 += 문자값 < 128 ? 1 : 문자값 < 2048 ? 2 : 3; }
        int 처리값 = 기억파일.wopu_a_ttaaleemüin_achuwalaa(바이트수); if (처리값 < 0) return 처리값;
        int 자리 = 0;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 이름.length(); eitawaakualü_ee_iyatialujuna++) {
            int 문자값 = 이름.charAt(eitawaakualü_ee_iyatialujuna);
            if (문자값 < 128) 기억파일.wopu_a_ttaaleemüin_waai(자리++, 문자값);
            else if (문자값 < 2048) { 기억파일.wopu_a_ttaaleemüin_waai(자리++, 0xc0 | (문자값 >> 6)); 기억파일.wopu_a_ttaaleemüin_waai(자리++, 0x80 | (문자값 & 63)); }
            else { 기억파일.wopu_a_ttaaleemüin_waai(자리++, 0xe0 | (문자값 >> 12)); 기억파일.wopu_a_ttaaleemüin_waai(자리++, 0x80 | ((문자값 >> 6) & 63)); 기억파일.wopu_a_ttaaleemüin_waai(자리++, 0x80 | (문자값 & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String 이름) {
        int 처리값 = 예제경로(이름); if (처리값 < 0) return 처리값;
        처리값 = 기억파일.폴더만들기(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String 이름, String atijaaya) {
        int 처리값 = 예제경로(이름); if (처리값 < 0) return 처리값;
        int anaajaalaa = 기억파일.열기(193); if (anaajaalaa == -17) return 0; if (anaajaalaa < 0) return anaajaalaa;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < atijaaya.length(); eitawaakualü_ee_iyatialujuna += 2) {
            처리값 = 기억파일.ashajaa(anaajaalaa, 십육(atijaaya.charAt(eitawaakualü_ee_iyatialujuna)) * 16 + 십육(atijaaya.charAt(eitawaakualü_ee_iyatialujuna + 1)));
            if (처리값 < 0) { 기억파일.asürülaa(anaajaalaa); return 처리값; }
        }
        return 기억파일.asürülaa(anaajaalaa);
    }
    static void 도움말() {
        a_yatawaajiraaya_a_yataaya.도움말();
        단말.ashajaa("sshd / 보안셸 start|stop|status: SSH :22 (user, 장치별 amoutia_ajutuu)\n");
        단말.ashajaa("vncd / 원격화면 start|stop|status: VNC :5900 (장치별 amoutia_ajutuu)\n");
        단말.ashajaa("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.ashajaa("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.ashajaa("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.ashajaa("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.ashajaa("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.ashajaa("모서리 + 왼쪽 버튼 ajarattaa_ajutuu: 터미널 크기 변경; terminal size: sha_washa_watüsü_ajutuu/aparatsee_ajutuu\n");
        단말.ashajaa("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.ashajaa("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.ashajaa("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.ashajaa("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.ashajaa("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.ashajaa("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.ashajaa("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.ashajaa("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.ashajaa("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.ashajaa("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.ashajaa("pip: MicroPython eejeejetülein_wunu_ulia e_itawaa_ajutuu; epiajatü --network --pip 필요; /lib는 RAM\n");
        단말.ashajaa("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.ashajaa("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.ashajaa("/example/java /example/c /example/python: examples ready at boot\n");
        단말.ashajaa("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void 터미널(boolean 전환여부) {
        if (전환여부 && 보드.터미널(2) != 0) { 보드.터미널(0); 단말.ashajaa("TERMINAL CLOSED\n"); }
        else if (보드.터미널(1) < 0) ajachitia(-19);
        else 단말.ashajaa("TERMINAL READY — guc terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void aluwataaya() {
        if (토큰수 == 0) return;
        if (a_yatawaajiraaya_a_yataaya.실행()) return;
        if (같음(0,"sshd") || 같음(0,"보안셸") || 같음(0,"vncd") || 같음(0,"원격화면")) {
            int 종류=같음(0,"vncd")||같음(0,"원격화면")?1:0;
            int aa_inra_awai=같음(1,"start")||같음(1,"시작")?1:같음(1,"stop")||같음(1,"eimale_eraa")?0:2;
            int jamakua_iparülein_ajutuu=보드.원격제어(종류,aa_inra_awai);
            if(jamakua_iparülein_ajutuu<0)ajachitia(jamakua_iparülein_ajutuu);else 단말.ashajaa(보드.원격제어(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else 도움말(); }
        else if (같음(0, "info") || 같음(0, "i")) keetnerü.정보();
        else if (같음(0, "pwd")) { 기억파일.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (토큰수 == 1) { 기억파일.wopu_a_ttaaleemüin_achuwalaa(1); 처리값 = 기억파일.wopu_a_ttaaleemüin_waai(0, '/'); } else 처리값 = 토큰수 == 2 ? wopu_a_ttaaleemüin(1) : -22;
            if (처리값 >= 0) 처리값 = 기억파일.폴더이동(); if (처리값 < 0) ajachitia(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int ajutuu_ee_iyatialujuna = 같음(1, "-l") ? 2 : 1, 처리값;
            if (토큰수 == ajutuu_ee_iyatialujuna) { 기억파일.wopu_a_ttaaleemüin_achuwalaa(1); 처리값 = 기억파일.wopu_a_ttaaleemüin_waai(0, '.'); } else 처리값 = 토큰수 == ajutuu_ee_iyatialujuna + 1 ? wopu_a_ttaaleemüin(ajutuu_ee_iyatialujuna) : -22;
            if (처리값 >= 0) 처리값 = 기억파일.경로목록(); if (처리값 < 0) ajachitia(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) 셸도구.anaajaalaa_achikii(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) 셸도구.ashataa_ajutuu(같음(0, "mv"));
        else if (같음(0, "cat")) 셸도구.e_rajaa_ajutuu();
        else if (같음(0, "wc")) 셸도구.세기();
        else if (같음(0, "grep")) 셸도구.찾기();
        else if (같음(0, "head") || 같음(0, "tail")) 셸도구.머리(같음(0, "tail"));
        else if (같음(0, "tee")) 셸도구.함께쓰기();
        else if (같음(0, "env")) aluwataalapu_u_anaatashajia.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (토큰수 == 1) aluwataalapu_u_anaatashajia.환경보기();
            for (int eitawaakualü_ee_iyatialujuna = 1; eitawaakualü_ee_iyatialujuna < 토큰수; eitawaakualü_ee_iyatialujuna++) { int 처리값 = aluwataalapu_u_anaatashajia.환경설정(eitawaakualü_ee_iyatialujuna, 같음(0, "unset")); if (처리값 != 0) { 결과 = 처리값; 단말.ashajaa("aluwataaya akatajaa_ajutuu: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) aluwataalapu_u_anaatashajia.파일실행();
        else if (같음(0, "true")) 결과 = 0;
        else if (같음(0, "false")) 결과 = 1;
        else if (같음(0, "history")) liinia_anaatülü.기록보기();
        else if (같음(0, "exit")) {
            if (aluwataalapu_u_anaatashajia.깊이 > 0) { 결과 = 토큰수 == 1 ? aluwataalapu_u_anaatashajia.jamakua_iparülein_ajutuu : 셸도구.숫자(1); if (결과 < 0 || 결과 > 255) 결과 = 2; aluwataalapu_u_anaatashajia.script_ajattiraa = true; }
            else if (보드.터미널(2) != 0) 터미널(true);
            else 단말.ashajaa("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) anaataa_ajutuu();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (토큰수 < 2) { 결과 = 2; 단말.ashajaa("사용법: rm anaajaalaa...\n"); }
            for (int eitawaakualü_ee_iyatialujuna = 1; eitawaakualü_ee_iyatialujuna < 토큰수; eitawaakualü_ee_iyatialujuna++) { int 처리값 = wopu_a_ttaaleemüin(eitawaakualü_ee_iyatialujuna); if (처리값 == 0) 처리값 = 기억파일.지우기(); if (처리값 < 0) ajachitia(처리값); }
        }
        else if (같음(0, "echo")) {
            int 시작자리 = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = 시작자리; 첫값 < 토큰수; 첫값++) { if (첫값 > 시작자리) 단말.문자(32); for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < akaliaa_ajutuu[첫값]; eitawaakualü_ee_iyatialujuna++) 보드.직렬쓰기(토큰[시작점[첫값] + eitawaakualü_ee_iyatialujuna]); }
            if (시작자리 == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.ashajaa("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? 파이썬꾸러미() : 도구(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !aluwataalapu_u_anaatashajia.연결중) { 단말.ashajaa("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = 도구(13); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = 도구(15); 결과 = 처리값 < 0 ? 126 : 처리값; if (!aluwataalapu_u_anaatashajia.연결중) { 단말.ashajaa("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = 도구(16); 결과 = 처리값 < 0 ? 126 : 처리값; if (!aluwataalapu_u_anaatashajia.연결중) { 단말.ashajaa("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int 크기 = 보드.터미널(13); 단말.ashajaa("TERMINAL SIZE "); 단말.수(크기 & 65535); 단말.문자('x'); 단말.수(크기 >>> 16); 단말.문자(10); }
            else 터미널(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { 보드.터미널(9); a_yataainpalaa.실행(); }
        else if (같음(0, "c")) keetnerü.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) keetnerü.작업시험();
        else if (같음(0, "g")) keetnerü.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) keetnerü.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = 보드.사용자실행(0); if (처리값 == 0) 단말.ashajaa("ELF DEMO PASS\n"); else ajachitia(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? a_yataaya_ekeroliaa(-2, 2) : 도구(-1); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !aluwataalapu_u_anaatashajia.연결중) { 단말.ashajaa("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) keetnerü.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = 보드.anaajaalaa_alate_eraa_akaaliijiaa(1); if (처리값 < 0) ajachitia(처리값); else { 단말.ashajaa("FTP listening "); a_yatawaajiraaya_a_yataaya.ashajaa_ejepüsee(보드.kusu_jamakua_iparülein(0,0)); 단말.ashajaa(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { 보드.anaajaalaa_alate_eraa_akaaliijiaa(0); 단말.ashajaa("FTP stopped\n"); }
            else 단말.ashajaa(보드.anaajaalaa_alate_eraa_akaaliijiaa(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { 꾸러미.준비(); 단말.ashajaa("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int anüikii_komputatooralujatü = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (토큰수 != 2 || anüikii_komputatooralujatü < 0) 단말.ashajaa("example java|c|python: 출력, anaajaalaa, 네트워크, 그래픽, Java Swing analaaya 예제\n");
            else { int 처리값 = 예제꾸러미.e_itawaa_ajutuu(anüikii_komputatooralujatü); if (처리값 < 0) { ajachitia(처리값); if (처리값 == -28) 단말.ashajaa("RAM full: remove unused files, then retry example\n"); } else 단말.ashajaa("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int akua_ipaa_ajutuu = 실행형식();
            if (akua_ipaa_ajutuu == 1 || akua_ipaa_ajutuu == 2) {
                int 처리값 = a_yataaya_ekeroliaa(akua_ipaa_ajutuu == 1 ? -1 : 14, 0); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !aluwataalapu_u_anaatashajia.연결중) { 단말.ashajaa("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (akua_ipaa_ajutuu == 0) { 결과 = 126; 단말.ashajaa("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { 결과 = 127; 단말.ashajaa("Unknown command. help: commands\n"); }
        }
    }
    public static void 실행() {
        꾸러미.준비();
        for (int anüikii_komputatooralujatü = 0; anüikii_komputatooralujatü < 3; anüikii_komputatooralujatü++) { int 처리값 = 예제꾸러미.e_itawaa_ajutuu(anüikii_komputatooralujatü); if (처리값 < 0) ajachitia(처리값); }
        도움말();
        while (true) {
            analaaya_a_ttawo_ulu.처리(); if (analaaya_a_ttawo_ulu.재개()) continue;
            if (!analaaya_a_ttawo_ulu.이어읽기) 단말.ashajaa("jkoros-native> "); liinia_anaatülü.liinia_aluwataayapala = true; 보드.원격대기(1); int 크기 = 줄읽기(); 보드.원격대기(0); liinia_anaatülü.liinia_aluwataayapala = false;
            if (크기 == -3) continue;
            if (크기 == -2) 단말.ashajaa("aluwataaya akatajaa_ajutuu: 명령줄이 너무 깁니다\n");
            if (크기 >= 0) { aluwataalapu_u_anaatashajia.script_ajattiraa = false; aluwataalapu_u_anaatashajia.실행(liinia, 0, 크기, 0); } else aluwataalapu_u_anaatashajia.jamakua_iparülein_ajutuu = 130;
            보드.원격명령끝(aluwataalapu_u_anaatashajia.jamakua_iparülein_ajutuu);
            liinia_anaatülü.크기 = liinia_anaatülü.ee_iyatiaa_ajutuu = liinia_anaatülü.achuwalaa_analaaya = 0;
        }
    }
}
