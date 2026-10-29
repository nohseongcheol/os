// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Latviešu.savs.paziņa;
import Latviešu.savs.실행인수;
import Latviešu.savs.datogramma_Kanāls;
import Latviešu.savs.문자;
import Latviešu.savs.Izvade;
import Latviešu.savs.검사;
import Latviešu.savs.ievades_straume;
import Latviešu.savs.ievadizvade_izņēmums;

public class TīklaPiemērs {
    public static void Palaist() throws ievadizvade_izņēmums {
        // viesot: python3 Rīki/예제되돌림.py --tcp-port 9000 --udp-port 9001
        paziņa Savienoties = paziņa.Atvērt("10.0.2.2", 문자.parsēt_vesels_skaitlis(실행인수.Teksts(0)));
        try {
            Savienoties.NOILGUMS(700);
            byte[] ziņa = 문자.kodēt("JAVA TCP lv\n");
            Savienoties.Izvade().Rakstīt(ziņa);
            ievades_straume 입력 = Savienoties.입력();
            for (int numurs = 0; numurs < 문자.byte_COUNT(ziņa); numurs++) {
                검사.참인지(입력.Lasīt() == (ziņa[numurs] & 255), "TCP atbilde 불일치");
            }
        } finally { Savienoties.Aizvērt(); }
        datogramma_Kanāls dalībnieks = datogramma_Kanāls.Atvērt(0);
        try {
            dalībnieks.NOILGUMS(700);
            dalībnieks.sūtīt("10.0.2.2", 문자.parsēt_vesels_skaitlis(실행인수.Teksts(1)), "JAVA UDP lv");
            검사.참인지(문자.같음(dalībnieks.saņemt(), "JAVA UDP lv"), "UDP atbilde 불일치");
        } finally { dalībnieks.Aizvērt(); }
        Izvade.rakstīšana_līnija("JAVA 네트워크 verificēt: TCP UDP lv");
    }
}
