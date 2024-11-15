# main.py
from PIL import Image, ImageDraw
from Character import Character
from Garbagebag import Garbagebag
from Item import Item
from Score import Score
from Joystick import Joystick
import time

def main():
    # 조이스틱 초기화
    joystick = Joystick()
    my_image = Image.new("RGB", (joystick.width, joystick.height))
    my_draw = ImageDraw.Draw(my_image)
    
    # 게임 객체 초기화
    character = Character(joystick.width, joystick.height)
    # 원하는 증가율 크기로 변경 가능
    character.size_increment = 0.3  # 30% 증가
    score = Score()
    items = [Item(joystick.width, joystick.height) for _ in range(3)]  # 3개의 아이템 동시 생성
    
    # 이미지 로드
    # main.py의 이미지 로드 부분 수정 60x60 으로 설정
    # 키 입력하지 않았을때의 캐릭터 설정
    init_character = Image.open('image/initCharacterState.png').convert('RGBA').resize((60, 60))
    walk_images = [Image.open(f'image/walk/walk{i+1}.png').convert('RGBA').resize((60, 60)) for i in range(8)]
    run_images = [Image.open(f'image/run/run{i+1}.png').convert('RGBA').resize((60, 60)) for i in range(8)]

    # 음식 이미지 (20x20 크기로 조정)
    food_images = [Image.open(f'image/{food}.png').convert('RGBA').resize((20, 20)) 
                for food in ['bread', 'chicken', 'ham', 'hamburger', 'hotdog']]

    # 쓰레기 이미지 (20x20 크기로 조정)
    trash_image = Image.open('image/food_trash.png').convert('RGBA').resize((20, 20))

    # 이미지 로드 부분에 쓰레기 봉투 이미지 추가
    garbagebag_image = Image.open('image/garbagebag.png').convert('RGBA').resize((20, 20))

    # 쓰레기 봉투 리스트 추가
    garbagebags = []
    
    game_time = 0

    # 이미지 크기를 저장할 딕셔너리
    character_images = {
        1: {'init': init_character,
            'walk': walk_images,
            'run': run_images}
    }

    max_level = 4  # 최대 레벨 설정
    # 각 레벨별 이미지 크기 미리 생성
    for level in range(2, max_level + 1):  # 최대 4배까지 준비
        size = int(60 * (1 + (level - 1) * character.size_increment))  # 30%씩 증가
        character_images[level] = {
            'init': init_character.resize((size, size)),
            'walk': [img.resize((size, size)) for img in walk_images],
            'run': [img.resize((size, size)) for img in run_images]
        }    
    
    while not score.game_over():
        # 배경 초기화 (흰색)
        my_draw.rectangle((0, 0, joystick.width, joystick.height), fill=(255, 255, 255))
        
        # 조이스틱 입력 처리
        command = {
            'left_pressed': not joystick.button_L.value,
            'right_pressed': not joystick.button_R.value,
        }

        # B 버튼으로 쓰레기 봉투 발사
        if not joystick.button_B.value:
            garbagebag = Garbagebag(character.position, character.current_size)  # current_size 전달
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
                if item.state == 'active' and bag.check_collision(item.position):
                    item.reset()  # 아이템 재설정
                    garbagebags.remove(bag)
                    break
        
        # 달리기 상태 설정
        character.set_running(not joystick.button_A.value)
        
        # 캐릭터 이동
        character.move(command)
        
        # 아이템 낙하 및 충돌 체크
        # 아이템 업데이트
        for item in items:
            if item.state == 'active':
                item.fall()
                # 캐릭터와 충돌
                if item.check_collision(character.position):
                    if item.item_type == 5:  # 쓰레기
                        score.lose_life()
                    else:  # 음식
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
        
        # 캐릭터 그리기 부분 수정
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
            
        # 아이템 그리기(음식: 0 ~ 4 및 음식물 쓰레기: 5)
        for item in items:
            if item.state == 'active':  # 활성화된 아이템만 그리기
                if item.item_type == 5:
                    item_img = trash_image
                else:
                    item_img = food_images[item.item_type]
                my_image.paste(item_img, 
                             (int(item.position[0]), int(item.position[1])), 
                             item_img)

        # 이미지 그리기
        # 쓰레기 봉투 그리기
        for bag in garbagebags:
            my_image.paste(garbagebag_image, 
                         (int(bag.position[0]), int(bag.position[1])), garbagebag_image)
            
        # 캐릭터 그리기
        my_image.paste(char_img, (int(character.position[0]), int(character.position[1])), char_img)
        
        # 점수와 생명력 표시
        my_draw.text((10, 10), f'Score: {score.get_score()}', fill=(0, 0, 0))
        my_draw.text((10, 30), f'Life: {score.get_life()}', fill=(0, 0, 0))
        
        # 화면 업데이트
        joystick.disp.image(my_image)
        
        game_time += 1
        time.sleep(0.03)
    
    # 게임 오버 화면
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill=(0, 0, 0))
    my_draw.text((joystick.width//2 - 40, joystick.height//2 - 20), 
                 f'Game Over!\nScore: {score.get_score()}', 
                 fill=(255, 255, 255))
    joystick.disp.image(my_image)
    time.sleep(3)

if __name__ == '__main__':
    main()