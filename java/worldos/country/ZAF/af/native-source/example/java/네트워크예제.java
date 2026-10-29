// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.verbinding;
import 한국어.자체.실행인수;
import 한국어.자체.전문통로;
import 한국어.자체.문자;
import 한국어.자체.Afvoer;
import 한국어.자체.검사;
import 한국어.자체.입력흐름;
import 한국어.자체.I_O_uitsondering;

public class 네트워크예제 {
    public static void Loop() throws I_O_uitsondering {
        // hou: python3 Nutsmiddels/예제되돌림.py --tcp-port 9000 --udp-port 9001
        verbinding Koppel = verbinding.skep("10.0.2.2", 문자.ontleed_heelgetal(실행인수.Teks(0)));
        try {
            Koppel.UITTELLING(700);
            byte[] e_pos_8c783e64 = 문자.부호화("JAVA TCP af\n");
            Koppel.Afvoer().Skryf(e_pos_8c783e64);
            입력흐름 입력 = Koppel.입력();
            for (int 수 = 0; 수 < 문자.greep_COUNT(e_pos_8c783e64); 수++) {
                검사.참인지(입력.Lees() == (e_pos_8c783e64[수] & 255), "TCP antwoord 불일치");
            }
        } finally { Koppel.Sluit(); }
        전문통로 종단 = 전문통로.skep(0);
        try {
            종단.UITTELLING(700);
            종단.e_pos("10.0.2.2", 문자.ontleed_heelgetal(실행인수.Teks(1)), "JAVA UDP af");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP af"), "UDP antwoord 불일치");
        } finally { 종단.Sluit(); }
        Afvoer.skryf_lyn("JAVA 네트워크 verifieer: TCP UDP af");
    }
}
