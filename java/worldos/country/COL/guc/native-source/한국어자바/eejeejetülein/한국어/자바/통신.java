// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP ajachitia 상태도 호출자가 판단할 수 있도록 응답 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI ejepüsee, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient a_ataa = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return a_ataa.send(HttpRequest.newBuilder(ejepüsee).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ejepüsee, int 포트, int 제한밀리초) throws IOException {
        Socket a_ataa = new Socket();
        try {
            a_ataa.connect(new InetSocketAddress(ejepüsee, 포트), 제한밀리초);
            a_ataa.setSoTimeout(제한밀리초);
            return a_ataa;
        } catch (IOException ajachitia) { a_ataa.close(); throw ajachitia; }
    }
}
