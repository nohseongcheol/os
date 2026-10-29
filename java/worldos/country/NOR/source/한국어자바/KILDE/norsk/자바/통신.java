// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP feil 상태도 호출자가 판단할 nummer 있도록 svar 전체를 반환한다. */
    public static HttpResponse<String> TA_VERDI(URI e_post, Duration tidsgrense)
            throws IOException, InterruptedException {
        HttpClient Koble_til = HttpClient.newBuilder().connectTimeout(tidsgrense).build();
        return Koble_til.send(HttpRequest.newBuilder(e_post).timeout(tidsgrense).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket KOBLE_TIL_deltaker(String e_post, int maskinvare_port, int 제한밀리초) throws IOException {
        Socket Koble_til = new Socket();
        try {
            Koble_til.connect(new InetSocketAddress(e_post, maskinvare_port), 제한밀리초);
            Koble_til.setSoTimeout(제한밀리초);
            return Koble_til;
        } catch (IOException feil) { Koble_til.close(); throw feil; }
    }
}
