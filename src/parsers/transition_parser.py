from src.exceptions import ValidationError


class TransitionParser:
    def __init__(self, statement):
        self._create_temporary_objects()

        events, left_statement = self._parse_events(statement)
        condition, left_statement = self._parse_condition(left_statement)
        actions, left_statement = self._parse_actions(left_statement)

        for ch in left_statement:
            self._update_counters(ch)

        self._validate_parsed_result()
        self._delete_temporary_objects()

        self.events = events
        self.condition = condition
        self.actions = actions

    def _create_temporary_objects(self):
        self._num_of_open_braces = 0
        self._num_of_open_parentheses = 0
        self._num_of_open_square_brackets = 0
        self._num_of_open_single_quote = 0
        self._num_of_open_double_quote = 0

    def _delete_temporary_objects(self):
        del self._num_of_open_braces
        del self._num_of_open_parentheses
        del self._num_of_open_square_brackets
        del self._num_of_open_single_quote
        del self._num_of_open_double_quote

    def _validate_parsed_result(self):
        if self._num_of_open_braces != 0 or \
           self._num_of_open_parentheses != 0 or \
           self._num_of_open_square_brackets != 0 or \
           self._num_of_open_single_quote != 0 or \
           self._num_of_open_double_quote != 0:
            raise ValidationError()

    def get_transition_items(self):
        return self.events, self.condition, self.actions

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
        statement = statement.strip()

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
        return events.strip(), statement[index:]

    def _parse_condition(self, statement):
        statement = statement.strip()

        index = 0
        condition = ''
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
            condition += ch
        return condition.strip(), statement[index:]

    def _parse_actions(self, statement):
        statement = statement.strip()

        index = 0
        actions = ''
        for ch in statement:
            index += 1
            if ch == '/' and \
                self._num_of_open_braces == 0 and \
                self._num_of_open_parentheses == 0 and \
                self._num_of_open_square_brackets == 0 and \
                self._num_of_open_single_quote == 0 and \
                self._num_of_open_double_quote == 0:
                continue
            self._update_counters(ch)
            actions += ch
        return actions.strip(), statement[index:]


if __name__ == '__main__':
    example = 'EvConfig1() [ i > k ] / Action() { [] }, Action2()'
    parser = TransitionParser(example)
    events, condition, actions = parser.get_transition_items()
    print(events)
    print(actions)
    print(condition)

