// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Սխալ 상태도 호출자가 판단할 수 있도록 պատասխանել 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI հասցե, Duration ժամանակի_սահմանափակում)
            throws IOException, InterruptedException {
        HttpClient Միացնել = HttpClient.newBuilder().connectTimeout(ժամանակի_սահմանափակում).build();
        return Միացնել.send(HttpRequest.newBuilder(հասցե).timeout(ժամանակի_սահմանափակում).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String հասցե, int 포트, int 제한밀리초) throws IOException {
        Socket Միացնել = new Socket();
        try {
            Միացնել.connect(new InetSocketAddress(հասցե, 포트), 제한밀리초);
            Միացնել.setSoTimeout(제한밀리초);
            return Միացնել;
        } catch (IOException Սխալ) { Միացնել.close(); throw Սխալ; }
    }
}
