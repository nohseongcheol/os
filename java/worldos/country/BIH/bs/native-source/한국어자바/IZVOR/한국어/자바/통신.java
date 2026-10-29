// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP GRESKA 상태도 호출자가 판단할 수 있도록 odgovoriti 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI adresa, Duration ograničenje_vremena_provedenog_za_ekranom)
            throws IOException, InterruptedException {
        HttpClient Spoji_se = HttpClient.newBuilder().connectTimeout(ograničenje_vremena_provedenog_za_ekranom).build();
        return Spoji_se.send(HttpRequest.newBuilder(adresa).timeout(ograničenje_vremena_provedenog_za_ekranom).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket povezati_završna_tačka(String adresa, int hardver_port, int 제한밀리초) throws IOException {
        Socket Spoji_se = new Socket();
        try {
            Spoji_se.connect(new InetSocketAddress(adresa, hardver_port), 제한밀리초);
            Spoji_se.setSoTimeout(제한밀리초);
            return Spoji_se;
        } catch (IOException GRESKA) { Spoji_se.close(); throw GRESKA; }
    }
}
