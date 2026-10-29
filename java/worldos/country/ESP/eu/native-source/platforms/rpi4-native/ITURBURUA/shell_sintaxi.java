// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interaktibo shell 문법. 파이프는 순차 exekutatu_komando, 환경은 같은 셸에서 공유한다. */
public final class shell_sintaxi {
    static int[] ITURBURUA = new int[4 * 4096], 종류 = new int[4 * 128], Exekutatu_2 = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], balio_luzera = new int[16];
    static int[] script_balio = new int[4 * 16384];
    static int Egoera_balio, 깊이, 쓴수;
    static boolean 연결중, script_amaitu, luzapen_errore;
    static boolean izen_karaktere(int karaktere_kode) { return karaktere_kode >= 'a' && karaktere_kode <= 'z' || karaktere_kode >= 'A' && karaktere_kode <= 'Z' || karaktere_kode == '_' || karaktere_kode >= 128; }
    static boolean 이름뒤(int karaktere_kode) { return izen_karaktere(karaktere_kode) || karaktere_kode >= '0' && karaktere_kode <= '9'; }
    static void errorea(String Testua) { arbel.입출력전환(0); 단말.Idatzi("Komandoa analizatu_balio: "); 단말.Idatzi(Testua); 단말.문자(10); Egoera_balio = 2; }
    static int Irakurri(int sarrera_ZENBATU, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, BASE_kargu = 중첩깊이 * 4096, karaktre_berezi = 중첩깊이 * 128;
        while (현재자리 < sarrera_ZENBATU) {
            while (현재자리 < sarrera_ZENBATU && (ITURBURUA[BASE_kargu + 현재자리] == 32 || ITURBURUA[BASE_kargu + 현재자리] == 9)) 현재자리++;
            if (현재자리 == sarrera_ZENBATU || ITURBURUA[BASE_kargu + 현재자리] == '#') break;
            if (총수 == 128) { errorea("낱말이 너무 많습니다"); return -1; }
            int HASI_kargu = 현재자리, karaktere_kode = ITURBURUA[BASE_kargu + 현재자리], 자료종류 = 0;
            if (karaktere_kode == ';') { 자료종류 = 1; 현재자리++; }
            else if (karaktere_kode == '&') { if (현재자리 + 1 >= sarrera_ZENBATU || ITURBURUA[BASE_kargu + 현재자리 + 1] != '&') { errorea("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (karaktere_kode == '|') { 현재자리++; 자료종류 = 현재자리 < sarrera_ZENBATU && ITURBURUA[BASE_kargu + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (karaktere_kode == '>') { 현재자리++; 자료종류 = 현재자리 < sarrera_ZENBATU && ITURBURUA[BASE_kargu + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (karaktere_kode == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int Aipua = 0;
                while (현재자리 < sarrera_ZENBATU) {
                    karaktere_kode = ITURBURUA[BASE_kargu + 현재자리];
                    if (karaktere_kode == '`' && Aipua != 39 || karaktere_kode == '$' && Aipua != 39 && 현재자리 + 1 < sarrera_ZENBATU && ITURBURUA[BASE_kargu + 현재자리 + 1] == '(') { errorea("Komandoa EMAITZA 치환은 지원하지 않습니다"); return -1; }
                    if (karaktere_kode == '\\' && Aipua != 39) { if (++현재자리 == sarrera_ZENBATU) { errorea("Marra 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (karaktere_kode == Aipua) { Aipua = 0; 현재자리++; continue; }
                    if (Aipua == 0 && (karaktere_kode == 39 || karaktere_kode == 34)) { Aipua = karaktere_kode; 현재자리++; continue; }
                    if (Aipua == 0 && (karaktere_kode == 32 || karaktere_kode == 9 || karaktere_kode == ';' || karaktere_kode == '&' || karaktere_kode == '|' || karaktere_kode == '<' || karaktere_kode == '>')) break;
                    현재자리++;
                }
                if (Aipua != 0) { errorea("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < sarrera_ZENBATU && (ITURBURUA[BASE_kargu + 현재자리] == '>' || ITURBURUA[BASE_kargu + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > HASI_kargu;
                    for (int Loop_INDIZE = HASI_kargu; Loop_INDIZE < 현재자리; Loop_INDIZE++) if (ITURBURUA[BASE_kargu + Loop_INDIZE] < '0' || ITURBURUA[BASE_kargu + Loop_INDIZE] > '9') 수치 = false;
                    if (수치) { errorea("번호를 지정한 Fitxategia 서술자 S_I 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[karaktre_berezi + 총수] = 자료종류; Exekutatu_2[karaktre_berezi + 총수] = HASI_kargu; 끝[karaktre_berezi + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int Loop_INDIZE = 0; Loop_INDIZE < 총수; Loop_INDIZE++) {
            int 임시값 = 종류[karaktre_berezi + Loop_INDIZE];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDIZE == 총수 || 종류[karaktre_berezi + Loop_INDIZE] != 0) { errorea("S_I 전환에 Fitxategia 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDIZE == 총수 - 1 && 임시값 != 1) { errorea("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[karaktre_berezi + 총수 - 1] != 1) { errorea("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean barruti_SMS(int[] datuak_matrize, int lokal_HASI, int sarrera_ZENBATU, String karaktere_kargu) {
        if (sarrera_ZENBATU != karaktere_kargu.length()) return false; for (int Loop_INDIZE = 0; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) if (datuak_matrize[lokal_HASI + Loop_INDIZE] != karaktere_kargu.charAt(Loop_INDIZE)) return false; return true;
    }
    static void 넣기(int byte_datuak) {
        if (쓴수 >= 명령해석기.token_balio.length) { if (!luzapen_errore) errorea("변수를 펼친 명령이 너무 깁니다"); luzapen_errore = true; return; }
        명령해석기.token_balio[쓴수++] = byte_datuak;
    }
    static void 변수(int[] datuak_matrize, int HASI_kargu, int sarrera_ZENBATU) {
        if (barruti_SMS(datuak_matrize, HASI_kargu, sarrera_ZENBATU, "PWD")) { 넣기('/'); for (int Loop_INDIZE = 0; Loop_INDIZE < Memoria_Fitxategiak.현재길이; Loop_INDIZE++) 넣기(Memoria_Fitxategiak.현재[Loop_INDIZE]); return; }
        if (barruti_SMS(datuak_matrize, HASI_kargu, sarrera_ZENBATU, "HOME")) { 넣기('/'); return; }
        if (barruti_SMS(datuak_matrize, HASI_kargu, sarrera_ZENBATU, "?")) {
            int datuak_balio = Egoera_balio, digitu = 100; boolean 시작여부 = false;
            while (digitu > 0) { int 뒷값 = datuak_balio / digitu; if (뒷값 != 0 || 시작여부 || digitu == 1) { 넣기('0' + 뒷값); 시작여부 = true; } datuak_balio %= digitu; digitu /= 10; } return;
        }
        for (int Loop_INDIZE = 0; Loop_INDIZE < 16; Loop_INDIZE++) if (이름길이[Loop_INDIZE] == sarrera_ZENBATU) {
            boolean BATDATOR = true; for (int barnekoa_kargu = 0; barnekoa_kargu < sarrera_ZENBATU; barnekoa_kargu++) if (변수이름[Loop_INDIZE * 32 + barnekoa_kargu] != datuak_matrize[HASI_kargu + barnekoa_kargu]) BATDATOR = false;
            if (BATDATOR) { for (int barnekoa_kargu = 0; barnekoa_kargu < balio_luzera[Loop_INDIZE]; barnekoa_kargu++) 넣기(변수값[Loop_INDIZE * 256 + barnekoa_kargu]); return; }
        }
    }
    static boolean Word_balio(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Exekutatu_2[중첩깊이 * 128 + 낱말번호], amaitu_kargu = 끝[중첩깊이 * 128 + 낱말번호], BASE_kargu = 중첩깊이 * 4096, Aipua = 0;
        if (읽는자리 < amaitu_kargu && ITURBURUA[BASE_kargu + 읽는자리] == '~' && (읽는자리 + 1 == amaitu_kargu || ITURBURUA[BASE_kargu + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < amaitu_kargu) {
            int karaktere_kode = ITURBURUA[BASE_kargu + 읽는자리++];
            if (karaktere_kode == Aipua) { Aipua = 0; continue; }
            if (Aipua == 0 && (karaktere_kode == 39 || karaktere_kode == 34)) { Aipua = karaktere_kode; continue; }
            if (karaktere_kode == '\\' && Aipua != 39) { int Hurrengoa_kargu = ITURBURUA[BASE_kargu + 읽는자리++]; if (Aipua == 34 && Hurrengoa_kargu != '$' && Hurrengoa_kargu != '"' && Hurrengoa_kargu != '\\') 넣기('\\'); 넣기(Hurrengoa_kargu); continue; }
            if (karaktere_kode == '$' && Aipua != 39 && 읽는자리 < amaitu_kargu) {
                boolean 중괄호자리 = ITURBURUA[BASE_kargu + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < amaitu_kargu && ITURBURUA[BASE_kargu + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < amaitu_kargu && 이름뒤(ITURBURUA[BASE_kargu + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == amaitu_kargu || ITURBURUA[BASE_kargu + 읽는자리] != '}')) { errorea("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(ITURBURUA, BASE_kargu + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(karaktere_kode);
        }
        return !luzapen_errore;
    }
    static int 환경설정(int arg_INDIZE, boolean kendu) {
        int lokal_HASI = 명령해석기.시작점[arg_INDIZE], amaitu_kargu = lokal_HASI + 명령해석기.luzera_balio[arg_INDIZE], 같음자리 = lokal_HASI;
        while (같음자리 < amaitu_kargu && 명령해석기.token_balio[같음자리] != '=') 같음자리++;
        int sarrera_ZENBATU = 같음자리 - lokal_HASI;
        if (sarrera_ZENBATU < 1 || sarrera_ZENBATU > 31 || !izen_karaktere(명령해석기.token_balio[lokal_HASI]) || !kendu && 같음자리 == amaitu_kargu || amaitu_kargu - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDIZE = lokal_HASI; Loop_INDIZE < 같음자리; Loop_INDIZE++) if (!이름뒤(명령해석기.token_balio[Loop_INDIZE])) return 2;
        if (barruti_SMS(명령해석기.token_balio, lokal_HASI, sarrera_ZENBATU, "PWD") || barruti_SMS(명령해석기.token_balio, lokal_HASI, sarrera_ZENBATU, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDIZE = 0; Loop_INDIZE < 16; Loop_INDIZE++) {
            if (이름길이[Loop_INDIZE] == 0) 빈여부 = Loop_INDIZE;
            if (이름길이[Loop_INDIZE] != sarrera_ZENBATU) continue;
            boolean BATDATOR = true; for (int barnekoa_kargu = 0; barnekoa_kargu < sarrera_ZENBATU; barnekoa_kargu++) if (변수이름[Loop_INDIZE * 32 + barnekoa_kargu] != 명령해석기.token_balio[lokal_HASI + barnekoa_kargu]) BATDATOR = false;
            if (BATDATOR) 찾은여부 = Loop_INDIZE;
        }
        if (kendu) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = sarrera_ZENBATU; balio_luzera[찾은여부] = amaitu_kargu - 같음자리 - 1;
        for (int Loop_INDIZE = 0; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) 변수이름[찾은여부 * 32 + Loop_INDIZE] = 명령해석기.token_balio[lokal_HASI + Loop_INDIZE];
        for (int Loop_INDIZE = 같음자리 + 1; Loop_INDIZE < amaitu_kargu; Loop_INDIZE++) 변수값[찾은여부 * 256 + Loop_INDIZE - 같음자리 - 1] = 명령해석기.token_balio[Loop_INDIZE];
        return 0;
    }
    static void 환경보기() {
        단말.Idatzi("HOME=/\nPWD="); Memoria_Fitxategiak.현재쓰기(); 단말.문자(10);
        for (int Loop_INDIZE = 0; Loop_INDIZE < 16; Loop_INDIZE++) if (이름길이[Loop_INDIZE] > 0) {
            for (int barnekoa_kargu = 0; barnekoa_kargu < 이름길이[Loop_INDIZE]; barnekoa_kargu++) arbel.직렬쓰기(변수이름[Loop_INDIZE * 32 + barnekoa_kargu]); 단말.문자('=');
            for (int barnekoa_kargu = 0; barnekoa_kargu < balio_luzera[Loop_INDIZE]; barnekoa_kargu++) arbel.직렬쓰기(변수값[Loop_INDIZE * 256 + barnekoa_kargu]); 단말.문자(10);
        }
    }
    static void exekutatu_komando(int[] datuak_matrize, int 시작변위, int sarrera_ZENBATU, int 중첩깊이) {
        if (중첩깊이 >= 4 || sarrera_ZENBATU > 4096) { errorea("Komandoa 파일의 habiaratze_balio 또는 Marra luzera_balio 제한을 넘었습니다"); return; }
        for (int Loop_INDIZE = 0; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) ITURBURUA[중첩깊이 * 4096 + Loop_INDIZE] = datuak_matrize[시작변위 + Loop_INDIZE];
        int 총수 = Irakurri(sarrera_ZENBATU, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int talde_amaitu = 읽는자리;
            while (talde_amaitu < 총수 && (종류[중첩깊이 * 128 + talde_amaitu] == 0 || 종류[중첩깊이 * 128 + talde_amaitu] >= 4)) talde_amaitu++;
            boolean exekutatu = 조건성립 == 1 || 조건성립 == 2 && Egoera_balio == 0 || 조건성립 == 3 && Egoera_balio != 0;
            if (exekutatu) {
                boolean 이전자리 = false;
                while (읽는자리 < talde_amaitu) {
                    int Hurrengoa_kargu = 읽는자리; while (Hurrengoa_kargu < talde_amaitu && 종류[중첩깊이 * 128 + Hurrengoa_kargu] != 4) Hurrengoa_kargu++;
                    boolean KONEKTATU_Stream = Hurrengoa_kargu < talde_amaitu; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.token_ZENBATU = 0; 쓴수 = 0; luzapen_errore = false;
                    for (int Loop_INDIZE = 읽는자리; Loop_INDIZE < Hurrengoa_kargu; Loop_INDIZE++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDIZE];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { errorea("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDIZE; } else { if (출력쪽 >= 0) { errorea("Irteera 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDIZE; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.token_ZENBATU == 32) { errorea("인수가 너무 많습니다"); return; }
                        int arg_INDIZE = 명령해석기.token_ZENBATU++; 명령해석기.시작점[arg_INDIZE] = 쓴수;
                        if (!Word_balio(Loop_INDIZE, 중첩깊이)) return;
                        명령해석기.luzera_balio[arg_INDIZE] = 쓴수 - 명령해석기.시작점[arg_INDIZE];
                    }
                    연결중 = 이전자리 || KONEKTATU_Stream || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { errorea("interaktibo 명령과 Komandoa 파일은 S_I 전환이나 Stream_balio 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Exekutatu_2(이전자리, KONEKTATU_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int sarrera_kargu = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (sarrera_kargu < 0) continue;
                        int HASI_kargu = 쓴수; if (!Word_balio(sarrera_kargu, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Memoria_Fitxategiak.bide_izen_HASI(쓴수 - HASI_kargu);
                        for (int barnekoa_kargu = HASI_kargu; 처리값 >= 0 && barnekoa_kargu < 쓴수; barnekoa_kargu++) 처리값 = Memoria_Fitxategiak.bide_izen_byte(barnekoa_kargu - HASI_kargu, 명령해석기.token_balio[barnekoa_kargu]);
                        if (처리값 >= 0) 처리값 = Memoria_Fitxategiak.Ireki(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.errorea(처리값); Egoera_balio = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.sarrerako_fitxategi = 처리값; else 셸입출력.출력파일 = 처리값;
                    }
                    셸입출력.Onartu_interaktibo = 중첩깊이 == 0 && 읽는자리 == 0 && Hurrengoa_kargu == 총수;
                    깊이 = 중첩깊이; 명령해석기.EMAITZA = 0; arbel.입출력전환(1);
                    명령해석기.Komandoa();
                    arbel.Terminala(3);
                    int 반환값 = 명령해석기.EMAITZA, Stream_errore = 셸입출력.hutsegite_balio;
                    셸입출력.끝(); 연결중 = false;
                    Egoera_balio = Stream_errore < 0 ? 1 : 반환값;
                    if (Stream_errore < 0) { 명령해석기.errorea(Stream_errore); return; }
                    if (script_amaitu || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = Hurrengoa_kargu + 1;
                }
            }
            if (talde_amaitu < 총수) 조건성립 = 종류[중첩깊이 * 128 + talde_amaitu];
            읽는자리 = talde_amaitu + 1;
        }
    }
    static void exekutatu_fitxategi() {
        if (명령해석기.token_ZENBATU != 2 || 깊이 >= 3) { 명령해석기.EMAITZA = 2; 단말.Idatzi("사용법: sh Fitxategia (habiaratze_balio 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.Bide_izena(1); if (처리값 >= 0) 처리값 = Memoria_Fitxategiak.Ireki(0);
        if (처리값 < 0) { 명령해석기.errorea(처리값); return; }
        int sarrera_ZENBATU = 0, byte_datuak;
        while ((byte_datuak = Memoria_Fitxategiak.Irakurri(처리값)) != 256 && byte_datuak >= 0 && sarrera_ZENBATU < 16384) script_balio[중첩깊이 * 16384 + sarrera_ZENBATU++] = byte_datuak;
        Memoria_Fitxategiak.Itxi(처리값); arbel.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < sarrera_ZENBATU && !script_amaitu;) {
            int amaitu_kargu = 읽는자리; while (amaitu_kargu < sarrera_ZENBATU && script_balio[중첩깊이 * 16384 + amaitu_kargu] != 10) amaitu_kargu++;
            int 유효길이 = amaitu_kargu - 읽는자리; if (유효길이 > 0 && script_balio[중첩깊이 * 16384 + amaitu_kargu - 1] == 13) 유효길이--;
            exekutatu_komando(script_balio, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = amaitu_kargu + 1;
        }
        명령해석기.EMAITZA = Egoera_balio; script_amaitu = false; 깊이 = 중첩깊이 - 1;
    }
}
