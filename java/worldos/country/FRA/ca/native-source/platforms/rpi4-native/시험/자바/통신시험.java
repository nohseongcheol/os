// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Català.propi.문자;
import Català.propi.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket frontal_VALOR = 통신.Obre(9431), ENRERE_VALOR = 통신.Obre(9432);
        try {
            통신.enviar(frontal_VALOR, 9432, "자바 UDP 한글😀"); System.out.println(통신.rebre(ENRERE_VALOR));
            byte[] FONT = 문자.부호화("회신"); frontal_VALOR.send(new DatagramPacket(FONT, FONT.length, InetAddress.getByName("localhost"), 9432));
            byte[] CANTIDAD_RECIBIDA_VALOR = new byte[32]; DatagramPacket 전문 = new DatagramPacket(CANTIDAD_RECIBIDA_VALOR, CANTIDAD_RECIBIDA_VALOR.length); ENRERE_VALOR.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(ENRERE_VALOR.getLocalPort());
            ENRERE_VALOR.setSoTimeout(10);
            try { ENRERE_VALOR.receive(전문); } catch (SocketTimeoutException e) { System.out.println("rebre_VALOR Hora_VALOR 초과"); }
            ENRERE_VALOR.close();
            try { ENRERE_VALOR.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { frontal_VALOR.close(); ENRERE_VALOR.close(); }
    }
}
