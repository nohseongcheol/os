// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import suomi.oma.yhteys;
import suomi.oma.실행인수;
import suomi.oma.datagrammi_Media;
import suomi.oma.문자;
import suomi.oma.tulostuspaikka;
import suomi.oma.검사;
import suomi.oma.syötevirta;
import suomi.oma.I_O_poikkeus;

public class Verkkoesimerkki {
    public static void Suorita_2() throws I_O_poikkeus {
        // isäntä: python3 työkalut/예제되돌림.py --tcp-port 9000 --udp-port 9001
        yhteys Yhdistä = yhteys.Avaa("10.0.2.2", 문자.jäsentää_kokonaisluku(실행인수.teksti(0)));
        try {
            Yhdistä.AIKAKATKAISU(700);
            byte[] sanoma = 문자.koodata("JAVA TCP suomi\n");
            Yhdistä.tulostuspaikka().Kirjoitus(sanoma);
            syötevirta syöte_ARVO = Yhdistä.syöte_ARVO();
            for (int numero = 0; numero < 문자.tavu_LASKE(sanoma); numero++) {
                검사.참인지(syöte_ARVO.Luku() == (sanoma[numero] & 255), "TCP palaute 불일치");
            }
        } finally { Yhdistä.Sulje(); }
        datagrammi_Media päätepiste = datagrammi_Media.Avaa(0);
        try {
            päätepiste.AIKAKATKAISU(700);
            päätepiste.lähettää("10.0.2.2", 문자.jäsentää_kokonaisluku(실행인수.teksti(1)), "JAVA UDP suomi");
            검사.참인지(문자.같음(päätepiste.saada(), "JAVA UDP suomi"), "UDP palaute 불일치");
        } finally { päätepiste.Sulje(); }
        tulostuspaikka.kirjoitus_rivi("JAVA 네트워크 tarkistaa: TCP UDP suomi");
    }
}
