from nicegui import ui
import pandas as pd
import string
import sqlite3

class Dictation:
    def __init__(self):
        self.index = 1
        self.user_answer = ""
        self.audio_player = None
        self.data = pd.DataFrame()  # Khởi tạo DataFrame rỗng
        self.selected_difficulty = None
        self.selected_topic = None
        self.notification_label = ui.label('').style('margin-top: 20px; font-size: 18px; color: black;')  # Khởi tạo label thông báo
        # Tạo các column cho từng trang
        
        self.difficulty_column = ui.column().style('width: 144%; height: 80px; padding: 20px;').classes('p-8 flex-1 items-center').style('background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);')
        self.topic_column = ui.column().style('width: 144%; height: 80px; padding: 20px;').classes('p-8 flex-1 items-center').style('background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);')
        self.dictation_column = ui.column().style('width: 144%; height: 80px; padding: 20px;').classes('p-8 flex-1 items-center').style('background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);')
        self.render_difficulty_page()  # Khởi động ứng dụng tại trang chọn độ khó

    def update_audio_file(self):
        #lấy file audio từ sql
        audio_file = self.get_audio_file_path()

        if self.audio_player:
            self.audio_player.delete()  # Xóa đối tượng âm thanh cũ

        # Tạo đối tượng âm thanh mới và hiển thị thanh điều khiển
        self.audio_player = ui.audio(audio_file).props('controls').style('width: 300px;')  
        self.audio_player.play()  # Phát âm thanh

    def normalize(self, text):
        return str(text).lower().translate(str.maketrans('', '', string.punctuation.replace("'", "")))

    def check_answer(self):
        user_words = self.normalize(self.user_answer).strip().split()
        correct_answer = self.get_correct_answer() # Lấy đáp án từ sql để so sánh với user_answer
        correct_words = self.normalize(correct_answer).strip().split()
        return user_words == correct_words

    def check_answer_click(self):
        if self.user_answer: # Nếu người người dùng đã nhập câu trả lời
            result = self.check_answer() # Kiểm tra đáp án
            if result:
                self.notification_label.text = 'Correct answer!'
                self.notification_label.style('color: green;')
                self.update_progress_status('correct')  # Cập nhật trạng thái cấu hỏi sang correct trên sql
            else:
                self.notification_label.text = 'Wrong answer!'
                self.notification_label.style('color: red;')
                self.update_progress_status('incorrect')  # Cập nhật trạng thái cấu hỏi sang incorrect trên sql
        else: # Nếu người người dùng chưa nhập câu trả lời, thông báo lỗi
            self.notification_label.text = 'Please enter your answer before checking.'
            self.notification_label.style('color: orange;')

    def show_answer(self):
        correct_answer = self.get_correct_answer() # Lấy đáp án từ sql
        self.notification_label.text = f"Answer: '{correct_answer}'"
        self.notification_label.style('color: green;')

    def skip(self):
        self.index = (self.index % 10) + 1  # Tăng chỉ số và quay lại đầu nếu vượt quá
        self.user_answer = "" # Xóa câu trả lời cũ
        self.input.value = ""  # Xóa ô nhập câu trả lời
        self.notification_label.text = ""  # Xóa nội dung thông báo
        self.update_audio_file()  # Cập nhật âm thanh cho câu tiếp theo
        self.no_sens.delete()
        self.no_sens = ui.label(f'({self.index}/10)').style('font-size: 18px;')

    def turnback(self):
        if self.index > 1:
            self.index -= 1
        else:
            self.index = 10
        self.user_answer = "" # Xóa câu trả lời cũ
        self.input.value = ""  # Xóa ô nhập câu trả lời
        self.notification_label.text = ""  # Xóa nội dung thông báo
        self.update_audio_file()  # Cập nhật âm thanh cho câu tiếp theo
        self.no_sens.delete()
        self.no_sens = ui.label(f'({self.index}/10)').style('font-size: 18px;')

    def go_to_topic_selection(self, difficulty):
        self.selected_difficulty = difficulty # Lưu độ khó đã chọn
        self.render_topic_page()  # Hiển thị trang chọn chủ đề

    def set_topic(self, topic):
        self.selected_topic = topic # Lưu chủ đề đã chọn
        self.index = 1
        self.render_dictation_page() # Hiển thị trang dictation

    def render_difficulty_page(self):
            self.difficulty_column.clear()  # Xóa nội dung cũ
            with self.difficulty_column:
                with ui.row().classes('w-full items-center gap-4 mb-6'):
                    ui.icon('school', size='32px').classes('text-pink-600')
                    ui.label('DICTATION').classes('text-2xl font-bold text-pink-600')
                ui.label('CHOOSE APPROPRIATE LEVEL').style('margin-bottom: 20px;').classes('text-2xl font-semibold text-gray-800')
                with ui.row().style('justify-content: center; margin: 10px 0;'):
                    ui.button('Easy', on_click=lambda: self.go_to_topic_selection('Easy')).props('rounded').style('margin: 10px; padding: 15px; font-size: 14px;').classes('bg-pink text-white')  # Căn giữa
                    ui.button('Hard', on_click=lambda: self.go_to_topic_selection('Hard')).props('rounded').style('margin: 10px; padding: 15px; font-size: 14px;').classes('bg-pink text-white')  # Căn giữa
            self.topic_column.clear()  # Xóa nội dung cũ
            self.dictation_column.clear()  # Xóa nội dung cũ
            self.difficulty_column.visible = True
            self.topic_column.visible = False
            self.dictation_column.visible = False

    def render_topic_page(self):
        self.topic_column.clear()  # Xóa nội dung cũ
        with self.topic_column:
            with ui.row().classes('w-full items-center gap-4 mb-6'):
                    ui.icon('school', size='32px').classes('text-pink-600')
                    ui.label('DICTATION').classes('text-2xl font-bold text-pink-600')
            #ui.label(f'Độ khó đã chọn: {self.selected_difficulty}').style('margin-bottom: 20px; font-size: 24px;')
            ui.label(f'DICTATION TOPIC').style('margin-bottom: 10px;').classes('text-2xl font-semibold text-gray-800')
        
            # Tạo hàng cho các nút chủ đề
            with ui.row().style('justify-content: center; margin: 10px 0;gap: 10px; flex-wrap: wrap;'):
                    if self.selected_difficulty == 'Easy':
                        ui.button('Topic 1', on_click=lambda: self.set_topic('Topic 1 - Easy')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md') 
                        ui.button('Topic 2', on_click=lambda: self.set_topic('Topic 2 - Easy')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')
                        ui.button('Topic 3', on_click=lambda: self.set_topic('Topic 3 - Easy')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')
                        ui.button('Topic 4', on_click=lambda: self.set_topic('Topic 4 - Easy')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')  
                        ui.button('Topic 5', on_click=lambda: self.set_topic('Topic 5 - Easy')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')
                    elif self.selected_difficulty == 'Hard':
                        ui.button('Topic 1', on_click=lambda: self.set_topic('Topic 1 - Hard')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')
                        ui.button('Topic 2', on_click=lambda: self.set_topic('Topic 2 - Hard')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')
                        ui.button('Topic 3', on_click=lambda: self.set_topic('Topic 3 - Hard')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')
                        ui.button('Topic 4', on_click=lambda: self.set_topic('Topic 4 - Hard')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')
                        ui.button('Topic 5', on_click=lambda: self.set_topic('Topic 5 - Hard')).props('rounded').classes('w-full bg-pink hover:bg-pink text-white font-semibold py-2 rounded-lg shadow-md')        
            
            # Nút Quay lại căn trái
            ui.button('Back', on_click=self.render_difficulty_page).props('rounded').style('margin: 10px 0; padding: 15px; font-size: 14px; align-self: flex-start;').classes('bg-pink text-white')
        self.difficulty_column.visible = False
        self.dictation_column.visible = False
        self.topic_column.visible = True

    def render_dictation_page(self):
        self.dictation_column.clear()  # Xóa nội dung cũ
        with self.dictation_column:
            with ui.row().classes('w-full items-center gap-4 mb-6'):
                    ui.icon('school', size='32px').classes('text-pink-600')
                    ui.label('DICTATION').classes('text-2xl font-bold text-pink-600')
            ui.label(f'Dictation: {self.selected_topic}').style('margin-bottom: 20px; font-size: 24px;').classes('font-semibold text-gray-800')
            with ui.row().style('justify-content: center; margin: 10px 0; align-items: center;'):
                ui.button(on_click=lambda: [self.turnback(), setattr(self.input, 'value', '')], icon='fast_rewind').props('rounded').style('width: 50px; height: 50px; padding: 0;').classes('bg-pink text-white')
                ui.button(on_click=lambda: [self.skip(), setattr(self.input, 'value', '')], icon='fast_forward').props('rounded').style('width: 50px; height: 50px; padding: 0;').classes('bg-pink text-white')
                self.update_audio_file()  # Cập nhật âm thanh
                self.no_sens = ui.label(f'({self.index+1}/10)').style('font-size: 18px;')
            self.input = ui.input('Enter your answer:', on_change=lambda: setattr(self, 'user_answer', self.input.value)).style('margin-bottom: 10px; font-size: 16px; width: 400px; padding: 10px;')
            # Hiển thị label thông báo ở đây
            self.notification_label = ui.label('').style('margin-top: 20px; font-size: 20px; color: black;')  # Khởi tạo label thông báo
            # Tạo hàng cho các nút
            with ui.row().style('justify-content: center; margin: 10px 0;'):
                ui.button('Check answer', on_click=self.check_answer_click).props('rounded').classes('bg-pink text-white')
                ui.button('Show answer', on_click=self.show_answer).props('rounded').classes('bg-pink text-white')
            with ui.row().style('justify-content: center; margin: 10px 0;'):
                ui.button('Choose dictation level', on_click=self.render_difficulty_page).props('rounded').classes('bg-pink text-white')
                ui.button('Choose dictation topic', on_click=self.render_topic_page).props('rounded').classes('bg-pink text-white')
        self.difficulty_column.visible = False
        self.topic_column.visible = False
        self.dictation_column.visible = True
        
    def get_connection(self):
        """Kết nối tới database."""
        return sqlite3.connect('path_to_database')

    def get_correct_answer(self):
        """Lấy câu trả lời đúng từ database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        question_name = f"(Q{self.index})"
        # Lấy user_id
        cursor.execute("SELECT user_id FROM user WHERE username = ?", ('user_name',))
        user_id = cursor.fetchone()
        if not user_id:
            conn.close()
            return "User not found"
        user_id = user_id[0]

        # Lấy topic_id
        cursor.execute("SELECT topic_id FROM dictation_topic WHERE topic_name = ?", (self.selected_topic,))
        topic_id = cursor.fetchone()
        if not topic_id:
            conn.close()
            return "Topic not found"
        topic_id = topic_id[0]

        # Lấy question_id
        cursor.execute(
            "SELECT question_id FROM dictation_question WHERE question_name = ? AND topic_id = ?", 
            (question_name, topic_id)
        )
        question_id = cursor.fetchone()
        if not question_id:
            conn.close()
            return "Question not found"
        question_id = question_id[0]

        # Lấy correct_answer
        cursor.execute("SELECT correct_answer FROM dictation_question WHERE question_id = ?", (question_id,))
        correct_answer = cursor.fetchone()

        conn.close()

        if correct_answer:
            return correct_answer[0]
        return "Correct answer not found"

    def get_audio_file_path(self):
        """Lấy đường dẫn file audio từ database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        question_name = f"(Q{self.index})"
        # Lấy user_id
        cursor.execute("SELECT user_id FROM user WHERE username = ?", ('user_name',))
        user_id = cursor.fetchone()
        if not user_id:
            conn.close()
            return "User not found"
        user_id = user_id[0]

        # Lấy topic_id
        cursor.execute("SELECT topic_id FROM dictation_topic WHERE topic_name = ?", (self.selected_topic,))
        topic_id = cursor.fetchone()
        if not topic_id:
            conn.close()
            return "Topic not found"
        topic_id = topic_id[0]

        # Lấy question_id
        cursor.execute(
            "SELECT question_id FROM dictation_question WHERE question_name = ? AND topic_id = ?", 
            (question_name, topic_id)
        )
        question_id = cursor.fetchone()
        if not question_id:
            conn.close()
            return "Question not found"
        question_id = question_id[0]

        # Lấy audio_file_path
        cursor.execute("SELECT audio_file_path FROM dictation_question WHERE question_id = ?", (question_id,))
        audio_file_path = cursor.fetchone()

        conn.close()

        if audio_file_path:
            return audio_file_path[0]
        return "Audio file path not found"

    def update_progress_status(self, new_status):
        """Cập nhật trạng thái tiến độ của một câu hỏi."""
        conn = self.get_connection()
        cursor = conn.cursor()
        question_name = f"(Q{self.index})"
        # Lấy user_id
        cursor.execute("SELECT user_id FROM user WHERE username = ?", ('user_name',))
        user_data = cursor.fetchone()
        if not user_data:
            print(f"User '{'user_name'}' không tồn tại.")
            conn.close()
            return
        user_id = user_data[0]

        # Lấy topic_id
        cursor.execute("SELECT topic_id FROM dictation_topic WHERE topic_name = ?", (self.selected_topic,))
        topic_data = cursor.fetchone()
        if not topic_data:
            print(f"Topic not found.")
            conn.close()
            return
        topic_id = topic_data[0]

        # Lấy question_id
        cursor.execute(
            "SELECT question_id FROM dictation_question WHERE question_name = ? AND topic_id = ?", 
            (question_name, topic_id)
        )
        question_data = cursor.fetchone()
        if not question_data:
            print(f"Câu hỏi '{question_name}' không tồn tại trong topic '{self.selected_topic}'.")
            conn.close()
            return
        question_id = question_data[0]

        # Cập nhật trạng thái
        cursor.execute(
            """
            UPDATE user_question_progress
            SET status = ?, attempt_date = CURRENT_TIMESTAMP
            WHERE user_id = ? AND topic_id = ? AND question_id = ?
            """, 
            (new_status, user_id, topic_id, question_id)
        )

        conn.commit()
        conn.close()

        print(f"Đã cập nhật trạng thái câu hỏi '{question_name}' của người dùng '{'user_name'}'.")

Dictation()
ui.run()
