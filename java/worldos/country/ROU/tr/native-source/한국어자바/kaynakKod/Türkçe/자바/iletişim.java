// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class iletişim {
    private iletişim() {}
    /** HTTP hata 상태도 호출자가 판단할 수 있도록 yanıt 전체를 반환한다. */
    public static HttpResponse<String> AL_değer(URI ADRES, Duration süre_sınırı)
            throws IOException, InterruptedException {
        HttpClient Bağlan = HttpClient.newBuilder().connectTimeout(süre_sınırı).build();
        return Bağlan.send(HttpRequest.newBuilder(ADRES).timeout(süre_sınırı).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket Connect_Endpoint(String ADRES, int donanım_taşımak, int 제한밀리초) throws IOException {
        Socket Bağlan = new Socket();
        try {
            Bağlan.connect(new InetSocketAddress(ADRES, donanım_taşımak), 제한밀리초);
            Bağlan.setSoTimeout(제한밀리초);
            return Bağlan;
        } catch (IOException hata) { Bağlan.close(); throw hata; }
    }
}
