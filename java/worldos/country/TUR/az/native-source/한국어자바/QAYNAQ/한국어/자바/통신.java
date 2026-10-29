// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP XƏTA 상태도 호출자가 판단할 수 있도록 cavab 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI ünvan, Duration vaxt_limiti)
            throws IOException, InterruptedException {
        HttpClient Bağlan = HttpClient.newBuilder().connectTimeout(vaxt_limiti).build();
        return Bağlan.send(HttpRequest.newBuilder(ünvan).timeout(vaxt_limiti).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ünvan, int 포트, int 제한밀리초) throws IOException {
        Socket Bağlan = new Socket();
        try {
            Bağlan.connect(new InetSocketAddress(ünvan, 포트), 제한밀리초);
            Bağlan.setSoTimeout(제한밀리초);
            return Bağlan;
        } catch (IOException XƏTA) { Bağlan.close(); throw XƏTA; }
    }
}
