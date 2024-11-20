import requests
import random
import re
from nicegui import ui

albums = {}  # Dictionary để lưu trữ các album flashcard
topic_flashcards = {
    "Nghề nghiệp": [
        {"word": "chef (n)", "info": "đầu bếp"},
        {"word": "comedian (n)", "info": "diễn viên hài"},
        {"word": "delivery man (n)", "info": "nhân viên giao hàng"},
        {"word": "doctor (n)", "info": "bác sĩ"},
        {"word": "entrepreneur (n)", "info": "nhà kinh doanh"},
        {"word": "engineer (n)", "info": "kỹ sư"},
        {"word": "factory worker (n)", "info": "công nhân nhà máy"},
        {"word": "office worker (n)", "info": "nhân viên văn phòng"},
        {"word": "florist (n)", "info": "người bán hoa"},
        {"word": "hairdresser (n)", "info": "thợ cắt tóc"},
    ],
    "Trái cây": [
        {"word": "pear (n)", "info": "quả lê"},
        {"word": "grape (n)", "info": "quả nho"},
        {"word": "peach (n)", "info": "quả đào"},
        {"word": "orange (n)", "info": "quả cam"},
        {"word": "mango (n)", "info": "quả xoài"},
        {"word": "coconut (n)", "info": "quả dừa"},
        {"word": "pineapple (n)", "info": "quả dứa"},
        {"word": "watermelon (n)", "info": "dưa hấu"},
        {"word": "durian (n)", "info": "sầu riêng"},
        {"word": "lychee (n)", "info": "quả vải"},
        {"word": "guava (n)", "info": "quả ổi"},
        {"word": "starfruit (n)", "info": "quả khế"},
    ],
    "Gia đình": [
        {"word": "parent (n)", "info": "bố hoặc mẹ"},
        {"word": "daughter (n)", "info": "con gái"},
        {"word": "son (n)", "info": "con trai"},
        {"word": "sibling (n)", "info": "anh chị em ruột"},
        {"word": "sister (n)", "info": "chị, em gái"},
        {"word": "brother (n)", "info": "anh, em trai"},
        {"word": "grandmother (n)", "info": "bà nội (ngoại)"},
        {"word": "grandfather (n)", "info": "ông nội (ngoại)"},
        {"word": "grandparent (n)", "info": "ông hoặc bà"},
        {"word": "relative (n)", "info": "họ hàng"},
        {"word": "aunt (n)", "info": "cô, dì"},
        {"word": "uncle (n)", "info": "chú, bác, cậu, dượng"},
    ],
    "Động Vật": [
        {"word": "mouse (n)", "info": "con chuột"},
        {"word": "cat (n)", "info": "con mèo"},
        {"word": "dog (n)", "info": "con chó"},
        {"word": "kitten (n)", "info": "mèo con"},
        {"word": "puppy (n)", "info": "chó con"},
        {"word": "pig (n)", "info": "con lợn, heo"},
        {"word": "chicken (n)", "info": "con gà"},
        {"word": "duck (n)", "info": "con vịt"},
        {"word": "goose (n)", "info": "con ngỗng"},
        {"word": "turkey (n)", "info": "con gà tây"},
        {"word": "stork (n)", "info": "con cò"},
        {"word": "swan (n)", "info": "thiên nga"},
    ],
    "Rau Quả": [
        {"word": "bean (n)", "info": "hạt đậu"},
        {"word": "pea (n)", "info": "đậu Hà Lan"},
        {"word": "cabbage (n)", "info": "bắp cải"},
        {"word": "carrot (n)", "info": "củ cà rốt"},
        {"word": "corn (n)", "info": "ngô, bắp"},
        {"word": "cucumber (n)", "info": "dưa chuột"},
        {"word": "tomato (n)", "info": "quả cà chua"},
        {"word": "garlic (n)", "info": "tỏi"},
        {"word": "onion (n)", "info": "củ hành"},
        {"word": "spring onion (n)", "info": "hành lá"},
        {"word": "ginger (n)", "info": "củ gừng"},
        {"word": "turmeric (n)", "info": "củ nghệ"},
        {"word": "potato (n)", "info": "khoai tây"},
        {"word": "sweet potato (n)", "info": "khoai lang"},
    ],
    "Đồ Ăn": [
        {"word": "soup (n)", "info": "món súp, món canh"},
        {"word": "salad (n)", "info": "rau trộn, nộm rau"},
        {"word": "bread (n)", "info": "bánh mì"},
        {"word": "sausage (n)", "info": "xúc xích"},
        {"word": "hot dog (n)", "info": "bánh mỳ kẹp xúc xích"},
        {"word": "bacon (n)", "info": "thịt xông khói"},
        {"word": "ham (n)", "info": "thịt giăm bông"},
        {"word": "egg (n)", "info": "trứng"},
        {"word": "pork (n)", "info": "thịt lợn"},
        {"word": "beef (n)", "info": "thịt bò"},
        {"word": "chicken (n)", "info": "thịt gà"},
        {"word": "duck (n)", "info": "thịt vịt"},
        {"word": "lamb (n)", "info": "thịt cừu"},
        {"word": "ribs (n)", "info": "sườn"},
    ],
    "Động tác cơ thể": [
        {"word": "tiptoe (v)", "info": "đi nhón chân"},
        {"word": "jump (v)", "info": "nhảy"},
        {"word": "leap (v)", "info": "nhảy vọt, nhảy xa"},
        {"word": "stand (v)", "info": "đứng"},
        {"word": "sit (v)", "info": "ngồi"},
        {"word": "lean (v)", "info": "dựa, tựa"},
        {"word": "wave (v)", "info": "vẫy tay"},
        {"word": "clap (v)", "info": "vỗ tay"},
        {"word": "point (v)", "info": "chỉ, trỏ"},
        {"word": "catch (v)", "info": "bắt, đỡ"},
        {"word": "stretch (v)", "info": "vươn (vai..), ưỡn lưng"},
        {"word": "push (v)", "info": "đẩy"},
        {"word": "pull (v)", "info": "kéo"},
        {"word": "crawl (v)", "info": "bò, trườn"},
    ],
    'Bộ phận cơ thế': [
    {"word": "head (n)", "info": "đầu"},
    {"word": "hair (n)", "info": "tóc"},
    {"word": "face (n)", "info": "gương mặt"},
    {"word": "forehead (n)", "info": "trán"},
    {"word": "eyebrow (n)", "info": "lông mày"},
    {"word": "eye (n)", "info": "mắt"},
    {"word": "eyelash (n)", "info": "lông mi"},
    {"word": "nose (n)", "info": "mũi"},
    {"word": "ear (n)", "info": "tai"},
    {"word": "cheek (n)", "info": "má"} 
    ],
    'Trường học': [
    {"word": "school (n)", "info": "trường học"},
    {"word": "class (n)", "info": "lớp học"},
    {"word": "student (n)", "info": "học sinh, sinh viên"},
    {"word": "pupil (n)", "info": "học sinh"},
    {"word": "teacher (n)", "info": "giáo viên"},
    {"word": "principal (n)", "info": "hiệu trưởng"},
    {"word": "course (n)", "info": "khóa học"},
    {"word": "semester (n)", "info": "học kì"},
    {"word": "exercise (n)", "info": "bài tập"},
    {"word": "homework (n)", "info": "bài tập về nhà"}
    ],
    'Tính cách': [
    {"word": "active (adj)", "info": "năng nổ, lanh lợi"},
    {"word": "alert (adj)", "info": "tỉnh táo, cảnh giác"},
    {"word": "ambitious (adj)", "info": "tham vọng"},
    {"word": "attentive (adj)", "info": "chăm chú, chú tâm"},
    {"word": "bold (adj)", "info": "táo bạo, mạo hiểm"},
    {"word": "brave (adj)", "info": "dũng cảm, gan dạ"},
    {"word": "careful (adj)", "info": "cẩn thận, thận trọng"},
    {"word": "careless (adj)", "info": "bất cẩn, cẩu thả"},
    {"word": "cautious (adj)", "info": "thận trọng, cẩn thận"},
    {"word": "conscientious (adj)", "info": "chu đáo, tỉ mỉ"},
    {"word": "courageous (adj)", "info": "can đảm"}
    ],
    'Đồ dùng học tập': 
    [
    {"word": "pen (n)", "info": "bút mực"},
    {"word": "pencil (n)", "info": "bút chì"},
    {"word": "highlighter (n)", "info": "bút nhớ"},
    {"word": "ruler (n)", "info": "thước kẻ"},
    {"word": "eraser (n)", "info": "tẩy, gôm"},
    {"word": "pencil case (n)", "info": "hộp bút"},
    {"word": "book (n)", "info": "quyển sách"},
    {"word": "notebook (n)", "info": "vở"},
    {"word": "paper (n)", "info": "giấy"},
    {"word": "scissors (n)", "info": "kéo"}
     ],
    'Thiên nhiên ': [
    {"word": "forest (n)", "info": "rừng"},
    {"word": "rainforest (n)", "info": "rừng mưa nhiệt đới"},
    {"word": "mountain (n)", "info": "núi, dãy núi"},
    {"word": "highland (n)", "info": "cao nguyên"},
    {"word": "hill (n)", "info": "đồi"},
    {"word": "valley (n)", "info": "thung lũng, châu thổ, lưu vực"},
    {"word": "cave (n)", "info": "hang động"},
    {"word": "rock (n)", "info": "đá"},
    {"word": "slope (n)", "info": "dốc"},
    {"word": "volcano (n)", "info": "núi lửa"}
    ],
    'Du lịch': [
    {"word": "travel (v)", "info": "đi du lịch"},
    {"word": "depart (v)", "info": "khởi hành"},
    {"word": "leave (v)", "info": "rời đi"},
    {"word": "arrive (v)", "info": "đến nơi"},
    {"word": "airport (n)", "info": "sân bay"},
    {"word": "take off (v)", "info": "cất cánh"},
    {"word": "land (v)", "info": "hạ cánh"},
    {"word": "check in (v)", "info": "đăng ký phòng ở khách sạn"},
    {"word": "check out (v)", "info": "trả phòng khách sạn"},
    {"word": "visit (v)", "info": "thăm viếng"}
]
}

