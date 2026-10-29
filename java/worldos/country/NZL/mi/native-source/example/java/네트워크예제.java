// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Reo_Māori.자체.hononga_d584d28a;
import Reo_Māori.자체.실행인수;
import Reo_Māori.자체.전문통로;
import Reo_Māori.자체.문자;
import Reo_Māori.자체.출력;
import Reo_Māori.자체.검사;
import Reo_Māori.자체.입력흐름;
import Reo_Māori.자체.입출력예외;

public class 네트워크예제 {
    public static void whakahaere() throws 입출력예외 {
        // taurima: python3 Ngā_Utauta/예제되돌림.py --tcp-port 9000 --udp-port 9001
        hononga_d584d28a TŪHONO = hononga_d584d28a.Huaki("10.0.2.2", 문자.poroporo_tau_tōpū(실행인수.Ngā_kupu(0)));
        try {
            TŪHONO.KUA_PAU_TE_WĀ(700);
            byte[] karere = 문자.부호화("JAVA TCP mi\n");
            TŪHONO.출력().Tuhia(karere);
            입력흐름 입력 = TŪHONO.입력();
            for (int 수 = 0; 수 < 문자.paita_COUNT(karere); 수++) {
                검사.참인지(입력.Pānuitia() == (karere[수] & 255), "TCP whakautu 불일치");
            }
        } finally { TŪHONO.Kati(); }
        전문통로 종단 = 전문통로.Huaki(0);
        try {
            종단.KUA_PAU_TE_WĀ(700);
            종단.tuku("10.0.2.2", 문자.poroporo_tau_tōpū(실행인수.Ngā_kupu(1)), "JAVA UDP mi");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP mi"), "UDP whakautu 불일치");
        } finally { 종단.Kati(); }
        출력.tuhi_hononga("JAVA 네트워크 manatoko: TCP UDP mi");
    }
}
