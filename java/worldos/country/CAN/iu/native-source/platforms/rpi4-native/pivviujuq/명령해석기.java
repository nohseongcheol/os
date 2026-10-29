// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 piqujivik. 따옴표, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] titikutaak = new int[4096], 토큰 = new int[4096], 시작점 = new int[32], takininga_atuutilik = new int[32];
    static int[] 편집내용 = new int[16384], aaqqigiarli_atiq = new int[63];
    static int 토큰수, aaqqigiarli_atiq_takininga, 결과;
    static boolean 앞줄;
    static void 원바이트(int atuutilik) { 보드.직렬쓰기(atuutilik); }
    static int 줄읽기() { return titikutaak_aaqqigiariji.읽기(); }
    static boolean 나누기(int anininga) {
        int 위치 = 0, 끝 = 0; 토큰수 = 0;
        while (위치 < anininga) {
            while (위치 < anininga && (titikutaak[위치] == 32 || titikutaak[위치] == 9)) 위치++;
            if (위치 == anininga) break;
            if (토큰수 == 16) { 단말.titiraq("piqujijjut agguqtuut_atuutilik: 인수가 너무 많습니다\n"); return false; }
            시작점[토큰수] = 끝; int 인용 = 0;
            while (위치 < anininga) {
                int atuutilik = titikutaak[위치++];
                if (인용 == 0 && (atuutilik == 32 || atuutilik == 9)) break;
                if (atuutilik == 인용) { 인용 = 0; continue; }
                if (인용 == 0 && (atuutilik == 39 || atuutilik == 34)) { 인용 = atuutilik; continue; }
                토큰[끝++] = atuutilik;
            }
            if (인용 != 0) { 단말.titiraq("piqujijjut agguqtuut_atuutilik: 따옴표가 닫히지 않았습니다\n"); return false; }
            takininga_atuutilik[토큰수] = 끝 - 시작점[토큰수]; 토큰수++;
        }
        return true;
    }
    static boolean 같음(int nalunaiqsimavik, String 말) {
        if (nalunaiqsimavik >= 토큰수) return false;
        int 자리=0;
        for (int 순번=0; 순번<말.length(); 순번++) {
            int immikkuuqtumut_nalunaikkut=말.charAt(순번);
            if (immikkuuqtumut_nalunaikkut>=0xd800 && immikkuuqtumut_nalunaikkut<=0xdbff && 순번+1<말.length()) immikkuuqtumut_nalunaikkut=0x10000+((immikkuuqtumut_nalunaikkut-0xd800)<<10)+말.charAt(++순번)-0xdc00;
            int 바이트수=immikkuuqtumut_nalunaikkut<128?1:immikkuuqtumut_nalunaikkut<2048?2:immikkuuqtumut_nalunaikkut<65536?3:4;
            for (int 차례=바이트수-1; 차례>=0; 차례--) {
                int atuutilik=바이트수==1?immikkuuqtumut_nalunaikkut:차례==바이트수-1?(바이트수==2?0xc0:바이트수==3?0xe0:0xf0)|(immikkuuqtumut_nalunaikkut>>(6*차례)):0x80|((immikkuuqtumut_nalunaikkut>>(6*차례))&63);
                if (자리>=takininga_atuutilik[nalunaiqsimavik] || 토큰[시작점[nalunaiqsimavik]+자리++]!=atuutilik) return false;
            }
        }
        return 자리==takininga_atuutilik[nalunaiqsimavik];
    }
    static int aqqut(int nalunaiqsimavik) {
        if (nalunaiqsimavik >= 토큰수) return -22;
        int 결과 = 기억파일.aqqut_pigiarli(takininga_atuutilik[nalunaiqsimavik]); if (결과 < 0) return 결과;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < takininga_atuutilik[nalunaiqsimavik]; piliqqittaajuq_nalunaiqsimavik++) {
            결과 = 기억파일.aqqut_byte(piliqqittaajuq_nalunaiqsimavik, 토큰[시작점[nalunaiqsimavik] + piliqqittaajuq_nalunaiqsimavik]); if (결과 < 0) return 결과;
        }
        return 0;
    }
    static void tammarniq(int nalunaiqsimavik) { 결과 = 1; 단말.titiraq("tammarniq "); 단말.수(nalunaiqsimavik); 단말.문자(10); }
    static void takussarurli_atuutilik() {
        if (토큰수 != 2) { 단말.titiraq("사용법: cat ini\n"); return; }
        int 결과 = aqqut(1); if (결과 < 0) { tammarniq(결과); return; }
        int ini = 기억파일.matuirli(0); if (ini < 0) { tammarniq(ini); return; }
        while (true) { int atuutilik = 기억파일.읽기(ini); if (atuutilik == 256) break; if (atuutilik < 0) { tammarniq(atuutilik); break; } 원바이트(atuutilik); }
        기억파일.matuli(ini); 단말.문자(10);
    }
    static void aaqqigiarli_atuutilik() {
        if (토큰수 != 2) { 단말.titiraq("사용법: edit ini\n"); return; }
        int 결과 = aqqut(1); if (결과 < 0) { tammarniq(결과); return; }
        aaqqigiarli_atiq_takininga = takininga_atuutilik[1];
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < aaqqigiarli_atiq_takininga; piliqqittaajuq_nalunaiqsimavik++) aaqqigiarli_atiq[piliqqittaajuq_nalunaiqsimavik] = 토큰[시작점[1] + piliqqittaajuq_nalunaiqsimavik];
        단말.titiraq("EDIT: ini 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int anininga = 0;
        while (true) {
            단말.titiraq("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.titiraq("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && titikutaak[0] == '.') break;
            if (입력 + 1 > 편집내용.length - anininga) { 단말.titiraq("EDIT CANCELLED: file too large\n"); return; }
            for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 입력; piliqqittaajuq_nalunaiqsimavik++) 편집내용[anininga++] = titikutaak[piliqqittaajuq_nalunaiqsimavik];
            편집내용[anininga++] = 10;
        }
        기억파일.aqqut_pigiarli(aaqqigiarli_atiq_takininga);
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < aaqqigiarli_atiq_takininga; piliqqittaajuq_nalunaiqsimavik++) 기억파일.aqqut_byte(piliqqittaajuq_nalunaiqsimavik, aaqqigiarli_atiq[piliqqittaajuq_nalunaiqsimavik]);
        int ini = 기억파일.matuirli(577); if (ini < 0) { tammarniq(ini); return; }
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < anininga; piliqqittaajuq_nalunaiqsimavik++) 기억파일.titiraq(ini, 편집내용[piliqqittaajuq_nalunaiqsimavik]);
        기억파일.matuli(ini); 단말.titiraq("SAVED "); 단말.수(anininga); 단말.titiraq("byte_atuutilik(주기억 ini)\n");
    }
    static int 십육(int atuutilik) {
        if (atuutilik >= '0' && atuutilik <= '9') return atuutilik - '0';
        if (atuutilik >= 'a' && atuutilik <= 'f') return atuutilik - 'a' + 10;
        if (atuutilik >= 'A' && atuutilik <= 'F') return atuutilik - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (토큰수 != 2) { 단말.titiraq("사용법: load ini | hex ini\n"); return; }
        int 결과 = aqqut(1); if (결과 < 0) { tammarniq(결과); return; }
        if (!넣기) {
            int ini = 기억파일.matuirli(0); if (ini < 0) { tammarniq(ini); return; }
            단말.titiraq("HEX BEGIN "); 단말.수(기억파일.anininga(ini)); 단말.문자(10);
            int 항목수 = 0;
            while (true) {
                int atuutilik = 기억파일.읽기(ini); if (atuutilik < 0 || atuutilik == 256) break;
                단말.문자("0123456789abcdef".charAt(atuutilik >> 4)); 단말.문자("0123456789abcdef".charAt(atuutilik & 15));
                if (++항목수 % 32 == 0) 단말.문자(10);
            }
            if (항목수 % 32 != 0) 단말.문자(10);
            기억파일.matuli(ini); 단말.titiraq("HEX END\n"); return;
        }
        aaqqigiarli_atiq_takininga = takininga_atuutilik[1];
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < aaqqigiarli_atiq_takininga; piliqqittaajuq_nalunaiqsimavik++) aaqqigiarli_atiq[piliqqittaajuq_nalunaiqsimavik] = 토큰[시작점[1] + piliqqittaajuq_nalunaiqsimavik];
        단말.titiraq("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int anininga = 0;
        while (true) {
            단말.titiraq("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.titiraq("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && titikutaak[0] == '.') break;
            int 앞 = -1;
            for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 입력; piliqqittaajuq_nalunaiqsimavik++) {
                if (titikutaak[piliqqittaajuq_nalunaiqsimavik] == 32 || titikutaak[piliqqittaajuq_nalunaiqsimavik] == 9) continue;
                int atuutilik = 십육(titikutaak[piliqqittaajuq_nalunaiqsimavik]);
                if (atuutilik < 0 || anininga >= 편집내용.length) { 단말.titiraq("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = atuutilik; else { 편집내용[anininga++] = 앞 * 16 + atuutilik; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.titiraq("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        기억파일.aqqut_pigiarli(aaqqigiarli_atiq_takininga);
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < aaqqigiarli_atiq_takininga; piliqqittaajuq_nalunaiqsimavik++) 기억파일.aqqut_byte(piliqqittaajuq_nalunaiqsimavik, aaqqigiarli_atiq[piliqqittaajuq_nalunaiqsimavik]);
        int ini = 기억파일.matuirli(577); if (ini < 0) { tammarniq(ini); return; }
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < anininga; piliqqittaajuq_nalunaiqsimavik++) 기억파일.titiraq(ini, 편집내용[piliqqittaajuq_nalunaiqsimavik]);
        기억파일.matuli(ini); 단말.titiraq("LOADED "); 단말.수(anininga); 단말.titiraq("byte_atuutilik(주기억 ini)\n");
    }
    static int 도구(int nalunaiqsimavik) {
        return sanajjut_Iliniku(nalunaiqsimavik, 1);
    }
    static int sanajjut_Iliniku(int nalunaiqsimavik, int 시작) {
        if (토큰수 - 시작 > 8) return -22;
        보드.인수준비(토큰수 - 시작);
        for (int 첫값 = 시작; 첫값 < 토큰수; 첫값++) {
            if (takininga_atuutilik[첫값] > 255) return -36;
            for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < takininga_atuutilik[첫값]; piliqqittaajuq_nalunaiqsimavik++) 보드.aturniqarnirainiq_byte(첫값 - 시작, piliqqittaajuq_nalunaiqsimavik, 토큰[시작점[첫값] + piliqqittaajuq_nalunaiqsimavik]);
        }
        return nalunaiqsimavik == -2 ? 보드.리눅스파일실행() : nalunaiqsimavik < 0 ? 보드.사용자파일실행() : 보드.사용자실행(nalunaiqsimavik);
    }
    static int 파이썬꾸러미() {
        if (토큰수 > 8) return -22;
        보드.인수준비(토큰수);
        String aqqut = "/lib/꾸러미.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int 자리 = 0;
        for (int 순번 = 0; 순번 < aqqut.length(); 순번++) {
            int immikkuuqtuq_atuutilik = aqqut.charAt(순번);
            if (immikkuuqtuq_atuutilik < 128) 보드.aturniqarnirainiq_byte(0, 자리++, immikkuuqtuq_atuutilik);
            else { 보드.aturniqarnirainiq_byte(0, 자리++, 0xe0 | (immikkuuqtuq_atuutilik >> 12)); 보드.aturniqarnirainiq_byte(0, 자리++, 0x80 | ((immikkuuqtuq_atuutilik >> 6) & 63)); 보드.aturniqarnirainiq_byte(0, 자리++, 0x80 | (immikkuuqtuq_atuutilik & 63)); }
        }
        for (int 순번 = 1; 순번 < 토큰수; 순번++) {
            if (takininga_atuutilik[순번] > 255) return -36;
            for (int immikkuuqtuq_atuutilik = 0; immikkuuqtuq_atuutilik < takininga_atuutilik[순번]; immikkuuqtuq_atuutilik++) 보드.aturniqarnirainiq_byte(순번, immikkuuqtuq_atuutilik, 토큰[시작점[순번] + immikkuuqtuq_atuutilik]);
        }
        return 보드.사용자실행(12);
    }
    static int 실행형식() {
        int 처리값 = aqqut(0); if (처리값 < 0) return 처리값;
        int ini = 기억파일.matuirli(0); if (ini < 0) return ini;
        int 첫값 = 기억파일.읽기(ini), byte_titiqqat = 기억파일.읽기(ini), immikkuuqtumut_nalunaikkut = 기억파일.읽기(ini), 뒷값 = 기억파일.읽기(ini);
        기억파일.matuli(ini);
        if (첫값 == 127 && byte_titiqqat == 'E' && immikkuuqtumut_nalunaikkut == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && byte_titiqqat == 'K' && immikkuuqtumut_nalunaikkut == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int nalunaiqsimavik, String 인수) {
        보드.인수준비(1);
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 인수.length(); piliqqittaajuq_nalunaiqsimavik++) 보드.aturniqarnirainiq_byte(0, piliqqittaajuq_nalunaiqsimavik, 인수.charAt(piliqqittaajuq_nalunaiqsimavik));
        return 보드.사용자실행(nalunaiqsimavik);
    }
    static void titiqqaq_byte(int ini, int atuutilik) { 기억파일.titiraq(ini, atuutilik); }
    static void surravviqanngittuq_ini(String atiq, String Ilulingit_atuutilik) {
        // 꾸러미 파일명은 ASCII. ini 내용은 UTF-8로 저장한다.
        기억파일.aqqut_pigiarli(atiq.length());
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < atiq.length(); piliqqittaajuq_nalunaiqsimavik++) 기억파일.aqqut_byte(piliqqittaajuq_nalunaiqsimavik, atiq.charAt(piliqqittaajuq_nalunaiqsimavik));
        int ini = 기억파일.matuirli(193); if (ini < 0) return;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < Ilulingit_atuutilik.length(); piliqqittaajuq_nalunaiqsimavik++) {
            int immikkuuqtumut_nalunaikkut = Ilulingit_atuutilik.charAt(piliqqittaajuq_nalunaiqsimavik);
            if (immikkuuqtumut_nalunaikkut >= 0xd800 && immikkuuqtumut_nalunaikkut <= 0xdbff && piliqqittaajuq_nalunaiqsimavik + 1 < Ilulingit_atuutilik.length()) immikkuuqtumut_nalunaikkut = 0x10000 + ((immikkuuqtumut_nalunaikkut - 0xd800) << 10) + Ilulingit_atuutilik.charAt(++piliqqittaajuq_nalunaiqsimavik) - 0xdc00;
            if (immikkuuqtumut_nalunaikkut < 128) titiqqaq_byte(ini, immikkuuqtumut_nalunaikkut);
            else {
                int 수 = immikkuuqtumut_nalunaikkut < 2048 ? 2 : immikkuuqtumut_nalunaikkut < 65536 ? 3 : 4;
                titiqqaq_byte(ini, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (immikkuuqtumut_nalunaikkut >> (6 * (수 - 1))));
                for (int 항목수 = 수 - 1; 항목수 > 0; 항목수--) titiqqaq_byte(ini, 0x80 | ((immikkuuqtumut_nalunaikkut >> (6 * (항목수 - 1))) & 63));
            }
        }
        기억파일.matuli(ini);
    }
    static void 한글도움말() {
        단말.titiraq("F9 / Shift+Space: [EN] ↔ [iu]\n");
        단말.titiraq("  [IU] keyboard; [EN] ASCII\n");
        단말.titiraq("  a → a\n");
        단말.titiraq("  F9: EN ↔ iu | Ctrl+Shift+V: UTF-8\n");
        단말.titiraq("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.titiraq("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String atiq) {
        int 바이트수 = 0;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < atiq.length(); piliqqittaajuq_nalunaiqsimavik++) { int immikkuuqtumut_nalunaikkut = atiq.charAt(piliqqittaajuq_nalunaiqsimavik); if (immikkuuqtumut_nalunaikkut >= 0xd800 && immikkuuqtumut_nalunaikkut <= 0xdfff) return -22; 바이트수 += immikkuuqtumut_nalunaikkut < 128 ? 1 : immikkuuqtumut_nalunaikkut < 2048 ? 2 : 3; }
        int 처리값 = 기억파일.aqqut_pigiarli(바이트수); if (처리값 < 0) return 처리값;
        int 자리 = 0;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < atiq.length(); piliqqittaajuq_nalunaiqsimavik++) {
            int immikkuuqtumut_nalunaikkut = atiq.charAt(piliqqittaajuq_nalunaiqsimavik);
            if (immikkuuqtumut_nalunaikkut < 128) 기억파일.aqqut_byte(자리++, immikkuuqtumut_nalunaikkut);
            else if (immikkuuqtumut_nalunaikkut < 2048) { 기억파일.aqqut_byte(자리++, 0xc0 | (immikkuuqtumut_nalunaikkut >> 6)); 기억파일.aqqut_byte(자리++, 0x80 | (immikkuuqtumut_nalunaikkut & 63)); }
            else { 기억파일.aqqut_byte(자리++, 0xe0 | (immikkuuqtumut_nalunaikkut >> 12)); 기억파일.aqqut_byte(자리++, 0x80 | ((immikkuuqtumut_nalunaikkut >> 6) & 63)); 기억파일.aqqut_byte(자리++, 0x80 | (immikkuuqtumut_nalunaikkut & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String atiq) {
        int 처리값 = 예제경로(atiq); if (처리값 < 0) return 처리값;
        처리값 = 기억파일.폴더만들기(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String atiq, String titiqqat) {
        int 처리값 = 예제경로(atiq); if (처리값 < 0) return 처리값;
        int ini = 기억파일.matuirli(193); if (ini == -17) return 0; if (ini < 0) return ini;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < titiqqat.length(); piliqqittaajuq_nalunaiqsimavik += 2) {
            처리값 = 기억파일.titiraq(ini, 십육(titiqqat.charAt(piliqqittaajuq_nalunaiqsimavik)) * 16 + 십육(titiqqat.charAt(piliqqittaajuq_nalunaiqsimavik + 1)));
            if (처리값 < 0) { 기억파일.matuli(ini); return 처리값; }
        }
        return 기억파일.matuli(ini);
    }
    static void saqqilli_Ikajuqtau() {
        qarasaujaq_sanajjut.saqqilli_Ikajuqtau();
        단말.titiraq("sshd / 보안셸 start|stop|status: SSH :22 (user, 장치별 isirut_atuutilik)\n");
        단말.titiraq("vncd / ungasittuq_saqqijaarli start|stop|status: VNC :5900 (장치별 isirut_atuutilik)\n");
        단말.titiraq("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.titiraq("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.titiraq("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.titiraq("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.titiraq("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.titiraq("모서리 + 왼쪽 버튼 Nusuarli_atuutilik: 터미널 anininga asijjirli_atuutilik; terminal size: ammukutaak_atuutilik/sanimukutaak_atuutilik\n");
        단말.titiraq("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.titiraq("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.titiraq("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.titiraq("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.titiraq("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.titiraq("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.titiraq("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.titiraq("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.titiraq("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.titiraq("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.titiraq("pip: MicroPython pivviujuq_attavigiit ilili_atuutilik; tuttarvik --network --pip 필요; /lib는 RAM\n");
        단말.titiraq("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.titiraq("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.titiraq("/example/java /example/c /example/python: examples ready at boot\n");
        단말.titiraq("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void 터미널(boolean 전환여부) {
        if (전환여부 && 보드.터미널(2) != 0) { 보드.터미널(0); 단말.titiraq("TERMINAL CLOSED\n"); }
        else if (보드.터미널(1) < 0) tammarniq(-19);
        else 단말.titiraq("TERMINAL READY — iu terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void piqujijjut() {
        if (토큰수 == 0) return;
        if (qarasaujaq_sanajjut.실행()) return;
        if (같음(0,"sshd") || 같음(0,"보안셸") || 같음(0,"vncd") || 같음(0,"ungasittuq_saqqijaarli")) {
            int 종류=같음(0,"vncd")||같음(0,"ungasittuq_saqqijaarli")?1:0;
            int sugiarut=같음(1,"start")||같음(1,"시작")?1:같음(1,"stop")||같음(1,"nuqqarli")?0:2;
            int qanuilinganiq_atuutilik=보드.ungasittuq_aulattivik(종류,sugiarut);
            if(qanuilinganiq_atuutilik<0)tammarniq(qanuilinganiq_atuutilik);else 단말.titiraq(보드.ungasittuq_aulattivik(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else saqqilli_Ikajuqtau(); }
        else if (같음(0, "info") || 같음(0, "i")) kernel.msinfo32_exe();
        else if (같음(0, "pwd")) { 기억파일.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (토큰수 == 1) { 기억파일.aqqut_pigiarli(1); 처리값 = 기억파일.aqqut_byte(0, '/'); } else 처리값 = 토큰수 == 2 ? aqqut(1) : -22;
            if (처리값 >= 0) 처리값 = 기억파일.asijjirli_tukimuagutiit(); if (처리값 < 0) tammarniq(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int aturniqarnirainiq_nalunaiqsimavik = 같음(1, "-l") ? 2 : 1, 처리값;
            if (토큰수 == aturniqarnirainiq_nalunaiqsimavik) { 기억파일.aqqut_pigiarli(1); 처리값 = 기억파일.aqqut_byte(0, '.'); } else 처리값 = 토큰수 == aturniqarnirainiq_nalunaiqsimavik + 1 ? aqqut(aturniqarnirainiq_nalunaiqsimavik) : -22;
            if (처리값 >= 0) 처리값 = 기억파일.경로목록(); if (처리값 < 0) tammarniq(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) 셸도구.ini_pijatsaq(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) 셸도구.ijjuarli_atuutilik(같음(0, "mv"));
        else if (같음(0, "cat")) 셸도구.takussarurli_atuutilik();
        else if (같음(0, "wc")) 셸도구.세기();
        else if (같음(0, "grep")) 셸도구.nanili_Iliniku();
        else if (같음(0, "head") || 같음(0, "tail")) 셸도구.머리(같음(0, "tail"));
        else if (같음(0, "tee")) 셸도구.함께쓰기();
        else if (같음(0, "env")) piqujijjutiliriji_syntax.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (토큰수 == 1) piqujijjutiliriji_syntax.환경보기();
            for (int piliqqittaajuq_nalunaiqsimavik = 1; piliqqittaajuq_nalunaiqsimavik < 토큰수; piliqqittaajuq_nalunaiqsimavik++) { int 처리값 = piqujijjutiliriji_syntax.환경설정(piliqqittaajuq_nalunaiqsimavik, 같음(0, "unset")); if (처리값 != 0) { 결과 = 처리값; 단말.titiraq("piqujijjut agguqtuut_atuutilik: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) piqujijjutiliriji_syntax.파일실행();
        else if (같음(0, "true")) 결과 = 0;
        else if (같음(0, "false")) 결과 = 1;
        else if (같음(0, "history")) titikutaak_aaqqigiariji.saqqilli_papattivik();
        else if (같음(0, "exit")) {
            if (piqujijjutiliriji_syntax.깊이 > 0) { 결과 = 토큰수 == 1 ? piqujijjutiliriji_syntax.qanuilinganiq_atuutilik : 셸도구.숫자(1); if (결과 < 0 || 결과 > 255) 결과 = 2; piqujijjutiliriji_syntax.pilirijjutiralaaq_isulittuq = true; }
            else if (보드.터미널(2) != 0) 터미널(true);
            else 단말.titiraq("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) aaqqigiarli_atuutilik();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (토큰수 < 2) { 결과 = 2; 단말.titiraq("사용법: rm ini...\n"); }
            for (int piliqqittaajuq_nalunaiqsimavik = 1; piliqqittaajuq_nalunaiqsimavik < 토큰수; piliqqittaajuq_nalunaiqsimavik++) { int 처리값 = aqqut(piliqqittaajuq_nalunaiqsimavik); if (처리값 == 0) 처리값 = 기억파일.지우기(); if (처리값 < 0) tammarniq(처리값); }
        }
        else if (같음(0, "echo")) {
            int 시작자리 = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = 시작자리; 첫값 < 토큰수; 첫값++) { if (첫값 > 시작자리) 단말.문자(32); for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < takininga_atuutilik[첫값]; piliqqittaajuq_nalunaiqsimavik++) 보드.직렬쓰기(토큰[시작점[첫값] + piliqqittaajuq_nalunaiqsimavik]); }
            if (시작자리 == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.titiraq("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? 파이썬꾸러미() : 도구(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !piqujijjutiliriji_syntax.연결중) { 단말.titiraq("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = 도구(13); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = 도구(15); 결과 = 처리값 < 0 ? 126 : 처리값; if (!piqujijjutiliriji_syntax.연결중) { 단말.titiraq("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = 도구(16); 결과 = 처리값 < 0 ? 126 : 처리값; if (!piqujijjutiliriji_syntax.연결중) { 단말.titiraq("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int anininga = 보드.터미널(13); 단말.titiraq("TERMINAL SIZE "); 단말.수(anininga & 65535); 단말.문자('x'); 단말.수(anininga >>> 16); 단말.문자(10); }
            else 터미널(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { 보드.터미널(9); igalaujaq.실행(); }
        else if (같음(0, "c")) kernel.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) kernel.작업시험();
        else if (같음(0, "g")) kernel.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) kernel.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = 보드.사용자실행(0); if (처리값 == 0) 단말.titiraq("ELF DEMO PASS\n"); else tammarniq(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? sanajjut_Iliniku(-2, 2) : 도구(-1); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !piqujijjutiliriji_syntax.연결중) { 단말.titiraq("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) kernel.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = 보드.ini_aullaaqtilli_pijittirut(1); if (처리값 < 0) tammarniq(처리값); else { 단말.titiraq("FTP listening "); qarasaujaq_sanajjut.titiraq_turaarut(보드.Kasuqatigiitsimajut_qanuilinganiq(0,0)); 단말.titiraq(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { 보드.ini_aullaaqtilli_pijittirut(0); 단말.titiraq("FTP stopped\n"); }
            else 단말.titiraq(보드.ini_aullaaqtilli_pijittirut(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { 꾸러미.Parnalli(); 단말.titiraq("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int pilirijjutinut_uqausiq = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (토큰수 != 2 || pilirijjutinut_uqausiq < 0) 단말.titiraq("example java|c|python: 출력, ini, 네트워크, 그래픽, Java Swing igalaangujaq 예제\n");
            else { int 처리값 = 예제꾸러미.ilili_atuutilik(pilirijjutinut_uqausiq); if (처리값 < 0) { tammarniq(처리값); if (처리값 == -28) 단말.titiraq("RAM full: remove unused files, then retry example\n"); } else 단말.titiraq("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int aaqqisurli_atuutilik = 실행형식();
            if (aaqqisurli_atuutilik == 1 || aaqqisurli_atuutilik == 2) {
                int 처리값 = sanajjut_Iliniku(aaqqisurli_atuutilik == 1 ? -1 : 14, 0); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !piqujijjutiliriji_syntax.연결중) { 단말.titiraq("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (aaqqisurli_atuutilik == 0) { 결과 = 126; 단말.titiraq("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { 결과 = 127; 단말.titiraq("Unknown command. help: commands\n"); }
        }
    }
    public static void 실행() {
        꾸러미.Parnalli();
        for (int pilirijjutinut_uqausiq = 0; pilirijjutinut_uqausiq < 3; pilirijjutinut_uqausiq++) { int 처리값 = 예제꾸러미.ilili_atuutilik(pilirijjutinut_uqausiq); if (처리값 < 0) tammarniq(처리값); }
        saqqilli_Ikajuqtau();
        while (true) {
            igalaangujaq_piliriaq.Pivallianiq_atuutilik_Iliniku(); if (igalaangujaq_piliriaq.재개()) continue;
            if (!igalaangujaq_piliriaq.이어읽기) 단말.titiraq("jkoros-native> "); titikutaak_aaqqigiariji.piqujivik = true; 보드.원격대기(1); int anininga = 줄읽기(); 보드.원격대기(0); titikutaak_aaqqigiariji.piqujivik = false;
            if (anininga == -3) continue;
            if (anininga == -2) 단말.titiraq("piqujijjut agguqtuut_atuutilik: 명령줄이 너무 깁니다\n");
            if (anininga >= 0) { piqujijjutiliriji_syntax.pilirijjutiralaaq_isulittuq = false; piqujijjutiliriji_syntax.실행(titikutaak, 0, anininga, 0); } else piqujijjutiliriji_syntax.qanuilinganiq_atuutilik = 130;
            보드.isulittuq_ungasittuq_piqujijjut(piqujijjutiliriji_syntax.qanuilinganiq_atuutilik);
            titikutaak_aaqqigiariji.anininga = titikutaak_aaqqigiariji.pigiarut_atuutilik = titikutaak_aaqqigiariji.pigiarli_igalaangujaq = 0;
        }
    }
}
