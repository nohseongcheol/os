// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 umugqa_wemiyalo. 따옴표, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] umugqa = new int[4096], ithokhini_inani = new int[4096], 시작점 = new int[32], ubude_inani = new int[32];
    static int[] 편집내용 = new int[16384], hlela_igama = new int[63];
    static int 토큰수, hlela_igama_ubude, 결과;
    static boolean 앞줄;
    static void 원바이트(int inani) { 보드.직렬쓰기(inani); }
    static int 줄읽기() { return umugqa_Umhleli.Funda(); }
    static boolean 나누기(int Ubungako) {
        int 위치 = 0, 끝 = 0; 토큰수 = 0;
        while (위치 < Ubungako) {
            while (위치 < Ubungako && (umugqa[위치] == 32 || umugqa[위치] == 9)) 위치++;
            if (위치 == Ubungako) break;
            if (토큰수 == 16) { 단말.Bhala("Umlayelo zawula_inani: 인수가 너무 많습니다\n"); return false; }
            시작점[토큰수] = 끝; int 인용 = 0;
            while (위치 < Ubungako) {
                int inani = umugqa[위치++];
                if (인용 == 0 && (inani == 32 || inani == 9)) break;
                if (inani == 인용) { 인용 = 0; continue; }
                if (인용 == 0 && (inani == 39 || inani == 34)) { 인용 = inani; continue; }
                ithokhini_inani[끝++] = inani;
            }
            if (인용 != 0) { 단말.Bhala("Umlayelo zawula_inani: 따옴표가 닫히지 않았습니다\n"); return false; }
            ubude_inani[토큰수] = 끝 - 시작점[토큰수]; 토큰수++;
        }
        return true;
    }
    static boolean 같음(int thola_inkomba, String Amagama_I_SMS) {
        if (thola_inkomba >= 토큰수) return false;
        int 자리=0;
        for (int 순번=0; 순번<Amagama_I_SMS.length(); 순번++) {
            int ikhodi_yohlamvu=Amagama_I_SMS.charAt(순번);
            if (ikhodi_yohlamvu>=0xd800 && ikhodi_yohlamvu<=0xdbff && 순번+1<Amagama_I_SMS.length()) ikhodi_yohlamvu=0x10000+((ikhodi_yohlamvu-0xd800)<<10)+Amagama_I_SMS.charAt(++순번)-0xdc00;
            int 바이트수=ikhodi_yohlamvu<128?1:ikhodi_yohlamvu<2048?2:ikhodi_yohlamvu<65536?3:4;
            for (int UKULANDELANA_inani=바이트수-1; UKULANDELANA_inani>=0; UKULANDELANA_inani--) {
                int inani=바이트수==1?ikhodi_yohlamvu:UKULANDELANA_inani==바이트수-1?(바이트수==2?0xc0:바이트수==3?0xe0:0xf0)|(ikhodi_yohlamvu>>(6*UKULANDELANA_inani)):0x80|((ikhodi_yohlamvu>>(6*UKULANDELANA_inani))&63);
                if (자리>=ubude_inani[thola_inkomba] || ithokhini_inani[시작점[thola_inkomba]+자리++]!=inani) return false;
            }
        }
        return 자리==ubude_inani[thola_inkomba];
    }
    static int Indlela_2(int thola_inkomba) {
        if (thola_inkomba >= 토큰수) return -22;
        int 결과 = inkumbulo_Amafayela.umzila_qala(ubude_inani[thola_inkomba]); if (결과 < 0) return 결과;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < ubude_inani[thola_inkomba]; iluphu_thola_inkomba++) {
            결과 = inkumbulo_Amafayela.umzila_ibhayithi(iluphu_thola_inkomba, ithokhini_inani[시작점[thola_inkomba] + iluphu_thola_inkomba]); if (결과 < 0) return 결과;
        }
        return 0;
    }
    static void Iphutha(int thola_inkomba) { 결과 = 1; 단말.Bhala("Iphutha "); 단말.수(thola_inkomba); 단말.문자(10); }
    static void buka_inani() {
        if (토큰수 != 2) { 단말.Bhala("사용법: cat Ihele\n"); return; }
        int 결과 = Indlela_2(1); if (결과 < 0) { Iphutha(결과); return; }
        int Ihele = inkumbulo_Amafayela.Vula(0); if (Ihele < 0) { Iphutha(Ihele); return; }
        while (true) { int inani = inkumbulo_Amafayela.Funda(Ihele); if (inani == 256) break; if (inani < 0) { Iphutha(inani); break; } 원바이트(inani); }
        inkumbulo_Amafayela.Vala(Ihele); 단말.문자(10);
    }
    static void hlela_inani() {
        if (토큰수 != 2) { 단말.Bhala("사용법: edit Ihele\n"); return; }
        int 결과 = Indlela_2(1); if (결과 < 0) { Iphutha(결과); return; }
        hlela_igama_ubude = ubude_inani[1];
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < hlela_igama_ubude; iluphu_thola_inkomba++) hlela_igama[iluphu_thola_inkomba] = ithokhini_inani[시작점[1] + iluphu_thola_inkomba];
        단말.Bhala("EDIT: Ihele 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Ubungako = 0;
        while (true) {
            단말.Bhala("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Bhala("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && umugqa[0] == '.') break;
            if (입력 + 1 > 편집내용.length - Ubungako) { 단말.Bhala("EDIT CANCELLED: file too large\n"); return; }
            for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 입력; iluphu_thola_inkomba++) 편집내용[Ubungako++] = umugqa[iluphu_thola_inkomba];
            편집내용[Ubungako++] = 10;
        }
        inkumbulo_Amafayela.umzila_qala(hlela_igama_ubude);
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < hlela_igama_ubude; iluphu_thola_inkomba++) inkumbulo_Amafayela.umzila_ibhayithi(iluphu_thola_inkomba, hlela_igama[iluphu_thola_inkomba]);
        int Ihele = inkumbulo_Amafayela.Vula(577); if (Ihele < 0) { Iphutha(Ihele); return; }
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Ubungako; iluphu_thola_inkomba++) inkumbulo_Amafayela.Bhala(Ihele, 편집내용[iluphu_thola_inkomba]);
        inkumbulo_Amafayela.Vala(Ihele); 단말.Bhala("SAVED "); 단말.수(Ubungako); 단말.Bhala("ibhayithi_inani(주기억 Ihele)\n");
    }
    static int 십육(int inani) {
        if (inani >= '0' && inani <= '9') return inani - '0';
        if (inani >= 'a' && inani <= 'f') return inani - 'a' + 10;
        if (inani >= 'A' && inani <= 'F') return inani - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (토큰수 != 2) { 단말.Bhala("사용법: load Ihele | hex Ihele\n"); return; }
        int 결과 = Indlela_2(1); if (결과 < 0) { Iphutha(결과); return; }
        if (!넣기) {
            int Ihele = inkumbulo_Amafayela.Vula(0); if (Ihele < 0) { Iphutha(Ihele); return; }
            단말.Bhala("HEX BEGIN "); 단말.수(inkumbulo_Amafayela.Ubungako(Ihele)); 단말.문자(10);
            int 항목수 = 0;
            while (true) {
                int inani = inkumbulo_Amafayela.Funda(Ihele); if (inani < 0 || inani == 256) break;
                단말.문자("0123456789abcdef".charAt(inani >> 4)); 단말.문자("0123456789abcdef".charAt(inani & 15));
                if (++항목수 % 32 == 0) 단말.문자(10);
            }
            if (항목수 % 32 != 0) 단말.문자(10);
            inkumbulo_Amafayela.Vala(Ihele); 단말.Bhala("HEX END\n"); return;
        }
        hlela_igama_ubude = ubude_inani[1];
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < hlela_igama_ubude; iluphu_thola_inkomba++) hlela_igama[iluphu_thola_inkomba] = ithokhini_inani[시작점[1] + iluphu_thola_inkomba];
        단말.Bhala("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Ubungako = 0;
        while (true) {
            단말.Bhala("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Bhala("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && umugqa[0] == '.') break;
            int 앞 = -1;
            for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 입력; iluphu_thola_inkomba++) {
                if (umugqa[iluphu_thola_inkomba] == 32 || umugqa[iluphu_thola_inkomba] == 9) continue;
                int inani = 십육(umugqa[iluphu_thola_inkomba]);
                if (inani < 0 || Ubungako >= 편집내용.length) { 단말.Bhala("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = inani; else { 편집내용[Ubungako++] = 앞 * 16 + inani; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.Bhala("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        inkumbulo_Amafayela.umzila_qala(hlela_igama_ubude);
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < hlela_igama_ubude; iluphu_thola_inkomba++) inkumbulo_Amafayela.umzila_ibhayithi(iluphu_thola_inkomba, hlela_igama[iluphu_thola_inkomba]);
        int Ihele = inkumbulo_Amafayela.Vula(577); if (Ihele < 0) { Iphutha(Ihele); return; }
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Ubungako; iluphu_thola_inkomba++) inkumbulo_Amafayela.Bhala(Ihele, 편집내용[iluphu_thola_inkomba]);
        inkumbulo_Amafayela.Vala(Ihele); 단말.Bhala("LOADED "); 단말.수(Ubungako); 단말.Bhala("ibhayithi_inani(주기억 Ihele)\n");
    }
    static int Amathuluzi(int thola_inkomba) {
        return ithuluzi_okufakwayo(thola_inkomba, 1);
    }
    static int ithuluzi_okufakwayo(int thola_inkomba, int Sebenzisa) {
        if (토큰수 - Sebenzisa > 8) return -22;
        보드.인수준비(토큰수 - Sebenzisa);
        for (int 첫값 = Sebenzisa; 첫값 < 토큰수; 첫값++) {
            if (ubude_inani[첫값] > 255) return -36;
            for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < ubude_inani[첫값]; iluphu_thola_inkomba++) 보드.i_agumenti_ibhayithi(첫값 - Sebenzisa, iluphu_thola_inkomba, ithokhini_inani[시작점[첫값] + iluphu_thola_inkomba]);
        }
        return thola_inkomba == -2 ? 보드.리눅스파일실행() : thola_inkomba < 0 ? 보드.yenza_umsebenzisi_ifayela() : 보드.sebenzisa_umsebenzisi_i_app(thola_inkomba);
    }
    static int 파이썬꾸러미() {
        if (토큰수 > 8) return -22;
        보드.인수준비(토큰수);
        String Indlela_2 = "/lib/isigaxa.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int 자리 = 0;
        for (int 순번 = 0; 순번 < Indlela_2.length(); 순번++) {
            int uhlamvusimo_inani = Indlela_2.charAt(순번);
            if (uhlamvusimo_inani < 128) 보드.i_agumenti_ibhayithi(0, 자리++, uhlamvusimo_inani);
            else { 보드.i_agumenti_ibhayithi(0, 자리++, 0xe0 | (uhlamvusimo_inani >> 12)); 보드.i_agumenti_ibhayithi(0, 자리++, 0x80 | ((uhlamvusimo_inani >> 6) & 63)); 보드.i_agumenti_ibhayithi(0, 자리++, 0x80 | (uhlamvusimo_inani & 63)); }
        }
        for (int 순번 = 1; 순번 < 토큰수; 순번++) {
            if (ubude_inani[순번] > 255) return -36;
            for (int uhlamvusimo_inani = 0; uhlamvusimo_inani < ubude_inani[순번]; uhlamvusimo_inani++) 보드.i_agumenti_ibhayithi(순번, uhlamvusimo_inani, ithokhini_inani[시작점[순번] + uhlamvusimo_inani]);
        }
        return 보드.sebenzisa_umsebenzisi_i_app(12);
    }
    static int 실행형식() {
        int 처리값 = Indlela_2(0); if (처리값 < 0) return 처리값;
        int Ihele = inkumbulo_Amafayela.Vula(0); if (Ihele < 0) return Ihele;
        int 첫값 = inkumbulo_Amafayela.Funda(Ihele), ibhayithi_imininingwane = inkumbulo_Amafayela.Funda(Ihele), ikhodi_yohlamvu = inkumbulo_Amafayela.Funda(Ihele), 뒷값 = inkumbulo_Amafayela.Funda(Ihele);
        inkumbulo_Amafayela.Vala(Ihele);
        if (첫값 == 127 && ibhayithi_imininingwane == 'E' && ikhodi_yohlamvu == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && ibhayithi_imininingwane == 'K' && ikhodi_yohlamvu == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int thola_inkomba, String 인수) {
        보드.인수준비(1);
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 인수.length(); iluphu_thola_inkomba++) 보드.i_agumenti_ibhayithi(0, iluphu_thola_inkomba, 인수.charAt(iluphu_thola_inkomba));
        return 보드.sebenzisa_umsebenzisi_i_app(thola_inkomba);
    }
    static void I_SMS_ibhayithi(int Ihele, int inani) { inkumbulo_Amafayela.Bhala(Ihele, inani); }
    static void ngaguquki_ifayela(String Igama, String Okuqukethwe_inani) {
        // isigaxa 파일명은 ASCII. Ihele 내용은 UTF-8로 저장한다.
        inkumbulo_Amafayela.umzila_qala(Igama.length());
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Igama.length(); iluphu_thola_inkomba++) inkumbulo_Amafayela.umzila_ibhayithi(iluphu_thola_inkomba, Igama.charAt(iluphu_thola_inkomba));
        int Ihele = inkumbulo_Amafayela.Vula(193); if (Ihele < 0) return;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Okuqukethwe_inani.length(); iluphu_thola_inkomba++) {
            int ikhodi_yohlamvu = Okuqukethwe_inani.charAt(iluphu_thola_inkomba);
            if (ikhodi_yohlamvu >= 0xd800 && ikhodi_yohlamvu <= 0xdbff && iluphu_thola_inkomba + 1 < Okuqukethwe_inani.length()) ikhodi_yohlamvu = 0x10000 + ((ikhodi_yohlamvu - 0xd800) << 10) + Okuqukethwe_inani.charAt(++iluphu_thola_inkomba) - 0xdc00;
            if (ikhodi_yohlamvu < 128) I_SMS_ibhayithi(Ihele, ikhodi_yohlamvu);
            else {
                int 수 = ikhodi_yohlamvu < 2048 ? 2 : ikhodi_yohlamvu < 65536 ? 3 : 4;
                I_SMS_ibhayithi(Ihele, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (ikhodi_yohlamvu >> (6 * (수 - 1))));
                for (int 항목수 = 수 - 1; 항목수 > 0; 항목수--) I_SMS_ibhayithi(Ihele, 0x80 | ((ikhodi_yohlamvu >> (6 * (항목수 - 1))) & 63));
            }
        }
        inkumbulo_Amafayela.Vala(Ihele);
    }
    static void 한글도움말() {
        단말.Bhala("F9 / Shift+Space: [EN] ↔ [zu]\n");
        단말.Bhala("  [ZU] keyboard; [EN] ASCII\n");
        단말.Bhala("  a → a\n");
        단말.Bhala("  F9: EN ↔ zu | Ctrl+Shift+V: UTF-8\n");
        단말.Bhala("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Bhala("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Igama) {
        int 바이트수 = 0;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Igama.length(); iluphu_thola_inkomba++) { int ikhodi_yohlamvu = Igama.charAt(iluphu_thola_inkomba); if (ikhodi_yohlamvu >= 0xd800 && ikhodi_yohlamvu <= 0xdfff) return -22; 바이트수 += ikhodi_yohlamvu < 128 ? 1 : ikhodi_yohlamvu < 2048 ? 2 : 3; }
        int 처리값 = inkumbulo_Amafayela.umzila_qala(바이트수); if (처리값 < 0) return 처리값;
        int 자리 = 0;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Igama.length(); iluphu_thola_inkomba++) {
            int ikhodi_yohlamvu = Igama.charAt(iluphu_thola_inkomba);
            if (ikhodi_yohlamvu < 128) inkumbulo_Amafayela.umzila_ibhayithi(자리++, ikhodi_yohlamvu);
            else if (ikhodi_yohlamvu < 2048) { inkumbulo_Amafayela.umzila_ibhayithi(자리++, 0xc0 | (ikhodi_yohlamvu >> 6)); inkumbulo_Amafayela.umzila_ibhayithi(자리++, 0x80 | (ikhodi_yohlamvu & 63)); }
            else { inkumbulo_Amafayela.umzila_ibhayithi(자리++, 0xe0 | (ikhodi_yohlamvu >> 12)); inkumbulo_Amafayela.umzila_ibhayithi(자리++, 0x80 | ((ikhodi_yohlamvu >> 6) & 63)); inkumbulo_Amafayela.umzila_ibhayithi(자리++, 0x80 | (ikhodi_yohlamvu & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Igama) {
        int 처리값 = 예제경로(Igama); if (처리값 < 0) return 처리값;
        처리값 = inkumbulo_Amafayela.yakha_umkhombandlela(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Igama, String imininingwane) {
        int 처리값 = 예제경로(Igama); if (처리값 < 0) return 처리값;
        int Ihele = inkumbulo_Amafayela.Vula(193); if (Ihele == -17) return 0; if (Ihele < 0) return Ihele;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < imininingwane.length(); iluphu_thola_inkomba += 2) {
            처리값 = inkumbulo_Amafayela.Bhala(Ihele, 십육(imininingwane.charAt(iluphu_thola_inkomba)) * 16 + 십육(imininingwane.charAt(iluphu_thola_inkomba + 1)));
            if (처리값 < 0) { inkumbulo_Amafayela.Vala(Ihele); return 처리값; }
        }
        return inkumbulo_Amafayela.Vala(Ihele);
    }
    static void khombisa_usizo() {
        isistimu_ithuluzi.khombisa_usizo();
        단말.Bhala("sshd / ivikelekile_isihumushi_miyalelo start|stop|status: SSH :22 (user, 장치별 iphasiwedi_inani)\n");
        단말.Bhala("vncd / kude_bonisa start|stop|status: VNC :5900 (장치별 iphasiwedi_inani)\n");
        단말.Bhala("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Bhala("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Bhala("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Bhala("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Bhala("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Bhala("모서리 + 왼쪽 버튼 donsa_inani: 터미널 Ubungako guqula_inani; terminal size: ikholomu_inani/umugqa_inani\n");
        단말.Bhala("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Bhala("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Bhala("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Bhala("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Bhala("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Bhala("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Bhala("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Bhala("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Bhala("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Bhala("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Bhala("pip: MicroPython umthombo_isihlahla faka_inani; singatha --network --pip 필요; /lib는 RAM\n");
        단말.Bhala("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Bhala("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Bhala("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Bhala("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void 터미널(boolean 전환여부) {
        if (전환여부 && 보드.터미널(2) != 0) { 보드.터미널(0); 단말.Bhala("TERMINAL CLOSED\n"); }
        else if (보드.터미널(1) < 0) Iphutha(-19);
        else 단말.Bhala("TERMINAL READY — zu terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Umlayelo() {
        if (토큰수 == 0) return;
        if (isistimu_ithuluzi.yenza_umyalo()) return;
        if (같음(0,"sshd") || 같음(0,"ivikelekile_isihumushi_miyalelo") || 같음(0,"vncd") || 같음(0,"kude_bonisa")) {
            int 종류=같음(0,"vncd")||같음(0,"kude_bonisa")?1:0;
            int Isenzo=같음(1,"start")||같음(1,"Sebenzisa")?1:같음(1,"stop")||같음(1,"Ima")?0:2;
            int isimo_inani=보드.ukulawula_ukude(종류,Isenzo);
            if(isimo_inani<0)Iphutha(isimo_inani);else 단말.Bhala(보드.ukulawula_ukude(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else khombisa_usizo(); }
        else if (같음(0, "info") || 같음(0, "i")) ikhenela.I_msinfo32_exe();
        else if (같음(0, "pwd")) { inkumbulo_Amafayela.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (토큰수 == 1) { inkumbulo_Amafayela.umzila_qala(1); 처리값 = inkumbulo_Amafayela.umzila_ibhayithi(0, '/'); } else 처리값 = 토큰수 == 2 ? Indlela_2(1) : -22;
            if (처리값 >= 0) 처리값 = inkumbulo_Amafayela.guqula_umkhombandlela(); if (처리값 < 0) Iphutha(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int i_agumenti_thola_inkomba = 같음(1, "-l") ? 2 : 1, 처리값;
            if (토큰수 == i_agumenti_thola_inkomba) { inkumbulo_Amafayela.umzila_qala(1); 처리값 = inkumbulo_Amafayela.umzila_ibhayithi(0, '.'); } else 처리값 = 토큰수 == i_agumenti_thola_inkomba + 1 ? Indlela_2(i_agumenti_thola_inkomba) : -22;
            if (처리값 >= 0) 처리값 = inkumbulo_Amafayela.경로목록(); if (처리값 < 0) Iphutha(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) isihumushi_miyalelo_Amathuluzi.ifayela_udaba(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) isihumushi_miyalelo_Amathuluzi.kopisha_inani(같음(0, "mv"));
        else if (같음(0, "cat")) isihumushi_miyalelo_Amathuluzi.buka_inani();
        else if (같음(0, "wc")) isihumushi_miyalelo_Amathuluzi.세기();
        else if (같음(0, "grep")) isihumushi_miyalelo_Amathuluzi.thola_okufakwayo();
        else if (같음(0, "head") || 같음(0, "tail")) isihumushi_miyalelo_Amathuluzi.머리(같음(0, "tail"));
        else if (같음(0, "tee")) isihumushi_miyalelo_Amathuluzi.함께쓰기();
        else if (같음(0, "env")) isihumushi_miyalelo_uhlelo_miyalelo.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (토큰수 == 1) isihumushi_miyalelo_uhlelo_miyalelo.환경보기();
            for (int iluphu_thola_inkomba = 1; iluphu_thola_inkomba < 토큰수; iluphu_thola_inkomba++) { int 처리값 = isihumushi_miyalelo_uhlelo_miyalelo.환경설정(iluphu_thola_inkomba, 같음(0, "unset")); if (처리값 != 0) { 결과 = 처리값; 단말.Bhala("Umlayelo zawula_inani: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) isihumushi_miyalelo_uhlelo_miyalelo.yenza_ifayela();
        else if (같음(0, "true")) 결과 = 0;
        else if (같음(0, "false")) 결과 = 1;
        else if (같음(0, "history")) umugqa_Umhleli.khombisa_loga();
        else if (같음(0, "exit")) {
            if (isihumushi_miyalelo_uhlelo_miyalelo.깊이 > 0) { 결과 = 토큰수 == 1 ? isihumushi_miyalelo_uhlelo_miyalelo.isimo_inani : isihumushi_miyalelo_Amathuluzi.idijithi_inani(1); if (결과 < 0 || 결과 > 255) 결과 = 2; isihumushi_miyalelo_uhlelo_miyalelo.uhlelosiluleko_yekisa = true; }
            else if (보드.터미널(2) != 0) 터미널(true);
            else 단말.Bhala("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) hlela_inani();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (토큰수 < 2) { 결과 = 2; 단말.Bhala("사용법: rm Ihele...\n"); }
            for (int iluphu_thola_inkomba = 1; iluphu_thola_inkomba < 토큰수; iluphu_thola_inkomba++) { int 처리값 = Indlela_2(iluphu_thola_inkomba); if (처리값 == 0) 처리값 = inkumbulo_Amafayela.지우기(); if (처리값 < 0) Iphutha(처리값); }
        }
        else if (같음(0, "echo")) {
            int 시작자리 = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = 시작자리; 첫값 < 토큰수; 첫값++) { if (첫값 > 시작자리) 단말.문자(32); for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < ubude_inani[첫값]; iluphu_thola_inkomba++) 보드.직렬쓰기(ithokhini_inani[시작점[첫값] + iluphu_thola_inkomba]); }
            if (시작자리 == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Bhala("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? 파이썬꾸러미() : Amathuluzi(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !isihumushi_miyalelo_uhlelo_miyalelo.연결중) { 단말.Bhala("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Amathuluzi(13); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Amathuluzi(15); 결과 = 처리값 < 0 ? 126 : 처리값; if (!isihumushi_miyalelo_uhlelo_miyalelo.연결중) { 단말.Bhala("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Amathuluzi(16); 결과 = 처리값 < 0 ? 126 : 처리값; if (!isihumushi_miyalelo_uhlelo_miyalelo.연결중) { 단말.Bhala("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Ubungako = 보드.터미널(13); 단말.Bhala("TERMINAL SIZE "); 단말.수(Ubungako & 65535); 단말.문자('x'); 단말.수(Ubungako >>> 16); 단말.문자(10); }
            else 터미널(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { 보드.터미널(9); ideskithophu.yenza_umyalo(); }
        else if (같음(0, "c")) ikhenela.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) ikhenela.작업시험();
        else if (같음(0, "g")) ikhenela.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) ikhenela.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = 보드.sebenzisa_umsebenzisi_i_app(0); if (처리값 == 0) 단말.Bhala("ELF DEMO PASS\n"); else Iphutha(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? ithuluzi_okufakwayo(-2, 2) : Amathuluzi(-1); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !isihumushi_miyalelo_uhlelo_miyalelo.연결중) { 단말.Bhala("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) ikhenela.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = 보드.ifayela_dlulisa_insiza(1); if (처리값 < 0) Iphutha(처리값); else { 단말.Bhala("FTP listening "); isistimu_ithuluzi.bhala_ikheli(보드.iNethiwekhi_isimo(0,0)); 단말.Bhala(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { 보드.ifayela_dlulisa_insiza(0); 단말.Bhala("FTP stopped\n"); }
            else 단말.Bhala(보드.ifayela_dlulisa_insiza(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { isigaxa.Hlela(); 단말.Bhala("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Ulimi = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (토큰수 != 2 || Ulimi < 0) 단말.Bhala("example java|c|python: 출력, Ihele, 네트워크, 그래픽, Java Swing ifasitela 예제\n");
            else { int 처리값 = 예제꾸러미.faka_inani(Ulimi); if (처리값 < 0) { Iphutha(처리값); if (처리값 == -28) 단말.Bhala("RAM full: remove unused files, then retry example\n"); } else 단말.Bhala("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int misa_inani = 실행형식();
            if (misa_inani == 1 || misa_inani == 2) {
                int 처리값 = ithuluzi_okufakwayo(misa_inani == 1 ? -1 : 14, 0); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !isihumushi_miyalelo_uhlelo_miyalelo.연결중) { 단말.Bhala("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (misa_inani == 0) { 결과 = 126; 단말.Bhala("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { 결과 = 127; 단말.Bhala("Unknown command. help: commands\n"); }
        }
    }
    public static void yenza_umyalo() {
        isigaxa.Hlela();
        for (int Ulimi = 0; Ulimi < 3; Ulimi++) { int 처리값 = 예제꾸러미.faka_inani(Ulimi); if (처리값 < 0) Iphutha(처리값); }
        khombisa_usizo();
        while (true) {
            ifasitela_isikhathi_sokwenza.Inqubo_inani_okufakwayo(); if (ifasitela_isikhathi_sokwenza.재개()) continue;
            if (!ifasitela_isikhathi_sokwenza.이어읽기) 단말.Bhala("jkoros-native> "); umugqa_Umhleli.umugqa_wemiyalo = true; 보드.원격대기(1); int Ubungako = 줄읽기(); 보드.원격대기(0); umugqa_Umhleli.umugqa_wemiyalo = false;
            if (Ubungako == -3) continue;
            if (Ubungako == -2) 단말.Bhala("Umlayelo zawula_inani: 명령줄이 너무 깁니다\n");
            if (Ubungako >= 0) { isihumushi_miyalelo_uhlelo_miyalelo.uhlelosiluleko_yekisa = false; isihumushi_miyalelo_uhlelo_miyalelo.yenza_umyalo(umugqa, 0, Ubungako, 0); } else isihumushi_miyalelo_uhlelo_miyalelo.isimo_inani = 130;
            보드.yekisa_kude_umyalo(isihumushi_miyalelo_uhlelo_miyalelo.isimo_inani);
            umugqa_Umhleli.Ubungako = umugqa_Umhleli.isikhombisi_inani = umugqa_Umhleli.qala_ifasitela = 0;
        }
    }
}
