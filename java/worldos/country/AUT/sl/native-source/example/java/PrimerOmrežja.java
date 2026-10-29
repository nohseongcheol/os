// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import slovenščina.lastno.povezava;
import slovenščina.lastno.실행인수;
import slovenščina.lastno.datagram_Kanal;
import slovenščina.lastno.문자;
import slovenščina.lastno.Izpis;
import slovenščina.lastno.검사;
import slovenščina.lastno.vhodni_tok;
import slovenščina.lastno.V_I_izjema;

public class PrimerOmrežja {
    public static void Zaženi() throws V_I_izjema {
        // gostiti: python3 Orodja/예제되돌림.py --tcp-port 9000 --udp-port 9001
        povezava Poveži = povezava.Odpri("10.0.2.2", 문자.razčlenjevati_celo_število(실행인수.Besedilo(0)));
        try {
            Poveži.TIMEOUT(700);
            byte[] e_pošta = 문자.kodirati("JAVA TCP sl\n");
            Poveži.Izpis().Pisanje(e_pošta);
            vhodni_tok 입력 = Poveži.입력();
            for (int 수 = 0; 수 < 문자.bajt_COUNT(e_pošta); 수++) {
                검사.참인지(입력.Branje() == (e_pošta[수] & 255), "TCP odgovor 불일치");
            }
        } finally { Poveži.Zapri(); }
        datagram_Kanal končna_točka = datagram_Kanal.Odpri(0);
        try {
            končna_točka.TIMEOUT(700);
            končna_točka.poslati("10.0.2.2", 문자.razčlenjevati_celo_število(실행인수.Besedilo(1)), "JAVA UDP sl");
            검사.참인지(문자.같음(končna_točka.sprejeti_sprejemati_prejeti_prejemati(), "JAVA UDP sl"), "UDP odgovor 불일치");
        } finally { končna_točka.Zapri(); }
        Izpis.pisati_linija("JAVA 네트워크 확인: TCP UDP sl");
    }
}