class FlashcardStudyPanel:
    def __init__(self):
        self.current_topic = None
        self.cards = []
        self.current_index = 0
        self.is_flipped = False
        self.setup_ui()
        
    def setup_ui(self):
        with ui.column().classes('w-full min-h-screen items-center p-4') \
                .style('background: linear-gradient(135deg, #f0f4ff, #e5e7ff)'):
            with ui.column().classes('w-full items-center gap-4 mb-6'):    
                ui.label('FLASHCARD').classes('text-2xl font-bold text-indigo-600')
            
            # Topic Selection Grid
                with ui.grid(columns=3).classes('gap-4'):
                    for topic in topic_flashcards.keys():
                        with ui.card().style('cursor: pointer'):
                            with ui.column().classes('p-4'):
                                ui.label(topic).classes('text-lg font-semibold mb-2')
                                word_count = len(topic_flashcards[topic])
                                ui.label(f'{word_count} words').style('color: gray')
                                ui.button(
                                    'Study Now', 
                                    on_click=lambda t=topic: self.load_topic(t)
                                ).style('padding: 8px 16px; border-radius: 8px; margin-top: 16px').props('rounded').classes('bg-indigo text-white')
            

            # Flashcard Display (initially hidden)
                self.flashcard_container = ui.card().style('width: 50%; height: 400px; display: none')
            
                with self.flashcard_container:
                    self.current_card = ui.card().style('width: 100%; height: 100%; cursor: pointer; position: relative')
                
                    with self.current_card:
                        # Front face
                        self.front_face = ui.column().style('width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; padding: 32px')
                        with self.front_face:
                            self.word_label = ui.label().style('font-size: 24px; font-weight: bold; margin-bottom: 16px')
                            ui.label('Click to flip').style('color: gray; font-size: 14px')
                    
                        # Back face (initially hidden)
                        self.back_face = ui.column().style('width: 100%; height: 100%; display: none; align-items: center; justify-content: center; padding: 32px; background-color: #e5e7ff')
                        with self.back_face:
                            self.info_label = ui.label().style('font-size: 20px; text-align: center')

                    # Navigation controls
                    with ui.row().classes('w-full justify-between mt-4 px-4'):
                        self.prev_button = ui.button('Previous', on_click=self.previous_card
                        ).style('padding: 8px 24px; border-radius: 8px').props('rounded').classes('bg-indigo text-white')
                    
                        self.progress_label = ui.label().style('color: gray')
                    
                        self.next_button = ui.button('Next', on_click=self.next_card
                        ).style('padding: 8px 24px; border-radius: 8px').props('rounded').classes('bg-indigo text-white')
                    
                    # Back to topics button
                    with ui.row().classes('w-full justify-center mt-4'):
                        ui.button('Back to Topics',on_click=self.back_to_topics
                        ).style('padding: 8px 24px; border-radius: 8px').props('rounded').classes('bg-indigo text-white')

            # Set up card flip event handler
            self.current_card.on('click', self.flip_card)

    def load_topic(self, topic: str):
        """Load flashcards for the selected topic."""
        self.current_topic = topic
        self.cards = topic_flashcards[topic]
        self.current_index = 0
        self.is_flipped = False
        self.flashcard_container.style('display: block')
        self.update_card_display()

    def update_card_display(self):
        """Update the current flashcard display."""
        if not self.cards:
            return
            
        current_card = self.cards[self.current_index]
        self.word_label.text = current_card['word']
        self.info_label.text = current_card['info']
        self.progress_label.text = f'Card {self.current_index + 1} of {len(self.cards)}'
        
        # Update navigation buttons state
        self.prev_button.disable() if self.current_index == 0 else self.prev_button.enable()
        self.next_button.disable() if self.current_index == len(self.cards) - 1 else self.next_button.enable()
        
        # Reset card to front face
        self.front_face.style('display: flex')
        self.back_face.style('display: none')
        self.is_flipped = False

    def flip_card(self):
        """Toggle the flashcard flip animation."""
        if self.is_flipped:
            self.front_face.style('display: flex')
            self.back_face.style('display: none')
        else:
            self.front_face.style('display: none')
            self.back_face.style('display: flex')
        self.is_flipped = not self.is_flipped

    def next_card(self):
        """Move to the next flashcard."""
        if self.current_index < len(self.cards) - 1:
            self.current_index += 1
            self.update_card_display()

    def previous_card(self):
        """Move to the previous flashcard."""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_card_display()

    def back_to_topics(self):
        """Return to topic selection."""
        self.flashcard_container.style('display: none')
        self.current_topic = None
        self.cards = []

def main():
    FlashcardStudyPanel()
    ui.run(title='Flashcard Study App')

if __name__ in {"__main__", "__mp_main__"}:
    main()