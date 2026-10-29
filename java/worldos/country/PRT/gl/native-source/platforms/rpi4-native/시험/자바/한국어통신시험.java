// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Galego.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] Argumentos) throws E_S_excepción {
        수신창구 porto_VALOR = 연결통신.수신열기(0);
        conexión convidado_VALOR = 연결통신.Abrir("127.0.0.1", porto_VALOR.número_do_porto());
        conexión 주인 = porto_VALOR.받기();
        convidado_VALOR.TIMEOUT(200); 주인.TIMEOUT(200);
        검사.참인지(convidado_VALOR.연결됨() && !convidado_VALOR.닫힘(), "Conectar Estado_VALOR");
        검사.참인지(주인.número_do_porto() == convidado_VALOR.local_número_do_porto(), "punto_VALOR número_do_porto");
        검사.참인지(convidado_VALOR.número_do_porto() == 주인.local_número_do_porto(), "local_Ámbito número_do_porto");
        입력흐름 입력 = 주인.입력(); 출력흐름 출력쪽 = convidado_VALOR.Saída();
        byte[] correo = 문자.부호화("한글 fluxo_VALOR");
        출력쪽.Escritura(correo, 0, correo.length); 출력쪽.내보내기();
        byte[] RECIBIDO_SMS = new byte[correo.length];
        int 읽은수 = 0;
        while (읽은수 < RECIBIDO_SMS.length) {
            int 더읽음 = 입력.Lectura(RECIBIDO_SMS, 읽은수, RECIBIDO_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Ficheiro 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.descifrar_datos(RECIBIDO_SMS), "한글 fluxo_VALOR"), "부분 읽기와 Escritura");
        출력쪽.Escritura(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Lectura(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "MATRIZ_VALOR Lectura");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Lectura();
        검사.참인지(두바이트[1] == 18, "나머지 Lectura");
        주인.Saída().Escritura(255);
        검사.참인지(convidado_VALOR.입력().Lectura() == 255, "codificación_VALOR 없는 한 byte_VALOR");
        출력쪽.Pechar();
        검사.참인지(convidado_VALOR.닫힘() && 입력.Lectura() == -1, "닫기와 Ficheiro 끝");
        입력.Pechar(); 검사.참인지(주인.닫힘(), "입력 fluxo_VALOR Pechar");
        convidado_VALOR.Pechar(); 주인.Pechar();
        porto_VALOR.TIMEOUT(15);
        boolean 시간제한 = false;
        try { porto_VALOR.받기(); } catch (agarda_TIMEOUT_excepción 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 TIMEOUT");
        porto_VALOR.Pechar(); 검사.참인지(porto_VALOR.닫힘(), "수신창구 Pechar");
        전문통로 받는곳 = 전문통로.Abrir(0), 보내는곳 = 전문통로.Abrir(0);
        받는곳.TIMEOUT(200);
        보내는곳.enviar("127.0.0.1", 받는곳.número_do_porto(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Pechar(); 받는곳.Pechar();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Pechar");
        Saída.escribir_liña("Galego 통신 verificar: Conectar 전문 fluxo_VALOR 시간제한 Pechar");
    }
}
