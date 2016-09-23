#! /usr/bin/python
import os

try:
    from pyfiglet import figlet_format
except:
    figlet_format = lambda x: x


def clear_screen():
    os.system('clear')


def read_input(st):
    try:
        return input(st)
    except SyntaxError:
        return ''


def render_title(story):
    clear_screen()
    print('')
    print('')
    print('')
    print('')
    print(figlet_format(story.title))
    print('')
    print('')
    read_input('<press enter to continue>')

def render_page(story, story_code, choices_code):
    if story_code not in story.stories:
        raise ValueError('Invalid Story Code : %s' % story_code)
    if choices_code not in story.choices:
        raise ValueError('Invalid Choices Code : %s' % choices_code)
    print('')
    print('')
    print(story.stories[story_code])
    print('')
    print('')
    choices = story.choices[choices_code]
    for i, c in enumerate(choices):
        print ('%s - %s' % (i+1, c.text))

    input_st = read_input('Please enter the number of your choice: ')
    try:
        input_num = int(input_st)
    except ValueError:
        clear_screen()
        print('!!! Not a number: "{0}" (Please enter a number instead)'.format(
            input_st))
        print('')
        print('')
        return render_page(story, story_code, choices_code)

    if input_num < 1 or input_num > len(choices):
        clear_screen()
        print('Please enter a number between 1 and {0}'.format(
            len(choices)))
        print('')
        print('')
        return render_page(story, story_code, choices_code)

    return choices[input_num-1]


def render_end(story, story_code):
    if story_code not in story.stories:
        raise ValueError('Invalid Story Code : %s' % story_code)
    print('')
    print('')
    print(story.stories[story_code])
    print('')
    print('')
    print(figlet_format('THE END'))

def start(story):
    render_title(story)
    current_story = story.start_story_code
    current_choice = story.start_choices_code
    choice = None
    while True:
        clear_screen()

        choice = render_page(story, current_story, current_choice)
        if choice.choice_code == 'end':
            clear_screen()
            render_end(story, choice.story_code)
            return
        else:
            current_story = choice.story_code
            current_choice = choice.choice_code
