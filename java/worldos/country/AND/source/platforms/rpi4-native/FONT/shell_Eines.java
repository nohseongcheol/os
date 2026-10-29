// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 shell 내장 Eines. */
public final class shell_Eines {
    static int[] dades = new int[16384];
    static int fitxer_d_entrada = -1;
    static int crear_arxiu(int arg_INDEX, int Procés_MODA) {
        int 처리값 = 명령해석기.Camí(arg_INDEX); return 처리값 < 0 ? 처리값 : Memòria_Fitxers.Obre(Procés_MODA);
    }
    static boolean 입력준비(int arg_INDEX) {
        fitxer_d_entrada = -1;
        if (arg_INDEX < 명령해석기.testimoni_COMPT) {
            fitxer_d_entrada = crear_arxiu(arg_INDEX, 0);
            if (fitxer_d_entrada < 0) { 명령해석기.s_ha_produït_un_error(fitxer_d_entrada); return false; }
        }
        return true;
    }
    static int Lectura() {
        if (fitxer_d_entrada >= 3) return Memòria_Fitxers.Lectura(fitxer_d_entrada);
        while (true) {
            int byte_dades = Tauler.직렬읽기(); if (byte_dades == -2 || byte_dades == 4) return 256;
            if (byte_dades == 3) { 명령해석기.RESULTAT = 130; return 256; }
            if (byte_dades >= 0) return byte_dades; Tauler.RENDTO_CPU();
        }
    }
    static void Tanca() { if (fitxer_d_entrada >= 3) Memòria_Fitxers.Tanca(fitxer_d_entrada); fitxer_d_entrada = -1; }
    static void visualitzar_VALOR() {
        int 마지막자리 = 명령해석기.testimoni_COMPT == 1 ? 2 : 명령해석기.testimoni_COMPT;
        for (int arg_INDEX = 1; arg_INDEX < 마지막자리; arg_INDEX++) {
            if (!입력준비(arg_INDEX)) continue;
            int byte_dades; while ((byte_dades = Lectura()) != 256 && byte_dades >= 0) Tauler.직렬쓰기(byte_dades);
            if (byte_dades < 0) 명령해석기.s_ha_produït_un_error(byte_dades); Tanca();
        }
    }
    static void arxiu_cas(String 동작번호) {
        if (명령해석기.testimoni_COMPT != 2) { 명령해석기.RESULTAT = 2; 단말.Escriptura("사용법: mkdir/rmdir/touch Fitxer\n"); return; }
        int 처리값 = 명령해석기.Camí(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Memòria_Fitxers.Crear_directori();
            else if (동작번호.charAt(0) == 'r') 처리값 = Memòria_Fitxers.suprimir_directori();
            else { 처리값 = Memòria_Fitxers.Obre(65); if (처리값 >= 3) 처리값 = Memòria_Fitxers.Tanca(처리값); }
        }
        if (처리값 < 0) 명령해석기.s_ha_produït_un_error(처리값);
    }
    static void copiar_VALOR(boolean 이동여부) {
        if (명령해석기.testimoni_COMPT != 3) { 명령해석기.RESULTAT = 2; 단말.Escriptura("사용법: cp/mv 원본 destinació_extrem (Fitxer)\n"); return; }
        int 처리값 = 명령해석기.Camí(1); if (처리값 >= 0) 처리값 = Memòria_Fitxers.normalitzar_VALOR();
        if (처리값 < 0) { 명령해석기.s_ha_produït_un_error(처리값); return; }
        int 원본번호 = Memòria_Fitxers.BUSCA_introducció(); if (원본번호 < 0) { 명령해석기.s_ha_produït_un_error(-2); return; }
        int introducció_COMPT = Memòria_Fitxers.durada_VALOR[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < introducció_COMPT; Loop_INDEX++) dades[Loop_INDEX] = Memòria_Fitxers.tancar_dades(원본번호, Loop_INDEX);
        처리값 = 명령해석기.Camí(2); if (처리값 >= 0) 처리값 = Memòria_Fitxers.normalitzar_VALOR();
        if (처리값 < 0) { 명령해석기.s_ha_produït_un_error(처리값); return; }
        if (Memòria_Fitxers.BUSCA_introducció() == 원본번호) { if (!이동여부) 명령해석기.s_ha_produït_un_error(-22); return; }
        if (이동여부) { 처리값 = Memòria_Fitxers.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.s_ha_produït_un_error(처리값); return; }
        int 열린파일번호 = Memòria_Fitxers.Obre(577); if (열린파일번호 < 0) { 명령해석기.s_ha_produït_un_error(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < introducció_COMPT; Loop_INDEX++) { 처리값 = Memòria_Fitxers.Escriptura(열린파일번호, dades[Loop_INDEX]); if (처리값 < 0) { 명령해석기.s_ha_produït_un_error(처리값); break; } }
        Memòria_Fitxers.Tanca(열린파일번호);
    }
    static int dígit_VALOR(int arg_INDEX) {
        if (arg_INDEX >= 명령해석기.testimoni_COMPT) return -1;
        int introducció_COMPT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.durada_VALOR[arg_INDEX]; Loop_INDEX++) { int codi_de_caràcter = 명령해석기.testimoni_VALOR[명령해석기.시작점[arg_INDEX] + Loop_INDEX]; if (codi_de_caràcter < '0' || codi_de_caràcter > '9' || introducció_COMPT > 10000) return -1; introducció_COMPT = introducció_COMPT * 10 + codi_de_caràcter - '0'; } return introducció_COMPT;
    }
    static void 세기() {
        int arg_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; arg_INDEX++; }
        if (명령해석기.testimoni_COMPT > arg_INDEX + 1) { 명령해석기.RESULTAT = 2; 단말.Escriptura("사용법: wc [-c|-l|-w] [Fitxer]\n"); return; }
        if (!입력준비(arg_INDEX)) return;
        int byte_COMPT = 0, 줄수 = 0, 낱말수 = 0, byte_dades; boolean 낱말 = false;
        while ((byte_dades = Lectura()) >= 0 && byte_dades != 256) { byte_COMPT++; if (byte_dades == 10) 줄수++; boolean espai = byte_dades == 32 || byte_dades >= 9 && byte_dades <= 13; if (!espai && !낱말) 낱말수++; 낱말 = !espai; }
        Tanca(); if (byte_dades < 0) { 명령해석기.s_ha_produït_un_error(byte_dades); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? byte_COMPT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(byte_COMPT); } 단말.문자(10);
    }
    static void BUSCA_introducció() {
        if (명령해석기.testimoni_COMPT < 2 || 명령해석기.testimoni_COMPT > 3) { 명령해석기.RESULTAT = 2; 단말.Escriptura("사용법: grep 찾을문구 [Fitxer]\n"); return; }
        if (!입력준비(2)) return;
        int introducció_COMPT = 0, byte_dades, 일치수 = 0;
        while (true) {
            byte_dades = Lectura();
            if (byte_dades == 10 || byte_dades == 256 || byte_dades < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= introducció_COMPT - 명령해석기.durada_VALOR[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int interna_càrrec = 0; interna_càrrec < 명령해석기.durada_VALOR[1]; interna_càrrec++) if (dades[Loop_INDEX + interna_càrrec] != 명령해석기.testimoni_VALOR[명령해석기.시작점[1] + interna_càrrec]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (introducció_COMPT > 0 || byte_dades == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < introducció_COMPT; Loop_INDEX++) Tauler.직렬쓰기(dades[Loop_INDEX]); 단말.문자(10); 일치수++; }
                introducció_COMPT = 0; if (byte_dades != 10) break;
            } else if (introducció_COMPT < dades.length) dades[introducció_COMPT++] = byte_dades;
            else { 명령해석기.s_ha_produït_un_error(-28); Tanca(); return; }
        }
        Tanca(); if (byte_dades < 0) 명령해석기.s_ha_produït_un_error(byte_dades); else if (명령해석기.RESULTAT == 0) 명령해석기.RESULTAT = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int arg_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = dígit_VALOR(2); arg_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.testimoni_COMPT > arg_INDEX + 1) { 명령해석기.RESULTAT = 2; 단말.Escriptura("사용법: head/tail [-n 줄수] [Fitxer]\n"); return; }
        if (!입력준비(arg_INDEX)) return;
        int introducció_COMPT = 0, byte_dades;
        while ((byte_dades = Lectura()) != 256 && byte_dades >= 0) { if (introducció_COMPT == dades.length) { 명령해석기.s_ha_produït_un_error(-28); Tanca(); return; } dades[introducció_COMPT++] = byte_dades; }
        Tanca(); if (byte_dades < 0) { 명령해석기.s_ha_produït_un_error(byte_dades); return; }
        int local_Inici = 0, finalitzar_càrrec = introducció_COMPT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int total_COMPT = 0; for (int Loop_INDEX = introducció_COMPT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (dades[Loop_INDEX] == 10 && ++total_COMPT == 줄수) { local_Inici = Loop_INDEX + 1; break; } }
        else { int total_COMPT = 0; for (int Loop_INDEX = 0; Loop_INDEX < introducció_COMPT; Loop_INDEX++) if (dades[Loop_INDEX] == 10 && ++total_COMPT == 줄수) { finalitzar_càrrec = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = local_Inici; Loop_INDEX < finalitzar_càrrec; Loop_INDEX++) Tauler.직렬쓰기(dades[Loop_INDEX]);
    }
    static void escriure_Junts() {
        boolean Annexa = 명령해석기.같음(1, "-a"); int arg_INDEX = Annexa ? 2 : 1;
        if (명령해석기.testimoni_COMPT != arg_INDEX + 1) { 명령해석기.RESULTAT = 2; 단말.Escriptura("사용법: tee [-a] Fitxer\n"); return; }
        int 열린파일번호 = crear_arxiu(arg_INDEX, Annexa ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.s_ha_produït_un_error(열린파일번호); return; }
        fitxer_d_entrada = -1; int byte_dades;
        while ((byte_dades = Lectura()) != 256 && byte_dades >= 0) { int 처리값 = Memòria_Fitxers.Escriptura(열린파일번호, byte_dades); if (처리값 < 0) { 명령해석기.s_ha_produït_un_error(처리값); break; } Tauler.직렬쓰기(byte_dades); }
        Memòria_Fitxers.Tanca(열린파일번호);
    }
}
