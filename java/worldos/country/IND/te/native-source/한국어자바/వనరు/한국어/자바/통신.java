// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP దోషం 상태도 호출자가 판단할 수 있도록 ప్రత్యుత్తరం_ఇవ్వు 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI ఇమెయిల్, Duration సమయ_పరిమితి)
            throws IOException, InterruptedException {
        HttpClient కనెక్టుచేయి = HttpClient.newBuilder().connectTimeout(సమయ_పరిమితి).build();
        return కనెక్టుచేయి.send(HttpRequest.newBuilder(ఇమెయిల్).timeout(సమయ_పరిమితి).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ఇమెయిల్, int 포트, int 제한밀리초) throws IOException {
        Socket కనెక్టుచేయి = new Socket();
        try {
            కనెక్టుచేయి.connect(new InetSocketAddress(ఇమెయిల్, 포트), 제한밀리초);
            కనెక్టుచేయి.setSoTimeout(제한밀리초);
            return కనెక్టుచేయి;
        } catch (IOException దోషం) { కనెక్టుచేయి.close(); throw దోషం; }
    }
}
