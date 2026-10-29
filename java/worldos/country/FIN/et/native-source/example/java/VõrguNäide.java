// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Eesti.oma.ühendus;
import Eesti.oma.실행인수;
import Eesti.oma.datagramm_Kanal;
import Eesti.oma.문자;
import Eesti.oma.Väljund;
import Eesti.oma.검사;
import Eesti.oma.sisendvoog;
import Eesti.oma.I_O_erand;

public class VõrguNäide {
    public static void Käivita_2() throws I_O_erand {
        // host: python3 Tööriistad/예제되돌림.py --tcp-port 9000 --udp-port 9001
        ühendus Ühendu = ühendus.Ava("10.0.2.2", 문자.sõeluma_täisarv(실행인수.Tekst(0)));
        try {
            Ühendu.TIMEOUT(700);
            byte[] meil = 문자.kodeerima("JAVA TCP et\n");
            Ühendu.Väljund().Kirjutamine(meil);
            sisendvoog 입력 = Ühendu.입력();
            for (int number = 0; number < 문자.bait_COUNT(meil); number++) {
                검사.참인지(입력.Lugemine() == (meil[number] & 255), "TCP vastus 불일치");
            }
        } finally { Ühendu.Suletud(); }
        datagramm_Kanal osaleja = datagramm_Kanal.Ava(0);
        try {
            osaleja.TIMEOUT(700);
            osaleja.saatma("10.0.2.2", 문자.sõeluma_täisarv(실행인수.Tekst(1)), "JAVA UDP et");
            검사.참인지(문자.같음(osaleja.saama(), "JAVA UDP et"), "UDP vastus 불일치");
        } finally { osaleja.Suletud(); }
        Väljund.kirjutamine_liin("JAVA 네트워크 kinnitama: TCP UDP et");
    }
}
