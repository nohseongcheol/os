#ifndef _include_அமைப்பு_socket
#define _include_அமைப்பு_socket

#include <அடிப்படை_வரையறைகள்.h>
#include <அமைப்பு/தரவு_வகைகள்.h>

typedef unsigned short முகவரிக்_குடும்ப_வகை;

struct தொடர்பு_முனை_முகவரி {
    முகவரிக்_குடும்ப_வகை முனை_முகவரிக்_குடும்பம்;
    char முகவரித்_தரவு[14];
};

#define குறிப்பிடாத_முகவரிக்_குடும்பம் 0
#define பிணையங்களிடை_முகவரிக்_குடும்பக்_குறியீடு 2
#define பிணையங்களிடை_நெறிமுறைக்_குடும்பம் பிணையங்களிடை_முகவரிக்_குடும்பக்_குறியீடு

#define தரவு_ஓட்ட_முனை 1
#define தரவுச்_செய்தி_முனை 2

#define பெறுதலை_நிறுத்து 0
#define அனுப்புதலை_நிறுத்து 1
#define இரு_திசைகளையும்_நிறுத்து 2

#ifdef __cplusplus
extern "C" {
#endif
int தொடர்பு_முனையை_உருவாக்கு(int domain, int type, int protocol);
int உள்ளக_முகவரியைப்_பிணை(int கோப்பு_விவரிப்பி, const struct தொடர்பு_முனை_முகவரி *address, முகவரி_நீள_வகை address_len);
int எதிர்_முனையுடன்_இணை(int கோப்பு_விவரிப்பி, const struct தொடர்பு_முனை_முகவரி *address, முகவரி_நீள_வகை address_len);
int இணைப்புகளை_ஏற்கத்_தயாராகு(int கோப்பு_விவரிப்பி, int backlog);
int இணைப்பை_ஏற்றுக்கொள்(int கோப்பு_விவரிப்பி, struct தொடர்பு_முனை_முகவரி *address, முகவரி_நீள_வகை *address_len);
int உள்ளக_முனையின்_முகவரியைப்_பெறு(int கோப்பு_விவரிப்பி, struct தொடர்பு_முனை_முகவரி *address, முகவரி_நீள_வகை *address_len);
int எதிர்_முனையின்_முகவரியைப்_பெறு(int கோப்பு_விவரிப்பி, struct தொடர்பு_முனை_முகவரி *address, முகவரி_நீள_வகை *address_len);
ssize_t அனுப்பு(int கோப்பு_விவரிப்பி, const void *பரிமாற்ற_இடையகம்_2, size_t நீளம், int flags);
ssize_t பெறு(int கோப்பு_விவரிப்பி, void *பரிமாற்ற_இடையகம்_2, size_t நீளம், int flags);
ssize_t இலக்கிற்கு_அனுப்பு(int கோப்பு_விவரிப்பி, const void *message, size_t நீளம், int flags,
               const struct தொடர்பு_முனை_முகவரி *dest_addr, முகவரி_நீள_வகை dest_len);
ssize_t அனுப்பிய_முகவரியுடன்_பெறு(int கோப்பு_விவரிப்பி, void *பரிமாற்ற_இடையகம்_2, size_t நீளம், int flags,
                 struct தொடர்பு_முனை_முகவரி *address, முகவரி_நீள_வகை *address_len);
int தொடர்புத்_திசையை_மூடு(int கோப்பு_விவரிப்பி, int how);
int தொடர்பு_முனையின்_விருப்பத்தை_அமை(int கோப்பு_விவரிப்பி, int level, int option_name,
               const void *option_value, முகவரி_நீள_வகை option_len);
#ifdef __cplusplus
}
#endif

#endif
