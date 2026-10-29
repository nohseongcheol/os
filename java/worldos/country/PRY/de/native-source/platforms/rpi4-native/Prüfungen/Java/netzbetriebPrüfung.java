// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Deutsch.eigen.Zeichen;
import Deutsch.eigen.Kommunikation;
public class netzbetriebPrüfung {
    public static void main(String[] args) throws Exception {
        DatagramSocket vorderseiteWert = Kommunikation.öffnen(9431), rückseiteWert = Kommunikation.öffnen(9432);
        try {
            Kommunikation.senden(vorderseiteWert, 9432, "Java UDP 한글😀"); System.out.println(Kommunikation.empfangen(rückseiteWert));
            byte[] Quelltext = Zeichen.kodieren("회신"); vorderseiteWert.send(new DatagramPacket(Quelltext, Quelltext.length, InetAddress.getByName("localhost"), 9432));
            byte[] empfangenWertWert = new byte[32]; DatagramPacket datagramm = new DatagramPacket(empfangenWertWert, empfangenWertWert.length); rückseiteWert.receive(datagramm);
            System.out.println(datagramm.getLength()); System.out.println(datagramm.getPort()); System.out.println(datagramm.getAddress().getHostAddress());
            System.out.println(rückseiteWert.getLocalPort());
            rückseiteWert.setSoTimeout(10);
            try { rückseiteWert.receive(datagramm); } catch (SocketTimeoutException e) { System.out.println("wertEmpfangen zeitWert 초과"); }
            rückseiteWert.close();
            try { rückseiteWert.receive(datagramm); } catch (java.io.IOException e) { System.out.println("닫힌 Kommunikation"); }
        } finally { vorderseiteWert.close(); rückseiteWert.close(); }
    }
}
