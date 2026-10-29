// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.lidhje;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.I_O_përjashtim;

public class 네트워크예제 {
    public static void Ekzekuto() throws I_O_përjashtim {
        // pritës: python3 Mjete/예제되돌림.py --tcp-port 9000 --udp-port 9001
        lidhje Lidhu = lidhje.Hap("10.0.2.2", 문자.analizoj_numër_i_plotë(실행인수.Teksti(0)));
        try {
            Lidhu.TIMEOUT(700);
            byte[] email_8c783e64 = 문자.부호화("JAVA TCP Albanian\n");
            Lidhu.출력().Shkrimi(email_8c783e64);
            입력흐름 입력 = Lidhu.입력();
            for (int 수 = 0; 수 < 문자.bajt_COUNT(email_8c783e64); 수++) {
                검사.참인지(입력.Leximi() == (email_8c783e64[수] & 255), "TCP replikë 불일치");
            }
        } finally { Lidhu.Mbyll(); }
        전문통로 종단 = 전문통로.Hap(0);
        try {
            종단.TIMEOUT(700);
            종단.dërgoj("10.0.2.2", 문자.analizoj_numër_i_plotë(실행인수.Teksti(1)), "JAVA UDP Albanian");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP Albanian"), "UDP replikë 불일치");
        } finally { 종단.Mbyll(); }
        출력.shkruaj_linjë("JAVA 네트워크 verifikoj: TCP UDP Albanian");
    }
}
