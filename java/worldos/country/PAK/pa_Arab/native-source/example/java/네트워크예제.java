// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.کنکشن;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.입출력예외;

public class 네트워크예제 {
    public static void چلاؤ() throws 입출력예외 {
        // مہمان_b78e430d: python3 اوزار/예제되돌림.py --tcp-port 9000 --udp-port 9001
        کنکشن جڑو = کنکشن.بنڑاؤ("10.0.2.2", 문자.정수읽기(실행인수.متن(0)));
        try {
            جڑو.대기시간(700);
            byte[] پیغام = 문자.부호화("JAVA TCP pa_Arab\n");
            جڑو.출력().لکھو(پیغام);
            입력흐름 입력 = جڑو.입력();
            for (int 수 = 0; 수 < 문자.바이트수(پیغام); 수++) {
                검사.참인지(입력.읽기() == (پیغام[수] & 255), "TCP جواب_دیوؤ 불일치");
            }
        } finally { جڑو.بند_کرو(); }
        전문통로 종단 = 전문통로.بنڑاؤ(0);
        try {
            종단.대기시간(700);
            종단.بھیجو("10.0.2.2", 문자.정수읽기(실행인수.متن(1)), "JAVA UDP pa_Arab");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP pa_Arab"), "UDP جواب_دیوؤ 불일치");
        } finally { 종단.بند_کرو(); }
        출력.لکھو_لائن("JAVA 네트워크 تصدیق_کرو: TCP UDP pa_Arab");
    }
}
