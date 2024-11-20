import requests
import random
import re

# Dictionary để lưu trữ các album flashcard 
albums = {}

# Data
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


class FlashcardManager:
    def __init__(self):
        self.albums = albums
        self.topic_flashcards = topic_flashcards

    # Lấy danh sách các chủ đề
    def get_topics(self):
        return list(self.topic_flashcards.keys())

    # Lấy các thẻ flashcard theo chủ đề
    def get_cards_for_topic(self, topic):
        return self.topic_flashcards.get(topic, [])

    # Đếm số lượng thẻ flashcard trong một chủ đề
    def get_card_count(self, topic):
        return len(self.topic_flashcards.get(topic, []))
