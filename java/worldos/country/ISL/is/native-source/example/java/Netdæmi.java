// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Íslenska.eigin.tenging;
import Íslenska.eigin.실행인수;
import Íslenska.eigin.전문통로;
import Íslenska.eigin.문자;
import Íslenska.eigin.úttak;
import Íslenska.eigin.검사;
import Íslenska.eigin.입력흐름;
import Íslenska.eigin.I_Ú_undantekning;

public class Netdæmi {
    public static void Keyra_2() throws I_Ú_undantekning {
        // hýsa: python3 Verkfæri/예제되돌림.py --tcp-port 9000 --udp-port 9001
        tenging Tengjast = tenging.Opna("10.0.2.2", 문자.þátta_heiltala(실행인수.Texti(0)));
        try {
            Tengjast.TIMEOUT(700);
            byte[] skeyti = 문자.부호화("JAVA TCP is\n");
            Tengjast.úttak().Skrift(skeyti);
            입력흐름 입력 = Tengjast.입력();
            for (int númer = 0; númer < 문자.bæti_COUNT(skeyti); númer++) {
                검사.참인지(입력.Lestur() == (skeyti[númer] & 255), "TCP svara 불일치");
            }
        } finally { Tengjast.Loka(); }
        전문통로 endastöð = 전문통로.Opna(0);
        try {
            endastöð.TIMEOUT(700);
            endastöð.senda("10.0.2.2", 문자.þátta_heiltala(실행인수.Texti(1)), "JAVA UDP is");
            검사.참인지(문자.같음(endastöð.받기(), "JAVA UDP is"), "UDP svara 불일치");
        } finally { endastöð.Loka(); }
        úttak.skrifa_lína("JAVA 네트워크 sannprófa: TCP UDP is");
    }
}
