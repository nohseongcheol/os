// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP juumre 상태도 호출자가 판단할 수 있도록 응답 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI ñiiɓirde, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient seŋaade = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return seŋaade.send(HttpRequest.newBuilder(ñiiɓirde).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ñiiɓirde, int 포트, int 제한밀리초) throws IOException {
        Socket seŋaade = new Socket();
        try {
            seŋaade.connect(new InetSocketAddress(ñiiɓirde, 포트), 제한밀리초);
            seŋaade.setSoTimeout(제한밀리초);
            return seŋaade;
        } catch (IOException juumre) { seŋaade.close(); throw juumre; }
    }
}
