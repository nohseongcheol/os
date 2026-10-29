// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Mearachd 상태도 호출자가 판단할 수 있도록 freagair 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI ADDRESS, Duration crìoch_ùine)
            throws IOException, InterruptedException {
        HttpClient CONNECT = HttpClient.newBuilder().connectTimeout(crìoch_ùine).build();
        return CONNECT.send(HttpRequest.newBuilder(ADDRESS).timeout(crìoch_ùine).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ADDRESS, int 포트, int 제한밀리초) throws IOException {
        Socket CONNECT = new Socket();
        try {
            CONNECT.connect(new InetSocketAddress(ADDRESS, 포트), 제한밀리초);
            CONNECT.setSoTimeout(제한밀리초);
            return CONNECT;
        } catch (IOException Mearachd) { CONNECT.close(); throw Mearachd; }
    }
}
