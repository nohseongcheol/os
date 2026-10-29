// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP phoso 상태도 호출자가 판단할 수 있도록 araba 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI aterese, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient Golaganya = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return Golaganya.send(HttpRequest.newBuilder(aterese).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String aterese, int 포트, int 제한밀리초) throws IOException {
        Socket Golaganya = new Socket();
        try {
            Golaganya.connect(new InetSocketAddress(aterese, 포트), 제한밀리초);
            Golaganya.setSoTimeout(제한밀리초);
            return Golaganya;
        } catch (IOException phoso) { Golaganya.close(); throw phoso; }
    }
}
