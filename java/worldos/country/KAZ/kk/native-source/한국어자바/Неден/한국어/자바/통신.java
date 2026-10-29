// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Қате 상태도 호출자가 판단할 수 있도록 жауап 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI мекенжай, Duration уақыт_шектеуі)
            throws IOException, InterruptedException {
        HttpClient Байланысу = HttpClient.newBuilder().connectTimeout(уақыт_шектеуі).build();
        return Байланысу.send(HttpRequest.newBuilder(мекенжай).timeout(уақыт_шектеуі).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket қосу_қатысушы(String мекенжай, int 포트, int 제한밀리초) throws IOException {
        Socket Байланысу = new Socket();
        try {
            Байланысу.connect(new InetSocketAddress(мекенжай, 포트), 제한밀리초);
            Байланысу.setSoTimeout(제한밀리초);
            return Байланысу;
        } catch (IOException Қате) { Байланысу.close(); throw Қате; }
    }
}
