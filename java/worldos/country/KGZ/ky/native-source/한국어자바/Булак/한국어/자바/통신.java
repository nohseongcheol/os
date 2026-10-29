// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Ката 상태도 호출자가 판단할 수 있도록 жооп_берүү 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI дарек, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient Туташуу = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return Туташуу.send(HttpRequest.newBuilder(дарек).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String дарек, int 포트, int 제한밀리초) throws IOException {
        Socket Туташуу = new Socket();
        try {
            Туташуу.connect(new InetSocketAddress(дарек, 포트), 제한밀리초);
            Туташуу.setSoTimeout(제한밀리초);
            return Туташуу;
        } catch (IOException Ката) { Туташуу.close(); throw Ката; }
    }
}
