// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 usuari punter/길이는 accés_introducció 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int MATRIU_durada(int Adreça) {
        if (!실행관리.clip(Adreça, 4)) return -14;
        int durada_VALOR = 실행관리.수(Adreça);
        if (durada_VALOR < 0 || durada_VALOR > (실행관리.usuari_finalitzar - Adreça - 4) / 4) return -14;
        return durada_VALOR;
    }

    public static int Procés_VALOR_introducció(int INDEX, int 가, int 나, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.crear_arxiu(가, 나, 다);
        if (INDEX == 31) return 파일서술자관리.tancar_arxiu(가, 나, 다);
        if (INDEX == 32) return 파일서술자관리.escriure_arxiu(가, 나, 다);
        if (INDEX == 33) return 파일서술자관리.Tanca_arxiu(가);
        if (INDEX == 34) return 파일서술자관리.cercar_arxiu(가, 나, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (INDEX == 37) return 파일서술자관리.tancar_arxiu_estat(가, 나);
        if (INDEX == 38) return 파일서술자관리.suprimir_arxiu_introducció_nom(가);
        if (INDEX == 39) return 파일서술자관리.conjunt_arxiu_durada(가, 나);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (INDEX == 41) return 파일서술자관리.Crear_extrem(가, 나, 다);
        if (INDEX == 42) return 파일서술자관리.enllaçar_ADREÇA(가, 나, 다);
        if (INDEX == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (INDEX == 46) return 파일서술자관리.conjunt_rebre_TIMEOUT(가, 나);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sincronitzar();
        }
        if (INDEX == 1) {
            int durada_VALOR = MATRIU_durada(가);
            if (durada_VALOR < 0) return durada_VALOR;
            if (durada_VALOR > 4096) return -90;
            for (int caràcter_VALOR = 0; caràcter_VALOR < durada_VALOR; caràcter_VALOR++) SMS_Terminal.문자(실행관리.수(가 + 4 + caràcter_VALOR * 4) & 65535);
            return durada_VALOR;
        }
        if (INDEX == 2) return 실행관리.arg_COMPT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.arg_COMPT ? 실행관리.arg_ADREÇA[가] : 0;
        if (INDEX == 10) return xarxa_Pila.Obre(가);
        if (INDEX == 11) {
            int durada_VALOR = MATRIU_durada(라);
            if (durada_VALOR < 0) return durada_VALOR;
            if (마 < 0 || 마 > durada_VALOR || 마 > 1024) return -90;
            for (int Posició = 0; Posició < 마; Posició++) 임시자료[Posició] = 실행관리.수(라 + 4 + Posició * 4) & 255;
            return xarxa_Pila.enviar(가, 나, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int durada_VALOR = MATRIU_durada(나);
            if (durada_VALOR < 0) return durada_VALOR;
            if (다 < 0 || 다 > 2000) return -22;
            int RESULTAT = xarxa_Pila.rebre(가, 임시자료, durada_VALOR < 1024 ? durada_VALOR : 1024, 다);
            if (RESULTAT >= 0) for (int Posició = 0; Posició < RESULTAT; Posició++) 실행관리.수쓰기(나 + 4 + Posició * 4, 임시자료[Posició]);
            return RESULTAT;
        }
        if (INDEX == 13) return xarxa_Pila.Tanca(가);
        if (INDEX == 14) return xarxa_Pila.내주소;
        if (INDEX == 15) return xarxa_Pila.homòleg_ADREÇA(가);
        if (INDEX == 16) return xarxa_Pila.homòleg_número_de_port(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int nom_canviar_la_mida = MATRIU_durada(가), dades_canviar_la_mida = MATRIU_durada(나);
            if (nom_canviar_la_mida < 0 || dades_canviar_la_mida < 0) return -14;
            if (nom_canviar_la_mida < 1 || nom_canviar_la_mida > 64) return -22;
            int durada_VALOR = 0;
            while (durada_VALOR < nom_canviar_la_mida && 실행관리.수(가 + 4 + durada_VALOR * 4) != 0) {
                Memòria_sistema_d_arxius.Nom[durada_VALOR] = 실행관리.수(가 + 4 + durada_VALOR * 4);
                durada_VALOR++;
            }
            if (!Memòria_sistema_d_arxius.xec_nom(Memòria_sistema_d_arxius.Nom, durada_VALOR)) return -22;
            if (INDEX == 20) {
                int Fitxer = Memòria_sistema_d_arxius.BUSCA_introducció(Memòria_sistema_d_arxius.Nom, durada_VALOR);
                if (Fitxer < 0) return Fitxer;
                int Mida = Memòria_sistema_d_arxius.canviar_la_mida_Llista[Fitxer];
                if (Mida > dades_canviar_la_mida) return -90;
                int Adreça = dispositiu_VALOR.arxiu_Memòria() + Fitxer * Memòria_sistema_d_arxius.최대크기;
                for (int 수 = 0; 수 < Mida; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, dispositiu_VALOR.tancar_Memòria(Adreça + 수));
                return Mida;
            }
            if (다 < 0 || 다 > dades_canviar_la_mida) return -22;
            if (다 > Memòria_sistema_d_arxius.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Memòria_sistema_d_arxius.Editar_VALOR[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return Memòria_sistema_d_arxius.Store_VALOR(Memòria_sistema_d_arxius.Nom, durada_VALOR, Memòria_sistema_d_arxius.Editar_VALOR, 다);
        }
        return -38;
    }
}
