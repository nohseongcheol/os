// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP kosa 상태도 호출자가 판단할 수 있도록 jibu 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI anwani, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient UNGANISHA = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return UNGANISHA.send(HttpRequest.newBuilder(anwani).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String anwani, int 포트, int 제한밀리초) throws IOException {
        Socket UNGANISHA = new Socket();
        try {
            UNGANISHA.connect(new InetSocketAddress(anwani, 포트), 제한밀리초);
            UNGANISHA.setSoTimeout(제한밀리초);
            return UNGANISHA;
        } catch (IOException kosa) { UNGANISHA.close(); throw kosa; }
    }
}
