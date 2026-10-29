// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import hrvatski.vlastiti.veza;
import hrvatski.vlastiti.실행인수;
import hrvatski.vlastiti.datogram_kanal;
import hrvatski.vlastiti.문자;
import hrvatski.vlastiti.Izlaz;
import hrvatski.vlastiti.검사;
import hrvatski.vlastiti.ulazni_tok;
import hrvatski.vlastiti.U_I_iznimka;

public class PrimjerMreže {
    public static void Pokreni() throws U_I_iznimka {
        // domaćin: python3 Alati/예제되돌림.py --tcp-port 9000 --udp-port 9001
        veza Spoji_se = veza.Otvori("10.0.2.2", 문자.rastavljati_cijeli_broj(실행인수.Tekst(0)));
        try {
            Spoji_se.TIMEOUT(700);
            byte[] poruka = 문자.kodirati("JAVA TCP hrvatski\n");
            Spoji_se.Izlaz().Zapisuj(poruka);
            ulazni_tok 입력 = Spoji_se.입력();
            for (int 수 = 0; 수 < 문자.bajt_COUNT(poruka); 수++) {
                검사.참인지(입력.Čitaj() == (poruka[수] & 255), "TCP odgovor 불일치");
            }
        } finally { Spoji_se.Zatvori(); }
        datogram_kanal sudionik = datogram_kanal.Otvori(0);
        try {
            sudionik.TIMEOUT(700);
            sudionik.slati("10.0.2.2", 문자.rastavljati_cijeli_broj(실행인수.Tekst(1)), "JAVA UDP hrvatski");
            검사.참인지(문자.같음(sudionik.primiti(), "JAVA UDP hrvatski"), "UDP odgovor 불일치");
        } finally { sudionik.Zatvori(); }
        Izlaz.zapisivanje_red("JAVA 네트워크 provjeriti: TCP UDP hrvatski");
    }
}
