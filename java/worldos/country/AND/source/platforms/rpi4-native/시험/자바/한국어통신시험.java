// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Català.propi.*;

/** 동일 바이트코드를 OpenJDK와 propi JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws E_S_excepció {
        rebre_port port_VALOR = 연결통신.수신열기(0);
        connexió convidat_VALOR = 연결통신.Obre("127.0.0.1", port_VALOR.número_de_port());
        connexió propietari_identificador = port_VALOR.rebre();
        convidat_VALOR.TIMEOUT(200); propietari_identificador.TIMEOUT(200);
        검사.참인지(convidat_VALOR.연결됨() && !convidat_VALOR.닫힘(), "Connecta Estat_VALOR");
        검사.참인지(propietari_identificador.número_de_port() == convidat_VALOR.local_número_de_port(), "homòleg_VALOR número_de_port");
        검사.참인지(convidat_VALOR.número_de_port() == propietari_identificador.local_número_de_port(), "local_Àmbit número_de_port");
        입력흐름 입력 = propietari_identificador.입력(); 출력흐름 출력쪽 = convidat_VALOR.Sortida();
        byte[] correu = 문자.부호화("한글 flux_VALOR");
        출력쪽.Escriptura(correu, 0, correu.length); 출력쪽.내보내기();
        byte[] CANTIDAD_RECIBIDA_SMS = new byte[correu.length];
        int tancar_COMPT = 0;
        while (tancar_COMPT < CANTIDAD_RECIBIDA_SMS.length) {
            int 더읽음 = 입력.Lectura(CANTIDAD_RECIBIDA_SMS, tancar_COMPT, CANTIDAD_RECIBIDA_SMS.length - tancar_COMPT);
            검사.참인지(더읽음 > 0, "예상하지 않은 Fitxer 끝"); tancar_COMPT += 더읽음;
        }
        검사.참인지(문자.같음(문자.desencriptar_dades(CANTIDAD_RECIBIDA_SMS), "한글 flux_VALOR"), "부분 읽기와 Escriptura");
        출력쪽.Escriptura(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Lectura(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "MATRIU_VALOR Lectura");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Lectura();
        검사.참인지(두바이트[1] == 18, "나머지 Lectura");
        propietari_identificador.Sortida().Escriptura(255);
        검사.참인지(convidat_VALOR.입력().Lectura() == 255, "codificació_VALOR 없는 한 byte_VALOR");
        출력쪽.Tanca();
        검사.참인지(convidat_VALOR.닫힘() && 입력.Lectura() == -1, "닫기와 Fitxer 끝");
        입력.Tanca(); 검사.참인지(propietari_identificador.닫힘(), "입력 flux_VALOR Tanca");
        convidat_VALOR.Tanca(); propietari_identificador.Tanca();
        port_VALOR.TIMEOUT(15);
        boolean 시간제한 = false;
        try { port_VALOR.rebre(); } catch (Espera_TIMEOUT_excepció 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "rebre_VALOR TIMEOUT");
        port_VALOR.Tanca(); 검사.참인지(port_VALOR.닫힘(), "rebre_port Tanca");
        전문통로 받는곳 = 전문통로.Obre(0), 보내는곳 = 전문통로.Obre(0);
        받는곳.TIMEOUT(200);
        보내는곳.enviar("127.0.0.1", 받는곳.número_de_port(), "전문 한글");
        검사.참인지(문자.같음(받는곳.rebre(), "전문 한글"), "전문 송수신");
        보내는곳.Tanca(); 받는곳.Tanca();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Tanca");
        Sortida.escriure_línia("Català 통신 verificar: Connecta 전문 flux_VALOR 시간제한 Tanca");
    }
}
