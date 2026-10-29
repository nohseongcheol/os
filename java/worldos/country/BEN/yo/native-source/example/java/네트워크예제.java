// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.Ìsomọ́;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.입출력예외;

public class 네트워크예제 {
    public static void Rọ́ọ̀nù() throws 입출력예외 {
        // olùpèsè: python3 Àwọn_irinṣẹ́/예제되돌림.py --tcp-port 9000 --udp-port 9001
        Ìsomọ́ Darapọ̀ = Ìsomọ́.Ṣi("10.0.2.2", 문자.ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(실행인수.SMS(0)));
        try {
            Darapọ̀.대기시간(700);
            byte[] iṣé = 문자.부호화("JAVA TCP yo\n");
            Darapọ̀.출력().Kọ(iṣé);
            입력흐름 입력 = Darapọ̀.입력();
            for (int 수 = 0; 수 < 문자.바이트수(iṣé); 수++) {
                검사.참인지(입력.Kàá() == (iṣé[수] & 255), "TCP Fèsì 불일치");
            }
        } finally { Darapọ̀.Ti(); }
        전문통로 종단 = 전문통로.Ṣi(0);
        try {
            종단.대기시간(700);
            종단.í_meèlì("10.0.2.2", 문자.ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(실행인수.SMS(1)), "JAVA UDP yo");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP yo"), "UDP Fèsì 불일치");
        } finally { 종단.Ti(); }
        출력.kọ_ìlà("JAVA 네트워크 ridájú: TCP UDP yo");
    }
}
