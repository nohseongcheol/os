// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP errorea 상태도 호출자가 판단할 수 있도록 erantzun 전체를 반환한다. */
    public static HttpResponse<String> HARTU_balio(URI helbide, Duration denbora_muga)
            throws IOException, InterruptedException {
        HttpClient Konektatu = HttpClient.newBuilder().connectTimeout(denbora_muga).build();
        return Konektatu.send(HttpRequest.newBuilder(helbide).timeout(denbora_muga).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket KONEKTATU_amaiera_puntu(String helbide, int 포트, int 제한밀리초) throws IOException {
        Socket Konektatu = new Socket();
        try {
            Konektatu.connect(new InetSocketAddress(helbide, 포트), 제한밀리초);
            Konektatu.setSoTimeout(제한밀리초);
            return Konektatu;
        } catch (IOException errorea) { Konektatu.close(); throw errorea; }
    }
}
