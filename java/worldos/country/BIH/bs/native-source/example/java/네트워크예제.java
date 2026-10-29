// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.veza;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.Ispis;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.U_I_izuzetak;

public class 네트워크예제 {
    public static void Pokreni() throws U_I_izuzetak {
        // organizator: python3 Alati/예제되돌림.py --tcp-port 9000 --udp-port 9001
        veza Spoji_se = veza.Otvori("10.0.2.2", 문자.raščlanjivati_cijeli_broj(실행인수.Tekst(0)));
        try {
            Spoji_se.TIMEOUT(700);
            byte[] poruka = 문자.부호화("JAVA TCP bs\n");
            Spoji_se.Ispis().Piši(poruka);
            입력흐름 입력 = Spoji_se.입력();
            for (int 수 = 0; 수 < 문자.bajt_COUNT(poruka); 수++) {
                검사.참인지(입력.Čitaj() == (poruka[수] & 255), "TCP odgovoriti 불일치");
            }
        } finally { Spoji_se.Zatvori(); }
        전문통로 završna_tačka = 전문통로.Otvori(0);
        try {
            završna_tačka.TIMEOUT(700);
            završna_tačka.poslati("10.0.2.2", 문자.raščlanjivati_cijeli_broj(실행인수.Tekst(1)), "JAVA UDP bs");
            검사.참인지(문자.같음(završna_tačka.받기(), "JAVA UDP bs"), "UDP odgovoriti 불일치");
        } finally { završna_tačka.Zatvori(); }
        Ispis.pisati_redak("JAVA 네트워크 potvrditi: TCP UDP bs");
    }
}
