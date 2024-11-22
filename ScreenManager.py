# ScreenManager.py
from PIL import Image, ImageDraw, ImageFont

class ScreenManager:
    def __init__(self, joystick):
        self.joystick = joystick
        self.width = joystick.width
        self.height = joystick.height
        self.font = ImageFont.load_default()
            
    def show_start_screen(self, background):
        start_image = Image.new("RGB", (self.width, self.height))
        start_image.paste(background, (0, 0))
        draw = ImageDraw.Draw(start_image)
        
        # 시작 메시지 중앙 정렬
        text = "Press any key to start"
        # 기본 폰트의 경우 대략적인 텍스트 너비 계산
        text_width = len(text) * 6  # 기본 폰트에서 한 글자당 약 6픽셀
        text_x = (self.width - text_width) // 2
        text_y = self.height // 2
        
        # 텍스트 색상 설정
        draw.text((text_x, text_y), text, font=self.font, fill=(0, 0, 0))
        self.joystick.disp.image(start_image)
        
        # 아무 키나 누를 때까지 대기
        while True:
            if (not self.joystick.button_A.value or 
                not self.joystick.button_B.value or 
                not self.joystick.button_U.value or 
                not self.joystick.button_D.value or 
                not self.joystick.button_L.value or 
                not self.joystick.button_R.value):
                break

    def show_ending_screen(self, ending_image, score):
        # 엔딩 이미지에 텍스트 추가
        end_image = ending_image.copy()
        draw = ImageDraw.Draw(end_image)
        
        # Game Over 텍스트
        game_over_text = "GAME OVER"
        game_over_width = len(game_over_text) * 6
        game_over_x = (self.width - game_over_width) // 2
        
        # 점수 텍스트
        score_text = f"Final Score: {score}"
        score_width = len(score_text) * 6
        score_x = (self.width - score_width) // 2
        
        # 텍스트 그리기
        draw.text((game_over_x, self.height//3), game_over_text, 
                 font=self.font, fill=(255, 255, 255))
        draw.text((score_x, self.height//2), score_text, 
                 font=self.font, fill=(255, 255, 255))
        
        self.joystick.disp.image(end_image)