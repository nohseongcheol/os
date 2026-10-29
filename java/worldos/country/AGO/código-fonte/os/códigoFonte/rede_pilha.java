// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** estático_VALOR IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class rede_pilha {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int máscara_de_rede = 0xffffff00; /* ip.conf:NETMASK */
    static final int gateway_VALOR = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] entrada_quadro = new int[1536], saída_quadro = new int[1536];
    static int[] 접속번호들 = new int[4], RECEBER_duração = new int[4], RECEBER_email = new int[4], RECEBER_número_da_porta = new int[4];
    static int[] RECEBER_dados = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identificador_VALOR = 0, 폐기수 = 0;

    static int inteiro_16(int[] quadro_ÍNDICE, int posição) { return (quadro_ÍNDICE[posição] << 8) | quadro_ÍNDICE[posição + 1]; }
    static int inteiro_32(int[] quadro_ÍNDICE, int posição) { return (inteiro_16(quadro_ÍNDICE, posição) << 16) | inteiro_16(quadro_ÍNDICE, posição + 2); }
    static void 넣기16(int[] quadro_ÍNDICE, int posição, int VALOR) { quadro_ÍNDICE[posição] = (VALOR >>> 8) & 255; quadro_ÍNDICE[posição + 1] = VALOR & 255; }
    static void 넣기32(int[] quadro_ÍNDICE, int posição, int VALOR) { 넣기16(quadro_ÍNDICE, posição, VALOR >>> 16); 넣기16(quadro_ÍNDICE, posição + 2, VALOR); }
    static int SUM_VALOR(int[] quadro_ÍNDICE, int iniciar, int duração_VALOR, int VALOR) {
        for (int ÍNDICE = 0; ÍNDICE < duração_VALOR; ÍNDICE += 2)
            VALOR += (quadro_ÍNDICE[iniciar + ÍNDICE] << 8) | (ÍNDICE + 1 < duração_VALOR ? quadro_ÍNDICE[iniciar + ÍNDICE + 1] : 0);
        while ((VALOR >>> 16) != 0) VALOR = (VALOR & 65535) + (VALOR >>> 16);
        return VALOR;
    }
    static int 가상머리합(int 출발, int 도착, int duração_VALOR) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + duração_VALOR;
    }

    static void TIRAR_Processo() {
        for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) {
            접속번호들[ÍNDICE] = 0; RECEBER_duração[ÍNDICE] = -1; RECEBER_email[ÍNDICE] = 0; RECEBER_número_da_porta[ÍNDICE] = 0;
        }
        for (int ÍNDICE = 0; ÍNDICE < 64; ÍNDICE++) if (rede_driver.receber(entrada_quadro) == 0) break;
    }
    static int ÍNDICE(int alça_VALOR) { return alça_VALOR >= 3 && alça_VALOR < 7 && 접속번호들[alça_VALOR - 3] != 0 ? alça_VALOR - 3 : -1; }
    static int Abrir(int número_da_porta) {
        if (rede_driver.입출력기준주소 == 0) return -19;
        if (número_da_porta < 0 || número_da_porta > 65535) return -22;
        if (número_da_porta != 0) for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) if (접속번호들[ÍNDICE] == número_da_porta) return -98;
        for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) if (접속번호들[ÍNDICE] == 0) {
            if (número_da_porta == 0) {
                número_da_porta = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int câmera_frontal_VALOR = 0; câmera_frontal_VALOR < 4; câmera_frontal_VALOR++) if (접속번호들[câmera_frontal_VALOR] == número_da_porta) 겹침 = true;
                    if (겹침) número_da_porta++;
                }
            }
            접속번호들[ÍNDICE] = número_da_porta; RECEBER_duração[ÍNDICE] = -1;
            return ÍNDICE + 3;
        }
        return -24;
    }
    static int Fechar(int alça_VALOR) {
        int slot_entrada = ÍNDICE(alça_VALOR);
        if (slot_entrada < 0) return -9;
        접속번호들[slot_entrada] = 0; RECEBER_duração[slot_entrada] = -1;
        return 0;
    }
    static int par_email(int alça_VALOR) { int slot_entrada = ÍNDICE(alça_VALOR); return slot_entrada < 0 ? -9 : RECEBER_email[slot_entrada]; }
    static int par_número_da_porta(int alça_VALOR) { int slot_entrada = ÍNDICE(alça_VALOR); return slot_entrada < 0 ? -9 : RECEBER_número_da_porta[slot_entrada]; }

    static void 바깥머리(int Tipo_VALOR, boolean difusão_VALOR) {
        for (int ÍNDICE = 0; ÍNDICE < 6; ÍNDICE++) {
            saída_quadro[ÍNDICE] = difusão_VALOR ? 255 : 찾은장치[ÍNDICE];
            saída_quadro[6 + ÍNDICE] = rede_driver.celular_email[ÍNDICE];
        }
        넣기16(saída_quadro, 12, Tipo_VALOR);
    }
    static void solicitação_email(int destino_VALOR) {
        바깥머리(0x0806, true);
        넣기16(saída_quadro, 14, 1); 넣기16(saída_quadro, 16, 0x0800);
        saída_quadro[18] = 6; saída_quadro[19] = 4; 넣기16(saída_quadro, 20, 1);
        for (int ÍNDICE = 0; ÍNDICE < 6; ÍNDICE++) {
            saída_quadro[22 + ÍNDICE] = rede_driver.celular_email[ÍNDICE]; saída_quadro[32 + ÍNDICE] = 0;
        }
        넣기32(saída_quadro, 28, 내주소); 넣기32(saída_quadro, 38, destino_VALOR);
        rede_driver.enviar(saída_quadro, 42);
    }
    static void Processo_email(int duração_VALOR) {
        if (duração_VALOR < 42 || inteiro_16(entrada_quadro, 14) != 1 || inteiro_16(entrada_quadro, 16) != 0x0800
            || entrada_quadro[18] != 6 || entrada_quadro[19] != 4 || inteiro_32(entrada_quadro, 38) != 내주소) { 폐기수++; return; }
        int Tipo_VALOR = inteiro_16(entrada_quadro, 20), par_VALOR = inteiro_32(entrada_quadro, 28);
        if (Tipo_VALOR == 2 && par_VALOR == 찾을주소) {
            for (int ÍNDICE = 0; ÍNDICE < 6; ÍNDICE++) {
                if (entrada_quadro[6 + ÍNDICE] != entrada_quadro[22 + ÍNDICE] || entrada_quadro[32 + ÍNDICE] != rede_driver.celular_email[ÍNDICE]) return;
            }
            for (int ÍNDICE = 0; ÍNDICE < 6; ÍNDICE++) 찾은장치[ÍNDICE] = entrada_quadro[22 + ÍNDICE];
            찾은주소 = par_VALOR;
        } else if (Tipo_VALOR == 1) {
            바깥머리(0x0806, false);
            넣기16(saída_quadro, 14, 1); 넣기16(saída_quadro, 16, 0x0800);
            saída_quadro[18] = 6; saída_quadro[19] = 4; 넣기16(saída_quadro, 20, 2);
            for (int ÍNDICE = 0; ÍNDICE < 6; ÍNDICE++) {
                saída_quadro[ÍNDICE] = entrada_quadro[22 + ÍNDICE]; saída_quadro[32 + ÍNDICE] = entrada_quadro[22 + ÍNDICE];
                saída_quadro[22 + ÍNDICE] = rede_driver.celular_email[ÍNDICE];
            }
            넣기32(saída_quadro, 28, 내주소); 넣기32(saída_quadro, 38, par_VALOR);
            rede_driver.enviar(saída_quadro, 42);
        }
    }

    static void Processo_quadro(int duração_VALOR) {
        if (duração_VALOR < 14 || duração_VALOR > entrada_quadro.length) { 폐기수++; return; }
        boolean 자기 = true, difusão_VALOR = true;
        for (int ÍNDICE = 0; ÍNDICE < 6; ÍNDICE++) {
            if (entrada_quadro[ÍNDICE] != rede_driver.celular_email[ÍNDICE]) 자기 = false;
            if (entrada_quadro[ÍNDICE] != 255) difusão_VALOR = false;
        }
        if (!자기 && !difusão_VALOR) return;
        if (inteiro_16(entrada_quadro, 12) == 0x0806) { Processo_email(duração_VALOR); return; }
        if (inteiro_16(entrada_quadro, 12) != 0x0800) return;
        if (duração_VALOR < 34 || (entrada_quadro[14] >>> 4) != 4) { 폐기수++; return; }
        int Cabeçalho_duração = (entrada_quadro[14] & 15) * 4, total_duração = inteiro_16(entrada_quadro, 16);
        if (Cabeçalho_duração < 20 || Cabeçalho_duração > 60 || total_duração < Cabeçalho_duração + 8 || total_duração > duração_VALOR - 14
            || (inteiro_16(entrada_quadro, 20) & 0x3fff) != 0 || entrada_quadro[23] != 17
            || inteiro_32(entrada_quadro, 30) != 내주소 || SUM_VALOR(entrada_quadro, 14, Cabeçalho_duração, 0) != 65535) { 폐기수++; return; }
        int iniciar = 14 + Cabeçalho_duração, dados_duração = inteiro_16(entrada_quadro, iniciar + 4);
        if (dados_duração < 8 || dados_duração != total_duração - Cabeçalho_duração || dados_duração > 1032) { 폐기수++; return; }
        int 출발 = inteiro_32(entrada_quadro, 26);
        if (inteiro_16(entrada_quadro, iniciar + 6) != 0 && SUM_VALOR(entrada_quadro, iniciar, dados_duração, 가상머리합(출발, 내주소, dados_duração)) != 65535) {
            폐기수++; return;
        }
        int destino_VALOR = inteiro_16(entrada_quadro, iniciar + 2);
        for (int slot_entrada = 0; slot_entrada < 4; slot_entrada++) if (접속번호들[slot_entrada] != 0 && 접속번호들[slot_entrada] == destino_VALOR) {
            if (RECEBER_duração[slot_entrada] >= 0) { 폐기수++; return; }
            RECEBER_duração[slot_entrada] = dados_duração - 8; RECEBER_email[slot_entrada] = 출발; RECEBER_número_da_porta[slot_entrada] = inteiro_16(entrada_quadro, iniciar);
            for (int ÍNDICE = 0; ÍNDICE < dados_duração - 8; ÍNDICE++) RECEBER_dados[slot_entrada * 1024 + ÍNDICE] = entrada_quadro[iniciar + 8 + ÍNDICE];
            return;
        }
    }

    static void verificar() {
        for (int ÍNDICE = 0; ÍNDICE < 16; ÍNDICE++) {
            int duração_VALOR = rede_driver.receber(entrada_quadro);
            if (duração_VALOR == 0) return;
            Processo_quadro(duração_VALOR);
        }
    }
    static int PROCURAR_email(int Endereço) {
        if (Endereço == 0 || Endereço == -1 || (Endereço >>> 28) >= 14 || (Endereço >>> 24) == 127 || Endereço == 내주소) return -101;
        int Avançar_item = (Endereço & máscara_de_rede) == (내주소 & máscara_de_rede) ? Endereço : gateway_VALOR;
        if (Avançar_item == 찾은주소) return 0;
        찾을주소 = Avançar_item;
        int iniciar = celular_VALOR.밀리초(), Avançar_solicitação = iniciar;
        while (celular_VALOR.밀리초() - iniciar < 1000) {
            if (celular_VALOR.밀리초() - Avançar_solicitação >= 0) { solicitação_email(Avançar_item); Avançar_solicitação += 300; }
            verificar();
            if (찾은주소 == Avançar_item) return 0;
            celular_VALOR.잠시양보();
        }
        return -110;
    }
    static int enviar(int alça_VALOR, int Endereço, int número_da_porta, int[] dados, int duração_VALOR) {
        int slot_entrada = ÍNDICE(alça_VALOR);
        if (slot_entrada < 0) return -9;
        if (rede_driver.입출력기준주소 == 0) return -19;
        if (número_da_porta < 1 || número_da_porta > 65535 || duração_VALOR < 0 || duração_VALOR > 1024) return -22;
        int resultado = PROCURAR_email(Endereço);
        if (resultado < 0) return resultado;
        바깥머리(0x0800, false);
        saída_quadro[14] = 0x45; saída_quadro[15] = 0; 넣기16(saída_quadro, 16, 28 + duração_VALOR);
        넣기16(saída_quadro, 18, identificador_VALOR++); 넣기16(saída_quadro, 20, 0x4000);
        saída_quadro[22] = 64; saída_quadro[23] = 17; 넣기16(saída_quadro, 24, 0);
        넣기32(saída_quadro, 26, 내주소); 넣기32(saída_quadro, 30, Endereço);
        넣기16(saída_quadro, 24, ~SUM_VALOR(saída_quadro, 14, 20, 0));
        넣기16(saída_quadro, 34, 접속번호들[slot_entrada]); 넣기16(saída_quadro, 36, número_da_porta);
        넣기16(saída_quadro, 38, duração_VALOR + 8); 넣기16(saída_quadro, 40, 0);
        for (int ÍNDICE = 0; ÍNDICE < duração_VALOR; ÍNDICE++) saída_quadro[42 + ÍNDICE] = dados[ÍNDICE] & 255;
        int soma_de_verificação = (~SUM_VALOR(saída_quadro, 34, duração_VALOR + 8, 가상머리합(내주소, Endereço, duração_VALOR + 8))) & 65535;
        넣기16(saída_quadro, 40, soma_de_verificação == 0 ? 65535 : soma_de_verificação);
        resultado = rede_driver.enviar(saída_quadro, duração_VALOR + 42);
        return resultado < 0 ? resultado : duração_VALOR;
    }
    static int receber(int alça_VALOR, int[] dados, int capacidade_VALOR, int 제한) {
        int slot_entrada = ÍNDICE(alça_VALOR);
        if (slot_entrada < 0) return -9;
        int iniciar = celular_VALOR.밀리초();
        while (true) {
            verificar();
            int duração_VALOR = RECEBER_duração[slot_entrada];
            if (duração_VALOR >= 0) {
                RECEBER_duração[slot_entrada] = -1;
                if (duração_VALOR > capacidade_VALOR) return -90;
                for (int ÍNDICE = 0; ÍNDICE < duração_VALOR; ÍNDICE++) dados[ÍNDICE] = RECEBER_dados[slot_entrada * 1024 + ÍNDICE];
                return duração_VALOR;
            }
            if (제한 == 0) return -11;
            if (celular_VALOR.밀리초() - iniciar >= 제한) return -110;
            celular_VALOR.잠시양보();
        }
    }
    static void Estado_VALOR() {
        SMS_Terminal.Escrita(rede_driver.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.Escrita("TX: "); SMS_Terminal.gravar_número(rede_driver.송신수);
        SMS_Terminal.Escrita(" RX: "); SMS_Terminal.gravar_número(rede_driver.receber_CONT_NÚM);
        SMS_Terminal.Escrita(" DROP: "); SMS_Terminal.gravar_número(폐기수);
        SMS_Terminal.Escrita("\n");
    }
}
