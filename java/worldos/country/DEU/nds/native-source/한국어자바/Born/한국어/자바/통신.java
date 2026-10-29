// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Fehler 상태도 호출자가 판단할 수 있도록 응답 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI 주소, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient Verbinnen = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return Verbinnen.send(HttpRequest.newBuilder(주소).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String 주소, int 포트, int 제한밀리초) throws IOException {
        Socket Verbinnen = new Socket();
        try {
            Verbinnen.connect(new InetSocketAddress(주소, 포트), 제한밀리초);
            Verbinnen.setSoTimeout(제한밀리초);
            return Verbinnen;
        } catch (IOException Fehler) { Verbinnen.close(); throw Fehler; }
    }
}
