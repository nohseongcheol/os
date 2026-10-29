// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 usuario 과정의 파일서술자와 열린 Ficheiro 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class 파일서술자관리 {
    static final int 서술자한도 = 32;
    static final int de_lectura_e_escrita_marca = 2, crear_introdución = 64, 독점생성 = 128, desmarcar_Contido = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] abrir_agarradoira = new int[서술자한도], 서술자설정 = new int[서술자한도];
    static int[] 종류 = new int[서술자한도], obxectivo_VALOR = new int[서술자한도];
    static int[] Ficheiro_cargo = new int[서술자한도], abrir_Configuración = new int[서술자한도], Material_de_referencia_CONTAR = new int[서술자한도];
    static int[] Rede_agarradoira = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] camiño_nome = new int[64], Transferir_datos = new int[1024];

    static int 기술찾기(int 파일서술자) {
        if (파일서술자 < 0 || 파일서술자 >= 서술자한도) return -9;
        return abrir_agarradoira[파일서술자] - 1;
    }
    static int 빈서술자(int Executar_2) {
        for (int ÍNDICE = Executar_2; ÍNDICE < 서술자한도; ÍNDICE++) if (abrir_agarradoira[ÍNDICE] == 0) return ÍNDICE;
        return -24;
    }
    static int baleiro_agarradoira() {
        for (int ÍNDICE = 0; ÍNDICE < 서술자한도; ÍNDICE++) if (Material_de_referencia_CONTAR[ÍNDICE] == 0) return ÍNDICE;
        return -24;
    }
    static int Conectar(int 서술자, int 기술, int 파일종류, int Ficheiro_obxectivo_VALOR, int Configuración) {
        abrir_agarradoira[서술자] = 기술 + 1; 서술자설정[서술자] = (Configuración & 실행시닫기) != 0 ? 1 : 0;
        종류[기술] = 파일종류; obxectivo_VALOR[기술] = Ficheiro_obxectivo_VALOR; Material_de_referencia_CONTAR[기술] = 1;
        abrir_Configuración[기술] = Configuración & (3 | 이어쓰기 | 기다리지않기); Ficheiro_cargo[기술] = 0;
        Rede_agarradoira[기술] = 0; 수신대기밀리초[기술] = 0;
        return 서술자;
    }
    static void START_Proceso() {
        Limpo_Proceso();
        for (int ÍNDICE = 0; ÍNDICE < 3; ÍNDICE++) Conectar(ÍNDICE, ÍNDICE, 1, ÍNDICE, ÍNDICE == 0 ? 0 : 1);
    }
    static void Limpo_Proceso() {
        for (int ÍNDICE = 0; ÍNDICE < 서술자한도; ÍNDICE++) if (abrir_agarradoira[ÍNDICE] != 0) peche_Ficheiro(ÍNDICE);
    }
    static int peche_Ficheiro(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        abrir_agarradoira[서술자] = 0; 서술자설정[서술자] = 0;
        Material_de_referencia_CONTAR[기술]--;
        if (Material_de_referencia_CONTAR[기술] == 0) {
            if (종류[기술] == 2) Memoria_sistema_de_ficheiros.abrir_CONTAR[obxectivo_VALOR[기술]]--;
            if (종류[기술] == 3 && Rede_agarradoira[기술] != 0) Rede_Montón.Pechar(Rede_agarradoira[기술]);
            종류[기술] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 byte_VALOR 문자열이다. 루트의 한 이름만 지원한다.
    static int 경로읽기(int ENDEREZO) {
        if (!실행관리.clip(ENDEREZO, 1)) return -14;
        int Posición = dispositivo_VALOR.기억읽기(ENDEREZO) == '/' ? 1 : 0;
        for (int duración_VALOR = 0; duración_VALOR < 64; duración_VALOR++) {
            if (!실행관리.clip(ENDEREZO + Posición + duración_VALOR, 1)) return -14;
            int VALOR = dispositivo_VALOR.기억읽기(ENDEREZO + Posición + duración_VALOR);
            camiño_nome[duración_VALOR] = VALOR;
            if (VALOR == 0) return duración_VALOR == 0 ? -2 : (Memoria_sistema_de_ficheiros.cheque_nome(camiño_nome, duración_VALOR) ? duración_VALOR : -22);
            if (VALOR == '/') return -20;
        }
        return -36;
    }
    static int abrir_Ficheiro(int nome_ENDEREZO, int Configuración, int 허가) {
        int duración_VALOR = 경로읽기(nome_ENDEREZO);
        if (duración_VALOR < 0) return duración_VALOR;
        if ((Configuración & ~(3 | crear_introdución | 독점생성 | desmarcar_Contido | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Configuración & 3) == 3 || ((Configuración & desmarcar_Contido) != 0 && (Configuración & 3) == 0)) return -22;
        int Ficheiro = Memoria_sistema_de_ficheiros.Busca_introdución(camiño_nome, duración_VALOR);
        if (Ficheiro >= 0 && (Configuración & (crear_introdución | 독점생성)) == (crear_introdución | 독점생성)) return -17;
        if (Ficheiro == -2 && (Configuración & crear_introdución) == 0) return -2;
        int 서술자 = 빈서술자(0), 기술 = baleiro_agarradoira();
        if (서술자 < 0 || 기술 < 0) return -24;
        if (Ficheiro == -2) {
            int RESULTANTE = Memoria_sistema_de_ficheiros.Store_VALOR(camiño_nome, duración_VALOR, camiño_nome, 0);
            if (RESULTANTE < 0) return RESULTANTE;
            Ficheiro = Memoria_sistema_de_ficheiros.Busca_introdución(camiño_nome, duración_VALOR);
            Memoria_sistema_de_ficheiros.허가들[Ficheiro] = 허가 & 511;
        }
        if (Ficheiro < 0) return Ficheiro;
        if ((Configuración & desmarcar_Contido) != 0) Memoria_sistema_de_ficheiros.크기들[Ficheiro] = 0;
        Memoria_sistema_de_ficheiros.abrir_CONTAR[Ficheiro]++;
        return Conectar(서술자, 기술, 2, Ficheiro, Configuración);
    }
    static int 파일읽기(int 서술자, int datos_ENDEREZO, int duración_VALOR) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (abrir_Configuración[기술] & 3) == 1) return -9;
        if (duración_VALOR < 0) return -22;
        if (duración_VALOR == 0) return 0;
        if (!실행관리.clip(datos_ENDEREZO, duración_VALOR)) return -14;
        if (종류[기술] == 3) return 자료전문받기(서술자, datos_ENDEREZO, duración_VALOR, 0, 0);
        if (종류[기술] == 1) {
            int RECIBIDO_CONTAR = 0;
            while (RECIBIDO_CONTAR < duración_VALOR) {
                int VALOR = SMS_Terminal.직렬읽기();
                if (VALOR < 0) VALOR = teclado.Lectura();
                if (VALOR < 0) {
                    if (RECIBIDO_CONTAR > 0) return RECIBIDO_CONTAR;
                    if ((abrir_Configuración[기술] & 기다리지않기) != 0) return -11;
                    if (dispositivo_VALOR.사용자남은밀리초() <= 10) return -11;
                    Rede_Montón.verificar(); dispositivo_VALOR.잠시양보();
                } else {
                    dispositivo_VALOR.escribir_Memoria(datos_ENDEREZO + RECIBIDO_CONTAR, VALOR); RECIBIDO_CONTAR++;
                }
            }
            return RECIBIDO_CONTAR;
        }
        int Ficheiro = obxectivo_VALOR[기술], Posición = Ficheiro_cargo[기술];
        if (Posición >= Memoria_sistema_de_ficheiros.크기들[Ficheiro]) return 0;
        if (duración_VALOR > Memoria_sistema_de_ficheiros.크기들[Ficheiro] - Posición) duración_VALOR = Memoria_sistema_de_ficheiros.크기들[Ficheiro] - Posición;
        int 원본주소 = dispositivo_VALOR.Ficheiro_Memoria() + Ficheiro * Memoria_sistema_de_ficheiros.최대크기 + Posición;
        for (int ÍNDICE = 0; ÍNDICE < duración_VALOR; ÍNDICE++) dispositivo_VALOR.escribir_Memoria(datos_ENDEREZO + ÍNDICE, dispositivo_VALOR.기억읽기(원본주소 + ÍNDICE));
        Ficheiro_cargo[기술] += duración_VALOR;
        return duración_VALOR;
    }
    static int escribir_Ficheiro(int 서술자, int datos_ENDEREZO, int duración_VALOR) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0 || (abrir_Configuración[기술] & 3) == 0) return -9;
        if (duración_VALOR < 0) return -22;
        if (duración_VALOR == 0) return 0;
        if (!실행관리.clip(datos_ENDEREZO, duración_VALOR)) return -14;
        if (종류[기술] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 destino_VALOR 주소가 필요하다.
        if (종류[기술] == 1) {
            if (duración_VALOR > 16384) duración_VALOR = 16384;
            for (int ÍNDICE = 0; ÍNDICE < duración_VALOR; ÍNDICE++) {
                int VALOR = dispositivo_VALOR.기억읽기(datos_ENDEREZO + ÍNDICE);
                SMS_Terminal.직렬바이트(VALOR); SMS_Terminal.화면문자(VALOR);
            }
            return duración_VALOR;
        }
        int Ficheiro = obxectivo_VALOR[기술], Tamaño = Memoria_sistema_de_ficheiros.크기들[Ficheiro];
        int Posición = (abrir_Configuración[기술] & 이어쓰기) != 0 ? Tamaño : Ficheiro_cargo[기술];
        if (Posición >= Memoria_sistema_de_ficheiros.최대크기) return -27;
        if (duración_VALOR > Memoria_sistema_de_ficheiros.최대크기 - Posición) duración_VALOR = Memoria_sistema_de_ficheiros.최대크기 - Posición;
        int destino_ENDEREZO = dispositivo_VALOR.Ficheiro_Memoria() + Ficheiro * Memoria_sistema_de_ficheiros.최대크기;
        for (int ÍNDICE = Tamaño; ÍNDICE < Posición; ÍNDICE++) dispositivo_VALOR.escribir_Memoria(destino_ENDEREZO + ÍNDICE, 0);
        for (int ÍNDICE = 0; ÍNDICE < duración_VALOR; ÍNDICE++) dispositivo_VALOR.escribir_Memoria(destino_ENDEREZO + Posición + ÍNDICE, dispositivo_VALOR.기억읽기(datos_ENDEREZO + ÍNDICE));
        Ficheiro_cargo[기술] = Posición + duración_VALOR;
        if (Posición + duración_VALOR > Tamaño) Memoria_sistema_de_ficheiros.크기들[Ficheiro] = Posición + duración_VALOR;
        return duración_VALOR;
    }
    static int buscar_Ficheiro(int 서술자, int DESPRAZAMENTO_VALOR, int Project_raíz) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2) return -29;
        if (Project_raíz < 0 || Project_raíz > 2) return -22;
        int Fondo_VALOR = Project_raíz == 0 ? 0 : (Project_raíz == 1 ? Ficheiro_cargo[기술] : Memoria_sistema_de_ficheiros.크기들[obxectivo_VALOR[기술]]);
        if (DESPRAZAMENTO_VALOR > 0 && Fondo_VALOR > 2147483647 - DESPRAZAMENTO_VALOR) return -75;
        if (DESPRAZAMENTO_VALOR < 0 && DESPRAZAMENTO_VALOR < -Fondo_VALOR) return -22;
        Ficheiro_cargo[기술] = Fondo_VALOR + DESPRAZAMENTO_VALOR;
        return Ficheiro_cargo[기술];
    }
    static int 서술자복제(int 서술자, int 새서술자, boolean Asignar_VALOR, int Configuración) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return Asignar_VALOR ? -9 : -22;
        if (Asignar_VALOR && 서술자 == 새서술자) return 새서술자;
        if (Asignar_VALOR) { if (abrir_agarradoira[새서술자] != 0) peche_Ficheiro(새서술자); }
        else { 새서술자 = 빈서술자(새서술자); if (새서술자 < 0) return 새서술자; }
        abrir_agarradoira[새서술자] = 기술 + 1; 서술자설정[새서술자] = Configuración; Material_de_referencia_CONTAR[기술]++;
        return 새서술자;
    }
    static int eliminar_Ficheiro_introdución_nome(int nome_ENDEREZO) {
        int duración_VALOR = 경로읽기(nome_ENDEREZO);
        if (duración_VALOR < 0) return duración_VALOR;
        int Ficheiro = Memoria_sistema_de_ficheiros.Busca_introdución(camiño_nome, duración_VALOR);
        if (Ficheiro < 0) return Ficheiro;
        Memoria_sistema_de_ficheiros.이름들[Ficheiro * 64] = 0;
        return 0;
    }
    static int conxunto_Ficheiro_duración(int 서술자, int duración_VALOR) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (종류[기술] != 2 || (abrir_Configuración[기술] & 3) == 0 || duración_VALOR < 0) return -22;
        if (duración_VALOR > Memoria_sistema_de_ficheiros.최대크기) return -27;
        int Ficheiro = obxectivo_VALOR[기술], ENDEREZO = dispositivo_VALOR.Ficheiro_Memoria() + Ficheiro * Memoria_sistema_de_ficheiros.최대크기;
        for (int ÍNDICE = Memoria_sistema_de_ficheiros.크기들[Ficheiro]; ÍNDICE < duración_VALOR; ÍNDICE++) dispositivo_VALOR.escribir_Memoria(ENDEREZO + ÍNDICE, 0);
        Memoria_sistema_de_ficheiros.크기들[Ficheiro] = duración_VALOR;
        return 0;
    }
    static int 파일상태읽기(int 서술자, int ENDEREZO) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (!실행관리.clip(ENDEREZO, 48)) return -14;
        for (int ÍNDICE = 0; ÍNDICE < 12; ÍNDICE++) 실행관리.수쓰기(ENDEREZO + ÍNDICE * 4, 0);
        int Ficheiro = obxectivo_VALOR[기술], Tamaño = 종류[기술] == 2 ? Memoria_sistema_de_ficheiros.크기들[Ficheiro] : 0;
        int 허가 = 종류[기술] == 2 ? Memoria_sistema_de_ficheiros.허가들[Ficheiro] : 438;
        실행관리.수쓰기(ENDEREZO, 1);
        실행관리.수쓰기(ENDEREZO + 4, 종류[기술] == 2 ? Ficheiro + 1 : 100 + 기술);
        실행관리.수쓰기(ENDEREZO + 8, (종류[기술] == 2 ? 32768 : (종류[기술] == 1 ? 8192 : 49152)) | 허가);
        실행관리.수쓰기(ENDEREZO + 12, 종류[기술] == 2 && Memoria_sistema_de_ficheiros.이름들[Ficheiro * 64] == 0 ? 0 : 1);
        실행관리.수쓰기(ENDEREZO + 28, Tamaño); 실행관리.수쓰기(ENDEREZO + 32, 512);
        실행관리.수쓰기(ENDEREZO + 36, (Tamaño + 511) / 512);
        return 0;
    }
    static int 서술자제어(int 서술자, int Orde, int VALOR) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        if (Orde == 0 || Orde == 1030) return 서술자복제(서술자, VALOR, false, Orde == 1030 ? 1 : 0);
        if (Orde == 1) return 서술자설정[서술자];
        if (Orde == 2) { if ((VALOR & ~1) != 0) return -22; 서술자설정[서술자] = VALOR; return 0; }
        if (Orde == 3) return abrir_Configuración[기술];
        if (Orde == 4) {
            if ((VALOR & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            abrir_Configuración[기술] = (abrir_Configuración[기술] & 3) | (VALOR & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int crear_extremo(int 주소체계, int 통신종류, int 규약번호) {
        if (주소체계 != 2) return -97;
        if (통신종류 != 2) return -93;
        if (규약번호 != 0 && 규약번호 != 17) return -93;
        int 서술자 = 빈서술자(0), 기술 = baleiro_agarradoira();
        if (서술자 < 0 || 기술 < 0) return -24;
        return Conectar(서술자, 기술, 3, 0, de_lectura_e_escrita_marca);
    }
    static int 종단점기술(int 서술자) {
        int 기술 = 기술찾기(서술자);
        if (기술 < 0) return -9;
        return 종류[기술] == 3 ? 기술 : -88;
    }
    static int ENDEREZO_32(int ENDEREZO) {
        return dispositivo_VALOR.기억읽기(ENDEREZO) << 24 | dispositivo_VALOR.기억읽기(ENDEREZO + 1) << 16
            | dispositivo_VALOR.기억읽기(ENDEREZO + 2) << 8 | dispositivo_VALOR.기억읽기(ENDEREZO + 3);
    }
    static int cheque_ENDEREZO(int ENDEREZO, int duración_VALOR) {
        if (duración_VALOR < 16) return -22;
        if (!실행관리.clip(ENDEREZO, 16)) return -14;
        return 실행관리.짧은수(ENDEREZO) == 2 ? 0 : -97;
    }
    static int ligar_ENDEREZO(int 서술자, int ENDEREZO, int duración_VALOR) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        int RESULTANTE = cheque_ENDEREZO(ENDEREZO, duración_VALOR);
        if (RESULTANTE < 0) return RESULTANTE;
        if (Rede_agarradoira[기술] != 0) return -22;
        int Rede_ENDEREZO = ENDEREZO_32(ENDEREZO + 4);
        if (Rede_ENDEREZO != 0 && Rede_ENDEREZO != Rede_Montón.내주소) return -99;
        int número_do_porto = dispositivo_VALOR.기억읽기(ENDEREZO + 2) << 8 | dispositivo_VALOR.기억읽기(ENDEREZO + 3);
        RESULTANTE = Rede_Montón.Abrir(número_do_porto);
        if (RESULTANTE < 0) return RESULTANTE;
        Rede_agarradoira[기술] = RESULTANTE; obxectivo_VALOR[기술] = Rede_ENDEREZO;
        return 0;
    }
    static int Automático_ligar(int 기술) {
        if (Rede_agarradoira[기술] != 0) return 0;
        int RESULTANTE = Rede_Montón.Abrir(0);
        if (RESULTANTE < 0) return RESULTANTE;
        Rede_agarradoira[기술] = RESULTANTE;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 solicitude 구조체로 전달한다.
    static int 자료전문보내기(int 서술자, int datos_ENDEREZO, int duración_VALOR, int Configuración, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (Configuración != 0) return -95;
        if (duración_VALOR < 0 || duración_VALOR > 1024) return -90;
        if (duración_VALOR != 0 && !실행관리.clip(datos_ENDEREZO, duración_VALOR)) return -14;
        if (!실행관리.clip(요청주소, 8)) return -14;
        int ENDEREZO = 실행관리.수(요청주소);
        int RESULTANTE = cheque_ENDEREZO(ENDEREZO, 실행관리.수(요청주소 + 4));
        if (RESULTANTE < 0) return RESULTANTE;
        int número_do_porto = dispositivo_VALOR.기억읽기(ENDEREZO + 2) << 8 | dispositivo_VALOR.기억읽기(ENDEREZO + 3);
        if (número_do_porto == 0) return -22;
        RESULTANTE = Automático_ligar(기술);
        if (RESULTANTE < 0) return RESULTANTE;
        for (int ÍNDICE = 0; ÍNDICE < duración_VALOR; ÍNDICE++) Transferir_datos[ÍNDICE] = dispositivo_VALOR.기억읽기(datos_ENDEREZO + ÍNDICE);
        return Rede_Montón.enviar(Rede_agarradoira[기술], ENDEREZO_32(ENDEREZO + 4), número_do_porto, Transferir_datos, duración_VALOR);
    }
    static void escribir_ENDEREZO(int ENDEREZO, int duración_VALOR, int Rede_ENDEREZO, int número_do_porto) {
        for (int ÍNDICE = 0; ÍNDICE < duración_VALOR && ÍNDICE < 16; ÍNDICE++) {
            int VALOR = 0;
            if (ÍNDICE == 0) VALOR = 2;
            if (ÍNDICE == 2) VALOR = número_do_porto >>> 8;
            if (ÍNDICE == 3) VALOR = número_do_porto;
            if (ÍNDICE >= 4 && ÍNDICE < 8) VALOR = Rede_ENDEREZO >>> (56 - ÍNDICE * 8);
            dispositivo_VALOR.escribir_Memoria(ENDEREZO + ÍNDICE, VALOR & 255);
        }
    }
    static int 자료전문받기(int 서술자, int datos_ENDEREZO, int duración_VALOR, int Configuración, int 요청주소) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if ((Configuración & ~64) != 0) return -95;
        if (duración_VALOR < 0) return -22;
        if (duración_VALOR != 0 && !실행관리.clip(datos_ENDEREZO, duración_VALOR)) return -14;
        int ENDEREZO = 0, ENDEREZO_duración_ENDEREZO = 0, ENDEREZO_duración = 0;
        if (요청주소 != 0) {
            if (!실행관리.clip(요청주소, 8)) return -14;
            ENDEREZO = 실행관리.수(요청주소); ENDEREZO_duración_ENDEREZO = 실행관리.수(요청주소 + 4);
            if (ENDEREZO != 0) {
                if (!실행관리.clip(ENDEREZO_duración_ENDEREZO, 4)) return -14;
                ENDEREZO_duración = 실행관리.수(ENDEREZO_duración_ENDEREZO);
                if (ENDEREZO_duración < 0) return -22;
                if (!실행관리.clip(ENDEREZO, ENDEREZO_duración < 16 ? ENDEREZO_duración : 16)) return -14;
            }
        }
        int RESULTANTE = Automático_ligar(기술);
        if (RESULTANTE < 0) return RESULTANTE;
        int Executar_2 = dispositivo_VALOR.밀리초();
        while (true) {
            RESULTANTE = Rede_Montón.받기(Rede_agarradoira[기술], Transferir_datos, 1024, 0);
            if (RESULTANTE != -11) break;
            if ((Configuración & 64) != 0 || (abrir_Configuración[기술] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[기술] > 0 && dispositivo_VALOR.밀리초() - Executar_2 >= 수신대기밀리초[기술]) return -11;
            if (dispositivo_VALOR.사용자남은밀리초() <= 10) return -11;
            dispositivo_VALOR.잠시양보();
        }
        if (RESULTANTE < 0) return RESULTANTE;
        if (RESULTANTE > duración_VALOR) RESULTANTE = duración_VALOR;
        for (int ÍNDICE = 0; ÍNDICE < RESULTANTE; ÍNDICE++) dispositivo_VALOR.escribir_Memoria(datos_ENDEREZO + ÍNDICE, Transferir_datos[ÍNDICE]);
        if (ENDEREZO != 0) {
            escribir_ENDEREZO(ENDEREZO, ENDEREZO_duración, Rede_Montón.punto_ENDEREZO(Rede_agarradoira[기술]), Rede_Montón.punto_número_do_porto(Rede_agarradoira[기술]));
            실행관리.수쓰기(ENDEREZO_duración_ENDEREZO, 16);
        }
        return RESULTANTE;
    }
    static int 통신주소읽기(int 서술자, int ENDEREZO, int duración_ENDEREZO) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (!실행관리.clip(duración_ENDEREZO, 4)) return -14;
        int duración_VALOR = 실행관리.수(duración_ENDEREZO);
        if (duración_VALOR < 0) return -22;
        if (!실행관리.clip(ENDEREZO, duración_VALOR < 16 ? duración_VALOR : 16)) return -14;
        int 칸 = Rede_Montón.ÍNDICE(Rede_agarradoira[기술]);
        escribir_ENDEREZO(ENDEREZO, duración_VALOR, obxectivo_VALOR[기술], 칸 < 0 ? 0 : Rede_Montón.접속번호들[칸]);
        실행관리.수쓰기(duración_ENDEREZO, 16);
        return 0;
    }
    static int 수신대기정하기(int 서술자, int 밀리초) {
        int 기술 = 종단점기술(서술자);
        if (기술 < 0) return 기술;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[기술] = 밀리초;
        return 0;
    }
}
