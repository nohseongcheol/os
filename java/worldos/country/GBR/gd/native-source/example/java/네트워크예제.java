// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.ceangal;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.입출력예외;

public class 네트워크예제 {
    public static void ruith() throws 입출력예외 {
        // òstair: python3 innealan/예제되돌림.py --tcp-port 9000 --udp-port 9001
        ceangal CONNECT = ceangal.fosgail("10.0.2.2", 문자.정수읽기(실행인수.SMS(0)));
        try {
            CONNECT.TIMEOUT(700);
            byte[] teachdaireachd = 문자.부호화("JAVA TCP gd\n");
            CONNECT.출력().sgrìobh(teachdaireachd);
            입력흐름 입력 = CONNECT.입력();
            for (int 수 = 0; 수 < 문자.baidht_COUNT(teachdaireachd); 수++) {
                검사.참인지(입력.읽기() == (teachdaireachd[수] & 255), "TCP freagair 불일치");
            }
        } finally { CONNECT.dùin(); }
        전문통로 종단 = 전문통로.fosgail(0);
        try {
            종단.TIMEOUT(700);
            종단.cuir("10.0.2.2", 문자.정수읽기(실행인수.SMS(1)), "JAVA UDP gd");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP gd"), "UDP freagair 불일치");
        } finally { 종단.dùin(); }
        출력.sgrìobh_loidhne("JAVA 네트워크 dearbh: TCP UDP gd");
    }
}
