// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Euskara.자체.konexio;
import Euskara.자체.실행인수;
import Euskara.자체.전문통로;
import Euskara.자체.문자;
import Euskara.자체.Irteera;
import Euskara.자체.검사;
import Euskara.자체.입력흐름;
import Euskara.자체.S_I_salbuespen;

public class 네트워크예제 {
    public static void Exekutatu_2() throws S_I_salbuespen {
        // Ostalari: python3 Tresnak/예제되돌림.py --tcp-port 9000 --udp-port 9001
        konexio Konektatu = konexio.Ireki("10.0.2.2", 문자.analizatu_osoko_zenbaki(실행인수.Testua(0)));
        try {
            Konektatu.DENBORA_MUGA(700);
            byte[] mezu = 문자.부호화("JAVA TCP eu\n");
            Konektatu.Irteera().Idatzi(mezu);
            입력흐름 입력 = Konektatu.입력();
            for (int 수 = 0; 수 < 문자.byte_ZENBATU(mezu); 수++) {
                검사.참인지(입력.Irakurri() == (mezu[수] & 255), "TCP erantzun 불일치");
            }
        } finally { Konektatu.Itxi(); }
        전문통로 amaiera_puntu = 전문통로.Ireki(0);
        try {
            amaiera_puntu.DENBORA_MUGA(700);
            amaiera_puntu.bidali("10.0.2.2", 문자.analizatu_osoko_zenbaki(실행인수.Testua(1)), "JAVA UDP eu");
            검사.참인지(문자.같음(amaiera_puntu.받기(), "JAVA UDP eu"), "UDP erantzun 불일치");
        } finally { amaiera_puntu.Itxi(); }
        Irteera.idatzi_lerro("JAVA 네트워크 egiaztatu: TCP UDP eu");
    }
}
