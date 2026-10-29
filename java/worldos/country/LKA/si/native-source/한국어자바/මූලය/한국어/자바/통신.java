// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP දෝෂය 상태도 호출자가 판단할 수 있도록 පිළිතුරු_දෙන්න 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI යොමුව, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient සම්බන්ද_වන්න = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return සම්බන්ද_වන්න.send(HttpRequest.newBuilder(යොමුව).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String යොමුව, int 포트, int 제한밀리초) throws IOException {
        Socket සම්බන්ද_වන්න = new Socket();
        try {
            සම්බන්ද_වන්න.connect(new InetSocketAddress(යොමුව, 포트), 제한밀리초);
            සම්බන්ද_වන්න.setSoTimeout(제한밀리초);
            return සම්බන්ද_වන්න;
        } catch (IOException දෝෂය) { සම්බන්ද_වන්න.close(); throw දෝෂය; }
    }
}
