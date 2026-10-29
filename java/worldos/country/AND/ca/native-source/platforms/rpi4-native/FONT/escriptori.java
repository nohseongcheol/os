// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 Executa_ordre 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * propi 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class escriptori {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 càrrec_INDEX 16진수. 프로젝트가 직접 정의한 5x7 tipus_de_lletra_VALOR.
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
    static int dígit_VALOR(int caràcter_VALOR) { return caràcter_VALOR <= '9' ? caràcter_VALOR - '0' : caràcter_VALOR - 'A' + 10; }
    static void SMS(int 가로, int Vertical_càrrec, String contingut_VALOR, int 색) {
        for (int caràcter_VALOR = 0; caràcter_VALOR < contingut_VALOR.length(); caràcter_VALOR++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == contingut_VALOR.charAt(caràcter_VALOR)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int FILA_VALOR = 0; FILA_VALOR < 7; FILA_VALOR++) {
                int Posició = 찾음 * 14 + FILA_VALOR * 2;
                int bit_VALOR = dígit_VALOR(모양들.charAt(Posició)) * 16 + dígit_VALOR(모양들.charAt(Posició + 1));
                for (int COLUMNA_VALOR = 0; COLUMNA_VALOR < 5; COLUMNA_VALOR++) if ((bit_VALOR & (16 >> COLUMNA_VALOR)) != 0)
                    nucli.사각형(가로 + caràcter_VALOR * 12 + COLUMNA_VALOR * 2, Vertical_càrrec + FILA_VALOR * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int selecció_VALOR, String Estat_VALOR) {
        nucli.사각형(0, 0, Tauler.화면너비(), Tauler.화면높이(), 0x302018);
        nucli.사각형(32, 24, 576, 432, 0xefe8e2);
        nucli.사각형(32, 24, 576, 48, 0x905020);
        SMS(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDEX = 0; INDEX < 5; INDEX++) {
            nucli.사각형(64, 112 + INDEX * 52, 512, 40, INDEX == selecció_VALOR ? 0xd0a040 : 0xd8d0c8);
            SMS(84, 128 + INDEX * 52, INDEX == 0 ? "RUN C++ FILE PROGRAM" : INDEX == 1 ? "RUN UDP LOOPBACK" : INDEX == 2 ? "COMPILE AND RUN JAVA" : INDEX == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        SMS(68, 384, Estat_VALOR, 0x205020);
        SMS(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void Executa_ordre() {
        if (Tauler.화면준비() == 0) { 단말.Escriptura("GUI unavailable\n"); return; }
        int selecció_VALOR = 0;
        String Estat_VALOR = "READY";
        boolean 앞줄 = 명령해석기.앞줄;
        그리기(selecció_VALOR, Estat_VALOR);
        단말.Escriptura("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int 입력 = Tauler.직렬읽기();
            if (입력 < 0) { Tauler.RENDTO_CPU(); continue; }
            if (입력 == 10 && 앞줄) { 앞줄 = false; continue; }
            앞줄 = 입력 == 13;
            if (입력 >= '1' && 입력 <= '5') { selecció_VALOR = 입력 - '1'; 입력 = 13; }
            if (입력 == 't' || 입력 == 'T') { 명령해석기.Terminal(false); return; }
            if (입력 == 'q' || 입력 == 'Q' || 입력 == 27) break;
            if (입력 == 9 || 입력 == 'j') {
                selecció_VALOR = (selecció_VALOR + 1) % 5; 그리기(selecció_VALOR, Estat_VALOR); 단말.Escriptura("GUI FOCUS "); 단말.수(selecció_VALOR); 단말.문자(10);
            } else if (입력 == 13 || 입력 == 10) {
                if (selecció_VALOR == 4) { 명령해석기.Terminal(false); return; }
                int RESULTAT;
                if (selecció_VALOR < 2) RESULTAT = Tauler.execució_usuari_programa(selecció_VALOR == 0 ? 0 : 9);
                else if (selecció_VALOR == 2) {
                    RESULTAT = 명령해석기.예제실행(10, "Hello.java");
                    if (RESULTAT == 0) RESULTAT = 명령해석기.예제실행(11, "Hello");
                } else RESULTAT = 명령해석기.예제실행(12, "hello.py");
                Estat_VALOR = RESULTAT != 0 ? "PROGRAM FAILED" : selecció_VALOR == 0 ? "C++ FILE OK" : selecció_VALOR == 1 ? "UDP LOOPBACK OK" : selecció_VALOR == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(selecció_VALOR, Estat_VALOR);
                단말.Escriptura("GUI ACTION "); 단말.수(selecció_VALOR); 단말.Escriptura(" RESULT "); 단말.수(RESULTAT); 단말.문자(10);
            }
        }
        nucli.화면();
        단말.Escriptura("GUI EXIT\n");
    }
}
