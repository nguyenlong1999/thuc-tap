class StatusTag():
    # tag cho status
    STATUS_CANCEL = '-1'  # Hủy
    STATUS_UNCONFIMRED = '0'  # Chưa nhận
    STATUS_APPROVED = '1'  # Đã duyệt
    STATUS_WAIT = '2'  # Chờ xác nhận
    STATUS_RECEIVED = '3'  # Đã nhận
    STATUS_PAID = '4'  # Đã trả

    SUCCESS = 200
    INVALID_FIELD = 201
    CAN_NOT_CHANGE_STATUS = 203
    INVALID_ID =204