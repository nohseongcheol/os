// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 Uitvoeren_opdracht scherm. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * Eigen 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class pc {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 plaatsingsindex 16진수. 프로젝트가 직접 정의한 5x7 lettertype_WAARDE.
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
    static int cijfer_WAARDE(int teken_WAARDE) { return teken_WAARDE <= '9' ? teken_WAARDE - '0' : teken_WAARDE - 'A' + 10; }
    static void tekst(int 가로, int Verticaal_functie, String Inhoud_WAARDE, int 색) {
        for (int teken_WAARDE = 0; teken_WAARDE < Inhoud_WAARDE.length(); teken_WAARDE++) {
            int 찾음 = -1;
            for (int sollicitant = 0; sollicitant < 문자들.length(); sollicitant++) if (문자들.charAt(sollicitant) == Inhoud_WAARDE.charAt(teken_WAARDE)) 찾음 = sollicitant;
            if (찾음 < 0) continue;
            for (int RIJ_WAARDE = 0; RIJ_WAARDE < 7; RIJ_WAARDE++) {
                int positie = 찾음 * 14 + RIJ_WAARDE * 2;
                int bit_WAARDE = cijfer_WAARDE(모양들.charAt(positie)) * 16 + cijfer_WAARDE(모양들.charAt(positie + 1));
                for (int KOLOM_WAARDE = 0; KOLOM_WAARDE < 5; KOLOM_WAARDE++) if ((bit_WAARDE & (16 >> KOLOM_WAARDE)) != 0)
                    Kern.rechthoek(가로 + teken_WAARDE * 12 + KOLOM_WAARDE * 2, Verticaal_functie + RIJ_WAARDE * 2, 2, 2, 색);
            }
        }
    }
    static void Paint_scherm(int selectie_WAARDE, String Status_WAARDE) {
        Kern.rechthoek(0, 0, Bord.화면너비(), Bord.scherm_hoogte(), 0x302018);
        Kern.rechthoek(32, 24, 576, 432, 0xefe8e2);
        Kern.rechthoek(32, 24, 576, 48, 0x905020);
        tekst(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDEX = 0; INDEX < 5; INDEX++) {
            Kern.rechthoek(64, 112 + INDEX * 52, 512, 40, INDEX == selectie_WAARDE ? 0xd0a040 : 0xd8d0c8);
            tekst(84, 128 + INDEX * 52, INDEX == 0 ? "RUN C++ FILE PROGRAM" : INDEX == 1 ? "RUN UDP LOOPBACK" : INDEX == 2 ? "COMPILE AND RUN JAVA" : INDEX == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        tekst(68, 384, Status_WAARDE, 0x205020);
        tekst(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void Uitvoeren_opdracht() {
        if (Bord.Bereid_voor_scherm() == 0) { 단말.Schrijven("GUI unavailable\n"); return; }
        int selectie_WAARDE = 0;
        String Status_WAARDE = "READY";
        boolean Vorige_lijn = Opdrachtvertolker.Vorige_lijn;
        Paint_scherm(selectie_WAARDE, Status_WAARDE);
        단말.Schrijven("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int invoer_WAARDE = Bord.직렬읽기();
            if (invoer_WAARDE < 0) { Bord.RENDEMENT_CPU(); continue; }
            if (invoer_WAARDE == 10 && Vorige_lijn) { Vorige_lijn = false; continue; }
            Vorige_lijn = invoer_WAARDE == 13;
            if (invoer_WAARDE >= '1' && invoer_WAARDE <= '5') { selectie_WAARDE = invoer_WAARDE - '1'; invoer_WAARDE = 13; }
            if (invoer_WAARDE == 't' || invoer_WAARDE == 'T') { Opdrachtvertolker.terminal(false); return; }
            if (invoer_WAARDE == 'q' || invoer_WAARDE == 'Q' || invoer_WAARDE == 27) break;
            if (invoer_WAARDE == 9 || invoer_WAARDE == 'j') {
                selectie_WAARDE = (selectie_WAARDE + 1) % 5; Paint_scherm(selectie_WAARDE, Status_WAARDE); 단말.Schrijven("GUI FOCUS "); 단말.nummer(selectie_WAARDE); 단말.문자(10);
            } else if (invoer_WAARDE == 13 || invoer_WAARDE == 10) {
                if (selectie_WAARDE == 4) { Opdrachtvertolker.terminal(false); return; }
                int resultaat;
                if (selectie_WAARDE < 2) resultaat = Bord.uitvoeren_gebruiker_app(selectie_WAARDE == 0 ? 0 : 9);
                else if (selectie_WAARDE == 2) {
                    resultaat = Opdrachtvertolker.예제실행(10, "Hello.java");
                    if (resultaat == 0) resultaat = Opdrachtvertolker.예제실행(11, "Hello");
                } else resultaat = Opdrachtvertolker.예제실행(12, "hello.py");
                Status_WAARDE = resultaat != 0 ? "PROGRAM FAILED" : selectie_WAARDE == 0 ? "C++ FILE OK" : selectie_WAARDE == 1 ? "UDP LOOPBACK OK" : selectie_WAARDE == 2 ? "JAVA OK" : "MICROPYTHON OK";
                Paint_scherm(selectie_WAARDE, Status_WAARDE);
                단말.Schrijven("GUI ACTION "); 단말.nummer(selectie_WAARDE); 단말.Schrijven(" RESULT "); 단말.nummer(resultaat); 단말.문자(10);
            }
        }
        Kern.scherm();
        단말.Schrijven("GUI EXIT\n");
    }
}
