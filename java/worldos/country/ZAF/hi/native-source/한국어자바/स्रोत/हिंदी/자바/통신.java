// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP त्रुटि 상태도 호출자가 판단할 수 있도록 उत्तर 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI पता, Duration समय_सीमा)
            throws IOException, InterruptedException {
        HttpClient जोड़ना = HttpClient.newBuilder().connectTimeout(समय_सीमा).build();
        return जोड़ना.send(HttpRequest.newBuilder(पता).timeout(समय_सीमा).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket कनेक्ट_एंडपॉइंट(String पता, int 포트, int 제한밀리초) throws IOException {
        Socket जोड़ना = new Socket();
        try {
            जोड़ना.connect(new InetSocketAddress(पता, 포트), 제한밀리초);
            जोड़ना.setSoTimeout(제한밀리초);
            return जोड़ना;
        } catch (IOException त्रुटि) { जोड़ना.close(); throw त्रुटि; }
    }
}
