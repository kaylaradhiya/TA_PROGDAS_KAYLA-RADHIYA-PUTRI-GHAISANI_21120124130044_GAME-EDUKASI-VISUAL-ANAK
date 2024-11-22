import pygame
import sys
import queue 

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Name It!")

menu_background = pygame.image.load("pict.1page/background.png")
menu_background = pygame.transform.scale(menu_background, (screen_width, screen_height))

start_button_image = pygame.image.load("pict.1page/mulai.png")
start_button_default = pygame.transform.smoothscale(start_button_image, (200, 70))
start_button_hover = pygame.transform.smoothscale(start_button_image, (210, 75))
start_button_rect = start_button_default.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

kategori_background = pygame.image.load("pict.2page/kategori.png")
kategori_background = pygame.transform.scale(kategori_background, (screen_width, screen_height))

kembali_button_image = pygame.image.load("pict.2page/kembali.png")
kembali_button_default = pygame.transform.smoothscale(kembali_button_image, (150, 60))
kembali_button_hover = pygame.transform.smoothscale(kembali_button_image, (140, 55))
kembali_button_rect = start_button_default.get_rect(center=(170, 530))

kategori = {
    "Buah": pygame.image.load("pict.2page/buah.png"),
    "Kendaraan": pygame.image.load("pict.2page/kendaraan.png"),
    "Hewan": pygame.image.load("pict.2page/hewan.png"),
    "Warna": pygame.image.load("pict.2page/warna.png"),
    "Benda": pygame.image.load("pict.2page/benda.png"),
}

kategori_button = {}
kategori_positions = {
    "Buah": (200, 200),
    "Kendaraan": (400, 200),
    "Hewan": (600, 200),
    "Warna": (500, 300),
    "Benda": (300, 300),
}

for kategori_name, position in kategori_positions.items():
    kategori_button[kategori_name] = {
        "image": pygame.transform.smoothscale(kategori[kategori_name], (200, 70)),
        "rect": pygame.Rect(position[0] - 100, position[1] - 35, 200, 70),
    }

quiz_data = {
    "Buah": ["apel", "mangga", "jeruk", "nanas", "semangka", "melon", "rambutan", "anggur", "alpukat", "durian"],
    "Kendaraan": ["mobil", "motor", "bus", "kapal", "perahu", "pesawat", "sepeda", "skuter", "truk", "helikopter"],
    "Hewan": ["anjing", "kucing", "ayam", "bebek", "harimau", "singa", "kuda", "serigala", "burung", "ikan"],
    "Warna": ["merah", "orange", "kuning", "hijau", "biru", "ungu", "pink", "hitam", "putih"],
    "Benda": ["meja", "kursi", "buku", "pensil", "topi", "sepatu", "gitar", "tas", "laptop", "kasur"],
}

right_popup = pygame.image.load("right.png")
wrong_popup = pygame.image.load("wrong.png")

def show_popup(image, duration):
    return pygame.time.get_ticks() + duration * 500, image

def quiz_page(kategori_name):
    pertanyaan_list = quiz_data[kategori_name]
    score = 0
    popup_time = 0
    popup_image = None

    question_queue = queue.Queue()
    for pertanyaan in pertanyaan_list:
        question_queue.put(pertanyaan)

    kategori_page_image = f"pict.3page/page_{kategori_name.lower()}.png"

    while not question_queue.empty():  
        pertanyaan = question_queue.get()  
        input_active = True
        user_input = ""

        while input_active:
            screen.fill((255, 255, 255))
            
            quiz_background = pygame.image.load(kategori_page_image)
            quiz_background = pygame.transform.scale(quiz_background, (800, 600))
            screen.blit(quiz_background, (0, 0))
 
            mouse_pos = pygame.mouse.get_pos()
            if kembali_button_rect.collidepoint(mouse_pos):
                screen.blit(kembali_button_hover, kembali_button_rect)
            else:
                screen.blit(kembali_button_default, kembali_button_rect)

            gambar_soal = f"{kategori_name.lower()}_{pertanyaan}.png"
    
            soal_image = pygame.image.load(gambar_soal)
            soal_image = pygame.transform.scale(soal_image, (300, 300))
            screen.blit(soal_image, (250, 128))
           

            font = pygame.font.Font(None, 36)
            pertanyaan_text = font.render(f"Apa nama {kategori_name.lower()} ini?", True, (0, 50, 100))
            screen.blit(pertanyaan_text, (235, 430))

            input_box = pygame.Rect(screen_width // 2 - 60, 500, 300, 50)
            pygame.draw.rect(screen, (255, 255, 255), input_box)
            input_text = font.render(user_input, True, (0, 0, 0))
            screen.blit(input_text, (input_box.x + 10, input_box.y + 10))

            score_text = font.render(f"Skor: {score}", True, (0, 50, 100))
            screen.blit(score_text, (10, 10))

            if popup_image and pygame.time.get_ticks() < popup_time:
                screen.blit(popup_image, (screen_width // 2 - popup_image.get_width() // 2, screen_height // 2 - popup_image.get_height() // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if kembali_button_rect.collidepoint(mouse_pos):
                        return 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        if user_input.lower() == pertanyaan.lower():
                            score += 1
                            popup_time, popup_image = show_popup(right_popup, 1)
                        else:
                            popup_time, popup_image = show_popup(wrong_popup, 1)
                        input_active = False
                    else:
                        user_input += event.unicode
            
    screen.fill((255, 255, 255))
    screen.blit(menu_background, (0, 0))
    result_font = pygame.font.Font(None, 50)
    result_text = result_font.render(f"Skor Anda: {score}/{len(pertanyaan_list)}", True, (255, 255, 255))
    screen.blit(result_text, (240, 430))
    pygame.display.flip()
    pygame.time.wait(2000)  

    return

def category_page():
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for kategori_name, button in kategori_button.items():
                    if button["rect"].collidepoint(mouse_pos):
                        quiz_page(kategori_name)
                
                if kembali_button_rect.collidepoint(mouse_pos):
                    main_menu()

        screen.fill((255, 255, 255))
        screen.blit(kategori_background, (0, 0))

        for kategori_name, button in kategori_button.items():
            screen.blit(button["image"], button["rect"])

        if kembali_button_rect.collidepoint(mouse_pos):
            screen.blit(kembali_button_hover, kembali_button_rect)
        else:
            screen.blit(kembali_button_default, kembali_button_rect)

        pygame.display.flip()


def main_menu():
    while True:
        screen.fill((255, 255, 255))
        screen.blit(menu_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(mouse_pos):
                    category_page()

        mouse_pos = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_pos):
            screen.blit(start_button_hover, start_button_rect)
        else:
            screen.blit(start_button_default, start_button_rect)

        pygame.display.flip()

main_menu()
