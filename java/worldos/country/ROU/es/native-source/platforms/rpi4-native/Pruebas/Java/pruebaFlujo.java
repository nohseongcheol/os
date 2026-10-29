// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class pruebaFlujo {
    public static void main(String[] args) throws Exception {
        ServerSocket valorServidor = new ServerSocket(9250);
        Socket valorInvitado = new Socket("localhost", 9250);
        Socket conectar = valorServidor.accept();
        if (conectar.getPort() != valorInvitado.getLocalPort() || valorInvitado.getPort() != conectar.getLocalPort()) throw new RuntimeException("valorPuerto 불일치");
        byte[] datagrama = "한글 valorFlujo".getBytes("UTF-8");
        valorInvitado.getOutputStream().write(datagrama);
        byte[] elementoListaRecibido = new byte[100];
        int longitud = conectar.getInputStream().read(elementoListaRecibido, 0, elementoListaRecibido.length);
        System.out.println(longitud == datagrama.length);
        for (int i = 0; i < longitud; i++) if (elementoListaRecibido[i] != datagrama[i]) throw new RuntimeException("valorContenidoValor 불일치");
        conectar.getOutputStream().write(42);
        System.out.println(valorInvitado.getInputStream().read());
        valorInvitado.close();
        System.out.println(conectar.getInputStream().read());
        conectar.close(); valorServidor.close();
        ServerSocket servidorVacíoEstado = new ServerSocket(9250);
        servidorVacíoEstado.setSoTimeout(10);
        try { servidorVacíoEstado.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("valorTiempo valorLímite"); }
        servidorVacíoEstado.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS esNoAdmitido"); }
        System.out.println("STREAM PASS");
    }
}
