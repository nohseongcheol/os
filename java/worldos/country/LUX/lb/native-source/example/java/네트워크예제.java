// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.Verbindung;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.입출력예외;

public class 네트워크예제 {
    public static void Laf() throws 입출력예외 {
        // Host: python3 Tools/예제되돌림.py --tcp-port 9000 --udp-port 9001
        Verbindung Verbannen = Verbindung.ariichten("10.0.2.2", 문자.analyséieren_Ganzzuel(실행인수.SMS(0)));
        try {
            Verbannen.TIMEOUT(700);
            byte[] Noriicht = 문자.부호화("JAVA TCP lb\n");
            Verbannen.출력().schreiwen(Noriicht);
            입력흐름 입력 = Verbannen.입력();
            for (int 수 = 0; 수 < 문자.Byte_COUNT(Noriicht); 수++) {
                검사.참인지(입력.읽기() == (Noriicht[수] & 255), "TCP äntweren 불일치");
            }
        } finally { Verbannen.Clôture(); }
        전문통로 종단 = 전문통로.ariichten(0);
        try {
            종단.TIMEOUT(700);
            종단.mailen("10.0.2.2", 문자.analyséieren_Ganzzuel(실행인수.SMS(1)), "JAVA UDP lb");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP lb"), "UDP äntweren 불일치");
        } finally { 종단.Clôture(); }
        출력.schreiwen_Zeil("JAVA 네트워크 verifizéieren: TCP UDP lb");
    }
}
