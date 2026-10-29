// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP ГРЕШКА 상태도 호출자가 판단할 수 있도록 одговори 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI адреса, Duration временско_ограничување)
            throws IOException, InterruptedException {
        HttpClient Врзи_се = HttpClient.newBuilder().connectTimeout(временско_ограничување).build();
        return Врзи_се.send(HttpRequest.newBuilder(адреса).timeout(временско_ограничување).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String адреса, int 포트, int 제한밀리초) throws IOException {
        Socket Врзи_се = new Socket();
        try {
            Врзи_се.connect(new InetSocketAddress(адреса, 포트), 제한밀리초);
            Врзи_се.setSoTimeout(제한밀리초);
            return Врзи_се;
        } catch (IOException ГРЕШКА) { Врзи_се.close(); throw ГРЕШКА; }
    }
}
