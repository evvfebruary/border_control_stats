# ToDo: Very raw version, definitely glad to improve this somehow
HASHTAGS_PATTERN = r"#(\w+)"
APPROVED_MARK, DECLINED_MARK = '✅', '❌'
PEOPLE_PATTERN = r'(мч|[мМжЖ][,!-/\s]*\d{2})'
MANS_PATTERN = ['м', 'мч', 'мж', 'мужчина', 'парень']
WOMANS_PATTERN = ['ж', 'Ж']
MALE_GENDER_VALUE = 'm'
FEMALE_GENDER_VALUE = 'f'
GENDER_MAPPING = {**{key: MALE_GENDER_VALUE for key in MANS_PATTERN},
                  **{key: FEMALE_GENDER_VALUE for key in WOMANS_PATTERN}}

# Some tricky variables for reports parsing
REPORTS_SEPARATOR_EXAMPLE = '\n—————————\n'
REPORTS_SEPARATOR_SYMBOL = list(set(REPORTS_SEPARATOR_EXAMPLE))[-1]
MIN_SYMBOL_CNT, MAX_SYMBOL_CNT = 7, 13
REPORTS_SEPARATORS = [cnt * REPORTS_SEPARATOR_SYMBOL for cnt in range(7, 13)]
