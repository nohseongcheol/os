// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import isiXhosa.자체.uqhagamshelo;
import isiXhosa.자체.실행인수;
import isiXhosa.자체.전문통로;
import isiXhosa.자체.문자;
import isiXhosa.자체.출력;
import isiXhosa.자체.검사;
import isiXhosa.자체.입력흐름;
import isiXhosa.자체.입출력예외;

public class 네트워크예제 {
    public static void Phumeza() throws 입출력예외 {
        // umsingathi: python3 Izixhobo/예제되돌림.py --tcp-port 9000 --udp-port 9001
        uqhagamshelo Nxulumanisa = uqhagamshelo.Vula("10.0.2.2", 문자.ingcaciso_yegama_inani_elipheleleyo(실행인수.Umbhalo(0)));
        try {
            Nxulumanisa.대기시간(700);
            byte[] umyalezo = 문자.부호화("JAVA TCP xh\n");
            Nxulumanisa.출력().Bhala(umyalezo);
            입력흐름 입력 = Nxulumanisa.입력();
            for (int 수 = 0; 수 < 문자.바이트수(umyalezo); 수++) {
                검사.참인지(입력.Funda() == (umyalezo[수] & 255), "TCP phendula 불일치");
            }
        } finally { Nxulumanisa.Vala(); }
        전문통로 종단 = 전문통로.Vula(0);
        try {
            종단.대기시간(700);
            종단.thumela("10.0.2.2", 문자.ingcaciso_yegama_inani_elipheleleyo(실행인수.Umbhalo(1)), "JAVA UDP xh");
            검사.참인지(문자.같음(종단.받기(), "JAVA UDP xh"), "UDP phendula 불일치");
        } finally { 종단.Vala(); }
        출력.bhala_umgca("JAVA 네트워크 ngqinisisa: TCP UDP xh");
    }
}
