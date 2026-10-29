// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP تېروتنه 상태도 호출자가 판단할 수 있도록 응답 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI پته, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient نښلېدل = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return نښلېدل.send(HttpRequest.newBuilder(پته).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String پته, int 포트, int 제한밀리초) throws IOException {
        Socket نښلېدل = new Socket();
        try {
            نښلېدل.connect(new InetSocketAddress(پته, 포트), 제한밀리초);
            نښلېدل.setSoTimeout(제한밀리초);
            return نښلېدل;
        } catch (IOException تېروتنه) { نښلېدل.close(); throw تېروتنه; }
    }
}
