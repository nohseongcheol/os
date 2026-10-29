// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Dansk.eget.forbindelse;
import Dansk.eget.실행인수;
import Dansk.eget.datagram_Kanal;
import Dansk.eget.문자;
import Dansk.eget.Udgang;
import Dansk.eget.검사;
import Dansk.eget.inputstream;
import Dansk.eget.I_O_undtagelse;

public class Netværkseksempel {
    public static void Kør_2() throws I_O_undtagelse {
        // vært: python3 Værktøjer/예제되돌림.py --tcp-port 9000 --udp-port 9001
        forbindelse Tilslut = forbindelse.Åbn("10.0.2.2", 문자.opdele_tekst_heltal(실행인수.Tekst(0)));
        try {
            Tilslut.TIMEOUT(700);
            byte[] mail_8c783e64 = 문자.kode("JAVA TCP da\n");
            Tilslut.Udgang().Skrive(mail_8c783e64);
            inputstream input_VÆRDI = Tilslut.input_VÆRDI();
            for (int tal = 0; tal < 문자.byte_TÆL(mail_8c783e64); tal++) {
                검사.참인지(input_VÆRDI.Læse() == (mail_8c783e64[tal] & 255), "TCP svar 불일치");
            }
        } finally { Tilslut.Luk(); }
        datagram_Kanal slutpunkt = datagram_Kanal.Åbn(0);
        try {
            slutpunkt.TIMEOUT(700);
            slutpunkt.maile("10.0.2.2", 문자.opdele_tekst_heltal(실행인수.Tekst(1)), "JAVA UDP da");
            검사.참인지(문자.같음(slutpunkt.modtage(), "JAVA UDP da"), "UDP svar 불일치");
        } finally { slutpunkt.Luk(); }
        Udgang.skrive_linje("JAVA 네트워크 bekræfte: TCP UDP da");
    }
}
