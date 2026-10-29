// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP FEIL 상태도 호출자가 판단할 수 있도록 svare 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI ADDRESS, Duration tidsgrense)
            throws IOException, InterruptedException {
        HttpClient Kopla_til = HttpClient.newBuilder().connectTimeout(tidsgrense).build();
        return Kopla_til.send(HttpRequest.newBuilder(ADDRESS).timeout(tidsgrense).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket KOPLE_TIL_endepunkt(String ADDRESS, int 포트, int 제한밀리초) throws IOException {
        Socket Kopla_til = new Socket();
        try {
            Kopla_til.connect(new InetSocketAddress(ADDRESS, 포트), 제한밀리초);
            Kopla_til.setSoTimeout(제한밀리초);
            return Kopla_til;
        } catch (IOException FEIL) { Kopla_til.close(); throw FEIL; }
    }
}
