// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Română.propriu.conexiune;
import Română.propriu.실행인수;
import Română.propriu.diagramă_informații_Canal;
import Română.propriu.문자;
import Română.propriu.Rezultat;
import Română.propriu.검사;
import Română.propriu.flux_de_intrare;
import Română.propriu.I_O_excepție;

public class ExempluRețea {
    public static void Pornește() throws I_O_excepție {
        // gazdă: python3 Instrumente/예제되돌림.py --tcp-port 9000 --udp-port 9001
        conexiune Conectează = conexiune.Deschide("10.0.2.2", 문자.analiza_întreg(실행인수.SMS(0)));
        try {
            Conectează.TIMEOUT(700);
            byte[] mesaj = 문자.codifica("JAVA TCP ro\n");
            Conectează.Rezultat().Scriere(mesaj);
            flux_de_intrare 입력 = Conectează.입력();
            for (int 수 = 0; 수 < 문자.byte_COUNT(mesaj); 수++) {
                검사.참인지(입력.Citire() == (mesaj[수] & 255), "TCP replică 불일치");
            }
        } finally { Conectează.Închide(); }
        diagramă_informații_Canal participant = diagramă_informații_Canal.Deschide(0);
        try {
            participant.TIMEOUT(700);
            participant.trimite("10.0.2.2", 문자.analiza_întreg(실행인수.SMS(1)), "JAVA UDP ro");
            검사.참인지(문자.같음(participant.primi(), "JAVA UDP ro"), "UDP replică 불일치");
        } finally { participant.Închide(); }
        Rezultat.scriere_linie("JAVA 네트워크 verifica: TCP UDP ro");
    }
}
