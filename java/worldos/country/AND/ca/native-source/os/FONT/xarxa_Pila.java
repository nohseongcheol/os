// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** estàtic_VALOR IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class xarxa_Pila {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int xarxa_màscara = 0xffffff00; /* ip.conf:NETMASK */
    static final int passarel_la_VALOR = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], CANTIDAD_RECIBIDA_durada = new int[4], CANTIDAD_RECIBIDA_ADREÇA = new int[4], CANTIDAD_RECIBIDA_número_de_port = new int[4];
    static int[] CANTIDAD_RECIBIDA_dades = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identificador_VALOR = 0, 폐기수 = 0;

    static int 수16(int[] marc_INDEX, int Posició) { return (marc_INDEX[Posició] << 8) | marc_INDEX[Posició + 1]; }
    static int 수32(int[] marc_INDEX, int Posició) { return (수16(marc_INDEX, Posició) << 16) | 수16(marc_INDEX, Posició + 2); }
    static void 넣기16(int[] marc_INDEX, int Posició, int VALOR) { marc_INDEX[Posició] = (VALOR >>> 8) & 255; marc_INDEX[Posició + 1] = VALOR & 255; }
    static void 넣기32(int[] marc_INDEX, int Posició, int VALOR) { 넣기16(marc_INDEX, Posició, VALOR >>> 16); 넣기16(marc_INDEX, Posició + 2, VALOR); }
    static int SUMA_VALOR(int[] marc_INDEX, int Executa_2, int durada_VALOR, int VALOR) {
        for (int INDEX = 0; INDEX < durada_VALOR; INDEX += 2)
            VALOR += (marc_INDEX[Executa_2 + INDEX] << 8) | (INDEX + 1 < durada_VALOR ? marc_INDEX[Executa_2 + INDEX + 1] : 0);
        while ((VALOR >>> 16) != 0) VALOR = (VALOR & 65535) + (VALOR >>> 16);
        return VALOR;
    }
    static int 가상머리합(int 출발, int 도착, int durada_VALOR) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + durada_VALOR;
    }

    static void NETEJA_Procés() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; CANTIDAD_RECIBIDA_durada[INDEX] = -1; CANTIDAD_RECIBIDA_ADREÇA[INDEX] = 0; CANTIDAD_RECIBIDA_número_de_port[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (xarxa_controlador.rebre(입력틀) == 0) break;
    }
    static int INDEX(int control_VALOR_f011887b) { return control_VALOR_f011887b >= 3 && control_VALOR_f011887b < 7 && 접속번호들[control_VALOR_f011887b - 3] != 0 ? control_VALOR_f011887b - 3 : -1; }
    static int Obre(int número_de_port) {
        if (xarxa_controlador.입출력기준주소 == 0) return -19;
        if (número_de_port < 0 || número_de_port > 65535) return -22;
        if (número_de_port != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == número_de_port) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (número_de_port == 0) {
                número_de_port = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int frontal_VALOR = 0; frontal_VALOR < 4; frontal_VALOR++) if (접속번호들[frontal_VALOR] == número_de_port) 겹침 = true;
                    if (겹침) número_de_port++;
                }
            }
            접속번호들[INDEX] = número_de_port; CANTIDAD_RECIBIDA_durada[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Tanca(int control_VALOR_f011887b) {
        int 칸 = INDEX(control_VALOR_f011887b);
        if (칸 < 0) return -9;
        접속번호들[칸] = 0; CANTIDAD_RECIBIDA_durada[칸] = -1;
        return 0;
    }
    static int homòleg_ADREÇA(int control_VALOR_f011887b) { int 칸 = INDEX(control_VALOR_f011887b); return 칸 < 0 ? -9 : CANTIDAD_RECIBIDA_ADREÇA[칸]; }
    static int homòleg_número_de_port(int control_VALOR_f011887b) { int 칸 = INDEX(control_VALOR_f011887b); return 칸 < 0 ? -9 : CANTIDAD_RECIBIDA_número_de_port[칸]; }

    static void 바깥머리(int 종류, boolean de_difusió_VALOR) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = de_difusió_VALOR ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = xarxa_controlador.dispositiu_ADREÇA[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void sol_licitud_ADREÇA(int destinació_VALOR) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = xarxa_controlador.dispositiu_ADREÇA[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, destinació_VALOR);
        xarxa_controlador.enviar(출력틀, 42);
    }
    static void Procés_ADREÇA(int durada_VALOR) {
        if (durada_VALOR < 42 || 수16(입력틀, 14) != 1 || 수16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || 수32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = 수16(입력틀, 20), homòleg_VALOR = 수32(입력틀, 28);
        if (종류 == 2 && homòleg_VALOR == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != xarxa_controlador.dispositiu_ADREÇA[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = homòleg_VALOR;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = xarxa_controlador.dispositiu_ADREÇA[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, homòleg_VALOR);
            xarxa_controlador.enviar(출력틀, 42);
        }
    }

    static void Procés_marc(int durada_VALOR) {
        if (durada_VALOR < 14 || durada_VALOR > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, de_difusió_VALOR = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != xarxa_controlador.dispositiu_ADREÇA[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) de_difusió_VALOR = false;
        }
        if (!자기 && !de_difusió_VALOR) return;
        if (수16(입력틀, 12) == 0x0806) { Procés_ADREÇA(durada_VALOR); return; }
        if (수16(입력틀, 12) != 0x0800) return;
        if (durada_VALOR < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Capçalera_durada = (입력틀[14] & 15) * 4, total_durada = 수16(입력틀, 16);
        if (Capçalera_durada < 20 || Capçalera_durada > 60 || total_durada < Capçalera_durada + 8 || total_durada > durada_VALOR - 14
            || (수16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || 수32(입력틀, 30) != 내주소 || SUMA_VALOR(입력틀, 14, Capçalera_durada, 0) != 65535) { 폐기수++; return; }
        int Executa_2 = 14 + Capçalera_durada, dades_durada = 수16(입력틀, Executa_2 + 4);
        if (dades_durada < 8 || dades_durada != total_durada - Capçalera_durada || dades_durada > 1032) { 폐기수++; return; }
        int 출발 = 수32(입력틀, 26);
        if (수16(입력틀, Executa_2 + 6) != 0 && SUMA_VALOR(입력틀, Executa_2, dades_durada, 가상머리합(출발, 내주소, dades_durada)) != 65535) {
            폐기수++; return;
        }
        int destinació_VALOR = 수16(입력틀, Executa_2 + 2);
        for (int 칸 = 0; 칸 < 4; 칸++) if (접속번호들[칸] != 0 && 접속번호들[칸] == destinació_VALOR) {
            if (CANTIDAD_RECIBIDA_durada[칸] >= 0) { 폐기수++; return; }
            CANTIDAD_RECIBIDA_durada[칸] = dades_durada - 8; CANTIDAD_RECIBIDA_ADREÇA[칸] = 출발; CANTIDAD_RECIBIDA_número_de_port[칸] = 수16(입력틀, Executa_2);
            for (int INDEX = 0; INDEX < dades_durada - 8; INDEX++) CANTIDAD_RECIBIDA_dades[칸 * 1024 + INDEX] = 입력틀[Executa_2 + 8 + INDEX];
            return;
        }
    }

    static void verificar() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int durada_VALOR = xarxa_controlador.rebre(입력틀);
            if (durada_VALOR == 0) return;
            Procés_marc(durada_VALOR);
        }
    }
    static int BUSCA_ADREÇA(int Adreça) {
        if (Adreça == 0 || Adreça == -1 || (Adreça >>> 28) >= 14 || (Adreça >>> 24) == 127 || Adreça == 내주소) return -101;
        int Següent_element = (Adreça & xarxa_màscara) == (내주소 & xarxa_màscara) ? Adreça : passarel_la_VALOR;
        if (Següent_element == 찾은주소) return 0;
        찾을주소 = Següent_element;
        int Executa_2 = dispositiu_VALOR.밀리초(), Següent_sol_licitud = Executa_2;
        while (dispositiu_VALOR.밀리초() - Executa_2 < 1000) {
            if (dispositiu_VALOR.밀리초() - Següent_sol_licitud >= 0) { sol_licitud_ADREÇA(Següent_element); Següent_sol_licitud += 300; }
            verificar();
            if (찾은주소 == Següent_element) return 0;
            dispositiu_VALOR.잠시양보();
        }
        return -110;
    }
    static int enviar(int control_VALOR_f011887b, int Adreça, int número_de_port, int[] dades, int durada_VALOR) {
        int 칸 = INDEX(control_VALOR_f011887b);
        if (칸 < 0) return -9;
        if (xarxa_controlador.입출력기준주소 == 0) return -19;
        if (número_de_port < 1 || número_de_port > 65535 || durada_VALOR < 0 || durada_VALOR > 1024) return -22;
        int RESULTAT = BUSCA_ADREÇA(Adreça);
        if (RESULTAT < 0) return RESULTAT;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + durada_VALOR);
        넣기16(출력틀, 18, identificador_VALOR++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, Adreça);
        넣기16(출력틀, 24, ~SUMA_VALOR(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[칸]); 넣기16(출력틀, 36, número_de_port);
        넣기16(출력틀, 38, durada_VALOR + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < durada_VALOR; INDEX++) 출력틀[42 + INDEX] = dades[INDEX] & 255;
        int suma_de_comprovació = (~SUMA_VALOR(출력틀, 34, durada_VALOR + 8, 가상머리합(내주소, Adreça, durada_VALOR + 8))) & 65535;
        넣기16(출력틀, 40, suma_de_comprovació == 0 ? 65535 : suma_de_comprovació);
        RESULTAT = xarxa_controlador.enviar(출력틀, durada_VALOR + 42);
        return RESULTAT < 0 ? RESULTAT : durada_VALOR;
    }
    static int rebre(int control_VALOR_f011887b, int[] dades, int capacitat_VALOR, int 제한) {
        int 칸 = INDEX(control_VALOR_f011887b);
        if (칸 < 0) return -9;
        int Executa_2 = dispositiu_VALOR.밀리초();
        while (true) {
            verificar();
            int durada_VALOR = CANTIDAD_RECIBIDA_durada[칸];
            if (durada_VALOR >= 0) {
                CANTIDAD_RECIBIDA_durada[칸] = -1;
                if (durada_VALOR > capacitat_VALOR) return -90;
                for (int INDEX = 0; INDEX < durada_VALOR; INDEX++) dades[INDEX] = CANTIDAD_RECIBIDA_dades[칸 * 1024 + INDEX];
                return durada_VALOR;
            }
            if (제한 == 0) return -11;
            if (dispositiu_VALOR.밀리초() - Executa_2 >= 제한) return -110;
            dispositiu_VALOR.잠시양보();
        }
    }
    static void Estat_VALOR() {
        SMS_Terminal.Escriptura(xarxa_controlador.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.Escriptura("TX: "); SMS_Terminal.수쓰기(xarxa_controlador.송신수);
        SMS_Terminal.Escriptura(" RX: "); SMS_Terminal.수쓰기(xarxa_controlador.rebre_COMPT);
        SMS_Terminal.Escriptura(" DROP: "); SMS_Terminal.수쓰기(폐기수);
        SMS_Terminal.Escriptura("\n");
    }
}
