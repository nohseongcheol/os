// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.Kgolagano;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.입출력예외;

public class 네트워크예제 {
    public static void dirisa() throws 입출력예외 {
        // pinagare: python3 Thuluse/예제되돌림.py --tcp-port 9000 --udp-port 9001
        Kgolagano Golaganya = Kgolagano.bula("10.0.2.2", 문자.go_lokolola_Palotlalo(실행인수.SMS(0)));
        try {
            Golaganya.대기시간(700);
            byte[] molaetsa = 문자.부호화("JAVA TCP tn\n");
            Golaganya.출력().kwala(molaetsa);
            입력흐름 입력 = Golaganya.입력();
            for (int 수 = 0; 수 < 문자.바이트수(molaetsa); 수++) {
                검사.참인지(입력.읽기() == (molaetsa[수] & 255), "TCP araba 불일치");
            }
        } finally { Golaganya.tswala(); }
        전문통로 종단 = 전문통로.bula(0);
        try {
            종단.대기시간(700);
            종단.romela("10.0.2.2", 문자.go_lokolola_Palotlalo(실행인수.SMS(1)), "JAVA UDP tn");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP tn"), "UDP araba 불일치");
        } finally { 종단.tswala(); }
        출력.kwala_Mola("JAVA 네트워크 netefatsa: TCP UDP tn");
    }
}
