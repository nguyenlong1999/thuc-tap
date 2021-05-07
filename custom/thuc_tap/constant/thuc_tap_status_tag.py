class StatusTag():
    # tag cho status
    STATUS_CANCEL = '-1'  # Hủy
    STATUS_UNCONFIMRED = '0'  # Chưa xác nhận
    STATUS_APPROVED = '1'  # Đã duyệt
    STATUS_WAIT = '2'  # Chờ xác nhận
    STATUS_RECEIVED = '3'  # Đã nhận
    STATUS_PAID = '4'  # Đã trả
    STATUS_NOT_RECEIVED = '5'   # Chưa nhận

    # Status API
    SUCCESS = 200
    INVALID_FIELD = 201
    CAN_NOT_CHANGE_STATUS = 203
    INVALID_ID = 204
