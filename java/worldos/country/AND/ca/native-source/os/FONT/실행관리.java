// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Lectura 전용 Executa_ordre 묶음의 ELF32 validar, 인수 desviar_VALOR, 한 번에 한 usuari Procés_VALOR Executa_ordre. */
public final class 실행관리 {
    static final int Inici_usuari_programa = 0x04000000;
    static final int usuari_finalitzar = 0x04400000;
    static final int IMATGE_finalitzar_ADREÇA = 0x04200000;
    static final int arg_Inici = 0x04300000;
    static int arg_COMPT = 0;
    static int[] arg_ADREÇA = new int[16];

    static boolean clip(int Adreça, int durada_VALOR) {
        return Adreça >= Inici_usuari_programa && Adreça < usuari_finalitzar && durada_VALOR >= 0 && durada_VALOR <= usuari_finalitzar - Adreça;
    }

    static int 수(int Adreça) { return 기억공간.정수읽기(Adreça); }
    static int 짧은수(int Adreça) { return dispositiu_VALOR.tancar_Memòria(Adreça) | dispositiu_VALOR.tancar_Memòria(Adreça + 1) << 8; }
    static void 수쓰기(int Adreça, int VALOR) {
        for (int INDEX = 0; INDEX < 4; INDEX++) dispositiu_VALOR.escriure_Memòria(Adreça + INDEX, VALOR >>> (INDEX * 8));
    }

    static int Grup_COMPT() {
        int Adreça = dispositiu_VALOR.실행묶음();
        int Mida = dispositiu_VALOR.실행묶음크기();
        if (Mida < 8 || 수(Adreça) != 0x50414b4a) return 0;
        int element_COMPT = 수(Adreça + 4);
        return element_COMPT >= 0 && element_COMPT <= 32 && element_COMPT <= (Mida - 8) / 24 ? element_COMPT : 0;
    }

    static void introducció_Llista() {
        for (int INDEX = 0; INDEX < Grup_COMPT(); INDEX++) {
            int introducció_VALOR = dispositiu_VALOR.실행묶음() + 8 + INDEX * 24;
            for (int caràcter_VALOR = 0; caràcter_VALOR < 16 && dispositiu_VALOR.tancar_Memòria(introducció_VALOR + caràcter_VALOR) != 0; caràcter_VALOR++)
                SMS_Terminal.문자(dispositiu_VALOR.tancar_Memòria(introducció_VALOR + caràcter_VALOR));
            SMS_Terminal.Escriptura("\n");
        }
    }

    static int BUSCA_introducció(int[] 입력, int Executa_2, int durada_VALOR) {
        if (durada_VALOR <= 0 || durada_VALOR >= 16) return 0;
        for (int INDEX = 0; INDEX < Grup_COMPT(); INDEX++) {
            int introducció_VALOR = dispositiu_VALOR.실행묶음() + 8 + INDEX * 24;
            boolean 같음 = dispositiu_VALOR.tancar_Memòria(introducció_VALOR + durada_VALOR) == 0;
            for (int caràcter_VALOR = 0; caràcter_VALOR < durada_VALOR; caràcter_VALOR++)
                if (입력[Executa_2 + caràcter_VALOR] != dispositiu_VALOR.tancar_Memòria(introducció_VALOR + caràcter_VALOR)) 같음 = false;
            if (같음) return introducció_VALOR;
        }
        return 0;
    }

