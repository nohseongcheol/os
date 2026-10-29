// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package தமிழ்.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP பிழை 상태도 호출자가 판단할 수 있도록 பதிலளி 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI முகவரி, Duration நேர_வரம்பு)
            throws IOException, InterruptedException {
        HttpClient இணைக்க = HttpClient.newBuilder().connectTimeout(நேர_வரம்பு).build();
        return இணைக்க.send(HttpRequest.newBuilder(முகவரி).timeout(நேர_வரம்பு).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket இணை_முடிவுப்_புள்ளி(String முகவரி, int 포트, int 제한밀리초) throws IOException {
        Socket இணைக்க = new Socket();
        try {
            இணைக்க.connect(new InetSocketAddress(முகவரி, 포트), 제한밀리초);
            இணைக்க.setSoTimeout(제한밀리초);
            return இணைக்க;
        } catch (IOException பிழை) { இணைக்க.close(); throw பிழை; }
    }
}
