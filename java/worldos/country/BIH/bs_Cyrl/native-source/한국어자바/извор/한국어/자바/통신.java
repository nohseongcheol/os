// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP грешка 상태도 호출자가 판단할 수 있도록 응답 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI адреса, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient повезати = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return повезати.send(HttpRequest.newBuilder(адреса).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket повезати_крајња_тачка(String адреса, int 포트, int 제한밀리초) throws IOException {
        Socket повезати = new Socket();
        try {
            повезати.connect(new InetSocketAddress(адреса, 포트), 제한밀리초);
            повезати.setSoTimeout(제한밀리초);
            return повезати;
        } catch (IOException грешка) { повезати.close(); throw грешка; }
    }
}
