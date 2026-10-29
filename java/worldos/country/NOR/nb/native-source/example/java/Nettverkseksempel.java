// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import norsk.eget.kontakt;
import norsk.eget.실행인수;
import norsk.eget.datagram_Kanal;
import norsk.eget.문자;
import norsk.eget.Utgang;
import norsk.eget.검사;
import norsk.eget.inndataflyt;
import norsk.eget.I_U_unntak;

public class Nettverkseksempel {
    public static void Kjør_2() throws I_U_unntak {
        // vert: python3 Verktøy/예제되돌림.py --tcp-port 9000 --udp-port 9001
        kontakt Koble_til = kontakt.Åpne("10.0.2.2", 문자.dele_opp_heltall(실행인수.Tekst(0)));
        try {
            Koble_til.TIMEOUT(700);
            byte[] e_post_8c783e64 = 문자.부호화("JAVA TCP nb\n");
            Koble_til.Utgang().Skriv(e_post_8c783e64);
            inndataflyt inndata_VERDI = Koble_til.inndata_VERDI();
            for (int nummer = 0; nummer < 문자.byte_ANTALL(e_post_8c783e64); nummer++) {
                검사.참인지(inndata_VERDI.Les() == (e_post_8c783e64[nummer] & 255), "TCP svar 불일치");
            }
        } finally { Koble_til.Lukk(); }
        datagram_Kanal deltaker = datagram_Kanal.Åpne(0);
        try {
            deltaker.TIMEOUT(700);
            deltaker.sende("10.0.2.2", 문자.dele_opp_heltall(실행인수.Tekst(1)), "JAVA UDP nb");
            검사.참인지(문자.같음(deltaker.motta(), "JAVA UDP nb"), "UDP svar 불일치");
        } finally { deltaker.Lukk(); }
        Utgang.skrive_linje("JAVA 네트워크 bekrefte: TCP UDP nb");
    }
}
