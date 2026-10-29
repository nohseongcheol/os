// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP ERREÁID 상태도 호출자가 판단할 수 있도록 freagair 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI ADDRESS, Duration teorainn_ar_am)
            throws IOException, InterruptedException {
        HttpClient Nasc = HttpClient.newBuilder().connectTimeout(teorainn_ar_am).build();
        return Nasc.send(HttpRequest.newBuilder(ADDRESS).timeout(teorainn_ar_am).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ADDRESS, int 포트, int 제한밀리초) throws IOException {
        Socket Nasc = new Socket();
        try {
            Nasc.connect(new InetSocketAddress(ADDRESS, 포트), 제한밀리초);
            Nasc.setSoTimeout(제한밀리초);
            return Nasc;
        } catch (IOException ERREÁID) { Nasc.close(); throw ERREÁID; }
    }
}
