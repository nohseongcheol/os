// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class komunikace {
    private komunikace() {}
    /** HTTP chyba 상태도 호출자가 판단할 číslo 있도록 odezva 전체를 반환한다. */
    public static HttpResponse<String> VZÍT_HODNOTA(URI Adresa, Duration časový_limit)
            throws IOException, InterruptedException {
        HttpClient Připojit = HttpClient.newBuilder().connectTimeout(časový_limit).build();
        return Připojit.send(HttpRequest.newBuilder(Adresa).timeout(časový_limit).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket Connect_Endpoint(String Adresa, int hardware_port, int 제한밀리초) throws IOException {
        Socket Připojit = new Socket();
        try {
            Připojit.connect(new InetSocketAddress(Adresa, hardware_port), 제한밀리초);
            Připojit.setSoTimeout(제한밀리초);
            return Připojit;
        } catch (IOException chyba) { Připojit.close(); throw chyba; }
    }
}
