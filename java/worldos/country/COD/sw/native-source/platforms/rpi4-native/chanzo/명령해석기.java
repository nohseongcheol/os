// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 tungo_amri. 따옴표, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] laini = new int[4096], tuzo_thamani = new int[4096], 시작점 = new int[32], urefu_thamani = new int[32];
    static int[] 편집내용 = new int[16384], hariri_jina = new int[63];
    static int 토큰수, hariri_jina_urefu, 결과;
    static boolean 앞줄;
    static void 원바이트(int thamani) { 보드.직렬쓰기(thamani); }
    static int 줄읽기() { return laini_Kihariri.읽기(); }
    static boolean 나누기(int panga_ukubwa) {
        int 위치 = 0, 끝 = 0; 토큰수 = 0;
        while (위치 < panga_ukubwa) {
            while (위치 < panga_ukubwa && (laini[위치] == 32 || laini[위치] == 9)) 위치++;
            if (위치 == panga_ukubwa) break;
            if (토큰수 == 16) { 단말.andika("amri changanua_thamani: 인수가 너무 많습니다\n"); return false; }
            시작점[토큰수] = 끝; int 인용 = 0;
            while (위치 < panga_ukubwa) {
                int thamani = laini[위치++];
                if (인용 == 0 && (thamani == 32 || thamani == 9)) break;
                if (thamani == 인용) { 인용 = 0; continue; }
                if (인용 == 0 && (thamani == 39 || thamani == 34)) { 인용 = thamani; continue; }
                tuzo_thamani[끝++] = thamani;
            }
            if (인용 != 0) { 단말.andika("amri changanua_thamani: 따옴표가 닫히지 않았습니다\n"); return false; }
            urefu_thamani[토큰수] = 끝 - 시작점[토큰수]; 토큰수++;
        }
        return true;
    }
    static boolean 같음(int kielezo, String Neno_SMS) {
        if (kielezo >= 토큰수) return false;
        int 자리=0;
        for (int 순번=0; 순번<Neno_SMS.length(); 순번++) {
            int msimbo_wa_kibambo=Neno_SMS.charAt(순번);
            if (msimbo_wa_kibambo>=0xd800 && msimbo_wa_kibambo<=0xdbff && 순번+1<Neno_SMS.length()) msimbo_wa_kibambo=0x10000+((msimbo_wa_kibambo-0xd800)<<10)+Neno_SMS.charAt(++순번)-0xdc00;
            int 바이트수=msimbo_wa_kibambo<128?1:msimbo_wa_kibambo<2048?2:msimbo_wa_kibambo<65536?3:4;
            for (int MFUATANO_thamani=바이트수-1; MFUATANO_thamani>=0; MFUATANO_thamani--) {
                int thamani=바이트수==1?msimbo_wa_kibambo:MFUATANO_thamani==바이트수-1?(바이트수==2?0xc0:바이트수==3?0xe0:0xf0)|(msimbo_wa_kibambo>>(6*MFUATANO_thamani)):0x80|((msimbo_wa_kibambo>>(6*MFUATANO_thamani))&63);
                if (자리>=urefu_thamani[kielezo] || tuzo_thamani[시작점[kielezo]+자리++]!=thamani) return false;
            }
        }
        return 자리==urefu_thamani[kielezo];
    }
    static int njia(int kielezo) {
        if (kielezo >= 토큰수) return -22;
        int 결과 = kumbukumbu_Faili.njia_Anza(urefu_thamani[kielezo]); if (결과 < 0) return 결과;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < urefu_thamani[kielezo]; kitanzi_kielezo++) {
            결과 = kumbukumbu_Faili.njia_baiti(kitanzi_kielezo, tuzo_thamani[시작점[kielezo] + kitanzi_kielezo]); if (결과 < 0) return 결과;
        }
        return 0;
    }
    static void kosa(int kielezo) { 결과 = 1; 단말.andika("kosa "); 단말.수(kielezo); 단말.문자(10); }
    static void Onesha_thamani() {
        if (토큰수 != 2) { 단말.andika("사용법: cat faili\n"); return; }
        int 결과 = njia(1); if (결과 < 0) { kosa(결과); return; }
        int faili = kumbukumbu_Faili.unda(0); if (faili < 0) { kosa(faili); return; }
        while (true) { int thamani = kumbukumbu_Faili.읽기(faili); if (thamani == 256) break; if (thamani < 0) { kosa(thamani); break; } 원바이트(thamani); }
        kumbukumbu_Faili.funga(faili); 단말.문자(10);
    }
    static void hariri_thamani() {
        if (토큰수 != 2) { 단말.andika("사용법: edit faili\n"); return; }
        int 결과 = njia(1); if (결과 < 0) { kosa(결과); return; }
        hariri_jina_urefu = urefu_thamani[1];
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < hariri_jina_urefu; kitanzi_kielezo++) hariri_jina[kitanzi_kielezo] = tuzo_thamani[시작점[1] + kitanzi_kielezo];
        단말.andika("EDIT: faili 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int panga_ukubwa = 0;
        while (true) {
            단말.andika("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.andika("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && laini[0] == '.') break;
            if (입력 + 1 > 편집내용.length - panga_ukubwa) { 단말.andika("EDIT CANCELLED: file too large\n"); return; }
            for (int kitanzi_kielezo = 0; kitanzi_kielezo < 입력; kitanzi_kielezo++) 편집내용[panga_ukubwa++] = laini[kitanzi_kielezo];
            편집내용[panga_ukubwa++] = 10;
        }
        kumbukumbu_Faili.njia_Anza(hariri_jina_urefu);
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < hariri_jina_urefu; kitanzi_kielezo++) kumbukumbu_Faili.njia_baiti(kitanzi_kielezo, hariri_jina[kitanzi_kielezo]);
        int faili = kumbukumbu_Faili.unda(577); if (faili < 0) { kosa(faili); return; }
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < panga_ukubwa; kitanzi_kielezo++) kumbukumbu_Faili.andika(faili, 편집내용[kitanzi_kielezo]);
        kumbukumbu_Faili.funga(faili); 단말.andika("SAVED "); 단말.수(panga_ukubwa); 단말.andika("baiti_thamani(주기억 faili)\n");
    }
    static int 십육(int thamani) {
        if (thamani >= '0' && thamani <= '9') return thamani - '0';
        if (thamani >= 'a' && thamani <= 'f') return thamani - 'a' + 10;
        if (thamani >= 'A' && thamani <= 'F') return thamani - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (토큰수 != 2) { 단말.andika("사용법: load faili | hex faili\n"); return; }
        int 결과 = njia(1); if (결과 < 0) { kosa(결과); return; }
        if (!넣기) {
            int faili = kumbukumbu_Faili.unda(0); if (faili < 0) { kosa(faili); return; }
            단말.andika("HEX BEGIN "); 단말.수(kumbukumbu_Faili.panga_ukubwa(faili)); 단말.문자(10);
            int 항목수 = 0;
            while (true) {
                int thamani = kumbukumbu_Faili.읽기(faili); if (thamani < 0 || thamani == 256) break;
                단말.문자("0123456789abcdef".charAt(thamani >> 4)); 단말.문자("0123456789abcdef".charAt(thamani & 15));
                if (++항목수 % 32 == 0) 단말.문자(10);
            }
            if (항목수 % 32 != 0) 단말.문자(10);
            kumbukumbu_Faili.funga(faili); 단말.andika("HEX END\n"); return;
        }
        hariri_jina_urefu = urefu_thamani[1];
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < hariri_jina_urefu; kitanzi_kielezo++) hariri_jina[kitanzi_kielezo] = tuzo_thamani[시작점[1] + kitanzi_kielezo];
        단말.andika("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int panga_ukubwa = 0;
        while (true) {
            단말.andika("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.andika("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && laini[0] == '.') break;
            int mbele_thamani = -1;
            for (int kitanzi_kielezo = 0; kitanzi_kielezo < 입력; kitanzi_kielezo++) {
                if (laini[kitanzi_kielezo] == 32 || laini[kitanzi_kielezo] == 9) continue;
                int thamani = 십육(laini[kitanzi_kielezo]);
                if (thamani < 0 || panga_ukubwa >= 편집내용.length) { 단말.andika("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (mbele_thamani < 0) mbele_thamani = thamani; else { 편집내용[panga_ukubwa++] = mbele_thamani * 16 + thamani; mbele_thamani = -1; }
            }
            if (mbele_thamani >= 0) { 단말.andika("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        kumbukumbu_Faili.njia_Anza(hariri_jina_urefu);
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < hariri_jina_urefu; kitanzi_kielezo++) kumbukumbu_Faili.njia_baiti(kitanzi_kielezo, hariri_jina[kitanzi_kielezo]);
        int faili = kumbukumbu_Faili.unda(577); if (faili < 0) { kosa(faili); return; }
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < panga_ukubwa; kitanzi_kielezo++) kumbukumbu_Faili.andika(faili, 편집내용[kitanzi_kielezo]);
        kumbukumbu_Faili.funga(faili); 단말.andika("LOADED "); 단말.수(panga_ukubwa); 단말.andika("baiti_thamani(주기억 faili)\n");
    }
    static int Zana(int kielezo) {
        return zana_ingizo(kielezo, 1);
    }
    static int zana_ingizo(int kielezo, int endesha) {
        if (토큰수 - endesha > 8) return -22;
        보드.인수준비(토큰수 - endesha);
        for (int 첫값 = endesha; 첫값 < 토큰수; 첫값++) {
            if (urefu_thamani[첫값] > 255) return -36;
            for (int kitanzi_kielezo = 0; kitanzi_kielezo < urefu_thamani[첫값]; kitanzi_kielezo++) 보드.hoja_baiti(첫값 - endesha, kitanzi_kielezo, tuzo_thamani[시작점[첫값] + kitanzi_kielezo]);
        }
        return kielezo == -2 ? 보드.리눅스파일실행() : kielezo < 0 ? 보드.tekeleza_mtumiaji_faili() : 보드.endesha_mtumiaji_programu(kielezo);
    }
    static int 파이썬꾸러미() {
        if (토큰수 > 8) return -22;
        보드.인수준비(토큰수);
        String njia = "/lib/fungasha.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int 자리 = 0;
        for (int 순번 = 0; 순번 < njia.length(); 순번++) {
            int kibambo_thamani = njia.charAt(순번);
            if (kibambo_thamani < 128) 보드.hoja_baiti(0, 자리++, kibambo_thamani);
            else { 보드.hoja_baiti(0, 자리++, 0xe0 | (kibambo_thamani >> 12)); 보드.hoja_baiti(0, 자리++, 0x80 | ((kibambo_thamani >> 6) & 63)); 보드.hoja_baiti(0, 자리++, 0x80 | (kibambo_thamani & 63)); }
        }
        for (int 순번 = 1; 순번 < 토큰수; 순번++) {
            if (urefu_thamani[순번] > 255) return -36;
            for (int kibambo_thamani = 0; kibambo_thamani < urefu_thamani[순번]; kibambo_thamani++) 보드.hoja_baiti(순번, kibambo_thamani, tuzo_thamani[시작점[순번] + kibambo_thamani]);
        }
        return 보드.endesha_mtumiaji_programu(12);
    }
    static int 실행형식() {
        int 처리값 = njia(0); if (처리값 < 0) return 처리값;
        int faili = kumbukumbu_Faili.unda(0); if (faili < 0) return faili;
        int 첫값 = kumbukumbu_Faili.읽기(faili), baiti_data = kumbukumbu_Faili.읽기(faili), msimbo_wa_kibambo = kumbukumbu_Faili.읽기(faili), 뒷값 = kumbukumbu_Faili.읽기(faili);
        kumbukumbu_Faili.funga(faili);
        if (첫값 == 127 && baiti_data == 'E' && msimbo_wa_kibambo == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && baiti_data == 'K' && msimbo_wa_kibambo == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int kielezo, String 인수) {
        보드.인수준비(1);
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 인수.length(); kitanzi_kielezo++) 보드.hoja_baiti(0, kitanzi_kielezo, 인수.charAt(kitanzi_kielezo));
        return 보드.endesha_mtumiaji_programu(kielezo);
    }
    static void SMS_baiti(int faili, int thamani) { kumbukumbu_Faili.andika(faili, thamani); }
    static void tuli_faili(String Jina, String maudhui_thamani) {
        // fungasha 파일명은 ASCII. faili 내용은 UTF-8로 저장한다.
        kumbukumbu_Faili.njia_Anza(Jina.length());
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < Jina.length(); kitanzi_kielezo++) kumbukumbu_Faili.njia_baiti(kitanzi_kielezo, Jina.charAt(kitanzi_kielezo));
        int faili = kumbukumbu_Faili.unda(193); if (faili < 0) return;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < maudhui_thamani.length(); kitanzi_kielezo++) {
            int msimbo_wa_kibambo = maudhui_thamani.charAt(kitanzi_kielezo);
            if (msimbo_wa_kibambo >= 0xd800 && msimbo_wa_kibambo <= 0xdbff && kitanzi_kielezo + 1 < maudhui_thamani.length()) msimbo_wa_kibambo = 0x10000 + ((msimbo_wa_kibambo - 0xd800) << 10) + maudhui_thamani.charAt(++kitanzi_kielezo) - 0xdc00;
            if (msimbo_wa_kibambo < 128) SMS_baiti(faili, msimbo_wa_kibambo);
            else {
                int 수 = msimbo_wa_kibambo < 2048 ? 2 : msimbo_wa_kibambo < 65536 ? 3 : 4;
                SMS_baiti(faili, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (msimbo_wa_kibambo >> (6 * (수 - 1))));
                for (int 항목수 = 수 - 1; 항목수 > 0; 항목수--) SMS_baiti(faili, 0x80 | ((msimbo_wa_kibambo >> (6 * (항목수 - 1))) & 63));
            }
        }
        kumbukumbu_Faili.funga(faili);
    }
    static void 한글도움말() {
        단말.andika("F9 / Shift+Space: [EN] ↔ [sw]\n");
        단말.andika("  [SW] keyboard; [EN] ASCII\n");
        단말.andika("  a → a\n");
        단말.andika("  F9: EN ↔ sw | Ctrl+Shift+V: UTF-8\n");
        단말.andika("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.andika("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Jina) {
        int 바이트수 = 0;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < Jina.length(); kitanzi_kielezo++) { int msimbo_wa_kibambo = Jina.charAt(kitanzi_kielezo); if (msimbo_wa_kibambo >= 0xd800 && msimbo_wa_kibambo <= 0xdfff) return -22; 바이트수 += msimbo_wa_kibambo < 128 ? 1 : msimbo_wa_kibambo < 2048 ? 2 : 3; }
        int 처리값 = kumbukumbu_Faili.njia_Anza(바이트수); if (처리값 < 0) return 처리값;
        int 자리 = 0;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < Jina.length(); kitanzi_kielezo++) {
            int msimbo_wa_kibambo = Jina.charAt(kitanzi_kielezo);
            if (msimbo_wa_kibambo < 128) kumbukumbu_Faili.njia_baiti(자리++, msimbo_wa_kibambo);
            else if (msimbo_wa_kibambo < 2048) { kumbukumbu_Faili.njia_baiti(자리++, 0xc0 | (msimbo_wa_kibambo >> 6)); kumbukumbu_Faili.njia_baiti(자리++, 0x80 | (msimbo_wa_kibambo & 63)); }
            else { kumbukumbu_Faili.njia_baiti(자리++, 0xe0 | (msimbo_wa_kibambo >> 12)); kumbukumbu_Faili.njia_baiti(자리++, 0x80 | ((msimbo_wa_kibambo >> 6) & 63)); kumbukumbu_Faili.njia_baiti(자리++, 0x80 | (msimbo_wa_kibambo & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Jina) {
        int 처리값 = 예제경로(Jina); if (처리값 < 0) return 처리값;
        처리값 = kumbukumbu_Faili.unda_Saraka(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Jina, String data) {
        int 처리값 = 예제경로(Jina); if (처리값 < 0) return 처리값;
        int faili = kumbukumbu_Faili.unda(193); if (faili == -17) return 0; if (faili < 0) return faili;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < data.length(); kitanzi_kielezo += 2) {
            처리값 = kumbukumbu_Faili.andika(faili, 십육(data.charAt(kitanzi_kielezo)) * 16 + 십육(data.charAt(kitanzi_kielezo + 1)));
            if (처리값 < 0) { kumbukumbu_Faili.funga(faili); return 처리값; }
        }
        return kumbukumbu_Faili.funga(faili);
    }
    static void onyesha_msaada() {
        mfumo_zana.onyesha_msaada();
        단말.andika("sshd / salama_sheli start|stop|status: SSH :22 (user, 장치별 nywila_thamani)\n");
        단말.andika("vncd / kwa_mbali_onyesha start|stop|status: VNC :5900 (장치별 nywila_thamani)\n");
        단말.andika("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.andika("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.andika("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.andika("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.andika("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.andika("모서리 + 왼쪽 버튼 kokota_thamani: 터미널 panga_ukubwa badilisha_thamani_16f64fe4; terminal size: safuwima_thamani/kumbukumbu_thamani\n");
        단말.andika("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.andika("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.andika("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.andika("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.andika("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.andika("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.andika("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.andika("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.andika("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.andika("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.andika("pip: MicroPython chanzo_mti sakinisha_thamani; mwenyeji --network --pip 필요; /lib는 RAM\n");
        단말.andika("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.andika("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.andika("/example/java /example/c /example/python: examples ready at boot\n");
        단말.andika("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void 터미널(boolean 전환여부) {
        if (전환여부 && 보드.터미널(2) != 0) { 보드.터미널(0); 단말.andika("TERMINAL CLOSED\n"); }
        else if (보드.터미널(1) < 0) kosa(-19);
        else 단말.andika("TERMINAL READY — sw terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void amri() {
        if (토큰수 == 0) return;
        if (mfumo_zana.tekeleza_amri()) return;
        if (같음(0,"sshd") || 같음(0,"salama_sheli") || 같음(0,"vncd") || 같음(0,"kwa_mbali_onyesha")) {
            int 종류=같음(0,"vncd")||같음(0,"kwa_mbali_onyesha")?1:0;
            int Kitendo=같음(1,"start")||같음(1,"endesha")?1:같음(1,"stop")||같음(1,"Simama")?0:2;
            int hali_thamani=보드.mtagusano(종류,Kitendo);
            if(hali_thamani<0)kosa(hali_thamani);else 단말.andika(보드.mtagusano(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else onyesha_msaada(); }
        else if (같음(0, "info") || 같음(0, "i")) kiini.msinfo32_exe();
        else if (같음(0, "pwd")) { kumbukumbu_Faili.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (토큰수 == 1) { kumbukumbu_Faili.njia_Anza(1); 처리값 = kumbukumbu_Faili.njia_baiti(0, '/'); } else 처리값 = 토큰수 == 2 ? njia(1) : -22;
            if (처리값 >= 0) 처리값 = kumbukumbu_Faili.badilisha_Saraka(); if (처리값 < 0) kosa(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int hoja_kielezo = 같음(1, "-l") ? 2 : 1, 처리값;
            if (토큰수 == hoja_kielezo) { kumbukumbu_Faili.njia_Anza(1); 처리값 = kumbukumbu_Faili.njia_baiti(0, '.'); } else 처리값 = 토큰수 == hoja_kielezo + 1 ? njia(hoja_kielezo) : -22;
            if (처리값 >= 0) 처리값 = kumbukumbu_Faili.경로목록(); if (처리값 < 0) kosa(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) sheli_Zana.faili_Kazi(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) sheli_Zana.mfano_thamani(같음(0, "mv"));
        else if (같음(0, "cat")) sheli_Zana.Onesha_thamani();
        else if (같음(0, "wc")) sheli_Zana.세기();
        else if (같음(0, "grep")) sheli_Zana.gundua_ingizo();
        else if (같음(0, "head") || 같음(0, "tail")) sheli_Zana.머리(같음(0, "tail"));
        else if (같음(0, "tee")) sheli_Zana.함께쓰기();
        else if (같음(0, "env")) sheli_sintaksi.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (토큰수 == 1) sheli_sintaksi.환경보기();
            for (int kitanzi_kielezo = 1; kitanzi_kielezo < 토큰수; kitanzi_kielezo++) { int 처리값 = sheli_sintaksi.환경설정(kitanzi_kielezo, 같음(0, "unset")); if (처리값 != 0) { 결과 = 처리값; 단말.andika("amri changanua_thamani: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) sheli_sintaksi.tekeleza_faili();
        else if (같음(0, "true")) 결과 = 0;
        else if (같음(0, "false")) 결과 = 1;
        else if (같음(0, "history")) laini_Kihariri.onyesha_batli();
        else if (같음(0, "exit")) {
            if (sheli_sintaksi.깊이 > 0) { 결과 = 토큰수 == 1 ? sheli_sintaksi.hali_thamani : sheli_Zana.dijiti_thamani(1); if (결과 < 0 || 결과 > 255) 결과 = 2; sheli_sintaksi.hati_tamatia = true; }
            else if (보드.터미널(2) != 0) 터미널(true);
            else 단말.andika("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) hariri_thamani();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (토큰수 < 2) { 결과 = 2; 단말.andika("사용법: rm faili...\n"); }
            for (int kitanzi_kielezo = 1; kitanzi_kielezo < 토큰수; kitanzi_kielezo++) { int 처리값 = njia(kitanzi_kielezo); if (처리값 == 0) 처리값 = kumbukumbu_Faili.futa_ingizo(); if (처리값 < 0) kosa(처리값); }
        }
        else if (같음(0, "echo")) {
            int 시작자리 = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = 시작자리; 첫값 < 토큰수; 첫값++) { if (첫값 > 시작자리) 단말.문자(32); for (int kitanzi_kielezo = 0; kitanzi_kielezo < urefu_thamani[첫값]; kitanzi_kielezo++) 보드.직렬쓰기(tuzo_thamani[시작점[첫값] + kitanzi_kielezo]); }
            if (시작자리 == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.andika("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? 파이썬꾸러미() : Zana(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !sheli_sintaksi.연결중) { 단말.andika("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Zana(13); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Zana(15); 결과 = 처리값 < 0 ? 126 : 처리값; if (!sheli_sintaksi.연결중) { 단말.andika("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Zana(16); 결과 = 처리값 < 0 ? 126 : 처리값; if (!sheli_sintaksi.연결중) { 단말.andika("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int panga_ukubwa = 보드.터미널(13); 단말.andika("TERMINAL SIZE "); 단말.수(panga_ukubwa & 65535); 단말.문자('x'); 단말.수(panga_ukubwa >>> 16); 단말.문자(10); }
            else 터미널(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { 보드.터미널(9); Eneo_kazi.tekeleza_amri(); }
        else if (같음(0, "c")) kiini.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) kiini.작업시험();
        else if (같음(0, "g")) kiini.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) kiini.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = 보드.endesha_mtumiaji_programu(0); if (처리값 == 0) 단말.andika("ELF DEMO PASS\n"); else kosa(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? zana_ingizo(-2, 2) : Zana(-1); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !sheli_sintaksi.연결중) { 단말.andika("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) kiini.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = 보드.faili_hamisha_huduma(1); if (처리값 < 0) kosa(처리값); else { 단말.andika("FTP listening "); mfumo_zana.andika_anwani(보드.Mtandao_hali(0,0)); 단말.andika(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { 보드.faili_hamisha_huduma(0); 단말.andika("FTP stopped\n"); }
            else 단말.andika(보드.faili_hamisha_huduma(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { fungasha.Andaa(); 단말.andika("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Lugha = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (토큰수 != 2 || Lugha < 0) 단말.andika("example java|c|python: 출력, faili, 네트워크, 그래픽, Java Swing dirisha 예제\n");
            else { int 처리값 = 예제꾸러미.sakinisha_thamani(Lugha); if (처리값 < 0) { kosa(처리값); if (처리값 == -28) 단말.andika("RAM full: remove unused files, then retry example\n"); } else 단말.andika("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int umbiza_thamani = 실행형식();
            if (umbiza_thamani == 1 || umbiza_thamani == 2) {
                int 처리값 = zana_ingizo(umbiza_thamani == 1 ? -1 : 14, 0); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !sheli_sintaksi.연결중) { 단말.andika("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (umbiza_thamani == 0) { 결과 = 126; 단말.andika("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { 결과 = 127; 단말.andika("Unknown command. help: commands\n"); }
        }
    }
    public static void tekeleza_amri() {
        fungasha.Andaa();
        for (int Lugha = 0; Lugha < 3; Lugha++) { int 처리값 = 예제꾸러미.sakinisha_thamani(Lugha); if (처리값 < 0) kosa(처리값); }
        onyesha_msaada();
        while (true) {
            dirisha_kipindi.Mchakato_thamani_ingizo(); if (dirisha_kipindi.재개()) continue;
            if (!dirisha_kipindi.이어읽기) 단말.andika("jkoros-native> "); laini_Kihariri.tungo_amri = true; 보드.kwa_mbali_subiri(1); int panga_ukubwa = 줄읽기(); 보드.kwa_mbali_subiri(0); laini_Kihariri.tungo_amri = false;
            if (panga_ukubwa == -3) continue;
            if (panga_ukubwa == -2) 단말.andika("amri changanua_thamani: 명령줄이 너무 깁니다\n");
            if (panga_ukubwa >= 0) { sheli_sintaksi.hati_tamatia = false; sheli_sintaksi.tekeleza_amri(laini, 0, panga_ukubwa, 0); } else sheli_sintaksi.hali_thamani = 130;
            보드.tamatia_kwa_mbali_amri(sheli_sintaksi.hali_thamani);
            laini_Kihariri.panga_ukubwa = laini_Kihariri.kielekezi_thamani = laini_Kihariri.Anza_dirisha = 0;
        }
    }
}
