// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Lietuvių.savas.ryšys;
import Lietuvių.savas.실행인수;
import Lietuvių.savas.paketų_kelio_schema_kanalas;
import Lietuvių.savas.문자;
import Lietuvių.savas.Išvestis;
import Lietuvių.savas.검사;
import Lietuvių.savas.įvesties_srautas;
import Lietuvių.savas.Į_I_išimtis;

public class TinkloPavyzdys {
    public static void Paleisti() throws Į_I_išimtis {
        // organizuoti: python3 Įrankiai/예제되돌림.py --tcp-port 9000 --udp-port 9001
        ryšys Prisijungti = ryšys.Atverti("10.0.2.2", 문자.analizuoti_sintaksę_sveikasis_skaičius(실행인수.Tekstas(0)));
        try {
            Prisijungti.SKIRTASIS_LAIKAS(700);
            byte[] žinutė = 문자.koduoti("JAVA TCP Lietuvių\n");
            Prisijungti.Išvestis().Rašymas(žinutė);
            įvesties_srautas 입력 = Prisijungti.입력();
            for (int numeris = 0; numeris < 문자.baitas_COUNT(žinutė); numeris++) {
                검사.참인지(입력.Skaitymas() == (žinutė[numeris] & 255), "TCP atsakyti 불일치");
            }
        } finally { Prisijungti.Užverti(); }
        paketų_kelio_schema_kanalas dalyvis = paketų_kelio_schema_kanalas.Atverti(0);
        try {
            dalyvis.SKIRTASIS_LAIKAS(700);
            dalyvis.siųsti("10.0.2.2", 문자.analizuoti_sintaksę_sveikasis_skaičius(실행인수.Tekstas(1)), "JAVA UDP Lietuvių");
            검사.참인지(문자.같음(dalyvis.gauti(), "JAVA UDP Lietuvių"), "UDP atsakyti 불일치");
        } finally { dalyvis.Užverti(); }
        Išvestis.rašymas_eilutė("JAVA 네트워크 patvirtinti: TCP UDP Lietuvių");
    }
}
