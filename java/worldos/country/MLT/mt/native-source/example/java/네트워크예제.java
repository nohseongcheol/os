// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Malti.자체.konnessjoni;
import Malti.자체.실행인수;
import Malti.자체.전문통로;
import Malti.자체.문자;
import Malti.자체.출력;
import Malti.자체.검사;
import Malti.자체.입력흐름;
import Malti.자체.입출력예외;

public class 네트워크예제 {
    public static void serje() throws 입출력예외 {
        // host: python3 Għodod/예제되돌림.py --tcp-port 9000 --udp-port 9001
        konnessjoni AQBAD = konnessjoni.fetaħ("10.0.2.2", 문자.analizza_numru_sħiħ(실행인수.SMS(0)));
        try {
            AQBAD.TIMEOUT(700);
            byte[] messaġġ = 문자.부호화("JAVA TCP mt\n");
            AQBAD.출력().kiteb(messaġġ);
            입력흐름 입력 = AQBAD.입력();
            for (int 수 = 0; 수 < 문자.byte_COUNT(messaġġ); 수++) {
                검사.참인지(입력.읽기() == (messaġġ[수] & 255), "TCP wieġeb 불일치");
            }
        } finally { AQBAD.agħlaq(); }
        전문통로 종단 = 전문통로.fetaħ(0);
        try {
            종단.TIMEOUT(700);
            종단.bagħat("10.0.2.2", 문자.analizza_numru_sħiħ(실행인수.SMS(1)), "JAVA UDP mt");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP mt"), "UDP wieġeb 불일치");
        } finally { 종단.agħlaq(); }
        출력.kiteb_linja("JAVA 네트워크 vverifika: TCP UDP mt");
    }
}
