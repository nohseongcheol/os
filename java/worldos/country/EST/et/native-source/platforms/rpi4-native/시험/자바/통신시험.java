// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Eesti.oma.문자;
import Eesti.oma.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket esikaamera_VALUE = 통신.Ava(9431), Tagasi_VALUE = 통신.Ava(9432);
        try {
            통신.saatma(esikaamera_VALUE, 9432, "자바 UDP 한글😀"); System.out.println(통신.saama(Tagasi_VALUE));
            byte[] ALLIKAS = 문자.kodeerima("회신"); esikaamera_VALUE.send(new DatagramPacket(ALLIKAS, ALLIKAS.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket datagramm = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); Tagasi_VALUE.receive(datagramm);
            System.out.println(datagramm.getLength()); System.out.println(datagramm.getPort()); System.out.println(datagramm.getAddress().getHostAddress());
            System.out.println(Tagasi_VALUE.getLocalPort());
            Tagasi_VALUE.setSoTimeout(10);
            try { Tagasi_VALUE.receive(datagramm); } catch (SocketTimeoutException e) { System.out.println("saama_VALUE Aeg_VALUE 초과"); }
            Tagasi_VALUE.close();
            try { Tagasi_VALUE.receive(datagramm); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { esikaamera_VALUE.close(); Tagasi_VALUE.close(); }
    }
}