    static int validar(int Fitxer, int durada_VALOR) {
        if (durada_VALOR < 52 || 수(Fitxer) != 0x464c457f || dispositiu_VALOR.tancar_Memòria(Fitxer + 4) != 1
            || dispositiu_VALOR.tancar_Memòria(Fitxer + 5) != 1 || dispositiu_VALOR.tancar_Memòria(Fitxer + 6) != 1
            || 짧은수(Fitxer + 16) != 2 || 짧은수(Fitxer + 18) != 3 || 수(Fitxer + 20) != 1
            || 짧은수(Fitxer + 40) != 52 || 짧은수(Fitxer + 42) != 32) return -8;
        int introducció_p_VALOR = 수(Fitxer + 24);
        int taula_càrrec = 수(Fitxer + 28);
        int element_COMPT = 짧은수(Fitxer + 44);
        if (element_COMPT == 0 || element_COMPT > 16 || taula_càrrec < 52 || taula_càrrec > durada_VALOR - element_COMPT * 32) return -8;
        boolean 실행가능 = false;
        for (int INDEX = 0; INDEX < element_COMPT; INDEX++) {
            int Cerca_taula = Fitxer + taula_càrrec + INDEX * 32;
            int 종류 = 수(Cerca_taula);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Connecta/analitzador_48ee4b1b 미지원
            if (종류 != 1) continue;
            int Posició = 수(Cerca_taula + 4), Adreça = 수(Cerca_taula + 8), arxiu_canviar_la_mida = 수(Cerca_taula + 16), Memòria_canviar_la_mida = 수(Cerca_taula + 20);
            int alinear_VALOR = 수(Cerca_taula + 28);
            if (Adreça < Inici_usuari_programa || Adreça >= IMATGE_finalitzar_ADREÇA || Memòria_canviar_la_mida < 0 || Memòria_canviar_la_mida > IMATGE_finalitzar_ADREÇA - Adreça
                || arxiu_canviar_la_mida < 0 || arxiu_canviar_la_mida > Memòria_canviar_la_mida || Posició < 0 || (arxiu_canviar_la_mida > 0 && Posició > durada_VALOR - arxiu_canviar_la_mida)
                || (alinear_VALOR != 0 && (alinear_VALOR < 0 || (alinear_VALOR & (alinear_VALOR - 1)) != 0
                    || ((Adreça - Posició) & (alinear_VALOR - 1)) != 0))) return -8;
            for (int frontal_VALOR = 0; frontal_VALOR < INDEX; frontal_VALOR++) {
                int 이전 = Fitxer + taula_càrrec + frontal_VALOR * 32;
                if (수(이전) == 1 && Memòria_canviar_la_mida > 0 && 수(이전 + 20) > 0
                    && Adreça < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < Adreça + Memòria_canviar_la_mida) return -8;
            }
            if ((수(Cerca_taula + 24) & 1) != 0 && introducció_p_VALOR >= Adreça && introducció_p_VALOR - Adreça < arxiu_canviar_la_mida) 실행가능 = true;
        }
        return 실행가능 ? introducció_p_VALOR : -8;
    }

    static int Executa_ordre(int[] 입력, int Executa_2, int durada_VALOR) {
        while (Executa_2 < durada_VALOR && 입력[Executa_2] == ' ') Executa_2++;
        int 끝 = Executa_2;
        while (끝 < durada_VALOR && 입력[끝] != ' ') 끝++;
        int introducció_VALOR = BUSCA_introducció(입력, Executa_2, 끝 - Executa_2);
        if (introducció_VALOR == 0) return -2;
        int Posició = 수(introducció_VALOR + 16), Mida = 수(introducció_VALOR + 20);
        if (Posició < 8 + Grup_COMPT() * 24 || Mida < 52 || Posició > dispositiu_VALOR.실행묶음크기() - Mida) return -8;
        int Fitxer = dispositiu_VALOR.실행묶음() + Posició;
        int introducció_p_VALOR = validar(Fitxer, Mida);
        if (introducció_p_VALOR < 0) return introducció_p_VALOR;
        dispositiu_VALOR.usuari_eliminar_Índex();
        int taula_càrrec = 수(Fitxer + 28), element_COMPT = 짧은수(Fitxer + 44);
        for (int INDEX = 0; INDEX < element_COMPT; INDEX++) {
            int Cerca_taula = Fitxer + taula_càrrec + INDEX * 32;
            if (수(Cerca_taula) != 1) continue;
            int 원본 = Fitxer + 수(Cerca_taula + 4), destinació_VALOR = 수(Cerca_taula + 8), arxiu_canviar_la_mida = 수(Cerca_taula + 16);
            for (int byte_VALOR = 0; byte_VALOR < arxiu_canviar_la_mida; byte_VALOR++) dispositiu_VALOR.escriure_Memòria(destinació_VALOR + byte_VALOR, dispositiu_VALOR.tancar_Memòria(원본 + byte_VALOR));
        }
        arg_COMPT = 0;
        int Store_VALOR = arg_Inici;
        while (끝 < durada_VALOR) {
            while (끝 < durada_VALOR && 입력[끝] == ' ') 끝++;
            if (끝 == durada_VALOR) break;
            if (arg_COMPT == arg_ADREÇA.length) return -22;
            Executa_2 = 끝;
            while (끝 < durada_VALOR && 입력[끝] != ' ') 끝++;
            arg_ADREÇA[arg_COMPT++] = Store_VALOR;
            수쓰기(Store_VALOR, 끝 - Executa_2);
            for (int caràcter_VALOR = Executa_2; caràcter_VALOR < 끝; caràcter_VALOR++) 수쓰기(Store_VALOR + 4 + (caràcter_VALOR - Executa_2) * 4, 입력[caràcter_VALOR]);
            Store_VALOR += 4 + (끝 - Executa_2) * 4;
        }
        xarxa_Pila.NETEJA_Procés();
        파일서술자관리.Inici_Procés();
        int RESULTAT = dispositiu_VALOR.execució_usuari_programa(introducció_p_VALOR, usuari_finalitzar - 16);
        파일서술자관리.NETEJA_Procés();
        xarxa_Pila.NETEJA_Procés();
        return RESULTAT;
    }
}
