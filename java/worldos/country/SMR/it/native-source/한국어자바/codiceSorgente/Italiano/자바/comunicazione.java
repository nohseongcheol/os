// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class comunicazione {
    private comunicazione() {}
    /** HTTP errore 상태도 호출자가 판단할 numero 있도록 replica 전체를 반환한다. */
    public static HttpResponse<String> INCLUDI_VALORE(URI e_mail, Duration limite_di_tempo)
            throws IOException, InterruptedException {
        HttpClient Connetti = HttpClient.newBuilder().connectTimeout(limite_di_tempo).build();
        return Connetti.send(HttpRequest.newBuilder(e_mail).timeout(limite_di_tempo).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket Connect_Endpoint(String e_mail, int hardware_porta, int 제한밀리초) throws IOException {
        Socket Connetti = new Socket();
        try {
            Connetti.connect(new InetSocketAddress(e_mail, hardware_porta), 제한밀리초);
            Connetti.setSoTimeout(제한밀리초);
            return Connetti;
        } catch (IOException errore) { Connetti.close(); throw errore; }
    }
}
