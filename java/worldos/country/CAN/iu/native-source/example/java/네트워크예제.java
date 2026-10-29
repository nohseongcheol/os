// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.kasuqsimaniq;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.입출력예외;

public class 네트워크예제 {
    public static void 시작() throws 입출력예외 {
        // tuttarvik: python3 도구/예제되돌림.py --tcp-port 9000 --udp-port 9001
        kasuqsimaniq kasurli = kasuqsimaniq.matuirli("10.0.2.2", 문자.agguqtuut_naasaut(실행인수.titiqqaq(0)));
        try {
            kasurli.대기시간(700);
            byte[] titiqqausiaq = 문자.부호화("JAVA TCP iu\n");
            kasurli.출력().titiraq(titiqqausiaq);
            입력흐름 입력 = kasurli.입력();
            for (int 수 = 0; 수 < 문자.바이트수(titiqqausiaq); 수++) {
                검사.참인지(입력.읽기() == (titiqqausiaq[수] & 255), "TCP 응답 불일치");
            }
        } finally { kasurli.matuli(); }
        전문통로 종단 = 전문통로.matuirli(0);
        try {
            종단.대기시간(700);
            종단.nassiutili("10.0.2.2", 문자.agguqtuut_naasaut(실행인수.titiqqaq(1)), "JAVA UDP iu");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP iu"), "UDP 응답 불일치");
        } finally { 종단.matuli(); }
        출력.titiraq_titikutaak("JAVA 네트워크 nalunairli_1aacb54c: TCP UDP iu");
    }
}
