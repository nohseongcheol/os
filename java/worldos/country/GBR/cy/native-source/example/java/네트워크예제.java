// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Cymraeg.자체.cyswllt;
import Cymraeg.자체.실행인수;
import Cymraeg.자체.전문통로;
import Cymraeg.자체.문자;
import Cymraeg.자체.Allbwn;
import Cymraeg.자체.검사;
import Cymraeg.자체.입력흐름;
import Cymraeg.자체.I_O_eithriad;

public class 네트워크예제 {
    public static void Gweithredu_2() throws I_O_eithriad {
        // lletya: python3 Offer/예제되돌림.py --tcp-port 9000 --udp-port 9001
        cyswllt Cysylltu = cyswllt.Agor("10.0.2.2", 문자.dosrannu_cyfanrif(실행인수.Testun(0)));
        try {
            Cysylltu.TIMEOUT(700);
            byte[] neges = 문자.부호화("JAVA TCP cy\n");
            Cysylltu.Allbwn().Ysgrifennu(neges);
            입력흐름 입력 = Cysylltu.입력();
            for (int 수 = 0; 수 < 문자.beit_COUNT(neges); 수++) {
                검사.참인지(입력.Darllen() == (neges[수] & 255), "TCP ateb 불일치");
            }
        } finally { Cysylltu.Cau(); }
        전문통로 종단 = 전문통로.Agor(0);
        try {
            종단.TIMEOUT(700);
            종단.anfon("10.0.2.2", 문자.dosrannu_cyfanrif(실행인수.Testun(1)), "JAVA UDP cy");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP cy"), "UDP ateb 불일치");
        } finally { 종단.Cau(); }
        Allbwn.ysgrifennu_llinell("JAVA 네트워크 dilysu: TCP UDP cy");
    }
}
