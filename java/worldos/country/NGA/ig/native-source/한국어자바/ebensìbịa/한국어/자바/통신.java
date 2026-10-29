// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP mmejọ 상태도 호출자가 판단할 수 있도록 nzaghachi 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI àdreèsì, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient Banye = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return Banye.send(HttpRequest.newBuilder(àdreèsì).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String àdreèsì, int ngwaike_pọọt, int 제한밀리초) throws IOException {
        Socket Banye = new Socket();
        try {
            Banye.connect(new InetSocketAddress(àdreèsì, ngwaike_pọọt), 제한밀리초);
            Banye.setSoTimeout(제한밀리초);
            return Banye;
        } catch (IOException mmejọ) { Banye.close(); throw mmejọ; }
    }
}
