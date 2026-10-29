// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP NAPAKA 상태도 호출자가 판단할 수 있도록 odgovor 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI naslov, Duration omejitev_časa)
            throws IOException, InterruptedException {
        HttpClient Poveži = HttpClient.newBuilder().connectTimeout(omejitev_časa).build();
        return Poveži.send(HttpRequest.newBuilder(naslov).timeout(omejitev_časa).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket POVEŽI_končna_točka(String naslov, int strojna_oprema_vrata, int 제한밀리초) throws IOException {
        Socket Poveži = new Socket();
        try {
            Poveži.connect(new InetSocketAddress(naslov, strojna_oprema_vrata), 제한밀리초);
            Poveži.setSoTimeout(제한밀리초);
            return Poveži;
        } catch (IOException NAPAKA) { Poveži.close(); throw NAPAKA; }
    }
}
