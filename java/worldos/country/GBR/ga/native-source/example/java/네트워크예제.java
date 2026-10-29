// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Gaeilge.자체.nasc;
import Gaeilge.자체.실행인수;
import Gaeilge.자체.전문통로;
import Gaeilge.자체.문자;
import Gaeilge.자체.Aschur;
import Gaeilge.자체.검사;
import Gaeilge.자체.입력흐름;
import Gaeilge.자체.I_O_eisceacht;

public class 네트워크예제 {
    public static void Rith_2() throws I_O_eisceacht {
        // óstach: python3 Uirlisí/예제되돌림.py --tcp-port 9000 --udp-port 9001
        nasc Nasc = nasc.Oscail("10.0.2.2", 문자.parsáil_slánuimhir(실행인수.Téacs(0)));
        try {
            Nasc.TIMEOUT(700);
            byte[] teachtaireacht = 문자.부호화("JAVA TCP ga\n");
            Nasc.Aschur().Scríobh(teachtaireacht);
            입력흐름 입력 = Nasc.입력();
            for (int 수 = 0; 수 < 문자.beart_COUNT(teachtaireacht); 수++) {
                검사.참인지(입력.Léigh() == (teachtaireacht[수] & 255), "TCP freagair 불일치");
            }
        } finally { Nasc.Dún(); }
        전문통로 종단 = 전문통로.Oscail(0);
        try {
            종단.TIMEOUT(700);
            종단.seol("10.0.2.2", 문자.parsáil_slánuimhir(실행인수.Téacs(1)), "JAVA UDP ga");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP ga"), "UDP freagair 불일치");
        } finally { 종단.Dún(); }
        Aschur.scríobh_líne("JAVA 네트워크 fíoraigh: TCP UDP ga");
    }
}
