// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Fout 상태도 호출자가 판단할 수 있도록 antwoord 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI adres, Duration tydlimiet)
            throws IOException, InterruptedException {
        HttpClient Koppel = HttpClient.newBuilder().connectTimeout(tydlimiet).build();
        return Koppel.send(HttpRequest.newBuilder(adres).timeout(tydlimiet).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String adres, int hardeware_ombou, int 제한밀리초) throws IOException {
        Socket Koppel = new Socket();
        try {
            Koppel.connect(new InetSocketAddress(adres, hardeware_ombou), 제한밀리초);
            Koppel.setSoTimeout(제한밀리초);
            return Koppel;
        } catch (IOException Fout) { Koppel.close(); throw Fout; }
    }
}
