// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP ጌጋ 상태도 호출자가 판단할 수 있도록 መልስ 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI ኣድራሻ, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient ኣላግብ = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return ኣላግብ.send(HttpRequest.newBuilder(ኣድራሻ).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ኣድራሻ, int ሃርድዌር_ወደብ, int 제한밀리초) throws IOException {
        Socket ኣላግብ = new Socket();
        try {
            ኣላግብ.connect(new InetSocketAddress(ኣድራሻ, ሃርድዌር_ወደብ), 제한밀리초);
            ኣላግብ.setSoTimeout(제한밀리초);
            return ኣላግብ;
        } catch (IOException ጌጋ) { ኣላግብ.close(); throw ጌጋ; }
    }
}
