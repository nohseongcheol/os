// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.epe_ipajia;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.입출력예외;

public class 네트워크예제 {
    public static void 시작() throws 입출력예외 {
        // epiajatü: python3 도구/예제되돌림.py --tcp-port 9000 --udp-port 9001
        epe_ipajia a_ataa = epe_ipajia.열기("10.0.2.2", 문자.akatajaa_waneepiasü(실행인수.글(0)));
        try {
            a_ataa.대기시간(700);
            byte[] pütchi = 문자.부호화("JAVA TCP guc\n");
            a_ataa.출력().ashajaa(pütchi);
            입력흐름 입력 = a_ataa.입력();
            for (int 수 = 0; 수 < 문자.바이트수(pütchi); 수++) {
                검사.참인지(입력.읽기() == (pütchi[수] & 255), "TCP 응답 불일치");
            }
        } finally { a_ataa.asürülaa(); }
        전문통로 종단 = 전문통로.열기(0);
        try {
            종단.대기시간(700);
            종단.ajütaa("10.0.2.2", 문자.akatajaa_waneepiasü(실행인수.글(1)), "JAVA UDP guc");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP guc"), "UDP 응답 불일치");
        } finally { 종단.asürülaa(); }
        출력.ashajaa_liinia("JAVA 네트워크 확인: TCP UDP guc");
    }
}
