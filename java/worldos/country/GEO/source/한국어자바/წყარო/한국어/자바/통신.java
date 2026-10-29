// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP შეცდომა 상태도 호출자가 판단할 수 있도록 პასუხი 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI მისამართი, Duration დროის_შეზღუდვა)
            throws IOException, InterruptedException {
        HttpClient დაკავშირება = HttpClient.newBuilder().connectTimeout(დროის_შეზღუდვა).build();
        return დაკავშირება.send(HttpRequest.newBuilder(მისამართი).timeout(დროის_შეზღუდვა).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String მისამართი, int 포트, int 제한밀리초) throws IOException {
        Socket დაკავშირება = new Socket();
        try {
            დაკავშირება.connect(new InetSocketAddress(მისამართი, 포트), 제한밀리초);
            დაკავშირება.setSoTimeout(제한밀리초);
            return დაკავშირება;
        } catch (IOException შეცდომა) { დაკავშირება.close(); throw შეცდომა; }
    }
}
