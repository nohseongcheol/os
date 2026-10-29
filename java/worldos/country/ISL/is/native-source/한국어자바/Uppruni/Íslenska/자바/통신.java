// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Villa 상태도 호출자가 판단할 númer 있도록 svara 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI slóð, Duration tímamörk)
            throws IOException, InterruptedException {
        HttpClient Tengjast = HttpClient.newBuilder().connectTimeout(tímamörk).build();
        return Tengjast.send(HttpRequest.newBuilder(slóð).timeout(tímamörk).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket TENGJA_endastöð(String slóð, int 포트, int 제한밀리초) throws IOException {
        Socket Tengjast = new Socket();
        try {
            Tengjast.connect(new InetSocketAddress(slóð, 포트), 제한밀리초);
            Tengjast.setSoTimeout(제한밀리초);
            return Tengjast;
        } catch (IOException Villa) { Tengjast.close(); throw Villa; }
    }
}
