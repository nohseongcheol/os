// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import hrvatski.vlastiti.문자;
import hrvatski.vlastiti.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket prednja_VALUE = 통신.Otvori(9431), TRAG_VALUE = 통신.Otvori(9432);
        try {
            통신.slati(prednja_VALUE, 9432, "자바 UDP 한글😀"); System.out.println(통신.primiti(TRAG_VALUE));
            byte[] IZVOR = 문자.kodirati("회신"); prednja_VALUE.send(new DatagramPacket(IZVOR, IZVOR.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket datogram = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); TRAG_VALUE.receive(datogram);
            System.out.println(datogram.getLength()); System.out.println(datogram.getPort()); System.out.println(datogram.getAddress().getHostAddress());
            System.out.println(TRAG_VALUE.getLocalPort());
            TRAG_VALUE.setSoTimeout(10);
            try { TRAG_VALUE.receive(datogram); } catch (SocketTimeoutException e) { System.out.println("primiti_VALUE TIME_VALUE 초과"); }
            TRAG_VALUE.close();
            try { TRAG_VALUE.receive(datogram); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { prednja_VALUE.close(); TRAG_VALUE.close(); }
    }
}
