import pygame
import sys
import random

# === Inisialisasi Pygame ===
pygame.init()

# === Konfigurasi Layar ===
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Name It!")

# === Aset ===
# 1. Background Halaman Menu
background_image = pygame.image.load("pict.1page/background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# 2. Tombol Mulai
start_button_image = pygame.image.load("pict.1page/mulai.png")
start_button_default = pygame.transform.smoothscale(start_button_image, (200, 70))
start_button_hover = pygame.transform.smoothscale(start_button_image, (170, 60))
start_button_rect = start_button_default.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

# 3. Background Halaman Kategori
category_background = pygame.image.load("pict.2page/kategori.png")
category_background = pygame.transform.scale(category_background, (screen_width, screen_height))

# 4. Tombol Kembali
back_button_image = pygame.image.load("pict.2page/kembali.png")
back_button_default = pygame.transform.smoothscale(back_button_image, (150, 60))
back_button_hover = pygame.transform.smoothscale(back_button_image, (120, 50))
back_button_rect = back_button_default.get_rect(center=(127, 530))

# 5. Tombol Kategori
categories = {
    "Buah": pygame.image.load("pict.2page/buah.png"),
    "Kendaraan": pygame.image.load("pict.2page/kendaraan.png"),
    "Hewan": pygame.image.load("pict.2page/hewan.png"),
    "Warna": pygame.image.load("pict.2page/warna.png"),
    "Random": pygame.image.load("pict.2page/randomob.png"),
}

# Skala tombol kategori dan posisi
category_buttons = {}
category_positions = {
    "Buah": (200, 220),
    "Kendaraan": (400, 220),
    "Hewan": (600, 220),
    "Warna": (300, 300),
    "Random": (500, 300),
}

for category_name, position in category_positions.items():
    category_buttons[category_name] = {
        "image": pygame.transform.smoothscale(categories[category_name], (200, 70)),
        "rect": pygame.Rect(position[0] - 100, position[1] - 35, 200, 70),
    }

# 6. Data Soal
quiz_data = {
    "Buah": ["apel", "mangga", "jeruk", "nanas", "semangka", "melon", "rambutan", "anggur", "alpukat", "durian"],
    "Kendaraan": ["mobil", "motor", "bus", "kapal", "perahu", "pesawat", "sepeda", "skuter", "truk", "helikopter"],
    "Hewan": ["anjing", "kucing", "ayam", "bebek", "harimau", "singa", "kuda", "serigala", "burung", "ikan"],
    "Warna": ["merah", "orange", "kuning", "hijau", "biru", "ungu", "merah muda", "hitam", "putih"],
    "Random": ["meja", "kursi", "buku", "pensil", "topi", "sepatu", "gitar", "tas", "laptop", "kasur"],
}

# 7. Pop-up Gambar
right_popup = pygame.image.load("right.png")
wrong_popup = pygame.image.load("wrong.png")
congratulations = pygame.image.load("selamat.png")
try_again = pygame.image.load("nt.png")

# === Fungsi Pendukung ===
def show_popup(image, duration):
    return pygame.time.get_ticks() + duration * 200, image

# === Fungsi Halaman Kuis ===
def quiz_page(category_name):
    questions = quiz_data[category_name]
    random.shuffle(questions)  # Acak soal
    score = 0
    current_question = 0
    popup_time = 0
    popup_image = None

    category_page_image = f"pict.3page/page_{category_name.lower()}.png"

    while current_question < len(questions):
        question = questions[current_question]
        input_active = True
        user_input = ""

        while input_active:
            screen.fill((255, 255, 255))  # Bersihkan layar

            # Memuat gambar latar
            try:
                page_background = pygame.image.load(category_page_image)
                page_background = pygame.transform.scale(page_background, (screen_width, screen_height))
                screen.blit(page_background, (0, 0))
            except pygame.error:
                print(f"Image not found: {category_page_image}")

            # Tombol Back
            mouse_pos = pygame.mouse.get_pos()
            if back_button_rect.collidepoint(mouse_pos):
                screen.blit(back_button_hover, back_button_rect)
            else:
                screen.blit(back_button_default, back_button_rect)

            # Menampilkan gambar soal
            image_path = f"{category_name.lower()}_{question}.png"
            try:
                question_image = pygame.image.load(image_path)
                question_image = pygame.transform.smoothscale(question_image, (300, 300))
                screen.blit(question_image, (screen_width // 2 - 150, 130))
            except pygame.error:
                print(f"Image not found: {image_path}")

            # Tampilkan teks soal
            font = pygame.font.Font(None, 40)
            question_text = font.render("Apa nama objek ini?", True, (0, 50, 100))
            screen.blit(question_text, (screen_width // 2 - question_text.get_width() // 2, 430))

            # Input pengguna
            input_box = pygame.Rect(screen_width // 2 - 50, 500, 300, 50)
            pygame.draw.rect(screen, (255, 255, 255), input_box)
            input_text = font.render(user_input, True, (0, 0, 0))
            screen.blit(input_text, (input_box.x + 10, input_box.y + 10))

            # Tampilkan skor
            score_text = font.render(f"Skor: {score}", True, (0, 50, 100))
            screen.blit(score_text, (10, 10))

            # Tampilkan pop-up jika ada
            if popup_image and pygame.time.get_ticks() < popup_time:
                screen.blit(popup_image, (screen_width // 2 - popup_image.get_width() // 2, screen_height // 2 - popup_image.get_height() // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(mouse_pos):
                        return  # Kembali ke halaman kategori
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        if user_input.lower() == question.lower():
                            score += 1
                            popup_time, popup_image = show_popup(right_popup, 3)
                        else:
                            popup_time, popup_image = show_popup(wrong_popup, 3)
                        current_question += 1
                        input_active = False
                    else:
                        user_input += event.unicode

    # Tampilkan hasil akhir
    if score == len(questions):
        popup_time, popup_image = show_popup(try_again, 10)
    else:
        popup_time, popup_image = show_popup(congratulations, 10)

    while pygame.time.get_ticks() < popup_time:
        screen.fill((255, 255, 255))
        if popup_image:
            screen.blit(popup_image, (screen_width // 2 - popup_image.get_width() // 2, screen_height // 2 - popup_image.get_height() // 2))
        pygame.display.flip()



# === Fungsi Halaman Kategori ===
def category_page():
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(mouse_pos):
                    return
                for category, button in category_buttons.items():
                    if button["rect"].collidepoint(mouse_pos):
                        quiz_page(category)

        # Tampilkan tombol kategori
        screen.blit(category_background, (0, 0))
        for button in category_buttons.values():
            screen.blit(button["image"], button["rect"])

        if back_button_rect.collidepoint(mouse_pos):
            screen.blit(back_button_hover, back_button_rect)
        else:
            screen.blit(back_button_default, back_button_rect)

        pygame.display.flip()


# === Fungsi Menu Utama ===
def main_menu():
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(mouse_pos):
                    category_page()

        # Tampilkan halaman utama
        screen.blit(background_image, (0, 0))
        if start_button_rect.collidepoint(mouse_pos):
            screen.blit(start_button_hover, start_button_rect)
        else:
            screen.blit(start_button_default, start_button_rect)

        pygame.display.flip()


# === Menjalankan Program ===
if __name__ == "__main__":
    main_menu()


