// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Hata 상태도 호출자가 판단할 수 있도록 jogap_bermek 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI salgy, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient Birikme = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return Birikme.send(HttpRequest.newBuilder(salgy).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String salgy, int 포트, int 제한밀리초) throws IOException {
        Socket Birikme = new Socket();
        try {
            Birikme.connect(new InetSocketAddress(salgy, 포트), 제한밀리초);
            Birikme.setSoTimeout(제한밀리초);
            return Birikme;
        } catch (IOException Hata) { Birikme.close(); throw Hata; }
    }
}
