// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.गाभा;

/** Java-व्यवस्थापित केंद्रक आणि CPU-विशिष्ट संकेत यांतील एकमेव सीमा. */
public interface हार्डवेअर_मूल्य {
    void अनुक्रमिक_प्रदान(String सामुग्री_मूल्य);

    int पॉर्ट_बाइट_वाचा(int हार्डवेअर_पोर्ट_नंबर);

    void पॉर्ट_बाइट_लिहा(int हार्डवेअर_पोर्ट_नंबर, int मूल्य);

    void थांबवा_प्रोसेसर();
}

