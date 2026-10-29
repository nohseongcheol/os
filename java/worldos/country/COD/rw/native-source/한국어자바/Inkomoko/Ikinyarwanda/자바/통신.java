// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ikinyarwanda.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP IKOSA 상태도 호출자가 판단할 수 있도록 gusubiza 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI aderesi, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient Guhuza = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return Guhuza.send(HttpRequest.newBuilder(aderesi).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String aderesi, int 포트, int 제한밀리초) throws IOException {
        Socket Guhuza = new Socket();
        try {
            Guhuza.connect(new InetSocketAddress(aderesi, 포트), 제한밀리초);
            Guhuza.setSoTimeout(제한밀리초);
            return Guhuza;
        } catch (IOException IKOSA) { Guhuza.close(); throw IKOSA; }
    }
}
