#ifndef _include_system_stat
#define _include_system_stat

#include <system/data_types.h>

#define file_kind_mask 0170000
#define directory_kind 0040000
#define character_device_kind 0020000
#define regular_file_kind 0100000
#define owner_read_permission 0400
#define owner_write_permission 0200
#define owner_execute_permission 0100
#define group_read_permission 0040
#define group_write_permission 0020
#define group_execute_permission 0010
#define others_read_permission 0004
#define others_write_permission 0002
#define others_execute_permission 0001
#define is_directory_mode(m) (((m) & file_kind_mask) == directory_kind)
#define is_character_device_mode(m) (((m) & file_kind_mask) == character_device_kind)
#define is_regular_file_mode(m) (((m) & file_kind_mask) == regular_file_kind)

struct stat {
    device_identifier_type containing_device;
    file_serial_number_type file_serial_number;
    file_mode_type file_kind_and_permissions;
    hard_link_count_type hard_link_count;
    user_identifier_type owner_user_identifier;
    group_identifier_type owner_group_identifier;
    device_identifier_type represented_device;
    file_offset_type file_size;
    block_size_type preferred_io_block_size;
    block_count_type allocated_block_count;
    time_value_type last_access_time;
    int last_access_nanoseconds;
    time_value_type last_content_change_time;
    int last_content_change_nanoseconds;
    time_value_type last_status_change_time;
    int last_status_change_nanoseconds;
};

#ifdef __cplusplus
extern "C" {
#endif
int stat(const char *path, struct stat *transfer_buffer);
int lstat(const char *path, struct stat *transfer_buffer);
int fstat(int file_descriptor, struct stat *transfer_buffer);
#ifdef __cplusplus
}
#endif

#endif
