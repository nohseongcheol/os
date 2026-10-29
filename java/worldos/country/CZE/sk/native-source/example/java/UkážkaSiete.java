// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Slovenský.vlastné.kontakt;
import Slovenský.vlastné.실행인수;
import Slovenský.vlastné.datagram_Kanál;
import Slovenský.vlastné.문자;
import Slovenský.vlastné.Výstup;
import Slovenský.vlastné.검사;
import Slovenský.vlastné.vstupný_prúd_údajov;
import Slovenský.vlastné.vstup_a_výstup_výnimka;

public class UkážkaSiete {
    public static void Spustiť_2() throws vstup_a_výstup_výnimka {
        // hostiteľ: python3 Nástroje/예제되돌림.py --tcp-port 9000 --udp-port 9001
        kontakt Pripojiť = kontakt.Otvoriť("10.0.2.2", 문자.analyzovať_celé_číslo(실행인수.Spracovanie_textu(0)));
        try {
            Pripojiť.TIMEOUT(700);
            byte[] e_mail = 문자.kódovať("JAVA TCP sk\n");
            Pripojiť.Výstup().Zápis(e_mail);
            vstupný_prúd_údajov vstup_VALUE = Pripojiť.vstup_VALUE();
            for (int 수 = 0; 수 < 문자.Byte_COUNT(e_mail); 수++) {
                검사.참인지(vstup_VALUE.Čítanie() == (e_mail[수] & 255), "TCP odozva 불일치");
            }
        } finally { Pripojiť.Zatvoriť(); }
        datagram_Kanál účastník = datagram_Kanál.Otvoriť(0);
        try {
            účastník.TIMEOUT(700);
            účastník.odoslať("10.0.2.2", 문자.analyzovať_celé_číslo(실행인수.Spracovanie_textu(1)), "JAVA UDP sk");
            검사.참인지(문자.같음(účastník.dostať(), "JAVA UDP sk"), "UDP odozva 불일치");
        } finally { účastník.Zatvoriť(); }
        Výstup.zapísať_linka("JAVA 네트워크 overiť: TCP UDP sk");
    }
}
