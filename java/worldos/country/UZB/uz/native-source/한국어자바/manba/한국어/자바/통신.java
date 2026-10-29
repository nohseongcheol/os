// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Xato 상태도 호출자가 판단할 수 있도록 javob_berish 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI manzil, Duration vaqt_cheklovi)
            throws IOException, InterruptedException {
        HttpClient Ulanish = HttpClient.newBuilder().connectTimeout(vaqt_cheklovi).build();
        return Ulanish.send(HttpRequest.newBuilder(manzil).timeout(vaqt_cheklovi).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String manzil, int 포트, int 제한밀리초) throws IOException {
        Socket Ulanish = new Socket();
        try {
            Ulanish.connect(new InetSocketAddress(manzil, 포트), 제한밀리초);
            Ulanish.setSoTimeout(제한밀리초);
            return Ulanish;
        } catch (IOException Xato) { Ulanish.close(); throw Xato; }
    }
}
