from nicegui import ui
from backend import FlashcardManager
from typing import List, Dict, Optional

class FlashcardStudyPanel:
    def __init__(self):
        self.flashcard_manager = FlashcardManager()
        self.current_topic: Optional[str] = None
        self.cards: List[Dict[str, str]] = []
        self.current_index: int = 0
        self.is_flipped: bool = False
        self.ui_elements: Dict = {}
        self.main_container = ui.column().classes('w-full min-h-screen items-center p-4') \
                .style('width: 144%; height: 80px; padding: 20px;').classes('p-8 flex-1').style('background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);')
        
        # Create containers for different views
        with self.main_container:
            self.topic_view = ui.column().classes('w-full max-w-4xl items-center gap-4')
            self.flashcard_view = ui.column().classes('w-full max-w-4xl items-center gap-4')
            self.flashcard_view.visible = False
            
        self.setup_topic_view()
        self.setup_flashcard_view()

    def setup_topic_view(self) -> None:
        """Initialize the topic selection view."""
        with self.topic_view:
            with ui.row().classes('w-full items-center gap-4 mb-6'):
                ui.icon('school', size='32px').classes('text-pink-600')
                ui.label('FLASHCARD STUDY').classes('text-2xl font-bold text-pink-600')
            
            # Topic Selection Grid
            with ui.grid(columns=3).classes('w-full gap-4'):
                self._create_topic_cards()

    def _create_topic_cards(self) -> None:
        """Create topic selection cards with study statistics."""
        for topic in self.flashcard_manager.get_topics():
            with ui.card().classes('hover:shadow-lg transition-shadow duration-200'):
                with ui.column().classes('p-4 gap-2'):
                    ui.label(topic).classes('text-xl font-semibold text-gray-800')
                    word_count = self.flashcard_manager.get_card_count(topic)
                    ui.label(f'{word_count} cards').classes('text-sm text-gray-600')
                    ui.button(
                        'Study Now',
                        on_click=lambda t=topic: self.show_flashcard_view(t)
                    ).props('rounded').classes('bg-pink text-white px-4 py-2 hover:bg-pink-700')

    def setup_flashcard_view(self) -> None:
        """Initialize the flashcard study view (initially hidden)."""
        with self.flashcard_view:
            # Topic header (will be updated when a topic is selected)
            self.ui_elements['topic_header'] = ui.label().classes('text-xl font-bold text-gray-700 mb-4')
            
            # Flashcard container
            self.ui_elements['flashcard_container'] = ui.card().classes('w-full max-w-2xl h-96 mb-4')
            
            with self.ui_elements['flashcard_container']:
                self._create_flashcard_content()
                self._create_navigation_controls()

            # Back to topics button
            ui.button(
                'Back to Topics',
                on_click=self.show_topic_view
            ).props('rounded').classes('bg-pink text-white px-6 py-2 rounded-lg hover:bg-pink-700')

    def _create_flashcard_content(self) -> None:
        """Create the flashcard content area with front and back faces."""
        self.ui_elements['card'] = ui.card().classes('w-full h-full cursor-pointer relative')
        
        with self.ui_elements['card']:
            # Front face
            self.ui_elements['front'] = ui.column().classes(
                'w-full h-full flex items-center justify-center p-8'
            )
            with self.ui_elements['front']:
                self.ui_elements['word'] = ui.label().classes('text-2xl font-bold mb-4')
                ui.label('Click to flip').classes('text-sm text-gray-500')
            
            # Back face
            self.ui_elements['back'] = ui.column().classes(
                'w-full h-full items-center justify-center p-8 bg-pink-50'
            )
            with self.ui_elements['back']:
                self.ui_elements['info'] = ui.label().classes('text-xl text-center')

        # Set up flip handler
        self.ui_elements['card'].on('click', self.flip_card)

    def _create_navigation_controls(self) -> None:
        """Create navigation buttons and progress indicator."""
        with ui.row().classes('w-full justify-between items-center mt-4 px-4'):
            self.ui_elements['prev_btn'] = ui.button(
                'Previous',
                on_click=self.previous_card
            ).props('rounded').classes('bg-pink text-white px-4 py-2  hover:bg-pink-700')
            
            self.ui_elements['progress'] = ui.label().classes('text-gray-600')
            
            self.ui_elements['next_btn'] = ui.button(
                'Next',
                on_click=self.next_card
            ).props('rounded').classes('bg-pink text-white px-4 py-2 hover:bg-pink-700')

    def show_flashcard_view(self, topic: str) -> None:
        """Switch to flashcard view and load the selected topic."""
        self.current_topic = topic
        self.cards = self.flashcard_manager.get_cards_for_topic(topic)
        self.current_index = 0
        self.is_flipped = False
        
        # Update UI
        self.ui_elements['topic_header'].text = f'Studying: {topic}'
        self.topic_view.visible = False
        self.flashcard_view.visible = True
        self.update_card_display()

    def show_topic_view(self) -> None:
        """Switch back to topic selection view."""
        self.flashcard_view.visible = False
        self.topic_view.visible = True
        self.current_topic = None
        self.cards = []

    def update_card_display(self) -> None:
        """Update the flashcard display with current card content."""
        if not self.cards:
            return

        current_card = self.cards[self.current_index]
        self.ui_elements['word'].text = current_card['word']
        self.ui_elements['info'].text = current_card['info']
        self.ui_elements['progress'].text = f'Card {self.current_index + 1} of {len(self.cards)}'

        # Update navigation buttons state
        self.ui_elements['prev_btn'].disable() if self.current_index == 0 else self.ui_elements['prev_btn'].enable()
        self.ui_elements['next_btn'].disable() if self.current_index == len(self.cards) - 1 else self.ui_elements['next_btn'].enable()

        # Reset to front face
        # Reset card to front face
        self.ui_elements['front'].style('display: flex')
        self.ui_elements['back'].style('display: none')
        self.is_flipped = False
        #self._show_front()

    def flip_card(self) -> None:
        """Toggle between front and back of the flashcard."""
        if self.is_flipped:
            self._show_front()
        else:
            self._show_back()
        self.is_flipped = not self.is_flipped

    def _show_front(self) -> None:
        """Show the front face of the flashcard."""
        self.ui_elements['front'].style('display: flex')
        self.ui_elements['back'].style('display: none')

    def _show_back(self) -> None:
        """Show the back face of the flashcard."""
        self.ui_elements['front'].style('display: none')
        self.ui_elements['back'].style('display: flex')
    
    def next_card(self) -> None:
        """Move to the next flashcard."""
        if self.current_index < len(self.cards) - 1:
            self.current_index += 1
            self.update_card_display()

    def previous_card(self) -> None:
        """Move to the previous flashcard."""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_card_display()

def main():
    FlashcardStudyPanel()
    ui.run(title='Flashcard Study App')

if __name__ in {"__main__", "__mp_main__"}:
    main()