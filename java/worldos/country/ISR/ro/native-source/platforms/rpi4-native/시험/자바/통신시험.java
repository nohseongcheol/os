// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Română.propriu.문자;
import Română.propriu.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket frontală_VALUE = 통신.Deschide(9431), ÎNAPOI_VALUE = 통신.Deschide(9432);
        try {
            통신.trimite(frontală_VALUE, 9432, "자바 UDP 한글😀"); System.out.println(통신.primi(ÎNAPOI_VALUE));
            byte[] SURSĂ = 문자.codifica("회신"); frontală_VALUE.send(new DatagramPacket(SURSĂ, SURSĂ.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket diagramă_informații = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); ÎNAPOI_VALUE.receive(diagramă_informații);
            System.out.println(diagramă_informații.getLength()); System.out.println(diagramă_informații.getPort()); System.out.println(diagramă_informații.getAddress().getHostAddress());
            System.out.println(ÎNAPOI_VALUE.getLocalPort());
            ÎNAPOI_VALUE.setSoTimeout(10);
            try { ÎNAPOI_VALUE.receive(diagramă_informații); } catch (SocketTimeoutException e) { System.out.println("primi_VALUE oră_VALUE 초과"); }
            ÎNAPOI_VALUE.close();
            try { ÎNAPOI_VALUE.receive(diagramă_informații); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { frontală_VALUE.close(); ÎNAPOI_VALUE.close(); }
    }
}
