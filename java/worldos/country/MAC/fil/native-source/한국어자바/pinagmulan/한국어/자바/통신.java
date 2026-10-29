// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP error 상태도 호출자가 판단할 수 있도록 tumugon 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI email, Duration limitasyon_sa_oras)
            throws IOException, InterruptedException {
        HttpClient CONNECT = HttpClient.newBuilder().connectTimeout(limitasyon_sa_oras).build();
        return CONNECT.send(HttpRequest.newBuilder(email).timeout(limitasyon_sa_oras).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String email, int 포트, int 제한밀리초) throws IOException {
        Socket CONNECT = new Socket();
        try {
            CONNECT.connect(new InetSocketAddress(email, 포트), 제한밀리초);
            CONNECT.setSoTimeout(제한밀리초);
            return CONNECT;
        } catch (IOException error) { CONNECT.close(); throw error; }
    }
}
