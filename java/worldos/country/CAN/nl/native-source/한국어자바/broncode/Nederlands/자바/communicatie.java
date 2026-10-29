// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class communicatie {
    private communicatie() {}
    /** HTTP fout 상태도 호출자가 판단할 nummer 있도록 reactie 전체를 반환한다. */
    public static HttpResponse<String> NEMEN_WAARDE(URI ADRES, Duration tijdslimiet)
            throws IOException, InterruptedException {
        HttpClient Verbinden = HttpClient.newBuilder().connectTimeout(tijdslimiet).build();
        return Verbinden.send(HttpRequest.newBuilder(ADRES).timeout(tijdslimiet).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket Connect_Endpoint(String ADRES, int hardware_poort, int 제한밀리초) throws IOException {
        Socket Verbinden = new Socket();
        try {
            Verbinden.connect(new InetSocketAddress(ADRES, hardware_poort), 제한밀리초);
            Verbinden.setSoTimeout(제한밀리초);
            return Verbinden;
        } catch (IOException fout) { Verbinden.close(); throw fout; }
    }
}
