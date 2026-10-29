// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP greška 상태도 호출자가 판단할 수 있도록 odgovor 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI adresa, Duration vremensko_ograničenje)
            throws IOException, InterruptedException {
        HttpClient veze = HttpClient.newBuilder().connectTimeout(vremensko_ograničenje).build();
        return veze.send(HttpRequest.newBuilder(adresa).timeout(vremensko_ograničenje).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket veze_učesnik(String adresa, int 포트, int 제한밀리초) throws IOException {
        Socket veze = new Socket();
        try {
            veze.connect(new InetSocketAddress(adresa, 포트), 제한밀리초);
            veze.setSoTimeout(제한밀리초);
            return veze;
        } catch (IOException greška) { veze.close(); throw greška; }
    }
}
