// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.aloqa;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.I_O_istisno;

public class 네트워크예제 {
    public static void Bajarish() throws I_O_istisno {
        // tashkilotchi: python3 Vositalar/예제되돌림.py --tcp-port 9000 --udp-port 9001
        aloqa Ulanish = aloqa.Ochish("10.0.2.2", 문자.tahlil_qilmoq_butun_son(실행인수.Matn(0)));
        try {
            Ulanish.TANAFFUS(700);
            byte[] xabar = 문자.부호화("JAVA TCP uz\n");
            Ulanish.출력().Yozish(xabar);
            입력흐름 입력 = Ulanish.입력();
            for (int 수 = 0; 수 < 문자.bayt_COUNT(xabar); 수++) {
                검사.참인지(입력.Oʻqish() == (xabar[수] & 255), "TCP javob_berish 불일치");
            }
        } finally { Ulanish.Yopish(); }
        전문통로 종단 = 전문통로.Ochish(0);
        try {
            종단.TANAFFUS(700);
            종단.yuborish("10.0.2.2", 문자.tahlil_qilmoq_butun_son(실행인수.Matn(1)), "JAVA UDP uz");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP uz"), "UDP javob_berish 불일치");
        } finally { 종단.Yopish(); }
        출력.yozmoq_satr("JAVA 네트워크 tasdiqlamoq: TCP UDP uz");
    }
}
