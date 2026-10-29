// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP VIGA 상태도 호출자가 판단할 number 있도록 vastus 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI ADDRESS, Duration ajapiirang)
            throws IOException, InterruptedException {
        HttpClient Ühendu = HttpClient.newBuilder().connectTimeout(ajapiirang).build();
        return Ühendu.send(HttpRequest.newBuilder(ADDRESS).timeout(ajapiirang).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket Ühenda_osaleja(String ADDRESS, int 포트, int 제한밀리초) throws IOException {
        Socket Ühendu = new Socket();
        try {
            Ühendu.connect(new InetSocketAddress(ADDRESS, 포트), 제한밀리초);
            Ühendu.setSoTimeout(제한밀리초);
            return Ühendu;
        } catch (IOException VIGA) { Ühendu.close(); throw VIGA; }
    }
}
