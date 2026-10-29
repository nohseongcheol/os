// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 Esegui_comando schermata. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * nativo 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class PC {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 funzione_INDICE 16진수. 프로젝트가 직접 정의한 5x7 tipo_di_carattere_VALORE.
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
    static int cifra_VALORE(int carattere_VALORE) { return carattere_VALORE <= '9' ? carattere_VALORE - '0' : carattere_VALORE - 'A' + 10; }
    static void testo(int 가로, int Verticale_funzione, String Contenuto_VALORE, int 색) {
        for (int carattere_VALORE = 0; carattere_VALORE < Contenuto_VALORE.length(); carattere_VALORE++) {
            int 찾음 = -1;
            for (int candidato = 0; candidato < 문자들.length(); candidato++) if (문자들.charAt(candidato) == Contenuto_VALORE.charAt(carattere_VALORE)) 찾음 = candidato;
            if (찾음 < 0) continue;
            for (int riga_VALORE = 0; riga_VALORE < 7; riga_VALORE++) {
                int posizione = 찾음 * 14 + riga_VALORE * 2;
                int bit_VALORE = cifra_VALORE(모양들.charAt(posizione)) * 16 + cifra_VALORE(모양들.charAt(posizione + 1));
                for (int colonna_VALORE = 0; colonna_VALORE < 5; colonna_VALORE++) if ((bit_VALORE & (16 >> colonna_VALORE)) != 0)
                    Nucleo.rettangolo(가로 + carattere_VALORE * 12 + colonna_VALORE * 2, Verticale_funzione + riga_VALORE * 2, 2, 2, 색);
            }
        }
    }
    static void Paint_schermata(int selezione_VALORE, String Stato_VALORE) {
        Nucleo.rettangolo(0, 0, scheda.화면너비(), scheda.schermata_altezza(), 0x302018);
        Nucleo.rettangolo(32, 24, 576, 432, 0xefe8e2);
        Nucleo.rettangolo(32, 24, 576, 48, 0x905020);
        testo(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDICE = 0; INDICE < 5; INDICE++) {
            Nucleo.rettangolo(64, 112 + INDICE * 52, 512, 40, INDICE == selezione_VALORE ? 0xd0a040 : 0xd8d0c8);
            testo(84, 128 + INDICE * 52, INDICE == 0 ? "RUN C++ FILE PROGRAM" : INDICE == 1 ? "RUN UDP LOOPBACK" : INDICE == 2 ? "COMPILE AND RUN JAVA" : INDICE == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        testo(68, 384, Stato_VALORE, 0x205020);
        testo(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void Esegui_comando() {
        if (scheda.Prepara_schermata() == 0) { 단말.Scrittura("GUI unavailable\n"); return; }
        int selezione_VALORE = 0;
        String Stato_VALORE = "READY";
        boolean Indietro_riga = InterpreteComandi.Indietro_riga;
        Paint_schermata(selezione_VALORE, Stato_VALORE);
        단말.Scrittura("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int input_VALORE = scheda.직렬읽기();
            if (input_VALORE < 0) { scheda.REND_CPU(); continue; }
            if (input_VALORE == 10 && Indietro_riga) { Indietro_riga = false; continue; }
            Indietro_riga = input_VALORE == 13;
            if (input_VALORE >= '1' && input_VALORE <= '5') { selezione_VALORE = input_VALORE - '1'; input_VALORE = 13; }
            if (input_VALORE == 't' || input_VALORE == 'T') { InterpreteComandi.terminale(false); return; }
            if (input_VALORE == 'q' || input_VALORE == 'Q' || input_VALORE == 27) break;
            if (input_VALORE == 9 || input_VALORE == 'j') {
                selezione_VALORE = (selezione_VALORE + 1) % 5; Paint_schermata(selezione_VALORE, Stato_VALORE); 단말.Scrittura("GUI FOCUS "); 단말.numero(selezione_VALORE); 단말.문자(10);
            } else if (input_VALORE == 13 || input_VALORE == 10) {
                if (selezione_VALORE == 4) { InterpreteComandi.terminale(false); return; }
                int risultato;
                if (selezione_VALORE < 2) risultato = scheda.eseguire_USER_app(selezione_VALORE == 0 ? 0 : 9);
                else if (selezione_VALORE == 2) {
                    risultato = InterpreteComandi.예제실행(10, "Hello.java");
                    if (risultato == 0) risultato = InterpreteComandi.예제실행(11, "Hello");
                } else risultato = InterpreteComandi.예제실행(12, "hello.py");
                Stato_VALORE = risultato != 0 ? "PROGRAM FAILED" : selezione_VALORE == 0 ? "C++ FILE OK" : selezione_VALORE == 1 ? "UDP LOOPBACK OK" : selezione_VALORE == 2 ? "JAVA OK" : "MICROPYTHON OK";
                Paint_schermata(selezione_VALORE, Stato_VALORE);
                단말.Scrittura("GUI ACTION "); 단말.numero(selezione_VALORE); 단말.Scrittura(" RESULT "); 단말.numero(risultato); 단말.문자(10);
            }
        }
        Nucleo.schermata();
        단말.Scrittura("GUI EXIT\n");
    }
}
