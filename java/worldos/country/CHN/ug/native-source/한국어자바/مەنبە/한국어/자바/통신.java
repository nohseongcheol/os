// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP خاتالىق 상태도 호출자가 판단할 수 있도록 جاۋابلاش 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI ئادرېس, Duration ۋاقىت_چېكى)
            throws IOException, InterruptedException {
        HttpClient ئۇلا = HttpClient.newBuilder().connectTimeout(ۋاقىت_چېكى).build();
        return ئۇلا.send(HttpRequest.newBuilder(ئادرېس).timeout(ۋاقىت_چېكى).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ئادرېس, int قاتتىق_دېتال_ئېغىز, int 제한밀리초) throws IOException {
        Socket ئۇلا = new Socket();
        try {
            ئۇلا.connect(new InetSocketAddress(ئادرېس, قاتتىق_دېتال_ئېغىز), 제한밀리초);
            ئۇلا.setSoTimeout(제한밀리초);
            return ئۇلا;
        } catch (IOException خاتالىق) { ئۇلا.close(); throw خاتالىق; }
    }
}
