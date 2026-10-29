// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP RALAT 상태도 호출자가 판단할 수 있도록 balas 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI e_mel, Duration had_masa)
            throws IOException, InterruptedException {
        HttpClient Sambung = HttpClient.newBuilder().connectTimeout(had_masa).build();
        return Sambung.send(HttpRequest.newBuilder(e_mel).timeout(had_masa).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket CONNECT_peserta(String e_mel, int 포트, int 제한밀리초) throws IOException {
        Socket Sambung = new Socket();
        try {
            Sambung.connect(new InetSocketAddress(e_mel, 포트), 제한밀리초);
            Sambung.setSoTimeout(제한밀리초);
            return Sambung;
        } catch (IOException RALAT) { Sambung.close(); throw RALAT; }
    }
}
