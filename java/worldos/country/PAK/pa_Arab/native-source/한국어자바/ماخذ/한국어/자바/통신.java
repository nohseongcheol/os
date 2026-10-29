// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP نقص 상태도 호출자가 판단할 수 있도록 جواب_دیوؤ 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI پتا, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient جڑو = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return جڑو.send(HttpRequest.newBuilder(پتا).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String پتا, int 포트, int 제한밀리초) throws IOException {
        Socket جڑو = new Socket();
        try {
            جڑو.connect(new InetSocketAddress(پتا, 포트), 제한밀리초);
            جڑو.setSoTimeout(제한밀리초);
            return جڑو;
        } catch (IOException نقص) { جڑو.close(); throw نقص; }
    }
}
