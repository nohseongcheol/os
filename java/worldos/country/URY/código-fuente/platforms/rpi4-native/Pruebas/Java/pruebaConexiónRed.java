// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import español.propio.Caracteres;
import español.propio.Comunicación;
public class pruebaConexiónRed {
    public static void main(String[] args) throws Exception {
        DatagramSocket valorLadoDelantero = Comunicación.abrir(9431), valorLadoPosterior = Comunicación.abrir(9432);
        try {
            Comunicación.enviar(valorLadoDelantero, 9432, "Java UDP 한글😀"); System.out.println(Comunicación.recibir(valorLadoPosterior));
            byte[] fuente = Caracteres.codificar("회신"); valorLadoDelantero.send(new DatagramPacket(fuente, fuente.length, InetAddress.getByName("localhost"), 9432));
            byte[] valorRecibido = new byte[32]; DatagramPacket datagrama = new DatagramPacket(valorRecibido, valorRecibido.length); valorLadoPosterior.receive(datagrama);
            System.out.println(datagrama.getLength()); System.out.println(datagrama.getPort()); System.out.println(datagrama.getAddress().getHostAddress());
            System.out.println(valorLadoPosterior.getLocalPort());
            valorLadoPosterior.setSoTimeout(10);
            try { valorLadoPosterior.receive(datagrama); } catch (SocketTimeoutException e) { System.out.println("recibirValor valorTiempo 초과"); }
            valorLadoPosterior.close();
            try { valorLadoPosterior.receive(datagrama); } catch (java.io.IOException e) { System.out.println("닫힌 Comunicación"); }
        } finally { valorLadoDelantero.close(); valorLadoPosterior.close(); }
    }
}
