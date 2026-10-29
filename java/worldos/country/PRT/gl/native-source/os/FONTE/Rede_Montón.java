// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** estático_VALOR IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Rede_Montón {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Rede_máscara = 0xffffff00; /* ip.conf:NETMASK */
    static final int pasarela_VALOR = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECIBIDO_duración = new int[4], RECIBIDO_ENDEREZO = new int[4], RECIBIDO_número_do_porto = new int[4];
    static int[] RECIBIDO_datos = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, 식별자 = 0, 폐기수 = 0;

    static int número_enteiro_16(int[] marco_ÍNDICE, int Posición) { return (marco_ÍNDICE[Posición] << 8) | marco_ÍNDICE[Posición + 1]; }
    static int número_enteiro_32(int[] marco_ÍNDICE, int Posición) { return (número_enteiro_16(marco_ÍNDICE, Posición) << 16) | número_enteiro_16(marco_ÍNDICE, Posición + 2); }
    static void 넣기16(int[] marco_ÍNDICE, int Posición, int VALOR) { marco_ÍNDICE[Posición] = (VALOR >>> 8) & 255; marco_ÍNDICE[Posición + 1] = VALOR & 255; }
    static void 넣기32(int[] marco_ÍNDICE, int Posición, int VALOR) { 넣기16(marco_ÍNDICE, Posición, VALOR >>> 16); 넣기16(marco_ÍNDICE, Posición + 2, VALOR); }
    static int SUMA_VALOR(int[] marco_ÍNDICE, int Executar_2, int duración_VALOR, int VALOR) {
        for (int ÍNDICE = 0; ÍNDICE < duración_VALOR; ÍNDICE += 2)
            VALOR += (marco_ÍNDICE[Executar_2 + ÍNDICE] << 8) | (ÍNDICE + 1 < duración_VALOR ? marco_ÍNDICE[Executar_2 + ÍNDICE + 1] : 0);
        while ((VALOR >>> 16) != 0) VALOR = (VALOR & 65535) + (VALOR >>> 16);
        return VALOR;
    }
    static int 가상머리합(int 출발, int 도착, int duración_VALOR) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + duración_VALOR;
    }

    static void Limpo_Proceso() {
        for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) {
            접속번호들[ÍNDICE] = 0; RECIBIDO_duración[ÍNDICE] = -1; RECIBIDO_ENDEREZO[ÍNDICE] = 0; RECIBIDO_número_do_porto[ÍNDICE] = 0;
        }
        for (int ÍNDICE = 0; ÍNDICE < 64; ÍNDICE++) if (Rede_controlador.받기(입력틀) == 0) break;
    }
    static int ÍNDICE(int agarradoira_VALOR) { return agarradoira_VALOR >= 3 && agarradoira_VALOR < 7 && 접속번호들[agarradoira_VALOR - 3] != 0 ? agarradoira_VALOR - 3 : -1; }
    static int Abrir(int número_do_porto) {
        if (Rede_controlador.입출력기준주소 == 0) return -19;
        if (número_do_porto < 0 || número_do_porto > 65535) return -22;
        if (número_do_porto != 0) for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) if (접속번호들[ÍNDICE] == número_do_porto) return -98;
        for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) if (접속번호들[ÍNDICE] == 0) {
            if (número_do_porto == 0) {
                número_do_porto = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int frontal_VALOR = 0; frontal_VALOR < 4; frontal_VALOR++) if (접속번호들[frontal_VALOR] == número_do_porto) 겹침 = true;
                    if (겹침) número_do_porto++;
                }
            }
            접속번호들[ÍNDICE] = número_do_porto; RECIBIDO_duración[ÍNDICE] = -1;
            return ÍNDICE + 3;
        }
        return -24;
    }
    static int Pechar(int agarradoira_VALOR) {
        int 칸 = ÍNDICE(agarradoira_VALOR);
        if (칸 < 0) return -9;
        접속번호들[칸] = 0; RECIBIDO_duración[칸] = -1;
        return 0;
    }
    static int punto_ENDEREZO(int agarradoira_VALOR) { int 칸 = ÍNDICE(agarradoira_VALOR); return 칸 < 0 ? -9 : RECIBIDO_ENDEREZO[칸]; }
    static int punto_número_do_porto(int agarradoira_VALOR) { int 칸 = ÍNDICE(agarradoira_VALOR); return 칸 < 0 ? -9 : RECIBIDO_número_do_porto[칸]; }

    static void 바깥머리(int 종류, boolean difundir_VALOR) {
        for (int ÍNDICE = 0; ÍNDICE < 6; ÍNDICE++) {
            출력틀[ÍNDICE] = difundir_VALOR ? 255 : 찾은장치[ÍNDICE];
            출력틀[6 + ÍNDICE] = Rede_controlador.dispositivo_ENDEREZO[ÍNDICE];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void solicitude_ENDEREZO(int destino_VALOR) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int ÍNDICE = 0; ÍNDICE < 6; ÍNDICE++) {
            출력틀[22 + ÍNDICE] = Rede_controlador.dispositivo_ENDEREZO[ÍNDICE]; 출력틀[32 + ÍNDICE] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, destino_VALOR);
        Rede_controlador.enviar(출력틀, 42);
    }
    static void Proceso_ENDEREZO(int duración_VALOR) {
        if (duración_VALOR < 42 || número_enteiro_16(입력틀, 14) != 1 || número_enteiro_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || número_enteiro_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = número_enteiro_16(입력틀, 20), punto_VALOR = número_enteiro_32(입력틀, 28);
        if (종류 == 2 && punto_VALOR == 찾을주소) {
            for (int ÍNDICE = 0; ÍNDICE < 6; ÍNDICE++) {
                if (입력틀[6 + ÍNDICE] != 입력틀[22 + ÍNDICE] || 입력틀[32 + ÍNDICE] != Rede_controlador.dispositivo_ENDEREZO[ÍNDICE]) return;
            }
            for (int ÍNDICE = 0; ÍNDICE < 6; ÍNDICE++) 찾은장치[ÍNDICE] = 입력틀[22 + ÍNDICE];
            찾은주소 = punto_VALOR;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int ÍNDICE = 0; ÍNDICE < 6; ÍNDICE++) {
                출력틀[ÍNDICE] = 입력틀[22 + ÍNDICE]; 출력틀[32 + ÍNDICE] = 입력틀[22 + ÍNDICE];
                출력틀[22 + ÍNDICE] = Rede_controlador.dispositivo_ENDEREZO[ÍNDICE];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, punto_VALOR);
            Rede_controlador.enviar(출력틀, 42);
        }
    }

    static void Proceso_marco(int duración_VALOR) {
        if (duración_VALOR < 14 || duración_VALOR > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, difundir_VALOR = true;
        for (int ÍNDICE = 0; ÍNDICE < 6; ÍNDICE++) {
            if (입력틀[ÍNDICE] != Rede_controlador.dispositivo_ENDEREZO[ÍNDICE]) 자기 = false;
            if (입력틀[ÍNDICE] != 255) difundir_VALOR = false;
        }
        if (!자기 && !difundir_VALOR) return;
        if (número_enteiro_16(입력틀, 12) == 0x0806) { Proceso_ENDEREZO(duración_VALOR); return; }
        if (número_enteiro_16(입력틀, 12) != 0x0800) return;
        if (duración_VALOR < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Cabeceira_duración = (입력틀[14] & 15) * 4, 전체길이 = número_enteiro_16(입력틀, 16);
        if (Cabeceira_duración < 20 || Cabeceira_duración > 60 || 전체길이 < Cabeceira_duración + 8 || 전체길이 > duración_VALOR - 14
            || (número_enteiro_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || número_enteiro_32(입력틀, 30) != 내주소 || SUMA_VALOR(입력틀, 14, Cabeceira_duración, 0) != 65535) { 폐기수++; return; }
        int Executar_2 = 14 + Cabeceira_duración, datos_duración = número_enteiro_16(입력틀, Executar_2 + 4);
        if (datos_duración < 8 || datos_duración != 전체길이 - Cabeceira_duración || datos_duración > 1032) { 폐기수++; return; }
        int 출발 = número_enteiro_32(입력틀, 26);
        if (número_enteiro_16(입력틀, Executar_2 + 6) != 0 && SUMA_VALOR(입력틀, Executar_2, datos_duración, 가상머리합(출발, 내주소, datos_duración)) != 65535) {
            폐기수++; return;
        }
        int destino_VALOR = número_enteiro_16(입력틀, Executar_2 + 2);
        for (int 칸 = 0; 칸 < 4; 칸++) if (접속번호들[칸] != 0 && 접속번호들[칸] == destino_VALOR) {
            if (RECIBIDO_duración[칸] >= 0) { 폐기수++; return; }
            RECIBIDO_duración[칸] = datos_duración - 8; RECIBIDO_ENDEREZO[칸] = 출발; RECIBIDO_número_do_porto[칸] = número_enteiro_16(입력틀, Executar_2);
            for (int ÍNDICE = 0; ÍNDICE < datos_duración - 8; ÍNDICE++) RECIBIDO_datos[칸 * 1024 + ÍNDICE] = 입력틀[Executar_2 + 8 + ÍNDICE];
            return;
        }
    }

    static void verificar() {
        for (int ÍNDICE = 0; ÍNDICE < 16; ÍNDICE++) {
            int duración_VALOR = Rede_controlador.받기(입력틀);
            if (duración_VALOR == 0) return;
            Proceso_marco(duración_VALOR);
        }
    }
    static int Busca_ENDEREZO(int ENDEREZO) {
        if (ENDEREZO == 0 || ENDEREZO == -1 || (ENDEREZO >>> 28) >= 14 || (ENDEREZO >>> 24) == 127 || ENDEREZO == 내주소) return -101;
        int Seguinte_elemento = (ENDEREZO & Rede_máscara) == (내주소 & Rede_máscara) ? ENDEREZO : pasarela_VALOR;
        if (Seguinte_elemento == 찾은주소) return 0;
        찾을주소 = Seguinte_elemento;
        int Executar_2 = dispositivo_VALOR.밀리초(), Seguinte_solicitude = Executar_2;
        while (dispositivo_VALOR.밀리초() - Executar_2 < 1000) {
            if (dispositivo_VALOR.밀리초() - Seguinte_solicitude >= 0) { solicitude_ENDEREZO(Seguinte_elemento); Seguinte_solicitude += 300; }
            verificar();
            if (찾은주소 == Seguinte_elemento) return 0;
            dispositivo_VALOR.잠시양보();
        }
        return -110;
    }
    static int enviar(int agarradoira_VALOR, int ENDEREZO, int número_do_porto, int[] datos, int duración_VALOR) {
        int 칸 = ÍNDICE(agarradoira_VALOR);
        if (칸 < 0) return -9;
        if (Rede_controlador.입출력기준주소 == 0) return -19;
        if (número_do_porto < 1 || número_do_porto > 65535 || duración_VALOR < 0 || duración_VALOR > 1024) return -22;
        int RESULTANTE = Busca_ENDEREZO(ENDEREZO);
        if (RESULTANTE < 0) return RESULTANTE;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + duración_VALOR);
        넣기16(출력틀, 18, 식별자++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, ENDEREZO);
        넣기16(출력틀, 24, ~SUMA_VALOR(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[칸]); 넣기16(출력틀, 36, número_do_porto);
        넣기16(출력틀, 38, duración_VALOR + 8); 넣기16(출력틀, 40, 0);
        for (int ÍNDICE = 0; ÍNDICE < duración_VALOR; ÍNDICE++) 출력틀[42 + ÍNDICE] = datos[ÍNDICE] & 255;
        int suma_de_comprobación = (~SUMA_VALOR(출력틀, 34, duración_VALOR + 8, 가상머리합(내주소, ENDEREZO, duración_VALOR + 8))) & 65535;
        넣기16(출력틀, 40, suma_de_comprobación == 0 ? 65535 : suma_de_comprobación);
        RESULTANTE = Rede_controlador.enviar(출력틀, duración_VALOR + 42);
        return RESULTANTE < 0 ? RESULTANTE : duración_VALOR;
    }
    static int 받기(int agarradoira_VALOR, int[] datos, int capacidade_VALOR, int 제한) {
        int 칸 = ÍNDICE(agarradoira_VALOR);
        if (칸 < 0) return -9;
        int Executar_2 = dispositivo_VALOR.밀리초();
        while (true) {
            verificar();
            int duración_VALOR = RECIBIDO_duración[칸];
            if (duración_VALOR >= 0) {
                RECIBIDO_duración[칸] = -1;
                if (duración_VALOR > capacidade_VALOR) return -90;
                for (int ÍNDICE = 0; ÍNDICE < duración_VALOR; ÍNDICE++) datos[ÍNDICE] = RECIBIDO_datos[칸 * 1024 + ÍNDICE];
                return duración_VALOR;
            }
            if (제한 == 0) return -11;
            if (dispositivo_VALOR.밀리초() - Executar_2 >= 제한) return -110;
            dispositivo_VALOR.잠시양보();
        }
    }
    static void Estado_VALOR() {
        SMS_Terminal.Escritura(Rede_controlador.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.Escritura("TX: "); SMS_Terminal.수쓰기(Rede_controlador.송신수);
        SMS_Terminal.Escritura(" RX: "); SMS_Terminal.수쓰기(Rede_controlador.수신수);
        SMS_Terminal.Escritura(" DROP: "); SMS_Terminal.수쓰기(폐기수);
        SMS_Terminal.Escritura("\n");
    }
}
