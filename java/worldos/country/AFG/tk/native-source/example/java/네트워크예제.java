// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.birikme;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.입출력예외;

public class 네트워크예제 {
    public static void Bitir() throws 입출력예외 {
        // esasy: python3 Gurallar/예제되돌림.py --tcp-port 9000 --udp-port 9001
        birikme Birikme = birikme.Aç("10.0.2.2", 문자.seljer_bitin(실행인수.Metin(0)));
        try {
            Birikme.대기시간(700);
            byte[] habar = 문자.부호화("JAVA TCP tk\n");
            Birikme.출력().Ýaz(habar);
            입력흐름 입력 = Birikme.입력();
            for (int 수 = 0; 수 < 문자.바이트수(habar); 수++) {
                검사.참인지(입력.Oka() == (habar[수] & 255), "TCP jogap_bermek 불일치");
            }
        } finally { Birikme.Ýap(); }
        전문통로 종단 = 전문통로.Aç(0);
        try {
            종단.대기시간(700);
            종단.iber("10.0.2.2", 문자.seljer_bitin(실행인수.Metin(1)), "JAVA UDP tk");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP tk"), "UDP jogap_bermek 불일치");
        } finally { 종단.Ýap(); }
        출력.ýaz_setir("JAVA 네트워크 barla: TCP UDP tk");
    }
}
