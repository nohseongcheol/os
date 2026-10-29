// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Nederlands.Eigen.verbinding;
import Nederlands.Eigen.실행인수;
import Nederlands.Eigen.datagram_Kanaal;
import Nederlands.Eigen.문자;
import Nederlands.Eigen.tekstuitvoer;
import Nederlands.Eigen.검사;
import Nederlands.Eigen.invoerstroom;
import Nederlands.Eigen.I_O_uitzondering;

public class Netwerkvoorbeeld {
    public static void starten() throws I_O_uitzondering {
        // host: python3 hulpmiddelen/예제되돌림.py --tcp-port 9000 --udp-port 9001
        verbinding Verbinden = verbinding.Openen("10.0.2.2", 문자.parseren_geheel_getal(실행인수.tekst(0)));
        try {
            Verbinden.TIMEOUT(700);
            byte[] e_mail = 문자.coderen("JAVA TCP Nederlands\n");
            Verbinden.tekstuitvoer().Schrijven(e_mail);
            invoerstroom invoer_WAARDE = Verbinden.invoer_WAARDE();
            for (int nummer = 0; nummer < 문자.byte_AANTAL(e_mail); nummer++) {
                검사.참인지(invoer_WAARDE.Lezen() == (e_mail[nummer] & 255), "TCP reactie 불일치");
            }
        } finally { Verbinden.Sluiten(); }
        datagram_Kanaal eindpunt = datagram_Kanaal.Openen(0);
        try {
            eindpunt.TIMEOUT(700);
            eindpunt.e_mailen("10.0.2.2", 문자.parseren_geheel_getal(실행인수.tekst(1)), "JAVA UDP Nederlands");
            검사.참인지(문자.같음(eindpunt.ontvangen(), "JAVA UDP Nederlands"), "UDP reactie 불일치");
        } finally { eindpunt.Sluiten(); }
        tekstuitvoer.schrijven_lijn("JAVA 네트워크 bevestigen: TCP UDP Nederlands");
    }
}
