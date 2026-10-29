// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Pōhēhē 상태도 호출자가 판단할 수 있도록 whakautu 전체를 반환한다. */
    public static HttpResponse<String> TAKE_uara(URI ADDRESS, Duration tepe_wā)
            throws IOException, InterruptedException {
        HttpClient TŪHONO = HttpClient.newBuilder().connectTimeout(tepe_wā).build();
        return TŪHONO.send(HttpRequest.newBuilder(ADDRESS).timeout(tepe_wā).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ADDRESS, int 포트, int 제한밀리초) throws IOException {
        Socket TŪHONO = new Socket();
        try {
            TŪHONO.connect(new InetSocketAddress(ADDRESS, 포트), 제한밀리초);
            TŪHONO.setSoTimeout(제한밀리초);
            return TŪHONO;
        } catch (IOException Pōhēhē) { TŪHONO.close(); throw Pōhēhē; }
    }
}
