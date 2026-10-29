// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP GREŠKA 상태도 호출자가 판단할 수 있도록 odgovor 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI adresa, Duration vremensko_ograničenje)
            throws IOException, InterruptedException {
        HttpClient Spoji_se = HttpClient.newBuilder().connectTimeout(vremensko_ograničenje).build();
        return Spoji_se.send(HttpRequest.newBuilder(adresa).timeout(vremensko_ograničenje).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket CONNECT_sudionik(String adresa, int 포트, int 제한밀리초) throws IOException {
        Socket Spoji_se = new Socket();
        try {
            Spoji_se.connect(new InetSocketAddress(adresa, 포트), 제한밀리초);
            Spoji_se.setSoTimeout(제한밀리초);
            return Spoji_se;
        } catch (IOException GREŠKA) { Spoji_se.close(); throw GREŠKA; }
    }
}
