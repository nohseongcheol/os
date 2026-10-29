// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malti.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP żball 상태도 호출자가 판단할 수 있도록 wieġeb 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI ADDRESS, Duration limitu_tal_ħin)
            throws IOException, InterruptedException {
        HttpClient AQBAD = HttpClient.newBuilder().connectTimeout(limitu_tal_ħin).build();
        return AQBAD.send(HttpRequest.newBuilder(ADDRESS).timeout(limitu_tal_ħin).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ADDRESS, int 포트, int 제한밀리초) throws IOException {
        Socket AQBAD = new Socket();
        try {
            AQBAD.connect(new InetSocketAddress(ADDRESS, 포트), 제한밀리초);
            AQBAD.setSoTimeout(제한밀리초);
            return AQBAD;
        } catch (IOException żball) { AQBAD.close(); throw żball; }
    }
}
