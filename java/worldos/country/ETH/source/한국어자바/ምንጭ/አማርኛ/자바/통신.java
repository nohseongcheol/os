// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP ስህተት 상태도 호출자가 판단할 수 있도록 መልስ 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI አድራሻ, Duration የ_ግዜ_ገደብ)
            throws IOException, InterruptedException {
        HttpClient መገናኛ = HttpClient.newBuilder().connectTimeout(የ_ግዜ_ገደብ).build();
        return መገናኛ.send(HttpRequest.newBuilder(አድራሻ).timeout(የ_ግዜ_ገደብ).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String አድራሻ, int 포트, int 제한밀리초) throws IOException {
        Socket መገናኛ = new Socket();
        try {
            መገናኛ.connect(new InetSocketAddress(አድራሻ, 포트), 제한밀리초);
            መገናኛ.setSoTimeout(제한밀리초);
            return መገናኛ;
        } catch (IOException ስህተት) { መገናኛ.close(); throw ስህተት; }
    }
}
