// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 명령줄. 따옴표, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] 줄 = new int[4096], 토큰 = new int[4096], 시작점 = new int[32], 길이 = new int[32];
    static int[] 편집내용 = new int[16384], 편집이름 = new int[63];
    static int 토큰수, 편집이름길이, 결과;
    static boolean 앞줄;
    static void 원바이트(int 값) { 보드.직렬쓰기(값); }
    static int 줄읽기() { return 줄편집.읽기(); }
    static boolean 나누기(int 크기) {
        int 위치 = 0, 끝 = 0; 토큰수 = 0;
        while (위치 < 크기) {
            while (위치 < 크기 && (줄[위치] == 32 || 줄[위치] == 9)) 위치++;
            if (위치 == 크기) break;
            if (토큰수 == 16) { 단말.쓰기("명령 해석: 인수가 너무 많습니다\n"); return false; }
            시작점[토큰수] = 끝; int 인용 = 0;
            while (위치 < 크기) {
                int 값 = 줄[위치++];
                if (인용 == 0 && (값 == 32 || 값 == 9)) break;
                if (값 == 인용) { 인용 = 0; continue; }
                if (인용 == 0 && (값 == 39 || 값 == 34)) { 인용 = 값; continue; }
                토큰[끝++] = 값;
            }
            if (인용 != 0) { 단말.쓰기("명령 해석: 따옴표가 닫히지 않았습니다\n"); return false; }
            길이[토큰수] = 끝 - 시작점[토큰수]; 토큰수++;
        }
        return true;
    }
    static boolean 같음(int 번호, String 말) {
        if (번호 >= 토큰수) return false;
        int 자리=0;
        for (int 순번=0; 순번<말.length(); 순번++) {
            int 문자값=말.charAt(순번);
            if (문자값>=0xd800 && 문자값<=0xdbff && 순번+1<말.length()) 문자값=0x10000+((문자값-0xd800)<<10)+말.charAt(++순번)-0xdc00;
            int 바이트수=문자값<128?1:문자값<2048?2:문자값<65536?3:4;
            for (int 차례=바이트수-1; 차례>=0; 차례--) {
                int 값=바이트수==1?문자값:차례==바이트수-1?(바이트수==2?0xc0:바이트수==3?0xe0:0xf0)|(문자값>>(6*차례)):0x80|((문자값>>(6*차례))&63);
                if (자리>=길이[번호] || 토큰[시작점[번호]+자리++]!=값) return false;
            }
        }
        return 자리==길이[번호];
    }
    static int 경로(int 번호) {
        if (번호 >= 토큰수) return -22;
        int 결과 = 기억파일.경로시작(길이[번호]); if (결과 < 0) return 결과;
        for (int 반복자리 = 0; 반복자리 < 길이[번호]; 반복자리++) {
            결과 = 기억파일.경로바이트(반복자리, 토큰[시작점[번호] + 반복자리]); if (결과 < 0) return 결과;
        }
        return 0;
    }
    static void 오류(int 번호) { 결과 = 1; 단말.쓰기("오류 "); 단말.수(번호); 단말.문자(10); }
    static void 보기() {
        if (토큰수 != 2) { 단말.쓰기("사용법: cat 파일\n"); return; }
        int 결과 = 경로(1); if (결과 < 0) { 오류(결과); return; }
        int 파일 = 기억파일.열기(0); if (파일 < 0) { 오류(파일); return; }
        while (true) { int 값 = 기억파일.읽기(파일); if (값 == 256) break; if (값 < 0) { 오류(값); break; } 원바이트(값); }
        기억파일.닫기(파일); 단말.문자(10);
    }
    static void 편집() {
        if (토큰수 != 2) { 단말.쓰기("사용법: edit 파일\n"); return; }
        int 결과 = 경로(1); if (결과 < 0) { 오류(결과); return; }
        편집이름길이 = 길이[1];
        for (int 반복자리 = 0; 반복자리 < 편집이름길이; 반복자리++) 편집이름[반복자리] = 토큰[시작점[1] + 반복자리];
        단말.쓰기("EDIT: 파일 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int 크기 = 0;
        while (true) {
            단말.쓰기("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.쓰기("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && 줄[0] == '.') break;
            if (입력 + 1 > 편집내용.length - 크기) { 단말.쓰기("EDIT CANCELLED: file too large\n"); return; }
            for (int 반복자리 = 0; 반복자리 < 입력; 반복자리++) 편집내용[크기++] = 줄[반복자리];
            편집내용[크기++] = 10;
        }
        기억파일.경로시작(편집이름길이);
        for (int 반복자리 = 0; 반복자리 < 편집이름길이; 반복자리++) 기억파일.경로바이트(반복자리, 편집이름[반복자리]);
        int 파일 = 기억파일.열기(577); if (파일 < 0) { 오류(파일); return; }
        for (int 반복자리 = 0; 반복자리 < 크기; 반복자리++) 기억파일.쓰기(파일, 편집내용[반복자리]);
        기억파일.닫기(파일); 단말.쓰기("SAVED "); 단말.수(크기); 단말.쓰기("바이트(주기억 파일)\n");
    }
    static int 십육(int 값) {
        if (값 >= '0' && 값 <= '9') return 값 - '0';
        if (값 >= 'a' && 값 <= 'f') return 값 - 'a' + 10;
        if (값 >= 'A' && 값 <= 'F') return 값 - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (토큰수 != 2) { 단말.쓰기("사용법: load 파일 | hex 파일\n"); return; }
        int 결과 = 경로(1); if (결과 < 0) { 오류(결과); return; }
        if (!넣기) {
            int 파일 = 기억파일.열기(0); if (파일 < 0) { 오류(파일); return; }
            단말.쓰기("HEX BEGIN "); 단말.수(기억파일.크기(파일)); 단말.문자(10);
            int 항목수 = 0;
            while (true) {
                int 값 = 기억파일.읽기(파일); if (값 < 0 || 값 == 256) break;
                단말.문자("0123456789abcdef".charAt(값 >> 4)); 단말.문자("0123456789abcdef".charAt(값 & 15));
                if (++항목수 % 32 == 0) 단말.문자(10);
            }
            if (항목수 % 32 != 0) 단말.문자(10);
            기억파일.닫기(파일); 단말.쓰기("HEX END\n"); return;
        }
        편집이름길이 = 길이[1];
        for (int 반복자리 = 0; 반복자리 < 편집이름길이; 반복자리++) 편집이름[반복자리] = 토큰[시작점[1] + 반복자리];
        단말.쓰기("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int 크기 = 0;
        while (true) {
            단말.쓰기("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.쓰기("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && 줄[0] == '.') break;
            int 앞 = -1;
            for (int 반복자리 = 0; 반복자리 < 입력; 반복자리++) {
                if (줄[반복자리] == 32 || 줄[반복자리] == 9) continue;
                int 값 = 십육(줄[반복자리]);
                if (값 < 0 || 크기 >= 편집내용.length) { 단말.쓰기("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = 값; else { 편집내용[크기++] = 앞 * 16 + 값; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.쓰기("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        기억파일.경로시작(편집이름길이);
        for (int 반복자리 = 0; 반복자리 < 편집이름길이; 반복자리++) 기억파일.경로바이트(반복자리, 편집이름[반복자리]);
        int 파일 = 기억파일.열기(577); if (파일 < 0) { 오류(파일); return; }
        for (int 반복자리 = 0; 반복자리 < 크기; 반복자리++) 기억파일.쓰기(파일, 편집내용[반복자리]);
        기억파일.닫기(파일); 단말.쓰기("LOADED "); 단말.수(크기); 단말.쓰기("바이트(주기억 파일)\n");
    }
    static int 도구(int 번호) {
        return 도구시작(번호, 1);
    }
    static int 도구시작(int 번호, int 시작) {
        if (토큰수 - 시작 > 8) return -22;
        보드.인수준비(토큰수 - 시작);
        for (int 첫값 = 시작; 첫값 < 토큰수; 첫값++) {
            if (길이[첫값] > 255) return -36;
            for (int 반복자리 = 0; 반복자리 < 길이[첫값]; 반복자리++) 보드.인수바이트(첫값 - 시작, 반복자리, 토큰[시작점[첫값] + 반복자리]);
        }
        return 번호 == -2 ? 보드.리눅스파일실행() : 번호 < 0 ? 보드.사용자파일실행() : 보드.사용자실행(번호);
    }
    static int 파이썬꾸러미() {
        if (토큰수 > 8) return -22;
        보드.인수준비(토큰수);
        String 경로 = "/lib/꾸러미.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int 자리 = 0;
        for (int 순번 = 0; 순번 < 경로.length(); 순번++) {
            int 글자 = 경로.charAt(순번);
            if (글자 < 128) 보드.인수바이트(0, 자리++, 글자);
            else { 보드.인수바이트(0, 자리++, 0xe0 | (글자 >> 12)); 보드.인수바이트(0, 자리++, 0x80 | ((글자 >> 6) & 63)); 보드.인수바이트(0, 자리++, 0x80 | (글자 & 63)); }
        }
        for (int 순번 = 1; 순번 < 토큰수; 순번++) {
            if (길이[순번] > 255) return -36;
            for (int 글자 = 0; 글자 < 길이[순번]; 글자++) 보드.인수바이트(순번, 글자, 토큰[시작점[순번] + 글자]);
        }
        return 보드.사용자실행(12);
    }
    static int 실행형식() {
        int 처리값 = 경로(0); if (처리값 < 0) return 처리값;
        int 파일 = 기억파일.열기(0); if (파일 < 0) return 파일;
        int 첫값 = 기억파일.읽기(파일), 바이트값 = 기억파일.읽기(파일), 문자값 = 기억파일.읽기(파일), 뒷값 = 기억파일.읽기(파일);
        기억파일.닫기(파일);
        if (첫값 == 127 && 바이트값 == 'E' && 문자값 == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && 바이트값 == 'K' && 문자값 == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int 번호, String 인수) {
        보드.인수준비(1);
        for (int 반복자리 = 0; 반복자리 < 인수.length(); 반복자리++) 보드.인수바이트(0, 반복자리, 인수.charAt(반복자리));
        return 보드.사용자실행(번호);
    }
    static void 글바이트(int 파일, int 값) { 기억파일.쓰기(파일, 값); }
    static void 정적파일(String 이름, String 내용) {
        // 꾸러미 파일명은 ASCII. 파일 내용은 UTF-8로 저장한다.
        기억파일.경로시작(이름.length());
        for (int 반복자리 = 0; 반복자리 < 이름.length(); 반복자리++) 기억파일.경로바이트(반복자리, 이름.charAt(반복자리));
        int 파일 = 기억파일.열기(193); if (파일 < 0) return;
        for (int 반복자리 = 0; 반복자리 < 내용.length(); 반복자리++) {
            int 문자값 = 내용.charAt(반복자리);
            if (문자값 >= 0xd800 && 문자값 <= 0xdbff && 반복자리 + 1 < 내용.length()) 문자값 = 0x10000 + ((문자값 - 0xd800) << 10) + 내용.charAt(++반복자리) - 0xdc00;
            if (문자값 < 128) 글바이트(파일, 문자값);
            else {
                int 수 = 문자값 < 2048 ? 2 : 문자값 < 65536 ? 3 : 4;
                글바이트(파일, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (문자값 >> (6 * (수 - 1))));
                for (int 항목수 = 수 - 1; 항목수 > 0; 항목수--) 글바이트(파일, 0x80 | ((문자값 >> (6 * (항목수 - 1))) & 63));
            }
        }
        기억파일.닫기(파일);
    }
    static void 한글도움말() {
        단말.쓰기("F9 / Shift+Space: [EN] ↔ [zea]\n");
        단말.쓰기("  [ZEA] keyboard; [EN] ASCII\n");
        단말.쓰기("  a → a\n");
        단말.쓰기("  F9: EN ↔ zea | Ctrl+Shift+V: UTF-8\n");
        단말.쓰기("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.쓰기("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String 이름) {
        int 바이트수 = 0;
        for (int 반복자리 = 0; 반복자리 < 이름.length(); 반복자리++) { int 문자값 = 이름.charAt(반복자리); if (문자값 >= 0xd800 && 문자값 <= 0xdfff) return -22; 바이트수 += 문자값 < 128 ? 1 : 문자값 < 2048 ? 2 : 3; }
        int 처리값 = 기억파일.경로시작(바이트수); if (처리값 < 0) return 처리값;
        int 자리 = 0;
        for (int 반복자리 = 0; 반복자리 < 이름.length(); 반복자리++) {
            int 문자값 = 이름.charAt(반복자리);
            if (문자값 < 128) 기억파일.경로바이트(자리++, 문자값);
            else if (문자값 < 2048) { 기억파일.경로바이트(자리++, 0xc0 | (문자값 >> 6)); 기억파일.경로바이트(자리++, 0x80 | (문자값 & 63)); }
            else { 기억파일.경로바이트(자리++, 0xe0 | (문자값 >> 12)); 기억파일.경로바이트(자리++, 0x80 | ((문자값 >> 6) & 63)); 기억파일.경로바이트(자리++, 0x80 | (문자값 & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String 이름) {
        int 처리값 = 예제경로(이름); if (처리값 < 0) return 처리값;
        처리값 = 기억파일.폴더만들기(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String 이름, String 자료) {
        int 처리값 = 예제경로(이름); if (처리값 < 0) return 처리값;
        int 파일 = 기억파일.열기(193); if (파일 == -17) return 0; if (파일 < 0) return 파일;
        for (int 반복자리 = 0; 반복자리 < 자료.length(); 반복자리 += 2) {
            처리값 = 기억파일.쓰기(파일, 십육(자료.charAt(반복자리)) * 16 + 십육(자료.charAt(반복자리 + 1)));
            if (처리값 < 0) { 기억파일.닫기(파일); return 처리값; }
        }
        return 기억파일.닫기(파일);
    }
    static void 도움말() {
        체계도구.도움말();
        단말.쓰기("sshd / 보안셸 start|stop|status: SSH :22 (user, 장치별 암호)\n");
        단말.쓰기("vncd / 원격화면 start|stop|status: VNC :5900 (장치별 암호)\n");
        단말.쓰기("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.쓰기("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.쓰기("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.쓰기("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.쓰기("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.쓰기("모서리 + 왼쪽 버튼 끌기: 터미널 크기 변경; terminal size: 열/행\n");
        단말.쓰기("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.쓰기("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.쓰기("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.쓰기("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.쓰기("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.쓰기("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.쓰기("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.쓰기("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.쓰기("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.쓰기("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.쓰기("pip: MicroPython 소스 설치; 호스트 --network --pip 필요; /lib는 RAM\n");
        단말.쓰기("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.쓰기("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.쓰기("/example/java /example/c /example/python: examples ready at boot\n");
        단말.쓰기("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void 터미널(boolean 전환여부) {
        if (전환여부 && 보드.터미널(2) != 0) { 보드.터미널(0); 단말.쓰기("TERMINAL CLOSED\n"); }
        else if (보드.터미널(1) < 0) 오류(-19);
        else 단말.쓰기("TERMINAL READY — zea terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void 명령() {
        if (토큰수 == 0) return;
        if (체계도구.실행()) return;
        if (같음(0,"sshd") || 같음(0,"보안셸") || 같음(0,"vncd") || 같음(0,"원격화면")) {
            int 종류=같음(0,"vncd")||같음(0,"원격화면")?1:0;
            int 동작=같음(1,"start")||같음(1,"시작")?1:같음(1,"stop")||같음(1,"중지")?0:2;
            int 상태=보드.원격제어(종류,동작);
            if(상태<0)오류(상태);else 단말.쓰기(보드.원격제어(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else 도움말(); }
        else if (같음(0, "info") || 같음(0, "i")) 핵심.정보();
        else if (같음(0, "pwd")) { 기억파일.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (토큰수 == 1) { 기억파일.경로시작(1); 처리값 = 기억파일.경로바이트(0, '/'); } else 처리값 = 토큰수 == 2 ? 경로(1) : -22;
            if (처리값 >= 0) 처리값 = 기억파일.폴더이동(); if (처리값 < 0) 오류(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int 인수번호 = 같음(1, "-l") ? 2 : 1, 처리값;
            if (토큰수 == 인수번호) { 기억파일.경로시작(1); 처리값 = 기억파일.경로바이트(0, '.'); } else 처리값 = 토큰수 == 인수번호 + 1 ? 경로(인수번호) : -22;
            if (처리값 >= 0) 처리값 = 기억파일.경로목록(); if (처리값 < 0) 오류(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) 셸도구.파일일(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) 셸도구.복사(같음(0, "mv"));
        else if (같음(0, "cat")) 셸도구.보기();
        else if (같음(0, "wc")) 셸도구.세기();
        else if (같음(0, "grep")) 셸도구.찾기();
        else if (같음(0, "head") || 같음(0, "tail")) 셸도구.머리(같음(0, "tail"));
        else if (같음(0, "tee")) 셸도구.함께쓰기();
        else if (같음(0, "env")) 셸문법.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (토큰수 == 1) 셸문법.환경보기();
            for (int 반복자리 = 1; 반복자리 < 토큰수; 반복자리++) { int 처리값 = 셸문법.환경설정(반복자리, 같음(0, "unset")); if (처리값 != 0) { 결과 = 처리값; 단말.쓰기("명령 해석: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) 셸문법.파일실행();
        else if (같음(0, "true")) 결과 = 0;
        else if (같음(0, "false")) 결과 = 1;
        else if (같음(0, "history")) 줄편집.기록보기();
        else if (같음(0, "exit")) {
            if (셸문법.깊이 > 0) { 결과 = 토큰수 == 1 ? 셸문법.상태 : 셸도구.숫자(1); if (결과 < 0 || 결과 > 255) 결과 = 2; 셸문법.스크립트끝 = true; }
            else if (보드.터미널(2) != 0) 터미널(true);
            else 단말.쓰기("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) 편집();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (토큰수 < 2) { 결과 = 2; 단말.쓰기("사용법: rm 파일...\n"); }
            for (int 반복자리 = 1; 반복자리 < 토큰수; 반복자리++) { int 처리값 = 경로(반복자리); if (처리값 == 0) 처리값 = 기억파일.지우기(); if (처리값 < 0) 오류(처리값); }
        }
        else if (같음(0, "echo")) {
            int 시작자리 = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = 시작자리; 첫값 < 토큰수; 첫값++) { if (첫값 > 시작자리) 단말.문자(32); for (int 반복자리 = 0; 반복자리 < 길이[첫값]; 반복자리++) 보드.직렬쓰기(토큰[시작점[첫값] + 반복자리]); }
            if (시작자리 == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.쓰기("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? 파이썬꾸러미() : 도구(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !셸문법.연결중) { 단말.쓰기("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = 도구(13); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = 도구(15); 결과 = 처리값 < 0 ? 126 : 처리값; if (!셸문법.연결중) { 단말.쓰기("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = 도구(16); 결과 = 처리값 < 0 ? 126 : 처리값; if (!셸문법.연결중) { 단말.쓰기("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int 크기 = 보드.터미널(13); 단말.쓰기("TERMINAL SIZE "); 단말.수(크기 & 65535); 단말.문자('x'); 단말.수(크기 >>> 16); 단말.문자(10); }
            else 터미널(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { 보드.터미널(9); 화면마당.실행(); }
        else if (같음(0, "c")) 핵심.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) 핵심.작업시험();
        else if (같음(0, "g")) 핵심.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) 핵심.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = 보드.사용자실행(0); if (처리값 == 0) 단말.쓰기("ELF DEMO PASS\n"); else 오류(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? 도구시작(-2, 2) : 도구(-1); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !셸문법.연결중) { 단말.쓰기("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) 핵심.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = 보드.파일전송서비스(1); if (처리값 < 0) 오류(처리값); else { 단말.쓰기("FTP listening "); 체계도구.주소쓰기(보드.망상태(0,0)); 단말.쓰기(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { 보드.파일전송서비스(0); 단말.쓰기("FTP stopped\n"); }
            else 단말.쓰기(보드.파일전송서비스(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { 꾸러미.준비(); 단말.쓰기("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int 언어 = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (토큰수 != 2 || 언어 < 0) 단말.쓰기("example java|c|python: 출력, 파일, 네트워크, 그래픽, Java Swing 창 예제\n");
            else { int 처리값 = 예제꾸러미.설치(언어); if (처리값 < 0) { 오류(처리값); if (처리값 == -28) 단말.쓰기("RAM full: remove unused files, then retry example\n"); } else 단말.쓰기("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int 형식 = 실행형식();
            if (형식 == 1 || 형식 == 2) {
                int 처리값 = 도구시작(형식 == 1 ? -1 : 14, 0); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !셸문법.연결중) { 단말.쓰기("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (형식 == 0) { 결과 = 126; 단말.쓰기("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { 결과 = 127; 단말.쓰기("Unknown command. help: commands\n"); }
        }
    }
    public static void 실행() {
        꾸러미.준비();
        for (int 언어 = 0; 언어 < 3; 언어++) { int 처리값 = 예제꾸러미.설치(언어); if (처리값 < 0) 오류(처리값); }
        도움말();
        while (true) {
            창세션.처리(); if (창세션.재개()) continue;
            if (!창세션.이어읽기) 단말.쓰기("jkoros-native> "); 줄편집.명령줄 = true; 보드.원격대기(1); int 크기 = 줄읽기(); 보드.원격대기(0); 줄편집.명령줄 = false;
            if (크기 == -3) continue;
            if (크기 == -2) 단말.쓰기("명령 해석: 명령줄이 너무 깁니다\n");
            if (크기 >= 0) { 셸문법.스크립트끝 = false; 셸문법.실행(줄, 0, 크기, 0); } else 셸문법.상태 = 130;
            보드.원격명령끝(셸문법.상태);
            줄편집.크기 = 줄편집.커서 = 줄편집.창시작 = 0;
        }
    }
}
