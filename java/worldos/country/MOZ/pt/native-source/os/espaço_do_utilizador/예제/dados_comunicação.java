// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class dados_comunicação {
    static int dígito_VALOR(String texto) {
        if (texto == null || texto.length() == 0) return -1;
        int resultado = 0;
        for (int ÍNDICE = 0; ÍNDICE < texto.length(); ÍNDICE++) {
            int VALOR = texto.charAt(ÍNDICE) - '0';
            if (VALOR < 0 || VALOR > 9 || resultado > 6553) return -1;
            resultado = resultado * 10 + VALOR;
            if (resultado > 65535) return -1;
        }
        return resultado;
    }
    static int Endereço(String texto) {
        if (texto == null) return 0;
        int VALOR = 0, resultado = 0, 부분 = 0, 자릿수 = 0;
        for (int ÍNDICE = 0; ÍNDICE <= texto.length(); ÍNDICE++) {
            int 문자 = ÍNDICE == texto.length() ? '.' : texto.charAt(ÍNDICE);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                resultado = (resultado << 8) | VALOR; 부분++; VALOR = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALOR = VALOR * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALOR > 255) return 0;
            }
        }
        return 부분 == 4 ? resultado : 0;
    }
    public static int iniciar() {
        if (espaço_do_utilizador.인수개수() != 3) { espaço_do_utilizador.Escrita("Usage: run udp IP PORT TEXT\n"); return 2; }
        int Endereço = Endereço(espaço_do_utilizador.argumentos(0)), porta_VALOR = dígito_VALOR(espaço_do_utilizador.argumentos(1));
        String Conteúdo_VALOR = espaço_do_utilizador.argumentos(2);
        if (Endereço == 0 || porta_VALOR < 1 || Conteúdo_VALOR.length() > 1024) { espaço_do_utilizador.Escrita("Bad destination\n"); return 2; }
        int alça_VALOR = espaço_do_utilizador.abrir_rede(0);
        if (alça_VALOR < 0) { espaço_do_utilizador.Escrita("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] dados = new int[1024];
        for (int ÍNDICE = 0; ÍNDICE < Conteúdo_VALOR.length(); ÍNDICE++) dados[ÍNDICE] = Conteúdo_VALOR.charAt(ÍNDICE);
        if (espaço_do_utilizador.enviar_dados(alça_VALOR, Endereço, porta_VALOR, dados, Conteúdo_VALOR.length()) < 0) {
            espaço_do_utilizador.Escrita("UDP SEND FAILED\n"); espaço_do_utilizador.Close_rede(alça_VALOR); return 4;
        }
        espaço_do_utilizador.Escrita("UDP SENT\n");
        int RECEBER_duração = espaço_do_utilizador.receber_dados(alça_VALOR, dados, 1500);
        boolean 같음 = RECEBER_duração == Conteúdo_VALOR.length() && espaço_do_utilizador.보낸주소(alça_VALOR) == Endereço && espaço_do_utilizador.보낸창구(alça_VALOR) == porta_VALOR;
        if (같음) for (int ÍNDICE = 0; ÍNDICE < RECEBER_duração; ÍNDICE++) if (dados[ÍNDICE] != Conteúdo_VALOR.charAt(ÍNDICE)) 같음 = false;
        espaço_do_utilizador.Close_rede(alça_VALOR);
        if (RECEBER_duração < 0) { espaço_do_utilizador.Escrita("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        espaço_do_utilizador.Escrita(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
