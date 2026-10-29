// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP ГРЕШКА 상태도 호출자가 판단할 수 있도록 отговор 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI адрес, Duration ограничение_на_времето)
            throws IOException, InterruptedException {
        HttpClient Свързване = HttpClient.newBuilder().connectTimeout(ограничение_на_времето).build();
        return Свързване.send(HttpRequest.newBuilder(адрес).timeout(ограничение_на_времето).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket връзка_участник(String адрес, int 포트, int 제한밀리초) throws IOException {
        Socket Свързване = new Socket();
        try {
            Свързване.connect(new InetSocketAddress(адрес, 포트), 제한밀리초);
            Свързване.setSoTimeout(제한밀리초);
            return Свързване;
        } catch (IOException ГРЕШКА) { Свързване.close(); throw ГРЕШКА; }
    }
}
