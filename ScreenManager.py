# ScreenManager.py
from PIL import Image, ImageDraw, ImageFont

class ScreenManager:
    def __init__(self, joystick):
        self.joystick = joystick
        self.width = joystick.width
        self.height = joystick.height
        self.font = ImageFont.load_default()
        self.title_font = ImageFont.truetype("font/Bangers-Regular.ttf", 46)
        self.start_font = ImageFont.truetype("font/Bangers-Regular.ttf", 16)
        self.game_over_font = ImageFont.truetype("font/Bangers-Regular.ttf", 42)  # 게임오버 폰트
        self.score_font = ImageFont.truetype("font/Bangers-Regular.ttf", 32)      # 점수 폰트
            
    def show_start_screen(self, background):
        start_image = Image.new("RGB", (self.width, self.height))
        start_image.paste(background, (0, 0))
        draw = ImageDraw.Draw(start_image)

        title_text = "FOOD RAIN"
        title_bbox = self.title_font.getbbox(title_text)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (self.width - title_width) // 2
        # 테두리 효과와 함께 제목 나타냄
        draw.text((title_x-2, 20), title_text, font=self.title_font, fill=(0, 0, 0))  # 그림자
        draw.text((title_x, 20), title_text, font=self.title_font, fill=(255, 0, 0))  # 메인 텍스트
        
        # 시작 메시지 (화면 하단에 위치)
        start_text = "Press any key to start"
        start_bbox = self.start_font.getbbox(start_text)
        start_width = start_bbox[2] - start_bbox[0]
        start_x = (self.width - start_width) // 2
        start_y = self.height - 20  # 하단 여백 조정
        
        # 두꺼운 효과를 위한 테두리 설정
        offsets = [(1,1), (-1,-1), (1,-1), (-1,1)]
        for dx, dy in offsets:
            draw.text((start_x + dx, start_y + dy), start_text, 
                     font=self.start_font, fill=(0, 0, 0))
        
        # 메인 텍스트
        draw.text((start_x, start_y), start_text, font=self.start_font, fill=(255, 255, 255))
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
        game_over_bbox = self.game_over_font.getbbox(game_over_text)
        game_over_width = game_over_bbox[2] - game_over_bbox[0]
        game_over_x = (self.width - game_over_width) // 2
        
        # 텍스트에 테두리 설정
        offsets = [(1,1), (-1,-1), (1,-1), (-1,1)]
        for dx, dy in offsets:
            draw.text((game_over_x + dx, self.height//3 + dy), game_over_text, 
                     font=self.game_over_font, fill=(0, 0, 0))
        draw.text((game_over_x, self.height//3), game_over_text, 
                 font=self.game_over_font, fill=(255, 255, 255))
        
        # 점수 텍스트
        score_text = f"Final Score: {score}"
        score_bbox = self.score_font.getbbox(score_text)
        score_width = score_bbox[2] - score_bbox[0]
        score_x = (self.width - score_width) // 2
        
        # 점수에도 테두리 설정
        for dx, dy in offsets:
            draw.text((score_x + dx, self.height//2 + dy), score_text, 
                     font=self.score_font, fill=(0, 0, 0))
        draw.text((score_x, self.height//2), score_text, 
                 font=self.score_font, fill=(255, 255, 255))
        
        self.joystick.disp.image(end_image)