// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class коммуникация {
    private коммуникация() {}
    /** HTTP ошибка 상태도 호출자가 판단할 수 있도록 ответ 전체를 반환한다. */
    public static HttpResponse<String> ВЗЯТЬ_ЗНАЧЕН(URI АДРЕС, Duration ограничение_времени)
            throws IOException, InterruptedException {
        HttpClient Подключить = HttpClient.newBuilder().connectTimeout(ограничение_времени).build();
        return Подключить.send(HttpRequest.newBuilder(АДРЕС).timeout(ограничение_времени).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket Connect_Endpoint(String АДРЕС, int аппаратный_порт, int 제한밀리초) throws IOException {
        Socket Подключить = new Socket();
        try {
            Подключить.connect(new InetSocketAddress(АДРЕС, аппаратный_порт), 제한밀리초);
            Подключить.setSoTimeout(제한밀리초);
            return Подключить;
        } catch (IOException ошибка) { Подключить.close(); throw ошибка; }
    }
}
