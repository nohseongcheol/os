// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.haɗi;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.출력;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.I_O_banbanchi;

public class 네트워크예제 {
    public static void Tafiyar_da() throws I_O_banbanchi {
        // sauka: python3 Kaya/예제되돌림.py --tcp-port 9000 --udp-port 9001
        haɗi Haɗi = haɗi.Buɗe("10.0.2.2", 문자.Daddatse_Lamba_mara(실행인수.SMS(0)));
        try {
            Haɗi.대기시간(700);
            byte[] imel_8c783e64 = 문자.부호화("JAVA TCP ha\n");
            Haɗi.출력().Yi_Rubutu(imel_8c783e64);
            입력흐름 입력 = Haɗi.입력();
            for (int 수 = 0; 수 < 문자.바이트수(imel_8c783e64); 수++) {
                검사.참인지(입력.Yi_Karatu() == (imel_8c783e64[수] & 255), "TCP mayar_da_martani 불일치");
            }
        } finally { Haɗi.Rufe(); }
        전문통로 종단 = 전문통로.Buɗe(0);
        try {
            종단.대기시간(700);
            종단.Aika("10.0.2.2", 문자.Daddatse_Lamba_mara(실행인수.SMS(1)), "JAVA UDP ha");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP ha"), "UDP mayar_da_martani 불일치");
        } finally { 종단.Rufe(); }
        출력.Rubuta_Layi("JAVA 네트워크 Tabbatar_da: TCP UDP ha");
    }
}
