// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class komunikasi {
    private komunikasi() {}
    /** HTTP galat 상태도 호출자가 판단할 수 있도록 balas 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI surel, Duration batas_waktu)
            throws IOException, InterruptedException {
        HttpClient Sambung = HttpClient.newBuilder().connectTimeout(batas_waktu).build();
        return Sambung.send(HttpRequest.newBuilder(surel).timeout(batas_waktu).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket CONNECT_peserta(String surel, int 포트, int 제한밀리초) throws IOException {
        Socket Sambung = new Socket();
        try {
            Sambung.connect(new InetSocketAddress(surel, 포트), 제한밀리초);
            Sambung.setSoTimeout(제한밀리초);
            return Sambung;
        } catch (IOException galat) { Sambung.close(); throw galat; }
    }
}
