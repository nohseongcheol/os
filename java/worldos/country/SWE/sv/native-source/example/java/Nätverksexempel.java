// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Svenska.eget.kontakt;
import Svenska.eget.실행인수;
import Svenska.eget.datagram_Kanal;
import Svenska.eget.문자;
import Svenska.eget.utmatningsposition;
import Svenska.eget.검사;
import Svenska.eget.indataström;
import Svenska.eget.indata_utleverans_fel;

public class Nätverksexempel {
    public static void Kör() throws indata_utleverans_fel {
        // värd: python3 verktyg/예제되돌림.py --tcp-port 9000 --udp-port 9001
        kontakt Anslut = kontakt.Öppna("10.0.2.2", 문자.parsa_heltal(실행인수.text(0)));
        try {
            Anslut.TIMEOUT(700);
            byte[] dokument = 문자.koda("JAVA TCP sv\n");
            Anslut.utmatningsposition().Skriv(dokument);
            indataström indata_värde = Anslut.indata_värde();
            for (int nummer = 0; nummer < 문자.byte_ANTAL(dokument); nummer++) {
                검사.참인지(indata_värde.Läs() == (dokument[nummer] & 255), "TCP svara 불일치");
            }
        } finally { Anslut.Stäng(); }
        datagram_Kanal deltagare = datagram_Kanal.Öppna(0);
        try {
            deltagare.TIMEOUT(700);
            deltagare.skicka("10.0.2.2", 문자.parsa_heltal(실행인수.text(1)), "JAVA UDP sv");
            검사.참인지(문자.같음(deltagare.få(), "JAVA UDP sv"), "UDP svara 불일치");
        } finally { deltagare.Stäng(); }
        utmatningsposition.skriva_rad("JAVA 네트워크 verifiera: TCP UDP sv");
    }
}
