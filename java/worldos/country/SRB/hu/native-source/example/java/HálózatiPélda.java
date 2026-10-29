// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import magyar.saját.ismerős;
import magyar.saját.실행인수;
import magyar.saját.datagram_Csatorna;
import magyar.saját.문자;
import magyar.saját.Kimenet;
import magyar.saját.검사;
import magyar.saját.bemeneti_adatfolyam;
import magyar.saját.I_O_kivétel;

public class HálózatiPélda {
    public static void Futtatás() throws I_O_kivétel {
        // gazda: python3 Eszközök/예제되돌림.py --tcp-port 9000 --udp-port 9001
        ismerős Kapcsolódás = ismerős.Megnyitás("10.0.2.2", 문자.elemez_egész_szám(실행인수.Szöveg(0)));
        try {
            Kapcsolódás.IDŐTÚLLÉPÉS(700);
            byte[] e_mail = 문자.kódolás("JAVA TCP hu\n");
            Kapcsolódás.Kimenet().Írás(e_mail);
            bemeneti_adatfolyam bevitel_ÉRTÉK = Kapcsolódás.bevitel_ÉRTÉK();
            for (int szám = 0; szám < 문자.bájt_DARAB(e_mail); szám++) {
                검사.참인지(bevitel_ÉRTÉK.Olvasás() == (e_mail[szám] & 255), "TCP válasz 불일치");
            }
        } finally { Kapcsolódás.Bezárás(); }
        datagram_Csatorna végpont = datagram_Csatorna.Megnyitás(0);
        try {
            végpont.IDŐTÚLLÉPÉS(700);
            végpont.küld("10.0.2.2", 문자.elemez_egész_szám(실행인수.Szöveg(1)), "JAVA UDP hu");
            검사.참인지(문자.같음(végpont.fogad(), "JAVA UDP hu"), "UDP válasz 불일치");
        } finally { végpont.Bezárás(); }
        Kimenet.ír_sor("JAVA 네트워크 igazol: TCP UDP hu");
    }
}
