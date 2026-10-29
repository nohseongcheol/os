// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class comunicação {
    private comunicação() {}
    /** HTTP erro 상태도 호출자가 판단할 número 있도록 resposta 전체를 반환한다. */
    public static HttpResponse<String> PEGAR_VALOR(URI Endereço, Duration limite_de_tempo)
            throws IOException, InterruptedException {
        HttpClient Ligar = HttpClient.newBuilder().connectTimeout(limite_de_tempo).build();
        return Ligar.send(HttpRequest.newBuilder(Endereço).timeout(limite_de_tempo).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket Connect_Endpoint(String Endereço, int hardware_porta, int 제한밀리초) throws IOException {
        Socket Ligar = new Socket();
        try {
            Ligar.connect(new InetSocketAddress(Endereço, hardware_porta), 제한밀리초);
            Ligar.setSoTimeout(제한밀리초);
            return Ligar;
        } catch (IOException erro) { Ligar.close(); throw erro; }
    }
}
