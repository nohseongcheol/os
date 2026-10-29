// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 interactiu shell 문법. 파이프는 순차 Executa_ordre, 환경은 같은 셸에서 공유한다. */
public final class shell_sintaxi {
    static int[] FONT = new int[4 * 4096], 종류 = new int[4 * 128], Executa_2 = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], VALOR_durada = new int[16];
    static int[] script_VALOR = new int[4 * 16384];
    static int Estat_VALOR, 깊이, 쓴수;
    static boolean 연결중, script_finalitzar, extensió_error;
    static boolean nom_caràcter(int codi_de_caràcter) { return codi_de_caràcter >= 'a' && codi_de_caràcter <= 'z' || codi_de_caràcter >= 'A' && codi_de_caràcter <= 'Z' || codi_de_caràcter == '_' || codi_de_caràcter >= 128; }
    static boolean 이름뒤(int codi_de_caràcter) { return nom_caràcter(codi_de_caràcter) || codi_de_caràcter >= '0' && codi_de_caràcter <= '9'; }
    static void s_ha_produït_un_error(String SMS) { Tauler.입출력전환(0); 단말.Escriptura("Ordre analitzar_VALOR: "); 단말.Escriptura(SMS); 단말.문자(10); Estat_VALOR = 2; }
    static int Lectura(int introducció_COMPT, int 중첩깊이) {
        int 현재자리 = 0, total_COMPT = 0, BASE_càrrec = 중첩깊이 * 4096, caràcter_especial = 중첩깊이 * 128;
        while (현재자리 < introducció_COMPT) {
            while (현재자리 < introducció_COMPT && (FONT[BASE_càrrec + 현재자리] == 32 || FONT[BASE_càrrec + 현재자리] == 9)) 현재자리++;
            if (현재자리 == introducció_COMPT || FONT[BASE_càrrec + 현재자리] == '#') break;
            if (total_COMPT == 128) { s_ha_produït_un_error("낱말이 너무 많습니다"); return -1; }
            int Inici_càrrec = 현재자리, codi_de_caràcter = FONT[BASE_càrrec + 현재자리], 자료종류 = 0;
            if (codi_de_caràcter == ';') { 자료종류 = 1; 현재자리++; }
            else if (codi_de_caràcter == '&') { if (현재자리 + 1 >= introducció_COMPT || FONT[BASE_càrrec + 현재자리 + 1] != '&') { s_ha_produït_un_error("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (codi_de_caràcter == '|') { 현재자리++; 자료종류 = 현재자리 < introducció_COMPT && FONT[BASE_càrrec + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (codi_de_caràcter == '>') { 현재자리++; 자료종류 = 현재자리 < introducció_COMPT && FONT[BASE_càrrec + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (codi_de_caràcter == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int oferta = 0;
                while (현재자리 < introducció_COMPT) {
                    codi_de_caràcter = FONT[BASE_càrrec + 현재자리];
                    if (codi_de_caràcter == '`' && oferta != 39 || codi_de_caràcter == '$' && oferta != 39 && 현재자리 + 1 < introducció_COMPT && FONT[BASE_càrrec + 현재자리 + 1] == '(') { s_ha_produït_un_error("Ordre RESULTAT 치환은 지원하지 않습니다"); return -1; }
                    if (codi_de_caràcter == '\\' && oferta != 39) { if (++현재자리 == introducció_COMPT) { s_ha_produït_un_error("línia 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (codi_de_caràcter == oferta) { oferta = 0; 현재자리++; continue; }
                    if (oferta == 0 && (codi_de_caràcter == 39 || codi_de_caràcter == 34)) { oferta = codi_de_caràcter; 현재자리++; continue; }
                    if (oferta == 0 && (codi_de_caràcter == 32 || codi_de_caràcter == 9 || codi_de_caràcter == ';' || codi_de_caràcter == '&' || codi_de_caràcter == '|' || codi_de_caràcter == '<' || codi_de_caràcter == '>')) break;
                    현재자리++;
                }
                if (oferta != 0) { s_ha_produït_un_error("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < introducció_COMPT && (FONT[BASE_càrrec + 현재자리] == '>' || FONT[BASE_càrrec + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > Inici_càrrec;
                    for (int Loop_INDEX = Inici_càrrec; Loop_INDEX < 현재자리; Loop_INDEX++) if (FONT[BASE_càrrec + Loop_INDEX] < '0' || FONT[BASE_càrrec + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { s_ha_produït_un_error("번호를 지정한 Fitxer 서술자 E_S 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[caràcter_especial + total_COMPT] = 자료종류; Executa_2[caràcter_especial + total_COMPT] = Inici_càrrec; 끝[caràcter_especial + total_COMPT] = 현재자리; total_COMPT++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < total_COMPT; Loop_INDEX++) {
            int 임시값 = 종류[caràcter_especial + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == total_COMPT || 종류[caràcter_especial + Loop_INDEX] != 0) { s_ha_produït_un_error("E_S 전환에 Fitxer 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == total_COMPT - 1 && 임시값 != 1) { s_ha_produït_un_error("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (total_COMPT > 0 && !낱말 && 종류[caràcter_especial + total_COMPT - 1] != 1) { s_ha_produït_un_error("명령이 빠졌습니다"); return -1; }
        return total_COMPT;
    }
    static boolean interval_SMS(int[] dades_MATRIU, int local_Inici, int introducció_COMPT, String caràcter_càrrec) {
        if (introducció_COMPT != caràcter_càrrec.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < introducció_COMPT; Loop_INDEX++) if (dades_MATRIU[local_Inici + Loop_INDEX] != caràcter_càrrec.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int byte_dades) {
        if (쓴수 >= 명령해석기.testimoni_VALOR.length) { if (!extensió_error) s_ha_produït_un_error("변수를 펼친 명령이 너무 깁니다"); extensió_error = true; return; }
        명령해석기.testimoni_VALOR[쓴수++] = byte_dades;
    }
    static void 변수(int[] dades_MATRIU, int Inici_càrrec, int introducció_COMPT) {
        if (interval_SMS(dades_MATRIU, Inici_càrrec, introducció_COMPT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < Memòria_Fitxers.현재길이; Loop_INDEX++) 넣기(Memòria_Fitxers.현재[Loop_INDEX]); return; }
        if (interval_SMS(dades_MATRIU, Inici_càrrec, introducció_COMPT, "HOME")) { 넣기('/'); return; }
        if (interval_SMS(dades_MATRIU, Inici_càrrec, introducció_COMPT, "?")) {
            int dades_VALOR = Estat_VALOR, dígit = 100; boolean 시작여부 = false;
            while (dígit > 0) { int 뒷값 = dades_VALOR / dígit; if (뒷값 != 0 || 시작여부 || dígit == 1) { 넣기('0' + 뒷값); 시작여부 = true; } dades_VALOR %= dígit; dígit /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == introducció_COMPT) {
            boolean COINCIDEIX = true; for (int interna_càrrec = 0; interna_càrrec < introducció_COMPT; interna_càrrec++) if (변수이름[Loop_INDEX * 32 + interna_càrrec] != dades_MATRIU[Inici_càrrec + interna_càrrec]) COINCIDEIX = false;
            if (COINCIDEIX) { for (int interna_càrrec = 0; interna_càrrec < VALOR_durada[Loop_INDEX]; interna_càrrec++) 넣기(변수값[Loop_INDEX * 256 + interna_càrrec]); return; }
        }
    }
    static boolean Word_VALOR(int 낱말번호, int 중첩깊이) {
        int tancar_cursor = Executa_2[중첩깊이 * 128 + 낱말번호], finalitzar_càrrec = 끝[중첩깊이 * 128 + 낱말번호], BASE_càrrec = 중첩깊이 * 4096, oferta = 0;
        if (tancar_cursor < finalitzar_càrrec && FONT[BASE_càrrec + tancar_cursor] == '~' && (tancar_cursor + 1 == finalitzar_càrrec || FONT[BASE_càrrec + tancar_cursor + 1] == '/')) { 넣기('/'); tancar_cursor++; }
        while (tancar_cursor < finalitzar_càrrec) {
            int codi_de_caràcter = FONT[BASE_càrrec + tancar_cursor++];
            if (codi_de_caràcter == oferta) { oferta = 0; continue; }
            if (oferta == 0 && (codi_de_caràcter == 39 || codi_de_caràcter == 34)) { oferta = codi_de_caràcter; continue; }
            if (codi_de_caràcter == '\\' && oferta != 39) { int Següent_càrrec = FONT[BASE_càrrec + tancar_cursor++]; if (oferta == 34 && Següent_càrrec != '$' && Següent_càrrec != '"' && Següent_càrrec != '\\') 넣기('\\'); 넣기(Següent_càrrec); continue; }
            if (codi_de_caràcter == '$' && oferta != 39 && tancar_cursor < finalitzar_càrrec) {
                boolean 중괄호자리 = FONT[BASE_càrrec + tancar_cursor] == '{'; if (중괄호자리) tancar_cursor++;
                int 처음자리 = tancar_cursor;
                if (tancar_cursor < finalitzar_càrrec && FONT[BASE_càrrec + tancar_cursor] == '?') tancar_cursor++;
                else while (tancar_cursor < finalitzar_càrrec && 이름뒤(FONT[BASE_càrrec + tancar_cursor])) tancar_cursor++;
                if (중괄호자리 && (tancar_cursor == finalitzar_càrrec || FONT[BASE_càrrec + tancar_cursor] != '}')) { s_ha_produït_un_error("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (tancar_cursor == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(FONT, BASE_càrrec + 처음자리, tancar_cursor - 처음자리); if (중괄호자리) tancar_cursor++; continue;
            }
            넣기(codi_de_caràcter);
        }
        return !extensió_error;
    }
    static int entorn_Configuració(int arg_INDEX, boolean suprimir) {
        int local_Inici = 명령해석기.시작점[arg_INDEX], finalitzar_càrrec = local_Inici + 명령해석기.durada_VALOR[arg_INDEX], 같음자리 = local_Inici;
        while (같음자리 < finalitzar_càrrec && 명령해석기.testimoni_VALOR[같음자리] != '=') 같음자리++;
        int introducció_COMPT = 같음자리 - local_Inici;
        if (introducció_COMPT < 1 || introducció_COMPT > 31 || !nom_caràcter(명령해석기.testimoni_VALOR[local_Inici]) || !suprimir && 같음자리 == finalitzar_càrrec || finalitzar_càrrec - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = local_Inici; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.testimoni_VALOR[Loop_INDEX])) return 2;
        if (interval_SMS(명령해석기.testimoni_VALOR, local_Inici, introducció_COMPT, "PWD") || interval_SMS(명령해석기.testimoni_VALOR, local_Inici, introducció_COMPT, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) 빈여부 = Loop_INDEX;
            if (이름길이[Loop_INDEX] != introducció_COMPT) continue;
            boolean COINCIDEIX = true; for (int interna_càrrec = 0; interna_càrrec < introducció_COMPT; interna_càrrec++) if (변수이름[Loop_INDEX * 32 + interna_càrrec] != 명령해석기.testimoni_VALOR[local_Inici + interna_càrrec]) COINCIDEIX = false;
            if (COINCIDEIX) 찾은여부 = Loop_INDEX;
        }
        if (suprimir) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = introducció_COMPT; VALOR_durada[찾은여부] = finalitzar_càrrec - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < introducció_COMPT; Loop_INDEX++) 변수이름[찾은여부 * 32 + Loop_INDEX] = 명령해석기.testimoni_VALOR[local_Inici + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < finalitzar_càrrec; Loop_INDEX++) 변수값[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.testimoni_VALOR[Loop_INDEX];
        return 0;
    }
    static void mostrar_entorn() {
        단말.Escriptura("HOME=/\nPWD="); Memòria_Fitxers.현재쓰기(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int interna_càrrec = 0; interna_càrrec < 이름길이[Loop_INDEX]; interna_càrrec++) Tauler.직렬쓰기(변수이름[Loop_INDEX * 32 + interna_càrrec]); 단말.문자('=');
            for (int interna_càrrec = 0; interna_càrrec < VALOR_durada[Loop_INDEX]; interna_càrrec++) Tauler.직렬쓰기(변수값[Loop_INDEX * 256 + interna_càrrec]); 단말.문자(10);
        }
    }
    static void Executa_ordre(int[] dades_MATRIU, int 시작변위, int introducció_COMPT, int 중첩깊이) {
        if (중첩깊이 >= 4 || introducció_COMPT > 4096) { s_ha_produït_un_error("Ordre 파일의 imbricació_VALOR 또는 línia durada_VALOR 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < introducció_COMPT; Loop_INDEX++) FONT[중첩깊이 * 4096 + Loop_INDEX] = dades_MATRIU[시작변위 + Loop_INDEX];
        int total_COMPT = Lectura(introducció_COMPT, 중첩깊이); if (total_COMPT < 0) return;
        int tancar_cursor = 0, 조건성립 = 1;
        while (tancar_cursor < total_COMPT) {
            int Grup_finalitzar = tancar_cursor;
            while (Grup_finalitzar < total_COMPT && (종류[중첩깊이 * 128 + Grup_finalitzar] == 0 || 종류[중첩깊이 * 128 + Grup_finalitzar] >= 4)) Grup_finalitzar++;
            boolean Executa_cc685ae5 = 조건성립 == 1 || 조건성립 == 2 && Estat_VALOR == 0 || 조건성립 == 3 && Estat_VALOR != 0;
            if (Executa_cc685ae5) {
                boolean 이전자리 = false;
                while (tancar_cursor < Grup_finalitzar) {
                    int Següent_càrrec = tancar_cursor; while (Següent_càrrec < Grup_finalitzar && 종류[중첩깊이 * 128 + Següent_càrrec] != 4) Següent_càrrec++;
                    boolean CONNECTA_flux = Següent_càrrec < Grup_finalitzar; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.testimoni_COMPT = 0; 쓴수 = 0; extensió_error = false;
                    for (int Loop_INDEX = tancar_cursor; Loop_INDEX < Següent_càrrec; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { s_ha_produït_un_error("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (출력쪽 >= 0) { s_ha_produït_un_error("Sortida 전환이 겹쳤습니다"); return; } 출력쪽 = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.testimoni_COMPT == 32) { s_ha_produït_un_error("인수가 너무 많습니다"); return; }
                        int arg_INDEX = 명령해석기.testimoni_COMPT++; 명령해석기.시작점[arg_INDEX] = 쓴수;
                        if (!Word_VALOR(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.durada_VALOR[arg_INDEX] = 쓴수 - 명령해석기.시작점[arg_INDEX];
                    }
                    연결중 = 이전자리 || CONNECTA_flux || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { s_ha_produït_un_error("interactiu 명령과 Ordre 파일은 E_S 전환이나 flux_VALOR 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Executa_2(이전자리, CONNECTA_flux);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int introducció_càrrec = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (introducció_càrrec < 0) continue;
                        int Inici_càrrec = 쓴수; if (!Word_VALOR(introducció_càrrec, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Memòria_Fitxers.camí_Inici(쓴수 - Inici_càrrec);
                        for (int interna_càrrec = Inici_càrrec; 처리값 >= 0 && interna_càrrec < 쓴수; interna_càrrec++) 처리값 = Memòria_Fitxers.camí_byte(interna_càrrec - Inici_càrrec, 명령해석기.testimoni_VALOR[interna_càrrec]);
                        if (처리값 >= 0) 처리값 = Memòria_Fitxers.Obre(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.s_ha_produït_un_error(처리값); Estat_VALOR = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.fitxer_d_entrada = 처리값; else 셸입출력.출력파일 = 처리값;
                    }
                    셸입출력.Permet_interactiu = 중첩깊이 == 0 && tancar_cursor == 0 && Següent_càrrec == total_COMPT;
                    깊이 = 중첩깊이; 명령해석기.RESULTAT = 0; Tauler.입출력전환(1);
                    명령해석기.Ordre();
                    Tauler.Terminal(3);
                    int 반환값 = 명령해석기.RESULTAT, flux_error = 셸입출력.error_VALOR;
                    셸입출력.끝(); 연결중 = false;
                    Estat_VALOR = flux_error < 0 ? 1 : 반환값;
                    if (flux_error < 0) { 명령해석기.s_ha_produït_un_error(flux_error); return; }
                    if (script_finalitzar || 반환값 == -1005) return;
                    이전자리 = true; tancar_cursor = Següent_càrrec + 1;
                }
            }
            if (Grup_finalitzar < total_COMPT) 조건성립 = 종류[중첩깊이 * 128 + Grup_finalitzar];
            tancar_cursor = Grup_finalitzar + 1;
        }
    }
    static void Executa_arxiu() {
        if (명령해석기.testimoni_COMPT != 2 || 깊이 >= 3) { 명령해석기.RESULTAT = 2; 단말.Escriptura("사용법: sh Fitxer (imbricació_VALOR 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.Camí(1); if (처리값 >= 0) 처리값 = Memòria_Fitxers.Obre(0);
        if (처리값 < 0) { 명령해석기.s_ha_produït_un_error(처리값); return; }
        int introducció_COMPT = 0, byte_dades;
        while ((byte_dades = Memòria_Fitxers.Lectura(처리값)) != 256 && byte_dades >= 0 && introducció_COMPT < 16384) script_VALOR[중첩깊이 * 16384 + introducció_COMPT++] = byte_dades;
        Memòria_Fitxers.Tanca(처리값); Tauler.입출력전환(0);
        for (int tancar_cursor = 0; tancar_cursor < introducció_COMPT && !script_finalitzar;) {
            int finalitzar_càrrec = tancar_cursor; while (finalitzar_càrrec < introducció_COMPT && script_VALOR[중첩깊이 * 16384 + finalitzar_càrrec] != 10) finalitzar_càrrec++;
            int 유효길이 = finalitzar_càrrec - tancar_cursor; if (유효길이 > 0 && script_VALOR[중첩깊이 * 16384 + finalitzar_càrrec - 1] == 13) 유효길이--;
            Executa_ordre(script_VALOR, 중첩깊이 * 16384 + tancar_cursor, 유효길이, 중첩깊이); tancar_cursor = finalitzar_càrrec + 1;
        }
        명령해석기.RESULTAT = Estat_VALOR; script_finalitzar = false; 깊이 = 중첩깊이 - 1;
    }
}
