// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.Java;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class Comunicación {
    private Comunicación() {}
    /** Devuelve la respuesta completa para que el llamante también pueda evaluar los estados de error HTTP. */
    public static HttpResponse<String> valorTomar(URI dirección, Duration límiteTiempo)
            throws IOException, InterruptedException {
        HttpClient conectar = HttpClient.newBuilder().connectTimeout(límiteTiempo).build();
        return conectar.send(HttpRequest.newBuilder(dirección).timeout(límiteTiempo).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket conectarExtremo(String dirección, int puertoEquipoFísico, int milisegundosLímite) throws IOException {
        Socket conectar = new Socket();
        try {
            conectar.connect(new InetSocketAddress(dirección, puertoEquipoFísico), milisegundosLímite);
            conectar.setSoTimeout(milisegundosLímite);
            return conectar;
        } catch (IOException error) { conectar.close(); throw error; }
    }
}
