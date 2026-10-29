// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.jokkalóo;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.입출력예외;

public class 네트워크예제 {
    public static void daw() throws 입출력예외 {
        // dalal: python3 Jumtukaay_yi/예제되돌림.py --tcp-port 9000 --udp-port 9001
        jokkalóo JOKKOO = jokkalóo.sos("10.0.2.2", 문자.Segg_lëmm(실행인수.Tekst(0)));
        try {
            JOKKOO.대기시간(700);
            byte[] bataaxal = 문자.부호화("JAVA TCP Wolof\n");
            JOKKOO.출력().biir(bataaxal);
            입력흐름 입력 = JOKKOO.입력();
            for (int 수 = 0; 수 < 문자.바이트수(bataaxal); 수++) {
                검사.참인지(입력.읽기() == (bataaxal[수] & 255), "TCP tontu 불일치");
            }
        } finally { JOKKOO.Tej(); }
        전문통로 종단 = 전문통로.sos(0);
        try {
            종단.대기시간(700);
            종단.Yónnee("10.0.2.2", 문자.Segg_lëmm(실행인수.Tekst(1)), "JAVA UDP Wolof");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP Wolof"), "UDP tontu 불일치");
        } finally { 종단.Tej(); }
        출력.biir_buum("JAVA 네트워크 luñutu: TCP UDP Wolof");
    }
}
