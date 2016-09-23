from collections import namedtuple

Choice = namedtuple('Choice', ['text', 'story_code', 'choice_code'])
Story = namedtuple('Story', ['title', 'stories', 'choices',
                             'start_story_code', 'start_choices_code'])

# stars::Int
# zero means it is text
# 'content'
Token = namedtuple('Token', ['stars', 'content'])


def read_stars(st):
    """Reads stars from current line and returns the rest of line."""
    star_num = 0
    rest = st
    while rest.startswith('*'):
        star_num += 1
        rest = rest[1:]
    return (star_num, rest.strip())


def get_content(stars, token):
        if token is None or token.stars != stars:
            raise Exception('Expected %s star token: %s' % (stars, token))
        else:
            return token.content


def read_next_token(stars, tokens):
    return get_content(stars, next(tokens, None))


def iter_tokens(lines):
    current_stars = None
    current = []
    for l in lines:
        (star_num, rest) = read_stars(l)
        if star_num == current_stars == 0:
            current.append(rest)
        else:
            # this will remove start values
            if current_stars is not None:
                yield Token(stars=current_stars, content='\n'.join(current))
            current_stars = star_num
            current = [rest]


def get_choices_list(tokens):
    resp = []
    token = next(tokens, None)
    while (token is not None) and token.stars > 3:
        text = get_content(4, token)
        story_code = read_next_token(5, tokens)
        choice_code = read_next_token(5, tokens)
        resp.append(Choice(text=text,
                           story_code=story_code,
                           choice_code=choice_code))
        token = next(tokens, None)
    return token, resp


def get_choices(tokens):
    resp = {}
    token = next(tokens, None)
    while (token is not None) and token.stars > 2:
        key = get_content(3, token)
        token, choices = get_choices_list(tokens)
        resp[key] = choices
    return token, resp


def get_stories(tokens):
    resp = {}
    token = next(tokens, None)
    while (token is not None) and token.stars > 2:
        key = get_content(3, token)
        value = read_next_token(0, tokens)
        token = next(tokens, None)
        resp[key] = value
    return token, resp


def tokens_to_story(tokens):
    token = next(tokens)
    assert token.stars == 1, 'First line should be title'
    title = token.content
    token = next(tokens, None)
    choices = None
    stories = None
    start_story = None
    start_choices = None
    while token is not None:
        if token == Token(stars=2, content='Story'):
            token, stories = get_stories(tokens)
        elif token == Token(stars=2, content='Choices'):
            token, choices = get_choices(tokens)
        elif token == Token(stars=2, content='Start'):
            start_story = read_next_token(3, tokens)
            start_choices = read_next_token(3, tokens)
            token = next(tokens)
        else:
            raise ValueError('Invalid Token: %s' % (token,))
    if (choices is None
        or stories is None
        or start_story is None
        or start_choices is None):
            raise Exception('Story and/or Choice is not provided in file.')

    return Story(title=title,
                 stories=stories,
                 choices=choices,
                 start_story_code=start_story,
                 start_choices_code=start_choices)


def read_content(file_name):
    """Reads story content from org file.

    returns two dictionaries.
    """
    with open(file_name) as f:
        raw_lines = filter(None, (l.strip() for l in f.readlines()))
        lines = list(raw_lines)

    return tokens_to_story(iter_tokens(lines))
