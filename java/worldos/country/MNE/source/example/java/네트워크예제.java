// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.veza;
import 한국어.자체.실행인수;
import 한국어.자체.datagram_Kanal;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.U_I_izuzetak;

public class 네트워크예제 {
    public static void koristiti() throws U_I_izuzetak {
        // host: python3 Alatke/예제되돌림.py --tcp-port 9000 --udp-port 9001
        veza veze = veza.otvoren("10.0.2.2", 문자.raščlaniti_ceo_broj(실행인수.SMS(0)));
        try {
            veze.TIMEOUT(700);
            byte[] poruka = 문자.kodirati("JAVA TCP српски\n");
            veze.출력().쓰기(poruka);
            입력흐름 입력 = veze.입력();
            for (int 수 = 0; 수 < 문자.bajt_COUNT(poruka); 수++) {
                검사.참인지(입력.읽기() == (poruka[수] & 255), "TCP odgovor 불일치");
            }
        } finally { veze.Zatvori(); }
        datagram_Kanal učesnik = datagram_Kanal.otvoren(0);
        try {
            učesnik.TIMEOUT(700);
            učesnik.poslati("10.0.2.2", 문자.raščlaniti_ceo_broj(실행인수.SMS(1)), "JAVA UDP српски");
            검사.참인지(문자.같음(učesnik.primiti(), "JAVA UDP српски"), "UDP odgovor 불일치");
        } finally { učesnik.Zatvori(); }
        출력.줄쓰기("JAVA 네트워크 verifikovati: TCP UDP српски");
    }
}
