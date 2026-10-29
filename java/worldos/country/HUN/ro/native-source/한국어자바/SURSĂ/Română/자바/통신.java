// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP eroare 상태도 호출자가 판단할 수 있도록 replică 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI adresa, Duration limită_de_timp)
            throws IOException, InterruptedException {
        HttpClient Conectează = HttpClient.newBuilder().connectTimeout(limită_de_timp).build();
        return Conectează.send(HttpRequest.newBuilder(adresa).timeout(limită_de_timp).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket conecta_participant(String adresa, int 포트, int 제한밀리초) throws IOException {
        Socket Conectează = new Socket();
        try {
            Conectează.connect(new InetSocketAddress(adresa, 포트), 제한밀리초);
            Conectează.setSoTimeout(제한밀리초);
            return Conectează;
        } catch (IOException eroare) { Conectează.close(); throw eroare; }
    }
}
