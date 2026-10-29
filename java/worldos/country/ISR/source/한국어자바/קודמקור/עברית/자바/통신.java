// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP שגיאה 상태도 호출자가 판단할 수 있도록 מענה 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI למען, Duration מגבלת_זמן)
            throws IOException, InterruptedException {
        HttpClient חיבור = HttpClient.newBuilder().connectTimeout(מגבלת_זמן).build();
        return חיבור.send(HttpRequest.newBuilder(למען).timeout(מגבלת_זמן).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket לקשר_משתתף(String למען, int חומרה_הסב, int 제한밀리초) throws IOException {
        Socket חיבור = new Socket();
        try {
            חיבור.connect(new InetSocketAddress(למען, חומרה_הסב), 제한밀리초);
            חיבור.setSoTimeout(제한밀리초);
            return חיבור;
        } catch (IOException שגיאה) { חיבור.close(); throw שגיאה; }
    }
}
