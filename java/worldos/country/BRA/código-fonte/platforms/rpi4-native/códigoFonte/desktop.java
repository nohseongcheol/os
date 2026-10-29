// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 Executar_comando tela. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * nativo 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class desktop {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 cargo_ÍNDICE 16진수. 프로젝트가 직접 정의한 5x7 fonte_VALOR.
    static String 모양들 =
        "0E11111F111111" + "1E11111E11111E" + "0F10101010100F" + "1E11111111111E" +
        "1F10101E10101F" + "1F10101E101010" + "0F10101711110F" + "1111111F111111" +
        "0E04040404040E" + "0702020212120C" + "11121418141211" + "1010101010101F" +
        "111B1515111111" + "11191915131311" + "0E11111111110E" + "1E11111E101010" +
        "0E11111115120D" + "1E11111E141211" + "0F10100E01011E" + "1F040404040404" +
        "1111111111110E" + "11111111110A04" + "11111115151B11" + "11110A040A1111" +
        "11110A04040404" + "1F01020408101F" + "0E11131519110E" + "040C040404040E" +
        "0E11010204081F" + "1E01010601011E" + "02060A121F0202" + "1F10101E01011E" +
        "0E10101E11110E" + "1F010204080808" + "0E11110E11110E" + "0E11110F01010E" +
        "0004041F040400" + "0000001F000000" + "00000000000C0C" + "000C0C000C0C00";
    static int dígito_VALOR(int caractere_VALOR) { return caractere_VALOR <= '9' ? caractere_VALOR - '0' : caractere_VALOR - 'A' + 10; }
    static void texto(int 가로, int Vertical_cargo, String Conteúdo_VALOR, int 색) {
        for (int caractere_VALOR = 0; caractere_VALOR < Conteúdo_VALOR.length(); caractere_VALOR++) {
            int 찾음 = -1;
            for (int candidato = 0; candidato < 문자들.length(); candidato++) if (문자들.charAt(candidato) == Conteúdo_VALOR.charAt(caractere_VALOR)) 찾음 = candidato;
            if (찾음 < 0) continue;
            for (int LIN_VALOR = 0; LIN_VALOR < 7; LIN_VALOR++) {
                int posição = 찾음 * 14 + LIN_VALOR * 2;
                int bit_VALOR = dígito_VALOR(모양들.charAt(posição)) * 16 + dígito_VALOR(모양들.charAt(posição + 1));
                for (int COL_VALOR = 0; COL_VALOR < 5; COL_VALOR++) if ((bit_VALOR & (16 >> COL_VALOR)) != 0)
                    Núcleo.retângulo(가로 + caractere_VALOR * 12 + COL_VALOR * 2, Vertical_cargo + LIN_VALOR * 2, 2, 2, 색);
            }
        }
    }
    static void Paint_tela(int seleção_VALOR, String Estado_VALOR) {
        Núcleo.retângulo(0, 0, Quadro.화면너비(), Quadro.tela_altura(), 0x302018);
        Núcleo.retângulo(32, 24, 576, 432, 0xefe8e2);
        Núcleo.retângulo(32, 24, 576, 48, 0x905020);
        texto(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int ÍNDICE = 0; ÍNDICE < 5; ÍNDICE++) {
            Núcleo.retângulo(64, 112 + ÍNDICE * 52, 512, 40, ÍNDICE == seleção_VALOR ? 0xd0a040 : 0xd8d0c8);
            texto(84, 128 + ÍNDICE * 52, ÍNDICE == 0 ? "RUN C++ FILE PROGRAM" : ÍNDICE == 1 ? "RUN UDP LOOPBACK" : ÍNDICE == 2 ? "COMPILE AND RUN JAVA" : ÍNDICE == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        texto(68, 384, Estado_VALOR, 0x205020);
        texto(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void Executar_comando() {
        if (Quadro.Preparar_tela() == 0) { 단말.Escrita("GUI unavailable\n"); return; }
        int seleção_VALOR = 0;
        String Estado_VALOR = "READY";
        boolean Anterior_linha = InterpretadorComandos.Anterior_linha;
        Paint_tela(seleção_VALOR, Estado_VALOR);
        단말.Escrita("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int entrada_VALOR = Quadro.직렬읽기();
            if (entrada_VALOR < 0) { Quadro.LUCRO_CPU(); continue; }
            if (entrada_VALOR == 10 && Anterior_linha) { Anterior_linha = false; continue; }
            Anterior_linha = entrada_VALOR == 13;
            if (entrada_VALOR >= '1' && entrada_VALOR <= '5') { seleção_VALOR = entrada_VALOR - '1'; entrada_VALOR = 13; }
            if (entrada_VALOR == 't' || entrada_VALOR == 'T') { InterpretadorComandos.terminal(false); return; }
            if (entrada_VALOR == 'q' || entrada_VALOR == 'Q' || entrada_VALOR == 27) break;
            if (entrada_VALOR == 9 || entrada_VALOR == 'j') {
                seleção_VALOR = (seleção_VALOR + 1) % 5; Paint_tela(seleção_VALOR, Estado_VALOR); 단말.Escrita("GUI FOCUS "); 단말.número(seleção_VALOR); 단말.문자(10);
            } else if (entrada_VALOR == 13 || entrada_VALOR == 10) {
                if (seleção_VALOR == 4) { InterpretadorComandos.terminal(false); return; }
                int resultado;
                if (seleção_VALOR < 2) resultado = Quadro.executar_usuário_app(seleção_VALOR == 0 ? 0 : 9);
                else if (seleção_VALOR == 2) {
                    resultado = InterpretadorComandos.예제실행(10, "Hello.java");
                    if (resultado == 0) resultado = InterpretadorComandos.예제실행(11, "Hello");
                } else resultado = InterpretadorComandos.예제실행(12, "hello.py");
                Estado_VALOR = resultado != 0 ? "PROGRAM FAILED" : seleção_VALOR == 0 ? "C++ FILE OK" : seleção_VALOR == 1 ? "UDP LOOPBACK OK" : seleção_VALOR == 2 ? "JAVA OK" : "MICROPYTHON OK";
                Paint_tela(seleção_VALOR, Estado_VALOR);
                단말.Escrita("GUI ACTION "); 단말.número(seleção_VALOR); 단말.Escrita(" RESULT "); 단말.número(resultado); 단말.문자(10);
            }
        }
        Núcleo.tela();
        단말.Escrita("GUI EXIT\n");
    }
}
