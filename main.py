# main.py
from PIL import Image, ImageDraw
from Character import Character
from Garbagebag import Garbagebag
from Item import Item
from Score import Score
from Joystick import Joystick
from ScreenManager import ScreenManager
import time

def main():
    # 조이스틱 초기화
    joystick = Joystick()
    screen_manager = ScreenManager(joystick)
    my_image = Image.new("RGB", (joystick.width, joystick.height))
    my_draw = ImageDraw.Draw(my_image)

    # 배경 이미지 로드
    background = Image.open('image/background_city.jpg').convert('RGB')
    background = background.resize((joystick.width, joystick.height))

    # 시작 화면 이미지 로드
    start_image = Image.open('image/startbackground.png').convert('RGB')
    start_image = start_image.resize((joystick.width, joystick.height))

    # 게임 종료 이미지 로드
    ending_image = Image.open('image/background_movie.jpg').convert('RGB')
    ending_image = ending_image.resize((joystick.width, joystick.height))

    # 시작 화면 표시
    screen_manager.show_start_screen(start_image)
    
    # 게임 객체 초기화
    character = Character(joystick.width, joystick.height)

    score = Score()
    items = [Item(joystick.width, joystick.height) for _ in range(8)]
    item_size = items[0].item_size
    
    # 이미지 로드
    # main.py의 이미지 로드 부분 수정 60x60 으로 설정    
    init_character = Image.open('image/initCharacterState.png').convert('RGBA').resize((60, 60))
    walk_images = [Image.open(f'image/walk/walk{i+1}.png').convert('RGBA').resize((60, 60)) for i in range(8)]
    run_images = [Image.open(f'image/run/run{i+1}.png').convert('RGBA').resize((60, 60)) for i in range(8)]

    # 음식 이미지 (30x30 크기로 조정 -> item 클래스에서 한번에 조정)
    food_images = [Image.open(f'image/{food}.png').convert('RGBA').resize((item_size, item_size)) 
                for food in ['bread', 'chicken', 'ham', 'hamburger', 'hotdog']]

    trash_image = Image.open('image/food_trash.png').convert('RGBA').resize((item_size, item_size))
    garbagebag_image = Image.open('image/garbagebag.png').convert('RGBA').resize((item_size, item_size))
    pill_image = Image.open('image/pill.png').convert('RGBA').resize((item_size, item_size))
    reduction_image = Image.open('image/reduction.png').convert('RGBA').resize((item_size, item_size))

    # 하트 이미지 로드
    life_3 = Image.open('image/life_3.png').convert('RGBA')
    life_2 = Image.open('image/life_2.png').convert('RGBA')
    life_1 = Image.open('image/life_1.png').convert('RGBA')

    heart_size = 15
    life_3 = life_3.resize((heart_size * 3, heart_size))
    life_2 = life_2.resize((heart_size * 3, heart_size))
    life_1 = life_1.resize((heart_size * 3, heart_size))

    # 쓰레기 봉투 리스트
    garbagebags = []

    # 이미지 크기를 저장할 딕셔너리
    character_images = {
        1: {'init': init_character,
            'walk': walk_images,
            'run': run_images}
    }

    # 각 레벨별 이미지 크기 미리 생성
    for level in range(2, character.max_level + 1):
        size = int(60 * (1 + (level - 1) * character.size_increment))
        character_images[level] = {
            'init': init_character.resize((size, size)),
            'walk': [img.resize((size, size)) for img in walk_images],
            'run': [img.resize((size, size)) for img in run_images]
        }    
    
    while not score.game_over():

        my_image.paste(background, (0, 0))

        command = {
            'left_pressed': not joystick.button_L.value,
            'right_pressed': not joystick.button_R.value,
            'up_pressed': not joystick.button_U.value,
        }

        # B 버튼으로 쓰레기 봉투 발사
        if not joystick.button_B.value:
            # 발사 방향 결정
            throw_direction = "up"  # 기본 방향은 수직으로
            
            # 대각선 방향 체크
            if not joystick.button_L.value and not joystick.button_U.value:
                throw_direction = "up_left"
            elif not joystick.button_R.value and not joystick.button_U.value:
                throw_direction = "up_right"

            garbagebag = Garbagebag(character.position, character.current_size, throw_direction)
            garbagebags.append(garbagebag)

        # 쓰레기 봉투 이동 및 충돌 체크
        for bag in garbagebags[:]:
            bag.move()
            
            # 화면 밖으로 나가면 제거
            if bag.position[3] < 0:
                garbagebags.remove(bag)
                continue
                
            # 아이템과 충돌 체크
            for item in items:
                if bag.check_collision(item.position):
                    item.reset()  # 아이템 재설정
                    garbagebags.remove(bag)
                    break
        
        # 달리기 상태 설정
        character.set_running(not joystick.button_A.value)
        
        # 캐릭터 이동
        character.move(command)
        
        # 아이템 낙하 및 충돌 체크
        for item in items:
            item.fall()
            # 캐릭터와 아이템이 충돌했을때
            if item.check_collision(character.position):
                if item.item_type == 5:  # 쓰레기일 때
                    score.lose_life()
                elif item.item_type == 6:  # 알약
                    score.add_life()  # 생명력 증가
                elif item.item_type == 7:  # 축소 아이템
                    if score.decrease_size_level():
                        character.resize(score.get_size_level())
                else:  # 음식일 때
                    if score.add_score():
                        character.resize(score.get_size_level())
                item.reset()
            # 바닥 충돌 체크
            elif item.check_bottom(joystick.height):
                if item.item_type == 5:  # 쓰레기일 때만 생명력 감소
                    score.lose_life()
                item.reset()
            # 화면 밖으로 완전히 나간 경우 재설정
            if item.position[1] > joystick.height:
                item.reset()
        
        # 캐릭터 나타냄
        current_level = score.get_size_level()
        if not character.is_moving:  # 움직이지 않을 때
            char_img = character_images[current_level]['init']
            if character.direction == "left":
                char_img = char_img.transpose(Image.FLIP_LEFT_RIGHT)
        else:  # 움직일 때
            if character.is_running:
                char_img = character_images[current_level]['run'][character.run_state]
            else:
                char_img = character_images[current_level]['walk'][character.walk_state]
                
            if character.direction == "left":
                char_img = char_img.transpose(Image.FLIP_LEFT_RIGHT)
        # 아이템 나타냄
        for item in items:
            if item.item_type == 5: # 쓰레기
                item_img = trash_image
            elif item.item_type == 6:  # 알약
                item_img = pill_image
            elif item.item_type == 7:  # 축소 아이템
                item_img = reduction_image
            else:
                item_img = food_images[item.item_type] # 음식들
            my_image.paste(item_img, (int(item.position[0]), int(item.position[1])), item_img)

        # 쓰레기 봉투 나타냄
        for bag in garbagebags:
            my_image.paste(garbagebag_image, 
                         (int(bag.position[0]), int(bag.position[1])), garbagebag_image)
            
        # 캐릭터 그리기
        my_image.paste(char_img, (int(character.position[0]), int(character.position[1])), char_img)
        
        # 점수 표시
        my_draw.text((10, 10), f'Score: {score.get_score()}', fill=(0, 0, 0))
        if score.size_level == 5:
            my_draw.text((10, 30), "Size: MAX Level!", fill=(255, 0, 0))  # 빨간색으로 표시
        else:
            remaining_food = 10 - score.size_counter
            my_draw.text((10, 30), f'Next Level: {remaining_food} foods', fill=(0, 0, 0))
        # 생명력 나타냄
        current_life = score.get_life()
        if current_life == 3:
            my_image.paste(life_3, (190, 10), life_3)
        elif current_life == 2:
            my_image.paste(life_2, (190, 10), life_2)
        elif current_life == 1:
            my_image.paste(life_1, (190, 10), life_1)
        
        # 화면 업데이트
        joystick.disp.image(my_image)
        
        time.sleep(0.03)
    
    # 게임 종료 화면
    screen_manager.show_ending_screen(ending_image, score.get_score())
    time.sleep(3)

if __name__ == '__main__':
    main()