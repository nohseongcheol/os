// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.ceŋondiral;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.입출력예외;

public class 네트워크예제 {
    public static void huutoraade() throws 입출력예외 {
        // njaatigi: python3 도구/예제되돌림.py --tcp-port 9000 --udp-port 9001
        ceŋondiral seŋaade = ceŋondiral.udditde("10.0.2.2", 문자.정수읽기(실행인수.binndi(0)));
        try {
            seŋaade.대기시간(700);
            byte[] ɓatakuru = 문자.부호화("JAVA TCP ff\n");
            seŋaade.출력().winndude(ɓatakuru);
            입력흐름 입력 = seŋaade.입력();
            for (int 수 = 0; 수 < 문자.바이트수(ɓatakuru); 수++) {
                검사.참인지(입력.읽기() == (ɓatakuru[수] & 255), "TCP 응답 불일치");
            }
        } finally { seŋaade.uddude(); }
        전문통로 종단 = 전문통로.udditde(0);
        try {
            종단.대기시간(700);
            종단.neldude("10.0.2.2", 문자.정수읽기(실행인수.binndi(1)), "JAVA UDP ff");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP ff"), "UDP 응답 불일치");
        } finally { 종단.uddude(); }
        출력.winndude_diidol("JAVA 네트워크 ƴeewtaade: TCP UDP ff");
    }
}
