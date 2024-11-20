from flask import Flask
from nicegui import ui
import os
from functools import partial

app = Flask(__name__)

def load_stories_from_file(filename):
    stories = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            current_title = None
            current_content = []
            current_questions = []

            for line in file:
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                if line.startswith("Title:"):
                    if current_title and current_content:
                        stories[current_title] = {
                            "content": current_content,
                            "questions": current_questions
                        }

                    current_title = line[6:].strip()
                    current_content = []
                    current_questions = []  # Reset for new story
                elif line.startswith("Question:"):
                    question_text = line[9:].strip()
                    try:
                        options = next(file).strip().split(';')  # Expect options on the next line
                        answer = next(file).strip()  # Expect the correct answer on the line after options
                        current_questions.append({
                            "question": question_text,
                            "options": options,
                            "answer": answer
                        })
                    except StopIteration:
                        print(f"Error: Incomplete question data for '{question_text}'.")
                        break  # Stop processing further questions
                else:
                    current_content.append(line)

            if current_title and current_content:
                stories[current_title] = {
                    "content": current_content,
                    "questions": current_questions
                }

    except FileNotFoundError:
        print(f"File {filename} not found.")
    return stories

def load_stories_from_multiple_files(filenames):
    all_stories = {}
    for filename in filenames:
        file_stories = load_stories_from_file(filename)
        if file_stories:  # Only add if there are valid stories
            all_stories.update(file_stories)
        else:
            print(f"No valid stories found in {filename}.")
    print("Loaded Stories:", all_stories)  # Debug print to verify loaded stories
    return all_stories

current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
file_list = [
    os.path.join(current_dir, 'alo.txt'),
    os.path.join(current_dir, 'alo1.txt'),
    os.path.join(current_dir, 'alo2.txt'),
    os.path.join(current_dir, 'alo3.txt')
]
stories = load_stories_from_multiple_files(file_list)


@ui.page('/')
def main_page():
    # Set the background gradient for the main page
    with ui.column().classes('w-full min-h-screen items-center p-4') \
                .style('background: linear-gradient(135deg, #f0f4ff, #e5e7ff)'):
    
    # Main content section
        with ui.card().classes('w-full max-w-3xl p-6 mt-8 items-center'):
            with ui.row().classes('w-full items-center gap-4 mb-6'):
                ui.icon('school', size='32px').classes('text-indigo-600')
                ui.label('READING').classes('text-2xl font-bold text-indigo-600')
            with ui.row().style('justify-content: center; margin: 10px 0;gap: 10px; flex-wrap: wrap;'): 
                for category in ['Short Stories', 'Articles', 'News']:
                    # Create links for each category
                    ui.link(category, f'/{category.lower().replace(" ", "-")}').classes('w-full bg-indigo hover:bg-indigo-600 text-white font-semibold py-2 rounded-lg shadow-md no-underline text-center')
                    

@ui.page('/short-stories')
def short_stories_page():
    with ui.column().classes('w-full min-h-screen items-center p-4') \
                .style('background: linear-gradient(135deg, #f0f4ff, #e5e7ff)'):
        # Main container for better layout
        with ui.column().classes('max-w-4xl mx-auto p-6 bg-gray-50 rounded-lg shadow-lg'):
            # Stories section header
            ui.label('List of Stories').classes('text-3xl font-bold text-gray-800 mb-4 text-center')
            ui.separator().classes('my-4')

            # Grid layout for stories
            with ui.grid().classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'):
                for story_title in stories.keys():
                    # Card for each story
                    with ui.card().classes('bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-200'):
                        # Title as link
                        ui.link(story_title, f'/story/{story_title}').classes(
                            'block text-xl font-semibold text-indigo-600 hover:text-indigo-800 py-4 px-6 no-underline'
                        )
                        # Check if description exists, and add it if it does
                        description = stories[story_title].get('description', 'No description available.')
                        ui.label(description[:100] + '...').classes(
                            'text-gray-600 px-6 pb-4'
                        )

#@ui.page('/short-stories')
#def short_stories_page():
#    # Stories section
#    with ui.card().classes('w-full mt-4'):
#        ui.label('List of Stories').classes('text-2xl font-semibold text-gray-700')
#        ui.separator().classes('my-2')
#        for story_title in stories.keys():
#            ui.link(story_title, f'/story/{story_title}').classes('bg-indigo hover:bg-indigo text-white font-semibold py-2 rounded-lg shadow-md text-center no-underline')
        
@ui.page('/story/{story_title}')
def show_story(story_title):
    story = stories.get(story_title, None)
    if story:
        story_content = story["content"]
        story_questions = story["questions"]
        
        # Create a styled container for the story
        with ui.column().classes('w-full min-h-screen items-center p-4') \
                .style('background: linear-gradient(135deg, #f0f4ff, #e5e7ff)'):
            with ui.column().classes('max-w-4xl mx-auto p-6 bg-gray-50 rounded-lg shadow-lg'):
            #with ui.card().classes('p-4 rounded-lg shadow-md'):
                ui.label(f"Story: {story_title}").classes('text-2xl font-bold mb-4')
                ui.label("\n".join(story_content)).classes('text-lg mb-4')
        
        # Pass the specific questions for this story
            show_exercise(story_questions)
    else:
        print(f"Story '{story_title}' not found in loaded stories.")

def create_check_answer_function(question_item, feedback_label):
    def check_answer(user_answer):
        correct_answer = question_item["answer"]
        
        # Clear previous classes to ensure feedback color updates correctly
        feedback_label.classes('')  # Clears all previously set classes
        
        if user_answer.lower() == correct_answer.lower():
            feedback_label.set_text("✓ Correct!")
            feedback_label.classes('text-lg text-green-500')
        else:
            feedback_label.set_text(f"✗ Incorrect! The correct answer was: {correct_answer}")
            feedback_label.classes('text-lg text-red-500')
    
    return check_answer

def show_exercise(story_questions):
    with ui.column().classes('w-full min-h-screen items-center p-4') \
                .style('background: linear-gradient(135deg, #f0f4ff, #e5e7ff)'):
        with ui.column().classes('max-w-4xl mx-auto p-6 bg-gray-50 rounded-lg shadow-lg'):
        #with ui.column().classes('space-y-4'):
        # Display each question in the story
            for question_item in story_questions:
                ui.label(question_item["question"]).classes('text-xl font-semibold mb-2')  # Question text
            
                with ui.column().classes('w-full mb-2'):
                    feedback_label = ui.label('').classes('text-lg mt-2')  # Separate label for each feedback below the select
                    check_answer_function = create_check_answer_function(question_item, feedback_label)
                
                    ui.select(
                        options=question_item["options"],  # List of options
                        label='Choose an answer',
                        on_change=lambda e, check_func=check_answer_function: check_func(e.value)  # Call the specific check_answer function
                    ).classes('w-full mb-2 bg-gray-100 border border-gray-300 rounded-md p-2')  # Styled dropdown

                    # Position the feedback label immediately below the dropdown menu
                    feedback_label.classes('text-lg mt-2')  # Adds spacing between answer and feedback


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='Reading Platform',)
