// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Ikinyarwanda.자체.kwihuza;
import Ikinyarwanda.자체.실행인수;
import Ikinyarwanda.자체.전문통로;
import Ikinyarwanda.자체.문자;
import Ikinyarwanda.자체.출력;
import Ikinyarwanda.자체.검사;
import Ikinyarwanda.자체.입력흐름;
import Ikinyarwanda.자체.입출력예외;

public class 네트워크예제 {
    public static void ihuriro() throws 입출력예외 {
        // gucumbikira: python3 Ibikoresho/예제되돌림.py --tcp-port 9000 --udp-port 9001
        kwihuza Guhuza = kwihuza.Gufungura("10.0.2.2", 문자.gusesengura_umubare_wuzuye(실행인수.Umwandiko(0)));
        try {
            Guhuza.대기시간(700);
            byte[] ubutumwa = 문자.부호화("JAVA TCP Ikinyarwanda\n");
            Guhuza.출력().kwandika(ubutumwa);
            입력흐름 입력 = Guhuza.입력();
            for (int 수 = 0; 수 < 문자.바이트수(ubutumwa); 수++) {
                검사.참인지(입력.읽기() == (ubutumwa[수] & 255), "TCP gusubiza 불일치");
            }
        } finally { Guhuza.Gufunga(); }
        전문통로 종단 = 전문통로.Gufungura(0);
        try {
            종단.대기시간(700);
            종단.kohereza("10.0.2.2", 문자.gusesengura_umubare_wuzuye(실행인수.Umwandiko(1)), "JAVA UDP Ikinyarwanda");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP Ikinyarwanda"), "UDP gusubiza 불일치");
        } finally { 종단.Gufunga(); }
        출력.kwandika_umurongo("JAVA 네트워크 gusuzuma: TCP UDP Ikinyarwanda");
    }
}
