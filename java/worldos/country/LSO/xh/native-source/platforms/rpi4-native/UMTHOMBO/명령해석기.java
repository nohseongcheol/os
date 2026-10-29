// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 umgca_wemiyalelo. 따옴표, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] umgca = new int[4096], ithokeni_ixabiso = new int[4096], 시작점 = new int[32], ubude_ixabiso = new int[32];
    static int[] 편집내용 = new int[16384], hlela_igama = new int[63];
    static int 토큰수, hlela_igama_ubude, 결과;
    static boolean 앞줄;
    static void 원바이트(int ixabiso) { 보드.직렬쓰기(ixabiso); }
    static int 줄읽기() { return umgca_Umhleli.Funda(); }
    static boolean 나누기(int Ubukhulu) {
        int 위치 = 0, 끝 = 0; 토큰수 = 0;
        while (위치 < Ubukhulu) {
            while (위치 < Ubukhulu && (umgca[위치] == 32 || umgca[위치] == 9)) 위치++;
            if (위치 == Ubukhulu) break;
            if (토큰수 == 16) { 단말.Bhala("Umyalelo ingcaciso_yegama_ixabiso: 인수가 너무 많습니다\n"); return false; }
            시작점[토큰수] = 끝; int 인용 = 0;
            while (위치 < Ubukhulu) {
                int ixabiso = umgca[위치++];
                if (인용 == 0 && (ixabiso == 32 || ixabiso == 9)) break;
                if (ixabiso == 인용) { 인용 = 0; continue; }
                if (인용 == 0 && (ixabiso == 39 || ixabiso == 34)) { 인용 = ixabiso; continue; }
                ithokeni_ixabiso[끝++] = ixabiso;
            }
            if (인용 != 0) { 단말.Bhala("Umyalelo ingcaciso_yegama_ixabiso: 따옴표가 닫히지 않았습니다\n"); return false; }
            ubude_ixabiso[토큰수] = 끝 - 시작점[토큰수]; 토큰수++;
        }
        return true;
    }
    static boolean 같음(int indeksa, String Igama_I_SMS) {
        if (indeksa >= 토큰수) return false;
        int 자리=0;
        for (int 순번=0; 순번<Igama_I_SMS.length(); 순번++) {
            int ikhowudi_yekharakhtha=Igama_I_SMS.charAt(순번);
            if (ikhowudi_yekharakhtha>=0xd800 && ikhowudi_yekharakhtha<=0xdbff && 순번+1<Igama_I_SMS.length()) ikhowudi_yekharakhtha=0x10000+((ikhowudi_yekharakhtha-0xd800)<<10)+Igama_I_SMS.charAt(++순번)-0xdc00;
            int 바이트수=ikhowudi_yekharakhtha<128?1:ikhowudi_yekharakhtha<2048?2:ikhowudi_yekharakhtha<65536?3:4;
            for (int ULANDELELWANO_ixabiso=바이트수-1; ULANDELELWANO_ixabiso>=0; ULANDELELWANO_ixabiso--) {
                int ixabiso=바이트수==1?ikhowudi_yekharakhtha:ULANDELELWANO_ixabiso==바이트수-1?(바이트수==2?0xc0:바이트수==3?0xe0:0xf0)|(ikhowudi_yekharakhtha>>(6*ULANDELELWANO_ixabiso)):0x80|((ikhowudi_yekharakhtha>>(6*ULANDELELWANO_ixabiso))&63);
                if (자리>=ubude_ixabiso[indeksa] || ithokeni_ixabiso[시작점[indeksa]+자리++]!=ixabiso) return false;
            }
        }
        return 자리==ubude_ixabiso[indeksa];
    }
    static int INDLELA(int indeksa) {
        if (indeksa >= 토큰수) return -22;
        int 결과 = imemori_Iifayile.indlela_qala(ubude_ixabiso[indeksa]); if (결과 < 0) return 결과;
        for (int iluphu_indeksa = 0; iluphu_indeksa < ubude_ixabiso[indeksa]; iluphu_indeksa++) {
            결과 = imemori_Iifayile.indlela_ibhayithi(iluphu_indeksa, ithokeni_ixabiso[시작점[indeksa] + iluphu_indeksa]); if (결과 < 0) return 결과;
        }
        return 0;
    }
    static void Impazamo(int indeksa) { 결과 = 1; 단말.Bhala("Impazamo "); 단말.수(indeksa); 단말.문자(10); }
    static void bona_ixabiso() {
        if (토큰수 != 2) { 단말.Bhala("사용법: cat iFayili\n"); return; }
        int 결과 = INDLELA(1); if (결과 < 0) { Impazamo(결과); return; }
        int iFayili = imemori_Iifayile.Vula(0); if (iFayili < 0) { Impazamo(iFayili); return; }
        while (true) { int ixabiso = imemori_Iifayile.Funda(iFayili); if (ixabiso == 256) break; if (ixabiso < 0) { Impazamo(ixabiso); break; } 원바이트(ixabiso); }
        imemori_Iifayile.Vala(iFayili); 단말.문자(10);
    }
    static void hlela_ixabiso() {
        if (토큰수 != 2) { 단말.Bhala("사용법: edit iFayili\n"); return; }
        int 결과 = INDLELA(1); if (결과 < 0) { Impazamo(결과); return; }
        hlela_igama_ubude = ubude_ixabiso[1];
        for (int iluphu_indeksa = 0; iluphu_indeksa < hlela_igama_ubude; iluphu_indeksa++) hlela_igama[iluphu_indeksa] = ithokeni_ixabiso[시작점[1] + iluphu_indeksa];
        단말.Bhala("EDIT: iFayili 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Ubukhulu = 0;
        while (true) {
            단말.Bhala("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Bhala("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && umgca[0] == '.') break;
            if (입력 + 1 > 편집내용.length - Ubukhulu) { 단말.Bhala("EDIT CANCELLED: file too large\n"); return; }
            for (int iluphu_indeksa = 0; iluphu_indeksa < 입력; iluphu_indeksa++) 편집내용[Ubukhulu++] = umgca[iluphu_indeksa];
            편집내용[Ubukhulu++] = 10;
        }
        imemori_Iifayile.indlela_qala(hlela_igama_ubude);
        for (int iluphu_indeksa = 0; iluphu_indeksa < hlela_igama_ubude; iluphu_indeksa++) imemori_Iifayile.indlela_ibhayithi(iluphu_indeksa, hlela_igama[iluphu_indeksa]);
        int iFayili = imemori_Iifayile.Vula(577); if (iFayili < 0) { Impazamo(iFayili); return; }
        for (int iluphu_indeksa = 0; iluphu_indeksa < Ubukhulu; iluphu_indeksa++) imemori_Iifayile.Bhala(iFayili, 편집내용[iluphu_indeksa]);
        imemori_Iifayile.Vala(iFayili); 단말.Bhala("SAVED "); 단말.수(Ubukhulu); 단말.Bhala("ibhayithi_ixabiso(주기억 iFayili)\n");
    }
    static int 십육(int ixabiso) {
        if (ixabiso >= '0' && ixabiso <= '9') return ixabiso - '0';
        if (ixabiso >= 'a' && ixabiso <= 'f') return ixabiso - 'a' + 10;
        if (ixabiso >= 'A' && ixabiso <= 'F') return ixabiso - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (토큰수 != 2) { 단말.Bhala("사용법: load iFayili | hex iFayili\n"); return; }
        int 결과 = INDLELA(1); if (결과 < 0) { Impazamo(결과); return; }
        if (!넣기) {
            int iFayili = imemori_Iifayile.Vula(0); if (iFayili < 0) { Impazamo(iFayili); return; }
            단말.Bhala("HEX BEGIN "); 단말.수(imemori_Iifayile.Ubukhulu(iFayili)); 단말.문자(10);
            int 항목수 = 0;
            while (true) {
                int ixabiso = imemori_Iifayile.Funda(iFayili); if (ixabiso < 0 || ixabiso == 256) break;
                단말.문자("0123456789abcdef".charAt(ixabiso >> 4)); 단말.문자("0123456789abcdef".charAt(ixabiso & 15));
                if (++항목수 % 32 == 0) 단말.문자(10);
            }
            if (항목수 % 32 != 0) 단말.문자(10);
            imemori_Iifayile.Vala(iFayili); 단말.Bhala("HEX END\n"); return;
        }
        hlela_igama_ubude = ubude_ixabiso[1];
        for (int iluphu_indeksa = 0; iluphu_indeksa < hlela_igama_ubude; iluphu_indeksa++) hlela_igama[iluphu_indeksa] = ithokeni_ixabiso[시작점[1] + iluphu_indeksa];
        단말.Bhala("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Ubukhulu = 0;
        while (true) {
            단말.Bhala("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Bhala("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && umgca[0] == '.') break;
            int 앞 = -1;
            for (int iluphu_indeksa = 0; iluphu_indeksa < 입력; iluphu_indeksa++) {
                if (umgca[iluphu_indeksa] == 32 || umgca[iluphu_indeksa] == 9) continue;
                int ixabiso = 십육(umgca[iluphu_indeksa]);
                if (ixabiso < 0 || Ubukhulu >= 편집내용.length) { 단말.Bhala("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = ixabiso; else { 편집내용[Ubukhulu++] = 앞 * 16 + ixabiso; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.Bhala("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        imemori_Iifayile.indlela_qala(hlela_igama_ubude);
        for (int iluphu_indeksa = 0; iluphu_indeksa < hlela_igama_ubude; iluphu_indeksa++) imemori_Iifayile.indlela_ibhayithi(iluphu_indeksa, hlela_igama[iluphu_indeksa]);
        int iFayili = imemori_Iifayile.Vula(577); if (iFayili < 0) { Impazamo(iFayili); return; }
        for (int iluphu_indeksa = 0; iluphu_indeksa < Ubukhulu; iluphu_indeksa++) imemori_Iifayile.Bhala(iFayili, 편집내용[iluphu_indeksa]);
        imemori_Iifayile.Vala(iFayili); 단말.Bhala("LOADED "); 단말.수(Ubukhulu); 단말.Bhala("ibhayithi_ixabiso(주기억 iFayili)\n");
    }
    static int Izixhobo(int indeksa) {
        return isixhobo_sokutayipha_ufako_nkcukacha(indeksa, 1);
    }
    static int isixhobo_sokutayipha_ufako_nkcukacha(int indeksa, int Phumeza) {
        if (토큰수 - Phumeza > 8) return -22;
        보드.인수준비(토큰수 - Phumeza);
        for (int 첫값 = Phumeza; 첫값 < 토큰수; 첫값++) {
            if (ubude_ixabiso[첫값] > 255) return -36;
            for (int iluphu_indeksa = 0; iluphu_indeksa < ubude_ixabiso[첫값]; iluphu_indeksa++) 보드.isiniki_myalelo_ibhayithi(첫값 - Phumeza, iluphu_indeksa, ithokeni_ixabiso[시작점[첫값] + iluphu_indeksa]);
        }
        return indeksa == -2 ? 보드.리눅스파일실행() : indeksa < 0 ? 보드.ukwenza_umsebenzisi_ifayile() : 보드.i_run_umsebenzisi_inkqubo(indeksa);
    }
    static int 파이썬꾸러미() {
        if (토큰수 > 8) return -22;
        보드.인수준비(토큰수);
        String INDLELA = "/lib/umqulu.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int 자리 = 0;
        for (int 순번 = 0; 순번 < INDLELA.length(); 순번++) {
            int ikharakhtha_ixabiso = INDLELA.charAt(순번);
            if (ikharakhtha_ixabiso < 128) 보드.isiniki_myalelo_ibhayithi(0, 자리++, ikharakhtha_ixabiso);
            else { 보드.isiniki_myalelo_ibhayithi(0, 자리++, 0xe0 | (ikharakhtha_ixabiso >> 12)); 보드.isiniki_myalelo_ibhayithi(0, 자리++, 0x80 | ((ikharakhtha_ixabiso >> 6) & 63)); 보드.isiniki_myalelo_ibhayithi(0, 자리++, 0x80 | (ikharakhtha_ixabiso & 63)); }
        }
        for (int 순번 = 1; 순번 < 토큰수; 순번++) {
            if (ubude_ixabiso[순번] > 255) return -36;
            for (int ikharakhtha_ixabiso = 0; ikharakhtha_ixabiso < ubude_ixabiso[순번]; ikharakhtha_ixabiso++) 보드.isiniki_myalelo_ibhayithi(순번, ikharakhtha_ixabiso, ithokeni_ixabiso[시작점[순번] + ikharakhtha_ixabiso]);
        }
        return 보드.i_run_umsebenzisi_inkqubo(12);
    }
    static int 실행형식() {
        int 처리값 = INDLELA(0); if (처리값 < 0) return 처리값;
        int iFayili = imemori_Iifayile.Vula(0); if (iFayili < 0) return iFayili;
        int 첫값 = imemori_Iifayile.Funda(iFayili), ibhayithi_iingcombolo = imemori_Iifayile.Funda(iFayili), ikhowudi_yekharakhtha = imemori_Iifayile.Funda(iFayili), 뒷값 = imemori_Iifayile.Funda(iFayili);
        imemori_Iifayile.Vala(iFayili);
        if (첫값 == 127 && ibhayithi_iingcombolo == 'E' && ikhowudi_yekharakhtha == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && ibhayithi_iingcombolo == 'K' && ikhowudi_yekharakhtha == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int indeksa, String 인수) {
        보드.인수준비(1);
        for (int iluphu_indeksa = 0; iluphu_indeksa < 인수.length(); iluphu_indeksa++) 보드.isiniki_myalelo_ibhayithi(0, iluphu_indeksa, 인수.charAt(iluphu_indeksa));
        return 보드.i_run_umsebenzisi_inkqubo(indeksa);
    }
    static void I_SMS_ibhayithi(int iFayili, int ixabiso) { imemori_Iifayile.Bhala(iFayili, ixabiso); }
    static void imi_ndawonye_ifayile(String Igama, String Isiqulatho_ixabiso) {
        // umqulu 파일명은 ASCII. iFayili 내용은 UTF-8로 저장한다.
        imemori_Iifayile.indlela_qala(Igama.length());
        for (int iluphu_indeksa = 0; iluphu_indeksa < Igama.length(); iluphu_indeksa++) imemori_Iifayile.indlela_ibhayithi(iluphu_indeksa, Igama.charAt(iluphu_indeksa));
        int iFayili = imemori_Iifayile.Vula(193); if (iFayili < 0) return;
        for (int iluphu_indeksa = 0; iluphu_indeksa < Isiqulatho_ixabiso.length(); iluphu_indeksa++) {
            int ikhowudi_yekharakhtha = Isiqulatho_ixabiso.charAt(iluphu_indeksa);
            if (ikhowudi_yekharakhtha >= 0xd800 && ikhowudi_yekharakhtha <= 0xdbff && iluphu_indeksa + 1 < Isiqulatho_ixabiso.length()) ikhowudi_yekharakhtha = 0x10000 + ((ikhowudi_yekharakhtha - 0xd800) << 10) + Isiqulatho_ixabiso.charAt(++iluphu_indeksa) - 0xdc00;
            if (ikhowudi_yekharakhtha < 128) I_SMS_ibhayithi(iFayili, ikhowudi_yekharakhtha);
            else {
                int 수 = ikhowudi_yekharakhtha < 2048 ? 2 : ikhowudi_yekharakhtha < 65536 ? 3 : 4;
                I_SMS_ibhayithi(iFayili, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (ikhowudi_yekharakhtha >> (6 * (수 - 1))));
                for (int 항목수 = 수 - 1; 항목수 > 0; 항목수--) I_SMS_ibhayithi(iFayili, 0x80 | ((ikhowudi_yekharakhtha >> (6 * (항목수 - 1))) & 63));
            }
        }
        imemori_Iifayile.Vala(iFayili);
    }
    static void 한글도움말() {
        단말.Bhala("F9 / Shift+Space: [EN] ↔ [xh]\n");
        단말.Bhala("  [XH] keyboard; [EN] ASCII\n");
        단말.Bhala("  a → a\n");
        단말.Bhala("  F9: EN ↔ xh | Ctrl+Shift+V: UTF-8\n");
        단말.Bhala("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Bhala("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Igama) {
        int 바이트수 = 0;
        for (int iluphu_indeksa = 0; iluphu_indeksa < Igama.length(); iluphu_indeksa++) { int ikhowudi_yekharakhtha = Igama.charAt(iluphu_indeksa); if (ikhowudi_yekharakhtha >= 0xd800 && ikhowudi_yekharakhtha <= 0xdfff) return -22; 바이트수 += ikhowudi_yekharakhtha < 128 ? 1 : ikhowudi_yekharakhtha < 2048 ? 2 : 3; }
        int 처리값 = imemori_Iifayile.indlela_qala(바이트수); if (처리값 < 0) return 처리값;
        int 자리 = 0;
        for (int iluphu_indeksa = 0; iluphu_indeksa < Igama.length(); iluphu_indeksa++) {
            int ikhowudi_yekharakhtha = Igama.charAt(iluphu_indeksa);
            if (ikhowudi_yekharakhtha < 128) imemori_Iifayile.indlela_ibhayithi(자리++, ikhowudi_yekharakhtha);
            else if (ikhowudi_yekharakhtha < 2048) { imemori_Iifayile.indlela_ibhayithi(자리++, 0xc0 | (ikhowudi_yekharakhtha >> 6)); imemori_Iifayile.indlela_ibhayithi(자리++, 0x80 | (ikhowudi_yekharakhtha & 63)); }
            else { imemori_Iifayile.indlela_ibhayithi(자리++, 0xe0 | (ikhowudi_yekharakhtha >> 12)); imemori_Iifayile.indlela_ibhayithi(자리++, 0x80 | ((ikhowudi_yekharakhtha >> 6) & 63)); imemori_Iifayile.indlela_ibhayithi(자리++, 0x80 | (ikhowudi_yekharakhtha & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Igama) {
        int 처리값 = 예제경로(Igama); if (처리값 < 0) return 처리값;
        처리값 = imemori_Iifayile.yila_isalathisi(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Igama, String iingcombolo) {
        int 처리값 = 예제경로(Igama); if (처리값 < 0) return 처리값;
        int iFayili = imemori_Iifayile.Vula(193); if (iFayili == -17) return 0; if (iFayili < 0) return iFayili;
        for (int iluphu_indeksa = 0; iluphu_indeksa < iingcombolo.length(); iluphu_indeksa += 2) {
            처리값 = imemori_Iifayile.Bhala(iFayili, 십육(iingcombolo.charAt(iluphu_indeksa)) * 16 + 십육(iingcombolo.charAt(iluphu_indeksa + 1)));
            if (처리값 < 0) { imemori_Iifayile.Vala(iFayili); return 처리값; }
        }
        return imemori_Iifayile.Vala(iFayili);
    }
    static void bonisa_uncedo() {
        inkqubo_isixhobo_sokutayipha.bonisa_uncedo();
        단말.Bhala("sshd / ikhuselekile_isiniki_myalelo start|stop|status: SSH :22 (user, 장치별 iphaswedi_ixabiso)\n");
        단말.Bhala("vncd / kude_bonisa start|stop|status: VNC :5900 (장치별 iphaswedi_ixabiso)\n");
        단말.Bhala("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Bhala("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Bhala("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Bhala("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Bhala("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Bhala("모서리 + 왼쪽 버튼 tsala_ixabiso: i_Terminal Ubukhulu tshintsha_ixabiso; terminal size: ikholam_ixabiso/umqolo_ixabiso\n");
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
        단말.Bhala("pip: MicroPython umthombo_umthi fakela_ixabiso; umsingathi --network --pip 필요; /lib는 RAM\n");
        단말.Bhala("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Bhala("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Bhala("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Bhala("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void i_Terminal(boolean 전환여부) {
        if (전환여부 && 보드.i_Terminal(2) != 0) { 보드.i_Terminal(0); 단말.Bhala("TERMINAL CLOSED\n"); }
        else if (보드.i_Terminal(1) < 0) Impazamo(-19);
        else 단말.Bhala("TERMINAL READY — xh terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Umyalelo() {
        if (토큰수 == 0) return;
        if (inkqubo_isixhobo_sokutayipha.ukwenza_umyalelo()) return;
        if (같음(0,"sshd") || 같음(0,"ikhuselekile_isiniki_myalelo") || 같음(0,"vncd") || 같음(0,"kude_bonisa")) {
            int 종류=같음(0,"vncd")||같음(0,"kude_bonisa")?1:0;
            int Intshukumo=같음(1,"start")||같음(1,"Phumeza")?1:같음(1,"stop")||같음(1,"Yima")?0:2;
            int imo_ixabiso=보드.ukusitha(종류,Intshukumo);
            if(imo_ixabiso<0)Impazamo(imo_ixabiso);else 단말.Bhala(보드.ukusitha(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else bonisa_uncedo(); }
        else if (같음(0, "info") || 같음(0, "i")) ikheneli.i_msinfo32_exe();
        else if (같음(0, "pwd")) { imemori_Iifayile.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (토큰수 == 1) { imemori_Iifayile.indlela_qala(1); 처리값 = imemori_Iifayile.indlela_ibhayithi(0, '/'); } else 처리값 = 토큰수 == 2 ? INDLELA(1) : -22;
            if (처리값 >= 0) 처리값 = imemori_Iifayile.tshintsha_isalathisi(); if (처리값 < 0) Impazamo(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int isiniki_myalelo_indeksa = 같음(1, "-l") ? 2 : 1, 처리값;
            if (토큰수 == isiniki_myalelo_indeksa) { imemori_Iifayile.indlela_qala(1); 처리값 = imemori_Iifayile.indlela_ibhayithi(0, '.'); } else 처리값 = 토큰수 == isiniki_myalelo_indeksa + 1 ? INDLELA(isiniki_myalelo_indeksa) : -22;
            if (처리값 >= 0) 처리값 = imemori_Iifayile.경로목록(); if (처리값 < 0) Impazamo(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) isiniki_myalelo_Izixhobo.ifayile_isiganeko(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) isiniki_myalelo_Izixhobo.kopa_ixabiso(같음(0, "mv"));
        else if (같음(0, "cat")) isiniki_myalelo_Izixhobo.bona_ixabiso();
        else if (같음(0, "wc")) isiniki_myalelo_Izixhobo.세기();
        else if (같음(0, "grep")) isiniki_myalelo_Izixhobo.fumana_ufako_nkcukacha();
        else if (같음(0, "head") || 같음(0, "tail")) isiniki_myalelo_Izixhobo.머리(같음(0, "tail"));
        else if (같음(0, "tee")) isiniki_myalelo_Izixhobo.함께쓰기();
        else if (같음(0, "env")) isiniki_myalelo_ukuma_kwezivakalisi.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (토큰수 == 1) isiniki_myalelo_ukuma_kwezivakalisi.환경보기();
            for (int iluphu_indeksa = 1; iluphu_indeksa < 토큰수; iluphu_indeksa++) { int 처리값 = isiniki_myalelo_ukuma_kwezivakalisi.환경설정(iluphu_indeksa, 같음(0, "unset")); if (처리값 != 0) { 결과 = 처리값; 단말.Bhala("Umyalelo ingcaciso_yegama_ixabiso: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) isiniki_myalelo_ukuma_kwezivakalisi.ukwenza_ifayile();
        else if (같음(0, "true")) 결과 = 0;
        else if (같음(0, "false")) 결과 = 1;
        else if (같음(0, "history")) umgca_Umhleli.bonisa_ilog();
        else if (같음(0, "exit")) {
            if (isiniki_myalelo_ukuma_kwezivakalisi.깊이 > 0) { 결과 = 토큰수 == 1 ? isiniki_myalelo_ukuma_kwezivakalisi.imo_ixabiso : isiniki_myalelo_Izixhobo.inani_ixabiso(1); if (결과 < 0 || 결과 > 255) 결과 = 2; isiniki_myalelo_ukuma_kwezivakalisi.iskripthi_phela = true; }
            else if (보드.i_Terminal(2) != 0) i_Terminal(true);
            else 단말.Bhala("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) hlela_ixabiso();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (토큰수 < 2) { 결과 = 2; 단말.Bhala("사용법: rm iFayili...\n"); }
            for (int iluphu_indeksa = 1; iluphu_indeksa < 토큰수; iluphu_indeksa++) { int 처리값 = INDLELA(iluphu_indeksa); if (처리값 == 0) 처리값 = imemori_Iifayile.지우기(); if (처리값 < 0) Impazamo(처리값); }
        }
        else if (같음(0, "echo")) {
            int 시작자리 = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = 시작자리; 첫값 < 토큰수; 첫값++) { if (첫값 > 시작자리) 단말.문자(32); for (int iluphu_indeksa = 0; iluphu_indeksa < ubude_ixabiso[첫값]; iluphu_indeksa++) 보드.직렬쓰기(ithokeni_ixabiso[시작점[첫값] + iluphu_indeksa]); }
            if (시작자리 == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Bhala("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? 파이썬꾸러미() : Izixhobo(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !isiniki_myalelo_ukuma_kwezivakalisi.연결중) { 단말.Bhala("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Izixhobo(13); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Izixhobo(15); 결과 = 처리값 < 0 ? 126 : 처리값; if (!isiniki_myalelo_ukuma_kwezivakalisi.연결중) { 단말.Bhala("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Izixhobo(16); 결과 = 처리값 < 0 ? 126 : 처리값; if (!isiniki_myalelo_ukuma_kwezivakalisi.연결중) { 단말.Bhala("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Ubukhulu = 보드.i_Terminal(13); 단말.Bhala("TERMINAL SIZE "); 단말.수(Ubukhulu & 65535); 단말.문자('x'); 단말.수(Ubukhulu >>> 16); 단말.문자(10); }
            else i_Terminal(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { 보드.i_Terminal(9); idesktophu.ukwenza_umyalelo(); }
        else if (같음(0, "c")) ikheneli.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) ikheneli.작업시험();
        else if (같음(0, "g")) ikheneli.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) ikheneli.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = 보드.i_run_umsebenzisi_inkqubo(0); if (처리값 == 0) 단말.Bhala("ELF DEMO PASS\n"); else Impazamo(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? isixhobo_sokutayipha_ufako_nkcukacha(-2, 2) : Izixhobo(-1); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !isiniki_myalelo_ukuma_kwezivakalisi.연결중) { 단말.Bhala("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) ikheneli.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = 보드.ifayile_gqithisela_isevisi(1); if (처리값 < 0) Impazamo(처리값); else { 단말.Bhala("FTP listening "); inkqubo_isixhobo_sokutayipha.bhala_idilesi(보드.Inethiwekhi_imo(0,0)); 단말.Bhala(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { 보드.ifayile_gqithisela_isevisi(0); 단말.Bhala("FTP stopped\n"); }
            else 단말.Bhala(보드.ifayile_gqithisela_isevisi(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { umqulu.lungisa(); 단말.Bhala("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Ulwimi = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (토큰수 != 2 || Ulwimi < 0) 단말.Bhala("example java|c|python: 출력, iFayili, 네트워크, 그래픽, Java Swing i_window 예제\n");
            else { int 처리값 = 예제꾸러미.fakela_ixabiso(Ulwimi); if (처리값 < 0) { Impazamo(처리값); if (처리값 == -28) 단말.Bhala("RAM full: remove unused files, then retry example\n"); } else 단말.Bhala("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int fomatha_ixabiso = 실행형식();
            if (fomatha_ixabiso == 1 || fomatha_ixabiso == 2) {
                int 처리값 = isixhobo_sokutayipha_ufako_nkcukacha(fomatha_ixabiso == 1 ? -1 : 14, 0); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !isiniki_myalelo_ukuma_kwezivakalisi.연결중) { 단말.Bhala("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (fomatha_ixabiso == 0) { 결과 = 126; 단말.Bhala("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { 결과 = 127; 단말.Bhala("Unknown command. help: commands\n"); }
        }
    }
    public static void ukwenza_umyalelo() {
        umqulu.lungisa();
        for (int Ulwimi = 0; Ulwimi < 3; Ulwimi++) { int 처리값 = 예제꾸러미.fakela_ixabiso(Ulwimi); if (처리값 < 0) Impazamo(처리값); }
        bonisa_uncedo();
        while (true) {
            i_window_iseshoni.Inkqubo_ixabiso_ufako_nkcukacha(); if (i_window_iseshoni.재개()) continue;
            if (!i_window_iseshoni.이어읽기) 단말.Bhala("jkoros-native> "); umgca_Umhleli.umgca_wemiyalelo = true; 보드.원격대기(1); int Ubukhulu = 줄읽기(); 보드.원격대기(0); umgca_Umhleli.umgca_wemiyalelo = false;
            if (Ubukhulu == -3) continue;
            if (Ubukhulu == -2) 단말.Bhala("Umyalelo ingcaciso_yegama_ixabiso: 명령줄이 너무 깁니다\n");
            if (Ubukhulu >= 0) { isiniki_myalelo_ukuma_kwezivakalisi.iskripthi_phela = false; isiniki_myalelo_ukuma_kwezivakalisi.ukwenza_umyalelo(umgca, 0, Ubukhulu, 0); } else isiniki_myalelo_ukuma_kwezivakalisi.imo_ixabiso = 130;
            보드.phela_kude_umyalelo(isiniki_myalelo_ukuma_kwezivakalisi.imo_ixabiso);
            umgca_Umhleli.Ubukhulu = umgca_Umhleli.ikhesa_ixabiso = umgca_Umhleli.qala_i_window = 0;
        }
    }
}
