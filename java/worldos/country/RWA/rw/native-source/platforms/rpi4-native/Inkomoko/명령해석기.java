// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 interuro_y_ibwiriza. 따옴표, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] umurongo = new int[4096], tike_agaciro = new int[4096], 시작점 = new int[32], uburebure_agaciro = new int[32];
    static int[] 편집내용 = new int[16384], guhindura_izina = new int[63];
    static int 토큰수, guhindura_izina_uburebure, 결과;
    static boolean 앞줄;
    static void 원바이트(int agaciro) { 보드.직렬쓰기(agaciro); }
    static int 줄읽기() { return umurongo_Muhindura.읽기(); }
    static boolean 나누기(int Ingano) {
        int 위치 = 0, 끝 = 0; 토큰수 = 0;
        while (위치 < Ingano) {
            while (위치 < Ingano && (umurongo[위치] == 32 || umurongo[위치] == 9)) 위치++;
            if (위치 == Ingano) break;
            if (토큰수 == 16) { 단말.kwandika("Icyo_wifuza gusesengura_agaciro: 인수가 너무 많습니다\n"); return false; }
            시작점[토큰수] = 끝; int 인용 = 0;
            while (위치 < Ingano) {
                int agaciro = umurongo[위치++];
                if (인용 == 0 && (agaciro == 32 || agaciro == 9)) break;
                if (agaciro == 인용) { 인용 = 0; continue; }
                if (인용 == 0 && (agaciro == 39 || agaciro == 34)) { 인용 = agaciro; continue; }
                tike_agaciro[끝++] = agaciro;
            }
            if (인용 != 0) { 단말.kwandika("Icyo_wifuza gusesengura_agaciro: 따옴표가 닫히지 않았습니다\n"); return false; }
            uburebure_agaciro[토큰수] = 끝 - 시작점[토큰수]; 토큰수++;
        }
        return true;
    }
    static boolean 같음(int umugerekashakiro, String Ijambo_SMS) {
        if (umugerekashakiro >= 토큰수) return false;
        int 자리=0;
        for (int 순번=0; 순번<Ijambo_SMS.length(); 순번++) {
            int 문자값=Ijambo_SMS.charAt(순번);
            if (문자값>=0xd800 && 문자값<=0xdbff && 순번+1<Ijambo_SMS.length()) 문자값=0x10000+((문자값-0xd800)<<10)+Ijambo_SMS.charAt(++순번)-0xdc00;
            int 바이트수=문자값<128?1:문자값<2048?2:문자값<65536?3:4;
            for (int URUKURIKIRANE_agaciro=바이트수-1; URUKURIKIRANE_agaciro>=0; URUKURIKIRANE_agaciro--) {
                int agaciro=바이트수==1?문자값:URUKURIKIRANE_agaciro==바이트수-1?(바이트수==2?0xc0:바이트수==3?0xe0:0xf0)|(문자값>>(6*URUKURIKIRANE_agaciro)):0x80|((문자값>>(6*URUKURIKIRANE_agaciro))&63);
                if (자리>=uburebure_agaciro[umugerekashakiro] || tike_agaciro[시작점[umugerekashakiro]+자리++]!=agaciro) return false;
            }
        }
        return 자리==uburebure_agaciro[umugerekashakiro];
    }
    static int Inzira(int umugerekashakiro) {
        if (umugerekashakiro >= 토큰수) return -22;
        int 결과 = ububiko_Dosiye.inzira_Itangira(uburebure_agaciro[umugerekashakiro]); if (결과 < 0) return 결과;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < uburebure_agaciro[umugerekashakiro]; gukora_mu_matsinda_umugerekashakiro++) {
            결과 = ububiko_Dosiye.inzira_bayiti(gukora_mu_matsinda_umugerekashakiro, tike_agaciro[시작점[umugerekashakiro] + gukora_mu_matsinda_umugerekashakiro]); if (결과 < 0) return 결과;
        }
        return 0;
    }
    static void IKOSA(int umugerekashakiro) { 결과 = 1; 단말.kwandika("IKOSA "); 단말.수(umugerekashakiro); 단말.문자(10); }
    static void igaragaza_agaciro() {
        if (토큰수 != 2) { 단말.kwandika("사용법: cat Idosiye\n"); return; }
        int 결과 = Inzira(1); if (결과 < 0) { IKOSA(결과); return; }
        int Idosiye = ububiko_Dosiye.Gufungura(0); if (Idosiye < 0) { IKOSA(Idosiye); return; }
        while (true) { int agaciro = ububiko_Dosiye.읽기(Idosiye); if (agaciro == 256) break; if (agaciro < 0) { IKOSA(agaciro); break; } 원바이트(agaciro); }
        ububiko_Dosiye.Gufunga(Idosiye); 단말.문자(10);
    }
    static void guhindura_agaciro() {
        if (토큰수 != 2) { 단말.kwandika("사용법: edit Idosiye\n"); return; }
        int 결과 = Inzira(1); if (결과 < 0) { IKOSA(결과); return; }
        guhindura_izina_uburebure = uburebure_agaciro[1];
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < guhindura_izina_uburebure; gukora_mu_matsinda_umugerekashakiro++) guhindura_izina[gukora_mu_matsinda_umugerekashakiro] = tike_agaciro[시작점[1] + gukora_mu_matsinda_umugerekashakiro];
        단말.kwandika("EDIT: Idosiye 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Ingano = 0;
        while (true) {
            단말.kwandika("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.kwandika("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && umurongo[0] == '.') break;
            if (입력 + 1 > 편집내용.length - Ingano) { 단말.kwandika("EDIT CANCELLED: file too large\n"); return; }
            for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 입력; gukora_mu_matsinda_umugerekashakiro++) 편집내용[Ingano++] = umurongo[gukora_mu_matsinda_umugerekashakiro];
            편집내용[Ingano++] = 10;
        }
        ububiko_Dosiye.inzira_Itangira(guhindura_izina_uburebure);
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < guhindura_izina_uburebure; gukora_mu_matsinda_umugerekashakiro++) ububiko_Dosiye.inzira_bayiti(gukora_mu_matsinda_umugerekashakiro, guhindura_izina[gukora_mu_matsinda_umugerekashakiro]);
        int Idosiye = ububiko_Dosiye.Gufungura(577); if (Idosiye < 0) { IKOSA(Idosiye); return; }
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Ingano; gukora_mu_matsinda_umugerekashakiro++) ububiko_Dosiye.kwandika(Idosiye, 편집내용[gukora_mu_matsinda_umugerekashakiro]);
        ububiko_Dosiye.Gufunga(Idosiye); 단말.kwandika("SAVED "); 단말.수(Ingano); 단말.kwandika("bayiti_agaciro(주기억 Idosiye)\n");
    }
    static int 십육(int agaciro) {
        if (agaciro >= '0' && agaciro <= '9') return agaciro - '0';
        if (agaciro >= 'a' && agaciro <= 'f') return agaciro - 'a' + 10;
        if (agaciro >= 'A' && agaciro <= 'F') return agaciro - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (토큰수 != 2) { 단말.kwandika("사용법: load Idosiye | hex Idosiye\n"); return; }
        int 결과 = Inzira(1); if (결과 < 0) { IKOSA(결과); return; }
        if (!넣기) {
            int Idosiye = ububiko_Dosiye.Gufungura(0); if (Idosiye < 0) { IKOSA(Idosiye); return; }
            단말.kwandika("HEX BEGIN "); 단말.수(ububiko_Dosiye.Ingano(Idosiye)); 단말.문자(10);
            int 항목수 = 0;
            while (true) {
                int agaciro = ububiko_Dosiye.읽기(Idosiye); if (agaciro < 0 || agaciro == 256) break;
                단말.문자("0123456789abcdef".charAt(agaciro >> 4)); 단말.문자("0123456789abcdef".charAt(agaciro & 15));
                if (++항목수 % 32 == 0) 단말.문자(10);
            }
            if (항목수 % 32 != 0) 단말.문자(10);
            ububiko_Dosiye.Gufunga(Idosiye); 단말.kwandika("HEX END\n"); return;
        }
        guhindura_izina_uburebure = uburebure_agaciro[1];
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < guhindura_izina_uburebure; gukora_mu_matsinda_umugerekashakiro++) guhindura_izina[gukora_mu_matsinda_umugerekashakiro] = tike_agaciro[시작점[1] + gukora_mu_matsinda_umugerekashakiro];
        단말.kwandika("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Ingano = 0;
        while (true) {
            단말.kwandika("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.kwandika("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && umurongo[0] == '.') break;
            int 앞 = -1;
            for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 입력; gukora_mu_matsinda_umugerekashakiro++) {
                if (umurongo[gukora_mu_matsinda_umugerekashakiro] == 32 || umurongo[gukora_mu_matsinda_umugerekashakiro] == 9) continue;
                int agaciro = 십육(umurongo[gukora_mu_matsinda_umugerekashakiro]);
                if (agaciro < 0 || Ingano >= 편집내용.length) { 단말.kwandika("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = agaciro; else { 편집내용[Ingano++] = 앞 * 16 + agaciro; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.kwandika("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        ububiko_Dosiye.inzira_Itangira(guhindura_izina_uburebure);
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < guhindura_izina_uburebure; gukora_mu_matsinda_umugerekashakiro++) ububiko_Dosiye.inzira_bayiti(gukora_mu_matsinda_umugerekashakiro, guhindura_izina[gukora_mu_matsinda_umugerekashakiro]);
        int Idosiye = ububiko_Dosiye.Gufungura(577); if (Idosiye < 0) { IKOSA(Idosiye); return; }
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Ingano; gukora_mu_matsinda_umugerekashakiro++) ububiko_Dosiye.kwandika(Idosiye, 편집내용[gukora_mu_matsinda_umugerekashakiro]);
        ububiko_Dosiye.Gufunga(Idosiye); 단말.kwandika("LOADED "); 단말.수(Ingano); 단말.kwandika("bayiti_agaciro(주기억 Idosiye)\n");
    }
    static int Ibikoresho(int umugerekashakiro) {
        return igikoresho_icyinjizwa(umugerekashakiro, 1);
    }
    static int igikoresho_icyinjizwa(int umugerekashakiro, int ihuriro) {
        if (토큰수 - ihuriro > 8) return -22;
        보드.인수준비(토큰수 - ihuriro);
        for (int 첫값 = ihuriro; 첫값 < 토큰수; 첫값++) {
            if (uburebure_agaciro[첫값] > 255) return -36;
            for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < uburebure_agaciro[첫값]; gukora_mu_matsinda_umugerekashakiro++) 보드.ingingo_bayiti(첫값 - ihuriro, gukora_mu_matsinda_umugerekashakiro, tike_agaciro[시작점[첫값] + gukora_mu_matsinda_umugerekashakiro]);
        }
        return umugerekashakiro == -2 ? 보드.리눅스파일실행() : umugerekashakiro < 0 ? 보드.gukora_ukoresha_dosiye() : 보드.ihuriro_ukoresha_porogaramu(umugerekashakiro);
    }
    static int 파이썬꾸러미() {
        if (토큰수 > 8) return -22;
        보드.인수준비(토큰수);
        String Inzira = "/lib/ipaki.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int 자리 = 0;
        for (int 순번 = 0; 순번 < Inzira.length(); 순번++) {
            int inyuguti_agaciro = Inzira.charAt(순번);
            if (inyuguti_agaciro < 128) 보드.ingingo_bayiti(0, 자리++, inyuguti_agaciro);
            else { 보드.ingingo_bayiti(0, 자리++, 0xe0 | (inyuguti_agaciro >> 12)); 보드.ingingo_bayiti(0, 자리++, 0x80 | ((inyuguti_agaciro >> 6) & 63)); 보드.ingingo_bayiti(0, 자리++, 0x80 | (inyuguti_agaciro & 63)); }
        }
        for (int 순번 = 1; 순번 < 토큰수; 순번++) {
            if (uburebure_agaciro[순번] > 255) return -36;
            for (int inyuguti_agaciro = 0; inyuguti_agaciro < uburebure_agaciro[순번]; inyuguti_agaciro++) 보드.ingingo_bayiti(순번, inyuguti_agaciro, tike_agaciro[시작점[순번] + inyuguti_agaciro]);
        }
        return 보드.ihuriro_ukoresha_porogaramu(12);
    }
    static int 실행형식() {
        int 처리값 = Inzira(0); if (처리값 < 0) return 처리값;
        int Idosiye = ububiko_Dosiye.Gufungura(0); if (Idosiye < 0) return Idosiye;
        int 첫값 = ububiko_Dosiye.읽기(Idosiye), bayiti_amakurushingiro = ububiko_Dosiye.읽기(Idosiye), 문자값 = ububiko_Dosiye.읽기(Idosiye), 뒷값 = ububiko_Dosiye.읽기(Idosiye);
        ububiko_Dosiye.Gufunga(Idosiye);
        if (첫값 == 127 && bayiti_amakurushingiro == 'E' && 문자값 == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && bayiti_amakurushingiro == 'K' && 문자값 == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int umugerekashakiro, String 인수) {
        보드.인수준비(1);
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 인수.length(); gukora_mu_matsinda_umugerekashakiro++) 보드.ingingo_bayiti(0, gukora_mu_matsinda_umugerekashakiro, 인수.charAt(gukora_mu_matsinda_umugerekashakiro));
        return 보드.ihuriro_ukoresha_porogaramu(umugerekashakiro);
    }
    static void SMS_bayiti(int Idosiye, int agaciro) { ububiko_Dosiye.kwandika(Idosiye, agaciro); }
    static void kitayega_dosiye(String Izina, String Ibirimo_agaciro) {
        // ipaki 파일명은 ASCII. Idosiye 내용은 UTF-8로 저장한다.
        ububiko_Dosiye.inzira_Itangira(Izina.length());
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Izina.length(); gukora_mu_matsinda_umugerekashakiro++) ububiko_Dosiye.inzira_bayiti(gukora_mu_matsinda_umugerekashakiro, Izina.charAt(gukora_mu_matsinda_umugerekashakiro));
        int Idosiye = ububiko_Dosiye.Gufungura(193); if (Idosiye < 0) return;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Ibirimo_agaciro.length(); gukora_mu_matsinda_umugerekashakiro++) {
            int 문자값 = Ibirimo_agaciro.charAt(gukora_mu_matsinda_umugerekashakiro);
            if (문자값 >= 0xd800 && 문자값 <= 0xdbff && gukora_mu_matsinda_umugerekashakiro + 1 < Ibirimo_agaciro.length()) 문자값 = 0x10000 + ((문자값 - 0xd800) << 10) + Ibirimo_agaciro.charAt(++gukora_mu_matsinda_umugerekashakiro) - 0xdc00;
            if (문자값 < 128) SMS_bayiti(Idosiye, 문자값);
            else {
                int 수 = 문자값 < 2048 ? 2 : 문자값 < 65536 ? 3 : 4;
                SMS_bayiti(Idosiye, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (문자값 >> (6 * (수 - 1))));
                for (int 항목수 = 수 - 1; 항목수 > 0; 항목수--) SMS_bayiti(Idosiye, 0x80 | ((문자값 >> (6 * (항목수 - 1))) & 63));
            }
        }
        ububiko_Dosiye.Gufunga(Idosiye);
    }
    static void 한글도움말() {
        단말.kwandika("F9 / Shift+Space: [EN] ↔ [rw]\n");
        단말.kwandika("  [RW] keyboard; [EN] ASCII\n");
        단말.kwandika("  a → a\n");
        단말.kwandika("  F9: EN ↔ rw | Ctrl+Shift+V: UTF-8\n");
        단말.kwandika("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.kwandika("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Izina) {
        int 바이트수 = 0;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Izina.length(); gukora_mu_matsinda_umugerekashakiro++) { int 문자값 = Izina.charAt(gukora_mu_matsinda_umugerekashakiro); if (문자값 >= 0xd800 && 문자값 <= 0xdfff) return -22; 바이트수 += 문자값 < 128 ? 1 : 문자값 < 2048 ? 2 : 3; }
        int 처리값 = ububiko_Dosiye.inzira_Itangira(바이트수); if (처리값 < 0) return 처리값;
        int 자리 = 0;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < Izina.length(); gukora_mu_matsinda_umugerekashakiro++) {
            int 문자값 = Izina.charAt(gukora_mu_matsinda_umugerekashakiro);
            if (문자값 < 128) ububiko_Dosiye.inzira_bayiti(자리++, 문자값);
            else if (문자값 < 2048) { ububiko_Dosiye.inzira_bayiti(자리++, 0xc0 | (문자값 >> 6)); ububiko_Dosiye.inzira_bayiti(자리++, 0x80 | (문자값 & 63)); }
            else { ububiko_Dosiye.inzira_bayiti(자리++, 0xe0 | (문자값 >> 12)); ububiko_Dosiye.inzira_bayiti(자리++, 0x80 | ((문자값 >> 6) & 63)); ububiko_Dosiye.inzira_bayiti(자리++, 0x80 | (문자값 & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Izina) {
        int 처리값 = 예제경로(Izina); if (처리값 < 0) return 처리값;
        처리값 = ububiko_Dosiye.kurema_ububiko(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Izina, String amakurushingiro) {
        int 처리값 = 예제경로(Izina); if (처리값 < 0) return 처리값;
        int Idosiye = ububiko_Dosiye.Gufungura(193); if (Idosiye == -17) return 0; if (Idosiye < 0) return Idosiye;
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < amakurushingiro.length(); gukora_mu_matsinda_umugerekashakiro += 2) {
            처리값 = ububiko_Dosiye.kwandika(Idosiye, 십육(amakurushingiro.charAt(gukora_mu_matsinda_umugerekashakiro)) * 16 + 십육(amakurushingiro.charAt(gukora_mu_matsinda_umugerekashakiro + 1)));
            if (처리값 < 0) { ububiko_Dosiye.Gufunga(Idosiye); return 처리값; }
        }
        return ububiko_Dosiye.Gufunga(Idosiye);
    }
    static void kugaragaza_ifashayoboro() {
        sisitemu_igikoresho.kugaragaza_ifashayoboro();
        단말.kwandika("sshd / gitekanye_insomamabwiriza start|stop|status: SSH :22 (user, 장치별 ijambobanga_agaciro)\n");
        단말.kwandika("vncd / kure_kwerekana start|stop|status: VNC :5900 (장치별 ijambobanga_agaciro)\n");
        단말.kwandika("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.kwandika("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.kwandika("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.kwandika("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.kwandika("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.kwandika("모서리 + 왼쪽 버튼 kunyereza_agaciro: 터미널 Ingano guhindura_agaciro_16f64fe4; terminal size: inkingi_agaciro/umurongo_agaciro_fc48bc81\n");
        단말.kwandika("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.kwandika("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.kwandika("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.kwandika("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.kwandika("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.kwandika("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.kwandika("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.kwandika("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.kwandika("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.kwandika("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.kwandika("pip: MicroPython inkomoko_igiti kwinjiza_agaciro; gucumbikira --network --pip 필요; /lib는 RAM\n");
        단말.kwandika("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.kwandika("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.kwandika("/example/java /example/c /example/python: examples ready at boot\n");
        단말.kwandika("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void 터미널(boolean 전환여부) {
        if (전환여부 && 보드.터미널(2) != 0) { 보드.터미널(0); 단말.kwandika("TERMINAL CLOSED\n"); }
        else if (보드.터미널(1) < 0) IKOSA(-19);
        else 단말.kwandika("TERMINAL READY — rw terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Icyo_wifuza() {
        if (토큰수 == 0) return;
        if (sisitemu_igikoresho.gukora_ibwiriza()) return;
        if (같음(0,"sshd") || 같음(0,"gitekanye_insomamabwiriza") || 같음(0,"vncd") || 같음(0,"kure_kwerekana")) {
            int 종류=같음(0,"vncd")||같음(0,"kure_kwerekana")?1:0;
            int Igikorwa=같음(1,"start")||같음(1,"ihuriro")?1:같음(1,"stop")||같음(1,"Guhagarara")?0:2;
            int imimerere_agaciro=보드.icengera(종류,Igikorwa);
            if(imimerere_agaciro<0)IKOSA(imimerere_agaciro);else 단말.kwandika(보드.icengera(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else kugaragaza_ifashayoboro(); }
        else if (같음(0, "info") || 같음(0, "i")) intima.msinfo32_exe();
        else if (같음(0, "pwd")) { ububiko_Dosiye.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (토큰수 == 1) { ububiko_Dosiye.inzira_Itangira(1); 처리값 = ububiko_Dosiye.inzira_bayiti(0, '/'); } else 처리값 = 토큰수 == 2 ? Inzira(1) : -22;
            if (처리값 >= 0) 처리값 = ububiko_Dosiye.guhindura_ububiko(); if (처리값 < 0) IKOSA(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int ingingo_umugerekashakiro = 같음(1, "-l") ? 2 : 1, 처리값;
            if (토큰수 == ingingo_umugerekashakiro) { ububiko_Dosiye.inzira_Itangira(1); 처리값 = ububiko_Dosiye.inzira_bayiti(0, '.'); } else 처리값 = 토큰수 == ingingo_umugerekashakiro + 1 ? Inzira(ingingo_umugerekashakiro) : -22;
            if (처리값 >= 0) 처리값 = ububiko_Dosiye.경로목록(); if (처리값 < 0) IKOSA(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) insomamabwiriza_Ibikoresho.dosiye_ikibazo(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) insomamabwiriza_Ibikoresho.kopi_agaciro(같음(0, "mv"));
        else if (같음(0, "cat")) insomamabwiriza_Ibikoresho.igaragaza_agaciro();
        else if (같음(0, "wc")) insomamabwiriza_Ibikoresho.세기();
        else if (같음(0, "grep")) insomamabwiriza_Ibikoresho.gushaka_icyinjizwa();
        else if (같음(0, "head") || 같음(0, "tail")) insomamabwiriza_Ibikoresho.머리(같음(0, "tail"));
        else if (같음(0, "tee")) insomamabwiriza_Ibikoresho.함께쓰기();
        else if (같음(0, "env")) insomamabwiriza_interuro.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (토큰수 == 1) insomamabwiriza_interuro.환경보기();
            for (int gukora_mu_matsinda_umugerekashakiro = 1; gukora_mu_matsinda_umugerekashakiro < 토큰수; gukora_mu_matsinda_umugerekashakiro++) { int 처리값 = insomamabwiriza_interuro.환경설정(gukora_mu_matsinda_umugerekashakiro, 같음(0, "unset")); if (처리값 != 0) { 결과 = 처리값; 단말.kwandika("Icyo_wifuza gusesengura_agaciro: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) insomamabwiriza_interuro.gukora_dosiye();
        else if (같음(0, "true")) 결과 = 0;
        else if (같음(0, "false")) 결과 = 1;
        else if (같음(0, "history")) umurongo_Muhindura.kugaragaza_kubika();
        else if (같음(0, "exit")) {
            if (insomamabwiriza_interuro.깊이 > 0) { 결과 = 토큰수 == 1 ? insomamabwiriza_interuro.imimerere_agaciro : insomamabwiriza_Ibikoresho.umubare_agaciro(1); if (결과 < 0 || 결과 > 255) 결과 = 2; insomamabwiriza_interuro.sikiributi_kurangiza = true; }
            else if (보드.터미널(2) != 0) 터미널(true);
            else 단말.kwandika("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) guhindura_agaciro();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (토큰수 < 2) { 결과 = 2; 단말.kwandika("사용법: rm Idosiye...\n"); }
            for (int gukora_mu_matsinda_umugerekashakiro = 1; gukora_mu_matsinda_umugerekashakiro < 토큰수; gukora_mu_matsinda_umugerekashakiro++) { int 처리값 = Inzira(gukora_mu_matsinda_umugerekashakiro); if (처리값 == 0) 처리값 = ububiko_Dosiye.지우기(); if (처리값 < 0) IKOSA(처리값); }
        }
        else if (같음(0, "echo")) {
            int 시작자리 = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = 시작자리; 첫값 < 토큰수; 첫값++) { if (첫값 > 시작자리) 단말.문자(32); for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < uburebure_agaciro[첫값]; gukora_mu_matsinda_umugerekashakiro++) 보드.직렬쓰기(tike_agaciro[시작점[첫값] + gukora_mu_matsinda_umugerekashakiro]); }
            if (시작자리 == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.kwandika("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? 파이썬꾸러미() : Ibikoresho(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !insomamabwiriza_interuro.연결중) { 단말.kwandika("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Ibikoresho(13); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Ibikoresho(15); 결과 = 처리값 < 0 ? 126 : 처리값; if (!insomamabwiriza_interuro.연결중) { 단말.kwandika("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Ibikoresho(16); 결과 = 처리값 < 0 ? 126 : 처리값; if (!insomamabwiriza_interuro.연결중) { 단말.kwandika("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Ingano = 보드.터미널(13); 단말.kwandika("TERMINAL SIZE "); 단말.수(Ingano & 65535); 단말.문자('x'); 단말.수(Ingano >>> 16); 단말.문자(10); }
            else 터미널(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { 보드.터미널(9); biro.gukora_ibwiriza(); }
        else if (같음(0, "c")) intima.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) intima.작업시험();
        else if (같음(0, "g")) intima.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) intima.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = 보드.ihuriro_ukoresha_porogaramu(0); if (처리값 == 0) 단말.kwandika("ELF DEMO PASS\n"); else IKOSA(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? igikoresho_icyinjizwa(-2, 2) : Ibikoresho(-1); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !insomamabwiriza_interuro.연결중) { 단말.kwandika("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) intima.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = 보드.dosiye_iyimura_serivisi(1); if (처리값 < 0) IKOSA(처리값); else { 단말.kwandika("FTP listening "); sisitemu_igikoresho.kwandika_aderesi(보드.Urusobemiyoboro_imimerere(0,0)); 단말.kwandika(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { 보드.dosiye_iyimura_serivisi(0); 단말.kwandika("FTP stopped\n"); }
            else 단말.kwandika(보드.dosiye_iyimura_serivisi(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { ipaki.Gutegura(); 단말.kwandika("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Ururimi = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (토큰수 != 2 || Ururimi < 0) 단말.kwandika("example java|c|python: 출력, Idosiye, 네트워크, 그래픽, Java Swing idirishya 예제\n");
            else { int 처리값 = 예제꾸러미.kwinjiza_agaciro(Ururimi); if (처리값 < 0) { IKOSA(처리값); if (처리값 == -28) 단말.kwandika("RAM full: remove unused files, then retry example\n"); } else 단말.kwandika("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int imiterere_agaciro = 실행형식();
            if (imiterere_agaciro == 1 || imiterere_agaciro == 2) {
                int 처리값 = igikoresho_icyinjizwa(imiterere_agaciro == 1 ? -1 : 14, 0); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !insomamabwiriza_interuro.연결중) { 단말.kwandika("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (imiterere_agaciro == 0) { 결과 = 126; 단말.kwandika("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { 결과 = 127; 단말.kwandika("Unknown command. help: commands\n"); }
        }
    }
    public static void gukora_ibwiriza() {
        ipaki.Gutegura();
        for (int Ururimi = 0; Ururimi < 3; Ururimi++) { int 처리값 = 예제꾸러미.kwinjiza_agaciro(Ururimi); if (처리값 < 0) IKOSA(처리값); }
        kugaragaza_ifashayoboro();
        while (true) {
            idirishya_kwihuza.Inzira_agaciro_icyinjizwa(); if (idirishya_kwihuza.재개()) continue;
            if (!idirishya_kwihuza.이어읽기) 단말.kwandika("jkoros-native> "); umurongo_Muhindura.interuro_y_ibwiriza = true; 보드.원격대기(1); int Ingano = 줄읽기(); 보드.원격대기(0); umurongo_Muhindura.interuro_y_ibwiriza = false;
            if (Ingano == -3) continue;
            if (Ingano == -2) 단말.kwandika("Icyo_wifuza gusesengura_agaciro: 명령줄이 너무 깁니다\n");
            if (Ingano >= 0) { insomamabwiriza_interuro.sikiributi_kurangiza = false; insomamabwiriza_interuro.gukora_ibwiriza(umurongo, 0, Ingano, 0); } else insomamabwiriza_interuro.imimerere_agaciro = 130;
            보드.kurangiza_kure_ibwiriza(insomamabwiriza_interuro.imimerere_agaciro);
            umurongo_Muhindura.Ingano = umurongo_Muhindura.inyoboranyandika_agaciro = umurongo_Muhindura.Itangira_idirishya = 0;
        }
    }
}
