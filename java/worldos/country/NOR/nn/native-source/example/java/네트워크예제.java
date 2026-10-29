// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.kontakt;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.Utdata;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.I_U_unntak;

public class 네트워크예제 {
    public static void Køyr_2() throws I_U_unntak {
        // vert: python3 Verktøy/예제되돌림.py --tcp-port 9000 --udp-port 9001
        kontakt Kopla_til = kontakt.Opna("10.0.2.2", 문자.dele_opp_heiltal(실행인수.Tekst(0)));
        try {
            Kopla_til.TIMEOUT(700);
            byte[] melding = 문자.부호화("JAVA TCP nn\n");
            Kopla_til.Utdata().Skriv(melding);
            입력흐름 입력 = Kopla_til.입력();
            for (int 수 = 0; 수 < 문자.byte_COUNT(melding); 수++) {
                검사.참인지(입력.Les() == (melding[수] & 255), "TCP svare 불일치");
            }
        } finally { Kopla_til.Lukk(); }
        전문통로 endepunkt = 전문통로.Opna(0);
        try {
            endepunkt.TIMEOUT(700);
            endepunkt.sende("10.0.2.2", 문자.dele_opp_heiltal(실행인수.Tekst(1)), "JAVA UDP nn");
            검사.참인지(문자.같음(endepunkt.받기(), "JAVA UDP nn"), "UDP svare 불일치");
        } finally { endepunkt.Lukk(); }
        Utdata.skrive_line("JAVA 네트워크 stadfeste: TCP UDP nn");
    }
}
