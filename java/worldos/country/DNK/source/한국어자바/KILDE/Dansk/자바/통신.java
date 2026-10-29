// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP fejl 상태도 호출자가 판단할 tal 있도록 svar 전체를 반환한다. */
    public static HttpResponse<String> TAG_VÆRDI(URI mail, Duration tidsbegrænsning)
            throws IOException, InterruptedException {
        HttpClient Tilslut = HttpClient.newBuilder().connectTimeout(tidsbegrænsning).build();
        return Tilslut.send(HttpRequest.newBuilder(mail).timeout(tidsbegrænsning).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket Forbind_slutpunkt(String mail, int hardware_port, int 제한밀리초) throws IOException {
        Socket Tilslut = new Socket();
        try {
            Tilslut.connect(new InetSocketAddress(mail, hardware_port), 제한밀리초);
            Tilslut.setSoTimeout(제한밀리초);
            return Tilslut;
        } catch (IOException fejl) { Tilslut.close(); throw fejl; }
    }
}
