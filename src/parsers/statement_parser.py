from exceptions import ValidationError


class StatementParser:
    def __init__(self, statement):
        self._statement = statement

    def parse(self):
        self._num_of_open_braces = 0
        self._num_of_open_parentheses = 0
        self._num_of_open_square_brackets = 0
        self._num_of_open_single_quote = 0
        self._num_of_open_double_quote = 0
        events = ''
        actions = ''
        conditions = ''
        events, left_statement, ch = self._parse_events(self._statement)
        if ch == '/':
            actions, left_statement, ch = self._parse_actions(left_statement)
        if ch == '[':
            conditions, left_statement, ch = self._parse_conditions(left_statement)
        for ch in left_statement:
            self._update_counters(ch)
        if self._num_of_open_braces != 0 or \
            self._num_of_open_parentheses != 0 or \
            self._num_of_open_square_brackets != 0 or \
            self._num_of_open_single_quote != 0 or \
            self._num_of_open_double_quote != 0:
            raise ValidationError()
        return events.strip(), actions.strip(), conditions.strip()

    def _update_counters(self, ch):
        if ch == '(':
            self._num_of_open_braces += 1
        elif ch == ')':
            self._num_of_open_braces -= 1
            if self._num_of_open_braces < 0:
                raise ValidationError()
        elif ch == '{':
            self._num_of_open_parentheses += 1
        elif ch == '}':
            self._num_of_open_parentheses -= 1
            if self._num_of_open_parentheses < 0:
                raise ValidationError()
        elif ch == '[':
            self._num_of_open_square_brackets += 1
        elif ch == ']':
            self._num_of_open_square_brackets -= 1
            if self._num_of_open_square_brackets < 0:
                raise ValidationError()
        elif ch == '\'':
            if self._num_of_open_single_quote == 0:
                self._num_of_open_single_quote += 1
            elif self._num_of_open_single_quote == 1:
                self._num_of_open_single_quote -= 1
        elif ch == '\"':
            if self._num_of_open_double_quote == 0:
                self._num_of_open_double_quote += 1
            elif self._num_of_open_double_quote == 1:
                self._num_of_open_double_quote -= 1

    def _parse_events(self, statement):
        index = 0
        events = ''
        for ch in statement:
            index += 1
            if ch == '/' and \
                self._num_of_open_braces == 0 and \
                self._num_of_open_parentheses == 0 and \
                self._num_of_open_square_brackets == 0 and \
                self._num_of_open_single_quote == 0 and \
                self._num_of_open_double_quote == 0:
                break
            if ch == '[' and \
                self._num_of_open_braces == 0 and \
                self._num_of_open_parentheses == 0 and \
                self._num_of_open_square_brackets == 0 and \
                self._num_of_open_single_quote == 0 and \
                self._num_of_open_double_quote == 0:
                break
            self._update_counters(ch)
            events += ch
        return events, statement[index:], ch

    def _parse_actions(self, statement):
        index = 0
        actions = ''
        for ch in statement:
            index += 1
            if ch == '[' and \
                self._num_of_open_braces == 0 and \
                self._num_of_open_parentheses == 0 and \
                self._num_of_open_square_brackets == 0 and \
                self._num_of_open_single_quote == 0 and \
                self._num_of_open_double_quote == 0:
                break
            self._update_counters(ch)
            actions += ch
        return actions, statement[index:], ch

    def _parse_conditions(self, statement):
        index = 0
        conditions = ''
        for ch in statement:
            index += 1
            if ch == ']' and \
                self._num_of_open_braces == 0 and \
                self._num_of_open_parentheses == 0 and \
                self._num_of_open_square_brackets == 0 and \
                self._num_of_open_single_quote == 0 and \
                self._num_of_open_double_quote == 0:
                break
            self._update_counters(ch)
            conditions += ch
        return conditions, statement[index:], ch


if __name__ == '__main__':
    example = 'EvConfig1() / Action() { [] }, Action2() [ i > k ]]'
    parser = StatementParser(example)
    events, actions, condition = parser.parse()
    print(events)
    print(actions)
    print(condition)

