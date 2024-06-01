from PIL import Image

# 載入圖片
messagetext_off = Image.open("icon/wnote_off.png")
alarmclock_on = Image.open("icon/wtime-quarter-to_off.png")

# 獲取圖片尺寸
width1, height1 = messagetext_off.size
width2, height2 = alarmclock_on.size

# 計算拼接後的圖片尺寸
new_width = width1 + width2+8
new_height = max(height1, height2)

transparent_color = (255, 255, 255, 0)

# 創建一個透明的空白圖片
new_image = Image.new("RGBA", (new_width, new_height), transparent_color)

# 將第一張圖片貼在左邊
new_image.paste(messagetext_off, (0, 0))

# 將第二張圖片貼在右邊
new_image.paste(alarmclock_on, (width1+8, 0))

# 顯示或儲存拼接後的圖片
# new_image.show()
new_image.save("icon/woff-off_image.png")
