// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.kgokaganya;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.입출력예외;

public class 네트워크예제 {
    public static void Diriša() throws 입출력예외 {
        // go_nea_ditirelo: python3 Ditholosi/예제되돌림.py --tcp-port 9000 --udp-port 9001
        kgokaganya Ikgokaganye = kgokaganya.Bula("10.0.2.2", 문자.ripaganya_palotlalo(실행인수.Sengwalwa(0)));
        try {
            Ikgokaganye.대기시간(700);
            byte[] molaetša = 문자.부호화("JAVA TCP nso\n");
            Ikgokaganye.출력().Ngwala(molaetša);
            입력흐름 입력 = Ikgokaganye.입력();
            for (int 수 = 0; 수 < 문자.바이트수(molaetša); 수++) {
                검사.참인지(입력.Bala() == (molaetša[수] & 255), "TCP fetola 불일치");
            }
        } finally { Ikgokaganye.Tswalela(); }
        전문통로 종단 = 전문통로.Bula(0);
        try {
            종단.대기시간(700);
            종단.Romela("10.0.2.2", 문자.ripaganya_palotlalo(실행인수.Sengwalwa(1)), "JAVA UDP nso");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP nso"), "UDP fetola 불일치");
        } finally { 종단.Tswalela(); }
        출력.ngwala_mothaladi("JAVA 네트워크 kgonthiša: TCP UDP nso");
    }
}
