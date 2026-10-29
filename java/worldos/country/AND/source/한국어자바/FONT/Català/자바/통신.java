// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP s_ha_produït_un_error 상태도 호출자가 판단할 수 있도록 resposta 전체를 반환한다. */
    public static HttpResponse<String> PREN_VALOR(URI Adreça, Duration límit_de_temps)
            throws IOException, InterruptedException {
        HttpClient Connecta = HttpClient.newBuilder().connectTimeout(límit_de_temps).build();
        return Connecta.send(HttpRequest.newBuilder(Adreça).timeout(límit_de_temps).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket CONNECTA_extrem(String Adreça, int 포트, int 제한밀리초) throws IOException {
        Socket Connecta = new Socket();
        try {
            Connecta.connect(new InetSocketAddress(Adreça, 포트), 제한밀리초);
            Connecta.setSoTimeout(제한밀리초);
            return Connecta;
        } catch (IOException s_ha_produït_un_error) { Connecta.close(); throw s_ha_produït_un_error; }
    }
}
