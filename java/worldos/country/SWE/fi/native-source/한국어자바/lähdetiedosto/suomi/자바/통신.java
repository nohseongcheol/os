// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP VIRHE 상태도 호출자가 판단할 numero 있도록 palaute 전체를 반환한다. */
    public static HttpResponse<String> OTA_ARVO(URI OSOITE, Duration aikaraja)
            throws IOException, InterruptedException {
        HttpClient Yhdistä = HttpClient.newBuilder().connectTimeout(aikaraja).build();
        return Yhdistä.send(HttpRequest.newBuilder(OSOITE).timeout(aikaraja).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket YHDISTÄ_päätepiste(String OSOITE, int laitteisto_portti, int 제한밀리초) throws IOException {
        Socket Yhdistä = new Socket();
        try {
            Yhdistä.connect(new InetSocketAddress(OSOITE, laitteisto_portti), 제한밀리초);
            Yhdistä.setSoTimeout(제한밀리초);
            return Yhdistä;
        } catch (IOException VIRHE) { Yhdistä.close(); throw VIRHE; }
    }
}
