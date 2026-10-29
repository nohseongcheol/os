// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class गणना {
    static int एकूण_मूल्य(int शेवट) {
        int मोजमाप = 0;
        for (int अनुक्रमणिका = 1; अनुक्रमणिका <= शेवट; अनुक्रमणिका++) मोजमाप += अनुक्रमणिका;
        return मोजमाप;
    }

    public static int सुरू_करा() {
        int[] मूल्ये = new int[3];
        मूल्ये[0] = एकूण_मूल्य(10);
        मूल्ये[1] = -7 / 3;
        मूल्ये[2] = "한글".length();
        return मूल्ये[0] == 55 && मूल्ये[1] == -2 && मूल्ये[2] == 2 ? 0 : 1;
    }
}
