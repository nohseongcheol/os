// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Slovenský.vlastné.문자;
import Slovenský.vlastné.통신;
public class test_Siete {
    public static void main(String[] args) throws Exception {
        DatagramSocket predný_VALUE = 통신.Otvoriť(9431), BACK_VALUE = 통신.Otvoriť(9432);
        try {
            통신.odoslať(predný_VALUE, 9432, "자바 UDP 한글😀"); System.out.println(통신.dostať(BACK_VALUE));
            byte[] ZDROJ = 문자.kódovať("회신"); predný_VALUE.send(new DatagramPacket(ZDROJ, ZDROJ.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket datagram = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); BACK_VALUE.receive(datagram);
            System.out.println(datagram.getLength()); System.out.println(datagram.getPort()); System.out.println(datagram.getAddress().getHostAddress());
            System.out.println(BACK_VALUE.getLocalPort());
            BACK_VALUE.setSoTimeout(10);
            try { BACK_VALUE.receive(datagram); } catch (SocketTimeoutException e) { System.out.println("dostať_VALUE čas_VALUE 초과"); }
            BACK_VALUE.close();
            try { BACK_VALUE.receive(datagram); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { predný_VALUE.close(); BACK_VALUE.close(); }
    }
}
