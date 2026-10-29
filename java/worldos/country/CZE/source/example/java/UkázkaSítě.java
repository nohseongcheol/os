// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import čeština.vlastní.kontakt;
import čeština.vlastní.실행인수;
import čeština.vlastní.datagram_Kanál;
import čeština.vlastní.문자;
import čeština.vlastní.výstupní_pozice;
import čeština.vlastní.검사;
import čeština.vlastní.vstupní_datový_proud;
import čeština.vlastní.vstup_a_výstup_výjimka;

public class UkázkaSítě {
    public static void Spustit_2() throws vstup_a_výstup_výjimka {
        // hostit: python3 nástroje/예제되돌림.py --tcp-port 9000 --udp-port 9001
        kontakt Připojit = kontakt.Otevřít("10.0.2.2", 문자.parsovat_integer(실행인수.text(0)));
        try {
            Připojit.TIMEOUT(700);
            byte[] e_mail = 문자.kódovat("JAVA TCP čeština\n");
            Připojit.výstupní_pozice().Zápis(e_mail);
            vstupní_datový_proud vstup_HODNOTA = Připojit.vstup_HODNOTA();
            for (int číslo = 0; číslo < 문자.bajt_POČET(e_mail); číslo++) {
                검사.참인지(vstup_HODNOTA.Čtení() == (e_mail[číslo] & 255), "TCP odezva 불일치");
            }
        } finally { Připojit.Zavřené(); }
        datagram_Kanál účastník = datagram_Kanál.Otevřít(0);
        try {
            účastník.TIMEOUT(700);
            účastník.poslat("10.0.2.2", 문자.parsovat_integer(실행인수.text(1)), "JAVA UDP čeština");
            검사.참인지(문자.같음(účastník.dostat(), "JAVA UDP čeština"), "UDP odezva 불일치");
        } finally { účastník.Zavřené(); }
        výstupní_pozice.zápis_čára("JAVA 네트워크 ověřit: TCP UDP čeština");
    }
}
