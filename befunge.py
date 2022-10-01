from random import choice

def interpret(code):

    def step(element, string_mode):
        new_direction = None
        special_instruction = None

        if string_mode:
            if element == '"':
                string_mode = False
            else:
                stack.append(ord(element))
        else:
            try:
                if type(int(element)) == int:
                    stack.append(int(element))
            except ValueError:
                pass

            match element:
                case '"': string_mode = True
                case '>': new_direction = 'right'
                case 'v': new_direction = 'down'
                case '<': new_direction = 'left'
                case '^': new_direction = 'up'
                case '?': new_direction = choice(['right', 'down', 'left', 'up'])

                case '+' | '-' | '*' | '%' | '/' | '`' | '\\':

                    if len(stack) < 2 and element == '\\':
                        stack.insert(0, 0)

                    a = stack.pop()
                    b = stack.pop()

                    match element:
                        case '+': stack.append(a + b)
                        case '-': stack.append(b - a)
                        case '*': stack.append(b * a)
                        case '%': stack.append(b % a)

                        case '/':
                            if not a == 0: stack.append(b // a)
                            else: stack.append(0)

                        case '`':
                            if b > a: stack.append(1)
                            else: stack.append(0)

                        case '\\':
                            stack.append(a)
                            stack.append(b)

                case '!' | '_' | '|' | '$' | '.' | ',' | ':':
                    try: a = stack.pop()
                    except IndexError: a = 0

                    match element:
                        case '!':
                            if a: stack.append(0)
                            else: stack.append(1)

                        case '_':
                            if a: new_direction = 'left'
                            else: new_direction = 'right'

                        case '|':
                            if a: new_direction = 'up'
                            else: new_direction = 'down'

                        case '$': pass
                        case '.': raw_output.append(a)
                        case ',': raw_output.append(chr(a))
                        case ':': stack.append(a); stack.append(a)

                case '#': special_instruction = 'skip'
                case 'p': special_instruction = 'put'
                case 'g': special_instruction = 'get'
                case '@': special_instruction = 'end'

            return new_direction, special_instruction, string_mode

    stack = []
    raw_output = []
    splitted_code = code.split('\n')
    splitted_into_chars = []
    for row in splitted_code:
        splitted_into_chars.append(list(row))

    current_direction = 'right'
    x_dimension = len(splitted_into_chars[0])
    y_dimension = len(splitted_into_chars)
    current_row = 0
    current_column = 0
    special_instruction = None
    string_mode = False

    while True:
        if not special_instruction == 'skip':
            special_instruction = None
            new_direction, special_instruction, string_mode = step(splitted_into_chars[current_row][current_column], string_mode)
            if new_direction != current_direction and new_direction is not None:
                current_direction = new_direction
        else:
            special_instruction = None

        match current_direction:
            case 'right':
                try: current_column += 1
                except IndexError: current_column = 0

            case 'left':
                try: current_column -= 1
                except IndexError: current_column = (x_dimension - 1)

            case 'down':
                try: current_row += 1
                except IndexError: current_row = 0

            case 'up':
                try: current_row -= 1
                except IndexError: current_row = (y_dimension - 1)

        match special_instruction:
            case 'end': break
            case 'put':
                y = stack.pop()
                x = stack.pop()
                v = stack.pop()
                splitted_into_chars[y][x] = chr(v)
            case 'get':
                y = stack.pop()
                x = stack.pop()
                stack.append(ord(splitted_into_chars[y][x]))

    raw_output = [str(x) for x in raw_output]
    output = ''.join(raw_output)
    return output

# example - interpreter('something with spaces included \n new row)