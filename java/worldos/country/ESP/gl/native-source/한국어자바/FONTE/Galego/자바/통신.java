// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP ERRO 상태도 호출자가 판단할 수 있도록 resposta 전체를 반환한다. */
    public static HttpResponse<String> COLLER_VALOR(URI ENDEREZO, Duration límite_de_tempo)
            throws IOException, InterruptedException {
        HttpClient Conectar = HttpClient.newBuilder().connectTimeout(límite_de_tempo).build();
        return Conectar.send(HttpRequest.newBuilder(ENDEREZO).timeout(límite_de_tempo).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket CONECTAR_extremo(String ENDEREZO, int 포트, int 제한밀리초) throws IOException {
        Socket Conectar = new Socket();
        try {
            Conectar.connect(new InetSocketAddress(ENDEREZO, 포트), 제한밀리초);
            Conectar.setSoTimeout(제한밀리초);
            return Conectar;
        } catch (IOException ERRO) { Conectar.close(); throw ERRO; }
    }
}
