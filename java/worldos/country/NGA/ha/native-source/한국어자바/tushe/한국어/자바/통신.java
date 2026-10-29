// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Kuskure 상태도 호출자가 판단할 수 있도록 mayar_da_martani 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI imel, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient Haɗi = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return Haɗi.send(HttpRequest.newBuilder(imel).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String imel, int kayan_haɗi_na_kwamfuta_fot, int 제한밀리초) throws IOException {
        Socket Haɗi = new Socket();
        try {
            Haɗi.connect(new InetSocketAddress(imel, kayan_haɗi_na_kwamfuta_fot), 제한밀리초);
            Haɗi.setSoTimeout(제한밀리초);
            return Haɗi;
        } catch (IOException Kuskure) { Haɗi.close(); throw Kuskure; }
    }
}
