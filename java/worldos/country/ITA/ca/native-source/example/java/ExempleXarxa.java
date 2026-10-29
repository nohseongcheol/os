// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Català.propi.connexió;
import Català.propi.실행인수;
import Català.propi.전문통로;
import Català.propi.문자;
import Català.propi.Sortida;
import Català.propi.검사;
import Català.propi.입력흐름;
import Català.propi.E_S_excepció;

public class ExempleXarxa {
    public static void Executa_2() throws E_S_excepció {
        // allotjar: python3 Eines/예제되돌림.py --tcp-port 9000 --udp-port 9001
        connexió Connecta = connexió.Obre("10.0.2.2", 문자.정수읽기(실행인수.SMS(0)));
        try {
            Connecta.TIMEOUT(700);
            byte[] correu = 문자.부호화("JAVA TCP ca\n");
            Connecta.Sortida().Escriptura(correu);
            입력흐름 입력 = Connecta.입력();
            for (int 수 = 0; 수 < 문자.byte_COMPT(correu); 수++) {
                검사.참인지(입력.Lectura() == (correu[수] & 255), "TCP resposta 불일치");
            }
        } finally { Connecta.Tanca(); }
        전문통로 extrem = 전문통로.Obre(0);
        try {
            extrem.TIMEOUT(700);
            extrem.enviar("10.0.2.2", 문자.정수읽기(실행인수.SMS(1)), "JAVA UDP ca");
            검사.참인지(문자.같음(extrem.rebre(), "JAVA UDP ca"), "UDP resposta 불일치");
        } finally { extrem.Tanca(); }
        Sortida.escriure_línia("JAVA 네트워크 verificar: TCP UDP ca");
    }
}
