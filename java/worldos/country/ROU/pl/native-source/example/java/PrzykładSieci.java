// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import polski.własny.połączenie;
import polski.własny.실행인수;
import polski.własny.datagram_Kanał;
import polski.własny.문자;
import polski.własny.pozycja_wyjścia;
import polski.własny.검사;
import polski.własny.strumień_wejściowy;
import polski.własny.We_Wy_wyjątek;

public class PrzykładSieci {
    public static void Uruchom_2() throws We_Wy_wyjątek {
        // host: python3 narzędzia/예제되돌림.py --tcp-port 9000 --udp-port 9001
        połączenie Połącz = połączenie.Otwórz("10.0.2.2", 문자.analizować_liczba_całkowita(실행인수.tekst(0)));
        try {
            Połącz.TIMEOUT(700);
            byte[] e_mail = 문자.kodować("JAVA TCP pl\n");
            Połącz.pozycja_wyjścia().Zapis(e_mail);
            strumień_wejściowy wejście_WARTOŚĆ = Połącz.wejście_WARTOŚĆ();
            for (int identyfikator = 0; identyfikator < 문자.bajt_ILE_LICZB(e_mail); identyfikator++) {
                검사.참인지(wejście_WARTOŚĆ.Odczyt() == (e_mail[identyfikator] & 255), "TCP odpowiedź 불일치");
            }
        } finally { Połącz.Zamknięte(); }
        datagram_Kanał uczestnik = datagram_Kanał.Otwórz(0);
        try {
            uczestnik.TIMEOUT(700);
            uczestnik.wysłać("10.0.2.2", 문자.analizować_liczba_całkowita(실행인수.tekst(1)), "JAVA UDP pl");
            검사.참인지(문자.같음(uczestnik.odbierać(), "JAVA UDP pl"), "UDP odpowiedź 불일치");
        } finally { uczestnik.Zamknięte(); }
        pozycja_wyjścia.zapis_linia("JAVA 네트워크 확인: TCP UDP pl");
    }
}
