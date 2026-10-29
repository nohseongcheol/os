// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Svenska.eget.문자;
import Svenska.eget.kommunikation;
public class test_Nätverk {
    public static void main(String[] args) throws Exception {
        DatagramSocket framåtvänd_värde = kommunikation.Öppna(9431), BACK_värde = kommunikation.Öppna(9432);
        try {
            kommunikation.skicka(framåtvänd_värde, 9432, "자바 UDP 한글😀"); System.out.println(kommunikation.få(BACK_värde));
            byte[] källfil = 문자.koda("회신"); framåtvänd_värde.send(new DatagramPacket(källfil, källfil.length, InetAddress.getByName("localhost"), 9432));
            byte[] BELOPP_värde = new byte[32]; DatagramPacket datagram = new DatagramPacket(BELOPP_värde, BELOPP_värde.length); BACK_värde.receive(datagram);
            System.out.println(datagram.getLength()); System.out.println(datagram.getPort()); System.out.println(datagram.getAddress().getHostAddress());
            System.out.println(BACK_värde.getLocalPort());
            BACK_värde.setSoTimeout(10);
            try { BACK_värde.receive(datagram); } catch (SocketTimeoutException e) { System.out.println("få_värde tid_värde 초과"); }
            BACK_värde.close();
            try { BACK_värde.receive(datagram); } catch (java.io.IOException e) { System.out.println("닫힌 kommunikation"); }
        } finally { framåtvänd_värde.close(); BACK_värde.close(); }
    }
}
