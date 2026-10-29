// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Português.nativo.문자;
import Português.nativo.comunicação;
public class teste_Rede {
    public static void main(String[] args) throws Exception {
        DatagramSocket câmera_frontal_VALOR = comunicação.Abrir(9431), BACK_VALOR = comunicação.Abrir(9432);
        try {
            comunicação.enviar(câmera_frontal_VALOR, 9432, "자바 UDP 한글😀"); System.out.println(comunicação.receber(BACK_VALOR));
            byte[] códigoFonte = 문자.codificar("회신"); câmera_frontal_VALOR.send(new DatagramPacket(códigoFonte, códigoFonte.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEBER_VALOR = new byte[32]; DatagramPacket datagrama = new DatagramPacket(RECEBER_VALOR, RECEBER_VALOR.length); BACK_VALOR.receive(datagrama);
            System.out.println(datagrama.getLength()); System.out.println(datagrama.getPort()); System.out.println(datagrama.getAddress().getHostAddress());
            System.out.println(BACK_VALOR.getLocalPort());
            BACK_VALOR.setSoTimeout(10);
            try { BACK_VALOR.receive(datagrama); } catch (SocketTimeoutException e) { System.out.println("receber_VALOR valor_temporal 초과"); }
            BACK_VALOR.close();
            try { BACK_VALOR.receive(datagrama); } catch (java.io.IOException e) { System.out.println("닫힌 comunicação"); }
        } finally { câmera_frontal_VALOR.close(); BACK_VALOR.close(); }
    }
}
