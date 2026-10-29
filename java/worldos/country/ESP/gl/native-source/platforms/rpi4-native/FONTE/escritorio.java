// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 executar_comando 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * 자체 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class escritorio {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 cargo_ÍNDICE 16진수. 프로젝트가 직접 정의한 5x7 tipo_de_letra_VALOR.
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
    static int díxito_VALOR(int carácter_VALOR) { return carácter_VALOR <= '9' ? carácter_VALOR - '0' : carácter_VALOR - 'A' + 10; }
    static void Texto(int 가로, int Vertical_cargo, String Contido_VALOR, int 색) {
        for (int carácter_VALOR = 0; carácter_VALOR < Contido_VALOR.length(); carácter_VALOR++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == Contido_VALOR.charAt(carácter_VALOR)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int FILA_VALOR = 0; FILA_VALOR < 7; FILA_VALOR++) {
                int Posición = 찾음 * 14 + FILA_VALOR * 2;
                int bit_VALOR = díxito_VALOR(모양들.charAt(Posición)) * 16 + díxito_VALOR(모양들.charAt(Posición + 1));
                for (int COLUMNA_VALOR = 0; COLUMNA_VALOR < 5; COLUMNA_VALOR++) if ((bit_VALOR & (16 >> COLUMNA_VALOR)) != 0)
                    kernel.사각형(가로 + carácter_VALOR * 12 + COLUMNA_VALOR * 2, Vertical_cargo + FILA_VALOR * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int selección_VALOR, String Estado_VALOR) {
        kernel.사각형(0, 0, Panel.화면너비(), Panel.화면높이(), 0x302018);
        kernel.사각형(32, 24, 576, 432, 0xefe8e2);
        kernel.사각형(32, 24, 576, 48, 0x905020);
        Texto(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int ÍNDICE = 0; ÍNDICE < 5; ÍNDICE++) {
            kernel.사각형(64, 112 + ÍNDICE * 52, 512, 40, ÍNDICE == selección_VALOR ? 0xd0a040 : 0xd8d0c8);
            Texto(84, 128 + ÍNDICE * 52, ÍNDICE == 0 ? "RUN C++ FILE PROGRAM" : ÍNDICE == 1 ? "RUN UDP LOOPBACK" : ÍNDICE == 2 ? "COMPILE AND RUN JAVA" : ÍNDICE == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        Texto(68, 384, Estado_VALOR, 0x205020);
        Texto(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void executar_comando() {
        if (Panel.화면준비() == 0) { 단말.Escritura("GUI unavailable\n"); return; }
        int selección_VALOR = 0;
        String Estado_VALOR = "READY";
        boolean 앞줄 = 명령해석기.앞줄;
        그리기(selección_VALOR, Estado_VALOR);
        단말.Escritura("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int 입력 = Panel.직렬읽기();
            if (입력 < 0) { Panel.suspender_CPU(); continue; }
            if (입력 == 10 && 앞줄) { 앞줄 = false; continue; }
            앞줄 = 입력 == 13;
            if (입력 >= '1' && 입력 <= '5') { selección_VALOR = 입력 - '1'; 입력 = 13; }
            if (입력 == 't' || 입력 == 'T') { 명령해석기.Terminal(false); return; }
            if (입력 == 'q' || 입력 == 'Q' || 입력 == 27) break;
            if (입력 == 9 || 입력 == 'j') {
                selección_VALOR = (selección_VALOR + 1) % 5; 그리기(selección_VALOR, Estado_VALOR); 단말.Escritura("GUI FOCUS "); 단말.수(selección_VALOR); 단말.문자(10);
            } else if (입력 == 13 || 입력 == 10) {
                if (selección_VALOR == 4) { 명령해석기.Terminal(false); return; }
                int RESULTANTE;
                if (selección_VALOR < 2) RESULTANTE = Panel.executar_usuario_apl(selección_VALOR == 0 ? 0 : 9);
                else if (selección_VALOR == 2) {
                    RESULTANTE = 명령해석기.예제실행(10, "Hello.java");
                    if (RESULTANTE == 0) RESULTANTE = 명령해석기.예제실행(11, "Hello");
                } else RESULTANTE = 명령해석기.예제실행(12, "hello.py");
                Estado_VALOR = RESULTANTE != 0 ? "PROGRAM FAILED" : selección_VALOR == 0 ? "C++ FILE OK" : selección_VALOR == 1 ? "UDP LOOPBACK OK" : selección_VALOR == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(selección_VALOR, Estado_VALOR);
                단말.Escritura("GUI ACTION "); 단말.수(selección_VALOR); 단말.Escritura(" RESULT "); 단말.수(RESULTANTE); 단말.문자(10);
            }
        }
        kernel.화면();
        단말.Escritura("GUI EXIT\n");
    }
}
