// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Isi_Zulu.자체.uxhumano;
import Isi_Zulu.자체.실행인수;
import Isi_Zulu.자체.전문통로;
import Isi_Zulu.자체.문자;
import Isi_Zulu.자체.출력;
import Isi_Zulu.자체.검사;
import Isi_Zulu.자체.입력흐름;
import Isi_Zulu.자체.입출력예외;

public class 네트워크예제 {
    public static void Sebenzisa() throws 입출력예외 {
        // singatha: python3 Amathuluzi/예제되돌림.py --tcp-port 9000 --udp-port 9001
        uxhumano Xhumanisa = uxhumano.Vula("10.0.2.2", 문자.zawula_inamba(실행인수.Itekisi(0)));
        try {
            Xhumanisa.대기시간(700);
            byte[] umlayezo = 문자.부호화("JAVA TCP zu\n");
            Xhumanisa.출력().Bhala(umlayezo);
            입력흐름 입력 = Xhumanisa.입력();
            for (int 수 = 0; 수 < 문자.바이트수(umlayezo); 수++) {
                검사.참인지(입력.Funda() == (umlayezo[수] & 255), "TCP phendula 불일치");
            }
        } finally { Xhumanisa.Vala(); }
        전문통로 종단 = 전문통로.Vula(0);
        try {
            종단.대기시간(700);
            종단.Thumela("10.0.2.2", 문자.zawula_inamba(실행인수.Itekisi(1)), "JAVA UDP zu");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP zu"), "UDP phendula 불일치");
        } finally { 종단.Vala(); }
        출력.bhala_umugqa("JAVA 네트워크 qiniseka: TCP UDP zu");
    }
}
