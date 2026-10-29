// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Galego.자체.문자;
import Galego.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket frontal_VALOR = 통신.Abrir(9431), ATRÁS_VALOR = 통신.Abrir(9432);
        try {
            통신.enviar(frontal_VALOR, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(ATRÁS_VALOR));
            byte[] FONTE = 문자.부호화("회신"); frontal_VALOR.send(new DatagramPacket(FONTE, FONTE.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECIBIDO_VALOR = new byte[32]; DatagramPacket 전문 = new DatagramPacket(RECIBIDO_VALOR, RECIBIDO_VALOR.length); ATRÁS_VALOR.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(ATRÁS_VALOR.getLocalPort());
            ATRÁS_VALOR.setSoTimeout(10);
            try { ATRÁS_VALOR.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 hora_VALOR 초과"); }
            ATRÁS_VALOR.close();
            try { ATRÁS_VALOR.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { frontal_VALOR.close(); ATRÁS_VALOR.close(); }
    }
}
