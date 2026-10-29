// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP chyba 상태도 호출자가 판단할 수 있도록 odozva 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI adresa, Duration časový_limit)
            throws IOException, InterruptedException {
        HttpClient Pripojiť = HttpClient.newBuilder().connectTimeout(časový_limit).build();
        return Pripojiť.send(HttpRequest.newBuilder(adresa).timeout(časový_limit).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket spojiť_účastník(String adresa, int hardvér_port, int 제한밀리초) throws IOException {
        Socket Pripojiť = new Socket();
        try {
            Pripojiť.connect(new InetSocketAddress(adresa, hardvér_port), 제한밀리초);
            Pripojiť.setSoTimeout(제한밀리초);
            return Pripojiť;
        } catch (IOException chyba) { Pripojiť.close(); throw chyba; }
    }
}
