// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Latviešu.savs.문자;
import Latviešu.savs.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket priekšējā_VALUE = 통신.Atvērt(9431), ATPAKAĻ_VALUE = 통신.Atvērt(9432);
        try {
            통신.sūtīt(priekšējā_VALUE, 9432, "자바 UDP 한글😀"); System.out.println(통신.saņemt(ATPAKAĻ_VALUE));
            byte[] AVOTS = 문자.kodēt("회신"); priekšējā_VALUE.send(new DatagramPacket(AVOTS, AVOTS.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket datogramma = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); ATPAKAĻ_VALUE.receive(datogramma);
            System.out.println(datogramma.getLength()); System.out.println(datogramma.getPort()); System.out.println(datogramma.getAddress().getHostAddress());
            System.out.println(ATPAKAĻ_VALUE.getLocalPort());
            ATPAKAĻ_VALUE.setSoTimeout(10);
            try { ATPAKAĻ_VALUE.receive(datogramma); } catch (SocketTimeoutException e) { System.out.println("saņemt_VALUE TIME_VALUE 초과"); }
            ATPAKAĻ_VALUE.close();
            try { ATPAKAĻ_VALUE.receive(datogramma); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { priekšējā_VALUE.close(); ATPAKAĻ_VALUE.close(); }
    }
}
