// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 usuari 과정의 파일서술자와 열린 Fitxer 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int lectura_escriptura_marcar = 2, Crear_introducció = 64, 독점생성 = 128, eliminar_Índex = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] crear_control = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], objectiu = new int[서술자한도];
    static int[] arxiu_càrrec = new int[서술자한도], crear_Configuració = new int[서술자한도], Referència_COMPT = new int[서술자한도];
    static int[] xarxa_control = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] camí_nom = new int[64], transferir_dades = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return crear_control[파일서술자] - 1;
    }
    static int 빈서술자(int Executa_2) {
        for (int INDEX = Executa_2; INDEX < 서술자한도; INDEX++) if (crear_control[INDEX] == 0) return INDEX;
        return -24;
    }
    static int 빈기술() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (Referència_COMPT[INDEX] == 0) return INDEX;
        return -24;
    }
    static int Connecta(int 서술자, int 기술, int 파일종류, int arxiu_objectiu, int Ajusts) {
        crear_control[서술자] = 기술 + 1; 서술자설정[서술자] = (Ajusts & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; objectiu[기술] = arxiu_objectiu; Referència_COMPT[기술] = 1;
        crear_Configuració[기술] = Ajusts & (3 | 이어쓰기 | 기다리지않기); arxiu_càrrec[기술] = 0;
        xarxa_control[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void Inici_Procés() {
        NETEJA_Procés();
        for (int INDEX = 0; INDEX < 3; INDEX++) Connecta(INDEX, INDEX, 1, INDEX, INDEX == 0 ? 0 : 1);
    }
    static void NETEJA_Procés() {
        for (int INDEX = 0; INDEX < 서술자한도; INDEX++) if (crear_control[INDEX] != 0) Tanca_arxiu(INDEX);
    }
    static int Tanca_arxiu(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        crear_control[서술자] = 0; 서술자설정[서술자] = 0;
        Referència_COMPT[기술]--;
        if (Referència_COMPT[기술] == 0) {
            if (종류[기술] == 2) Memòria_sistema_d_arxius.crear_COMPT[objectiu[기술]]--;
            if (종류[기술] == 3 && xarxa_control[기술] != 0) xarxa_Pila.Tanca(xarxa_control[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 byte_VALOR 문자열이다. 루트의 한 이름만 지원한다.
    static int tancar_camí(int Adreça) {
        if (!실행관리.clip(Adreça, 1)) return -14;
        int Posició = dispositiu_VALOR.tancar_Memòria(Adreça) == '/' ? 1 : 0;
        for (int durada_VALOR = 0; durada_VALOR < 64; durada_VALOR++) {
            if (!실행관리.clip(Adreça + Posició + durada_VALOR, 1)) return -14;
            int VALOR = dispositiu_VALOR.tancar_Memòria(Adreça + Posició + durada_VALOR);
            camí_nom[durada_VALOR] = VALOR;
            if (VALOR == 0) return durada_VALOR == 0 ? -2 : (Memòria_sistema_d_arxius.xec_nom(camí_nom, durada_VALOR) ? durada_VALOR : -22);
            if (VALOR == '/') return -20;
        }
        return -36;
    }
    static int crear_arxiu(int nom_ADREÇA, int Ajusts, int 허가) {
        int durada_VALOR = tancar_camí(nom_ADREÇA);
        if (durada_VALOR < 0) return durada_VALOR;
        if ((Ajusts & ~(3 | Crear_introducció | 독점생성 | eliminar_Índex | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Ajusts & 3) == 3 || ((Ajusts & eliminar_Índex) != 0 && (Ajusts & 3) == 0)) return -22;
        int Fitxer = Memòria_sistema_d_arxius.BUSCA_introducció(camí_nom, durada_VALOR);
        if (Fitxer >= 0 && (Ajusts & (Crear_introducció | 독점생성)) == (Crear_introducció | 독점생성)) return -17;
        if (Fitxer == -2 && (Ajusts & Crear_introducció) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Fitxer == -2) {
            int RESULTAT = Memòria_sistema_d_arxius.Store_VALOR(camí_nom, durada_VALOR, camí_nom, 0);
            if (RESULTAT < 0) return RESULTAT;
            Fitxer = Memòria_sistema_d_arxius.BUSCA_introducció(camí_nom, durada_VALOR);
            Memòria_sistema_d_arxius.허가들[Fitxer] = 허가 & 511;
        }
        if (Fitxer < 0) return Fitxer;
        if ((Ajusts & eliminar_Índex) != 0) Memòria_sistema_d_arxius.canviar_la_mida_Llista[Fitxer] = 0;
        Memòria_sistema_d_arxius.crear_COMPT[Fitxer]++;
        return Connecta(서술자, 기술, 2, Fitxer, Ajusts);
    }
    static int tancar_arxiu(int 서술자, int dades_ADREÇA, int durada_VALOR) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (crear_Configuració[기술] & 3) == 1) return -9;
        if (durada_VALOR < 0) return -22;
        if (durada_VALOR == 0) return 0;
        if (!실행관리.clip(dades_ADREÇA, durada_VALOR)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, dades_ADREÇA, durada_VALOR, 0, 0);
        if (종류[기술] == 1) {
            int CANTIDAD_RECIBIDA_COMPT = 0;
            while (CANTIDAD_RECIBIDA_COMPT < durada_VALOR) {
                int VALOR = SMS_Terminal.직렬읽기();
                if (VALOR < 0) VALOR = teclat.Lectura();
                if (VALOR < 0) {
                    if (CANTIDAD_RECIBIDA_COMPT > 0) return CANTIDAD_RECIBIDA_COMPT;
                    if ((crear_Configuració[기술] & 기다리지않기) != 0) return -11;
                    if (dispositiu_VALOR.사용자남은밀리초() <= 10) return -11;
                    xarxa_Pila.verificar(); dispositiu_VALOR.잠시양보();
                } else {
                    dispositiu_VALOR.escriure_Memòria(dades_ADREÇA + CANTIDAD_RECIBIDA_COMPT, VALOR); CANTIDAD_RECIBIDA_COMPT++;
                }
            }
            return CANTIDAD_RECIBIDA_COMPT;
        }
        int Fitxer = objectiu[기술], Posició = arxiu_càrrec[기술];
        if (Posició >= Memòria_sistema_d_arxius.canviar_la_mida_Llista[Fitxer]) return 0;
        if (durada_VALOR > Memòria_sistema_d_arxius.canviar_la_mida_Llista[Fitxer] - Posició) durada_VALOR = Memòria_sistema_d_arxius.canviar_la_mida_Llista[Fitxer] - Posició;
        int 원본주소 = dispositiu_VALOR.arxiu_Memòria() + Fitxer * Memòria_sistema_d_arxius.최대크기 + Posició;
        for (int INDEX = 0; INDEX < durada_VALOR; INDEX++) dispositiu_VALOR.escriure_Memòria(dades_ADREÇA + INDEX, dispositiu_VALOR.tancar_Memòria(원본주소 + INDEX));
        arxiu_càrrec[기술] += durada_VALOR;
        return durada_VALOR;
    }
    static int escriure_arxiu(int 서술자, int dades_ADREÇA, int durada_VALOR) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (crear_Configuració[기술] & 3) == 0) return -9;
        if (durada_VALOR < 0) return -22;
        if (durada_VALOR == 0) return 0;
        if (!실행관리.clip(dades_ADREÇA, durada_VALOR)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 destinació_VALOR 주소가 필요하다.
        if (종류[기술] == 1) {
            if (durada_VALOR > 16384) durada_VALOR = 16384;
            for (int INDEX = 0; INDEX < durada_VALOR; INDEX++) {
                int VALOR = dispositiu_VALOR.tancar_Memòria(dades_ADREÇA + INDEX);
                SMS_Terminal.직렬바이트(VALOR); SMS_Terminal.화면문자(VALOR);
            }
            return durada_VALOR;
        }
        int Fitxer = objectiu[기술], Mida = Memòria_sistema_d_arxius.canviar_la_mida_Llista[Fitxer];
        int Posició = (crear_Configuració[기술] & 이어쓰기) != 0 ? Mida : arxiu_càrrec[기술];
        if (Posició >= Memòria_sistema_d_arxius.최대크기) return -27;
        if (durada_VALOR > Memòria_sistema_d_arxius.최대크기 - Posició) durada_VALOR = Memòria_sistema_d_arxius.최대크기 - Posició;
        int destinació_ADREÇA = dispositiu_VALOR.arxiu_Memòria() + Fitxer * Memòria_sistema_d_arxius.최대크기;
        for (int INDEX = Mida; INDEX < Posició; INDEX++) dispositiu_VALOR.escriure_Memòria(destinació_ADREÇA + INDEX, 0);
        for (int INDEX = 0; INDEX < durada_VALOR; INDEX++) dispositiu_VALOR.escriure_Memòria(destinació_ADREÇA + Posició + INDEX, dispositiu_VALOR.tancar_Memòria(dades_ADREÇA + INDEX));
        arxiu_càrrec[기술] = Posició + durada_VALOR;
        if (Posició + durada_VALOR > Mida) Memòria_sistema_d_arxius.canviar_la_mida_Llista[Fitxer] = Posició + durada_VALOR;
        return durada_VALOR;
    }
    static int cercar_arxiu(int 서술자, int DESPLAÇAMENT_VALOR, int Project_rel) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (Project_rel < 0 || Project_rel > 2) return -22;
        int Fons_VALOR = Project_rel == 0 ? 0 : (Project_rel == 1 ? arxiu_càrrec[기술] : Memòria_sistema_d_arxius.canviar_la_mida_Llista[objectiu[기술]]);
        if (DESPLAÇAMENT_VALOR > 0 && Fons_VALOR > 2147483647 - DESPLAÇAMENT_VALOR) return -75;
        if (DESPLAÇAMENT_VALOR < 0 && DESPLAÇAMENT_VALOR < -Fons_VALOR) return -22;
        arxiu_càrrec[기술] = Fons_VALOR + DESPLAÇAMENT_VALOR;
        return arxiu_càrrec[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean cedir_VALOR, int Ajusts) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return cedir_VALOR ? -9 : -22;
        if (cedir_VALOR && 서술자 == 새서술자) return 새서술자;
        if (cedir_VALOR) { if (crear_control[새서술자] != 0) Tanca_arxiu(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        crear_control[새서술자] = 기술 + 1; 서술자설정[새서술자] = Ajusts; Referència_COMPT[기술]++;
        return 새서술자;
    }
    static int suprimir_arxiu_introducció_nom(int nom_ADREÇA) {
        int durada_VALOR = tancar_camí(nom_ADREÇA);
        if (durada_VALOR < 0) return durada_VALOR;
        int Fitxer = Memòria_sistema_d_arxius.BUSCA_introducció(camí_nom, durada_VALOR);
        if (Fitxer < 0) return Fitxer;
        Memòria_sistema_d_arxius.이름들[Fitxer * 64] = 0;
        return 0;
    }
    static int conjunt_arxiu_durada(int 서술자, int durada_VALOR) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (crear_Configuració[기술] & 3) == 0 || durada_VALOR < 0) return -22;
        if (durada_VALOR > Memòria_sistema_d_arxius.최대크기) return -27;
        int Fitxer = objectiu[기술], Adreça = dispositiu_VALOR.arxiu_Memòria() + Fitxer * Memòria_sistema_d_arxius.최대크기;
        for (int INDEX = Memòria_sistema_d_arxius.canviar_la_mida_Llista[Fitxer]; INDEX < durada_VALOR; INDEX++) dispositiu_VALOR.escriure_Memòria(Adreça + INDEX, 0);
        Memòria_sistema_d_arxius.canviar_la_mida_Llista[Fitxer] = durada_VALOR;
        return 0;
    }
    static int tancar_arxiu_estat(int 서술자, int Adreça) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.clip(Adreça, 48)) return -14;
        for (int INDEX = 0; INDEX < 12; INDEX++) 실행관리.수쓰기(Adreça + INDEX * 4, 0);
        int Fitxer = objectiu[기술], Mida = 종류[기술] == 2 ? Memòria_sistema_d_arxius.canviar_la_mida_Llista[Fitxer] : 0;
        int 허가 = 종류[기술] == 2 ? Memòria_sistema_d_arxius.허가들[Fitxer] : 438;
        실행관리.수쓰기(Adreça, 1);
        실행관리.수쓰기(Adreça + 4, 종류[기술] == 2 ? Fitxer + 1 : 100 + 기술);
        실행관리.수쓰기(Adreça + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(Adreça + 12, 종류[기술] == 2 && Memòria_sistema_d_arxius.이름들[Fitxer * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(Adreça + 28, Mida); 실행관리.수쓰기(Adreça + 32, 512);
        실행관리.수쓰기(Adreça + 36, (Mida + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Ordre, int VALOR) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Ordre == 0 || Ordre == 1030) return 서술자복제(서술자, VALOR, false, Ordre == 1030 ? 1 : 0);
        if (Ordre == 1) return 서술자설정[서술자];
        if (Ordre == 2) { if ((VALOR & ~1) != 0) return -22; 서술자설정[서술자] = VALOR; return 0; }
        if (Ordre == 3) return crear_Configuració[기술];
        if (Ordre == 4) {
            if ((VALOR & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            crear_Configuració[기술] = (crear_Configuració[기술] & 3) | (VALOR & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int Crear_extrem(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = 빈기술();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Connecta(서술자, 기술, 3, 0, lectura_escriptura_marcar);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int ADREÇA_32(int Adreça) {
        return dispositiu_VALOR.tancar_Memòria(Adreça) << 24 | dispositiu_VALOR.tancar_Memòria(Adreça + 1) << 16
            | dispositiu_VALOR.tancar_Memòria(Adreça + 2) << 8 | dispositiu_VALOR.tancar_Memòria(Adreça + 3);
    }
    static int xec_ADREÇA(int Adreça, int durada_VALOR) {
        if (durada_VALOR < 16) return -22;
        if (!실행관리.clip(Adreça, 16)) return -14;
        return 실행관리.짧은수(Adreça) == 2 ? 0 : -97;
    }
    static int enllaçar_ADREÇA(int 서술자, int Adreça, int durada_VALOR) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int RESULTAT = xec_ADREÇA(Adreça, durada_VALOR);
        if (RESULTAT < 0) return RESULTAT;
        if (xarxa_control[기술] != 0) return -22;
        int xarxa_ADREÇA = ADREÇA_32(Adreça + 4);
        if (xarxa_ADREÇA != 0 && xarxa_ADREÇA != xarxa_Pila.내주소) return -99;
        int número_de_port = dispositiu_VALOR.tancar_Memòria(Adreça + 2) << 8 | dispositiu_VALOR.tancar_Memòria(Adreça + 3);
        RESULTAT = xarxa_Pila.Obre(número_de_port);
        if (RESULTAT < 0) return RESULTAT;
        xarxa_control[기술] = RESULTAT; objectiu[기술] = xarxa_ADREÇA;
        return 0;
    }
    static int Automàtic_enllaçar(int 기술) {
        if (xarxa_control[기술] != 0) return 0;
        int RESULTAT = xarxa_Pila.Obre(0);
        if (RESULTAT < 0) return RESULTAT;
        xarxa_control[기술] = RESULTAT;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 sol_licitud 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int dades_ADREÇA, int durada_VALOR, int Ajusts, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Ajusts != 0) return -95;
        if (durada_VALOR < 0 || durada_VALOR > 1024) return -90;
        if (durada_VALOR != 0 && !실행관리.clip(dades_ADREÇA, durada_VALOR)) return -14;
        if (!실행관리.clip(요청주소, 8)) return -14;
        int Adreça = 실행관리.수(요청주소);
        int RESULTAT = xec_ADREÇA(Adreça, 실행관리.수(요청주소 + 4));
        if (RESULTAT < 0) return RESULTAT;
        int número_de_port = dispositiu_VALOR.tancar_Memòria(Adreça + 2) << 8 | dispositiu_VALOR.tancar_Memòria(Adreça + 3);
        if (número_de_port == 0) return -22;
        RESULTAT = Automàtic_enllaçar(기술);
        if (RESULTAT < 0) return RESULTAT;
        for (int INDEX = 0; INDEX < durada_VALOR; INDEX++) transferir_dades[INDEX] = dispositiu_VALOR.tancar_Memòria(dades_ADREÇA + INDEX);
        return xarxa_Pila.enviar(xarxa_control[기술], ADREÇA_32(Adreça + 4), número_de_port, transferir_dades, durada_VALOR);
    }
    static void escriure_ADREÇA(int Adreça, int durada_VALOR, int xarxa_ADREÇA, int número_de_port) {
        for (int INDEX = 0; INDEX < durada_VALOR && INDEX < 16; INDEX++) {
            int VALOR = 0;
            if (INDEX == 0) VALOR = 2;
            if (INDEX == 2) VALOR = número_de_port >>> 8;
            if (INDEX == 3) VALOR = número_de_port;
            if (INDEX >= 4 && INDEX < 8) VALOR = xarxa_ADREÇA >>> (56 - INDEX * 8);
            dispositiu_VALOR.escriure_Memòria(Adreça + INDEX, VALOR & 255);
        }
    }
    static int 자료전문받기(int 서술자, int dades_ADREÇA, int durada_VALOR, int Ajusts, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Ajusts & ~64) != 0) return -95;
        if (durada_VALOR < 0) return -22;
        if (durada_VALOR != 0 && !실행관리.clip(dades_ADREÇA, durada_VALOR)) return -14;
        int Adreça = 0, ADREÇA_durada_ADREÇA = 0, ADREÇA_durada = 0;
        if (요청주소 != 0) {
            if (!실행관리.clip(요청주소, 8)) return -14;
            Adreça = 실행관리.수(요청주소); ADREÇA_durada_ADREÇA = 실행관리.수(요청주소 + 4);
            if (Adreça != 0) {
                if (!실행관리.clip(ADREÇA_durada_ADREÇA, 4)) return -14;
                ADREÇA_durada = 실행관리.수(ADREÇA_durada_ADREÇA);
                if (ADREÇA_durada < 0) return -22;
                if (!실행관리.clip(Adreça, ADREÇA_durada < 16 ? ADREÇA_durada : 16)) return -14;
            }
        }
        int RESULTAT = Automàtic_enllaçar(기술);
        if (RESULTAT < 0) return RESULTAT;
        int Executa_2 = dispositiu_VALOR.밀리초();
        while (true) {
            RESULTAT = xarxa_Pila.rebre(xarxa_control[기술], transferir_dades, 1024, 0);
            if (RESULTAT != -11) break;
            if ((Ajusts & 64) != 0 || (crear_Configuració[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && dispositiu_VALOR.밀리초() - Executa_2 >= 수신대기밀리초[기술]) return -11;
            if (dispositiu_VALOR.사용자남은밀리초() <= 10) return -11;
            dispositiu_VALOR.잠시양보();
        }
        if (RESULTAT < 0) return RESULTAT;
        if (RESULTAT > durada_VALOR) RESULTAT = durada_VALOR;
        for (int INDEX = 0; INDEX < RESULTAT; INDEX++) dispositiu_VALOR.escriure_Memòria(dades_ADREÇA + INDEX, transferir_dades[INDEX]);
        if (Adreça != 0) {
            escriure_ADREÇA(Adreça, ADREÇA_durada, xarxa_Pila.homòleg_ADREÇA(xarxa_control[기술]), xarxa_Pila.homòleg_número_de_port(xarxa_control[기술]));
            실행관리.수쓰기(ADREÇA_durada_ADREÇA, 16);
        }
        return RESULTAT;
    }
    static int 통신주소읽기(int 서술자, int Adreça, int durada_ADREÇA) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.clip(durada_ADREÇA, 4)) return -14;
        int durada_VALOR = 실행관리.수(durada_ADREÇA);
        if (durada_VALOR < 0) return -22;
        if (!실행관리.clip(Adreça, durada_VALOR < 16 ? durada_VALOR : 16)) return -14;
        int 칸 = xarxa_Pila.INDEX(xarxa_control[기술]);
        escriure_ADREÇA(Adreça, durada_VALOR, objectiu[기술], 칸 < 0 ? 0 : xarxa_Pila.접속번호들[칸]);
        실행관리.수쓰기(durada_ADREÇA, 16);
        return 0;
    }
    static int conjunt_rebre_TIMEOUT(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
